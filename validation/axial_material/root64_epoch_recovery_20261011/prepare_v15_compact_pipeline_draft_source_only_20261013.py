#!/usr/bin/env python3
"""Prepare an unexecuted v15 Host draft; never import a Host or run a child."""
from pathlib import Path
import ast, hashlib, json, os, stat

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'aaa_three_plane_streaming_pipeline_source_v14'
NEW=REC/'aaa_three_plane_compact_expected_pipeline_source_draft_v1_20261013'

GATES=r'''# These admission routines read genuine completed prerequisites only. They do
# not execute a compiler/control, reuse an old-reader PASS, or grant physics.
def selected_pin(hf,key):
    row=hf.get(key)
    if not isinstance(row,dict)or set(row)!={'path','sha256','size_bytes','identity'}:
        raise RuntimeError('exact actual selected prerequisite fullpin required: '+key)
    table={x['path']:x for x in unique(hf['dependencies'])}
    if table.get(row['path'])!=row:raise RuntimeError('selected actual prerequisite belongs to owning HF: '+key)
    return row

def read_selected(hf,key):
    chosen=selected_pin(hf,key)
    value,checked=c.read_bound_json_current(chosen['path'],chosen)
    if checked!=chosen:raise RuntimeError('selected current prerequisite fullpin: '+key)
    return value,chosen

def current_pin_table(rows):
    return {row['path']:row for row in unique(rows)}

def compact_log_rows(root,record):
    label=record['label']
    if not isinstance(label,str)or label.startswith('/')or any(x in ('','..','.')for x in label.split('/')):
        raise RuntimeError('exact owned prerequisite stage label')
    path=root/(label+'.log');pf=c.pin(path)
    if pf['sha256']!=record['log_sha256']:raise RuntimeError('closed prerequisite full log SHA')
    rows=[]
    with path.open('r',encoding='utf-8',errors='strict')as stream:
        for line in stream:
            if len(line)>65536:raise RuntimeError('bounded actual control JSON line')
            line=line.strip()
            if line.startswith('{')and line.endswith('}'):
                value=json.loads(line)
                if isinstance(value,dict):rows.append(value)
    c.same_pin(path,pf);return rows,pf

def exact_counter_oracles(actual,declared,prefixes):
    for key,value in declared.items():
        if key.startswith(prefixes):
            observed=actual.get(key[9:])
            if type(value)is not int or type(observed)is not int or observed!=value:
                raise RuntimeError('exact integer actual control status/call-count: '+key)

def admit_compact_build(args,hf,helper,cache,p_cache,old9):
    build,pbuild=ext(args,'new_build70')
    if pbuild!=selected_pin(hf,'selected_actual_new_build70_report_pin')or \
       build.get('schema')!='ACTUAL_BQ64_COMPACT_EXPECTED_COMPLETE70_BUILD_ONLY_V1'or \
       build.get('status')!='ACTUAL_ONE_BOOTQ_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'or \
       [x['label'].rsplit('/',1)[-1]for x in build['records']]!=['compile_BOOTQ','link_Dragon']or \
       any(build.get(k)is not True for k in ('Dragon_linked','final_report_resource_check_passed',
         'original69_other_inputs_identical_and_retained','original_four_archives_identical_and_retained',
         'original_eight_unchanged_core_objects_identical_and_retained'))or \
       any(build.get(k)is not False for k in ('transport_executed','new_entry_controls_executed','new_reader_control_qualification')):
        raise RuntimeError('genuine closed2 compact BOOTQ build prerequisite')
    c.closed_report(build,helper,Path(pbuild['path']).parent,2)
    if build.get('secondary_failures')!=[]or any(build.get(k)is not False for k in c.scope()):
        raise RuntimeError('no secondary actual build failure or inherited physics scope')
    bhf,pbhf=read_selected(hf,'selected_new_build_Host_freeze_pin')
    sf,psf=read_selected(hf,'selected_new_Fortran_Source_freeze_pin')
    if bhf.get('schema')!='COMPLETE_BQ64_COMPACT_EXPECTED_BUILD_HOST_SOURCE_ONLY_FREEZE_V1'or \
       any(bhf.get(k)is not False for k in ('compiler_executed','numerical_executed','Host_imported_or_executed'))or \
       sf.get('schema')!='COMPLETE_BQ64_COMPACT_EXPECTED_COMPOSED_FORTRAN_SOURCE_ONLY_FREEZE_V1'or \
       sf.get('source_only')is not True or any(sf.get(k)is not False for k in ('compiled','numerical_executed'))or \
       bhf['selected_new_Fortran_Source_freeze_pin']!=psf or \
       bhf['selected_original_actual_complete70_report_pin']!=p_cache:
        raise RuntimeError('exact Source-only new build Host and compact Fortran authority')
    c.verify_rows(bhf['dependencies']);c.same_pin(bhf['host_source']['path'],bhf['host_source'])
    btable=current_pin_table(bhf['dependencies'])
    pp=bhf['build_plan_pin']
    if btable.get(pp['path'])!=pp:raise RuntimeError('exact owning newbuild plan dependency')
    plan,checked=c.read_bound_json_current(pp['path'],pp)
    if checked!=pp or plan.get('source_only')is not True or \
       any(plan.get(k)is not False for k in ('compiler_executed','numerical_executed'))or \
       any(plan.get(k)is not None for k in ('actual_new_BOOTQ_object_pin','actual_new_Dragon_pin','actual_new_build_report_pin'))or \
       plan['original_actual_complete70_report_pin']!=p_cache:
        raise RuntimeError('frozen parameterized build plan does not predict actual results')
    caps=dict(original_stage_wall_cap_seconds=600,whole_wall_cap_seconds=1800,
      SELF_and_each_own_child_RSS_cap_bytes=512*2**20,threads=1,children_at_once=1,retries=0,
      fresh_output_cap_bytes=2*2**30,history_cap_bytes=96*2**30,filesystem_floor_bytes=8*2**30,
      original_cold_reserve_bytes=20971764748)
    if plan['original_caps']!=caps or bhf['original_caps']!=caps or build.get('original_caps')!=caps:
        raise RuntimeError('unchanged complete original newbuild caps')
    old70=plan['original_ordered70_input_pins']
    cache_table=current_pin_table(cache['fixed_current_pins']+cache['output_pins'])
    if old70!=build['original_ordered70_input_pins']or \
       [x['path']for x in old70]!=cache['actual_complete70_link_inputs']or \
       len(old70)!=70 or len({x['path']for x in old70})!=70 or \
       any(cache_table.get(x['path'])!=x for x in old70)or \
       plan['original_nine_core_object_pins']!=old9 or build['original_nine_core_object_pins']!=old9 or \
       len(old9)!=9 or old70[40]!=old9[5]or \
       build.get('replacement_zero_based_complete70_input_index')!=40 or \
       build.get('original_actual_complete70_report_pin')!=p_cache:
        raise RuntimeError('old69 inputs and exact core6/ordered70 index40 historical mapping')
    sf_rows=unique(sf['files']+sf['original_source_pins']+[sf['complete_byte_inverse_pin'],sf['control_plan_pin']])
    c.verify_rows(sf_rows)
    source=bhf['new_production_Fortran_Source_pin']
    if source not in sf['files']or build['actual_new_Source_pin']!=source:
        raise RuntimeError('one actual new compact BOOTQ Fortran Source')
    actual_table=current_pin_table(build['fixed_current_pins']+build['output_pins'])
    if any(actual_table.get(x['path'])!=x for x in (pbhf,psf,bhf['host_source'],pp,source))or \
       build['actual_host_Source_freeze_pin']!=pbhf or build['actual_new_Source_freeze_pin']!=psf:
        raise RuntimeError('newbuild own Host/SF/Source/plan exact fixed closure')
    root=Path(pbuild['path']).parent
    objects=[x for x in build['output_pins']if x['path']==str(root/'build/SPOR64_BOOTQ64.o')]
    dragons=[x for x in build['output_pins']if x['path']==str(root/'runtime/Dragon')]
    modules=[x for x in build['output_pins']if Path(x['path']).parent==root/'build'and Path(x['path']).suffix=='.mod']
    if len(objects)!=1 or len(dragons)!=1 or not modules or plan['planned_output_root']!=str(root):
        raise RuntimeError('genuine new object/module/Dragon exact output namespace')
    obj=objects[0];new70=list(old70);new70[40]=obj
    command=build['records'][0]['command'];old_command=cache['records'][0]['command']
    includes=['-I'+str(root/'build')]+plan['original_compile_include_arguments']
    expected_compile=[old_command[0],*c.FLAGS,*includes,'-J'+str(root/'build'),'-c',source['path'],'-o',obj['path']]
    expected_link=[old_command[0],'-O2','-ffp-contract=off',*[x['path']for x in new70],'-o',dragons[0]['path']]
    if command!=expected_compile or build['records'][1]['command']!=expected_link or \
       c.FLAGS!=plan['original_compile_flags']or old_command[0]!=plan['original_compiler_pin']['path']or \
       build['actual_complete70_link_inputs']!=[x['path']for x in new70]or \
       any(actual_table.get(x['path'])!=x for x in new70):
        raise RuntimeError('exact actual compact compile and one40-only ordered70 relink')
    c.verify_rows(new70)
    return dict(report=build,report_pin=pbuild,object_pin=obj,Dragon_pin=dragons[0],module_pins=modules,
      current70_pins=new70,source_pin=source,source_freeze_pin=psf,build_Host_freeze_pin=pbhf,
      fixed=unique([pbuild,pbhf,psf,bhf['host_source'],pp]+bhf['dependencies']+sf_rows+
        build['fixed_current_pins']+build['output_pins']),caps=caps)

def admit_control_host(hf,report,role,schema,selected_hf_key,compact):
    own,pown=read_selected(hf,selected_hf_key)
    if own.get('schema')!=schema or own.get('compiler_executed')is not False or \
       own.get('selected_new_build_Host_freeze_pin')!=compact['build_Host_freeze_pin']or \
       own.get('selected_new_Fortran_Source_freeze_pin')!=compact['source_freeze_pin']or \
       report.get('actual_host_Source_freeze_pin')!=pown:
        raise RuntimeError('exact actual '+role+' owning Host freeze')
    if role=='fresh17':
        if own.get('controls_executed')is not False:raise RuntimeError('Source-only fresh17 Host premise')
    elif own.get('numerical_executed')is not False:raise RuntimeError('Source-only control Host premise')
    c.same_pin(own['host_source']['path'],own['host_source']);c.verify_rows(own['dependencies'])
    table=current_pin_table(report['fixed_current_pins']);deps=current_pin_table(own['dependencies'])
    for x in (pown,own['host_source'],compact['build_Host_freeze_pin'],compact['source_freeze_pin']):
        if table.get(x['path'])!=x:raise RuntimeError('actual control fixed own-source provenance')
    for x in (compact['build_Host_freeze_pin'],compact['source_freeze_pin']):
        if deps.get(x['path'])!=x:raise RuntimeError('own Host explicit selected compact freezes')
    if report.get('actual_new_build70_report_pin')!=compact['report_pin']:
        raise RuntimeError('control actual newbuild report identity')
    if report.get('genuine_production_new_BOOTQ_object_pin'if role=='fresh17'else'actual_new_BOOTQ_object_pin')!=compact['object_pin']:
        raise RuntimeError('same genuine new BOOTQ object across all controls')
    return own,pown

def admit_compact_controls(args,hf,helper,compact,old17,pold17):
    fixed=[];provenance={}
    oracle_pin=old17['actual_current_control_binding_pin']
    oracle,checked=c.read_bound_json_current(oracle_pin['path'],oracle_pin)
    if checked!=oracle_pin or oracle['source_pin']!=old17['actual_current_control_source_pin']or \
       oracle['source_pin']['sha256']!='1b782030e20d4a254052937fd37ff6ef0e145969604e6ef6d365957ea29a9af3':
        raise RuntimeError('unchanged original17 factory Source/oracle authority')
    specs=[('fresh17','fresh_seventeen','selected_actual_fresh17_report_pin',20,
      'ACTUAL_BQ64_COMPACT_EXPECTED_FRESH_CONNECTED17_COMPONENT_CONTROLS_V1',
      'ACTUAL_NEW_BOOTQ_CURRENT17_CONNECTED_CONTROLS_CLOSED0_ONLY',
      'COMPLETE_BQ64_COMPACT_EXPECTED_CONNECTED17_HOST_SOURCE_ONLY_FREEZE_V1','selected_fresh17_Host_freeze_pin'),
     ('model','private_model','selected_actual_private_model_report_pin',3,
      'ACTUAL_BQ64_PRIVATE_GANLIB_MODEL_GUARDED_CONTROL_REPORT_V1',
      'ACTUAL_PRIVATE_GANLIB_MODEL_CONTROLS_CLOSED0_ONLY',
      'COMPLETE_BQ64_PRIVATE_GANLIB_MODEL_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1','selected_private_model_Host_freeze_pin'),
     ('public7','public_read_seven','selected_actual_public7_report_pin',11,
      'ACTUAL_GENUINE_PUBLIC_READ_COMPACT_BQ_ADMISSION_GUARDED_CONTROL_REPORT_V1',
      'ACTUAL_SEVEN_GENUINE_PUBLIC_READ_CONTROLS_NINE_PHASES_CLOSED0_ONLY',
      'COMPLETE_GENUINE_PUBLIC_READ_COMPACT_BQ_ADMISSION_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1','selected_public7_Host_freeze_pin')]
    for role,prefix,selected,count,schema,status,own_schema,own_key in specs:
        d,pd=ext(args,prefix);root=Path(pd['path']).parent
        if pd!=selected_pin(hf,selected)or d.get('schema')!=schema or d.get('status')!=status or \
           d.get('final_report_resource_check_passed')is not True or d.get('secondary_failures')!=[]:
            raise RuntimeError('genuine completed exact '+role+' control report')
        c.closed_report(d,helper,root,count)
        if any(d.get(k)is not False for k in c.scope()):raise RuntimeError('unqualified prerequisite scope must remain false')
        own,pown=admit_control_host(hf,d,role,own_schema,own_key,compact)
        if role=='fresh17':
            if d.get('actual_logical_control_count')!=17 or d.get('actual_run_phase_count')!=18 or \
               d.get('all17_original_names_exercised')is not True or d.get('old_seventeen_PASS_inherited')is not False or \
               d.get('other_eight_core_objects_and_original_oracles_unchanged')is not True or \
               any(d.get(k)is not False for k in ('new_private_model_controls_qualified','new_extra_public_READ_controls_qualified','production_reader_admitted'))or \
               d.get('original_current17_report_pin')!=pold17 or d.get('original_current17_oracle_pin')!=oracle_pin or \
               d.get('actual_current_control_source_pin')!=oracle['source_pin']or \
               own.get('selected_original17_report_pin')!=pold17 or \
               own.get('selected_actual_new_build70_report_pin')!=compact['report_pin']:
                raise RuntimeError('new actual17 scope and unchanged historical oracle Source')
            compile_cmd=list(oracle['planned_compile_command']);old_out=oracle['planned_output_root']
            include_at=next(i for i,x in enumerate(compile_cmd)if x.startswith('-I'))
            compile_cmd.insert(include_at,'-I'+str(Path(compact['object_pin']['path']).parent))
            compile_cmd=[('-J'+str(root/'build'))if x=='-J'+old_out+'/build'else x for x in compile_cmd]
            old_obj=compile_cmd[-1];new_obj=str(root/'build/test_ROOT64_full_connected17.o');compile_cmd[-1]=new_obj
            old_link=oracle['planned_link_command'];inputs=list(old_link[3:-2])
            if len(inputs)!=14 or inputs[0]!=old_obj or Path(inputs[3]).name!='SPOR64_BOOTQ64.o':
                raise RuntimeError('original current17 exact main0/BOOTQ3 link role')
            inputs[0]=new_obj;inputs[3]=compact['object_pin']['path'];exe=str(root/'build/full_connected17_unqualified')
            commands=[compile_cmd,[*old_link[:3],*inputs,'-o',exe]]+[[exe,*x[1:]]for x in oracle['planned_run_commands']]
            if [x['command']for x in d['records']]!=commands or len(commands)!=20 or \
               any(x not in compact['report']['actual_complete70_link_inputs']for x in inputs[1:])or len(d['actual_cases'])!=18:
                raise RuntimeError('genuine fresh20 commands and exact current9/fourarchives')
            for i,(record,case)in enumerate(zip(d['records'][2:],d['actual_cases'])):
                rows,lp=compact_log_rows(root,record);command=commands[i+2]
                name=command[1];phase=command[2]if len(command)==3 else'single'
                if len(rows)!=2 or rows!=[case['assertions'],case['actual_statuses_and_call_counts']]or \
                   (case['case'],case['phase'])!=(name,phase)or \
                   any((x.get('case'),x.get('phase'))!=(name,phase)for x in rows)or \
                   rows[0].get('all_actual_assertions_completed')is not True or rows[0].get('synthetic_fixture')is not True or \
                   any(rows[0].get(k)is not False for k in ('genuine_producer_qualified','solver_executed','physics_qualified','old_seventeen_PASS_inherited')):
                    raise RuntimeError('real fresh17 assertion/log case and unqualified scope')
                declared=next(x for x in oracle['declared_case_oracles']if x['case']==name)
                exact_counter_oracles(rows[1],declared,('expected_actual_','expected_explicit_'))
            refusal=d['actual_independent_host_coherent_refusal'];baseline=d['independent_coherent_baseline_manifest_pin']
            value,checked=c.read_bound_json_current(baseline['path'],baseline)
            if checked!=baseline or value['actual_before_pin']!=refusal['before']or \
               refusal.get('actual_refused')is not True or refusal.get('Fortran_internal_refusal_claimed')is not False or \
               refusal.get('actual_original_Host_gate')!='same_pin'or not isinstance(refusal.get('actual_refusal_error'),str)or \
               not refusal['actual_refusal_error']or refusal['before']['sha256']==refusal['after']['sha256']or \
               refusal['before']['identity']==refusal['after']['identity']:
                raise RuntimeError('real independent coherent immutable Host gate refusal')
            c.same_pin(refusal['after']['path'],refusal['after'])
        else:
            if d.get('logical_control_count')!=(1 if role=='model'else 7)or d.get('actual_run_phase_count')!=(1 if role=='model'else 9)or \
               d.get('old17_PASS_inherited')is not False or d.get('private_model_does_not_independently_qualify_public_reader')is not True or \
               any(d.get(k)is not False for k in ('new_reader_qualified','physics_qualified'))or \
               d.get('original_caps')!=compact['caps']or d.get('original_aux_cap_bytes')!=128*MI or \
               d.get('original_pending_metadata_bytes')!=8*MI or d.get('terminal_receipt_required_for_qualification')is not True:
                raise RuntimeError('separate model/public7 exact scope and original caps')
            plan_pin=own['control_host_plan_pin'];table=current_pin_table(own['dependencies'])
            if table.get(plan_pin['path'])!=plan_pin:raise RuntimeError('own frozen control plan')
            plan,checked=c.read_bound_json_current(plan_pin['path'],plan_pin)
            sfpin=d['actual_Source_freeze_pin'];sf,checked_sf=c.read_bound_json_current(sfpin['path'],sfpin)
            if checked!=plan_pin or checked_sf!=sfpin or d['actual_control_Source_pin']!=plan['control_Source_pin']or \
               sfpin!=plan['selected_control_Source_freeze_pin']or d['actual_control_Source_pin']not in sf['files']or \
               plan['selected_new_build_Host_freeze_pin']!=compact['build_Host_freeze_pin']or \
               plan['selected_new_Fortran_Source_freeze_pin']!=compact['source_freeze_pin']or \
               plan['planned_output_root']!=str(root)or plan['production_Source_pin']!=compact['source_pin']:
                raise RuntimeError('exact separate model/public control Source and frozenplan')
            if plan.get('source_only')is not True or any(plan.get(k)is not False for k in ('compiler_executed','numerical_executed','Host_imported'))or \
               any(plan.get(k)is not None for k in ('future_actual_new_build70_report_pin','future_actual_control_object_pin','future_actual_control_executable_pin','future_actual_control_report_pin','future_actual_stale_manifests'))or \
               plan['kind']!=('model'if role=='model'else'public')or \
               plan['original_nine_core_pins']!=compact['report']['original_nine_core_object_pins']or \
               plan['original_nine_core_paths']!=[x['path']for x in plan['original_nine_core_pins']]or \
               plan['original_ordered70_paths']!=[x['path']for x in compact['report']['original_ordered70_input_pins']]or \
               plan['original_four_archive_paths']!=[x for x in compact['report']['actual_complete70_link_inputs']if x.endswith('.a')]or \
               plan['original_compile_flags']!=c.FLAGS or plan['original_caps']!=compact['caps']:
                raise RuntimeError('parameterized control plan exact original core/order/caps and futureNone')
            c.verify_rows(sf['files']+sf['original_source_pins']+sf.get('dependencies',[]))
            if (sfpin if role=='model'else sf['candidate_fortran_source_freeze_pin'])!=compact['source_freeze_pin']:
                raise RuntimeError('control SF selects same compact production Source')
            compiler=compact['report']['records'][0]['command'][0]
            includes=['-I'+str(root/'build'),'-I'+str(Path(compact['object_pin']['path']).parent),*plan['original_compile_include_arguments']]
            compile_cmd=[compiler,*c.FLAGS,*includes,'-J'+str(root/'build'),'-c',plan['control_Source_pin']['path'],'-o',str(root/'build/control.o')]
            core=[] if role=='model'else list(plan['original_nine_core_paths'])
            if role=='public7':core[5]=compact['object_pin']['path']
            exe=str(root/'runtime/control_unqualified');link_cmd=[compiler,'-O2','-ffp-contract=off',str(root/'build/control.o'),*core,*plan['original_four_archive_paths'],'-o',exe]
            if d['records'][0]['command']!=compile_cmd or d['records'][1]['command']!=link_cmd or \
               d['actual_compile_command']!=compile_cmd or d['actual_link_command']!=link_cmd or \
               d['actual_link_core_paths']!=core or any(x not in compact['report']['actual_complete70_link_inputs']for x in core+plan['original_four_archive_paths']):
                raise RuntimeError('exact actual own control main/current production cores/archive commands')
            if role=='model':
                rows,lp=compact_log_rows(root,d['records'][2]);cases=d['actual_control_results']
                if d.get('actual_model_controls_passed')is not True or d.get('actual_seven_genuine_public_READ_controls_passed')is not False or \
                   d['records'][2]['command']!=[exe]or len(cases)!=1 or len(rows)!=1 or rows[0]!=cases[0]['actual_terminal']or \
                   rows[0].get('status')!='ACTUAL_COMPACT_GANLIB_MODEL_CONTROLS_ONLY'or type(rows[0].get('assertions'))is not int or rows[0]['assertions']!=36 or \
                   any(rows[0].get(k)is not False for k in ('physics_qualified','reader_qualified','AAA_qualified')):
                    raise RuntimeError('genuine private model assertions are not public qualification')
                models=cases[0]['actual_retained_model_file_pins'];c.verify_rows(models)
                if len(models)!=2 or [x['path']for x in models]!=[str(root/'model/C64-EXP'),str(root/'model/C64-ACT')]or \
                   models[0]['size_bytes']!=948232 or not models[0]['size_bytes']<models[1]['size_bytes']<=32*MI or \
                   models[0]['sha256']==models[1]['sha256']or any(x['identity'][3]!=1 for x in models):
                    raise RuntimeError('actual model compact948232 and complete retained independent files')
            else:
                phases=plan['planned_run_phases'];cases=d['actual_control_results'];stale=d['actual_stale_host_evidence']
                if d.get('actual_seven_genuine_public_READ_controls_passed')is not True or d.get('actual_model_controls_passed')is not False or \
                   len(phases)!=9 or len(cases)!=9 or len(stale)!=2:
                    raise RuntimeError('genuine7 public READ controls require9phases/two stale baselines')
                for declared,record,case in zip(phases,d['records'][2:],cases):
                    name,phase=declared['case'],declared['phase'];cmd=[exe,name]+([phase]if phase in ('prepare','read')else[])
                    rows,lp=compact_log_rows(root,record)
                    if record['command']!=cmd or len(rows)!=1 or rows[0]!=case['actual_terminal']or case['actual_log_pin']!=lp or \
                       rows[0].get('schema')!='GENUINE_PUBLIC_READ_COMPACT_BQ_ADMISSION_CONTROL_V1'or \
                       (rows[0].get('case'),rows[0].get('phase'))!=(name,phase)or rows[0].get('all_actual_assertions_completed')is not True or \
                       rows[0].get('synthetic_fixture')is not True or any(rows[0].get(k)is not False for k in \
                        ('private_matcher_used_as_assertion_oracle','physics_qualified','reader_qualified','AAA_qualified','ABA_admitted')):
                        raise RuntimeError('real public READ log/oracle scope and phase')
                    exact_counter_oracles(rows[0],declared,('expected_',))
                if {x['case']for x in stale}!={'public_read_stale_BQ_SRC','public_read_stale_BQ_MAC'}:
                    raise RuntimeError('exact two independent stale private stage refusals')
                for evidence in stale:
                    before=evidence['actual_before_manifest_pin'];value,checked=c.read_bound_json_current(before['path'],before)
                    name=evidence['case']
                    prepare_record=next(x for x in d['records']if x['command']==[exe,name,'prepare'])
                    read_record=next(x for x in d['records']if x['command']==[exe,name,'read'])
                    if value.get('schema')!='ACTUAL_PUBLIC_READ_STALE_BEFORE_FULL_EOF_SHA_ALL7_V1'or value.get('case')!=name or \
                       value.get('other_BQ_absent')is not True or value.get('genuine_prepare_child_closed0')is not True or \
                       value.get('actual_prepare_record')!=prepare_record or evidence.get('actual_read_record')!=read_record:
                        raise RuntimeError('two-phase stale baseline binds genuine prepare and read records')
                    if checked!=before or value['actual_bundle_pin']!=evidence['actual_bundle_before_pin']or \
                       value['actual_stale_pin']!=evidence['actual_stale_before_pin']or \
                       evidence['actual_bundle_before_pin']!=evidence['actual_bundle_after_pin']or \
                       evidence['actual_stale_before_pin']!=evidence['actual_stale_after_pin']or \
                       any(evidence.get(k)is not True for k in ('actual_two_files_full_EOF_SHA_all7_unchanged','actual_other_BQ_absent','genuine_read_child_closed0')):
                        raise RuntimeError('real same-file fullEOF stale baseline remains unchanged')
                    c.verify_rows([before,evidence['actual_bundle_after_pin'],evidence['actual_stale_after_pin']])
                    other='BQ64-MAC-ST'if evidence['case']=='public_read_stale_BQ_SRC'else'BQ64-SRC-ST'
                    op=root/evidence['case']/other
                    if op.exists()or op.is_symlink():raise RuntimeError('other stale BQ stage remains absent')
        fixed.extend([pd,pown,own['host_source']]+own['dependencies']+d['fixed_current_pins']+d['output_pins'])
        provenance[role]=dict(actual_report_pin=pd,actual_own_Host_freeze_pin=pown,
          exact_completed_record_count=count,old17_PASS_inherited=False,physics_qualified=False)
    return dict(fixed=unique(fixed),provenance=provenance)

'''

