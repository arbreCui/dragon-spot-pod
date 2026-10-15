"""Finite Source-only author repair, preserves complete preceding draft bytes."""
import ast
import difflib
import hashlib
import json
from pathlib import Path
import shutil

P=Path('/private/tmp/axmat_N8_exact_owner_complete_UNREADY_Source_mjczixe4')
MOTHER=Path('/private/tmp/axmat_complete_native_observation_N7_failure_only_monitor_UNREADY_Source_piquf6v6')

VALIDATOR='''def validate_saved_metadata_types(value):
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

'''

def pin(path):
    s=path.lstat()
    with path.open('rb')as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    return dict(path=str(path),sha256=sha,size_bytes=s.st_size,identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns])

def main():
    backup=P/'AUTHOR_DRAFT_ERRORS/before_typed_metadata_and_protocol_scope_repair';backup.mkdir()
    names=['N8_actual_controls_qualification_gate.Source_META_only.py','N8_bind_monitor_controls_SOURCE_META_only.UNREADY.py','N8_genuine_integrated_controls_driver.UNREADY.py','N8_Root_controls_postclose_META.UNREADY.py']
    for name in names:
        path=P/name;shutil.copy2(path,backup/name);text=path.read_text()
        node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)and n.name=='strict_json')
        lines=text.splitlines(keepends=True);body=''.join(lines[node.lineno-1:node.end_lineno])
        assert body.count('return json.loads(')==1
        newbody=body.replace('return json.loads(','return validate_saved_metadata_types(json.loads(',1)
        pos=newbody.rfind(')');newbody=newbody[:pos]+')'+newbody[pos:]
        lines[node.lineno-1:node.end_lineno]=[VALIDATOR+newbody];text=''.join(lines);ast.parse(text);path.write_text(text)
    gate=(P/names[0]).read_text();gate=gate[gate.index('CASE_IDS='):]
    import re
    for name in ('require','strict_json','fullpin','recheck_pinned','read_pinned','actual_closed_zero','validate_saved_metadata_types'):
        gate=re.sub(r'\b'+name+r'\b','n8_'+name,gate)
    gate=gate.replace('CASE_IDS','N8_CASE_IDS')
    for name in ('complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py'):
        path=P/name;shutil.copy2(path,backup/name);text=path.read_text();start=text.index('N8_CASE_IDS=');node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)and n.name=='validate_actual_N8_monitor_controls');lines=text.splitlines(keepends=True);end=len(''.join(lines[:node.end_lineno]));text=text[:start]+gate.rstrip()+'\n\n'+text[end:];ast.parse(text);path.write_text(text)
    path=P/'N8_TWELVE_GENUINE_CONTROL_PROTOCOL.UNREADY.json';shutil.copy2(path,backup/path.name);d=json.loads(path.read_bytes())
    d['new_instrumentation']['production_post_start_control_callback']=None
    d['cases'][0]['source_required_behavior']+=' A second real early-exit child is reaped by its exact original Popen wait before any business census and is explicitly refused as unknown ancestry.'
    d['cases'][6]['source_required_behavior']='Real untracked descendant is selected in fullPS then closed/reaped by its own parent during the one-shot transition. The single canonical lsof must be rejected on nonzero or incomplete selected-PID coverage. A fully complete passing scan instead fails this expected-refusal control, with no retry or whitelist.'
    path.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
    inv=json.loads((P/'COMPLETE_N8_FOUR_ROLE_BYTE_AST_INVERSE.json').read_bytes())
    for row in inv['roles']:
        old=(MOTHER/row['role_basename']).read_text();new=(P/row['role_basename']).read_text();oldlines=old.splitlines(keepends=True);newlines=new.splitlines(keepends=True);hunks=[]
        for tag,a,b,c,e in difflib.SequenceMatcher(a=oldlines,b=newlines,autojunk=False).get_opcodes():
            if tag!='equal':hunks.append(dict(old_start_line0=a,old_end_line0=b,new_start_line0=c,new_end_line0=e,old_text=''.join(oldlines[a:b]),new_text=''.join(newlines[c:e])))
        restored=newlines[:]
        for h in reversed(hunks):assert ''.join(restored[h['new_start_line0']:h['new_end_line0']])==h['new_text'];restored[h['new_start_line0']:h['new_end_line0']]=h['old_text'].splitlines(keepends=True)
        assert ''.join(restored)==old and ast.dump(ast.parse(''.join(restored)),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False)
        row['hunks']=hunks;row['new_complete_Source_pin']=pin(P/row['role_basename'])
    (P/'COMPLETE_N8_FOUR_ROLE_BYTE_AST_INVERSE.json').write_text(json.dumps(inv,indent=2,allow_nan=False)+'\n')
    contract=P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json'
    (P/'COMPLETE_REQUIRED_SCOPE_JSON_BYTE_INVERSE.json').write_text(json.dumps(dict(schema='COMPLETE_N8_REQUIRED_SCOPE_JSON_FULL_BYTE_INVERSE_V1',source_only=True,parent_original_Source_pin=pin(MOTHER/contract.name),new_contract_pin=pin(contract),complete_original_bytes_base64=__import__('base64').b64encode((MOTHER/contract.name).read_bytes()).decode(),complete_new_bytes_base64=__import__('base64').b64encode(contract.read_bytes()).decode()),indent=2)+'\n')
    print(json.dumps(dict(status='AUTHOR_FINITE_TYPED_SOURCE_AND_PROTOCOL_REPAIR_ONLY',source_only=True,actual_candidate_or_API_execution=False),allow_nan=False))

if __name__=='__main__':main()
