"""Independent sign assembly and white recovery against all sealed exact cases."""
import sys
import unittest
from pathlib import Path
import numpy as np
from qualify_native_directional import load_native
from exact_native_flight import compare
from native_oblique_full_action import evaluate,close_white
from native_oblique_streaming import ratio
from calibrate_native_oblique_streaming import read

ROOT=Path(sys.argv.pop(1)).resolve()


class FullActionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=load_native(ROOT/'inputs/track_data.bin')

    def setup_group(self,group):
        old=read(ROOT/f'inputs/green_{group}.npz');a=next(a for a in self.d['group_data'] if a['group']==group)
        g={k:np.stack([v,v]) for k,v in dict(volume=old['iso']+old['own'],jx=old['jx'],abs_jx=old['abs_jx'],boundary=old['boundary']).items()}
        inp=read(ROOT/f'inputs/prepared_{group}.npz');return a,g,inp

    def assert_compares(self,value,reference):
        metrics=compare(self.d,value,reference)
        for key,v in metrics.items():
            if 'induced_relative' in key:self.assertLess(float(v.max()),5e-12,key)

    def test_all_648_saved_inputs(self):
        for group in [51,61,98]:
            a,g,inp=self.setup_group(group);f=evaluate(self.d,a,g,inp['q'],inp['inflow'])
            self.assert_compares(f,read(ROOT/f'inputs/fixed_{group}.npz'))

    def test_all_201_common_white_cases(self):
        import json
        for group in [51,61,98]:
            a,g,inp=self.setup_group(group);f=evaluate(self.d,a,g,inp['q'],inp['inflow'])
            tags=json.loads((ROOT/f'inputs/cases_{group}.json').read_text());white=close_white(self.d,a,g,f,tags)
            self.assertEqual(white['q'].shape[-1],67);self.assert_compares(white,read(ROOT/f'inputs/white_{group}.npz'))
            self.assertGreaterEqual(white['boundary_inverse'].min(),0)

    def test_independent_axial_signs(self):
        a,g,inp=self.setup_group(61);f=evaluate(self.d,a,g,inp['q'],inp['inflow'])
        flipped=evaluate(self.d,a,g,inp['q'][::-1],inp['inflow'][::-1])
        self.assertLess(float(ratio(f['phi']-flipped['phi'],f['phi_scale']).max()),5e-12)
        self.assertLess(float(ratio(f['jz']+flipped['jz'],f['jz_scale']).max()),5e-12)
        self.assertGreater(float(abs(f['jz']).max()),0)


if __name__=='__main__':unittest.main()
