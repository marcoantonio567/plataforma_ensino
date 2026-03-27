from django.contrib import admin
from .models import Aluno, Matricula, Aproveitamento, SegundaChamada, RevisaoNota


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "cpf", "data_nascimento")


class AproveitamentoInline(admin.TabularInline):
    model = Aproveitamento
    extra = 0


class SegundaChamadaInline(admin.TabularInline):
    model = SegundaChamada
    extra = 0


class RevisaoNotaInline(admin.TabularInline):
    model = RevisaoNota
    extra = 0


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "curso", "status", "data_matricula")
    list_filter = ("status",)
    inlines = [AproveitamentoInline, SegundaChamadaInline, RevisaoNotaInline]


@admin.register(Aproveitamento)
class AproveitamentoAdmin(admin.ModelAdmin):
    list_display = ("matricula", "disciplina_origem", "nota", "status")
    list_filter = ("status",)


@admin.register(SegundaChamada)
class SegundaChamadaAdmin(admin.ModelAdmin):
    list_display = ("matricula", "avaliacao", "status", "solicitado_em")
    list_filter = ("status",)


@admin.register(RevisaoNota)
class RevisaoNotaAdmin(admin.ModelAdmin):
    list_display = ("matricula", "avaliacao", "nota_atual", "nota_revisada", "status")
    list_filter = ("status",)
