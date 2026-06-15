from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Curso
from students.application import selectors, services
from students.models import Matricula


def login_view(request):
    if request.user.is_authenticated:
        return redirect("courses:home")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get("next") or "students:minhas_matriculas")
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
    student = services.get_or_create_student(request.user)
    enrollments = selectors.list_student_enrollments(student)
    return render(
        request,
        "students/minhas_matriculas.html",
        {"matriculas": enrollments},
    )


@login_required(login_url="students:login")
def matricular_curso(request, curso_id):
    if request.method != "POST":
        return redirect("courses:curso_detail", curso_id=curso_id)

    course = get_object_or_404(Curso, pk=curso_id)
    student = services.get_or_create_student(request.user)
    result = services.enroll_student(student, course)

    if result.created:
        messages.success(request, f'Matricula realizada com sucesso em "{course.nome}"!')
    elif result.reactivated:
        messages.success(request, f'Matricula reativada em "{course.nome}"!')
    else:
        messages.info(request, f'Voce ja esta matriculado em "{course.nome}".')
    return redirect("students:minhas_matriculas")


@login_required(login_url="students:login")
def cancelar_matricula(request, matricula_id):
    if request.method != "POST":
        return redirect("students:minhas_matriculas")

    student = services.get_or_create_student(request.user)
    enrollment = get_object_or_404(
        Matricula.objects.select_related("curso"),
        pk=matricula_id,
        aluno=student,
    )
    services.cancel_enrollment(enrollment)
    messages.success(request, f'Matricula em "{enrollment.curso.nome}" cancelada.')
    return redirect("students:minhas_matriculas")
