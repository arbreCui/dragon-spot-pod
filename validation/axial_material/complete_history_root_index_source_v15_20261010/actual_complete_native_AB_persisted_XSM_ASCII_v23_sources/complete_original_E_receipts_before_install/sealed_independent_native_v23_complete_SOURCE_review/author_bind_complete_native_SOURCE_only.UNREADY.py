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
    require(type(peer)is dict and peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1'
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
    require(type(admission)is dict and admission['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_HOST_BINDER_SOURCE_ADMISSION_V1'
            and admission['status']=='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE'
            and admission['source_only']is True and admission['scientific_qualification_created']is False
            and admission['actual_native_byte_qualification_sha256']is None
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
            and output['status']=='ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE',
            'genuine actual Source admission output scope required')
    typed_pin(output['source_admission_pin'])
    require(output['source_admission_pin']==request['source_admission_pin'],
            'actual Source admission tool output fullpin must equal actual admission record')
    return dict(schema='ACTUAL_COMPLETE_NATIVE_SOURCE_SCOPE_COUPLING_V1',source_only=True,
                all_four_actual_author_Source_fullpins_coupled=True,independent_full_Source_checks_count=len(checks),
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
    require(mp['sha256']==args.source_manifest_sha256,'exact independently reviewed complete Source manifest')
    manifest=strict_json((P/'MANIFEST.json').read_bytes())
    members=manifest['members']
    require(type(members)is list and type(manifest['member_count'])is int and len(members)==manifest['member_count'],'complete Source inventory')
    files=[]
    for f in sorted(P.rglob('*')):
        require(not f.is_symlink(),'complete Source copy forbids aliases')
        if f.is_file()and f!=P/'MANIFEST.json':files.append(str(f))
    require(files==[m['path']for m in members],'no omitted or added Source file')
    for m in members:typed_pin({key:m[key]for key in ('path','sha256','size_bytes','identity')})
    request_pin=pin(args.request)
    require(request_pin['sha256']==args.request_sha256,'actual Root Source request full SHA')
    request=strict_json(Path(args.request).read_bytes())
    require(request['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_BINDING_REQUEST_V1'
            and request['source_only']is True,'actual Source-only Root request')
    for key in ('source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin','prior_actual_V22_build_tool_return_pin'):
        typed_pin(request[key])
    source_truth=actual_terminal(request['actual_Root_Source_admission_tool_return_pin'],True,'ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1')
    prior_truth=actual_terminal(request['prior_actual_V22_build_tool_return_pin'],False,'ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1')
    expected_sources=dict(qualified_source_manifest=mp,
                          host_template=pin(P/'complete_native_XSM_ASCII_genuine_host.UNREADY.py'),
                          checker_template=pin(P/'complete_native_XSM_ASCII_checker_v4.UNREADY.py'),
                          binder=pin(Path(__file__).resolve()))
    scope_coupling=source_scope_contract(request,expected_sources,source_truth)
    namespaces=request['namespaces']
    require(type(namespaces)is dict and set(namespaces)=={'host','output','control','source','receipts'}
            and all(type(v)is str and Path(v).is_absolute()and '..'not in Path(v).parts for v in namespaces.values()),'complete genuine native namespace request')
    paths={key:Path(value)for key,value in namespaces.items()}
    require(all(paths[key].is_relative_to(ART)and paths[key]!=ART for key in ('host','output','control'))
            and all(paths[key].is_relative_to(BASE)and paths[key]!=BASE for key in ('source','receipts')),'original ART history and separately counted B Source/receipt roots')
    require(len(set(paths.values()))==5 and not any(a.is_relative_to(b)for a in paths.values()for b in paths.values()if a!=b),'all five roots distinct and nonoverlapping')
    require(all(not os.path.lexists(paths[key])for key in ('host','output','control','source')),'future actual H/O/C/D fresh; no retry')
    destination=Path(args.output_source_dir)
    require(destination.is_absolute()and destination.is_relative_to(Path('/private/tmp'))and not os.path.lexists(destination)
            and not destination.is_relative_to(P)and not P.is_relative_to(destination),'fresh TMP Source only destination; no project or ART writes')
    binding=strict_json((P/'ORIGINAL_FIXED_HOST_BINDER_SOURCE/PARENT_NATIVE_SOURCE/ROOT_BINDING_BLUEPRINT.UNREADY.json').read_bytes())
    require(len(binding['complete_input_pins'])==129 and len({p['path']for p in binding['complete_input_pins']})==129,'all original129 complete pins retained unchanged')
    # These original Source/material pins come from the real saved parent META.
    # Binder never reads them; the genuine host and native checker hash all129.
    binding.update(source_only=True,scientific_qualification_created=False,
                   actual_author_Source_contract=expected_sources,actual_Source_scope_coupling=scope_coupling,
                   namespaces=namespaces,joint_archive_roots=[namespaces[k]for k in ('host','output','control','source','receipts')],
                   source_admission_pin=request['source_admission_pin'],
                   actual_Root_Source_admission_tool_return_pin=request['actual_Root_Source_admission_tool_return_pin'],
                   independent_host_binder_Source_review_pin=request['independent_host_binder_Source_review_pin'],
                   prior_actual_V22_build_tool_return_pin=request['prior_actual_V22_build_tool_return_pin'],
                   new_native_walker_controls_actual_run=None,actual_native_byte_qualification_sha256=None,
                   actual_scientific_qualification_sha256=None,original_native_build_binary_Source_linkage_qualified=False)
    require(binding['original_caps']==CAPS and all(type(v)is int for v in binding['original_caps'].values()),'all original fixed caps')
    binding_bytes=(json.dumps(binding,indent=2,allow_nan=False)+'\n').encode()
    binding_sha=hashlib.sha256(binding_bytes).hexdigest()
    checker=(P/'complete_native_XSM_ASCII_checker_v4.UNREADY.py').read_bytes()
    bound_checker,checker_inverse=bind_globals(checker,dict(SOURCE_STATUS='ROOT_BOUND_SOURCE_ONLY_NOT_QUALIFIED',ROOT_BOUND_BINDING_SHA256=binding_sha))
    checker_sha=hashlib.sha256(bound_checker).hexdigest()
    host=(P/'complete_native_XSM_ASCII_genuine_host.UNREADY.py').read_bytes()
    host_changes=dict(SOURCE_STATUS='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED',SOURCE_ARCHIVE=namespaces['source'],RECEIPTS=namespaces['receipts'],HOST=namespaces['host'],OUT=namespaces['output'],CONTROL=namespaces['control'],TARGET=str(paths['source']/'Root_bound_complete_native_checker.py'),TARGET_SHA=checker_sha,BINDING=str(paths['source']/'Root_actual_native_SOURCE_binding.json'),BINDING_SHA=binding_sha,SOURCE_ADMISSION_SHA=request['source_admission_pin']['sha256'])
    bound_host,host_inverse=bind_globals(host,host_changes)
    shutil.copytree(P,destination)
    outputs={
        'Root_actual_native_SOURCE_binding.json':binding_bytes,
        'Root_bound_complete_native_checker.py':bound_checker,
        'Root_bound_complete_native_genuine_host.py':bound_host,
        'Root_actual_complete_native_Source_binding_inverse.json':(json.dumps(dict(schema='ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_BOUND_GLOBALS_FULL_REVERSE_V1',source_only=True,checker_full_inverse=checker_inverse,host_full_inverse=host_inverse,checker_original_bytes_restored=True,host_original_bytes_restored=True,no_candidate_or_guard_execution=True,no_original_material_payload_read=True),indent=2)+'\n').encode(),
    }
    for name,raw in outputs.items():
        with(destination/name).open('xb')as stream:stream.write(raw)
    record=dict(schema='ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_BINDING_RECORD_V1',source_only=True,
                request=request_pin,author_manifest=mp,complete_parent_Source_members=manifest['member_count'],
                complete_original_input_pins_count=129,all_original_input_pins_preserved_exact=True,
                bound_outputs={name:pin(destination/name)for name in outputs},
                future_actual_namespaces=namespaces,actual_source_admission=request['source_admission_pin'],
                actual_Source_admission_tool_truth=source_truth,prior_actual_closed_V22_build_tool_truth=prior_truth,
                actual_Source_scope_coupling=scope_coupling,actual_author_Source_contract=expected_sources,
                original_caps=CAPS,actual_source_installed=None,actual_genuine_host_run=None,actual_native_success=None,
                actual_native_byte_qualification_sha256=None,actual_scientific_qualification_sha256=None,
                original_native_build_binary_Source_linkage_qualified=False,new_native_walker_controls_actual_run=None,
                no_candidate_helper_API_guard_compile_or_business_execution=True,no_original_numeric_native_or_ASCII_payload_read=True,
                no_project_ART_or_existing_Source_package_write=True)
    record_path=destination/'Root_actual_complete_native_Source_binding_record.json'
    with record_path.open('x')as stream:json.dump(record,stream,indent=2,allow_nan=False);stream.write('\n')
    require(pin(P/'MANIFEST.json')==mp and pin(args.request)==request_pin,'complete Source/request unchanged')
    for m in members:typed_pin({key:m[key]for key in ('path','sha256','size_bytes','identity')})
    for key in ('source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin','prior_actual_V22_build_tool_return_pin'):typed_pin(request[key])
    require(source_scope_contract(request,expected_sources,actual_terminal(request['actual_Root_Source_admission_tool_return_pin'],True,'ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1'))==scope_coupling,'all Source admission/peer coupling unchanged after Source binding')
    actual_terminal(request['prior_actual_V22_build_tool_return_pin'],False,'ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1')
    print(json.dumps(dict(source_only=True,status='ACTUAL_NATIVE_SOURCE_BOUND_ONLY_NOT_INSTALLED_OR_RUN',complete_original_input_pins=129,binding_record=pin(record_path),bound_outputs=record['bound_outputs'],no_candidate_helper_API_guard_or_business_execution=True,no_native_numeric_material_payload_read=True),indent=2,allow_nan=False),flush=True)


if __name__=='__main__':
    main()
