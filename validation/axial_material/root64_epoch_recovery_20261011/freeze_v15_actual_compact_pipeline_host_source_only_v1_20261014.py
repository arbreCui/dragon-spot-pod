#!/usr/bin/env python3
"""Write one reviewed v15 Host HF and exact CLI; never import/run a Host."""
from pathlib import Path
import argparse,ast,hashlib,json,os,stat

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
HERE=REC/'aaa_three_plane_compact_expected_pipeline_source_v15_20261014'
HF=HERE/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'
CLI=HERE/'DECLARED_EXECUTION_INTERFACE.json'

def seven(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    path=Path(path);before=seven(path.lstat())
    if not stat.S_ISREG(before[2])or path.is_symlink():raise RuntimeError('regular exact Source/current metadata')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if seven(os.fstat(fd))!=before:raise RuntimeError('opened exact7 changed')
        with os.fdopen(fd,'rb')as stream:
            fd=None;raw=stream.read()
            if seven(os.fstat(stream.fileno()))!=before:raise RuntimeError('EOF exact7 changed')
    finally:
        if fd is not None:os.close(fd)
    if seven(path.lstat())!=before:raise RuntimeError('after exact7 changed')
    return raw,dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)
def read(row):
    raw,current=pin(row['path'])
    if current!=row:raise RuntimeError('bound complete exact PF differs')
    return json.loads(raw)
def unique(rows):
    table={}
    for row in rows:
        if not isinstance(row,dict)or set(row)!={'path','sha256','size_bytes','identity'}:
            raise RuntimeError('canonical complete PF')
        if row['path']in table and table[row['path']]!=row:raise RuntimeError('inconsistent complete PF')
        table[row['path']]=row
    return list(table.values())
def current7(rows):
    for row in unique(rows):
        p=Path(row['path'])
        if p.is_symlink()or seven(p.lstat())!=row['identity']:raise RuntimeError('current dependency exact7 differs: '+row['path'])
