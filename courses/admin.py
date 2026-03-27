from django.contrib import admin
from .models import Curso, Modulo, Aula, PreRequisito


class ModuloInline(admin.TabularInline):
    model = Modulo
    extra = 1


class PreRequisitoInline(admin.TabularInline):
    model = PreRequisito
    fk_name = "curso"
    extra = 1


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "carga_horaria", "nota_minima")
    inlines = [PreRequisitoInline, ModuloInline]


class AulaInline(admin.TabularInline):
    model = Aula
    extra = 1


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ("titulo", "curso", "ordem")
    inlines = [AulaInline]


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "modulo", "ordem", "duracao")
