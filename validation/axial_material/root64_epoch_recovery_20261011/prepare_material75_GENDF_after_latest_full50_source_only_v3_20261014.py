#!/usr/bin/env python3
"""Prepare Source candidates after genuine selected latest full50 engineering closure.

No Host, observer, parser, solver, cleanup or mathematical module is imported.
Candidate metadata templates are review material, not owning runtime freezes.
The current original cache70 plus five observers remains the material runtime.
"""
from pathlib import Path
import argparse,ast,hashlib,json,os,shlex,stat

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
SPEC=REC/'MATERIAL75_GENDF_AFTER_LATEST_FULL50_PREPARER_SOURCE_SPEC_V3_20261014.json'
OLD_M=REC/'current_formal_material_authority_exact_cache70_source_v7'
OLD_G=REC/'current_eleven_saved_gendf_current_mount_host_source_v4'
NEW_M=REC/'current_formal_material_authority_exact_cache70_post_curated66_latest_full50_source_v8_20261014'
NEW_G=REC/'current_eleven_saved_gendf_post_curated66_latest_full50_host_source_v5_20261014'
PF_KEYS={'path','sha256','size_bytes','identity'}

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def canonical(p):
    if not isinstance(p,dict)or set(p)!=PF_KEYS or not isinstance(p['identity'],list)or len(p['identity'])!=7 or \
       any(type(x)is not int for x in p['identity'])or type(p['size_bytes'])is not int or \
       p['size_bytes']!=p['identity'][4]or not stat.S_ISREG(p['identity'][2]):
        raise RuntimeError('canonical complete fullpin required')
    return p
def pin(path):
    path=Path(path);before=identity(path.lstat())
    if path.is_symlink()or not stat.S_ISREG(before[2]):raise RuntimeError('regular no-symlink selected Source/metadata')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd))!=before:raise RuntimeError('opened input exact7 differs')
        with os.fdopen(fd,'rb')as f:
            fd=None;raw=f.read()
            if identity(os.fstat(f.fileno()))!=before:raise RuntimeError('EOF input exact7 differs')
    finally:
        if fd is not None:os.close(fd)
    if identity(path.lstat())!=before:raise RuntimeError('after EOF input exact7 differs')
    return raw,dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)
def read(row):
    canonical(row);raw,now=pin(row['path'])
    if now!=row:raise RuntimeError('exact selected Source/metadata fullpin changed')
    return json.loads(raw)
def external(a,prefix):
    raw,row=pin(getattr(a,prefix+'_summary'))
    if row['sha256']!=getattr(a,prefix+'_sha256')or row['identity']!=json.loads(getattr(a,prefix+'_seven_id')):
        raise RuntimeError('required actual external fullpin differs: '+prefix)
    return json.loads(raw),row
def unique(rows):
    table={}
    for row in rows:
        canonical(row)
        if row['path']in table and table[row['path']]!=row:raise RuntimeError('conflicting selected current fullpin')
        table[row['path']]=row
    return list(table.values())
def current7(rows):
    for row in unique(rows):
        p=Path(row['path'])
        if p.is_symlink()or identity(p.lstat())!=row['identity']:
            raise RuntimeError('selected current fullpin exact7 differs: '+row['path'])
def write(path,data):
    if not isinstance(data,bytes):data=data.encode()
    with Path(path).open('xb')as f:f.write(data);f.flush();os.fsync(f.fileno())
    _,row=pin(path)
    if row['identity'][3]!=1 or Path(path).lstat().st_uid!=os.getuid():raise RuntimeError('own Source UID/singlelink')
    return row
