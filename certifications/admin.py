from django.contrib import admin
from .models import Certificado, IncidenteIntegridade


@admin.register(IncidenteIntegridade)
class IncidenteIntegridadeAdmin(admin.ModelAdmin):
    list_display = ("matricula", "tipo", "gravidade", "data")
    list_filter = ("tipo", "gravidade")


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ("matricula", "data_emissao", "validade", "status")
    list_filter = ("status",)
