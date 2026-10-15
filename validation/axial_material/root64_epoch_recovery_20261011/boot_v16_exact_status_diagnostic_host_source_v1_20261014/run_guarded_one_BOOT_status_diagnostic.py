#!/usr/bin/env python3
"""Guarded compile68/link70/one BOOT diagnostic. No GLOBAL/PROJECT/full50 rerun."""
import argparse,hashlib,importlib.util,json,os,shutil,stat,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
HERE=Path(__file__).absolute().parent
PLAN=HERE/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json'
OUT=R/'validation/artifacts/axial-material-new-one-BOOT-exact-status-diagnostic-20261014-v1'
WORK=OUT/'AAA'
ALIAS_ROOT=R/'validation/artifacts/axial-material-bi-261014-v1'
COMMON=REC/'post_curated66_current_catalog_common_source_v2_20261013/guarded_warm_A_common.py'
COMMON_SHA='a5b774a6b62e229f8f6360a284354e2f0af8ff3860602b061de376b2624fc040'
MI=2**20
HF_SCHEMA='COMPLETE_GUARDED_ONE_BOOT_EXACT_STATUS_DIAGNOSTIC_HOST_SOURCE_ONLY_FREEZE_V1'
SF_SCHEMA='COMPLETE_BOOT_EXACT_RETURN_STATUS_DIAGNOSTIC_FORTRAN_SOURCE_ONLY_FREEZE_V1'

# The exact original guard helpers and physical classifier are appended by the
# Source-only authoring step, without importing a candidate or running a child.