def dump(path,data):return write(path,json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def closed0(actual):
    if not isinstance(actual,dict)or type(actual.get('exit_code'))is not int or actual['exit_code']!=0 or \
       actual.get('session_id')is not None:raise RuntimeError('genuine terminal integer0/no session required')
def replace_selected(value,mapping):
    # Only complete PFs in the explicitly assembled Source/current-Common map
    # are substituted. Historical document bodies are never traversed as DAGs.
    if isinstance(value,dict):
        if set(value)==PF_KEYS:
            canonical(value)
            if value['path']not in mapping:return value
            before,after=mapping[value['path']]
            if value!=before:raise RuntimeError('selected original Source PF conflict')
            return after
        return{k:replace_selected(v,mapping)for k,v in value.items()}
    if isinstance(value,list):return[replace_selected(v,mapping)for v in value]
    return value

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    for prefix in ('preparation-plan','aaa3','aaa3-host-freeze','aaa3-root-argv','aaa3-root-tool','aaa3-post-tools'):
        for suffix in ('summary','sha256','seven-id'):ap.add_argument('--'+prefix+'-'+suffix,required=True)
    args=ap.parse_args();spec,pspec=external(args,'preparation_plan')
    if pspec['path']!=str(SPEC)or spec.get('schema')!='MATERIAL75_GENDF_AFTER_LATEST_FULL50_PREPARER_SOURCE_SPEC_V1'or \
       spec.get('source_only')is not True or spec['preparer_source_pin']!=pin(__file__)[1]or \
       any(spec.get(k)is not False for k in ('compiler_executed','numerical_executed','business_executed','files_deleted'))or \
       any(k not in spec or spec[k]is not None for k in spec['future_actual_keys']):
        raise RuntimeError('exact Source preparer specification and future PFs None')
    authority=spec['latest_full50_exact_authority_contract']
    if not isinstance(authority,dict)or set(authority)!={'Host_freeze_schema','post_schema','post_status'}or any(not isinstance(v,str)or not v for v in authority.values()):raise RuntimeError('exact latest full50 HF/post contract unknown None refused')
    if spec['selected_static_pins']['latest_full50_Host_freeze']is None or spec['selected_static_pins']['latest_full50_CLI']is None or not isinstance(spec['required_actual_latest_full50_output_directory'],str):raise RuntimeError('actual selected latest full50 HF/CLI/output authority required; future None refused')
    migration=read(spec['original_migration_plan_pin']);static=spec['selected_static_pins']
    for row in static.values():
        canonical(row)
        if pin(row['path'])[1]!=row:raise RuntimeError('selected static Source/metadata exact fullpin')
    boot,pboot=external(args,'aaa3');hf,phf=external(args,'aaa3_host_freeze')
    argv,pargv=external(args,'aaa3_root_argv');tools,ptools=external(args,'aaa3_root_tool')
    posttools,pposttools=external(args,'aaa3_post_tools')
    if phf!=static['latest_full50_Host_freeze']or hf['schema']!=authority['Host_freeze_schema']or \
       Path(pboot['path']).parent!=Path(spec['required_actual_latest_full50_output_directory'])or \
       boot.get('schema')!='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1'or \
       boot.get('status')!='ACTUAL_THREE_PLANE_ENGINEERING_CLOSED0_ONLY'or boot.get('failure')is not None or \
       boot.get('after_check_error')is not None or boot.get('engineering_three_plane_closed0')is not True or \
       boot.get('all_new_storage_entry_controls_closed')is not True or \
       type(boot.get('SELF_peak_bytes'))is not int or not 0<=boot['SELF_peak_bytes']<512*2**20 or \
       type(boot.get('wall_seconds'))not in (int,float)or not 0<boot['wall_seconds']<1800 or \
       boot.get('original_guard_class')!='OwnRSSSerialExecutor'or boot.get('original_guard_MRO_unchanged')is not True or \
       len(boot['records'])!=50 or sum(r['status']=='PASS'for r in boot['records'])!=17 or \
       sum(r['status']=='FAILED'for r in boot['records'])!=33 or len(boot['actual_operator_refusals'])!=33 or \
       any(boot.get(k)is not False for k in ('AAA_qualified','ABA_admitted','goal_complete')):
        raise RuntimeError('actual successful complete original engineering50, never a failed or Source-only substitute')
    if phf not in boot['fixed_current_pins']or hf['host_source']not in boot['fixed_current_pins']:
        raise RuntimeError('actual engineering execution consumed exact selected latest full50 Source/HF')
    cli=read(static['latest_full50_CLI']);want=cli['exact_reviewable_argv']
    if len(want)!=96 or argv['exact_argv']!=want or len(cli['mandatory_external_prefixes'])!=14 or argv['interface_pin']!=static['latest_full50_CLI']or argv['Host_freeze_pin']!=phf:
        raise RuntimeError('actual exact selected full50 ninety-six-token fourteen-prefix argv')
    closed0(tools['actual_terminal_return'])
    executed=tools.get('exact_executed_command');executed=shlex.split(executed)if isinstance(executed,str)else executed
    if tools.get('observed_closed')is not True or type(tools.get('original_integer_exit_code'))is not int or \
       tools['original_integer_exit_code']!=0 or executed!=want:
        raise RuntimeError('actual Root observed terminal0 and exact selected executed argv')
    reviewreturn=posttools.get('actual_review_return');closed0(reviewreturn)
    lines=reviewreturn.get('output','').strip().splitlines()
    if posttools.get('observed_closed')is not True or not lines:raise RuntimeError('genuine independent actual post0 required')
    ppost=canonical(json.loads(lines[-1])['review_pin']);post=read(ppost)
    if post.get('schema')!=authority['post_schema']or \
       post.get('status')!=authority['post_status']or post.get('failure')is not None or \
       post.get('actual_report_pin')!=pboot or post.get('actual_Host_freeze_pin')!=phf or \
       post.get('actual_Root_true_tool_return_pin')!=ptools or post.get('actual_Root_argv_pin')!=pargv or \
       any(post.get(k)is not False for k in ('independent_business_executed','independent_compiler_executed',
          'independent_numerical_executed','independent_deletion_executed'))or \
       any(post.get(k)is not True for k in ('actual_engineering_three_plane_closed0',
          'all_actual_child_watch_limit_failures_absent','actual_complete_pair_payload_bits_equal',
          'all_current_output_pins_full_EOF_SHA_all7'))or \
       any(type(post.get(k))is not int or post[k]!=n for k,n in
          [('actual_stage_count',50),('actual_positive_count',17),('actual_exact_refusal_count',33)]):
        raise RuntimeError('exact independent genuine50 logs/watch/refusal/seal/full-output post0 facts')
    current7(hf['dependencies']+boot['fixed_current_pins']+boot['output_pins'])
    if boot['actual_terminal']['actual_Fortran_complete_copy_readback']['status']!='PASS'or \
       boot['actual_terminal']['actual_Fortran_complete_copy_readback']['all_payload_bits_equal']is not True:
        raise RuntimeError('complete genuine Fortran sealed pair readback required')
    # No raw scientific body SHA is repeated. Preserve the exact33/51 authority
    # rows and eleven GENDF input pins; this phase rechecks their complete7 only.
    originM=read(migration['original_material_origin33_pin']);originG=read(migration['original_GENDF_origin51_pin'])
    if len(originM['rows'])!=33 or len(originG['rows'])!=51:raise RuntimeError('original scientific33/51 authority scope')
    science=[]
    for row in originM['rows']+originG['rows']:
        if not isinstance(row,dict)or 'current_pin'not in row:raise RuntimeError('original explicit current science authority row')
        science.append(row['current_pin'])
    science+=migration['GENDF_exact_eleven_saved_input_pins_unchanged'];current7(science)
    if NEW_M.exists()or NEW_M.is_symlink()or NEW_G.exists()or NEW_G.is_symlink():raise RuntimeError('unique two Source namespaces only')
    NEW_M.mkdir();NEW_G.mkdir();copied=[];inverse=[];mapping={}
    change_by_path={x['predecessor_Source_pin']['path']:x for x in migration['exact_Source_literal_changes']}
    declared_source=unique(spec['original_frozen_code_and_static_input_pins'])
    declared={x['path']:x for x in declared_source}
    if len(declared_source)!=24 or sum(Path(x['path']).suffix in ('.py','.f','.f90')for x in declared_source)!=22:
        raise RuntimeError('exact frozen twenty-two code and two static Source inputs')
    current7(declared_source)
    for old,new in ((OLD_M,NEW_M),(OLD_G,NEW_G)):
        expected={Path(x['path']).name for x in declared_source if Path(x['path']).parent==old and Path(x['path']).suffix in ('.py','.f','.f90')}
        actual={x.name for x in old.iterdir()if x.suffix in ('.py','.f','.f90')}
        if actual!=expected:raise RuntimeError('exact frozen code inventory; no undeclared added code')
        for name in sorted(expected):
            source=old/name
            raw,pbefore=pin(source);text=raw.decode();blocks=[]
            if declared.get(str(source))!=pbefore:raise RuntimeError('copied code must equal original frozen Source fullpin')
            if str(source)in change_by_path:
                item=change_by_path[str(source)]
                if item['predecessor_Source_pin']!=pbefore:raise RuntimeError('exact planned original literal Source')
                for block in item['exact_literal_change_blocks']:
                    before=block['before'];after=block['after'].replace('post_curated66_v15_source_v8_20261014','post_curated66_latest_full50_source_v8_20261014')
                    if text.count(before)!=1:raise RuntimeError('one exact Common/own Source literal')
                    text=text.replace(before,after,1);blocks.append(dict(before=before,after=after,reason='current Common or own namespace only'))
            if source.name=='current_material_prerequisite_admission.py':
                before='actual prerequisite must consume exact frozen v11 host Source';after='actual prerequisite must consume exact selected full50 host Source'
                if text.count(before)!=1:raise RuntimeError('one original stale diagnostic label')
                text=text.replace(before,after,1);blocks.append(dict(before=before,after=after,reason='diagnostic label follows explicit required actual selected full50 HF; gate bytes unchanged'))
            restored=text
            for block in reversed(blocks):
                if restored.count(block['after'])!=1:raise RuntimeError('unambiguous complete Source inverse')
                restored=restored.replace(block['after'],block['before'],1)
            if restored.encode()!=raw:raise RuntimeError('whole original Source bytes recovered')
            if blocks:ast.parse(text)
            pafter=write(new/source.name,text);mapping[pbefore['path']]=(pbefore,pafter)
            copied.append(dict(predecessor_pin=pbefore,candidate_pin=pafter,whole_bytes_unchanged=not blocks))
            if blocks:inverse.append(dict(predecessor_pin=pbefore,candidate_pin=pafter,changes=blocks,whole_inverse_bytes_equal=True))
    if sum(len(x['changes'])for x in inverse)!=7:raise RuntimeError('exact original six literal changes plus one diagnostic label')
    for name in ('CURRENT_FORMAL_COMPLETE_AB_ORIGINAL_MATERIAL_SEED_PLAN_SOURCE_ONLY.json',
      'FULL_ACTUAL_CONTEXT_AND_SNAPSHOT_EXTENSION_CONTRACT.UNREADY.json'):
        data,before=pin(OLD_M/name)
        if declared.get(str(OLD_M/name))!=before:raise RuntimeError('two static Source inputs equal exact original frozen fullpins')
        after=write(NEW_M/name,data);mapping[before['path']]=(before,after)
        copied.append(dict(predecessor_pin=before,candidate_pin=after,whole_bytes_unchanged=True))
    # The only external current-role substitutions are precisely the three
    # Common/catalog/binding files named by the already reviewed migration.
    old_common_pins=spec['original_current_Common_role_pins']
    for key in ('Common_Source','catalog','binding'):
        before=old_common_pins[key];after=static['new_'+key];mapping[before['path']]=(before,after)
    template_fields={
      'CURRENT_FORMAL_MATERIAL_AUTHORITY_SELECTED_CACHE70_PLAN.json':['complete_source_copies','original4_math_source_copies','current_seed_plan_pin'],
      'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json':['files','current_plan_pin'],
      'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json':['host_source','dependencies','selected_source_freeze_pin'],
      'COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json':['host_source','dependencies','selected_build_host_freeze_pin','selected_seed_plan_pin'],
      'COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json':['complete_source_file_pins'],
      'COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json':['host_source','dependencies'],
      'EXPLICIT_CURRENT_MATERIAL_ORIGIN_REATTESTATION_SOURCE_ONLY.json':['actual_current_catalog_pin'],
      'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json':['complete_source_file_pins','current_Common_Source_freeze_pin'],
      'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json':['host_source','dependencies','selected_current_Common_Source_pin'],
      'CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN.json':['complete_source_file_pins','selected_current_Common_Source_pin','selected_current_Common_binding_pin'],
      'COMPLETE_CURRENT_GENDF_INPUT_METADATA_REATTESTATION_SOURCE_ONLY.json':['selected_current_Common_Source_freeze_pin','selected_current_Common_binding_pin','selected_current_mount_catalog_pin']}
    future_own_fields={
      'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json':['current_plan_pin'],
      'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json':['selected_source_freeze_pin'],
      'COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json':['selected_build_host_freeze_pin'],
      'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json':['current_plan_pin','explicit_current_input_reattestation_pin'],
      'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json':['selected_source_freeze_pin','explicit_current_input_reattestation_pin'],
      'CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN.json':['complete_current_input_reattestation_pin','complete_scoped_byte_inverse_pin']}
    templates=[]
    for name,keys in template_fields.items():
        old=OLD_G if 'GENDF'in name else OLD_M;raw,pold=pin(old/name);value=json.loads(raw);candidate=dict(value)
        for key in keys:candidate[key]=replace_selected(value[key],mapping)
        if name=='COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json':
            candidate.update(required_actual_AAA3_output_directory=str(Path(pboot['path']).parent),required_actual_AAA3_host_freeze_pin=phf)
        if name=='COMPLETE_CURRENT_GENDF_INPUT_METADATA_REATTESTATION_SOURCE_ONLY.json':
            candidate.update(selected_current_Common_Source_freeze_pin=static['new_Common_Source_freeze'],
              complete_current_Common_binding_rows_fullEOF=2012,complete_selected_catalog_rows_fullEOF=3030,
              inherited_scientific_EOF_then_actual_current7=True)
        if name=='COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json':
            candidate['current_Common_Source_freeze_pin']=static['new_Common_Source_freeze']
        unresolved=[]
        for key in future_own_fields.get(name,[]):
            if key not in value:raise RuntimeError('exact required future owning metadata field')
            unresolved.append(dict(field=key,predecessor_pin=value[key],future_owning_pin=None,
              must_bind_actual_reviewed_new_metadata_before_runtime=True))
            candidate[key]=None
        candidate.update(predecessor_statistics_and_claims_are_historical_declarations=True,
          current_role_reconciliation=dict(catalog_active_rows=3030,catalog_unique_physical_files=2979,binding_rows=2012),
          only_selected_current_Source_metadata_fields_rebound=True,original_scientific_raw_rows_and_thresholds_unchanged=True)
        templates.append(dict(original_metadata_pin=pold,original_metadata_value=value,selected_live_fields=keys,
          proposed_current_metadata=candidate,owning_frozen_metadata_pin=None,requires_final_independent_Source_review_before_owning_freeze=True))
        templates[-1]['future_owning_metadata_field_bindings']=unresolved
    inv=dump(NEW_M/'COMPLETE_MATERIAL_GENDF_COMMON_AND_LATEST_FULL50_BINDING_SOURCE_INVERSE.json',dict(
      schema='COMPLETE_MATERIAL_GENDF_COMMON_AND_LATEST_FULL50_BINDING_SOURCE_INVERSE_V1',changed_sources=inverse,
      unchanged_source_copies=copied,original_six_literal_scope_preserved=True,extra_one_diagnostic_label_only=True,
      metadata_templates=templates,old_source_packages_modified=False,compiler_executed=False,numerical_executed=False))
    dependencies=unique([pspec,spec['preparer_source_pin'],spec['original_migration_plan_pin'],spec['original_migration_tools_pin'],
      pboot,phf,pargv,ptools,pposttools,ppost]+list(static.values())+hf['dependencies']+boot['fixed_current_pins']+boot['output_pins']+
      [p for x in copied for p in (x['predecessor_pin'],x['candidate_pin'])]+[x['original_metadata_pin']for x in templates]+science+[inv])
    current7(dependencies)
    future=dict(actual_observer75_report_pin=None,actual_saved_full370_report_pin=None,actual_first_A_material_report_pin=None,
      actual_GENDF_report_pin=None,own_material_math_Source_freeze_pin=None,own_material_build_Host_freeze_pin=None,
      own_material_observation_Host_freeze_pin=None,own_material_evidence_Source_freeze_pin=None,
      own_material_evidence_Host_freeze_pin=None,own_GENDF_Source_freeze_pin=None,own_GENDF_Host_freeze_pin=None,own_runnable_CLIs=None)
    plan=dump(NEW_M/'MATERIAL_GENDF_ACTUAL_LATEST_FULL50_BOUND_CANDIDATE_SOURCE_PREPARATION_PLAN.json',dict(
      schema='MATERIAL_GENDF_ACTUAL_LATEST_FULL50_BOUND_CANDIDATE_SOURCE_PREPARATION_PLAN_V1',source_only=True,
      selected_actual_latest_full50_report_pin=pboot,selected_actual_latest_full50_Host_freeze_pin=phf,selected_actual_latest_full50_Root_argv_pin=pargv,
      selected_actual_latest_full50_Root_tool_pin=ptools,selected_actual_latest_full50_post_review_pin=ppost,selected_actual_latest_full50_post_tools_pin=pposttools,
      selected_new_Common_Source_pin=static['new_Common_Source'],selected_new_Common_Source_freeze_pin=static['new_Common_Source_freeze'],
      selected_new_catalog_pin=static['new_catalog'],selected_new_binding_pin=static['new_binding'],
      material_Source_namespace=str(NEW_M),GENDF_Source_namespace=str(NEW_G),source_copies=copied,complete_inverse_pin=inv,
      current_live_metadata_templates=templates,dependencies=dependencies,original_material33_rows=originM['rows'],
      original_GENDF51_rows=originG['rows'],original_GENDF11_input_pins=migration['GENDF_exact_eleven_saved_input_pins_unchanged'],
      original_scientific_EOF_not_repeated=True,all_scientific_current7_checked=True,
      original_material_observer75_native_cache70_and_five_order_retained=True,new_BOOTQ_or_Driver_not_inserted_in_material75=True,
      original_owned_library_copy_lifecycle_bytes=979740136,original_caps=migration['original_thresholds'],
      required_saved370_actual_authority_still_pending=True,old_metadata_files_not_rewritten=True,
      compiler_executed=False,numerical_executed=False,material_job_executed=False,GENDF_executed=False,files_deleted=False,
      AAA_qualified=False,ABA_admitted=False,goal_complete=False,future_actual=future))
    ready=dump(NEW_M/'SOURCE_REVIEW_READY.json',dict(schema='MATERIAL_GENDF_ACTUAL_LATEST_FULL50_BOUND_CANDIDATE_SOURCE_REVIEW_READY_V1',
      status='SOURCE_ONLY_READY_FOR_INDEPENDENT_REVIEW_NOT_RUNTIME_FREEZE',failure=None,plan_pin=plan,inverse_pin=inv,
      source_copies=copied,source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,
      files_deleted=False,future_actual=future))
    print(json.dumps(dict(status=ready['path'],plan_pin=plan,ready_pin=ready,inverse_pin=inv,dependency_count=len(dependencies),
      compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False),ensure_ascii=False),flush=True)

if __name__=='__main__':main()
