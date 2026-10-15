"""One finite V25 utility Source seal and full postseal, no utility execution."""
import hashlib,json,stat,sys
from pathlib import Path
F=Path('/private/tmp/axmat_INDEPENDENT_V25_poststage_finite_utilities_V3_Source_693yodpc')
U=Path('/private/tmp/axmat_V25_poststage_complete_finite_utilities_V3_UNREADY_Source_20261010')
S=Path(str(F)+'_seal_receipt')
def ident(p):
    s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);a=ident(p)
    if not(p.is_absolute() and not any(x.is_symlink() for x in(p,*p.parents)) and stat.S_ISREG(a[2]) and a[3]==1):raise ValueError('ordinary Source/META')
    with p.open('rb') as f:d=hashlib.file_digest(f,'sha256').hexdigest()
    if ident(p)!=a:raise ValueError('Source full EOF7ID changed')
    return dict(path=str(p),sha256=d,size_bytes=a[4],identity=a)
def strict(raw):
    def pairs(rows):
        d={}
        for k,v in rows:
            if k in d:raise ValueError('duplicate META key')
            d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in()).throw(ValueError(s)))
def load(p):
    a=pin(p);d=strict(Path(p).read_bytes())
    if pin(p)!=a:raise ValueError('Source META parse changed')
    return d
def view(root,exclude=()):
    root=Path(root);ds={'.':ident(root)};fs={}
    for p in sorted(root.rglob('*'),key=lambda p:str(p.relative_to(root))):
        rel=str(p.relative_to(root));i=ident(p)
        if stat.S_ISDIR(i[2]):ds[rel]=i
        elif stat.S_ISREG(i[2]):
            if rel not in exclude:fs[rel]=pin(p)
        else:raise ValueError('nonordinary Source namespace')
    return dict(root=str(root),files=fs,directories=ds,symlinks={})
def validate():
    r=load(F/'REVIEW.json');cs=r['checks']
    if not(r['schema']=='INDEPENDENT_V25_POSTSTAGE_COMPLETE_UTILITIES_SOURCE_REVIEW_V1' and r['status']=='PASS_COMPLETE_POSTSTAGE_UTILITIES_SOURCE_ONLY_UNREADY_NO_EXECUTION' and r['source_only'] is True and r['all_checks_typed_true'] is True and r['all_checks_passed'] is True and r['blockers']==[] and r['errors']==[] and r['check_count']==len(cs)==30 and len({c['check'] for c in cs})==30 and all(type(c['passed']) is bool and c['passed'] is True for c in cs) and len(r['qualified_role_Source_pins'])==7 and r['actual_original_owned_file_count']==463 and r['actual_all463_original_owned_Source_full_EOF_read'] is True):raise ValueError('complete independent Source review contract')
    if view(U)!=r['complete_reviewed_utility_original_fullview']:raise ValueError('whole original utility Source changed')
    for owner in r['complete_original_owned_Source_views'].values():
        if view(owner['root'])!=owner:raise ValueError('whole original463 Source owner changed')
    for q in r['qualified_role_Source_pins'].values():
        if pin(q['path'])!=q:raise ValueError('qualified original utility role changed')
    w=load(F/'ACTUAL_INDEPENDENT_SOURCE_REVIEW_TOOL_RETURN.json');t=w['terminal_tool_return'];o=strict(t['output'])
    if not(w['closed'] is True and w['observed_terminal'] is True and type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t and t['chunk_id']=='d4e6dc' and o['review_pin']==pin(F/'REVIEW.json') and o['check_count']==30 and o['blockers']==[]):raise ValueError('actual genuine independent review terminal coupling')
    return r
