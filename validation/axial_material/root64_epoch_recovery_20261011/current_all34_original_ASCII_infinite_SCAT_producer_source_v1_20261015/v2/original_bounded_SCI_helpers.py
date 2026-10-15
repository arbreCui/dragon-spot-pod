"""Bounded saved GENDF -> original DRAGR NX producer replay only.

No GENDF input, transport, compiler, SPH or scalar-yield inference.  Only the
already saved MF3/MF6 MT5 vectors are read.  Original SCI directory extents and
the selected TEMPERATURE/NX leaves are read with bounded pread.  SCI whole SHA
is checked separately; its whole tree is never decoded or spooled.
"""
import argparse,base64,hashlib,importlib.util,json,math,os,resource,stat,struct,sys,time
from pathlib import Path

CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,
 history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
 free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(DRAGR_complete_packed_kernel_replayed=False,finite_dilution_NX_replayed=False,
 current_SPH_MASK_context_applied=False,three_current_raw_MACRO_comparisons_performed=False,
 complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,
 unreduced_reference_qualified=False,scientific_accuracy_qualified=False,AAA_qualified=False,
 ABA_admitted=False,goal_complete=False,native_engines_started=0,original_input_or_library_writes=0)
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
NAMES=('U235','U238','Fe54','Fe56','Fe57','Fe58','Cr50','Cr52','Cr53','Cr54','Mn55')

def require(ok,text):
 if type(ok)is not bool or not ok:raise ValueError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def strict(raw):
 def pairs(items):
  out={}
  for k,v in items:require(k not in out,'duplicate metadata key');out[k]=v
  return out
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON '+x)))
def shape(p):
 require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'},'exact complete PF')
 require(type(p['path'])is str and Path(p['path']).is_absolute()and'..'not in Path(p['path']).parts
  and type(p['sha256'])is str and len(p['sha256'])==64 and all(c in '0123456789abcdef'for c in p['sha256'])
  and type(p['size_bytes'])is int and p['size_bytes']>=0 and type(p['identity'])is list
  and len(p['identity'])==7 and all(type(v)is int for v in p['identity'])and p['identity'][3]==1
  and p['identity'][4]==p['size_bytes'],'complete strict typed PF/one link')
def current(p):
 shape(p);q=Path(p['path']);s=q.lstat()
 require(not any(a.is_symlink()for a in(q,*q.parents))and stat.S_ISREG(s.st_mode)
  and identity(s)==p['identity'],'exact fullcurrent7 ordinary input')
 return q
def check(p,budget):
 q=current(p);h=hashlib.sha256();count=0
 with q.open('rb')as f:
  require(identity(os.fstat(f.fileno()))==p['identity'],'opened exact7')
  while True:
   budget();raw=f.read(2**20)
   if not raw:break
   h.update(raw);count+=len(raw)
  require(identity(os.fstat(f.fileno()))==p['identity'],'EOF exact7')
 require(count==p['size_bytes']and h.hexdigest()==p['sha256'],'whole EOF SHA/size')
 current(p)
def read(p,budget):
 check(p,budget);require(p['size_bytes']<8*2**20,'bounded selected metadata/vector document')
 v=strict(Path(p['path']).read_bytes());check(p,budget);return v
def pin(p):
 p=Path(p);s=p.lstat();h=hashlib.sha256(p.read_bytes()).hexdigest()
 require(identity(p.lstat())==identity(s),'new output exact7')
 return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=identity(s))
def write(p,v):
 with Path(p).open('x')as f:json.dump(v,f,separators=(',',':'),allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

class Budget:
 def __init__(self,roots,metadata):
  require(type(roots)is list and len(roots)==36 and len(set(roots))==36,'bound prior34 plus corrected NX Source/output, no cumulative reset')
  self.roots=[Path(p)for p in roots];self.metadata=metadata;self.started=time.monotonic();self.last=0
  require(all(p.is_absolute()for p in self.roots)and not any(a.is_relative_to(b)for a in self.roots for b in self.roots if a!=b),'exact disjoint roots')
 def check(self):
  now=time.monotonic();peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  require(now-self.started<600 and peak<512*2**20,'original SELF512/child600')
  if now-self.last<0.25:return
  self.last=now;total=0
  for r in self.roots:
   if not r.exists():continue
   for p in r.rglob('*'):
    s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'joint namespace alias')
    if stat.S_ISREG(s.st_mode):total+=s.st_size
  for p in self.metadata:
   current(p)
   if not any(Path(p['path']).is_relative_to(r)for r in self.roots):total+=p['size_bytes']
  unlinked={}
  for fd in os.listdir('/dev/fd'):
   try:s=os.fstat(int(fd))
   except(ValueError,OSError):continue
   if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
  require(total+sum(unlinked.values())<2*2**30,'unchanged complete cumulative2GiB/open-unlinked')

