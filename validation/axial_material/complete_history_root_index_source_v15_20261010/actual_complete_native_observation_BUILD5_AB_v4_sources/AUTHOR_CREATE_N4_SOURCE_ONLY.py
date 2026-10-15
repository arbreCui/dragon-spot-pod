"""Author only Source text/AST/inverse in fresh TMP. Never import/run candidates."""
from pathlib import Path
import ast
import difflib
import hashlib
import json
import shutil
import tempfile

P=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_E_fullpin_same_sort_finite_UNREADY_Source_fix_pb5gkdac')
E=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_observation_BUILD5_AB_v3_receipts')
FILES=['Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','complete_observation_BUILD5_AB_runtime.UNREADY.py','complete_observation_genuine_host.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py']
TOOLS={'fortran':'/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15','c':'/usr/bin/gcc','cpp':'/usr/bin/cpp','ar':'/usr/bin/ar','lsof':'/usr/sbin/lsof','ps':'/bin/ps'}
HELPER="""CANONICAL_OS_TOOL_PATHS = {tools!r}

def source_tool_nlink_allowed(path,nlink,tool_role=None):
    # Default stays the original single-link contract. Only an explicit one of
    # these six original OS tool roles may preserve a positive real hardlink
    # count. Paths, bytes, all seven identity integers and caller order stay real.
    if tool_role is None:return type(nlink)is int and nlink==1
    require(type(tool_role)is str and tool_role in CANONICAL_OS_TOOL_PATHS,'declared original canonical OS tool role only')
    return str(path)==CANONICAL_OS_TOOL_PATHS[tool_role]and type(nlink)is int and nlink>=1

""".format(tools=TOOLS)

def pin(p):
    a=p.lstat();raw=p.read_bytes();b=p.lstat();assert a==b
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=[b.st_dev,b.st_ino,b.st_mode,b.st_nlink,b.st_size,b.st_mtime_ns,b.st_ctime_ns])

def replace(text,old,new):
    assert text.count(old)==1,(old,text.count(old))
    return text.replace(old,new,1)

def insert_helper(text):
    at=text.index('def require(')
    return text[:at]+HELPER+text[at:]

