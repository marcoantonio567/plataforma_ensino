from django.shortcuts import get_object_or_404, render
from .models import Curso, Modulo, Aula


def home(request):
    cursos = Curso.objects.prefetch_related("modulos").all()
    return render(request, "courses/home.html", {"cursos": cursos})


def curso_detail(request, curso_id):
    curso = get_object_or_404(Curso.objects.prefetch_related("modulos__aulas"), pk=curso_id)
    primeiro_modulo = curso.modulos.first()
    return render(request, "courses/curso_detail.html", {
        "curso": curso,
        "modulo_ativo": primeiro_modulo,
    })


def modulo_detail(request, curso_id, modulo_id):
    curso = get_object_or_404(Curso.objects.prefetch_related("modulos__aulas"), pk=curso_id)
    modulo = get_object_or_404(Modulo, pk=modulo_id, curso=curso)
    return render(request, "courses/modulo_detail.html", {
        "curso": curso,
        "modulo_ativo": modulo,
    })


def aula_detail(request, curso_id, modulo_id, aula_id):
    curso = get_object_or_404(Curso.objects.prefetch_related("modulos__aulas"), pk=curso_id)
    modulo = get_object_or_404(Modulo, pk=modulo_id, curso=curso)
    aula = get_object_or_404(Aula, pk=aula_id, modulo=modulo)
    return render(request, "courses/aula_detail.html", {
        "curso": curso,
        "modulo_ativo": modulo,
        "aula_ativa": aula,
    })
