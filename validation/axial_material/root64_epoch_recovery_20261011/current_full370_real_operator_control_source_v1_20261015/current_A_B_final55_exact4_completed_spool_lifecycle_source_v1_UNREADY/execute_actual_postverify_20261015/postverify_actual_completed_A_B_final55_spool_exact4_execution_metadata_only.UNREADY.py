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
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_A_B_final55_exact4_completed_spool_lifecycle_source_v1_UNREADY/AUTHOR_SOURCE_FREEZE.json', 'sha256': 'f2d6b7633317cfb6d4e9ec8a2c46aece8482d4ff676318d972957dc728a2c4b5', 'size_bytes': 3825, 'identity': [16777229, 50896325, 33188, 1, 3825, 1792077945270923991, 1792077945270923991]}
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
 early=plan['exact16_retired_temporary_target_pins'];presence=plan['historical_retired_presence_full_pin'];originals=plan['exact28_retired_result_JSONL_target_pins']
 need(len(early)==16 and all(set(p)=={'path','sha256','size_bytes','identity'}for p in early[:15])and set(early[-1])=={'path','size_bytes','identity'}and len(originals)==28 and all(set(p)=={'path','sha256','size_bytes','identity'}for p in originals),'exact16 mixed historical plus28 fullPF retired JSONL, no generic missing role')
 historical=early+[presence]+originals
 need(len({p['path']for p in historical})==45,'only exact16+presence+28 historical paths')
 for p in historical:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only specifically closed oldpaths absent; do not stat/relabel retired fullPFs')

