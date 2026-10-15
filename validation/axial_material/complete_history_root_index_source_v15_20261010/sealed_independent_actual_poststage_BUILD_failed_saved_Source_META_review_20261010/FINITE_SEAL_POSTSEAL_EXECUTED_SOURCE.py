"""Finite Source/small META seal only. No project code or physical payload read."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
F=Path('/private/tmp/axmat_V25_actual_poststage_BUILD_saved_Source_META_independent_j7jg4y4k')
S=Path(str(F)+'_seal_receipt')
def identity(p):
    s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);i=identity(p);assert stat.S_ISREG(i[2]) and i[3]==1 and not p.is_symlink()
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    assert identity(p)==i
    return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def read(p):return json.loads(Path(p).read_text())
def view(root):
    fs={};ds={'.':identity(root)}
    for p in sorted(root.rglob('*'),key=lambda p:str(p.relative_to(root))):
        i=identity(p);r=str(p.relative_to(root));assert not stat.S_ISLNK(i[2])
        if stat.S_ISDIR(i[2]):ds[r]=i
        else:assert stat.S_ISREG(i[2]);fs[r]=pin(p)
    assert all(identity(root/r)==i for r,i in ds.items())
    return fs,ds
def write(p,v):
    with p.open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
assert sys.argv[1:] in (['seal'],['postseal'])
r=read(F/'REVIEW.json')
assert r['schema']=='INDEPENDENT_V25_ACTUAL_COMPLETE_BUILD_SAVED_SOURCE_META_REVIEW_V1' and r['status']=='PASS_ACTUAL_FAILED_BUILD_EVIDENCE_ONLY'
assert r['source_only'] is True and r['all_checks_typed_true'] is True and r['blockers']==[]
assert r['check_count']==13==len(r['checks']) and len({q['id'] for q in r['checks']})==13 and all(type(q['passed']) is bool and q['passed'] is True for q in r['checks'])
assert r['actual_Root_terminal_chunk']=='251fd3' and r['actual_metadata_writer_terminal_chunk']=='b0681b' and r['actual_Root_exit_code']==1 and r['actual_metadata_writer_exit_code']==0
assert all(r[k] is False for k in ('whole_combined_build_qualified','whole_combined_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','goal_complete','physical_graph_trace_gzip_binary_material_DB_payload_read','candidate_binder_helper_guard_API_compile_material_numeric_executed'))
for q in r['all_complete_EOF_Source_small_META_pins']:assert pin(q['path'])==q
assert r['historical_E2_full_directory_identity_available'] is False and r['historical_E2_full_directory_identity'] is None
assert len(r['historical_E2_complete_file_pins'])==2 and len(r['actual_E5_before_manifest_summary_append_view']['files'])==5 and len(r['actual_current_E8_complete_view']['files'])==8
e=r['actual_current_E8_complete_view']
assert all(identity(Path(e['root'])/n)==i for n,i in e['directories'].items()) and all(pin(q['path'])==q for q in e['files'].values())
if sys.argv[1]=='seal':
    assert not os.path.lexists(F/'MANIFEST.json') and not os.path.lexists(S)
    (F/'FINITE_SEAL_POSTSEAL_EXECUTED_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    fs,ds=view(F);m=dict(schema='INDEPENDENT_ACTUAL_FAILED_BUILD_SAVED_SOURCE_META_FINITE_PACKAGE_MANIFEST_V1',source_only=True,member_count=len(fs),members=fs,directories=ds,no_large_parent_history_or_physical_payload_copied=True,candidate_guard_API_build_native_numeric_executed=False,new_business_or_science_qualified=False)
    write(F/'MANIFEST.json',m);nowfs,nowds=view(F);m['directories']=nowds
    with (F/'MANIFEST.json').open('w') as f:json.dump(m,f,indent=2,allow_nan=False);f.write('\n')
    nowfs,nowds=view(F);assert nowds==m['directories'] and set(nowfs)==set(fs)|{'MANIFEST.json'} and all(nowfs[n]==q for n,q in fs.items())
    S.mkdir();print(json.dumps(dict(manifest_pin=pin(F/'MANIFEST.json'),review_pin=pin(F/'REVIEW.json'),source_only=True,status=r['status'],check_count=13,complete_file_count=len(nowfs),complete_directory_count_including_root=len(nowds),actual_Root_BUILD_summary_pin=r['actual_Root_BUILD_summary_pin'],actual_Root_BUILD_terminal_pin=r['actual_Root_BUILD_terminal_pin'],actual_complete_namespace_manifest_pin=r['actual_complete_namespace_manifest_pin']),allow_nan=False))
else:
    m=read(F/'MANIFEST.json');fs,ds=view(F);assert set(fs)==set(m['members'])|{'MANIFEST.json'} and ds==m['directories'] and len(m['members'])==m['member_count'] and all(fs[n]==q for n,q in m['members'].items())
    receipt=read(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json');tr=receipt['terminal_tool_return'];assert receipt['closed'] is True and receipt['observed_terminal'] is True and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr
    stdout=json.loads(tr['output']);assert stdout['manifest_pin']==pin(F/'MANIFEST.json') and stdout['review_pin']==pin(F/'REVIEW.json')
    proof=dict(schema='ACTUAL_FAILED_BUILD_SAVED_SOURCE_META_FULL_POSTSEAL_VERIFICATION_V1',source_only=True,manifest_pin=pin(F/'MANIFEST.json'),review_pin=pin(F/'REVIEW.json'),complete_file_count=len(fs),complete_directory_count_including_root=len(ds),all_member_fullEOF_SHA7ID_and_directory7ID_exact=True,all_checks_unique_typed_true=13,no_package_append_after_seal=True,historical_E2_root7ID_unknown_preserved=True,actual_seal_receipt_pin=pin(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),candidate_guard_API_native_numeric_executed=False,new_business_or_science_qualified=False)
    write(S/'FULL_SOURCE_META_POSTSEAL_VERIFICATION.json',proof)
    print(json.dumps(dict(manifest_pin=pin(F/'MANIFEST.json'),review_pin=pin(F/'REVIEW.json'),verification_pin=pin(S/'FULL_SOURCE_META_POSTSEAL_VERIFICATION.json'),source_only=True,complete_file_count=len(fs),complete_directory_count_including_root=len(ds),all_member_fullEOF_SHA7ID_and_directory7ID_exact=True),allow_nan=False))
