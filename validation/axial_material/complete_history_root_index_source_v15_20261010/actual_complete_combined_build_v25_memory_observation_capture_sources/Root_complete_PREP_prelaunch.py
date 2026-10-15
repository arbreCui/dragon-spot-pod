import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import time

R=Path('/Users/wen/spot')
B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
ART=R/'validation/artifacts'
D=B/'actual_complete_combined_prepare_v25_memory_observation_capture_sources'
E=B/'actual_complete_combined_prepare_v25_memory_observation_capture_receipts'
C=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_memory_observation_capture.py'
H=ART/'axial-material-complete-combined-prepare-host-v25-memory-observation-capture-20261010'
S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-memory-observation-capture-20261010'
O=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-20261010'
T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-memory-observation-capture-20261010'
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,w=None):
    i=identity(p);assert stat.S_ISREG(i[2]) and not p.is_symlink()
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    assert identity(p)==i and (w is None or h==w)
    return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def frozen_D():
    f=json.loads((E/'Root_prelaunch_complete_source_freeze.json').read_bytes())
    files={};dirs={}
    for folder,dnames,names in os.walk(D,followlinks=False):
        p=Path(folder);assert not p.is_symlink() and stat.S_ISDIR(p.lstat().st_mode)
        dirs[str(p.relative_to(D))]=identity(p)
        for n in names:files[str((p/n).relative_to(D))]=pin(p/n)
    assert files==f['complete_files']
    assert dirs.pop('.')==f['source_root_identity']
    assert dirs==f['complete_directories']
    assert pin(C)==f['canonical_factory']
    return f
def regular_total():
    n=C.lstat().st_size
    for root in (H,S,O,T,D,E):
        if not root.exists():continue
        for folder,dirs,names in os.walk(root,followlinks=False):
            for name in names:
                s=(Path(folder)/name).lstat()
                if stat.S_ISREG(s.st_mode):n+=s.st_size
    return n

started=time.monotonic()
assert len(sys.argv)==1 and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None
assert Path(sys.executable).resolve()==Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
assert all(os.environ.get(k)=='1' for k in THREAD_KEYS)
frozen=frozen_D()

