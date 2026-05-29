from django.db import models


class StatusCertificado(models.TextChoices):
    EMITIDO = "EMITIDO", "Emitido"
    SUSPENSO = "SUSPENSO", "Suspenso"
    REVOGADO = "REVOGADO", "Revogado"


class TipoIncidente(models.TextChoices):
    COLA = "COLA", "Cola"
    PLAGIO = "PLAGIO", "Plágio"
    FRAUDE = "FRAUDE", "Fraude"
    OUTROS = "OUTROS", "Outros"


class IncidenteIntegridade(models.Model):
    matricula = models.ForeignKey(
        "students.Matricula", on_delete=models.CASCADE, related_name="incidentes"
    )
    tipo = models.CharField(max_length=10, choices=TipoIncidente.choices)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Incidente de Integridade"
        verbose_name_plural = "Incidentes de Integridade"

    def __str__(self):
        return f"Incidente [{self.get_tipo_display()}] — {self.matricula}"


class Certificado(models.Model):
    matricula = models.OneToOneField(
        "students.Matricula", on_delete=models.CASCADE, related_name="certificado"
    )
    data_emissao = models.DateField(auto_now_add=True)
    validade = models.DateField(
        null=True, blank=True, help_text="Deixar em branco para certificado vitalício"
    )
    status = models.CharField(
        max_length=10, choices=StatusCertificado.choices, default=StatusCertificado.EMITIDO
    )

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"

    def __str__(self):
        return f"Certificado — {self.matricula}"

    def revogar(self):
        self.status = StatusCertificado.REVOGADO
        self.save()

    def suspender(self):
        self.status = StatusCertificado.SUSPENSO
        self.save()

    def renovar(self, nova_validade=None):
        self.status = StatusCertificado.EMITIDO
        if nova_validade:
            self.validade = nova_validade
        self.save()
