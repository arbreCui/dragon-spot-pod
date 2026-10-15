"""Root-only postclose META writer. No production/controller/candidate imports.
Consumes exact actual CLOSED tool truth and persisted host evidence. Does not
run native/API controls, certify bit equivalence, reference accuracy, AAA/ABA.
"""
import argparse
import hashlib
import importlib.util
import sys
import json
import math
import os
from pathlib import Path
import re
import stat
import time

CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FUTURE=dict(actual_runtime_qualification_sha256=None,actual_observer_native_controls_run=None,actual_native_Source_binary_linkage_qualification_sha256=None,actual_scientific_qualification_sha256=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_transport_executed=False,complete_context_aggregation_qualified=False)

CANONICAL_OS_TOOL_PATHS = {'fortran': '/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15', 'c': '/usr/bin/gcc', 'cpp': '/usr/bin/cpp', 'ar': '/usr/bin/ar', 'lsof': '/usr/sbin/lsof', 'ps': '/bin/ps'}

def source_tool_nlink_allowed(path,nlink,tool_role=None):
    # Default stays the original single-link contract. Only an explicit one of
    # these six original OS tool roles may preserve a positive real hardlink
    # count. Paths, bytes, all seven identity integers and caller order stay real.
    if tool_role is None:return type(nlink)is int and nlink==1
    require(type(tool_role)is str and tool_role in CANONICAL_OS_TOOL_PATHS,'declared original canonical OS tool role only')
    return str(path)==CANONICAL_OS_TOOL_PATHS[tool_role]and type(nlink)is int and nlink>=1

def require(v,m):
    if type(v)is not bool or not v:raise ValueError(m)

def strict_json(raw):
    def pairs(items):
        d={}
        for k,v in items:require(k not in d,'duplicate postclose metadata key');d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))

def fullpin(path,tool_role=None):
    p=Path(path);s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    require(p.is_absolute()and all(not q.is_symlink()for q in(p,*p.parents))and stat.S_ISREG(s.st_mode)and source_tool_nlink_allowed(p,s.st_nlink,tool_role),'full postclose regular noalias; default single-link except explicit canonical OS tools')
    with p.open('rb')as f:d=hashlib.file_digest(f,'sha256').hexdigest()
    t=p.lstat();require([t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==before,'full postclose EOF frozen')
    return dict(path=str(p),sha256=d,size_bytes=s.st_size,identity=before)

def check(p,tool_role=None):
    require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['path'])is str and Path(p['path']).is_absolute()and type(p['sha256'])is str and re.fullmatch('[0-9a-f]{64}',p['sha256'])is not None and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])and source_tool_nlink_allowed(p['path'],p['identity'][3],tool_role)and p['identity'][4]==p['size_bytes'],'strict fullpin types')
    require(fullpin(p['path'],tool_role=tool_role)==p,'full postclose pin differs');return p

def write_new(path,value):
    with Path(path).open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

