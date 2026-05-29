from django.contrib import admin
from .models import (
    Aluno,
    Matricula,
    Solicitacao,
    RevisaoNota,
    SegundaChamada,
    Aproveitamento,
    Equivalencia,
)


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "numero_matricula", "data_ingresso")


class EquivalenciaInline(admin.TabularInline):
    model = Equivalencia
    extra = 0


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "curso", "status", "data_matricula", "progresso", "media_final")
    list_filter = ("status",)
    inlines = [EquivalenciaInline]


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "matricula", "status", "data")
    list_filter = ("status",)


@admin.register(RevisaoNota)
class RevisaoNotaAdmin(admin.ModelAdmin):
    list_display = ("matricula", "avaliacao", "status", "data")
    list_filter = ("status",)


@admin.register(SegundaChamada)
class SegundaChamadaAdmin(admin.ModelAdmin):
    list_display = ("matricula", "avaliacao", "status", "data")
    list_filter = ("status",)


@admin.register(Aproveitamento)
class AproveitamentoAdmin(admin.ModelAdmin):
    list_display = ("matricula", "modulo", "status", "data")
    list_filter = ("status",)


@admin.register(Equivalencia)
class EquivalenciaAdmin(admin.ModelAdmin):
    list_display = ("matricula", "disciplina_origem", "disciplina_destino", "aprovado")
    list_filter = ("aprovado",)
