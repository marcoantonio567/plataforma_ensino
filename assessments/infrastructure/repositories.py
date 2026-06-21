from assessments.models import AvaliacaoRealizada


class DjangoAssessmentRepository:
    def record_grade(self, *, student, assessment, grade: float, date):
        result, _ = AvaliacaoRealizada.objects.get_or_create(
            aluno=student,
            avaliacao=assessment,
            defaults={"nota": grade, "data": date},
        )
        result.registrar_nota(grade, data=date)
        result.save(update_fields=["nota", "data"])
        return result