def tree(path):
    p=Path(path);files=[];dirs={}
    for q in[p,*sorted(p.rglob('*'))]:
        s=q.lstat();require(not stat.S_ISLNK(s.st_mode),'postclose noSource aliases')
        if stat.S_ISDIR(s.st_mode):dirs[str(q)]=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
        else:require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'complete postclose files');files.append(fullpin(q))
    return dict(files=files,directories=dirs)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--actual-root-terminal',required=True);ap.add_argument('--actual-root-terminal-sha256',required=True);ap.add_argument('--host-result',required=True);ap.add_argument('--host-result-sha256',required=True);ap.add_argument('--binding',required=True);ap.add_argument('--binding-sha256',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();terminal_pin=fullpin(a.actual_root_terminal);host_pin=fullpin(a.host_result);binding_pin=fullpin(a.binding)
    require(terminal_pin['sha256']==a.actual_root_terminal_sha256 and host_pin['sha256']==a.host_result_sha256 and binding_pin['sha256']==a.binding_sha256,'Root actual exact terminal/result/binding SHA')
    truth=strict_json(Path(a.actual_root_terminal).read_bytes());t=truth['terminal_tool_return'];require(truth['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_TOOL_TERMINAL_RETURN_V1'and truth['closed']is True and truth['observed_terminal']is True and truth['session_repolled_after_close']is False and type(t['exit_code'])is int and 'session_id'not in t and type(t['chunk_id'])is str and bool(t['chunk_id'])and truth['actual_terminal_chunk']==t['chunk_id'],'exact actual Root CLOSED int terminal, no reopened session')
    b=strict_json(Path(a.binding).read_bytes());h=strict_json(Path(a.host_result).read_bytes());require(b['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_BUILD_BINDING_V1'and b['source_only']is True and b['original_caps']==CAPS and all(type(v)is int for v in b['original_caps'].values()),'actual whole observation Source binding')
    require(h['schema']=='ACTUAL_COMPLETE_NATIVE_OBSERVATION_BUILD_GENUINE_HOST_RESULT_V1'and h['status']=='ACTUAL_COMPLETE_FIVE_STAGE_BUILD_AND_AB_OBSERVATION_EVIDENCE_ONLY_EXTERNAL_ROOT_CLOSURE_REQUIRED'and h['source_only']is False and h['original_caps']==CAPS and h['supervisor_class_or_MRO_modified']is False and h['own_child_RSS_scope_only']is True and h['compiler_descendant_RSS_scope_not_certified']is True,'complete genuinely saved host result only')
    require(t['exit_code']==0,'actual success coverage requires Root typed zero, nonzero is retained failure only')
    stdout=strict_json(t['output']);require(stdout['status']==h['status']and stdout['actual_host_result_pin']==host_pin and stdout['actual_observation_manifest_pin']==h['actual_observation_manifest_pin']and stdout['actual_build_evidence_pin']==h['actual_build_evidence_pin'],'actual Root stdout fullpin matches host result and all raw evidence')
    for k,v in FUTURE.items():require(h[k]is v,'future qualifications must remain unknown/false')
    require(type(b['tool_pins'])is dict and set(b['tool_pins'])==set(CANONICAL_OS_TOOL_PATHS),'complete original six OS tools before postclose full input checking')
    for role,p in b['tool_pins'].items():check(p,tool_role=role)
    tool_roles_by_path={p['path']:role for role,p in b['tool_pins'].items()}
    for p in h['complete_input_pins_before_and_after']:check(p,tool_role=tool_roles_by_path.get(p['path']))
    ds=Path(b['namespaces']['source']);es=Path(b['namespaces']['receipts']);require(tree(ds)==h['complete_Source_D_freeze']and tree(es)==h['complete_receipt_E_freeze'],'fullSource D/E unchanged since host freeze before postclose output')
    check(h['actual_build_evidence_pin']);check(h['actual_observation_manifest_pin']);build=strict_json(Path(h['actual_build_evidence_pin']['path']).read_bytes());m=strict_json(Path(h['actual_observation_manifest_pin']['path']).read_bytes())
    require(build['schema']=='ACTUAL_FROZEN_COMPLETE_NATIVE_SOURCE_OBJECT_ARCHIVE_LINK_EXECUTABLE_EVIDENCE_V1'and build['whole5stage_executed']is True and build['all_sources_objects_archives_checked_after_actual_link']is True and build['no_old_binary_object_archive_used']is True and build['stage_order']==['Ganlib','Utilib','Trivac','Dragon','Dragon_link'],'new full compiledSource-to-object-archive-link evidence')
    check(build['new_actual_executable_pin'])
    for row in build['frozen_all_compiled_and_include_Source']:check(row['input_pin'])
    for stage in build['all_four_complete_library_build_stages']:
        require(stage['component']in('Ganlib','Utilib','Trivac','Dragon')and 0<=stage['elapsed_seconds']<600,'all real group wall cap');check(stage['new_archive_pin']);check(stage['original_recipe_library_copy_pin'])
        for module in stage['original_recipe_module_copy_pins']:check(module['original_generated_module_pin']);check(module['original_recipe_module_copy_pin'])
        for obj in stage['all_object_inputs_in_original_archive_order']:
            check(obj['original_source_pin']);check(obj['new_object_pin'])
            if obj['retained_complete_preprocessor_Source_pin']is not None:check(obj['retained_complete_preprocessor_Source_pin'])
        for command in stage['all_commands']+[stage['actual_archive_command']]:
            check(command['actual_watchdog_pin']);check(command['actual_merged_stdout_stderr_pin']);w=strict_json(Path(command['actual_watchdog_pin']['path']).read_bytes());require(w==command['watchdog']and type(w['returncode'])is int and w['returncode']==0 and w['command']==command['command']and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True,'every actual compile/archive closed watch and exact argv')
    link=build['actual_final_link_command'];check(link['actual_watchdog_pin']);check(link['actual_merged_stdout_stderr_pin']);require(strict_json(Path(link['actual_watchdog_pin']['path']).read_bytes())==link['watchdog']and link['watchdog']['returncode']==0,'actual final new link watch')
    for p in build['all_actual_link_input_pins']:check(p)
    require(m['schema']=='ACTUAL_COMPLETE_AXOBSCTXv2_AB_OBSERVATION_MANIFEST_V1'and m['source_only']is False and m['state_order']==['A','B']and m['all_A_handles_closed_before_B']is True and m['actual_Source_binary_link_evidence_pin']==h['actual_build_evidence_pin']and m['actual_observer_executable_pin']==build['new_actual_executable_pin'],'complete actual observer manifest matches actual new program')
    fullstates={}
    for state in('A','B'):
        row=m['states'][state];require(row['state']==state and row['all_actual_events_and_snapshots_saved']is True and row['actual_material_child_closed_before_manifest']is True and row['all_producer_file_handles_closed_before_next_state']is True and row['new_final_micro_from_actual_TONDRV_observer']is True,'whole actual state closure and newly observed finalmicro')
        require([e['event']for e in row['actual_all_event_headers_in_original_execution_order']]==list(range(1,len(row['actual_all_event_headers_in_original_execution_order'])+1)),'whole consecutive event order')
        for p in row['complete_context_pins']+row['actual_material_product_pins']+row['actual_material_seed_copy_pins']:check(p)
        for p in row['complete_state_snapshot_inputs']:
            require(set(p)=={'event','role','root_prefix','logical_prefix','input_pin'}and p['root_prefix']==[]and p['logical_prefix']==([]if p['role']=='final-complete-micro'else['MACROLIB']),'explicit native root[] and original pool logical prefix');check(p['input_pin'])
        require(row['legacy_context_source_snapshot_request_rows']==[dict(event=p['event'],role=p['role'],root_prefix=p['logical_prefix'],input_pin=p['input_pin'])for p in row['complete_state_snapshot_inputs']]and row['legacy_context_root_prefix_semantics']=='output_pool_logical_path_prefix_only_not_native_directory_lookup'and row['actual_native_snapshot_root_prefix']==[],'explicit legacy logical-prefix-only handoff; no nonexistent MACROLIB child')
        stage=row['actual_genuine_material_stage'];check(stage['actual_watchdog_pin']);check(stage['actual_merged_stdout_stderr_pin']);w=strict_json(Path(stage['actual_watchdog_pin']['path']).read_bytes());require(w==stage['watchdog']and type(w['returncode'])is int and w['returncode']==0 and w['command']==[build['new_actual_executable_pin']['path']]and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True,'actual state material newexe guarded closed zero')
        fullstates[state]=row
    require(type(h['whole_seconds'])in(int,float)and not isinstance(h['whole_seconds'],bool)and math.isfinite(h['whole_seconds'])and 0<=h['whole_seconds']<1800,'actual whole wall cap')
    namespace_keys=('host','output','control','source','receipts');roots=[Path(b['namespaces'][k])for k in namespace_keys]
    resource_path=Path('/Users/wen/spot/validation/axial_material/moment_order_complete_history_resource_trie_20261010.py');require(fullpin(resource_path)['sha256']=='ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022','original admitted metadata-only resource Source')
    spec=importlib.util.spec_from_file_location('axmat_observation_postclose_original_resource_META',resource_path);resource=importlib.util.module_from_spec(spec);sys.modules[spec.name]=resource;spec.loader.exec_module(resource)
    art=Path('/Users/wen/spot/validation/artifacts');history=resource.history_roots([str(p)for p in roots[:3]],art);resource_checker=resource.DynamicHistoryResources(art,history,8*2**30,96*2**30);resource_before=resource_checker.check();outside=sum(q.stat().st_size for root in roots[3:]for q in root.rglob('*')if q.is_file());require(resource_before['artifact_bytes']+outside<96*2**30,'Root whole dynamic history plus frozen D/E96GiB')
    out=Path(a.output);require(out.is_absolute()and out.parent.is_dir()and not os.path.lexists(out)and out.is_relative_to(es),'fresh postclose META within E after the genuine child closure')
    # Full EOF views cover every regular file, not only known Source/build/event
    # pins. E is deliberately captured before appending this manifest; a JSON
    # manifest cannot contain its own complete hash/identity recursively.
    namespace_views={key:tree(Path(b['namespaces'][key]))for key in namespace_keys}
    require(namespace_views['source']==h['complete_Source_D_freeze']and namespace_views['receipts']==h['complete_receipt_E_freeze'],'complete D remains frozen; complete E captured before this single append')
    total=sum(p['size_bytes']for view in namespace_views.values()for p in view['files']);outside=sum(p['size_bytes']for key in('source','receipts')for p in namespace_views[key]['files'])
    require(total<2*2**30 and resource_before['artifact_bytes']+outside<96*2**30,'all complete namespace fullpins counted before append')

    result=dict(m);result.update(schema='ROOT_ACTUAL_COMPLETE_AXOBSCTXv2_AB_OBSERVATION_POSTCLOSE_MANIFEST_V1',Root_observed_tool_terminal=terminal_pin,Root_actual_host_result_pin=host_pin,Root_actual_binding_pin=binding_pin,Root_checked_full_Input_Source_D_E_freeze=True,Root_checked_all_whole_event_snapshot_and_new_executable_fullpins=True,actual_raw_observation_manifest_pin=h['actual_observation_manifest_pin'],Root_postclose_joint_HOCDE_bytes_before_receipt=total,Root_postclose_original_dynamic_history_resource_before=resource_before,Root_postclose_external_Source_D_receipt_E_bytes=outside,Root_complete_postclose_HOCDE_namespace_views=namespace_views,Root_complete_postclose_HOCDE_namespace_view_contract=dict(schema='ROOT_COMPLETE_HOCDE_POSTCLOSE_FULL_EOF_VIEWS_BEFORE_OWN_E_APPEND_V1',namespace_order=list(namespace_keys),all_directories_and_regular_files_saved=True,all_regular_file_full_EOF_sha256_size_and_7_identity_saved=True,E_view_before_this_manifest_append=True,this_manifest_not_self_pinned_in_its_content=True,this_manifest_actual_fullpin_is_in_actual_Root_stdout=True,this_manifest_append_counts_in_joint_history_free_caps=True,D_namespace_never_appended=True),Root_postclose_coverage_contract=dict(schema='ROOT_ACTUAL_COMPLETE_AXOBSCTXv2_OBSERVATION_COVERAGE_V1',state_order=['A','B'],all_complete_observer_events_and_snapshots_saved=True,native_snapshot_API_bit_equivalence_qualified=False,independent_observation_Source_admission_pin=b['independent_observation_Source_admission_pin'],new_native_walker_controls_actual_run=None,new_complete_aggregation_controls_actual_run=None,**FUTURE))
    write_new(out,result)
    # Re-read all five complete views after the append. H/O/C/D must be byte
    # and identity stable. E may gain exactly this new receipt and only its
    # containing directory metadata may change. No D Source is appended.
    after_views={key:tree(Path(b['namespaces'][key]))for key in namespace_keys};out_pin=fullpin(out)
    require(all(after_views[key]==namespace_views[key]for key in namespace_keys[:-1]),'postclose H/O/C/D full views unchanged across own E append')
    require(sorted(after_views['receipts']['files'],key=lambda p:p['path'])==sorted([*namespace_views['receipts']['files'],out_pin],key=lambda p:p['path'])and set(after_views['receipts']['directories'])==set(namespace_views['receipts']['directories']),'E gains exactly own manifest with complete full EOF pin and no extra directory')
    for directory,identity in namespace_views['receipts']['directories'].items():
        current=after_views['receipts']['directories'][directory]
        require((current[:3]==identity[:3])if directory==str(out.parent)else current==identity,'only E own append directory nlink/size/timestamps may change; dev/inode/mode stay identical')
    resource_after=resource_checker.check();outside_after=sum(p['size_bytes']for key in('source','receipts')for p in after_views[key]['files']);joint_after=sum(p['size_bytes']for view in after_views.values()for p in view['files'])
    require(resource_after['artifact_bytes']+outside_after<96*2**30,'postclose receipt itself counts in history96GiB/free8GiB');require(joint_after<2*2**30,'postclose receipt itself counts in joint archive')
    print(json.dumps(dict(status='ACTUAL_COMPLETE_OBSERVATION_POSTCLOSE_META_ONLY_NO_NATIVE_OR_SCIENCE_QUALIFICATION',actual_observation_manifest_pin=out_pin,Root_postclose_complete_namespace_views_saved_before_own_E_append=True,Root_postclose_joint_HOCDE_bytes_including_own_manifest=joint_after,Root_postclose_original_dynamic_history_resource_after=resource_after,Root_postclose_external_Source_D_receipt_E_bytes_including_own_manifest=outside_after,raw_observation_manifest_pin=h['actual_observation_manifest_pin'],independent_observation_Source_admission_pin=b['independent_observation_Source_admission_pin'],complete_state_snapshot_inputs=m['complete_state_snapshot_inputs'],complete_context_inputs=m['complete_context_inputs'],**FUTURE),allow_nan=False),flush=True)
if __name__=='__main__':main()
