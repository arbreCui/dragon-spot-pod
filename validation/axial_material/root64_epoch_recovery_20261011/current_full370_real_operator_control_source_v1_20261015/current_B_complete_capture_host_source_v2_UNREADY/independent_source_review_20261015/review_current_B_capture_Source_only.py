"""Independent frozen Source/metadata review. Never imports an authored helper."""
import argparse, ast, hashlib, json, os, resource, stat, sys, time
from pathlib import Path

BASE=Path(__file__).absolute().parent
PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
OUT=ROOT/'validation/artifacts/axial-material-inputs-20261003/A/b63'
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
    ap=argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--ready-pin',required=True);ap.add_argument('--generation-tools-pin',required=True)
    a=ap.parse_args();need(not (BASE/'REVIEW.json').exists(),'one formal review, no overwrite')
    ready_pin=json.loads(a.ready_pin);gen_pin=json.loads(a.generation_tools_pin)
    ready=meta(ready_pin);generation=meta(gen_pin)
    need(ready_pin['path']==str(PACKAGE/'SOURCE_REVIEW_READY.json'),'exact package READY role')
    genuine(generation,'actual_Source_preparation_return',ready_pin,'ready_pin')
    need(ready['schema']=='CURRENT_B_COMPLETE_CAPTURE_SOURCE_REVIEW_READY_V1'and ready['source_only']is True and ready['Source_or_native_business_executed']is False and ready['original_caps']==CAPS,'actual READY Source-only schema')
    plan=meta(ready['control_plan_pin']);author_pin=pin_small(PACKAGE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');author=meta(author_pin)
    need(author['Source_only_frozen_before_Root_generation']is True and author['native_or_compiler_executed_by_author']is False and author['Source_preparer_or_publisher_executed_by_author']is False,'actual author Source freeze')
    need(ready['complete_source_file_pins']==author['whole_Source_file_pins'],'complete unselected author Source table exact')
    text={}
    for p in ready['complete_source_file_pins']:
        q=full(p)
        if q.suffix=='.py':ast.parse(q.read_bytes());text[q.name]=q.read_text()
    need(ready['host_source_pin']in ready['complete_source_file_pins']and ready['contract_Source_pin']in ready['complete_source_file_pins'],'host/contract frozen in complete Source table')
    need(plan['schema']=='CURRENT_B_COMPLETE_CAPTURE_SOURCE_ONLY_PLAN_V1'and plan['source_only']is True and plan['actual_business_preconditions_closed']is True and plan['source_role_pin_audit_complete']is True and plan['actual_B_build_role_keys_audited']is True and plan['original_caps']==CAPS,'complete actually bound plan')
    need(plan['Source_generation_science_bodies_decoded']is False and plan['Source_generation_native_executed']is False,'GEN did not decode or execute native')
    latest=meta(plan['latest_complete_plan_pin']);build=meta(plan['actual_B_IO_build_plan_pin']);host=meta(plan['actual_B_IO_build_Host_report_pin']);raw=meta(plan['actual_B_IO_build_Root_tools_pin']);post=meta(plan['actual_B_IO_build_post_pin']);posttools=meta(plan['actual_B_IO_build_post_tools_pin'])
    roots=plan['complete_joint_roots'];need(roots==latest['complete_joint_roots']+[str(OUT)]and len(roots)==len(set(roots))and not os.path.lexists(OUT),'exact whole latest prefix plus one fresh literal capture root')
    need(build['complete_joint_roots']==roots[:-1][:len(build['complete_joint_roots'])]and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y),'build prefix retained, no nested cumulative roots')
    genuine(raw,'actual_terminal_return',plan['actual_B_IO_build_Host_report_pin'],'report_pin');genuine(posttools,'actual_review_return',plan['actual_B_IO_build_post_pin'],'review_pin')
    need(raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False,'original build guard permission and no retry')
    need(host['schema']=='ACTUAL_B_IO_FOUR_COMPILE_ONE_LINK_QUALIFICATION_REPORT_V1'and host['status']=='ACTUAL_B_IO_BUILD_FIVE_STAGE0_CLOSED_ONLY'and host['failure']is None and host['control_plan_pin']==plan['actual_B_IO_build_plan_pin']and host['build_stage_count']==5 and host['final_report_resource_check_passed']is True and host['original_caps']==CAPS,'genuine build five-stage closure')
    need(post['schema']=='RECORDED_B_IO_FIVE_STAGE_BUILD_METADATA_POSTVERIFY_V1'and post['status']=='PASS_ACTUAL_B_IO_FOUR_COMPILE_ONE_LINK_STAGE0_METADATA_ONLY_NO_NATIVE_QUALIFICATION'and post['failure']is None and post['actual_Root_tools_pin']==plan['actual_B_IO_build_Root_tools_pin']and post['actual_Host_report_pin']==plan['actual_B_IO_build_Host_report_pin']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0 and post['actual_child_integer_exit_codes']==[0]*5 and all(type(v)is int for v in post['actual_child_integer_exit_codes']),'exact independent actual build post0')
    need(len(host['records'])==len(host['actual_watchdog_checks'])==len(build['exact_five_stage_commands'])==5,'five original actual stages')
    for record,watch,command in zip(host['records'],host['actual_watchdog_checks'],build['exact_five_stage_commands']):
        w=watch['actual_watchdog'];need(record['status']=='PASS'and record['command']==w['command']==command and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'actual five original child0 closures')
        need(watch['actual_stage_record_label']==record['label']and watch['actual_watchdog_pin']['path']==str(Path(build['planned_actual_output_root'])/(record['label']+'.watchdog.json'))and watch['actual_log_pin']['path']==str(Path(build['planned_actual_output_root'])/(record['label']+'.log'))and watch['actual_log_pin']['sha256']==record['log_sha256'],'record.label original exact monitor paths')
        need(meta(watch['actual_watchdog_pin'])==w,'actual saved watchdog equals Host')
        current(watch['actual_log_pin'])
    runtime=plan['new_IO_runtime_pin'];need(runtime==post['new_runtime_full_pin']and runtime in host['whole_new_output_pins']and runtime['path']==str(Path(build['planned_actual_output_root'])/'sources/runtime/Dragon'),'exact genuinely emitted new runtime')
    current(runtime)
    for p in host['whole_new_output_pins']:current(p)
    for key in('explicit_cumulative_metadata_file_pins','inherited_metadata_current7_pins','explicit_control_metadata_pins'):
        for p in plan[key]:current(p)
    for p in ready['dependencies']:current(p)
    for p in build['compile_and_link_input_pins']+build['original_SCI_current7_only_pins']+build['readonly_system_tool_metadata_pins']+build['readonly_system_SDK_header_pins']+build['current48_compressed_archive_pins']+build['prior_failed_B_partial_output_pins']:current(p)
    for p in build['exact_early14_retired_pins']+build['historical48_plain_full_pins']:need(not os.path.lexists(p['path']),'historical retired operands absent, never current-input recast')
    need(len(build['complete_joint_roots'])==68 and len(roots)==69,'this genuine build68 and complete capture69 observation, never count-only admission')
    need(plan['bounded_new_capture_output_reservation_bytes']==640*2**20 and plan['bounded_new_Source_metadata_reservation_bytes']==16*2**20 and plan['full_extraction_scope_deferred_not_reduced']is True and plan['historical_capture_reference_bytes']==569395111 and plan['historical_full_extraction_reference_bytes']==438863526 and plan['new_B_upper_size_forecast_claimed']is False,'full capture hard bound and separate later full extraction')
    seed=meta(plan['original_v10_seed_plan_pin']);io=meta(plan['original_B_IO_Source_metadata_plan_pin']);binding=plan['B_binding_template']
    need(seed['current_case_spec_pin']['sha256']=='fbe3362e16c19c93b87de2ebf67607c5ac0a579daa1f7af5891aae9c9faa7b16'and plan['original_v10_seed_plan_pin']['sha256']=='9bf2ba8444f0fe17989db3a31c373730da1d73bae564405c6ca71f5bc6c6579b','original B seed/CASE')
    need(plan['original_B_native_stage_inputs']==binding['original_B_native_stage_inputs']==seed['states']['B']['native_stage_inputs']==io['original_B_native_stage_inputs']and len(plan['original_B_native_stage_inputs'])==7,'all exact original B input rows')
    for row in plan['original_B_native_stage_inputs']:current(row['input_pin'])
    need(plan['actual_consumed_readonly_cwd_role_pins']==binding['actual_consumed_readonly_cwd_role_pins']==io['actual_consumed_readonly_cwd_role_pins'],'readonly old-cwd role table')
    for p in plan['actual_consumed_readonly_cwd_role_pins'].values():current(p)
    oldcwd=Path(binding['actual_native_cwd']);observed={p.name:identity(p.lstat())for p in oldcwd.iterdir()if p.name!='b63'}
    need(observed==plan['all_old_cwd_entries_current7_before_child'],'fresh full old-cwd current7 inventory')
    inverse=meta(author['Source_static_evidence_pin']);need(author['Source_static_evidence_pin']==plan['source_transfer_fix_whole_inverse_pin'],'same v2 actual inverse role')
    failed=meta(inverse['original_failed_Source_generation_true_tools_pin']);ft=failed['actual_Source_preparation_return']
    need(failed['observed_closed']is True and type(failed['original_integer_exit_code'])is int and failed['original_integer_exit_code']==1 and type(ft['exit_code'])is int and ft['exit_code']==1 and ft.get('session_id')is None and "NameError: name 'bm' is not defined"in ft['output'],'original genuine v1 GEN1 data-passing failure preserved')
    for row in inverse['whole_Source_copy_rows']:
        left=full(row['original_Source_pin']);right=full(row['new_Source_pin']);before=left.read_bytes();after=right.read_bytes()
        if right.name=='capture_Source_contract.UNREADY.py':
            restored=after.replace(b' return build,bm\ndef admit(packet):',b' return build\ndef admit(packet):',1).replace(b' build,bm=admit_build(packet);latest=',b' build=admit_build(packet);latest=',1)
            need(restored==before,'whole contract exact two-literal inverse; return and caller unpack bm')
        else:need(before==after,'all other v2 Source whole unchanged')
    need(' return build,bm\ndef admit(packet):'in text['capture_Source_contract.UNREADY.py']and 'build,bm=admit_build(packet)'in text['capture_Source_contract.UNREADY.py'],'both actual bm return/unpack edges corrected')
    proof=meta(pin_small(PACKAGE.with_name('current_B_complete_capture_host_source_v1_UNREADY')/'SOURCE_ONLY_AST_AND_WHOLE_COPY_INVERSE_EVIDENCE.json'))
    for row in proof['whole_Source_copies']:
        left=full(row['original_Source_pin']);right=full(row['candidate_Source_pin']);need(left.read_bytes()==right.read_bytes(),'whole original core/launcher/deck bytes')
    oldhelper=PACKAGE.parent/'current_extra_reaction_source_v2/B_only_observer_IO_source_v1/B_original_input_binding.UNREADY.py';oldtext=oldhelper.read_text();full(pin_small(oldhelper));oldfunc=functions(oldtext);newfunc=functions(text['B_original_input_binding.UNREADY.py'])
    for name in proof['binding_helper_whole_unchanged_functions']:need(oldfunc[name]==newfunc[name],'whole unchanged route helper function '+name)
    hosttext=text['run_guarded_current_B_complete_capture.UNREADY.py'];need(hosttext.index("with claim.open('x')")<hosttext.index("sf,psf=frozen_arg")<hosttext.index('spec=importlib.util.spec_from_file_location'),'exclusive Root claim before metadata EOF/import')
    need("(m.OUT/'B_capture').mkdir()"in hosttext and "wp=m.OUT/(record['label']+'.watchdog.json')"in hosttext and "lp=m.OUT/(record['label']+'.log')"in hosttext,'case journal parent and original record.label paths')
    launcher=text['exec_original_B_in_fresh_IO.UNREADY.py'];need("os.getppid()==args.expected_parent_pid"in launcher and "os.execve(runtime['path'],[runtime['path']],env)"in launcher and 'subprocess'not in launcher,'one original direct child, same PID native exec')
    need('640*2**20'in text['capture_Source_contract.UNREADY.py']and 'own<m.CAPTURE_BOUND'in hosttext and 'prospective+m.CAPTURE_BOUND+m.SOURCE_BOUND<2*2**30'in hosttext,'full capture640 hard bound and original prospective cumulative2GiB')
    pub=text['publish_current_B_capture_CLI.UNREADY.py'];need("('review-pin','review-tools-pin','generation-tools-pin')"in pub and "review['status']=='PASS_SOURCE_ONLY_CURRENT_B_COMPLETE_CAPTURE'"in pub and "m.need(len(argv)==24"in pub and "Root_actual_exec_command_sandbox_permissions_required='require_escalated'"in pub,'actual publisher schema/three PF args/24argv/permission contract')
    need(all(plan[k]is False for k in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete','compiled_IO_semantics_qualified','B_full_extraction_completed','B_six_phase_construction_completed','B_OVERV_control_completed')),'no native/extraction/physics/AAA/ABA qualification minted')
    for p in list(FULL.values()):full(p)
    for p in list(CURRENT.values()):current(p)
    report=dict(schema='INDEPENDENT_CURRENT_B_COMPLETE_CAPTURE_FROZEN_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_B_COMPLETE_CAPTURE',failure=None,source_only=True,metadata_only=True,control_plan_pin=ready['control_plan_pin'],complete_source_file_pins=ready['complete_source_file_pins'],Root_Source_generation_tools_pin=gen_pin,Root_Source_generation_READY_pin=ready_pin,author_Source_freeze_pin=author_pin,actual_B_IO_build_Root_tools_pin=plan['actual_B_IO_build_Root_tools_pin'],actual_B_IO_build_Host_report_pin=plan['actual_B_IO_build_Host_report_pin'],actual_B_IO_build_post_pin=plan['actual_B_IO_build_post_pin'],new_runtime_current7_only_pin=runtime,complete_joint_roots=roots,whole_small_Source_and_metadata_twice_pins=list(FULL.values()),nondecoding_current7_only_pins=[p for k,p in CURRENT.items()if k not in FULL],historical_deck_seed_role_not_live_current7=True,original_caps=CAPS,helper_imported=False,compiler_or_native_executed=False,Source_preparer_or_publisher_executed=False,scientific_body_opened_hashed_or_decoded=False,full_extraction_scope_deferred_not_reduced=True,entire_capture_hard_bound_bytes=640*2**20,reviewer_Source_pin=pin_small(Path(__file__).absolute()),elapsed_seconds=time.monotonic()-START,**FALSE)
    raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'Source review report6MiB')
    with (BASE/'REVIEW.json').open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    budget();print(json.dumps(dict(status=report['status'],review_pin=pin_small(BASE/'REVIEW.json'),small_Source_metadata_count=len(FULL),current7_only_count=len(CURRENT)-len(FULL))),flush=True)

if __name__=='__main__':main()
