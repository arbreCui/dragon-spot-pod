"""Synthetic orchestration and exact-comparison failures; no native execution."""
from contextlib import ExitStack
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_d4a_material_candidate_library as r


class LibraryTests(unittest.TestCase):
    def test_physical_root_union_and_conflict(self):
        first = {('ENERGY',): (2, (2., 1.)), ('CHI-LIMITS',): (1, (0, 2)), ('README',): (3, 'Monday')}
        merged = dict(first)
        r.merge_roots(merged, {('ENERGY',): first[('ENERGY',)], ('README',): (3, 'Sunday')})
        self.assertEqual(merged[('CHI-LIMITS',)], first[('CHI-LIMITS',)])
        self.assertEqual(merged[('README',)], (3, 'Sunday'))
        with self.assertRaises(ValueError):
            r.merge_roots(merged, {('CHI-LIMITS',): (1, (0, 1))})
        with self.assertRaises(ValueError):
            r.merge_roots(merged, {('ENERGY',): (2, (2., 1.001))})

    def test_complete_record_changes_refused(self):
        original = {('SCAT01',): (2, (-0.1, 0.3)), ('DILUTION',): (2, (10., 1.))}
        for modified in ({('SCAT01',): original[('SCAT01',)]},
                         {**original, ('SCAT01',): (2, (0., 0.3))},
                         {**original, ('DILUTION',): (4, (10., 1.))}):
            with self.assertRaises(ValueError):
                r.c.API['equal_records'](original, modified)

    def test_export_is_format_only(self):
        rows = [{'nuclide': 'Am241'}, {'nuclide': 'Fe56'}]
        deck = r.export_deck(rows)
        for row in rows:
            self.assertIn('STEP UP '+row['nuclide'], deck)
            self.assertIn('DEL '+row['nuclide'], deck)
        self.assertNotIn('TONE:', deck)
        self.assertEqual(r.MERGE.splitlines()[1], '0 0 0 0 0 29 30 0 /')
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'log'
            path.write_text('->@BEGIN MODULE : TONE:\nnormal end of execution for dragon\nDONE')
            with self.assertRaises(ValueError):
                r.dragon_terminal(path, 'DONE')

    def test_bad_authorization_cannot_launch(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(r.c.sp, 'Popen', side_effect=AssertionError('no native launch')):
            root = Path(temp)
            (root/'result.sha256').write_text('synthetic only\n')
            receipt = root/'authorization.json'
            with patch.object(r, 'RUNTIME', root):
                valid = dict(status='EXPLICIT_USER_APPROVAL', user_approval_text='批准', scope=r.SCOPE,
                    prepared_manifest_sha256=r.SEAL, runtime_manifest_sha256=r.sha(root/'result.sha256'),
                    driver_sha256=r.sha(r.__file__), total_seconds=r.TOTAL, review_reserve_seconds=r.RESERVE,
                    native_stages=30, attempts=1, retry=False)
                for key, value in [('status', 'PREPARED'), ('scope', 'MATERIAL'), ('native_stages', 31),
                                   ('retry', True), ('total_seconds', 901), ('review_reserve_seconds', 181),
                                   ('driver_sha256', '0'*64), ('runtime_manifest_sha256', '0'*64)]:
                    receipt.write_text(json.dumps(dict(valid, **{key: value})))
                    with self.assertRaises(ValueError):
                        r.controller(receipt)

    def exercise(self, failure=False):
        with tempfile.TemporaryDirectory() as temp, ExitStack() as stack:
            root = Path(temp)
            work, control, runtime = root/'work', root/'control', root/'runtime'
            for folder in (work, control, runtime):
                folder.mkdir()
            (control/'authorization.json').write_text('{}')
            fixture = root/'runtime-fixture'; fixture.write_text('fixture only')
            pins = {str(fixture): r.sha(fixture)}
            rows = []
            for index in range(28):
                path = root/f'source{index:02d}'; path.write_text(f'SYNTHETIC {index}\n')
                rows.append(dict(nuclide=f'X{index:02d}', path=str(path), sha256=r.sha(path)))
                pins[str(path)] = r.sha(path)
            for name in ('merge.inp', 'import.x2m', 'export.x2m'):
                path = runtime/name; path.write_text('not executable fixture')
                pins[str(path)] = r.sha(path)
            plan = dict(sources=rows, assets={'Dragon': {'path': str(fixture)}})
            labels = []

            def fake(exe, deck, log, timeout):
                label = str(deck.parent.relative_to(work)); labels.append(label)
                if failure:
                    raise RuntimeError('synthetic refusal, no retry')
                self.assertGreater(timeout, 0)
                log.write_text('synthetic native log')
                if label.startswith('merge/'):
                    previous = deck.parent/'tape30'
                    before = previous.read_text() if previous.exists() else ''
                    previous.write_text(before+(deck.parent/'tape29').read_text())
                elif label == 'import':
                    (deck.parent/'DLIB_370_bin').write_text('synthetic binary')
                else:
                    for name in ['root']+[row['nuclide'] for row in rows]:
                        (deck.parent/f'{name}.ascii').write_text('synthetic subtree')

            for name, value in [('WORK', work), ('CONTROL', control), ('RUNTIME', runtime), ('EXE', fixture), ('DYLIB', fixture)]:
                stack.enter_context(patch.object(r, name, value))
            stack.enter_context(patch.object(r, 'load', return_value=(plan, pins, {})))
            stack.enter_context(patch.object(r, 'authorization', return_value={}))
            stack.enter_context(patch.object(r, 'check_saved', return_value={'synthetic_only': True}))
            stack.enter_context(patch.object(r, 'dragon_terminal'))
            stack.enter_context(patch.object(r.c, 'native_terminal'))
            stack.enter_context(patch.object(r.c.bounded, 'run', side_effect=fake))
            stack.enter_context(patch.object(r.c.sp, 'Popen', side_effect=AssertionError('no native launch')))
            stack.enter_context(patch('builtins.print'))
            if failure:
                with self.assertRaisesRegex(RuntimeError, 'no retry'):
                    r.worker(time.monotonic()+10)
                self.assertEqual(len(labels), 1)
                self.assertFalse((work/'completed.json').exists())
            else:
                r.worker(time.monotonic()+10)
                self.assertEqual(len(labels), 30)
                receipts = json.loads((work/'receipts.json').read_text())
                self.assertEqual(receipts[0]['mutable_input_preimages'], {})
                for old, new in zip(receipts[:27], receipts[1:28]):
                    self.assertEqual(new['mutable_input_preimages']['tape30'], old['outputs']['tape30'])
                r.verify(json.loads((work/'staged_inputs.json').read_text()))
            self.assertTrue((work/'result.sha256').exists())
            r.verify(pins)

    def test_thirty_stages_mutable_parent_chain(self):
        self.exercise()

    def test_first_error_stops_without_retry(self):
        self.exercise(failure=True)


if __name__ == '__main__':
    unittest.main()
