"""UNREADY independent metadata post for the actual tiny non-scientific readonly FD same-PID exec control.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Only Source and saved metadata are read. Old objects, Dragon and selected native payloads get current7 only. Only this new tiny control owning output may receive blind SHA twice after genuine Root closure.
The exact pre-GEN author freeze is bound below; actual execution remains NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_readonly_FD_same_PID_exec_control_source_v1_UNREADY/AUTHOR_SOURCE_FREEZE.json', 'sha256': '1dd24e717df4b3f9c881708896320b6836998dd9c44ed793597fa28f127f2780', 'size_bytes': 5096, 'identity': [16777229, 50956707, 33188, 1, 5096, 1792082792047424917, 1792082792047424917]}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(compiler_executed=False,native_executed=False,children_started_by_post=False,worker_or_guard_helpers_imported=False,original_plain_payload_body_opened=False,original_plain_payload_SHA_recomputed=False,gzip_payload_body_opened_by_post=False,compression_repeated=False,decompression_repeated=False,restored_product_file_written=False,scientific_values_decoded=False,files_deleted=False,retirement_authorized=False,paired_SQL_pool_archive_complete=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
START=time.monotonic()
def need(v,m):
 if type(v)is not bool or not v:raise RuntimeError(m)
def budget():
 need(time.monotonic()-START<600 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)<512*2**20,'metadata post stage600/SELF512')
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 budget();q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1 and ids(s)==p['identity']and s.st_size==p['size_bytes']and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'exact ordinary owned current7')
 return q
def full(p):
 q=current(p);h=hashlib.sha256();n=0
 with q.open('rb')as f:
  need(ids(os.fstat(f.fileno()))==p['identity'],'opened7')
  while b:=f.read(2**20):h.update(b);n+=len(b);budget()
  need(ids(os.fstat(f.fileno()))==p['identity'],'EOF7')
 need(n==p['size_bytes']and h.hexdigest()==p['sha256'],'blind whole-file SHA/length');current(p);return q
def pin(q):
 q=Path(q);s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  need(ids(os.fstat(f.fileno()))==ids(s),'opened new file7')
  while b:=f.read(2**20):h.update(b);budget()
  need(ids(os.fstat(f.fileno()))==ids(s),'new file EOF7')
 p=dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=ids(s));current(p);return p
def meta(p):
 need(p['size_bytes']<8*2**20,'only bounded control metadata8MiB is decoded')
 q=full(p);v=json.loads(q.read_bytes());full(p);return v
def genuine(v,key,p,field):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None and json.loads(t['output'].strip().splitlines()[-1])[field]==p,'genuine closed typed0 and exact output artifact PF')
def current_role(p,build):
 budget();q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes']and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'same exact inherited current7 without old payload read')
 if p in build['readonly_system_SDK_header_pins']:
  root=Path(build['readonly_system_SDK_root']);rs=root.lstat()
  need(str(root)=='/Library/Developer/CommandLineTools/SDKs/MacOSX27.0.sdk'and stat.S_ISDIR(rs.st_mode)and rs.st_uid==0 and ids(rs)==build['readonly_system_SDK_root_identity']and not any(x.is_symlink()for x in(root,*root.parents))and str(q)in{str(root/'usr/include'/n)for n in('stdio.h','stdlib.h','stdint.h')}and s.st_uid==0 and s.st_nlink==1,'only frozen selected readonly SDK headers current7')
 elif p in build['readonly_system_tool_metadata_pins']:
  need(str(q)in('/bin/ps','/usr/sbin/lsof')and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only explicitly frozen readonly PS/lsof roles')
 elif p==build['C_compiler_pin']:
  need(str(q)=='/Library/Developer/CommandLineTools/usr/bin/clang'and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only explicit frozen current readonly clang role')
 elif str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15':
  need(p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_uid==os.getuid()and s.st_nlink==p['identity'][3]==2,'only original frozen gfortran link exception')
 else:need(s.st_uid==os.getuid()and s.st_nlink==1,'same owned ordinary inherited role')
def all_output_pins(out):
 rows=[]
 if not os.path.lexists(out):return rows
 need(out.is_dir()and not any(x.is_symlink()for x in(out,*out.parents)),'literal fresh current B55 control output')
 for q in sorted(out.rglob('*')):
  s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no new output alias')
  if stat.S_ISREG(s.st_mode):p=pin(q);full(p);rows.append(p)
  else:need(stat.S_ISDIR(s.st_mode),'ordinary new output files/directories only')
 return rows
def counted_bytes(roots):
 total=0
 for value in roots:
  root=Path(value);need(root.is_absolute()and not any(x.is_symlink()for x in(root,*root.parents)),'literal counted root')
  if not os.path.lexists(root):continue
  need(root.is_dir(),'counted root directory')
  for q in root.rglob('*'):
   budget();s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no alias in full counted scope')
   if stat.S_ISREG(s.st_mode):total+=s.st_size
 return total
def unlinked_bytes():
 rows={}
 for name in os.listdir('/dev/fd'):
  try:s=os.fstat(int(name))
  except(ValueError,OSError):continue
  if stat.S_ISREG(s.st_mode)and s.st_nlink==0:rows[s.st_dev,s.st_ino]=s.st_size
 return sum(rows.values())
def member0_resource_facts(v,roots):
 need(v['SELF_peak_bytes']<512*2**20 and 0<=v['original_elapsed_seconds']<600 and v['complete_joint_root_count']==len(roots)and v['non_scalar_resource_inventories_omitted']is True,'actual original Root-only SELF512/stage600 and scalar snapshots for entire bound root topology')
 h=v['original_history'];j=v['complete_joint']
 need(j['artifact_bytes']+v['explicit_external_metadata_bytes']+v['own_open_unlinked_bytes']<2*2**30 and h['artifact_bytes']+20971764748+64*2**20<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual saved original cumulative/history/cold/metadata/free caps')
def save(report,source_limit,joint_existing=None):
 report.update(metadata_only=True,Source_author_task=AUTHOR,actual_executor_task=EXECUTOR,actual_post_not_executed_by_Source_author=True,reviewer_Source_pin=pin(Path(__file__).absolute()),helper_or_candidate_module_imported=False,Source_GEN_or_publication_executed=False,native_or_compiler_or_worker_executed=False,scientific_values_or_SQLite_or_native_XSM_or_context_body_decoded=False,original_collect_or_snapshot_pair_readback_repeated=False,historical_issue_records_modified=False,wall_seconds=time.monotonic()-START,**FALSE)
 raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'post control report6MiB')
 need(counted_bytes([str(PACKAGE)])+len(raw)<source_limit,'entire Source/metadata bound including new post')
 if joint_existing is not None:need(joint_existing+len(raw)<2*2**30,'entire current cumulative2GiB including post')
 q=BASE/'REVIEW.json'
 with q.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 budget();print(json.dumps(dict(status=report['status'],review_pin=pin(q))),flush=True)


R=ROOT
OUTPUT_BOUND=32*2**20;SOURCE_BOUND=8*2**20
OUT=R / 'validation/artifacts/axial-material-current-readonly-FD-same-PID-exec-control-20261016-v1'
EXPECTED_CORE_PLAN_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_readonly_FD_same_PID_exec_control_source_v1_UNREADY/PLAN.json', 'sha256': '81cb450d8c8888a29523ce59e195da1988f464965d98b7f00a527ee78b7b94b2', 'size_bytes': 1055034, 'identity': [16777229, 50956704, 33188, 1, 1055034, 1792082790566917852, 1792082790566917852]}
EXPECTED_CORE_HOST_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_readonly_FD_same_PID_exec_control_source_v1_UNREADY/run_readonly_FD_exec_contract_control_Root_only.UNREADY.py', 'sha256': 'ff2aac8493795a72c4714a8f2d4d11b614cd08caf8bc1954df6873b2dd0d8197', 'size_bytes': 14907, 'identity': [16777229, 50956463, 33188, 1, 14907, 1792082719496014845, 1792082719496014845]}
EXPECTED_CORE_SOURCE_PINS=[{'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_readonly_FD_same_PID_exec_control_source_v1_UNREADY/run_readonly_FD_exec_contract_control_Root_only.UNREADY.py', 'sha256': 'ff2aac8493795a72c4714a8f2d4d11b614cd08caf8bc1954df6873b2dd0d8197', 'size_bytes': 14907, 'identity': [16777229, 50956463, 33188, 1, 14907, 1792082719496014845, 1792082719496014845]}, {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_readonly_FD_same_PID_exec_control_source_v1_UNREADY/readonly_FD_exec_control_contract.UNREADY.py', 'sha256': '15130c241891aa33b1dba86e468e157724d3059d7079aa311281dd31d90805b8', 'size_bytes': 6633, 'identity': [16777229, 50956356, 33188, 1, 6633, 1792082518761894078, 1792082518761894078]}, {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_readonly_FD_same_PID_exec_control_source_v1_UNREADY/open_fixture_FDs_then_same_PID_exec.UNREADY.py', 'sha256': '680c7375482c85e1933f1a8b1633253d2ba055d89c4ffd0c0c774ec213a4fe4a', 'size_bytes': 4619, 'identity': [16777229, 50956354, 33188, 1, 4619, 1792082518760325446, 1792082518760325446]}, {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_readonly_FD_same_PID_exec_control_source_v1_UNREADY/readonly_fd_native_startup_control.UNREADY.f90', 'sha256': 'c68a3973ff0cd7209bf1db570d41ad50b2b56084245b4677b3b2c29714444cf6', 'size_bytes': 5154, 'identity': [16777229, 50956355, 33188, 1, 5154, 1792082671088360107, 1792082671088360107]}]

def unique(rows):
 t={}
 for p in rows:
  if p['path']in t:need(t[p['path']]==p,'one exact fullPF per path')
  t[p['path']]=p
 return list(t.values())

def admit(plan):
    need(plan['schema'] == 'ROOT_NONSCIENTIFIC_READONLY_FD_SAME_PID_EXEC_CONTROL_PLAN_V1' and plan['actual_runtime_build_and_independent_post_closed'] is True and (plan['original_caps'] == CAPS) and (plan['bounded_new_output_reservation_bytes'] == OUTPUT_BOUND) and (plan['bounded_own_Source_metadata_receipts_bytes'] == SOURCE_BOUND), 'new fixture-only control exact caps and true prerequisites, NULL hard reject')
    p = meta(plan['runtime_actual_post_pin'])
    tools = meta(plan['runtime_actual_post_tools_pin'])
    root = meta(plan['runtime_Root_tools_pin'])
    host = meta(plan['runtime_Host_report_pin'])
    genuine(tools, 'actual_review_return', plan['runtime_actual_post_pin'], 'review_pin')
    genuine(root, 'actual_terminal_return', plan['runtime_Host_report_pin'], 'report_pin')
    need(p['schema'] == 'B_PLANE2_RUNTIME_COMPLETE71_BUILD_ACTUAL_METADATA_POSTVERIFY_V1' and p['status'] == 'PASS_ACTUAL_B_PLANE2_THREE_COMPILE_COMPLETE71_LINK_ROOT0_FOUR_CHILD0_METADATA_ONLY_NO_RUNTIME_QUALIFICATION' and (p['failure'] is None) and (type(p['actual_Root_integer_exit_code']) is int) and (p['actual_Root_integer_exit_code'] == 0) and (p['actual_child_integer_exit_codes'] == [0, 0, 0, 0]) and all((type(x) is int for x in p['actual_child_integer_exit_codes'])) and (p['actual_Host_report_pin'] == plan['runtime_Host_report_pin']) and (p['actual_Root_tools_pin'] == plan['runtime_Root_tools_pin']), 'genuine runtime compile/link Root0 and separate actual metadata0, no old missing raw invented')
    need(p['actual_new_Dragon_pin'] == plan['retained_new_runtime_pin'] and p['new_runtime_compile_link_only_not_executed'] is True and (p['new_B_formal13_compatible'] is p['online_BOOT_qualified'] is p['physics_qualified'] is False), 'only build facts consumed; no context or science claim')
    need(plan['complete_joint_roots'] == p['complete_joint_roots'] + [str(OUT)] and len(plan['complete_joint_roots']) == len(set(plan['complete_joint_roots'])) == 85 and (not any((Path(x).is_relative_to(Path(y)) for x in plan['complete_joint_roots'] for y in plan['complete_joint_roots'] if x != y))) and any((BASE.is_relative_to(Path(x)) for x in p['complete_joint_roots'])) and os.path.lexists(OUT), 'entire actual control85 now present and Source still counted under FTOP')
    need(host['records'] == p['actual_four_stage_records'] and len(host['records']) == 4 and all((x['status'] == 'PASS' for x in host['records'])) and (host['actual_ordered71_link_inputs'] == p['actual_ordered71_link_inputs']), 'actual new complete71/four stage0 metadata')
    return p

def resource_facts(v,roots):
 ps=v['Root_same_PID_PS']
 need(type(v['SELF_peak_bytes'])is int and v['SELF_peak_bytes']<512*2**20 and 0<=v['elapsed_seconds']<1800 and v['own_output_bytes']<32*2**20 and v['own_Source_bytes']<8*2**20 and len(roots)==85,'actual saved original SELF512/whole1800/control32/Source8/full85 scalar resources')
 need(type(ps['returncode'])is int and ps['returncode']==0 and ps['stderr']==''and len(ps['stdout'])<1024 and ps['stdout'].strip().isdigit()and int(ps['stdout'].strip())*1024<512*2**20,'saved original same-PID PS512, never rerun')
 need(v['complete_joint_bytes']+v['explicit_external_metadata_bytes']+v['open_unlinked_bytes']<2*2**30 and v['history_artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and v['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original joint2/history96/cold/meta64reserve/free8 with all external/open-unlinked unchanged')

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for name in('Root-tools-pin','Host-pin','executor-task-name'):ap.add_argument('--'+name,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'independent once-only metadata post, Source author cannot self-run')
 pRoot=json.loads(a.Root_tools_pin);pHost=json.loads(a.Host_pin);raw=meta(pRoot);terminal=raw['actual_terminal_return'];host=None if pHost is None else meta(pHost);core=meta(EXPECTED_CORE_AUTHOR_FREEZE);plan=meta(EXPECTED_CORE_PLAN_PIN)
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==raw['original_integer_exit_code']and terminal.get('session_id')is None and raw['actual_retried']is False and raw['actual_execution_permission_mode']=='require_escalated','genuine actual typed closed Root code/no session/no retry/original permission')
 need(plan['host_source_pin']==EXPECTED_CORE_HOST_PIN and plan['complete_source_file_pins']==EXPECTED_CORE_SOURCE_PINS and len(EXPECTED_CORE_SOURCE_PINS)==4 and plan['contract_Source_pin']['path']==str(PACKAGE/'readonly_FD_exec_control_contract.UNREADY.py')and plan['bounded_own_Source_metadata_receipts_bytes']==8*2**20 and plan['bounded_new_output_reservation_bytes']==32*2**20,'same exact final four Sources/PLAN protocol and local Source8/control32')
 need(core['schema']=='NONSCIENTIFIC_READONLY_FD_SAME_PID_EXEC_CONTROL_AUTHOR_SOURCE_FREEZE_V1'and core['source_only']is True and core['plan_pin']==EXPECTED_CORE_PLAN_PIN and core['host_source_pin']==EXPECTED_CORE_HOST_PIN and core['whole_Source_file_pins']==EXPECTED_CORE_SOURCE_PINS and core['Source_generation_or_publisher_required']is False,'exact frozen four Source/PLAN protocol requires neither GEN nor publisher')
 for p in EXPECTED_CORE_SOURCE_PINS:full(p)
 if host is not None:need(pHost['path']==str(OUT/'Root_actual_non_scientific_readonly_FD_exec_control_summary.json')and host['schema']=='ROOT_NONSCIENTIFIC_READONLY_FD_SAME_PID_EXEC_CONTRACT_CONTROL_REPORT_V1'and host['source_pin']==EXPECTED_CORE_HOST_PIN and host['plan_pin']==EXPECTED_CORE_PLAN_PIN,'same actual owning non-scientific FD control report role and Source/PLAN')
 code=raw['original_integer_exit_code']
 if code!=0:
  result=dict(schema='NONSCIENTIFIC_FD_CONTROL_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=code,actual_Host_status=None if host is None else host['status'],actual_Host_failure=None if host is None else host['failure'],actual_original_stage_records=None if host is None else host['original_stage_records'],actual_stage_checks=None if host is None else host['actual_stage_checks'],actual_child_integer_exit_codes=None if host is None else host['actual_child_integer_exit_codes'],successful_FD_control_or_production_qualification_inferred=False,partial_probe_or_fixture_body_opened_or_hashed=False)
  save(result,8*2**20);return
 need(host is not None,'genuine Root0 requires actual emitted FD control report');genuine(raw,'actual_terminal_return',pHost,'report_pin');stdout=json.loads(terminal['output'].strip().splitlines()[-1])
 need(host['status']=='PASS_NONSCIENTIFIC_GNU_STARTUP_READONLY_FD_EXEC_CONTRACT_CONTROLS_ONLY'and host['failure']is None and host['secondary_failures']==[]and host['complete_source_file_pins']==EXPECTED_CORE_SOURCE_PINS and host['original_guard_class']=='OwnRSSSerialExecutor'and host['original_guard_MRO_unchanged']is True and host['final_report_resource_check_passed']is True and host['negative_original_FAILED_records_preserved']is True and host['expected_negative_refusals_do_not_qualify_production_launcher']is True,'Root0 fixture-only controls and original guard/MRO/FAILED records kept')
 peerpin=host['independent_Source_review_pin'];peertools_pin=host['independent_Source_review_tools_pin'];peer=meta(peerpin);peertools=meta(peertools_pin);genuine(peertools,'actual_review_return',peerpin,'review_pin')
 need(peer['schema']=='INDEPENDENT_SOURCE_ONLY_NONSCIENTIFIC_FD_EXEC_CONTRACT_CONTROL_REVIEW_V1'and peer['status']=='PASS_SOURCE_ONLY_NONSCIENTIFIC_READONLY_FD_SAME_PID_EXEC_CONTROL'and peer['source_only']is True and peer['failure']is None and peer['source_pin']==EXPECTED_CORE_HOST_PIN and peer['plan_pin']==EXPECTED_CORE_PLAN_PIN and peer['complete_source_file_pins']==EXPECTED_CORE_SOURCE_PINS,'actual independent exact Source/PLAN review0 only')
 prefix=plan['original_complete_ENV_Python_B_prefix'];expected_argv=prefix+[EXPECTED_CORE_HOST_PIN['path']]
 for name,p in(('source-pin',EXPECTED_CORE_HOST_PIN),('plan-pin',EXPECTED_CORE_PLAN_PIN),('Source-review-pin',peerpin),('Source-review-tools-pin',peertools_pin)):expected_argv+=['--'+name,json.dumps(p,separators=(',',':'))]
 need(shlex.split(raw['exact_executed_command'])==expected_argv and len(expected_argv)==20,'actual original full20 CLI argv exact Source/PLAN/peer roles, original command string preserved')
 claimPin=pin(PACKAGE/'ROOT_CONTROL_EXECUTION_CLAIM.json');claim=meta(claimPin);need(claim['schema']=='ROOT_EXCLUSIVE_NONSCIENTIFIC_FD_CONTROL_CLAIM_V1'and type(claim['PID'])is int and claim['PID']>0 and claim['argv']==expected_argv[len(prefix):]and claim['claim_before_bound_metadata_or_helper_import']is True,'actual exclusive Root claim before helper/body/child admission')
 runtime_post=admit(plan);need(type(runtime_post['actual_original_owned_runtime_Root_integer_exit_code'])is int and runtime_post['actual_original_owned_runtime_Root_integer_exit_code']==1 and runtime_post['actual_original_owned_runtime_compile_link_children_exit0_only']is True,'original prior runtime Root1 preserved; no missing old success raw invented');explicit=unique(plan['explicit_cumulative_metadata_file_pins']+[EXPECTED_CORE_HOST_PIN,EXPECTED_CORE_PLAN_PIN,peerpin,peertools_pin]);table={p['path']:p for p in explicit};ext=runtime_post['all69_external_compile_toolchain_full_pins'];need(len(ext)==69 and sum(p['size_bytes']for p in ext)==36068911 and all(table.get(p['path'])==p for p in ext)and runtime_post['actual_new_Dragon_pin']==plan['retained_new_runtime_pin'],'all69 inherited external compiler/toolchain bytes retained exactly and no new Dragon execution')
 probe=host['actual_new_probe_binary_pin'];fixtures=host['actual_fixture_full_pins'];need(probe['path']==str(OUT/'build/readonly_fd_native_startup_control')and probe['size_bytes']>0 and [p['path']for p in fixtures]==[str(OUT/'fixtures'/('fixture'+str(i)+'.bin'))for i in(1,2,3)]and [p['size_bytes']for p in fixtures]==[257,521,1031]and len({tuple(p['identity'][:2])for p in fixtures})==3,'only exact newly made three distinct regular tiny fixtures and new standalone probe')
 compile_cmd=[plan['Fortran_compiler_pin']['path'],*plan['original_Fortran_flags'],'-J'+str(OUT/'build'),str(OUT/'sources/readonly_fd_native_startup_control.UNREADY.f90'),'-o',str(OUT/'build/readonly_fd_native_startup_control')]
 labels=['compile_and_link_non_scientific_probe','positive','closed_fd','wrong7','duplicate_inode'];codes=[0,0,71,1,1];checks=host['actual_stage_checks'];records=host['original_stage_records'];need(len(checks)==len(records)==5 and host['actual_child_integer_exit_codes']==codes and all(type(x)is int for x in host['actual_child_integer_exit_codes']),'exact real five child codes; negatives never converted to child0')
 logs={};watches={}
 for stage,record,label,expected in zip(checks,records,labels,codes):
  w=stage['actual_watchdog'];lp=stage['actual_log_pin'];wp=stage['actual_watchdog_pin'];need(stage['label']==label and record['label'].split('/')[-1]==label and stage['expected_integer_exit_code']==expected and type(stage['actual_integer_exit_code'])is int and stage['actual_integer_exit_code']==expected and type(w['returncode'])is int and w['returncode']==expected and w['command']==record['command']and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and stage['negative_refusal_expected']is(expected!=0),'every exact original monitor/code/command/stage600/RSS512/group closure; sampled0 is only recorded sample')
  need(lp['path']==str(OUT/(record['label']+'.log'))and wp['path']==str(OUT/(record['label']+'.watchdog.json'))and meta(wp)==w and stage['actual_original_record_status']==record['status']==('PASS'if expected==0 else'FAILED'),'standalone real monitor/log path uses actual record.label and original negative FAILED status unchanged')
  if expected==0:need(stage['actual_error']is None and lp['sha256']==record['log_sha256'],'positive actual runner PASS log SHA')
  else:need(type(stage['actual_error'])is str and bool(stage['actual_error'])and type(record['error'])is str and bool(record['error']),'negative original error and FAILED record preserved; no invented log_sha field')
  full(lp);need(lp['size_bytes']<2**20,'bounded newly saved control stdout/log metadata');log=Path(lp['path']).read_text();current(lp);logs[label]=log;watches[label]=w
  if label==labels[0]:need(w['command']==compile_cmd,'single real compile+link standalone non-scientific probe')
  else:
   casepin=pin(OUT/label/'CASE.json');case=meta(casepin);need(case['schema']=='NONSCIENTIFIC_READONLY_FD_EXEC_FIXTURE_CASE_V1'and case['case']==label and case['scientific_data']is False and case['fixture_full_pins']==fixtures,'each exact small non-scientific fixture case metadata')
   cmd=[prefix[-2],'-B',str(OUT/'sources/open_fixture_FDs_then_same_PID_exec.UNREADY.py'),'--case-pin',json.dumps(casepin,separators=(',',':')),'--probe-pin',json.dumps(probe,separators=(',',':')),'--case',label];need(w['command']==cmd,'actual wrapper argv case/probe pinned and exact inherited interpreter; no fake native aliases')
 receipt_rows=host['actual_launcher_before_exec_receipts'];need(len(receipt_rows)==2,'only positive and closedFD reach exec; wrong7/duplicate refuse inside wrapper')
 for row,label in zip(receipt_rows,('positive','closed_fd')):
  receipt=row['receipt'];w=watches[label];need(row['receipt_pin']['path']==str(OUT/label/'FD_LAUNCHER_BEFORE_EXEC_RECEIPT.json')and meta(row['receipt_pin'])==receipt and receipt['schema']=='READONLY_FD_LAUNCHER_BEFORE_SAME_PID_EXEC_RECEIPT_V1'and receipt['case']==label and type(receipt['PID'])is int and receipt['PID']==receipt['process_group']==w['pid']and receipt['PID']!=claim['PID']and receipt['new_child_spawned']is False and receipt['scientific_payload_opened']is False and receipt['original_path_identity_only_no_payload_SHA']is True and receipt['exec_executable_pin']==probe and receipt['exact_native_exec_argv']==[probe['path'],str(w['pid']),str(w['pid'])],'actual same PID/process group after exec and no further wrapper spawn or scientific data role')
  proofs=receipt['fixed_fd_proofs'];need(len(proofs)==3 and [x['readonly_fd']for x in proofs]==[101,102,103]and [x['real_original_full_pin']for x in proofs]==fixtures and all(x['actual_fd_current7']==p['identity']and x['inheritable']is True and type(x['F_GETFL_access_mode'])is int and x['F_GETFL_access_mode']==0 and x['payload_body_SHA_repeated']is False for x,p in zip(proofs,fixtures)),'all actual readonly fixed descriptors101..103 exact fixture identity and F_GETFL readonly0 before exec')
  if label=='closed_fd':need(receipt['intentionally_closed_fd_for_negative_control']==103,'only third descriptor intentionally closed; prior two fixture checks may already have read tiny data')
 positive=host['actual_native_positive_proof'];pw=watches['positive'];native_rows=[x.split()for x in logs['positive'].splitlines()if x.startswith('FD_NATIVE_PID_GROUP_BYTES ')];need(positive==dict(PID=pw['pid'],process_group=pw['pid'],complete_fixture_bytes=1809,fixture_count=3,full_reads_seeks_EOF_and_readonly_EBADF_verified=True)and len(native_rows)==1 and list(map(int,native_rows[0][1:]))==[pw['pid'],pw['pid'],1809,3]and 'FD_READONLY_EXEC_NATIVE_POSITIVE_V1'in logs['positive'].splitlines(),'actual GNU startup stdout and native-source fullread/seek/EOF/kernel write-1EBADF/close tests on tiny fixture bytes only')
 refused=[x.split()for x in logs['closed_fd'].splitlines()if x.startswith('FD_CONTRACT_REFUSAL ')];need(refused==[['FD_CONTRACT_REFUSAL','71','INHERITED_FD_PRESENT']]and 'FD_READONLY_EXEC_NATIVE_POSITIVE_V1'not in logs['closed_fd'].splitlines(),'closed third inheritedFD actual native refusal71; no all-data-before-read claim')
 for label,reason in(('wrong7','CURRENT7_MISMATCH'),('duplicate_inode','DUPLICATE_DEVICE_INODE')):
  lines=[json.loads(x)for x in logs[label].splitlines()if x.startswith('{')];w=watches[label];need(len(lines)==1 and lines[0]['schema']=='FD_CONTRACT_LAUNCHER_REFUSAL_V1'and lines[0]['case']==label and lines[0]['reason_code']==reason and lines[0]['PID']==lines[0]['process_group']==w['pid']and lines[0]['native_exec_reached']is False and lines[0]['scientific_payload_opened']is False and not os.path.lexists(OUT/label/'FD_LAUNCHER_BEFORE_EXEC_RECEIPT.json'),'exact pre-exec wrong7/duplicate refusal reason and genuine child1, no extra native exec/spawn or fabricated alias')
 whole=host['whole_new_output_pins'];need(len(whole)==len({p['path']for p in whole})and all(Path(p['path']).is_relative_to(OUT)for p in whole),'only new owning FD outputs, never old native/object bodies');new=all_output_pins(OUT);seen={p['path']:p for p in new};need(seen=={p['path']:p for p in whole+[pHost]}and seen[probe['path']]==probe and all(seen[p['path']]==p for p in fixtures),'whole exact new fixture/probe/Source/metadata owning outputs blindSHA twice; original payload never opened')
 need(sorted(str(q)for q in OUT.rglob('*')if q.is_file())==[p['path']for p in new],'same complete new output inventory after two blindSHA passes')
 for p in new:current(p)
 for key in('launcher_Source_pin','Fortran_probe_Source_pin','original_bounded_Source_pin'):
  p=plan[key];name='runtime/run_bounded_dragon.py'if key=='original_bounded_Source_pin'else'sources/'+Path(p['path']).name;q=seen[str(OUT/name)];need((q['sha256'],q['size_bytes'])==(p['sha256'],p['size_bytes']),'whole new copied probe/wrapper/original bounded Sources')
 roots=plan['complete_joint_roots'];build=meta(plan['original_guard_build_plan_pin']);retained=unique(runtime_post['original_current70_ordered_input_pins']+ext+plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+plan['retained_B2_current_epoch_readonly_pins']+plan['selected31_current_epoch_readonly_pins']+explicit+[plan['retained_new_runtime_pin']])
 for _ in range(2):
  for p in retained:current_role(p,build)
  for p in plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins']:need(set(p)=={'path','size_bytes','identity'},'old failed rows stat3 only, no partial SHA claim');current(p)
  need(len(plan['exact59_historical_absent_pins'])==len({p['path']for p in plan['exact59_historical_absent_pins']})==59,'exact59 historical paths only')
  for p in plan['exact59_historical_absent_pins']:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only narrow known history absent, no generic skip')
 need(host['complete_joint_roots']==roots and len(roots)==85 and roots[-1]==str(OUT)and host['original_caps']==plan['original_caps']==CAPS and host['bounded_new_output_reservation_bytes']==32*2**20 and host['bounded_own_Source_metadata_receipts_bytes']==8*2**20 and host['all_three_tiny_fixture_fullpins_unchanged']is True,'complete original84 to85 and unchanged original caps/component8/output32')
 for k in('scientific_native_payload_opened','scientific_native_payload_hashed','production_FD_launcher_qualified','PACK_produced','new_B_formal13_compatible','online_BOOT_qualified','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(host[k]is False and stdout[k]is False,'tiny FD semantics are not production GANLIB/PACK/online or scientific qualification')
 for key in('resources_before','resources_after'):resource_facts(host[key],roots)
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in explicit if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));unlinked=unlinked_bytes();need(host['resources_before']['explicit_external_metadata_bytes']==host['resources_after']['explicit_external_metadata_bytes']==extra and joint+extra+unlinked<2*2**30 and sum(p['size_bytes']for p in new)<32*2**20 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'entire latest85 plus all inherited external/openunlinked/source/ownoutputs and unchanged cold/free reserves')
 result=dict(schema='NONSCIENTIFIC_READONLY_FD_EXEC_ACTUAL_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_NONSCIENTIFIC_READONLY_FD_SAME_PID_EXEC_ROOT0_WITH_EXACT_NEGATIVE_CHILD_CODES_METADATA_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=0,actual_child_integer_exit_codes=host['actual_child_integer_exit_codes'],source_pin=EXPECTED_CORE_HOST_PIN,plan_pin=EXPECTED_CORE_PLAN_PIN,core_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,complete_source_file_pins=EXPECTED_CORE_SOURCE_PINS,actual_independent_Source_review_pin=peerpin,actual_independent_Source_review_tools_pin=peertools_pin,actual_Root_claim_pin=claimPin,actual_exact_Root_command=raw['exact_executed_command'],actual_original_stage_records=records,actual_stage_checks=checks,negative_original_FAILED_records_preserved=True,negative_refusals_do_not_mean_child0=True,actual_native_positive_proof=positive,actual_launcher_before_exec_receipts=receipt_rows,actual_fixture_full_pins=fixtures,actual_new_probe_binary_pin=probe,only_three_tiny_nonscientific_fixtures_total_bytes=1809,actual_new_own_output_blind_SHA_twice_pins=new,actual_new_own_output_bytes=sum(p['size_bytes']for p in new),all69_external_compile_toolchain_full_pins=ext,all69_external_compile_toolchain_bytes=36068911,original_owned_runtime_Root_integer_exit_code=1,original_owned_runtime_compile_link_children_exit0_only=True,retained_original_current70_input_pins=runtime_post['original_current70_ordered_input_pins'],retained_new_runtime_pin=plan['retained_new_runtime_pin'],old_Dragon_objects_native_cold_current7_only=True,all_retained_current7_verified_twice=True,retained_all_current7_pins=plan['retained_current7_pins'],retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'],exact59_historical_absent_pins=plan['exact59_historical_absent_pins'],complete_joint_roots=roots,original_caps=CAPS,local_Source_limit_bytes=8*2**20,new_output_limit_bytes=32*2**20,actual_resources_before=host['resources_before'],actual_resources_after=host['resources_after'],actual_final_report_resource_check_passed=True,current_joint_bytes=joint,current_explicit_external_bytes=extra,current_post_open_unlinked_bytes=unlinked,production_FD_launcher_qualified=False,GANLIB_or_complete_PACK_qualified=False,PACK_produced=False,new_B_formal13_compatible=False,online_BOOT_qualified=False,physics_qualified=False)
 save(result,8*2**20,joint+extra+unlinked)
if __name__=='__main__':main()
