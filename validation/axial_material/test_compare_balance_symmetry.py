"""Independent fixtures for signed accounting and simultaneous mirror inference."""
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np

import compare_balance_symmetry as bs
import reference_statistics as rs


class BalanceSymmetry(unittest.TestCase):
    def setUp(self):
        self.rules=bs.predeclared_rules();self.rules['bootstrap_replicates']=400
        nr=8;nz=12
        profile=np.array([1,2,3,4,5,6,6,5,4,3,2,1.])
        rates=np.zeros((nr,nz,2))
        for region in range(nr):
            rates[region,:,0]=(region+1)*profile
            if 3<=region<=6:rates[region,:,1]=profile
        volumes=np.ones((nr,nz));d=float(rates[:,:,1].sum())
        row=np.array([-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6.])/10
        currents=np.tile(row,(nr,1))
        summary={'global_nufission':str(d),'current_telescoping_difference':'0',
            'escape_per_nufission':str((currents[:,-1].sum()-currents[:,0].sum())/d),
            'negative_outward_end_region_group_currents':'0','nonpositive_scalar_entries':'0',
            'minimum_group_scalar_flux':'.01','radial_regions':'8','axial_cells':'12','groups':'370'}
        self.production=dict(rates=rates,volumes=volumes,current=currents,z=np.linspace(0,150,13),
            denominator=d,exporter_denominator=d,summary=summary,nonpositive_group_count=0)
        cells=[dict(region=r+1,layer=z+1,physical_zone=z//4+1,composition='A',volume_cm3=1.) for z in range(nz) for r in range(nr)]
        self.contract=dict(case='AAA',region_layer_bins=cells,layer_bins=[{} for _ in range(nz)],
            plane_bins=[dict(z_cm=12.5*i,positive_normal='+z') for i in range(nz+1)])
        raw=rates.transpose(1,0,2).reshape(96,2)
        net=currents.sum(axis=0)
        partial=np.stack([-10+net/2,10+net/2],axis=-1)
        partial[0]=[net[0],0];partial[-1]=[0,net[-1]]
        self.batches=dict(rates=np.tile(raw,(250,1,1)),current=np.tile(net,(250,1)),partial=np.tile(partial,(250,1,1)))

    def test_symmetric_complete_accounting_passes_with_real_outward_escape(self):
        result=bs.compare(self.production,self.batches,self.contract,self.rules)
        self.assertEqual(result['status'],'PASS')
        self.assertTrue(all(v=='PASS' for v in result['checks'].values()))
        self.assertGreater(result['production']['bottom_outward_per_nufission'],0)
        self.assertEqual(result['production']['bottom_outward_per_nufission'],result['production']['top_outward_per_nufission'])
        self.assertEqual(len(result['ce']['simultaneous_family_labels']),116)
        self.assertIsNone(result['comparison']['accuracy_gate'])
        self.assertIn('NOT_ASSESSED',result['full_particle_balance'])

    def test_cross_method_current_difference_does_not_invent_accuracy_gate(self):
        scaled={key:value.copy() for key,value in self.batches.items()}
        scaled['current']*=2;scaled['partial']*=2
        result=bs.compare(self.production,scaled,self.contract,self.rules)
        self.assertEqual(result['status'],'PASS')
        self.assertGreater(max(abs(np.array(result['comparison']['signed_production_minus_ce']))),0)
        self.assertTrue(result['comparison']['report_only'])

    def test_zero_center_current_uses_profile_scale_not_local_relative_division(self):
        self.production['current'][0,6]=1e-8
        check=bs.evaluate_production(self.production,self.rules)
        self.assertEqual(check['checks']['production_mirror_symmetry'],'PASS')
        self.production['current'][0,6]=1e-3
        check=bs.evaluate_production(self.production,self.rules)
        self.assertEqual(check['checks']['production_mirror_symmetry'],'FAIL')

    def test_groupwise_end_sign_failure_is_not_hidden_by_outward_total(self):
        self.production['summary']['negative_outward_end_region_group_currents']='1'
        result=bs.evaluate_production(self.production,self.rules)
        self.assertGreater(result['total_escape_per_nufission'],0)
        self.assertEqual(result['checks']['production_end_current_signs'],'FAIL')

    def test_exporter_telescope_bound_is_strict_roundoff_not_fitted(self):
        result=bs.evaluate_production(self.production,self.rules)
        bound=result['accounting']['roundoff_bound']
        self.production['summary']['current_telescoping_difference']=str(2*bound/self.production['denominator'])
        self.assertEqual(bs.evaluate_production(self.production,self.rules)['checks']['production_telescoping'],'FAIL')
        self.production['summary']['current_telescoping_difference']=str(bound/2/self.production['denominator'])
        self.assertEqual(bs.evaluate_production(self.production,self.rules)['checks']['production_telescoping'],'PASS')

    def test_production_mirror_threshold_is_fixed_from_outer_gate(self):
        self.assertAlmostEqual(self.rules['symmetry_relative_tolerance'],2.5e-5,places=18)
        self.production['rates'][0,0,0]+=1e-2
        result=bs.evaluate_production(self.production,self.rules)
        self.assertEqual(result['checks']['production_mirror_symmetry'],'FAIL')

    def test_ce_persistent_source_asymmetry_is_inconclusive_not_physics_fail(self):
        self.batches['rates'][:,3,0]*=1.01
        result=bs.evaluate_ce(self.batches,self.contract,self.rules)
        self.assertEqual(result['checks']['ce_simultaneous_mirror_symmetry'],'INCONCLUSIVE_SOURCE_SYMMETRY')
        self.assertTrue(result['block_reports'][0]['outside_component_indices'])

    def test_ce_wrong_direction_or_sum_cannot_pass(self):
        self.batches['partial'][0,0,1]=.1
        result=bs.evaluate_ce(self.batches,self.contract,self.rules)
        self.assertEqual(result['checks']['ce_signed_partials_and_vacuum'],'FAIL')
        self.assertEqual(result['checks']['ce_net_equals_signed_partials'],'FAIL')

    def test_middle_face_is_included_in_ce_antisymmetry_family(self):
        self.batches['current'][:,6]=.1
        self.batches['partial'][:,6,1]+=.1
        result=bs.evaluate_ce(self.batches,self.contract,self.rules)
        self.assertEqual(result['checks']['ce_net_equals_signed_partials'],'PASS')
        self.assertEqual(result['checks']['ce_simultaneous_mirror_symmetry'],'INCONCLUSIVE_SOURCE_SYMMETRY')
        self.assertIn('net:F6+F6',result['simultaneous_family_labels'])

    def test_smoke_and_incomplete_blocks_are_refused(self):
        smoke={key:value[:20] for key,value in self.batches.items()}
        with self.assertRaises(rs.EvidenceError):bs.evaluate_ce(smoke,self.contract,self.rules)
        smoke_rules={**self.rules,'active_batches':20}
        with self.assertRaisesRegex(rs.EvidenceError,'only 4 blocks'):bs.evaluate_ce(smoke,self.contract,smoke_rules)

    def test_global_denominator_and_all_scores_share_one_resample(self):
        amplitude=np.random.default_rng(17).uniform(.5,2,250)
        noisy={key:value*amplitude.reshape(250,*([1]*(value.ndim-1))) for key,value in self.batches.items()}
        result=bs.evaluate_ce(noisy,self.contract,self.rules)
        self.assertEqual(result['checks']['ce_simultaneous_mirror_symmetry'],'PASS')
        np.testing.assert_allclose(result['normalized_net_plus_z_full_section'],self.batches['current'][0]/self.production['denominator'])

    def test_joint_band_controls_max_family_error_not_marginal_intervals(self):
        rng=np.random.default_rng(314)
        draws=rng.normal(size=(4000,60))
        result=bs.simultaneous_centered_band(np.zeros(60),draws,self.rules)
        q=result['critical_max_standardized_error']
        # A marginal normal 95% band has halfwidth about 1.96, far too narrow
        # for the maximum over 60 independent components.
        self.assertGreater(q,3)
        width=np.asarray(result['upper'])
        simultaneously_covered=np.mean(np.all(abs(draws)<=width,axis=1))
        self.assertGreaterEqual(simultaneously_covered,.95)
        self.assertLess(simultaneously_covered,.952)
        constant=bs.simultaneous_centered_band(np.array([.01]),np.full((400,1),.01),self.rules)
        self.assertFalse(constant['zero_vector_in_simultaneous_band'])

    def write_fixture(self,directory):
        p=self.production;rpath=directory/'p.regions.csv';fpath=directory/'p.faces.csv';spath=directory/'p.summary.txt'
        with rpath.open('w') as stream:
            writer=csv.writer(stream);writer.writerow(['radial_region','axial_cell','physical_zone','volume_cm3','integrated_flux','integrated_nufission','flux_per_global_nufission','nufission_fraction','nonpositive_group_flux_count'])
            for r in range(8):
                for z in range(12):
                    flux,nuf=p['rates'][r,z]
                    writer.writerow([r+1,z+1,z//4+1,1,flux,nuf,flux/p['denominator'],nuf/p['denominator'],0])
        with fpath.open('w') as stream:
            writer=csv.writer(stream);writer.writerow(['radial_region','face','z_cm','area_cm2','integrated_net_current_plus_z','current_per_global_nufission'])
            for r in range(8):
                for z in range(13):
                    current=p['current'][r,z]
                    writer.writerow([r+1,z,12.5*z,.08,current,current/p['denominator']])
        spath.write_text('\n'.join(f'{key}={value}' for key,value in p['summary'].items())+'\n')
        return rpath,fpath,spath

    def test_csv_reader_preserves_signs_and_rejects_denominator_repair(self):
        with tempfile.TemporaryDirectory() as temporary:
            paths=self.write_fixture(Path(temporary))
            actual=bs.read_production(*paths,self.rules)
            np.testing.assert_array_equal(actual['current'],self.production['current'])
            self.assertEqual(actual['denominator'],168)
            paths[2].write_text(paths[2].read_text().replace('global_nufission=168.0','global_nufission=169.0'))
            with self.assertRaisesRegex(rs.EvidenceError,'normalization summary'):bs.read_production(*paths,self.rules)

    def test_duplicate_face_and_wrong_mirror_material_are_refused(self):
        with tempfile.TemporaryDirectory() as temporary:
            paths=self.write_fixture(Path(temporary))
            with paths[1].open('a') as stream:stream.write(paths[1].read_text().splitlines()[1]+'\n')
            with self.assertRaisesRegex(rs.EvidenceError,'duplicate or incomplete'):bs.read_production(*paths,self.rules)
        self.contract['region_layer_bins'][0]['composition']='B'
        with self.assertRaisesRegex(rs.EvidenceError,'material/volume mirror'):bs.evaluate_ce(self.batches,self.contract,self.rules)

    def test_missing_evidence_cli_writes_inconclusive_without_transport(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory=Path(temporary);rules=directory/'rules.json';stats=directory/'stats.json';output=directory/'result.json'
            rs.write_json(rules,bs.predeclared_rules());rs.write_json(stats,rs.predeclared_rules())
            contract=directory/'contract.json';contract.write_text('{}')
            command=[sys.executable,'-B',str(Path(bs.__file__)),'compare','--rules',str(rules),'--statistics-rules',str(stats),
                '--contract',str(contract),'--statepoints',str(directory),'--production-regions',str(directory/'missing.csv'),
                '--production-faces',str(directory/'missing2.csv'),'--production-summary',str(directory/'missing.txt'),'--output',str(output)]
            subprocess.run(command,check=True,capture_output=True,text=True)
            result=json.loads(output.read_text())
            self.assertEqual(result['status'],'INCONCLUSIVE')
            self.assertFalse(result['transport_executed'])


if __name__=='__main__':unittest.main()
