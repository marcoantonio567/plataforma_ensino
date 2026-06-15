from courses.models import Curso, Modulo


def list_courses():
    return Curso.objects.prefetch_related("modulos").all()


def get_course(course_id: int):
    return Curso.objects.prefetch_related("modulos__aulas").get(pk=course_id)


def get_module(course, module_id: int):
    return Modulo.objects.get(pk=module_id, curso=course)


def find_student_enrollment(user, course):
    if not user.is_authenticated or not hasattr(user, "aluno"):
        return None

    from students.models import Matricula

    return Matricula.objects.filter(aluno=user.aluno, curso=course).first()
