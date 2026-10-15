"""Independent extract-only Source/metadata review. No candidate/helper imports."""
import argparse, ast, hashlib, json, os, resource, stat, sys, time
from pathlib import Path

BASE=Path(__file__).absolute().parent
PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
OUT=ROOT/'validation/artifacts/axial-material-current-B-complete-fullfield-extract-20261015-v2'
OLD_PACKAGE=PACKAGE.parent/'current_B_complete_extract_host_source_v1_UNREADY'
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

def declared_v1_inverse(texts,source_table,limit):
    old_author=meta(pin_small(OLD_PACKAGE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json'));oldtable={Path(p['path']).name:p for p in old_author['whole_Source_file_pins']}
    need(set(oldtable)==set(source_table)and len(oldtable)==13,'all original thirteen core Source roles retained')
    rows=[];unchanged=0
    for name,p in source_table.items():
        previous=full(oldtable[name]).read_text();current_text=texts[name];expected=previous
        if name=='current_B_material_lineage_evidence.UNREADY.py':
            first='        self.last=now;total=0';second="        require(total+sum(unlinked.values())<2*2**30,'unchanged joint fresh2GiB including SQLite/open-unlinked')"
            need(previous.count(first)==previous.count(second)==1,'exact two original worker Budget markers')
            expected=expected.replace(first,'        total=0',1).replace(second,second+'\n        self.last=time.monotonic()',1)
        elif name=='extract_Source_contract.UNREADY.py':
            need(previous.count('axial-material-current-B-complete-fullfield-extract-20261015-v1')==1 and previous.count('OUTPUT_BOUND=512*2**20')==1,'exact original contract namespace/phase bound')
            expected=expected.replace('axial-material-current-B-complete-fullfield-extract-20261015-v1','axial-material-current-B-complete-fullfield-extract-20261015-v2',1).replace('OUTPUT_BOUND=512*2**20','OUTPUT_BOUND='+str(limit//2**20)+'*2**20',1).replace('extract-only512MiB','extract-only'+str(limit//2**20)+'MiB').replace('extract512/Source16','extract'+str(limit//2**20)+'/Source16')
        elif name in('run_guarded_current_B_complete_extract.UNREADY.py','prepare_current_B_extract_Source.UNREADY.py'):
            expected=expected.replace('under512MiB','under'+str(limit//2**20)+'MiB').replace('extraction512MiB','extraction'+str(limit//2**20)+'MiB')
        need(current_text==expected,'whole v2 Source is exact declared v1 inverse '+name)
        same=current_text==previous;unchanged+=same;rows.append(dict(name=name,old_v1_Source_pin=oldtable[name],new_Source_pin=p,whole_v1_bytes_unchanged=same,only_declared_metadata_or_namespace_or_harder_phase_bound_change=True))
    return rows,unchanged

def admit_original_v1_failure(plan,latest):
    need(plan['actual_v1_failure_roles_audited']is True and plan['if_v1_success_do_not_run_v2']is True,'v2 requires actual audited failure of v1, never retry original owning root')
    pr=plan['prior_v1_actual_Root_tools_pin'];ph=plan['prior_v1_actual_Host_report_pin'];pp=plan['prior_v1_actual_failure_post_pin'];pt=plan['prior_v1_actual_failure_post_tools_pin'];r=meta(pr);h=meta(ph);p=meta(pp);t=meta(pt);a=r['actual_terminal_return']
    need(r['observed_closed']is True and type(r['original_integer_exit_code'])is int and r['original_integer_exit_code']==1 and type(a['exit_code'])is int and a['exit_code']==1 and a.get('session_id')is None and r['actual_execution_permission_mode']=='require_escalated'and r['actual_retried']is False,'prior genuine closed Root1 preserved once')
    genuine(t,'actual_review_return',pp,'review_pin')
    need(p['schema']=='CURRENT_B_COMPLETE_EXTRACT_ACTUAL_FAILURE_FACTS_METADATA_POST_V1'and p['status']=='PASS_FAILURE_FACTS_ONLY'and p['failure']is None and p['metadata_only']is True and p['actual_Root_tools_pin']==pr and p['actual_Host_report_pin']==ph and type(p['actual_Root_integer_exit_code'])is int and p['actual_Root_integer_exit_code']==1 and p['actual_recorded_child_integer_exit_codes']==[-15]and p['absent_child_code_invented']is False and p['child_code_inferred_from_Root_return']is False and p['complete_extraction_inferred']is False,'genuine independent failure facts preserve Root1/observed child-15')
    need(h['schema']=='ACTUAL_CURRENT_B_COMPLETE_EXTRACT_GUARDED_ROOT_REPORT_V1'and h['status']=='FAILED_CURRENT_B_COMPLETE_EXTRACT_NO_RETRY'and h['failure']is not None and h['actual_intentional_exit2_normal_closure']is False and type(h['actual_child_integer_exit_code'])is int and h['actual_child_integer_exit_code']==-15 and h['actual_complete_child_receipt']is None and h['actual_child_report_pin']is None and h['original_caps']==CAPS and h['control_plan_pin']==plan['latest_complete_plan_pin']and h['complete_joint_roots']==latest['complete_joint_roots'],'original failed full-prefix Host retained, no extraction report or SQL qualification')
    need(len(h['records'])==1 and h['records']==p['actual_stage_records'],'exact original failed record preserved');record=h['records'][0];w=meta(h['actual_watchdog_full_pin'])
    need(w==h['actual_watchdog']and record['status']=='FAILED'and record['error']==h['original_runner_error']=='own-child wall cap reached'and w['command']==record['command']and type(w['returncode'])is int and w['returncode']==-15 and w['limit_failure']=="RuntimeError('own-child wall cap reached')"and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['wall_cap_seconds']<=600 and w['elapsed_seconds']>w['wall_cap_seconds'],'genuine wall-limit failure remains failed, no threshold or exit-code rewrite')
    parts=p['new_partial_output_blind_fullEOF_twice_pins'];need(len(parts)==6 and ph in parts and not any(Path(x['path']).suffix=='.sqlite'for x in parts),'exact six original partial files/Host retained and no completed SQL pair invented')
    for x in parts:current(x)
    need(all(plan[k]is False for k in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete'))and all(p[k]is False for k in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete')),'old failure never promoted to scientific success')
    return dict(actual_Root_tools_pin=pr,actual_Host_report_pin=ph,independent_failure_post_pin=pp,independent_failure_post_tools_pin=pt,actual_Root_integer_exit_code=1,actual_child_integer_exit_code=-15,actual_failed_record=record,actual_watchdog=w,all_six_partial_output_current7_only_pins=parts)

def main():
    import builtins,symtable
    ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--ready-pin',required=True);ap.add_argument('--generation-tools-pin',required=True);a=ap.parse_args()
    need(not (BASE/'REVIEW.json').exists(),'one immutable independent formal Source review')
    pr=json.loads(a.ready_pin);pg=json.loads(a.generation_tools_pin);ready=meta(pr);generation=meta(pg)
    need(pr['path']==str(PACKAGE/'SOURCE_REVIEW_READY.json'),'literal READY role');genuine(generation,'actual_Source_preparation_return',pr,'ready_pin')
    need(ready['schema']=='CURRENT_B_COMPLETE_EXTRACT_SOURCE_REVIEW_READY_V1'and ready['source_only']is True and ready['Source_or_decoder_or_native_business_executed']is False and ready['original_caps']==CAPS,'actual Source-only READY schema')
    plan=meta(ready['control_plan_pin']);author_pin=pin_small(PACKAGE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');author=meta(author_pin)
    need(author['Source_only_frozen_before_Root_generation']is True and author['native_or_compiler_executed_by_author']is False and author['Source_preparer_or_publisher_executed_by_author']is False and author['whole_Source_file_pins']==ready['complete_source_file_pins'],'entire exact author Source table, no selected-name omission')
    static=meta(author['Source_static_evidence_pin']);meta(author['admission_packet_pin']);need(static['source_only']is True and static['all13_whole_reverse_equal_frozen_v1']is True and static['metadata_scan_throttle_only_after_complete_success']is True and static['per_call_SELF512_stage600_checks_before_throttle_unchanged']is True and static['all_roots_external_metadata_open_unlinked_and_1MiB_SHA_scope_unchanged']is True and static['all_original_math_55context_8tree_original_caps_and_guard_unchanged']is True and static['GEN_pub_worker_helper_or_science_executed_by_author']is False,'actual final author inverse evidence preserves all scope/caps and exact metadata-only throttle')
    for role in('original_Common_Source_pin','original_support_Source_pin','original_bounded_Source_pin','original_production_inputs_Source_pin'):full(plan[role])
    texts={};trees={};unbound=[]
    for p in ready['complete_source_file_pins']:
        q=full(p)
        if q.suffix=='.py':
            text=q.read_text();trees[q.name]=ast.parse(text);texts[q.name]=text;top=symtable.symtable(text,str(q),'exec');known=set(top.get_identifiers())|set(dir(builtins))|{'__file__','__name__'}
            def scan(scope):
                for s in scope.get_symbols():
                    if s.is_global()and s.is_referenced()and s.get_name()not in known:unbound.append(dict(file=q.name,scope=scope.get_name(),line=scope.get_lineno(),name=s.get_name()))
                for child in scope.get_children():scan(child)
            scan(top)
    need(unbound==[],'no unbound global data-flow candidates in frozen Source')
    need(ready['host_source_pin']in ready['complete_source_file_pins']and ready['contract_Source_pin']in ready['complete_source_file_pins'],'host and contract in complete Source table')
    need(plan['schema']=='CURRENT_B_COMPLETE_EXTRACT_SOURCE_ONLY_PLAN_V1'and plan['source_only']is True and plan['actual_business_preconditions_closed']is True and plan['source_role_pin_audit_complete']is True and plan['capture_actual_role_keys_audited']is True and plan['original_caps']==CAPS,'actual fully bound extract-only plan')
    limit=plan['bounded_new_extract_output_reservation_bytes'];need(type(limit)is int and 0<limit<=512*2**20 and limit%2**20==0,'actual stricter extraction phase bound from plan')
    need(plan['only_current_stage']=='extract'and plan['future_aggregate_and_B_OVERV_budget_added_to_this_stage']is False and plan['bounded_new_extract_output_reservation_bytes']==limit and plan['bounded_new_Source_metadata_reservation_bytes']==16*2**20 and plan['Source_generation_science_bodies_decoded']is False and plan['Source_generation_decoder_or_native_executed']is False,'only full extract512MiB+Source16MiB; no future phase admission or decoding')
    latest=meta(plan['latest_complete_plan_pin']);roots=plan['complete_joint_roots'];need(roots==latest['complete_joint_roots']+[str(OUT)]and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and not os.path.lexists(OUT),'exact whole latest prefix plus one fresh owning extraction root')
    v1_failure=admit_original_v1_failure(plan,latest);need(plan['latest_complete_plan_pin']['path']==str(OLD_PACKAGE/'PLAN.json')and str(OUT)!=latest['complete_joint_roots'][-1],'entire failed v1 prefix plus one distinct new owning root, no fixed ordinal admission')
    h=meta(plan['actual_capture_Host_report_pin']);manifest=meta(plan['actual_observation_manifest_pin']);binding=meta(plan['current_B_case_input_binding_pin']);proof=plan['actual_capture_control_binding'];raw=meta(proof['actual_Root_tools_pin']);post=meta(proof['actual_capture_post_pin']);pt=meta(proof['actual_capture_post_tools_pin'])
    genuine(raw,'actual_terminal_return',plan['actual_capture_Host_report_pin'],'report_pin');genuine(pt,'actual_review_return',proof['actual_capture_post_pin'],'review_pin')
    need(raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False,'actual capture original PS permission and no retry')
    need(proof['actual_Host_report_pin']==plan['actual_capture_Host_report_pin']and h['schema']=='ACTUAL_CURRENT_B_COMPLETE_NATIVE_CAPTURE_ROOT_REPORT_V1'and h['status']=='ACTUAL_CURRENT_B_FULL55_CONTEXT_8TREE_4PRODUCT_CAPTURE_CLOSED0_ONLY'and h['failure']is None and h['secondary_failures']==[]and h['final_report_resource_check_passed']is True and h['original_caps']==CAPS,'actual full B native capture Root0')
    stdout=json.loads(raw['actual_terminal_return']['output'].strip().splitlines()[-1]);need(stdout['manifest_pin']==plan['actual_observation_manifest_pin']and stdout['actual_B_native_capture_closed0']is True,'actual Root stdout binds whole B manifest')
    roles=proof['capture_post_role_projection'];need(post['schema']==roles['schema']and post['status']==roles['status']and post['failure']is None and post['metadata_only']is True and post[roles['actual_Host_report_pin_field']]==plan['actual_capture_Host_report_pin']and post[roles['actual_Root_tools_pin_field']]==proof['actual_Root_tools_pin']and type(post[roles['actual_Root_integer_exit_code_field']])is int and post[roles['actual_Root_integer_exit_code_field']]==0,'exact actual independent capture post0 schema/key projection')
    need(len(h['records'])==len(h['actual_watchdog_checks'])==1,'one genuine capture child');record=h['records'][0];watch=h['actual_watchdog_checks'][0];w=meta(watch['actual_watchdog_pin'])
    need(record['status']=='PASS'and w==watch['actual_watchdog']and w['command']==record['command']and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'original capture child0/caps/closure retained')
    state=h['actual_B_state'];need(manifest['state_order']==['B']and set(manifest['states'])=={'B'}and manifest['states']['B']==dict(state,actual_owning_report_pin=plan['actual_capture_Host_report_pin'])and manifest['current_B_case_input_binding_pin']==plan['current_B_case_input_binding_pin']and binding['original_caps']==CAPS,'exact immutable current B manifest/state/input binding')
    need(len(state['complete_context_pins'])==55 and len(state['complete_state_snapshot_inputs'])==8 and len(state['actual_material_product_pins'])==4 and len(state['actual_all_event_headers_in_original_execution_order'])==55,'complete 55-context/8-tree/four-product roles')
    for p in state['physical_input_pins']+state['complete_observed_file_pins']:current(p)
    lifecycle=plan['completed_capture_ASCII_lifecycle_binding'];retired=[]
    if lifecycle is None:
        for p in state['actual_material_product_pins']:current(p)
    else:
        need(lifecycle['actual_role_projection_audited']is True,'actual optional ASCII lifecycle roles audited');k=lifecycle['actual_role_projection'];r=meta(lifecycle['receipt_pin']);rt=meta(lifecycle['Root_tools_pin']);p=meta(lifecycle['post_pin']);t=meta(lifecycle['post_tools_pin']);genuine(rt,k['Root_return_field'],lifecycle['receipt_pin'],k['Root_output_receipt_field']);genuine(t,k['post_return_field'],lifecycle['post_pin'],k['post_output_review_field'])
        retired=[p for p in state['actual_material_product_pins']if Path(p['path']).name in('u.asc','a.asc','t.asc')]
        need(len(retired)==3 and r['schema']==k['receipt_schema']and r['status']==k['receipt_status']and r['failure']is None and r[k['released_pins_field']]==retired and r[k['released_bytes_field']]==sum(p['size_bytes']for p in retired)and all(not os.path.lexists(p['path'])for p in retired),'exact real three ASCII retirement only; all binary/context scope retained')
        need(p['schema']==k['post_schema']and p['status']==k['post_status']and p['failure']is None and p[k['post_receipt_field']]==lifecycle['receipt_pin']and p[k['post_Root_tools_field']]==lifecycle['Root_tools_pin'],'actual independent ASCII lifecycle post0')
        for p in state['actual_material_product_pins']:
            if p not in retired:current(p)
    prefix=binding['complete_latest_prefix_roots']+[binding['actual_output_root']];need(roots[:-1][:len(prefix)]==prefix,'entire prior capture/failure ledger prefix retained')
    build=meta(plan['original_guard_build_plan_pin']);full(plan['original_guard_build_contract_Source_pin'])
    for key in('explicit_cumulative_metadata_file_pins','inherited_metadata_current7_pins','explicit_control_metadata_pins','child_ordinary_explicit_metadata_pins'):
        for p in plan[key]:current(p)
    for p in ready['dependencies']:current(p)
    for p in plan['child_ordinary_explicit_metadata_pins']:need(Path(p['path']).lstat().st_uid==os.getuid()and p['identity'][3]==1,'child ordinary metadata only; system roles stay outer')
    for p in build['compile_and_link_input_pins']+build['original_SCI_current7_only_pins']+build['readonly_system_tool_metadata_pins']+build['readonly_system_SDK_header_pins']+build['current48_compressed_archive_pins']+build['prior_failed_B_partial_output_pins']:current(p)
    for p in build['exact_early14_retired_pins']+build['historical48_plain_full_pins']:need(not os.path.lexists(p['path']),'historical retired A operands remain absent')
    integration=PACKAGE.parent/'current_extra_reaction_source_v2/B_complete_evidence_integration_source_v3_UNREADY';inv=meta(pin_small(integration/'UNREADY_SOURCE_COPY_AND_METADATA_INVERSE_INVENTORY.json'));source_table={Path(p['path']).name:p for p in ready['complete_source_file_pins']}
    need(len(inv['Source_file_pins'])==9,'all nine whole original integration Sources included')
    for p in inv['Source_file_pins']:
        original=full(p);candidate=full(source_table[original.name])
        if original.name!='current_B_material_lineage_evidence.UNREADY.py':need(original.read_bytes()==candidate.read_bytes(),'whole eight original integration Sources; no mathematics/decoder edits')
    inverse_rows,whole_v1_count=declared_v1_inverse(texts,source_table,limit);need(whole_v1_count==static['whole_v1_Source_equal_count']==author['whole_v1_Source_equal_count']and len(inverse_rows)-whole_v1_count==static['modified_Source_count']==author['modified_Source_count']and static['new_phase_output_bound_bytes']==author['current_extract_phase_output_hard_bound_bytes']==limit,'independent all13 inverse matches exact author change census and stricter actual phase bound')
    throttle=meta(plan['peer_metadata_Budget_throttle_whole_inverse_pin']);meta(plan['peer_metadata_Budget_throttle_Source_freeze_pin']);need(throttle['only_worker_Budget_check_changed']is True and throttle['whole_worker_inverse_restores_original']is True and throttle['every_Budget_call_SELF_and_elapsed_checks_before_throttle_unchanged']is True and throttle['all_joint_roots_and_explicit_metadata_and_open_unlinked_scan_loop_bytes_unchanged']is True and throttle['original_1MiB_full_EOF_SHA_loop_wholebytes_unchanged']is True and throttle['original_SELF_threshold_bytes']==512*2**20 and throttle['original_child_elapsed_seconds']==600 and throttle['original_cumulative_bytes']==2*2**30,'independently exact two-marker worker inverse preserves SELF/600/every root/metadata/open-unlinked/1MiB EOF SHA')
    host=texts['run_guarded_current_B_complete_extract.UNREADY.py'];contract=texts['extract_Source_contract.UNREADY.py'];gen=texts['prepare_current_B_extract_Source.UNREADY.py'];pub=texts['publish_current_B_extract_CLI.UNREADY.py'];worker=texts['current_B_material_lineage_evidence.UNREADY.py']
    bound_node=next(n.value for n in trees['extract_Source_contract.UNREADY.py'].body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='OUTPUT_BOUND'for t in n.targets));need(integer_expression(bound_node)==limit,'actual outer Source phase bound equals exact plan value')
    need(host.index(".open('x')")<host.index('sf,psf=frozen_arg')<host.index('spec=importlib.util.spec_from_file_location'),'exclusive Root claim before metadata EOF/import/decoder')
    fn=next(n for n in trees['extract_Source_contract.UNREADY.py'].body if isinstance(n,ast.FunctionDef)and n.name=='admit');returns=[n for n in ast.walk(fn)if isinstance(n,ast.Return)]
    need(len(returns)==1 and isinstance(returns[0].value,ast.Tuple)and [n.id for n in returns[0].value.elts]==['build','bm','manifest','binding','state'],'five required data-flow outputs actually returned')
    need('build,bm,manifest,binding,state=m.admit(packet)'in host and 'build,bm,manifest,binding,state=m.admit(packet)'in gen,'both live caller sites unpack exact five outputs')
    call=next(n for n in ast.walk(trees['run_guarded_current_B_complete_extract.UNREADY.py'])if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='extract_request');signature=next(n for n in trees['build_current_B_evidence_requests.UNREADY.py'].body if isinstance(n,ast.FunctionDef)and n.name=='extract_request')
    need(len(call.args)==len(signature.args.args) and call.keywords==[],'actual AST request constructor call and signature agree without guessed fixed count')
    need("(m.OUT/'evidence-stage').mkdir()"in host and 'm.admit_extract_only_stage(packet,binding,before)'in host and 'admit_operation_ledger('not in host and 'admit_operation_ledger('not in contract,'case journal parent created; only independently admitted current extract stage')
    need(host.index("m.source(packet['original_production_inputs_Source_pin'],'production_inputs')")<host.index('helper,_=support.load'),'original production_inputs preload precedes original private guard imports')
    need("record['status']=='FAILED'"in host and "watch['returncode']==2"in host and "original_error=='own-child stage failed; no retry'"in host and "raise SystemExit(2)"in worker and "len(v['states']['B'])==8"in host and "len(v['context_states']['B'])==55"in host,'original worker2/FAILED/error retained with entire8/55 scope')
    need("watch_path=m.OUT/(record['label']+'.watchdog.json')"in host and "log_path=m.OUT/(record['label']+'.log')"in host and 'own<m.OUTPUT_BOUND'in host,'original record.label paths and entire extraction output512 bound')
    need("review['status']=='PASS_SOURCE_ONLY_CURRENT_B_COMPLETE_EXTRACT'"in pub and "('review-pin','review-tools-pin','generation-tools-pin')"in pub and "m.need(len(argv)==24"in pub and "Root_actual_exec_command_sandbox_permissions_required='require_escalated'"in pub,'publisher exact review schema/three PF args/24argv/permission')
    need(all(plan[k]is False for k in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete','B_OVERV_control_completed','B_six_phase_construction_completed')),'no extraction/control/aggregation/physics qualification minted')
    joint=0
    for root in roots:
        for path in Path(root).rglob('*'):
            s=path.lstat();need(not stat.S_ISLNK(s.st_mode),'no alias in whole latest joint prefix')
            if stat.S_ISREG(s.st_mode):joint+=s.st_size
    extra=sum(p['size_bytes']for p in plan['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));need(joint+extra+limit+16*2**20<2*2**30,'fresh entire prefix+only full extract512/Source16 fits original cumulative2GiB')
    for p in list(FULL.values()):full(p)
    for p in list(CURRENT.values()):current(p)
    report=dict(schema='INDEPENDENT_CURRENT_B_COMPLETE_EXTRACT_FROZEN_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_B_COMPLETE_EXTRACT',failure=None,source_only=True,metadata_only=True,control_plan_pin=ready['control_plan_pin'],complete_source_file_pins=ready['complete_source_file_pins'],Root_Source_generation_tools_pin=pg,Root_Source_generation_READY_pin=pr,author_Source_freeze_pin=author_pin,actual_capture_Host_report_pin=plan['actual_capture_Host_report_pin'],actual_capture_post_pin=proof['actual_capture_post_pin'],actual_observation_manifest_pin=plan['actual_observation_manifest_pin'],complete_joint_roots=roots,whole_small_Source_metadata_twice_pins=list(FULL.values()),nondecoding_current7_only_pins=[p for k,p in CURRENT.items()if k not in FULL],all_frozen_Source_AST_and_global_names_checked=True,unbound_global_candidates=unbound,all_eight_original_scientific_integration_Source_wholebytes_preserved=True,whole_v1_Source_inverse_rows=inverse_rows,whole_v1_unchanged_Source_count=whole_v1_count,worker_only_complete_scan_timestamp_throttle_changed=True,old_v1_actual_failure_evidence=v1_failure,Source_reviewer_task='/root/b_capture_actual_post_source',core_or_worker_Source_authored_by_this_reviewer=False,actual_post_Source_authored_by_this_reviewer=True,original_worker_exit2_FAILED_error_preserved=True,all55_contexts_and8_native_trees_retained=True,optional_historical_completed_ASCII_retired_pins=retired,original_caps=CAPS,existing_joint_bytes=joint,current_external_metadata_bytes=extra,extract_only_reservation_bytes=limit,Source_metadata_reservation_bytes=16*2**20,helper_imported=False,Source_GEN_or_publication_executed=False,decoder_or_scientific_body_opened=False,compiler_or_native_executed=False,adapted_from_v1_reviewer_Source_pin=pin_small(OLD_PACKAGE/'independent_source_review_20261015/corrected_exact_AST_interface_v2/review_current_B_extract_Source_only.py'),open_unlinked_not_assumed_zero_actual_Root_original_guard_required=True,actual_request_AST_call_count=len(call.args),actual_request_AST_signature_count=len(signature.args.args),reviewer_Source_pin=pin_small(Path(__file__).absolute()),elapsed_seconds=time.monotonic()-START,**FALSE)
    raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'review report6MiB')
    with (BASE/'REVIEW.json').open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    budget();print(json.dumps(dict(status=report['status'],review_pin=pin_small(BASE/'REVIEW.json'),small_Source_metadata_count=len(FULL),current7_only_count=len(CURRENT)-len(FULL))),flush=True)

if __name__=='__main__':main()

