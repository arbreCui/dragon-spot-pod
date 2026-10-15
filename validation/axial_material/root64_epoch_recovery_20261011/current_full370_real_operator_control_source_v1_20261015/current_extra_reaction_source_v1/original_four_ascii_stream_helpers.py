"""Once streaming original ASCII GENDF validation; no restored payload or matrix."""
import argparse,gzip,hashlib,importlib.util,io,json,math,os,resource,stat,sys,time
from pathlib import Path
CAPS={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'fresh_bytes':2147483648,'history_bytes':103079215104,'cold_reserve_bytes':20971764748,'metadata_reserve_bytes':67108864,'free_floor_bytes':8589934592,'threads':1,'children_at_once':1,'retries':0}
FALSE=dict(physics_qualified=False,scientific_accuracy_qualified=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,full_reference_qualified=False,unreduced_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,DRAGR_packed_raw_words_replayed=False,SCAT_constructed=False,current_SPH_MASK_context_applied=False,historical_machine_bit_replay=False)
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();require(q.is_absolute()and not any(a.is_symlink()for a in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and identity(s)==p['identity']and s.st_size==p['size_bytes'],'exact ordinary current7')
def metadata(p):
 current(p);require(p['size_bytes']<8*2**20,'bounded metadata');raw=Path(p['path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==p['sha256'],'whole metadata SHA');current(p);return json.loads(raw)
def pin(q):
 q=Path(q);s=q.lstat();p=dict(path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=identity(s));current(p);return p
def write(p,v):
 with Path(p).open('x')as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
class Budget:
 def __init__(self,roots,explicit):
  require(len(roots)==44 and len(set(roots))==44 and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'complete44 disjoint cumulative roots');self.roots=[Path(p)for p in roots];self.explicit=explicit;self.started=time.monotonic();self.last=0.0
 def check(self):
  now=time.monotonic();peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);require(now-self.started<600 and peak<512*2**20,'original child600/SELF512')
  if now-self.last<0.25:return
  self.last=now;total=0
  for root in self.roots:
   if not root.exists():continue
   for p in root.rglob('*'):
    s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'no joint namespace alias')
    if stat.S_ISREG(s.st_mode):total+=s.st_size
  nodes=set()
  for p in self.explicit:
   current(p);node=tuple(p['identity'][:2]);require(node not in nodes,'distinct explicit metadata nodes');nodes.add(node)
   if not any(Path(p['path']).is_relative_to(root)for root in self.roots):total+=p['size_bytes']
  unlinked={}
  for fd in os.listdir('/dev/fd'):
   try:s=os.fstat(int(fd))
   except(ValueError,OSError):continue
   if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
  require(total+sum(unlinked.values())<2*2**30,'original cumulative2GiB and open-unlinked')
class Compressed(io.RawIOBase):
 def __init__(self,stream,p,budget):self.stream=stream;self.expected=p;self.budget=budget;self.digest=hashlib.sha256();self.bytes=0
 def readable(self):return True
 def read(self,n=-1):
  self.budget();require(n>=0,'bounded compressed read');v=self.stream.read(n);self.digest.update(v);self.bytes+=len(v);require(identity(os.fstat(self.stream.fileno()))==self.expected['identity'],'opened gzip7 unchanged');return v
class Lines:
 def __init__(self,stream,budget):self.stream=stream;self.budget=budget;self.digest=hashlib.sha256();self.bytes=self.lines=0
 def next(self):
  self.budget();raw=self.stream.readline(83)
  if not raw:return None
  require(len(raw)==81 and raw.endswith(b'\n'),'original80-column ASCII newline, no truncation');raw.decode('ascii');self.digest.update(raw);self.bytes+=len(raw);self.lines+=1;return raw
def extract(row,scalar,budget):
 context=dict(nuclide=row['nuclide'],stage='before originalASCII first record')
 def require(ok,message):
  if type(ok)is not bool or not ok:raise RuntimeError(message+'; actual originalASCII context='+json.dumps(context,separators=(',',':'),allow_nan=False))
 p=row['gzip_primary_current_full_pin'];current(p);sections=[];grids=[];active=None;key=None;boundary_counts={};seen=set()
 def close():
  nonlocal active,key
  if active is not None:
   stamp=(active['mf'],active['mt'],active['temperature_K']);require(stamp not in seen and active['LIST_records']>0,'unique complete actual reaction section');seen.add(stamp);active['incident_groups_present']=[i+1 for i,v in enumerate(active.pop('incident_mask'))if v];sections.append(active)
  active=key=None
 with Path(p['path']).open('rb')as raw:
  require(identity(os.fstat(raw.fileno()))==p['identity'],'opened exact gzip primary');compressed=Compressed(raw,p,budget)
  with gzip.GzipFile(fileobj=compressed,mode='rb')as decoded:
   reader=Lines(decoded,budget)
   while True:
    line=reader.next()
    if line is None:break
    text=line[:-1].decode('ascii');k=scalar.identity(text);mat,mf,mt=k
    if mf==0 or mt==0:
     require(active is None or k==(row['mat'],active['mf'],0),'explicit actual reaction SEND');close();boundary_counts[str(k)]=boundary_counts.get(str(k),0)+1;continue
    context=dict(nuclide=row['nuclide'],mat=mat,mf=mf,mt=mt,raw_header_ascii=text);require(mat==row['mat'],'exact original isotope material');h=scalar.fields(text);context.update(temperature_K=h[0],NG2=h[2],lower=h[3],NPL=h[4],incident_group=h[5])
    if key is None:
     key=k;require(mf in(1,3,5,6),'only declared actual GENDF LIST families')
     if (mf,mt)==(1,451):nz=scalar.integer(h[3]);require(nz==10,'original full10 dilution grid')
     elif mf in(3,6):
      nl,nz,ng=scalar.integer(h[2]),scalar.integer(h[3]),scalar.integer(h[5]);require(1<=nl<=8 and nz in(1,10)and ng==370,'actual original370 reaction dimensions');active=dict(mat=mat,mf=mf,mt=mt,nl=nl,nz=nz,energy_groups=ng,temperature_K=None,temperature_header_ascii=None,section_header_ascii=text,section_header_sha256=hashlib.sha256(line).hexdigest(),LIST_records=0,payload_values=0,incident_mask=[False]*370,spectrum_LIST_present=False,actual_NG2_histogram={},actual_LIST_index_dimensions=[])
     continue
    require(k==key,'explicit SEND before next section');npl=scalar.integer(h[4]);require(0<=npl<=88800,'bounded original LIST values');payload=[];payloadsha=hashlib.sha256()
    for _ in range((npl+5)//6):
     data=reader.next();require(data is not None and scalar.identity(data[:-1].decode('ascii'))==k,'complete actual LIST payload identity');payloadsha.update(data);payload.extend(scalar.fields(data[:-1].decode('ascii')))
    payload=payload[:npl];require(len(payload)==npl,'complete actual NPL')
    if (mf,mt)==(1,451):
     ng,ngg=scalar.integer(h[2]),scalar.integer(h[3]);require(ng==370 and ngg==0 and npl==383,'full original370 neutron-only grid');sigma=payload[1:11];energy=payload[11:382];require(len(sigma)==10 and all(v>0 for v in sigma)and len(set(sigma))==10 and len(energy)==371 and all(a<b for a,b in zip(energy,energy[1:])),'exact finite10 sigma and ascending371 boundaries');require(h[0]not in [g['temperature_K']for g in grids],'unique original MF1 temperature');grids.append(dict(original_temperature_index_one_based=len(grids)+1,temperature_K=h[0],raw_LIST_header_ascii=text,raw_LIST_header_sha256=hashlib.sha256(line).hexdigest(),raw_grid_payload_sha256=payloadsha.hexdigest(),sigma0_barn=sigma,ascending_energy_eV=energy,source_deck_temperature_K=row['original_source_deck_temperatures_K'][len(grids)]));continue
    if active is not None:
     ng2,lower,ig=[scalar.integer(h[i])for i in(2,3,5)];require(ng2>=1 and npl==ng2*active['nl']*active['nz']and 0<=ig<=370,'complete actual reaction LIST dimensions');require(active['temperature_K']in(None,h[0]),'single original ASCII section temperature');active['temperature_K']=h[0]
     if active['temperature_header_ascii']is None:active['temperature_header_ascii']=text;active['temperature_header_sha256']=hashlib.sha256(line).hexdigest()
     active['LIST_records']+=1;active['payload_values']+=npl;active['actual_NG2_histogram'][str(ng2)]=active['actual_NG2_histogram'].get(str(ng2),0)+1;active['actual_LIST_index_dimensions'].append([ig,lower,ng2,npl])
     if ig==0:require(mf==6 and not active['spectrum_LIST_present']and 1<=lower and lower+ng2-1<=370,'unique actual spectrum LIST');active['spectrum_LIST_present']=True
     else:
      require(not active['incident_mask'][ig-1]and ng2>=2,'unique actual incident group, flux+values');active['incident_mask'][ig-1]=True
      if mf==6:require(lower==0 or 1<=lower<=370 and lower+ng2-2<=370,'actual MF6 destination dimensions')
   require(key is None,'complete final GENDF boundary');require(reader.bytes==row['historical_original_ASCII_size_bytes']and reader.digest.hexdigest()==row['historical_original_ASCII_sha256'],'whole original ASCII size/SHA, no restored inode claim')
  require(compressed.read(1)==b''and compressed.bytes==p['size_bytes']and compressed.digest.hexdigest()==p['sha256'],'whole compressed primary EOF/SHA');require(identity(os.fstat(raw.fileno()))==p['identity'],'final opened gzip7')
 current(p);require(len(grids)==8 and len(set(g['temperature_K']for g in grids))==8,'all original8 grids');require(bool(sections),'actual MF3 and MF6 inventories present')
 for section in sections:require(len([g for g in grids if g['temperature_K']==section['temperature_K']])==1,'reaction belongs to exact decoded originalASCII grid')
 inventory={}
 histograms={}
 for s in sections:
  inventory.setdefault((s['mf'],s['mt']),[]).append(s['temperature_K']);histogram=histograms.setdefault((s['mf'],s['mt']),{})
  for ng2,count in s['actual_NG2_histogram'].items():histogram[ng2]=histogram.get(ng2,0)+count
 require({s['mf']for s in sections}=={3,6},'both actual reaction inventories')
 return dict(schema='ACTUAL_FOUR_ORIGINAL_ASCII_GENDF_STREAM_INVENTORY_V1',nuclide=row['nuclide'],mat=row['mat'],current_gzip_primary_full_pin=p,historical_original_ASCII_path=row['historical_original_ASCII_path'],actual_decompressed_SHA256=reader.digest.hexdigest(),actual_decompressed_bytes=reader.bytes,actual_ASCII_records=reader.lines,full_current_compressed_SHA256=compressed.digest.hexdigest(),original_ASCII_fullEOF_validated=True,gzip_CRC_and_ISIZE_validated=True,original_ASCII_not_written=True,current_original_inode_not_invented=True,original8_MF1_grids=grids,actual_MF3_MF6_reaction_inventory=[dict(mf=k[0],mt=k[1],temperature_sections=len(v),actual_decoded_temperatures_K=v,actual_NG2_histogram=histograms[k])for k,v in sorted(inventory.items())],actual_LIST_index_dimension_columns=['incident_group','lower','NG2','NPL'],actual_sections=sections,boundary_counts=boundary_counts,original_receipt_and_deck_proof=row['historical_proof'],original_formatter_already_applied=True,second_quantization_performed=False,**FALSE)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--binding-pin',required=True);ap.add_argument('--expected-parent-pid',type=int,required=True);a=ap.parse_args();require(os.getppid()==a.expected_parent_pid and not sys.flags.optimize and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in THREADS),'actual original single-thread owning unoptimized child');pb=json.loads(a.binding_pin);b=metadata(pb);require(b['schema']=='FOUR_ORIGINAL_ASCII_GENDF_EXECUTION_BINDING_V1'and b['original_caps']==CAPS,'same exact once binding');budget=Budget(b['complete_joint_roots'],b['explicit_cumulative_metadata_file_pins']);budget.check();plan=metadata(b['control_plan_pin']);require(plan['original_caps']==CAPS and plan['complete_joint_roots']==b['complete_joint_roots'],'same cumulative original caps plan');p=plan['original_scalar_helper_source_copy_pin'];current(p);require(hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],'whole unchanged scalar helper Source');spec=importlib.util.spec_from_file_location('whole_original_ascii_scalar_helpers',p['path']);scalar=importlib.util.module_from_spec(spec);spec.loader.exec_module(scalar);current(p)
 out=Path(b['output_directory']);require(out.is_dir(),'owning host output exists');results=[]
 for row in plan['inputs']:
  value=extract(row,scalar,budget.check);target=out/(row['nuclide']+'_original_ASCII_GENDF_inventory.json');write(target,value);results.append(dict(nuclide=row['nuclide'],complete_inventory_pin=pin(target),actual_decompressed_SHA256=value['actual_decompressed_SHA256'],actual_decompressed_bytes=value['actual_decompressed_bytes'],MF1_grids=len(value['original8_MF1_grids']),MF3_MF6_sections=len(value['actual_sections'])));del value
 for p in b['fixed_small_metadata_pins']:metadata(p)
 metadata(pb);budget.last=0;budget.check();report=out/'ACTUAL_FOUR_ORIGINAL_ASCII_GENDF_STREAM_EVIDENCE.json';write(report,dict(schema='ACTUAL_FOUR_ORIGINAL_ASCII_GENDF_STREAM_EVIDENCE_V1',status='ACTUAL_ALL_FOUR_ORIGINAL_ASCII_FULLSHA_GRID_INVENTORIES_CLOSED0_ONLY',execution_binding_pin=pb,control_plan_pin=b['control_plan_pin'],source_freeze_pin=b['source_freeze_pin'],actual_extractions=results,original_caps=CAPS,native_engines_started=0,original_inputs_written=0,original_ASCII_files_written=0,**FALSE));budget.last=0;budget.check();print(json.dumps(dict(status='ACTUAL_ALL_FOUR_ORIGINAL_ASCII_FULLSHA_GRID_INVENTORIES_CLOSED0_ONLY',report_pin=pin(report),**FALSE)),flush=True)
if __name__=='__main__':main()
