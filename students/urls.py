from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("registro/", views.registro_view, name="registro"),
    path("minhas-matriculas/", views.minhas_matriculas, name="minhas_matriculas"),
    path("matricular/<int:curso_id>/", views.matricular_curso, name="matricular_curso"),
    path("cancelar/<int:matricula_id>/", views.cancelar_matricula, name="cancelar_matricula"),
]
