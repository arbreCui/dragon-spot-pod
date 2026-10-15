"""UNREADY independent metadata post for the actual two-stage B engineering continuation, metadata only. The original Root1/last-marker FAILED remains separate from the new Root result.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Only Source and saved metadata are read. All scientific output, decks, copied scientific inputs, stage logs and native tools receive current7 only. No numerical log, native payload, object, Dragon, PACK/RCON or gzip body is opened or hashed by this post.
The exact pre-GEN author freeze is bound below; actual execution remains NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE=None
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
OUTPUT_BOUND=128*2**20;SOURCE_BOUND=8*2**20
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-current-B-small-axial-engineering-continuation-20261016-v1')
EXPECTED_CORE_PLAN_PIN=None
EXPECTED_CORE_AUTHOR_SCHEMA=None
EXPECTED_CORE_HOST_PIN=None
EXPECTED_CORE_SOURCE_PINS=None
EXPECTED_CONFIG={'axial_acce_accel': 0, 'axial_acce_free': 3, 'cells_per_zone': 16, 'eps_axial': 5e-08, 'eps_mccg': 2.5e-08, 'eps_radial': 2.5e-07, 'maxinr': 740, 'maxout': 500, 'radial_acce_accel': 3, 'radial_acce_free': 3, 'rank': 1, 'sn': 32, 'zone_height_cm': 50.0}

def unique(rows):
 t={}
 for p in rows:
  if p['path']in t:need(t[p['path']]==p,'one exact fullPF per path')
  t[p['path']]=p
 return list(t.values())

def admit_prior_frozen_configuration_metadata(plan):
    need(plan['schema'] == 'CURRENT_A1_B2_A3_SMALL_B_AXIAL_ENGINEERING_CONTEXT_PLAN_V1' and plan['actual_PACK_Root0_and_independent_post0_closed'] is True and (plan['original_caps'] == CAPS) and (plan['bounded_new_output_reservation_bytes'] == OUTPUT_BOUND) and (plan['bounded_own_Source_metadata_receipts_bytes'] == SOURCE_BOUND), 'genuine PACK0/post0/full87 conditional128+Source8 required')
    four = [plan[k] for k in ('PACK_Root_report_pin', 'PACK_Root_tools_pin', 'PACK_actual_post_pin', 'PACK_actual_post_tools_pin')]
    need(all((p is not None for p in four)), 'four true current PACK closure PFs cannot be NULL')
    r = meta(four[0])
    raw = meta(four[1])
    p = meta(four[2])
    pt = meta(four[3])
    genuine(raw, 'actual_terminal_return', four[0], 'report_pin')
    genuine(pt, 'actual_review_return', four[2], 'review_pin')
    need(r['schema'] == 'ROOT_CURRENT_A1_B2_A3_COMPLETE18_PACK_READONLY_FD_REPORT_V1' and r['status'] == 'PASS_ACTUAL_A1_B2_A3_COMPLETE18_PACK_ONLY_NATIVE0_INDEPENDENT_READBACK0' and (r['failure'] is None) and (r['final_report_resource_check_passed'] is True), 'actual full independent PACK18 readback Root0')
    need(p['schema'] == 'A1_B2_A3_COMPLETE18_PACK_FD_ACTUAL_METADATA_POSTVERIFY_V1' and p['status'] == 'PASS_ACTUAL_A1_B2_A3_COMPLETE18_PACK_ROOT0_CHILD0_ROOT_SCIENTIFIC_READBACK_RECORDED_METADATA_ONLY' and (p['metadata_only'] is True) and (p['failure'] is None) and (p['actual_Host_report_pin'] == four[0]) and (p['actual_Root_tools_pin'] == four[1]) and (type(p['actual_Root_integer_exit_code']) is int) and (p['actual_Root_integer_exit_code'] == 0) and (type(p['actual_child_integer_exit_code']) is int) and (p['actual_child_integer_exit_code'] == 0) and (p['Root_recorded_full18_and_three_RCON_and_strict_plane_readback_verified'] is True), 'independent PACK0/post0 genuine prior stages, not inferred compatibility')
    need(plan['PACK_full_pin'] == r['actual_complete_PACK_pin'] == p['actual_complete_PACK_pin'] and plan['ordered_three_plane_RCON_pins'] == r['actual_ordered_three_RCON_pins'] == p['actual_ordered_three_RCON_pins'] and (len(p['actual_independent_complete18_tree_proofs']) == 18) and (len(p['actual_independent_three_RCON_tree_proofs']) == 3) and (len(p['actual_independent_strict_plane_case_epoch_type4_keff_proofs']) == 3), 'exact newly produced PACK and original A1/B2/A3 plane contracts')
    f = meta(plan['formal_prepared_current_epoch_full_pin'])
    di = meta(plan['formal_deck_inputs_current_epoch_full_pin'])
    spec = meta(plan['formal_case_spec_current_epoch_full_pin'])
    need(f['production_config'] == di['config'] == plan['production_config'] == EXPECTED_CONFIG and di['shared_basis_required'] is True and (di['training_slots'] == spec['basis']['training_slots'] == ['A', 'B', 'A']) and (spec['basis']['requested_rank'] == 1) and (spec['basis']['fixed_once_for_both_cases'] is True), 'exact frozen48cell SN32 rank1 parameters, fresh common basis trained once from current A1/B2/A3')
    need([(x['plane'], x['material'], x['expected_case']) for x in plan['producers']] == [(1, 'A', 'R64WARM-A-V1 '), (2, 'B', 'R64WARM-B-V1 '), (3, 'A', 'R64-A3-WARM1 ')] and plan['global_case_name'] == 'PIN-ABA' and (plan['old_allA_basis_or_context_reused'] is False), 'new B-bearing engineering only; global declaration is not native plane case')
    for role, name in (('white_tracking', 'white_tracking'), ('make_route_contract', 'make_route_contract')):
        candidate = plan['small_tool_saved_SHA_and_current7_candidate_roles'][role]
        need(set(candidate) == {'path', 'sha256', 'size_bytes', 'identity'} and candidate['path'] == f['runtime_sources'][name]['path'] and (candidate['sha256'] == f['runtime_sources'][name]['sha256']), 'exact old declared tool SHA plus candidate current7, not preclaimed Root proof')
        current(candidate)
    need(plan['small_tools_current_epoch_EOF_proof_not_yet_executed'] is True, 'new exact Root byteproof must run after claim before small tool invocation')
    return p

def admit(plan):
    need(plan['schema'] == 'CURRENT_B_SMALL_AXIAL_ENGINEERING_CONTINUATION_PLAN_V1' and plan['actual_prior_Root1_and_independent_failure_post0_closed'] is True and (plan['original_caps'] == CAPS) and (plan['bounded_new_output_reservation_bytes'] == OUTPUT_BOUND) and (plan['bounded_own_Source_metadata_receipts_bytes'] == SOURCE_BOUND), 'real prior failurefacts0 and full88 conditional128+Source8 required')
    previous = meta(plan['prior_failed_execution_plan_pin'])
    admit_prior_frozen_configuration_metadata(previous)
    four = [plan[k] for k in ('prior_failed_Root_report_pin', 'prior_failed_Root_tools_pin', 'prior_failure_actual_post_pin', 'prior_failure_actual_post_tools_pin')]
    need(all((p is not None for p in four)), 'prior real Root1/child0/failurepost0 proof cannot remain NULL')
    h = meta(four[0])
    raw = meta(four[1])
    p = meta(four[2])
    pt = meta(four[3])
    genuine(pt, 'actual_review_return', four[2], 'review_pin')
    terminal = raw['actual_terminal_return']
    cli = meta(plan['prior_exact_executed_Root_CLI_pin'])
    need(raw['observed_closed'] is True and type(raw['original_integer_exit_code']) is int and (raw['original_integer_exit_code'] == 1) and (type(terminal['exit_code']) is int) and (terminal['exit_code'] == 1) and (terminal.get('session_id') is None) and (raw['actual_retried'] is False) and (raw['exact_executed_command'] == cli['command']), 'actual original Root1 command preserved, no invented success stdout')
    need(h['schema'] == 'ROOT_CURRENT_B_SMALL_AXIAL_ENGINEERING_CONTEXT_REPORT_V1' and h['status'] == 'FAILED_CURRENT_B_SMALL_AXIAL_ENGINEERING_CONTEXT_NO_RETRY' and (h['failure'] == "Refusal('host marker missing: ROUTE CONTRACT SEALED:')") and (h['plan_pin'] == plan['prior_failed_execution_plan_pin']) and (h['source_pin'] == previous['host_source_pin']) and (h['complete_source_file_pins'] == previous['complete_source_file_pins']), 'exact original marker failure retains original Source and PLAN')
    need(p['schema'] == 'CURRENT_B_SMALL_ENGINEERING_CONTEXT_ACTUAL_FAILURE_FACTS_METADATA_POST_V1' and p['status'] == 'PASS_FAILURE_FACTS_ONLY' and (p['failure'] is None) and (p['actual_Host_report_pin'] == four[0]) and (p['actual_Root_tools_pin'] == four[1]) and (type(p['actual_Root_integer_exit_code']) is int) and (p['actual_Root_integer_exit_code'] == 1) and (p['actual_Host_status'] == h['status']) and (p['actual_Host_failure'] == h['failure']) and (p['success_or_context_or_online_qualification_inferred'] is False), 'genuine independent failure-facts-only0 never makes failed original Root0')
    need(h['actual_child_integer_exit_codes'] == p['actual_child_integer_exit_codes'] == [0, 0, 0, 0] and [x['status'] for x in h['original_stage_records']] == ['PASS', 'PASS', 'PASS', 'FAILED'] and (p['original_stage_records'] == h['original_stage_records']) and (p['actual_stage_checks'] == h['actual_stage_checks']) and (h['original_stage_records'][3]['error'] == 'host marker missing: ROUTE CONTRACT SEALED:'), 'four real original child0, original last host-marker FAILED intact')
    need([x['stage_label'] for x in h['actual_stage_checks']] == ['train', 'rank', 'white_tracking', 'make_route_contract'] and h['actual_complete_engineering_scientific_readback'] is None and (h['actual_complete_scientific_output_pins'] == []) and (p['Root_saved_scientific_readback'] is None) and (p['Root_saved_scientific_output_pins'] == []), 'no initial/axial or completed scientific result falsely inferred')
    for e in h['actual_stage_checks']:
        w = e['actual_watchdog']
        need(type(w['returncode']) is int and w['returncode'] == 0 and (w['limit_failure'] is None) and (w['own_child_only'] is True) and (w['liveness_group_cleanup'] is True), 'four original mature native child0 closures')
    need(h['actual_fresh_complete370_rank_admission']['classification'] == 'VALID_RANK_INPUT_PRECISION' and h['actual_fresh_complete370_rank_admission']['requested_rank'] == 1 and (len(h['actual_fresh_complete370_rank_admission']['groups']) == 370) and (p['Root_saved_rank_admission'] == h['actual_fresh_complete370_rank_admission']), 'prior one genuinely trained new A1/B2/A3 shared basis/rank0 retained')
    need(h['actual_Root_small_tools_fullEOF_and_stable7_verified_pins'] == p['Root_saved_small_tool_proofs'] == plan['small_tool_saved_SHA_and_current7_candidate_roles'], 'real old tool EOF7 proof retained, neither tool repeated')
    need(plan['complete_joint_roots'] == h['complete_joint_roots'] + [str(OUT)] and h['complete_joint_roots'] == previous['complete_joint_roots'] and (len(plan['complete_joint_roots']) == len(set(plan['complete_joint_roots'])) == 88) and (not any((Path(a).is_relative_to(Path(b)) for a in plan['complete_joint_roots'] for b in plan['complete_joint_roots'] if a != b))) and os.path.lexists(OUT), 'entire actual88 includes failed prior87 and new continuation root, no aliases or generic skip')
    expected = ['basis.xsm', 'axial_track_unmarked.xsm', 'axial_track.xsm', 'axial_macro.xsm', 'global_rcon.xsm', 'plane3_rcon.xsm', 'radial1.bin', 'radial2.bin', 'radial3.bin']
    saved = {Path(x['path']).name: x for x in h['whole_new_output_pins'] if Path(x['path']).name in expected}
    need(plan['ordered_reused_nine_complete_full_pins'] == [saved[n] for n in expected] and len(saved) == 9 and (sum((x['size_bytes'] for x in plan['ordered_reused_nine_complete_full_pins'])) == 35653716), 'exact nine Root-recorded full EOF files, never partial or old allA substitute')
    for row in plan['ordered_reused_nine_complete_full_pins']:
        current(row)
    need(plan['production_config'] == previous['production_config'] == EXPECTED_CONFIG and plan['PACK_full_pin'] == previous['PACK_full_pin'] and (plan['ordered_three_plane_RCON_pins'] == previous['ordered_three_plane_RCON_pins']) and (plan['old_allA_basis_or_context_reused'] is False), 'continuation keeps same newly trained B material/basis/configuration')
    return (h, p)

def tree_facts(v):
 need(set(v)=={'sha256','leaves','bytes','directories','list_items'}and type(v['sha256'])is str and len(v['sha256'])==64 and all(c in'0123456789abcdef'for c in v['sha256'])and all(type(v[k])is int and v[k]>=0 for k in('leaves','bytes','directories','list_items'))and v['leaves']>0 and v['directories']>0 and v['leaves']+v['directories']+v['list_items']<=2000000,'saved complete-tree digest/count shape only, no science body replay')

def resource_facts(v):
 ps=v['Root_same_PID_PS'];need(type(v['SELF_peak_bytes'])is int and v['SELF_peak_bytes']<512*2**20 and 0<=v['elapsed_seconds']<1800 and v['own_output_bytes']<OUTPUT_BOUND and v['own_Source_bytes']<SOURCE_BOUND,'actual saved SELF512/whole1800/context128/Source8')
 need(type(ps['returncode'])is int and ps['returncode']==0 and ps['stderr']==''and len(ps['stdout'])<1024 and ps['stdout'].strip().isdigit()and int(ps['stdout'].strip())*1024<512*2**20,'actual original same-PID PS metadata')
 need(v['complete_joint_bytes']+v['explicit_external_metadata_bytes']+v['open_unlinked_bytes']<2*2**30 and v['history_artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and v['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'all original cumulative/history/cold/meta64/free8 caps')

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('Root-tools-pin','Host-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 args=ap.parse_args();need(args.executor_task_name==EXECUTOR and args.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'independent once-only post; author cannot self-run')
 need(all(p is not None for p in(EXPECTED_CORE_AUTHOR_FREEZE,EXPECTED_CORE_PLAN_PIN,EXPECTED_CORE_HOST_PIN,EXPECTED_CORE_SOURCE_PINS,EXPECTED_CORE_AUTHOR_SCHEMA)),'draft post cannot run before final author/PLAN/Source freeze')
 pRoot=json.loads(args.Root_tools_pin);pHost=json.loads(args.Host_pin);raw=meta(pRoot);terminal=raw['actual_terminal_return'];host=None if pHost is None else meta(pHost);core=meta(EXPECTED_CORE_AUTHOR_FREEZE);plan=meta(EXPECTED_CORE_PLAN_PIN)
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==raw['original_integer_exit_code']and terminal.get('session_id')is None and raw['actual_retried']is False and raw['actual_execution_permission_mode']=='require_escalated','genuine original typed Root status, closed/no retry/required permission')
 need(core['schema']==EXPECTED_CORE_AUTHOR_SCHEMA and core['source_only']is True and core['core_writing_stopped']is True and core['plan_pin']==EXPECTED_CORE_PLAN_PIN and core['source_pin']==EXPECTED_CORE_HOST_PIN and core['complete_source_file_pins']==EXPECTED_CORE_SOURCE_PINS and plan['host_source_pin']==EXPECTED_CORE_HOST_PIN and plan['complete_source_file_pins']==EXPECTED_CORE_SOURCE_PINS==[plan[k]for k in('host_source_pin','contract_Source_pin','launcher_Source_pin','readback_Source_pin','deck_builder_Source_pin')]and len(EXPECTED_CORE_SOURCE_PINS)==5 and plan['bounded_own_Source_metadata_receipts_bytes']==SOURCE_BOUND and plan['bounded_new_output_reservation_bytes']==OUTPUT_BOUND,'exact final five Source/PLAN roles; own Source8/context128')
 for p in EXPECTED_CORE_SOURCE_PINS+[plan['original_XSM_parser_Source_pin']]:full(p)
 if host is not None:need(pHost['path']==str(OUT/'Root_actual_current_B_small_engineering_continuation_summary.json')and host['schema']=='ROOT_CURRENT_B_SMALL_ENGINEERING_CONTINUATION_REPORT_V1'and host['source_pin']==EXPECTED_CORE_HOST_PIN and host['plan_pin']==EXPECTED_CORE_PLAN_PIN,'actual emitted same-source small B engineering Host role')
 code=raw['original_integer_exit_code']
 if code!=0:
  result=dict(schema='CURRENT_B_ENGINEERING_CONTINUATION_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=code,actual_Host_status=None if host is None else host['status'],actual_Host_failure=None if host is None else host['failure'],actual_secondary_failures=None if host is None else host['secondary_failures'],actual_stage_checks=None if host is None else host['actual_stage_checks'],original_stage_records=None if host is None else host['original_stage_records'],actual_child_integer_exit_codes=None if host is None else host['actual_child_integer_exit_codes'],Root_saved_prior_small_tool_proofs=None if host is None else host['retained_prior_actual_tool_fullEOF_proof_pins'],Root_saved_prior_rank_admission=None if host is None else host['reused_prior_genuine_complete370_rank_admission'],Root_saved_scientific_readback=None if host is None else host['actual_complete_engineering_scientific_readback'],Root_saved_scientific_output_pins=None if host is None else host['actual_complete_scientific_output_pins'],prior_original_Root_integer_exit_code=None if host is None else host['prior_original_Root_integer_exit_code'],prior_actual_child_integer_exit_codes=None if host is None else host['prior_actual_child_integer_exit_codes'],prior_original_stage_records=None if host is None else host['prior_original_stage_records'],Root_saved_nine_copy_proofs=None if host is None else host['actual_independent_nine_fullEOF_copy_proofs'],success_or_context_or_online_qualification_inferred=False,scientific_outputs_and_numerical_logs_body_opened_or_hashed_by_post=False)
  save(result,SOURCE_BOUND);return
 need(host is not None,'Root0 requires emitted actual engineering report');genuine(raw,'actual_terminal_return',pHost,'report_pin');stdout=json.loads(terminal['output'].strip().splitlines()[-1])
 need(host['status']=='PASS_ACTUAL_CURRENT_B_ENGINEERING_CONTINUATION_ROOT0_TWO_CHILD0_COMPLETE_READBACK0'and host['failure']is None and host['secondary_failures']==[]and host['complete_source_file_pins']==EXPECTED_CORE_SOURCE_PINS and host['final_report_resource_check_passed']is True and host['original_guard_class']=='OwnRSSSerialExecutor'and host['original_guard_MRO_unchanged']is True,'actual two continuation child0 plus complete scientific readback0 closed under original guard')
 peerpin=host['independent_Source_review_pin'];peertools_pin=host['independent_Source_review_tools_pin'];peer=meta(peerpin);peertools=meta(peertools_pin);genuine(peertools,'actual_review_return',peerpin,'review_pin')
 need(peer['schema']=='INDEPENDENT_SOURCE_ONLY_CURRENT_B_ENGINEERING_CONTINUATION_REVIEW_V1'and peer['status']=='PASS_SOURCE_ONLY_CURRENT_B_ENGINEERING_CONTINUATION'and peer['source_only']is True and peer['failure']is None and peer['source_pin']==EXPECTED_CORE_HOST_PIN and peer['plan_pin']==EXPECTED_CORE_PLAN_PIN and peer['complete_source_file_pins']==EXPECTED_CORE_SOURCE_PINS,'same genuine independent five-Source review0')
 prefix=plan['original_complete_ENV_Python_B_prefix'];expected_argv=prefix+[EXPECTED_CORE_HOST_PIN['path']]
 for n,p in(('source-pin',EXPECTED_CORE_HOST_PIN),('plan-pin',EXPECTED_CORE_PLAN_PIN),('Source-review-pin',peerpin),('Source-review-tools-pin',peertools_pin)):expected_argv+=['--'+n,json.dumps(p,separators=(',',':'))]
 need(len(expected_argv)==20 and shlex.split(raw['exact_executed_command'])==expected_argv,'real full20 Root argv binds all four exact Source/PLAN/review roles')
 claimPin=pin(PACKAGE/'ROOT_CONTROL_EXECUTION_CLAIM.json');claim=meta(claimPin);need(claim['schema']=='ROOT_EXCLUSIVE_CURRENT_B_SMALL_ENGINEERING_CONTINUATION_CLAIM_V1'and type(claim['PID'])is int and claim['PID']>0 and claim['argv']==expected_argv[len(prefix):]and claim['claim_before_bound_metadata_or_helper_import']is True,'actual exclusive claim before bound metadata/helper/tool invocations')
 prior_host,prior_failure_post=admit(plan);prior_plan=meta(plan['prior_failed_execution_plan_pin']);need((plan['readback_Source_pin']['sha256'],plan['readback_Source_pin']['size_bytes'])==(prior_plan['readback_Source_pin']['sha256'],prior_plan['readback_Source_pin']['size_bytes']),'exact whole prior complete engineering readback Source reused; no scientific algorithm change')
 # Current runtime closure is inherited through the exact actual PACK PLAN, never guessed from a runtime path.
 pack_plan=meta(meta(plan['PACK_Root_report_pin'])['plan_pin']);runtime_post=meta(pack_plan['runtime_actual_post_pin'])
 four=[plan[k]for k in('PACK_Root_report_pin','PACK_Root_tools_pin','PACK_actual_post_pin','PACK_actual_post_tools_pin')]
 need(host['actual_PACK_four_closure_pins']==four and host['PACK_full_pin']==plan['PACK_full_pin']and host['original_three_plane_RCON_pins']==plan['ordered_three_plane_RCON_pins']and host['production_config']==plan['production_config']==EXPECTED_CONFIG and host['global_case_name']==plan['global_case_name']=='PIN-ABA'and host['existing_new_A1_B2_A3_common_basis_reused_from_failed_v1']is True and host['old_allA_basis_or_context_reused']is False,'same genuine PACK4 and exact new B-bearing common basis engineering parameters')
 toolpins=host['retained_prior_actual_tool_fullEOF_proof_pins'];need(set(toolpins)=={'white_tracking','make_route_contract'}and toolpins==prior_host['actual_Root_small_tools_fullEOF_and_stable7_verified_pins']==plan['small_tool_saved_SHA_and_current7_candidate_roles'],'retain actual prior two tool EOF7 proofs only; no new tool invocation or new fullEOF proof claimed')
 priorfour=[plan[k]for k in('prior_failed_Root_report_pin','prior_failed_Root_tools_pin','prior_failure_actual_post_pin','prior_failure_actual_post_tools_pin')];need([host[k]for k in('prior_failed_Root_report_pin','prior_failed_Root_tools_pin','prior_failure_actual_post_pin','prior_failure_actual_post_tools_pin')]==priorfour and type(host['prior_original_Root_integer_exit_code'])is int and host['prior_original_Root_integer_exit_code']==1 and host['prior_actual_child_integer_exit_codes']==prior_host['actual_child_integer_exit_codes']==[0,0,0,0]and host['prior_original_stage_records']==prior_host['original_stage_records']and host['prior_original_marker_failed_record_preserved']is True,'old genuine Root1/four child0 and exact last-marker FAILED records remain separate from new Root success')
 for k in('common_basis_retrained','rank_native_stage_repeated','white_tracking_tool_repeated','make_route_contract_tool_repeated'):need(host[k]is False,'continuation repeats none of original four completed native/tool stages')
 for p in toolpins.values():current(p)
 labels=['initial','axial'];native_labels=['initial','axial'];stages=host['actual_stage_checks'];records=host['original_stage_records'];codes=host['actual_child_integer_exit_codes']
 need(type(codes)is list and all(type(x)is int for x in codes)and codes==[0,0]and len(stages)==len(records)==2 and [x['stage_label']for x in stages]==labels and [x['original_record']for x in stages]==records,'all and only two real continuation child0 records; no invented stage codes')
 manifestpins={};receiptpins=[];watchpins=[];logpins=[];fdrows=[plan['PACK_full_pin'],*plan['ordered_three_plane_RCON_pins'][:2]]
 for entry,record,label in zip(stages,records,labels):
  w=entry['actual_watchdog'];wp=entry['actual_watchdog_pin'];lp=entry['actual_log_pin'];need(record['status']=='PASS'and record['label'].split('/')[-1]==label and wp['path']==str(OUT/(record['label']+'.watchdog.json'))and lp['path']==str(OUT/(record['label']+'.log'))and meta(wp)==w and lp['sha256']==record['log_sha256']and type(w['returncode'])is int and w['returncode']==0 and w['command']==record['command']and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'actual original per-label watchdog0/stage600/RSS512; original scientific logs current7 only')
  watchpins.append(wp);logpins.append(lp);current(lp)
  if label in native_labels:
   mp=pin(OUT/'context'/(label+'.FD_manifest.json'));manifest=meta(mp);manifestpins[label]=mp
   need(manifest['schema']=='CURRENT_B_ENGINEERING_PACK_RCON_FD_MANIFEST_V1'and manifest['stage_label']==label and manifest['runtime_pin']==plan['runtime_pin']and manifest['ordered_exact_PACK_RCON1_RCON2_full_pins']==fdrows and manifest['actual_PACK_four_closure_pins']==four and manifest['PACK_Root0_and_independent_post0_closed']is True,'actual exact current PACK plus original RCON1/2 FD manifest')
   command=[prefix[-2],'-B',str(OUT/'sources/open_exact_PACK_and_RCONs_then_same_PID_exec.UNREADY.py'),'--manifest-pin',json.dumps(mp,separators=(',',':'))];need(w['command']==command,'same already-built Dragon positive-only launcher invocation')
   rp=entry['actual_before_exec_receipt_pin'];receipt=entry['actual_before_exec_receipt'];need(rp['path']==str(OUT/'context'/(label+'.FD_before_exec.json'))and meta(rp)==receipt and receipt['schema']=='CURRENT_B_ENGINEERING_BEFORE_SAME_PID_EXEC_READONLY_FD_RECEIPT_V1'and receipt['stage_label']==label and receipt['manifest_pin']==mp and receipt['runtime_pin']==plan['runtime_pin']and type(receipt['PID'])is int and receipt['PID']==receipt['process_group']==w['pid']and receipt['PID']!=claim['PID']and receipt['exact_native_exec_argv']==[plan['runtime_pin']['path']],'actual launcher and Dragon same ownchild PID/group, no extra native spawn')
   for k in('new_child_spawned','negative_control_modes_available','scientific_large_input_copies_written','symlinks_or_hardlinks_created'):need(receipt[k]is False,'positive-only same-PID readonly entry with no alias/copy/nested child')
   fdproofs=receipt['fixed_fd_proofs'];need(len(fdproofs)==3 and [x['readonly_fd']for x in fdproofs]==[101,102,103]and [x['real_original_full_pin']for x in fdproofs]==fdrows and len({tuple(p['identity'][:2])for p in fdrows})==3 and all(x['actual_fd_current7']==p['identity']and x['inheritable']is True and type(x['F_GETFL_access_mode'])is int and x['F_GETFL_access_mode']==0 and x['payload_body_SHA_repeated']is False for x,p in zip(fdproofs,fdrows)),'three exact stable readonly descriptors101..103, no native body reread by wrapper')
   receiptpins.append(rp)
 need(len(manifestpins)==len(receiptpins)==2,'both actual native readonly FD handoffs preserved')
 rank=host['reused_prior_genuine_complete370_rank_admission'];need(rank==prior_host['actual_fresh_complete370_rank_admission']==prior_failure_post['Root_saved_rank_admission']and rank['classification']=='VALID_RANK_INPUT_PRECISION'and type(rank['requested_rank'])is int and rank['requested_rank']==1 and len(rank['groups'])==370 and [x['group']for x in rank['groups']]==list(range(1,371))and all(type(x['production_rank'])is int and x['production_rank']==1 and x['pass']is True and type(x['sigma'])is list and len(x['sigma'])==3 for x in rank['groups']),'Root recorded all370 ordered original rank1 decisions; no numerical log parsing or ratio recomputation by post')
 scientific_proof=host['actual_complete_engineering_scientific_readback'];need(0<host['actual_independent_readback_elapsed_seconds']<600,'actual bounded complete scientific readback elapsed time')
 for k in('common_basis_370_group_rank1_and_complete_three_spectra','exact_new48cell_SN32_SCAT3_plane_MIX_mapping','new_global_PIN_ABA_RCON_exact_declared_parameters'):need(scientific_proof[k]is True,'actual Root full scientific readback proof, not post rederivation')
 trees=scientific_proof['whole_output_logical_tree_digests'];need(set(trees)=={'axial_track.xsm','axial_macro.xsm','initial_system.xsm','ax_current.xsm'},'all four complete engineering output logical trees recorded')
 for v in trees.values():tree_facts(v)
 white=scientific_proof['only_original_two_white_markers_added'];need(white['status']=='PASS_ONLY_TWO_WHITE_MARKERS_ADDED'and type(white['inherited_records'])is int and white['inherited_records']>0 and white['new_records']==2 and white['physical_geometry_and_boundary_records_unchanged']is True and white['model']=='conditional constant outer-sodium trace, uniform transverse azimuth'and white['AAA_accuracy_qualified']is False and white['ABA_admitted']is False,'Root saved full inherited TRACK comparison, only exact two conditional white markers added without accuracy qualification')
 macro=scientific_proof['complete_current_PACK_three_material_macrolib_copy'];need(macro['planes']==3 and macro['groups']==370 and all(type(macro[k])is int and macro[k]>0 for k in('all_directory_leaf_records','all_compared_raw_words','source_mixtures_per_plane')),'actual complete three material macro leaf/raw-word comparison counts, no mixture1 assumption')
 mapping=scientific_proof['complete_current_three_plane_axial_material_block_mapping'];need(all(type(mapping[k])is int and mapping[k]>0 for k in('source_mixtures_per_plane','actual_TRACK_total_mixtures','actual_SPOLIB_total_mixtures','radial_regions','axial_cells','all_region_floor_material_ids_compared','middle_B_block_nonvoid_ids_compared'))and mapping['source_mixtures_per_plane']==macro['source_mixtures_per_plane']and mapping['actual_TRACK_total_mixtures']==mapping['actual_SPOLIB_total_mixtures']==3*mapping['source_mixtures_per_plane']and mapping['axial_cells']==48 and mapping['all_region_floor_material_ids_compared']==48*mapping['radial_regions']and mapping['geometry_MIX_means_snapshot_slot']is True and mapping['full_SPOT_original_MATCOD_mapping_equal']is True,'Root recorded complete region-major48-floor material block map including nonvoid middle B, no numerical replay')
 names=['basis.xsm','axial_track_unmarked.xsm','axial_track.xsm','axial_macro.xsm','initial_system.xsm','ax_current.xsm','global_rcon.xsm','plane3_rcon.xsm','radial1.bin','radial2.bin','radial3.bin'];scientific=host['actual_complete_scientific_output_pins'];need(len(scientific)==11 and [p['path']for p in scientific]==[str(OUT/'context'/n)for n in names]and all(type(p['size_bytes'])is int and p['size_bytes']>0 for p in scientific),'exact11 Root fullEOF scientific output PFs, post only stat7')
 copies=host['actual_independent_nine_fullEOF_copy_proofs'];copyinputs=plan['ordered_reused_nine_complete_full_pins'];need(len(copies)==9 and [x['original_saved_full_pin']for x in copies]==copyinputs and [x['new_owned_complete_copy_full_pin']for x in copies]==[scientific[names.index(Path(p['path']).name)]for p in copyinputs]and all(x['original_saved_full_pin']['sha256']==x['new_owned_complete_copy_full_pin']['sha256']and x['original_saved_full_pin']['size_bytes']==x['new_owned_complete_copy_full_pin']['size_bytes']for x in copies)and type(host['actual_independent_nine_copy_bytes'])is int and host['actual_independent_nine_copy_bytes']==sum(x['new_owned_complete_copy_full_pin']['size_bytes']for x in copies)==35653716,'actual nine independently fullEOF copied prior completed science files with exact original/destination SHA+length; post only saved metadata and stat7')
 whole=host['whole_new_output_pins'];allrows=whole+[pHost];table={p['path']:p for p in allrows};need(len(whole)==len({p['path']for p in whole})and len(table)==len(allrows)and all(Path(p['path']).is_relative_to(OUT)for p in allrows)and all(table.get(p['path'])==p for p in scientific),'complete new output Root PF inventory, scientific roles are permanent stat-only')
 metadata_paths=[OUT/'runtime/run_bounded_dragon.py',*[OUT/'sources'/Path(plan[k]['path']).name for k in('launcher_Source_pin','readback_Source_pin','deck_builder_Source_pin')],*[Path(manifestpins[n]['path'])for n in native_labels],*[Path(p['path'])for p in receiptpins],*[Path(p['path'])for p in watchpins],Path(pHost['path'])];metadata_rows=[table[str(q)]for q in metadata_paths];excluded={p['path']for p in scientific+logpins}|{str(OUT/'context'/(n+'.x2m'))for n in native_labels}
 need(len(metadata_paths)==len(set(metadata_paths))==11 and not {str(q)for q in metadata_paths}&excluded and all(p['size_bytes']<8*2**20 for p in metadata_rows),'exact11 Source/control metadata allowlist; all scientific output, both continuation decks and every numerical stage log excluded regardless of size')
 for _ in range(2):
  for p in metadata_rows:full(p)
  for p in allrows:current(p)
 actual=[]
 for q in sorted(OUT.rglob('*')):
  st=q.lstat();need(not stat.S_ISLNK(st.st_mode),'no new output aliases')
  if stat.S_ISREG(st.st_mode):actual.append(str(q));need(table.get(str(q))is not None and ids(st)==table[str(q)]['identity'],'each new owning file exact saved identity, no content opened')
  else:need(stat.S_ISDIR(st.st_mode),'ordinary owning files/directories only')
 need(actual==sorted(table),'entire new output inventory, no generic missing path skip')
 for role,name in[(k,'sources/'+Path(plan[k]['path']).name)for k in('launcher_Source_pin','readback_Source_pin','deck_builder_Source_pin')]+[('original_bounded_Source_pin','runtime/run_bounded_dragon.py')]:
  p=plan[role];cp=table[str(OUT/name)];need((cp['sha256'],cp['size_bytes'])==(p['sha256'],p['size_bytes']),'whole reviewed Source copies only')
 explicit=unique(plan['explicit_cumulative_metadata_file_pins']+[EXPECTED_CORE_HOST_PIN,EXPECTED_CORE_PLAN_PIN,peerpin,peertools_pin]);et={p['path']:p for p in explicit};ext=runtime_post['all69_external_compile_toolchain_full_pins'];need(len(ext)==69 and sum(p['size_bytes']for p in ext)==36068911 and all(et.get(p['path'])==p for p in ext),'all69 external code/toolchain roles preserved and fully counted, no ledger omissions')
 build=meta(plan['original_guard_build_plan_pin']);retained=unique(runtime_post['original_current70_ordered_input_pins']+plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+plan['retained_B2_current_epoch_readonly_pins']+plan['selected31_current_epoch_readonly_pins']+explicit+[plan['PACK_full_pin'],*plan['ordered_three_plane_RCON_pins'],plan['runtime_pin'],*toolpins.values(),*copyinputs]);roots=plan['complete_joint_roots']
 for _ in range(2):
  for p in retained:current_role(p,build)
  for p in plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins']:need(set(p)=={'path','size_bytes','identity'},'historical failed rows remain three-field stat-only, no payload SHA claim');current(p)
  need(len(plan['exact59_historical_absent_pins'])==len({p['path']for p in plan['exact59_historical_absent_pins']})==59,'only exact59 previously closed history paths')
  for p in plan['exact59_historical_absent_pins']:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'exact historical absence only')
 need(host['complete_joint_roots']==roots and len(roots)==88 and roots[-1]==str(OUT)and host['original_caps']==plan['original_caps']==CAPS and host['bounded_new_output_reservation_bytes']==OUTPUT_BOUND and host['bounded_own_Source_metadata_receipts_bytes']==SOURCE_BOUND,'same full88/caps/128conditional/Source8')
 for k in('compiler_executed','build_reexecuted','production_runner_run_ABA_or_qualify_ABA_called','coupled_reference_executed'):need(host[k]is False,'small ordinary-FLU engineering only, no rebuild/coupled solver/production qualify')
 for k in('GLOBAL_or_PROJECT_produced','all_transitive_inputs_recertified','new_B_formal13_compatible','online_BOOT_qualified','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(host[k]is False and stdout[k]is False,'engineering evidence cannot grant future GLOBAL/PROJECT/Bformal/transitive/online/physics qualification')
 resource_facts(host['resources_before']);resource_facts(host['resources_after']);need(host['resources_before']['complete_joint_bytes']+host['resources_before']['explicit_external_metadata_bytes']+host['resources_before']['open_unlinked_bytes']+OUTPUT_BOUND+SOURCE_BOUND<2*2**30,'actual initial whole88 plus context128/Source8 complete reserve');joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in explicit if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));unlinked=unlinked_bytes();need(host['resources_before']['explicit_external_metadata_bytes']==host['resources_after']['explicit_external_metadata_bytes']==extra and joint+extra+unlinked<2*2**30 and sum(p['size_bytes']for p in allrows)<OUTPUT_BOUND and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'all current88/output/Source/external/open-unlinked counted without payload IO')
 result=dict(schema='CURRENT_B_SMALL_ENGINEERING_CONTINUATION_ACTUAL_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_CURRENT_B_ENGINEERING_CONTINUATION_ROOT0_TWO_CHILD0_COMPLETE_READBACK_METADATA_ONLY_PRIOR_ROOT1_PRESERVED',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=0,actual_child_integer_exit_codes=codes,source_pin=EXPECTED_CORE_HOST_PIN,plan_pin=EXPECTED_CORE_PLAN_PIN,core_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,complete_source_file_pins=EXPECTED_CORE_SOURCE_PINS,actual_independent_Source_review_pin=peerpin,actual_independent_Source_review_tools_pin=peertools_pin,actual_Root_claim_pin=claimPin,actual_exact_Root_command=raw['exact_executed_command'],actual_stage_checks=stages,original_stage_records=records,actual_PACK_four_closure_pins=four,PACK_full_pin=plan['PACK_full_pin'],original_three_plane_RCON_pins=plan['ordered_three_plane_RCON_pins'],production_config=plan['production_config'],global_case_name='PIN-ABA',existing_new_A1_B2_A3_common_basis_reused_from_failed_v1=True,old_allA_basis_or_context_reused=False,retained_prior_actual_tool_fullEOF_proof_pins=toolpins,prior_failed_Root_report_pin=priorfour[0],prior_failed_Root_tools_pin=priorfour[1],prior_failure_actual_post_pin=priorfour[2],prior_failure_actual_post_tools_pin=priorfour[3],prior_original_Root_integer_exit_code=1,prior_actual_child_integer_exit_codes=host['prior_actual_child_integer_exit_codes'],prior_original_stage_records=host['prior_original_stage_records'],prior_original_marker_failed_record_preserved=True,common_basis_retrained=False,rank_native_stage_repeated=False,white_tracking_tool_repeated=False,make_route_contract_tool_repeated=False,reused_prior_genuine_complete370_rank_admission=rank,actual_complete_engineering_scientific_readback=scientific_proof,actual_independent_readback_elapsed_seconds=host['actual_independent_readback_elapsed_seconds'],actual_complete_scientific_output_pins=scientific,actual_independent_nine_fullEOF_copy_proofs=copies,actual_independent_nine_copy_bytes=35653716,Root_recorded_complete_readback_and_prior_rank_lineage_verified=True,new_scientific_outputs_and_decks_and_all_numerical_logs_current7_only_by_post=True,scientific_payload_or_rank_log_body_opened_or_SHA_recomputed_by_post=False,scientific_XSM_tree_or_numerical_readback_repeated_by_post=False,whole_new_output_Root_saved_full_pins_current7_verified=allrows,new_control_metadata_full_SHA_verified_pins=metadata_rows,all_retained_roles_current7_verified_twice=True,retained_all_current7_pins=plan['retained_current7_pins'],retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'],exact59_historical_absent_pins=plan['exact59_historical_absent_pins'],all69_external_compile_toolchain_full_pins=ext,all69_external_compile_toolchain_bytes=36068911,complete_joint_roots=roots,original_caps=CAPS,local_Source_limit_bytes=SOURCE_BOUND,new_output_limit_bytes=OUTPUT_BOUND,actual_resources_before=host['resources_before'],actual_resources_after=host['resources_after'],actual_final_report_resource_check_passed=True,current_joint_bytes=joint,current_explicit_external_bytes=extra,current_post_open_unlinked_bytes=unlinked,GLOBAL_or_PROJECT_produced=False,new_B_formal13_compatible=False,online_BOOT_qualified=False,physics_qualified=False)
 save(result,SOURCE_BOUND,joint+extra+unlinked)
if __name__=='__main__':main()
