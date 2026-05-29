from django.db import models


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


class RegraCurso(models.Model):
    media_minima = models.FloatField(default=6.0)
    carga_horaria_minima = models.PositiveIntegerField(default=0, help_text="Em horas")
    exige_projeto_final = models.BooleanField(default=False)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Regra de Curso"
        verbose_name_plural = "Regras de Curso"

    def __str__(self):
        return f"Regra (início: {self.data_inicio})"


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


class PreRequisito(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="pre_requisitos")
    tipo = models.CharField(max_length=10, choices=TipoPreRequisito.choices)
    referencia_id = models.PositiveIntegerField(help_text="ID do Curso ou Módulo exigido")

    class Meta:
        verbose_name = "Pré-requisito"
        verbose_name_plural = "Pré-requisitos"

    def __str__(self):
        return f"{self.get_tipo_display()} #{self.referencia_id} → {self.curso}"
