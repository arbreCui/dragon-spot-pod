"""One isotope/one temperature compact original ASCII LIST -> infinite P0 only.

Original scalar parsing, matrix and nonfinite packing are copied whole and
called unchanged. No dense field file, finite branch, second a11 or solver.
"""
import argparse,contextlib,hashlib,importlib.util,json,math,os,resource,stat,struct,sys,time
from pathlib import Path
CAPS={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'fresh_bytes':2147483648,'history_bytes':103079215104,'cold_reserve_bytes':20971764748,'metadata_reserve_bytes':67108864,'free_floor_bytes':8589934592,'threads':1,'children_at_once':1,'retries':0}
FALSE=dict(physics_qualified=False,scientific_accuracy_qualified=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,full_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,finite18_replayed=False,temperature_interpolation_replayed=False,current_SPH_MASK_context_applied=False,historical_machine_bit_replay=False,original_XSM_memory_bits_verified=False)
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
MTS=(2,5,16,17,28,37,*range(51,92))
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
def module(p,name):
 current(p);require(hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],'whole unchanged helper Source');spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current(p);return m
class Budget:
 def __init__(self,roots,explicit):
  require(len(roots)==49 and len(set(roots))==49 and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'complete prior47 plus Source/output49 disjoint roots');self.roots=[Path(p)for p in roots];self.explicit=explicit;self.started=time.monotonic();self.last=0.0
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
def target_leaf(sci,e):
 """Only three new target roles; original raw/directory/lookup stay unchanged."""
 name=e['name'];require(name in('SCAT00','NJJS00','IJJS00'),'literal infinite P0 target only')
 kind=2 if name=='SCAT00'else 1;limit=370*370 if kind==2 else 370
 require(e['kind']==kind and 0<e['words']<=limit and(kind==2 or e['words']==370),'exact target kind and original bounded word count')
 raw=sci.raw(e['offset_words'],e['words'])
 if kind==2:require(all(math.isfinite(v[0])for v in struct.iter_unpack('<f',raw)),'finite original SCAT00')
 return raw
