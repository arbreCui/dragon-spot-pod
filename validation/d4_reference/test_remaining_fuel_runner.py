"""Authorization and synthetic one-shot orchestration, never native physics."""
from contextlib import ExitStack
import json
from pathlib import Path
import shutil
import tempfile
import time
import unittest
from unittest.mock import patch

import run_remaining_fuel_temperatures as r


class FuelRunnerTests(unittest.TestCase):
    def valid_auth(self):
        return dict(status='EXPLICIT_USER_APPROVAL',user_approval_text='TEST_ONLY_NOT_A_REAL_APPROVAL',
            prepared_manifest_sha256=r.SEAL,driver_sha256=r.sha(Path(r.__file__)),scope=r.SCOPE,
            native_stages=83,cached_stages=5,total_seconds=28800,review_reserve_seconds=600,
            attempts=1,retry=False)

    def test_invalid_approval_never_launches(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(r.c.sp,'Popen',side_effect=AssertionError('no launch')):
            path = Path(tmp)/'authorization.json'
            for field,value in [('status','PREPARED'),('user_approval_text',''),('native_stages',84),
                                ('cached_stages',4),('total_seconds',28801),('retry',True),
                                ('driver_sha256','0'*64),('prepared_manifest_sha256','0'*64)]:
                auth = self.valid_auth(); auth[field] = value
                path.write_text(json.dumps(auth))
                with self.assertRaises(ValueError):
                    r.controller(path)

    def test_saved_preflight_without_launch(self):
        with patch.object(r.c.sp,'Popen',side_effect=AssertionError('no launch')):
            plan,pins = r.load()
        self.assertEqual(len(plan['stages']),83)
        self.assertIn(plan['candidate_executable'],pins)
        self.assertIn(plan['candidate_dylib'],pins)

    def test_cached_am241_real_control_replay(self):
        """Relocate accepted data as the worker does, then use the real checker."""
        with tempfile.TemporaryDirectory() as tmp, patch.object(r.c.sp,'Popen',side_effect=AssertionError('no launch')):
            work = Path(tmp)
            plan,pins = r.load()
            copied = {}
            for item in plan['reused_stages']:
                # The checker reads the four GENDF/DRAGLIB outputs, not PENDF.
                if item['kind'] == 'pendf':
                    continue
                source = Path(item['source_directory'])/'tape30'
                target = work/item['label']/'tape30'
                target.parent.mkdir(parents=True)
                shutil.copyfile(source,target)
                self.assertEqual(r.sha(target),pins[str(source)])
                copied[str(target)] = pins[str(source)]
            row = next(row for row in plan['cases'] if row['nuclide'] == 'Am241')
            actual = r.b.control_check(row,work)
            accepted = json.loads((r.prep.am.WORK/'control_check.json').read_text())
            self.assertEqual(actual,{key:accepted[key] for key in actual})
            self.assertEqual(actual['non_scatter_records_exact'],823)
            self.assertEqual(actual['low_records_retained'],630)
            self.assertEqual(len(actual['finite_weighted_tables']),90)
            self.assertEqual(actual['high_or_single_replay']['records_checked']+
                             actual['low_replay']['records_checked'],600)
            r.verify(copied)
            r.verify(pins)

    def fixture(self, root):
        work,control = root/'work',root/'control'
        work.mkdir(); control.mkdir()
        (control/'authorization.json').write_text('{}\n')
        common_input = root/'fixture-input'; common_input.write_text('synthetic only\n')
        pins = {str(common_input):r.sha(common_input)}
        native,cached = r.prep.graph(work)
        for item in native:
            item['deck'] = str(common_input)
            item['inputs'] = {k:(v if Path(v).is_relative_to(work) else str(common_input))
                              for k,v in item['inputs'].items()}
        for item in cached:
            source = root/'cache'/item['label']; source.mkdir(parents=True)
            (source/'tape30').write_text('SYNTHETIC CACHE\n')
            (source/'native.log').write_text('njoy synthetic fixture\n 0.0s\n ********************\n')
            (source/'receipt.json').write_text(json.dumps(dict(returncode=0,elapsed_s=0,
                output_sha256=r.sha(source/'tape30'))))
            item['source_directory'] = str(source)
            for name in item['copy_files']:
                pins[str(source/name)] = r.sha(source/name)
        plan = dict(stages=native,reused_stages=cached,cases=r.prep.rows(),
                    candidate_executable=str(common_input),candidate_dylib=str(common_input))
        return work,control,plan,pins

    def exercise_worker(self, fail=False):
        with tempfile.TemporaryDirectory() as tmp:
            work,control,plan,pins = self.fixture(Path(tmp))
            labels = []
            def fake_run(executable,deck,log,timeout):
                self.assertGreater(timeout,0)
                labels.append(str(deck.parent.relative_to(work)))
                if fail:
                    raise RuntimeError('synthetic first-stage refusal')
                log.write_text('njoy synthetic fixture\n 0.0s\n ********************\n')
                (deck.parent/'tape30').write_text('SYNTHETIC OUTPUT '+labels[-1]+'\n')
            with ExitStack() as stack:
                for obj,field,value in [(r,'WORK',work),(r,'CONTROL',control)]:
                    stack.enter_context(patch.object(obj,field,value))
                stack.enter_context(patch.object(r,'load',return_value=(plan,pins)))
                stack.enter_context(patch.object(r,'authorization',return_value={}))
                stack.enter_context(patch.object(r.c.bounded,'run',side_effect=fake_run))
                stack.enter_context(patch.object(r.c.sp,'Popen',side_effect=AssertionError('no launch')))
                stack.enter_context(patch.object(r.b,'control_check',return_value={'status':'REPAIRED_FIVE_POINT_CONTROL_PASS'}))
                stack.enter_context(patch.object(r.b,'expanded_check',return_value={'synthetic_only':True}))
                stack.enter_context(patch('builtins.print'))
                if fail:
                    with self.assertRaisesRegex(RuntimeError,'first-stage refusal'):
                        r.worker(time.monotonic()+30)
                else:
                    r.worker(time.monotonic()+30)
            self.assertTrue((work/'result.sha256').exists())
            if fail:
                self.assertEqual(len(labels),1)
                self.assertFalse((work/'completed.json').exists())
            else:
                self.assertEqual(labels,[s['label'] for s in plan['stages']])
                self.assertFalse(any(s.startswith('Am241/control/') for s in labels))
                self.assertEqual(len(json.loads((work/'output_hashes.json').read_text())),88)
                self.assertEqual(json.loads((work/'completed.json').read_text())['native_stages'],83)
            r.verify(pins)

    def test_83_stages_with_five_cached_not_recomputed(self):
        self.exercise_worker()

    def test_first_failure_preserved_without_retry(self):
        self.exercise_worker(fail=True)


if __name__ == '__main__':
    unittest.main()
