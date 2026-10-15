"""Short synthetic checks; no native engines and no real experiment writes."""
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

import numpy as np
import check_d4a_material_candidate as q
import run_d4a_material_candidate as run


def log(temperature=650):
    return ('\n'.join('->@BEGIN MODULE : '+m for m in ('LIB:', 'SALT:', 'TONE:', 'EQU:'))+
        f'\nCONVERGENCE REACHED AT TONE ITERATION = 4 ERROR = 4.513E-06\n'
        f'D4A-ACTUAL-MATERIAL{temperature}-COMPLETE\nnormal end of execution for dragon\n')


class MaterialChecks(unittest.TestCase):
    def test_original_terminal_and_module_scope(self):
        self.assertEqual(q.terminal(log(), 650)['tone_iteration'], 4)
        for wrong in (log().replace('4.513E-06', '1.1E-05'), log()+log(),
                      log()+'\n->@BEGIN MODULE : FLU:', log().replace('650-COMPLETE', '750-COMPLETE'),
                      log().replace('normal end of execution for dragon', 'failed')):
            with self.subTest(wrong=wrong):
                with self.assertRaises(ValueError):
                    q.terminal(wrong, 650)

    def test_two_matrix_expanders_retain_signed_p1(self):
        row = {'NJJS01': (1, 2), 'IJJS01': (1, 2), 'SCAT01': (-0.25, 0.5, -0.75)}
        a = q.matrix(row, 1, 2)
        self.assertTrue(q.exact(a, [[-0.25, 0], [-0.75, 0.5]]))
        self.assertFalse(q.exact(a, np.maximum(a, 0)))
        with self.assertRaises((ValueError, AssertionError)):
            q.matrix(dict(row, SCAT01=(1.,)), 1, 2)

    def test_masked_scalar_not_forced_to_final_micro(self):
        initial = [[1, 2, 3, 4], [5, 6, 7, 8]]
        returned = [[9, 10, 11, 12], [13, 14, 15, 16]]
        result = q.masked_scalar(initial, returned, [1., 0.5], [1, 1], 2, 3)
        self.assertTrue(q.exact(result[0], [3.5, 17, 18.5, 8]))
        self.assertFalse(q.exact(result, q.density_mix(returned, [1., 0.5], [1, 1])))

    def test_missing_higher_order_is_zero_not_p0(self):
        row = {'NJJS00': (1, 1), 'IJJS00': (1, 2), 'SCAT00': (2., 3.)}
        self.assertTrue(q.exact(q.matrix(row, 1, 2), np.zeros((2, 2))))
        self.assertFalse(q.exact(q.matrix(row, 1, 2), q.matrix(row, 0, 2)))
        with self.assertRaises(ValueError): q.matrix(dict(row, SIGS01=(0., 0.)), 1, 2)

    def test_density_is_separately_rounded_and_ordered(self):
        v = [[2**24], [1.], [-2**24]]
        self.assertTrue(q.exact(q.density_mix(v, [1., 1., 1.], [1, 1, 1])[0], [0.]))
        with self.assertRaises(ValueError):
            q.density_mix(v, [1., 1., -1.], [1, 1, 1])

    def test_temperature_and_mo_routes_fail_closed(self):
        refs = ['Mo92']*14+['Na23']*45
        meta = {('ISOTOPERNAME',): (3, ''.join(f'{n:<12}' for n in refs)),
                ('ISOTOPESUSED',): (3, 'fixed aliases'), ('ISOTOPESMIX',): (1, (1,)*59),
                ('ISOTOPESDENS',): (2, (1.,)*59), ('ISOTOPESTEMP',): (2, (748.15,)*59),
                ('ENERGY',): (2, (10., 1.)),
                ('SHIBA', 'STATE-VECTOR'): (1, (25, 281, 20)),
                ('SHIBA', 'EPS-SHIBA'): (2, (1e-5,)),
                ('SHIBA', 'TCEPS-SHIBA'): (2, (1e-3,)),
                ('ILIBRARYNAME',): (3, f'{"DLIB_ACTUAL":<64}{"DLIB8R1_370":<64}'),
                ('ILIBRARYINDX',): (1, (2,)*14+(1,)*45)}
        plan = {'temperature_routes': [dict(nuclide=n, temperature_K=748.15,
            locations=[dict(plane=1, index=i)]) for i, n in enumerate(refs, 1)]}
        self.assertEqual(q.route_check(meta, meta, plan, 1), refs)
        wrong = dict(meta); wrong[('ILIBRARYINDX',)] = (1, (1,)*59)
        with self.assertRaises(ValueError): q.route_check(wrong, meta, plan, 1)

    def test_complete_material_checker_and_physical_negative_cases(self):
        import hashlib
        groups = 370
        refs = ['Mo92']*14+['Na23']*45
        mixtures = tuple(i % 6 + 1 for i in range(59))
        energy = tuple(float(i) for i in range(371, 0, -1))
        sparse = {'NJJS00': (1,)*groups, 'IJJS00': tuple(range(1, groups+1)),
                  'SCAT00': (2.,)*groups, 'SIGS00': (2.,)*groups, 'NTOT0': (3.,)*groups}
        signed = dict(sparse, NJJS01=(1,)*groups, IJJS01=tuple(range(1, groups+1)),
                      SCAT01=(-0.25,)*groups, SIGS01=(-0.25,)*groups)
        meta = {('ISOTOPERNAME',): (3, ''.join(f'{n:<12}' for n in refs)),
                ('ISOTOPESUSED',): (3, 'synthetic aliases'), ('ISOTOPESMIX',): (1, mixtures),
                ('ISOTOPESDENS',): (2, (1.,)*59), ('ISOTOPESTEMP',): (2, (748.15,)*59),
                ('ISOTOPESDSN',): (2, (1e10,)*(59*groups)), ('ENERGY',): (2, energy),
                ('SHIBA', 'STATE-VECTOR'): (1, (25, 281, 20)),
                ('SHIBA', 'EPS-SHIBA'): (2, (1e-5,)), ('SHIBA', 'TCEPS-SHIBA'): (2, (1e-3,)),
                ('ILIBRARYNAME',): (3, f'{"DLIB_ACTUAL":<64}{"DLIB8R1_370":<64}'),
                ('ILIBRARYINDX',): (1, (2,)*14+(1,)*45)}
        plan = dict(energy_float32_sha256=hashlib.sha256(np.asarray(energy,dtype='<f4').tobytes()).hexdigest(),
            temperature_routes=[dict(nuclide=n, temperature_K=748.15,
                locations=[dict(plane=1,index=i)]) for i,n in enumerate(refs,1)])
        full = dict(meta); full[('ISOTOPESLIST',)] = (10, 59)
        for i, ref in enumerate(refs, 1):
            for key, value in (sparse if ref == 'Mo92' else signed).items():
                full[('ISOTOPESLIST', i, key)] = (1 if key.startswith(('NJJS','IJJS')) else 2, value)
        macro = {('synthetic',): (3, 'complete export')}
        full[('MACROLIB', 'synthetic')] = macro[('synthetic',)]
        p0 = tuple(2.*mixtures.count(m) for m in range(1,7))
        p1 = tuple(-.25*sum(ref=='Na23' and mix==m for ref,mix in zip(refs,mixtures)) for m in range(1,7))
        macro_rows = {g: dict(NJJS00=(1,)*6,IJJS00=(g,)*6,IPOS00=tuple(range(1,7)),SCAT00=p0,SIGS00=p0,
                             NJJS01=(1,)*6,IJJS01=(g,)*6,IPOS01=tuple(range(1,7)),SCAT01=p1,SIGS01=p1)
                      for g in range(1,371)}
        parsed = dict(groups=370,mixtures=6,rows=macro_rows)
        libraries = {}
        for ref, row in [('Mo92',sparse),('Na23',signed)]:
            library = {('ENERGY',):(2,energy),(ref,'TEMPERATURE'):(2,(293.,550.,748.15,900.,1200.))}
            for j in range(1,6):
                for key,value in row.items():
                    library[(ref,f'SUBTMP{j:04d}',key)] = (1 if key.startswith(('NJJS','IJJS')) else 2,value)
            libraries[ref] = library
        def decode(path, *_):
            name = Path(path).name
            if name == 'microlib.ascii': return full
            if name in ('metadata.ascii','meta1.ascii'): return meta
            if name == 'macro.ascii': return macro
            return libraries[name]
        with tempfile.TemporaryDirectory() as tmp, patch.object(q,'decode',side_effect=decode), \
             patch.object(q.nr,'macro',return_value=parsed):
            folder=Path(tmp); (folder/'material.log').write_text(log()); (folder/'macro.ascii').write_bytes(b'synthetic')
            ref_paths={name:Path(name) for name in libraries}
            result=q.analyze(folder,1,plan,ref_paths)
            self.assertEqual(len(result['microscopic']),59)
            self.assertTrue(all(r['thermal_P0_P1_exact'] for r in result['microscopic']))
            for key,value in [(('ISOTOPESLIST',15,'SCAT00'),(-1e-30,)*groups),
                              (('ISOTOPESLIST',15,'SCAT01'),(0.,)*groups),
                              (('ISOTOPESLIST',15,'SIGS00'),(3.,)*groups)]:
                old=full[key]; full[key]=(2,value)
                with self.subTest(key=key), self.assertRaises(ValueError): q.analyze(folder,1,plan,ref_paths)
                full[key]=old
        wrong = dict(meta); wrong[('ISOTOPESTEMP',)] = (2, (749.,)*59)
        with self.assertRaises(ValueError): q.route_check(wrong, meta, plan, 1)

    def test_declared_physical_scope(self):
        self.assertEqual(run.runtime_plan()['native_stages'], 3)
        self.assertEqual(run.runtime_plan()['temperatures_C'], [650, 750, 850])
        self.assertEqual((run.TOTAL, run.RESERVE), (1800, 300))
        plan = {'assets': {name: {'path': '/original/'+name} for name in
            ('full_library', 'rnr_cc.c2m', 'rnr_interpol.c2m', 'geometry.dat')}}
        sources = run.stage_inputs(plan, 650)
        self.assertEqual(sources['DLIB_ACTUAL'], run.BINARY)
        self.assertEqual(sources['DLIB8R1_370'], Path('/original/full_library'))
        self.assertEqual(len(sources), 7)

    def test_p0_sign_and_finiteness_have_no_fitted_tolerance(self):
        q.nonnegative_p0([np.asarray([[0., 1.]])], 'synthetic')
        for value in (-np.nextafter(np.float32(0), np.float32(1)), np.nan):
            with self.subTest(value=value), self.assertRaises(ValueError):
                q.nonnegative_p0([np.asarray([[value]])], 'synthetic')

    def test_new_authorization_required(self):
        good = dict(status='EXPLICIT_USER_APPROVAL', user_approval_text='批准', scope=run.SCOPE,
            runtime_manifest_sha256='frozen', driver_sha256='frozen', candidate_binary_sha256=run.BINARY_SHA,
            total_seconds=1800, review_reserve_seconds=300, native_stages=3,
            temperatures_C=[650, 750, 850], attempts=1, retry=False)
        with tempfile.TemporaryDirectory() as tmp, patch.object(run, 'sha', return_value='frozen'):
            path = Path(tmp)/'approval.json'
            path.write_text(json.dumps(good)); self.assertEqual(run.authorization(path), good)
            for key, value in [('status', 'AUTOMATIC_CONTINUATION'), ('total_seconds', 900),
                               ('native_stages', 30), ('retry', True), ('scope', run.lib.SCOPE),
                               ('temperatures_C', [650]), ('candidate_binary_sha256', 'changed')]:
                path.write_text(json.dumps(dict(good, **{key: value})))
                with self.subTest(key=key), self.assertRaises(ValueError): run.authorization(path)

    def test_first_native_failure_stops_all_later_states(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); work = root/'work'; work.mkdir(); control = root/'control'; control.mkdir()
            src = root/'input'; src.write_text('synthetic only')
            auth = control/'authorization.json'; auth.write_text('{}')
            plan = {'assets': {'Dragon': {'path': str(src), 'sha256': run.sha(src)}}}
            pins = {str(src): run.sha(src)}
            with patch.object(run, 'WORK', work), patch.object(run, 'CONTROL', control), \
                 patch.object(run, 'load', return_value=(plan, pins, {})), \
                 patch.object(run, 'authorization', return_value={}), \
                 patch.object(run, 'stage_inputs', return_value={'material.x2m': src}), \
                 patch.object(run.c.bounded, 'run', side_effect=RuntimeError('synthetic native failure')) as native:
                with self.assertRaisesRegex(RuntimeError, 'synthetic native failure'):
                    run.worker(time.monotonic()+5)
            self.assertEqual(native.call_count, 1)
            self.assertFalse((work/'material750').exists())
            self.assertFalse((work/'completed.json').exists())
            self.assertTrue((work/'result.sha256').exists())


if __name__ == '__main__':
    unittest.main()
