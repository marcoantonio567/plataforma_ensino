from django.contrib import admin
from .models import Avaliacao, TrabalhoPratico


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo", "modulo", "peso", "nota_maxima")
    list_filter = ("tipo",)


@admin.register(TrabalhoPratico)
class TrabalhoPraticoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "curso", "prazo", "nota_maxima")
