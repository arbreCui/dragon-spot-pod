"""Execution reliability checks with fake children; never run OpenMC."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import ce_execution as ce


class Process:
    pid = 424242
    args = ['fake-native-child']

    def __init__(self):
        self.returncode = None

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        if self.returncode is None:
            self.returncode = 0
        return self.returncode


class ExecutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.artifacts = self.root/'artifacts'
        self.folder = self.artifacts/'experiment'/'AAA'
        self.folder.mkdir(parents=True)
        self.case = self.root/'case_spec.json'
        self.spec = dict(resource_caps=dict(ce_smoke_wall_s=120, ce_production_wall_s_per_case=1800,
            new_numeric_children_at_once=1, new_child_threads=1, automatic_retries_after_solver_failure=0,
            disk_min_free_GiB=8, new_case_artifact_budget_GiB=12),
            reference=dict(particles_per_batch=50000, inactive_batches=100, active_batches=250))
        self.case.write_text(json.dumps(self.spec))
        self.executable = self.root/'fake-openmc'
        self.executable.write_text('This fixture is never executed.\n')
        self.watchdog = self.root/'watchdog.py'
        self.watchdog.write_text('# Only mocked in execute tests.\n')
        self.manifest = self.folder/'execution.json'
        self.contract = dict(wall_seconds=120, threads=1, executable=str(self.executable),
            watchdog_source=str(self.watchdog), artifact_root=str(self.artifacts),
            resource_roots=[str(self.artifacts/'experiment')],
            case_spec=dict(path=str(self.case), sha256=ce.digest(self.case)), files={})
        self.pin_files = [Path(ce.__file__).resolve(), Path(ce.production_runner.__file__).resolve(),
                          Path(ce.production_inputs.__file__).resolve(), self.watchdog, self.executable, self.case]

    def seal(self):
        self.contract['files'] = {str(path):ce.digest(path) for path in self.pin_files}
        self.manifest.write_text(json.dumps(self.contract))
        return ce.digest(self.manifest)

    def helper(self, process):
        helper = Mock()
        helper.start_liveness_watchdog.return_value = object()
        helper.terminate_process_group.side_effect = lambda pid,grace,child:setattr(child,'returncode',-15)
        helper.finish_liveness_watchdog.side_effect = lambda fd,child:os.close(fd)
        return helper

    def test_insufficient_disk_does_not_claim_or_start(self):
        identity=self.seal()
        with patch.object(ce.production_runner.shutil,'disk_usage',return_value=SimpleNamespace(free=0)), \
             patch.object(ce.subprocess,'Popen') as start:
            with self.assertRaises(ce.ResourceFailure):
                ce.execute(self.manifest,identity)
        start.assert_not_called()
        self.assertFalse((self.folder/'run_claim.json').exists())
        self.assertFalse((self.folder/'openmc.log').exists())

    def test_runtime_budget_breach_terminates_only_owned_group(self):
        self.spec['resource_caps']['new_case_artifact_budget_GiB']=16384/2**30
        self.case.write_text(json.dumps(self.spec));self.contract['case_spec']['sha256']=ce.digest(self.case)
        identity=self.seal();process=Process();helper=self.helper(process)
        def launch(*args,**kwargs):
            self.assertTrue(kwargs['start_new_session'])
            (self.folder/'growing-output.h5').write_bytes(b'x'*32768)
            return process
        with patch.object(ce.production_runner.shutil,'disk_usage',return_value=SimpleNamespace(free=20*2**30)), \
             patch.object(ce,'load_watchdog',return_value=helper), \
             patch.object(ce.subprocess,'Popen',side_effect=launch) as start, \
             patch.object(ce.signal,'signal'):
            result=ce.execute(self.manifest,identity)
        self.assertEqual(result['status'],'FAIL_RESOURCE')
        self.assertEqual(result['returncode'],-15)
        self.assertIn('artifact budget',result['resources_failure']['reason'])
        self.assertEqual(start.call_count,1)
        helper.terminate_process_group.assert_called_once_with(process.pid,5.0,process)
        self.assertEqual(json.loads((self.folder/'native_result.json').read_text())['status'],'FAIL_RESOURCE')

    def test_success_cannot_be_claimed_twice(self):
        identity=self.seal();process=Process();helper=self.helper(process)
        with patch.object(ce.production_runner.shutil,'disk_usage',return_value=SimpleNamespace(free=20*2**30)), \
             patch.object(ce,'load_watchdog',return_value=helper), \
             patch.object(ce.subprocess,'Popen',return_value=process) as start, \
             patch.object(ce.signal,'signal'):
            self.assertEqual(ce.execute(self.manifest,identity)['status'],'NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS')
            with self.assertRaisesRegex(RuntimeError,'duplicate claim'):
                ce.execute(self.manifest,identity)
        self.assertEqual(start.call_count,1)
        helper.terminate_process_group.assert_not_called()

    def test_atomic_claim_race_does_not_start_a_second_child(self):
        identity=self.seal()
        def race(path):
            (self.folder/'run_claim.json').write_text('{"other_owner":true}')
            return Mock()
        with patch.object(ce.production_runner.shutil,'disk_usage',return_value=SimpleNamespace(free=20*2**30)), \
             patch.object(ce,'load_watchdog',side_effect=race), patch.object(ce.subprocess,'Popen') as start:
            with self.assertRaises(FileExistsError):
                ce.execute(self.manifest,identity)
        start.assert_not_called()

    def test_actual_imported_modules_must_be_pinned(self):
        self.pin_files.remove(Path(ce.production_inputs.__file__).resolve())
        identity=self.seal()
        with self.assertRaisesRegex(RuntimeError,'actual runtime/input file is not frozen'):
            ce.load_contract(self.manifest,identity)

    def test_changed_actual_production_runner_hash_refused(self):
        self.seal()
        self.contract['files'][str(Path(ce.production_runner.__file__).resolve())]='0'*64
        self.manifest.write_text(json.dumps(self.contract))
        with patch.object(ce.subprocess,'Popen') as start:
            with self.assertRaisesRegex(RuntimeError,'frozen input changed'):
                ce.execute(self.manifest,ce.digest(self.manifest))
        start.assert_not_called()

    def test_explicit_resource_root_and_output_coverage_required(self):
        del self.contract['artifact_root'];identity=self.seal()
        with self.assertRaisesRegex(RuntimeError,'explicitly declare artifact_root'):
            ce.load_contract(self.manifest,identity)
        self.contract['artifact_root']=str(self.artifacts)
        self.contract['resource_roots']=[str(self.artifacts/'unrelated')];identity=self.seal()
        with self.assertRaisesRegex(RuntimeError,'do not cover'):
            ce.load_contract(self.manifest,identity)
        self.contract['resource_roots']=[str(self.artifacts/'experiment'),str(self.folder)];identity=self.seal()
        with self.assertRaisesRegex(RuntimeError,'overlap'):
            ce.load_contract(self.manifest,identity)

    def test_5400_addendum_bound_to_current_case_and_sample_counts(self):
        supplement=dict(schema='AXMAT_CE_RESOURCE_ADDENDUM_V1',status='PREDECLARED_BEFORE_FORMAL_CE_TRANSPORT',
            case_spec_sha256=ce.digest(self.case),formal_ce_wall_seconds_per_case=5400,automatic_retries=0,
            threads=1,new_numeric_children_at_once=1,formal_particles_per_batch=50000,
            formal_inactive_batches=100,formal_active_batches=250)
        path=self.root/'resource_addendum.json';path.write_text(json.dumps(supplement))
        self.pin_files.append(path);self.contract.update(wall_seconds=5400,resource_addendum=str(path))
        identity=self.seal()
        with patch.object(ce.production_runner.shutil,'disk_usage',return_value=SimpleNamespace(free=20*2**30)):
            self.assertEqual(ce.load_contract(self.manifest,identity)[0]['wall_seconds'],5400)
        self.spec['experiment_id']='new-rank1-case';self.case.write_text(json.dumps(self.spec))
        self.contract['case_spec']['sha256']=ce.digest(self.case);identity=self.seal()
        with self.assertRaisesRegex(RuntimeError,'addendum does not admit'):
            ce.load_contract(self.manifest,identity)
        supplement['case_spec_sha256']=ce.digest(self.case);supplement['formal_active_batches']=249
        path.write_text(json.dumps(supplement));identity=self.seal()
        with self.assertRaisesRegex(RuntimeError,'addendum does not admit'):
            ce.load_contract(self.manifest,identity)

    def test_copied_three_file_bundle_uses_declared_artifact_root(self):
        runtime=self.artifacts/'runtime';runtime.mkdir()
        originals=[Path(ce.__file__).resolve(),Path(ce.production_runner.__file__).resolve(),Path(ce.production_inputs.__file__).resolve()]
        for path in originals:
            shutil.copyfile(path,runtime/path.name)
            self.pin_files.remove(path);self.pin_files.append(runtime/path.name)
        self.spec['resource_caps']['disk_min_free_GiB']=1/2**30
        self.case.write_text(json.dumps(self.spec));self.contract['case_spec']['sha256']=ce.digest(self.case)
        identity=self.seal()
        checked=subprocess.run([sys.executable,'-B',str(runtime/'ce_execution.py'),str(self.manifest),
                                '--sha256',identity,'--check'],capture_output=True,text=True,timeout=10)
        self.assertEqual(checked.returncode,0,checked.stderr)
        self.assertEqual(json.loads(checked.stdout)['artifact_root'],str(self.artifacts))
        self.assertFalse((self.folder/'run_claim.json').exists())
        self.assertFalse((self.folder/'openmc.log').exists())


if __name__=='__main__':
    unittest.main()
