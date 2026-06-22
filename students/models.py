from django.db import models
from django.contrib.auth.models import User

from students.domain.exceptions import (
    InvalidEnrollmentTransition,
    InvalidRequestTransition,
)
from students.domain.value_objects import (
    CargaHorariaCumprida,
    InvalidStudentValue,
    MediaFinal,
    NumeroMatricula,
    PercentualProgresso,
)


class Aluno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="aluno")
    numero_matricula = models.CharField(max_length=20, unique=True)
    data_ingresso = models.DateField()

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username

    def _validate_value_objects(self):
        self.numero_matricula = str(NumeroMatricula(self.numero_matricula))

    def clean(self):
        super().clean()
        self._validate_value_objects()

    def save(self, *args, **kwargs):
        self._validate_value_objects()
        return super().save(*args, **kwargs)

    def matricular(self, curso):
        from students.domain.factories import MatriculaFactory

        matricula = MatriculaFactory.criar(self, curso)
        matricula.save()
        return matricula

    def trancar_matricula(self, matricula):
        self._ensure_matricula_belongs_to_student(matricula)
        matricula.trancar()
        matricula.save()

    def solicitar_aproveitamento(self, matricula, modulo, justificativa=""):
        self._ensure_matricula_belongs_to_student(matricula)
        solicitacao = matricula.solicitar_aproveitamento(modulo, justificativa=justificativa)
        solicitacao.save()
        return solicitacao

    def solicitar_segunda_chamada(self, matricula, avaliacao, justificativa=""):
        self._ensure_matricula_belongs_to_student(matricula)
        solicitacao = matricula.solicitar_segunda_chamada(avaliacao, justificativa=justificativa)
        solicitacao.save()
        return solicitacao

    def solicitar_revisao_nota(self, matricula, avaliacao, justificativa=""):
        self._ensure_matricula_belongs_to_student(matricula)
        solicitacao = matricula.solicitar_revisao_nota(avaliacao, justificativa=justificativa)
        solicitacao.save()
        return solicitacao

    def _ensure_matricula_belongs_to_student(self, matricula):
        if matricula.aluno_id != self.pk:
            raise ValueError("A matricula informada nao pertence a este aluno.")


