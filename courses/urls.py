from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:curso_id>/", views.curso_detail, name="curso_detail"),
    path("<int:curso_id>/modulo/<int:modulo_id>/", views.modulo_detail, name="modulo_detail"),
    path("<int:curso_id>/modulo/<int:modulo_id>/aula/<int:aula_id>/", views.aula_detail, name="aula_detail"),
]
