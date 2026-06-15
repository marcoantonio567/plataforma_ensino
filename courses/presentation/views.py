from django.shortcuts import get_object_or_404, redirect, render

from courses.application import selectors, services
from courses.models import Aula, Curso
from courses.presentation.forms import AulaForm, CursoForm, ModuloForm


def home(request):
    return render(request, "courses/home.html", {"cursos": selectors.list_courses()})


def curso_detail(request, curso_id):
    curso = get_object_or_404(
        Curso.objects.prefetch_related("modulos__aulas"),
        pk=curso_id,
    )
    return render(request, "courses/curso_detail.html", {
        "curso": curso,
        "modulo_ativo": curso.modulos.first(),
        "matricula": selectors.find_student_enrollment(request.user, curso),
    })


def modulo_detail(request, curso_id, modulo_id):
    curso = get_object_or_404(
        Curso.objects.prefetch_related("modulos__aulas"),
        pk=curso_id,
    )
    modulo = get_object_or_404(curso.modulos, pk=modulo_id)
    return render(request, "courses/modulo_detail.html", {
        "curso": curso,
        "modulo_ativo": modulo,
    })


def aula_detail(request, curso_id, modulo_id, aula_id):
    curso = get_object_or_404(
        Curso.objects.prefetch_related("modulos__aulas"),
        pk=curso_id,
    )
    modulo = get_object_or_404(curso.modulos, pk=modulo_id)
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
    curso = get_object_or_404(
        Curso.objects.prefetch_related("modulos__aulas"),
        pk=curso_id,
    )
    curso_form = CursoForm(instance=curso)
    modulo_form = ModuloForm()
    aula_forms = {modulo.pk: AulaForm() for modulo in curso.modulos.all()}

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
                services.create_module(curso, name=modulo_form.cleaned_data["nome"])
                return redirect("courses:gerenciar_curso", curso_id=curso.pk)
        elif action == "criar_aula":
            modulo = get_object_or_404(
                curso.modulos,
                pk=request.POST.get("modulo_id"),
            )
            aula_form = AulaForm(request.POST)
            if aula_form.is_valid():
                services.create_lesson(
                    modulo,
                    title=aula_form.cleaned_data["titulo"],
                    duration=aula_form.cleaned_data["duracao"],
                    content=aula_form.cleaned_data["conteudo"],
                )
                return redirect("courses:gerenciar_curso", curso_id=curso.pk)
            aula_forms[modulo.pk] = aula_form
        elif action == "excluir_modulo":
            services.delete_module(curso.pk, request.POST.get("modulo_id"))
            return redirect("courses:gerenciar_curso", curso_id=curso.pk)
        elif action == "excluir_aula":
            services.delete_lesson(curso.pk, request.POST.get("aula_id"))
            return redirect("courses:gerenciar_curso", curso_id=curso.pk)

    return render(request, "courses/gerenciar_curso.html", {
        "curso": curso,
        "curso_form": curso_form,
        "modulo_form": modulo_form,
        "aula_forms": aula_forms,
        "erro": None,
    })