class Matricula(models.Model):
    class Status(models.TextChoices):
        ATIVA = "ATIVA", "Ativa"
        TRANCADA = "TRANCADA", "Trancada"
        CONCLUIDA = "CONCLUIDA", "Concluída"
        CANCELADA = "CANCELADA", "Cancelada"

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="matriculas")
    curso = models.ForeignKey(
        "courses.Curso", on_delete=models.CASCADE, related_name="matriculas"
    )
    regra_curso = models.ForeignKey(
        "courses.RegraCurso",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matriculas",
    )
    data_matricula = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ATIVA)
    media_final = models.FloatField(null=True, blank=True)
    progresso = models.FloatField(default=0.0, help_text="Percentual de conclusão (0–100)")
    carga_horaria_cumprida = models.PositiveIntegerField(
        default=0, help_text="Em horas"
    )

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        unique_together = ("aluno", "curso")

    def __str__(self):
        return f"{self.aluno} — {self.curso} ({self.get_status_display()})"


    def _ensure_status(self, allowed_statuses, operation):
        if self.status not in allowed_statuses:
            allowed = ", ".join(allowed_statuses)
            raise InvalidEnrollmentTransition(
                f"Nao e possivel {operation} uma matricula com status {self.status}. "
                f"Status permitidos: {allowed}."
            )

    def _validate_status_transition(self):
        if self.pk is None:
            return

        previous = type(self).objects.only("status").get(pk=self.pk)
        if previous.status == self.status:
            return

        allowed_transitions = {
            self.Status.ATIVA: {
                self.Status.TRANCADA,
                self.Status.CANCELADA,
                self.Status.CONCLUIDA,
            },
            self.Status.TRANCADA: {self.Status.ATIVA, self.Status.CANCELADA},
            self.Status.CANCELADA: {self.Status.ATIVA},
            self.Status.CONCLUIDA: set(),
        }
        if self.status not in allowed_transitions[previous.status]:
            raise InvalidEnrollmentTransition(
                f"Transicao de matricula invalida: {previous.status} -> {self.status}."
            )

    def _validate_course_rule(self):
        if self.regra_curso_id is None:
            raise InvalidEnrollmentTransition(
                "A matricula deve registrar a regra de curso vigente."
            )

        rule_course_id = getattr(self.regra_curso, "curso_id", None)
        if rule_course_id is not None and self.curso_id is not None:
            if rule_course_id != self.curso_id:
                raise InvalidEnrollmentTransition(
                    "A regra de curso da matricula deve pertencer ao mesmo curso."
                )

    def _validate_value_objects(self):
        if self.media_final is not None:
            self.media_final = float(MediaFinal(self.media_final))
        self.progresso = float(PercentualProgresso(self.progresso))
        self.carga_horaria_cumprida = int(CargaHorariaCumprida(self.carga_horaria_cumprida))

    def clean(self):
        super().clean()
        self._validate_value_objects()
        self._validate_course_rule()
        self._validate_status_transition()

    def save(self, *args, **kwargs):
        self._validate_value_objects()
        self._validate_course_rule()
        self._validate_status_transition()
        return super().save(*args, **kwargs)

    def cancelar(self):
        self._ensure_status([self.Status.ATIVA, self.Status.TRANCADA], "cancelar")
        self.status = self.Status.CANCELADA
        return self

    def trancar(self):
        self._ensure_status([self.Status.ATIVA], "trancar")
        self.status = self.Status.TRANCADA
        return self

    def reativar(self):
        self._ensure_status([self.Status.CANCELADA, self.Status.TRANCADA], "reativar")
        self.status = self.Status.ATIVA
        return self

    def concluir(self, *, media_final, carga_horaria_cumprida=None):
        self._ensure_status([self.Status.ATIVA], "concluir")
        if media_final is None:
            raise InvalidEnrollmentTransition("A media final e obrigatoria para concluir.")

        try:
            self.media_final = float(MediaFinal(media_final))
            if carga_horaria_cumprida is not None:
                self.carga_horaria_cumprida = int(CargaHorariaCumprida(carga_horaria_cumprida))
            self.progresso = float(PercentualProgresso(100))
        except InvalidStudentValue as exc:
            raise InvalidEnrollmentTransition(str(exc)) from exc
        self.status = self.Status.CONCLUIDA
        return self

    def atualizar_progresso(self, percentual, *, carga_horaria_cumprida=None):
        self._ensure_status([self.Status.ATIVA], "atualizar o progresso de")
        try:
            percentual = PercentualProgresso(percentual)
            carga_horaria = (
                None
                if carga_horaria_cumprida is None
                else CargaHorariaCumprida(carga_horaria_cumprida)
            )
        except InvalidStudentValue as exc:
            raise InvalidEnrollmentTransition(str(exc)) from exc

        self.progresso = float(percentual)
        if carga_horaria is not None:
            self.carga_horaria_cumprida = int(carga_horaria)
        return self

    def solicitar_aproveitamento(self, modulo, justificativa=""):
        self._ensure_status([self.Status.ATIVA], "solicitar aproveitamento para")
        self._ensure_modulo_belongs_to_course(modulo)
        return Aproveitamento(matricula=self, modulo=modulo, justificativa=justificativa)

    def solicitar_segunda_chamada(self, avaliacao, justificativa=""):
        self._ensure_status([self.Status.ATIVA], "solicitar segunda chamada para")
        self._ensure_avaliacao_belongs_to_course(avaliacao)
        return SegundaChamada(
            matricula=self,
            avaliacao=avaliacao,
            justificativa=justificativa,
        )

    def solicitar_revisao_nota(self, avaliacao, justificativa=""):
        self._ensure_status([self.Status.ATIVA], "solicitar revisao de nota para")
        self._ensure_avaliacao_belongs_to_course(avaliacao)
        return RevisaoNota(
            matricula=self,
            avaliacao=avaliacao,
            justificativa=justificativa,
        )

    def registrar_equivalencia(
        self,
        *,
        instituicao_origem,
        disciplina_origem,
        disciplina_destino,
    ):
        self._ensure_status([self.Status.ATIVA], "registrar equivalencia para")
        return Equivalencia(
            matricula=self,
            instituicao_origem=instituicao_origem,
            disciplina_origem=disciplina_origem,
            disciplina_destino=disciplina_destino,
        )

    def registrar_incidente_integridade(self, *, tipo, gravidade):
        from certifications.models import IncidenteIntegridade

        return IncidenteIntegridade(
            matricula=self,
            tipo=tipo,
            gravidade=gravidade,
        )

    def _ensure_modulo_belongs_to_course(self, modulo):
        if modulo.curso_id != self.curso_id:
            raise InvalidEnrollmentTransition(
                "O modulo informado nao pertence ao curso da matricula."
            )

    def _ensure_avaliacao_belongs_to_course(self, avaliacao):
        if avaliacao.modulo.curso_id != self.curso_id:
            raise InvalidEnrollmentTransition(
                "A avaliacao informada nao pertence ao curso da matricula."
            )

    def emitir_certificado(self, validade=None):
        from certifications.models import Certificado

        return Certificado(matricula=self, validade=validade)


