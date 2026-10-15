"""UNREADY independent metadata post after actual SQL and incomplete pool gzip exact1 execution.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Only Source/small saved metadata and current7 are read. No target/gzip body, worker, lsof, native child or cleanup runs here.
Source and plan are checked against the real owning receipt and author freeze; future actual parameters remain NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_A_B_native_exact10_redundant_plaintext_retirement_source_v1_UNREADY/AUTHOR_SOURCE_FREEZE.json', 'sha256': '454910d9f83cb59b7f2868316ed39e859d9084f936a66a6291c28fa98a00c69b', 'size_bytes': 7554, 'identity': [16777229, 50947988, 33188, 1, 7554, 1792079673033875042, 1792079673033875042]}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(target_payload_body_opened_or_hashed=False,gzip_payload_body_opened_or_hashed=False,worker_or_guard_helpers_imported=False,worker_executed=False,lsof_executed=False,PS_executed=False,native_executed=False,compiler_executed=False,compression_repeated=False,decompression_repeated=False,numerical_executed=False,JSONL_or_array_values_decoded=False,files_deleted_by_post=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
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
def readonly_resource_facts(v,roots):
 need(v['SELF_peak_bytes']<512*2**20 and 0<=v['elapsed_seconds']<600 and v['joint']['resource_roots']==roots,'actual same original SELF512/stage600 and complete joint root topology')
 h=v['history'];j=v['joint'];sample=v['actual_PS_return']
 need(type(sample['returncode'])is int and sample['returncode']==0 and sample['stderr']==''and type(sample['stdout'])is str and sample['stdout'].strip().isdigit()and int(sample['stdout'].strip())*1024<512*2**20,'actual saved original same-PID PS return/RSS facts, PS not repeated by post')
 need(j['artifact_bytes']+v['external_metadata_bytes']+v['open_unlinked_bytes']<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual original joint/history/cold/metadata/free caps including external/open-unlinked')
def save(report,source_limit,joint_existing=None):
 report.update(metadata_only=True,Source_author_task=AUTHOR,actual_executor_task=EXECUTOR,actual_post_not_executed_by_Source_author=True,reviewer_Source_pin=pin(Path(__file__).absolute()),helper_or_candidate_module_imported=False,Source_GEN_or_publication_executed=False,native_or_compiler_or_worker_executed=False,scientific_values_or_SQLite_or_native_XSM_or_context_body_decoded=False,original_collect_or_snapshot_pair_readback_repeated=False,historical_issue_records_modified=False,wall_seconds=time.monotonic()-START,**FALSE)
 raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'post control report6MiB')
 need(counted_bytes([str(PACKAGE)])+len(raw)<source_limit,'entire Source/metadata bound including new post')
 if joint_existing is not None:need(joint_existing+len(raw)<2*2**30,'entire current cumulative2GiB including post')
 q=BASE/'REVIEW.json'
 with q.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 budget();print(json.dumps(dict(status=report['status'],review_pin=pin(q))),flush=True)
def current_failed_v1(p,plan):
 need(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in plan['retained_failed_v1_current7_only_pins'],'only exact failed-v1 current7-only role, never fullPF/SHA or deletion target')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==501==os.getuid()and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])and ids(s)==p['identity']and s.st_size==p['size_bytes'],'entire exact oldfailed file stable current7 only; no body read/hash or generic missing skip')
 return q

def current_failed_pool(p,plan):
 need(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in plan['retained_failed_pool_archive_current7_only_pins'],
  'only exact retained failed-pool metadata/runtime rows, never fullPF/SHA or deletion targets')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)
  and s.st_uid==501==os.getuid()and s.st_nlink==1 and type(p['size_bytes'])is int
  and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])
  and ids(s)==p['identity']and s.st_size==p['size_bytes'],'entire exact failed-pool retained row stable current7 only')
 return q

def unique(rows):
 out={}
 for p in rows:need(p['path']not in out or out[p['path']]==p,'same path same fullPF');out[p['path']]=p
 return list(out.values())

def exact_historical_absence(plan):
 rows=plan['exact49_historical_absent_pins'];need(len(rows)==len({p['path']for p in rows})==49,'only exact inherited49 historical paths, never generic missing')
 for p in rows:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'precise already closed historical path absence only')

def admit_native_byte_control(plan):
    cp = plan['actual_native_byte_control_closure_pins']
    need(type(cp) is dict and all((type(cp[k]) is dict for k in ('report', 'Root_tools', 'post', 'post_tools'))) and (plan['actual_native_byte_control_Root0_independent_post0_complete'] is True), 'future genuine new native control Root0/post0 roles NULL hard reject')
    controlplan = meta(plan['native_byte_control_plan_pin'])
    control = meta(cp['report'])
    raw = meta(cp['Root_tools'])
    post = meta(cp['post'])
    tools = meta(cp['post_tools'])
    genuine(raw, 'actual_terminal_return', cp['report'], 'report_pin')
    genuine(tools, 'actual_review_return', cp['post'], 'review_pin')
    contract = plan['actual_native_byte_control_post_key_projection']
    projection = meta(plan['actual_native_byte_control_post_Source_projection_pin'])
    postauthor = meta(plan['actual_native_byte_control_post_author_freeze_pin'])
    full(plan['actual_native_byte_control_post_Source_pin'])
    need(type(contract) is dict and contract['schema'] == projection['schema'] and (contract['status'] == projection['status']), 'frozen actual post Source projection exact schema/status; no guessed PASS')
    need(post['schema'] == contract['schema'] and post['status'] == contract['status'] and (post['failure'] is None) and (post['metadata_only'] is True) and (post[contract['Root_report_pin_field']] == cp['report']) and (post[contract['Root_tools_pin_field']] == cp['Root_tools']) and (type(post[contract['Root_integer_exit_code_field']]) is int) and (post[contract['Root_integer_exit_code_field']] == 0), 'genuine separate control metadata0 binds same Root report/tools typed0')
    need(post['reviewer_Source_pin'] == plan['actual_native_byte_control_post_Source_pin'] == postauthor['post_Source_pin'] and postauthor['core_plan_pin'] == plan['native_byte_control_plan_pin'] and (postauthor['core_Source_author_freeze_pin'] == plan['native_byte_control_author_freeze_pin']) and (postauthor['exact_success_field_projection_pin'] == plan['actual_native_byte_control_post_Source_projection_pin']) and (Path(plan['actual_native_byte_control_post_Source_pin']['path']).parent == Path(cp['post']['path']).parent) and (post['Root_recorded_all17_native_fullEOF_SHA_and_stable7_verified'] is True) and (post['Root_new_B_final55_independent_complete_stream_verified'] is True) and (post['retirement_authorized'] is False) and (post['files_deleted'] is False), 'same genuinely executed corrected post Source/author/projection path and explicit17/newBfinal proof; old unexecuted post is not actual evidence')
    need(control['schema'] == 'ROOT_A_B_NATIVE_EXACT10_BYTE_PRESERVATION_CONTROL_REPORT_V1' and control['status'] == 'PASS_ROOT_NATIVE_EXACT10_COMPLETE_BYTE_PRESERVATION_CONTROL_NO_RETIREMENT' and (control['failure'] is None) and (control['source_pin'] == plan['native_byte_control_Source_pin']) and (control['plan_pin'] == plan['native_byte_control_plan_pin']) and (control['role_projection_pin'] == plan['native_role_projection_pin']) and (control['children_started'] == 0) and (control['actual_child_integer_exit_code'] is None) and (control['files_deleted'] is False) and (control['retirement_authorized'] is False) and (control['final_report_resource_check_passed'] is True) and (control['native_or_scientific_values_decoded'] is False) and (control['restored_large_file_written'] is False), 'only actual Root byte preservation control completed; never old m proof, native rerun, deletion or new scientific qualification')
    targets = plan['exact_target_pins']
    canonical = plan['retained_ordered7_canonical_native_full_pins']
    maps = plan['exact_ordered10_recovery_mappings']
    all17 = control['all17_native_full_pins']
    need(targets == control['exact_ordered10_candidate_full_pins'] == controlplan['exact_ordered10_candidate_full_pins'] and canonical == control['retained_ordered7_canonical_native_full_pins'] == controlplan['retained_ordered7_canonical_native_full_pins'] and (maps == control['exact_ordered10_recovery_mappings'] == controlplan['exact_ordered10_recovery_mappings']) and (len(targets) == 10) and (len(canonical) == 7) and (all17 == controlplan['all17_native_full_pins'] == unique(targets + canonical)) and (len(all17) == 17) and (len({p['path'] for p in all17}) == 17) and (len(maps) == 10) and ([m['target_pin'] for m in maps] == targets) and (sum((p['size_bytes'] for p in targets)) == control['candidate_total_bytes'] == plan['planned_released_bytes'] == 232289584), 'precise10 candidate maps plus canonical7 native fullPF roles, no generic duplicate reduction')
    need(control['all17_native_fullEOF_SHA_and_stable7_verified'] is True and control['all17_native_current7_verified_before_and_after'] is True and (len(control['all17_native_blind_fullEOF_SHA_length_proofs']) == 17), 'new actual complete17 blindSHA and stable7 proof')
    for row, p in zip(control['all17_native_blind_fullEOF_SHA_length_proofs'], all17):
        r = row['blind_fullEOF_SHA_length']
        need(row['original_full_pin'] == p and r['sha256'] == p['sha256'] and (r['size_bytes'] == p['size_bytes']) and (r['full_EOF'] is True) and (r['stable_opened_and_EOF_identity'] == p['identity']), 'each actual fullEOF SHA/length and stable7 exactly matches saved original/canonical PF')
    gzip = plan['retained_complete_B4_gzip_pin']
    entry = plan['retained_B4_member0_entry_pin']
    index = plan['retained_B4_all4_lookup_index_pin']
    bf = targets[1]
    need(gzip == control['existing_complete_B4_gzip_pin'] == controlplan['existing_complete_B4_gzip_pin'] and entry == control['existing_B4_member0_entry_pin'] and (index == control['existing_B4_all4_lookup_index_pin']) and (control['new_B_final55_full_pin'] == bf) and (control['new_B_final55_independent_complete_stream_verified'] is True) and (control['new_B_final55_streamed_decompressed_SHA'] == bf['sha256']) and (control['new_B_final55_streamed_decompressed_length'] == bf['size_bytes'] == 76594248) and (control['gzip_blind_fullEOF_before'] == control['gzip_blind_fullEOF_after']) and (control['gzip_blind_fullEOF_before']['sha256'] == gzip['sha256']) and (control['gzip_blind_fullEOF_before']['size_bytes'] == gzip['size_bytes'] == 33559716) and (control['gzip_blind_fullEOF_before']['full_EOF'] is True), 'genuine new Bfinal complete stream restoration proof and blind2 same retained gzip; old B4m proof alone insufficient')
    need(control['old_A_Root_integer_exit_code'] == 1 and control['A_continuation_Root_integer_exit_code'] == 0 and (control['A_continuation_new_material_children_started'] == 0) and (control['old_B4_member0_proof_relabelled_as_new_B_final55_control'] is False), 'old A Root1/continuation0/no newchild and old m/newBfinal distinction preserved')
    for m in maps:
        p = m['target_pin']
        if m['mode'] == 'retained_native_copy':
            c = m['canonical_pin']
            need(c in canonical and c['path'] != p['path'] and ((c['sha256'], c['size_bytes']) == (p['sha256'], p['size_bytes'])), 'each native-copy full byte map exact, no native-as-spool waiver')
        else:
            need(m['mode'] == 'existing_complete_gzip_member' and p == bf and (m['canonical_gzip_pin'] == gzip) and (m['canonical_entry_pin'] == entry) and (m['canonical_B4_lookup_index_pin'] == index), 'only exact Bfinal uses complete permanent compressed original byte map')
    need(plan['complete_joint_roots'] == control['complete_joint_roots'] == controlplan['complete_joint_roots'] and len(plan['complete_joint_roots']) == 83 and (plan['original_caps'] == control['original_caps'] == controlplan['original_caps']) and (plan['bounded_own_Source_metadata_receipts_bytes'] == 8 * 2 ** 20) and (plan['exact49_historical_absent_pins'] == control['exact49_historical_absent_pins'] == controlplan['exact49_historical_absent_pins']), 'unchanged original83/caps/Source8 and exact prior49absence')
    expected = unique([p for p in control['retained_current7_pins'] if p['path'] not in {q['path'] for q in targets}] + canonical + [gzip, entry, index])
    need(plan['retained_current7_pins'] == expected and plan['retained_B2_current_epoch_readonly_pins'] == control['retained_B2_current_epoch_readonly_pins'] and (plan['retained_failed_v1_current7_only_pins'] == control['retained_failed_v1_current7_only_pins']) and (plan['retained_failed_pool_archive_current7_only_pins'] == control['retained_failed_pool_archive_current7_only_pins']), 'latest real control live roles minus only exact10 plus explicit canonical/gzip/entry/index, never selected-table completeness assumption')
    proofs = list(cp.values()) + [plan['native_byte_control_plan_pin'], plan['native_byte_control_Source_pin'], plan['native_byte_control_author_freeze_pin'], plan['native_role_projection_pin'], plan['actual_native_byte_control_post_Source_projection_pin'], plan['actual_native_byte_control_post_Source_pin'], plan['actual_native_byte_control_post_author_freeze_pin']]
    need(plan['explicit_cumulative_metadata_file_pins'] == unique(controlplan['explicit_cumulative_metadata_file_pins'] + proofs) and plan['retained_archive_metadata_current7_pins'] == unique(control['retained_archive_metadata_current7_pins'] + proofs), 'entire inherited cumulative metadata plus all new control/post proofs; no omitted external bytes')
    for key in ('original_guard_build_plan_pin', 'original_guard_build_contract_Source_pin', 'original_production_inputs_Source_pin', 'original_production_resource_Source_pin', 'original_history_resource_Source_pin', 'original_complete_ENV_Python_B_prefix'):
        need(plan[key] == controlplan[key], 'same frozen original guard/runtime Source roles')
    return (controlplan, control)

def complete_archive_metadata(plan,receipt,check_targets_live):
 controlplan,control=admit_native_byte_control(plan);roots=plan['complete_joint_roots'];build=meta(plan['original_guard_build_plan_pin'])
 need(roots==receipt['complete_joint_roots']==controlplan['complete_joint_roots']and len(roots)==83 and plan['no_new_output_root']is True and plan['original_caps']==controlplan['original_caps']==CAPS and len(roots)==len(set(roots))and all(not Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b)and any(PACKAGE.is_relative_to(Path(x))for x in roots),'whole existing83 unchanged originalcaps/no new root')
 targets=plan['exact_target_pins'];canonical=plan['retained_ordered7_canonical_native_full_pins'];maps=plan['exact_ordered10_recovery_mappings'];gzip=plan['retained_complete_B4_gzip_pin'];entry=plan['retained_B4_member0_entry_pin'];index=plan['retained_B4_all4_lookup_index_pin'];cp=plan['actual_native_byte_control_closure_pins']
 retained=unique(plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+plan['explicit_cumulative_metadata_file_pins']+plan['retained_B2_current_epoch_readonly_pins']+canonical+[gzip,entry,index])
 need(not{p['path']for p in targets}&{p['path']for p in retained+plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins']},'only exact10 targets excluded from everyretained role; canonical/archive/results never targets')
 need(plan['all_native_original_bytes_must_remain_exactly_recoverable']is True and plan['completed_spool_lifecycle_used_as_native_retirement_basis']is False and plan['future_consumer_must_restore_exact_native_role_from_explicit_map_then_admit_new_current_identity']is True and plan['historical_original_current7_identity_reused_after_restore']is False and plan['generic_missing_path_skip_authorized']is False,'explicit native byte-preservation mappings only, no completed-spool waiver or generic missing exception')
 need(receipt['native_original_complete_bytes_preserved_by_exact_recovery_maps']is True and receipt['completed_spool_lifecycle_used_as_native_retirement_basis']is False and receipt['exact_target_pins']==targets and receipt['retained_ordered7_canonical_native_full_pins']==canonical and receipt['exact_ordered10_recovery_mappings']==maps and receipt['retained_complete_B4_gzip_pin']==gzip and receipt['retained_B4_member0_entry_pin']==entry and receipt['retained_B4_all4_lookup_index_pin']==index and receipt['actual_native_byte_control_closure_pins']==cp and receipt['native_byte_control_plan_pin']==plan['native_byte_control_plan_pin']and receipt['native_byte_control_Source_pin']==plan['native_byte_control_Source_pin']and receipt['native_role_projection_pin']==plan['native_role_projection_pin'],'same original/canonical maps, new bytecontrol0/post0 and exact Source/PLAN proofroles')
 need(receipt['new_B_final55_independent_complete_stream_verified']is True and receipt['new_B_final55_streamed_decompressed_SHA']==control['new_B_final55_streamed_decompressed_SHA']and receipt['new_B_final55_streamed_decompressed_length']==control['new_B_final55_streamed_decompressed_length']and receipt['all17_original_and_canonical_native_fullEOF_proof_pins']==control['all17_native_full_pins']and receipt['all17_original_and_canonical_native_fullEOF_SHA_verified']is True,'actual new Bfinal complete stream distinct from old m and full17 nativeproof metadata, no repeat body reads')
 need(receipt['old_A_Root_integer_exit_code']==1 and receipt['A_continuation_Root_integer_exit_code']==0 and receipt['A_continuation_new_material_children_started']==0 and receipt['native_redundant_originals_retired']is(not check_targets_live)and receipt['future_consumer_must_restore_exact_native_role_from_explicit_map_then_admit_new_current_identity']is True and receipt['historical_original_current7_identity_reused_after_restore']is False and receipt['generic_missing_path_skip_authorized']is False,'original A Root1/continuation0 unchanged; restored path requires new current identity/admission')
 for k in('retained_current7_pins','retained_archive_metadata_current7_pins','retained_B2_current_epoch_readonly_pins','retained_failed_v1_current7_only_pins','retained_failed_pool_archive_current7_only_pins','exact49_historical_absent_pins'):need(receipt[k]==plan[k],'same whole savedretainer and exact49 historical tables')
 for _ in range(2):
  if check_targets_live:
   for p in targets:current(p)
  else:
   for p in targets:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only precisely retired native10 absent; never stat retired original as current')
  for p in canonical+[gzip,entry,index]:current(p)
  for p in retained:current_role(p,build)
  for p in plan['retained_failed_v1_current7_only_pins']:current_failed_v1(p,plan)
  for p in plan['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,plan)
  exact_historical_absence(plan)
 return roots,targets,[gzip],[entry],cp,plan['exact49_historical_absent_pins'],control


def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('execution-receipt-pin','Root-tools-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'exact independent executor and immutable single execution post')
 pReceipt=json.loads(a.execution_receipt_pin);pTools=json.loads(a.Root_tools_pin);tools=meta(pTools);terminal=tools['actual_terminal_return'];receipt=None if pReceipt is None else meta(pReceipt)
 need(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==tools['original_integer_exit_code']and terminal.get('session_id')is None,'genuine observed closed execution Root integer; no live handle inference')
 author_pin=pin(PACKAGE/'AUTHOR_SOURCE_FREEZE.json');need(author_pin==EXPECTED_CORE_AUTHOR_FREEZE,'exact frozen core author metadata PF');author=meta(author_pin);pp=author['whole_plan_pin'];plan=meta(pp);source_limit=plan['bounded_own_Source_metadata_receipts_bytes'];ps=next(p for p in author['whole_Source_file_pins']if p['path']==str(PACKAGE/'retire_exact10_redundant_native_original_paths.UNREADY.py'))
 need(source_limit==8*2**20 and pp['path']==str(PACKAGE/'PLAN.json')and plan['schema']=='CURRENT_A_B_NATIVE_EXACT10_REDUNDANT_ORIGINAL_RETIREMENT_PLAN_V1'and plan['Source_admission_ready']is True and plan['draft_unready']is False and plan['original_caps']==CAPS,'same frozen A_B_native_exact10 Source/PLAN and unchanged original global caps/localSource8MiB')
 if pReceipt is not None:need(pReceipt['path']==str(PACKAGE/'EXECUTION_RECEIPT.json')and receipt['schema']=='CURRENT_A_B_NATIVE_EXACT10_REDUNDANT_ORIGINAL_RETIREMENT_RECEIPT_V1'and receipt['mode']=='execute'and receipt['source_pin']==ps and receipt['plan_pin']==pp,'actual exact owning execution receipt/schema/mode and Source/plan')
 code=tools['original_integer_exit_code']
 if code!=0:
  result=dict(schema='CURRENT_A_B_NATIVE_EXACT10_RETIREMENT_EXECUTION_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_execution_receipt_pin=pReceipt,actual_Root_tools_pin=pTools,actual_Root_integer_exit_code=code,actual_receipt_status=None if receipt is None else receipt['status'],actual_receipt_failure=None if receipt is None else receipt['failure'],actual_released_pins=None if receipt is None else receipt['actual_released_pins'],actual_released_bytes=None if receipt is None else receipt['actual_released_bytes'],files_deleted=None if receipt is None else receipt['files_deleted'],source_pin=ps,plan_pin=pp,full_A_B_native_exact10_retirement_success_inferred=False)
  save(result,source_limit);return
 need(receipt is not None,'actual execution Root0 requires emitted exact receipt PF');genuine(tools,'actual_terminal_return',pReceipt,'receipt_pin')
 need(tools['actual_execution_permission_mode']=='require_escalated'and receipt['status']=='RETIRED_CURRENT_A_B_NATIVE_EXACT10_ORIGINAL_BYTES_PRESERVED_IN_EXACT_RECOVERY_MAPS'and receipt['failure']is None and receipt['files_deleted']is True and receipt['native_original_complete_bytes_preserved_by_exact_recovery_maps']is True and receipt['resources_after_original_classes_forced_fresh']is True,'actual A_B_native_exact10 execution Root0/retirement/no lost complete result bytes/fresh original resource closure')
 targets=plan['exact_target_pins'];released=receipt['actual_released_pins'];releasedbytes=receipt['actual_released_bytes'];expectedbytes=sum(p['size_bytes']for p in targets)
 need(receipt['exact_target_pins']==released==targets and len(targets)==len({p['path']for p in targets})==10 and type(releasedbytes)is int and releasedbytes==expectedbytes==plan['planned_released_bytes']==232289584and json.loads(terminal['output'].strip().splitlines()[-1])['actual_released_bytes']==releasedbytes,'actual precisely ordered two exact SQL/partial fullPF target and exact bytes in receipt/genuine stdout')
 for p in targets:
  need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only genuinely deleted exact target paths absent; historical fullPF never relabelled current')
 cli_pin=pin(PACKAGE/'ROOT_EXECUTE_REVIEWABLE_CLI.json');cli=meta(cli_pin)
 need(cli['schema']=='CURRENT_A_B_NATIVE_EXACT10_ORIGINAL_RETIREMENT_GUARDED_REVIEWABLE_CLI_V1'and cli['mode']=='execute'and cli['source_pin']==ps and cli['plan_pin']==pp and cli['independent_Source_review_pin']==receipt['peer_review_pin']and cli['independent_Source_review_tools_pin']==receipt['peer_tools_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated'and shlex.split(tools['exact_executed_command'])==cli['argv']==shlex.split(cli['command']),'actual exact published execute CLI and same Source/plan/peer identities')
 for p in author['whole_Source_file_pins']:full(p);full(p)
 peer=meta(receipt['peer_review_pin']);peer_tools=meta(receipt['peer_tools_pin']);genuine(peer_tools,'actual_review_return',receipt['peer_review_pin'],'review_pin');need(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')and peer['source_pin']==ps and peer['plan_pin']==pp,'genuine independent Source review0 for same exact worker/plan')
 readonly_pin=receipt['actual_readonly_receipt_pin'];readonly_tools_pin=receipt['actual_readonly_tools_pin'];readonly_post_pin=receipt['actual_readonly_post_pin'];readonly_post_tools_pin=receipt['actual_readonly_post_tools_pin']
 need(cli['actual_readonly_receipt_pin']==readonly_pin and cli['actual_readonly_tools_pin']==readonly_tools_pin and cli['actual_readonly_post_pin']==readonly_post_pin and cli['actual_readonly_post_tools_pin']==readonly_post_tools_pin,'actual execute CLI/receipt consumes exact genuine readonly0/post0 PFs')
 readonly=meta(readonly_pin);readonly_tools=meta(readonly_tools_pin);readonly_post=meta(readonly_post_pin);readonly_post_tools=meta(readonly_post_tools_pin);genuine(readonly_tools,'actual_readonly_return',readonly_pin,'receipt_pin');genuine(readonly_post_tools,'actual_review_return',readonly_post_pin,'review_pin')
 need(readonly_pin['path']==str(PACKAGE/'READONLY_RECEIPT.json')and readonly_tools['actual_readonly_permission_mode']=='require_escalated'and readonly['schema']=='CURRENT_A_B_NATIVE_EXACT10_REDUNDANT_ORIGINAL_RETIREMENT_RECEIPT_V1'and readonly['mode']=='check'and readonly['status']=='READONLY_READY_CURRENT_A_B_NATIVE_EXACT10_NO_UNLINK'and readonly['failure']is None and readonly['source_pin']==ps and readonly['plan_pin']==pp and readonly['exact_target_pins']==targets and readonly['actual_released_pins']==[]and readonly['actual_released_bytes']==0 and readonly['files_deleted']is False and readonly['resources_after_original_classes_forced_fresh']is True,'actual earlier readonly Root0/no-unlink/fresh resource proof remains historical and unmodified')
 contract=plan['readonly_post_report_contract'];need(readonly_post['schema']==contract['schema']and readonly_post['status']==contract['status']and readonly_post['failure']is None and readonly_post['metadata_only']is True and readonly_post['actual_readonly_receipt_pin']==readonly_pin and readonly_post['actual_readonly_tools_pin']==readonly_tools_pin and readonly_post['source_pin']==ps and readonly_post['plan_pin']==pp and readonly_post['exact_target_pins']==targets and readonly_post['actual_released_pins']==[]and readonly_post['actual_released_bytes']==0 and readonly_post['files_deleted']is False and readonly_post['resources_after_original_classes_forced_fresh']is True and type(readonly_post['actual_readonly_Root_integer_exit_code'])is int and readonly_post['actual_readonly_Root_integer_exit_code']==0,'genuine independent readonly metadata post0 exact execution prerequisite, not self-reexecuted')
 lsof=receipt['actual_lsof_owner_check'];need(lsof['argv']==['/usr/sbin/lsof','-n','-P','-Fpcfn','--']+[p['path']for p in targets]and type(lsof['returncode'])is int and lsof['returncode']==1 and lsof['stdout']==lsof['stderr']=='','actual saved original A_B_native_exact10 lsof owner check1/empty only; lsof not repeated by post')
 roots,targets,archives,entries,archive_cp,historical,archive_post=complete_archive_metadata(plan,receipt,False)
 readonly_resource_facts(receipt['resources_before'],roots);readonly_resource_facts(receipt['resources_after'],roots)
 for name in('history','joint'):need(type(receipt['resources_after'][name]['checked_unix'])in(int,float)and receipt['resources_after'][name]['checked_unix']>=receipt['resources_before'][name]['checked_unix'],'saved forced-fresh after original resource scans follow before scans, no fabricated final-unlink timestamp')
 need(receipt['native_original_complete_bytes_preserved_by_exact_recovery_maps']is True and receipt['completed_spool_lifecycle_used_as_native_retirement_basis']is False and receipt['future_consumer_must_restore_exact_native_role_from_explicit_map_then_admit_new_current_identity']is True,'canonical native and completed result documents retained; future replay needs new extraction/admission, no archive success inferred')
 for key in('numerical_executed','compiler_executed','JSONL_or_array_values_decoded','compression_repeated','decompression_repeated','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(receipt[key]is False,'exact cleanup metadata cannot mint science/physical/goal qualification')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in plan['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current unchanged original cumulative/free reserve with post metadata and own open-unlinked')
 for p in(pReceipt,pTools,ps,pp,receipt['peer_review_pin'],receipt['peer_tools_pin'],cli_pin,author_pin,readonly_pin,readonly_tools_pin,readonly_post_pin,readonly_post_tools_pin):full(p)
 result=dict(schema='CURRENT_A_B_NATIVE_EXACT10_RETIREMENT_EXECUTION_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_A_B_NATIVE_EXACT10_REDUNDANT_ORIGINALS_RETIRED_ALL_BYTES_RECOVERABLE_METADATA_ONLY',failure=None,actual_execution_receipt_pin=pReceipt,actual_Root_tools_pin=pTools,actual_Root_integer_exit_code=0,source_pin=ps,plan_pin=pp,exact_target_pins=targets,actual_released_pins=released,actual_released_bytes=releasedbytes,files_deleted=True,exact_ten_targets_absent_verified_twice=True,resources_after_original_classes_forced_fresh=True,actual_readonly_receipt_pin=readonly_pin,actual_readonly_tools_pin=readonly_tools_pin,actual_readonly_post_pin=readonly_post_pin,actual_readonly_post_tools_pin=readonly_post_tools_pin,actual_execute_reviewable_CLI_pin=cli_pin,actual_Source_peer_pin=receipt['peer_review_pin'],actual_Source_peer_tools_pin=receipt['peer_tools_pin'],actual_Source_author_freeze_pin=author_pin,actual_saved_lsof_owner_check=lsof,native_original_complete_bytes_preserved_by_exact_recovery_maps=True,completed_spool_lifecycle_used_as_native_retirement_basis=False,native_redundant_originals_retired=True,retained_ordered7_canonical_native_full_pins=plan['retained_ordered7_canonical_native_full_pins'],exact_ordered10_recovery_mappings=plan['exact_ordered10_recovery_mappings'],retained_complete_B4_gzip_pin=archives[0],retained_B4_member0_entry_pin=entries[0],retained_B4_all4_lookup_index_pin=plan['retained_B4_all4_lookup_index_pin'],actual_native_byte_control_closure_pins=archive_cp,native_byte_control_plan_pin=plan['native_byte_control_plan_pin'],native_byte_control_Source_pin=plan['native_byte_control_Source_pin'],native_role_projection_pin=plan['native_role_projection_pin'],new_B_final55_independent_complete_stream_verified=archive_post['new_B_final55_independent_complete_stream_verified'],new_B_final55_streamed_decompressed_SHA=archive_post['new_B_final55_streamed_decompressed_SHA'],new_B_final55_streamed_decompressed_length=archive_post['new_B_final55_streamed_decompressed_length'],all17_original_and_canonical_native_fullEOF_proof_pins=archive_post['all17_native_full_pins'],all17_original_and_canonical_native_fullEOF_SHA_verified=True,all_canonical7_gzip_entry_index_current7_verified_twice=True,retained_all_current7_pins=plan['retained_current7_pins'],retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'],retained_B2_current_epoch_readonly_pins=plan['retained_B2_current_epoch_readonly_pins'],retained_failed_v1_current7_only_pins=plan['retained_failed_v1_current7_only_pins'],retained_failed_pool_archive_current7_only_pins=plan['retained_failed_pool_archive_current7_only_pins'],all_retained_roles_current7_verified_twice=True,exact49_historical_absent_pins=plan['exact49_historical_absent_pins'],exact49_historical_absence_only_verified_twice=True,old_A_Root_integer_exit_code=1,A_continuation_Root_integer_exit_code=0,A_continuation_new_material_children_started=0,old_B4_member0_proof_relabelled_as_new_B_final55_control=False,future_consumer_must_restore_exact_native_role_from_explicit_map_then_admit_new_current_identity=True,historical_original_current7_identity_reused_after_restore=False,generic_missing_path_skip_authorized=False,historical_deleted_target_PFs_not_claimed_current=True,local_Source_bound_bytes=source_limit,complete_joint_roots=roots,no_new_output_root=True,original_caps=CAPS,actual_original_resources_before=receipt['resources_before'],actual_original_resources_after=receipt['resources_after'],current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked)
 save(result,source_limit,joint+extra+unlinked)

if __name__=='__main__':main()
