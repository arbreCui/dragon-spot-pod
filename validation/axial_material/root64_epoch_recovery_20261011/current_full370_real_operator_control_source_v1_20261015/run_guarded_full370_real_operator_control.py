"""Original OwnRSSSerialExecutor; one child, no compiler, retry or cleanup."""
import argparse, json, os, resource, shutil, sys, time
from pathlib import Path
import control_source_common as c

def rewrite_owned_summary(path,previous,value):
    c.current(previous)
    c.require(c.pin(path)==previous,'own summary bytes before finalization')
    fd=os.open(path,os.O_WRONLY|os.O_NOFOLLOW)
    try:
        c.require(c.identity(os.fstat(fd))==previous['identity'],'own summary opened7')
        with os.fdopen(fd,'w',encoding='utf-8') as f:
            fd=None;f.seek(0);f.truncate(0)
            json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    finally:
        if fd is not None:os.close(fd)
    c.require(c.identity(Path(path).lstat())[:4]==previous['identity'][:4],'own summary physical role')

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    for role in ('source-freeze','host-freeze'):
        for suffix in ('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
    args=ap.parse_args();started=time.monotonic()
    def argument(role):
        key=role.replace('-','_');q=Path(getattr(args,key+'_summary'))
        p=dict(path=str(q),sha256=getattr(args,key+'_sha256'),size_bytes=q.lstat().st_size,
            identity=json.loads(getattr(args,key+'_seven_id')))
        return c.read(p),p
    sf,sp=argument('source-freeze');hf,hp=argument('host-freeze')
    c.require(sf['schema']=='COMPLETE_FULL370_REAL_OPERATOR_CONTROL_SOURCE_ONLY_FREEZE_V1'
        and hf['schema']=='COMPLETE_FULL370_REAL_OPERATOR_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1'
        and sf['source_only'] is True and hf['source_only'] is True and hf['selected_source_freeze_pin']==sp
        and sf['original_caps']==c.CAPS and hf['original_caps']==c.CAPS
        and hf['host_source_pin']['path']==str(Path(__file__).absolute()), 'exact current Source-only host/caps')
    plan=c.read(sf['control_plan_pin']);c.check_finite(plan);out=Path(plan['planned_actual_output_root'])
    c.require(out==c.OUT and not os.path.lexists(out), 'fresh actual control namespace, zero retry')
    common=c.load(plan['original_Common_Source_pin'],'full_operator_original_common')
    support=c.load(plan['original_support_Source_pin'],'full_operator_original_support')
    c.require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None
        and all(os.environ.get(k)=='1' for k in c.THREADS) and Path(sys.executable).resolve()==support.PYTHON,
        'original singlethread unprofiled unoptimized Python')
    helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'full_operator_original_helper')
    factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'full_operator_original_resource_factory')
    full,production=helper.modules();guard_files=helper.guard_admission(full)
    c.require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)
        and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,
        'genuine original owning guard Source/MRO')
    fixed=c.unique(hf['dependencies']+[sp,hp]+[c.pin(p) for p in guard_files])
    science={p['path'] for p in plan['scientific_input_current7_pins']}
    # The actual parent performs exactly one whole-file hash for each science
    # input. Further parent checks are current7; the child verifies selected
    # original record words, plus the unchanged original ray parser's SHA.
    for p in fixed:
        c.current(p)
        if p['path'] not in science:c.require(c.pin(p['path'])==p,'complete Source/metadata dependency')
    for p in plan['scientific_input_current7_pins']:
        c.require(c.pin(p['path'])==p,'actual parent initial science fullEOF/SHA/7')
    roots=plan['complete_joint_roots']
    c.require(len(roots)==len(set(roots)) and all(not Path(a).is_relative_to(Path(b))
        for a in roots for b in roots if a!=b), 'inherited complete disjoint cumulative roots')
    joined=production.DiskResources(c.R/'validation',roots,8*2**30,2*2**30)
    history=factory.DynamicHistoryResources(c.ART,factory.history_roots([str(out)],c.ART),
        8*2**30,96*2**30,production.ResourceFailure)
    class Resources:
        def check(self):
            peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
            c.require(peak<512*2**20 and time.monotonic()-started<1800,'original SELF512/host1800')
            h=history.check();f=joined.check();extra=0
            for p in plan['explicit_cumulative_metadata_file_pins']:
                c.current(p)
                if not any(Path(p['path']).is_relative_to(Path(root)) for root in roots):extra+=p['size_bytes']
            c.require(h['artifact_bytes']+20971764748+64*2**20<96*2**30
                and f['artifact_bytes']+extra<2*2**30
                and f['disk_free_bytes']-20971764748-2*2**30>=8*2**30,
                'unchanged cumulative2/history96/cold/meta/free8 caps')
            return dict(original_history=h,complete_joint=f,explicit_external_metadata_bytes=extra,
                host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-started)
    resources=Resources();before=resources.check()
    c.require(before['original_history']['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,
        'original complete-family fullfresh2/cold/meta reservation')
    # Uncompressed current white-cache payload, complete outputs and compact
    # receipts are reserved before the one child; no partial-cache retry.
    c.require(before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']
        +plan['new_control_reserved_bytes']<2*2**30,'room for complete cache/control within same cumulative2')
    out.mkdir();(out/'runtime').mkdir();(out/'control').mkdir();(out/'operator-control').mkdir()
    shutil.copy2(support.BOUNDED,out/'runtime/run_bounded_dragon.py')
    runtime=c.pin(out/'runtime/run_bounded_dragon.py')
    c.require(runtime['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original bounded copy')
    runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-started),'operator-control',resources)
    c.require(type(runner) is full.OwnRSSSerialExecutor and runner.resources is resources
        and Path(runner.bounded.__file__).resolve()==out/'runtime/run_bounded_dragon.py','one actual owning runner')
    def check_all():
        for p in fixed:
            c.current(p)
            if p['path'] not in science:c.require(c.pin(p['path'])==p,'Source/metadata unchanged')
        c.require(c.pin(runtime['path'])==runtime,'owned bounded copy unchanged')
        return resources.check()
    command=[str(support.PYTHON),'-B',plan['worker_source_pin']['path'],'--plan-pin',
        json.dumps(sf['control_plan_pin'],separators=(',',':')),'--report',
        str(out/'control/ACTUAL_FULL370_REAL_OPERATOR_CONTROL.json'),'--expected-parent-pid',str(os.getpid())]
    failure=None;after_error=None;watches=[];actual=None;after=None
    try:
        check_all();runner.execute(out/'control','full370_real_operator',command,600)
        watches.append(helper.check_watch(out,runner.records[-1]));check_all()
        rp=c.pin(out/'control/ACTUAL_FULL370_REAL_OPERATOR_CONTROL.json');result=c.read(rp)
        c.require(result['passed'] is True and result['all_control_assertions_passed'] is True
            and result['white_preparation_actions']==181824 and result['transport_action_calls']==363648
            and result['prepare_white_calls']==1 and result['apply_calls']==1
            and result['complete_original_tracks']==11364 and result['groups']==370
            and result['axial_cells']==48 and result['retained_moments']==9
            and len(result['complete_white_cache_pins'])==370 and len(runner.records)==1
            and runner.records[0]['status']=='PASS','one actual complete current operator control')
        actual=dict(actual_control_report_pin=rp,all_one_stage_PASS=True,
            actual_kernel_origin_pin=result['actual_kernel_origin_pin'],
            actual_kernel_library_pin=result['actual_kernel_library_pin'],
            actual_kernel_build_report_pin=result['actual_kernel_build_report_pin'],
            complete_kernel_source_pins=result['complete_kernel_source_pins'],**c.FALSE)
    except BaseException as error:failure=repr(error)
    try:after=check_all()
    except BaseException as error:after_error=repr(error)
    good=failure is None and after_error is None and actual is not None
    target=out/'Root_actual_full370_real_operator_control_summary.json'
    summary=dict(schema='ACTUAL_FULL370_REAL_OPERATOR_CONTROL_GUARDED_REPORT_V1',
        status='ACTUAL_FULL370_REAL_OPERATOR_CONTROL_CLOSED0_ONLY' if good else 'ACTUAL_FULL370_REAL_OPERATOR_CONTROL_FAILED_UNQUALIFIED',
        failure=failure,after_check_error=after_error,records=runner.records,actual_watchdog_checks=watches,
        fixed_current_pins=fixed,actual_initial_parent_science_fullhash_pins=plan['scientific_input_current7_pins'],
        owned_runtime_pins=[runtime],output_pins=[c.pin(p) for p in sorted(out.rglob('*')) if p.is_file()],
        actual_control_results=actual,original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,
        original_caps=c.CAPS,resources_before=before,resources_after=after,wall_seconds=time.monotonic()-started,
        complete_original_tracks=11364,actions_per_group_sweep=181824,groups=370,axial_cells=48,retained_moments=9,
        finite18_prerequisite_pins=plan['finite18_prerequisite_pins'],formal_metadata_current_attestations=plan['formal_metadata_current_attestations'],
        signed_current_scope='TWO_END_FACES_ONLY',formal_SN32_equivalence_claimed=False,
        final_report_resource_check_passed=False,**c.FALSE)
    c.write(target,summary)
    try:
        final=check_all();previous=c.pin(target)
        summary['resources_after_including_summary_bytes']=final;summary['final_report_resource_check_passed']=True
        # Only this new host's ordinary single-link summary is finalized.
        rewrite_owned_summary(target,previous,summary)
        check_all()
    except BaseException as error:
        good=False
        if failure is None:failure=repr(error)
        summary.update(status='ACTUAL_FULL370_REAL_OPERATOR_CONTROL_FAILED_UNQUALIFIED',failure=failure,
            final_report_resource_check_passed=False)
        rewrite_owned_summary(target,c.pin(target),summary)
        raise
    c.require(good,'actual full operator failed, retained without retry: '+str(failure or after_error))
    print(json.dumps(dict(status=summary['status'],report_pin=c.pin(target),**c.FALSE)),flush=True)

if __name__=='__main__':main()
