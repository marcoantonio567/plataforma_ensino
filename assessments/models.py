from django.db import models

from assessments.domain.policies import validate_grade


class Avaliacao(models.Model):
    class Tipo(models.TextChoices):
        OBJETIVA = "OBJETIVA", "Objetiva"
        DISCURSIVA = "DISCURSIVA", "Discursiva"
        PROJETO_PRATICO = "PROJETO_PRATICO", "Projeto Prático"
        PROVA_MONITORADA = "PROVA_MONITORADA", "Prova com Monitoramento Remoto"

    modulo = models.ForeignKey(
        "courses.Modulo", on_delete=models.CASCADE, related_name="avaliacoes"
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    peso = models.FloatField(default=1.0)

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def __str__(self):
        return f"[{self.get_tipo_display()}] — {self.modulo}"

    def nota_ponderada(self, nota):
        return validate_grade(nota) * self.peso

    def _validate_weight(self):
        self.peso = float(self.peso)
        if self.peso <= 0:
            raise ValueError("O peso da avaliacao deve ser maior que zero.")

    def clean(self):
        super().clean()
        self._validate_weight()

    def save(self, *args, **kwargs):
        self._validate_weight()
        return super().save(*args, **kwargs)

    def alterar_peso(self, novo_peso):
        self.peso = novo_peso
        self._validate_weight()
        return self


class AvaliacaoObjetiva(Avaliacao):
    questoes = models.JSONField(default=list, help_text="Lista de questões objetivas")

    def adicionar_questao(self, questao):
        if not questao:
            raise ValueError("A questao objetiva e obrigatoria.")
        self.questoes = [*self.questoes, questao]
        return self

    class Meta:
        verbose_name = "Avaliação Objetiva"
        verbose_name_plural = "Avaliações Objetivas"


class AvaliacaoDiscursiva(Avaliacao):
    descricao = models.TextField()

    class Meta:
        verbose_name = "Avaliação Discursiva"
        verbose_name_plural = "Avaliações Discursivas"


class ProjetoPratico(Avaliacao):
    repositorio = models.URLField(blank=True)

    def vincular_repositorio(self, repositorio):
        if not repositorio:
            raise ValueError("O repositorio do projeto e obrigatorio.")
        self.repositorio = repositorio
        return self

    class Meta:
        verbose_name = "Projeto Prático"
        verbose_name_plural = "Projetos Práticos"


class ProvaMonitorada(Avaliacao):
    monitoramento_ativo = models.BooleanField(default=True)

    def ativar_monitoramento(self):
        self.monitoramento_ativo = True
        return self

    def desativar_monitoramento(self):
        self.monitoramento_ativo = False
        return self

    class Meta:
        verbose_name = "Prova Monitorada"
        verbose_name_plural = "Provas Monitoradas"


class AvaliacaoRealizada(models.Model):
    aluno = models.ForeignKey(
        "students.Aluno", on_delete=models.CASCADE, related_name="avaliacoes_realizadas"
    )
    avaliacao = models.ForeignKey(
        Avaliacao, on_delete=models.CASCADE, related_name="realizacoes"
    )
    nota = models.FloatField()
    data = models.DateField()

    class Meta:
        verbose_name = "Avaliação Realizada"
        verbose_name_plural = "Avaliações Realizadas"
        unique_together = ("aluno", "avaliacao")

    def __str__(self):
        return f"{self.aluno} — {self.avaliacao}: {self.nota}"

    def _validate_value_objects(self):
        if self.nota is not None:
            self.nota = validate_grade(self.nota)

    def clean(self):
        super().clean()
        self._validate_value_objects()

    def save(self, *args, **kwargs):
        self._validate_value_objects()
        return super().save(*args, **kwargs)

    def registrar_nota(self, nota, *, data):
        self.nota = validate_grade(nota)
        self.data = data
        return self

    def nota_ponderada(self):
        return self.avaliacao.nota_ponderada(self.nota)

    def foi_aprovada(self, media_minima):
        return self.nota >= media_minima