def compare_leaf(sci,e,replayed):
 original=target_leaf(sci,e);mismatch=0;samples=[]
 for i in range(max(len(original),len(replayed))//4):
  a=original[4*i:4*i+4];b=replayed[4*i:4*i+4]
  if a!=b:
   mismatch+=1
   if len(samples)<12:samples.append(dict(word_one_based=i+1,original_hex=a.hex(),replayed_hex=b.hex()))
 return dict(original_leaf=e,original_byte_offset=4*e['offset_words'],original_kind=e['kind'],original_words=e['words'],original_raw_sha256=hashlib.sha256(original).hexdigest(),replayed_words=len(replayed)//4,replayed_raw_sha256=hashlib.sha256(replayed).hexdigest(),exact_raw_words_equal=original==replayed,mismatching_raw_words=mismatch,bounded_mismatch_samples=samples)
def replay_temperature(row,grid,sections,section_indexes,scalar,sci,iso,temperature_leaf,temperature_raw,temps,energy,inventory_mf6):
 np=scalar.np;actual=grid['temperature_K'];word=struct.pack('<f',actual);hits=[i for i,v in enumerate(temps)if struct.pack('<f',v)==word];require(len(hits)==1,'exact REAL32 original temperature word selects one SCI SUBTMP')
 index=hits[0]+1;subname='SUBTMP'+format(index,'04d');sub=sci.lookup(iso['offset_words'],subname);require(sub['kind']==0 and sub['words']==-1,'actual original SUBTMP directory')
 require(struct.pack('<371f',*grid['ascending_energy_eV'][::-1])==energy['raw'],'original energy mesh REAL32 matches stored SCI ENERGY')
 cutoff_energy=energy['values']if row['original_drahd_existing_ENERGY_REAL32_branch']else grid['ascending_energy_eV'][::-1]
 igrest=sum(row['original_thermal_cutoff_eV']>=0.999*v for v in cutoff_energy[1:370]);thermals=sorted((mt for mt in sections if 221<=mt<=250),reverse=True)
 elastic=sections.get(2);require(elastic is not None and elastic['actual_nz']==len(grid['sigma0_barn']),'actual elastic and global dilution widths')
 first_thermal=next((mt for mt in sections if 221<=mt<=250),None);ngther=0
 if first_thermal is not None:
  for ig in sections[first_thermal]['records']:
   if ig==370:break
   ngther=max(ngther,ig)
 ngther=min(ngther,igrest);first=370-ngther;total=np.zeros((370,370),dtype='f8')
 def matrix(mt):
  section=sections[mt];require(section['actual_nz']in(1,elastic['actual_nz']),'original drasc nz1 broadcast or elastic NZ')
  value,flux=scalar.matrix(section);return value[0,0],flux[0,0]
 for mt in thermals:
  require(sections[mt]['actual_nz']==1 and sections[mt]['actual_nl']==elastic['actual_nl'],'original thermal nz1 and Legendre width')
  value,_=matrix(mt);total[first:,:]+=value[first:,:];del value
 if thermals:
  value,_=matrix(2);total[first:,:]-=value[first:,:];del value
 used=[]
 for mt in MTS:
  if mt not in sections:continue
  value,_=matrix(mt);total+=value;used.append(mt);del value
 require(bool(np.isfinite(total).all()),'finite original accumulated infinite P0')
 if row['original_ipflag']==1:
  for incident in range(370):
   dgar=0.0
   for outgoing in range(370):dgar=dgar+float(total[incident,outgoing])
   total[incident,:]=0.0;total[incident,incident]=dgar
 else:require(row['original_ipflag']==0,'original ipflag0 or1 only')
 njjs,ijjs,scat=scalar.packed(total,False,(0,0),total)
 replayed={'SCAT00':scat.astype('<f4',copy=False).tobytes(),'NJJS00':struct.pack('<370i',*njjs),'IJJS00':struct.pack('<370i',*ijjs)}
 comparisons={name:compare_leaf(sci,sci.lookup(sub['offset_words'],name),raw)for name,raw in replayed.items()}
 exact=all(v['exact_raw_words_equal']for v in comparisons.values())
 return dict(nuclide=row['nuclide'],mat=row['mat'],actual_original_ASCII_temperature_K=actual,original_MF1_grid_index_one_based=grid['original_temperature_index_one_based'],original_SCI_SUBTMP=subname,original_temperature_leaf=temperature_leaf,original_temperature_leaf_raw_sha256=hashlib.sha256(temperature_raw).hexdigest(),selected_temperature_raw32_hex=word.hex(),original_thermal_cutoff_eV=row['original_thermal_cutoff_eV'],original_igrest=igrest,original_ipflag=row['original_ipflag'],original_ENERGY_cutoff_branch='existing_REAL32_promoted'if row['original_drahd_existing_ENERGY_REAL32_branch']else'new_GENDF_binary64',actual_thermal_MTs_descending=thermals,original_ngther=ngther,actual_elastic_NL=elastic['actual_nl'],actual_elastic_NZ=elastic['actual_nz'],original_strict47_MTs=MTS,actual_used_strict47_MTs=used,actual_inventory_section_indexes_one_based=section_indexes,actual_MF6_MTs_outside_strict47_and_thermal=[mt for mt in inventory_mf6 if mt not in MTS and not 221<=mt<=250],comparisons=comparisons,exact_infinite_P0_three_leaf_raw_words_equal=exact,compact_P0_z0_LIST_only=True,no_dense_field_spool=True,**FALSE)
def extract(row,scalar,streamer,budget,sci,energy):
 expected=None
 if row.get('actual_complete_inventory_pin'):
  inventory=metadata(row['actual_complete_inventory_pin']);expected=inventory['actual_sections'];require(inventory['nuclide']==row['nuclide']and inventory['mat']==row['mat']and inventory['original_ASCII_fullEOF_validated']is True,'same original first4 verified inventory')
 iso=sci.lookup(sci.root,row['nuclide']);require(iso['kind']==0 and iso['words']==-1,'original SCI isotope route')
 tleaf=sci.lookup(iso['offset_words'],'TEMPERATURE');traw,temps=sci.leaf(tleaf);nt=len(row['original_source_deck_temperatures_K']);require(len(temps)==nt and len(set(temps))==nt and all(math.isfinite(v)for v in temps),'actual native SCI/deck unique temperature count')
 p=row['current_original_input_full_pin'];current(p);active=None;key=None;cursor=0;grid=None;grid_nz=None;sections={};section_indexes=[];rows=[];grids=[];ledger=[];seen=set();boundaries={};cohort_mf6=[]
 def flush_temperature():
  if grid is None:return
  require(bool(sections),'nonempty one-temperature compact MF6 buffer');rows.append(replay_temperature(row,grid,sections,section_indexes,scalar,sci,iso,tleaf,traw,temps,energy,cohort_mf6));sections.clear();section_indexes.clear();cohort_mf6.clear()
 def close():
  nonlocal active,key,cursor
  if active is not None:
   require(active['LIST_records']>0,'complete nonempty actual MF3/MF6 section');stamp=(active['mf'],active['mt'],active['temperature_K']);require(stamp not in seen,'unique actual section MF/MT/T');seen.add(stamp)
   if expected is not None:
    require(cursor<len(expected),'bounded prior first4 original inventory');e=expected[cursor];require(active['temperature_K']==e['temperature_K']and active['dimensions']==e['actual_LIST_index_dimensions']and active['LIST_records']==e['LIST_records'],'first4 original T/all LIST dimensions exact inventory')
   if active['mf']==6:cohort_mf6.append(active['mt'])
   ledger.append(dict(section_index_one_based=cursor+1,mat=row['mat'],mf=active['mf'],mt=active['mt'],nl=active['nl'],nz=active['nz'],energy_groups=370,temperature_K=active['temperature_K'],section_header_sha256=active['header_sha256'],LIST_records=active['LIST_records'],LIST_dimension_sequence_sha256=active['dimension_digest'].hexdigest(),incident_present_mask_hex=bytes(active['mask']).hex(),spectrum_LIST_present=active['spectrum']))
   if active['selected']:
    mt=active['mt'];require(mt not in sections,'unique oneT selected MF6');sections[mt]=dict(nz=1,nl=1,ng=370,actual_nz=active['nz'],actual_nl=active['nl'],records=active['records']);section_indexes.append(cursor+1)
   cursor+=1
  active=key=None
 with Path(p['path']).open('rb')as raw:
  require(identity(os.fstat(raw.fileno()))==p['identity'],'opened exact current original input')
  compressed=streamer.Compressed(raw,p,budget)if row['input_encoding']=='gzip'else None
  with streamer.gzip.GzipFile(fileobj=compressed,mode='rb')if compressed is not None else contextlib.nullcontext(raw)as decoded:
   reader=streamer.Lines(decoded,budget)
   while True:
    line=reader.next()
    if line is None:break
    text=line[:-1].decode('ascii');k=scalar.identity(text);mat,mf,mt=k
    if mf==0 or mt==0:
     require(active is None or k==(row['mat'],active['mf'],0),'explicit original SEND');close();boundaries[str(k)]=boundaries.get(str(k),0)+1;continue
    require(mat==row['mat'],'exact original material');h=scalar.fields(text)
    if key is None:
     key=k;require(mf in(1,3,5,6),'original declared GENDF families')
     if(mf,mt)==(1,451):grid_nz=scalar.integer(h[3]);require(grid_nz==row['original_expected_nz']and 1<=grid_nz<=30,'actual bounded MF1 dilution width')
     elif mf in(3,6):
      nl,nz,ng=scalar.integer(h[2]),scalar.integer(h[3]),scalar.integer(h[5]);require(1<=nl<=8 and nz in(1,grid_nz)and ng==370,'original actual MF3/MF6 dimensions')
      if expected is not None:
       require(cursor<len(expected),'bounded first4 original section count');e=expected[cursor];require((mat,mf,mt,nl,nz,ng)==(e['mat'],e['mf'],e['mt'],e['nl'],e['nz'],370)and hashlib.sha256(line).hexdigest()==e['section_header_sha256'],'first4 original full header')
      selected=mf==6 and(mt in MTS or 221<=mt<=250);active=dict(mf=mf,mt=mt,nl=nl,nz=nz,temperature_K=None,selected=selected,records={},dimensions=[],dimension_digest=hashlib.sha256(),mask=bytearray(370),spectrum=False,header_sha256=hashlib.sha256(line).hexdigest(),LIST_records=0)
     continue
    require(k==key,'explicit SEND before next section');npl=scalar.integer(h[4]);require(0<=npl<=88800,'bounded original LIST values');payload=[];payloadsha=hashlib.sha256()
    for _ in range((npl+5)//6):
     data=reader.next();require(data is not None and scalar.identity(data[:-1].decode('ascii'))==k,'complete original LIST payload identity');payloadsha.update(data);payload.extend(scalar.fields(data[:-1].decode('ascii')))
    payload=payload[:npl];require(len(payload)==npl,'complete original NPL')
    if(mf,mt)==(1,451):
     ng,ngg=scalar.integer(h[2]),scalar.integer(h[3]);require(ng==370 and ngg==0 and npl==1+grid_nz+ng+1+ngg+1,'actual generic original MF1 NPL dimensions');flush_temperature();i=len(grids);require(i<nt,'actual native grid count bound');sigma=payload[1:1+grid_nz];mesh=payload[1+grid_nz:2+grid_nz+ng];require(len(sigma)==grid_nz and all(v>0 for v in sigma)and len(set(sigma))==grid_nz and len(mesh)==371 and all(a<b for a,b in zip(mesh,mesh[1:]))and h[0]not in grids,'original finite sigma grid/ascending371/unique T');require(struct.pack('<f',h[0])==struct.pack('<f',row['original_source_deck_temperatures_K'][i]),'original deck temperature REAL32 word')
     grid=dict(original_temperature_index_one_based=i+1,temperature_K=h[0],sigma0_barn=sigma,ascending_energy_eV=mesh,raw_LIST_header_sha256=hashlib.sha256(line).hexdigest(),raw_grid_payload_sha256=payloadsha.hexdigest())
     if expected is not None:
      prior=inventory['original8_MF1_grids'][i];require(h[0]==prior['temperature_K']and grid['raw_LIST_header_sha256']==prior['raw_LIST_header_sha256']and grid['raw_grid_payload_sha256']==prior['raw_grid_payload_sha256'],'first4 original MF1 raw proof')
     grids.append(h[0]);continue
    if active is not None:
     ng2,lower,ig=[scalar.integer(h[i])for i in(2,3,5)];require(ng2>=1 and npl==ng2*active['nl']*active['nz']and 0<=ig<=370 and grid is not None and h[0]==grid['temperature_K'],'exact actual LIST dimensions and oneT cohort');require(active['temperature_K']in(None,h[0]),'single section temperature');active['temperature_K']=h[0];dims=[ig,lower,ng2,npl];active['dimension_digest'].update(struct.pack('<4i',*dims));active['LIST_records']+=1
     if expected is not None:active['dimensions'].append(dims)
     if ig==0:require(not active['spectrum'],'unique spectrum LIST');active['spectrum']=True
     else:require(active['mask'][ig-1]==0,'unique original incident LIST');active['mask'][ig-1]=1
     if active['selected']:
      require(ig not in active['records'],'unique selected incident/spectrum LIST');values=scalar.np.asarray(payload[::active['nl']*active['nz']],dtype='f8').reshape(ng2,1,1);active['records'][ig]=(lower,values)
   require(key is None,'complete final GENDF boundary');flush_temperature();require((expected is None or cursor==len(expected))and len(rows)==nt and len(grids)==nt,'complete actual sections/native grids');require(reader.bytes==row['original_ASCII_expected_size_bytes']and reader.digest.hexdigest()==row['original_ASCII_expected_sha256'],'whole original ASCII EOF SHA/size')
  if compressed is not None:require(compressed.read(1)==b''and compressed.bytes==p['size_bytes']and compressed.digest.hexdigest()==p['sha256'],'whole compressed primary EOF SHA/size')
  require(identity(os.fstat(raw.fileno()))==p['identity'],'final original input opened7')
 current(p);return dict(nuclide=row['nuclide'],SCI_role=row['SCI_role'],actual_complete_inventory_pin=row.get('actual_complete_inventory_pin'),current_original_input_full_pin=p,input_encoding=row['input_encoding'],actual_compressed_EOF_SHA256=None if compressed is None else compressed.digest.hexdigest(),actual_original_ASCII_EOF_SHA256=reader.digest.hexdigest(),actual_decompressed_bytes=reader.bytes,all_actual_MF3_MF6_sections_verified=cursor,actual_MF3_MF6_compact_inventory=ledger,actual_GENDF_boundary_counts=boundaries,actual_MF6_MTs=sorted(set(s['mt']for s in ledger if s['mf']==6)),temperature_comparisons=rows,original_formatter_already_applied=True,second_quantization_performed=False,Mo_historical_input_PF_invented=False,**FALSE)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--binding-pin',required=True);ap.add_argument('--expected-parent-pid',type=int,required=True);a=ap.parse_args();require(os.getppid()==a.expected_parent_pid and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in THREADS),'original owning parent/single-thread child');pb=json.loads(a.binding_pin);b=metadata(pb);require(b['schema']=='ALL34_ORIGINAL_ASCII_INFINITE_SCAT_EXECUTION_BINDING_V1'and b['original_caps']==CAPS and b['SCI1_and_SCI2_whole_PF_verified_by_original_parent_before_child']is True,'exact owning binding and both whole SCI preverification');budget=Budget(b['complete_joint_roots'],b['explicit_cumulative_metadata_file_pins']);budget.check();plan=metadata(b['control_plan_pin']);require(plan['original_caps']==CAPS and plan['complete_joint_roots']==b['complete_joint_roots'],'same cumulative plan');scalar=module(plan['original_scalar_helper_source_copy_pin'],'original_SCAT_scalar');streamer=module(plan['original_stream_helpers_copy_pin'],'original_SCAT_stream');helpers=module(plan['original_bounded_SCI_helpers_copy_pin'],'original_SCAT_SCI');results=[];science=[]
 for role in('SCI1','SCI2'):
  sci=helpers.BoundedSCI(plan['actual_current_'+role+'_pin'],budget.check)
  try:
   e=sci.lookup(sci.root,'ENERGY');require(e['kind']==2 and e['words']==371,'original stored ENERGY role');eraw=sci.raw(e['offset_words'],371);energy=dict(raw=eraw,values=struct.unpack('<371f',eraw));require(all(math.isfinite(v)for v in energy['values']),'finite original ENERGY')
   for row in plan['inputs']:
    if row['SCI_role']==role:budget.check();results.append(extract(row,scalar,streamer,budget.check,sci,energy))
   science.append(dict(role=role,current_SCI_pin=sci.p,original_SCI_ENERGY_leaf=e,original_SCI_ENERGY_raw_sha256=hashlib.sha256(eraw).hexdigest(),selective_SCI_read_bytes=sci.read_bytes,selective_SCI_directory_extents=sci.extents))
  finally:sci.close()
 for p in b['fixed_small_metadata_pins']:metadata(p)
 metadata(pb);budget.last=0;budget.check();out=Path(b['output_directory']);require(out.is_dir(),'owning output exists');exact=all(t['exact_infinite_P0_three_leaf_raw_words_equal']for r in results for t in r['temperature_comparisons']);nt=sum(len(r['temperature_comparisons'])for r in results);require(len(results)==plan['expected_nuclides']and nt==plan['expected_temperature_records'],'all34 native temperature coverage');report=out/'ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_EVIDENCE.json';value=dict(schema='ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_PRODUCER_COMPARISON_V1',status='ALL34_ORIGINAL_ASCII_234T_INFINITE_P0_RAW_WORDS_EQUAL'if exact else'ALL34_ORIGINAL_ASCII_INFINITE_P0_RAW_WORDS_MISMATCH',execution_binding_pin=pb,control_plan_pin=b['control_plan_pin'],source_freeze_pin=b['source_freeze_pin'],actual_current_SCI1_pin=plan['actual_current_SCI1_pin'],actual_current_SCI2_pin=plan['actual_current_SCI2_pin'],actual_extractions=results,compared_unique_nuclides=len(results),compared_temperature_records=nt,compared_original_leaf_records=3*nt,actual_infinite_P0_producer_all_nativeT_raw_words_equal=exact,selective_SCI_roles=science,original_caps=CAPS,native_engines_started=0,original_inputs_written=0,original_ASCII_files_written=0,dense_field_spool_files_written=0,scope=plan['scope'],**FALSE);write(report,value);budget.last=0;budget.check();print(json.dumps(dict(status=value['status'],report_pin=pin(report),**FALSE)),flush=True);require(exact,'actual original infinite P0 packed mismatch retained; no retry')
if __name__=='__main__':main()
