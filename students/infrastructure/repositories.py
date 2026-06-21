import uuid

from django.utils import timezone

from students.domain.value_objects import NumeroMatricula
from students.models import Aluno, Matricula


class DjangoStudentRepository:
    def get_or_create_student(self, user):
        try:
            return user.aluno
        except Aluno.DoesNotExist:
            return Aluno.objects.create(
                usuario=user,
                numero_matricula=str(NumeroMatricula(f"ALU{uuid.uuid4().hex[:8].upper()}")),
                data_ingresso=timezone.localdate(),
            )

    def find_enrollment(self, student, course):
        return Matricula.objects.filter(aluno=student, curso=course).first()

    def enroll(self, student, course):
        rule = course.regra_vigente()
        return Matricula.objects.create(
            aluno=student,
            curso=course,
            regra_curso=rule,
        )

    def save_enrollment(self, enrollment, *, fields: list[str]) -> None:
        enrollment.save(update_fields=fields)
