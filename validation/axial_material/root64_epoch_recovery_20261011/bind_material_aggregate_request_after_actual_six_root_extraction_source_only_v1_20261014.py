"""Metadata-only aggregate command binder. Unknown extraction post/coverage protocol hard-refuses main."""
import argparse,hashlib,json,os,shlex,stat
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
M=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_material_evidence_six_root_validation_scope_source_v1_20261014')
DYNAMIC_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_material_evidence_six_root_validation_scope_source_v1_20261014/ROOT_REVIEWABLE_MATERIAL_EVIDENCE_DYNAMIC_INTERFACE_SOURCE_ONLY.json', 'sha256': '872c8d81fb7f7ae08caf8ecb4ecdc9356b4be23506666d9fe56674488e40aef8', 'size_bytes': 4013, 'identity': [16777229, 50163817, 33188, 1, 4013, 1791967313996890460, 1791967313996890460]}
REQUEST_BUILDER=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_material_evidence_six_root_validation_scope_source_v1_20261014/prepare_current_material_evidence_requests.py')
REQUEST_BUILDER_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_material_evidence_six_root_validation_scope_source_v1_20261014/prepare_current_material_evidence_requests.py', 'sha256': '29f946eba64fa0fe24e2a87bb9e730d92bf48bef8d37f612dd3bb83b61875ce0', 'size_bytes': 14998, 'identity': [16777229, 50163314, 33188, 1, 14998, 1791966656396213298, 1791966656396213298]}
OUT_CLI=M/'ROOT_REVIEWABLE_EXACT_AGGREGATE_REQUEST_AFTER_ACTUAL_SIX_ROOT_EXTRACTION_ARGV_20261014.json'
EXPECTED_POST_SCHEMA=None
EXPECTED_POST_STATUS=None
POST_COVERAGE_CANONICAL_FIELD=None
FUTURE_ACTUAL=dict(extraction_post=None,extraction_post_tools=None,independent_helper_coverage=None,aggregate_request=None,aggregate_report=None,GENDF_report=None)

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path):
 p=Path(path)
 if not p.is_absolute()or '..'in p.parts:raise RuntimeError('absolute canonical metadata path')
 for a in reversed(p.parents):
  if not stat.S_ISDIR(a.lstat().st_mode):raise RuntimeError('ordinary metadata ancestor')
 s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('bounded Source metadata fullEOF only')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened7')
  raw=f.read()
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('EOF7')
 if identity(p.lstat())!=identity(s):raise RuntimeError('after7')
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))

def exact(p):
 if pin(p['path'])!=p:raise RuntimeError('metadata complete fullPF')
 return json.loads(Path(p['path']).read_bytes())

def same7(p):
 s=Path(p['path']).lstat()
 if not stat.S_ISREG(s.st_mode)or identity(s)!=p['identity']:raise RuntimeError('explicit live current7 '+p['path'])

def term0(t):
 if type(t.get('exit_code'))is not int or t['exit_code']!=0 or t.get('session_id')is not None or not isinstance(t.get('output'),str):raise RuntimeError('actual original typed terminal0/no session')

