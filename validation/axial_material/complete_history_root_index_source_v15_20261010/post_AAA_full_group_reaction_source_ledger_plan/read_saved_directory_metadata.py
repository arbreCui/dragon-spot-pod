"""Standard-library-only read of XSM headers/directories/state-vector integers.
No scalar flux/cross-section/source/current values are read or calculated.
No business modules are imported. Payload SHA values come from frozen manifests,
not from this directory reader; no complete XSM payload hash is claimed.
"""
from pathlib import Path
import os, struct, json, hashlib
from collections import Counter

D=Path('/private/tmp/axmat_refined_AAA_full_group_reaction_source_ledger_plan_20261010')
P=Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005')

def identity(s):
 return {k:getattr(s,k) for k in ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')}

class DirectoryReader:
 def __init__(self,path):
  self.path=path; self.path_before=identity(path.stat());self.f=path.open('rb');self.fd_before=identity(os.fstat(self.f.fileno()));self.bytes_read=0
  if self.path_before!=self.fd_before:raise ValueError('path/fd differ before read')
  if self.read(0,3)[:4]!=b'$XSM':raise ValueError('invalid XSM format')
  self.root=self.directory(self.integers(2,1)[0])
 def read(self,offset,words):
  if type(offset) is not int or type(words) is not int or offset<0 or words<0 or (offset+words)*4>self.fd_before['st_size']:raise ValueError('invalid metadata range')
  self.f.seek(offset*4);b=self.f.read(words*4);self.bytes_read+=len(b)
  if len(b)!=words*4:raise ValueError('short metadata read')
  return b
 def integers(self,offset,count):return struct.unpack(f'<{count}i',self.read(offset,count))
 def directory(self,start):
  out={};seen=set();offset=start
  while offset not in seen:
   seen.add(offset)
   magic,capacity,count,following,_=struct.unpack_from('<4s4i',self.read(offset,8))
   if magic!=b'$$$$' or not 0<=count<=capacity<=30:raise ValueError('invalid directory header')
   b=self.read(offset+8,6*capacity)
   for i in range(count):
    e=tuple(struct.unpack_from('<i',b,4*(k*capacity+i))[0] for k in range(3))
    name=b[12*(capacity+i):12*(capacity+i+1)].decode('ascii').rstrip(' \0')
    if name in out:raise ValueError('duplicate record '+name)
    out[name]=e
   offset=following
  if offset!=start:raise ValueError('nonroot extent cycle')
  return out
 def list_entries(self,root,name):
  e=root.get(name)
  if e is None:return None
  if e[2]!=10 or e[1]<=0:raise ValueError('not list '+name)
  return [self.directory(p)['***HANDLE***'] for p in self.integers(e[0],e[1])]
 def finish(self):
  after=identity(os.fstat(self.f.fileno()));self.f.close();path_after=identity(self.path.stat())
  if after!=self.fd_before or path_after!=self.path_before:raise ValueError('XSM identity changed')
  return {'path':str(self.path),'path_7id_before':self.path_before,'fd_7id_before':self.fd_before,'fd_7id_after':after,'path_7id_after':path_after,'metadata_bytes_read':self.bytes_read}

seals={name:json.loads((P/name/'result.json').read_text()) for name in ['AAA/bootstrap','AAA/map012']}
files={'track':('AAA/bootstrap','initial_axial_track.xsm'),'macro':('AAA/bootstrap','initial_axial_macrolib.xsm'),'closed_axial':('AAA/map012','closed_axial.xsm'),'candidate_axial':('AAA/map012','candidate_axial.xsm'),'system':('AAA/map012','candidate_system.xsm')}
result={}
for role,(directory,basename) in files.items():
 r=DirectoryReader(P/directory/basename)
 state=r.root.get('STATE-VECTOR'); ints=None
 if state is not None:
  if state[1:]!=(40,1):raise ValueError('unexpected state vector')
  ints=list(r.integers(state[0],40))
 summary={'root_directory':r.root,'state_vector':ints,'manifest_sha256':seals[directory]['sha256'][basename],'manifest_scope':'frozen SEALED_STAGE_OUTPUTS digest; not freshly rehashed here'}
 for name in ['GROUP','FLUX64','FLUX','SOUR','SOUR64','SOURCE','SCAT-SOURCE','FISS-SOURCE']:
  entries=r.list_entries(r.root,name)
  if entries is None:continue
  summary[name+'_entries']=entries
  summary[name+'_type_length_counts']=[{'length_words':key[0],'type':key[1],'count':n} for key,n in sorted(Counter((v[1],v[2]) for v in entries).items())]
  if name=='GROUP':
   if any(e[1:]!=(-1,0) for e in entries):raise ValueError('not group directories')
   groups=[r.directory(e[0]) for e in entries];summary['all_group_directories']=groups
   names=sorted({k for g in groups for k in g});summary['group_field_presence']={k:{'present':sum(k in g for g in groups),'absent_group_ids_1based':[i+1 for i,g in enumerate(groups) if k not in g]} for k in names}
 summary.update(r.finish());result[role]=summary
metadata={'classification':'READ_ONLY_SAVED_XSM_DIRECTORY_METADATA_ONLY','payload_values_read':False,'transport_launched':False,'scientific_accuracy_qualified':False,'business_modules_imported':False,'archives':result}
(D/'saved_directory_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps({k:{'size_bytes':v['path_7id_before']['st_size'],'metadata_bytes_read':v['metadata_bytes_read'],'root_keys':list(v['root_directory']),'state_vector_first14':v['state_vector'][:14] if v['state_vector'] else None,'group_count':len(v.get('all_group_directories',[])),'list_counts':{n:len(v[n+'_entries']) for n in ['FLUX64','FLUX','SOUR','SOUR64'] if n+'_entries'in v},'requested_group_fields':{n:v.get('group_field_presence',{}).get(n,{'present':0}) for n in ['NUSIGF','CHI','NJJS00','IJJS00','IPOS00','SCAT00','DRAGON-TXSC','DRAGON-S0XSC','RADIAL-OP64','SOUR64']}} for k,v in result.items()},indent=2))
