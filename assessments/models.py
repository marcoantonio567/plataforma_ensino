from django.db import models
from courses.models import Modulo, Curso


class Avaliacao(models.Model):
    class Tipo(models.TextChoices):
        OBJETIVA = "OBJETIVA", "Objetiva"
        DISCURSIVA = "DISCURSIVA", "Discursiva"
        PROJETO_PRATICO = "PROJETO_PRATICO", "Projeto Prático"
        PROVA_MONITORADA = "PROVA_MONITORADA", "Prova com Monitoramento Remoto"

    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name="avaliacoes")
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    peso = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    nota_maxima = models.DecimalField(max_digits=4, decimal_places=2, default=10.0)

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.titulo}"


class TrabalhoPratico(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="trabalhos_praticos")
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    prazo = models.DateField()
    nota_maxima = models.DecimalField(max_digits=4, decimal_places=2, default=10.0)

    class Meta:
        verbose_name = "Trabalho Prático"
        verbose_name_plural = "Trabalhos Práticos"

    def __str__(self):
        return f"{self.titulo} ({self.curso})"
