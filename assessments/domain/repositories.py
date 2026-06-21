from typing import Protocol


class AssessmentRepository(Protocol):
    """Repository do aggregate root Avaliacao.

    AvaliacaoRealizada e resultado interno do agregado de avaliacao neste
    contexto; por isso nao existe um repository separado para ela.
    """

    def save_result_for_assessment(self, *, student, assessment, grade: float, date): ...
