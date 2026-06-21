import uuid

from django.utils import timezone

from students.domain.value_objects import NumeroMatricula
from students.models import Aluno, Matricula


class DjangoEnrollmentRepository:
    def get_or_create_student(self, user):
        try:
            return user.aluno
        except Aluno.DoesNotExist:
            return Aluno.objects.create(
                usuario=user,
                numero_matricula=str(NumeroMatricula(f"ALU{uuid.uuid4().hex[:8].upper()}")),
                data_ingresso=timezone.localdate(),
            )

    def find_by_student_and_course(self, student, course):
        return Matricula.objects.filter(aluno=student, curso=course).first()

    def add(self, student, course):
        return student.matricular(course)

    def save(self, enrollment, *, fields: list[str] | None = None) -> None:
        if fields is None:
            enrollment.save()
        else:
            enrollment.save(update_fields=fields)


DjangoStudentRepository = DjangoEnrollmentRepository
