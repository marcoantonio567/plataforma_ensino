from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AulaForm, CursoForm, ModuloForm
from .models import Aula, Curso, Modulo


def home(request):
    """Exibe a pagina inicial com todos os cursos cadastrados."""
    cursos = Curso.objects.prefetch_related("modulos").all()
    return render(request, "courses/home.html", {"cursos": cursos})


def curso_detail(request, curso_id):
    """Mostra os detalhes de um curso e carrega o primeiro modulo como ativo."""
    curso = get_object_or_404(Curso.objects.prefetch_related("modulos__aulas"), pk=curso_id)
    primeiro_modulo = curso.modulos.first()

    matricula = None
    if request.user.is_authenticated:
        # Se o usuario estiver logado, tenta buscar a matricula dele neste curso.
        try:
            from students.models import Matricula
            matricula = Matricula.objects.filter(
                aluno=request.user.aluno, curso=curso
            ).first()
        except Exception:
            pass

    return render(request, "courses/curso_detail.html", {
        "curso": curso,
        "modulo_ativo": primeiro_modulo,
        "matricula": matricula,
    })


def modulo_detail(request, curso_id, modulo_id):
    """Mostra um modulo especifico dentro de um curso."""
    curso = get_object_or_404(Curso.objects.prefetch_related("modulos__aulas"), pk=curso_id)
    modulo = get_object_or_404(Modulo, pk=modulo_id, curso=curso)
    return render(request, "courses/modulo_detail.html", {
        "curso": curso,
        "modulo_ativo": modulo,
    })


def aula_detail(request, curso_id, modulo_id, aula_id):
    """Mostra uma aula especifica dentro de um modulo e curso."""
    curso = get_object_or_404(Curso.objects.prefetch_related("modulos__aulas"), pk=curso_id)
    modulo = get_object_or_404(Modulo, pk=modulo_id, curso=curso)
    aula = get_object_or_404(Aula, pk=aula_id, modulo=modulo)
    return render(request, "courses/aula_detail.html", {
        "curso": curso,
        "modulo_ativo": modulo,
        "aula_ativa": aula,
    })


def criar_curso(request):
    """Cria um novo curso e redireciona para a tela de gerenciamento."""
    form = CursoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        curso = form.save()
        return redirect("courses:gerenciar_curso", curso_id=curso.pk)
    return render(request, "courses/criar_curso.html", {"form": form})


def gerenciar_curso(request, curso_id):
    """Permite editar o curso e criar ou excluir seus modulos e aulas."""
    curso = get_object_or_404(Curso.objects.prefetch_related("modulos__aulas"), pk=curso_id)
    curso_form = CursoForm(instance=curso)
    modulo_form = ModuloForm()
    aula_forms = {modulo.pk: AulaForm() for modulo in curso.modulos.all()}
    erro = None

    if request.method == "POST":
        # O campo action informa qual operacao o formulario enviado deve executar.
        action = request.POST.get("action")

        if action == "editar_curso":
            # Atualiza os dados principais do curso.
            curso_form = CursoForm(request.POST, instance=curso)
            if curso_form.is_valid():
                curso_form.save()
                return redirect("courses:gerenciar_curso", curso_id=curso.pk)

        elif action == "criar_modulo":
            # Cria um modulo novo no final da ordem atual do curso.
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
            # Cria uma aula nova dentro do modulo escolhido.
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
            # Exclui o modulo selecionado do curso.
            modulo_id = request.POST.get("modulo_id")
            Modulo.objects.filter(pk=modulo_id, curso=curso).delete()
            return redirect("courses:gerenciar_curso", curso_id=curso.pk)

        elif action == "excluir_aula":
            # Exclui a aula selecionada, garantindo que ela pertence a este curso.
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
