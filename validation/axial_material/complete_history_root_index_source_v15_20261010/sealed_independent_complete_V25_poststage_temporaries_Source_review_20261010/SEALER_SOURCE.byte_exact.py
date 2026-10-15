"""Finite one-use private TMP independent Source report seal / postseal only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

def identity(p):
    s=Path(p).lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    p=Path(p);i=identity(p)
    if not p.is_absolute()or any(q.is_symlink()for q in(p,*p.parents))or not stat.S_ISREG(i[2]):raise ValueError('ordinary regular private Source/META')
    with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    if identity(p)!=i:raise ValueError('member changed during full EOF')
    return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)

def read(p):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d:raise ValueError('duplicate META key')
            d[k]=v
        return d
    def reject(v):raise ValueError('nonfinite JSON')
    return json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=reject)

def snapshot(root):
    files={};dirs={'.':identity(root)}
    for p in sorted(root.rglob('*')):
        i=identity(p);rel=str(p.relative_to(root))
        if stat.S_ISDIR(i[2]):dirs[rel]=i
        elif stat.S_ISREG(i[2]):files[rel]=pin(p)
        else:raise ValueError('ordinary finite peer package only')
    return files,dirs

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--mode',required=True,choices=('seal','postseal'));a=ap.parse_args();root=Path(a.root)
    if not root.is_relative_to(Path('/private/tmp'))or root.is_symlink():raise ValueError('private TMP peer report only')
    r=read(root/'REVIEW.json');tool=read(root/'ACTUAL_REVIEW_TOOL_RETURN.json');t=tool['actual_tool_return']
    if r['schema']!='INDEPENDENT_V25_POSTSTAGE_TEMPORARIES_COMPLETE_SOURCE_REVIEW_V1'or r['status']!='PASS_COMPLETE_POSTSTAGE_TEMPORARIES_SOURCE_ONLY_UNREADY_NO_EXECUTION'or r['source_only']is not True or r['all_checks_typed_true']is not True or r['blockers']!=[]:raise ValueError('complete independent Source-only PASS required')
    if type(r['check_count'])is not int or r['check_count']!=len(r['checks'])or any(type(q['passed'])is not bool or q['passed']is not True for q in r['checks']):raise ValueError('all exact typedTrue checks')
    if tool['closed']is not True or tool['observed_terminal']is not True or type(t['exit_code'])is not int or t['exit_code']!=0 or 'session_id'in t:raise ValueError('real actual review terminal')
    actual=json.loads(t['output'])
    if actual['review_pin']!=pin(root/'REVIEW.json')or actual['check_count']!=len(r['checks'])or actual['blockers']!=[]:raise ValueError('actual review output coupling')
    if any(r[k]is not False for k in('whole_build_qualified','whole_combined_INPUT_admitted','native_RSS_qualified','native_transport_executed','physical_balance_qualified','AAA_accuracy_qualified','ABA_admitted','goal_complete')):raise ValueError('no business or science qualification')
    mf=root/'MANIFEST.json'
    if a.mode=='seal':
        if os.path.lexists(mf):raise ValueError('fresh exclusive peer seal only')
        mf.touch(exist_ok=False);files,dirs=snapshot(root);members={k:v for k,v in files.items()if k!='MANIFEST.json'}
        value=dict(schema='INDEPENDENT_V25_POSTSTAGE_TEMPORARIES_COMPLETE_SOURCE_REVIEW_PACKAGE_MANIFEST_V1',source_only=True,members=members,directories=dirs,member_count=len(members),complete_member_bytes=sum(q['size_bytes']for q in members.values()),review_pin=pin(root/'REVIEW.json'),qualified_complete_Source_manifest_pin=r['qualified_complete_Source_manifest_pin'],candidate_binder_helper_guard_API_compile_native_material_numeric_executed=False,whole_build_INPUT_native_science_qualified=False)
        mf.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
    v=read(mf);files,dirs=snapshot(root)
    if dirs!=v['directories']or set(files)!=set(v['members'])|{'MANIFEST.json'}or any(files[k]!=q for k,q in v['members'].items()):raise ValueError('complete sealed peer changed')
    if pin(root/'REVIEW.json')!=v['review_pin']or v['member_count']!=len(v['members']):raise ValueError('complete Source peer coupling changed')
    print(json.dumps(dict(status='PASS_COMPLETE_POSTSTAGE_SOURCE_PEER_SEAL'if a.mode=='seal'else'PASS_COMPLETE_POSTSTAGE_SOURCE_PEER_POSTSEAL',source_only=True,manifest_pin=pin(mf),review_pin=pin(root/'REVIEW.json'),qualified_complete_Source_manifest_pin=r['qualified_complete_Source_manifest_pin'],complete_file_count=len(files),complete_subdirectory_count=len(dirs)-1,check_count=r['check_count'],candidate_binder_helper_guard_API_compile_native_material_numeric_executed=False,whole_build_INPUT_native_science_qualified=False),allow_nan=False))

if __name__=='__main__':main()
