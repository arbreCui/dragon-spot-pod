"""Independent full B55/nativeWarmB2 typed original-word comparison Source/metadata review. No candidate/helper imports."""
import argparse, ast, hashlib, json, os, resource, stat, sys, time
from pathlib import Path

BASE=Path(__file__).absolute().parent
PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
OUT=ROOT/'validation/artifacts/axial-material-current-B55-nativeWarmB2-complete-typed-macro-compare-20261015-v2'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(B_native_executed=False,B_observation_context_produced=False,compiled_IO_semantics_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
START=time.monotonic()
FULL={}
CURRENT={}
FAILED_CURRENT7={}
SOURCE_BOUND=16*2**20

def need(value,message):
    if value is not True:raise RuntimeError(message)

def budget():
    need(time.monotonic()-START<600,'Source reviewer600s')
    need(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)<512*2**20,'Source reviewer512MiB')

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def current(p):
    budget();q=Path(p['path']);s=q.lstat()
    need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents)),'literal current role without aliases')
    need(type(p['size_bytes'])is int and len(p['identity'])==7 and all(type(v)is int for v in p['identity'])and identity(s)==p['identity']and s.st_size==p['size_bytes']and stat.S_ISREG(s.st_mode),'exact fullPF integer7 current role')
    special=q==Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_nlink==2
    need(s.st_nlink==1 or special,'ordinary one-link or exact original Fortran role')
    if set(p)=={'path','size_bytes','identity'}:
        need(FAILED_CURRENT7.get(str(q))==p and s.st_uid==os.getuid(),'only explicitly bound failed-v1 stat-only role, no invented SHA/fullPF');return q
    old=CURRENT.get(str(q));need(old is None or old==p,'one admitted current fullPF per literal path');CURRENT[str(q)]=p
    return q

def full(p):
    q=current(p);need(p['size_bytes']<8*2**20,'Source/control8MiB');h=hashlib.sha256()
    with q.open('rb')as f:
        need(identity(os.fstat(f.fileno()))==p['identity'],'opened Source/control7')
        while True:
            b=f.read(2**20)
            if not b:break
            h.update(b);budget()
        need(identity(os.fstat(f.fileno()))==p['identity'],'EOF Source/control7')
    need(h.hexdigest()==p['sha256'],'complete Source/control SHA');current(p);FULL[str(q)]=p
    return q

def pin_small(q):
    q=Path(q);s=q.lstat();need(s.st_size<8*2**20,'small Source/control discovery')
    p=dict(path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=identity(s));current(p);return p

def meta(p):return json.loads(full(p).read_bytes())