def emit(v):print(json.dumps(v,allow_nan=False),flush=True)
def main():
    r=validate()
    if sys.argv[1]=='seal':
        with(F/'MANIFEST.json').open('xb') as f:
            v=view(F,('MANIFEST.json',))
            m=dict(schema='INDEPENDENT_V25_POSTSTAGE_COMPLETE_UTILITIES_SOURCE_REVIEW_MANIFEST_V1',status='SEALED_SOURCE_ONLY_NO_EXECUTION_OR_SCIENCE',source_only=True,members=v['files'],directories=v['directories'],member_count=len(v['files']),file_count_including_manifest=len(v['files'])+1,directory_count=len(v['directories']),review_pin=pin(F/'REVIEW.json'),actual_review_tool_truth_pin=pin(F/'ACTUAL_INDEPENDENT_SOURCE_REVIEW_TOOL_RETURN.json'),qualified_complete_utility_manifest_pin=pin(U/'MANIFEST.json'),qualified_role_Source_pins=r['qualified_role_Source_pins'],check_count=30,blockers=[],actual_original_owned_Source_file_count=463,actual_Source_installation=None,actual_prelaunch=None,actual_native_or_science=None,whole_INPUT_native_RSS_science_qualified=False)
            f.write((json.dumps(m,indent=2,allow_nan=False)+'\n').encode())
        if view(F,('MANIFEST.json',))!=v:raise ValueError('seal changed reviewed Source files or dirs')
        emit(dict(status=m['status'],source_only=True,manifest_pin=pin(F/'MANIFEST.json'),review_pin=pin(F/'REVIEW.json'),members=m['member_count'],files=m['file_count_including_manifest'],directories=m['directory_count'],check_count=30,blockers=[],actual_candidate_or_utility_execution=False))
    elif sys.argv[1]=='postseal':
        m=load(F/'MANIFEST.json');mp=pin(F/'MANIFEST.json');v=view(F,('MANIFEST.json',))
        if m['members']!=v['files'] or m['directories']!=v['directories'] or m['member_count']!=len(v['files']) or m['file_count_including_manifest']!=len(v['files'])+1 or m['directory_count']!=len(v['directories']):raise ValueError('complete Source fullEOF7ID namespace postseal mismatch')
        w=load(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json');t=w['terminal_tool_return'];o=strict(t['output'])
        if not(w['closed'] is True and w['observed_terminal'] is True and type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t and o['manifest_pin']==mp and o['review_pin']==pin(F/'REVIEW.json') and o['check_count']==30):raise ValueError('actual genuine seal tool coupling')
        proof=dict(schema='INDEPENDENT_V25_COMPLETE_FINITE_UTILITY_SOURCE_FULL_POSTSEAL_VERIFICATION_V1',source_only=True,manifest_pin=mp,review_pin=pin(F/'REVIEW.json'),actual_Source_seal_tool_truth_pin=pin(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),members=m['member_count'],files=m['file_count_including_manifest'],directories=m['directory_count'],check_count=30,all_checks_unique_typed_true=True,blockers=[],complete_file_and_directory_sets_full_EOF_SHA_size_7ID_unchanged=True,original_utility_Source_and_all463_original_owners_unchanged=True,utility_candidate_binder_helper_guard_API_compile_material_numeric_or_Rootwriter_executed=False,actual_new_PREP_or_BUILD_business_result=None,whole_INPUT_native_RSS_science_qualified=False)
        dest=S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json'
        with dest.open('x') as f:json.dump(proof,f,indent=2,allow_nan=False);f.write('\n')
        if pin(F/'MANIFEST.json')!=mp or view(F,('MANIFEST.json',))!=v:raise ValueError('postseal mutated sealed Source')
        emit(dict(status='FULL_SOURCE_POSTSEAL_VERIFIED_ONLY',source_only=True,manifest_pin=mp,review_pin=pin(F/'REVIEW.json'),verification_pin=pin(dest),members=m['member_count'],files=m['file_count_including_manifest'],directories=m['directory_count'],check_count=30,blockers=[],actual_candidate_or_utility_execution=False))
    else:raise ValueError('explicit one seal or postseal')
if __name__=='__main__':main()
