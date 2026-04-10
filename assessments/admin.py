from django.contrib import admin
from .models import (
    Avaliacao,
    AvaliacaoObjetiva,
    AvaliacaoDiscursiva,
    ProjetoPratico,
    ProvaMonitorada,
    AvaliacaoRealizada,
)


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("tipo", "modulo", "peso")
    list_filter = ("tipo",)


@admin.register(AvaliacaoObjetiva)
class AvaliacaoObjetivaAdmin(admin.ModelAdmin):
    list_display = ("modulo", "peso")


@admin.register(AvaliacaoDiscursiva)
class AvaliacaoDiscursivaAdmin(admin.ModelAdmin):
    list_display = ("modulo", "peso")


@admin.register(ProjetoPratico)
class ProjetoPraticoAdmin(admin.ModelAdmin):
    list_display = ("modulo", "peso", "repositorio")


@admin.register(ProvaMonitorada)
class ProvaMonitoradaAdmin(admin.ModelAdmin):
    list_display = ("modulo", "peso", "monitoramento_ativo")


@admin.register(AvaliacaoRealizada)
class AvaliacaoRealizadaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "avaliacao", "nota", "data")
    list_filter = ("data",)
