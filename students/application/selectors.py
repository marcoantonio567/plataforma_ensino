def list_student_enrollments(student):
    return student.matriculas.select_related("curso").order_by("-data_matricula")
