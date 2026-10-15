#!/usr/bin/env python3
"""Prepare new v15 Sources only after exact public7 actual inputs are supplied.

No compiler, control, pipeline or cleanup is imported or run. Own HF/CLI are
left uncreated for a separate independent exact candidate Source review.
"""
from pathlib import Path
import argparse,ast,hashlib,json,os,shlex,stat

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
SOURCE_PLAN=REC/'V15_ACTUAL_PREREQUISITE_PREPARER_SOURCE_PLAN_V2_20261014.json'
OLD=REC/'aaa_three_plane_compact_expected_pipeline_source_draft_v2_20261013'
NEW=REC/'aaa_three_plane_compact_expected_pipeline_source_v15_20261014'
NEW_OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261014-v15')
RETIREMENT=REC/'v15_exact_completed_SRC_retirement_admission_source_v1_20261014.py'

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
    path=getattr(args,key+'_summary');raw,row=pin(path)
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

def walk_fullpins(value):
    if isinstance(value,dict):
        if set(value)=={'path','sha256','size_bytes','identity'}:
            yield exact_pin(value)
        else:
            for child in value.values():yield from walk_fullpins(child)
    elif isinstance(value,list):
        for child in value:yield from walk_fullpins(child)

def require_public_post0(tools,report_pin):
    actual=tools.get('actual_review_return')
    require_terminal0(actual)
    if tools.get('observed_closed')is not True:raise RuntimeError('genuine public actual post-review closed flag')
    lines=actual.get('output','').strip().splitlines()
    if not lines:raise RuntimeError('actual public post-review output must bind exact review pin')
    review_pin=exact_pin(json.loads(lines[-1])['review_pin']);review=read(review_pin)
    if review.get('failure')is not None or not isinstance(review.get('status'),str)or not review['status'].startswith('PASS')or \
       report_pin not in list(walk_fullpins(review)):
        raise RuntimeError('public actual successful post-review must bind exact report fullpin')
    return review_pin