assert Path(__file__)==D/'Root_complete_PREP_prelaunch.py' and pin(Path(__file__))==frozen['complete_files']['Root_complete_PREP_prelaunch.py']
assert pin(D/'Root_poststage_Source_META_contract.py')==frozen['complete_files']['Root_poststage_Source_META_contract.py']
import Root_poststage_Source_META_contract as scope
assert Path(scope.__file__).resolve()==D/'Root_poststage_Source_META_contract.py'
request,installation=scope.installed_request(D,'PREP')
exact_prefix=scope.original_prefix_seven(request['bound']['roles'])
assert exact_prefix==installation['exact_original_host_prefix_seven_input_pins']
expected_host_inputs=exact_prefix+[scope.host_pin(frozen['complete_files'][k]) for k in sorted(frozen['complete_files'])]
assert len({q['path'] for q in expected_host_inputs})==len(expected_host_inputs) and all(set(q)=={'path','sha256','identity'} for q in expected_host_inputs)
for q in expected_host_inputs:scope.exact(q)
for p in (H,S,O,T):assert not os.path.lexists(p),str(p)
assert pin(D/'combined_prepare_host.py')==frozen['complete_files']['combined_prepare_host.py']
assert pin(D/'write_actual_prepare_terminal.py')==frozen['complete_files']['write_actual_prepare_terminal.py']
assert pin(C)==frozen['canonical_factory']
support_path=B/'actual_prepare_sources/prepare_cli_host_v15.py'
support_pin=pin(support_path,'3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7')
spec=importlib.util.spec_from_file_location('Root_v25_prelaunch_genuine_support',support_path)
support=importlib.util.module_from_spec(spec);sys.modules[spec.name]=support;spec.loader.exec_module(support)
helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'Root_v25_prelaunch_original619')
resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'Root_v25_prelaunch_original_resource')
full,production=helper.modules();helper.guard_admission(full)
assert full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)
assert Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT
inputs=[pin(support.TARGET,support.TARGET_SHA),pin(support.OUT/'seal.json','b6b3b1477835bd6e312ac833d4cc681e0b7ca15482964f88daf0edb581d60206'),pin(support.TERMINAL/'terminal_return.json','ad1d11d68f2ae052068bd6d752ce7b2d64c6cbfcf699713aa684cdc347655d7e'),pin(support.FULL,support.FULL_SHA),pin(support.PARENT,support.PARENT_SHA),pin(support.BOUNDED,support.BOUNDED_SHA),pin(R/'validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py','3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'),pin(B/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json','c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b')]
qwriter=B/'actual_joint_helper_admission_v25_receipts/Root_actual_joint_helper_META_admission_writer_tool_terminal_return.json'
qpeer=B/'actual_joint_helper_admission_v25_receipts/sealed_independent_actual_joint_Q_saved_META_review/REVIEW.json'
qretention=B/'actual_joint_helper_admission_v25_receipts/Root_actual_joint_Q_saved_META_peer_retention_record.json'
qwriterpin=pin(qwriter);qpeerpin=pin(qpeer,'e958262fdf80ab80ffcc38db2b7e83e1c937fdab3143372eddce2f327b85b7aa');qretentionpin=pin(qretention,'b0927681a39202e5d24d84b336c965a89a44de03cd9808664286433059ae3d2c')
qw=json.loads(qwriter.read_bytes());qt=qw['terminal_tool_return'];assert qw['closed'] is True and type(qt['exit_code']) is int and qt['exit_code']==0 and 'session_id' not in qt and qt['chunk_id']=='94520a'
qp=json.loads(qpeer.read_bytes());assert qp['schema']=='INDEPENDENT_V25_ACTUAL_JOINT_HELPER_Q_SAVED_META_REVIEW_V1' and qp['status']=='PASS_ACTUAL_JOINT_HELPER_Q_METADATA_ONLY' and qp['all_checks_typed_true'] is True and qp['blockers']==[] and qp['check_count']==48 and all(type(c['passed']) is bool and c['passed'] is True for c in qp['checks'])
assert qp['Root_actual_Q_pin']==inputs[-1] and qp['Root_actual_Q_writer_terminal_pin']==qwriterpin
inputs.extend([qwriterpin,qpeerpin,qretentionpin])
roots=resource.history_roots([str(p) for p in (H,S,O,T)],support.ART)
resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)
actual=resources.check()
assert actual['artifact_bytes']+2*2**30<96*2**30
assert actual['disk_free_bytes']-2*2**30>=8*2**30
assert regular_total()<2*2**30
assert frozen_D()==frozen
for q in inputs:assert pin(Path(q['path']))==q
assert pin(support_path)==support_pin
record=dict(exact_original_host_input_sources=expected_host_inputs,actual_original_host_ordered_input_count=len(expected_host_inputs),old_original142_input_count_is_provenance_only=True,actual_source_request=installation['installed_request'],schema='ROOT_V25_ACTUAL_COMPLETE_PREP_FINAL_PRELAUNCH_SOURCE_AND_GENUINE_RESERVE_CHECK_V1',full_SOURCE_freeze=pin(E/'Root_prelaunch_complete_source_freeze.json'),complete_SOURCE_file_count=len(frozen['complete_files']),complete_SOURCE_directory_count=len(frozen['complete_directories']),all_SOURCE_full_EOF_SHA7ID_unchanged=True,canonical=pin(C),actual_prerequisites=inputs,original_support= support_pin,original_helper=hpin,original_resource_factory=rpin,genuine_supervisor_MRO_unchanged=True,actual_original_dynamic_history_roots=roots,actual_original_resource_check=actual,complete_H_S_O_T_D_E_and_canonical_regular_bytes=regular_total(),complete_joint_archive_cap_bytes=2*2**30,original_host_internal_archive_scope=[str(p) for p in (H,S,O,D)],Root_additional_complete_joint_scope=[str(p) for p in (H,S,O,T,D,E,C)],whole_seconds=1800,stage_seconds=600,rss_mib=512,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0,metadata_writer_already_frozen=True,all_new_H_S_O_T_absent=True,PREP_or_build_launched=False,native_or_science_qualified=False,elapsed_seconds=time.monotonic()-started)
path=E/'Root_final_prelaunch_source_and_reserve_check.json'
with path.open('x') as f:json.dump(record,f,indent=2,allow_nan=False);f.write('\n')
assert regular_total()<2*2**30 and frozen_D()==frozen
print(json.dumps({'prelaunch':pin(path),'actual_resources':actual,'full_D_files':len(frozen['complete_files']),'full_D_dirs':len(frozen['complete_directories']),'complete_joint_bytes_after_report':regular_total(),'genuine_original_MRO_and_caps_unchanged':True,'PREP_or_build_executed':False}))
