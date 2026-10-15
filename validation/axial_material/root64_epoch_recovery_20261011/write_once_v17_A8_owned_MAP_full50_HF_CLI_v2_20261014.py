#!/usr/bin/env python3
"""One reviewed v17 HF/CLI publication; no Host import, compiler or solver.

Source-only until the final candidate, genuine Source-generation receipt and
independent same-round Source review exist. Inherited scientific dependencies
receive current7 checks, while Source and metadata receive complete EOF pins.
Only the exact18 approved duplicate-body rows leave current roles.
"""
from pathlib import Path
import argparse,ast,hashlib,json,os,stat

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
HERE=REC/'aaa_three_plane_A8_owned_MAP_pipeline_source_v17_20261014'
HF=HERE/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'
CLI=HERE/'DECLARED_EXECUTION_INTERFACE.json'
PLAN=HERE/'ACTUAL_OWNED_RUNTIME_BOUND_V17_SOURCE_PREPARATION_PLAN.json'
READY=HERE/'SOURCE_REVIEW_READY.json'

def seven(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path):
    path=Path(path);before=seven(path.lstat())
    if path.is_symlink()or not stat.S_ISREG(before[2]):raise RuntimeError('ordinary exact Source/current metadata')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if seven(os.fstat(fd))!=before:raise RuntimeError('opened exact7 differs')
        with os.fdopen(fd,'rb')as stream:
            fd=None;raw=stream.read()
            if seven(os.fstat(stream.fileno()))!=before:raise RuntimeError('full EOF exact7 differs')
    finally:
        if fd is not None:os.close(fd)
    if seven(path.lstat())!=before:raise RuntimeError('after exact7 differs')
    return raw,dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)

def fullpin(row):
    if not isinstance(row,dict)or set(row)!={'path','sha256','size_bytes','identity'}or not isinstance(row['path'],str)or not Path(row['path']).is_absolute()or not isinstance(row['sha256'],str)or len(row['sha256'])!=64 or any(c not in '0123456789abcdef'for c in row['sha256'])or type(row['size_bytes'])is not int or not isinstance(row['identity'],list)or len(row['identity'])!=7 or any(type(v)is not int for v in row['identity'])or row['identity'][4]!=row['size_bytes']or not stat.S_ISREG(row['identity'][2]):raise RuntimeError('canonical full PF')
    return row

def read(row):
    fullpin(row);raw,current=pin(row['path'])
    if current!=row:raise RuntimeError('bound complete exact PF differs: '+row['path'])
    return json.loads(raw)

def unique(rows):
    table={}
    for row in rows:
        fullpin(row)
        if row['path']in table and table[row['path']]!=row:raise RuntimeError('inconsistent complete PF')
        table[row['path']]=row
    return list(table.values())

def current7(rows):
    for row in unique(rows):
        p=Path(row['path'])
        if p.is_symlink()or seven(p.lstat())!=row['identity']:raise RuntimeError('current dependency exact7 differs: '+row['path'])

def live(rows,retired):
    table={r['path']:r for r in unique(retired)};out=[]
    for row in rows:
        if row['path']in table:
            if row!=table[row['path']]:raise RuntimeError('only declared exact historical PF excluded from current')
        else:out.append(row)
    return unique(out)

