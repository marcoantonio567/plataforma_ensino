from students.domain.factories import AlunoFactory, MatriculaFactory
from students.models import Aluno, Matricula


class DjangoEnrollmentRepository:
    def get_or_create_student(self, user):
        try:
            return user.aluno
        except Aluno.DoesNotExist:
            student = AlunoFactory.criar_para_usuario(user)
            student.save()
            return student

    def find_by_student_and_course(self, student, course):
        return Matricula.objects.filter(aluno=student, curso=course).first()

    def add(self, student, course):
        enrollment = MatriculaFactory.criar(student, course)
        enrollment.save()
        return enrollment

    def save(self, enrollment, *, fields: list[str] | None = None) -> None:
        if fields is None:
            enrollment.save()
        else:
            enrollment.save(update_fields=fields)


DjangoStudentRepository = DjangoEnrollmentRepository