def main():
    parser=argparse.ArgumentParser()
    for prefix in ('preparation-plan','public7','public7-root-tool','public7-post-tools'):
        for suffix in ('summary','sha256','seven-id'):parser.add_argument('--'+prefix+'-'+suffix,required=True)
    args=parser.parse_args()
    source_plan,source_plan_pin=external(args,'preparation_plan')
    if source_plan_pin['path']!=str(SOURCE_PLAN)or source_plan.get('schema')!='V15_ACTUAL_PREREQUISITE_PREPARER_SOURCE_PLAN_V1'or \
       any(source_plan.get(k)is not False for k in ('compiler_executed','numerical_executed','pipeline_executed','files_deleted'))or \
       any(k not in source_plan or source_plan[k]is not None for k in ('future_actual_public7_report_pin','future_actual_public7_Root_tool_pin',
          'future_actual_public7_post_review_pin','future_actual_public7_post_tools_pin','future_actual_v15_Host_freeze_pin',
          'future_actual_v15_CLI_pin','future_actual_v15_report_pin')):
        raise RuntimeError('exact unexecuted preparer Source plan with future actual PFs None')
    selected=source_plan['selected_existing_pins'];values={k:read(v)for k,v in selected.items()}
    if pin(__file__)[1]!=source_plan['preparer_source_pin']or pin(RETIREMENT)[1]!=source_plan['retirement_admission_Source_pin']:
        raise RuntimeError('preparer and exact retirement Source bytes differ from reviewed plan')
    public,public_pin=external(args,'public7')
    root_tools,root_tools_pin=external(args,'public7_root_tool')
    post_tools,post_tools_pin=external(args,'public7_post_tools')
    if public_pin['path']!=source_plan['expected_actual_public7_report_path']:
        raise RuntimeError('only exact public7 current actual report namespace')
    require_terminal0(root_tools.get('actual_terminal_return'))
    if shlex.split(root_tools.get('exact_executed_command',''))!=values['Root_public7_exact_argv']['argv']:
        raise RuntimeError('genuine Root public7 terminal0 belongs to exact frozen thirty-argument command')
    public_post_pin=require_public_post0(post_tools,public_pin)
    reports=dict(new_build70=values['actual_new_build70_report'],fresh17=values['actual_fresh17_report'],
                 private_model=values['actual_private_model_report'],public7=public)
    report_pins=dict(new_build70=selected['actual_new_build70_report'],fresh17=selected['actual_fresh17_report'],
                     private_model=selected['actual_private_model_report'],public7=public_pin)
    expected=[('new_build70',2,'ACTUAL_ONE_BOOTQ_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'),
      ('fresh17',20,'ACTUAL_NEW_BOOTQ_CURRENT17_CONNECTED_CONTROLS_CLOSED0_ONLY'),
      ('private_model',3,'ACTUAL_PRIVATE_GANLIB_MODEL_CONTROLS_CLOSED0_ONLY'),
      ('public7',11,'ACTUAL_SEVEN_GENUINE_PUBLIC_READ_CONTROLS_NINE_PHASES_CLOSED0_ONLY')]
    for role,count,status in expected:
        d=reports[role]
        if d.get('status')!=status or d.get('failure')is not None or d.get('after_check_error')is not None or \
           d.get('secondary_failures')!=[]or d.get('final_report_resource_check_passed')is not True or \
           d.get('original_guard_class')!='OwnRSSSerialExecutor'or d.get('original_guard_MRO_unchanged')is not True or \
           len(d['records'])!=count or any(x.get('status')!='PASS'for x in d['records'])or \
           type(d.get('SELF_peak_bytes'))is not int or not 0<=d['SELF_peak_bytes']<512*2**20 or \
           type(d.get('wall_seconds'))not in (int,float)or not 0<d['wall_seconds']<1800:
            raise RuntimeError('exact closed guarded prerequisite status/count/caps: '+role)
        own_key={'new_build70':'new_build_Host_freeze','fresh17':'fresh17_Host_freeze',
          'private_model':'private_model_Host_freeze','public7':'public7_Host_freeze'}[role]
        if d.get('actual_host_Source_freeze_pin')!=selected[own_key]:
            raise RuntimeError('actual prerequisite belongs to selected exact own SourceHF: '+role)
        if d.get('actual_new_Source_freeze_pin'if role=='new_build70'else'actual_new_build70_report_pin')!= \
           (selected['compact_Fortran_Source_freeze']if role=='new_build70'else report_pins['new_build70']):
            raise RuntimeError('actual prerequisite selects same compact SF or genuine newbuild: '+role)
    if public.get('actual_seven_genuine_public_READ_controls_passed')is not True or \
       public.get('actual_model_controls_passed')is not False or public.get('new_reader_qualified')is not False or \
       public.get('physics_qualified')is not False or len(public['actual_control_results'])!=9 or \
       len(public['actual_stale_host_evidence'])!=2 or len(public.get('actual_completed_bundle_retirements',[]))!=1:
        raise RuntimeError('actual public7 scope and complete sole completed SRC retirement required')
    old14=values['original_v14_Host_freeze'];old_plan=values['predecessor_draft_plan']
    if len(old14['dependencies'])!=377 or old_plan['original377_dependency_rows_to_retain']!=old14['dependencies']:
        raise RuntimeError('all original377 dependencies remain exact')
    selection=dict(selected_actual_new_build70_report_pin=report_pins['new_build70'],
      selected_new_build_Host_freeze_pin=selected['new_build_Host_freeze'],
      selected_new_Fortran_Source_freeze_pin=selected['compact_Fortran_Source_freeze'],
      selected_actual_fresh17_report_pin=report_pins['fresh17'],selected_fresh17_Host_freeze_pin=selected['fresh17_Host_freeze'],
      selected_actual_private_model_report_pin=report_pins['private_model'],selected_private_model_Host_freeze_pin=selected['private_model_Host_freeze'],
      selected_actual_public7_report_pin=public_pin,selected_public7_Host_freeze_pin=selected['public7_Host_freeze'],
      selected_completed_first_SRC_bundle_lifetime_Source_plan_pin=selected['public7_lifetime_Source_plan'],
      selected_post_release_Common_Source_freeze_pin=selected['current_Common_Source_freeze'])
    deps=list(old14['dependencies'])+[selected['original_v14_Host_freeze'],source_plan_pin,source_plan['preparer_source_pin'],
      source_plan['retirement_admission_Source_pin'],root_tools_pin,post_tools_pin,public_post_pin]+list(selected.values())+[public_pin]
    for key in ('new_build_Host_freeze','fresh17_Host_freeze','private_model_Host_freeze','public7_Host_freeze'):
        own=values[key];deps.extend(own['dependencies']);deps.append(own['host_source'])
    for role in reports:
        deps.extend(reports[role]['fixed_current_pins']);deps.extend(reports[role]['output_pins'])
    deps=unique(deps);recheck(deps)
    if NEW.exists()or NEW.is_symlink()or NEW_OUT.exists()or NEW_OUT.is_symlink():raise RuntimeError('fresh unique final candidate Source and future own OUT only')
    raw,old_host_pin=pin(OLD/'run_actual_three_plane_pipeline.py');text=raw.decode();changes=[]
    def replace(before,after,reason):
        nonlocal text
        if text.count(before)!=1:raise RuntimeError('one exact Source splice: '+reason)
        changes.append(dict(before=before,after=after,reason=reason));text=text.replace(before,after,1)
    replace("OUT=Path('"+old_plan['planned_output_root']+"')","OUT=Path('"+str(NEW_OUT)+"')",'unique v15 own output literal')
    for exact in ("+       direct_binding['actual_complete70_source_freeze_pin']!=compact['source_freeze_pin']or ",
                  "+       direct_original_inputs!=compact['current70_pins']or "):
        replace(exact,exact[1:],'remove one literal leading plus token; preserve strict comparison')
    retirement_text=pin(RETIREMENT)[0].decode();tree=ast.parse(retirement_text)
    first_function=next(x for x in tree.body if isinstance(x,ast.FunctionDef))
    retirement_functions='\n'.join(retirement_text.splitlines()[first_function.lineno-1:])+'\n\n'
    replace('def admit_compact_controls(args,hf,helper,compact,old17,pold17):',
            retirement_functions+'def admit_compact_controls(args,hf,helper,compact,old17,pold17):','add exact SRC completed-retirement/MAC-current admission only')
    block_start=text.index("                if {x['case']for x in stale}!=")
    block_end=text.index('        fixed.extend([pd,pown,own',block_start)
    replace(text[block_start:block_end],
      '                admit_exact_public_stale_lifetimes(hf,own,plan,d,root,exe)\n','replace stale current-bundle checks with strict sole SRC lifetime gate')
    ast.parse(text);inverse=text
    for block in reversed(changes):
        if inverse.count(block['after'])!=1:raise RuntimeError('unambiguous complete Source inverse')
        inverse=inverse.replace(block['after'],block['before'],1)
    if inverse.encode()!=raw:raise RuntimeError('whole-file inverse must recover entire draft2 bytes')
    old14_raw=pin(REC/'aaa_three_plane_streaming_pipeline_source_v14/run_actual_three_plane_pipeline.py')[0]
    protected=old14_raw[old14_raw.index(b'    try:\n        # Replace ONLY the main object'):old14_raw.index(b'        raw=dict(schema=')]
    if protected not in text.encode():raise RuntimeError('original guarded50 continuous body and math must remain wholebytes')
    NEW.mkdir();host_pin=write(NEW/'run_actual_three_plane_pipeline.py',text);helpers=[]
    for name in ('actual_inputs_and_readback.py','direct_alias_entry_controls.f90','mutate_owned_control.f90'):
        data,previous=pin(OLD/name);current=write(NEW/name,data)
        helpers.append(dict(predecessor_pin=previous,candidate_pin=current,whole_bytes_unchanged=True))
    direct=dict(values['predecessor_direct_binding']);new70=reports['new_build70']['actual_complete70_link_inputs']
    table={x['path']:x for x in unique(reports['new_build70']['fixed_current_pins']+reports['new_build70']['output_pins'])}
    ordered=[table[path]for path in new70]
    if len(ordered)!=70 or len(set(new70))!=70 or ordered[12]!=direct['excluded_original_main_pin']:
        raise RuntimeError('genuine actual new ordered70 retains exact old main12 for direct alias replacement')
    direct.update(selected_actual_build70_report_pin=report_pins['new_build70'],actual_original_ordered_70_link_inputs=ordered,
      actual_complete70_source_freeze_pin=selected['compact_Fortran_Source_freeze'],
      new_probe_source=str(NEW/'direct_alias_entry_controls.f90'),Source_only_parameterized_template=False,actual_pipeline_executed=False)
    direct_pin=write_json(NEW/'DIRECT_ALIAS_ENTRY_BINDING.json',direct)
    inverse_pin=write_json(NEW/'COMPLETE_DRAFT2_TO_V15_ACTUAL_ADMISSION_WHOLE_BYTE_INVERSE.json',dict(
      schema='COMPLETE_DRAFT2_TO_V15_ACTUAL_ADMISSION_WHOLE_BYTE_INVERSE_V1',original_pin=old_host_pin,candidate_pin=host_pin,
      changes=changes,whole_restored_bytes_equal=True,restored_sha256=hashlib.sha256(inverse.encode()).hexdigest(),
      original50_continuous_source_bytes=len(protected),original50_continuous_source_sha256=hashlib.sha256(protected).hexdigest(),
      original50_continuous_source_unchanged=True,helpers=helpers,direct_binding_predecessor_pin=selected['predecessor_direct_binding'],
      direct_binding_actual_pin=direct_pin,direct_binding_old_data=values['predecessor_direct_binding'],source_only=True,
      compiler_executed=False,numerical_executed=False,files_deleted=False))
    deps=unique(deps+[direct_pin,inverse_pin]+[x['candidate_pin']for x in helpers]);recheck(deps)
    plan_pin=write_json(NEW/'ACTUAL_PREREQUISITE_BOUND_V15_SOURCE_PREPARATION_PLAN.json',dict(
      schema='ACTUAL_PREREQUISITE_BOUND_V15_SOURCE_PREPARATION_PLAN_V1',source_only=True,host_source=host_pin,
      original_v14_Host_freeze_pin=selected['original_v14_Host_freeze'],original377_dependency_rows_to_retain=old14['dependencies'],
      selected_actual_prerequisites=selection,dependencies=deps,complete_byte_inverse_pin=inverse_pin,
      direct_alias_binding_pin=direct_pin,helper_byte_equality=helpers,planned_output_root=str(NEW_OUT),
      actual_prerequisite_counts=dict(new_build70=2,fresh17=20,private_model=3,public7=11),
      original_pipeline_records_expected=dict(total=50,PASS=17,expected_refusal=33),
      original_caps=old_plan['original_caps'],strict_forecast_MiB=old_plan['strict_forecast_MiB'],
      public7_actual_Root_tool_pin=root_tools_pin,public7_actual_post_review_pin=public_post_pin,
      public7_actual_post_tools_pin=post_tools_pin,current_Common_Source_freeze_pin=selected['current_Common_Source_freeze'],
      actual_pipeline_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,
      own_Host_freeze_pin=None,own_CLI_pin=None,future_actual_v15_report_pin=None,AAA_qualified=False,ABA_admitted=False))
    ready_pin=write_json(NEW/'SOURCE_REVIEW_READY.json',dict(schema='V15_ACTUAL_PREREQUISITE_BOUND_CANDIDATE_SOURCE_REVIEW_READY_V1',
      status='SOURCE_ONLY_CANDIDATE_READY_FOR_INDEPENDENT_SOURCE_REVIEW',failure=None,host_source=host_pin,plan_pin=plan_pin,
      inverse_pin=inverse_pin,helpers=helpers,direct_binding_pin=direct_pin,original377_all_retained=True,
      original50_continuous_source_unchanged=True,strict_SRC_retired_MAC_current_admission=True,
      selected_actual_prerequisites=selection,source_change_blocks=len(changes),source_only=True,
      compiler_executed=False,numerical_executed=False,pipeline_executed=False,files_deleted=False,
      actual_Host_freeze_pin=None,actual_CLI_pin=None,actual_v15_report_pin=None))
    print(json.dumps(dict(status='V15_ACTUAL_PREREQUISITE_BOUND_SOURCE_CANDIDATE_CREATED_ONLY',host_source=host_pin,
      plan_pin=plan_pin,ready_pin=ready_pin,inverse_pin=inverse_pin,actual_dependency_count=len(deps),
      compiler_executed=False,numerical_executed=False,pipeline_executed=False,files_deleted=False),ensure_ascii=False))

if __name__=='__main__':main()
