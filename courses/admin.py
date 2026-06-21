from django.contrib import admin
from .models import Curso, RegraCurso, Modulo, Aula, PreRequisito


class PreRequisitoInline(admin.TabularInline):
    model = PreRequisito
    extra = 1


class ModuloInline(admin.TabularInline):
    model = Modulo
    extra = 1


class RegraCursoInline(admin.TabularInline):
    model = RegraCurso
    extra = 1


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("nome", "carga_horaria")
    inlines = [RegraCursoInline, PreRequisitoInline, ModuloInline]


@admin.register(RegraCurso)
class RegraCursoAdmin(admin.ModelAdmin):
    list_display = ("curso", "data_inicio", "data_fim", "media_minima", "carga_horaria_minima", "exige_projeto_final")
    list_filter = ("curso", "exige_projeto_final")


class AulaInline(admin.TabularInline):
    model = Aula
    extra = 1


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ("nome", "curso", "ordem")
    inlines = [AulaInline]


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "modulo", "ordem", "duracao")
