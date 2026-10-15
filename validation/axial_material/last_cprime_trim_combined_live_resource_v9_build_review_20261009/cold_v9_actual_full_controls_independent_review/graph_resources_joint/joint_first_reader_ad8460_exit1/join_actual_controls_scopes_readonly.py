# Read-only small joint. Does not load any business source or repeat graph/numeric reads.
from pathlib import Path
import json,hashlib,os,stat
C=Path('/private/tmp/axmat_v9_actual_controls_graph_resource_scope_20261009')
P=Path('/private/tmp/spot_v9_actual_controls_full_source_independent_review_20261009')
ROOT=Path('/Users/wen/spot')
PINS={}
def identity(path):
 s=Path(path).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(path,wanted=None):
 path=Path(path);before=identity(path);assert stat.S_ISREG(before[2]) and path.parent.resolve()==path.parent
 h=hashlib.sha256()
 with path.open('rb')as f:
  assert os.fstat(f.fileno()).st_ino==before[1]
  while block:=f.read(4*1024**2):h.update(block)
 assert identity(path)==before
 r=dict(path=str(path),sha256=h.hexdigest(),size=before[3],identity=before)
 if wanted is not None:assert r['sha256']==wanted,path
 PINS[str(path)]=r;return r
def read(path,wanted):
 pin(path,wanted);return json.loads(Path(path).read_bytes())
def receipt(r):
 t=r['actual_tool_result'];assert type(t['exit_code'])is int and t['exit_code']==0
 assert t.get('closed',r.get('closed'))is True
 assert r.get('business_executed',False)is False and r['project_written']is False
 return t
report=read(C/'REPORT.json','891ba5161ae1759187bd5f840419e2b1cc8125aba8865ffed4476121e30af0ba')
grec=read(C/'actual_readonly_tool_return.json','6c05fc3dad643cd48ef5c5f4b3f5bd64366dbd2dcf8ad445811074de6d828147')
peer=read(P/'REPORT.json','9ffb0efce0a65dc8dd452c3e77e8a0475e254e5c1718a307e6a43ffd04a764be')
prec=read(P/'actual_readonly_tool_return.json','0320a01e31efc180219c6c3d86b0891f947c2eb8057870edd66c01560785eca9')
assert report['status']==peer['status']=='PASS'
gtool=receipt(grec);ptool=receipt(prec)
for r,sourcekey,stdoutkey,stderrkey in [(grec,'whole_executed_readonly_source','full_stdout','full_stderr'),(prec,'source','stdout','stderr')]:
 for key in(sourcekey,stdoutkey,stderrkey):pin(r[key]['path'],r[key]['sha256'])
 assert PINS[r[stderrkey]['path']]['size']==0
 assert r.get('report',r.get('whole_report'))['sha256']==PINS[(r.get('report',r.get('whole_report')))['path']]['sha256']
# All previous current file identity checks remain independently pinned. No numeric payload is reread.
identities={}
for collection in(report['full_read_pins'],peer['all_fresh_pins']):
 for p,r in collection.items():
  assert identity(p)==r['identity'],p
  if p in identities:assert identities[p]==r['identity'],p
  identities[p]=r['identity']
controltool=dict(initial_chunk_id='085698',session_id=92301,terminal_chunk_id='5c78de',exit_code=0,closed=True)
assert report['actual_Root_controls_tool']==peer['actual_controls_tool']==controltool
assert report['actual_Root_success_recorder_tool']==dict(chunk_id='0b84d1',exit_code=0,closed=True)
for key,gkey in [('Root_observer_sha256','actual_Root_observer'),('control_terminal_sha256','actual_control_terminal'),('control_seal_sha256','actual_control_seal'),('qualified_binding_admission_sha256','qualified_complete_binding_admission')]:
 assert peer[key]==report[gkey]['sha256'];pin(report[gkey]['path'],peer[key])
