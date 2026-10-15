"""Finite Root controls Source binder: full Source/small META only, no imports.
Creates fresh complete D, bound driver, actual binding and full inverse. It
neither executes controls nor creates business/native/scientific qualification.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat

P=Path(__file__).resolve().parent
CANONICAL={'fortran':'/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15','c':'/usr/bin/gcc','cpp':'/usr/bin/cpp','ar':'/usr/bin/ar','lsof':'/usr/sbin/lsof','ps':'/bin/ps'}
STDLIB_PATH='/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12/subprocess.py'
STDLIB_SHA='85d29b2bf0249f5436838298c9a60ee93508b1102e9ac43b001f8a7e7ae8f375'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)

def require(v,m):
    if type(v) is not bool or not v:raise ValueError(m)

def validate_saved_metadata_types(value):
    if type(value)is dict:
        if set(value) in ({'path','sha256','identity'},{'path','sha256','size_bytes','identity'}):
            require(type(value['path'])is str and Path(value['path']).is_absolute()and '..'not in Path(value['path']).parts and type(value['sha256'])is str and len(value['sha256'])==64 and all(c in '0123456789abcdef'for c in value['sha256']),'typed complete metadata pin path/SHA')
            require(type(value['identity'])is list and len(value['identity'])==7 and all(type(x)is int and x>=0 for x in value['identity']),'typed complete metadata integer7ID')
            if 'size_bytes'in value:require(type(value['size_bytes'])is int and value['size_bytes']>=0 and value['size_bytes']==value['identity'][4],'typed complete metadata size')
        for k,v in value.items():
            if k=='original_caps':require(type(v)is dict and set(v)==set(CAPS)and all(type(x)is int for x in v.values())and v==CAPS,'typed unchanged original nine caps')
            if k=='directories':require(type(v)is dict and all(type(row)is list and len(row)==7 and all(type(x)is int and x>=0 for x in row)for row in v.values()),'typed complete directory7IDs')
            validate_saved_metadata_types(v)
    elif type(value)is list:
        for v in value:validate_saved_metadata_types(v)
    elif type(value)is float:require(value-value==0,'finite saved metadata float')
    return value

def strict_json(raw):
    def pairs(items):
        d={}
        for k,v in items:require(k not in d,'duplicate Source binding key');d[k]=v
        return d
    return validate_saved_metadata_types(json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v))))

def fullpin(path,positive_nlink_role=None):
    p=Path(path);s=p.lstat();ident=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    allowed=s.st_nlink==1
    if positive_nlink_role in CANONICAL:allowed=str(p)==CANONICAL[positive_nlink_role] and s.st_nlink>=1
    elif positive_nlink_role=='exact_subprocess_Source':allowed=str(p)==STDLIB_PATH and s.st_nlink>=1
    elif positive_nlink_role is not None:raise ValueError('undeclared positive-link role')
    require(p.is_absolute() and stat.S_ISREG(s.st_mode) and allowed and all(not q.is_symlink()for q in(p,*p.parents)),'exact declared Source/tool nonalias link contract')
    with p.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    t=p.lstat();require([t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==ident,'complete Source/META EOF unchanged')
    return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ident)

def write_new(path,value):
    with path.open('x') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

def main():
    cli=argparse.ArgumentParser()
    for name in('source-manifest-sha256','independent-Source-review','Source-admission','actual-Source-admission-terminal','actual-tool-pins-meta','actual-stdlib-Source-witness','output-source-dir','receipts'):cli.add_argument('--'+name,required=True)
    a=cli.parse_args();mfpin=fullpin(P/'MANIFEST.json');require(mfpin['sha256']==a.source_manifest_sha256,'actual complete Source manifest SHA')
    mf=strict_json((P/'MANIFEST.json').read_bytes());members=mf['members']
    require(mf['source_only'] is True and mf['status']=='UNREADY_SOURCE_ONLY_REQUIRES_INDEPENDENT_REVIEW' and type(members) is list and bool(members),'actual full UNREADY Source')
    before={}
    for row in members:
        rel=Path(row['relative_path']);require(not rel.is_absolute()and '..'not in rel.parts and str(rel) not in before,'unique complete relative Source member')
        require(fullpin(P/rel)==row['fullpin'],'all complete Source members');before[str(rel)]=row['fullpin']
    require({str(p.relative_to(P))for p in P.rglob('*')if p.is_file()}==set(before)|{'MANIFEST.json'},'complete Source owner files, no omitted members')
    contract=strict_json((P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json').read_bytes())
    author={k:fullpin(P/v)for k,v in contract['required_author_Source_roles'].items()}
    peer_pin=fullpin(a.independent_Source_review);peer=strict_json(Path(a.independent_Source_review).read_bytes())
    ad_pin=fullpin(a.Source_admission);ad=strict_json(Path(a.Source_admission).read_bytes())
    truth_pin=fullpin(a.actual_Source_admission_terminal);truth=strict_json(Path(a.actual_Source_admission_terminal).read_bytes());terminal=truth['terminal_tool_return']
    require(peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_BINDER_SOURCE_REVIEW_V1'and peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and peer['source_only'] is True and peer['all_checks_passed'] is True and peer['blockers']==[] and peer['actual_author_Source_contract']==author,'actual independent complete N8 Source review')
    checks=peer['checks'];require(type(checks) is list and type(peer['check_count']) is int and peer['check_count']==len(checks)>0 and len({c['check']for c in checks})==len(checks) and all(type(c) is dict and set(c)=={'check','passed'}and type(c['check']) is str and bool(c['check'])and c['passed'] is True for c in checks),'all unique typed Source checks')
    require(ad['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_V1'and ad['status']=='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE'and ad['source_only'] is True and ad['actual_author_Source_contract']==author and ad['independent_Source_review_pin']==peer_pin and ad['scientific_qualification_created'] is False,'Root complete Source-only admission')
    require(truth['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1'and truth['closed'] is True and truth['observed_terminal'] is True and truth['session_repolled_after_close'] is False and type(terminal['exit_code']) is int and terminal['exit_code']==0 and 'session_id'not in terminal and terminal['chunk_id']==truth['actual_terminal_chunk'],'actual Root Source admission typed CLOSED0')
    require(strict_json(terminal['output'])['source_admission_pin']==ad_pin,'actual Root Source-admission output pin coupling')
    tools_meta_pin=fullpin(a.actual_tool_pins_meta);tools=strict_json(Path(a.actual_tool_pins_meta).read_bytes())['tool_pins'];require(type(tools) is dict and set(tools)==set(CANONICAL),'all six exact canonical tools')
    for k,v in tools.items():require(fullpin(v['path'],k)==v,'real whole canonical tool Source pin, never replacement producer')
    stdlib_witness_pin=fullpin(a.actual_stdlib_Source_witness);witness=strict_json(Path(a.actual_stdlib_Source_witness).read_bytes());std=witness['actual_stdlib_subprocess_Source_pin']
    require(witness['schema']=='ROOT_ACTUAL_N8_PYTHON_SUBPROCESS_SOURCE_AND_WAIT_OWNER_WITNESS_V1' and witness['source_only'] is True and witness['actual_wait_poll_signal_or_control_execution'] is False and std['path']==STDLIB_PATH and std['sha256']==STDLIB_SHA and std['size_bytes']==88747 and fullpin(std['path'],'exact_subprocess_Source')==std,'actual exact Source witness, no guessed wait capability')
    base=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010');art=Path('/Users/wen/spot/validation/artifacts')
    D=base/'actual_complete_native_observation_BUILD5_AB_v9_link_count_monitor_controls_sources';E=base/'actual_complete_native_observation_BUILD5_AB_v9_link_count_monitor_controls_receipts'
    require(Path(a.output_source_dir)==D and Path(a.receipts)==E and not os.path.lexists(D) and E.is_dir()and not E.is_symlink(),'fixed fresh controls D and actual preexisting E')
    case_ids=strict_json((P/'N8_TWELVE_GENUINE_CONTROL_PROTOCOL.UNREADY.json').read_bytes())['case_ids'];require(type(case_ids) is list and len(case_ids)==12 and len(set(case_ids))==12,'all twelve Source-defined categories')
    namespaces={}
    for n,case_id in enumerate(case_ids,1):
        prefix='axial-material-complete-native-observation-BUILD5-AB-v9-link-count-monitor-controls-case'+str(n).zfill(2)
        ns=dict(host=str(art/(prefix+'-host-20261011')),output=str(art/(prefix+'-runtime-20261011')),control=str(art/(prefix+'-control-20261011')),source=str(D),receipts=str(E))
        require(not any(os.path.lexists(ns[k])for k in('host','output','control')),'all fresh case HOC zero retries')
        namespaces[case_id]=ns
    D.mkdir()
    for p in sorted(P.rglob('*')):
        target=D/p.relative_to(P)
        if p.is_dir():target.mkdir()
        else:shutil.copy2(p,target)
    binding=dict(schema='ROOT_ACTUAL_N8_MONITOR_CONTROLS_SOURCE_BINDING_V1',source_only=True,actual_author_Source_contract=author,actual_independent_Source_review_pin=peer_pin,actual_Source_admission_pin=ad_pin,actual_Root_Source_admission_tool_terminal_pin=truth_pin,actual_canonical_tools_META_pin=tools_meta_pin,actual_stdlib_Source_witness_pin=stdlib_witness_pin,actual_stdlib_subprocess_Source_pin=std,tool_pins=tools,case_namespaces=namespaces,original_caps=CAPS,actual_control_execution=None,actual_monitor_controls_qualification=None,actual_native_or_scientific_qualification=None,scientific_qualification_created=False)
    binding_path=D/'Root_actual_N8_monitor_controls_Source_binding.json';write_new(binding_path,binding);bp=fullpin(binding_path)
    original=(P/'N8_genuine_integrated_controls_driver.UNREADY.py').read_bytes();text=original.decode();lines=text.splitlines(keepends=True);changes=dict(SOURCE_STATUS='READY_SOURCE_REVIEWED_ROOT_CONTROLS_BINDING_REQUIRED',SOURCE_BINDING_PATH=str(binding_path),SOURCE_BINDING_SHA256=bp['sha256']);hunks=[]
    for node in ast.parse(text).body:
        if isinstance(node,ast.Assign)and len(node.targets)==1 and isinstance(node.targets[0],ast.Name)and node.targets[0].id in changes:
            key=node.targets[0].id;old=''.join(lines[node.lineno-1:node.end_lineno]);new=key+' = '+repr(changes[key])+'\n';hunks.append(dict(key=key,line=node.lineno,end_line=node.end_lineno,old=old,new=new))
    require(len(hunks)==len(changes),'all and only three complete control driver globals')
    for h in reversed(hunks):lines[h['line']-1:h['end_line']]=[h['new']]
    bound=''.join(lines).encode();ast.parse(bound);restored=bound
    for h in hunks:require(restored.count(h['new'].encode())==1,'unique whole control driver inverse');restored=restored.replace(h['new'].encode(),h['old'].encode(),1)
    require(restored==original,'complete control driver byte and AST inverse')
    bound_path=D/'Root_bound_N8_genuine_monitor_controls_driver.py';bound_path.write_bytes(bound)
    inverse_path=D/'Root_actual_N8_bound_controls_Source_full_inverse.json';write_new(inverse_path,dict(schema='ROOT_ACTUAL_N8_BOUND_MONITOR_CONTROLS_SOURCE_INVERSE_V1',source_only=True,original_driver_Source_pin=author['monitor_control_driver'],actual_bound_driver_Source_pin=fullpin(bound_path),hunks=hunks,whole_byte_and_AST_inverse=True,actual_controls_execution=None))
    require(all(fullpin(P/rel)==wanted for rel,wanted in before.items()) and fullpin(P/'MANIFEST.json')==mfpin,'complete author Source unchanged')
    print(json.dumps(dict(status='BOUND_N8_GENUINE_MONITOR_CONTROLS_SOURCE_ONLY_NOT_EXECUTED',source_only=True,actual_controls_Source_binding_pin=bp,bound_controls_driver_Source_pin=fullpin(bound_path),actual_bound_controls_inverse_pin=fullpin(inverse_path),actual_monitor_controls_qualification=None,actual_native_or_scientific_qualification_created=False),allow_nan=False),flush=True)

if __name__=='__main__':main()