class BoundedSCI:
 """Same raw xsmdir layout as original retained byte extractor; selective paths."""
 def __init__(self,p,budget):
  self.p=p;self.budget=budget;self.f=current(p).open('rb');self.fd=self.f.fileno();self.read_bytes=0;self.extents=0
  require(identity(os.fstat(self.fd))==p['identity'],'SCI opened exact7')
  require(self.raw(0,3)[:4]==b'$XSM','original little-endian four-byte XSM')
  self.high,self.root=struct.unpack('<2i',self.raw(1,2))
 def raw(self,at,n):
  self.budget();require(type(at)is int and type(n)is int and at>=0 and 0<=n<=262144
   and 4*(at+n)<=self.p['size_bytes'],'bounded SCI original offset/count')
  require(identity(os.fstat(self.fd))==self.p['identity'],'SCI before pread7')
  b=os.pread(self.fd,4*n,4*at);self.read_bytes+=len(b)
  require(len(b)==4*n and identity(os.fstat(self.fd))==self.p['identity'],'SCI after pread7')
  return b
 def directory(self,start):
  seen=set();entries=[];names=set();at=start
  while at not in seen:
   require(len(seen)<10000,'bounded original named directory extent chain');seen.add(at)
   h=self.raw(at,8);magic,cap,count,nxt,parent=struct.unpack_from('<4s4i',h)
   require(magic==b'$$$$'and 0<=count<=cap<=30,'original xsmdir header')
   available=min(6*cap,max(0,self.p['size_bytes']//4-at-8))
   require(count==0 or available==6*cap,'complete populated original directory extent')
   b=self.raw(at+8,available);self.extents+=1
   for i in range(count):
    offset,words,kind=[struct.unpack_from('<i',b,4*(j*cap+i))[0]for j in range(3)]
    nr=b[12*(cap+i):12*(cap+i+1)];name=nr.split(b'\0',1)[0].rstrip(b' ').decode('ascii')
    if name=='***DEL***':continue
    require(name and name not in names,'unique original named directory slots');names.add(name)
    entries.append(dict(name=name,offset_words=offset,words=words,kind=kind,extent_words=at,slot_zero_based=i,original_name_bytes_hex=nr.hex()))
   at=nxt
  require(at==start,'directory cycle closes at actual origin');return entries
 def lookup(self,start,name):
  matches=[x for x in self.directory(start)if x['name']==name]
  require(len(matches)==1,'exact original named leaf/directory '+name);return matches[0]
 def leaf(self,e):
  require(e['kind']==2 and 0<e['words']<=370,'bounded original REAL32 leaf')
  b=self.raw(e['offset_words'],e['words']);return b,struct.unpack('<'+str(e['words'])+'f',b)
 def close(self):
  require(identity(os.fstat(self.fd))==self.p['identity'],'SCI final opened7');self.f.close();current(self.p)

def payload64(v):return base64.b64encode(struct.pack('<'+str(len(v))+'d',*v)).decode('ascii')
def mask(v):return base64.b64encode(bytes(int(x)for x in v)).decode('ascii')
def finite_vector(s):
 require(s['mt']==5 and s['nz']==1 and len(s['P0_vector64'])==1 and len(s['P0_vector64'][0])==370
  and len(s['incident_present'])==370 and all(type(x)is bool for x in s['incident_present']),'complete original MT5 P0/mask, nz1 only')
 v=s['P0_vector64'][0];require(all(type(x)in(int,float)and math.isfinite(x)and x>=0 for x in v),'finite nonnegative saved P0')
 return v

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--binding-pin',required=True);ap.add_argument('--expected-parent-pid',type=int,required=True);a=ap.parse_args()
 require(os.getppid()==a.expected_parent_pid and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in THREADS),'original owning parent/unprofiled single-thread child')
 bp=strict(a.binding_pin);b=read(bp,lambda:None);require(b['schema']=='SAVED_MT5_NX_RAW32_YIELD_EXECUTION_BINDING_V1'and b['original_caps']==CAPS,'single purpose frozen binding')
 budget=Budget(b['complete_joint_roots'],b['explicit_cumulative_metadata_file_pins']);budget.check()
 sf=read(b['source_freeze_pin'],budget.check);plan=read(sf['control_plan_pin'],budget.check)
 require(sf['schema']=='SAVED_MT5_NX_RAW32_YIELD_SOURCE_ONLY_FREEZE_V1'and sf['candidate_executed']is False,'same immutable Source-only package')
 for p in sf['complete_source_file_pins']:check(p,budget.check)
 require(any(p['path']==str(Path(__file__).absolute())for p in sf['complete_source_file_pins']),'whole child Source protected')
 evidence=read(plan['actual_GENDF_evidence_pin'],budget.check);findings=read(plan['original_NX_findings_pin'],budget.check)
 require(evidence['status']=='ACTUAL_ALL_ELEVEN_SAVED_MT5_EXTRACTIONS_CLOSED0_ONLY'and evidence['native_engines_started']==0 and evidence['complete_reaction_authority_qualified']is False,'actual closed GF11 evidence only')
 extraction=evidence['actual_extractions'];require(tuple(r['nuclide']for r in extraction)==NAMES,'all eleven actual unique references in original order')
 sci_pin=plan['actual_current_SCI1_pin'];current(sci_pin)
 require(b['SCI1_whole_PF_verified_by_original_parent_before_child']is True,'original parent closed whole SHA before owned child')
 historical=[r for r in findings['complete_actual_source_library_isotope_NX_inventory']if r['library_pin']['sha256']==sci_pin['sha256']and r['library_pin']['size_bytes']==sci_pin['size_bytes']]
 require(len(historical)==1,'exact full SCI content equals original raw NX inventory; historical PF not rewritten')
 original_refs={r['reference']:r for r in historical[0]['actual_refs']};sci=BoundedSCI(sci_pin,budget.check);rows=[];all_exact=True
 try:
  for r in extraction:
   budget.check();name=r['nuclide'];d=read(r['actual_complete_extraction_pin'],budget.check)
   require(d['schema']=='SAVED_BINARY_GENDF_REACTION_P0_EXTRACTION_ONLY_V1'and d['input_pin']==r['input_pin']and d['mat']==r['mat']and d['requested_mts']==[5]and d['energy_groups']==370,'same complete saved original GF extraction')
   iso=sci.lookup(sci.root,name);require(iso['kind']==0 and iso['words']==-1,'original SCI isotope directory')
   tentry=sci.lookup(iso['offset_words'],'TEMPERATURE');traw,temps=sci.leaf(tentry)
   sections=d['actual_P0_sections'];by={}
   for s in sections:
    require(s['mf']in(3,6)and s['mt']==5,'MT5 saved sections only');stamp=(s['mf'],s['temperature_K']);require(stamp not in by,'unique saved MF/T');by[stamp]=s
   require(len(by)==2*len(temps)and set(t for mf,t in by if mf==3)==set(temps)and set(t for mf,t in by if mf==6)==set(temps),'exact SCI TEMPERATURE selects all saved MF3/MF6, no invented temperature')
   old={r['relative_path']:r for r in original_refs[name]['NX_leaves']};require(len(old)==len(temps),'complete original all-temperature NX inventory')
   for index,temp in enumerate(temps,1):
    subname='SUBTMP'+format(index,'04d');sub=sci.lookup(iso['offset_words'],subname);require(sub['kind']==0 and sub['words']==-1,'actual original SUBTMP')
    entries=sci.directory(sub['offset_words']);nx=[e for e in entries if e['name']=='NX'];require(len(nx)==1,'actual original NX leaf')
    original_raw,values=sci.leaf(nx[0]);sigma=finite_vector(by[3,temp]);production=finite_vector(by[6,temp])
    nonzero=[i for i,v in enumerate(sigma)if v!=0];require(bool(nonzero),'original DRAGR would omit all-zero NX')
    last=nonzero[-1]+1;replay=struct.pack('<'+str(last)+'f',*sigma[:last]);rel=name+'/'+subname+'/NX';prior=old[rel]
    require(prior['words']==len(original_raw)//4 and prior['type']==2 and prior['payload_sha256']==hashlib.sha256(original_raw).hexdigest(),'original findings raw hash/count against exact current SCI leaf')
    exact=replay==original_raw;all_exact=all_exact and exact;mismatches=sum(a!=b for a,b in zip(struct.iter_unpack('<I',replay),struct.iter_unpack('<I',original_raw)))if len(replay)==len(original_raw)else None
    finite_dirs=[e for e in entries if e['name'].startswith('SUBMAT')]
    for e in finite_dirs:
     require(e['kind']==0 and e['words']==-1 and not any(k['name']=='NX'for k in sci.directory(e['offset_words'])),'nz1 MT5 has no finite-dilution NX leaf; do not certify dilution replay')
    delta=[p-s for p,s in zip(production,sigma)];valid=[s>0 for s in sigma];nu=[p/s if ok else 0.0 for p,s,ok in zip(production,sigma,valid)]
    require(all(math.isfinite(v)for v in delta+nu),'finite actual saved production diagnostics')
    actual_nu=[v for v,ok in zip(nu,valid)if ok]
    rows.append(dict(nuclide=name,mat=r['mat'],temperature_K=temp,original_SUBTMP=subname,original_temperature_leaf=tentry,original_temperature_raw32_hex=traw.hex(),original_NX_leaf=nx[0],original_NX_words=len(original_raw)//4,replayed_NX_words=last,original_NX_raw_sha256=hashlib.sha256(original_raw).hexdigest(),replayed_NX_raw_sha256=hashlib.sha256(replay).hexdigest(),exact_NX_raw32_equal=exact,mismatching_raw_words=mismatches,finite_dilution_NX_leaf_count=0,finite_dilution_NX_replayed=False,sigma5_all370_binary64_sha256=hashlib.sha256(base64.b64decode(payload64(sigma))).hexdigest(),production5_all370_binary64_sha256=hashlib.sha256(base64.b64decode(payload64(production))).hexdigest(),production_minus_sigma_all370_binary64_sha256=hashlib.sha256(base64.b64decode(payload64(delta))).hexdigest(),production_minus_sigma_range=[min(delta),max(delta)],production_minus_sigma_negative_groups=sum(v<0 for v in delta),nu_effective_valid_sigma_positive_groups=sum(valid),nu_effective_range=None if not actual_nu else[min(actual_nu),max(actual_nu)],sigma_zero_production_nonzero_groups=sum(s==0 and p!=0 for s,p in zip(sigma,production)),nu_effective_invalid_groups_not_assigned_a_yield=True,MF3_original_incident_present_mask_b64=mask(by[3,temp]['incident_present']),MF6_original_incident_present_mask_b64=mask(by[6,temp]['incident_present']),original_saved_extraction_pin=r['actual_complete_extraction_pin'],SCAT00_component_comparison_performed=False))
 finally:sci.close()
 current(sci_pin);budget.check()
 out=Path(b['output_directory']);require(out.parent==Path(plan['planned_actual_output_root'])and not os.path.lexists(out),'fresh owning child report namespace');out.mkdir()
 report=out/'ACTUAL_SAVED_MT5_NX_RAW32_AND_YIELD_DIAGNOSTIC.json'
 v=dict(schema='ACTUAL_SAVED_MT5_NX_RAW32_PRODUCER_REPLAY_AND_YIELD_DIAGNOSTIC_V1',status='ALL_ORIGINAL_NX_PRODUCER_RAW32_EQUAL'if all_exact else'ORIGINAL_NX_PRODUCER_RAW32_MISMATCH',source_freeze_pin=b['source_freeze_pin'],actual_GENDF_evidence_pin=plan['actual_GENDF_evidence_pin'],original_NX_findings_pin=plan['original_NX_findings_pin'],actual_current_SCI1_pin=sci_pin,actual_NX_producer_all_temperature_replay_passed=all_exact,compared_unique_nuclides=11,compared_temperature_records=len(rows),selective_SCI_payload_and_directory_bytes=sci.read_bytes,selective_SCI_directory_extents=sci.extents,original_SCI_tree_whole_decoded=False,original_dragr_formula='vector(ig)=real(rv(ig,1,1)); truncate after last exact nonzero; MF3 MT5 nz=1',yield_diagnostic_formula='P5(g)=saved MF6 MT5 P0 outgoing sum; Delta5=P5-sigma5; nu_eff=P5/sigma5 only where sigma5>0',yield_diagnostic_not_applied_to_current_SPH_or_MACRO=True,temperature_diagnostics=rows,**FALSE)
 write(report,v);budget.check();print(json.dumps(dict(status=v['status'],report=pin(report),**FALSE)),flush=True)
 require(all_exact,'real original NX raw32 mismatch; retain result and no retry')
if __name__=='__main__':main()