def derive(name,raw):
    text=raw.decode();text=insert_helper(text)
    if name==FILES[0]:
        text=replace(text,'def pin(path,deadline):','def pin(path,deadline,tool_role=None):')
        text=replace(text,"and s.st_nlink==1,'actual Root full regular singlelink pin')","and source_tool_nlink_allowed(p,s.st_nlink,tool_role),'actual Root full regular pin; only declared canonical OS tools may have real positive hardlinks')")
        text=replace(text,"tools={k:pin(getattr(a,k),deadline)for k in('fortran','c','cpp','ar','lsof','ps')};libraries={}","require(all(getattr(a,k)==v for k,v in CANONICAL_OS_TOOL_PATHS.items()),'all six original canonical OS tool CLI paths unchanged')\n    tools={k:pin(getattr(a,k),deadline,tool_role=k)for k in('fortran','c','cpp','ar','lsof','ps')};libraries={}")
    elif name==FILES[1]:
        text=replace(text,'def pin(path):','def pin(path,tool_role=None):')
        text=replace(text,"and s.st_nlink==1,'regular single-link nonalias Source/META')","and source_tool_nlink_allowed(p,s.st_nlink,tool_role),'regular nonalias Source/META; default single-link, canonical OS tool role preserves actual positive nlink')")
        text=replace(text,'def shape(p):','def shape(p,tool_role=None):')
        text=replace(text,"and p['identity'][3]==1 and p['identity'][4]==p['size_bytes']","and source_tool_nlink_allowed(p['path'],p['identity'][3],tool_role)and p['identity'][4]==p['size_bytes']")
        text=replace(text,'    for p in rows+extra:shape(p)',"    require(type(b['tool_pins'])is dict and set(b['tool_pins'])==set(CANONICAL_OS_TOOL_PATHS),'complete fixed six OS tool roles before extra pin shapes')\n    for role,p in b['tool_pins'].items():shape(p,tool_role=role)\n    tool_roles_by_path={p['path']:role for role,p in b['tool_pins'].items()}\n    for p in rows:shape(p)\n    for p in extra:shape(p,tool_role=tool_roles_by_path.get(p['path']))")
        text=replace(text,"    for p in b['tool_pins'].values():shape(p);require(allpins.get(p['path'])==p,'all actual toolpins protected')","    for role,p in b['tool_pins'].items():shape(p,tool_role=role);require(allpins.get(p['path'])==p,'all actual toolpins protected')")
    elif name==FILES[2]:
        text=replace(text,'def fullpin(path,budget=lambda:None):','def fullpin(path,budget=lambda:None,tool_role=None):')
        text=replace(text,"and before[3]==1,'regular nonalias single-link full input')","and source_tool_nlink_allowed(path,before[3],tool_role),'regular nonalias full input; default single-link except explicit canonical OS tools')")
        text=replace(text,'def pinshape(p):','def pinshape(p,tool_role=None):')
        text=replace(text,"and p['identity'][3]==1 and p['identity'][4]==p['size_bytes']","and source_tool_nlink_allowed(p['path'],p['identity'][3],tool_role)and p['identity'][4]==p['size_bytes']")
        text=replace(text,"def recheck(p,budget=lambda:None):\n    pinshape(p);require(fullpin(p['path'],budget)==p,'complete input SHA/7ID changed: '+p['path']);return p","def recheck(p,budget=lambda:None,tool_role=None):\n    pinshape(p,tool_role=tool_role);require(fullpin(p['path'],budget,tool_role=tool_role)==p,'complete input SHA/7ID changed: '+p['path']);return p")
        text=replace(text,'    for p in allpins.values():pinshape(p)',"    require(type(b['tool_pins'])is dict and set(b['tool_pins'])==set(CANONICAL_OS_TOOL_PATHS),'complete fixed six OS tool roles before extra input shapes')\n    for role,p in b['tool_pins'].items():pinshape(p,tool_role=role)\n    tool_roles_by_path={p['path']:role for role,p in b['tool_pins'].items()}\n    for p in rows:pinshape(p)\n    for p in extra:pinshape(p,tool_role=tool_roles_by_path.get(p['path']))")
        text=replace(text,"    for p in b['tool_pins'].values():pinshape(p);require(allpins.get(p['path'])==p,'all actual tools in full protected input list')","    for role,p in b['tool_pins'].items():pinshape(p,tool_role=role);require(allpins.get(p['path'])==p,'all actual tools in full protected input list')")
        text=replace(text,'    for p in inputs:recheck(p)',"    tool_roles_by_path={p['path']:role for role,p in b['tool_pins'].items()}\n    for p in inputs:recheck(p,tool_role=tool_roles_by_path.get(p['path']))")
        text=replace(text,'        for p in inputs:recheck(p,budget)',"        for p in inputs:recheck(p,budget,tool_role=tool_roles_by_path.get(p['path']))")
        text=replace(text,'                try:after_inputs.append(recheck(p))',"                try:after_inputs.append(recheck(p,tool_role=tool_roles_by_path.get(p['path'])))")
    elif name==FILES[3]:
        text=replace(text,'def typed_full_pin(expected):','def typed_full_pin(expected,tool_role=None):')
        text=replace(text,"and expected['identity'][3]==1 and expected['identity'][4]==expected['size_bytes']","and source_tool_nlink_allowed(expected['path'],expected['identity'][3],tool_role)and expected['identity'][4]==expected['size_bytes']")
        text=replace(text,'def recheck_full_pin(support,expected):\n    typed_full_pin(expected)','def recheck_full_pin(support,expected,tool_role=None):\n    typed_full_pin(expected,tool_role=tool_role)')
    elif name==FILES[4]:
        text=replace(text,'def fullpin(path):','def fullpin(path,tool_role=None):')
        text=replace(text,"and s.st_nlink==1,'full postclose pin regular noalias')","and source_tool_nlink_allowed(p,s.st_nlink,tool_role),'full postclose regular noalias; default single-link except explicit canonical OS tools')")
        text=replace(text,'def check(p):','def check(p,tool_role=None):')
        text=replace(text,"and p['identity'][3]==1 and p['identity'][4]==p['size_bytes']","and source_tool_nlink_allowed(p['path'],p['identity'][3],tool_role)and p['identity'][4]==p['size_bytes']")
        text=replace(text,"require(fullpin(p['path'])==p,'full postclose pin differs');return p","require(fullpin(p['path'],tool_role=tool_role)==p,'full postclose pin differs');return p")
        text=replace(text,"    for p in h['complete_input_pins_before_and_after']:check(p)","    require(type(b['tool_pins'])is dict and set(b['tool_pins'])==set(CANONICAL_OS_TOOL_PATHS),'complete original six OS tools before postclose full input checking')\n    for role,p in b['tool_pins'].items():check(p,tool_role=role)\n    tool_roles_by_path={p['path']:role for role,p in b['tool_pins'].items()}\n    for p in h['complete_input_pins_before_and_after']:check(p,tool_role=tool_roles_by_path.get(p['path']))")
    ast.parse(text)
    return text.encode()

