#!/usr/bin/env python3
"""One fresh actual A material observation, no old context reconstruction.

This independent current entry retains the entire original six-function
shared-input/capture implementation. Numerical TONE/decks and every original
observation/math source are unchanged. Root supplies real build and Source
freeze pins. No captured value or actual output SHA is predicted at Source time.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import time

R=Path('/Users/wen/spot')
REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
COMMON=REC/'post_literal3_old_pack_current_catalog_common_source_v1_20261014/guarded_warm_A_common.py'
spec=importlib.util.spec_from_file_location('current_material_original_guard_common',COMMON)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
from current_material_prerequisite_admission import replace_owned_failure_summary,check_original_host_limits

def require(ok,message):
    if type(ok)is not bool or not ok:raise RuntimeError(message)

def fullpin(path,budget=lambda:None):
    budget();value=c.pin(path);budget();return value

def recheck(p,budget=lambda:None):
    budget();value=c.same_pin(p['path'],p);budget();return value

FUTURE=c.scope()|dict(historical_unsaved_context_recovered=False,
  reaction_multiplicity_qualified=False,physical_neutron_balance_qualified=False,
  coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False)
LABELS={'LIBMIX_BEFORE','LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION',
 'LIBMIX_AFTER','TONDRV_AFTER_REAL_MAT_ELIMINATION','TONDRV_ACTUAL_FINAL_LIBMIX_MASK',
 'TONSPH_BEFORE_ACTUAL_TONCMI','TONDRV_ACTUAL_SPH_CALL_DECISION','TONDRV_FINAL_AFTER_SHIBA'}
ROLE_LABELS={'LIBMIX_BEFORE':'oldmacro-pre-LIBMIX','LIBDEN_OLD_CONTEXT':'oldmacro-LIBDEN',
 'LIBMIX_AFTER':'postmacro-LIBMIX','TONDRV_FINAL_AFTER_SHIBA':'final-complete-micro'}
SHARED_INPUT_LIBRARY_LAYOUT={'schema': 'COMPLETE_AB_SINGLE_COPY_ORIGINAL_SHARED_LIBRARIES_AND_EXACT_PROCEDURE_FILE_LITERALS_V1', 'shared_directory': 's', 'state_order': ['A', 'B'], 'seed_destination_order': ['material.x2m', 'AxMatTone.c2m', 'geometry.dat', 'rnr_cc.c2m', 'rnr_interpol.c2m', 'DLIB_ACTUAL', 'DLIB8R1_370'], 'original_procedure_copy_name': 'AxMatTone.c2m.original', 'literal_replacements': [{'original': "FIL: 'DLIB_ACTUAL'", 'derived': "FIL: '../s/A'", 'count': 2}, {'original': "FIL: 'DLIB8R1_370'", 'derived': "FIL: '../s/B'", 'count': 1}], 'physical_file_names': {'DLIB_ACTUAL': 'A', 'DLIB8R1_370': 'B'}}

def original_shared_libraries(b):
    libraries={}
    for state in ('A','B'):
        for row in b['states'][state]['native_stage_inputs']:
            if row['destination']in('DLIB_ACTUAL','DLIB8R1_370'):
                previous=libraries.get(row['destination'])
                require(previous is None or previous==row['input_pin'],'same complete original library source for A and B')
                libraries[row['destination']]=row['input_pin']
    require(list(libraries)==['DLIB_ACTUAL','DLIB8R1_370'],'both complete original library roles ordered')
    return libraries


def prepare_shared_libraries(out,b,budget):
    shared=out/SHARED_INPUT_LIBRARY_LAYOUT['shared_directory'];require(not os.path.lexists(shared),'fresh one-copy original library directory');shared.mkdir()
    originals=original_shared_libraries(b);copies={}
    for name,p in originals.items():
        recheck(p,budget);dest=shared/SHARED_INPUT_LIBRARY_LAYOUT['physical_file_names'][name]
        with Path(p['path']).open('rb')as src,dest.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
        actual=fullpin(dest,budget);require(actual['sha256']==p['sha256']and actual['size_bytes']==p['size_bytes'],'entire original library copied once without aliases');copies[name]=actual;recheck(p,budget)
    return dict(schema='ACTUAL_AB_SINGLE_COPY_COMPLETE_ORIGINAL_LIBRARY_EVIDENCE_V1',original_input_pins=originals,shared_copy_pins=copies,material_input_layout=SHARED_INPUT_LIBRARY_LAYOUT,shared_library_directory=str(shared),all_library_bytes_preserved_without_symlinks_or_hardlinks=True,actual_state_library_full_EOF_observations={})


def recheck_shared_libraries(shared,budget):
    originals={name:recheck(p,budget)for name,p in shared['original_input_pins'].items()}
    copies={name:recheck(p,budget)for name,p in shared['shared_copy_pins'].items()}
    return dict(original_library_full_EOF_pins=originals,shared_library_full_EOF_pins=copies)


def derive_original_procedure(raw):
    require(type(raw)is bytes and len(raw)<=2**20,'small complete pinned procedure Source only')
    result=raw
    for row in SHARED_INPUT_LIBRARY_LAYOUT['literal_replacements']:
        old=row['original'].encode('ascii');new=row['derived'].encode('ascii')
        require(raw.count(old)==row['count']and raw.count(new)==0 and len(new.split(b"'")[1])<=12,'all and only original FIL literal occurrences fit actual LIBLIC and LIBSUB NAMFIL(:12)')
        result=result.replace(old,new)
    restored=result
    for row in SHARED_INPUT_LIBRARY_LAYOUT['literal_replacements']:
        old=row['original'].encode('ascii');new=row['derived'].encode('ascii');require(restored.count(new)==row['count'],'derived complete FIL occurrence count');restored=restored.replace(new,old)
    require(restored==raw,'entire procedure reverse replacement exactly original Source bytes')
    return result


def copy_state_seeds(folder,seeds,shared,budget):
    require([row['destination']for row in seeds]==SHARED_INPUT_LIBRARY_LAYOUT['seed_destination_order'],'all seven original seed roles in original order')
    copies=[];mapping=[];procedure=None
    for row in seeds:
        p=row['input_pin'];name=row['destination'];recheck(p,budget);original_procedure_pin=None
        if name in('DLIB_ACTUAL','DLIB8R1_370'):
            require(p==shared['original_input_pins'][name],'same original library role source');actual=recheck(shared['shared_copy_pins'][name],budget)
        else:
            dest=folder/name;require(not os.path.lexists(dest),'fresh material seed Source')
            if name=='AxMatTone.c2m':
                original=folder/SHARED_INPUT_LIBRARY_LAYOUT['original_procedure_copy_name'];require(not os.path.lexists(original),'fresh retained complete original procedure')
                with Path(p['path']).open('rb')as src,original.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
                original_procedure_pin=fullpin(original,budget);require(original_procedure_pin['sha256']==p['sha256']and original_procedure_pin['size_bytes']==p['size_bytes'],'complete original procedure independently retained')
                raw=original.read_bytes();derived=derive_original_procedure(raw)
                with dest.open('xb')as dst:dst.write(derived)
                actual=fullpin(dest,budget)
                procedure=dict(schema='ACTUAL_COMPLETE_ORIGINAL_PROCEDURE_THREE_FIL_LITERAL_PATH_REPLACEMENTS_V1',original_input_pin=p,retained_original_procedure_pin=original_procedure_pin,actual_consumed_derived_procedure_pin=actual,original_complete_ASCII_Source=raw.decode('ascii'),derived_complete_ASCII_Source=derived.decode('ascii'),exact_literal_replacements=SHARED_INPUT_LIBRARY_LAYOUT['literal_replacements'],whole_reverse_replacement_equals_original_bytes=True,all_numeric_and_non_FIL_Source_bytes_unchanged=True,actual_genuine_material_CWD=str(folder),relative_shared_library_targets={name:str((folder/('../s/'+SHARED_INPUT_LIBRARY_LAYOUT['physical_file_names'][name])).resolve())for name in shared['shared_copy_pins']},ILIBRARYNAME_filename_provenance_changes_are_preserved_not_claimed_equal=True)
                require(procedure['relative_shared_library_targets']=={name:p['path']for name,p in shared['shared_copy_pins'].items()},'actual A/B relative file paths resolve only to original shared copies')
            else:
                with Path(p['path']).open('rb')as src,dest.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
                actual=fullpin(dest,budget);require(actual['sha256']==p['sha256']and actual['size_bytes']==p['size_bytes'],'all other original seed Source bytes unchanged')
        copies.append(actual);mapping.append(dict(destination=name,original_input_pin=p,actual_consumed_pin=actual,retained_original_procedure_pin=original_procedure_pin))
        recheck(p,budget)
    require(procedure is not None,'complete original and actual consumed procedure evidence')
    copies.append(procedure['retained_original_procedure_pin'])
    return copies,mapping,procedure


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
    for name in('material.xsm','microlib.ascii','macro.ascii','metadata.ascii'):outputs.append(fullpin(folder/name,budget))
    return dict(state=state,actual_material_deck_pin=deck_pin,actual_executable_pin=exe_pin,actual_genuine_material_stage=stage,actual_material_product_pins=outputs,actual_all_event_headers_in_original_execution_order=events,complete_context_pins=contexts,complete_state_snapshot_inputs=snapshots,legacy_context_source_snapshot_request_rows=[dict(event=item['event'],role=item['role'],root_prefix=item['logical_prefix'],input_pin=item['input_pin'])for item in snapshots],legacy_context_root_prefix_semantics='output_pool_logical_path_prefix_only_not_native_directory_lookup',actual_native_snapshot_root_prefix=[],selected_last_libmix_number=last_libmix,all_actual_events_and_snapshots_saved=True,actual_material_child_closed_before_manifest=True,all_producer_file_handles_closed_before_next_state=True,new_final_micro_from_actual_TONDRV_observer=True,native_snapshot_api_or_memory_bits_qualified=False,**FUTURE)


def release_closed_owned_library_copies(out,shared,states,records,fixed,budget):
    """One closed-stage lifecycle; original libraries and all results survive.

    Complete real group census and strict own-host lsof observation precede
    any unlink. This is separate evidence, not inherited monitoring authority.
    A missing process/stream/tool observation refuses release. No library copy
    is put into the following live fixed input set after its explicit release.
    """
    table={p['path']:p for p in fixed};ps='/bin/ps';lsof='/usr/sbin/lsof'
    require(ps in table and lsof in table,'both real process metadata tools fully pinned')
    recheck(table[ps],budget);recheck(table[lsof],budget)
    require(records and all(r['status']=='PASS'for r in records),'only all closed actual stages may release private input copies')
    groups=[]
    for record in records:
        watch=Path(out)/(record['label']+'.watchdog.json')
        value=json.loads(watch.read_text())
        require(value['returncode']==0 and value['limit_failure']is None and
          value['command']==record['command']and value['liveness_group_cleanup']is True,
          'actual owning stage closed0 watch before independent census')
        require(type(value['pid'])is int and value['pid']>1,'actual process group identity')
        groups.append(value['pid'])
    census=subprocess.run([ps,'-axo','pid=,ppid=,pgid=,stat='],capture_output=True,text=True,timeout=2)
    require(census.returncode==0 and len(census.stdout)<8*2**20 and len(census.stderr)<8*2**20,
      'full finite actual process census')
    rows=[]
    for line in census.stdout.splitlines():
        words=line.split();require(len(words)==4 and all(w.isdigit()for w in words[:3]),'complete PS row')
        rows.append([int(w)for w in words[:3]]+[words[3]])
    require(not any(r[0]in groups or r[2]in groups for r in rows),'no surviving or reused actual producer PID/group')
    observed=subprocess.run([lsof,'-nP','-F','pfnsiDt','-a','-p',str(os.getpid())],
      capture_output=True,text=True,timeout=2)
    require(observed.returncode==0 and len(observed.stdout)<8*2**20 and len(observed.stderr)<8*2**20,
      'strict lsof0 finite full own-host stream')
    pids=[int(line[1:])for line in observed.stdout.splitlines()if line.startswith('p')and line[1:].isdigit()]
    require(pids==[os.getpid()],'full exact sole owner lsof coverage')
    directory=Path(shared['shared_library_directory'])
    require(directory==out/'s'and directory.is_dir()and not directory.is_symlink(),
      'own fresh library directory only')
    require(not any(line.startswith('n'+str(directory)+'/')for line in observed.stdout.splitlines()),
      'no own-host descriptor holds an original or unlinked shared copy')
    original=recheck_shared_libraries(shared,budget)
    for state in states.values():
        for p in state['complete_observed_file_pins']+state['actual_material_product_pins']:recheck(p,budget)
        procedure=state['actual_procedure_three_literal_inverse']
        recheck(procedure['retained_original_procedure_pin'],budget)
        recheck(procedure['actual_consumed_derived_procedure_pin'],budget)
        require(procedure['whole_reverse_replacement_equals_original_bytes']is True and
          procedure['all_numeric_and_non_FIL_Source_bytes_unchanged']is True,'actual consumed original math/procedure full inverse')
    before=[]
    for name,p in shared['shared_copy_pins'].items():
        require(Path(p['path'])==directory/SHARED_INPUT_LIBRARY_LAYOUT['physical_file_names'][name] and p['sha256']==shared['original_input_pins'][name]['sha256']and
          p['size_bytes']==shared['original_input_pins'][name]['size_bytes'],'one complete owned same-byte copy role')
        before.append(recheck(p,budget))
    receipt=dict(schema='ACTUAL_CLOSED_PRIVATE_MATERIAL_INPUT_COPY_RELEASE_V1',
      original_live_input_pins=shared['original_input_pins'],owned_copy_pins_before_release=before,
      actual_observed_stable_libraries_after_capture=original,actual_closed_stage_records=records,
      actual_PS_argv=census.args,actual_PS_stdout=census.stdout,actual_PS_stderr=census.stderr,
      actual_PS_returncode=census.returncode,actual_lsof_argv=observed.args,
      actual_lsof_stdout=observed.stdout,actual_lsof_stderr=observed.stderr,actual_lsof_returncode=observed.returncode,
      actual_tool_pins=[table[ps],table[lsof]],all_results_contexts_native_observations_retained=True,
      total_owned_bytes_released=0,all_owned_copy_paths_absent_after_release=False,**FUTURE)
    for p in before:
        recheck(p,budget);Path(p['path']).unlink();require(not os.path.lexists(p['path']),'actual private copy absent after release')
        receipt['total_owned_bytes_released']+=p['size_bytes']
    for p in shared['original_input_pins'].values():recheck(p,budget)
    recheck(table[ps],budget);recheck(table[lsof],budget)
    receipt['all_owned_copy_paths_absent_after_release']=True
    target=out/'ACTUAL_CLOSED_OWNED_LIBRARY_COPY_RELEASE.json';c.write(target,receipt)
    return fullpin(target,budget),{p['path']for p in before}


def main():
    parser=argparse.ArgumentParser(allow_abbrev=False)
    roles=['original-phase','original-Root-tools','original-Root-argv','original-host-freeze','original-CLI','failed-post','failed-post-tools','continuation-host-freeze']
    for role in roles:
        for suffix in ['summary','sha256','seven-id']:parser.add_argument('--'+role+'-'+suffix,required=True)
    parser.add_argument('--output-dir',required=True)
    args=parser.parse_args();start=time.monotonic();pins={};data={}
    for role in roles:
        key=role.replace('-','_');data[role],pins[role]=c.load_json_exact(getattr(args,key+'_summary'),getattr(args,key+'_sha256'),getattr(args,key+'_seven_id'))
    d=data['original-phase'];root=data['original-Root-tools'];ra=data['original-Root-argv'];oldhf=data['original-host-freeze'];cli=data['original-CLI'];post=data['failed-post'];pt=data['failed-post-tools'];hf=data['continuation-host-freeze']
    import copy,hashlib,shlex,sys,stat
    q=root['actual_terminal_return']
    require(root['observed_closed']is True and type(root['original_integer_exit_code'])is int and root['original_integer_exit_code']==1 and type(q['exit_code'])is int and q['exit_code']==1 and q.get('session_id')is None,'original actual Root1 retained')
    require(shlex.split(root['exact_executed_command'])==ra['exact_argv']==cli['exact_argv']and len(ra['exact_argv'])==32 and ra['actual_CLI_pin']==pins['original-CLI']and ra['actual_Host_freeze_pin']==pins['original-host-freeze']and cli['Host_freeze_pin']==pins['original-host-freeze'],'original genuine exact32/HF/CLI')
    require(d['schema']=='ACTUAL_CURRENT_FORMAL_A_MATERIAL_OBSERVATION_EXECUTION_V1'and d['status']=='FAILED_CURRENT_OBSERVATION_NO_RETRY'and d['failure']=='RuntimeError: both real process metadata tools fully pinned'and d['actual_closed_owned_library_copy_release_pin']is None and d['actual_full_A_observation_executed']is False and len(d['records'])==1 and d['records'][0]['status']=='PASS','only original post-stage process-tool omission; not material retry')
    require(post['schema']=='INDEPENDENT_MATERIAL_FIRST_A_SHORT_FIL_V10_ACTUAL_OBSERVATION_POSTVERIFICATION_V1'and post['status']=='PASS_ACTUAL_MATERIAL_FIRST_A_SHORT_FIL_V10_STAGE0_CAPTURE_RELEASE_BLOCKED_FACTUAL_POSTVERIFICATION'and post['failure']is None and post['actual_material_stage_closed0']is True and post['actual_stage_statuses']==['PASS']and post['actual_context_collection_source_function_verified']is True,'required actual cached collection factual post0')
    canonical={'actual_report_pin':pins['original-phase'],'actual_Host_freeze_pin':pins['original-host-freeze'],'actual_CLI_pin':pins['original-CLI'],'actual_Root_true_tool_return_pin':pins['original-Root-tools'],'actual_Root_argv_pin':pins['original-Root-argv']}
    require(all(post[k]==v for k,v in canonical.items())and all(post[k]is False for k in ['business_executed','compiler_executed','numerical_executed','files_deleted'])and post['actual_observation_manifest_pin']is None and post['actual_closed_owned_library_copy_release_pin']is None,'five real authorities; original no manifest/release')
    require(pt['observed_closed']is True and type(pt['original_integer_exit_code'])is int and pt['original_integer_exit_code']==0,'factual post observed closed0')
    for k in ['actual_review_return','actual_postverification_return']:
        z=pt[k];require(type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'].strip().splitlines()[-1])['review_pin']==pins['failed-post'],'genuine post original integer0/stdoutPF')
    require(hf['schema']=='COMPLETE_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_HOST_SOURCE_ONLY_FREEZE_V1'and hf['host_source']==c.pin(Path(__file__).absolute())and hf['selected_original_failed_phase_pin']==pins['original-phase']and hf['selected_original_failed_post_pin']==pins['failed-post']and hf['selected_original_Host_freeze_pin']==pins['original-host-freeze']and hf['Dragon_rerun_permitted']is False,'explicit own continuation Source binding')
    owner=Path(pins['original-phase']['path']).parent;out=Path(args.output_dir)
    require(str(owner)==cli['output_root']and out.is_absolute()and out.parent==c.ART and not os.path.lexists(out)and not out.is_relative_to(owner)and not owner.is_relative_to(out),'fresh separate reports; original owner unchanged')
    require(ra['exact_argv'][-2:]==['--output-dir',str(owner)]and d['actual_B_observation_executed']is False and d['three_recaptured_plane_histories_claimed']is False,'actual original A only')
    def current7(p):
        path=Path(p['path']);s=path.lstat()
        require(stat.S_ISREG(s.st_mode)and not any(a.is_symlink()for a in [path,*path.parents])and c.identity(path)==p['identity'],'selected live current7; no generic historical skip')
    for p in hf['dependencies']:current7(p)
    original_source=Path(oldhf['host_source']['path']);c.same_pin(original_source,oldhf['host_source'])
    for field in ['original_release_function_Source','original_collect_function_Source']:
        require(hf[field]['source_pin']==oldhf['host_source'],'original function Source')
    supportspec=importlib.util.spec_from_file_location('continuation_original_support',c.SUPPORT);support=importlib.util.module_from_spec(supportspec);supportspec.loader.exec_module(support)
    require(c.pin(c.SUPPORT)['sha256']==c.SUPPORT_SHA and Path(sys.executable).resolve()==support.PYTHON and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in c.THREADS),'original environment and guard Source')
    helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'continuation_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'continuation_original_resources');full,production=helper.modules();helper.guard_admission(full)
    require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'original OwnRSS guard class/MRO; no stage execution')
    history=factory.DynamicHistoryResources(c.ART,factory.history_roots([str(owner),str(out)],c.ART),8*2**30,96*2**30,production.ResourceFailure)
    fresh=production.DiskResources(c.ART,[str(owner),str(out)],8*2**30,2*2**30)
    class Resources:
        def check(self):
            h=history.check();f=fresh.check()
            if h['artifact_bytes']+20971764748+64*2**20>=96*2**30:raise RuntimeError('history96GiB original cold reserve')
            if f['disk_free_bytes']-20971764748-2*2**30<8*2**30:raise RuntimeError('filesystem8GiB original reserves')
            return dict(h,fresh_output=f)
    resources=Resources();before=resources.check()
    def budget():
        require(time.monotonic()-start<1800,'original whole1800');resources.check();check_original_host_limits(c,start)
    records=copy.deepcopy(d['records']);state=copy.deepcopy(post['actual_collected_A_observation_state']);states={'A':state}
    require(state['state']=='A'and state['actual_genuine_material_stage']==records[0]and state['actual_cwd']==str(owner/'A')and state['actual_material_child_closed_before_manifest']is True and state['all_producer_file_handles_closed_before_next_state']is True,'only cached exact original closed A collection')
    require(state['complete_observed_file_pins']and state['actual_procedure_three_literal_inverse']['whole_reverse_replacement_equals_original_bytes']is True and state['actual_procedure_three_literal_inverse']['all_numeric_and_non_FIL_Source_bytes_unchanged']is True,'cached original complete collection/procedure proof required')
    plan=json.loads(Path(cli['seed_plan_pin']['path']).read_bytes());c.same_pin(cli['seed_plan_pin']['path'],cli['seed_plan_pin'])
    originals=original_shared_libraries(plan);copies=post['actual_owned_library_copy_pins_current']
    require(type(copies)is list and len(copies)==2 and sum(p['size_bytes']for p in copies)==979740136,'exact original private2 current')
    shared=dict(schema='ACTUAL_AB_SINGLE_COPY_COMPLETE_ORIGINAL_LIBRARY_EVIDENCE_V1',original_input_pins=originals,shared_copy_pins=dict(zip(originals,copies)),material_input_layout=SHARED_INPUT_LIBRARY_LAYOUT,shared_library_directory=str(owner/'s'),all_library_bytes_preserved_without_symlinks_or_hardlinks=True,actual_state_library_full_EOF_observations={})
    for name,p in shared['shared_copy_pins'].items():require(p['path']==str(owner/'s'/SHARED_INPUT_LIBRARY_LAYOUT['physical_file_names'][name])and p['sha256']==originals[name]['sha256']and p['size_bytes']==originals[name]['size_bytes'],'exact actual original shared two copies')
    fixed=list(d['fixed_current_pins']);lsof=c.pin('/usr/sbin/lsof');require('/usr/sbin/lsof'not in {p['path']for p in fixed},'only omitted lsof authority appended');fixed+=[lsof]+list(pins.values())+hf['dependencies']
    table={}
    for p in fixed:require(p['path']not in table or table[p['path']]==p,'same current path exactPF');table[p['path']]=p
    fixed=list(table.values());owned=[p for p in d['owned_input_copy_pins']];outputs_original=list(d['output_pins'])
    def check_current():
        budget()
        for p in fixed+owned+outputs_original:current7(p)
    check_current();out.mkdir();newwatch=[]
    for suffix in ['.log','.watchdog.json']:
        oldpath=owner/(records[0]['label']+suffix);want=next(p for p in outputs_original if p['path']==str(oldpath));target=out/oldpath.name
        with oldpath.open('rb')as src,target.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
        pp=fullpin(target,budget);require(pp['sha256']==want['sha256']and pp['size_bytes']==want['size_bytes']and pp['identity'][:2]!=want['identity'][:2],'entire original log/watch ordinary distinct copies')
        if suffix=='.watchdog.json':newwatch.append(dict(path=pp['path'],sha256=pp['sha256']))
    release_receipt=None;failure=None;first=None;tb=None;after=None
    try:
        check_current()
        release_receipt,released=release_closed_owned_library_copies(owner,shared,states,records,fixed,budget)
        owned=[p for p in owned if p['path']not in released];outputs_original=[p for p in outputs_original if p['path']not in released]
        check_current();after=resources.check()
        require(after['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'after exact release original real fullfresh2 reserve')
    except BaseException as error:first=error;tb=error.__traceback__;failure=repr(error)
    phase=out/'Root_actual_material_observation_execution_summary.json';phase_data=dict(schema='ACTUAL_CURRENT_FORMAL_A_MATERIAL_OBSERVATION_EXECUTION_V1',status='ACTUAL_ONE_A_MATERIAL_STAGE_CLOSED0_EVIDENCE_ONLY'if failure is None else'FAILED_CURRENT_OBSERVATION_NO_RETRY',failure=failure,after_check_error=None,records=records,actual_watchdog_checks=newwatch,fixed_current_pins=fixed,owned_input_copy_pins=owned,output_pins=outputs_original+[fullpin(p,budget)for p in out.iterdir()if p.is_file()],current_case_spec_pin=d['current_case_spec_pin'],actual_observer_build_report_pin=d['actual_observer_build_report_pin'],actual_runtime_pin=d['actual_runtime_pin'],original_guard_class=d['original_guard_class'],original_guard_MRO_unchanged=d['original_guard_MRO_unchanged'],SELF_peak_bytes=max(d['SELF_peak_bytes'],c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss),wall_seconds=time.monotonic()-start,resources_before=before,resources_after=after,actual_full_A_observation_executed=failure is None,actual_B_observation_executed=False,three_recaptured_plane_histories_claimed=False,actual_closed_owned_library_copy_release_pin=release_receipt,completion_only_existing_closed_stage=True,Dragon_or_compiler_or_material_child_launched_by_continuation=False,original_failed_phase_pin=pins['original-phase'],original_Root_true_tool_pin=pins['original-Root-tools'],original_Root_exit_code_retained=1,original_Root_failure_retained=d['failure'],actual_prior_material_stage_record_reused_wholebytes=True,actual_prior_A_cwd=str(owner/'A'),original_material_host_wall_seconds=d['wall_seconds'],cached_actual_collection_post_pin=pins['failed-post'],original_capture_collector_not_reexecuted=True,original_release_owner_output_root=str(owner),original_release_four_library_full_EOF_observations_required=True,new_scientific_outputs_created=False,requires_host_process_metadata_access=True,final_report_bytes_in_original_resources=True,**FUTURE)
    c.write(phase,phase_data);phasepin=fullpin(phase,budget)
    if first is not None:raise first.with_traceback(tb)
    state['actual_owning_report_pin']=phasepin;state['actual_stage_label']=records[0]['label'];state['actual_command']=records[0]['command']
    manifest=out/'ACTUAL_CURRENT_FORMAL_COMPLETE_OBSERVATION_MANIFEST.json'
    c.write(manifest,dict(schema='ACTUAL_CURRENT_FORMAL_COMPLETE_OBSERVATION_MANIFEST_V1',current_case_spec_pin=d['current_case_spec_pin'],state_order=['A'],states=states,observation_scope='ONE_SAME_PHYSICAL_A_MATERIAL_CONSTRUCTION_NOT_THREE_HISTORIES',actual_observer_build_report_pin=d['actual_observer_build_report_pin'],actual_runtime_pin=d['actual_runtime_pin'],actual_shared_input_library_evidence=shared,actual_closed_owned_library_copy_release_pin=release_receipt,shared_copy_pins_are_historical_closed_consumption_not_current_live_inputs=True,material_input_layout=SHARED_INPUT_LIBRARY_LAYOUT,all_host_managed_handles_closed=True,actual_lsof_owner_handle_closure_qualified=False,original_caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0),completion_only_original_Root1_preserved=True,original_failed_phase_pin=pins['original-phase'],original_Root_true_tool_pin=pins['original-Root-tools'],cached_actual_collection_post_pin=pins['failed-post'],**FUTURE))
    check_current();resources.check();check_original_host_limits(c,start)
    print(json.dumps(dict(status='ACTUAL_EXISTING_A10_CAPTURE_CONTINUATION_AND_PRIVATE_COPY_RELEASE_CLOSED0_NO_DRAGON_RERUN',completion_report_pin=phasepin,observation_manifest_pin=fullpin(manifest,budget),release_receipt_pin=release_receipt,original_Root_exit_code_retained=1,actual_original_material_stage_count=1,new_material_child_launch_count=0,physics_qualified=False)),flush=True)


if __name__=='__main__':main()
