import unittest
from analyze_true_residual import analyze


def fixture():
    return '''AXMAT-TRUE GROUP= 1 ITER= 4 EST/TRUE/REPEAT/NORM= 1e-9 1e-6 0 1
AXMAT-VECTOR 1 1 1 0 1e-6 1e-6
AXMAT-TRUE-RESIDUAL-PROBE-COMPLETE
'''


class TrueResidualTest(unittest.TestCase):
    def test_recurrence_false_acceptance_is_detected(self):
        result = analyze(fixture(), groups=1, unknowns=1)
        self.assertEqual(result['false_acceptance_count'], 1)
        self.assertFalse(result['numerical_acceptance'])

    def test_incomplete_or_duplicate_observations_fail(self):
        for text in (fixture().replace('AXMAT-VECTOR', 'MISSING'),
                     fixture() + 'AXMAT-VECTOR 1 1 1 0 1e-6 1e-6\n'):
            with self.assertRaises(ValueError):
                analyze(text, groups=1, unknowns=1)

    def test_bad_residual_or_nonrepeatable_map_fails(self):
        for text in (fixture().replace('1e-9 1e-6', '1e-9 1e-7'),
                     fixture().replace('1 0 1e-6 1e-6', '1 0 1e-6 2e-6')):
            with self.assertRaises(ValueError):
                analyze(text, groups=1, unknowns=1)


if __name__ == '__main__':
    unittest.main()