def admit_completed_consumers(plan, archiveplan):
    audit = meta(plan['actual_completed_spool_role_audit_pin'])
    need(audit['schema'] == 'FINAL_A_B_FINAL55_EXACT4_COMPLETED_DERIVED_SPOOL_SOURCE_METADATA_AUDIT_V1' and audit['source_only'] is True and (audit['metadata_only'] is True) and (audit['formal_retirement_admission'] is False) and (audit['payload_SQL_pool_XSM_gzip_or_scientific_JSONL_body_read_or_hashed'] is False), 'independent Source/meta audit is role evidence, not execution admission')
    targets = plan['exact_target_pins']
    native = plan['retained_exact_canonical_observer_XSM_full_pins']
    need(targets == audit['exact_ordered4_candidate_target_full_pins'] == plan['ordered_completed_derived_spool_full_pins'] and len(targets) == 4 and all((set(p) == {'path', 'sha256', 'size_bytes', 'identity'} for p in targets)) and ([p['size_bytes'] for p in targets] == [16953344, 74693004, 16953344, 74693004]) and (sum((p['size_bytes'] for p in targets)) == 183292696) and (native == audit['retained_exact_canonical_observer_XSM_full_pins']) and (len(native) == 2), 'exact ordered finalA SQL/pool then finalB SQL/pool and their canonical observer native2')
    posts = {}
    reports = {}
    specs = (('A_full_aggregate', 'INDEPENDENT_ACTUAL_CURRENT_A_FULL_AGGREGATE_AFTER_OVERV_METADATA_POSTVERIFY_V1', 'PASS_RECORDED_CURRENT_A_FULL_AGGREGATE_SOURCE_GAP0_METADATA_ONLY_CHILD2_PRESERVED', 'actual_Host_report_pin', 'actual_Root_tools_pin'), ('A_three_producer_typed_compare', 'INDEPENDENT_ACTUAL_SAVED_THREE_TYPED_PATH_FINITE_POSTVERIFICATION_V1', 'PASS_ACTUAL_SAVED_THREE_TYPED_PATH_FINITE_POSTVERIFICATION', 'actual_Host_report_pin', 'actual_Root_true_tool_pin'), ('A_OVERV_control', 'INDEPENDENT_OVERV_ORIGINAL_MIXED_PRECISION_INTEGER_CONTROL_ACTUAL_POSTVERIFICATION_V1', 'PASS_ACTUAL_OVERV_ORIGINAL_MIXED_PRECISION_CURRENT_CONTROL_FACTS_POSTVERIFIED_NO_HISTORICAL_OR_PHYSICS_QUALIFICATION', 'actual_report_pin', 'actual_Root_true_tool_return_pin'), ('B_full_aggregate', None, None, 'actual_Host_report_pin', 'actual_Root_tools_pin'), ('B_B55_vs_nativeB2_typed_compare', 'RECORDED_CURRENT_B55_NATIVEWARM_B2_COMPLETE_TYPED_COMPARISON_METADATA_POSTVERIFY_V2', 'PASS_ACTUAL_CURRENT_B55_B2_COMPLETE_TYPED_COMPARISON_V2_ROOT0_CHILD2_METADATA_ONLY_DIFFERENCES_RECORDED', 'actual_Host_report_pin', 'actual_Root_tools_pin'), ('B55_OVERV_control', 'RECORDED_CURRENT_B55_OVERV_NATIVE_INTEGER_CONTROL_METADATA_POSTVERIFY_V1', 'PASS_ACTUAL_CURRENT_B55_OVERV_THREE_STAGE0_2960_WORDS_MATCH_METADATA_ONLY_NO_PHYSICS_QUALIFICATION', 'actual_Host_report_pin', 'actual_Root_tools_pin'))
    for name, schema, status, hostfield, toolsfield in specs:
        c = audit['completed_consumer_closures'][name]
        report = meta(c['Root_report'])
        raw = meta(c['Root_tools'])
        post = meta(c['post'])
        tools = meta(c['post_tools'])
        genuine(raw, 'actual_terminal_return', c['Root_report'], 'report_pin')
        if name == 'A_three_producer_typed_compare':
            r = tools['actual_terminal_return']
            text = tools['actual_initial_return']['output'] + r['output']
            need(tools['observed_closed'] is True and type(tools['original_integer_exit_code']) is int and (tools['original_integer_exit_code'] == 0) and (type(r['exit_code']) is int) and (r['exit_code'] == 0) and ('session_id' not in r) and (tools['actual_full_stdout'] == text) and (json.loads(text.splitlines()[-1])['review_pin'] == c['post']), 'exact historical A3post initialstdout+terminal0 source, no fabricated terminal stdout alias')
        else:
            genuine(tools, 'actual_review_return', c['post'], 'review_pin')
        if name == 'B_full_aggregate':
            schema = c['post_schema']
            status = c['post_status']
        need(report['failure'] is None and post['schema'] == schema and (post['status'] == status) and (post['failure'] is None) and (post[hostfield] == c['Root_report']) and (post[toolsfield] == c['Root_tools']) and (type(post['actual_Root_integer_exit_code']) is int) and (post['actual_Root_integer_exit_code'] == 0), 'six genuine completed Root0/independentpost0 exact report/tool roles, not Source status substituted')
        posts[name] = post
        reports[name] = report
    A = posts['A_full_aggregate']
    B = posts['B_full_aggregate']
    T = posts['A_three_producer_typed_compare']
    C = posts['B_B55_vs_nativeB2_typed_compare']
    AC = posts['A_OVERV_control']
    BC = posts['B55_OVERV_control']
    for post in (A, B, C):
        need(type(post['actual_child_integer_exit_code']) is int and post['actual_child_integer_exit_code'] == 2, 'original completed evidence-only child2/FAILED preserved')
    need(type(T['original_intentional_evidence_child_exit_code']) is int and T['original_intentional_evidence_child_exit_code'] == 2, 'original A-three comparison evidence child2 preserved')
    need(A['actual_snapshot_count'] == 8 and A['actual_context_event_count'] == 55 and (A['actual_compared_source_fields'] == 19249) and (A['actual_all_mismatch_elements'] == A['actual_unknown_macro_producers'] == A['actual_context_or_operand_issues'] == 0) and (A['complete_phases'] == [dict(phase=x, computation_finished=True) for x in ('scattering', 'scalar', 'fission', 'extras', 'overv_fallback', 'metadata')]), 'A8/55/full19249/sixphase completed actual zeros')
    expectedB = dict(actual_compared_source_fields=19249, actual_compared_known_elements=1829421, actual_context_or_operand_issues=0, actual_all_mismatch_elements=0, actual_unknown_macro_producers=0)
    need(all((type(B[k]) is int and B[k] == v for k, v in expectedB.items())) and B['actual_snapshot_pair_count'] == 8 and (B['actual_context_event_count'] == 55) and (B['actual_six_phase_results'] == A['complete_phases']), 'B8/55/full19249/1829421/sixphase completed actual zeros')
    ar = meta(A['actual_execution_request_pin'])
    apair = ar['aggregation_binding']['actual_context_states']['A']['all_snapshot_pairs'][-1]
    bpair = B['all_snapshot_pairs'][-1]
    need(apair['event'] == bpair['event'] == 55 and apair['role'] == bpair['role'] == 'final-complete-micro' and ([apair['sqlite_pin'], apair['native_pool_pin'], bpair['sqlite_pin'], bpair['native_pool_pin']] == targets) and ([apair['input_pin'], bpair['input_pin']] == native), 'completed original consumers actually used these exact four derived spools from two retained native snapshots')
    tc = meta(T['actual_child_report_pin'])
    cc = meta(C['control_plan_pin'])
    need(tc['observed_pair'] == apair and (T['total_macro_record_comparisons'], T['total_compared_original_words'], T['all_raw_word_mismatches'], T['all_metadata_mismatches']) == (58860, 6792456, 0, 0) and (cc['observed_B55_pair'] == bpair) and (C['actual_comparison_counts'] == dict(compared_all_macro_records=19620, compared_original_payload_words=2264152, raw_word_mismatches=0, metadata_mismatches=0)) and (C['actual_path_sets_equal'] is True) and (C['actual_exact_inventory_metadata_and_all_words_equal'] is True), 'A wholethree58860/6792456 and B19620/2264152 completed original typed/allword comparisons zero')
    am = A['current_OVERV_control_admission_metadata']
    ac = audit['completed_consumer_closures']['A_OVERV_control']
    bc = audit['completed_consumer_closures']['B55_OVERV_control']
    need(am['same_original_final_pair'] == apair and all((am['control_metadata_pins'][k] == ac[j] for k, j in (('control_report', 'Root_report'), ('control_returns', 'Root_tools'), ('control_post', 'post'), ('control_post_returns', 'post_tools')))) and (AC['actual_current_overv_words_compared'] == 2960) and (AC['all_current_native_vs_independent_integer_model_vs_saved_words_equal'] is True) and (len(AC['actual_watchdog_results']) == 3) and all((type(w['returncode']) is int and w['returncode'] == 0 and (w['limit_failure'] is None) for w in AC['actual_watchdog_results'])) and (BC['selected_actual_B55_SQL_pool_pair'] == dict(sqlite_pin=targets[2], native_pool_pin=targets[3])) and (BC['actual_child_integer_exit_codes'] == [0, 0, 0]) and all((type(x) is int for x in BC['actual_child_integer_exit_codes'])) and (BC['all_current_native_vs_integer_model_vs_saved_word_equality_recorded_by_actual_Root'] is True), 'both actual ENERGY/2960word OVERV controls consumed exact final pairs; all original stage0 facts preserved')
    pending = meta(plan['specific_pending_new_B_context_Source_plan_pin'])
    need(pending['schema'] == 'DRAFT_NEW_A1_B2_A3_COMPLETE_CONTEXT_AND_PLANE2_UNSEALED_CONSUMER_PLAN_V1' and pending['Source_only'] is True and (pending['Source_admission_ready'] is False) and (pending['draft_unready'] is True) and (pending['compiler_executed'] is False) and (pending['native_executed'] is False) and (pending['actual_new_ARCHIVE_pin'] is None) and (pending['actual_new_GLOBAL_pin'] is None) and (pending['actual_new_PROJECT_pin'] is None) and (pending['actual_plane2_QBUILD_and_strict_BOOTB_result_pin'] is None), 'only this specified unfinished newB native-only Source plan audited, never all future science consumers globally waived')
    for e in audit['actual_consumer_and_future_native_only_Source_evidence']:
        full(e['Source_pin'])
        lines = Path(e['Source_pin']['path']).read_text().splitlines()
        need(all((lines[x['line'] - 1] == x['text'] for x in e['exact_lines'])), 'exact completed consumer and specified future native-only Source call evidence')
    for p in native + audit['required_result_documents_preserved_pins']:
        need(p in plan['retained_current7_pins'], 'canonical native and all result documents are never temporary targets')
        current(p)
    need(plan['future_use_requires_new_full_native_extraction_and_independent_admission'] is True and plan['new_SQL_or_pool_byte_identity_with_retired_file_claimed'] is False and (plan['old_SQLgzip_with_newly_extracted_pool_automatically_compatible_claimed'] is False) and (plan['all_original_spool_file_bytes_archived_or_reconstructable_claimed'] is False), 'completed temporary spool lifecycle only; replay requires newly admitted full extraction, no oldbyte or SQLgzip/newpool compatibility promise')
    return (audit, dict(completed_consumer_closure_pins=audit['completed_consumer_closures'], A_full6phase_counts=audit['A_full6phase_counts'], A_saved_three_typed_counts=audit['A_saved_three_typed_counts'], B_full6phase_counts=expectedB, B_full_typed_counts=C['actual_comparison_counts'], retained_exact_canonical_observer_XSM_full_pins=native, specific_pending_native_only_B_context_Source_plan_pin=plan['specific_pending_new_B_context_Source_plan_pin'], all_future_scientific_consumers_claimed_native_only=False))

