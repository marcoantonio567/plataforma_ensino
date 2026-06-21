from django.db import models
from django.utils import timezone

from courses.domain.policies import current_course_rule


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

    def regra_vigente(self, data=None):
        data = data or timezone.localdate()
        return current_course_rule(self.regras.all(), date=data)

    def adicionar_modulo(self, *, nome, ordem):
        if not nome or not nome.strip():
            raise ValueError("O nome do modulo e obrigatorio.")
        if ordem < 1:
            raise ValueError("A ordem do modulo deve ser maior que zero.")
        return Modulo(curso=self, nome=nome.strip(), ordem=ordem)


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


    def adicionar_aula(self, *, titulo, duracao, conteudo="", ordem):
        if not titulo or not titulo.strip():
            raise ValueError("O titulo da aula e obrigatorio.")
        if duracao <= 0:
            raise ValueError("A duracao da aula deve ser maior que zero.")
        if ordem < 1:
            raise ValueError("A ordem da aula deve ser maior que zero.")
        return Aula(
            modulo=self,
            titulo=titulo.strip(),
            duracao=duracao,
            conteudo=conteudo,
            ordem=ordem,
        )

    def reordenar(self, nova_ordem):
        if nova_ordem < 1:
            raise ValueError("A ordem do modulo deve ser maior que zero.")
        self.ordem = nova_ordem
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


    def reordenar(self, nova_ordem):
        if nova_ordem < 1:
            raise ValueError("A ordem da aula deve ser maior que zero.")
        self.ordem = nova_ordem
        return self

    def atualizar_conteudo(self, *, titulo=None, conteudo=None, duracao=None):
        if titulo is not None:
            if not titulo.strip():
                raise ValueError("O titulo da aula e obrigatorio.")
            self.titulo = titulo.strip()
        if conteudo is not None:
            self.conteudo = conteudo
        if duracao is not None:
            if duracao <= 0:
                raise ValueError("A duracao da aula deve ser maior que zero.")
            self.duracao = duracao
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
