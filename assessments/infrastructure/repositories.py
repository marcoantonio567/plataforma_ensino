from assessments.models import AvaliacaoRealizada


class DjangoAssessmentRepository:
    def record_grade(self, *, student, assessment, grade: float, date):
        result, _ = AvaliacaoRealizada.objects.update_or_create(
            aluno=student,
            avaliacao=assessment,
            defaults={"nota": grade, "data": date},
        )
        return result
