from django.db import models


class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    carga_horaria = models.PositiveIntegerField(help_text="Em horas")
    nota_minima = models.DecimalField(max_digits=4, decimal_places=2, default=6.0)
    pre_requisitos = models.ManyToManyField(
        "self",
        through="PreRequisito",
        symmetrical=False,
        related_name="requerido_por",
        blank=True,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo


class PreRequisito(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="requisitos")
    curso_requerido = models.ForeignKey(
        Curso, on_delete=models.CASCADE, related_name="exigido_por"
    )

    class Meta:
        verbose_name = "Pré-requisito"
        verbose_name_plural = "Pré-requisitos"
        unique_together = ("curso", "curso_requerido")

    def __str__(self):
        return f"{self.curso_requerido} → {self.curso}"


class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="modulos")
    titulo = models.CharField(max_length=200)
    ordem = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ["curso", "ordem"]
        unique_together = ("curso", "ordem")

    def __str__(self):
        return f"{self.curso} — Módulo {self.ordem}: {self.titulo}"


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
