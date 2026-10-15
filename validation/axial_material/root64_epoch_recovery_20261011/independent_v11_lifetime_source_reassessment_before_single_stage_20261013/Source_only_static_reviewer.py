from pathlib import Path
import ast,hashlib,json,os,stat
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';D=REC/'independent_v11_lifetime_source_reassessment_before_single_stage_20261013'
paths=[REC/'aaa_three_plane_streaming_pipeline_source_v11/run_actual_three_plane_pipeline.py',REC/'aaa_three_plane_streaming_pipeline_source_v11/actual_inputs_and_readback.py',REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py',R/'validation/axial_material/snapshot_control_preflight.py',R/'validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py',R/'validation/axial_material/qualify_refined_AAA_layered_full.py']
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(p):
 before=identity(p.lstat());assert stat.S_ISREG(before[2]);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);raw=bytearray()
 try:
  assert identity(os.fstat(fd))==before
  while True:
   b=os.read(fd,65536)
   if not b:break
   raw.extend(b)
  assert identity(os.fstat(fd))==before
 finally:os.close(fd)
 assert identity(p.lstat())==before and len(raw)==before[4]
 return raw.decode(),dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)
sources={};pins=[]
for p in paths:text,pf=read(p);ast.parse(text);sources[str(p)]=text;pins.append(pf)
def fn(text,name):return next(n for n in ast.walk(ast.parse(text))if isinstance(n,ast.FunctionDef)and n.name==name)
host=sources[str(paths[0])];data=sources[str(paths[1])];common=sources[str(paths[2])];parser=sources[str(paths[3])]
record=ast.get_source_segment(common,fn(common,'_record_metadata_reattestation'));assert 'metadata_path=str(path)'in record and 'original_JSON_value_sha256=raw_hash'in record and 'explicit_current_JSON_view_sha256=view_hash'in record
append=next(n for n in ast.walk(fn(common,'_record_metadata_reattestation'))if isinstance(n,ast.Call)and ast.unparse(n.func)=='_METADATA_REATTESTATIONS.append');assert ast.unparse(append.args[0])=='record'
main=fn(host,'main');gc_node=next(n for n in main.body if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and ast.unparse(n.value.func)=='gc.collect')
runtime_calls=[dict(name=ast.unparse(n.func),line=n.lineno)for n in ast.walk(main)if isinstance(n,ast.Call)and n.lineno>gc_node.lineno and ast.unparse(n.func)in('c.read_bound_json_current','c.load_json_exact','c.current_metadata_reattestation_provenance','data.tree_digest','data.packed_readback','data.transfer_readback')]
assert not any(x['name']in('c.read_bound_json_current','c.load_json_exact')for x in runtime_calls)
tree=fn(data,'tree_digest');assert [n.name for n in tree.body if isinstance(n,ast.FunctionDef)]==['directory','entry']
bounded=next(n for n in ast.parse(data).body if isinstance(n,ast.ClassDef)and n.name=='BoundedFDBytes');bounded_body=ast.get_source_segment(data,bounded);assert 'self.fd=fd;self.size=size;self.largest_read=0'in bounded_body and 'MAX_READ_BYTES'in bounded_body
xsm=next(n for n in ast.parse(parser).body if isinstance(n,ast.ClassDef)and n.name=='_XSM');xbody=ast.get_source_segment(parser,xsm);assert 'self.data = data'in xbody and 'self.root = self.directory'in xbody and 'capacity <= 30'in xbody
proof=dict(schema='STATIC_V11_LIFETIME_SOURCE_REASSESSMENT_BEFORE_ONE_ACTUAL_DIAGNOSTIC_STAGE_V1',status='READONLY_STATIC_REASSESSMENT_NO_NEW_SUPPORTED_FIX_POINT',input_whole_EOF_Source_fullpins=pins,all_Source_whole_AST_read=True,metadata_record_complete_body=record,metadata_view_complete_body=ast.get_source_segment(common,fn(common,'bound_json_current_view')),tree_digest_complete_body=ast.get_source_segment(data,tree),BoundedFDBytes_complete_body=bounded_body,original_XSM_complete_class_body=xbody,actual_original_v11_admission_gc_line=gc_node.lineno,runtime_pertinent_calls=runtime_calls,conclusions=[
 'Current metadata reattestation global stores compact physical pins, hashes and flags; it does not retain raw/view JSON objects. Recursive visit captures its own function and catalog mapping table; all bound loads occur before the explicit admission gc.collect, with no runtime repeated bound-json load per stage.',
 'Runtime main retains original fixed/owned pins, plan, host freeze, direct binding, link caches and proof/case/scratch/release/records collections. Those should be retained in the upcoming single-stage fixture for a closer baseline than simplified earlier fixtures.',
 'Tree digest has mutually recursive closure functions directory and entry, retaining a streaming _XSM/root directory and hash/counts until collection. Its data is bounded fd/pread state rather than whole-file bytes or mmap; directory capacity is at most30. Tree calls occur at pack and transfer phases, not each operator refusal.',
 'Source structure alone does not establish a hundreds-of-MiB leak or authorize a new math/guard/cap/Source fix. Existing actual immutable v11 remains failed; one future replay stage may only be a diagnostic, never original full50 engineering success.'
],candidate_imported=False,guard_or_Dragon_or_fixture_executed=False,cleanup_executed=False,original_Source_modified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
D.mkdir()
with(D/'REVIEW.json').open('x')as f:json.dump(proof,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
text,pf=read(D/'REVIEW.json');print(json.dumps(dict(status=proof['status'],review_pin=pf,full_Source_files=len(pins),runtime_pertinent_calls=runtime_calls)))
