from django.test import TestCase

from assessments.domain.policies import InvalidGrade, validate_grade
from assessments.domain.value_objects import Nota
from assessments.models import Avaliacao, AvaliacaoRealizada
from courses.models import Curso


class GradePolicyTest(TestCase):
    def test_rejects_grade_outside_allowed_range(self):
        with self.assertRaises(InvalidGrade):
            validate_grade(10.1)

    def test_evaluation_result_validates_grade(self):
        result = AvaliacaoRealizada()

        with self.assertRaises(InvalidGrade):
            result.registrar_nota(-1, data=None)

    def test_grade_is_value_object(self):
        self.assertEqual(Nota(8), Nota(8.0))

        with self.assertRaises(Exception):
            Nota(8).valor = 9

    def test_evaluation_rejects_invalid_weight_on_save(self):
        course = Curso.objects.create(nome="Avaliacao", carga_horaria=10)
        module = course.adicionar_modulo(nome="Modulo", ordem=1)
        module.save()

        evaluation = Avaliacao(
            modulo=module,
            tipo=Avaliacao.Tipo.OBJETIVA,
            peso=0,
        )

        with self.assertRaises(ValueError):
            evaluation.save()
