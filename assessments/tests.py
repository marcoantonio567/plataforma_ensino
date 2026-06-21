from django.test import SimpleTestCase

from assessments.domain.policies import InvalidGrade, validate_grade
from assessments.domain.value_objects import Nota
from assessments.models import AvaliacaoRealizada


class GradePolicyTest(SimpleTestCase):
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
