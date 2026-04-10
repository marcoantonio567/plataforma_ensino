from django.db import models
from django.contrib.auth.models import User


class Aluno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="aluno")
    numero_matricula = models.CharField(max_length=20, unique=True)
    data_ingresso = models.DateField()

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username

    def matricular(self, curso):
        regra = getattr(curso, "regra", None)
        return Matricula.objects.create(aluno=self, curso=curso, regra_curso=regra)

    def trancar_matricula(self, matricula):
        matricula.status = Matricula.Status.TRANCADA
        matricula.save()

    def solicitar_aproveitamento(self, matricula, modulo, justificativa=""):
        return Aproveitamento.objects.create(
            matricula=matricula, modulo=modulo, justificativa=justificativa
        )

    def solicitar_segunda_chamada(self, matricula, avaliacao, justificativa=""):
        return SegundaChamada.objects.create(
            matricula=matricula, avaliacao=avaliacao, justificativa=justificativa
        )

    def solicitar_revisao_nota(self, matricula, avaliacao, justificativa=""):
        return RevisaoNota.objects.create(
            matricula=matricula, avaliacao=avaliacao, justificativa=justificativa
        )


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

    class Meta:
        verbose_name = "Equivalência"
        verbose_name_plural = "Equivalências"

    def __str__(self):
        return f"{self.disciplina_origem} → {self.disciplina_destino} ({self.matricula.aluno})"
