from django.db import models
from django.utils import timezone

from courses.domain.policies import current_course_rule
from courses.domain.value_objects import (
    CargaHoraria,
    CargaHorariaMinima,
    DuracaoAula,
    MediaMinima,
    Ordem,
)


class TipoPreRequisito(models.TextChoices):
    CURSO = "CURSO", "Curso"
    MODULO = "MODULO", "Módulo"


class Curso(models.Model):
    nome = models.CharField(max_length=200)
    carga_horaria = models.PositiveIntegerField(help_text="Em horas")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    def _validate_value_objects(self):
        self.carga_horaria = int(CargaHoraria(self.carga_horaria))

    def clean(self):
        super().clean()
        self._validate_value_objects()

    def save(self, *args, **kwargs):
        self._validate_value_objects()
        return super().save(*args, **kwargs)

    def regra_vigente(self, data=None):
        data = data or timezone.localdate()
        return current_course_rule(self.regras.all(), date=data)

    def adicionar_modulo(self, *, nome, ordem):
        if not nome or not nome.strip():
            raise ValueError("O nome do modulo e obrigatorio.")
        return Modulo(curso=self, nome=nome.strip(), ordem=int(Ordem(ordem)))

    def adicionar_aula(self, modulo, *, titulo, duracao, conteudo="", ordem):
        self._ensure_modulo_belongs_to_course(modulo)
        return modulo._adicionar_aula(
            titulo=titulo,
            duracao=duracao,
            conteudo=conteudo,
            ordem=ordem,
        )

    def remover_modulo(self, modulo):
        self._ensure_modulo_belongs_to_course(modulo)
        modulo.delete()

    def remover_aula(self, aula):
        self._ensure_modulo_belongs_to_course(aula.modulo)
        aula.delete()

    def _ensure_modulo_belongs_to_course(self, modulo):
        if modulo.curso_id != self.pk:
            raise ValueError("O modulo informado nao pertence a este curso.")


class RegraCurso(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="regras")
    media_minima = models.FloatField(default=6.0)
    carga_horaria_minima = models.PositiveIntegerField(default=0, help_text="Em horas")
    exige_projeto_final = models.BooleanField(default=False)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Regra de Curso"
        verbose_name_plural = "Regras de Curso"
        ordering = ["curso", "-data_inicio"]

    def __str__(self):
        return f"Regra (início: {self.data_inicio})"


    def _validate_value_objects(self):
        self.media_minima = float(MediaMinima(self.media_minima))
        self.carga_horaria_minima = int(CargaHorariaMinima(self.carga_horaria_minima))

    def clean(self):
        super().clean()
        self._validate_value_objects()
        self.validar_periodo()

    def save(self, *args, **kwargs):
        self._validate_value_objects()
        self.validar_periodo()
        return super().save(*args, **kwargs)

    def esta_vigente(self, data=None):
        data = data or timezone.localdate()
        return self.data_inicio <= data and (
            self.data_fim is None or self.data_fim >= data
        )

    def validar_periodo(self):
        if self.data_fim is not None and self.data_fim < self.data_inicio:
            raise ValueError("A data final da regra nao pode ser anterior ao inicio.")
        return self

    def exige_projeto(self):
        return self.exige_projeto_final


class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="modulos")
    nome = models.CharField(max_length=200)
    ordem = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ["curso", "ordem"]
        unique_together = ("curso", "ordem")

    def __str__(self):
        return f"{self.curso} — Módulo {self.ordem}: {self.nome}"


    def _validate_value_objects(self):
        self.ordem = int(Ordem(self.ordem))

    def clean(self):
        super().clean()
        self._validate_value_objects()

    def save(self, *args, **kwargs):
        self._validate_value_objects()
        return super().save(*args, **kwargs)

    def _adicionar_aula(self, *, titulo, duracao, conteudo="", ordem):
        if not titulo or not titulo.strip():
            raise ValueError("O titulo da aula e obrigatorio.")
        duracao = DuracaoAula(duracao)
        ordem = Ordem(ordem)
        return Aula(
            modulo=self,
            titulo=titulo.strip(),
            duracao=int(duracao),
            conteudo=conteudo,
            ordem=int(ordem),
        )

    def adicionar_aula(self, *, titulo, duracao, conteudo="", ordem):
        return self._adicionar_aula(
            titulo=titulo,
            duracao=duracao,
            conteudo=conteudo,
            ordem=ordem,
        )

    def reordenar(self, nova_ordem):
        self.ordem = int(Ordem(nova_ordem))
        return self


class Aula(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name="aulas")
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField(blank=True)
    duracao = models.PositiveIntegerField(help_text="Em minutos")
    ordem = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"
        ordering = ["modulo", "ordem"]
        unique_together = ("modulo", "ordem")

    def __str__(self):
        return f"{self.modulo} — Aula {self.ordem}: {self.titulo}"


    def _validate_value_objects(self):
        self.duracao = int(DuracaoAula(self.duracao))
        self.ordem = int(Ordem(self.ordem))

    def clean(self):
        super().clean()
        self._validate_value_objects()

    def save(self, *args, **kwargs):
        self._validate_value_objects()
        return super().save(*args, **kwargs)

    def reordenar(self, nova_ordem):
        self.ordem = int(Ordem(nova_ordem))
        return self

    def atualizar_conteudo(self, *, titulo=None, conteudo=None, duracao=None):
        if titulo is not None:
            if not titulo.strip():
                raise ValueError("O titulo da aula e obrigatorio.")
            self.titulo = titulo.strip()
        if conteudo is not None:
            self.conteudo = conteudo
        if duracao is not None:
            self.duracao = int(DuracaoAula(duracao))
        return self


class PreRequisito(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="pre_requisitos")
    tipo = models.CharField(max_length=10, choices=TipoPreRequisito.choices)
    referencia_id = models.PositiveIntegerField(help_text="ID do Curso ou Módulo exigido")

    def referencia_curso(self):
        return self.tipo == TipoPreRequisito.CURSO

    def referencia_modulo(self):
        return self.tipo == TipoPreRequisito.MODULO

    class Meta:
        verbose_name = "Pré-requisito"
        verbose_name_plural = "Pré-requisitos"

    def __str__(self):
        return f"{self.get_tipo_display()} #{self.referencia_id} → {self.curso}"
