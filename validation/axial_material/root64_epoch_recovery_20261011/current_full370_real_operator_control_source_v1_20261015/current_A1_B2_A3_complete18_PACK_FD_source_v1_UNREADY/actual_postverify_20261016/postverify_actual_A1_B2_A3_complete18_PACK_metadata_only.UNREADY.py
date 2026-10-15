"""UNREADY independent metadata post for the actual complete18 A1/B2/A3 PACK production metadata only.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Only Source and saved metadata are read. All scientific PACK/RCON and original native/object/Dragon files receive current7 only. No scientific payload SHA, parser import or tree/numeric decoding is repeated by this post.
The exact pre-GEN author freeze is bound below; actual execution remains NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_A1_B2_A3_complete18_PACK_FD_source_v1_UNREADY/AUTHOR_SOURCE_FREEZE.json', 'sha256': '3a52b687e342c98dd945837a381b54b59a26e05fcb3965cab9d39e91f846d6fc', 'size_bytes': 5797, 'identity': [16777229, 50959370, 33188, 1, 5797, 1792083774727007437, 1792083774727007437]}
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
OUTPUT_BOUND=512*2**20;SOURCE_BOUND=8*2**20
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-current-A1-B2-A3-complete18-PACK-readonly-FD-20261016-v1')
EXPECTED_CORE_PLAN_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_A1_B2_A3_complete18_PACK_FD_source_v1_UNREADY/PLAN.json', 'sha256': '55612b1ddebc16533b7979e5fcc04cdd3efc5ef70ca20b627d52d521da31d9d2', 'size_bytes': 1126398, 'identity': [16777229, 50959367, 33188, 1, 1126398, 1792083772447795714, 1792083772447795714]}
EXPECTED_CORE_HOST_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_A1_B2_A3_complete18_PACK_FD_source_v1_UNREADY/run_A1_B2_A3_complete18_PACK_readonly_FD_Root_only.UNREADY.py', 'sha256': '37129ab1a13484251913d58a660011402b24b6c6210cd23c77b24968cdbb5ce0', 'size_bytes': 17256, 'identity': [16777229, 50958349, 33188, 1, 17256, 1792083675454751301, 1792083675454751301]}
EXPECTED_CORE_SOURCE_PINS=[{'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_A1_B2_A3_complete18_PACK_FD_source_v1_UNREADY/run_A1_B2_A3_complete18_PACK_readonly_FD_Root_only.UNREADY.py', 'sha256': '37129ab1a13484251913d58a660011402b24b6c6210cd23c77b24968cdbb5ce0', 'size_bytes': 17256, 'identity': [16777229, 50958349, 33188, 1, 17256, 1792083675454751301, 1792083675454751301]}, {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_A1_B2_A3_complete18_PACK_FD_source_v1_UNREADY/production_PACK_FD_Source_contract.UNREADY.py', 'sha256': 'f3d8dfe6dc0da214351dc148123069b3bac6e3460ad29c4877bf1c4dfba5239f', 'size_bytes': 7829, 'identity': [16777229, 50958214, 33188, 1, 7829, 1792083247490501732, 1792083247490501732]}, {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_A1_B2_A3_complete18_PACK_FD_source_v1_UNREADY/open_exact_three_cold_archives_then_exec_Dragon.UNREADY.py', 'sha256': 'add258785f9cc21ed0c86a730a8b716b7672971ba5ac28507351374a69f0c669', 'size_bytes': 5619, 'identity': [16777229, 50958212, 33188, 1, 5619, 1792083604466417585, 1792083604466417585]}, {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_A1_B2_A3_complete18_PACK_FD_source_v1_UNREADY/complete18_independent_PACK_readback.UNREADY.py', 'sha256': 'c8be076b075af840e2b79992e8bb80807e06d97729d9dfe493ca6145dca7e7e6', 'size_bytes': 6890, 'identity': [16777229, 50958213, 33188, 1, 6890, 1792083604495925316, 1792083604495925316]}, {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_A1_B2_A3_complete18_PACK_FD_source_v1_UNREADY/pack_exact_A1_B2_A3_readonly_FD.UNREADY.x2m', 'sha256': '5d2d64233dd6eb770eeafb7a194534c0357d6e25561001eb754ff2e1cacf4c4d', 'size_bytes': 429, 'identity': [16777229, 50958215, 33188, 1, 429, 1792083165928181507, 1792083165928181507]}]

def unique(rows):
 t={}
 for p in rows:
  if p['path']in t:need(t[p['path']]==p,'one exact fullPF per path')
  t[p['path']]=p
 return list(t.values())

def admit(plan):
    need(plan['schema'] == 'CURRENT_A1_B2_A3_PACK_ONLY_FD_SOURCE_PLAN_V1' and plan['actual_FD_control_Root0_and_independent_post0_closed'] is True and (plan['original_caps'] == CAPS) and (plan['bounded_new_output_reservation_bytes'] == OUTPUT_BOUND) and (plan['bounded_own_Source_metadata_receipts_bytes'] == SOURCE_BOUND), 'FD control actual Root0/post0 and latest512+8 reservation still NULL hard reject')
    four = [plan[k] for k in ('FD_control_Root_report_pin', 'FD_control_Root_tools_pin', 'FD_control_actual_post_pin', 'FD_control_actual_post_tools_pin')]
    need(all((p is not None for p in four)), 'genuine four control closure PFs required')
    r = meta(four[0])
    raw = meta(four[1])
    p = meta(four[2])
    pt = meta(four[3])
    genuine(raw, plan['FD_control_actual_Root_return_field'], four[0], 'report_pin')
    genuine(pt, 'actual_review_return', four[2], 'review_pin')
    need(r['schema'] == 'ROOT_NONSCIENTIFIC_READONLY_FD_SAME_PID_EXEC_CONTRACT_CONTROL_REPORT_V1' and r['status'] == 'PASS_NONSCIENTIFIC_GNU_STARTUP_READONLY_FD_EXEC_CONTRACT_CONTROLS_ONLY' and (r['failure'] is None) and (r['actual_child_integer_exit_codes'] == [0, 0, 71, 1, 1]) and (r['negative_original_FAILED_records_preserved'] is True) and (r['final_report_resource_check_passed'] is True), 'complete actual GNU startup/kernel readonly control0 including exact original FAILED negatives')
    need(p['schema'] == 'NONSCIENTIFIC_READONLY_FD_EXEC_ACTUAL_METADATA_POSTVERIFY_V1' and p['status'] == 'PASS_ACTUAL_NONSCIENTIFIC_READONLY_FD_SAME_PID_EXEC_ROOT0_WITH_EXACT_NEGATIVE_CHILD_CODES_METADATA_ONLY' and (p['metadata_only'] is True) and (p['failure'] is None) and (p['actual_Host_report_pin'] == four[0]) and (p['actual_Root_tools_pin'] == four[1]) and (type(p['actual_Root_integer_exit_code']) is int) and (p['actual_Root_integer_exit_code'] == 0) and (p['actual_child_integer_exit_codes'] == [0, 0, 71, 1, 1]) and (p['negative_original_FAILED_records_preserved'] is True), 'genuine independent metadata control0; no Source-only/partial success inference')
    need(plan['complete_joint_roots'] == r['complete_joint_roots'] + [str(OUT)] and len(plan['complete_joint_roots']) == len(set(plan['complete_joint_roots'])) == 86 and (not any((Path(x).is_relative_to(Path(y)) for x in plan['complete_joint_roots'] for y in plan['complete_joint_roots'] if x != y))) and any((BASE.is_relative_to(Path(x)) for x in r['complete_joint_roots'])) and os.path.lexists(OUT), 'entire86 includes actual PACK owning root, no missing roots/aliases or oldcwd writes')
    cat = meta(plan['selected27_catalog_pin'])
    need(cat['producers'] == plan['producers'] and len(cat['producers']) == 3 and (cat['selected_readonly_role_count'] == 27) and (cat['new_B_bearing_formal_configuration_or_GLOBAL_RCON_compatibility_proved'] is False), 'exact current27 only, formal13 bytebridge not B compatibility')
    need([(x['plane'], x['material'], x['expected_case']) for x in plan['producers']] == [(1, 'A', 'R64WARM-A-V1 '), (2, 'B', 'R64WARM-B-V1 '), (3, 'A', 'R64-A3-WARM1 ')] and [x['archive'] for x in plan['producers']] == plan['ordered_three_real_archive_full_pins'], 'strict ordered independent A1/B2/A3 full current archives')
    rp = meta(plan['runtime_actual_post_pin'])
    rt = meta(plan['runtime_actual_post_tools_pin'])
    genuine(rt, 'actual_review_return', plan['runtime_actual_post_pin'], 'review_pin')
    need(rp['schema'] == 'B_PLANE2_RUNTIME_COMPLETE71_BUILD_ACTUAL_METADATA_POSTVERIFY_V1' and rp['status'] == 'PASS_ACTUAL_B_PLANE2_THREE_COMPILE_COMPLETE71_LINK_ROOT0_FOUR_CHILD0_METADATA_ONLY_NO_RUNTIME_QUALIFICATION' and (rp['failure'] is None) and (rp['actual_child_integer_exit_codes'] == [0, 0, 0, 0]) and (rp['actual_new_Dragon_pin'] == plan['runtime_pin']) and (rp['new_B_formal13_compatible'] is False), 'use exact genuinely built APACK-B runtime, no compilation or oldA2 rename')
    return r

def tree_facts(v):
 need(set(v)=={'sha256','leaves','bytes','directories','list_items'}and type(v['sha256'])is str and len(v['sha256'])==64 and all(c in'0123456789abcdef'for c in v['sha256'])and all(type(v[k])is int and v[k]>=0 for k in('leaves','bytes','directories','list_items'))and v['leaves']>0 and v['directories']>0 and v['leaves']+v['directories']+v['list_items']<=2000000,'actual saved complete-tree digest/count shape only; no scientific payload replay or numerical rederivation')
def resource_facts(v):
 ps=v['Root_same_PID_PS'];need(type(v['SELF_peak_bytes'])is int and v['SELF_peak_bytes']<512*2**20 and 0<=v['elapsed_seconds']<1800 and v['own_output_bytes']<OUTPUT_BOUND and v['own_Source_bytes']<SOURCE_BOUND,'actual Root saved SELF512/whole1800/PACK512/Source8')
 need(type(ps['returncode'])is int and ps['returncode']==0 and ps['stderr']==''and len(ps['stdout'])<1024 and ps['stdout'].strip().isdigit()and int(ps['stdout'].strip())*1024<512*2**20,'original same-PID PS metadata only')
 need(v['complete_joint_bytes']+v['explicit_external_metadata_bytes']+v['open_unlinked_bytes']<2*2**30 and v['history_artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and v['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original full cumulative/history/cold/meta64/free8 caps, no class changes')
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('Root-tools-pin','Host-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 args=ap.parse_args();need(args.executor_task_name==EXECUTOR and args.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'independent once-only metadata post; Source author cannot self-run')
 pRoot=json.loads(args.Root_tools_pin);pHost=json.loads(args.Host_pin);raw=meta(pRoot);terminal=raw['actual_terminal_return'];host=None if pHost is None else meta(pHost);core=meta(EXPECTED_CORE_AUTHOR_FREEZE);plan=meta(EXPECTED_CORE_PLAN_PIN)
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==raw['original_integer_exit_code']and terminal.get('session_id')is None and raw['actual_retried']is False and raw['actual_execution_permission_mode']=='require_escalated','actual genuine typed Root code/no session/no retry/required permission')
 need(core['schema']=='AUTHOR_PACK_ONLY_COMPLETE18_READONLY_FD_FIVE_SOURCE_FREEZE_V1'and core['source_only']is True and core['core_writing_stopped']is True and core['plan_pin']==EXPECTED_CORE_PLAN_PIN and core['source_pin']==EXPECTED_CORE_HOST_PIN and core['complete_source_file_pins']==EXPECTED_CORE_SOURCE_PINS and plan['host_source_pin']==EXPECTED_CORE_HOST_PIN and plan['complete_source_file_pins']==EXPECTED_CORE_SOURCE_PINS==[plan[k]for k in('host_source_pin','contract_Source_pin','launcher_Source_pin','readback_Source_pin','exact_PACK_deck_Source_pin')]and len(EXPECTED_CORE_SOURCE_PINS)==5 and plan['bounded_own_Source_metadata_receipts_bytes']==SOURCE_BOUND and plan['bounded_new_output_reservation_bytes']==OUTPUT_BOUND,'same exact final four Python plus deck Source/PLAN and component8/output512')
 for p in EXPECTED_CORE_SOURCE_PINS+[plan['original_XSM_parser_Source_pin']]:full(p)
 if host is not None:need(pHost['path']==str(OUT/'Root_actual_A1_B2_A3_complete18_PACK_FD_summary.json')and host['schema']=='ROOT_CURRENT_A1_B2_A3_COMPLETE18_PACK_READONLY_FD_REPORT_V1'and host['source_pin']==EXPECTED_CORE_HOST_PIN and host['plan_pin']==EXPECTED_CORE_PLAN_PIN,'actual complete18 PACK-only owning report role')
 code=raw['original_integer_exit_code']
 if code!=0:
  result=dict(schema='A1_B2_A3_PACK_ONLY_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=code,actual_Host_status=None if host is None else host['status'],actual_Host_failure=None if host is None else host['failure'],actual_stage_records=None if host is None else host['actual_stage_records'],actual_watchdog_pin=None if host is None else host['actual_watchdog_pin'],actual_watchdog=None if host is None else host['actual_watchdog'],actual_log_pin=None if host is None else host['actual_log_pin'],Root_saved_PACK_pin=None if host is None else host['actual_complete_PACK_pin'],Root_saved_three_RCON_pins=None if host is None else host['actual_ordered_three_RCON_pins'],complete18_or_PACK_or_online_success_inferred=False,scientific_payload_body_opened_or_hashed_by_post=False)
  save(result,SOURCE_BOUND);return
 need(host is not None,'Root0 requires actual emitted PACK report');genuine(raw,'actual_terminal_return',pHost,'report_pin');stdout=json.loads(terminal['output'].strip().splitlines()[-1]);need(host['status']=='PASS_ACTUAL_A1_B2_A3_COMPLETE18_PACK_ONLY_NATIVE0_INDEPENDENT_READBACK0'and host['failure']is None and host['secondary_failures']==[]and host['complete_source_file_pins']==EXPECTED_CORE_SOURCE_PINS and host['final_report_resource_check_passed']is True and host['original_guard_class']=='OwnRSSSerialExecutor'and host['original_guard_MRO_unchanged']is True,'actual Root closed native0+independent complete scientific readback0 under original guard, not post recomputation')
 peerpin=host['independent_Source_review_pin'];peertools_pin=host['independent_Source_review_tools_pin'];peer=meta(peerpin);peertools=meta(peertools_pin);genuine(peertools,'actual_review_return',peerpin,'review_pin');need(peer['schema']=='INDEPENDENT_SOURCE_ONLY_A1_B2_A3_PACK_ONLY_FD_REVIEW_V1'and peer['status']=='PASS_SOURCE_ONLY_CURRENT_A1_B2_A3_COMPLETE18_PACK_READONLY_FD'and peer['source_only']is True and peer['failure']is None and peer['source_pin']==EXPECTED_CORE_HOST_PIN and peer['plan_pin']==EXPECTED_CORE_PLAN_PIN and peer['complete_source_file_pins']==EXPECTED_CORE_SOURCE_PINS,'same genuine independent five Source/PLAN review0')
 prefix=plan['original_complete_ENV_Python_B_prefix'];expected_argv=prefix+[EXPECTED_CORE_HOST_PIN['path']]
 for n,p in(('source-pin',EXPECTED_CORE_HOST_PIN),('plan-pin',EXPECTED_CORE_PLAN_PIN),('Source-review-pin',peerpin),('Source-review-tools-pin',peertools_pin)):expected_argv+=['--'+n,json.dumps(p,separators=(',',':'))]
 need(len(expected_argv)==20 and shlex.split(raw['exact_executed_command'])==expected_argv,'genuine original full20 Root argv exact actual Source/PLAN/peer roles')
 claimPin=pin(PACKAGE/'ROOT_CONTROL_EXECUTION_CLAIM.json');claim=meta(claimPin);need(claim['schema']=='ROOT_EXCLUSIVE_A1_B2_A3_COMPLETE18_PACK_FD_CLAIM_V1'and type(claim['PID'])is int and claim['PID']>0 and claim['argv']==expected_argv[len(prefix):]and claim['claim_before_bound_metadata_or_helper_import']is True,'Root claim before helper/cold archive/science execution')
 fd_report=admit(plan);runtime_post=meta(plan['runtime_actual_post_pin']);four=[plan[k]for k in('FD_control_Root_report_pin','FD_control_Root_tools_pin','FD_control_actual_post_pin','FD_control_actual_post_tools_pin')];need(host['actual_FD_control_four_closure_pins']==four and host['selected27_catalog_pin']==plan['selected27_catalog_pin']and host['runtime_pin']==plan['runtime_pin']and host['ordered_three_real_archive_full_pins']==plan['ordered_three_real_archive_full_pins'],'actual four FD controls/native runtime/catalog and three ordered real input PFs exact')
 records=host['actual_stage_records'];w=host['actual_watchdog'];wp=host['actual_watchdog_pin'];lp=host['actual_log_pin'];need(type(host['actual_production_child_count'])is int and host['actual_production_child_count']==len(records)==1,'exactly one production child; no compiler/nested subprocess')
 record=records[0];need(record['status']=='PASS'and record['label'].split('/')[-1]=='produce_complete18_PACK_only'and wp['path']==str(OUT/(record['label']+'.watchdog.json'))and lp['path']==str(OUT/(record['label']+'.log'))and meta(wp)==w and lp['sha256']==record['log_sha256']and type(w['returncode'])is int and w['returncode']==0 and w['command']==record['command']and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'actual one original per-label monitor0/stage600/RSS512; sampled0 is recorded sample only')
 mp=pin(OUT/'pack/READONLY_FD_MANIFEST.json');manifest=meta(mp);need(manifest['schema']=='CURRENT_A1_B2_A3_PRODUCTION_PACK_READONLY_FD_MANIFEST_V1'and manifest['catalog_pin']==plan['selected27_catalog_pin']and manifest['runtime_pin']==plan['runtime_pin']and manifest['ordered_three_real_archive_full_pins']==plan['ordered_three_real_archive_full_pins']and manifest['actual_FD_control_four_closure_pins']==four and manifest['FD_control_Root0_and_post0_closed']is True,'same real positive-only FD manifest, no Source-only substitution')
 cmd=[prefix[-2],'-B',str(OUT/'sources/open_exact_three_cold_archives_then_exec_Dragon.UNREADY.py'),'--manifest-pin',json.dumps(mp,separators=(',',':'))];need(w['command']==cmd,'exact positive-only production launcher argv')
 rp=host['actual_production_FD_before_exec_receipt_pin'];receipt=host['actual_production_FD_before_exec_receipt'];need(rp['path']==str(OUT/'pack/PRODUCTION_FD_LAUNCHER_BEFORE_EXEC_RECEIPT.json')and meta(rp)==receipt and receipt['schema']=='PRODUCTION_A1_B2_A3_PACK_READONLY_FD_BEFORE_EXEC_RECEIPT_V1'and receipt['manifest_pin']==mp and receipt['catalog_pin']==plan['selected27_catalog_pin']and receipt['runtime_pin']==plan['runtime_pin']and type(receipt['PID'])is int and receipt['PID']==receipt['process_group']==w['pid']and receipt['PID']!=claim['PID']and receipt['exact_native_exec_argv']==[plan['runtime_pin']['path']],'same actual wrapper→already-built Dragon PID/group; no copy or recompile')
 for k in('new_child_spawned','symlinks_or_hardlinks_created','scientific_archive_copies_written','negative_control_modes_available','scientific_archive_body_SHA_repeated_by_launcher'):need(receipt[k]is False,'positive-only launcher preserves actual originals without aliases/copy/extra spawn/native input rehash')
 fdproofs=receipt['fixed_fd_proofs'];need(len(fdproofs)==3 and [x['readonly_fd']for x in fdproofs]==[101,102,103]and [x['real_original_full_pin']for x in fdproofs]==plan['ordered_three_real_archive_full_pins']and len({tuple(p['identity'][:2])for p in plan['ordered_three_real_archive_full_pins']})==3 and all(x['actual_fd_current7']==p['identity']and x['inheritable']is True and type(x['F_GETFL_access_mode'])is int and x['F_GETFL_access_mode']==0 and x['payload_body_SHA_repeated']is False for x,p in zip(fdproofs,plan['ordered_three_real_archive_full_pins'])),'all exact independent A1/B2/A3 readonly descriptors101..103 current7, no fake aliases')
 need(lp['size_bytes']<2**20,'bounded new execution log metadata');full(lp);log=Path(lp['path']).read_text();current(lp);need(plan['executed_PACK_completion_marker']in log,'actual native PACK completion marker saved in original execution log')
 pack=host['actual_complete_PACK_pin'];rcons=host['actual_ordered_three_RCON_pins'];scientific=[pack,*rcons];need(pack['path']==str(OUT/'pack/initial_pack.xsm')and [p['path']for p in rcons]==[str(OUT/'pack'/('plane'+str(i)+'_rcon.xsm'))for i in(1,2,3)]and all(type(p['size_bytes'])is int and p['size_bytes']>0 for p in scientific),'exact four new scientific XSM roles; saved wholeEOF PFs from Root only, post never opens/hashes them')
 trees=host['actual_independent_complete18_tree_proofs'];rconproofs=host['actual_independent_three_RCON_tree_proofs'];strict=host['actual_independent_strict_plane_case_epoch_type4_keff_proofs'];fields=['TRACK','MICROLIB2','SYSTEM','FLUX','RCONTRACT','BOOT_BIND'];need(len(trees)==18 and [(x['plane'],x['field'])for x in trees]==[(p,n)for p in(1,2,3)for n in fields]and len(rconproofs)==len(strict)==3 and 0<host['actual_independent_readback_elapsed_seconds']<600,'actual complete18 ordered full trees and all3 strict/RCON proofs plus original readback600; no sampled substitute')
 for x in trees:tree_facts(x['complete_tree'])
 for p,(row,rc,proof)in enumerate(zip(plan['producers'],rconproofs,strict),1):
  need(rc['plane']==p and rc['complete_RCON_tree']==next(x['complete_tree']for x in trees if x['plane']==p and x['field']=='RCONTRACT'),'each actual full standalone RCON matches same complete PACK route subtree');tree_facts(rc['complete_RCON_tree'])
  bits=proof['native_keff64_raw_bytes'];need(proof['plane']==p and proof['material']==row['material']and proof['expected_case']==row['expected_case']and proof['epoch']==0 and proof['groups']==370 and proof['unknowns']==14 and type(proof['verified_full_type4_group_records'])is int and proof['verified_full_type4_group_records']==1110 and proof['native64_seal64_equal']is True and proof['native32_mirror_equal']is True and type(bits)is str and len(bits)==16 and all(c in'0123456789abcdef'for c in bits),'Root recorded strict ordered A1/B2/A3 plane/e0/full370×14 typed groups/keff bit equality; no numeric decoding by post')
 whole=host['whole_new_output_pins'];allrows=whole+[pHost];table={p['path']:p for p in allrows};need(len(whole)==len({p['path']for p in whole})and len(table)==len(allrows)and all(Path(p['path']).is_relative_to(OUT)for p in allrows)and all(table.get(p['path'])==p for p in scientific),'all Root-saved new whole-output fullPF roles exact; no full-body scientific replay')
 metadata_paths=[OUT/'runtime/run_bounded_dragon.py',OUT/'sources'/Path(plan['launcher_Source_pin']['path']).name,OUT/'sources'/Path(plan['readback_Source_pin']['path']).name,OUT/'pack/pack.x2m',Path(mp['path']),Path(rp['path']),Path(wp['path']),Path(lp['path']),Path(pHost['path'])];metadata_rows=[table[str(q)]for q in metadata_paths];need(len(metadata_paths)==len(set(metadata_paths))and not set(str(q)for q in metadata_paths)&{p['path']for p in scientific}and all(p['size_bytes']<8*2**20 for p in metadata_rows),'exact Source/control-metadata allowlist only; PACK/RCON are excluded regardless of size')
 for _ in range(2):
  for p in metadata_rows:full(p)
  for p in allrows:current(p)
 actual=[]
 for q in sorted(OUT.rglob('*')):
  st=q.lstat();need(not stat.S_ISLNK(st.st_mode),'no new output aliases')
  if stat.S_ISREG(st.st_mode):actual.append(str(q));need(table.get(str(q))is not None and ids(st)==table[str(q)]['identity'],'every new owning file enumerated/stat-only and equal saved Root PF identity')
  else:need(stat.S_ISDIR(st.st_mode),'ordinary owning files/directories only')
 need(actual==sorted(table),'entire new output inventory, no hidden/generic missing skip')
 for role,name in(('launcher_Source_pin','sources/'+Path(plan['launcher_Source_pin']['path']).name),('readback_Source_pin','sources/'+Path(plan['readback_Source_pin']['path']).name),('exact_PACK_deck_Source_pin','pack/pack.x2m'),('original_bounded_Source_pin','runtime/run_bounded_dragon.py')):
  p=plan[role];cp=table[str(OUT/name)];need((cp['sha256'],cp['size_bytes'])==(p['sha256'],p['size_bytes']),'whole reviewed Source/deck copies only, never original science payload copies')
 explicit=unique(plan['explicit_cumulative_metadata_file_pins']+[EXPECTED_CORE_HOST_PIN,EXPECTED_CORE_PLAN_PIN,peerpin,peertools_pin]);et={p['path']:p for p in explicit};ext=runtime_post['all69_external_compile_toolchain_full_pins'];need(len(ext)==69 and sum(p['size_bytes']for p in ext)==36068911 and all(et.get(p['path'])==p for p in ext),'all69 external toolchain roles still fully deduplicated counted; no external-byte omission')
 build=meta(plan['original_guard_build_plan_pin']);retained=unique(runtime_post['original_current70_ordered_input_pins']+plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+plan['retained_B2_current_epoch_readonly_pins']+plan['selected31_current_epoch_readonly_pins']+explicit+plan['ordered_three_real_archive_full_pins']+[plan['runtime_pin']]);roots=plan['complete_joint_roots']
 for _ in range(2):
  for p in retained:current_role(p,build)
  for p in plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins']:need(set(p)=={'path','size_bytes','identity'},'historical failed rows stay stat3 with no payload SHA claim');current(p)
  need(len(plan['exact59_historical_absent_pins'])==len({p['path']for p in plan['exact59_historical_absent_pins']})==59,'only exact59 previously closed paths')
  for p in plan['exact59_historical_absent_pins']:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'exact historical absence only, not missing input bypass')
 need(host['complete_joint_roots']==roots and len(roots)==86 and roots[-1]==str(OUT)and host['original_caps']==plan['original_caps']==CAPS and host['bounded_new_output_reservation_bytes']==OUTPUT_BOUND and host['bounded_own_Source_metadata_receipts_bytes']==SOURCE_BOUND and host['all27_real_cold_producer_roles_current7_retained']is True,'same entire86/prefix/caps/PACK512/Source8 and all27 cold producer roles kept')
 for k in('scientific_archive_copies_written','symlinks_or_hardlinks_created','compiler_executed','build_reexecuted','APACK_negative_controls_executed'):need(host[k]is False,'PACK-only production no oldbody copies/aliases/compile/rebuild or extra negative run')
 for k in('GLOBAL_or_PROJECT_produced','all_transitive_inputs_recertified','new_B_formal13_compatible','online_BOOT_qualified','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(host[k]is False and stdout[k]is False,'complete PACK proof cannot certify GLOBAL/PROJECT/new Bformal/alltransitive/online/physics')
 resource_facts(host['resources_before']);resource_facts(host['resources_after']);joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in explicit if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));unlinked=unlinked_bytes();need(host['resources_before']['explicit_external_metadata_bytes']==host['resources_after']['explicit_external_metadata_bytes']==extra and joint+extra+unlinked<2*2**30 and sum(p['size_bytes']for p in allrows)<OUTPUT_BOUND and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'all current86/source/scientific outputs/metadata/external/openunlinked fully counted, no data body IO by post')
 result=dict(schema='A1_B2_A3_COMPLETE18_PACK_FD_ACTUAL_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_A1_B2_A3_COMPLETE18_PACK_ROOT0_CHILD0_ROOT_SCIENTIFIC_READBACK_RECORDED_METADATA_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=0,actual_child_integer_exit_code=w['returncode'],source_pin=EXPECTED_CORE_HOST_PIN,plan_pin=EXPECTED_CORE_PLAN_PIN,core_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,complete_source_file_pins=EXPECTED_CORE_SOURCE_PINS,actual_independent_Source_review_pin=peerpin,actual_independent_Source_review_tools_pin=peertools_pin,actual_Root_claim_pin=claimPin,actual_exact_Root_command=raw['exact_executed_command'],actual_stage_records=records,actual_watchdog_pin=wp,actual_watchdog=w,actual_log_pin=lp,actual_FD_control_four_closure_pins=four,actual_production_FD_before_exec_receipt_pin=rp,actual_production_FD_before_exec_receipt=receipt,selected27_catalog_pin=plan['selected27_catalog_pin'],runtime_pin=plan['runtime_pin'],ordered_three_real_archive_full_pins=plan['ordered_three_real_archive_full_pins'],actual_complete_PACK_pin=pack,actual_ordered_three_RCON_pins=rcons,actual_independent_complete18_tree_proofs=trees,actual_independent_three_RCON_tree_proofs=rconproofs,actual_independent_strict_plane_case_epoch_type4_keff_proofs=strict,Root_recorded_full18_and_three_RCON_and_strict_plane_readback_verified=True,actual_Root_scientific_readback_elapsed_seconds=host['actual_independent_readback_elapsed_seconds'],new_scientific_PACK_and_RCON_current7_verified_twice_only=True,scientific_payload_body_opened_or_SHA_recomputed_by_post=False,scientific_XSM_tree_or_numerical_readback_repeated_by_post=False,whole_new_output_Root_saved_full_pins_current7_verified=allrows,new_control_metadata_full_SHA_verified_pins=metadata_rows,all_retained_roles_current7_verified_twice=True,retained_all_current7_pins=plan['retained_current7_pins'],retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'],exact59_historical_absent_pins=plan['exact59_historical_absent_pins'],all69_external_compile_toolchain_full_pins=ext,all69_external_compile_toolchain_bytes=36068911,complete_joint_roots=roots,original_caps=CAPS,local_Source_limit_bytes=SOURCE_BOUND,new_output_limit_bytes=OUTPUT_BOUND,actual_resources_before=host['resources_before'],actual_resources_after=host['resources_after'],actual_final_report_resource_check_passed=True,current_joint_bytes=joint,current_explicit_external_bytes=extra,current_post_open_unlinked_bytes=unlinked,GLOBAL_or_PROJECT_produced=False,all_transitive_inputs_recertified=False,new_B_formal13_compatible=False,online_BOOT_qualified=False,physics_qualified=False)
 save(result,SOURCE_BOUND,joint+extra+unlinked)
if __name__=='__main__':main()
