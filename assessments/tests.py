from django.test import SimpleTestCase

from assessments.domain.policies import InvalidGrade, validate_grade
from assessments.models import AvaliacaoRealizada


class GradePolicyTest(SimpleTestCase):
    def test_rejects_grade_outside_allowed_range(self):
        with self.assertRaises(InvalidGrade):
            validate_grade(10.1)

    def test_evaluation_result_validates_grade(self):
        result = AvaliacaoRealizada()

        with self.assertRaises(InvalidGrade):
            result.registrar_nota(-1, data=None)
