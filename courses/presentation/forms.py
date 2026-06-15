from django import forms

from courses.models import Aula, Curso, Modulo


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ["nome", "carga_horaria"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Python para Iniciantes"}),
            "carga_horaria": forms.NumberInput(attrs={"placeholder": "Ex.: 40", "min": 1}),
        }
        labels = {"nome": "Nome do curso", "carga_horaria": "Carga horaria (horas)"}


class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = ["nome"]
        widgets = {"nome": forms.TextInput(attrs={"placeholder": "Ex.: Introducao ao Python"})}
        labels = {"nome": "Nome do modulo"}


class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ["titulo", "duracao", "conteudo"]
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Ex.: Variaveis e tipos"}),
            "duracao": forms.NumberInput(attrs={"placeholder": "Ex.: 30", "min": 1}),
            "conteudo": forms.Textarea(attrs={"rows": 4, "placeholder": "Conteudo da aula..."}),
        }
        labels = {"titulo": "Titulo da aula", "duracao": "Duracao (minutos)", "conteudo": "Conteudo"}
