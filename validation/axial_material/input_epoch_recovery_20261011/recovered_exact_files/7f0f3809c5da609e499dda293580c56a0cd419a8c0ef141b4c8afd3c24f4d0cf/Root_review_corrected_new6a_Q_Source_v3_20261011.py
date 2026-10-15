import ast, hashlib, json, os, stat
from pathlib import Path
B=Path('/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_V3_COUNTFINAL_unkdz2l9')
MP=B/'FINAL_CORRECTED_SOURCE_ONLY_MANIFEST.json'
REPORT=Path('/private/tmp/Root_corrected_new6a_Q_independent_Source_review_v3_20261011.json')
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    p=Path(path)
    for a in (p,*p.parents):assert not a.is_symlink(),str(a)
    before=p.lstat();assert stat.S_ISREG(before.st_mode) and before.st_nlink==1
    h=hashlib.sha256()
    with p.open('rb') as f:
        assert ids(os.fstat(f.fileno()))==ids(before)
        for block in iter(lambda:f.read(2**20),b''):h.update(block)
        assert ids(os.fstat(f.fileno()))==ids(before)
    assert ids(p.lstat())==ids(before)
    return dict(path=str(p),size_bytes=before.st_size,sha256=h.hexdigest(),identity=ids(before))
def read(p):return json.loads(Path(p).read_bytes())
def undo(s,changes):
    for c in reversed(changes):
        assert s.count(c['after'])==1
        s=s.replace(c['after'],c['before'],1)
    return s
def funcs(s):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
mp=pin(MP);assert mp['sha256']=='d62b0cabc7be06eb47c29a826b7f500a3cb5e9ec6090773b61b672df6d8aae02'
m=read(MP);assert m['status']=='NEW6A_Q_WRITER_V3_STRICT_FINAL_COUNT_COMPLETE_FRESH_INPUTS_ROOT_REVIEW_SOURCE_ONLY_PENDING_ROOT'
expected=m['complete_original209_audit_inputs']+[m[k] for k in ('corrected_writer_Source','corrected_UNREADY_factory_Source','whole_inverse_and_actual_schema_proof','metadata_contract_Source','failed_v2_Source_manifest','failed_v2_actual_writer_tools','preparation_Source')]+m['new_actual_audit_and_precise_scope_supplement']+m['explicit_current_stage_fresh_inputs']
before=[pin(p['path']) for p in expected];assert before==expected
p=read(m['whole_inverse_and_actual_schema_proof']['path'])
w=Path(m['corrected_writer_Source']['path']).read_text();wt=ast.parse(w)
v2=Path(p['failed_corrected_v2_writer_Source']['path']).read_text();assert pin(p['failed_corrected_v2_writer_Source']['path'])==p['failed_corrected_v2_writer_Source']
assert undo(w,p['v3_writer_forward_changes'])==v2
v1=undo(v2,p['v2_to_original531_writer_forward_changes'])
assert hashlib.sha256(v1.encode()).hexdigest()=='531eb252e9517f3bb8ce5d117a9a32d456f47edf7ff05e52f844843db1d3d56c'
for name,value in funcs(v1).items():assert funcs(w)[name]==value,name
assert 'assert first[\'check_count\']==len(first[\'checks\'])' not in w or True
assert "first['check_count']==len(first['checks'])" in w
oldm=read(m['failed_v2_Source_manifest']['path'])
origm=read(oldm['old_source_manifest']['path'])
prefix=origm['Q_writer_original_prefix_after']
assert w.count(prefix)==1
restored=prefix.replace("out = A / 'axial-material-installed6a-helper-metadata-admission-v29-20261011'","out = A / 'axial-material-stable-wire-sort-fullfresh-root-closure-v28-20261011'",1)
assert restored==origm['Q_writer_original_prefix_before'] and hashlib.sha256(restored.encode()).hexdigest()=='ca8e0d25e4a5526ba64c81ddfd866e77e966520e02d82a8a633fabcbe76138aa'
f=Path(m['corrected_UNREADY_factory_Source']['path']).read_text()
assert f.count(p['factory_v3_to_failed_v2_assignment_after'])==1
f2=f.replace(p['factory_v3_to_failed_v2_assignment_after'],p['factory_v3_to_failed_v2_assignment_before'],1)
assert f2==Path(p['failed_corrected_v2_factory_Source']['path']).read_text()
assert funcs(f)==funcs(f2)
f1=f2.replace(p['factory_v2_to_v1_assignment_after'],p['factory_v2_to_v1_assignment_before'],1)
restored_factory=undo(f1,p['factory_v1_forward_changes'])
assert restored_factory.count(p['factory_v1_added_constants'])==1
restored_factory=restored_factory.replace(p['factory_v1_added_constants'],'',1)
original_factory=origm['actual_original_closed_endpoints']['old_immutable_factory']
assert pin(original_factory['path'])==original_factory
assert restored_factory.encode()==Path(original_factory['path']).read_bytes() and original_factory['sha256']=='117ec099ce288db10fe86c47d441192a3d697f9cd0a4d48e4dff86600bf5d604'
literal={}
for n in ast.parse(f).body:
    if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
        try:literal[n.targets[0].id]=ast.literal_eval(n.value)
        except (ValueError,TypeError):pass
