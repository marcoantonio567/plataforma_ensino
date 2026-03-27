import uuid
from django.db import models
from students.models import Aluno, Matricula
from courses.models import Curso


class IncidenteIntegridade(models.Model):
    class Gravidade(models.TextChoices):
        LEVE = "LEVE", "Leve"
        GRAVE = "GRAVE", "Grave"

    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        EM_AVALIACAO = "EM_AVALIACAO", "Em Avaliação pelo Comitê"
        SUSPENSAO = "SUSPENSAO", "Suspensão"
        REVOGACAO = "REVOGACAO", "Revogação"
        ENCERRADO = "ENCERRADO", "Encerrado sem penalidade"

    matricula = models.ForeignKey(
        Matricula, on_delete=models.CASCADE, related_name="incidentes"
    )
    descricao = models.TextField()
    gravidade = models.CharField(max_length=5, choices=Gravidade.choices)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDENTE)
    registrado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Incidente de Integridade"
        verbose_name_plural = "Incidentes de Integridade"

    def __str__(self):
        return f"Incidente [{self.get_gravidade_display()}] — {self.matricula.aluno}"


class Certificado(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="certificados")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="certificados")
    codigo_verificacao = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    data_emissao = models.DateField(auto_now_add=True)
    validade = models.DateField(
        null=True, blank=True, help_text="Deixar em branco para certificado vitalício"
    )

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"
        unique_together = ("aluno", "curso")

    def __str__(self):
        return f"Certificado: {self.aluno} — {self.curso}"

    @property
    def e_vitalicio(self):
        return self.validade is None