def topdefs(raw):
    text=raw.decode();lines=text.splitlines(keepends=True)
    return {n.name:dict(bytes=''.join(lines[n.lineno-1:n.end_lineno]),AST=ast.dump(n,include_attributes=False))for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}

def main():
    mf=json.loads((P/'MANIFEST.json').read_bytes());assert hashlib.sha256((P/'MANIFEST.json').read_bytes()).hexdigest()=='5313b65cc109d93816137f8c53e6cdcfbf6d5044310762ac65a20a2f76330593'
    before={str(p.relative_to(P)):pin(p)for p in P.rglob('*')if p.is_file()};assert len(before)==81
    N=Path(tempfile.mkdtemp(prefix='axmat_complete_native_observation_BUILD5_AB_role_limited_OS_tools_N4_UNREADY_Source_',dir='/private/tmp'))
    for p in sorted(P.rglob('*')):
        if p.name=='MANIFEST.json'and p.parent==P:continue
        q=N/p.relative_to(P)
        if p.is_dir():q.mkdir(exist_ok=True)
        else:shutil.copyfile(p,q)
    previous=N/'PREVIOUS_SEALED_N3_SOURCE_PROVENANCE';previous.mkdir();shutil.copyfile(P/'MANIFEST.json',previous/'MANIFEST.json')
    old=previous/'FIVE_ORIGINAL_N3_SOURCE';old.mkdir()
    allhunks={};proof={}
    for name in FILES:
        original=(P/name).read_bytes();(old/name).write_bytes(original);new=derive(name,original);(N/name).write_bytes(new)
        a=original.decode().splitlines(keepends=True);b=new.decode().splitlines(keepends=True);hunks=[]
        for op,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
            if op!='equal':hunks.append(dict(original_start0=i,original_stop0=j,derived_start0=k,derived_stop0=l,original=''.join(a[i:j]),derived=''.join(b[k:l])))
        restored=b[:]
        for h in reversed(hunks):restored[h['derived_start0']:h['derived_stop0']]=h['original'].splitlines(keepends=True)
        assert ''.join(restored).encode()==original
        oa,na=topdefs(original),topdefs(new);unchanged=[key for key in oa if oa[key]==na[key]];changed=[key for key in oa if oa[key]!=na[key]]
        allhunks[name]=hunks;proof[name]=dict(original_pin=before[name],derived_pin=pin(N/name),full_byte_inverse_restores_N3=True,full_AST_inverse_restores_N3=True,all_original_topdef_names_retained=set(oa)<=set(na),unchanged_topdefs_fullbytes_and_AST=unchanged,changed_original_topdefs=changed,added_topdefs=[k for k in na if k not in oa])
    evidence=N/'ACTUAL_PRIOR_N3_SOURCE_META_FAILURE_EVIDENCE';evidence.mkdir()
    actual=[]
    for name in ['Root_actual_complete_native_observation_N3_Source_admission.json','Root_actual_observation_Source_admission_tool_terminal_return.json','Root_actual_observation_request_META_alias_failure_tool_terminal_return.json']:
        src=E/name;sp=pin(src);shutil.copyfile(src,evidence/name);assert pin(src)==sp;actual.append(dict(original_pin=sp,copied_pin=pin(evidence/name),original_scope='N3_ONLY_NOT_N4_SOURCE_ADMISSION'))
    (N/'COMPLETE_FIVE_ROLE_OS_TOOL_NLINK_SOURCE_INVERSE.json').write_text(json.dumps(dict(schema='COMPLETE_N4_ROLE_LIMITED_OS_TOOL_NLINK_SOURCE_INVERSE_V1',source_only=True,coordinate_convention='0-based half-open line spans',canonical_OS_tool_paths=TOOLS,five_role_complete_inverse_hunks=allhunks,five_role_full_definition_proof=proof,all_original_N3_members_other_than_five_roles_byte_exact=True,N3_original_manifest_pin=before['MANIFEST.json'],N3_original_fullfile_pins=before,actual_prior_N3_Source_META_evidence=actual,actual_independent_N4_Source_review=None,actual_Root_N4_Source_admission=None,actual_build_native_or_material_execution=None,scientific_qualification_created=False),indent=2,allow_nan=False)+'\n')
    (N/'N4_ROOT_NEXT_STEPS_SOURCE_ONLY.txt').write_text('N4 is UNREADY Source only. Preserve original129 and full14 author pins. Six canonical OS tool roles alone may preserve exact positive actual nlink; all ordinary inputs/Source/material/library/produced files and H/O/C/D/E namespace entries retain nlink1. Never copy/rename OS tools or normalize7ID. N3 actual988463 Source admission belongs only to N3; request88c74a failed before output/build/material. Root9261c9 tool stat receipt is to be preserved only from its genuine saved original, never reconstructed. After independent N4 Source review, Root must create new N4-only Source admission and genuine typed0CLOSED wrapper, then use this N4 request_preparer and binder. Future business pins remain None/false. Complete V25 five-stage build first, observer full four libraries/newlink/AthenB afterwards serially under original1800/600/512MiB/2GiB joint/96GiB history/free8GiB/1thread/1child/0retry. Complete D/E freeze precedes live business. CLOSED actual business terminal first goes H; E gains only own postclose manifest after complete HOCDE views, then later receipt appends are honestly labeled. AAA7/8 and ABAunstarted; no runtime, native Source-bin qualification or science granted.\n')
    (N/'N4_CANONICAL_OS_TOOL_ROLE_CONTRACT.Source_META.json').write_text(json.dumps(dict(schema='N4_CANONICAL_OS_TOOL_ROLE_LIMITED_POSITIVE_NLINK_SOURCE_CONTRACT_V1',source_only=True,canonical_OS_tool_paths=TOOLS,explicit_tool_role_required=True,default_nlink=1,allowed_tool_nlink='exact int >=1, complete actual 7ID never rewritten',same_original_calls_paths_basename_flags=True,namespace_tree_and_joint_hardlink_prohibition_unchanged=True,new_original129_new_library_or_deck_generation=False,actual_independent_N4_Source_review=None,actual_Root_N4_Source_admission=None,actual_Root_N4_runtime_terminal=None,actual_tool_controls_execution=None,scientific_qualification_created=False),indent=2)+'\n')
    assert before=={str(p.relative_to(P)):pin(p)for p in P.rglob('*')if p.is_file()}
    (N/'AUTHOR_CREATE_N4_SOURCE_ONLY.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps(dict(status='AUTHORED_MUTABLE_N4_SOURCE_ONLY_NOT_SEALED_OR_ADMITTED',source_only=True,path=str(N),five_changed_Source_pins={name:pin(N/name)for name in FILES},inverse_pin=pin(N/'COMPLETE_FIVE_ROLE_OS_TOOL_NLINK_SOURCE_INVERSE.json'),old_N3_Source_unchanged=True,candidate_API_guard_compile_native_or_material_executed=False),allow_nan=False))

if __name__=='__main__':main()