def genuine(value,key,p,output_key):
    t=value[key]
    need(value['observed_closed']is True and type(value['original_integer_exit_code'])is int and value['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None,'genuine closed typed0 tool return')
    need(json.loads(t['output'].strip().splitlines()[-1])[output_key]==p,'genuine tool output binds exact artifact PF')

def functions(text):
    return{n.name:ast.get_source_segment(text,n)for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}

def integer_expression(node):
    if isinstance(node,ast.Constant)and type(node.value)is int:return node.value
    need(isinstance(node,ast.BinOp)and isinstance(node.op,(ast.Add,ast.Sub,ast.Mult,ast.Pow)),'constant integer bound AST only')
    left=integer_expression(node.left);right=integer_expression(node.right)
    if isinstance(node.op,ast.Add):return left+right
    if isinstance(node.op,ast.Sub):return left-right
    if isinstance(node.op,ast.Mult):return left*right
    need(0<=right<=40,'bounded power AST');return left**right

def current_role(p,build):
    q=current(p);s=q.lstat()
    if p in build['readonly_system_SDK_header_pins']:
        root=Path(build['readonly_system_SDK_root']);rs=root.lstat()
        need(str(root)=='/Library/Developer/CommandLineTools/SDKs/MacOSX27.0.sdk'and stat.S_ISDIR(rs.st_mode)and rs.st_uid==0 and identity(rs)==build['readonly_system_SDK_root_identity']and not any(x.is_symlink()for x in(root,*root.parents))and str(q)in{str(root/'usr/include'/n)for n in('stdio.h','stdlib.h','stdint.h')}and s.st_uid==0 and s.st_nlink==1,'only exact selected original readonly SDK roles')
    elif p in build['readonly_system_tool_metadata_pins']:
        need(str(q)in('/bin/ps','/usr/sbin/lsof')and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only explicitly frozen readonly system PS/lsof metadata roles')
    elif p==build['C_compiler_pin']:
        need(str(q)=='/Library/Developer/CommandLineTools/usr/bin/clang'and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only explicit frozen readonly clang metadata role')
    else:need(s.st_uid==os.getuid()and(s.st_nlink==1 or(str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'and s.st_nlink==2 and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492')),'ordinary owned exact role or original immutable Fortran link exception')

def unique(rows):
    t={}
    for p in rows:
        need(p['path']not in t or t[p['path']]==p,'same literal metadata path one exact PF');t[p['path']]=p
    return list(t.values())

def whole_current_bytes(roots):
    n=0
    for value in roots:
        root=Path(value);need(root.is_absolute()and not any(x.is_symlink()for x in(root,*root.parents)),'entire literal resource root without alias')
        if not os.path.lexists(root):continue
        need(root.is_dir(),'resource root is a directory')
        for q in root.rglob('*'):
            budget();s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no alias in entire counted namespace')
            if stat.S_ISREG(s.st_mode):n+=s.st_size
    return n

def own_open_unlinked_bytes():
    rows={}
    for name in os.listdir('/dev/fd'):
        try:s=os.fstat(int(name))
        except(ValueError,OSError):continue
        if stat.S_ISREG(s.st_mode)and s.st_nlink==0:rows[s.st_dev,s.st_ino]=s.st_size
    return sum(rows.values())

def actual_preconditions(plan):
    bridge=meta(plan['actual_B2_current_epoch_bridge_report_pin']);bt=meta(plan['actual_B2_current_epoch_bridge_Root_tools_pin']);bp=meta(plan['actual_B2_current_epoch_bridge_post_pin']);bpt=meta(plan['actual_B2_current_epoch_bridge_post_tools_pin']);genuine(bt,'actual_terminal_return',plan['actual_B2_current_epoch_bridge_report_pin'],'report_pin');genuine(bpt,'actual_review_return',plan['actual_B2_current_epoch_bridge_post_pin'],'review_pin')
    need(bridge['schema']=='ROOT_NATIVE_WARM_B2_CURRENT_EPOCH_BLIND_FULLFILE_BINDING_REPORT_V1'and bridge['status']=='PASS_B2_SELECTED_READONLY_ROLES_CURRENT_EPOCH_BLIND_SHA_ONLY'and bridge['failure']is None and bridge['children_started']==0 and bridge['final_report_resource_check_passed']is True and bridge['original_caps']==CAPS and len(bridge['ordered_role_pairs'])==9,'genuine Root-only nine-role bridge, no data child or lineage/science qualification')
    bc=plan['bridge_post_contract'];need(bp['schema']==bc['schema']and bp['status']==bc['status']and bp['failure']is None and bp['metadata_only']is True and bp[bc['Root_report_pin_field']]==plan['actual_B2_current_epoch_bridge_report_pin']and bp[bc['Root_tools_pin_field']]==plan['actual_B2_current_epoch_bridge_Root_tools_pin'],'independent actual bridgepost0 same Root report/tools')
    need(plan['actual_current_epoch_B2_archive_pin']==bridge['current_epoch_B2_archive_pin']and plan['retained_B2_current_epoch_readonly_pins']==[r['current_epoch_full_pin']for r in bridge['ordered_role_pairs']],'exact current epoch archive and all nine readonly input roles')
    for row in bridge['ordered_role_pairs']:
        old=row['historical_full_pin'];p=row['current_epoch_full_pin'];need(row['blind_complete_SHA_and_length_equal']is True and row['before_open_EOF_after_current7_stable']is True and old['sha256']==p['sha256']and old['size_bytes']==p['size_bytes']and old['identity'][1:]==p['identity'][1:]and old['identity'][0]==16777234 and p['identity'][0]==16777229,'explicit only-device epoch rebind preserves historical seven tuple separately');current(p)
    need(plan['historical_B2_archive_pin']==next(r['historical_full_pin']for r in bridge['ordered_role_pairs']if r['role']=='B2_archive'),'unchanged actual historical B2 role, no guessed alternative index')
    retire=meta(plan['actual_latest_complete_prefix_plan_pin']);r=meta(plan['actual_presence_retirement_receipt_pin']);rt=meta(plan['actual_presence_retirement_Root_tools_pin']);rp=meta(plan['actual_presence_retirement_post_pin']);rpt=meta(plan['actual_presence_retirement_post_tools_pin']);genuine(rt,'actual_terminal_return',plan['actual_presence_retirement_receipt_pin'],'receipt_pin');genuine(rpt,'actual_review_return',plan['actual_presence_retirement_post_pin'],'review_pin')
    target=retire['exact_target_pins'];need(retire['schema']=='CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT_PLAN_V1'and retire['Source_admission_ready']is True and retire['draft_unready']is False and len(target)==1 and target[0]['size_bytes']==169615994 and target[0]['sha256']=='9ac74eebba95d541a6281d61e3be7ad527cf19d44de54078e8ffc7627660eda7','only exact complete presence original historical mapping, no generic missing-file permission')
    need(r['schema']=='CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT_RECEIPT_V1'and r['mode']=='execute'and r['status']=='RETIRED_CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_COMPLETE_BYTES_IN_ARCHIVE'and r['failure']is None and r['plan_pin']==plan['actual_latest_complete_prefix_plan_pin']and r['actual_released_pins']==r['exact_target_pins']==target and type(r['actual_released_bytes'])is int and r['actual_released_bytes']==169615994 and r['files_deleted']is True and r['resources_after_original_classes_forced_fresh']is True,'genuine Root exact1 release and forced-fresh original resource closure')
    need(rp['schema']==retire['execute_post_report_contract']['schema']and rp['status']==retire['execute_post_report_contract']['status']and rp['failure']is None and rp['metadata_only']is True and rp['actual_execution_receipt_pin']==plan['actual_presence_retirement_receipt_pin']and rp['actual_Root_tools_pin']==plan['actual_presence_retirement_Root_tools_pin']and type(rp['actual_Root_integer_exit_code'])is int and rp['actual_Root_integer_exit_code']==0 and rp['actual_released_pins']==target and rp['actual_released_bytes']==169615994 and rp['historical_retired_presence_full_pin']==target[0]and rp['future_consumer_must_use_exact_single_presence_archive_mapping']is True and rp['generic_missing_path_skip_authorized']is False and rp['files_deleted_by_post']is False,'genuine independent exact1 metadata post0, immutable exact original PF and no generic absent-file skipping')
    for p in target:need(not os.path.lexists(p['path']),'only exact presence retired pathname absent; body never read')
    cp=retire['actual_archive_closure_pins'];ap=meta(cp['post']);genuine(meta(cp['post_tools']),'actual_review_return',cp['post'],'review_pin');genuine(meta(cp['Root_tools']),'actual_terminal_return',cp['Host'],'report_pin')
    need(plan['actual_presence_archive_report_pin']==cp['Host']and plan['actual_presence_archive_Root_tools_pin']==cp['Root_tools']and plan['actual_presence_archive_post_pin']==cp['post']and plan['actual_presence_archive_post_tools_pin']==cp['post_tools']and ap['original_presence_full_pin']==target[0]and ap['Root_actual_streamed_decompression_proof_matched_original_fullPF']is True and ap['actual_Root_integer_exit_code']==ap['actual_child_integer_exit_code']==0 and ap['failure']is None,'same true single-presence Root0/child0/post0 archived byte proof; no repeated decompression')
    archive=meta(retire['inherited_complete_archive_plan_pin']);need(plan['retained_current7_pins']==retire['retained_current7_pins']+retire['retained_presence_gzip_pins']+retire['retained_presence_entry_pins']+[cp['index']]and not{p['path']for p in target}&{p['path']for p in plan['retained_current7_pins']+plan['explicit_cumulative_metadata_file_pins']},'all other16 Bagg outputs plus original native/SQLpool/B4all4 gzip-entry-index remain exact current7')
    for p in plan['retained_current7_pins']:current(p)
    lineage=meta(plan['actual_B2_lineage_metadata_audit_pin'])
    return bridge,retire,archive,target,cp,lineage

def admit_failed_v1(packet,extractplan):
 pp=packet['actual_failed_v1_plan_pin'];previous=meta(pp)
 ph=packet['actual_failed_v1_Host_report_pin'];h=meta(ph);raw=meta(packet['actual_failed_v1_Root_tools_pin'])
 postpin=packet['actual_failed_v1_post_pin'];post=meta(postpin)
 genuine(meta(packet['actual_failed_v1_post_tools_pin']),'actual_review_return',postpin,'review_pin')
 cli=meta(packet['actual_failed_v1_final_CLI_pin']);terminal=raw['actual_terminal_return']
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and raw['original_integer_exit_code']==1 and type(terminal['exit_code'])is int and terminal['exit_code']==1 and terminal.get('session_id')is None and raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False and raw['failed_Host_report_pin']==ph and raw['exact_executed_command']==cli['command'],'genuine prior comparisonRoot1, original command/failure preserved; no success stdout invented')
 need(previous['schema']=='CURRENT_B55_B2_COMPLETE_COMPARISON_SOURCE_ONLY_PLAN_V1'and previous['original_caps']==CAPS and len(previous['complete_joint_roots'])==78 and previous['complete_joint_roots'][:-1]==extractplan['complete_joint_roots']and previous['bounded_new_output_reservation_bytes']==32*2**20 and previous['bounded_new_Source_metadata_reservation_bytes']==SOURCE_BOUND,'entire actual failed v1 original78 prefix and original32+Source16 stage retained')
 need(h['schema']=='ACTUAL_CURRENT_B55_NATIVEWARM_B2_COMPLETE_COMPARISON_GUARDED_ROOT_REPORT_V1'and h['status']=='FAILED_CURRENT_B55_NATIVEWARM_B2_COMPLETE_COMPARISON_NO_RETRY'and h['failure']is not None and h['complete_typed_word_comparison_completed']is False and h['actual_child_report_pin']is None and h['actual_child_receipt']is None and type(h['actual_child_integer_exit_code'])is int and h['actual_child_integer_exit_code']==-15 and h['original_runner_error']=='own-child wall cap reached'and h['control_plan_pin']==pp and h['complete_joint_roots']==previous['complete_joint_roots']and h['original_caps']==CAPS,'prior timeout did not complete comparison, produce counts, or establish equality; no retry of original namespace')
 watch=meta(h['actual_watchdog_full_pin']);need(watch==h['actual_watchdog']and type(watch['returncode'])is int and watch['returncode']==-15 and watch['limit_failure']=="RuntimeError('own-child wall cap reached')"and 0<watch['wall_cap_seconds']<=watch['elapsed_seconds']and watch['wall_cap_seconds']<=600 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['rss_cap_mib']==512 and 0<=watch['sampled_peak_rss_mib']<512,'original independent watchdog child-15/wallcap, not an expected evidencechild2')
 need(post['schema']=='RECORDED_CURRENT_B55_NATIVEWARM_B2_COMPLETE_COMPARISON_FAILURE_METADATA_POSTVERIFY_V1'and post['status']=='PASS_RECORDED_ACTUAL_CURRENT_B55_B2_COMPARISON_FAILURE_FACTS_METADATA_ONLY'and post['failure']is None and post['metadata_only']is True and post['actual_Host_report_pin']==ph and post['actual_Root_tools_pin']==packet['actual_failed_v1_Root_tools_pin']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==1 and type(post['actual_child_integer_exit_code'])is int and post['actual_child_integer_exit_code']==-15 and post['actual_watchdog']==watch and post['original_Host_failure']==h['failure']and post['original_Host_status']==h['status']and post['original_records']==h['records']and post['original_runner_error']==h['original_runner_error']and post['complete_typed_word_comparison_completed']is False and post['actual_comparison_counts']is None and post['actual_exact_inventory_metadata_and_all_words_equal']is None and post['control_plan_pin']==pp and post['source_freeze_pin']==h['source_freeze_pin']and post['host_freeze_pin']==h['host_freeze_pin']and post['complete_joint_roots']==previous['complete_joint_roots']and post['original_caps']==CAPS and post['retained_roles_current7_verified_twice']is True and post['no_payload_body_hashed_by_failure_post']is True,'genuine independent failure-facts post0 preserves Root1/child-15 and unknown counts/equality')
 rows=packet['retained_failed_v1_current7_only_pins'];failedroot=Path(previous['planned_actual_output_root']);observed={}
 need(failedroot==Path(previous['complete_joint_roots'][-1])and failedroot!=OUT and failedroot.is_dir()and not failedroot.is_symlink(),'separate retained failed-v1 owning root')
 for q in sorted(failedroot.rglob('*')):
  s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no alias in entire failed-v1 output')
  if stat.S_ISREG(s.st_mode):observed[str(q)]=dict(path=str(q),size_bytes=s.st_size,identity=identity(s))
 need(type(rows)is list and rows and all(type(p)is dict and set(p)=={'path','size_bytes','identity'}for p in rows)and {p['path']:p for p in rows}==observed and len(rows)==len(observed),'all failed-v1 files preserved by exact current7-only rows, no body SHA/fullPF/completion claimed or generic missing skip')
 for p in rows:FAILED_CURRENT7[p['path']]=p;current(p)
 hf=meta(h['host_freeze_pin']);proofs=[packet[k]for k in('actual_failed_v1_plan_pin','actual_failed_v1_Host_report_pin','actual_failed_v1_Root_tools_pin','actual_failed_v1_post_pin','actual_failed_v1_post_tools_pin','actual_failed_v1_final_CLI_pin')]+[h[k]for k in('source_freeze_pin','host_freeze_pin','actual_watchdog_full_pin','actual_log_full_pin','actual_execution_request_pin')]
 need(packet['explicit_cumulative_metadata_file_pins']==unique(previous['explicit_cumulative_metadata_file_pins']+hf['explicit_cumulative_metadata_file_pins']+proofs),'all original metadata roles plus actual failed-v1 metadata proof table, no cold body or partial result in metadata fullPF roles')
 return previous

def declared_whole_v1_inverse(author,table,texts):
    inv=meta(author['whole_inverse_pin']);oldauthor=meta(pin_small(PACKAGE.parent/'current_B55_vs_nativeWarmB2_full_macro_compare_source_v1_UNREADY/AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json'));oldtable={Path(p['path']).name:p for p in oldauthor['whole_Source_file_pins']}
    need(set(table)==set(oldtable)and inv['whole_Source_file_pins']==author['whole_Source_file_pins']and inv['reverse_order_replacements_restore_entire_original_v1_contract']is True and inv['six_other_Source_files_wholebytes_equal']is True,'all7 original roles and actual declared whole-contract inverse/6whole table')
    name='B55_B2_compare_Source_contract.UNREADY.py';need(inv['new_contract_pin']==table[name]and inv['old_contract_pin']==oldtable[name],'whole inverse binds exact old and new contract PFs')
    restored=texts[name]
    for row in reversed(inv['literal_replacements']):
        need(restored.count(row['new'])==1,'each inverse splice has exactly one actual new occurrence');restored=restored.replace(row['new'],row['old'],1)
    need(restored==full(oldtable[name]).read_text(),'entire new contract reverses to the exact original v1 bytes, no hidden edits')
    for name in table:
        if name!='B55_B2_compare_Source_contract.UNREADY.py':need(full(table[name]).read_bytes()==full(oldtable[name]).read_bytes(),'six other Sources wholebytes v1, including original algorithms and all owning callers')
    return inv

def main():
    import builtins,symtable
    ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--ready-pin',required=True);ap.add_argument('--generation-tools-pin',required=True);a=ap.parse_args();need(not os.path.lexists(BASE/'REVIEW.json'),'immutable one formal independent Source review')
    pr=json.loads(a.ready_pin);pg=json.loads(a.generation_tools_pin);ready=meta(pr);generation=meta(pg);genuine(generation,'actual_Source_preparation_return',pr,'ready_pin')
    need(pr['path']==str(PACKAGE/'SOURCE_REVIEW_READY.json')and ready['schema']=='CURRENT_B55_B2_COMPLETE_TYPED_COMPARISON_SOURCE_REVIEW_READY_V1'and ready['source_only']is True and ready['Source_or_decoder_or_native_business_executed']is False and ready['original_caps']==CAPS,'genuine current comparison Source-only GEN0 and exact READY')
    author_pin=pin_small(PACKAGE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');author=meta(author_pin);plan=meta(ready['control_plan_pin']);packet=meta(author['admission_packet_pin']);authorstatic=meta(author['source_static_evidence_pin']);genCLI=meta(pin_small(PACKAGE/'EXACT_ROOT_SOURCE_GENERATION_COMMAND_NOT_EXECUTED.json'))
    need(author['Source_only_frozen_before_Root_generation']is True and author['native_or_compiler_executed_by_author']is False and author['Source_preparer_or_publisher_executed_by_author']is False and author['whole_Source_file_pins']==ready['complete_source_file_pins']and author['original_caps']==CAPS,'entire exact final author Source table before genuine GEN0')
    need(author['helper_or_decoder_or_worker_executed_by_author']is False and author['failed_v1_payload_files_current7_only_not_fullPF']is True and author['original_failed_v1_unchanged']is True and authorstatic['source_only']is True and authorstatic['candidate_or_helper_or_business_executed']is False and authorstatic['packet_pin']==author['admission_packet_pin']and authorstatic['six_noncontract_Source_files_byte_equal_v1']is True and authorstatic['algorithm7445_byte_equal_v1']is True and authorstatic['original_OwnRSS_Budget_and_check_frequency_unchanged']is True and authorstatic['own_bytes_every_call_fresh_scandir_DirEntry_stat_recursive_no_symlinks_no_cache']is True,'final v2 Source-only declaration preserves every original mathematical byte and original guard/check frequency, changes only fresh tree scan and honest failure/scope metadata')
    need(generation['actual_Source_preparation_permission_mode']=='require_escalated'and generation['actual_retried']is False and generation['exact_executed_command']==genCLI['command']and genCLI['admission_packet_pin']==author['admission_packet_pin'],'actual same exact Source-generation command and original same-PID PS permission; no reconstructed run')
    table={Path(p['path']).name:p for p in ready['complete_source_file_pins']};expected={'B55_B2_compare_Source_contract.UNREADY.py','run_guarded_complete_B55_B2_typed_compare.UNREADY.py','run_complete_B55_B2_typed_comparison_child.UNREADY.py','prepare_complete_B55_B2_compare_Source.UNREADY.py','publish_complete_B55_B2_compare_CLI.UNREADY.py','compare_complete_B55_to_nativeWarmB2_typed_original_words.UNREADY.py','saved_native_data_access_adapter.UNREADY.py'}
    need(set(table)==expected and len(table)==len(ready['complete_source_file_pins'])==7 and ready['host_source_pin']==table['run_guarded_complete_B55_B2_typed_compare.UNREADY.py']and ready['contract_Source_pin']==table['B55_B2_compare_Source_contract.UNREADY.py'],'complete exact7 Source roles, no decoder/AAA producer Source substituted')
    texts={};trees={};unbound=[]
    for name,p in table.items():
        q=full(p);s=q.read_text();texts[name]=s;trees[name]=ast.parse(s);top=symtable.symtable(s,str(q),'exec');known=set(top.get_identifiers())|set(dir(builtins))|{'__file__','__name__'}
        def scan(scope):
            for item in scope.get_symbols():
                if item.is_global()and item.is_referenced()and item.get_name()not in known:unbound.append(dict(file=name,scope=scope.get_name(),line=scope.get_lineno(),name=item.get_name()))
            for child in scope.get_children():scan(child)
        scan(top)
    need(unbound==[],'all7 AST and global names checked without candidate/helper import')
    inverse=declared_whole_v1_inverse(author,table,texts)
    contract=texts['B55_B2_compare_Source_contract.UNREADY.py'];host=texts['run_guarded_complete_B55_B2_typed_compare.UNREADY.py'];child=texts['run_complete_B55_B2_typed_comparison_child.UNREADY.py'];gen=texts['prepare_complete_B55_B2_compare_Source.UNREADY.py'];pub=texts['publish_complete_B55_B2_compare_CLI.UNREADY.py'];compare=texts['compare_complete_B55_to_nativeWarmB2_typed_original_words.UNREADY.py']
    need(plan['schema']=='CURRENT_B55_B2_COMPLETE_COMPARISON_SOURCE_ONLY_PLAN_V1'and plan['source_only']is True and plan['actual_business_preconditions_closed']is True and plan['source_role_pin_audit_complete']is True and plan['original_caps']==CAPS and plan['Source_only_stat_budget_fits']is True and plan['Root_original_classes_recheck_required']is True and plan['only_current_stage']=='complete_B55_B2_compare'and plan['bounded_new_output_reservation_bytes']==24*2**20 and plan['bounded_new_Source_metadata_reservation_bytes']==16*2**20 and plan['B2_archive_not_redecoded']is True and plan['Source_generation_science_payload_decoded']is False and plan['Source_generation_worker_or_native_executed']is False,'complete comparison only strict24MiB/Source16 with original caps and actual full prior closures, no new extraction or online qualification')
    need(plan['actual_comparison_executed']is False and plan['actual_raw_word_mismatches']is None and plan['actual_metadata_mismatches']is None,'actual comparison counts remain genuinely unknown at Source stage')
    false=next(n.value for n in trees['B55_B2_compare_Source_contract.UNREADY.py'].body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='FALSE'for x in n.targets));need(isinstance(false,ast.Call)and all(isinstance(k.value,ast.Constant)and k.value.value is False for k in false.keywords),'all new qualification flags remain literal False')
    expectedplan=dict(packet);expectedplan.update(schema='CURRENT_B55_B2_COMPLETE_COMPARISON_SOURCE_ONLY_PLAN_V1',source_only=True,Source_generation_science_payload_decoded=False,Source_generation_worker_or_native_executed=False,Source_only_resource_snapshot=plan['Source_only_resource_snapshot'],**{k.arg:k.value.value for k in false.keywords});need(plan==expectedplan,'whole GEN plan preserves exact author packet with only declared schema/snapshot/Source/false flags')
    oldplan=meta(plan['actual_latest_complete_prefix_plan_pin']);bridge,retire,archive,target,cp,lineage=actual_preconditions(oldplan)
    h=meta(plan['actual_B2_extraction_Host_report_pin']);raw=meta(plan['actual_B2_extraction_Root_tools_pin']);facts=meta(plan['actual_B2_complete_extraction_report_pin']);post=meta(plan['actual_B2_complete_extraction_post_pin']);pt=meta(plan['actual_B2_complete_extraction_post_tools_pin']);genuine(raw,'actual_terminal_return',plan['actual_B2_extraction_Host_report_pin'],'report_pin');genuine(pt,'actual_review_return',plan['actual_B2_complete_extraction_post_pin'],'review_pin')
    need(h['schema']=='ACTUAL_CURRENT_NATIVEWARM_B2_COMPLETE_EXTRACTION_GUARDED_ROOT_REPORT_V1'and h['status']=='ACTUAL_CURRENT_NATIVEWARM_B2_COMPLETE_EXTRACTION_EVIDENCE_CHILD2_CLOSED_ONLY'and h['failure']is None and h['secondary_failures']==[]and h['complete_physical_tree_extraction_completed']is True and h['final_report_resource_check_passed']is True and type(h['actual_child_integer_exit_code'])is int and h['actual_child_integer_exit_code']==2 and h['actual_child_report_pin']==plan['actual_B2_complete_extraction_report_pin']and h['control_plan_pin']==plan['actual_latest_complete_prefix_plan_pin']and len(h['records'])==1 and h['records'][0]['status']=='FAILED'and h['records'][0]['error']==h['original_runner_error']=='own-child stage failed; no retry','actual complete B2 Root0 and intentional child2/FAILED original error retained')
    need(post['schema']=='RECORDED_CURRENT_NATIVEWARM_B2_COMPLETE_PHYSICAL_TREE_EXTRACTION_METADATA_POSTVERIFY_V1'and post['status']=='PASS_ACTUAL_CURRENT_B2_COMPLETE_PHYSICAL_TREE_EXTRACTION_ROOT0_CHILD2_METADATA_ONLY'and post['failure']is None and post['metadata_only']is True and post['actual_Host_report_pin']==plan['actual_B2_extraction_Host_report_pin']and post['actual_Root_tools_pin']==plan['actual_B2_extraction_Root_tools_pin']and post['actual_child_report_pin']==plan['actual_B2_complete_extraction_report_pin']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0 and type(post['actual_child_integer_exit_code'])is int and post['actual_child_integer_exit_code']==2 and post['control_plan_pin']==plan['actual_latest_complete_prefix_plan_pin']and post['complete_joint_roots']==oldplan['complete_joint_roots']and post['original_caps']==CAPS and post['comparison_stage_not_executed']is True and post['new_output_blind_fullEOF_SHA_verified_twice']is True,'genuine independent B2 completed extraction post0 same host/child/fullscope; no comparison already claimed')
    countkeys=('complete_physical_tree_records','complete_directories','complete_extents','complete_MICROLIB2_list1_MACROLIB_records')
    need(facts['schema']=='ACTUAL_COMPLETE_NATIVEWARM_B2_PHYSICAL_TREE_EXTRACTION_V1'and facts['status']=='COMPLETE_NATIVEWARM_B2_PHYSICAL_TREE_READONLY_EVIDENCE_ONLY'and post['actual_full_physical_tree_counts']=={k:facts[k]for k in countkeys}and facts['complete_MICROLIB2_list1_MACROLIB_records']==19620 and facts['entire_original_physical_tree_walked']is True and facts['all_original_types_counts_words_and_physical_API_orders_saved']is True and facts['unrelated_original_containers_retained']is True and post['not_limited_to_constructed19249_fields']is True,'all original physical-tree record metadata and full19620 macro root, not reconstructed fields')
    pair=plan['native_B2_pair'];need(pair==dict(archive_pin=oldplan['actual_current_epoch_B2_archive_pin'],sqlite_pin=facts['paired_SQLite_pin'],native_pool_pin=facts['paired_original_pool_pin'])and plan['actual_current_epoch_B2_archive_pin']==facts['actual_current_epoch_B2_archive_pin']==post['actual_current_epoch_B2_archive_pin']==pair['archive_pin']and post['paired_SQLite_pin']==pair['sqlite_pin']and post['paired_original_pool_pin']==pair['native_pool_pin']and post['complete_physical_directory_slots_pin']==facts['complete_physical_directory_slots_pin'],'same full B2 SQL/pool/physical index, no old AAA/material pair substituted')
    b55=meta(plan['actual_B_complete_context_snapshot_extraction_post_pin']);genuine(meta(plan['actual_B_complete_context_snapshot_extraction_post_tools_pin']),'actual_review_return',plan['actual_B_complete_context_snapshot_extraction_post_pin'],'review_pin')
    need(b55['schema']=='ROOT_ACTUAL_CURRENT_MATERIAL_EXTRACTION_REVIEW_V1'and b55['status']=='PASS_ACTUAL_CURRENT_B_FULL55_CONTEXT8_SNAPSHOT_EXTRACTION_EVIDENCE_CHILD2_METADATA_ONLY'and b55['failure']is None and len(b55['all_snapshot_pairs'])==8 and len(b55['complete_context_pins'])==55 and plan['observed_B55_pair']==b55['all_snapshot_pairs'][-1]and plan['observed_B55_pair']['event']==55 and plan['observed_B55_pair']['role']=='final-complete-micro','true last B55 complete saved pair from all8 snapshots/55 consecutive contexts')
    need(plan['actual_B2_lineage_metadata_audit_pin']==oldplan['actual_B2_lineage_metadata_audit_pin'],'unchanged explicit known/unknown physical-input lineage audit')
    previous=admit_failed_v1(plan,oldplan);failedrows=plan['retained_failed_v1_current7_only_pins']
    priorauthor=meta(pin_small(PACKAGE.parent/'current_B55_vs_nativeWarmB2_full_macro_source_v1_UNREADY/AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json'));oldtable={Path(p['path']).name:p for p in priorauthor['whole_Source_file_pins']}
    for name in('compare_complete_B55_to_nativeWarmB2_typed_original_words.UNREADY.py','saved_native_data_access_adapter.UNREADY.py'):need(full(table[name]).read_bytes()==full(oldtable[name]).read_bytes(),'whole actual B2 author comparator and adapter bytes, no numerical/word scope change')
    need(table['compare_complete_B55_to_nativeWarmB2_typed_original_words.UNREADY.py']['sha256']=='8bf41758be358707c736e52d29fb726f512743bc04777687cced2a9eff77bbd5'and table['saved_native_data_access_adapter.UNREADY.py']['sha256']=='e4dc78c1bd84799c38c0ec05102e0555d243de8ae438c9c08a2296c3601ab742'and plan['frozen_B2_extraction_contract_Source_pin']==oldtable['B2_extract_Source_contract.UNREADY.py'],'exact whole comparator/adapter and prior lifecycle metadata delegate, not decoder')
    full(plan['frozen_B2_extraction_contract_Source_pin']);roots=plan['complete_joint_roots'];need(roots==previous['complete_joint_roots']+[str(OUT)]and len(roots)==79 and roots[:-2]==oldplan['complete_joint_roots']==h['complete_joint_roots']and roots[-1]==plan['planned_actual_output_root']and len(roots)==len(set(roots))and not any(Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and not os.path.lexists(OUT)and any(PACKAGE.is_relative_to(Path(r))for r in roots[:-1]),'full actual failed-v1 inherited78 plus one fresh comparison79, all Source and retained prior output roots counted')
    need(plan['retained_current7_pins']==unique(oldplan['retained_current7_pins']+facts['all_output_file_pins']+failedrows)and plan['retained_B2_current_epoch_readonly_pins']==oldplan['retained_B2_current_epoch_readonly_pins'],'every previous result/native/archive/entry/index and all3 B2 extraction products retained')
    for p in plan['retained_current7_pins']+plan['retained_B2_current_epoch_readonly_pins']:current(p)
    build=meta(plan['original_guard_build_plan_pin'])
    for p in plan['explicit_cumulative_metadata_file_pins']+ready['dependencies']:current_role(p,build)
    for p in plan['child_ordinary_explicit_metadata_pins']:current(p);need(Path(p['path']).lstat().st_uid==os.getuid()and p['identity'][3]==1,'child ordinary metadata only, exact system roles stay outer')
    need(len(unique(plan['explicit_cumulative_metadata_file_pins']))==len(plan['explicit_cumulative_metadata_file_pins'])and len({(p['identity'][0],p['identity'][1])for p in plan['child_ordinary_explicit_metadata_pins']})==len(plan['child_ordinary_explicit_metadata_pins']),'whole cumulative metadata path/node uniqueness')
    union={p['path']:p for p in plan['explicit_cumulative_metadata_file_pins']}
    for p in oldplan['explicit_cumulative_metadata_file_pins']+[plan[k]for k in('actual_latest_complete_prefix_plan_pin','actual_B2_extraction_Host_report_pin','actual_B2_extraction_Root_tools_pin','actual_B2_complete_extraction_report_pin','actual_B2_complete_extraction_post_pin','actual_B2_complete_extraction_post_tools_pin','actual_B_complete_context_snapshot_extraction_post_pin','actual_B_complete_context_snapshot_extraction_post_tools_pin','frozen_B2_extraction_contract_Source_pin')]:need(union.get(p['path'])==p,'all previous full metadata and true runtime/post closures counted without reset or hidden external bytes')
    cold=plan['retained_B2_current_epoch_readonly_pins'];need(not{p['path']for p in cold}&set(union),'nine cold readonly inputs not ordinary external metadata')
    for k in('original_Common_Source_pin','original_support_Source_pin','original_bounded_Source_pin','original_production_inputs_Source_pin','original_budget_worker_Source_pin','original_history_resource_Source_pin','original_production_resource_Source_pin'):need(plan[k]==oldplan[k],'same inherited original guard dependency');full(plan[k])
    budgettext=full(plan['original_budget_worker_Source_pin']).read_text();need(plan['original_budget_worker_Source_pin']['sha256']=='68abfe4702eee0853db8b8340d92ecc46fad2f82c039542ba8ee34eb4c9e0c5b','whole original Bagg metadata-throttled Budget Source, no original mutation')
    admit=next(n for n in trees['B55_B2_compare_Source_contract.UNREADY.py'].body if isinstance(n,ast.FunctionDef)and n.name=='admit');returns=[n for n in ast.walk(admit)if isinstance(n,ast.Return)];need(len(returns)==1 and isinstance(returns[0].value,ast.Tuple)and[n.id for n in returns[0].value.elts]==['build','bm','extractplan','extraction','post'],'five required values actually returned by final admit AST')
    need('build,bm,extractplan,extraction,post=m.admit(packet)'in host and 'build,bm,extractplan,extraction,post=m.admit(packet)'in gen and 'build,bm,extractplan,extraction,post=m.admit(packet,True)'in child and 'old.admit(extractplan,True)'in contract,'all actual owning call sites unpack same five; prior frozen admission is metadata-only lifecycle delegate')
    ops=next(n.value for n in ast.walk(trees['run_complete_B55_B2_typed_comparison_child.UNREADY.py'])if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='ops'for x in n.targets));wired={k.arg for k in ops.keywords};needed={n.slice.value for n in ast.walk(trees['compare_complete_B55_to_nativeWarmB2_typed_original_words.UNREADY.py'])if isinstance(n,ast.Subscript)and isinstance(n.value,ast.Name)and n.value.id=='ops'and isinstance(n.slice,ast.Constant)and isinstance(n.slice.value,str)}
    need(isinstance(ops,ast.Call)and isinstance(ops.func,ast.Name)and ops.func.id=='dict'and wired=={'require','check','pin','current7','identity','module','write','admit_B2_metadata_and_original_owning_guard'}and needed<=wired,'all eight actual owning ops wired and every comparison algorithm use supplied')
    call=next(n for n in ast.walk(trees['run_complete_B55_B2_typed_comparison_child.UNREADY.py'])if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='compare_complete_B55_B2');sig=next(n for n in trees['compare_complete_B55_to_nativeWarmB2_typed_original_words.UNREADY.py'].body if isinstance(n,ast.FunctionDef)and n.name=='compare_complete_B55_B2');need(len(call.args)==len(sig.args.args)and call.keywords==[],'actual comparison AST call/signature agree without guessed argument count')
    need(host.index(".open('x')")<host.index('spec=importlib.util.spec_from_file_location')and child.index(".open('x')")<child.index('spec=importlib.util.spec_from_file_location')and host.index("m.source(packet['original_production_inputs_Source_pin'],'production_inputs')")<host.index('helper,_=support.load'),'Root/child exclusive claim before project helpers/body, production_inputs preloaded before original private guard')
    need('full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)'in host and 'full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)'in child and "record['status']=='FAILED'"in host and "watch['returncode']==2"in host and "original_error=='own-child stage failed; no retry'"in host and 'raise SystemExit(2)'in child and "m.OUT/(record['label']+'.watchdog.json')"in host and "m.OUT/(record['label']+'.log')"in host and "(m.OUT/'compare-stage').mkdir()"in host,'unchanged private OwnRSS/MRO/origins/record.label paths and intentional evidencechild2 retains original FAILED/error')
    need("native_keys == observed_keys"in compare and "len(observed_keys) == 19620"in compare and "count == len(observed_keys) == len(native_keys) == 19620"in compare and "('MACROLIB',)"in compare and "('MICROLIB2', 1, 'MACROLIB')"in compare and 'itertools.zip_longest(saved.iter_raw(a)'in compare and 'for i in range(0, max(len(aa), len(bb)), 4)'in compare and "('kind', 'declared_count', 'original_word_count')"in compare and "a['path_types'] == b['path_types'][2:]"in compare and "raw_word_mismatches=word_mismatches"in compare and "metadata_mismatches=metadata_mismatches"in compare and 'constructed_19249_field_subset_used=False'in compare and 'original_orders_not_sorted_or_rewritten=True'in compare,'full bidirectional typed root inventories, exact path/kind/count/all words, physical/API ordinal preservation and both actual mismatch counts; no reduced constructed subset')
    need("v['raw_word_mismatches']>=0"in host and "v['metadata_mismatches']>=0"in host and "v['raw_word_mismatches']==0"not in host and "v['metadata_mismatches']==0"not in host and "m.current(v['detail_pin'])"in host and "all_output_file_pins"not in host,'completion honestly records both nonnegative actual mismatch counts and real detail_pin; never forces equality or invents absent report field')
    need("command=['/bin/ps','-o','rss=','-p',str(os.getpid())]"in contract and 'int(sample.stdout.strip())*1024<512*2**20'in contract and "actual_PS_return=dict(argv=command"in contract and "receipt['actual_parent_PID']==os.getpid()"in host and "receipt['resources_after']['current_parent_PID']==os.getpid()"in host and "actual_parent_PID=os.getppid()"in child,'same-PID PS hard RSS512 and actual direct owning parent chain retained')
    need('self.original.check();resources.light()'in child and 'self.original.last=time.monotonic()'in child and 'now-self.start<600 and peak<512*2**20'in budgettext and 'self.last=time.monotonic()'in budgettext,'whole original per-call SELF/time600 before successful completed-metadata-scan throttling, no threshold change')
    bounds={}
    for n in trees['B55_B2_compare_Source_contract.UNREADY.py'].body:
        if isinstance(n,ast.Assign):
            for x in n.targets:
                if isinstance(x,ast.Name)and x.id in('OUTPUT_BOUND','SOURCE_BOUND'):bounds[x.id]=integer_expression(n.value)
    need(bounds==dict(OUTPUT_BOUND=24*2**20,SOURCE_BOUND=16*2**20)and 'self.history.check();j=self.joined.check()'in contract and "for p in self.packet['retained_B2_current_epoch_readonly_pins']"in contract and "is_relative_to(Path(r))for r in h['resource_roots']"in contract and 'sum(unlinked.values())'in contract and 'existing+OUTPUT_BOUND+SOURCE_BOUND<2*2**30'in contract,'same complete original history/fresh/metadata/cold/openunlinked classes, all outputs strict24+Source16 before admission')
    need("for n in('review-pin','review-tools-pin','generation-tools-pin')"in pub and "review['status']=='PASS_SOURCE_ONLY_CURRENT_B55_B2_COMPLETE_TYPED_COMPARISON'"in pub and "m.need(len(argv)==24"in pub and "Root_actual_exec_command_sandbox_permissions_required='require_escalated'"in pub and "m.genuine(m.metadata(pg),'actual_Source_preparation_return'"in pub,'exact publisher3 PFs/genuine Source GEN0+independentSource0/full7 table and original24 argv permission')
    scanner=functions(contract)['own_bytes'];need("root=os.fspath(root)"in scanner and "os.lstat(root)"in scanner and "with os.scandir(directory)as entries"in scanner and "entry.stat(follow_symlinks=False)"in scanner and "not stat.S_ISLNK(s.st_mode)"in scanner and "total+=scan(entry.path)"in scanner and "total+=s.st_size"in scanner and "return scan(root)"in scanner and 'rglob'not in scanner and 'cache'not in scanner and 'time.'not in scanner and 'self.'not in scanner,'every call uses a new recursive whole-directory scan with no-follow fresh entry stats, no symlink/cache/skipped regular files/timing throttle; original light caller bytes kept by whole inverse')
    need(plan['prior_failed_v1_is_success']is False and plan['own_bytes_fresh_scandir_without_cache_or_frequency_change']is True,'old failed comparison never treated as prior success; only directory traversal implementation optimized')
    for k in('actual_lineage_qualified','physics_qualified','AAA_qualified','ABA_admitted','goal_complete','online_BOOT_qualified'):need(plan[k]is False,'Source completion cannot grant word equality/lineage/online/science qualifications')
    joint=whole_current_bytes(roots);external=sum(p['size_bytes']for p in plan['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));opened=own_open_unlinked_bytes();need(joint+external+opened+40*2**20<2*2**30,'actual full79 scope+all external/openunlinked+complete comparison24+Source16 fits original cumulative2GiB')
    before=plan['Source_only_resource_snapshot'];h=before['original_history'];j=before['complete_joint'];sample=before['actual_PS_return'];need(j['resource_roots']==roots and all(any(Path(p['path']).is_relative_to(Path(r))for r in h['resource_roots'])for p in cold)and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30 and before['host_SELF_peak_bytes']<512*2**20 and sample['argv']==['/bin/ps','-o','rss=','-p',str(before['current_PID'])]and type(sample['returncode'])is int and sample['returncode']==0 and sample['stderr']==''and sample['stdout'].strip().isdigit()and int(sample['stdout'].strip())*1024<512*2**20,'saved genuine GEN original caps/history96/cold/meta/free8/same-PID PS and9readonlyhistory coverage; no process/sample rerun')
    for p in list(FULL.values()):full(p)
    for p in list(CURRENT.values()):current(p)
    report=dict(schema='INDEPENDENT_CURRENT_B55_NATIVEWARM_B2_COMPLETE_TYPED_COMPARISON_V2_FROZEN_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_B55_B2_COMPLETE_TYPED_COMPARISON',failure=None,source_only=True,metadata_only=True,control_plan_pin=ready['control_plan_pin'],complete_source_file_pins=ready['complete_source_file_pins'],Root_Source_generation_tools_pin=pg,Root_Source_generation_READY_pin=pr,author_Source_freeze_pin=author_pin,whole_Source_metadata_twice_pins=list(FULL.values()),nondecoding_current7_only_pins=[p for k,p in CURRENT.items()if k not in FULL],complete_joint_roots=roots,original_caps=CAPS,all7_frozen_Source_AST_and_global_names_checked=True,six_other_Source_whole_v1_and_entire_contract_inverse_checked=True,declared_whole_contract_inverse_pin=author['whole_inverse_pin'],actual_failed_v1_Root_tools_pin=plan['actual_failed_v1_Root_tools_pin'],actual_failed_v1_failure_post_pin=plan['actual_failed_v1_post_pin'],retained_failed_v1_current7_only_pins=failedrows,failed_v1_body_SHA_not_invented=True,actual_failed_v1_counts_and_equality_remain_None=True,whole_scope_fresh_scandir_stat_nofollow_no_cache_no_frequency_change=True,unbound_global_candidates=unbound,whole_original_comparator_and_adapter_bytes_preserved=True,all8_owning_ops_wired=True,actual_compare_AST_call_count=len(call.args),actual_compare_AST_signature_count=len(sig.args.args),full19620_bidirectional_original_typed_paths_and_all_words_required=True,original_kind_count_and_path_types_required=True,original_physical_and_API_ordinals_retained=True,word_and_metadata_mismatch_counts_recorded_as_actual=True,Source_completion_not_word_equality=True,future_online_admission_requires_both_mismatch_counts_zero=True,actual_comparison_counts=None,actual_word_mismatches=None,actual_metadata_mismatches=None,actual_B2_extraction_Host_report_pin=plan['actual_B2_extraction_Host_report_pin'],actual_B2_extraction_post_pin=plan['actual_B2_complete_extraction_post_pin'],actual_B55_saved_pair=plan['observed_B55_pair'],actual_B2_saved_pair=pair,actual_B2_full_physical_tree_counts=post['actual_full_physical_tree_counts'],genuine_prior_B2_Root0_child2_FAILED_preserved=True,original_private_guard_and_same_PID_PS_and_parent_chain_required=True,nine_readonly_cold_roles_current7_only_pins=cold,exact_historical_presence_retirement_full_pin=target[0],generic_missing_path_skip_authorized=False,Source_reviewer_task='/root/b_capture_actual_post_source',core_algorithm_or_owning_Source_authored_by_this_reviewer=False,current_joint_bytes=joint,current_external_metadata_bytes=external,current_review_open_unlinked_bytes=opened,entire_new_comparison_reservation_bytes=24*2**20,Source_metadata_reservation_bytes=16*2**20,candidate_or_helper_imported=False,Source_GEN_or_publication_executed=False,worker_or_comparison_or_native_executed=False,SQL_pool_native_JSONL_or_gzip_values_decoded=False,actual_lineage_qualified=False,online_BOOT_qualified=False,reviewer_Source_pin=pin_small(Path(__file__).absolute()),elapsed_seconds=time.monotonic()-START,**FALSE)
    data=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(data)<6*2**20 and whole_current_bytes([str(PACKAGE)])+len(data)<16*2**20,'review report6 and whole Source16 metadata bound')
    with(BASE/'REVIEW.json').open('xb')as f:f.write(data);f.flush();os.fsync(f.fileno())
    budget();print(json.dumps(dict(status=report['status'],review_pin=pin_small(BASE/'REVIEW.json'))),flush=True)
if __name__=='__main__':main()
