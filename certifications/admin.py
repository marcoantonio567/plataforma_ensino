from django.contrib import admin
from .models import Certificado, IncidenteIntegridade


@admin.register(IncidenteIntegridade)
class IncidenteIntegridadeAdmin(admin.ModelAdmin):
    list_display = ("matricula", "gravidade", "status", "registrado_em")
    list_filter = ("gravidade", "status")


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ("aluno", "curso", "data_emissao", "validade", "e_vitalicio")
    readonly_fields = ("codigo_verificacao",)