def write(path,data):
    with path.open('x')as stream:
        json.dump(data,stream,indent=2,ensure_ascii=False,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    _,row=pin(path)
    if row['identity'][3]!=1:raise RuntimeError('own output singlelink required')
    return row
def external(args,prefix):
    raw,row=pin(getattr(args,prefix+'_summary'))
    if row['sha256']!=getattr(args,prefix+'_sha256')or row['identity']!=json.loads(getattr(args,prefix+'_seven_id')):
        raise RuntimeError('external complete exact PF differs')
    return json.loads(raw),row
def fullpins(value):
    if isinstance(value,dict):
        if set(value)=={'path','sha256','size_bytes','identity'}:yield value
        else:
            for v in value.values():yield from fullpins(v)
    elif isinstance(value,list):
        for v in value:yield from fullpins(v)

def main():
    p=argparse.ArgumentParser()
    for prefix in ('peer-review','peer-tools'):
        for suffix in ('summary','sha256','seven-id'):p.add_argument('--'+prefix+'-'+suffix,required=True)
    args=p.parse_args();review,review_pin=external(args,'peer_review');tools,tools_pin=external(args,'peer_tools')
    actual=tools.get('actual_review_return')
    if tools.get('observed_closed')is not True or not isinstance(actual,dict)or \
       type(actual.get('exit_code'))is not int or actual['exit_code']!=0 or actual.get('session_id')is not None:
        raise RuntimeError('genuine independent candidate Source review terminal integer0 closed without session')
    lines=actual.get('output','').strip().splitlines()
    if not lines or json.loads(lines[-1]).get('review_pin')!=review_pin:
        raise RuntimeError('true Source-review stdout binds exact independent review PF')
    if 'failure'not in review or review['failure']is not None or not isinstance(review.get('status'),str)or not review['status'].startswith('PASS')or \
       review.get('source_only')is not True or review.get('numerical_executed')is not False:
        raise RuntimeError('independent Source-only candidate review status')
    plan_path=HERE/'ACTUAL_PREREQUISITE_BOUND_V15_SOURCE_PREPARATION_PLAN.json';plan_raw,plan_pin=pin(plan_path);plan=json.loads(plan_raw)
    ready_path=HERE/'SOURCE_REVIEW_READY.json';ready_raw,ready_pin=pin(ready_path);ready=json.loads(ready_raw)
    if plan.get('schema')!='ACTUAL_PREREQUISITE_BOUND_V15_SOURCE_PREPARATION_PLAN_V1'or plan.get('source_only')is not True or \
       any(plan.get(k)is not False for k in ('actual_pipeline_executed','compiler_executed','numerical_executed','files_deleted'))or \
       any(k not in plan or plan[k]is not None for k in ('own_Host_freeze_pin','own_CLI_pin','future_actual_v15_report_pin'))or \
       ready['host_source']!=plan['host_source']or ready['plan_pin']!=plan_pin or ready.get('failure')is not None:
        raise RuntimeError('actual candidate Source-only plan and future v15 PFs None')
    reviewed=list(fullpins(review))
    for row in [plan['host_source'],plan_pin,ready_pin,plan['complete_byte_inverse_pin'],plan['direct_alias_binding_pin'],pin(__file__)[1]]:
        if row not in reviewed:raise RuntimeError('independent review must bind exact candidate/freezer Source PF')
    raw,host=pin(HERE/'run_actual_three_plane_pipeline.py');ast.parse(raw)
    if host!=plan['host_source']:raise RuntimeError('actual Host Source differs')
    original=read(plan['original_v14_Host_freeze_pin'])
    if len(original['dependencies'])!=377 or plan['original377_dependency_rows_to_retain']!=original['dependencies']:
        raise RuntimeError('original377 exact fullpins retained')
    prereq=plan['selected_actual_prerequisites'];public_hf=read(prereq['selected_public7_Host_freeze_pin'])
    addpaths=[plan_path,ready_path,Path(__file__),
      REC/'ACTUAL_V15_ACTUAL_PREREQUISITE_BOUND_SOURCE_PREPARATION_TRUE_TOOL_RETURN_20261014.json',
      REC/'V15_PREPARER_V1_TO_V2_EXACT_SOURCE_PLAN_INVERSE_20261014.json',
      REC/'ACTUAL_V15_PREPARER_V2_EXACT_INVERSE_SOURCE_ONLY_TRUE_TOOL_RETURN_20261014.json',
      REC/'independent_v15_actual_preparer_v2_and_SRC_retirement_admission_Source_review_20261014/REVIEW.json',
      REC/'independent_v15_actual_preparer_v2_and_SRC_retirement_admission_Source_review_20261014/TRUE_TOOL_RETURNS.json',
      REC/'ROOT_V15_ACTUAL_PREREQUISITE_CANDIDATE_SOURCE_REVIEW_20261014.json',
      REC/'ROOT_V15_ACTUAL_PREREQUISITE_CANDIDATE_SOURCE_REVIEW_TRUE_TOOL_RETURN_20261014.json']
    dependencies=unique(plan['dependencies']+[pin(x)[1]for x in addpaths]+[review_pin,tools_pin])
    current7(dependencies)
    if any(x not in dependencies for x in original['dependencies']):raise RuntimeError('all original377 belong to final owning HF')
    if HF.exists()or HF.is_symlink()or CLI.exists()or CLI.is_symlink()or Path(plan['planned_output_root']).exists()or \
       Path(plan['planned_output_root']).is_symlink():raise RuntimeError('one fresh Source-only HF/CLI and absent future own OUT')
    freeze=dict(original)
    freeze.update(schema='COMPLETE_ACTUAL_AAA3_COMPACT_EXPECTED_PIPELINE_HOST_SOURCE_FREEZE_V15',
      host_source=host,dependencies=dependencies,predecessor_host_freeze=plan['original_v14_Host_freeze_pin'],
      predecessor_source_claims_are_historical_declarations=True,
      complete_original_v14_dependency_rows_retained=377,actual_dependency_count=len(dependencies),
      actual_prerequisite_bound_Source_plan_pin=plan_pin,complete_DRAFT2_to_V15_byte_inverse_pin=plan['complete_byte_inverse_pin'],
      independent_V15_candidate_Source_review_pin=review_pin,independent_V15_candidate_Source_true_tool_pin=tools_pin,
      actual_independent_Source_review_return=0,prepared_only=True,actual_pipeline_executed=False,
      actual_qualified_numeric_pipeline=False,no_prefilled_actual_success=True,
      Source_revision_scope='actual compact build/control bindings and exact sole SRC historical lifetime admission; original math/50 wholebytes',
      selected_post_release_Common_Source_pin=public_hf['selected_post_release_Common_Source_pin'],
      selected_post_release_current_catalog_pin=public_hf['selected_post_release_current_catalog_pin'],
      selected_post_release_current_binding_pin=public_hf['selected_post_release_current_binding_pin'],
      original_caps=plan['original_caps'],strict_forecast_MiB=plan['strict_forecast_MiB'],
      mathematical_or_material_or_threshold_changes=False,same_original_50_stages_17_positive_33_exact_negative_controls=True,
      exact_completed_first_SRC_retirement_only=True,all_other_files_current_full_EOF_all7_required=True,
      new_reader_prerequisites_genuinely_closed=True,physics_qualification=False,AAA_qualified=False,ABA_admitted=False,
      future_actual_v15_summary_pin=None,future_actual_v15_raw_pin=None,future_actual_v15_capture_pins=None,
      **prereq)
    hf_pin=write(HF,freeze)
    old_cli=json.loads(pin(REC/'aaa_three_plane_streaming_pipeline_source_v14/DECLARED_EXECUTION_INTERFACE.json')[0])
    interface=dict(old_cli);prefixes=['a1','a2','a3','build70','seventeen','source-freeze','host-freeze',
                                    'new-build70','fresh-seventeen','private-model','public-read-seven']
    interface.update(schema='DECLARED_ACTUAL_AAA3_COMPACT_EXPECTED_ONE_SERIAL_50_STAGE_INTERFACE_V15',
      host_source=host['path'],host_source_pin=host,output_root=plan['planned_output_root'],mandatory_external_prefixes=prefixes,
      selected_actual_prerequisites=prereq,selected_own_Host_freeze_pin=hf_pin,Source_revision_scope=freeze['Source_revision_scope'],
      current_Common_source_pin=freeze['selected_post_release_Common_Source_pin'],
      current_Common_binding_pin=freeze['selected_post_release_current_binding_pin'],
      current_Common_Source_freeze_pin=prereq['selected_post_release_Common_Source_freeze_pin'],
      current_mount_full_identity_catalog_pin=freeze['selected_post_release_current_catalog_pin'],
      actual_pipeline_executed=False,compiler_executed_by_this_prepare=False,mathematical_or_material_or_threshold_changes=False,
      actual_future_v15_reports=None,AAA_qualified=False,ABA_admitted=False,
      predecessor_interface_claims_are_historical_declarations=True,
      unchanged_original_nine_objects_scope='Old nine are Source lineage; actual new nine preserve eight and replace core slot6/complete70 index40; fresh17/model/public7 bind the same genuine new object.')
    bound=dict(zip(('a1','a2','a3'),old_cli['selected_actual_producer_report_pins']))
    bound.update({'build70':original['selected_actual_build70_report'],'seventeen':old_cli['selected_actual_seventeen_report_pin'],
      'source-freeze':original['selected_fortran_freeze'],'host-freeze':hf_pin,
      'new-build70':prereq['selected_actual_new_build70_report_pin'],'fresh-seventeen':prereq['selected_actual_fresh17_report_pin'],
      'private-model':prereq['selected_actual_private_model_report_pin'],'public-read-seven':prereq['selected_actual_public7_report_pin']})
    argv=['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1',
      'OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1',
      '/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',host['path']]
    for prefix in prefixes:
        row=bound[prefix]
        argv.extend(['--'+prefix+'-summary',row['path'],'--'+prefix+'-sha256',row['sha256'],
                     '--'+prefix+'-seven-id',json.dumps(row['identity'],separators=(',',':'))])
    interface.update(exact_reviewable_argv=argv,mandatory_external_fullpin_bindings=bound,
      original50_math_and_caps_unchanged=True,actual_prerequisite_counts=plan['actual_prerequisite_counts'])
    cli_pin=write(CLI,interface)
    print(json.dumps(dict(status='V15_ACTUAL_PREREQUISITE_BOUND_HOST_SOURCE_HF_CLI_FROZEN_ONLY',host_source=host,
      host_freeze_pin=hf_pin,CLI_pin=cli_pin,actual_dependency_count=len(dependencies),mandatory_external_prefix_count=len(prefixes),
      actual_pipeline_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False),ensure_ascii=False))

if __name__=='__main__':main()
