"""Mutation checks for read-only material qualification predicates."""
import unittest

import numpy as np

import material_audit as a


def material_log():
    modules = ['LIB:', 'SALT:', 'TONE:', 'GREP:', 'GREP:', 'GREP:', 'EQU:', 'UTL:']
    return ('\n'.join('->@BEGIN MODULE : ' + x for x in modules)
            + '\nCONVERGENCE REACHED AT TONE ITERATION = 4 ERROR = 9.0E-6\n'
            + ' EPS 1.0E-05 (STOPING CRITERION)\n'
            + '>|AXMAT-MATERIAL-A-COMPLETE     |>0032\n'
            + 'normal end of execution for dragon\n')


class AuditTests(unittest.TestCase):
    def test_density_matches_independently_saved_corrected_a(self):
        expected = dict(U235=3.77126489e-05, U238=.0188186113, Pu238=.000128930085,
                        Pu239=.00274785352, Pu240=.00128681189, Pu241=.000361900282,
                        Pu242=.000391768233, Am241=6.07315451e-05, O16=.0471919551)
        self.assertTrue(all(a.core.exact(v, expected[k]) for k, v in a.fuel_densities(.21, .79).items()))

    def test_b_changes_composition_without_changing_internal_vectors(self):
        x, y = a.fuel_densities(.21, .79), a.fuel_densities(.2436, .7564)
        self.assertGreater(y['Pu239'], x['Pu239'])
        self.assertLess(y['U238'], x['U238'])
        self.assertNotEqual(y['O16'], x['O16'])
        self.assertAlmostEqual(float(y['Pu238'] / y['Pu239']), .0259 / .552, places=7)

    def test_real_terminal_passes_but_echo_spoof_does_not(self):
        self.assertEqual(a.terminal(material_log(), 'A')['tone_iteration'], 4)
        bad = material_log().replace('>|AXMAT-MATERIAL-A-COMPLETE     |>0032',
                                    '<|ECHO "AXMAT-MATERIAL-A-COMPLETE" ; |<0032')
        with self.assertRaisesRegex(ValueError, 'executed completion'):
            a.terminal(bad, 'A')

    def test_failed_or_unexpected_native_work_rejected(self):
        for old, new in [('9.0E-6', '-1.1E-5'), ('ITERATION = 4', 'ITERATION = 21'),
                         ('normal end of execution for dragon', ''), ('UTL:', 'FLU:')]:
            with self.subTest(new=new), self.assertRaises(ValueError):
                a.terminal(material_log().replace(old, new), 'A')

    def test_native_masked_convergence_distinct_from_printed_global_error(self):
        result = a.terminal(material_log().replace('9.0E-6', '2.333E-5'), 'A')
        self.assertTrue(result['native_masked_convergence'])
        self.assertFalse(result['printed_global_error_within_epsilon'])
        with self.assertRaises(ValueError):
            a.terminal(material_log() + 'TONDRV: MAXIMUM NUMBER OF SELF-SHIELDING ITERATIONS EXCEEDED.\n', 'A')

    def test_duplicate_terminal_and_wrong_state_rejected(self):
        with self.assertRaises(ValueError):
            a.terminal(material_log() + '\n>|AXMAT-MATERIAL-A-COMPLETE |>55\n', 'A')
        with self.assertRaises(ValueError):
            a.terminal(material_log(), 'B')

    def test_negative_p0_rejected_signed_p1_not_clipped(self):
        value = np.zeros((3, 3), dtype=np.float32)
        value[0, 1] = -1e-20
        with self.assertRaises(ValueError):
            a.core.nonnegative_p0([value], 'test')
        mixed = a.core.density_mix([value], [.3], [8], 8)
        self.assertLess(mixed[7, 0, 1], 0)
        self.assertTrue(a.core.exact(mixed[7], np.float32(.3) * value))

    def test_native_empty_alias_resolves_only_prior_identical_isotope(self):
        row = {'NTOT0': [1.]}
        got, indices = a.resolve_isotope_rows([row, {}, {}], ['O       0007'] * 3,
                                              ['O16'] * 3, [1023.15] * 3)
        self.assertEqual(indices, [1, 1, 1])
        self.assertIs(got[2], row)
        with self.assertRaises(ValueError):
            a.resolve_isotope_rows([{}, row], ['O       0007'] * 2, ['O16'] * 2, [1023.15] * 2)
        with self.assertRaises(ValueError):
            a.resolve_isotope_rows([row, {}], ['O       0007'] * 2, ['O16'] * 2, [1023.15, 923.15])
        with self.assertRaises(ValueError):
            a.resolve_isotope_rows([row, {}], ['O       0007', 'O       0006'], ['O16'] * 2, [1023.15] * 2)

    def test_snapshot_completion_retains_archive_dimension_limit(self):
        log = '\n'.join('->@BEGIN MODULE : ' + x for x in
                         ['SALT:', 'MCCGT:', 'ASM:', 'FLU:'] + ['BACKUP:'] * 4)
        log += '\n>|AXMAT-SNAPSHOT-A-COMPLETE 1.2 |>0038\nnormal end of execution for dragon\n'
        result = a.terminal(log, 'A', 'SNAPSHOT')
        self.assertEqual(result['printed_keff'], 1.2)
        self.assertIn('REQUIRE_INDEPENDENT_ARCHIVE_READER', result['archive_dimensions'])
        with self.assertRaises(ValueError):
            a.terminal(log.replace('BACKUP:', 'EQU:', 1), 'A', 'SNAPSHOT')


if __name__ == '__main__':
    unittest.main()