def write(path,value):
    with path.open('x')as stream:
        json.dump(value,stream,indent=2,ensure_ascii=False,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    _,row=pin(path)
    if row['identity'][3]!=1:raise RuntimeError('own output single-link')
    return row

def external(args,prefix):
    raw,row=pin(getattr(args,prefix+'_summary'))
    if row['sha256']!=getattr(args,prefix+'_sha256')or row['identity']!=json.loads(getattr(args,prefix+'_seven_id')):raise RuntimeError('external complete PF differs')
    return json.loads(raw),row

def fullpins(value):
    if isinstance(value,dict):
        if set(value)=={'path','sha256','size_bytes','identity'}:yield fullpin(value)
        else:
            for item in value.values():yield from fullpins(item)
    elif isinstance(value,list):
        for item in value:yield from fullpins(item)

def terminal0(tools,key):
    result=tools[key]
    if not isinstance(result,dict)or type(result.get('exit_code'))is not int or result['exit_code']!=0 or result.get('session_id')is not None or tools.get('observed_closed')is not True or type(tools.get('original_integer_exit_code'))is not int or tools['original_integer_exit_code']!=0:raise RuntimeError('genuine observed closed integer0 without session')
    return result

def main():
    p=argparse.ArgumentParser(allow_abbrev=False)
    for prefix in ('peer-review','peer-tools','Source-generation-tools'):
        for suffix in ('summary','sha256','seven-id'):p.add_argument('--'+prefix+'-'+suffix,required=True)
    args=p.parse_args();review,review_pin=external(args,'peer_review');tools,tools_pin=external(args,'peer_tools');generation,generation_pin=external(args,'Source_generation_tools')
    result=terminal0(tools,'actual_review_return');lines=result['output'].strip().splitlines()
    if not lines or json.loads(lines[-1])['review_pin']!=review_pin:raise RuntimeError('independent actual Source-review stdout exact review PF')
    if review.get('failure','MISSING')is not None or not isinstance(review.get('status'),str)or not review['status'].startswith('PASS')or review.get('source_only')is not True or review.get('numerical_executed')is not False:raise RuntimeError('same-round independent final candidate/writer Source-only review')
    generated=terminal0(generation,'actual_Source_preparation_return');generated_lines=generated['output'].strip().splitlines()
    if not generated_lines:raise RuntimeError('genuine Source generation stdout')
    observed=json.loads(generated_lines[-1])
    if any(observed.get(k)is not False for k in ('compiler_executed','numerical_executed','pipeline_executed','files_deleted')):raise RuntimeError('Source-only generation was not business')
    plan_raw,plan_pin=pin(PLAN);plan=json.loads(plan_raw);ready_raw,ready_pin=pin(READY);ready=json.loads(ready_raw)
    if plan.get('schema')!='ACTUAL_OWNED_RUNTIME_BOUND_V17_SOURCE_PREPARATION_PLAN_V1'or plan.get('source_only')is not True or any(plan.get(k)is not False for k in ('compiler_executed','numerical_executed','pipeline_executed','files_deleted'))or any(k not in plan or plan[k]is not None for k in ('own_Host_freeze_pin','own_CLI_pin','future_actual_v17_report_pin'))or ready['host_source']!=plan['host_source']or ready['plan_pin']!=plan_pin or ready['inverse_pin']!=plan['complete_byte_inverse_pin']or ready.get('failure','MISSING')is not None:raise RuntimeError('final bound Source-only plan/ready and null future pipeline PF')
    if observed['host_source']!=plan['host_source']or observed['plan_pin']!=plan_pin or observed['ready_pin']!=ready_pin or observed['inverse_pin']!=plan['complete_byte_inverse_pin']:raise RuntimeError('genuine Source-generation stdout exact four candidate PFs')
    raw,host=pin(HERE/'run_actual_three_plane_pipeline.py');tree=ast.parse(raw)
    if host!=plan['host_source']:raise RuntimeError('actual owning Host Source')
    reviewed=list(fullpins(review));ownpins=[host,plan_pin,ready_pin,plan['complete_byte_inverse_pin'],plan['direct_alias_binding_pin'],pin(__file__)[1],plan['preparer_source_pin']]+[x['candidate_pin']for x in plan['helper_byte_equality']]
    if any(row not in reviewed for row in ownpins):raise RuntimeError('peer same-round review includes every exact candidate/helper/writer/preparer Source PF')
    original=read(plan['predecessor_v16_Host_freeze_pin']);prior_plan=read(original['actual_prerequisite_bound_Source_plan_pin']);inverse=read(plan['complete_byte_inverse_pin']);restored=raw.decode()
    for change in reversed(inverse['changes']):
        if restored.count(change['after'])!=1:raise RuntimeError('unambiguous actual whole Host inverse')
        restored=restored.replace(change['after'],change['before'],1)
    previous,previous_pin=pin(original['host_source']['path'])
    if previous_pin!=original['host_source']or restored.encode()!=previous or inverse['original_pin']!=previous_pin or inverse['candidate_pin']!=host or inverse.get('original50_continuous_source_unchanged')is not True or inverse.get('original_compact40_fourcontrols_Driver37_budget_functions_wholebytes_unchanged')is not True:raise RuntimeError('whole v16 byte inverse; original50 and all original admission functions intact')
    if len(original['dependencies'])!=2920 or len(prior_plan['original377_dependency_rows_to_retain'])!=377:raise RuntimeError('exact old v16 2920 and original377 Source lineage')
    for helper in plan['helper_byte_equality']:
        a,ap=pin(helper['predecessor_pin']['path']);b,bp=pin(helper['candidate_pin']['path'])
        if ap!=helper['predecessor_pin']or bp!=helper['candidate_pin']or a!=b:raise RuntimeError('whole three original helper files')
    spec=read(plan['binding_spec_pin']);selected=plan['selected_actual_prerequisites'];retired=plan['historical_retired_exact_private_body_pins'];release_sf=read(selected['selected_exact18_release_Source_freeze_pin']);targets=release_sf['literal18_fullpins']
    if targets!=spec['additional_exact_retired_body_pins']or len(targets)!=18 or sum(x['size_bytes']for x in targets)!=1604468368 or any(Path(x['path']).exists()or Path(x['path']).is_symlink()for x in targets):raise RuntimeError('actual exact18 approved duplicate nines remain absent')
    if plan['truthful_retained_scientific_input_count']!=9 or len(plan['retained_original_science_nine_input_pins'])!=9 or plan['exact18_release_contract']!=spec['exact18_release_contract']:raise RuntimeError('truthful originalSCI9 after exact18 Source role migration')
    old_cli_path=REC/'aaa_three_plane_cache336_pipeline_source_v16_20261014/DECLARED_EXECUTION_INTERFACE.json';old_cli_raw,old_cli_pin=pin(old_cli_path);old_cli=json.loads(old_cli_raw)
    dependencies=unique(live(plan['dependencies']+original['dependencies']+prior_plan['original377_dependency_rows_to_retain'],retired)+ownpins+[plan['binding_spec_pin'],plan['predecessor_v16_Host_freeze_pin'],old_cli_pin,generation_pin,review_pin,tools_pin])
    current7(dependencies)
    if any(row not in dependencies for row in live(original['dependencies']+prior_plan['original377_dependency_rows_to_retain'],retired)):raise RuntimeError('every unretired2920/377 PF remains current')
    if any(row not in dependencies for row in fullpins(selected)):raise RuntimeError('all selected actual Source/prerequisite proof PFs belong to current HF')
    main=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
    prefix_nodes=[n for n in main.body if isinstance(n,ast.For)and isinstance(n.target,ast.Name)and n.target.id=='prefix']
    if len(prefix_nodes)!=1:raise RuntimeError('one literal actual main external prefix loop')
    prefixes=ast.literal_eval(prefix_nodes[0].iter)
    if prefixes!=old_cli['mandatory_external_prefixes']+['owned-runtime']or len(prefixes)!=14:raise RuntimeError('actual parser old13 plus only owned-runtime')
    bound=dict(old_cli['mandatory_external_fullpin_bindings']);bound['owned-runtime']=selected['selected_actual_owned_runtime_report_pin']
    if len(old_cli['exact_reviewable_argv'][:11])!=11 or 12+6*len(prefixes)!=96 or set(bound)!=set(prefixes):raise RuntimeError('complete final96 interface validated before HF publication')
    for prefix in prefixes:fullpin(bound[prefix])
    # All validation and Source/metadata reads precede the once-only writes.
    if HF.exists()or HF.is_symlink()or CLI.exists()or CLI.is_symlink()or Path(plan['planned_output_root']).exists()or Path(plan['planned_output_root']).is_symlink():raise RuntimeError('one absent future HF/CLI/business OUT namespace')
    freeze=dict(original);freeze.update(schema='COMPLETE_ACTUAL_AAA3_A8_OWNED_MAP_PIPELINE_HOST_SOURCE_FREEZE_V17',host_source=host,dependencies=dependencies,
      predecessor_host_freeze=plan['predecessor_v16_Host_freeze_pin'],predecessor_source_claims_are_historical_declarations=True,
      actual_dependency_count=len(dependencies),actual_prerequisite_bound_Source_plan_pin=plan_pin,complete_V16_to_V17_byte_inverse_pin=plan['complete_byte_inverse_pin'],
      independent_V17_candidate_Source_review_pin=review_pin,independent_V17_candidate_Source_true_tool_pin=tools_pin,actual_Source_generation_true_tool_pin=generation_pin,
      once_writer_Source_pin=pin(__file__)[1],actual_independent_Source_review_return=0,prepared_only=True,actual_pipeline_executed=False,actual_qualified_numeric_pipeline=False,
      no_prefilled_actual_success=True,Source_revision_scope='retain original compactQ40/fourcontrols/Driver37/338121 and original50; admit owned18 repaired only1 runtime with original Root1 parser failure transparently retained plus independent complete-pair readback0',
      historical_retired_exact_private_body_pins=retired,exact18_release_contract=plan['exact18_release_contract'],retained_original_science_nine_input_pins=plan['retained_original_science_nine_input_pins'],
      truthful_retained_scientific_input_count=9,ancestor_sealed_output_tables_never_promoted=True,no_generic_missing_pin_skip=True,original_caps=plan['original_caps'],
      current_owned_runtime_ordered70_pins=plan['current_owned_runtime_ordered70_pins'],same_original_50_stages_17_positive_33_exact_negative_controls=True,
      runtime_compact40_then_Driver37_separate_admission=True,runtime_owned_A8_only1_with_other69_preserved=True,runtime_bootstrap9_exact=True,
      mathematics_conditions_thresholds_four_helper_Source_bytes_unchanged=True,only_single_BOOT0_prerequisite_not_full50_qualification=True,
      original_owned_Runtime_Root_exit1_and_failed_summary_TB_preserved=True,independent_original_helper_readback0_not_second_solver_run=True,
      physics_qualification=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,
      future_actual_v17_summary_pin=None,future_actual_v17_raw_pin=None,future_actual_v17_capture_pins=None,**selected)
    current7(dependencies);hf_pin=write(HF,freeze);bound['host-freeze']=hf_pin
    argv=old_cli['exact_reviewable_argv'][:11]+[host['path']]
    for prefix in prefixes:
        row=fullpin(bound[prefix]);argv+=['--'+prefix+'-summary',row['path'],'--'+prefix+'-sha256',row['sha256'],'--'+prefix+'-seven-id',json.dumps(row['identity'],separators=(',',':'))]
    if len(argv)!=96:raise RuntimeError('exact actual parser final96 argv tokens')
    interface=dict(old_cli);interface.update(schema='DECLARED_ACTUAL_AAA3_A8_OWNED_MAP_ONE_SERIAL_50_STAGE_INTERFACE_V17',host_source=host['path'],host_source_pin=host,
      output_root=plan['planned_output_root'],mandatory_external_prefixes=prefixes,mandatory_external_fullpin_bindings=bound,exact_reviewable_argv=argv,
      selected_actual_prerequisites=selected,selected_own_Host_freeze_pin=hf_pin,Source_revision_scope=freeze['Source_revision_scope'],original50_math_and_caps_unchanged=True,
      actual_pipeline_executed=False,compiler_executed_by_this_prepare=False,mathematical_or_material_or_threshold_changes=False,
      exact18_retired_duplicate_body_count=18,retained_original_scientific_input_count=9,whole_module6092_ABI_actual_prerequisite_verified=True,
      actual_future_v17_reports=None,AAA_qualified=False,ABA_admitted=False,goal_complete=False,predecessor_interface_claims_are_historical_declarations=True)
    cli_pin=write(CLI,interface);current7(dependencies)
    print(json.dumps(dict(status='V17_ACTUAL_OWNED_RUNTIME_BOUND_HOST_SOURCE_HF_CLI_FROZEN_ONLY',host_source=host,host_freeze_pin=hf_pin,CLI_pin=cli_pin,
      actual_dependency_count=len(dependencies),mandatory_external_prefix_count=len(prefixes),actual_argv_count=len(argv),actual_pipeline_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)

if __name__=='__main__':main()
