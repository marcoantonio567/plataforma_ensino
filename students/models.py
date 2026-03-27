from django.db import models
from django.contrib.auth.models import User
from courses.models import Curso
from assessments.models import Avaliacao


class Aluno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="aluno")
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username


class Matricula(models.Model):
    class Status(models.TextChoices):
        ATIVA = "ATIVA", "Ativa"
        TRANCADA = "TRANCADA", "Trancada"
        CONCLUIDA = "CONCLUIDA", "Concluída"
        CANCELADA = "CANCELADA", "Cancelada"

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="matriculas")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="matriculas")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ATIVA)
    data_matricula = models.DateField(auto_now_add=True)
    data_trancamento = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        unique_together = ("aluno", "curso")

    def __str__(self):
        return f"{self.aluno} — {self.curso} ({self.get_status_display()})"


class Aproveitamento(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        APROVADO = "APROVADO", "Aprovado"
        REJEITADO = "REJEITADO", "Rejeitado"

    matricula = models.ForeignKey(
        Matricula, on_delete=models.CASCADE, related_name="aproveitamentos"
    )
    disciplina_origem = models.CharField(max_length=200)
    instituicao_origem = models.CharField(max_length=200)
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDENTE)
    solicitado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Aproveitamento"
        verbose_name_plural = "Aproveitamentos"

    def __str__(self):
        return f"Aproveitamento: {self.disciplina_origem} ({self.get_status_display()})"


class SegundaChamada(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        APROVADA = "APROVADA", "Aprovada"
        REJEITADA = "REJEITADA", "Rejeitada"

    matricula = models.ForeignKey(
        Matricula, on_delete=models.CASCADE, related_name="segundas_chamadas"
    )
    avaliacao = models.ForeignKey(
        Avaliacao, on_delete=models.CASCADE, related_name="segundas_chamadas"
    )
    justificativa = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDENTE)
    solicitado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Segunda Chamada"
        verbose_name_plural = "Segundas Chamadas"

    def __str__(self):
        return f"2ª Chamada: {self.matricula.aluno} — {self.avaliacao}"


class RevisaoNota(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        EM_ANALISE = "EM_ANALISE", "Em Análise"
        DEFERIDA = "DEFERIDA", "Deferida"
        INDEFERIDA = "INDEFERIDA", "Indeferida"

    matricula = models.ForeignKey(
        Matricula, on_delete=models.CASCADE, related_name="revisoes_nota"
    )
    avaliacao = models.ForeignKey(
        Avaliacao, on_delete=models.CASCADE, related_name="revisoes"
    )
    nota_atual = models.DecimalField(max_digits=4, decimal_places=2)
    nota_revisada = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    justificativa = models.TextField()
    status = models.CharField(max_length=11, choices=Status.choices, default=Status.PENDENTE)
    solicitado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Revisão de Nota"
        verbose_name_plural = "Revisões de Nota"

    def __str__(self):
        return f"Revisão: {self.matricula.aluno} — {self.avaliacao} ({self.get_status_display()})"
