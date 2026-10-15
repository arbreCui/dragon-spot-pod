"""Only exact loaded-SF/HF publication cardinality and selected metadata revision."""
import ast,copy,hashlib,json,os
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'current_eleven_saved_gendf_actual_cumulative_seventeen_roots_host_source_v11_20261014'
def pin(p):
 p=Path(p);s=p.stat();b=p.read_bytes();ids=lambda z:[z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns]
 if ids(p.stat())!=ids(s):raise RuntimeError('current7')
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))
def write(p,v):
 b=v if type(v)is bytes else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 return pin(p)
ready=json.loads((P/'SOURCE_REVIEW_READY.json').read_bytes())
plan=json.loads(Path(ready['plan_pin']['path']).read_bytes());iv=json.loads(Path(ready['complete_inverse_pin']['path']).read_bytes())
original=Path(ready['writer_source_pin']['path']).read_text();candidate=original
changes=[('counts!=[2,2,2]','counts!=[2,3,2]'),('exact three SF and three HF current Source pointers','exact seven current pointers: three SF, three HF dependencies and one HF host_source'),('SOURCE_REVIEW_READY.json','SOURCE_REVIEW_READY_v2.json')]
appended=[]
for a,b in changes:
 count=candidate.count(a)
 if count!=1 and a!='SOURCE_REVIEW_READY.json':raise RuntimeError('one exact correction')
 # READY selection appears in three exact current-publication checks.
 if a=='SOURCE_REVIEW_READY.json'and count!=3:raise RuntimeError('three exact READY references')
 before=candidate;candidate=candidate.replace(a,b);appended.append(dict(before=before,after=candidate))
ast.parse(candidate)
mapping=plan['publication_source_mapping'];counts=[0,0,0]
def inspect(v):
 if type(v)is dict:
  for i,row in enumerate(mapping):
   if v==row['predecessor_pin']:counts[i]+=1;return
  for item in v.values():inspect(item)
 elif type(v)is list:
  for item in v:inspect(item)
for key in('predecessor_source_freeze_pin','predecessor_host_freeze_pin'):inspect(json.loads(Path(plan[key]['path']).read_bytes()))
if counts!=[2,3,2]:raise RuntimeError('actual loaded predecessor seven pointer mapping')
wp=write(P/'write_once_GENDF_cumulative_ten_roots_SF_HF_recipe_v2.py',candidate.encode())
iv['writer_candidate_pin']=wp;iv['writer_changes']+=appended
iv['actual_loaded_predecessor_exact_replacement_counts']=counts
iv['all_current_SF_HF_source_pointer_count']=sum(counts)
back=candidate
for change in reversed(iv['writer_changes']):
 if back.count(change['after'])!=1:raise RuntimeError('complete unique inverse')
 back=back.replace(change['after'],change['before'],1)
if back.encode()!=__import__('base64').b64decode(iv['writer_original_whole_bytes_base64']):raise RuntimeError('whole inverse to immutable v10 writer')
ip=write(P/'COMPLETE_GENDF_V10_TO_V11_EXACT_PUBLICATION_AND_RESOURCE_WHOLE_BYTE_INVERSE_v2.json',iv)
plan['complete_scoped_byte_inverse_pin']=ip;plan['actual_loaded_predecessor_exact_replacement_counts']=counts
plan['predecessor_v11_Source_author_pin']=plan['Source_author_pin'];plan['Source_author_pin']=pin(__file__)
pp=write(P/'CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN_v2.json',plan)
ready['plan_pin']=pp;ready['complete_inverse_pin']=ip;ready['writer_source_pin']=wp
ready['selected_Source_pins']=ready['selected_Source_pins'][:3]+[pp,ip,wp]
rp=write(P/'SOURCE_REVIEW_READY_v2.json',ready)
fd=os.open(P,os.O_RDONLY|os.O_DIRECTORY)
try:os.fsync(fd)
finally:os.close(fd)
print(json.dumps(dict(status='GENDF_V11_EXACT_SEVEN_PUBLICATION_POINTERS_SOURCE_ONLY_READY',ready_pin=rp,plan_pin=pp,inverse_pin=ip,writer_source_pin=wp,Source_author_pin=pin(__file__),runtime_source_bytes_unchanged=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
