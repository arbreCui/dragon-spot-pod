"""Synthetic statistical-contract tests; no particle transport or fitted gates."""
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

import reference_statistics as rs


class BlockStatistics(unittest.TestCase):
    def setUp(self):
        self.rules=rs.predeclared_rules()
        # Unit tests exercise the same formulas with fewer bootstrap draws.
        self.rules['bootstrap_replicates']=300
        self.volumes=np.array([2.,1.,2.,1.,2.,1.])
        self.regions=np.array([1,4,1,4,1,4])
        self.zones=np.array([1,1,2,2,3,3])
        self.axial=self.zones.copy()
        self.base=np.array([[3.,0.],[5.,1.],[4.,0.],[7.,2.],[3.,0.],[5.,1.]])
        self.rates=np.tile(self.base,(250,1,1))
        self.history={'k_generation':np.full(350,1.4),'entropy':np.full(350,4.)}

    def analyze(self,**changes):
        args=dict(batch_rates=self.rates,volumes=self.volumes,regions=self.regions,zones=self.zones,
                  axial_cells=self.axial,production_rates=self.base,production_volumes=self.volumes,
                  k_reference=1.4,sigma_k_reference=0.0001,k_production=1.4,
                  history=self.history,rules=self.rules)
        args.update(changes)
        return rs.analyze_batches(**args)

    def test_difference_uses_cumulative_sums_and_first_realization(self):
        raw=np.array([[[2.,3.]],[[5.,7.]],[[11.,13.]]])
        np.testing.assert_array_equal(rs.incremental_batches(raw.cumsum(axis=0),[1,2,3]),raw)
        with self.assertRaises(rs.EvidenceError):rs.incremental_batches(raw,[2,3,4])
        with self.assertRaises(rs.EvidenceError):rs.incremental_batches(raw,[1,3,4])

    def test_no_truncated_tail_or_fewer_than_twenty_blocks(self):
        self.assertEqual(rs.contiguous_blocks(self.rates,10).shape,(25,6,2))
        for values,length in [(self.rates[:249],10),(self.rates[:20],5),(self.rates,0)]:
            with self.assertRaises(rs.EvidenceError):rs.contiguous_blocks(values,length)

    def test_joint_denominator_cancels_perfect_common_amplitude_noise(self):
        amplitude=np.random.default_rng(11).uniform(.2,2.0,250)
        rates=self.rates*amplitude[:,None,None]
        result=self.analyze(batch_rates=rates)
        self.assertEqual(result['status'],'PASS')
        self.assertLess(max(result['conservative_upper_95']),1e-12)
        # Raw uncertainty is nonzero, while the paired normalized uncertainty cancels.
        self.assertGreater(np.std(rates[:,1,1]),.1)
        self.assertLess(result['block_reports'][0]['normalized_reference_covariance_trace']['nu_fission'],1e-25)

    def test_volume_weighted_flux_is_flux_not_fission(self):
        changed=self.base.copy();changed[:,0]*=1.02
        result=self.analyze(production_rates=changed)
        self.assertEqual(result['status'],'FAIL')
        np.testing.assert_allclose(result['point_discrepancies'],[.02,0],atol=1e-14)
        self.assertEqual(result['checks']['nu_fission'],'PASS')
        self.assertEqual(result['checks']['scalar_flux'],'FAIL')

    def test_fission_shape_uses_global_integral_not_per_layer_scaling(self):
        changed=self.base.copy();changed[1,1]*=1.2
        result=self.analyze(production_rates=changed)
        expected=abs((1.2/4.2)/(1/4)-1)
        self.assertAlmostEqual(result['point_discrepancies'][1],expected)
        self.assertEqual(result['checks']['nu_fission'],'FAIL')

    def test_determinism_and_refusal_of_bad_physical_arrays(self):
        a=self.analyze();b=self.analyze()
        self.assertEqual(a,b)
        for rates in [self.rates[:20],self.rates*np.nan,-self.rates]:
            with self.assertRaises(rs.EvidenceError):self.analyze(batch_rates=rates)
        with self.assertRaises(rs.EvidenceError):self.analyze(production_volumes=self.volumes*1.01)

    def test_entropy_and_inactive_bridge_are_required(self):
        for history in [{'k_generation':self.history['k_generation']},
                        {**self.history,'entropy':np.r_[np.full(100,3.),np.full(250,4.)]}]:
            result=self.analyze(history=history)
            self.assertEqual(result['status'],'INCONCLUSIVE')
            self.assertEqual(result['checks']['scalar_flux'],'INCONCLUSIVE')
            self.assertEqual(result['checks']['source_convergence_screen'],'INCONCLUSIVE')

    def test_axial_shape_drift_is_detected_even_with_constant_keff(self):
        drift=self.rates.copy()
        drift[125:,1,1]*=1.1;drift[125:,5,1]*=.9
        result=self.analyze(batch_rates=drift)
        self.assertEqual(result['status'],'INCONCLUSIVE')
        self.assertIn('block_5_source_history',result['inconclusive_reasons'])
        checks=result['block_reports'][0]['source_stationarity']['checks']
        self.assertFalse(checks['axial_cell_1_fission_proxy']['passed'])
        self.assertTrue(checks['k_generation']['passed'])

    def test_inadequate_resolution_cannot_be_promoted_to_pass(self):
        rng=np.random.default_rng(42)
        noisy=self.rates*np.exp(rng.normal(0,.5,self.rates.shape))
        result=self.analyze(batch_rates=noisy,production_rates=noisy.mean(axis=0))
        self.assertEqual(result['status'],'INCONCLUSIVE')
        self.assertEqual(result['checks']['statistical_resolution'],'INCONCLUSIVE')

    def test_keff_uses_reactivity_units_and_sigma_admission(self):
        result=self.analyze(sigma_k_reference=.001)
        self.assertAlmostEqual(result['k']['sigma_pcm'],1e5*.001/1.4**2)
        self.assertEqual(result['status'],'INCONCLUSIVE')
        result=self.analyze(k_production=1.5)
        self.assertEqual(result['checks']['keff'],'FAIL')
        self.assertEqual(result['status'],'FAIL')

    def test_signed_currents_reuse_joint_resampling_denominator(self):
        amplitude=np.random.default_rng(3).uniform(.5,1.5,250)
        currents=amplitude[:,None]*np.array([-.1,0,.1])
        result=self.analyze(batch_rates=self.rates*amplitude[:,None,None],batch_currents=currents)
        np.testing.assert_allclose(result['currents']['net_plus_z_per_nufission'],[-.025,0,.025])
        self.assertAlmostEqual(result['currents']['total_axial_escape'],.05)
        for report in result['block_reports']:
            np.testing.assert_allclose(report['current_per_global_nufission']['lower_05'],[-.025,0,.025])
        self.assertEqual(result['checks']['full_particle_balance'],'NOT_ASSESSED')

    def test_refined_cells_sum_raw_integrals_before_normalization(self):
        contract={'region_layer_bins':[
            {'region':4,'production_axial_cell':1,'physical_zone':1,'volume_cm3':.5},
            {'region':4,'production_axial_cell':1,'physical_zone':1,'volume_cm3':1.5}]}
        raw=np.array([[[2,1],[6,3]],[[4,2],[12,6]]],dtype=float)
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'regions.csv'
            path.write_text('radial_region,axial_cell,physical_zone,volume_cm3,integrated_flux,integrated_nufission,nonpositive_group_flux_count\n4,1,1,2,8,4,0\n')
            mapped=rs.mapped_comparison_inputs(contract,raw,path)
            np.testing.assert_array_equal(mapped[0],[[[8,4]],[[16,8]]])
            np.testing.assert_array_equal(mapped[1],[2])
            contract['region_layer_bins'][1]['physical_zone']=2
            with self.assertRaises(rs.EvidenceError):rs.mapped_comparison_inputs(contract,raw,path)


