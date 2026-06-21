from django.db import models


class StatusCertificado(models.TextChoices):
    EMITIDO = "EMITIDO", "Emitido"
    SUSPENSO = "SUSPENSO", "Suspenso"
    REVOGADO = "REVOGADO", "Revogado"


class TipoIncidente(models.TextChoices):
    COLA = "COLA", "Cola"
    PLAGIO = "PLAGIO", "Plagio"
    FRAUDE = "FRAUDE", "Fraude"
    OUTROS = "OUTROS", "Outros"


class GravidadeIncidente(models.TextChoices):
    BAIXA = "BAIXA", "Baixa"
    MEDIA = "MEDIA", "Media"
    GRAVE = "GRAVE", "Grave"


class IncidenteIntegridade(models.Model):
    matricula = models.ForeignKey(
        "students.Matricula", on_delete=models.CASCADE, related_name="incidentes"
    )
    tipo = models.CharField(max_length=10, choices=TipoIncidente.choices)
    gravidade = models.CharField(
        max_length=10,
        choices=GravidadeIncidente.choices,
        default=GravidadeIncidente.MEDIA,
    )
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Incidente de Integridade"
        verbose_name_plural = "Incidentes de Integridade"

    def __str__(self):
        return f"Incidente [{self.get_tipo_display()}] - {self.matricula}"


class Certificado(models.Model):
    matricula = models.OneToOneField(
        "students.Matricula", on_delete=models.CASCADE, related_name="certificado"
    )
    data_emissao = models.DateField(auto_now_add=True)
    validade = models.DateField(
        null=True, blank=True, help_text="Deixar em branco para certificado vitalicio"
    )
    status = models.CharField(
        max_length=10, choices=StatusCertificado.choices, default=StatusCertificado.EMITIDO
    )

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"

    def __str__(self):
        return f"Certificado - {self.matricula}"

    def revogar(self):
        from certifications.application.services import revoke

        return revoke(self)

    def suspender(self):
        from certifications.application.services import suspend

        return suspend(self)

    def renovar(self, nova_validade=None):
        from certifications.application.services import renew

        return renew(self, nova_validade)
