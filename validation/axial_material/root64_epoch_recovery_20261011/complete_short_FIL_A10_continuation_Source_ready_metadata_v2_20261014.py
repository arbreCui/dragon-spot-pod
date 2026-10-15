"""Finish READY for the already-written Source only; do not modify its four existing files."""
import ast,hashlib,json,os
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011');B=R/'current_formal_short_FIL_A10_closed_capture_continuation_source_v1_20261014'
def pin(p):
 p=Path(p);s=p.stat();return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns])
def main():
 p=B/'SOURCE_REVIEW_READY.json'
 if p.exists():raise RuntimeError('READY unique append only')
 host=pin(B/'complete_closed_short_FIL_A10_capture_and_release.py');helper=pin(B/'current_material_prerequisite_admission.py');plan=pin(B/'CONTINUATION_SOURCE_PLAN.json');iv=pin(B/'COMPLETE_SHORT_FIL_A10_CONTINUATION_WHOLE_MAIN_BYTE_INVERSE.json');writer=pin(B/'write_once_closed_A10_continuation_HF_CLI.py')
 for f in [host,helper,writer]:ast.parse(Path(f['path']).read_text())
 inv=json.loads(Path(iv['path']).read_bytes());s=Path(host['path']).read_text()
 for c in reversed(inv['changes']):
  if s.count(c['after'])!=1:raise RuntimeError('exact main byte inverse')
  s=s.replace(c['after'],c['before'],1)
 if s.encode()!=Path(inv['predecessor_source_pin']['path']).read_bytes():raise RuntimeError('whole original producer bytes')
 value=dict(schema='SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_SOURCE_ONLY_READY_V1',host_source_pin=host,helper_source_pin=helper,plan_pin=plan,inverse_pin=iv,writer_source_pin=writer,Source_author_pin=pin(R/'prepare_short_FIL_A10_closed_capture_continuation_source_only_v1_20261014.py'),Source_ready_completion_author_pin=pin(__file__),future_actual_failed_post_pin=None,future_actual_failed_post_tools_pin=None,future_actual_own_HF_pin=None,future_actual_own_CLI_pin=None,Source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)
 with p.open('xb')as f:f.write((json.dumps(value,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
 fd=os.open(B,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='CLOSED_A10_CONTINUATION_CANDIDATE_AND_ONCE_WRITER_SOURCE_ONLY_READY',**value,ready_pin=pin(p))),flush=True)
if __name__=='__main__':main()