class Solicitacao(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        EM_ANALISE = "EM_ANALISE", "Em Análise"
        APROVADA = "APROVADA", "Aprovada"
        REJEITADA = "REJEITADA", "Rejeitada"

    matricula = models.ForeignKey(
        Matricula, on_delete=models.CASCADE, related_name="solicitacoes"
    )
    data = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=11, choices=Status.choices, default=Status.PENDENTE
    )
    justificativa = models.TextField()

    class Meta:
        verbose_name = "Solicitação"
        verbose_name_plural = "Solicitações"

    def __str__(self):
        return f"Solicitação #{self.pk} ({self.get_status_display()})"


    def iniciar_analise(self):
        if self.status != self.Status.PENDENTE:
            raise InvalidRequestTransition(
                "Somente solicitacoes pendentes podem entrar em analise."
            )
        self.status = self.Status.EM_ANALISE
        return self

    def aprovar(self):
        if self.status not in [self.Status.PENDENTE, self.Status.EM_ANALISE]:
            raise InvalidRequestTransition(
                "Somente solicitacoes pendentes ou em analise podem ser aprovadas."
            )
        self.status = self.Status.APROVADA
        return self

    def rejeitar(self):
        if self.status not in [self.Status.PENDENTE, self.Status.EM_ANALISE]:
            raise InvalidRequestTransition(
                "Somente solicitacoes pendentes ou em analise podem ser rejeitadas."
            )
        self.status = self.Status.REJEITADA
        return self


class RevisaoNota(Solicitacao):
    avaliacao = models.ForeignKey(
        "assessments.Avaliacao", on_delete=models.CASCADE, related_name="revisoes"
    )

    class Meta:
        verbose_name = "Revisão de Nota"
        verbose_name_plural = "Revisões de Nota"

    def __str__(self):
        return f"Revisão de Nota: {self.matricula.aluno} — {self.avaliacao}"


class SegundaChamada(Solicitacao):
    avaliacao = models.ForeignKey(
        "assessments.Avaliacao", on_delete=models.CASCADE, related_name="segundas_chamadas"
    )

    class Meta:
        verbose_name = "Segunda Chamada"
        verbose_name_plural = "Segundas Chamadas"

    def __str__(self):
        return f"2ª Chamada: {self.matricula.aluno} — {self.avaliacao}"


class Aproveitamento(Solicitacao):
    modulo = models.ForeignKey(
        "courses.Modulo", on_delete=models.CASCADE, related_name="aproveitamentos"
    )

    class Meta:
        verbose_name = "Aproveitamento"
        verbose_name_plural = "Aproveitamentos"

    def __str__(self):
        return f"Aproveitamento: {self.matricula.aluno} — {self.modulo}"


class Equivalencia(models.Model):
    matricula = models.ForeignKey(
        Matricula, on_delete=models.CASCADE, related_name="equivalencias"
    )
    instituicao_origem = models.CharField(max_length=200)
    disciplina_origem = models.CharField(max_length=200)
    disciplina_destino = models.CharField(max_length=200)
    aprovado = models.BooleanField(default=False)

    def aprovar(self):
        self.aprovado = True
        return self

    def reprovar(self):
        self.aprovado = False
        return self

    class Meta:
        verbose_name = "Equivalência"
        verbose_name_plural = "Equivalências"

    def __str__(self):
        return f"{self.disciplina_origem} → {self.disciplina_destino} ({self.matricula.aluno})"
