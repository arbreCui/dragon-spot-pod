"""UNREADY explicit B capture core for a future separately admitted Root host.

Root must acquire its exclusive claim before any EOF/check/import, install the
unaltered private original OwnRSS runner and full latest cumulative Resource
binding, and independently admit new IO build/publication before calling this.
No main performs business or Source-generation. The collector keeps original
v10 event header arithmetic and traversal; only four output basenames change.
"""
import importlib.util
import json
import os
from pathlib import Path
import struct
import sys

BASE=Path(__file__).absolute().parent
B_PRODUCT_NAMES=('m.xsm','u.asc','a.asc','t.asc')
FUTURE=dict(three_plane_qualified=False,GLOBAL_qualified=False,rank_qualified=False,
 online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,
 historical_unsaved_context_recovered=False,reaction_multiplicity_qualified=False,
 physical_neutron_balance_qualified=False,coupled_370group_reference_qualified=False,
 scientific_accuracy_qualified=False)
LABELS={'LIBMIX_BEFORE','LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION',
 'LIBMIX_AFTER','TONDRV_AFTER_REAL_MAT_ELIMINATION','TONDRV_ACTUAL_FINAL_LIBMIX_MASK',
 'TONSPH_BEFORE_ACTUAL_TONCMI','TONDRV_ACTUAL_SPH_CALL_DECISION','TONDRV_FINAL_AFTER_SHIBA'}
ROLE_LABELS={'LIBMIX_BEFORE':'oldmacro-pre-LIBMIX','LIBDEN_OLD_CONTEXT':'oldmacro-LIBDEN',
 'LIBMIX_AFTER':'postmacro-LIBMIX','TONDRV_FINAL_AFTER_SHIBA':'final-complete-micro'}
_ROOT_FULLPIN=None

def require(ok,message):
    if type(ok)is not bool or not ok:raise RuntimeError(message)

def fullpin(path,budget):
    require(_ROOT_FULLPIN is not None,'only actual owning Root installs fullEOF callback')
    return _ROOT_FULLPIN(path,budget)

def collect_state(folder,state,deck_pin,exe_pin,stage,budget):
    # Read headers in actual consecutive event number order, never native record
    # sorting. Every full event file reaches EOF in fullpin/extract_event.
    files={p.name:p for p in folder.glob('axobs-*')};events=[];snapshots=[];contexts=[];number=1;last_libmix=0;closed=[];all_observer_names=set()
    while True:
        name='axobs-'+format(number,'06d')+'.context.bin'
        if name not in files:break
        path=files[name];pp=fullpin(path,budget)
        with path.open('rb')as stream:
            require(stream.read(8)==b'AXOBSCTX','whole observer magic')
            raw=stream.read(16);require(len(raw)==16,'actual full event header');version,event,libmix,length=struct.unpack('<4i',raw)
            require(version==2 and event==number and libmix>=last_libmix and 1<=length<=256,'actual consecutive AXOBSCTXv2 event/libmix header')
            label=stream.read(length).decode('ascii');require(label in LABELS,'no unknown/omitted observer event')
        role=ROLE_LABELS.get(label);snapshot=None;all_observer_names.add(name);contexts.append(pp)
        if role is not None:
            n='axobs-'+format(event,'06d')+'-'+role+'.xsm'
            if n in files:
                snapshot=fullpin(files[n],budget);all_observer_names.add(n);snapshots.append(dict(event=event,role=role,root_prefix=[],logical_prefix=[]if role=='final-complete-micro'else['MACROLIB'],input_pin=snapshot))
            else:require(role not in('postmacro-LIBMIX','final-complete-micro'),'every postmacro and actual final micro snapshot mandatory')
        if label=='LIBMIX_BEFORE':require(libmix==last_libmix+1,'every actual LIBMIX begin counted')
        events.append(dict(event=event,libmix=libmix,label=label,complete_context_pin=pp,snapshot_role=role,actual_snapshot_pin=snapshot,actual_native_snapshot_root_prefix=[]if snapshot is not None else None,snapshot_logical_prefix=([]if role=='final-complete-micro'else['MACROLIB'])if snapshot is not None else None,actual_old_macro_absent_at_event=(role is not None and snapshot is None)))
        last_libmix=libmix;number+=1
    require(events and set(files)==all_observer_names,'full actual observer namespace no holes/unknown/leftover entries')
    require(any(e['label']=='TONDRV_FINAL_AFTER_SHIBA'for e in events)and any(e['label']=='TONDRV_ACTUAL_SPH_CALL_DECISION'for e in events),'complete final snapshot and true/false SPH decision events required')
    # The existing full context parser is separately bound/read by the context
    # host. Production manifest retains all bytes and original order now.
    outputs=[]
    for name in B_PRODUCT_NAMES:outputs.append(fullpin(folder/name,budget))
    return dict(state=state,actual_material_deck_pin=deck_pin,actual_executable_pin=exe_pin,actual_genuine_material_stage=stage,actual_material_product_pins=outputs,actual_all_event_headers_in_original_execution_order=events,complete_context_pins=contexts,complete_state_snapshot_inputs=snapshots,legacy_context_source_snapshot_request_rows=[dict(event=item['event'],role=item['role'],root_prefix=item['logical_prefix'],input_pin=item['input_pin'])for item in snapshots],legacy_context_root_prefix_semantics='output_pool_logical_path_prefix_only_not_native_directory_lookup',actual_native_snapshot_root_prefix=[],selected_last_libmix_number=last_libmix,all_actual_events_and_snapshots_saved=True,actual_material_child_closed_before_manifest=True,all_producer_file_handles_closed_before_next_state=True,new_final_micro_from_actual_TONDRV_observer=True,native_snapshot_api_or_memory_bits_qualified=False,**FUTURE)


