"""Independent complete nativeWarmB2 physical extraction Source/metadata review. No candidate/helper imports."""
import argparse, ast, hashlib, json, os, resource, stat, sys, time
from pathlib import Path

BASE=Path(__file__).absolute().parent
PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
OUT=ROOT/'validation/artifacts/axial-material-current-nativeWarmB2-complete-physical-tree-extract-20261015-v1'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(B_native_executed=False,B_observation_context_produced=False,compiled_IO_semantics_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
START=time.monotonic()
FULL={}
CURRENT={}

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

def main():
    import builtins,symtable
    ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--ready-pin',required=True);ap.add_argument('--generation-tools-pin',required=True);a=ap.parse_args()
    need(not os.path.lexists(BASE/'REVIEW.json'),'immutable once-only formal Source review')
    pr=json.loads(a.ready_pin);pg=json.loads(a.generation_tools_pin);ready=meta(pr);generation=meta(pg);genuine(generation,'actual_Source_preparation_return',pr,'ready_pin')
    need(pr['path']==str(PACKAGE/'SOURCE_REVIEW_READY.json')and ready['schema']=='CURRENT_B2_COMPLETE_PHYSICAL_EXTRACTION_SOURCE_REVIEW_READY_V1'and ready['source_only']is True and ready['Source_or_decoder_or_native_business_executed']is False and ready['original_caps']==CAPS,'true only Source GEN0 and complete extraction READY')
    author_pin=pin_small(PACKAGE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');author=meta(author_pin);plan=meta(ready['control_plan_pin'])
    need(author['Source_only_frozen_before_Root_generation']is True and author['native_or_compiler_executed_by_author']is False and author['Source_preparer_or_publisher_executed_by_author']is False and author['whole_Source_file_pins']==ready['complete_source_file_pins'],'exact final whole author Source table; no selectively omitted source')
    packet=meta(author['admission_packet_pin']);author_static=meta(author['static_evidence_pin']);generationCLI=meta(author['exact_Root_Source_generation_command_pin']);need(author['author_STOP_CORE_WRITES']is True and author['original5_algorithm_adapter_walker_reference_wholebytes_unchanged']is True and author['worker_helpers_PS_lsof_or_data_payload_read_by_author']is False and author['original_caps']==CAPS and author_static['packet_pin']==author['admission_packet_pin']and author_static['original5_wholebytes_unchanged']is True and author_static['all8_ops_connected']is True and author_static['Source_author_no_GEN_pub_candidate_import_PS_lsof_NATIVE_decoder_or_data_body_reads']is True,'true final author-only freeze and whole original scientific Sources preserved')
    need(generation['actual_Source_preparation_permission_mode']=='require_escalated'and generation['actual_retried']is False and generation['exact_executed_command']==generationCLI['command']and generationCLI['admission_packet_pin']==author['admission_packet_pin'],'true GEN same saved exact author command and Root-only same-PID PS permission; not a reconstructed run')
    table={Path(p['path']).name:p for p in ready['complete_source_file_pins']};expected={'B2_extract_Source_contract.UNREADY.py','run_guarded_complete_nativeWarmB2_extract.UNREADY.py','run_complete_B2_physical_extraction_child.UNREADY.py','prepare_complete_nativeWarmB2_extract_Source.UNREADY.py','publish_complete_nativeWarmB2_extract_CLI.UNREADY.py','extract_complete_nativeWarmB2_physical_tree.UNREADY.py','compare_complete_B55_to_nativeWarmB2_typed_original_words.UNREADY.py','saved_native_data_access_adapter.UNREADY.py','complete_observed_old_post_final_XSM_extractor.UNREADY.py','REFERENCE_COMPLETE_AAA_THREE_TYPED_COMPARATOR_NOT_FOR_B2.py'}
    need(set(table)==expected and len(table)==len(ready['complete_source_file_pins'])==10 and ready['host_source_pin']==table['run_guarded_complete_nativeWarmB2_extract.UNREADY.py']and ready['contract_Source_pin']==table['B2_extract_Source_contract.UNREADY.py'],'whole exact10 Sources including algorithm/comparator/whole original walker-adapter-reference and owning five')
    texts={};trees={};unbound=[]
    for name,p in table.items():
        q=full(p);text=q.read_text();texts[name]=text;trees[name]=ast.parse(text);top=symtable.symtable(text,str(q),'exec');known=set(top.get_identifiers())|set(dir(builtins))|{'__file__','__name__'}
        def scan(scope):
            for symbol in scope.get_symbols():
                if symbol.is_global()and symbol.is_referenced()and symbol.get_name()not in known:unbound.append(dict(file=name,scope=scope.get_name(),line=scope.get_lineno(),name=symbol.get_name()))
            for child in scope.get_children():scan(child)
        scan(top)
    need(unbound==[],'all frozen Source AST/global names resolve without importing or executing candidate')
    copies=meta(pin_small(PACKAGE/'WHOLE_ORIGINAL_ADAPTER_WALKER_AND_COMPARATOR_REFERENCE_COPY_INVENTORY.json'));copyproof=[]
    for pair in copies['copy_pairs']:
        old=pair['original_Source_pin'];new=pair['whole_copy_Source_pin'];need(new==table[Path(new['path']).name]and full(old).read_bytes()==full(new).read_bytes(),'whole original adapter/walker/AAA reference Source bytes unchanged');copyproof.append(pair)
    need(table['extract_complete_nativeWarmB2_physical_tree.UNREADY.py']['sha256']=='570c92fb449e2a083c7ad674da00813a5451b0df647cdd7a6b599fba1dd4ec19'and table['compare_complete_B55_to_nativeWarmB2_typed_original_words.UNREADY.py']['sha256']=='8bf41758be358707c736e52d29fb726f512743bc04777687cced2a9eff77bbd5','both complete algorithms remain exactly frozen b2 Source bytes; this reviewer authored neither')
    need(plan['schema']=='CURRENT_B2_COMPLETE_EXTRACTION_SOURCE_ONLY_PLAN_V1'and plan['source_only']is True and plan['actual_business_preconditions_closed']is True and plan['source_role_pin_audit_complete']is True and plan['original_caps']==CAPS and plan['only_current_stage']=='complete_B2_extract'and plan['comparison_stage_not_in_this_execution']is True and plan['bounded_new_output_reservation_bytes']==256*2**20 and plan['bounded_new_Source_metadata_reservation_bytes']==16*2**20 and plan['Source_generation_science_payload_decoded']is False and plan['Source_generation_worker_or_native_executed']is False,'actual complete256MiB extraction only plus Source16, exact original caps and no future comparison admission')
    false_node=next(n.value for n in trees['B2_extract_Source_contract.UNREADY.py'].body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='FALSE'for x in n.targets));need(isinstance(false_node,ast.Call)and all(isinstance(k.value,ast.Constant)and k.value.value is False for k in false_node.keywords),'all frozen contract qualification flags are literal False');expected_plan=dict(packet);expected_plan.update(schema='CURRENT_B2_COMPLETE_EXTRACTION_SOURCE_ONLY_PLAN_V1',source_only=True,Source_generation_science_payload_decoded=False,Source_generation_worker_or_native_executed=False,Source_only_resource_snapshot=plan['Source_only_resource_snapshot'],**{k.arg:k.value.value for k in false_node.keywords});need(plan==expected_plan,'whole GEN plan is frozen actual packet plus only declared Source-only snapshot/schema/false flags, no consumer lifecycle or scope rebinding')
    bridge,retire,archive,target,cp,lineage=actual_preconditions(plan);roots=plan['complete_joint_roots']
    need(roots[:-1]==retire['complete_joint_roots']==archive['complete_joint_roots']and roots==bridge['complete_joint_roots']+[archive['planned_actual_output_root'],str(OUT)]and len(roots)==77 and len(roots)==len(set(roots))and not any(Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and not os.path.lexists(OUT)and plan['planned_actual_output_root']==str(OUT)and any(PACKAGE.is_relative_to(Path(x))for x in roots[:-1]),'entire original75, true presence76, new literal extraction77; all Source in counted FTOP, no silently excluded roots')
    build=meta(plan['original_guard_build_plan_pin']);full(plan['original_guard_build_contract_Source_pin'])
    for p in plan['explicit_cumulative_metadata_file_pins']:current_role(p,build)
    for p in ready['dependencies']:current_role(p,build)
    for p in plan['child_ordinary_explicit_metadata_pins']:
        current(p);need(Path(p['path']).lstat().st_uid==os.getuid()and p['identity'][3]==1,'child ordinary explicit metadata only; selected system roles stay outer exact table')
    need(len(unique(plan['explicit_cumulative_metadata_file_pins']))==len(plan['explicit_cumulative_metadata_file_pins'])and len({(p['identity'][0],p['identity'][1])for p in plan['child_ordinary_explicit_metadata_pins']})==len(plan['child_ordinary_explicit_metadata_pins']),'complete metadata de-duplicated by literal path and child ordinary nodes')
    union={p['path']:p for p in plan['explicit_cumulative_metadata_file_pins']}
    for p in bridge['explicit_cumulative_metadata_file_pins']+retire['explicit_cumulative_metadata_file_pins']+[plan[k]for k in('actual_B2_current_epoch_bridge_report_pin','actual_B2_current_epoch_bridge_Root_tools_pin','actual_B2_current_epoch_bridge_post_pin','actual_B2_current_epoch_bridge_post_tools_pin','actual_presence_retirement_receipt_pin','actual_presence_retirement_Root_tools_pin','actual_presence_retirement_post_pin','actual_presence_retirement_post_tools_pin','actual_B2_lineage_metadata_audit_pin')]:need(union.get(p['path'])==p,'entire cumulative bridge/retirement metadata and actual role closures counted, no prior8MiB metadata reset')
    cold=plan['retained_B2_current_epoch_readonly_pins'];need(not{p['path']for p in cold}&set(union),'nine large readonly bodies stay original history/cold inputs, never smuggled as ordinary external metadata')
    for k in('original_Common_Source_pin','original_support_Source_pin','original_bounded_Source_pin','original_production_inputs_Source_pin','original_budget_worker_Source_pin','original_history_resource_Source_pin','original_production_resource_Source_pin'):full(plan[k])
    budgettext=full(plan['original_budget_worker_Source_pin']).read_text();need(plan['original_budget_worker_Source_pin']['sha256']=='68abfe4702eee0853db8b8340d92ecc46fad2f82c039542ba8ee34eb4c9e0c5b','whole original completed-scan Budget Source, no changed original guard file')
    contract=texts['B2_extract_Source_contract.UNREADY.py'];host=texts['run_guarded_complete_nativeWarmB2_extract.UNREADY.py'];child=texts['run_complete_B2_physical_extraction_child.UNREADY.py'];extract=texts['extract_complete_nativeWarmB2_physical_tree.UNREADY.py'];gen=texts['prepare_complete_nativeWarmB2_extract_Source.UNREADY.py'];pub=texts['publish_complete_nativeWarmB2_extract_CLI.UNREADY.py'];compare=texts['compare_complete_B55_to_nativeWarmB2_typed_original_words.UNREADY.py']
    admit=next(n for n in trees['B2_extract_Source_contract.UNREADY.py'].body if isinstance(n,ast.FunctionDef)and n.name=='admit');returns=[n for n in ast.walk(admit)if isinstance(n,ast.Return)];need(len(returns)==1 and isinstance(returns[0].value,ast.Tuple)and[n.id for n in returns[0].value.elts]==['build','bm','archive','retirement','bridge'],'actual AST five return values agree with all callers')
    need('build,bm,archive,retirement,bridge=m.admit(packet)'in host and 'build,bm,archive,retirement,bridge=m.admit(packet)'in gen and 'build,bm,archive,retirement,bridge=m.admit(packet,True)'in child,'all owning caller sites unpack same five required outputs')
    required=next(n.value for n in trees['extract_complete_nativeWarmB2_physical_tree.UNREADY.py'].body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='REQUIRED_OPS'for x in n.targets));required_ops=ast.literal_eval(required);ops=next(n.value for n in ast.walk(trees['run_complete_B2_physical_extraction_child.UNREADY.py'])if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='ops'for x in n.targets));need(isinstance(ops,ast.Call)and isinstance(ops.func,ast.Name)and ops.func.id=='dict'and{k.arg for k in ops.keywords}==set(required_ops),'all actual algorithm ops wired exactly once from final owning child')
    call=next(n for n in ast.walk(trees['run_complete_B2_physical_extraction_child.UNREADY.py'])if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='extract_complete_B2');sig=next(n for n in trees['extract_complete_nativeWarmB2_physical_tree.UNREADY.py'].body if isinstance(n,ast.FunctionDef)and n.name=='extract_complete_B2');need(len(call.args)==len(sig.args.args)and call.keywords==[],'actual complete extract call/signature agree, no guessed arity')
    need(host.index(".open('x')")<host.index("spec=importlib.util.spec_from_file_location")and child.index(".open('x')")<child.index("spec=importlib.util.spec_from_file_location")and host.index("m.source(packet['original_production_inputs_Source_pin'],'production_inputs')")<host.index('helper,_=support.load'),'exclusive Root/child claims before project import, original production input preload before private guard')
    need('full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)'in host and 'full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)'in child and "record['status']=='FAILED'"in host and "watch['returncode']==2"in host and "original_error=='own-child stage failed; no retry'"in host and 'raise SystemExit(2)'in child and "m.OUT/(record['label']+'.watchdog.json')"in host and "m.OUT/(record['label']+'.log')"in host,'unchanged private OwnRSS MRO/origins, exact stage label paths and intentional child2/FAILED original error retained')
    need("(m.OUT/'extract-stage').mkdir()"in host and "(m.OUT/'evidence').mkdir()"in host and 'tree.walk()'in extract and 'rows.close()'in extract and 'finally:'in extract and 'ReadOnlyFileBytes(stream)'in extract and 'ops[\'check\'](expected, budget.check)'in extract and "complete_macro_count == 19620"in extract and "for row in rows.iter_rows():"in extract and "all_output_file_pins=artifacts"in extract,'whole physical tree and complete payload SQL/physical index, close final DB, before/after full EOF input SHA, actual19620 macro records, no scope cut')
    need('constructed_19249_field_subset_used=False'in compare and 'itertools.zip_longest(saved.iter_raw(a)'in compare and 'count == len(observed_keys) == len(native_keys) == 19620'in compare and 'compare_complete_B55_B2('not in host and 'compare_complete_B55_B2('not in child,'full macro comparator Source remains separate future stage, never current construction subset or combined qualification')
    bounds={}
    for n in trees['B2_extract_Source_contract.UNREADY.py'].body:
        if isinstance(n,ast.Assign):
            for x in n.targets:
                if isinstance(x,ast.Name)and x.id in('OUTPUT_BOUND','SOURCE_BOUND'):bounds[x.id]=integer_expression(n.value)
    need(bounds==dict(OUTPUT_BOUND=256*2**20,SOURCE_BOUND=16*2**20)and "self.original.last=time.monotonic()"in child and 'self.original.check();resources.light()'in child and "now-self.start<600 and peak<512*2**20"in budgettext and "self.last=time.monotonic()"in budgettext,'same original per-call SELF512/time600 and completed-metadata-scan throttling; entire output256 plus Source16')
    need("for n in('review-pin','review-tools-pin','generation-tools-pin')"in pub and "review['status']=='PASS_SOURCE_ONLY_CURRENT_B2_COMPLETE_PHYSICAL_EXTRACTION'"in pub and "m.need(len(argv)==24"in pub and "Root_actual_exec_command_sandbox_permissions_required='require_escalated'"in pub and "m.genuine(m.metadata(pg),'actual_Source_preparation_return'"in pub,'publisher exact three PFs/whole Source report interface/genuine GEN0/Root original24argv and permission')
    need("command=['/bin/ps','-o','rss=','-p',str(os.getpid())]"in contract and "sample.returncode==0"in contract and "int(sample.stdout.strip())*1024<512*2**20"in contract and "actual_PS_return=dict(argv=command"in contract and "current_parent_PID=os.getppid()"in contract and "receipt['actual_parent_PID']==os.getpid()"in host and "receipt['resources_after']['current_parent_PID']==os.getpid()"in host and "actual_parent_PID=os.getppid()"in child,'original same-PID PS hard512 and direct actual parent chain retained without imposing unrelated whole-system ancestry requirements')
    need('self.history.check();j=self.joined.check()'in contract and "for p in self.packet['retained_B2_current_epoch_readonly_pins']"in contract and "is_relative_to(Path(r))for r in h['resource_roots']"in contract and 'sum(unlinked.values())'in contract and 'existing+OUTPUT_BOUND+SOURCE_BOUND<2*2**30'in contract,'original dynamic history/fresh classes plus all metadata/cold coverage/open-unlinked counted with full256+16 reservation')
    for k in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(plan[k]is False,'Source preparation never mints physical or goal qualification')
    joint=whole_current_bytes(roots);external=sum(p['size_bytes']for p in plan['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));opened=own_open_unlinked_bytes();need(joint+external+opened+256*2**20+16*2**20<2*2**30,'entire actual prefix+all current external/open-unlinked+complete extraction256+Source16 fits original cumulative2GiB')
    before=plan['Source_only_resource_snapshot'];h=before['original_history'];j=before['complete_joint'];need(j['resource_roots']==roots and all(any(Path(p['path']).is_relative_to(Path(r))for r in h['resource_roots'])for p in cold)and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30 and before['host_SELF_peak_bytes']<512*2**20,'saved genuine GEN original history96/cold/meta/free8 and selected readonlyroles covered in history, no cold-body count reset')
    sample=before['actual_PS_return'];need(sample['argv']==['/bin/ps','-o','rss=','-p',str(before['current_PID'])]and type(sample['returncode'])is int and sample['returncode']==0 and sample['stderr']==''and sample['stdout'].strip().isdigit()and int(sample['stdout'].strip())*1024<512*2**20,'saved genuine Source-generation same-PID PS RSS original hard guard, not rerun by reviewer')
    for p in list(FULL.values()):full(p)
    for p in list(CURRENT.values()):current(p)
    report=dict(schema='INDEPENDENT_CURRENT_NATIVEWARM_B2_COMPLETE_PHYSICAL_EXTRACTION_FROZEN_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_B2_COMPLETE_PHYSICAL_EXTRACTION',failure=None,source_only=True,metadata_only=True,control_plan_pin=ready['control_plan_pin'],complete_source_file_pins=ready['complete_source_file_pins'],Root_Source_generation_tools_pin=pg,Root_Source_generation_READY_pin=pr,author_Source_freeze_pin=author_pin,whole_Source_metadata_twice_pins=list(FULL.values()),nondecoding_current7_only_pins=[p for k,p in CURRENT.items()if k not in FULL],complete_joint_roots=roots,original_caps=CAPS,all10_frozen_Source_AST_and_global_names_checked=True,unbound_global_candidates=unbound,whole_original_copy_pairs=copyproof,both_algorithm_Source_bytes_preserved=True,all8_algorithm_ops_wired=True,actual_extract_AST_call_count=len(call.args),actual_extract_AST_signature_count=len(sig.args.args),actual_bridge_root0_post0_preserved=True,exact_presence_retirement_Root0_post0_preserved=True,exact_only_retired_presence_full_pin=target[0],future_consumer_must_use_exact_single_presence_archive_mapping=True,generic_missing_path_skip_authorized=False,all_other_current_results_and_native_inputs_retained=True,original_Bagg_child2_FAILED_error_retained_via_actual_presence_closure=True,original_private_guard_class_and_MRO_unchanged=True,original_completed_scan_Budget_whole_Source_pin=plan['original_budget_worker_Source_pin'],nine_readonly_cold_roles_current7_only_pins=cold,cold_role_bodies_or_SQLpool_or_gzip_or_native_XSM_decoded=False,all_complete_physical_tree_output_scope_not_filtered=True,Source_reviewer_task='/root/b_capture_actual_post_source',core_or_algorithm_or_owning_Source_authored_by_this_reviewer=False,actual_independent_POST_Source_authored_by_this_reviewer=True,current_joint_bytes=joint,current_external_metadata_bytes=external,current_review_open_unlinked_bytes=opened,entire_new_extraction_reservation_bytes=256*2**20,Source_metadata_reservation_bytes=16*2**20,helper_or_candidate_imported=False,Source_GEN_or_publication_executed=False,worker_or_comparison_or_native_executed=False,reviewer_Source_pin=pin_small(Path(__file__).absolute()),elapsed_seconds=time.monotonic()-START,**FALSE)
    raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20 and whole_current_bytes([str(PACKAGE)])+len(raw)<16*2**20,'Source review report6MiB and entire packageSource16MiB')
    with(BASE/'REVIEW.json').open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    budget();print(json.dumps(dict(status=report['status'],review_pin=pin_small(BASE/'REVIEW.json'))),flush=True)
if __name__=='__main__':main()
