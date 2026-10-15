"""Independent current B55 Source/metadata review. No SQL or helper imports."""
import argparse, ast, hashlib, json, os, resource, stat, sys, time
from pathlib import Path

BASE=Path(__file__).absolute().parent
PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
OUT=ROOT/'validation/artifacts/axial-material-current-B55-OVERV-original-native-integer-control-20261015-v1'
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
    need(not (BASE/'REVIEW.json').exists(),'one immutable formal Source review')
    pr=json.loads(a.ready_pin);pg=json.loads(a.generation_tools_pin);ready=meta(pr);generation=meta(pg)
    need(pr['path']==str(PACKAGE/'SOURCE_REVIEW_READY.json'),'literal current B55 READY role');genuine(generation,'actual_Source_preparation_return',pr,'ready_pin')
    need(ready['schema']=='CURRENT_B55_OVERV_CONTROL_SOURCE_REVIEW_READY_V1'and ready['source_only']is True and ready['SQL_pool_science_compiler_or_native_executed']is False and ready['original_caps']==CAPS,'actual current B55 Source-only READY schema')
    plan=meta(ready['control_plan_pin']);author_pin=pin_small(PACKAGE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');author=meta(author_pin)
    need(author['Source_only_frozen_before_Root_generation']is True and author['native_or_compiler_executed_by_author']is False and author['Source_preparer_or_publisher_executed_by_author']is False and author['whole_Source_file_pins']==ready['complete_source_file_pins'],'all author-frozen Source retained without selected-name subset')
    meta(author['Source_static_evidence_pin']);meta(author['admission_packet_pin'])
    texts={};trees={};unbound=[]
    for p in ready['complete_source_file_pins']:
        q=full(p)
        if q.suffix=='.py':
            text=q.read_text();texts[q.name]=text;trees[q.name]=ast.parse(text);top=symtable.symtable(text,str(q),'exec');known=set(top.get_identifiers())|set(dir(builtins))|{'__file__','__name__'}
            def scan(scope):
                for s in scope.get_symbols():
                    if s.is_global()and s.is_referenced()and s.get_name()not in known:unbound.append(dict(file=q.name,scope=scope.get_name(),line=scope.get_lineno(),name=s.get_name()))
                for child in scope.get_children():scan(child)
            scan(top)
    need(unbound==[],'frozen Source AST/global names have no unbound candidates')
    for p in(ready['host_source_pin'],ready['contract_Source_pin'],ready['control_Fortran_Source_pin'],ready['integer_oracle_Source_pin']):need(p in ready['complete_source_file_pins'],'every execution/math entry in complete Source table')
    need(plan['schema']=='CURRENT_B55_OVERV_CONTROL_PENDING_ACTUAL_BINDINGS_V1'and plan['source_only']is True and plan['actual_business_preconditions_closed']is True and plan['actual_B_extraction_and_post_roles_audited']is True and plan['original_caps']==CAPS,'actual current B extraction roles bound before Source GEN')
    need(plan['Source_generation_SQL_pool_or_science_body_opened']is False and plan['Source_generation_compiler_or_native_executed']is False,'GEN did not execute saved-reader/oracle/compiler/native')
    for k in('actual_B_native_control_report_pin','actual_B_integer_control_report_pin','actual_B_control_Root_tools_pin','actual_B_control_post_pin','actual_B_control_post_tools_pin'):need(plan[k]is None,'no new B control result fabricated before actual execution')
    roots=plan['complete_joint_roots'];latest=meta(plan['latest_complete_plan_pin']);need(roots==latest['complete_joint_roots']+[str(OUT)]and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and not os.path.lexists(OUT),'exact whole latest prefix plus one fresh owning B55 control root')
    need(len(latest['complete_joint_roots'])==71 and len(roots)==72,'observed complete71→72 ledger; entire prefix equality is mandatory')
    need(plan['bounded_new_control_output_reservation_bytes']==16*2**20 and plan['bounded_new_Source_metadata_reservation_bytes']==16*2**20 and plan['future_aggregate_budget_added_to_this_stage']is False,'complete control16MiB+Source16MiB only; later full aggregation remains separate')
    h=meta(plan['actual_B_extraction_Host_report_pin']);raw=meta(plan['actual_B_extraction_Root_tools_pin']);post=meta(plan['actual_B_extraction_post_pin']);pt=meta(plan['actual_B_extraction_post_tools_pin']);ep=plan['actual_B_extraction_child_report_pin'];extraction=meta(ep)
    genuine(raw,'actual_terminal_return',plan['actual_B_extraction_Host_report_pin'],'report_pin');genuine(pt,'actual_review_return',plan['actual_B_extraction_post_pin'],'review_pin')
    need(raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False,'actual extraction original PS guard permission/no retry')
    need(h['schema']=='ACTUAL_CURRENT_B_COMPLETE_EXTRACT_GUARDED_ROOT_REPORT_V1'and h['status']=='ACTUAL_CURRENT_B_COMPLETE_EXTRACT_EVIDENCE_CHILD2_CLOSED_ONLY'and h['failure']is None and h['secondary_failures']==[]and h['final_report_resource_check_passed']is True and h['original_caps']==CAPS and type(h['actual_child_integer_exit_code'])is int and h['actual_child_integer_exit_code']==2 and h['actual_intentional_exit2_normal_closure']is True,'new complete B extraction Root0 and genuine original worker2')
    need(len(h['records'])==1 and h['records'][0]['status']=='FAILED'and h['records'][0]['error']==h['original_runner_error']=='own-child stage failed; no retry','intentional original FAILED/error retained, never converted to child0')
    need(post['schema']=='ROOT_ACTUAL_CURRENT_MATERIAL_EXTRACTION_REVIEW_V1'and post['status']=='PASS_ACTUAL_CURRENT_B_FULL55_CONTEXT8_SNAPSHOT_EXTRACTION_EVIDENCE_CHILD2_METADATA_ONLY'and post['failure']is None and post['metadata_only']is True and post['actual_extraction_host_pin']==plan['actual_B_extraction_Host_report_pin']and post['actual_Root_true_tool_return_pin']==plan['actual_B_extraction_Root_tools_pin']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0 and type(post['actual_child_integer_exit_code'])is int and post['actual_child_integer_exit_code']==2,'independent new B extraction metadata post0; no SQL replay claimed')
    need(h['actual_child_report_pin']==ep and post['actual_extraction_report_pin']==ep and extraction['state_order']==['B']and set(extraction['states'])=={'B'}and len(extraction['states']['B'])==8 and len(extraction['context_states']['B'])==55,'all eight new B saved pairs and55contexts retained')
    descriptor=extraction['states']['B'][-1];pair=dict(sqlite_pin=descriptor['paired_SQLite_pin'],native_pool_pin=descriptor['paired_original_pool_pin'])
    need(descriptor==plan['selected_actual_B55_snapshot_descriptor']and descriptor['state']=='B'and descriptor['event']==55 and descriptor['role']=='final-complete-micro'and descriptor['root_prefix']==[]and pair==plan['selected_actual_B55_SQL_pool_pair'],'exact new B55 descriptor/pair; no A input substitution')
    need(extraction['actual_observation_manifest_pin']==plan['actual_B_manifest_pin']and extraction['current_B_case_input_binding_pin']==plan['actual_B_input_binding_pin']and post['actual_observation_manifest_pin']==plan['actual_B_manifest_pin']and post['current_B_case_input_binding_pin']==plan['actual_B_input_binding_pin']and post['all_original_snapshot_and_context_pins_verified']is True,'actual capture/extraction/post/current B input lineage')
    for row in extraction['states']['B']:
        current(row['input_pin']);current(row['paired_SQLite_pin']);current(row['paired_original_pool_pin'])
        for p in row['all_output_file_pins']:current(p)
    binding=meta(plan['actual_B_input_binding_pin']);manifest=meta(plan['actual_B_manifest_pin']);prefix=binding['complete_latest_prefix_roots']+[binding['actual_output_root']]
    need(roots[:-1][:len(prefix)]==prefix and manifest['state_order']==['B']and manifest['current_B_case_input_binding_pin']==plan['actual_B_input_binding_pin'],'all original capture/failure history inside latest prefix')
    build=meta(plan['original_guard_build_plan_pin']);full(plan['original_guard_build_contract_Source_pin'])
    for k in('original_Common_Source_pin','original_support_Source_pin','original_bounded_Source_pin','original_production_inputs_Source_pin','original_OVERV_shared_methods_Source_pin'):full(plan[k])
    for k in('explicit_cumulative_metadata_file_pins','inherited_metadata_current7_pins','explicit_control_metadata_pins'):
        for p in plan[k]:current(p)
    for p in ready['dependencies']:current(p)
    for p in[plan['original_compiler_pin'],*plan['original_four_archive_pins']]:current(p)
    need(plan['original_compile_flags']==['-O2','-march=native','-ffp-contract=off','-fcheck=all','-fbacktrace','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none']and len(plan['original_four_archive_pins'])==4,'original nine flags/four archive order retained')
    for p in build['compile_and_link_input_pins']+build['original_SCI_current7_only_pins']+build['readonly_system_tool_metadata_pins']+build['readonly_system_SDK_header_pins']+build['current48_compressed_archive_pins']+build['prior_failed_B_partial_output_pins']:current(p)
    for p in build['exact_early14_retired_pins']+build['historical48_plain_full_pins']:need(not os.path.lexists(p['path']),'old retired result/data roles absent and never new compiler inputs')
    mathproof=meta(pin_small(PACKAGE/'B55_SOURCE_ONLY_MATH_BYTE_COPY_AND_INTERFACE_STATIC_EVIDENCE.json'))
    for row in mathproof['whole_Source_copies']:
        left=full(row['original_Source_pin']);right=full(row['new_Source_pin']);need(left.read_bytes()==right.read_bytes(),'whole original Fortran/oracle/adapter/B55 interface')
    need(ready['control_Fortran_Source_pin']['sha256']=='dc89ba9c94ebe9e709c7ba0bad8a59d1a7269ee8a5389209982ad13c44a3ca3f'and ready['integer_oracle_Source_pin']['sha256']=='36cfc700c7e5454f5223eacfda37b623689057649b6f1de6d04535009a9bd888','original unchanged native and integer arithmetic Source bytes')
    template=PACKAGE.parents[1]/'OVERV_original_guarded_integer_control_source_v3_20261014/run_guarded_OVERV_integer_current_control.py';templatepin=pin_small(template);ot=full(templatepin).read_text();host=texts['run_guarded_current_B55_OVERV_control.UNREADY.py'];shared=texts['original_OVERV_shared_methods.UNREADY.py']
    of=functions(ot);nf=functions(shared)
    for name in mathproof['whole_original_shared_function_copies']:need(of[name]==nf[name],'whole original shared Source function '+name)
    start="  adapter=source_module(plan['original_saved_input_adapter_Source_pin'],'OVERV_original_saved_adapter')\n";end="  require(actual['all_three_stages_PASS']is True,'exact three original native stages');verified=True\n"
    need(ot[ot.index(start):ot.index(end)+len(end)]==host[host.index(start):host.index(end)+len(end)],'entire saved-reader/native/exact-integer comparison block wholebytes; template Source only, no old A runtime result used')
    need(host.index(".open('x')")<host.index('sf,psf=frozen_arg')<host.index('spec=importlib.util.spec_from_file_location'),'exclusive Root claim before metadata EOF/project import/SQL')
    need(host.index("m.source(plan['original_production_inputs_Source_pin'],'production_inputs')")<host.index('helper,_=support.load'),'original production_inputs preload before private guard imports')
    fn=next(n for n in trees['B55_owning_Source_contract.UNREADY.py'].body if isinstance(n,ast.FunctionDef)and n.name=='admit');returns=[n for n in ast.walk(fn)if isinstance(n,ast.Return)];need(len(returns)==1 and isinstance(returns[0].value,ast.Tuple),'actual owning contract data tuple returned');names=[n.id for n in returns[0].value.elts]
    need(names==['build','bm','descriptor','selected','bridge','capture_binding','latest'],'all required original guard/descriptor/resource values returned')
    for file in('run_guarded_current_B55_OVERV_control.UNREADY.py','prepare_current_B55_OVERV_Source.UNREADY.py'):
        calls=[n for n in ast.walk(trees[file])if isinstance(n,ast.Assign)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Attribute)and n.value.func.attr=='admit']
        need(len(calls)==1 and isinstance(calls[0].targets[0],ast.Tuple)and [n.id for n in calls[0].targets[0].elts]==names,'both real admit callers unpack all seven Source data roles')
    need("(out/'OVERV-original-control').mkdir()"in host and "wp=out/(record['label']+'.watchdog.json')"in host and "lp=out/(record['label']+'.log')"in host and 'own<m.OUTPUT_BOUND'in host and 'bridge.admit_control_only_stage(plan,capture_binding,latest,before)'in host,'original journal/record.label monitors and current control16MiB hard/resource gates')
    pub=texts['publish_current_B55_OVERV_CLI.UNREADY.py'];need("review['status']=='PASS_SOURCE_ONLY_CURRENT_B55_OVERV_CONTROL'"in pub and "('review-pin','review-tools-pin','generation-tools-pin')"in pub and "m.need(len(argv)==24"in pub and "Root_actual_exec_command_sandbox_permissions_required='require_escalated'"in pub,'publisher actual current B55 schema/three PF inputs/24argv/original PS permission')
    need(plan['A_control_reused']is False and all(plan[k]is False for k in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete'))and plan.get('source_context_issue_resolved')is not True,'no inherited A runtime or premature issue/physics/goal qualification; actual missing issue field remains missing')
    joint=0
    for root in roots:
        for path in Path(root).rglob('*'):
            s=path.lstat();need(not stat.S_ISLNK(s.st_mode),'no alias across entire joint prefix')
            if stat.S_ISREG(s.st_mode):joint+=s.st_size
    extra=sum(p['size_bytes']for p in plan['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));need(joint+extra+32*2**20<2*2**30,'current entire prefix+complete control16/Source16 fits unchanged2GiB')
    for p in list(FULL.values()):full(p)
    for p in list(CURRENT.values()):current(p)
    report=dict(schema='INDEPENDENT_CURRENT_B55_OVERV_CONTROL_FROZEN_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_B55_OVERV_CONTROL',failure=None,source_only=True,metadata_only=True,control_plan_pin=ready['control_plan_pin'],complete_source_file_pins=ready['complete_source_file_pins'],Root_Source_generation_tools_pin=pg,Root_Source_generation_READY_pin=pr,author_Source_freeze_pin=author_pin,actual_B_extraction_Host_report_pin=plan['actual_B_extraction_Host_report_pin'],actual_B_extraction_post_pin=plan['actual_B_extraction_post_pin'],selected_actual_B55_SQL_pool_pair_current7_only=pair,selected_actual_B55_snapshot_descriptor=descriptor,complete_joint_roots=roots,whole_small_Source_metadata_twice_pins=list(FULL.values()),nondecoding_current7_only_pins=[p for k,p in CURRENT.items()if k not in FULL],all_frozen_Python_AST_and_global_names_checked=True,unbound_global_candidates=unbound,whole_original_Fortran_integer_oracle_adapter_and_shared_methods=True,whole_original_saved_reader_and_math_try_block_preserved=True,old_A_control_Source_template_pin=templatepin,old_A_control_runtime_evidence_used=False,actual_original_B_extraction_worker2_FAILED_error_retained=True,required_actual_control_payload_bytes=13324,required_ENERGY_original_words=371,required_OVERV_original_words=370*8,original_caps=CAPS,current_joint_bytes=joint,current_external_metadata_bytes=extra,control_only_reservation_bytes=16*2**20,Source_metadata_reservation_bytes=16*2**20,SQL_pool_or_scientific_body_read=False,helper_imported=False,integer_oracle_or_Fortran_executed=False,Source_GEN_or_publication_executed=False,compiler_or_native_executed=False,A_control_reused=False,source_context_issue_resolved=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,reviewer_Source_pin=pin_small(Path(__file__).absolute()),elapsed_seconds=time.monotonic()-START)
    raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'Source review report6MiB')
    with (BASE/'REVIEW.json').open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    budget();print(json.dumps(dict(status=report['status'],review_pin=pin_small(BASE/'REVIEW.json'),small_Source_metadata_count=len(FULL),current7_only_count=len(CURRENT)-len(FULL))),flush=True)

if __name__=='__main__':main()

