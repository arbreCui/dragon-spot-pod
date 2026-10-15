"""Seal only the review Source/small META package; never invoke project code."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

F=Path('/private/tmp/axmat_V25_poststage_actual_bound_BUILD_Source_independent_86b8ry0u')
S=Path(str(F)+'_seal_receipt')

def identity(p):
    s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    p=Path(p);i=identity(p)
    assert p.is_absolute() and stat.S_ISREG(i[2]) and i[3]==1 and not p.is_symlink()
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    assert identity(p)==i
    return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)

def read(p):return json.loads(Path(p).read_text())

def inv(root):
    files={};dirs={'.':identity(root)}
    for p in sorted(root.rglob('*'),key=lambda p:str(p.relative_to(root))):
        i=identity(p);r=str(p.relative_to(root));assert not stat.S_ISLNK(i[2])
        if stat.S_ISDIR(i[2]):dirs[r]=i
        else:assert stat.S_ISREG(i[2]);files[r]=pin(p)
    assert all(identity(root/r)==i for r,i in dirs.items())
    return files,dirs

def write_new(p,v):
    with p.open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')

assert sys.argv[1:] in (['seal'],['postseal'])
report=read(F/'REVIEW.json')
assert report['source_only'] is True and report['all_checks_typed_true'] is True and report['blockers']==[]
assert report['check_count']==19==len(report['checks']) and len({q['id'] for q in report['checks']})==19
assert all(type(q['passed']) is bool and q['passed'] is True for q in report['checks'])
assert report['schema']=='INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_POSTCLOSE_META_SOURCE_REVIEW_V1' and report['status']=='PASS_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY'
assert report['candidate_binder_utility_helper_guard_API_compiler_numeric_executed'] is False
# Only already independently read Source/small META files are reread to EOF.
for q in report['independent_complete_EOF_Source_small_META_pins']:assert pin(q['path'])==q
for q in report['details']['original_complete340_Q_proof_owners_exact_hash_current7ID']['current_exact7ID_pins'].values():assert identity(q['path'])==q['identity']
for q in report['details']['new_PREP_five_outputs_original_EOF_claims_current7ID_only']['Root_complete_EOF_output_pins'].values():assert identity(q['path'])==q['identity']
for root,key in [('complete_actual_bound_package','manifest'),('qualified_complete_mother_Source_package','mother')]:
    q=report['details'][root][key];assert pin(q['path'])==q
if sys.argv[1]=='seal':
    assert not os.path.lexists(F/'MANIFEST.json') and not os.path.lexists(S)
    (F/'FINITE_SEAL_POSTSEAL_EXECUTED_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    files,dirs=inv(F)
    m=dict(schema='INDEPENDENT_V25_ACTUAL_BOUND_BUILD_FINITE_SOURCE_REVIEW_PACKAGE_MANIFEST_V1',source_only=True,member_count=len(files),members=files,directories=dirs,whole_original_reviewed_Source_copies_retained=True,candidate_guard_API_compile_native_numeric_executed=False,new_business_or_science_qualified=False)
    write_new(F/'MANIFEST.json',m)
    nowfiles,nowdirs=inv(F)
    # Adding MANIFEST changes only the root directory. Record its actual final7ID.
    m['directories']=nowdirs
    with (F/'MANIFEST.json').open('w') as f:json.dump(m,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
    nowfiles,nowdirs=inv(F)
    assert nowdirs==m['directories'] and set(nowfiles)==set(files)|{'MANIFEST.json'}
    assert all(nowfiles[r]==q for r,q in files.items())
    S.mkdir()
    print(json.dumps(dict(manifest_pin=pin(F/'MANIFEST.json'),review_pin=pin(F/'REVIEW.json'),source_only=True,check_count=19,complete_file_count=len(nowfiles),complete_directory_count_including_root=len(nowdirs),actual_bound_Source_manifest_pin=report['qualified_actual_bound_Source_manifest_pin'],actual_bound_build_host_pin=report['actual_bound_build_host_pin'],actual_postclose_META_writer_pin=report['actual_postclose_META_writer_pin'],actual_Root_Source_binding_tool_receipt_pin=report['actual_Root_Source_binding_tool_receipt_pin']),allow_nan=False))
else:
    m=read(F/'MANIFEST.json');files,dirs=inv(F)
    assert m['member_count']==len(m['members']) and set(files)==set(m['members'])|{'MANIFEST.json'} and dirs==m['directories']
    assert all(files[r]==q for r,q in m['members'].items())
    receipt=read(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json');tr=receipt['terminal_tool_return']
    assert receipt['closed'] is True and receipt['observed_terminal'] is True and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr
    sealed=json.loads(tr['output'])
    assert sealed['manifest_pin']==pin(F/'MANIFEST.json') and sealed['review_pin']==pin(F/'REVIEW.json')
    proof=dict(schema='INDEPENDENT_V25_ACTUAL_BOUND_BUILD_FINITE_FULL_POSTSEAL_VERIFICATION_V1',source_only=True,manifest_pin=pin(F/'MANIFEST.json'),review_pin=pin(F/'REVIEW.json'),complete_file_count=len(files),complete_directory_count_including_root=len(dirs),all_member_fullEOF_SHA7ID_and_dir7ID_exact=True,all_check_count_exact_typed_true=19,no_member_append_after_seal=True,actual_seal_receipt_pin=pin(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),candidate_guard_API_compile_native_numeric_executed=False,new_business_or_science_qualified=False)
    write_new(S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json',proof)
    print(json.dumps(dict(manifest_pin=pin(F/'MANIFEST.json'),review_pin=pin(F/'REVIEW.json'),verification_pin=pin(S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json'),source_only=True,complete_file_count=len(files),complete_directory_count_including_root=len(dirs),all_member_fullEOF_SHA7ID_and_dir7ID_exact=True),allow_nan=False))
