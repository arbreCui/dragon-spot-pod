"""Root future request META producer; no native/controller/candidate import.
Read complete actual Source/small receipts/tool/library bytes solely for pins.
Only Root executes this after independent observer Source admission. UNREADY
inputs are not guessed; all actual runtime/observations/science remain unknown.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import time

P=Path(__file__).resolve().parent
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FUTURE=dict(actual_runtime_qualification_sha256=None,actual_observer_native_controls_run=None,actual_native_Source_binary_linkage_qualification_sha256=None,actual_scientific_qualification_sha256=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_transport_executed=False,complete_context_aggregation_qualified=False)
ROLES={'qualified_source_manifest':'MANIFEST.json','host_template':'complete_observation_genuine_host.UNREADY.py','runtime_template':'complete_observation_BUILD5_AB_runtime.UNREADY.py','binder':'bind_complete_observation_SOURCE_only.UNREADY.py','postclose_writer':'Root_observation_postclose_META_writer.UNREADY.py','native_Source_archive':'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','native_Source_index':'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json','observer_module':'OBSERVATION_SOURCE/AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90','context_extractor':'OBSERVATION_SOURCE/extract_actual_complete_context_with_SPH_decisions.UNREADY.py','original_complete_native_walker':'PARENT_SOURCE/Root_bound_complete_native_checker.py','original_material_seed_contract':'ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json','material_blueprint_Source':'GUARD_SOURCE/material_inputs.py','request_preparer':'Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','legacy_context_old_XSM_extractor':'COMPLETE_LEGACY_CONTEXT_HANDOFF_SOURCE/complete_observed_old_post_final_XSM_extractor.UNREADY.py'}

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

def pin(path,deadline,tool_role=None):
    p=Path(path);s=p.lstat();identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];require(p.is_absolute()and all(not q.is_symlink()for q in(p,*p.parents))and stat.S_ISREG(s.st_mode)and source_tool_nlink_allowed(p,s.st_nlink,tool_role),'actual Root full regular pin; only declared canonical OS tools may have real positive hardlinks')
    d=hashlib.sha256()
    with p.open('rb')as f:
        while True:
            require(time.monotonic()<deadline,'actual Root request preparation600 cap');raw=f.read(2**20)
            if not raw:break
            d.update(raw)
    t=p.lstat();require([t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==identity,'full requestSource/META/library/tool EOF unchanged')
    return dict(path=str(p),sha256=d.hexdigest(),size_bytes=s.st_size,identity=identity)

def strict_json(raw):
    def pairs(items):
        d={}
        for k,v in items:require(k not in d,'duplicate actual Root metadata key');d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))

SHARED_INPUT_LIBRARY_LAYOUT = {'schema': 'COMPLETE_AB_SINGLE_COPY_ORIGINAL_SHARED_LIBRARIES_AND_EXACT_PROCEDURE_FILE_LITERALS_V1', 'shared_directory': 'shared_input_libraries', 'state_order': ['A', 'B'], 'seed_destination_order': ['material.x2m', 'AxMatTone.c2m', 'geometry.dat', 'rnr_cc.c2m', 'rnr_interpol.c2m', 'DLIB_ACTUAL', 'DLIB8R1_370'], 'original_procedure_copy_name': 'AxMatTone.c2m.original', 'literal_replacements': [{'original': "FIL: 'DLIB_ACTUAL'", 'derived': "FIL: '../shared_input_libraries/DLIB_ACTUAL'", 'count': 2}, {'original': "FIL: 'DLIB8R1_370'", 'derived': "FIL: '../shared_input_libraries/DLIB8R1_370'", 'count': 1}]}
REQUIRED_N6_FRESH_NAMESPACES = {'host': '/Users/wen/spot/validation/artifacts/axial-material-complete-native-observation-BUILD5-AB-v6-host-20261010', 'output': '/Users/wen/spot/validation/artifacts/axial-material-complete-native-observation-BUILD5-AB-v6-runtime-20261010', 'control': '/Users/wen/spot/validation/artifacts/axial-material-complete-native-observation-BUILD5-AB-v6-control-20261010', 'source': '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_observation_BUILD5_AB_v6_sources', 'receipts': '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_observation_BUILD5_AB_v6_receipts'}

def main():
    ap=argparse.ArgumentParser()
    for name in('independent-review','Source-admission','actual-admission-terminal','fortran','c','cpp','ar','lsof','ps','host','output','control','source','receipts','request-output'):ap.add_argument('--'+name,required=True)
    a=ap.parse_args();require({k:getattr(a,k)for k in REQUIRED_N6_FRESH_NAMESPACES}==REQUIRED_N6_FRESH_NAMESPACES,'new fixed v6 Rootrequest namespaces only');deadline=time.monotonic()+600;require(not sys_optimized(),'unprofiled nonoptimized Root metadata pin preparation')
    seed=strict_json((P/'ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json').read_bytes());review=pin(a.independent_review,deadline);admission=pin(a.Source_admission,deadline);terminal=pin(a.actual_admission_terminal,deadline);author={k:pin(P/v,deadline)for k,v in ROLES.items()};ad=strict_json(Path(a.Source_admission).read_bytes());peer=strict_json(Path(a.independent_review).read_bytes())
    require(ad['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_V1'and ad['status']=='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE'and ad['source_only']is True and ad['actual_author_Source_contract']==author and ad['independent_Source_review_pin']==review,'actual independently admitted complete observer Source required before input hashing')
    require(peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_BINDER_SOURCE_REVIEW_V1'and peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and peer['source_only']is True and peer['actual_author_Source_contract']==author and peer['all_checks_passed']is True and peer['blockers']==[],'real whole Source peer pass exact source')
    for k,v in FUTURE.items():require(ad[k]is v,'actual future still unknown/false')
    require(all(getattr(a,k)==v for k,v in CANONICAL_OS_TOOL_PATHS.items()),'all six original canonical OS tool CLI paths unchanged')
    tools={k:pin(getattr(a,k),deadline,tool_role=k)for k in('fortran','c','cpp','ar','lsof','ps')};libraries={}
    for name,value in seed['libraries'].items():
        actual=pin(value['path'],deadline);require(actual['sha256']==value['generation_sha256'],'actual immutable original library generation hash');libraries[name]=actual
    states={}
    for state in('A','B'):
        rows=[dict(destination=name,input_pin=seed['states'][state][name])for name in('material.x2m','AxMatTone.c2m','geometry.dat','rnr_cc.c2m','rnr_interpol.c2m')]+[dict(destination=name,input_pin=libraries[name])for name in('DLIB_ACTUAL','DLIB8R1_370')]
        states[state]=dict(original_material_deck_pin=seed['states'][state]['material.x2m'],native_stage_inputs=rows)
    original=seed['original129_input_pins'];extra=[];seen={r['path']for r in original}
    for p in[review,admission,terminal,*tools.values(),*libraries.values()]:
        require(p['path']not in seen,'all additional actual Source/tool/library pins disjoint from original129');seen.add(p['path']);extra.append(p)
    request=dict(schema='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_BUILD_BINDING_REQUEST_V1',source_only=True,Root_only_actual_execution=True,scientific_qualification_created=False,original_caps=CAPS,state_order=['A','B'],build_stage_order=['Ganlib','Utilib','Trivac','Dragon','Dragon_link'],SPOT_AXMAT_OBSERVATION='ADMITTED_SOURCE_ONLY',actual_author_Source_contract=author,independent_observation_Source_review_pin=review,independent_observation_Source_admission_pin=admission,actual_Root_observation_Source_admission_tool_return_pin=terminal,original129_input_pins=original,additional_actual_evidence_input_pins=extra,tool_pins=tools,states=states,material_input_layout=SHARED_INPUT_LIBRARY_LAYOUT,namespaces={k:getattr(a,k)for k in('host','output','control','source','receipts')},actual_observation_manifest=None,actual_Root_observed_runtime_terminal=None,actual_runtime_observer_executable=None,**FUTURE)
    output=Path(a.request_output);require(output.is_absolute()and output.parent.is_dir()and not os.path.lexists(output),'fresh Rootrequest file')
    with output.open('x')as f:json.dump(request,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status='ACTUAL_ROOT_OBSERVATION_REQUEST_META_ONLY_NO_BUILD_OR_MATERIAL_RUN',source_only=True,actual_request_pin=pin(output,deadline),native_build_or_API_or_material_execution=False,all_runtime_and_observations_unknown=True,**FUTURE),allow_nan=False),flush=True)

def sys_optimized():
    import sys
    return bool(sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE')or sys.getprofile()is not None)
if __name__=='__main__':main()