def complete_archive_metadata(plan,receipt,check_targets_live):
 archiveplan=meta(plan['inherited_exact28_retirement_plan_pin']);roots=plan['complete_joint_roots'];build=meta(plan['original_guard_build_plan_pin'])
 need(roots==receipt['complete_joint_roots']==archiveplan['complete_joint_roots']and len(roots)==83 and plan['no_new_output_root']is True and plan['original_caps']==archiveplan['original_caps']==CAPS and len(roots)==len(set(roots))and all(not Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b)and any(PACKAGE.is_relative_to(Path(x))for x in roots),'whole existing83, no new data root or resource reset')
 need(plan['actual_six_completed_consumers_closed0']is True and plan['actual_exact28_execute0_independent_post0_complete']is True and plan['temporary_completed_derived_spool_lifecycle_only']is True and plan['all_original_spool_file_bytes_archived_or_reconstructable_claimed']is False,'only completed derived temporary lifecycle, no old-byte reconstruction or archive-success claim')
 cp = plan['actual_exact28_retirement_closure_pins']
 need(all((type(cp[k]) is dict for k in ('receipt', 'Root_tools', 'post', 'post_tools'))) and plan['actual_exact28_execute0_independent_post0_complete'] is True, 'future exact28 actualexecute0 plus independentpost0 NULL hard reject')
 receipt28 = meta(cp['receipt'])
 raw28 = meta(cp['Root_tools'])
 post28 = meta(cp['post'])
 tools28 = meta(cp['post_tools'])
 genuine(raw28, 'actual_terminal_return', cp['receipt'], 'receipt_pin')
 genuine(tools28, 'actual_review_return', cp['post'], 'review_pin')
 contract = plan['actual_exact28_post_key_projection']
 need(type(contract) is dict and type(plan['actual_exact28_post_Source_projection_pin']) is dict, 'exact future frozen execute-post schema/field projection required')
 projection = meta(plan['actual_exact28_post_Source_projection_pin'])
 need(projection['schema'] == contract['schema'] and projection['status'] == contract['status'], 'same frozen execute-post Source contract')
 need(receipt28['schema'] == 'CURRENT_B_COMPLETE28_JSONL_EXACT28_ORIGINAL_RETIREMENT_RECEIPT_V1' and receipt28['mode'] == 'execute' and (receipt28['status'] == 'RETIRED_CURRENT_B_COMPLETE28_JSONL_EXACT28_ORIGINAL_COMPLETE_BYTES_IN_ARCHIVE') and (receipt28['failure'] is None) and (receipt28['plan_pin'] == plan['inherited_exact28_retirement_plan_pin']) and (receipt28['exact_target_pins'] == receipt28['actual_released_pins'] == archiveplan['exact_target_pins'] == plan['exact28_retired_result_JSONL_target_pins']) and (receipt28['actual_released_bytes'] == 249929878) and (receipt28['files_deleted'] is True) and (receipt28['resources_after_original_classes_forced_fresh'] is True), 'genuine exact28 result plaintext retirement execute0, never readonly/postonly substituted')
 need(post28['schema'] == contract['schema'] == 'CURRENT_B_COMPLETE28_JSONL_EXACT28_ACTUAL_EXECUTION_METADATA_POSTVERIFY_V1' and post28['status'] == contract['status'] == 'PASS_ACTUAL_B_COMPLETE28_JSONL_EXACT28_ORIGINALS_RETIRED_FULL_BYTES_ARCHIVED_METADATA_ONLY' and (post28['failure'] is None) and (post28['metadata_only'] is True) and (post28['actual_execution_receipt_pin'] == cp['receipt']) and (post28['actual_Root_tools_pin'] == cp['Root_tools']) and (post28['plan_pin'] == plan['inherited_exact28_retirement_plan_pin']) and (post28['source_pin'] == receipt28['source_pin']) and (type(post28['actual_Root_integer_exit_code']) is int) and (post28['actual_Root_integer_exit_code'] == 0) and (post28['exact_target_pins'] == post28['actual_released_pins'] == plan['exact28_retired_result_JSONL_target_pins']) and (post28['actual_released_bytes'] == 249929878) and (post28['files_deleted'] is True) and (post28['files_deleted_by_post'] is False) and (post28['resources_after_original_classes_forced_fresh'] is True) and (post28[contract['exact28_absence_twice_field']] is True), 'real independent exact28 execute metadata0 including preciseabsence, originalfullbytes archived')
 targets = plan['exact_target_pins']
 completed = plan['ordered_completed_derived_spool_full_pins']
 need(targets == completed and len(targets) == len({p['path'] for p in targets}) == 4 and (sum((p['size_bytes'] for p in targets)) == plan['planned_released_bytes'] == plan['target_total_bytes'] == 183292696), 'only four completed finalA/finalB SQL/pool derived temporaries, never original data')
 audit, consumedProof = admit_completed_consumers(plan, archiveplan)
 need(post28[contract['retained_current7_array_field']] == receipt28['retained_current7_pins'] and post28['all_retained_roles_current7_verified_twice'] is True and (plan['retained_current7_pins'] == unique([p for p in post28[contract['retained_current7_array_field']] if p not in targets] + audit['retained_exact_canonical_observer_XSM_full_pins'] + audit['required_result_documents_preserved_pins'])) and (plan['retained_failed_v1_current7_only_pins'] == archiveplan['retained_failed_v1_current7_only_pins']) and (plan['retained_failed_pool_archive_current7_only_pins'] == archiveplan['retained_failed_pool_archive_current7_only_pins']) and (plan['retained_B2_current_epoch_readonly_pins'] == archiveplan['retained_B2_current_epoch_readonly_pins']), 'latest exact28 actual post current-role array minus only four targets plus explicitly preserved native/docs, never assume old E16 selected roles were complete')
 gzips = plan['permanent_result28_gzip_pins']
 entries = plan['permanent_result28_entry_pins']
 indexpin = plan['permanent_result28_lookup_index_pin']
 empty = plan['retained_empty_numeric_mismatch_JSONL_pin']
 need(gzips == archiveplan['retained_ordered_result_JSONL_gzip_pins'] == receipt28['compressed_result_full_pins'] == post28['retained_ordered_result_JSONL_gzip_pins'] and entries == archiveplan['retained_ordered_result_JSONL_entry_pins'] == receipt28['retained_ordered_result_JSONL_entry_pins'] == post28['retained_ordered_result_JSONL_entry_pins'] and (indexpin == archiveplan['actual_archive_closure_pins']['index'] == receipt28['original_lookup_index_pin'] == post28['original_lookup_index_pin']) and (len(gzips) == len(entries) == 28) and (empty == archiveplan['retained_empty_numeric_mismatch_JSONL_pin'] == post28['retained_empty_numeric_mismatch_JSONL_pin']) and (empty['size_bytes'] == 0) and (post28['exact16_retired_temporary_target_pins'] == plan['exact16_retired_temporary_target_pins']) and (post28['historical_retired_presence_full_pin'] == plan['historical_retired_presence_full_pin']) and (post28['past_exact16_and_presence_historical_absence_only'] is True), 'permanent full28 gzip/entry/lookup exact original order and empty0 plus exact historical roles genuinely checked by actual post; original entry creation history unchanged')
 index = meta(indexpin)
 need(index['ordered_original_result_JSONL_pins'] == plan['exact28_retired_result_JSONL_target_pins'] and index['ordered_result_JSONL_archive_entry_pins'] == entries and ([r['compressed_archive_full_pin'] for r in index['entries']] == gzips), 'precise permanent result restoremapping for full28 no generic missing skip')
 proofpins = list(cp.values()) + [plan['inherited_exact28_retirement_plan_pin'], plan['actual_exact28_post_Source_projection_pin'], plan['actual_completed_spool_role_audit_pin'], plan['specific_pending_new_B_context_Source_plan_pin']] + [c[k] for c in audit['completed_consumer_closures'].values() for k in ('Root_report', 'Root_tools', 'post', 'post_tools')] + [e['Source_pin'] for e in audit['actual_consumer_and_future_native_only_Source_evidence']]
 need(plan['retained_archive_metadata_current7_pins'] == unique(archiveplan['retained_archive_metadata_current7_pins'] + proofpins) and plan['explicit_cumulative_metadata_file_pins'] == unique(archiveplan['explicit_cumulative_metadata_file_pins'] + proofpins), 'full inherited cumulativemetadata plus exact new lifecycle/sixconsumer/Source proofs, no excluded externalaccounting')
 need(plan['exact16_retired_temporary_target_pins'] == archiveplan['exact16_retired_temporary_target_pins'] and plan['historical_retired_presence_full_pin'] == archiveplan['historical_retired_presence_full_pin'], 'same exact priorhistorical roles, never current relabelled')
 retained = plan['retained_current7_pins'] + plan['retained_archive_metadata_current7_pins'] + plan['explicit_cumulative_metadata_file_pins'] + plan['retained_B2_current_epoch_readonly_pins'] + gzips + entries + [indexpin, empty]
 need(not {p['path'] for p in targets} & {p['path'] for p in retained + plan['retained_failed_v1_current7_only_pins'] + plan['retained_failed_pool_archive_current7_only_pins']}, 'precise four target paths excluded from everyretained role; native/results/docs/archive/history never target')
 exact_historical_absence(plan)
 need(receipt['exact_target_pins']==targets and receipt['completed_derived_spool_full_pins']==completed and receipt['target_role_kinds']==plan['target_role_kinds']and receipt['actual_completed_consumer_proof']==consumedProof and receipt['actual_exact28_retirement_closure_pins']==cp,'same exact four targets and all six actual consumer closure proofs/counts')
 need(receipt['temporary_completed_derived_spool_lifecycle_only']is True and receipt['all_authoritative_native_and_completed_result_documents_preserved']is True and receipt['retired_spool_file_bytes_archived_or_byte_reconstructable_claimed']is False and receipt['complete_pair_archive_success']is False and receipt['historical_original_PFs_not_current_relabelled']is True and receipt['generic_missing_path_skip_authorized']is False,'completed temporary lifecycle only, retained canonical native/results and no fabricated pair-archive or byte restoration claim')
 need(receipt['future_use_requires_new_full_native_extraction_and_independent_admission']is True and receipt['new_SQL_or_pool_byte_identity_with_retired_file_claimed']is False and receipt['old_SQLgzip_with_newly_extracted_pool_automatically_compatible_claimed']is False and receipt['completed_derived_spools_retired']is(not check_targets_live)and receipt['all_future_scientific_consumers_claimed_native_only']is False and receipt['specific_pending_native_only_B_context_Source_plan_pin']==plan['specific_pending_new_B_context_Source_plan_pin'],'newly admitted full native extraction required; no oldbyte/automatic pool compatibility or global future-consumer waiver')
 for k in('retained_current7_pins','retained_failed_v1_current7_only_pins','retained_failed_pool_archive_current7_only_pins','retained_B2_current_epoch_readonly_pins','retained_archive_metadata_current7_pins','exact16_retired_temporary_target_pins','historical_retired_presence_full_pin','exact28_retired_result_JSONL_target_pins','permanent_result28_gzip_pins','permanent_result28_entry_pins','permanent_result28_lookup_index_pin','retained_empty_numeric_mismatch_JSONL_pin'):need(receipt[k]==plan[k],'actual exact retainer, archive and narrow historical-role tables match frozen plan')
 for _ in range(2):
  if check_targets_live:
   for p in completed:current(p)
  else:
   for p in targets:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only exact four genuinely retired temporary paths absent; never stat retired targets as current')
  for p in retained:current_role(p,build)
  for p in plan['retained_failed_v1_current7_only_pins']:current_failed_v1(p,plan)
  for p in plan['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,plan)
  exact_historical_absence(plan)
 return roots,targets,gzips,entries,cp,plan['exact16_retired_temporary_target_pins']+[plan['historical_retired_presence_full_pin']]+plan['exact28_retired_result_JSONL_target_pins'],consumedProof


def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('execution-receipt-pin','Root-tools-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'exact independent executor and immutable single execution post')
 pReceipt=json.loads(a.execution_receipt_pin);pTools=json.loads(a.Root_tools_pin);tools=meta(pTools);terminal=tools['actual_terminal_return'];receipt=None if pReceipt is None else meta(pReceipt)
 need(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==tools['original_integer_exit_code']and terminal.get('session_id')is None,'genuine observed closed execution Root integer; no live handle inference')
 author_pin=pin(PACKAGE/'AUTHOR_SOURCE_FREEZE.json');need(author_pin==EXPECTED_CORE_AUTHOR_FREEZE,'exact frozen core author metadata PF');author=meta(author_pin);pp=author['whole_plan_pin'];plan=meta(pp);source_limit=plan['bounded_own_Source_metadata_receipts_bytes'];ps=next(p for p in author['whole_Source_file_pins']if p['path']==str(PACKAGE/'retire_exact4_completed_A_B_final55_SQL_pool_spools.UNREADY.py'))
 need(source_limit==8*2**20 and pp['path']==str(PACKAGE/'PLAN.json')and plan['schema']=='CURRENT_A_B_FINAL55_COMPLETED_DERIVED_SPOOL_EXACT4_LIFECYCLE_PLAN_V1'and plan['Source_admission_ready']is True and plan['draft_unready']is False and plan['original_caps']==CAPS,'same frozen A_B_final55_completed_spool_exact4 Source/PLAN and unchanged original global caps/localSource8MiB')
 if pReceipt is not None:need(pReceipt['path']==str(PACKAGE/'EXECUTION_RECEIPT.json')and receipt['schema']=='CURRENT_A_B_FINAL55_COMPLETED_DERIVED_SPOOL_EXACT4_LIFECYCLE_RECEIPT_V1'and receipt['mode']=='execute'and receipt['source_pin']==ps and receipt['plan_pin']==pp,'actual exact owning execution receipt/schema/mode and Source/plan')
 code=tools['original_integer_exit_code']
 if code!=0:
  result=dict(schema='CURRENT_A_B_FINAL55_COMPLETED_DERIVED_SPOOL_EXACT4_EXECUTION_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_execution_receipt_pin=pReceipt,actual_Root_tools_pin=pTools,actual_Root_integer_exit_code=code,actual_receipt_status=None if receipt is None else receipt['status'],actual_receipt_failure=None if receipt is None else receipt['failure'],actual_released_pins=None if receipt is None else receipt['actual_released_pins'],actual_released_bytes=None if receipt is None else receipt['actual_released_bytes'],files_deleted=None if receipt is None else receipt['files_deleted'],source_pin=ps,plan_pin=pp,full_A_B_final55_completed_spool_exact4_retirement_success_inferred=False)
  save(result,source_limit);return
 need(receipt is not None,'actual execution Root0 requires emitted exact receipt PF');genuine(tools,'actual_terminal_return',pReceipt,'receipt_pin')
 need(tools['actual_execution_permission_mode']=='require_escalated'and receipt['status']=='RETIRED_CURRENT_A_B_FINAL55_COMPLETED_SPOOL_EXACT4_DERIVED_TEMPORARIES_ONLY'and receipt['failure']is None and receipt['files_deleted']is True and receipt['all_authoritative_native_and_completed_result_documents_preserved']is True and receipt['resources_after_original_classes_forced_fresh']is True,'actual A_B_final55_completed_spool_exact4 execution Root0/retirement/no lost complete result bytes/fresh original resource closure')
 targets=plan['exact_target_pins'];released=receipt['actual_released_pins'];releasedbytes=receipt['actual_released_bytes'];expectedbytes=sum(p['size_bytes']for p in targets)
 need(receipt['exact_target_pins']==released==targets and len(targets)==len({p['path']for p in targets})==4 and type(releasedbytes)is int and releasedbytes==expectedbytes==plan['target_total_bytes']==plan['planned_released_bytes']and json.loads(terminal['output'].strip().splitlines()[-1])['actual_released_bytes']==releasedbytes,'actual precisely ordered two exact SQL/partial fullPF target and exact bytes in receipt/genuine stdout')
 for p in targets:
  need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'only genuinely deleted exact target paths absent; historical fullPF never relabelled current')
 cli_pin=pin(PACKAGE/'ROOT_EXECUTE_REVIEWABLE_CLI.json');cli=meta(cli_pin)
 need(cli['schema']=='CURRENT_A_B_FINAL55_COMPLETED_DERIVED_SPOOL_EXACT4_LIFECYCLE_GUARDED_REVIEWABLE_CLI_V1'and cli['mode']=='execute'and cli['source_pin']==ps and cli['plan_pin']==pp and cli['independent_Source_review_pin']==receipt['peer_review_pin']and cli['independent_Source_review_tools_pin']==receipt['peer_tools_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated'and shlex.split(tools['exact_executed_command'])==cli['argv']==shlex.split(cli['command']),'actual exact published execute CLI and same Source/plan/peer identities')
 for p in author['whole_Source_file_pins']:full(p);full(p)
 peer=meta(receipt['peer_review_pin']);peer_tools=meta(receipt['peer_tools_pin']);genuine(peer_tools,'actual_review_return',receipt['peer_review_pin'],'review_pin');need(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')and peer['source_pin']==ps and peer['plan_pin']==pp,'genuine independent Source review0 for same exact worker/plan')
 readonly_pin=receipt['actual_readonly_receipt_pin'];readonly_tools_pin=receipt['actual_readonly_tools_pin'];readonly_post_pin=receipt['actual_readonly_post_pin'];readonly_post_tools_pin=receipt['actual_readonly_post_tools_pin']
 need(cli['actual_readonly_receipt_pin']==readonly_pin and cli['actual_readonly_tools_pin']==readonly_tools_pin and cli['actual_readonly_post_pin']==readonly_post_pin and cli['actual_readonly_post_tools_pin']==readonly_post_tools_pin,'actual execute CLI/receipt consumes exact genuine readonly0/post0 PFs')
 readonly=meta(readonly_pin);readonly_tools=meta(readonly_tools_pin);readonly_post=meta(readonly_post_pin);readonly_post_tools=meta(readonly_post_tools_pin);genuine(readonly_tools,'actual_readonly_return',readonly_pin,'receipt_pin');genuine(readonly_post_tools,'actual_review_return',readonly_post_pin,'review_pin')
 need(readonly_pin['path']==str(PACKAGE/'READONLY_RECEIPT.json')and readonly_tools['actual_readonly_permission_mode']=='require_escalated'and readonly['schema']=='CURRENT_A_B_FINAL55_COMPLETED_DERIVED_SPOOL_EXACT4_LIFECYCLE_RECEIPT_V1'and readonly['mode']=='check'and readonly['status']=='READONLY_READY_CURRENT_A_B_FINAL55_COMPLETED_SPOOL_EXACT4_NO_UNLINK'and readonly['failure']is None and readonly['source_pin']==ps and readonly['plan_pin']==pp and readonly['exact_target_pins']==targets and readonly['actual_released_pins']==[]and readonly['actual_released_bytes']==0 and readonly['files_deleted']is False and readonly['resources_after_original_classes_forced_fresh']is True,'actual earlier readonly Root0/no-unlink/fresh resource proof remains historical and unmodified')
 contract=plan['readonly_post_report_contract'];need(readonly_post['schema']==contract['schema']and readonly_post['status']==contract['status']and readonly_post['failure']is None and readonly_post['metadata_only']is True and readonly_post['actual_readonly_receipt_pin']==readonly_pin and readonly_post['actual_readonly_tools_pin']==readonly_tools_pin and readonly_post['source_pin']==ps and readonly_post['plan_pin']==pp and readonly_post['exact_target_pins']==targets and readonly_post['actual_released_pins']==[]and readonly_post['actual_released_bytes']==0 and readonly_post['files_deleted']is False and readonly_post['resources_after_original_classes_forced_fresh']is True and type(readonly_post['actual_readonly_Root_integer_exit_code'])is int and readonly_post['actual_readonly_Root_integer_exit_code']==0,'genuine independent readonly metadata post0 exact execution prerequisite, not self-reexecuted')
 lsof=receipt['actual_lsof_owner_check'];need(lsof['argv']==['/usr/sbin/lsof','-n','-P','-Fpcfn','--']+[p['path']for p in targets]and type(lsof['returncode'])is int and lsof['returncode']==1 and lsof['stdout']==lsof['stderr']=='','actual saved original A_B_final55_completed_spool_exact4 lsof owner check1/empty only; lsof not repeated by post')
 roots,targets,archives,entries,archive_cp,historical,archive_post=complete_archive_metadata(plan,receipt,False)
 readonly_resource_facts(receipt['resources_before'],roots);readonly_resource_facts(receipt['resources_after'],roots)
 for name in('history','joint'):need(type(receipt['resources_after'][name]['checked_unix'])in(int,float)and receipt['resources_after'][name]['checked_unix']>=receipt['resources_before'][name]['checked_unix'],'saved forced-fresh after original resource scans follow before scans, no fabricated final-unlink timestamp')
 need(receipt['all_authoritative_native_and_completed_result_documents_preserved']is True and receipt['complete_pair_archive_success']is False and receipt['future_use_requires_new_full_native_extraction_and_independent_admission']is True,'canonical native and completed result documents retained; future replay needs new extraction/admission, no archive success inferred')
 for key in('numerical_executed','compiler_executed','JSONL_or_array_values_decoded','compression_repeated','decompression_repeated','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(receipt[key]is False,'exact cleanup metadata cannot mint science/physical/goal qualification')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in plan['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current unchanged original cumulative/free reserve with post metadata and own open-unlinked')
 for p in(pReceipt,pTools,ps,pp,receipt['peer_review_pin'],receipt['peer_tools_pin'],cli_pin,author_pin,readonly_pin,readonly_tools_pin,readonly_post_pin,readonly_post_tools_pin):full(p)
 result=dict(schema='CURRENT_A_B_FINAL55_COMPLETED_SPOOL_EXACT4_EXECUTION_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_A_B_FINAL55_COMPLETED_SPOOL_EXACT4_TEMPORARIES_RETIRED_NATIVE_AND_RESULTS_PRESERVED_METADATA_ONLY',failure=None,actual_execution_receipt_pin=pReceipt,actual_Root_tools_pin=pTools,actual_Root_integer_exit_code=0,source_pin=ps,plan_pin=pp,exact_target_pins=targets,actual_released_pins=released,actual_released_bytes=releasedbytes,files_deleted=True,exact_four_targets_absent_verified_twice=True,resources_after_original_classes_forced_fresh=True,actual_readonly_receipt_pin=readonly_pin,actual_readonly_tools_pin=readonly_tools_pin,actual_readonly_post_pin=readonly_post_pin,actual_readonly_post_tools_pin=readonly_post_tools_pin,actual_execute_reviewable_CLI_pin=cli_pin,actual_Source_peer_pin=receipt['peer_review_pin'],actual_Source_peer_tools_pin=receipt['peer_tools_pin'],actual_Source_author_freeze_pin=author_pin,actual_saved_lsof_owner_check=lsof,completed_derived_spool_full_pins=plan['ordered_completed_derived_spool_full_pins'],target_role_kinds=plan['target_role_kinds'],actual_completed_consumer_proof=archive_post,actual_exact28_retirement_closure_pins=archive_cp,temporary_completed_derived_spool_lifecycle_only=True,all_authoritative_native_and_completed_result_documents_preserved=True,retired_spool_file_bytes_archived_or_byte_reconstructable_claimed=False,future_use_requires_new_full_native_extraction_and_independent_admission=True,new_SQL_or_pool_byte_identity_with_retired_file_claimed=False,old_SQLgzip_with_newly_extracted_pool_automatically_compatible_claimed=False,all_future_scientific_consumers_claimed_native_only=False,specific_pending_native_only_B_context_Source_plan_pin=plan['specific_pending_new_B_context_Source_plan_pin'],complete_pair_archive_success=False,completed_derived_spools_retired=True,retained_exact_canonical_observer_XSM_full_pins=plan['retained_exact_canonical_observer_XSM_full_pins'],permanent_result28_gzip_pins=archives,permanent_result28_entry_pins=entries,permanent_result28_lookup_index_pin=plan['permanent_result28_lookup_index_pin'],retained_empty_numeric_mismatch_JSONL_pin=plan['retained_empty_numeric_mismatch_JSONL_pin'],exact16_retired_temporary_target_pins=plan['exact16_retired_temporary_target_pins'],historical_retired_presence_full_pin=plan['historical_retired_presence_full_pin'],exact28_retired_result_JSONL_target_pins=plan['exact28_retired_result_JSONL_target_pins'],historical45_absence_only_verified_twice=True,retained_failed_pool_archive_current7_only_pins=plan['retained_failed_pool_archive_current7_only_pins'],retained_failed_v1_current7_only_pins=plan['retained_failed_v1_current7_only_pins'],prior_v1_Root1_child_minus15_unknown_counts_equality_preserved=True,prior_partial_payload_body_not_opened_or_hashed_by_post=True,retained_all_current7_pins=plan['retained_current7_pins'],retained_B2_current_epoch_readonly_pins=plan['retained_B2_current_epoch_readonly_pins'],retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'],all_retained_roles_current7_verified_twice=True,generic_missing_path_skip_authorized=False,historical_deleted_target_PFs_not_claimed_current=True,local_Source_bound_bytes=source_limit,complete_joint_roots=roots,no_new_output_root=True,original_caps=CAPS,actual_original_resources_before=receipt['resources_before'],actual_original_resources_after=receipt['resources_after'],current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked)
 save(result,source_limit,joint+extra+unlinked)

if __name__=='__main__':main()
