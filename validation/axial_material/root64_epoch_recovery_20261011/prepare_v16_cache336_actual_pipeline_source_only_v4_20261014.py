#!/usr/bin/env python3
"""Create one v16 Source candidate after genuine build and bit-control results.

No compiler, control Host, pipeline, cleanup or mathematical Source is imported.
All actual future PFs in the reviewed preparation plan remain null until supplied.
"""
from pathlib import Path
import argparse,ast,hashlib,json,os,shlex,stat

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
SOURCE_PLAN=REC/'V16_CACHE336_ACTUAL_PIPELINE_PREPARER_SOURCE_PLAN_V3_20261014.json'
OLD=REC/'aaa_three_plane_compact_expected_pipeline_source_v15_20261014'
NEW=REC/'aaa_three_plane_cache336_pipeline_source_v16_20261014'
NEW_OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-cache336-20261014-v16')

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path):
    path=Path(path);before=identity(path.lstat())
    if not stat.S_ISREG(before[2])or path.is_symlink():raise RuntimeError('regular non-symlink Source/input')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd))!=before:raise RuntimeError('opened input exact7 differs')
        with os.fdopen(fd,'rb')as stream:
            fd=None;raw=stream.read()
            if identity(os.fstat(stream.fileno()))!=before:raise RuntimeError('input EOF exact7 differs')
    finally:
        if fd is not None:os.close(fd)
    if identity(path.lstat())!=before:raise RuntimeError('input after EOF exact7 differs')
    return raw,dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)

def exact_pin(row):
    if not isinstance(row,dict)or set(row)!={'path','sha256','size_bytes','identity'}or \
       not isinstance(row['identity'],list)or len(row['identity'])!=7 or any(type(x)is not int for x in row['identity'])or \
       type(row['size_bytes'])is not int or row['size_bytes']!=row['identity'][4]or \
       not stat.S_ISREG(row['identity'][2]):raise RuntimeError('exact canonical fullpin')
    return row

def read(row):
    exact_pin(row);raw,current=pin(row['path'])
    if current!=row:raise RuntimeError('exact selected Source/report PF changed: '+row['path'])
    return json.loads(raw)

def external(args,key):
    raw,row=pin(getattr(args,key+'_summary'))
    if row['sha256']!=getattr(args,key+'_sha256')or row['identity']!=json.loads(getattr(args,key+'_seven_id')):
        raise RuntimeError('actual external fullpin differs: '+key)
    return json.loads(raw),row

def unique(rows):
    table={}
    for row in rows:
        exact_pin(row)
        if row['path']in table and table[row['path']]!=row:raise RuntimeError('inconsistent exact complete dependency PF')
        table[row['path']]=row
    return list(table.values())

def recheck(rows):
    for row in unique(rows):
        path=Path(row['path'])
        if path.is_symlink()or identity(path.lstat())!=row['identity']:
            raise RuntimeError('inherited current dependency exact7 differs: '+row['path'])

def write(path,data):
    if isinstance(data,str):data=data.encode()
    with Path(path).open('xb')as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
    _,row=pin(path)
    if row['identity'][3]!=1:raise RuntimeError('new own Source output must be single-link')
    return row