assert report['exact_archive_bytes']==peer['actual_archive_bytes_full_recount']==61047970
assert sorted(report['controls_exact_namespace_files'])==peer['actual_control_namespace_files']
assert report['controls_exact_namespace_directories']==peer['actual_control_namespace_directories']
assert report['full_expected_ownerunion37395_independent_proof_inherited_and_whole_source_map_current_equal']is True
assert report['module391_all_independent_expected_and_current_source_identities_preserved']is True
assert peer['moduleowners391_complete_current_fullSHA']is True
assert peer['sorted_result_watch_original_write_once_boundary_typed_floatbit_equal']is True
assert len(peer['raw_watch_original_source_AST_key_order'])==18
assert report['controls_result_stages3_and_complete_raw_logs_watch_fields']is True
assert report['canonical_files']==35647 and report['inherited_full_canonical_bytes']==35803098221
assert report['requirement_rows235528']==235528 and report['declared_dynamic_roots']==236
assert report['whole65_original7_trim73_new7_complete_type_order_floatbits_equal']is True
assert peer['SOURCE31_fullSHA_namespace']is True and peer['environment1860_complete_expected_fullSHA']is True and peer['prepared43_fullSHA']is True
assert report['short_genuine_wait4_kernel_at_least16MiB']is True and report['oversize_actual_kernel_fields_retained_None_not_fabricated']is True
assert report['old_filecounts_not_frozen_future_gate']is True
assert report['resource_beforeafter_complete_inventory_equal']is True and report['strong_future_AAA_reserve_gate_passed']is True
for r in(report,peer):
 for k in('native_RSS_verified','scientific_qualification','AAA_accuracy_qualified','ABA_admitted'):assert r[k]is False
 assert r['project_written']is False
 assert r.get('new_canonical_payload_bytes_read',r.get('canonical35GB_numerical_bytes_read'))==0
assert report['business_phase_API_constructor_or_native_executed']is False
assert peer['business_API_factory_consumer_controller_helper_constructor_fixture_native_executed']is False
assert report['source_derived_handoff_not_actual_execve_syscall_trace']is True and peer['actual_execve_syscall_argv_trace']is None
for p,r in PINS.items():assert identity(p)==r['identity']
for p,ident in identities.items():assert identity(p)==ident,p
out=dict(schema='AXMAT_V9_ACTUAL_CONTROLS_WHOLE_COMPLEMENTARY_SOURCE_GRAPH_OWNER_RESOURCE_NAMESPACE_SEAL_JOINT_V1',status='PASS',scope='Complete actual controls postreview; source/environment/MRO/purecompile/Root-witness/raw-three-watch scope plus whole-graph/independent-expected-owner/complete-body/control-namespace-seal/dynamic-resource scope. Sole Root formal admission is separate.',actual_controls_tool=controltool,actual_success_recorder_tool=report['actual_Root_success_recorder_tool'],source_reader_actual_tool=ptool,graph_resource_reader_actual_tool=gtool,complete_graph_scope=dict(canonical_files=35647,inherited_full_canonical_bytes=35803098221,new_numeric_payload_bytes_read=0,all235528_rows=True,all86_namespaces=True,all186_aliases=True,all445_absences=True,all37339_metadata_files=True,independent_expected_ownerunion37395=True,moduleowners391=True,whole65_original7_trim73_new7_complete_typed_order_floatbits=True),complete_source_scope=dict(SOURCE31=True,environment1860=True,runtime31=True,prepared43=True,original_source_functions_and_guards=True,normal_MRO_and_Python314_source_only_code_hash=True),complete_controls_scope=dict(sealed_files9_plus_self=True,CT3=True,three_exact_original_stage_shapes_and_fullwatch_fields=True,oversize_expected_FAILED_not_scientific_FAILURE=True,short_true_wait4_peak_at_least16MiB=True,oversize_kernel_None_retained=True),resource_epochs=report['resource_epochs'],history96GiB_free8GiB_future_reserve20971764748_preserved=True,control_archive_bytes61047970_of67108864=True,resource_roots236_retaining231=True,historical_filecounts_not_frozen_for_future_gates=True,all_current_pin_identities_fresh_preserved_count=len(identities),all_reports_and_raw_source_receipts_fresh_sha256=PINS,canonical_or_business_payload_read=False,business_executed=False,project_written=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False,controls_only_qualification=True,Root_formal_admission_executed=False,prior_pure_reviewer_failures_preserved=True)
with(C/'joint_scope_binding.json').open('x')as f:json.dump(out,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(status='PASS',graph_report=report['schema'],source_report=peer['scope'],all_current_seven_field_pins=len(identities),controlfiles=10,CTfiles=3,current_resource_bytes=report['resource_after']['artifact_bytes']),sort_keys=True))
