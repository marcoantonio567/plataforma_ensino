import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from courses.models import Curso
from .models import Aluno, Matricula


def _get_or_create_aluno(user):
    try:
        return user.aluno
    except Aluno.DoesNotExist:
        numero = f"ALU{uuid.uuid4().hex[:8].upper()}"
        return Aluno.objects.create(
            usuario=user,
            numero_matricula=numero,
            data_ingresso=timezone.now().date(),
        )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("courses:home")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        next_url = request.GET.get("next") or "students:minhas_matriculas"
        return redirect(next_url)
    return render(request, "students/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("courses:home")


def registro_view(request):
    if request.user.is_authenticated:
        return redirect("courses:home")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Bem-vindo, {user.username}! Conta criada com sucesso.")
        return redirect("students:minhas_matriculas")
    return render(request, "students/registro.html", {"form": form})


@login_required(login_url="students:login")
def minhas_matriculas(request):
    aluno = _get_or_create_aluno(request.user)
    matriculas = aluno.matriculas.select_related("curso").order_by("-data_matricula")
    return render(request, "students/minhas_matriculas.html", {"matriculas": matriculas})


@login_required(login_url="students:login")
def matricular_curso(request, curso_id):
    if request.method != "POST":
        return redirect("courses:curso_detail", curso_id=curso_id)

    curso = get_object_or_404(Curso, pk=curso_id)
    aluno = _get_or_create_aluno(request.user)

    matricula_existente = Matricula.objects.filter(aluno=aluno, curso=curso).first()
    if matricula_existente:
        if matricula_existente.status == Matricula.Status.CANCELADA:
            matricula_existente.status = Matricula.Status.ATIVA
            matricula_existente.save()
            messages.success(request, f'Matrícula reativada em "{curso.nome}"!')
        else:
            messages.info(request, f'Você já está matriculado em "{curso.nome}".')
        return redirect("students:minhas_matriculas")

    aluno.matricular(curso)
    messages.success(request, f'Matrícula realizada com sucesso em "{curso.nome}"!')
    return redirect("students:minhas_matriculas")


@login_required(login_url="students:login")
def cancelar_matricula(request, matricula_id):
    if request.method != "POST":
        return redirect("students:minhas_matriculas")

    aluno = _get_or_create_aluno(request.user)
    matricula = get_object_or_404(Matricula, pk=matricula_id, aluno=aluno)
    matricula.status = Matricula.Status.CANCELADA
    matricula.save()
    messages.success(request, f'Matrícula em "{matricula.curso.nome}" cancelada.')
    return redirect("students:minhas_matriculas")
