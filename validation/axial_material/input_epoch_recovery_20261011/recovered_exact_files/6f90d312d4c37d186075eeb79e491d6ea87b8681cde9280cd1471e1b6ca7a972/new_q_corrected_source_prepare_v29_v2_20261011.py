import ast,hashlib,json,os,pathlib,stat,tempfile,time
START=time.monotonic();O=pathlib.Path('/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_wbh7cowp');N=pathlib.Path(tempfile.mkdtemp(prefix='SPOT_INSTALLED6A_NEW_Q_FACTORY_CORRECTED_SOURCE_ONLY_V29_',dir='/private/tmp'))
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=pathlib.Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and not any(q.is_symlink() for q in (p,*p.parents));h=hashlib.sha256();n=0
 with p.open('rb') as f:
  assert ids(os.fstat(f.fileno()))==ids(s)
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
  assert ids(os.fstat(f.fileno()))==ids(s)
 assert ids(p.lstat())==ids(s) and n==s.st_size
 return dict(path=str(p),size_bytes=n,sha256=h.hexdigest(),identity=ids(s))
def write(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 return pin(p)
M=json.loads((O/'FINAL_SOURCE_ONLY_MANIFEST.json').read_bytes());A=pathlib.Path('/private/tmp/new_q_contract_independent_audit_v29_20261011.json');S=pathlib.Path('/private/tmp/new_q_contract_independent_scope_supplement_v29_20261011.json');AD=json.loads(A.read_bytes());SD=json.loads(S.read_bytes());assert len(AD['all_verified_inputs'])==209 and AD['all_checks_typed_true'] is True;assert SD['new_Q_Source_package_complete_root']['complete_regular_bytes']==459468
for r in AD['all_verified_inputs']:assert pin(r['path'])==r
for r in SD['new_Q_Source_package_complete_root']['files']:assert pin(r['path'])==r
W=(O/'WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py').read_text();F=(O/'UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py').read_text();assert pin(O/'WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py')==M['Q_writer_Source'];assert pin(O/'UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py')==M['UNREADY_factory_Source']
AUDIT_PINS=[pin(A),pin(S)];newnames=['WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py','UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py','CORRECTED_SOURCE_WHOLE_INVERSE_AND_SCHEMA_PROOF.json','FINAL_CORRECTED_SOURCE_ONLY_MANIFEST.json'];oldnames=sorted(SD['new_Q_Source_package_complete_root']['names'])
addition='''
# A new Source family is added without altering the original resource prefix.
_SOURCE_ROOTS = [Path(OLD_SOURCE_ROOT), Path(__file__).parent]
_SOURCE_NAMESPACE_BEFORE = None
_PRESERVED_AUDIT_INPUTS = []

def _audit_json_pairs(rows):
    d={}
    for k,v in rows:
        assert k not in d,'duplicate audit JSON key'
        d[k]=v
    return d

def _audit_json_nonfinite(value):
    raise ValueError('nonfinite saved independent review metadata')

def _read_pinned_audit(wanted):
    assert pin(wanted['path'])==wanted
    with Path(wanted['path']).open('rt',encoding='utf8') as f:
        value=json.load(f,object_pairs_hook=_audit_json_pairs,parse_constant=_audit_json_nonfinite)
    assert pin(wanted['path'])==wanted
    return value

def verify_preserved_independent_audit_inputs():
    global _PRESERVED_AUDIT_INPUTS
    first,scope=(_read_pinned_audit(p) for p in _AUDIT_EVIDENCE_PINS)
    assert first['schema']=='SPOT_V29_NEW6A_Q_CONTRACT_INDEPENDENT_SOURCE_ONLY_AUDIT_V1'
    assert first['Source_only'] is True and first['writer_factory_helper_production_Native_or_PS_executed'] is False and first['all_checks_typed_true'] is True
    assert type(first['check_count']) is int and first['check_count']==len(first['checks']) and all(type(c['passed']) is bool and c['passed'] is True for c in first['checks'])
    assert scope['schema']=='SPOT_V29_NEW6A_Q_INDEPENDENT_RESOURCE_SCOPE_SUPPLEMENT_V1' and scope['Source_only'] is True and scope['writer_factory_Native_or_PS_executed'] is False
    assert scope['initial_readonly_audit']==_AUDIT_EVIDENCE_PINS[0]
    assert scope['actual_original_pure_joint_scope']=='Original d19 H/O/C+D/E plus Root publication; pure H/O use original 64MiB protocol archive guard and remain in complete96GiB history'
    rows=first['all_verified_inputs'];assert type(rows) is list and len(rows)==209 and len({r['path'] for r in rows})==209
    for r in rows:
        assert type(r['identity']) is list and len(r['identity'])==7 and all(type(v) is int for v in r['identity'])
        assert pin(r['path'])==r
    old=scope['new_Q_Source_package_complete_root'];assert old['path']==OLD_SOURCE_ROOT and sorted(old['names'])==_OLD_SOURCE_NAMES and len(old['files'])==6 and old['complete_regular_bytes']==459468
    assert ids_old_root()==old['identity']
    for r in old['files']:assert pin(r['path'])==r
    _PRESERVED_AUDIT_INPUTS=rows+_AUDIT_EVIDENCE_PINS

def ids_old_root():
    return identity(Path(OLD_SOURCE_ROOT).lstat())

def complete_Source_namespace(root,expected_names):
    root=Path(root);assert root.is_dir() and not root.is_symlink()
    for p in root.parents:assert not p.is_symlink()
    before=identity(root.lstat());paths=sorted(root.rglob('*'),key=str)
    assert sorted(p.name for p in root.iterdir())==sorted(expected_names)
    directories=[dict(path=str(root),identity=before)];files=[]
    for p in paths:
        s=p.lstat();assert not stat.S_ISLNK(s.st_mode)
        if stat.S_ISDIR(s.st_mode):directories.append(dict(path=str(p),identity=identity(s)))
        else:assert stat.S_ISREG(s.st_mode) and s.st_nlink==1;files.append(pin(p))
    assert paths==sorted(root.rglob('*'),key=str) and identity(root.lstat())==before
    for r in directories:assert identity(Path(r['path']).lstat())==r['identity']
    return dict(root=str(root),directories=directories,files=files,regular_bytes=sum(r['size_bytes'] for r in files))

def _complete_new_Q_joint_inode_once():
    roots=[H,O,C,out,AH,AO,AS,*_SOURCE_ROOTS]
    roots += [Path(min(record['directories'],key=lambda p:len(Path(p).parts))) for record in t['current_complete_D_E_freeze'].values()]
    seen=set();total=0;root_records=[]
    for root in roots:
        if not root.exists():assert not root.is_symlink();continue
        assert root.is_dir() and not root.is_symlink()
        paths=sorted(root.rglob('*'),key=str);before=identity(root.lstat());root_bytes=0
        for p in paths:
            s=p.lstat();assert not stat.S_ISLNK(s.st_mode)
            if stat.S_ISDIR(s.st_mode):continue
            assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
            key=(s.st_dev,s.st_ino)
            if key not in seen:seen.add(key);total+=s.st_size;root_bytes+=s.st_size
        assert paths==sorted(root.rglob('*'),key=str) and identity(root.lstat())==before
        root_records.append(dict(path=str(root),identity=before,new_unique_regular_bytes=root_bytes))
    return total,root_records

def account_complete_new_Q(reserve):
    global _SOURCE_NAMESPACE_BEFORE
    assert type(reserve) is int and reserve>=0
    original=account(reserve)
    namespaces=[complete_Source_namespace(_SOURCE_ROOTS[0],_OLD_SOURCE_NAMES),complete_Source_namespace(_SOURCE_ROOTS[1],_NEW_SOURCE_NAMES)]
    if _SOURCE_NAMESPACE_BEFORE is None:_SOURCE_NAMESPACE_BEFORE=namespaces
    else:assert namespaces==_SOURCE_NAMESPACE_BEFORE,'whole original and new Source namespace changed'
    complete,roots=_complete_new_Q_joint_inode_once()
    assert complete>=original['joint_bytes'] and complete+reserve<2*2**30
    frees={str(root):int(os.statvfs(root).f_bavail)*int(os.statvfs(root).f_frsize) for root in _SOURCE_ROOTS}
    assert min(frees.values())-reserve>=8*2**30
    assert time.monotonic()-started<600
    for r in _PRESERVED_AUDIT_INPUTS:assert pin(r['path'])==r
    return dict(original_resource_return=original,complete_new_Q_joint_bytes=complete,additional_unique_Source_bytes=complete-original['joint_bytes'],reserved_bytes=reserve,complete_joint_cap_bytes=2*2**30,complete_joint_roots_inode_once=roots,complete_original_and_new_Source_namespaces=namespaces,tmp_disk_free_bytes=frees,min_free_bytes=8*2**30,reused_closed_protocol_scope='Original v27 and v28 protocol64MiB controls remain complete historical inputs under original96GiB history; no37k-canonical fresh2GiB substitution',original_five_guards_and_DE_preserved=True)

def complete_Q_input_pins(fixed,extra):
    rows={}
    for r in fixed+extra+_PRESERVED_AUDIT_INPUTS+[r for ns in _SOURCE_NAMESPACE_BEFORE for r in ns['files']]:
        assert pin(r['path'])==r
        if r['path'] in rows:assert rows[r['path']]==r
        rows[r['path']]=r
    return list(rows.values())
'''
addition='\nOLD_SOURCE_ROOT='+repr(str(O))+'\n_OLD_SOURCE_NAMES='+repr(oldnames)+'\n_NEW_SOURCE_NAMES='+repr(newnames)+'\n_AUDIT_EVIDENCE_PINS='+repr(AUDIT_PINS)+'\n'+addition
changes=[]
def change(a,b):
 global W
 assert W.count(a)==1,(a[:150],W.count(a));W=W.replace(a,b,1);changes.append(dict(before=a,after=b))
anchor='assert len(sys.argv)==1 and Path(sys.executable).resolve()=='
change(anchor,addition+'\nverify_preserved_independent_audit_inputs()\n'+anchor)
change('before=account(64*2**20);checkpoint()','before=account_complete_new_Q(64*2**20);checkpoint()')
change('complete_Root_metadata_EOF7ID_inputs=fixed+[selfpin,CONTRACT_PIN]','complete_Root_metadata_EOF7ID_inputs=complete_Q_input_pins(fixed,[selfpin,CONTRACT_PIN])')
change('after=account(1024*1024);checkpoint()','''after=account_complete_new_Q(1024*1024)
finalcheckpoint=checkpoint()
witness=dict(schema='SPOT_V29_ACTUAL_NEW6A_METADATA_Q_WRITER_COMPLETE_RESOURCE_WITNESS_V1',actual_metadata_Q=qpin,actual_Source_writer=selfpin,metadata_contract_Source=CONTRACT_PIN,resources_before=before,resources_after_Q_before_witness=after,checkpoint_after_Q_before_witness=finalcheckpoint,complete_Root_metadata_EOF7ID_inputs=q['complete_Root_metadata_EOF7ID_inputs'],writer_does_not_PIN_its_future_self_receipt=True,whole_build_qualified=False,whole_INPUT_admitted=False,science_or_BOOT_admitted=False)
with (out/'ACTUAL_NEW6A_Q_COMPLETE_RESOURCE_WITNESS.json').open('x') as f:json.dump(witness,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\\n');f.flush();os.fsync(f.fileno())
witnesspin=pin(out/'ACTUAL_NEW6A_Q_COMPLETE_RESOURCE_WITNESS.json')
assert witnesspin['size_bytes']<1024*1024
final_after_witness=account_complete_new_Q(0)
final_after_witness_checkpoint=checkpoint()''')
oldprint="print(json.dumps(dict(status=q['status'],actual_metadata_Q=qpin,actual_Source_writer=selfpin,metadata_contract_Source=CONTRACT_PIN,new_Q_created=True,whole_build_qualified=False,whole_INPUT_admitted=False,science_or_BOOT_admitted=False)),flush=True)"
newprint="print(json.dumps(dict(status=q['status'],actual_metadata_Q=qpin,actual_Source_writer=selfpin,metadata_contract_Source=CONTRACT_PIN,actual_complete_resource_witness=witnesspin,actual_final_complete_joint_bytes=final_after_witness['complete_new_Q_joint_bytes'],actual_final_history_including_external_DE_bytes=final_after_witness['original_resource_return']['history_including_external_DE_bytes'],actual_final_checkpoint=final_after_witness_checkpoint,new_Q_created=True,whole_build_qualified=False,whole_INPUT_admitted=False,science_or_BOOT_admitted=False)),flush=True)"
change(oldprint,newprint)
wp=write(N/newnames[0],W.encode());oldexp="EXPECTED_NEW6A_Q_WRITER_SOURCE_PIN="+repr(M['Q_writer_Source']);newexp="EXPECTED_NEW6A_Q_WRITER_SOURCE_PIN="+repr(wp);assert F.count(oldexp)==1;F=F.replace(oldexp,newexp,1);fp=write(N/newnames[1],F.encode())
# Full reversals are proven; no generated Source is imported or executed.
r=W
for c in reversed(changes):assert r.count(c['after'])==1;r=r.replace(c['after'],c['before'],1)
assert r.encode()==(O/newnames[0]).read_bytes();assert hashlib.sha256(r.encode()).hexdigest()==M['Q_writer_Source']['sha256']
fi=F.replace(newexp,oldexp,1);assert fi.encode()==(O/newnames[1]).read_bytes();x=fi.replace(M['factory_added_constants'],'',1)
for c in reversed(M['factory_forward_changes']):assert x.count(c['after'])==1;x=x.replace(c['after'],c['before'],1)
assert x.encode()==pathlib.Path(M['actual_original_closed_endpoints']['old_immutable_factory']['path']).read_bytes()
wo=ast.parse((O/newnames[0]).read_bytes());wn=ast.parse(W);fo=ast.parse((O/newnames[1]).read_bytes());fn=ast.parse(F)
def defs(t):return {n.name:ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
dwo,dwn=defs(wo),defs(wn);assert all(dwn[n]==v for n,v in dwo.items());assert defs(fo)==defs(fn)
assert W.count(M['Q_writer_original_prefix_after'])==1
# Strict saved schema paths statically verified from real files only.
expected_ad_fields=['schema','Source_only','writer_factory_helper_production_Native_or_PS_executed','all_checks_typed_true','check_count','checks','all_verified_inputs'];assert all(k in AD for k in expected_ad_fields)
expected_sd_fields=['schema','Source_only','writer_factory_Native_or_PS_executed','initial_readonly_audit','actual_original_pure_joint_scope','new_Q_Source_package_complete_root'];assert all(k in SD for k in expected_sd_fields)
assert not pathlib.Path(M['candidate_Q_future_path']).parent.exists()
P=dict(status='SOURCE_ONLY_CORRECTED_NEW_Q_WRITER_RESOURCE_ACCOUNT_AND_ACTUAL_WITNESS_NO_EXECUTION',original_writer= M['Q_writer_Source'],corrected_writer=wp,writer_whole_inverse_byte_exact=True,writer_whole_inverse_sha256=hashlib.sha256(r.encode()).hexdigest(),writer_forward_changes=changes,all_original_writer_function_and_class_AST_identical=True,added_pure_metadata_functions=sorted(set(dwn)-set(dwo)),original_resource_prefix_whole_bytes_preserved=True,original_resource_prefix_sha256=M['Q_writer_prefix_original_full_inverse_sha256'],uncorrected_factory=M['UNREADY_factory_Source'],corrected_factory=fp,factory_only_changed_assignment='EXPECTED_NEW6A_Q_WRITER_SOURCE_PIN',factory_corrected_assignment_before=oldexp,factory_corrected_assignment_after=newexp,all_uncorrected_factory_function_and_class_AST_identical=True,corrected_factory_original117ec_whole_inverse_byte_exact=True,corrected_factory_original117ec_whole_inverse_sha256=hashlib.sha256(x.encode()).hexdigest(),original_factory_forward_changes=M['factory_forward_changes'],original_factory_added_constants=M['factory_added_constants'],actual_audit_saved_schema_fields_reviewed=True,metadata_contract_Source=M['metadata_contract_Source'],independent_readonly_review_evidence=AUDIT_PINS,complete_original209_audit_inputs=AD['all_verified_inputs'],Source_preparation_only=True,writer_factory_or_Native_executed=False,Q_created=False,whole_INPUT_or_native_BOOT_AAA_ABA_admission=False)
pp=write(N/newnames[2],(json.dumps(P,ensure_ascii=False,indent=2)+'\n').encode())
NEW=dict(status='CORRECTED_NEW6A_METADATA_Q_WRITER_AND_UNREADY_FACTORY_SOURCE_ONLY_PENDING_ROOT_REVIEW',old_source_manifest=pin(O/'FINAL_SOURCE_ONLY_MANIFEST.json'),corrected_writer_Source=wp,corrected_UNREADY_factory_Source=fp,whole_inverse_and_actual_schema_proof=pp,metadata_contract_Source=M['metadata_contract_Source'],independent_source_audit_and_precise_scope_supplement=AUDIT_PINS,old_Source_package_complete_namespace=SD['new_Q_Source_package_complete_root'],new_Source_package_expected_filenames=newnames,complete_original209_audit_inputs=AD['all_verified_inputs'],preserve_original_joint_account_and_prefix_fullbytes=True,new_joint_addition_scope='Original whole joint roots plus complete original sixfile Q Source package and this complete new fourfile corrected Source package, all ordinary no aliases and inode-once; existing v27 protocol/reusedRootclosed metadata remain original history96/protocol64',account_complete_new_Q_actual_before_after_calls=3,actual_Q_resources_before_in_Q=True,future_actual_Q_resource_witness_output=str(pathlib.Path(M['candidate_Q_future_path']).parent/'ACTUAL_NEW6A_Q_COMPLETE_RESOURCE_WITNESS.json'),actual_after_Q_and_after_witness_checkpoint_saved_or_stdout_bound=True,old_candidate_Q_output_path=M['candidate_Q_future_path'],actual_Q_pin=None,actual_Q_writer_closed_return=None,future_new6a_Q_pin_and_external_postclose_binding_still_None=True,factory_original117ec_complete_inverse=True,factory_all_original_functions_and_classes_AST_held=True,Source_preparation_only=True,writer_factory_or_Native_executed=False,Q_created=False,whole_522_to_512_memory_pass=False,science_or_BOOT_admitted=False,preparation_Source=pin(__file__),elapsed_seconds=time.monotonic()-START)
mp=write(N/newnames[3],(json.dumps(NEW,ensure_ascii=False,indent=2)+'\n').encode());assert sorted(p.name for p in N.iterdir())==sorted(newnames)
for r in AD['all_verified_inputs']:assert pin(r['path'])==r
for r in SD['new_Q_Source_package_complete_root']['files']:assert pin(r['path'])==r
print(json.dumps(dict(Source_root=str(N),Source_only=True,writer=wp,factory=fp,inverse_proof=pp,manifest=mp,files=len(newnames),Source_bytes=sum(p.lstat().st_size for p in N.iterdir()),writer_factory_or_Native_executed=False,Q_created=False)))
