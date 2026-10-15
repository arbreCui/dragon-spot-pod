"""Root-only stdlib SOURCE binder. No candidate/guard/API import or execution.

Creates a fresh TMP complete Source copy. Root separately installs it, then
runs the genuine host after its actual V22 full-build tool has CLOSED.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile

P = Path(__file__).resolve().parent
CAPS = dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,
            history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART = Path('/Users/wen/spot/validation/artifacts')
UNKNOWN = None


def require(value, message):
    if type(value) is not bool or not value:
        raise ValueError(message)


def strict_json(raw):
    def pairs(items):
        result={}
        for key,value in items:
            require(key not in result,'duplicate Source metadata key')
            result[key]=value
        return result
    def reject(value):
        raise ValueError('nonfinite Source metadata '+value)
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=reject)


def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pin(path):
    path=Path(path)
    before=path.lstat()
    require(path.is_absolute()and stat.S_ISREG(before.st_mode)and before.st_nlink==1,'real unaliased Source/META file')
    with path.open('rb')as stream:
        require(identity(os.fstat(stream.fileno()))==identity(before),'Source open7ID')
        digest=hashlib.file_digest(stream,'sha256').hexdigest()
        require(identity(os.fstat(stream.fileno()))==identity(before),'Source fullEOF7ID')
    require(identity(path.lstat())==identity(before),'Source path7ID')
    return dict(path=str(path),sha256=digest,size_bytes=before.st_size,identity=identity(before))


def typed_pin(expected):
    require(type(expected)is dict and set(expected)=={'path','sha256','size_bytes','identity'},'exact Source/META full pin schema')
    require(type(expected['path'])is str and Path(expected['path']).is_absolute()
            and type(expected['sha256'])is str and re.fullmatch('[0-9a-f]{64}',expected['sha256'])is not None,'exact full path/SHA')
    require(type(expected['size_bytes'])is int and expected['size_bytes']>=0
            and type(expected['identity'])is list and len(expected['identity'])==7
            and all(type(v)is int and v>=0 for v in expected['identity'])
            and expected['identity'][3]==1 and expected['identity'][4]==expected['size_bytes'],'exact typedsize7ID')
    require(pin(expected['path'])==expected,'actual Root Source/META fullEOF/SHA7ID differs')


def actual_terminal(expected, zero, expected_schema):
    typed_pin(expected)
    value=strict_json(Path(expected['path']).read_bytes())
    require(type(value)is dict and value['schema']==expected_schema
            and value['closed']is True and value['observed_terminal']is True
            and value['session_repolled_after_close']is False,
            'actual Root observed CLOSED family required; PREP cannot stand for BUILD')
    terminal=value['terminal_tool_return']
    require(type(terminal)is dict and type(terminal['exit_code'])is int
            and 'session_id'not in terminal and type(terminal['chunk_id'])is str and bool(terminal['chunk_id'])
            and type(value['actual_terminal_chunk'])is str
            and value['actual_terminal_chunk']==terminal['chunk_id'],
            'genuine Root typed CLOSED tool truth and exact observed terminal chunk required')
    require(not zero or terminal['exit_code']==0,'Source admission actual typedzero required')
    return value


def source_scope_contract(request, expected_sources, source_truth):
    for expected in expected_sources.values():typed_pin(expected)
    peer=strict_json(Path(request['independent_host_binder_Source_review_pin']['path']).read_bytes())
    require(type(peer)is dict and peer['schema']=='INDEPENDENT_COMPLETE_FINAL_AGGREGATION_ENGINE_HOST_BINDER_SOURCE_REVIEW_V1'
            and peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'
            and peer['source_only']is True and peer['all_checks_passed']is True
            and type(peer['blockers'])is list and peer['blockers']==[],
            'actual independent full native host/binder Source review scope required')
    checks=peer['checks']
    require(type(checks)is list and type(peer['check_count'])is int and peer['check_count']==len(checks)>0
            and all(type(row)is dict and set(row)=={'check','passed'}
                    and type(row['check'])is str and bool(row['check'])and row['passed']is True for row in checks)
            and len({row['check']for row in checks})==len(checks),
            'all independent Source checks retained, exact count and typed PASS')
    admission=strict_json(Path(request['source_admission_pin']['path']).read_bytes())
    require(type(admission)is dict and admission['schema']=='ROOT_ACTUAL_COMPLETE_FINAL_AGGREGATION_ENGINE_HOST_BINDER_SOURCE_ADMISSION_V1'
            and admission['status']=='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE'
            and admission['source_only']is True and admission['scientific_qualification_created']is False
            and admission['new_aggregation_qualification_sha256']is None
            and admission['actual_scientific_qualification_sha256']is None,
            'actual Root Source admission must retain software-only scope and unknown qualifications')
    for key,expected in expected_sources.items():
        typed_pin(peer[key]);typed_pin(admission[key])
        require(peer[key]==expected and admission[key]==expected,
                'peer/admission fullpin must match actual complete author manifest and each Source body: '+key)
    typed_pin(admission['independent_Source_review_pin'])
    require(admission['independent_Source_review_pin']==request['independent_host_binder_Source_review_pin'],
            'Source admission must bind this same independently reviewed Source report')
    output=strict_json(source_truth['terminal_tool_return']['output'])
    require(type(output)is dict and output['source_only']is True
            and output['status']=='ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE',
            'genuine actual Source admission output scope required')
    typed_pin(output['source_admission_pin'])
    require(output['source_admission_pin']==request['source_admission_pin'],
            'actual Source admission tool output fullpin must equal actual admission record')
    return dict(schema='ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_SCOPE_COUPLING_V1',source_only=True,
                all_five_actual_author_Source_fullpins_coupled=True,independent_full_Source_checks_count=len(checks),
                Source_admission_actual_tool_output_fullpin_coupled=True,PREP_is_not_BUILD=True,
                actual_Source_admission=request['source_admission_pin'],
                actual_independent_Source_review=request['independent_host_binder_Source_review_pin'],
                actual_author_Source_contract=expected_sources)


def bind_globals(source, changes):
    tree=ast.parse(source)
    lines=source.decode().splitlines(keepends=True)
    found={}
    for n in tree.body:
        if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id in changes:
            name=n.targets[0].id
            require(name not in found,'duplicate binding global')
            found[name]=n
    require(set(found)==set(changes),'all exact Source binding globals required')
    inverse=[]
    for name,n in sorted(found.items(),key=lambda row:row[1].lineno,reverse=True):
        old=lines[n.lineno-1:n.end_lineno]
        new=[name+' = '+repr(changes[name])+'\n']
        inverse.append(dict(name=name,one_based_line=n.lineno,old_full_lines=old,new_full_lines=new))
        lines[n.lineno-1:n.end_lineno]=new
    bound=''.join(lines).encode()
    restored=bound.decode().splitlines(keepends=True)
    for item in sorted(inverse,key=lambda x:x['one_based_line'],reverse=True):
        at=item['one_based_line']-1
        require(restored[at:at+1]==item['new_full_lines'],'actual full bound Source inverse hunk differs')
        restored[at:at+1]=item['old_full_lines']
    require(''.join(restored).encode()==source,'all original Source bytes must restore')
    ast.parse(bound)
    return bound,inverse


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-manifest-sha256',required=True)
    parser.add_argument('--request',required=True)
    parser.add_argument('--request-sha256',required=True)
    parser.add_argument('--output-source-dir',required=True)
    args=parser.parse_args()
    mp=pin(P/'MANIFEST.json')
    require(mp['sha256']==args.source_manifest_sha256,'complete independent Source manifest')
    manifest=strict_json((P/'MANIFEST.json').read_bytes())
    members=manifest['members']
    require(type(members)is list and type(manifest['member_count'])is int and len(members)==manifest['member_count'],'complete author Source inventory')
    files=[]
    for f in sorted(P.rglob('*')):
        require(not f.is_symlink(),'complete Source copy cannot alias')
        if f.is_file()and f!=P/'MANIFEST.json':files.append(str(f))
    require(files==[m['path']for m in members],'no omitted/extra Source member')
    for m in members:typed_pin({k:m[k]for k in('path','sha256','size_bytes','identity')})
    rp=pin(args.request)
    require(rp['sha256']==args.request_sha256,'actual Root request full pin')
    request=strict_json(Path(args.request).read_bytes())
    require(request['schema']=='ROOT_ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_BINDING_REQUEST_V1'and request['source_only']is True,'new Source family only')
    for k in('source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin','prior_actual_V22_build_tool_return_pin','actual_native_terminal_pin','actual_native_saved_coverage_contract_pin'):
        typed_pin(request[k])
    source_truth=actual_terminal(request['actual_Root_Source_admission_tool_return_pin'],True,'ROOT_ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1')
    prior=actual_terminal(request['prior_actual_V22_build_tool_return_pin'],False,'ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1')
    # This prescribed Root observation wrapper keeps the original underlying
    # receipt/output intact. Honest native nonzero is allowed if full saved pools
    # independently exist; Source/binary linkage is not a made-up data gate.
    native=actual_terminal(request['actual_native_terminal_pin'],False,'ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVED_TERMINAL_FOR_AGGREGATION_V1')
    coverage=strict_json(Path(request['actual_native_saved_coverage_contract_pin']['path']).read_bytes())
    require(coverage['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_SAVED_POOL_COVERAGE_FOR_AGGREGATION_V1'and coverage['all_complete_paired_pools_saved']is True and coverage['actual_native_terminal_pin']==request['actual_native_terminal_pin']and coverage['state_order']==['A','B']and coverage['same_actual_native_report_and_independent_review_bound']is True and coverage['scientific_qualification_created']is False,'actual independent complete saved-pool coverage, not raw-reader qualification')
    for key in('actual_native_report_pin','actual_native_independent_review_pin'):typed_pin(coverage[key])
    expected=dict(qualified_source_manifest=mp,host_template=pin(P/'complete_final_MICROLIB_MACROLIB_aggregation_genuine_host.UNREADY.py'),engine_template=pin(P/'complete_final_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'),adapter=pin(P/'saved_native_data_access_adapter.UNREADY.py'),binder=pin(Path(__file__).resolve()))
    coupling=source_scope_contract(request,expected,source_truth)
    namespaces=request['namespaces']
    require(type(namespaces)is dict and set(namespaces)=={'host','output','control','source','receipts'}and all(type(v)is str and Path(v).is_absolute()and '..'not in Path(v).parts for v in namespaces.values()),'complete genuine namespaces')
    paths={k:Path(v)for k,v in namespaces.items()}
    require(all(paths[k].is_relative_to(ART)and paths[k]!=ART for k in('host','output','control'))and all(paths[k].is_relative_to(BASE)and paths[k]!=BASE for k in('source','receipts')),'original history and separate Source/receipts')
    require(len(set(paths.values()))==5 and not any(a.is_relative_to(b)for a in paths.values()for b in paths.values()if a!=b),'five disjoint roots')
    require(all(not os.path.lexists(paths[k])for k in('host','output','control','source')),'fresh H/O/C/D zero retry')
    dest=Path(args.output_source_dir)
    require(dest.is_absolute()and dest.is_relative_to(Path('/private/tmp'))and not os.path.lexists(dest)and not dest.is_relative_to(P)and not P.is_relative_to(dest),'fresh TMP only')
    original=request['original129_input_pins']
    additional=request['additional_actual_evidence_input_pins']
    require(type(original)is list and len(original)==129 and type(additional)is list and len(additional)>0,'all original129 plus actual native/context/meta pins')
    complete=original+additional
    # Shape-only: Source binder MUST NOT hash or read numeric/native/material
    # inputs. Genuine host/child later protect all complete inputs at full EOF.
    for p in complete:
        require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['path'])is str and Path(p['path']).is_absolute()and type(p['sha256'])is str and re.fullmatch('[0-9a-f]{64}',p['sha256'])is not None and type(p['size_bytes'])is int and p['size_bytes']>=0 and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int and x>=0 for x in p['identity'])and p['identity'][3]==1 and p['identity'][4]==p['size_bytes'],'all original exact typed input pin shapes')
    require(len({p['path']for p in complete})==len(complete),'all inputs unique, no replacement of129')
    states=request['states']
    require(type(states)is dict and set(states)=={'A','B'},'complete A/B states')
    for state in('A','B'):
        require(states[state]==coverage['states'][state]and type(states[state])is dict and set(states[state])=={'sqlite_pin','native_pool_pin'},'full actual paired native state pins')
        for p in states[state].values():
            require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['path'])is str and Path(p['path']).is_absolute()and type(p['sha256'])is str and re.fullmatch('[0-9a-f]{64}',p['sha256'])is not None and type(p['size_bytes'])is int and p['size_bytes']>=0 and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int and x>=0 for x in p['identity'])and p['identity'][3]==1 and p['identity'][4]==p['size_bytes'],'strict shape paired native pins without Source-only payload read')
        require(all(states[state][k]in complete for k in('sqlite_pin','native_pool_pin')),'both paired native files protected by genuine fullinputs')
    require(request['new_aggregation_qualification_sha256']is None and request['actual_scientific_qualification_sha256']is None and request['new_complete_aggregation_controls_actual_run']is None,'future qualification unknown, no invented arithmetic/walker controls')
    # This unchanged sealed adapter has a real observed full7ID already. No
    # staging copy or guessed future inode is needed. Host pins its Source too.
    adapter_pin=expected['adapter']
    binding=dict(schema='ROOT_ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_BINDING_V1',source_only=True,Root_only_actual_execution=True,scientific_qualification_created=False,original_caps=CAPS,state_order=['A','B'],states=states,Source_route=dict(schema='ROOT_BOUND_FINAL_TONE_LIBMIX_SOURCE_ROUTE_V1',ITSTMP=0,historical_call_proved=False),namespaces=namespaces,joint_archive_roots=[namespaces[k]for k in('host','output','control','source','receipts')],original129_input_pins=original,complete_input_pins=complete,source_admission_pin=request['source_admission_pin'],actual_Root_Source_admission_tool_return_pin=request['actual_Root_Source_admission_tool_return_pin'],independent_host_binder_Source_review_pin=request['independent_host_binder_Source_review_pin'],prior_actual_V22_build_tool_return_pin=request['prior_actual_V22_build_tool_return_pin'],actual_author_Source_contract=expected,actual_Source_scope_coupling=coupling,saved_native_adapter_pin=adapter_pin,actual_native_terminal_pin=request['actual_native_terminal_pin'],actual_native_saved_coverage_contract_pin=request['actual_native_saved_coverage_contract_pin'],new_complete_aggregation_controls_actual_run=None,new_aggregation_qualification_sha256=None,actual_scientific_qualification_sha256=None,original_native_build_binary_Source_linkage_qualified=False,historical_original_context_saved=False)
    binding_raw=(json.dumps(binding,indent=2,allow_nan=False)+'\n').encode()
    binding_sha=hashlib.sha256(binding_raw).hexdigest()
    # Bind only the actual deterministic binding SHA. The genuine host and
    # child observe its installed full7ID and protect it before/after; the Source
    # binder never invents a copy's future inode/time and needs no second bind.
    engine=(P/'complete_final_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py').read_bytes()
    engine_bound,engine_inverse=bind_globals(engine,dict(SOURCE_STATUS='READY_ROOT_BOUND_SOURCE_ONLY',SOURCE_BINDING_SHA256=binding_sha,BOUND_ADAPTER_PIN=adapter_pin))
    engine_sha=hashlib.sha256(engine_bound).hexdigest()
    host=(P/'complete_final_MICROLIB_MACROLIB_aggregation_genuine_host.UNREADY.py').read_bytes()
    bound_host,host_inverse=bind_globals(host,dict(SOURCE_STATUS='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED',SOURCE_ARCHIVE=namespaces['source'],RECEIPTS=namespaces['receipts'],HOST=namespaces['host'],OUT=namespaces['output'],CONTROL=namespaces['control'],TARGET=str(paths['source']/'Root_bound_complete_final_aggregation_engine.py'),TARGET_SHA=engine_sha,BINDING=str(paths['source']/'Root_actual_aggregation_SOURCE_binding.json'),BINDING_SHA=binding_sha,SOURCE_ADMISSION_SHA=request['source_admission_pin']['sha256']))
    shutil.copytree(P,dest)
    outputs={'Root_actual_aggregation_SOURCE_binding.json':binding_raw,'Root_bound_complete_final_aggregation_engine.py':engine_bound,'Root_bound_complete_final_aggregation_genuine_host.py':bound_host,'Root_actual_complete_aggregation_Source_binding_inverse.json':(json.dumps(dict(schema='ROOT_ACTUAL_COMPLETE_AGGREGATION_SOURCE_GLOBALS_FULL_INVERSE_V1',source_only=True,engine_full_inverse=engine_inverse,host_full_inverse=host_inverse,engine_original_bytes_restored=True,host_original_bytes_restored=True,installed_binding7ID_observed_only_at_actual_runtime=True),indent=2)+'\n').encode()}
    for name,raw in outputs.items():
        with(dest/name).open('xb')as stream:stream.write(raw)
    record=dict(schema='ROOT_ACTUAL_COMPLETE_AGGREGATION_SOURCE_BINDING_RECORD_V1',source_only=True,request=rp,author_manifest=mp,actual_Source_scope_coupling=coupling,actual_native_terminal=native,prior_actual_build_terminal=prior,complete_original129_preserved=True,complete_inputs_count=len(complete),bound_outputs={name:pin(dest/name)for name in outputs},actual_source_installed=None,actual_genuine_host_run=None,new_aggregation_qualification_sha256=None,actual_scientific_qualification_sha256=None,no_candidate_helper_API_guard_compile_execution=True,no_numeric_material_payload_read=True)
    with(dest/'Root_actual_complete_aggregation_Source_binding_record.json').open('x')as stream:json.dump(record,stream,indent=2,allow_nan=False);stream.write('\n')
    require(pin(P/'MANIFEST.json')==mp and pin(args.request)==rp,'complete Source/request unchanged')
    for m in members:typed_pin({k:m[k]for k in('path','sha256','size_bytes','identity')})
    print(json.dumps(dict(source_only=True,status='ACTUAL_AGGREGATION_SOURCE_DERIVED_UNREADY_NOT_RUN',binding_record=pin(dest/'Root_actual_complete_aggregation_Source_binding_record.json'),bound_outputs=record['bound_outputs'],complete_inputs_count=len(complete),actual_engine_activation=None),indent=2,allow_nan=False),flush=True)


if __name__=='__main__':main()
