from pathlib import Path
import hashlib,json,os,stat,shutil
P=Path('/private/tmp/axmat_native_actual_BOUND_complete_SOURCE_peer__g2keoz6')
B=Path('/private/tmp/axmat_complete_native_actual_BOUND_SOURCE_ROOT_20261010_503adf')
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1
 with p.open('rb')as f:
  assert identity(os.fstat(f.fileno()))==identity(s);b=f.read();assert len(b)==s.st_size and f.read(1)==b'';assert identity(os.fstat(f.fileno()))==identity(s)
 assert identity(p.lstat())==identity(s)
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=identity(s))
r=json.loads((P/'REVIEW.json').read_bytes());assert r['schema']=='INDEPENDENT_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_REVIEW_V1'and r['status']=='PASS_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_ONLY'and r['source_only']is True and r['all_checks_typed_true']is True and r['blockers']==[]
assert len(r['checks'])==r['check_count']==8133 and all(v['passed']is True for v in r['checks'])and len({v['check']for v in r['checks']})==8133
for k in('actual_bound_Source_manifest_pin','actual_binding_pin','actual_host_pin','actual_checker_pin','actual_Root_binding_tool_receipt_pin'):assert pin(Path(r[k]['path']))==r[k]
tr=json.loads((P/'ACTUAL_BOUND_SOURCE_REVIEW_TOOL_TERMINAL_RETURN.json').read_bytes());assert tr['closed']is True and tr['actual_tool_terminal_return_observed']is True and type(tr['terminal_tool_return']['exit_code'])is int and tr['terminal_tool_return']['exit_code']==0 and 'session_id'not in tr['terminal_tool_return']and tr['review_sha256']==pin(P/'REVIEW.json')['sha256']
shutil.copytree(B,P/'COMPLETE_ACTUAL_BOUND_SOURCE')
meta=P/'COMPLETE_ACTUAL_ROOT_SOURCE_META';meta.mkdir();copies=[]
for k in('actual_Root_request_pin','actual_Root_Source_admission_pin','actual_Root_Source_admission_terminal_pin','actual_failed_BUILD_CLOSED1_pin','actual_complete_archived5741_Source_peer_pin','actual_Root_binding_tool_receipt_pin'):
 v=r[k];o=Path(v['path']);assert pin(o)==v;c=meta/(k+'.json');shutil.copy2(o,c);assert o.read_bytes()==c.read_bytes();copies.append(dict(original_full_pin=v,peer_copy=pin(c)))
m=P/'MANIFEST.json';assert not m.exists();m.write_text('{}\n');members=[dict(relative_path=q.relative_to(P).as_posix(),**pin(q))for q in sorted(P.rglob('*'))if q.is_file()and q!=m];dirs={str(q):identity(q.lstat())for q in[P,*sorted(q for q in P.rglob('*')if q.is_dir())]}
manifest=dict(schema='INDEPENDENT_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_PEER_SEAL_V1',source_only=True,status='SEALED_PASS_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_ONLY',member_count=len(members),member_bytes=sum(v['size_bytes']for v in members),members=members,directories=dirs,independent_report=pin(P/'REVIEW.json'),actual_Source_review_tool=pin(P/'ACTUAL_BOUND_SOURCE_REVIEW_TOOL_TERMINAL_RETURN.json'),all8133_complete_checks_typed_true=True,complete89_actual_bound_Source_files_copied=True,complete_true_Root_Source_META_copies=copies,actual_native_checker_or_guard_or_material_execution=None,whole_build_INPUT_native_RSS_and_science_qualified=False)
m.write_text(json.dumps(manifest,indent=2)+'\n')
for v in members:assert pin(Path(v['path']))=={k:v[k]for k in('path','sha256','size_bytes','identity')}
assert dirs=={str(q):identity(q.lstat())for q in[P,*sorted(q for q in P.rglob('*')if q.is_dir())]}
assert sorted(q.relative_to(B).as_posix()for q in B.rglob('*')if q.is_file())==sorted(q.relative_to(P/'COMPLETE_ACTUAL_BOUND_SOURCE').as_posix()for q in(P/'COMPLETE_ACTUAL_BOUND_SOURCE').rglob('*')if q.is_file())
assert len([q for q in(P/'COMPLETE_ACTUAL_BOUND_SOURCE').rglob('*')if q.is_file()])==89
for key in('actual_bound_Source_manifest_pin','actual_binding_pin','actual_host_pin','actual_checker_pin','actual_Root_binding_tool_receipt_pin'):assert pin(Path(r[key]['path']))==r[key]
print(json.dumps(dict(source_only=True,status=manifest['status'],manifest=pin(m),review=pin(P/'REVIEW.json'),member_count=len(members),all8133_complete_checks_typed_true=True,complete89_bound_Source_and_six_true_Root_META_retained=True,no_candidate_helper_API_guard_reader_or_payload_execution=True),indent=2))