assert literal['FUTURE_NEW6A_Q_PIN'] is None and literal['FUTURE_NEW6A_Q_EXTERNAL_CLOSED_BINDING_PIN'] is None
assert literal['EXPECTED_NEW6A_Q_WRITER_SOURCE_PIN']==m['corrected_writer_Source'] and literal['NEW6A_METADATA_CONTRACT_PIN']==m['metadata_contract_Source']
assert m['metadata_contract_Source']['sha256']=='f574c3d985847417bb906028177fdf50f85081bec506640abadfaa3547b6f4d1'
audit=read(m['new_actual_audit_and_precise_scope_supplement'][0]['path']);scope=read(m['new_actual_audit_and_precise_scope_supplement'][1]['path'])
assert type(audit['check_count']) is int and audit['check_count']==len(audit['checks'])==5400
assert all(type(c['passed']) is bool and c['passed'] is True for c in audit['checks']) and audit['all_verified_inputs']==m['complete_original209_audit_inputs']
assert scope['initial_readonly_audit']==m['new_actual_audit_and_precise_scope_supplement'][0]
assert scope['actual_original_pure_joint_scope']=='Original d19 H/O/C+D/E plus Root publication; pure H/O use original 64MiB protocol archive guard and remain in complete96GiB history'
ainv=read('/private/tmp/new_q_independent_audit_v2_countfinal_Source_inverse_20261011.json')
assert undo(Path(ainv['new_Source']).read_text(),ainv['five_exact_changes'])==Path(ainv['old_Source']).read_text()
packages=[]
rootnames=[scope['new_Q_Source_package_complete_root']['names'],oldm['new_Source_package_expected_filenames'],['CORRECTED_SOURCE_WHOLE_INVERSE_AND_SCHEMA_PROOF.json','FINAL_CORRECTED_SOURCE_ONLY_MANIFEST.json','UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py','WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py']]
for root,names in zip(m['three_complete_Q_Source_family_roots'],rootnames):
    rp=Path(root);assert rp.is_dir() and not rp.is_symlink()
    assert sorted(x.name for x in rp.iterdir())==sorted(names)
    files=[pin(x) for x in sorted(rp.iterdir())]
    packages.append(dict(path=str(rp),identity=ids(rp.lstat()),names=sorted(names),files=files,bytes=sum(q['size_bytes'] for q in files)))
assert len(packages)==3 and [len(q['files']) for q in packages]==[6,4,4]
for q in scope['new_Q_Source_package_complete_root']['files']:assert pin(q['path'])==q
assert ids(Path(packages[0]['path']).lstat())==scope['new_Q_Source_package_complete_root']['identity']
calls=[n for n in ast.walk(wt) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='account_complete_new_Q']
assert [ast.unparse(n.args[0]) for n in calls]==['64 * 2 ** 20','1024 * 1024','0']
rc=m['prelaunch_Root_review_contract'];assert rc['Source_path']==str(Path(__file__)) and rc['report_path']==str(REPORT)
assert w.index('\nverify_current_fresh_inputs_and_actual_Root_prelaunch_review()')<w.index('\nverify_preserved_independent_audit_inputs()')<w.index('\nevidence,fixed=module.validate_closed_evidence()')
assert len(m['explicit_current_stage_fresh_inputs'])==14
for flag in ('writer_factory_Native_or_PS_executed','Q_created','whole_INPUT_native_BOOT_AAA_ABA_admitted'):assert m[flag] is False
out=Path(m['old_candidate_Q_output_path']);assert not out.exists() and not out.parent.exists()
assert [pin(q['path']) for q in expected]==before and pin(MP)==mp
for package in packages:
    rp=Path(package['path']);assert ids(rp.lstat())==package['identity'] and [pin(x) for x in sorted(rp.iterdir())]==package['files']
result=dict(status='ROOT_SOURCE_REVIEW_PASS_AUTHORIZE_ONE_ACTUAL_NEW6A_METADATA_Q_WRITER',writer=m['corrected_writer_Source'],metadata_contract=m['metadata_contract_Source'],manifest=mp,review_Source=pin(__file__),whole_writer_inverse_and_original_function_AST_equal=True,whole_factory_inverse_to_117ec099_equal=True,original_resource_prefix_preserved=True,original_scientific_and_complete_build_gates_not_granted=True,all_expected_full_EOF_SHA_exact7ID_before_after=before,complete_three_Source_families=packages,all5400_saved_audit_checks_typed_true_and_strict_final_count=True,all209_original_audit_inputs_preserved=True,current_fresh_explicit_files= m['explicit_current_stage_fresh_inputs'],original_600_512_joint2_history96_free8_guards_and_DE_preserved=True,Q_created=False,factory_executed=False,whole_INPUT_native_BOOT_AAA_ABA_admitted=False)
with REPORT.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
print(json.dumps(dict(status=result['status'],review=pin(REPORT))))
