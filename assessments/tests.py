from django.test import SimpleTestCase

from assessments.domain.policies import InvalidGrade, validate_grade


class GradePolicyTest(SimpleTestCase):
    def test_rejects_grade_outside_allowed_range(self):
        with self.assertRaises(InvalidGrade):
            validate_grade(10.1)