def alias_identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def borrowed_alias_inventory(rows,expected=None):
    state=ALIAS_ROOT.lstat()
    if not stat.S_ISDIR(state.st_mode)or state.st_uid!=os.getuid():raise RuntimeError('exclusive ordinary borrowed alias namespace')
    fd=os.open(ALIAS_ROOT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        if alias_identity(os.fstat(fd))!=alias_identity(state):raise RuntimeError('alias root opened7 changed')
        names=sorted(e.name for e in os.scandir(fd))
        if names!=sorted(row['short_name']for row in rows):raise RuntimeError('only nine literal borrowed links allowed')
        found=[]
        for row in rows:
            p=ALIAS_ROOT/row['short_name'];z=os.stat(row['short_name'],dir_fd=fd,follow_symlinks=False)
            text=os.readlink(row['short_name'],dir_fd=fd);target=Path(text);st=target.lstat()
            if not stat.S_ISLNK(z.st_mode)or z.st_nlink!=1 or z.st_uid!=os.getuid()or text!=row['target_pin']['path']or \
               not stat.S_ISREG(st.st_mode)or alias_identity(st)!=row['target_pin']['identity']or st.st_nlink!=1 or st.st_uid!=os.getuid():raise RuntimeError('literal borrowed link and immutable real readonly target changed')
            found.append(dict(short_path=str(p),link_identity=alias_identity(z),link_text=text,target_pin=row['target_pin']))
        if alias_identity(os.fstat(fd))!=alias_identity(state)or alias_identity(ALIAS_ROOT.lstat())!=alias_identity(state):raise RuntimeError('alias namespace after7 changed')
    finally:os.close(fd)
    actual=dict(root_identity=alias_identity(state),links=found,symlink_metadata_bytes=sum(r['link_identity'][4]for r in found))
    if expected is not None and actual!=expected:raise RuntimeError('borrowed alias ownUID/readlink/stat7 changed')
    return actual

class DiagnosticResources:
    def __init__(self,phase,rows,aliases):self.phase=phase;self.rows=rows;self.aliases=aliases
    def check(self):
        r=self.phase.check();a=borrowed_alias_inventory(self.rows,self.aliases);n=a['symlink_metadata_bytes']
        # Count the nine borrowed-link metadata bytes independently; no fresh
        # subtraction or skipped own output. Original classifier stays exact.
        if r['storage_inventory']['aux_bytes']+n+self.phase.pending_publication_reserved_bytes>128*MI or \
           r['storage_inventory']['inventory_bytes']+n+self.phase.pending_publication_reserved_bytes>=2*2**30:raise RuntimeError('original auxiliary128 and totalfresh2 including borrowed links')
        return dict(r,borrowed_alias_metadata=a)

def genuine_terminal(d,required):
    keys=[k for k in ('actual_terminal_return','actual_execute_return','actual_release_return')if k in d]
    if not keys or any(d[k]!=d[keys[0]]for k in keys):raise RuntimeError('one genuine terminal object, all named copies agree')
    a=d[keys[0]]
    if type(a['exit_code'])is not int or a['exit_code']!=required or a.get('session_id')is not None or d['observed_closed']is not True:raise RuntimeError('genuine closed integer Root terminal')
    return a

def make_commands(c,base,plan,source):
    old=list(base['actual_complete70_link_inputs']);last=base['records'][1]['command'];first=base['records'][0]['command']
    if len(old)!=70 or len(set(old))!=70 or last!=[first[0],'-O2','-ffp-contract=off',*old,'-o',plan['base_Dragon_pin']['path']]or \
       old!=[p['path']for p in plan['current_ordered70_input_pins']]or old[37]!=plan['retained_Driver37_pin']['path']or \
       old[40]!=plan['retained_BOOTQ40_pin']['path']or old[57]!=plan['retained_math57_pin']['path']or \
       Path(old[68]).name!='SPOBOOX64.o'or [p for p in old if p.endswith('.a')]!=[p['path']for p in plan['original_four_archive_pins']]:raise RuntimeError('exact current Driver2 ordered70/37/40/57/four archives')
    if c.FLAGS!=plan['original_compile_flags']or first[0]!=plan['original_compiler_pin']['path']or \
       [v for v in first if v.startswith('-I')]!=plan['original_compile_include_arguments']:raise RuntimeError('original exact compiler/flags/include order')
    obj=str(OUT/'build/SPOBOOX64.o');new=list(old);new[68]=obj
    if [i for i,(x,y)in enumerate(zip(old,new))if x!=y]!=[68]:raise RuntimeError('only object68 may be replaced')
    compile_cmd=[first[0],*c.FLAGS,'-I'+str(OUT/'build'),*plan['original_compile_include_arguments'],'-J'+str(OUT/'build'),'-c',source['path'],'-o',obj]
    link_cmd=[*last[:3],*new,'-o',str(OUT/'runtime/Dragon')]
    return [compile_cmd,link_cmd,[str(OUT/'runtime/Dragon')]],new

def read_BOOT_outcome(c,runner,expected_error,expected_tb):
    record=runner.records[-1];wp=c.pin(WORK/'BOOT_diagnostic.watchdog.json');lp=c.pin(WORK/'BOOT_diagnostic.log')
    w=json.loads(Path(wp['path']).read_text());text=Path(lp['path']).read_text();rows=[]
    for line in text.splitlines():
        if len(line)>65536:raise RuntimeError('bounded actual diagnostic JSON/log line')
        if line.strip().startswith('{')and line.strip().endswith('}'):
            row=json.loads(line)
            if isinstance(row,dict):rows.append(row)
    if w['command']!=record['command']or w['rss_cap_mib']!=512 or w['own_child_only']is not True or w['liveness_group_cleanup']is not True or \
       w['limit_failure']is not None or not 0<=w['sampled_peak_rss_mib']<512 or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 or type(w['returncode'])is not int:raise RuntimeError('true own-child closed BOOT watch with unchanged caps')
    diagnostics=[r for r in rows if r.get('schema')=='ACTUAL_BOOT_EXACT_FAILURE_STATUS_DIAGNOSTIC_V1']
    seals=[r for r in rows if r.get('schema')=='ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1']
    if w['returncode']==1:
        if expected_error is None or str(expected_error)!='own-child stage failed; no retry'or record['status']!='FAILED'or \
           text.count('SPOBOOX64: ACTUAL STRICT SOLVE NOT COMMITTED.')!=1 or len(diagnostics)!=1 or seals or 'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE'in text:raise RuntimeError('only exact original strict BOOT abort1 is diagnostic, never PASS')
        row=diagnostics[0]
        if type(row.get('boot_plane'))is not int or row['boot_plane']not in(1,2,3)or type(row.get('actual_return_status'))is not int or row['actual_return_status']not in range(1,8)or row.get('required_committed_status')!=8:raise RuntimeError('exact true failure plane/status1..7')
        return dict(kind='REAL_ORIGINAL_BOOT_ABORT1_DIAGNOSTIC_ONLY',actual_exit_code=1,actual_failed_record_preserved=True,actual_diagnostic=row,actual_log_pin=lp,actual_watchdog_pin=wp,original_expected_child_error_repr=repr(expected_error),original_expected_child_traceback_preserved=True,engineering_qualified=False),None
    if w['returncode']!=0 or expected_error is not None or record['status']!='PASS'or diagnostics or len(seals)!=1 or \
       seals[0].get('status')!='PASS'or seals[0].get('all_payload_bits_equal')is not True or seals[0].get('complete_lifecycle_checked')is not True or \
       (seals[0].get('groups'),seals[0].get('planes'),seals[0].get('epoch'))!=(370,3,0)or 'normal end of execution'not in text or 'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE'not in text:
        if expected_error is not None:raise expected_error.with_traceback(expected_tb)
        raise RuntimeError('actual status8 path requires original genuine full seal/readback, no promotion from missing diagnostic')
    return dict(kind='REAL_ORIGINAL_SINGLE_BOOT_SEAL_READBACK0_ONLY',actual_exit_code=0,actual_Fortran_complete_copy_readback=seals[0],actual_log_pin=lp,actual_watchdog_pin=wp,engineering_qualified=False),seals[0]

def main():
    p=argparse.ArgumentParser(allow_abbrev=False)
    for prefix in ('driver-build','v16-failure','diag-source-freeze','host-freeze','literal3-release','literal3-Root-tools'):
        for suffix in ('summary','sha256','seven-id'):p.add_argument('--'+prefix+'-'+suffix,required=True)
    a=p.parse_args();start=time.monotonic();c=load_common()
    def load(prefix):
        name=prefix.replace('-','_');return c.load_json_exact(getattr(a,name+'_summary'),getattr(a,name+'_sha256'),getattr(a,name+'_seven_id'))
    hf,phf=load('host-freeze');deps=unique(hf['dependencies']);dt={r['path']:r for r in deps}
    if hf['schema']!=HF_SCHEMA or hf['compiler_executed']is not False or hf['numerical_executed']is not False or hf['host_source']['path']!=str(Path(__file__).absolute()):raise RuntimeError('exact own Source-only diagnostic HF')
    c.same_pin(__file__,hf['host_source']);c.verify_rows(deps)
    pp=hf['diagnostic_host_plan_pin'];plan=c.load_json_exact(pp['path'],pp['sha256'],json.dumps(pp['identity']))[0]
    if pp['path']!=str(PLAN)or dt.get(str(PLAN))!=pp or plan['source_only']is not True or plan['planned_output_root']!=str(OUT)or \
       plan['borrowed_alias_root']!=str(ALIAS_ROOT)or any(plan[k]is not None for k in ('future_actual_object_pin','future_actual_Dragon_pin','future_actual_BOOT_report_pin')):raise RuntimeError('Source plan has no fake actuals or substituted output/input alias namespace')
    selected=('selected_Driver2_Host_freeze_pin','selected_diag_Fortran_Source_freeze_pin','selected_closed_v16_Host_freeze_pin','selected_closed_v16_Root_tool_pin','selected_closed_v16_actual_post_review_pin','selected_closed_v16_actual_post_tools_pin','selected_literal3_actual_release_pin','selected_literal3_actual_Root_tool_pin')
    for k in selected:
        if not isinstance(hf[k],dict)or dt.get(hf[k]['path'])!=hf[k]:raise RuntimeError('all selected actual authorities in ownHF dependencies')
    base,pbase=load('driver-build');v16,pv16=load('v16-failure');sf,psf=load('diag-source-freeze');release,pr=load('literal3-release');rt,prt=load('literal3-Root-tools')
    if pbase!=plan['actual_Driver2_report_pin']or pv16!=plan['actual_closed_v16_report_pin']or pr!=hf['selected_literal3_actual_release_pin']or prt!=hf['selected_literal3_actual_Root_tool_pin']:raise RuntimeError('exact selected reports and real release authorities')
    genuine_terminal(rt,0)
    if release['status']!='EXACT_LITERAL3_CLOSED_FAILED_V15_PRIVATE_OLD_PRIVATE_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED'or release['deleted_files']!=3 or release['logical_bytes_released']!=1504027360 or release['original_budget_after']['original_initial_reserve_admitted']is not True:raise RuntimeError('literal3 actualclosed0 release and original reserve required before diagnostic')
    for row in plan['released_only_old_v15_literal3_pins']:
        if os.path.lexists(row['path']):raise RuntimeError('exact retired old-v15 literal3 remain absent')
    if base['schema']!='ACTUAL_NATIVE_RANK1_CACHE336_DRIVER_COMPLETE70_BUILD_ONLY_V1'or base['status']!='ACTUAL_ONE_CACHE336_DRIVER_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'or base['failure']is not None or base['after_check_error']is not None or base['Dragon_linked']is not True or base['final_report_resource_check_passed']is not True or base['actual_host_Source_freeze_pin']!=hf['selected_Driver2_Host_freeze_pin']:raise RuntimeError('genuine current Driver2 closedcompile/link runtime')
    post=c.load_json_exact(hf['selected_closed_v16_actual_post_review_pin']['path'],hf['selected_closed_v16_actual_post_review_pin']['sha256'],json.dumps(hf['selected_closed_v16_actual_post_review_pin']['identity']))[0]
    roottool=c.load_json_exact(hf['selected_closed_v16_Root_tool_pin']['path'],hf['selected_closed_v16_Root_tool_pin']['sha256'],json.dumps(hf['selected_closed_v16_Root_tool_pin']['identity']))[0];genuine_terminal(roottool,1)
    pt=c.load_json_exact(hf['selected_closed_v16_actual_post_tools_pin']['path'],hf['selected_closed_v16_actual_post_tools_pin']['sha256'],json.dumps(hf['selected_closed_v16_actual_post_tools_pin']['identity']))[0];pa=pt['actual_review_return']
    if pt['observed_closed']is not True or type(pa['exit_code'])is not int or pa['exit_code']!=0 or pa.get('session_id')is not None or json.loads(pa['output'].strip().splitlines()[-1])['review_pin']!=hf['selected_closed_v16_actual_post_review_pin']or post['actual_report_pin']!=pv16 or post['actual_Host_freeze_pin']!=hf['selected_closed_v16_Host_freeze_pin']or post['actual_Root_true_tool_return_pin']!=hf['selected_closed_v16_Root_tool_pin']or post['actual_stage_count']!=50 or post['actual_positive_count']!=16 or post['actual_exact_refusal_count']!=33 or post['actual_unexpected_failed_record_indices']!=[49]or post['actual_engineering_three_plane_closed0']is not False:raise RuntimeError('genuine v16 failedBOOT-only context post0, not engineering')
    if v16['status']!='FAILED_UNQUALIFIED_NO_RETRY'or v16['engineering_three_plane_closed0']is not False or v16['failure']!=post['failure']or v16['actual_terminal']is not None:raise RuntimeError('closed v16 remains unqualified')
    if psf!=hf['selected_diag_Fortran_Source_freeze_pin']or psf['path']!=plan['selected_diag_Fortran_Source_freeze_path']or sf['schema']!=SF_SCHEMA or sf['source_only']is not True or sf['compiled']is not False or sf['numerical_executed']is not False or sf['public_subroutine_ABI_unchanged']is not True or sf['mathematics_conditions_thresholds_and_success_commit_order_unchanged']is not True or sf['failure_only_stdout_plane_and_status']is not True or sf['replacement_zero_based_link_index']!=68 or sf['diagnostic_source_pin']!=plan['diagnostic_Source_pin']:raise RuntimeError('failure-only diagnostic Source, ABI/math/commit order unchanged')
    sfrows=unique(sf['files']+[sf['diagnostic_source_pin'],sf['original_source_pin'],sf['complete_byte_inverse_pin'],sf['diagnostic_plan_pin']]);c.verify_rows(sfrows)
    binding,fixed,support,helper,full,base_resources,before=c.initialize(OUT,start)
    caps=dict(original_stage_wall_cap_seconds=600,whole_wall_cap_seconds=1800,SELF_and_each_own_child_RSS_cap_bytes=512*2**20,threads=1,children_at_once=1,retries=0,fresh_output_cap_bytes=2*2**30,history_cap_bytes=96*2**30,filesystem_floor_bytes=8*2**30,original_cold_reserve_bytes=20971764748)
    if caps!=plan['original_caps']or any(binding[k]!=v for k,v in caps.items())or before['artifact_bytes']+20971764748+64*MI+2*2**30>=96*2**30:raise RuntimeError('original caps and actual initial fullfresh2 reserve')
    c.closed_report(base,helper,Path(pbase['path']).parent,2)
    inputs=plan['borrowed_readonly_input_rows'];live={r['path']:r for r in unique(v16['fixed_current_pins']+v16['output_pins'])}
    if len(inputs)!=9 or len({r['short_name']for r in inputs})!=9 or any(live.get(r['target_pin']['path'])!=r['target_pin']or len(str(ALIAS_ROOT/r['short_name']))>72 for r in inputs):raise RuntimeError('nine actual readonly v16 PFs, each exact short CLE path≤72')
    planned,new70=make_commands(c,base,plan,sf['diagnostic_source_pin']);old70=plan['current_ordered70_input_pins'];old9=plan['current_nine_core_object_pins']
    fixed=unique(fixed+[phf,hf['host_source'],pp,pbase,pv16,psf,pr,prt]+deps+sfrows+base['fixed_current_pins']+base['output_pins']+v16['fixed_current_pins']+v16['output_pins']+old70+old9+[r['target_pin']for r in inputs]);c.verify_rows(fixed)
    if ALIAS_ROOT.exists()or ALIAS_ROOT.is_symlink():raise RuntimeError('one new borrowed alias namespace, no reuse/retry')
    OUT.mkdir();(OUT/'build').mkdir();(OUT/'runtime').mkdir();WORK.mkdir();ALIAS_ROOT.mkdir()
    afd=os.open(ALIAS_ROOT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        for row in inputs:os.symlink(row['target_pin']['path'],row['short_name'],dir_fd=afd)
        os.fsync(afd)
    finally:os.close(afd)
    aliases=borrowed_alias_inventory(inputs)
    shutil.copy2(support.BOUNDED,OUT/'runtime/run_bounded_dragon.py');owned=[c.pin(OUT/'runtime/run_bounded_dragon.py')]
    phase=PhaseResources(base_resources);phase.phase='build';resources=DiagnosticResources(phase,inputs,aliases)
    runner=full.OwnRSSSerialExecutor(OUT,1800-(time.monotonic()-start),'one-BOOT-diagnostic',resources)
    if type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources or Path(runner.bounded.__file__).resolve()!=OUT/'runtime/run_bounded_dragon.py':raise RuntimeError('original OwnRSS supervisor/MRO/guard')
    deck=WORK/'BOOT_diagnostic.x2m';deck.write_text(plan['exact_BOOT_deck']);owned.append(c.pin(deck));first=FirstFatal();after=None;outcome=None;seal=None;watches=[]
    def check():
        c.check_full_current(fixed,owned);borrowed_alias_inventory(inputs,aliases)
        if not 0<time.monotonic()-start<1800:raise RuntimeError('original whole1800 includes final publication')
        return resources.check()
    try:
        for label,command in zip(('compile_BOOT_diagnostic','link_Dragon'),planned[:2]):
            check();runner.execute(OUT/'build',label,command,600);watches.append(helper.check_watch(OUT,runner.records[-1]))
            if label=='compile_BOOT_diagnostic':
                names=sorted(['SPOBOOX64.o','compile_BOOT_diagnostic.log','compile_BOOT_diagnostic.watchdog.json'])
                if sorted(p.name for p in (OUT/'build').iterdir())!=names:raise RuntimeError('one object+compile log/watch; no MODULE/other outputs')
                for name in names:
                    p=OUT/'build'/name;s=p.lstat()
                    if not stat.S_ISREG(s.st_mode)or s.st_nlink!=1 or s.st_uid!=os.getuid():raise RuntimeError('ordinary compile outputs owned UID/nlink1')
                    c.pin(p)
                owned.append(c.pin(OUT/'build/SPOBOOX64.o'))
            else:owned.append(c.pin(OUT/'runtime/Dragon'))
            after=check()
        phase.phase='BOOT';check();expected=None;tb=None
        try:runner.execute(WORK,'BOOT_diagnostic',planned[2],600,deck=deck.name)
        except RuntimeError as exc:expected=exc;tb=exc.__traceback__
        outcome,seal=read_BOOT_outcome(c,runner,expected,tb)
        if seal is not None:
            hp=plan['readonly_pair_helper_pin'];c.same_pin(hp['path'],hp);spec=importlib.util.spec_from_file_location('known_readonly_BOOT_pair_helper',hp['path']);data=importlib.util.module_from_spec(spec);spec.loader.exec_module(data)
            terminal=data.final_readback(WORK/'closed_boot_axial.xsm',WORK/'closed_boot_archive.xsm');outcome['complete_terminal_readback']=terminal
            owned.extend(c.pin(WORK/n)for n in('closed_boot_axial.xsm','closed_boot_archive.xsm'))
        after=check();c.verify_rows(old70+old9)
    except BaseException as exc:first.capture(exc,'compile_link_or_single_BOOT')
    try:after=check()
    except BaseException as exc:first.capture(exc,'after_original_resource_check')
    good=first.error is None and outcome is not None and len(runner.records)==3 and [r['status']for r in runner.records[:2]]==['PASS','PASS']
    target=OUT/'Root_actual_one_BOOT_status_diagnostic_summary.json';summary=None
    try:
        phase.pending_publication_reserved_bytes=8*MI
        summary=dict(schema='ACTUAL_GUARDED_ONE_BOOT_RETURN_STATUS_DIAGNOSTIC_V1',status=('ACTUAL_ONE_BOOT_FAILURE_STATUS_DIAGNOSTIC_CLOSED_ONLY'if outcome and outcome['actual_exit_code']==1 else'ACTUAL_ONE_BOOT_ORIGINAL_SEAL_READBACK_CLOSED_ONLY')if good else'FAILED_DIAGNOSTIC_UNQUALIFIED',failure=None if first.error is None else repr(first.error),first_failure_secondary_errors=list(first.secondary),records=runner.records,fixed_current_pins=fixed,output_pins=[c.pin(p)for p in sorted(OUT.rglob('*'))if p.is_file()],owned_runtime_pins=owned,borrowed_readonly_alias_identity_facts=aliases,borrowed_inputs_never_copied_or_hardlinked=True,actual_outcome=outcome,actual_host_Source_freeze_pin=phf,actual_diagnostic_Fortran_Source_freeze_pin=psf,original_actual_Driver2_report_pin=pbase,actual_closed_v16_context_report_pin=pv16,required_literal3_actual_release_pin=pr,actual_commands=planned,actual_ordered70_link_inputs=new70,replacement_zero_based_link_index=68,other69_current_Driver37_BOOTQ40_math57_and_four_archives_unchanged=True,current_all9_core_objects_unchanged=True,actual_watchdog_checks=watches,original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,original_caps=caps,resources_before=before,resources_after=after,SELF_peak_bytes=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-start,final_report_resource_check_passed=False,full50_executed=False,GLOBAL_or_PROJECT_reexecuted=False,expected_child_failure_record_never_changed_to_PASS=True,engineering_qualified=False,AAA_qualified=False,ABA_admitted=False,physics_qualified=False,goal_complete=False)
        c.write(target,summary);phase.pending_publication_reserved_bytes=0;summary['resources_after_including_summary_bytes']=check();summary['final_report_resource_check_passed']=True;rewrite_summary(c,target,c.pin(target),summary);check()
    except BaseException as exc:
        first.capture(exc,'summary_publication_or_final_check')
        try:
            if summary is not None:
                summary.update(status='FAILED_DIAGNOSTIC_UNQUALIFIED',failure=repr(first.error),first_failure_secondary_errors=list(first.secondary),final_report_resource_check_passed=False)
                if target.exists():rewrite_summary(c,target,c.pin(target),summary)
        except BaseException as later:first.capture(later,'failed_summary_publication')
    first.reraise()
    if not good:raise RuntimeError('incomplete guarded three-stage diagnostic; no retry')

if __name__=='__main__':main()
