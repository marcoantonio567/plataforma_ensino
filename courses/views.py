from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AulaForm, CursoForm, ModuloForm
from .models import Aula, Curso, Modulo


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


def criar_curso(request):
    form = CursoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        curso = form.save()
        return redirect("courses:gerenciar_curso", curso_id=curso.pk)
    return render(request, "courses/criar_curso.html", {"form": form})


def gerenciar_curso(request, curso_id):
    curso = get_object_or_404(Curso.objects.prefetch_related("modulos__aulas"), pk=curso_id)
    curso_form = CursoForm(instance=curso)
    modulo_form = ModuloForm()
    aula_forms = {modulo.pk: AulaForm() for modulo in curso.modulos.all()}
    erro = None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "editar_curso":
            curso_form = CursoForm(request.POST, instance=curso)
            if curso_form.is_valid():
                curso_form.save()
                return redirect("courses:gerenciar_curso", curso_id=curso.pk)

        elif action == "criar_modulo":
            modulo_form = ModuloForm(request.POST)
            if modulo_form.is_valid():
                proxima_ordem = (
                    curso.modulos.aggregate(max=Max("ordem"))["max"] or 0
                ) + 1
                modulo = modulo_form.save(commit=False)
                modulo.curso = curso
                modulo.ordem = proxima_ordem
                modulo.save()
                return redirect("courses:gerenciar_curso", curso_id=curso.pk)

        elif action == "criar_aula":
            modulo_id = request.POST.get("modulo_id")
            modulo = get_object_or_404(Modulo, pk=modulo_id, curso=curso)
            aula_form = AulaForm(request.POST)
            if aula_form.is_valid():
                proxima_ordem = (
                    modulo.aulas.aggregate(max=Max("ordem"))["max"] or 0
                ) + 1
                aula = aula_form.save(commit=False)
                aula.modulo = modulo
                aula.ordem = proxima_ordem
                aula.save()
                return redirect("courses:gerenciar_curso", curso_id=curso.pk)
            else:
                aula_forms[modulo.pk] = aula_form

        elif action == "excluir_modulo":
            modulo_id = request.POST.get("modulo_id")
            Modulo.objects.filter(pk=modulo_id, curso=curso).delete()
            return redirect("courses:gerenciar_curso", curso_id=curso.pk)

        elif action == "excluir_aula":
            aula_id = request.POST.get("aula_id")
            Aula.objects.filter(pk=aula_id, modulo__curso=curso).delete()
            return redirect("courses:gerenciar_curso", curso_id=curso.pk)

    return render(request, "courses/gerenciar_curso.html", {
        "curso": curso,
        "curso_form": curso_form,
        "modulo_form": modulo_form,
        "aula_forms": aula_forms,
        "erro": erro,
    })
