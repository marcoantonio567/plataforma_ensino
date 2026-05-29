from django import forms
from .models import Aula, Curso, Modulo


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ["nome", "carga_horaria"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Python para Iniciantes"}),
            "carga_horaria": forms.NumberInput(attrs={"placeholder": "Ex.: 40", "min": 1}),
        }
        labels = {
            "nome": "Nome do curso",
            "carga_horaria": "Carga horária (horas)",
        }


class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = ["nome"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Introdução ao Python"}),
        }
        labels = {
            "nome": "Nome do módulo",
        }


class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ["titulo", "duracao", "conteudo"]
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Ex.: Variáveis e tipos"}),
            "duracao": forms.NumberInput(attrs={"placeholder": "Ex.: 30", "min": 1}),
            "conteudo": forms.Textarea(attrs={"rows": 4, "placeholder": "Conteúdo da aula..."}),
        }
        labels = {
            "titulo": "Título da aula",
            "duracao": "Duração (minutos)",
            "conteudo": "Conteúdo",
        }
