"""Short graph, saved-data and no-launch tests; never invoke NJOY/Dragon."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import remaining_temperature_batch as batch
import run_remaining_temperature_batch as runner


class BatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = batch.cases()
        cls.work = Path('/private/tmp/NOT_AN_ACTIVE_D4A_TEST')

    def test_138_ordered_stages_and_pins(self):
        graph = batch.validate_graph(self.rows,self.work)
        self.assertEqual(len(graph),138)
        self.assertEqual(sum(x['control'] for x in graph),42)
        pins = json.loads((batch.PREP/'inputs.json').read_text())
        for item in graph:
            for path in item['inputs'].values():
                if not path.is_relative_to(self.work):
                    self.assertIn(str(path),pins)
                    self.assertEqual(batch.sha(path),pins[str(path)])

    def test_low_high_link_and_preserved_decks(self):
        for row in self.rows:
            if row['expected_finite_dilutions'] != 18:
                continue
            g = batch.stages(row,self.work)
            for family in ('control','expanded'):
                p = self.work/row['nuclide']/family
                high = next(s for s in g if s['output'] == p/'high/dragr/tape30')
                self.assertEqual(high['inputs']['tape29'],p/'low/dragr/tape30')
                self.assertNotEqual(high['inputs']['tape29'],Path(row['original_library']))
                low_g = next(s for s in g if s['output'] == p/'low/groupr/tape30')
                self.assertEqual(low_g['inputs']['tape29'],p/'low/pendf/tape30')
            high_g = next(s for s in g if s['output'] == self.work/row['nuclide']/'control/high/groupr/tape30')
            self.assertEqual(high_g['inputs']['tape29'],Path(row['control_pendf']))

    def test_invalid_graph_refused(self):
        row = copy.deepcopy(self.rows[0]); row['route'] = 'UNKNOWN'
        with self.assertRaisesRegex(ValueError,'unknown route'):
            batch.stages(row,self.work)
        with patch.object(batch,'stages',return_value=[dict(label='bad',deck=Path(__file__),
                         inputs={'tape29':self.work/'future/tape30'},output=self.work/'bad/tape30')]):
            with self.assertRaisesRegex(ValueError,'future/missing'):
                batch.validate_graph([self.rows[0]],self.work)

    def test_no_approval_no_process(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(runner.sp,'Popen',side_effect=AssertionError('must not launch')):
            p = Path(tmp)
            with (p/'approval.json').open('x') as f:
                json.dump({'status':'PREPARED_NOT_AUTHORIZED'},f)
            with self.assertRaisesRegex(ValueError,'approval is missing'):
                runner.controller(p/'absent-runtime',p/'absent-work',p/'approval.json')
            self.assertFalse((p/'absent-work').exists())

    def test_terminal_refuses_partial_log(self):
        path = batch.ART/'d4a-fe56-actual-temperature-run-20260929/dragr/native.log'
        text = path.read_text()
        runner.native_terminal(text)
        with self.assertRaisesRegex(ValueError,'terminal'):
            runner.native_terminal(text.rsplit('\n',3)[0])
        with self.assertRaisesRegex(ValueError,'error marker'):
            runner.native_terminal('error in dragr\n'+text)

    def test_saved_single_pass_and_high_fuel_replay(self):
        for name in ('Cr52','Am241'):
            row = next(r for r in self.rows if r['nuclide'] == name)
            p = Path(row['original_library'])
            raw = (p.parent/('gendf_neutron_'+name)).read_bytes()
            deck = batch.PREP/name/('control/high/dragr.in' if row['expected_finite_dilutions']==18 else 'control/dragr.in')
            ss,thermal = batch.dragr_limits(deck,raw,row['mat'])
            self.assertEqual(ss,(25,281) if name == 'Cr52' else (51,281))
            self.assertEqual(thermal,85)
            records = batch.decode(p,True)
            result = batch.mt51.replay(raw,records,name,row['mat'],ss,thermal)
            self.assertEqual(result['records_checked'],300)
            # The original defective weighted tables are not required positive.
            # Numeric storage agreement is deliberately separate from that gate.
            self.assertEqual(batch.low_records_preserved(records,records,name),
                             sum(len(k)>=3 and k[0]==name and str(k[1]).startswith('SUBTMP')
                                 and str(k[2]).startswith('SUBMAT') for k in records))
            key = (name,'SUBTMP0001','SUBMAT0001','SCAT00')
            bad = dict(records)
            values = np.asarray(bad[key][1],dtype='f4').copy()
            index = int(np.argmax(abs(values)))
            values[index] = np.nextafter(values[index],np.float32(np.inf))
            bad[key] = (2,tuple(float(x) for x in values))
            with self.assertRaises(ValueError):
                batch.low_records_preserved(records,bad,name)


if __name__ == '__main__':
    unittest.main()
