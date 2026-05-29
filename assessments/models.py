from django.db import models


class Avaliacao(models.Model):
    class Tipo(models.TextChoices):
        OBJETIVA = "OBJETIVA", "Objetiva"
        DISCURSIVA = "DISCURSIVA", "Discursiva"
        PROJETO_PRATICO = "PROJETO_PRATICO", "Projeto Prático"
        PROVA_MONITORADA = "PROVA_MONITORADA", "Prova com Monitoramento Remoto"

    modulo = models.ForeignKey(
        "courses.Modulo", on_delete=models.CASCADE, related_name="avaliacoes"
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    peso = models.FloatField(default=1.0)

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def __str__(self):
        return f"[{self.get_tipo_display()}] — {self.modulo}"


class AvaliacaoObjetiva(Avaliacao):
    questoes = models.JSONField(default=list, help_text="Lista de questões objetivas")

    class Meta:
        verbose_name = "Avaliação Objetiva"
        verbose_name_plural = "Avaliações Objetivas"


class AvaliacaoDiscursiva(Avaliacao):
    descricao = models.TextField()

    class Meta:
        verbose_name = "Avaliação Discursiva"
        verbose_name_plural = "Avaliações Discursivas"


class ProjetoPratico(Avaliacao):
    repositorio = models.URLField(blank=True)

    class Meta:
        verbose_name = "Projeto Prático"
        verbose_name_plural = "Projetos Práticos"


class ProvaMonitorada(Avaliacao):
    monitoramento_ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Prova Monitorada"
        verbose_name_plural = "Provas Monitoradas"


class AvaliacaoRealizada(models.Model):
    aluno = models.ForeignKey(
        "students.Aluno", on_delete=models.CASCADE, related_name="avaliacoes_realizadas"
    )
    avaliacao = models.ForeignKey(
        Avaliacao, on_delete=models.CASCADE, related_name="realizacoes"
    )
    nota = models.FloatField()
    data = models.DateField()

    class Meta:
        verbose_name = "Avaliação Realizada"
        verbose_name_plural = "Avaliações Realizadas"
        unique_together = ("aluno", "avaliacao")

    def __str__(self):
        return f"{self.aluno} — {self.avaliacao}: {self.nota}"
