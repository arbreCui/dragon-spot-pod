"""Only immutable metadata correction; all runtime Sources remain current v4 bytes."""
import ast,base64,copy,hashlib,json,os
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
B=R/'current_material_evidence_empty_root_cumulative_twelve_roots_source_v4_20261014'
def pin(p):
 p=Path(p);s=p.stat();b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns])
def write(p,v):
 b=v if isinstance(v,bytes)else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 return pin(p)
def read(p):return json.loads(p.read_bytes())
def main():
 old_iv=B/'COMPLETE_V2_TO_V4_PRIOR_AGGREGATE_CUMULATIVE_RESOURCE_SOURCE_BYTE_INVERSE.json'
 old_plan=B/'EMPTY_ROOT_CUMULATIVE_TWELVE_ROOTS_SOURCE_PLAN.json';old_ready=B/'SOURCE_REVIEW_READY.json'
 old_writer=B/'write_once_empty_root_cumulative_twelve_roots_evidence_SF_HF_dynamic.py'
 iv=read(old_iv);plan=read(old_plan);ready=read(old_ready);old=old_writer.read_text();new=old
 edits=[("ready=read(pin(BASE/'SOURCE_REVIEW_READY.json'))","ready=read(pin(BASE/'SOURCE_REVIEW_READY_v2.json'))"),("pin(BASE/'SOURCE_REVIEW_READY.json'),wp]","pin(BASE/'SOURCE_REVIEW_READY_v2.json'),wp]")]
 for a,b in edits:
  if new.count(a)!=1:raise RuntimeError('unique READY metadata Source reference')
  new=new.replace(a,b)
 ast.parse(new)
 status=dict(original="status='EXPLICIT_EMPTY_MACROLIB_ROOT_EVIDENCE_SF_HF_DYNAMIC24_SOURCE_ONLY_PUBLISHED'",candidate="status='EMPTY_ROOT_CUMULATIVE_TWELVE_ROOTS_EVIDENCE_SF_HF_DYNAMIC24_SOURCE_ONLY_PUBLISHED'")
 blocks=iv['writer_exact_original_candidate_blocks']+[status]+[dict(original=a,candidate=b)for a,b in edits]
 restored=new
 for change in reversed(blocks):
  if restored.count(change['candidate'])!=1:raise RuntimeError('unique complete writer inverse block')
  restored=restored.replace(change['candidate'],change['original'])
 origin=base64.b64decode(iv['original_writer_whole_bytes_base64'])
 if restored.encode()!=origin:raise RuntimeError('full five-block writer inverse must restore original v2 writer')
 wp=write(B/'write_once_empty_root_cumulative_twelve_roots_evidence_SF_HF_dynamic_v2.py',new.encode())
 iv.update(writer_exact_original_candidate_blocks=blocks,candidate_writer_whole_bytes_base64=base64.b64encode(new.encode()).decode(),candidate_writer_Source_pin=wp,whole_writer_inverse_byte_equal=True,predecessor_v4_inverse_pin=pin(old_iv),only_previous_missing_status_splice_and_two_immutable_READY_references_corrected=True,all_runtime_source_bytes_unchanged=True)
 ip=write(B/'COMPLETE_V2_TO_V4_PRIOR_AGGREGATE_CUMULATIVE_RESOURCE_SOURCE_BYTE_INVERSE_v2.json',iv)
 plan.update(complete_byte_inverse_pin=ip,predecessor_v4_plan_pin=pin(old_plan),actual_metadata_correction_Source_pin=pin(Path(__file__).absolute()),all_runtime_source_bytes_unchanged=True)
 pp=write(B/'EMPTY_ROOT_CUMULATIVE_TWELVE_ROOTS_SOURCE_PLAN_v2.json',plan)
 ready.update(plan_pin=pp,inverse_pin=ip,writer_source_pin=wp,Source_author_pin=pin(Path(__file__).absolute()),predecessor_v4_READY_pin=pin(old_ready),all_runtime_source_bytes_unchanged=True)
 rp=write(B/'SOURCE_REVIEW_READY_v2.json',ready)
 fd=os.open(B,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='CUMULATIVE12_COMPLETE_WRITER_INVERSE_METADATA_ONLY_READY',Source_author_pin=pin(Path(__file__).absolute()),plan_pin=pp,inverse_pin=ip,ready_pin=rp,writer_source_pin=wp,whole_writer_inverse_byte_equal=True,all_runtime_source_bytes_unchanged=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