class CumulativeReader(unittest.TestCase):
    def test_actual_reader_schema_differences_and_signed_direction_reorder(self):
        class CellFilter:
            def __init__(self,bins):self.bins=bins
        class SurfaceFilter(CellFilter):pass
        class PolarFilter(CellFilter):pass
        class Tally:
            def __init__(self,filters,raw,n):
                self.filters=filters;self.raw=np.asarray(raw)*n
                self.num_realizations=n;self.nuclides=['total']
                self.scores=['flux','nu-fission'] if type(filters[0]) is CellFilter else ['current']
            def get_values(self,scores,value):
                assert value=='sum'
                return self.raw[...,{'flux':0,'nu-fission':1}[scores[0]]] if scores[0]!='current' else self.raw
        class SP:
            def __init__(self,path,autolink):
                self.current_batch=int(path.stem.split('.')[1]);n=self.current_batch-2
                self.n_realizations=n;self.run_mode='eigenvalue';self.n_batches=6
                self.n_inactive=2;self.n_particles=100;self.generations_per_batch=1;self.seed=7
                self.keff=SimpleNamespace(nominal_value=1.4,std_dev=.001)
                self.k_generation=np.full(6,1.4);self.entropy=np.full(6,4.)
                self.tallies={1:Tally([CellFilter([11,12])],[[2,1],[3,2]],n),
                    2:Tally([CellFilter([21])],[[5,3]],n),
                    3:Tally([SurfaceFilter([31,32,33])],[-2,1,3],n),
                    4:Tally([SurfaceFilter([31,32,33]),PolarFilter([[0,np.pi/2],[np.pi/2,np.pi]])],[[0,-2],[3,-2],[3,0]],n)}
            def get_tally(self,id):return self.tallies[id]
            def __enter__(self):return self
            def __exit__(self,*args):pass
        fake=SimpleNamespace(StatePoint=SP,CellFilter=CellFilter,SurfaceFilter=SurfaceFilter,PolarFilter=PolarFilter)
        contract={'schema':'AXMAT_CE_INPUT_V2','case':'AAA','statepoint_every_active_batch':True,
            'directional_current_filter':{'type':'polar','raw_bin_order':['positive_z','negative_z'],'signed_score':True},
            'region_layer_bins':[{'cell_id':11},{'cell_id':12}],
            'layer_bins':[{'cell_id':21,'region_tally_bins':[0,1]}],
            'plane_bins':[{'surface_id':31},{'surface_id':32},{'surface_id':33}],
            'tally_ids':dict(region_layer_rates=1,layer_rates=2,axial_plane_net_current=3,axial_plane_directional_current=4)}
        rules={**rs.predeclared_rules(),'active_batches':4,'inactive_batches':2,'particles':100,'seeds':{'AAA':7}}
        with tempfile.TemporaryDirectory() as temporary,patch.dict(sys.modules,{'openmc':fake}):
            directory=Path(temporary)
            for batch in range(3,7):(directory/f'statepoint.{batch:02}.h5').touch()
            batches,k,sigma,history,identities=rs.extract_statepoints(directory,contract,rules)
            np.testing.assert_array_equal(batches['rates'],np.tile([[2,1],[3,2]],(4,1,1)))
            np.testing.assert_array_equal(batches['partial'][0],[[-2,0],[-2,3],[0,3]])
            self.assertEqual(len(identities),4)
            contract['schema']='AXMAT_CE_INPUT_V1'
            with self.assertRaisesRegex(rs.EvidenceError,'MuSurface V1'):rs.extract_statepoints(directory,contract,rules)

    def test_missing_evidence_cli_writes_inconclusive_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory=Path(temporary);rules=directory/'rules.json';output=directory/'result.json'
            rs.write_json(rules,rs.predeclared_rules())
            contract=directory/'contract.json';contract.write_text('{}')
            command=[sys.executable,'-B',str(Path(rs.__file__)),'analyze','--rules',str(rules),
                     '--contract',str(contract),'--statepoints',str(directory),
                     '--production-regions',str(directory/'missing.csv'),
                     '--production-summary',str(directory/'missing.txt'),'--output',str(output)]
            subprocess.run(command,check=True,capture_output=True,text=True)
            result=json.loads(output.read_text())
            self.assertEqual(result['status'],'INCONCLUSIVE')
            self.assertFalse(result['transport_executed'])
            with self.assertRaises(FileExistsError):rs.write_json(output,{})


if __name__=='__main__':unittest.main()