def jsonpin(p):return json.dumps(p,separators=(',',':'))

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 roles=('extraction-host','Root-tools','Root-argv','post-review','post-tools','independent-extraction-review')
 for role in roles:
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 ap.add_argument('--request-output-dir',required=True);ap.add_argument('--future-host-output-dir',required=True)
 a=ap.parse_args()
 if EXPECTED_POST_SCHEMA is None or EXPECTED_POST_STATUS is None or POST_COVERAGE_CANONICAL_FIELD is None:raise RuntimeError('actual independent extraction post/coverage protocol required; unknown Source contract cannot run')
 pins={}
 for role in roles:
  attr=role.replace('-','_');p=pin(getattr(a,attr+'_summary'))
  if p['sha256']!=getattr(a,attr+'_sha256')or p['identity']!=json.loads(getattr(a,attr+'_seven_id')):raise RuntimeError('required actual full authority '+role)
  pins[role]=p
 dynamic=exact(DYNAMIC_PIN);builderpin=pin(REQUEST_BUILDER)
 if builderpin!=dynamic['request_builder_source_pin']or builderpin!=REQUEST_BUILDER_PIN or dynamic['schema']!='MATERIAL_EVIDENCE_SOURCE_INTERFACE_FUTURE_ACTUAL_REQUEST_REQUIRED_V1'or dynamic['required_actual_prefix']!='request'or len(dynamic['known_argv_prefix'])!=24:raise RuntimeError('actual unchanged published request-builder/dynamic24')
 sf=exact(dynamic['selected_source_freeze_pin']);hf=exact(dynamic['selected_host_freeze_pin'])
 if sf['schema']!='COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_ONLY_FREEZE_V1'or sf['candidate_executed']is not False or hf['schema']!='COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_ONLY_FREEZE_V1'or hf['candidate_executed']is not False or hf['host_source']!=dynamic['host_source_pin']:raise RuntimeError('immutable exact evidence Source/HF')
 host=exact(pins['extraction-host']);root=exact(pins['Root-tools']);ra=exact(pins['Root-argv']);post=exact(pins['post-review']);pt=exact(pins['post-tools']);coverage=exact(pins['independent-extraction-review'])
 term0(root['actual_terminal_return'])
 if root['observed_closed']is not True or type(root['original_integer_exit_code'])is not int or root['original_integer_exit_code']!=0 or shlex.split(root['exact_executed_command'])!=ra['exact_argv']or len(ra['exact_argv'])!=30 or ra['exact_argv'][:24]!=dynamic['known_argv_prefix']:raise RuntimeError('genuine exact extraction Root0/runtime30')
 v=ra['exact_argv'][24:]
 if v[0]!='--request-summary'or v[2]!='--request-sha256'or v[4]!='--request-seven-id':raise RuntimeError('original exact actual request triple')
 reqpin=pin(v[1])
 if reqpin['sha256']!=v[3]or reqpin['identity']!=json.loads(v[5]):raise RuntimeError('actual extracted request fullPF')
 request=exact(reqpin);manifestpin=request['actual_observation_manifest_pin'];manifest=exact(manifestpin)
 if request['schema']!='CURRENT_FORMAL_MATERIAL_LINEAGE_EVIDENCE_REQUEST_V1'or request['operation']!='extract'or request['complete_source_freeze_pin']!=dynamic['selected_source_freeze_pin']:raise RuntimeError('one original actual extraction request')
 if post['schema']!=EXPECTED_POST_SCHEMA or post['status']!=EXPECTED_POST_STATUS or post['failure']is not None or any(post[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted'))or post[POST_COVERAGE_CANONICAL_FIELD]!=pins['independent-extraction-review']:raise RuntimeError('genuine separate post and actual exact-schema coverage artifact')
 canonical={'actual_report_pin':pins['extraction-host'],'actual_Host_freeze_pin':dynamic['selected_host_freeze_pin'],'actual_Root_true_tool_return_pin':pins['Root-tools'],'actual_Root_argv_pin':pins['Root-argv']}
 if any(post[k]!=p for k,p in canonical.items()):raise RuntimeError('actual extraction post canonical authorities')
 for k in('actual_review_return','actual_postverification_return'):
  term0(pt[k])
  if json.loads(pt[k]['output'].strip().splitlines()[-1])['review_pin']!=pins['post-review']:raise RuntimeError('genuine post0 stdout exact reviewPF')
 if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0:raise RuntimeError('genuine post closed0')
 if host['schema']!='ACTUAL_CURRENT_FORMAL_MATERIAL_COMPLETE_EVIDENCE_GUARDED_ROOT_V1'or host['status']!='ACTUAL_COMPLETE_CURRENT_EVIDENCE_EXIT2_CLOSED_ONLY'or host['operation']!='extract'or host['failure']is not None or host['after_check_error']is not None or host['actual_intentional_exit2_normal_closure']is not True or len(host['records'])!=1:raise RuntimeError('original intentional exit2 extraction host, never fake childPASS')
 record=host['records'][0];watch=exact(host['actual_watchdog_full_pin'])
 if record['status']!='FAILED'or record['error']!='own-child stage failed; no retry'or type(watch['returncode'])is not int or watch['returncode']!=2 or watch['limit_failure']is not None or watch['command']!=record['command']or watch['own_child_only']is not True or watch['liveness_group_cleanup']is not True or watch['rss_cap_mib']!=512 or not 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 or not 0<=watch['sampled_peak_rss_mib']<512 or type(host['SELF_peak_bytes'])is not int or host['SELF_peak_bytes']>=512*2**20 or not 0<host['wall_seconds']<1800:raise RuntimeError('original stage2 deliberate exit/512/600/1800 facts')
 receipt=host['actual_complete_child_receipt'];reportpin=receipt['report'];extraction=exact(reportpin)
 loglines=Path(host['actual_log_full_pin']['path']).read_text().splitlines()
 if len(loglines)!=1 or json.loads(loglines[0])!=receipt:raise RuntimeError('full actual extraction stdout one-line receipt')
 if extraction['schema']!='ACTUAL_COMPLETE_OBSERVED_OLD_POST_FINAL_XSM_EXTRACTION_EVIDENCE_ONLY_V1'or extraction['actual_observation_manifest_pin']!=manifestpin or extraction['all_complete_state_scope_retained']is not True or extraction['state_order']!=['A']or manifest['state_order']!=['A']:raise RuntimeError('original complete extraction and same one A capture')
 state=manifest['states']['A'];pairs=[dict(event=r['event'],role=r['role'],root_prefix=r['root_prefix'],input_pin=r['input_pin'],sqlite_pin=r['paired_SQLite_pin'],native_pool_pin=r['paired_original_pool_pin'])for r in extraction['states']['A']]
 if not pairs or pairs[-1]['role']!='final-complete-micro':raise RuntimeError('full actual last final micro retained')
 if coverage['schema']!='ROOT_ACTUAL_CURRENT_MATERIAL_EXTRACTION_REVIEW_V1'or coverage['actual_extraction_report_pin']!=reportpin or coverage['actual_extraction_host_pin']!=pins['extraction-host']or coverage['actual_observation_manifest_pin']!=manifestpin or coverage['all_snapshot_pairs']!=pairs or coverage['complete_context_pins']!=state['complete_context_pins']or coverage['all_original_snapshot_and_context_pins_verified']is not True:raise RuntimeError('exact original independent helper coverage; no schema alias or fabricated qualification')
 live=host['fixed_current_pins']+host['complete_output_pins']+state['complete_observed_file_pins']+state['physical_input_pins']+[reportpin,manifestpin,reqpin]+list(pins.values())
 for row in pairs:
  for key in('input_pin','sqlite_pin','native_pool_pin'):live.append(row[key])
 for p in live:same7(p)
 req=Path(a.request_output_dir);future=Path(a.future_host_output_dir);child=future.with_name(future.name+'-evidence')
 if not req.is_absolute()or req.parent!=REC or req==M or not future.is_absolute()or future.parent!=Path(request['owning_host_output_directory']).parent or any(os.path.lexists(p)for p in(req,future,child)):raise RuntimeError('fresh three aggregate metadata/evidence namespaces')
 observed=Path(state['actual_cwd']).parent;completion=Path(manifestpin['path']).parent;roots=[str(future),str(child),str(observed),str(Path(dynamic['selected_source_freeze_pin']['path']).parent),str(req),str(completion)]
 for p in [str(Path(pins['extraction-host']['path']).parent),str(Path(reportpin['path']).parent)]:
  if p not in roots:roots.append(p)
 if len(set(roots))!=len(roots)or any(Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y):raise RuntimeError('original six plus both retained complete extraction outputs; no2GiB reset')
 argv=dynamic['known_argv_prefix'][:11]+[str(REQUEST_BUILDER),'aggregate','--source-freeze-pin',jsonpin(dynamic['selected_source_freeze_pin']),'--observation-manifest-pin',jsonpin(manifestpin),'--request-output-dir',str(req),'--future-host-output-dir',str(future),'--extraction-host-pin',jsonpin(pins['extraction-host']),'--independent-extraction-review-pin',jsonpin(pins['independent-extraction-review'])]
 if len(argv)!=25:raise RuntimeError('original aggregate request interface25: extract21 plus two actual pin options')
 for p in live:same7(p)
 value=dict(schema='ROOT_REVIEWABLE_EXACT_AGGREGATE_REQUEST_AFTER_ACTUAL_SIX_ROOT_EXTRACTION_ARGV_V1',exact_argv=argv,exact_command=shlex.join(argv),request_builder_source_pin=REQUEST_BUILDER_PIN,published_evidence_dynamic_interface_pin=DYNAMIC_PIN,actual_extraction_authority_pins=pins,actual_extraction_child_report_pin=reportpin,actual_observation_manifest_pin=manifestpin,actual_independent_extraction_helper_coverage_pin=pins['independent-extraction-review'],complete_joint_retained_roots=roots,original_joint2GiB_8GiB_96GiB_512_600_1800_unchanged=True,actual_aggregate_request_pin=None,actual_aggregate_report_pin=None,actual_GENDF_report_pin=None,request_builder_not_executed=True,aggregate_engine_not_executed=True,GENDF_not_executed=True,science_body_EOF_not_read_by_binder=True,current_runtime_budget_admission_not_issued=True,binder_source_pin=pin(Path(__file__).absolute()),business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False)
 raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
 with OUT_CLI.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status='AGGREGATE_REQUEST25_COMMAND_BOUND_SOURCE_ONLY_NO_AGGREGATION',CLI_pin=pin(OUT_CLI),actual_argv_count=25,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)

if __name__=='__main__':main()