def pin(path):
    s=path.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    assert stat.S_ISREG(s.st_mode)and s.st_nlink==1
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:
        q=os.fstat(f.fileno());assert [q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]==before
        raw=f.read();q=os.fstat(f.fileno());assert [q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]==before
    s=path.lstat();assert [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before
    return raw,dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)

def write(path,raw):
    if isinstance(raw,str):raw=raw.encode()
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    return pin(path)[1]

def json_write(path,obj):return write(path,json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

def main():
    assert not NEW.exists(),'fresh Source-only draft namespace required'
    raw,oldpin=pin(OLD/'run_actual_three_plane_pipeline.py');text=raw.decode();changes=[]
    def replace(before,after,why):
        nonlocal text
        assert text.count(before)==1,(why,text.count(before));text=text.replace(before,after,1)
        changes.append(dict(reason=why,before=before,after=after))
    replace("actual-operator-global-BOOT-20261013-v14')","actual-operator-global-BOOT-20261013-v15')",'fresh literal output namespace only')
    replace(" 'BOOT_solve':{'maximum_live':['PROJECT','private solved archive','one same-plane Q','one MAC','remaining128MiB including empty final metadata'],\n               'upper_bound_bytes':(800+480+560+16+128)*MI},",
      " 'BOOT_solve':{'maximum_live':['PROJECT','private solved archive','one same-plane Q','one MAC','compact expected SRC32MiB','expected MAC16MiB','remaining128MiB including empty final metadata'],\n               'upper_bound_bytes':(800+480+560+16+32+16+128)*MI},",'strict2032MiB conditional forecast, original fresh2 unchanged')
    replace('    principal=0;aux=0;total=0;count=0;qs=[];macs=[];finals={}',
      '    principal=0;aux=0;total=0;count=0;qs=[];macs=[];finals={};bq=[];seen_paths=set()', 'scalar exact private BQ role state')
    replace("        rel=row['relative_path'];n=row['size_bytes'];count+=1",
      "        rel=row['relative_path'];n=row['size_bytes'];count+=1\n        if rel in seen_paths:raise RuntimeError('duplicate exact output inventory path')\n        seen_paths.add(rel)", 'reject duplicate role inventory entries')
    replace("        elif direct and name in ('closed_boot_axial.xsm','closed_boot_archive.xsm'):",
      "        elif name in ('BQ64-MAC-ST','BQ64-SRC-ST'):\n            if not direct or phase!='BOOT':raise RuntimeError('literal BOOT-only expected BQ stage role required')\n            cap=(16 if name=='BQ64-MAC-ST'else 32)*MI\n            if n>cap:raise RuntimeError('strict compact expected storage planning bound exceeded: '+name)\n            bq.append(name);principal+=n\n        elif direct and name in ('closed_boot_axial.xsm','closed_boot_archive.xsm'):", 'only literal32MiBSRC16MiBMAC principal roles')
    replace("    if aux+reserved_bytes>128*MI:raise RuntimeError('remaining runtime/context/log/meta storage planning bound128MiB')",
      "    if bq:\n        if set(bq)not in ({'BQ64-MAC-ST'},{'BQ64-MAC-ST','BQ64-SRC-ST'})or len(bq)!=len(set(bq))or len(qs)!=1 or macs!=qs:\n            raise RuntimeError('expected BQ stages require unique same-plane outer Q/MAC and MAC-first/SRC-first-close lifetime')\n        if seal_seen or payload or finals!={'closed_boot_axial.xsm':'empty','closed_boot_archive.xsm':'empty'}:\n            raise RuntimeError('expected BQ stages require canonical empty final pair and no seal')\n    if aux+reserved_bytes>128*MI:raise RuntimeError('remaining runtime/context/log/meta storage planning bound128MiB')", 'strict outerpair/blankfinal/seal/lifetime gate')
    replace("                final_payload_seen=bool(seal_seen or payload),", "                expected_BQ_stage_names=sorted(bq),\n                final_payload_seen=bool(seal_seen or payload),", 'report observedBQnames only no qualification')
    replace('def main():\n    p=argparse.ArgumentParser()',GATES+'def main():\n    p=argparse.ArgumentParser()', 'read-only new actual prerequisites, no child launch')
    replace("    for prefix in ['a1','a2','a3','build70','seventeen','source-freeze','host-freeze']:",
      "    for prefix in ['a1','a2','a3','build70','seventeen','source-freeze','host-freeze','new-build70','fresh-seventeen','private-model','public-read-seven']:", 'four real report triples, original six preserved')
    replace("COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V14", "COMPLETE_ACTUAL_AAA3_COMPACT_EXPECTED_PIPELINE_HOST_SOURCE_FREEZE_V15", 'distinct final owningHFschema')
    replace("    direct_binding_path=HERE/'DIRECT_ALIAS_ENTRY_BINDING.json'",
      "    cache_build=build;cache_build_pin=pbuild\n    compact=admit_compact_build(args,hf,helper,cache_build,cache_build_pin,old9)\n    build=compact['report'];pbuild=compact['report_pin']\n    current70_link=build['actual_complete70_link_inputs']\n    direct_binding_path=HERE/'DIRECT_ALIAS_ENTRY_BINDING.json'", 'retain cache history, select real newruntime70')
    replace("       direct_binding['selected_actual_build70_report_pin']!=pbuild or ",
      "       direct_binding['selected_actual_build70_report_pin']!=pbuild or \\\n+       direct_binding['actual_complete70_source_freeze_pin']!=compact['source_freeze_pin']or \\\n+       direct_original_inputs!=compact['current70_pins']or ", 'future finalbinding exact actual ordered70 fullpins withnewQ retained')
    replace("    seventeen,p17=c.admit17(args.seventeen_summary,args.seventeen_sha256,args.seventeen_seven_id,helper)",
      "    seventeen,p17=c.admit17(args.seventeen_summary,args.seventeen_sha256,args.seventeen_seven_id,helper)\n    controls=admit_compact_controls(args,hf,helper,compact,seventeen,p17)\n    compact_admission_provenance=dict(new_build70_report_pin=pbuild,new_BOOTQ_object_pin=compact['object_pin'],\n      compact_Fortran_Source_freeze_pin=compact['source_freeze_pin'],new_build_Host_freeze_pin=compact['build_Host_freeze_pin'],\n      actual_new_control_prerequisites=controls['provenance'],old17_is_historical_source_oracle_only=True,\n      production_core_replacement_one_based_slot=6,complete70_replacement_zero_based_index=40,\n      new_reader_prerequisites_genuinely_closed=True,physics_qualified=False)", 'admit three completed actual controls before any output namespace')
    replace("    fixed=unique(fixed+[phf,hf['host_source'],pbuild,p17,psf]+hf['dependencies']+sf['files']+",
      "    fixed=unique(fixed+compact['fixed']+controls['fixed']+[cache_build_pin]+cache_build['fixed_current_pins']+cache_build['output_pins']+\n                 [phf,hf['host_source'],pbuild,p17,psf]+hf['dependencies']+sf['files']+", 'explicit union old377/currentnewactualclosures without fakefuturepins')
    replace('    del build,current69,original69,seventeen,producer_reports,row,producer_fixed,sf,binding,native_sf',
      '    del compact,controls,cache_build\n    del build,current69,original69,seventeen,producer_reports,row,producer_fixed,sf,binding,native_sf', 'discard newly unused JSONs before unchanged originalGC')
    replace("          engineering_three_plane_closed0=False,", "          actual_compact_expected_reader_admission=compact_admission_provenance,\n          compact_expected_internal_disposal=dict(names=['BQ64-SRC-ST','BQ64-MAC-ST'],\n            source=hf['selected_new_Fortran_Source_freeze_pin'],private_READ_only=True,\n            independent_physical_EOF_pins_available=False,exact_raw_replay_retained=False,physics_qualified=False),\n          engineering_three_plane_closed0=False,", 'precise new internaldisposal scope with no rawEOFgrant')
    replace("          frozen_Fortran_internal_disposal=raw['frozen_Fortran_internal_disposal'],angular_moments_status='UNKNOWN',",
      "          frozen_Fortran_internal_disposal=raw['frozen_Fortran_internal_disposal'],\n          compact_expected_internal_disposal=raw['compact_expected_internal_disposal'],\n          actual_compact_expected_reader_admission=compact_admission_provenance,angular_moments_status='UNKNOWN',", 'summary actual prerequisite provenance, no physicsgrant')
    ast.parse(text)
    inverse=text
    for block in reversed(changes):
        assert inverse.count(block['after'])==1,block['reason'];inverse=inverse.replace(block['after'],block['before'],1)
    assert inverse.encode()==raw,'whole-file inverse must restore entirev14 bytes'
    # Original guarded50 body, its nested helpers, FirstFatal/observation and
    # original GC statements are unchanged continuous source bytes.
    start=raw.index(b'    try:\n        # Replace ONLY the main object')
    end=raw.index(b'        raw=dict(schema=')
    protected=raw[start:end];assert protected in text.encode()
    NEW.mkdir()
    hostpin=write(NEW/'run_actual_three_plane_pipeline.py',text)
    helpers=[]
    for name in ['actual_inputs_and_readback.py','direct_alias_entry_controls.f90','mutate_owned_control.f90']:
        b,old=pin(OLD/name);new=write(NEW/name,b);assert old['sha256']==new['sha256'];helpers.append(dict(original_pin=old,candidate_pin=new,whole_bytes_unchanged=True))
    original_binding=json.loads(pin(OLD/'DIRECT_ALIAS_ENTRY_BINDING.json')[0]);template=json.loads(json.dumps(original_binding))
    template['selected_actual_build70_report_pin']=None;template['actual_original_ordered_70_link_inputs']=None
    template['actual_complete70_source_freeze_pin']=None;template['new_probe_source']=str(NEW/'direct_alias_entry_controls.f90')
    template['original_actual_cache70_report_pin']=original_binding['selected_actual_build70_report_pin']
    template['Source_only_parameterized_template']=True;template['actual_pipeline_executed']=False
    templatepin=json_write(NEW/'DIRECT_ALIAS_ENTRY_BINDING.json',template)
    inversepin=json_write(NEW/'COMPLETE_V14_TO_V15_DRAFT_WHOLE_FILE_BYTE_INVERSE.json',dict(schema='COMPLETE_V14_TO_V15_DRAFT_WHOLE_FILE_BYTE_INVERSE_V1',original_pin=oldpin,candidate_pin=hostpin,changes=changes,restored_sha256=hashlib.sha256(inverse.encode()).hexdigest(),whole_restored_bytes_equal=True,original_guarded50_continuous_source_sha256=hashlib.sha256(protected).hexdigest(),original_guarded50_continuous_source_bytes=len(protected),original_guarded50_continuous_source_present_unchanged=True,helper_byte_equality=helpers,Source_only=True,Host_imported_or_executed=False))
    frozen_design_pin=pin(REC/'independent_v15_compact_BQ_full_pipeline_integration_design_20261013/REVIEW.json')[1]
    h14=json.loads(pin(OLD/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')[0])
    bhfpath=REC/'bq64_compact_expected_build_host_source_v3_20261013/COMPLETE_BQ64_COMPACT_EXPECTED_BUILD_HOST_SOURCE_FREEZE.json';bhfraw,bhfpin=pin(bhfpath);bhf=json.loads(bhfraw)
    plan=dict(schema='PARAMETERIZED_COMPACT_EXPECTED_FULL_PIPELINE_V15_SOURCE_ONLY_PLAN_V1',Source_only=True,Host_imported_or_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,original_v14_Host_pin=oldpin,original_v14_Host_freeze_pin=pin(OLD/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')[1],selected_independent_design_pin=frozen_design_pin,candidate_Host_pin=hostpin,whole_inverse_pin=inversepin,helper_byte_equality=helpers,direct_binding_parameterized_template_pin=templatepin,planned_output_root='/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v15',existing_cache70_report_pin=h14['selected_actual_build70_report'],existing_original_handle69_report_pin=h14['selected_original_actual69_handle_lifetime_report'],existing_original_v4_69_report_pin=h14['selected_original_actual69_v4_report'],existing_Fortran_pipeline_Source_freeze_pin=h14['selected_fortran_freeze'],existing_compact_Fortran_Source_freeze_pin=bhf['selected_new_Fortran_Source_freeze_pin'],existing_compact_build_Host_freeze_pin=bhfpin,original377_dependency_rows_to_retain=h14['dependencies'],mandatory_existing_external_prefixes=['a1','a2','a3','build70','seventeen','source-freeze','host-freeze'],mandatory_new_external_prefixes=['new-build70','fresh-seventeen','private-model','public-read-seven'],each_external_requires=['summary','sha256','seven-id'],future_actual_report_pins=dict(new_build70=None,fresh17=None,private_model=None,public7=None),future_actual_own_Host_freeze_pins=dict(fresh17=None,private_model=None,public7=None,v15=None),future_actual_object_pin=None,future_actual_module_pins=None,future_actual_Dragon_pin=None,future_actual_v15_CLI_pin=None,future_actual_v15_reports=None,actual_prerequisite_counts=dict(build2=2,fresh17=20,model=3,public7=11),original_pipeline_records_expected=dict(total=50,PASS=17,expected_refusal=33),strict_forecast_MiB=dict(BOOT_solve=2032,BOOT_seal=1888,aux=128,fresh=2048),original_caps=bhf['original_caps'],future_final_preparation_obligations=['Root must independently attest four real actual terminal tools integer0/exactargv/actualfullreportPF before finalHF freeze; no Source preparation tool0 counts as businesssuccess','Copy only exact unchanged Host/threehelpers to finalSource dir; actual template binding must be instantiated from real newbuild ordered70 fullpins; current draftNone cannot pass','Freeze real ownHF/SourceSF/commands and four report closures; measure actualdependency count rather than predict','Retain original377 unchanged and old original69/cache70/17 science/math authority as historical sources','Root/independent peer Source review and genuine trueTool receipts enter finalHF explicitdeps; no futurepipelineHF/CLI now'],new_reader_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    plan['future_corrected_Common_Source_pin']=None
    plan['future_corrected_Common_catalog_pin']=None
    plan['pending_exact_catalog10_historical_migration']=True
    plan['current_Common_literal_is_original_v14_inverse_baseline_not_final_runtime_admission']=True
    plan['future_final_preparation_obligations'].append('Root must provide real corrected Common path/PF and exact10 catalog migration evidence; no skipmissing or catalog widening; final source may need a sole Common literal replacement in a new draft version')
    planpin=json_write(NEW/'PARAMETERIZED_V15_ACTUAL_PREREQUISITE_ADMISSION_PLAN.json',plan)
    ready=json_write(NEW/'SOURCE_REVIEW_READY.json',dict(schema='COMPACT_EXPECTED_V15_HOST_DRAFT_SOURCE_REVIEW_READY_V1',status='SOURCE_ONLY_DRAFT_NOT_RUNTIME_OR_READER_QUALIFIED',candidate_Source_pin=hostpin,parameterized_plan_pin=planpin,whole_inverse_pin=inversepin,helpers=helpers,direct_binding_template_pin=templatepin,source_change_block_count=len(changes),original_v14_full_bytes_inverse=True,original50_continuous_body_unchanged=True,failure=None,business_executed=False,compiler_executed=False,files_deleted=False,actual_Host_freeze_pin=None,actual_CLI_pin=None,pending_corrected_Common_Source_pin=None,runtime_ready=False))
    print(json.dumps(dict(status='SOURCE_ONLY_V15_DRAFT_CREATED_NO_EXECUTION',candidate_Source_pin=hostpin,plan_pin=planpin,inverse_pin=inversepin,ready_pin=ready,change_block_count=len(changes),business_executed=False,all_future_actual_report_pins_None=True),ensure_ascii=False))

if __name__=='__main__':main()
