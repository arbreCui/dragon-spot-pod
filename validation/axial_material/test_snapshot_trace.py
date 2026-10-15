import unittest
from analyze_snapshot_trace import analyze


class TraceObservations(unittest.TestCase):
    def test_krylov_exit_and_missing_outer_flux_not_promoted(self):
        result = analyze('''OUT(0) EIG: PRC= 1.0E0 TAR= 2.5E-7
MCGMRE-TRACE ITER= 1 PHASE=INITIAL ACTIVE-AFTER= 1 MAX-REPS= 1.0E-4 EPSI= 2.5E-8
MCGMRE-TRACE ITER= 3 PHASE=KRYLOV ACTIVE-AFTER= 0 MAX-REPS= 1.0E-8 EPSI= 2.5E-8
 M O C PARAMETERS:
 GROUP ( 17) :
 MCCGF: NUMBER OF MCCG ITERATIONS= 3 ACCURACY= 1.0000E-08.
OUT(1) EIG: PRC= 1.0E-8 TAR= 2.5E-7
OUT(1) FLX: PRC= 1.0E-6 TAR= 2.5E-7
MCGMRE-TRACE ITER= 1 PHASE=INITIAL ACTIVE-AFTER= 1 MAX-REPS= 1.0E-5 EPSI= 2.5E-8
''')
        self.assertFalse(result['parser_errors'])
        self.assertIsNone(result['outer'][0]['flux'])
        self.assertEqual(result['calls_with_group_summaries'],1)
        self.assertEqual(result['all_started_calls'],2)
        self.assertEqual(result['maximum_reported_group_iterations'],3)
        self.assertEqual(result['minimum_printed_outer_flux_change'],1e-6)

    def test_active_at_cap_without_warning_is_detected(self):
        result = analyze('''MCGMRE-TRACE ITER= 1 PHASE=INITIAL ACTIVE-AFTER= 1 MAX-REPS= 1.0E-4 EPSI= 2.5E-8
MCGMRE-TRACE ITER= 19 PHASE=KRYLOV ACTIVE-AFTER= 1 MAX-REPS= 1.0E-6 EPSI= 2.5E-8
M O C PARAMETERS:
GROUP ( 1) :
MCCGF: NUMBER OF MCCG ITERATIONS= 19 ACCURACY= 1.0000E-06.
GROUP ( 2) :''')
        self.assertEqual(result['completed_calls_with_active_groups'],[1])
        self.assertEqual(len(result['printed_group_residuals_above_epsi']),1)
        self.assertEqual(result['unpaired_final_group'],2)


if __name__ == '__main__':
    unittest.main()
