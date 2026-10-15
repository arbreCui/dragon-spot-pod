"""Root Source/small-META postclose assembler. No candidate/process/API import.

Only reads Source or explicitly saved control facts/raw META. It cannot supply
missing OS observations. Root records actual terminal/group/resource evidence;
an independent saved-controls review is still mandatory before qualification.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
CASE_IDS=('01_exact_environment_and_sole_wait_owner','02_actual_live_business_and_descendants','03_actual_closed_after_live_PS_census','04_actual_nonzero_exit_preserves_stage_failure','05_actual_closed_leader_and_reparented_group','06_unknown_owner_ECHILD_and_PID_reuse_refusals','07_actual_late_descendant_exit_strict_lsof_failure','08_actual_strict_stream_nonzero_timeout_oversize','09_original_resource_caps_and_frozen_Source','10_original_cleanup_exceptions_and_group_evidence','11_actual_watchdog_pipe_and_group_closure','12_actual_Root_and_independent_saved_control_closure')

def require(v,m):
    if type(v) is not bool or not v:raise ValueError(m)

def strict_json(raw):
    def pairs(items):
        d={}
        for k,v in items:require(k not in d,'duplicate actual controls saved key');d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))

def fullpin(path):
    p=Path(path);s=p.lstat();ident=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    require(p.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and all(not q.is_symlink()for q in(p,*p.parents)),'actual complete regular singlelink Source/control META')
    with p.open('rb')as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    t=p.lstat();require([t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==ident,'complete actual Source/control EOF')
    return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ident)

def read_actual(path):
    return fullpin(path),strict_json(Path(path).read_bytes())

def actual_zero(path,schema):
    pin,w=read_actual(path);t=w['terminal_tool_return']
    require(w['schema']==schema and w['closed']is True and w['observed_terminal']is True and w['session_repolled_after_close']is False and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and type(t['chunk_id'])is str and t['chunk_id']==w['actual_terminal_chunk'],'actual CLOSED0 saved Root controls tool')
    return pin,strict_json(t['output'])

def tree(path):
    p=Path(path);files=[];directories={}
    for q in [p,*sorted(p.rglob('*'))]:
        s=q.lstat();require(not stat.S_ISLNK(s.st_mode),'control namespace noaliases')
        if stat.S_ISDIR(s.st_mode):directories[str(q)]=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
        else:files.append(fullpin(q))
    return dict(files=files,directories=directories)

def write_new(path,value):
    p=Path(path);require(p.is_absolute()and p.parent.is_dir()and not os.path.lexists(p),'fresh Source/META output')
    with p.open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
    return fullpin(p)

def case_mode(a):
    fp,f=read_actual(a.facts);binding_pin,b=read_actual(a.binding)
    require(f['schema']=='ACTUAL_N8_GENUINE_MONITOR_CONTROL_CASE_FACTS_V1'and f['case_id']in CASE_IDS and f['actual_controls_Source_binding_pin']==binding_pin and f['actual_author_Source_contract']==b['actual_author_Source_contract'],'actual case Source binding and complete owners')
    tp,out=actual_zero(a.case_terminal,'ROOT_ACTUAL_N8_MONITOR_CONTROL_CASE_TOOL_TERMINAL_RETURN_V1');require(out['actual_control_case_facts_pin']==fp and out['actual_monitor_controls_qualification']is None,'Root actual case output couples saved facts, no self-qualification')
    gp,g=read_actual(a.current_group_closure);gt,gout=actual_zero(a.current_group_terminal,'ROOT_ACTUAL_N8_CONTROL_GROUP_CLOSURE_TOOL_TERMINAL_RETURN_V1')
    require(gout['actual_current_group_closure_pin']==gp,'Root actual group tool output exact saved diagnostic pin')
    require(g['schema']=='ROOT_ACTUAL_N8_CONTROL_CASE_CURRENT_GROUP_CLOSURE_V1'and g['actual_control_case_facts_pin']==fp and g['actual_current_process_groups_absent']is True and g['kill_action_performed']is False and g['historical_cleanup_success_inferred']is False,'separately observed current group closure, no historical cleanup claim')
    require(type(g['actual_full_PS_returncode'])is int and g['actual_full_PS_returncode']==0 and type(g['actual_full_PS_stdout'])is str and type(g['actual_full_PS_stderr'])is str and g['streams_complete']is True,'actual strict complete PS closure raw')
    rows={}
    for line in g['actual_full_PS_stdout'].splitlines():
        w=line.split();require(len(w)==4 and all(x.isdigit()for x in w[:3]),'real complete closure pid/ppid/pgid/state table');p,pp,pg=map(int,w[:3]);require(p>0 and p not in rows,'unique closure PID');rows[p]=(pp,pg,w[3])
    owners=f['actual_exact_owner_state']['owners'];targets={f['actual_host_PID']}|{o['pid']for o in owners};groups={o['pgid']for o in owners}
    for event in f['actual_gate_events']:
        ready=event.get('actual_ready')
        if ready is not None and type(ready.get('descendant_pid'))is int:targets.add(ready['descendant_pid'])
    require(g['actual_target_PIDs']==sorted(targets) and g['actual_target_PGIDs']==sorted(groups),'complete actual owner/host/descendant/group targets, no omission')
    require(not any(p in targets or pp in targets or pg in groups for p,(pp,pg,state)in rows.items()),'current full PS no owned target/group/parent remnants')
    rp,r=read_actual(a.postclose_resources);rt,rout=actual_zero(a.postclose_resource_terminal,'ROOT_ACTUAL_N8_CONTROL_POSTCLOSE_RESOURCE_TOOL_TERMINAL_RETURN_V1')
    require(rout['actual_postclose_resource_pin']==rp,'Root actual resource tool output exact saved META pin')
    require(r['schema']=='ROOT_ACTUAL_N8_CONTROL_CASE_POSTCLOSE_RESOURCE_V1'and r['actual_control_case_facts_pin']==fp and r['original_caps']==CAPS and r['actual_original_resource_factory_pin']==f['actual_original_resource_pin'],'actual Root original resource factory and original caps')
    HOCDE=b['case_namespaces'][f['case_id']];views={k:tree(v)for k,v in HOCDE.items()}
    require(views['source']==f['actual_complete_Source_D_freeze'] and views['receipts']==f['actual_complete_receipt_E_freeze'],'complete actual D/E exact frozen after Root close')
    total=sum(p['size_bytes']for v in views.values()for p in v['files']);external=sum(p['size_bytes']for k in('source','receipts')for p in views[k]['files'])
    require(type(r['artifact_bytes'])is int and type(r['disk_free_bytes'])is int and total<2*2**30 and r['artifact_bytes']+external<=96*2**30 and r['disk_free_bytes']>=8*2**30,'actual closed full HOCDE/history/free original bounds')
    require(f['actual_original_caps']==CAPS and f['actual_original_guard_classes_MRO_modified']is False and f['canonical_OS_nonzero_timeout_oversize_or_EPERM_manufactured']is False,'original guards and no manufactured canonical OS failures')
    value=dict(schema='ROOT_ACTUAL_N8_MONITOR_CONTROL_CASE_POSTCLOSE_V1',case_id=f['case_id'],passed=True,actual_author_Source_contract=b['actual_author_Source_contract'],actual_controls_Source_binding_pin=binding_pin,actual_control_case_facts_pin=fp,actual_Root_case_tool_terminal_return_pin=tp,actual_current_group_closure_pin=gp,actual_current_group_tool_terminal_pin=gt,actual_Root_postclose_resource_pin=rp,actual_Root_postclose_resource_terminal_pin=rt,actual_complete_postclose_namespace_views=views,actual_complete_joint_bytes=total,actual_genuine_runner_used=True,actual_shared_resource_factory_used=True,actual_exact_owner_observer_used=True,synthetic_PS_or_lsof_or_cleanup_error_used_for_qualification=False,actual_complete_raw_evidence_saved=True,actual_Source_D_and_receipt_E_frozen=True,actual_original_caps_verified=True,actual_remaining_owned_groups_absent_after_Root_closure=True,actual_complete_evidence_pins=[fp,tp,gp,gt,rp,rt],actual_native_or_scientific_qualification_created=False)
    # This append is explicitly before its own fullpin. Caller must place it
    # under case H/O/C and reserve its bytes in the same unchanged cap account.
    p=Path(a.output);require(any(p.is_relative_to(Path(HOCDE[k]))for k in('host','output','control')),'case postclose META within original counted HOC')
    raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode();require(total+len(raw)<2*2**30 and r['artifact_bytes']+external+len(raw)<=96*2**30 and r['disk_free_bytes']-len(raw)>=8*2**30,'own META append counted, no new allowance')
    return write_new(p,value)

def account_combined_append(a,b,value):
    rp,r=read_actual(a.controls_postclose_resources);rt,rout=actual_zero(a.controls_postclose_resource_terminal,'ROOT_ACTUAL_N8_ALL_CONTROLS_RESOURCE_TOOL_TERMINAL_RETURN_V1')
    require(rout['actual_postclose_resource_pin']==rp and r['schema']=='ROOT_ACTUAL_N8_ALL_CONTROLS_POSTCLOSE_RESOURCE_V1'and r['actual_controls_Source_binding_pin']==fullpin(a.binding)and r['original_caps']==CAPS,'actual refreshed Root whole-controls resource account')
    roots={Path(v)for ns in b['case_namespaces'].values()for v in ns.values()};files={};dirs={}
    for root in roots:
        view=tree(root);dirs.update(view['directories'])
        for p in view['files']:
            require(p['path']not in files or files[p['path']]==p,'same complete shared Source/receipt pin');files[p['path']]=p
    total=sum(p['size_bytes']for p in files.values());external=sum(p['size_bytes']for p in files.values()if any(Path(p['path']).is_relative_to(Path(ns[k]))for ns in b['case_namespaces'].values()for k in('source','receipts')))
    value['actual_Root_complete_controls_postclose_resource_pin']=rp;value['actual_Root_complete_controls_resource_terminal_pin']=rt
    value['actual_complete_controls_regular_file_pins_before_own_append']=list(files.values());value['actual_complete_controls_directories_before_own_append']=dirs
    output=Path(a.output);require(output.is_relative_to(Path(b['case_namespaces'][CASE_IDS[-1]]['control'])),'manifest/Q within declared counted case12 C, never frozen D/E')
    raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    require(type(r['artifact_bytes'])is int and type(r['disk_free_bytes'])is int and total+len(raw)<2*2**30 and r['artifact_bytes']+external+len(raw)<=96*2**30 and r['disk_free_bytes']-len(raw)>=8*2**30,'all control bytes and own append in original 2GiB/96GiB/8GiB, no allowance')
    return value

def manifest_mode(a):
    bp,b=read_actual(a.binding);require(len(a.case_final or [])==12,'all twelve actual saved cases, never filter missing')
    cases=[]
    for path,case_id in zip(a.case_final,CASE_IDS):
        pin,c=read_actual(path);require(c['schema']=='ROOT_ACTUAL_N8_MONITOR_CONTROL_CASE_POSTCLOSE_V1'and c['case_id']==case_id and c['passed']is True and c['actual_author_Source_contract']==b['actual_author_Source_contract']and c['actual_controls_Source_binding_pin']==bp,'ordered actual twelve case closure facts')
        c['actual_complete_evidence_pins'].append(pin);cases.append(c)
    value=dict(schema='ACTUAL_N8_TWELVE_GENUINE_MONITOR_CONTROLS_MANIFEST_V1',source_only=False,actual_author_Source_contract=b['actual_author_Source_contract'],actual_controls_Source_binding_pin=bp,original_caps=CAPS,cases=cases,all_required_controls_passed=True,blockers=[],actual_monitor_controls_qualification=None,actual_native_or_scientific_qualification_created=False)
    return write_new(Path(a.output),account_combined_append(a,b,value))

def qualification_mode(a):
    mp,m=read_actual(a.manifest);bp,b=read_actual(a.binding);peer_pin,peer=read_actual(a.independent_saved_review)
    root_pin,root_out=actual_zero(a.controls_terminal,'ROOT_ACTUAL_N8_MONITOR_CONTROLS_TOOL_TERMINAL_RETURN_V1')
    require(root_out['actual_controls_manifest_pin']==mp and root_out['all_required_controls_passed']is True,'Root actual complete controls output pin')
    require(m['schema']=='ACTUAL_N8_TWELVE_GENUINE_MONITOR_CONTROLS_MANIFEST_V1'and m['actual_controls_Source_binding_pin']==bp and m['actual_author_Source_contract']==b['actual_author_Source_contract']and m['all_required_controls_passed']is True and m['blockers']==[] and [c['case_id']for c in m['cases']]==list(CASE_IDS),'complete actual controls before qualification')
    require(peer['schema']=='INDEPENDENT_ACTUAL_N8_SAVED_GENUINE_MONITOR_CONTROLS_REVIEW_V1'and peer['status']=='PASS_ACTUAL_SAVED_TWELVE_GENUINE_MONITOR_CONTROLS_NO_NATIVE_OR_SCIENCE'and peer['qualified_actual_controls_manifest_pin']==mp and peer['qualified_actual_controls_Source_binding_pin']==bp and peer['qualified_actual_Root_controls_tool_terminal_return_pin']==root_pin and peer['actual_author_Source_contract']==b['actual_author_Source_contract']and peer['all_checks_passed']is True and peer['blockers']==[],'independent actual saved controls mandatory')
    value=dict(schema='ROOT_ACTUAL_N8_EXACT_OWNER_MONITOR_CONTROLS_QUALIFICATION_V1',status='ACTUAL_TWELVE_GENUINE_MONITOR_CONTROLS_QUALIFIED_NO_NATIVE_OR_SCIENCE',source_only=False,actual_monitor_controls_qualified=True,actual_author_Source_contract=b['actual_author_Source_contract'],original_caps=CAPS,actual_controls_Source_binding_pin=bp,actual_controls_manifest_pin=mp,actual_Root_controls_tool_terminal_return_pin=root_pin,actual_independent_saved_controls_review_pin=peer_pin,actual_stdlib_subprocess_Source_pin=b['actual_stdlib_subprocess_Source_pin'],actual_native_build_or_AB_executed=False,native_transport_executed=False,scientific_qualification_created=False,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    return write_new(Path(a.output),account_combined_append(a,b,value))

def main():
    cli=argparse.ArgumentParser();cli.add_argument('--mode',choices=('case','manifest','qualification'),required=True)
    for name in('binding','output'):cli.add_argument('--'+name,required=True)
    for name in('facts','case-terminal','current-group-closure','current-group-terminal','postclose-resources','postclose-resource-terminal','manifest','controls-terminal','independent-saved-review','controls-postclose-resources','controls-postclose-resource-terminal'):cli.add_argument('--'+name)
    cli.add_argument('--case-final',action='append');a=cli.parse_args()
    p={'case':case_mode,'manifest':manifest_mode,'qualification':qualification_mode}[a.mode](a)
    key={'case':'actual_case_postclose_pin','manifest':'actual_controls_manifest_pin','qualification':'actual_monitor_controls_qualification_pin'}[a.mode]
    print(json.dumps(dict(status='ACTUAL_N8_CONTROLS_POSTCLOSE_SOURCE_META_ONLY',source_only=True,**{key:p},all_required_controls_passed=(a.mode=='manifest'),actual_monitor_controls_qualified=(a.mode=='qualification'),native_or_scientific_qualification_created=False),allow_nan=False),flush=True)

if __name__=='__main__':main()
