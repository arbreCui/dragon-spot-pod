"""Independent B4 archive Source/metadata review. No gzip or product-byte IO."""
import argparse, ast, hashlib, json, os, resource, stat, sys, time
from pathlib import Path

BASE=Path(__file__).absolute().parent
PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
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

def main():
    import builtins,symtable
    ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--ready-pin',required=True);ap.add_argument('--generation-tools-pin',required=True);a=ap.parse_args()
    need(not (BASE/'REVIEW.json').exists(),'single immutable independent Source review')
    pr=json.loads(a.ready_pin);pg=json.loads(a.generation_tools_pin);ready=meta(pr);gen=meta(pg)
    genuine(gen,'actual_Source_preparation_return',pr,'ready_pin');need(pr['path']==str(PACKAGE/'SOURCE_REVIEW_READY.json'),'literal current READY role')
    need(ready['schema']=='CURRENT_B4_COMPLETE_PRODUCT_ARCHIVE_SOURCE_REVIEW_READY_V1'and ready['source_only']is True and ready['product_payload_opened']is False and ready['gzip_executed']is False and ready['original_caps']==CAPS,'actual byte-archive Source-only READY')
    pb=ready['execution_binding_pin'];b=meta(pb);authorpin=pin_small(PACKAGE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');author=meta(authorpin)
    need(author['Source_only_frozen_before_Root_generation']is True and author['Source_preparer_or_publisher_executed_by_author']is False and author['product_byte_IO_gzip_or_compiler_executed_by_author']is False and author['whole_Source_file_pins']==ready['complete_source_file_pins'],'entire author-frozen Source table exact; no partial selection')
    meta(ready['author_admission_binding_pin'])
    if 'Source_static_evidence_pin'in author:meta(author['Source_static_evidence_pin'])
    texts={};trees={};unbound=[]
    for p in ready['complete_source_file_pins']:
        q=full(p);need(q.suffix=='.py','all byte-archive execution Sources Python');text=q.read_text();texts[q.name]=text;trees[q.name]=ast.parse(text);top=symtable.symtable(text,str(q),'exec');known=set(top.get_identifiers())|set(dir(builtins))|{'__file__','__name__'}
        def scan(scope):
            for s in scope.get_symbols():
                if s.is_global()and s.is_referenced()and s.get_name()not in known:unbound.append(dict(file=q.name,scope=scope.get_name(),line=scope.get_lineno(),name=s.get_name()))
            for child in scope.get_children():scan(child)
        scan(top)
    need(unbound==[],'all frozen Python AST/global names have no unbound candidates')
    for p in(ready['host_source_pin'],ready['common_source_pin'],ready['worker_source_pin'],ready['writer_source_pin']):need(p in ready['complete_source_file_pins'],'every actual entry is in complete frozen Source table')
    need(b['schema']=='CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ARCHIVE_BINDING_V1'and b['prerequisite_binding_complete']is True and b['draft_unready']is False and b['Source_admission_ready']is False and b['original_caps']==CAPS,'actual current four-product binding schema')
    need(b['Source_generation_product_payload_opened']is False and b['Source_generation_gzip_executed']is False,'Root GEN did not open products or run gzip')
    capture=meta(b['actual_B_capture_Host_report_pin']);cp=meta(b['actual_B_capture_post_pin']);cr=meta(b['actual_B_capture_Root_tools_pin']);ct=meta(b['actual_B_capture_post_tools_pin']);manifest=meta(b['actual_B_manifest_pin']);inputbinding=meta(b['actual_B_input_binding_pin'])
    genuine(cr,'actual_terminal_return',b['actual_B_capture_Host_report_pin'],'report_pin');genuine(ct,'actual_review_return',b['actual_B_capture_post_pin'],'review_pin')
    need(capture['schema']=='ACTUAL_CURRENT_B_COMPLETE_NATIVE_CAPTURE_ROOT_REPORT_V1'and capture['status']=='ACTUAL_CURRENT_B_FULL55_CONTEXT_8TREE_4PRODUCT_CAPTURE_CLOSED0_ONLY'and capture['failure']is None and capture['final_report_resource_check_passed']is True and capture['original_caps']==CAPS,'same real complete B capture Root0')
    need(cp['schema']=='RECORDED_CURRENT_B_COMPLETE_CAPTURE_METADATA_POSTVERIFY_V1'and cp['status']=='PASS_ACTUAL_CURRENT_B_FULL4PRODUCT_55CONTEXT_8TREE_CAPTURE_CHILD0_METADATA_ONLY'and cp['failure']is None and cp['actual_Host_report_pin']==b['actual_B_capture_Host_report_pin']and cp['actual_Root_tools_pin']==b['actual_B_capture_Root_tools_pin'],'same real independent capture metadata post0')
    state=capture['actual_B_state'];products=state['actual_material_product_pins'];need(b['all4_product_pins']==products and len(products)==len({p['path']for p in products})==4 and {Path(p['path']).name for p in products}=={'m.xsm','u.asc','a.asc','t.asc'}and all(Path(p['path']).parent==Path(inputbinding['actual_output_root'])for p in products),'all four exact captured products in producer order; no format assumption or omitted m.xsm')
    need(b['original4_product_total_bytes']==sum(p['size_bytes']for p in products),'original byte total derived from exact four complete PFs')
    need(manifest['state_order']==['B']and manifest['states']['B']['actual_owning_report_pin']==b['actual_B_capture_Host_report_pin']and manifest['current_B_case_input_binding_pin']==b['actual_B_input_binding_pin'],'same original B capture/manifest/input lineage')
    eh=meta(b['actual_B_extraction_Host_report_pin']);ep=meta(b['actual_B_extraction_post_pin']);er=meta(b['actual_B_extraction_Root_tools_pin']);et=meta(b['actual_B_extraction_post_tools_pin']);ex=meta(b['actual_B_extraction_child_report_pin'])
    genuine(er,'actual_terminal_return',b['actual_B_extraction_Host_report_pin'],'report_pin');genuine(et,'actual_review_return',b['actual_B_extraction_post_pin'],'review_pin')
    need(eh['status']=='ACTUAL_CURRENT_B_COMPLETE_EXTRACT_EVIDENCE_CHILD2_CLOSED_ONLY'and eh['failure']is None and type(eh['actual_child_integer_exit_code'])is int and eh['actual_child_integer_exit_code']==2 and len(eh['records'])==1 and eh['records'][0]['status']=='FAILED'and eh['records'][0]['error']=='own-child stage failed; no retry'and eh['actual_child_report_pin']==b['actual_B_extraction_child_report_pin'],'new full extraction Root0 with original worker2/FAILED/error preserved')
    need(ep['schema']=='ROOT_ACTUAL_CURRENT_MATERIAL_EXTRACTION_REVIEW_V1'and ep['status']=='PASS_ACTUAL_CURRENT_B_FULL55_CONTEXT8_SNAPSHOT_EXTRACTION_EVIDENCE_CHILD2_METADATA_ONLY'and ep['failure']is None and ep['actual_extraction_host_pin']==b['actual_B_extraction_Host_report_pin']and ep['actual_extraction_report_pin']==b['actual_B_extraction_child_report_pin']and ep['current_B_case_input_binding_pin']==b['actual_B_input_binding_pin']and ex['state_order']==['B']and len(ex['states']['B'])==8 and len(ex['context_states']['B'])==55,'new complete B extraction independent metadata post0')
    control=meta(b['actual_B55_control_Host_report_pin']);post=meta(b['actual_B55_control_post_pin']);raw=meta(b['actual_B55_control_Root_tools_pin']);tools=meta(b['actual_B55_control_post_tools_pin'])
    genuine(raw,'actual_terminal_return',b['actual_B55_control_Host_report_pin'],'report_pin');genuine(tools,'actual_review_return',b['actual_B55_control_post_pin'],'review_pin')
    need(b['actual_B55_control_and_post_role_keys_audited']is True and control['schema']=='ACTUAL_CURRENT_B55_OVERV_ORIGINAL_NATIVE_INTEGER_CONTROL_GUARDED_REPORT_V1'and control['status']=='ACTUAL_CURRENT_B55_OVERV_NATIVE_INTEGER_CONTROL_CLOSED0_ONLY'and control['failure']is None and control['final_report_resource_check_passed']is True and control['original_caps']==CAPS and control['actual_B_manifest_pin']==b['actual_B_manifest_pin']and control['actual_B_extraction_report_pin']==b['actual_B_extraction_child_report_pin'],'actual current B55 Root0, no A runtime evidence')
    need(len(control['records'])==len(control['actual_watchdog_checks'])==3,'all three genuine original B55 stages')
    for record,watch in zip(control['records'],control['actual_watchdog_checks']):
        w=watch['actual_watchdog'];need(record['status']=='PASS'and record['command']==w['command']and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'actual original B55 stages preserve all guard limits')
        need(meta(watch['actual_watchdog_pin'])==w,'actual saved B55 watchdog matches report metadata');current(watch['actual_log_pin'])
    results=control['actual_control_results'];need(results['all_three_stages_PASS']is True and results['all_constant64_and_overv370x8_current_words_match']is True and type(results['actual_native_vs_integer_model_and_saved_word_mismatches'])is int and results['actual_native_vs_integer_model_and_saved_word_mismatches']==0 and type(results['actual_current_overv_words_compared'])is int and results['actual_current_overv_words_compared']==2960,'new actual B55 saved/native/integer2960 words match; archive review performs no arithmetic replay')
    roles=b['actual_B55_control_post_role_projection'];need(post['schema']==roles['schema']and post['status']==roles['status']and post['failure']is None and post[roles['actual_Host_report_pin_field']]==b['actual_B55_control_Host_report_pin']and post[roles['actual_Root_tools_pin_field']]==b['actual_B55_control_Root_tools_pin']and type(post[roles['actual_Root_integer_exit_code_field']])is int and post[roles['actual_Root_integer_exit_code_field']]==0,'exact actual B55 post schema/role mapping')
    retained=state['complete_context_pins']+[r['input_pin']for r in state['complete_state_snapshot_inputs']]+[p for row in ex['states']['B']for p in(row['paired_SQLite_pin'],row['paired_original_pool_pin'])]
    need(b['retained_native_current7_pins']==retained and len(retained)==79 and not {p['path']for p in products}&{p['path']for p in retained},'entire55+8+16 retained independently of four archive inputs')
    for p in products+retained+b['original_B_native_and_readonly_input_current7_pins']:current(p);need(Path(p['path']).lstat().st_uid==os.getuid()and p['identity'][3]==1,'all actual data roles remain ordinary owned one-link files')
    latest=meta(b['latest_complete_plan_pin']);prefix=b['inherited_latest_complete_joint_roots'];out=Path(b['planned_actual_output_root']);roots=b['complete_joint_roots'];capture_prefix=inputbinding['complete_latest_prefix_roots']+[inputbinding['actual_output_root']]
    need(prefix==latest['complete_joint_roots']and prefix[:len(capture_prefix)]==capture_prefix and roots==prefix+[str(out)]and out.parent==ROOT/'validation/artifacts'and not os.path.lexists(out)and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y),'entire then-latest prefix including all failures/control outputs plus one fresh archive root; no fixed-count substitute')
    need(b['bounded_total_output_bytes']==64*2**20 and b['bounded_archive_payload_bytes']==56*2**20 and b['bounded_Source_metadata_bytes']==16*2**20,'full output64/payload56/metadata headroom8/Source16')
    build=meta(b['original_guard_build_plan_pin']);full(b['original_guard_build_contract_Source_pin'])
    for p in b['explicit_cumulative_metadata_file_pins']:current(p)
    for k in('original_support_Source_pin','original_bounded_Source_pin','original_production_inputs_Source_pin','original_production_resource_Source_pin','original_history_resource_Source_pin'):full(b[k])
    for p in build['compile_and_link_input_pins']+build['original_SCI_current7_only_pins']+build['readonly_system_tool_metadata_pins']+build['readonly_system_SDK_header_pins']+build['current48_compressed_archive_pins']:current(p)
    for p in build['exact_early14_retired_pins']+build['historical48_plain_full_pins']:need(not os.path.lexists(p['path']),'old retired A roles are not archive operands or live data')
    common=texts['B4_archive_common.UNREADY.py'];worker=texts['archive_B4_products_serial.UNREADY.py'];host=texts['run_guarded_B4_products_lossless_archive.UNREADY.py'];pub=texts['publish_B4_products_archive_CLI.UNREADY.py']
    old_worker=PACKAGE.parent/'current_result43_lossless_archive_source_v3_UNREADY/archive_result43_serial.UNREADY.py';oldpin=pin_small(old_worker);oldtext=full(oldpin).read_text();need(functions(worker)['archive_one']==functions(oldtext)['archive_one'],'whole original streamed SHA/gzip/decompressed SHA+length function preserved')
    need('bm.current_metadata_role(p,build)'in functions(common)['current_metadata']and "build=metadata(binding['original_guard_build_plan_pin'])"in functions(common)['metadata_role_context'],'read-only SDK/clang/PS ownership exceptions delegated to exact frozen B3 metadata roles')
    need('self.metadata_context=metadata_role_context(binding)'in common and 'current_metadata(p,self.binding,self.metadata_context)'in common,'role context cached once while every metadata current7 remains checked')
    admit=functions(common)['admit'];need(not any(x in admit for x in('all48','all43','A2','early14','.jsonl')),'no old result48/A2/early14/JSONL operand or count admission')
    need("with claim.open('x')"in host and host.index("with claim.open('x')")<host.index("initial_hf=json.loads")<host.index('c=bootstrap'),'exclusive owning claim before metadata/project Source imports')
    spine=functions(common)['original_resource_modules'];need(spine.index("'production_inputs'")<spine.index("'production_runner'")and host.index('c.original_resource_modules(b)')<host.index('helper,_=support.load'),'original production_inputs preload and unchanged private OwnRSS import spine')
    need("stage=out/'archive-stage';stage.mkdir()"in host and "watchpath=out/(runner.records[0]['label']+'.watchdog.json')"in host and "log=out/(runner.records[0]['label']+'.log')"in host and "'archive-stage',resources"in host,'case journal parent and exact original record.label monitoring')
    need("for ordinal,p in enumerate(b['all4_product_pins'])"in worker and "c.require(len(entries)==4"in worker and "out/'CURRENT_B4_LOSSLESS_ARCHIVE_INDEX.json'"in worker and 'archive_one(c,p,q,completed_bytes,resources)'in worker,'all four complete product paths retained in serial byte-only archive/index')
    need(not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in('unlink','remove','rmdir')for tree in trees.values()for n in ast.walk(tree)),'no original product deletion or cleanup code')
    need("review['status']=='PASS_SOURCE_ONLY_CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ARCHIVE'"in pub and "review['binding_pin']==ready['execution_binding_pin']"in pub and "('review-pin','review-tools-pin','generation-tools-pin')"in pub and "c.require(len(argv)==24"in pub and "Root_actual_exec_command_sandbox_permissions_required='require_escalated'"in pub,'publisher actual B4 review schema/whole table/three PF inputs/24argv/PS permission')
    joint=0
    for root in roots:
        for p in Path(root).rglob('*'):
            s=p.lstat();need(not stat.S_ISLNK(s.st_mode),'no alias anywhere in full joint prefix')
            if stat.S_ISREG(s.st_mode):joint+=s.st_size
    extra=sum(p['size_bytes']for p in b['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));need(joint+extra+80*2**20<2*2**30,'current full prefix plus archive64/Source16 reserve fits unchanged2GiB, without ratio assumption')
    for p in list(FULL.values()):full(p)
    for p in list(CURRENT.values()):current(p)
    report=dict(schema='INDEPENDENT_CURRENT_B4_COMPLETE_PRODUCT_ARCHIVE_FROZEN_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ARCHIVE',failure=None,source_only=True,metadata_only=True,binding_pin=pb,complete_source_file_pins=ready['complete_source_file_pins'],Root_Source_generation_READY_pin=pr,Root_Source_generation_true_tools_pin=pg,author_Source_freeze_pin=authorpin,actual_B_capture_Host_report_pin=b['actual_B_capture_Host_report_pin'],actual_B_extraction_Host_report_pin=b['actual_B_extraction_Host_report_pin'],actual_B55_control_Host_report_pin=b['actual_B55_control_Host_report_pin'],actual_B55_control_post_pin=b['actual_B55_control_post_pin'],ordered4_complete_original_product_full_pins=products,original4_product_total_bytes=sum(p['size_bytes']for p in products),all79_context_snapshot_saved_pair_current7_pins=retained,complete_joint_roots=roots,inherited_root_count_observed=len(prefix),new_root_count_observed=len(roots),whole_original_archive_one_Source_function_preserved=True,original_archive_worker_Source_reference_pin=oldpin,old48_A2_early14_or_JSONL_operand_admission_reused=False,B3_exact_readonly_system_metadata_roles_preserved=True,whole_small_Source_metadata_twice_pins=list(FULL.values()),nondecoding_current7_only_pins=[p for k,p in CURRENT.items()if k not in FULL],Source_AST_and_global_names_checked=True,unbound_global_candidates=unbound,current_joint_bytes=joint,current_external_metadata_bytes=extra,archive_total_bound_bytes=64*2**20,archive_payload_bound_bytes=56*2**20,Source_metadata_bound_bytes=16*2**20,original_caps=CAPS,product_bytes_opened_or_format_interpreted=False,gzip_or_decompression_executed=False,helper_or_native_imported=False,Source_GEN_or_publication_executed=False,files_deleted=False,plain_retirement_authorized=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,reviewer_Source_pin=pin_small(Path(__file__).absolute()),elapsed_seconds=time.monotonic()-START)
    raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'Source review report6MiB')
    with (BASE/'REVIEW.json').open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    budget();print(json.dumps(dict(status=report['status'],review_pin=pin_small(BASE/'REVIEW.json'),small_Source_metadata_count=len(FULL),current7_only_count=len(CURRENT)-len(FULL))),flush=True)

if __name__=='__main__':main()