def write_json(path,data):return write(path,json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

def require_terminal0(actual):
    if not isinstance(actual,dict)or type(actual.get('exit_code'))is not int or actual['exit_code']!=0 or \
       actual.get('session_id')is not None:raise RuntimeError('genuine terminal integer0 and no session required')

def require_post0(tools,report_pin,root_pin,role):
    actual=tools.get('actual_review_return');require_terminal0(actual)
    if tools.get('observed_closed')is not True:raise RuntimeError('genuine actual post-review closed flag')
    lines=actual.get('output','').strip().splitlines()
    if not lines:raise RuntimeError('actual post-review output binds exact review PF')
    review_pin=exact_pin(json.loads(lines[-1])['review_pin']);review=read(review_pin)
    if review.get('schema')!='LIMITED_ACTUAL_CACHE336_BUILD_OR_BIT_POSTVERIFICATION_V1'or \
       review.get('role')!=role or review.get('failure')is not None or not review.get('status','').startswith('PASS')or \
       review.get('actual_report_pin')!=report_pin or review.get('actual_Root_true_tool_return_pin')!=root_pin or \
       any(review.get(k)is not False for k in ('independent_business_executed','independent_compiler_executed',
         'independent_numerical_executed','independent_deletion_executed')):
        raise RuntimeError('exact independent post0 role/report/Roottool and no reviewer business')
    return review_pin

def require_cache336_bit_compiler_metadata(report,pactual,pown,review,root,compile_watch_pin):
    # Preserve the sealed false field; admit its precisely documented path error
    # only alongside the genuine three watches and two compile/link records.
    cause='own Host checks compile watch under compact-cache336-controls, actual watch is build/compile_control.watchdog.json'
    expected=dict(field='compiler_executed',reported_value=False,actual_value=True,cause=cause,
      actual_Host_Source_pin=pown,actual_report_pin=pactual,actual_compile_watch_pin=compile_watch_pin,
      wrong_summary_watch_path=str(root/'compact-cache336-controls/compile_control.watchdog.json'),
      actual_compile_watch_path=str(root/'build/compile_control.watchdog.json'))
    discrepancy=review.get('known_summary_metadata_discrepancy')
    if report.get('compiler_executed')is not False or review.get('actual_compiler_executed')is not True or \
       type(review.get('actual_compile_link_stage_count'))is not int or review['actual_compile_link_stage_count']!=2 or \
       type(review.get('actual_watch_stage_count'))is not int or review['actual_watch_stage_count']!=3 or \
       discrepancy!=expected or discrepancy.get('reported_value')is not False or discrepancy.get('actual_value')is not True:
        raise RuntimeError('exact sealed compiler-field path discrepancy and genuine actual compile/link evidence')
    wrong=root/'compact-cache336-controls/compile_control.watchdog.json'
    if wrong.exists()or wrong.is_symlink():raise RuntimeError('exact erroneous summary watch path must remain absent')
    records=report['records'];watches=review.get('actual_watch_and_log_evidence')
    if not isinstance(watches,list)or len(watches)!=3 or len(records)!=3 or \
       [x['label'].rsplit('/',1)[-1]for x in records]!=['compile_control','link_control','run_budget_bits']:
        raise RuntimeError('genuine exact ordered compile/link/run compiler evidence')
    outputs={x['path']:x for x in report['output_pins']}
    for record,item in zip(records,watches):
        wp=item['watch_pin'];lp=item['log_pin'];watch=item['actual_watch']
        if item['record_label']!=record['label']or record['status']!='PASS'or \
           wp['path']!=str(root/(record['label']+'.watchdog.json'))or lp['path']!=str(root/(record['label']+'.log'))or \
           outputs.get(wp['path'])!=wp or outputs.get(lp['path'])!=lp or lp['sha256']!=record['log_sha256']or \
           watch['command']!=record['command']or type(watch.get('returncode'))is not int or watch['returncode']!=0 or \
           watch.get('limit_failure')is not None or watch.get('rss_cap_mib')!=512 or \
           watch.get('own_child_only')is not True or watch.get('liveness_group_cleanup')is not True:
            raise RuntimeError('exact actual three closed0 watch/log/fullPF compiler facts')
    if watches[0]['watch_pin']!=compile_watch_pin:raise RuntimeError('precise normal compile watch identity')
    return expected

CACHE_ADMISSION_SOURCE=r'''def admit_cache336_driver_build(args,hf,helper,compact):
    build,pbuild=ext(args,'cache336_build70');root=Path(pbuild['path']).parent
    if pbuild!=selected_pin(hf,'selected_actual_cache336_build_report_pin')or \
       build.get('schema')!='ACTUAL_NATIVE_RANK1_CACHE336_DRIVER_COMPLETE70_BUILD_ONLY_V1'or \
       build.get('status')!='ACTUAL_ONE_CACHE336_DRIVER_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'or \
       [x['label'].rsplit('/',1)[-1]for x in build['records']]!=['compile_Driver','link_Dragon']or \
       any(build.get(k)is not True for k in ('Dragon_linked','final_report_resource_check_passed',
         'original69_other_inputs_identical_and_retained','original_four_archives_identical_and_retained',
         'current_nine_core_objects_identical_and_retained'))or \
       any(build.get(k)is not False for k in ('transport_executed','new_entry_controls_executed',
         'new_reader_control_qualification','new_cache_budget_component_control_qualification'))or \
       build.get('secondary_failures')!=[]or any(build.get(k)is not False for k in c.scope()):
        raise RuntimeError('genuine closed2 separate cache336 Driver-only build')
    c.closed_report(build,helper,root,2)
    bhf,pbhf=read_selected(hf,'selected_cache336_build_Host_freeze_pin')
    sf,psf=read_selected(hf,'selected_cache336_Fortran_Source_freeze_pin')
    if bhf.get('schema')!='COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_ONLY_FREEZE_V1'or \
       any(bhf.get(k)is not False for k in ('compiler_executed','numerical_executed','Host_imported_or_executed'))or \
       sf.get('schema')!='COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_ONLY_FREEZE_V1'or \
       sf.get('source_only')is not True or any(sf.get(k)is not False for k in ('compiled','numerical_executed','original_math_modified'))or \
       sf.get('Driver_single_literal_368_to336')is not True or sf.get('public_Driver_ABI_unchanged')is not True or \
       sf.get('internal_exact_cache_working_set_bytes')!=336*MI or \
       bhf['selected_new_Fortran_Source_freeze_pin']!=psf or \
       bhf['selected_original_actual_complete70_report_pin']!=compact['report_pin']or \
       bhf['selected_previous_complete70_Host_freeze_pin']!=compact['build_Host_freeze_pin']or \
       bhf['selected_previous_compact_Fortran_Source_freeze_pin']!=compact['source_freeze_pin']:
        raise RuntimeError('exact separate Driver Host/SF, prior compact741 and original math')
    c.verify_rows(bhf['dependencies']);c.same_pin(bhf['host_source']['path'],bhf['host_source'])
    pp=bhf['build_plan_pin'];deps=current_pin_table(bhf['dependencies'])
    if deps.get(pp['path'])!=pp or deps.get(psf['path'])!=psf:
        raise RuntimeError('own Driver HF binds exact plan/SF')
    plan,checked=c.read_bound_json_current(pp['path'],pp)
    if checked!=pp or plan.get('source_only')is not True or \
       any(plan.get(k)is not False for k in ('compiler_executed','numerical_executed'))or \
       any(k not in plan or plan[k]is not None for k in ('actual_new_Driver_object_pin','actual_new_Dragon_pin','actual_new_build_report_pin'))or \
       plan['original_actual_complete70_report_pin']!=compact['report_pin']or plan['planned_output_root']!=str(root)or \
       plan['original_caps']!=compact['caps']or bhf['original_caps']!=compact['caps']or build['original_caps']!=compact['caps']:
        raise RuntimeError('original caps and unexecuted Driver Source plan')
    old70=compact['current70_pins'];actual=current_pin_table(build['fixed_current_pins']+build['output_pins'])
    core=list(compact['report']['original_nine_core_object_pins']);core[5]=compact['object_pin']
    if plan['original_ordered70_input_pins']!=old70 or build['original_ordered70_input_pins']!=old70 or \
       build['original_actual_complete70_report_pin']!=compact['report_pin']or \
       build['replacement_zero_based_complete70_input_index']!=37 or \
       plan['current_nine_core_object_pins']!=core or build['original_nine_core_object_pins']!=core or \
       build['retained_current_BOOTQ_object_pin']!=compact['object_pin']or \
       build['selected_previous_complete70_Host_freeze_pin']!=compact['build_Host_freeze_pin']or \
       build['selected_previous_compact_Fortran_Source_freeze_pin']!=compact['source_freeze_pin']or \
       len(old70)!=70 or len({x['path']for x in old70})!=70 or old70[40]!=core[5]:
        raise RuntimeError('two separate replacement layers: compact40 then Driver37; current9 exact')
    sf_rows=unique(sf['files']+sf['original_source_pins']+sf['exact_source_evidence_pins'])
    c.verify_rows(sf_rows)
    source=bhf['new_production_Fortran_Source_pin']
    if source not in sf['files']or build['actual_new_Source_pin']!=source or \
       plan['original_Driver_Source_pin']not in sf['original_source_pins']or \
       plan['unchanged_SPOT1P64_Source_pin']!=sf['original_math_SPOT1P64_pin']:
        raise RuntimeError('single actual bound Driver Source, unchanged mathematical Source')
    for row in (pbhf,psf,bhf['host_source'],pp,source):
        if actual.get(row['path'])!=row:raise RuntimeError('actual Driver build binds own Source provenance')
    if build['actual_host_Source_freeze_pin']!=pbhf or build['actual_new_Source_freeze_pin']!=psf:
        raise RuntimeError('actual Driver report selects exact own freezes')
    objs=[x for x in build['output_pins']if x['path']==str(root/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o')]
    dragons=[x for x in build['output_pins']if x['path']==str(root/'runtime/Dragon')]
    builds=[x for x in build['output_pins']if Path(x['path']).parent==root/'build']
    expected_build_names=['SPOT_GLOBAL_NATIVE_DRIVER64.o','compile_Driver.log','compile_Driver.watchdog.json','link_Dragon.log','link_Dragon.watchdog.json']
    if len(objs)!=1 or len(dragons)!=1 or sorted(Path(x['path']).name for x in builds)!=sorted(expected_build_names)or \
       any(not stat.S_ISREG(x['identity'][2])or x['identity'][3]!=1 for x in builds):
        raise RuntimeError('Driver-only one-object and exact two-stage log/watch outputs, noMOD/other')
    new70=list(old70);new70[37]=objs[0]
    first=compact['report']['records'][0]['command']
    expected_compile=[first[0],*c.FLAGS,'-I'+str(root/'build'),*plan['original_compile_include_arguments'],
      '-J'+str(root/'build'),'-c',source['path'],'-o',objs[0]['path']]
    expected_link=[first[0],'-O2','-ffp-contract=off',*[x['path']for x in new70],'-o',dragons[0]['path']]
    if build['records'][0]['command']!=expected_compile or build['records'][1]['command']!=expected_link or \
       build['actual_complete70_link_inputs']!=[x['path']for x in new70]or \
       [(i,x,y)for i,(x,y)in enumerate(zip(old70,new70))if x!=y]!=[(37,old70[37],objs[0])]or \
       c.FLAGS!=plan['original_compile_flags']or any(actual.get(x['path'])!=x for x in new70+core)or \
       [x for x in new70 if x['path'].endswith('.a')]!=[x for x in old70 if x['path'].endswith('.a')]:
        raise RuntimeError('only37 whole-PF delta, remaining69 and archive order exact')
    c.verify_rows(new70+core)
    return dict(report=build,report_pin=pbuild,object_pin=objs[0],Dragon_pin=dragons[0],current70_pins=new70,
      source_pin=source,source_freeze_pin=psf,build_Host_freeze_pin=pbhf,math_object_pin=old70[57],
      retained_compact_source_freeze_pin=compact['source_freeze_pin'],caps=compact['caps'],
      fixed=unique([pbuild,pbhf,psf,bhf['host_source'],pp]+bhf['dependencies']+sf_rows+
        build['fixed_current_pins']+build['output_pins']))

def admit_cache336_budget_bit_controls(args,hf,helper,runtime):
    report,pactual=ext(args,'cache336_budget_bits');root=Path(pactual['path']).parent
    own,pown=read_selected(hf,'selected_cache336_budget_bit_Host_freeze_pin')
    if pactual!=selected_pin(hf,'selected_actual_cache336_budget_bit_report_pin')or \
       report.get('schema')!='ACTUAL_NATIVE_RANK1_CACHE336_BUDGET_BIT_GUARDED_CONTROL_REPORT_V1'or \
       report.get('status')!='ACTUAL_CACHE336_ENABLED_STORE_REJECT_MIXED_GROUP_BIT_CONTROLS_CLOSED0_ONLY'or \
       report.get('actual_cache336_budget_bit_controls_passed')is not True or \
       report.get('actual_model_controls_passed')is not False or report.get('actual_seven_genuine_public_READ_controls_passed')is not False or \
       report.get('new_reader_qualified')is not False or report.get('physics_qualified')is not False or \
       report.get('secondary_failures')!=[]or any(report.get(k)is not False for k in c.scope())or \
       [x['label'].rsplit('/',1)[-1]for x in report['records']]!=['compile_control','link_control','run_budget_bits']:
        raise RuntimeError('genuine three-stage new enabled/fallback/mixed-group bit controls')
    c.closed_report(report,helper,root,3)
    post,ppost=read_selected(hf,'selected_cache336_bits_actual_post_review_pin')
    posttools,pptools=read_selected(hf,'selected_cache336_bits_actual_post_tools_pin')
    proottool=selected_pin(hf,'selected_cache336_bits_actual_Root_tool_pin')
    actual_review=posttools.get('actual_review_return')
    if not isinstance(actual_review,dict)or type(actual_review.get('exit_code'))is not int or actual_review['exit_code']!=0 or \
       actual_review.get('session_id')is not None or posttools.get('observed_closed')is not True:
        raise RuntimeError('genuine exact closed independent bit post-review0')
    lines=actual_review.get('output','').strip().splitlines()
    if not lines or json.loads(lines[-1])['review_pin']!=ppost or \
       post.get('schema')!='LIMITED_ACTUAL_CACHE336_BUILD_OR_BIT_POSTVERIFICATION_V1'or post.get('role')!='bit'or \
       post.get('status')!='PASS_LIMITED_ACTUAL_CACHE336_BIT_POSTVERIFICATION'or post.get('failure')is not None or \
       post.get('actual_report_pin')!=pactual or post.get('actual_Host_freeze_pin')!=pown or \
       post.get('actual_Root_true_tool_return_pin')!=proottool or \
       any(post.get(k)is not False for k in ('independent_business_executed','independent_compiler_executed',
         'independent_numerical_executed','independent_deletion_executed')):
        raise RuntimeError('exact actual bit independent post facts/source/report binding')
    compiler_discrepancy=require_cache336_bit_compiler_metadata(report,pactual,own['host_source'],post,root,c.pin(root/'build/compile_control.watchdog.json'))
    if own.get('schema')!='COMPLETE_NATIVE_RANK1_CACHE336_BUDGET_BIT_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1'or \
       any(own.get(k)is not False for k in ('compiler_executed','numerical_executed','Host_imported_or_executed'))or \
       own['selected_new_build_Host_freeze_pin']!=runtime['build_Host_freeze_pin']or \
       own['selected_new_Fortran_Source_freeze_pin']!=runtime['source_freeze_pin']or \
       own['selected_unchanged_math_object_pin']!=runtime['math_object_pin']or \
       report['actual_host_Source_freeze_pin']!=pown or report['actual_Source_freeze_pin']!=runtime['source_freeze_pin']or \
       report['actual_new_build70_report_pin']!=runtime['report_pin']or \
       report['actual_new_Driver_object_pin']!=runtime['object_pin']or report['original_caps']!=runtime['caps']or \
       own['original_caps']!=runtime['caps']or report['original_aux_cap_bytes']!=128*MI or \
       report['original_pending_metadata_bytes']!=8*MI:
        raise RuntimeError('actual bit report ownHF/newDriverHF/sharedSF/math57/caps identity')
    c.same_pin(own['host_source']['path'],own['host_source']);c.verify_rows(own['dependencies'])
    pp=own['control_host_plan_pin'];dep=current_pin_table(own['dependencies'])
    actual=current_pin_table(report['fixed_current_pins']+report['output_pins'])
    for row in (pown,own['host_source'],pp,runtime['build_Host_freeze_pin'],runtime['source_freeze_pin'],runtime['math_object_pin']):
        if actual.get(row['path'])!=row:raise RuntimeError('exact actual budget-bit fixed Source authority')
    for row in (pp,runtime['build_Host_freeze_pin'],runtime['source_freeze_pin']):
        if dep.get(row['path'])!=row:raise RuntimeError('budget-bit ownHF selects exact current Source freezes')
    plan,checked=c.read_bound_json_current(pp['path'],pp)
    if checked!=pp or plan.get('source_only')is not True or plan['kind']!='cache336'or \
       any(plan.get(k)is not False for k in ('compiler_executed','numerical_executed','original_math_module_recompiled'))or \
       any(k not in plan or plan[k]is not None for k in ('future_actual_new_build70_report_pin',
        'future_actual_control_object_pin','future_actual_control_executable_pin','future_actual_control_report_pin'))or \
       plan['selected_new_build_Host_freeze_pin_path']!=runtime['build_Host_freeze_pin']['path']or \
       plan['selected_new_Fortran_Source_freeze_pin_path']!=runtime['source_freeze_pin']['path']or \
       plan['unchanged_math_object_pin']!=runtime['math_object_pin']or plan['planned_output_root']!=str(root):
        raise RuntimeError('exact unexecuted bit control Source plan, unchanged math object')
    source=plan['control_Source_pin'];obj=root/'build/control.o';exe=root/'runtime/control_unqualified'
    source_sf,checked_sf=c.read_bound_json_current(runtime['source_freeze_pin']['path'],runtime['source_freeze_pin'])
    if checked_sf!=runtime['source_freeze_pin']or source not in source_sf['files']or report['actual_control_Source_pin']!=source:
        raise RuntimeError('exact reviewed extended Fortran control Source')
    includes=['-I'+str(root/'build'),'-I'+plan['new_build_expected_build_directory'],*plan['original_compile_include_arguments']]
    compiler=plan['original_compiler_pin']['path'];archives=[x['path']for x in runtime['current70_pins']if x['path'].endswith('.a')]
    compile_cmd=[compiler,*c.FLAGS,*includes,'-J'+str(root/'build'),'-c',source['path'],'-o',str(obj)]
    link_cmd=[compiler,'-O2','-ffp-contract=off',str(obj),runtime['math_object_pin']['path'],*archives,'-o',str(exe)]
    if report['records'][0]['command']!=compile_cmd or report['records'][1]['command']!=link_cmd or \
       report['records'][2]['command']!=[str(exe)]or report['actual_compile_command']!=compile_cmd or \
       report['actual_link_command']!=link_cmd or report['actual_link_core_paths']!=[runtime['math_object_pin']['path']]or \
       any(Path(x['path']).suffix=='.mod'for x in report['output_pins'])or \
       sorted(Path(x['path']).name for x in report['output_pins']if Path(x['path']).parent==root/'build')!= \
         ['compile_control.log','compile_control.watchdog.json','control.o','link_control.log','link_control.watchdog.json']or \
       plan['original_four_archive_paths']!=archives or report['logical_control_count']!=1 or report['actual_run_phase_count']!=1:
        raise RuntimeError('compile test only/noMOD, exact retained math57+four archives and one actual run')
    results=report['actual_control_results'];rows,log_pin=compact_log_rows(root,report['records'][2])
    matches=[x for x in rows if x.get('status')=='ACTUAL_GENERIC_RANK1_CACHE336_BUDGET_COMPONENT_BIT_CONTROLS_COMPLETED_ONLY']
    if len(results)!=1 or len(matches)!=1 or results[0]['actual_terminal']!=matches[0]or results[0]['actual_log_pin']!=log_pin:
        raise RuntimeError('actual338/121 terminal equals full genuine log')
    terminal=matches[0]
    if type(terminal.get('actual_assertions'))is not int or terminal['actual_assertions']!=338 or \
       type(terminal.get('actual_SPOT1P64_calls'))is not int or terminal['actual_SPOT1P64_calls']!=121 or \
       results[0]['actual_assertions']!=338 or results[0]['actual_SPOT1P64_calls']!=121 or \
       any(terminal.get(k)is not False for k in ('formal_SN32_quadrature_equivalence','genuine_solver_qualified',
         'physics_qualified','AAA_qualified','ABA_admitted','goal_complete')):
        raise RuntimeError('new actual enabled STORE-reject/mixed bit assertion counts and precise scope')
    c.verify_rows(report['fixed_current_pins']+report['output_pins'])
    return dict(report_pin=pactual,own_Host_freeze_pin=pown,actual_assertions=338,actual_calls=121,
      known_summary_metadata_discrepancy=compiler_discrepancy,actual_compiler_executed=True,actual_compile_link_stage_count=2,
      actual_post_review_pin=ppost,actual_post_tools_pin=pptools,
      fixed=unique([pactual,pown,own['host_source'],pp,ppost,pptools,proottool]+own['dependencies']+report['fixed_current_pins']+report['output_pins']))

'''

def main():
    ap=argparse.ArgumentParser()
    for prefix in ('preparation-plan','cache336-build70','cache336-build-root-tool','cache336-build-post-tools',
                   'cache336-budget-bits','cache336-bits-root-tool','cache336-bits-post-tools'):
        for suffix in ('summary','sha256','seven-id'):ap.add_argument('--'+prefix+'-'+suffix,required=True)
    args=ap.parse_args()
    spec,pspec=external(args,'preparation_plan')
    if pspec['path']!=str(SOURCE_PLAN)or spec.get('schema')!='V16_CACHE336_ACTUAL_PIPELINE_PREPARER_SOURCE_PLAN_V1'or \
       spec.get('source_only')is not True or any(spec.get(k)is not False for k in ('compiler_executed','numerical_executed','pipeline_executed','files_deleted'))or \
       any(k not in spec or spec[k]is not None for k in spec['future_actual_keys']):
        raise RuntimeError('exact reviewed Source-only preparer specification; unknown future PFs null')
    if pin(__file__)[1]!=spec['preparer_source_pin']:raise RuntimeError('exact reviewed preparer Source')
    selected=spec['selected_existing_pins'];values={k:read(v)for k,v in selected.items()}
    b,pb=external(args,'cache336_build70');bt,pbt=external(args,'cache336_build_root_tool');bp,pbp=external(args,'cache336_build_post_tools')
    d,pd=external(args,'cache336_budget_bits');dt,pdt=external(args,'cache336_bits_root_tool');dp,pdp=external(args,'cache336_bits_post_tools')
    for role,report,pactual,tools,proot,post in [('build',b,pb,bt,pbt,bp),('bit',d,pd,dt,pdt,dp)]:
        expected=spec['expected_actual_'+role+'_report_path']
        if pactual['path']!=expected:raise RuntimeError('only selected future actual report namespace: '+role)
        require_terminal0(tools[spec['root_terminal_keys'][role]])
        if tools.get('observed_closed')is not True or type(tools.get('original_integer_exit_code'))is not int or tools['original_integer_exit_code']!=0:
            raise RuntimeError('genuine Root observed terminal closure and original integer0')
        argv=tools.get('exact_executed_command')
        argv=shlex.split(argv)if isinstance(argv,str)else argv
        if role=='build':want=values['Driver_build_CLI']['argv']
        else:
            iface=values['Budget_bit_CLI'];want=list(iface['python_environment_and_Host_prefix'])
            for prefix,row in [('new-build70',pb),('source-freeze',selected['cache336_Fortran_Source_freeze']),('host-freeze',selected['Budget_bit_Host_freeze'])]:
                want+=['--'+prefix+'-summary',row['path'],'--'+prefix+'-sha256',row['sha256'],'--'+prefix+'-seven-id',json.dumps(row['identity'],separators=(',',':'))]
        if argv!=want:raise RuntimeError('genuine Root terminal belongs to exact frozen thirty-token argv: '+role)
        require_post0(post,pactual,proot,role)
    post_build=require_post0(bp,pb,pbt,'build');post_bit=require_post0(dp,pd,pdt,'bit')
    bit_post=read(post_bit)
    require_cache336_bit_compiler_metadata(d,pd,values['Budget_bit_Host_freeze']['host_source'],bit_post,Path(pd['path']).parent,
      pin(Path(pd['path']).parent/'build/compile_control.watchdog.json')[1])
    for role,report,count,status,schema,own in [('build',b,2,'ACTUAL_ONE_CACHE336_DRIVER_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY',
      'ACTUAL_NATIVE_RANK1_CACHE336_DRIVER_COMPLETE70_BUILD_ONLY_V1','Driver_Host_freeze'),
      ('bit',d,3,'ACTUAL_CACHE336_ENABLED_STORE_REJECT_MIXED_GROUP_BIT_CONTROLS_CLOSED0_ONLY',
      'ACTUAL_NATIVE_RANK1_CACHE336_BUDGET_BIT_GUARDED_CONTROL_REPORT_V1','Budget_bit_Host_freeze')]:
        if report.get('schema')!=schema or report.get('status')!=status or report.get('failure')is not None or \
           report.get('after_check_error')is not None or report.get('secondary_failures')!=[]or \
           report.get('final_report_resource_check_passed')is not True or report.get('original_guard_class')!='OwnRSSSerialExecutor'or \
           report.get('original_guard_MRO_unchanged')is not True or len(report['records'])!=count or \
           any(x.get('status')!='PASS'for x in report['records'])or report['actual_host_Source_freeze_pin']!=selected[own]or \
           type(report.get('SELF_peak_bytes'))is not int or not 0<=report['SELF_peak_bytes']<512*2**20 or \
           type(report.get('wall_seconds'))not in (int,float)or not 0<report['wall_seconds']<1800:
            raise RuntimeError('genuine exact guarded actual prerequisite: '+role)
    if b['actual_new_Source_freeze_pin']!=selected['cache336_Fortran_Source_freeze']or \
       d['actual_Source_freeze_pin']!=selected['cache336_Fortran_Source_freeze']or d['actual_new_build70_report_pin']!=pb or \
       b['original_actual_complete70_report_pin']!=values['v15_candidate_plan']['selected_actual_prerequisites']['selected_actual_new_build70_report_pin']or \
       b['replacement_zero_based_complete70_input_index']!=37 or d['actual_cache336_budget_bit_controls_passed']is not True:
        raise RuntimeError('separate actual Driver37 and current budget-bit chain after compact40')
    hf=values['v15_Host_freeze'];prior=values['v15_candidate_plan']
    if len(hf['dependencies'])!=2802 or len(prior['original377_dependency_rows_to_retain'])!=377:
        raise RuntimeError('entire original v15 2802 and original377 Source closure retained')
    deps=unique(hf['dependencies']+[selected['v15_Host_freeze'],pspec,spec['preparer_source_pin'],pb,pbt,pbp,post_build,pd,pdt,pdp,post_bit]+list(selected.values())+
      values['Driver_Host_freeze']['dependencies']+values['Budget_bit_Host_freeze']['dependencies']+
      b['fixed_current_pins']+b['output_pins']+d['fixed_current_pins']+d['output_pins'])
    recheck(deps)
    if NEW.exists()or NEW.is_symlink()or NEW_OUT.exists()or NEW_OUT.is_symlink():raise RuntimeError('unique final v16 Source and future OUT only')
    raw,old_host=pin(OLD/'run_actual_three_plane_pipeline.py');text=raw.decode();changes=[]
    def replace(before,after,reason):
        nonlocal text
        if text.count(before)!=1:raise RuntimeError('one exact Source splice: '+reason)
        changes.append(dict(before=before,after=after,reason=reason));text=text.replace(before,after,1)
    replace("OUT=Path('"+prior['planned_output_root']+"')","OUT=Path('"+str(NEW_OUT)+"')",'unique v16 own OUT')
    replace("'private-model','public-read-seven']:","'private-model','public-read-seven','cache336-build70','cache336-budget-bits']:",'two new exact external report triplets')
    replace("hf['schema']!='COMPLETE_ACTUAL_AAA3_COMPACT_EXPECTED_PIPELINE_HOST_SOURCE_FREEZE_V15'", "hf['schema']!='COMPLETE_ACTUAL_AAA3_CACHE336_PIPELINE_HOST_SOURCE_FREEZE_V16'",'own complete v16 Source HF')
    own_source=pin(__file__)[0].decode();own_tree=ast.parse(own_source)
    metadata_node=next(n for n in own_tree.body if isinstance(n,ast.FunctionDef)and n.name=='require_cache336_bit_compiler_metadata')
    metadata_source=ast.get_source_segment(own_source,metadata_node)+'\n\n'
    replace('def main():\n',metadata_source+CACHE_ADMISSION_SOURCE+'def main():\n','separate Driver37 and genuine338/121 budget-bit admission')
    replace("    build=compact['report'];pbuild=compact['report_pin']\n    current70_link=build['actual_complete70_link_inputs']",
      "    runtime=admit_cache336_driver_build(args,hf,helper,compact)\n    build=runtime['report'];pbuild=runtime['report_pin']\n    current70_link=build['actual_complete70_link_inputs']",'only final Driver70 selected for runtime and alias')
    replace("direct_binding['schema']!='DECLARED_ACTUAL_COMPONENT_DIRECT_ALIAS_ENTRY_BINDING_V2'", "direct_binding['schema']!='DECLARED_ACTUAL_COMPONENT_DIRECT_ALIAS_ENTRY_BINDING_V3'",'two-layer direct alias Source binding')
    replace("       direct_binding['actual_complete70_source_freeze_pin']!=compact['source_freeze_pin']or \\\n       direct_original_inputs!=compact['current70_pins']or ",
      "       direct_binding['actual_complete70_source_freeze_pin']!=runtime['source_freeze_pin']or \\\n       direct_binding['retained_compact_BOOTQ_source_freeze_pin']!=compact['source_freeze_pin']or \\\n       direct_binding['runtime_base_compact_build_report_pin']!=compact['report_pin']or \\\n       direct_original_inputs!=runtime['current70_pins']or ",'alias main12 uses final70 while keeping exact Q3fdf lineage')
    replace("    compact_admission_provenance=dict(new_build70_report_pin=pbuild,new_BOOTQ_object_pin=compact['object_pin'],",
      "    budget=admit_cache336_budget_bit_controls(args,hf,helper,runtime)\n    cache336_admission_provenance=dict(new_driver_build_report_pin=pbuild,new_Driver_object_pin=runtime['object_pin'],\n      new_Driver_Fortran_Source_freeze_pin=runtime['source_freeze_pin'],new_Driver_Host_freeze_pin=runtime['build_Host_freeze_pin'],\n      budget_bit_report_pin=budget['report_pin'],budget_bit_Host_freeze_pin=budget['own_Host_freeze_pin'],\n      actual_assertions=budget['actual_assertions'],actual_calls=budget['actual_calls'],complete70_replacement_zero_based_index=37,\n      bit_known_summary_metadata_discrepancy=budget['known_summary_metadata_discrepancy'],bit_actual_compiler_executed=True,\n      bit_actual_compile_link_stage_count=2,bit_actual_post_review_pin=budget['actual_post_review_pin'],\n      retained_compact_build_report_pin=compact['report_pin'],retained_compact_Fortran_Source_freeze_pin=compact['source_freeze_pin'],physics_qualified=False)\n    compact_admission_provenance=dict(new_build70_report_pin=compact['report_pin'],new_BOOTQ_object_pin=compact['object_pin'],",'separate truthful 40 and37 actual provenance')
    replace("    fixed=unique(fixed+compact['fixed']+controls['fixed']+[cache_build_pin]", "    fixed=unique(fixed+compact['fixed']+controls['fixed']+runtime['fixed']+budget['fixed']+[cache_build_pin]",'retain both chains complete current fixed authority')
    replace('    del compact,controls,cache_build\n','    del compact,controls,cache_build,runtime,budget\n','release only unused admission JSON containers before guarded runtime')
    replace('          actual_compact_expected_reader_admission=compact_admission_provenance,\n', '          actual_compact_expected_reader_admission=compact_admission_provenance,\n          actual_cache336_driver_and_budget_bit_admission=cache336_admission_provenance,\n','raw separate cache336 provenance')
    replace("          actual_compact_expected_reader_admission=compact_admission_provenance,angular_moments_status='UNKNOWN',", "          actual_compact_expected_reader_admission=compact_admission_provenance,\n          actual_cache336_driver_and_budget_bit_admission=cache336_admission_provenance,angular_moments_status='UNKNOWN',",'compact summary separate cache336 provenance')
    ast.parse(text);restored=text
    for block in reversed(changes):
        if restored.count(block['after'])!=1:raise RuntimeError('unambiguous Source inverse')
        restored=restored.replace(block['after'],block['before'],1)
    if restored.encode()!=raw:raise RuntimeError('entire v15 Host bytes recovered')
    protected=raw[raw.index(b'    try:\n        # Replace ONLY the main object'):raw.index(b'        raw=dict(schema=')]
    if protected not in text.encode():raise RuntimeError('original guarded50 body and all science statements unchanged')
    for name in ('admit_compact_build','admit_control_host','admit_exact_public_stale_lifetimes','admit_compact_controls'):
        oldtree=ast.parse(raw);newtree=ast.parse(text)
        oldfun=next(n for n in oldtree.body if isinstance(n,ast.FunctionDef)and n.name==name)
        newfun=next(n for n in newtree.body if isinstance(n,ast.FunctionDef)and n.name==name)
        if ast.get_source_segment(raw.decode(),oldfun)!=ast.get_source_segment(text,newfun):raise RuntimeError('original compact40/fourcontrol admission helper wholebytes unchanged')
    NEW.mkdir();host=write(NEW/'run_actual_three_plane_pipeline.py',text);helpers=[]
    for name in ('actual_inputs_and_readback.py','direct_alias_entry_controls.f90','mutate_owned_control.f90'):
        data,previous=pin(OLD/name);candidate=write(NEW/name,data)
        helpers.append(dict(predecessor_pin=previous,candidate_pin=candidate,whole_bytes_unchanged=True))
    direct=dict(values['v15_direct_alias_binding']);table={x['path']:x for x in unique(b['fixed_current_pins']+b['output_pins'])}
    ordered=[table[path]for path in b['actual_complete70_link_inputs']]
    if len(ordered)!=70 or ordered[12]!=direct['excluded_original_main_pin']:raise RuntimeError('final Driver70 retains exact original main12')
    direct.update(schema='DECLARED_ACTUAL_COMPONENT_DIRECT_ALIAS_ENTRY_BINDING_V3',selected_actual_build70_report_pin=pb,
      actual_original_ordered_70_link_inputs=ordered,actual_complete70_source_freeze_pin=selected['cache336_Fortran_Source_freeze'],
      retained_compact_BOOTQ_source_freeze_pin=hf['selected_new_Fortran_Source_freeze_pin'],
      runtime_base_compact_build_report_pin=hf['selected_actual_new_build70_report_pin'],
      new_probe_source=str(NEW/'direct_alias_entry_controls.f90'),actual_pipeline_executed=False)
    pdir=write_json(NEW/'DIRECT_ALIAS_ENTRY_BINDING.json',direct)
    inv=write_json(NEW/'COMPLETE_V15_TO_V16_CACHE336_ADMISSION_WHOLE_BYTE_INVERSE.json',dict(
      schema='COMPLETE_V15_TO_V16_CACHE336_ADMISSION_WHOLE_BYTE_INVERSE_V1',original_pin=old_host,candidate_pin=host,
      changes=changes,whole_restored_bytes_equal=True,restored_sha256=hashlib.sha256(restored.encode()).hexdigest(),
      original50_continuous_source_bytes=len(protected),original50_continuous_source_sha256=hashlib.sha256(protected).hexdigest(),
      original50_continuous_source_unchanged=True,original_compact40_and_four_control_admission_helpers_unchanged=True,
      helpers=helpers,direct_binding_predecessor_pin=selected['v15_direct_alias_binding'],direct_binding_actual_pin=pdir,
      direct_binding_old_data=values['v15_direct_alias_binding'],source_only=True,compiler_executed=False,
      numerical_executed=False,files_deleted=False))
    selection=dict(prior['selected_actual_prerequisites'],selected_actual_cache336_build_report_pin=pb,
      selected_cache336_build_Host_freeze_pin=selected['Driver_Host_freeze'],
      selected_cache336_Fortran_Source_freeze_pin=selected['cache336_Fortran_Source_freeze'],
      selected_actual_cache336_budget_bit_report_pin=pd,selected_cache336_budget_bit_Host_freeze_pin=selected['Budget_bit_Host_freeze'],
      selected_cache336_bits_actual_post_review_pin=post_bit,selected_cache336_bits_actual_post_tools_pin=pdp,
      selected_cache336_bits_actual_Root_tool_pin=pdt)
    deps=unique(deps+[pdir,inv]+[h['candidate_pin']for h in helpers]);recheck(deps)
    plan=write_json(NEW/'ACTUAL_CACHE336_PREREQUISITE_BOUND_V16_SOURCE_PREPARATION_PLAN.json',dict(
      schema='ACTUAL_CACHE336_PREREQUISITE_BOUND_V16_SOURCE_PREPARATION_PLAN_V1',source_only=True,host_source=host,
      predecessor_v15_Host_freeze_pin=selected['v15_Host_freeze'],entire_original2802_dependencies_to_retain=hf['dependencies'],
      original377_dependency_rows_to_retain=prior['original377_dependency_rows_to_retain'],selected_actual_prerequisites=selection,
      dependencies=deps,complete_byte_inverse_pin=inv,direct_alias_binding_pin=pdir,helper_byte_equality=helpers,
      planned_output_root=str(NEW_OUT),original_pipeline_records_expected=dict(total=50,PASS=17,expected_refusal=33),
      original_caps=prior['original_caps'],strict_forecast_MiB=prior['strict_forecast_MiB'],
      cache336_build_actual_Root_tool_pin=pbt,cache336_build_actual_post_review_pin=post_build,cache336_build_actual_post_tools_pin=pbp,
      cache336_bits_actual_Root_tool_pin=pdt,cache336_bits_actual_post_review_pin=post_bit,cache336_bits_actual_post_tools_pin=pdp,
      current_Common_Source_freeze_pin=prior['current_Common_Source_freeze_pin'],expected_external_prefix_count=13,
      expected_argv_scalar_field_count=39,expected_total_argv_count=90,actual_pipeline_executed=False,
      compiler_executed=False,numerical_executed=False,files_deleted=False,own_Host_freeze_pin=None,own_CLI_pin=None,
      future_actual_v16_report_pin=None,AAA_qualified=False,ABA_admitted=False))
    ready=write_json(NEW/'SOURCE_REVIEW_READY.json',dict(schema='V16_CACHE336_ACTUAL_BOUND_SOURCE_REVIEW_READY_V1',
      status='SOURCE_ONLY_CANDIDATE_READY_FOR_INDEPENDENT_SOURCE_REVIEW',failure=None,host_source=host,plan_pin=plan,
      inverse_pin=inv,helpers=helpers,direct_binding_pin=pdir,original2802_and377_all_retained=True,
      original50_continuous_source_unchanged=True,compact40_and_driver37_admitted_separately=True,
      selected_actual_prerequisites=selection,source_change_blocks=len(changes),source_only=True,
      compiler_executed=False,numerical_executed=False,pipeline_executed=False,files_deleted=False,
      actual_Host_freeze_pin=None,actual_CLI_pin=None,actual_v16_report_pin=None))
    print(json.dumps(dict(status='V16_GENUINE_CACHE336_PREREQUISITE_BOUND_SOURCE_CREATED_ONLY',host_source=host,
      plan_pin=plan,ready_pin=ready,inverse_pin=inv,actual_dependency_count=len(deps),compiler_executed=False,
      numerical_executed=False,pipeline_executed=False,files_deleted=False),ensure_ascii=False),flush=True)

if __name__=='__main__':main()
