#!/usr/bin/env python3
"""Seal only finite SOURCE package; compile never executes code."""
from pathlib import Path
import ast
import hashlib
import json
import stat

BASE=Path(__file__).absolute().parent
PARENT_SHA='566939e3fbc7eddcc2b5af324a6dd11e97f83b033994e36389f7819d06084de3'
CANDIDATE_SHA='75969eafb9e1eead11e25d8838c6e3be13ea64babdc56ee222252a5e11bded62'
PROTOTYPE_SHA='f229e3116f61caad7b4c34f3ccd5705e5392f58ee2fd97066425bd64f57f5125'

def ident(path):
    s=path.lstat()
    if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1:raise ValueError('single-link SOURCE ordinary file required')
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def read_source(path):
    a=ident(path);data=path.read_bytes();b=ident(path)
    if a!=b or len(data)!=a[4]:raise ValueError('SOURCE full EOF identity changed')
    return data,dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity7=a)

def main():
    proofraw,proofpin=read_source(BASE/'full_finite_source_inverse_proof.json')
    proof=json.loads(proofraw)
    candidate=Path(proof['candidate']['path'])
    craw,cpin=read_source(candidate)
    if cpin['sha256']!=CANDIDATE_SHA or proof['candidate']['sha256']!=CANDIDATE_SHA:
        raise ValueError('sealed complete candidate SHA differs')
    parentraw,parentpin=read_source(BASE/'frozen_complete_parent_V20_566939.SOURCE.py')
    proraw,propin=read_source(BASE/'frozen_reviewed_strict_decode_prototype_f229.SOURCE.py')
    if parentpin['sha256']!=PARENT_SHA or propin['sha256']!=PROTOTYPE_SHA:
        raise ValueError('complete SOURCE snapshot SHA differs')
    restored=craw.decode('utf-8')
    for e in reversed(proof['edits']):
        if e['count']!=1 or restored.count(e['new'])!=1:raise ValueError('full inverse not unique')
        restored=restored.replace(e['new'],e['old'],1)
    if restored.encode()!=parentraw or hashlib.sha256(restored.encode()).hexdigest()!=PARENT_SHA:
        raise ValueError('whole SOURCE inverse differs')
    if len(proof['edits'])!=13 or len(proof['definition_inventory'])!=70 or proof['inverse_sha256']!=PARENT_SHA:
        raise ValueError('complete finite inventory differs')
    for pin in proof['full_SOURCE_inputs_before_after']:
        data,now=read_source(Path(pin['path']))
        if now['sha256']!=pin['sha256'] or now['identity7']!=pin['identity7']:
            raise ValueError('original fixed SOURCE before/after pin changed')
    plan=json.loads((BASE/'future_actual_helper_binding_contract.UNREADY.json').read_bytes())
    if (plan['accepted_actual_qualification_schema'] is not None
        or plan['new_helper_qualification_sha256'] is not None
        or any(x is not None for x in plan['future_business_pins'].values())
        or plan['ready_binding_not_implemented_or_executed'] is not True):
        raise ValueError('future actual helper/business binding must remain unknown')
    files=[]
    paths=sorted(BASE.iterdir(),key=lambda p:p.name)
    if (BASE/'sealed_manifest.json').exists():raise ValueError('package is already sealed')
    for path in paths:
        if path.name=='sealed_manifest.json':continue
        data,pin=read_source(path)
        if path.suffix=='.py':
            ast.parse(data.decode('utf-8'))
            compile(data,str(path),'exec',dont_inherit=True,optimize=0)
        files.append(dict(relative=path.name,**pin))
    for pin in files:
        _,now=read_source(Path(pin['path']))
        if {k:v for k,v in pin.items() if k!='relative'}!=now:
            raise ValueError('package SOURCE pin changed')
    payload=dict(schema='AXMAT_V21_COMPLETE_RUNTIME_UNREADY_SOURCE_PACKAGE_MANIFEST_V1',
        status='SEALED_SOURCE_ONLY_UNREADY_NO_BUSINESS_CREDIT',
        candidate=cpin,parent=parentpin,reviewed_prototype=propin,source_inverse_proof=proofpin,
        full_byte_inverse_to=PARENT_SHA,member_count=len(files),files=files,
        package_total_source_bytes=sum(x['size_bytes'] for x in files),
        original_top_level_definitions=70,non_decoder_definitions=69,
        all_original_physics_inputs_caps_fullscope_and_five_stages_unchanged=True,
        actual_new_helper_Q_read=False,actual_new_helper_Q=None,
        six_future_combined_native_success_pins=None,
        project_helper_guard_API_business_numeric_historyscan_executed=False,
        canonical_ART_frozen_or_results_modified=False,
        static_compile_only=True,actual_RSS_or_business_success_claimed=False)
    out=(json.dumps(payload,ensure_ascii=False,indent=2)+'\n').encode()
    with (BASE/'sealed_manifest.json').open('xb') as f:f.write(out)
    _,mpin=read_source(BASE/'sealed_manifest.json')
    print(json.dumps(dict(status=payload['status'],manifest=mpin,member_count=len(files),
        candidate=cpin,full_inverse_exact=True,source_only=True),ensure_ascii=False))

if __name__=='__main__':main()