def execute_B_with_original_runner(runner,full,production,resources,binding,binding_pin,
                                   seed,seed_pin,Root_fullpin,Root_recheck,budget):
    global _ROOT_FULLPIN
    require(binding['entry_mode']=='Root'and binding['actual_Root_PID']==os.getpid()and
      binding['business_admission_complete']is True,'separate real Root business admission')
    # The caller's exclusive xb claim is created BEFORE all entry checks/EOFs.
    Root_recheck(binding['exclusive_Root_claim_pin'],budget)
    require(type(runner)is full.OwnRSSSerialExecutor and
      full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and
      runner.resources is resources and runner.work==Path(binding['actual_output_root'])and
      Path(full.__file__).absolute()==Path(binding['original_OwnRSS_Source_pin']['path'])and
      Path(production.__file__).absolute()==Path(binding['original_SerialExecutor_Source_pin']['path'])and
      Path(runner.bounded.__file__).absolute()==Path(binding['owned_original_bounded_Source_pin']['path']),
      'exact private original MRO/Source/resources/bounded watchdog binding')
    for key in('original_OwnRSS_Source_pin','original_SerialExecutor_Source_pin',
                'owned_original_bounded_Source_pin'):
        Root_recheck(binding[key],budget)
    helper=BASE/'B_original_input_binding.UNREADY.py'
    source_table={p['path']:p for p in binding['execution_Source_pins']}
    require(str(helper)in source_table and str(Path(__file__).absolute())in source_table,
      'full own Source and role helper')
    for p in source_table.values():Root_recheck(p,budget)
    spec=importlib.util.spec_from_file_location('bound_B_route_for_Root',helper)
    route=importlib.util.module_from_spec(spec);spec.loader.exec_module(route)
    Root_recheck(source_table[str(helper)],budget)
    route.validate_B_binding(binding,seed,seed_pin)
    route.require_output_reserve(binding['complete_latest_prefix_roots'],binding['actual_output_root'],
      binding['prospective_existing_joint_bytes'],binding['context_tree_extraction_reserve_bytes'],
      binding['new_build_reserve_bytes'])
    # Only Root performs the original blind whole-input checks, not any peer.
    fixed=[r['input_pin']for r in binding['original_B_native_stage_inputs']]
    fixed+=list(binding['actual_consumed_readonly_cwd_role_pins'].values())
    fixed+=[binding['new_IO_runtime_pin'],binding['derived_B_material_deck_pin'],binding_pin,seed_pin]
    for p in fixed:Root_recheck(p,budget)
    before=route.snapshot_old_cwd_current7()
    require(before==binding['all_old_cwd_entries_current7_before_child'],'pre-child old cwd inventory')
    _ROOT_FULLPIN=Root_fullpin
    output=Path(binding['actual_observation_directory']);directory=output/'native'
    require(directory.is_dir()and not directory.is_symlink(),'owned original guard stage already created')
    command=[sys.executable,str(BASE/'exec_original_B_in_fresh_IO.UNREADY.py'),
      '--binding-pin',json.dumps(binding_pin,separators=(',',':'),allow_nan=False),
      '--expected-parent-pid',str(os.getpid())]
    require(len(runner.records)==0,'one actual B material child, no retry/prior stage reuse')
    resources.check();budget()
    native_error=None;after_errors=[]
    try:
        runner.execute(directory,'material',command,600,
          marker='AXMAT-MATERIAL-B-COMPLETE',deck=binding['derived_B_material_deck_pin']['path'])
    except BaseException as error:native_error=error
    # The original runner retains the actual stage/monitor return. Closing
    # Source/input/cwd checks run even on its nonzero; never turn it into PASS.
    for p in fixed+list(source_table.values()):
        try:Root_recheck(p,budget)
        except BaseException as error:after_errors.append(repr(error))
    for closing in (lambda:route.recheck_old_cwd_current7(before),resources.check,budget):
        try:closing()
        except BaseException as error:after_errors.append(repr(error))
    if native_error is not None:
        native_error.B_IO_after_check_errors=after_errors
        raise native_error
    require(not after_errors,'post-child Source/input/cwd/resource failures '+repr(after_errors))
    record=dict(runner.records[-1]);require(record['status']=='PASS','original guard closed B child0')
    state=collect_state(output,'B',binding['derived_B_material_deck_pin'],
      binding['new_IO_runtime_pin'],record,budget)
    require(len(state['complete_context_pins'])==55 and len(state['complete_state_snapshot_inputs'])==8,
      'actual full B55events/8trees required; no reduced capture')
    for p in fixed:Root_recheck(p,budget)
    for p in source_table.values():Root_recheck(p,budget)
    route.recheck_old_cwd_current7(before)
    state.update(current_B_case_input_binding_pin=binding_pin,
      original_B_material_deck_pin=binding['original_B_material_deck_pin'],
      actual_native_cwd=binding['actual_native_cwd'],actual_stage_cwd=str(directory),
      actual_observation_directory=str(output),actual_stage_label=record['label'],actual_command=command,
      physical_input_pins=fixed,complete_observed_file_pins=state['complete_context_pins']+
        [row['input_pin']for row in state['complete_state_snapshot_inputs']],
      all_old_cwd_entries_current7_before=before,all_old_cwd_entries_current7_after=route.snapshot_old_cwd_current7(),
      source_and_input_before_after_checks_completed=True)
    return state,record


def make_B_manifest(state,binding,binding_pin,actual_owning_report_pin):
    require(state['state']=='B'and state['current_B_case_input_binding_pin']==binding_pin,
      'original B capture state, not A state replacement')
    state=dict(state,actual_owning_report_pin=actual_owning_report_pin)
    return dict(schema='ACTUAL_CURRENT_FORMAL_COMPLETE_OBSERVATION_MANIFEST_V1',
      current_case_spec_pin=binding['current_case_spec_pin'],state_order=['B'],states={'B':state},
      current_B_case_input_binding_pin=binding_pin,
      observation_scope='ONE_CURRENT_ORIGINAL_B_MATERIAL_CONSTRUCTION_FULL_CONTEXT_NOT_A_RELABELLING',
      actual_B_observation_executed=True,actual_A_observation_executed=False,
      three_recaptured_plane_histories_claimed=False,original_caps=binding['original_caps'],
      all_original_input_libraries_retained=True,library_copy_created=False,**FUTURE)
