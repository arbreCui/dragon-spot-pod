"""Selected 21-channel GENDF operands; no multiplicity-completeness admission.

The original parser and matrix helper are copied whole and called unchanged.
One original archive is streamed at a time. Only one selected P0 matrix lives
at once; all retained matrices are independent uncompressed little-endian f8.
"""
import argparse,contextlib,hashlib,importlib.util,json,math,os,resource,stat,struct,sys,time
from pathlib import Path
CAPS={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'fresh_bytes':2147483648,'history_bytes':103079215104,'cold_reserve_bytes':20971764748,'metadata_reserve_bytes':67108864,'free_floor_bytes':8589934592,'threads':1,'children_at_once':1,'retries':0}
FALSE=dict(physics_qualified=False,scientific_accuracy_qualified=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,full_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,temperature_interpolation_replayed=False,current_SPH_MASK_context_applied=False,MT5_partition_qualified=False,fission_producer_replayed=False,reaction_exclusive_partition_qualified=False,original_evaluation_neutron_yield_branch_captured=False,MF6_GENDF_label_proves_original_processing_branch=False)
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
 raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode();require(len(raw)<16*2**20,'selected capture metadata16MiB bound')
 with Path(p).open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
def module(p,name):
 current(p);require(hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],'whole unchanged helper Source');spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current(p);return m
class Budget:
 def __init__(self,roots,explicit):
  require(len(roots)==60 and len(set(roots))==60 and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'exact inherited59 plus newoutput60 disjoint roots');self.roots=[Path(p)for p in roots];self.explicit=explicit;self.started=time.monotonic();self.last=0.0
 def check(self):
  now=time.monotonic();peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);require(now-self.started<600 and peak<512*2**20,'original child600/SELF512')
  if now-self.last<0.25:return
  total=0
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
  require(total+sum(unlinked.values())<2*2**30,'original cumulative2GiB and open-unlinked');self.last=time.monotonic()
def retained_channel(row,grid,mf3,mf6,scalar,out):
 np=scalar.np;mt=mf6['mt'];require(mf3['mt']==mt and mf3['temperature_K']==mf6['temperature_K']==grid['temperature_K']and mf3['nz']==mf6['nz']==1,'same original selected channel/cohort/NZ1')
 section=dict(nz=1,nl=1,ng=370,records=mf6['records']);matrix,flux=scalar.matrix(section);p0=matrix[0,0];ownflux=flux[0,0];spectrum=np.zeros(370,dtype='<f8')
 if 0 in mf6['records']:
  lower,data=mf6['records'][0];spectrum[lower-1:lower-1+len(data)]=data[:,0,0]
 a=np.asarray(mf3['mask'][::-1],dtype='u1');b=np.asarray(mf6['mask'][::-1],dtype='u1');common=(a!=0)&(b!=0);production=np.zeros(370,dtype='<f8')
 for ig in range(370):
  total=0.0
  for outgoing in range(370):total+=float(p0[ig,outgoing])
  production[ig]=total
 delta=np.zeros(370,dtype='<f8');delta[common]=production[common]-mf3['event'][common];ratio_mask=common&(mf3['event']!=0);ratio=np.zeros(370,dtype='<f8');ratio[ratio_mask]=production[ratio_mask]/mf3['event'][ratio_mask];zero_sigma_nonzero_production=common&(mf3['event']==0)&(production!=0)
 union=(a!=0)|(b!=0);mf3_only=(a!=0)&(b==0);mf6_only=(a==0)&(b!=0);reconstructed_delta=production-mf3['event'];reconstructed_ratio_mask=mf3['event']!=0;reconstructed_ratio=np.zeros(370,dtype='<f8');reconstructed_ratio[reconstructed_ratio_mask]=production[reconstructed_ratio_mask]/mf3['event'][reconstructed_ratio_mask];reconstructed_zero_event_nonzero_production=(mf3['event']==0)&(production!=0)
 require(bool(np.isfinite(p0).all())and bool(np.isfinite(production).all())and bool(np.isfinite(reconstructed_delta).all())and bool(np.isfinite(reconstructed_ratio).all()),'finite original selected operands and scalar diagnostics, no fitted correction')
 def raw_list_operands(section):
  arrays=[value[1][:,0,0]for value in section['records'].values()];ranges=[];cursor=0
  for values in arrays:ranges.append([cursor,cursor+len(values)]);cursor+=len(values)
  require(len(arrays)==len(section['dimensions'])and all(len(values)==dimension[2]for values,dimension in zip(arrays,section['dimensions'])),'exact decoded P0 raw span lengths/original LIST NG2')
  flat=np.concatenate(arrays).astype('<f8',copy=False);require(flat.dtype.str=='<f8'and flat.nbytes==cursor*8,'literal original parsed binary64 P0 numeric dtype/source span bound')
  return flat,np.asarray(ranges,dtype='<i4')
 raw_mf3,ranges_mf3=raw_list_operands(mf3);raw_mf6,ranges_mf6=raw_list_operands(mf6)
 target=out/(row['nuclide']+'_MT'+str(mt)+'_T'+format(grid['original_temperature_index_one_based'],'02d')+'_selected_P0_operands.npz')
 require(not os.path.lexists(target),'once unique selected channel/nativeT output')
 with target.open('xb')as stream:
  np.savez(stream,MF3_original_P0_LIST_numeric_values=raw_mf3,MF6_original_P0_LIST_numeric_values=raw_mf6,MF3_P0_LIST_numeric_start_end=ranges_mf3,MF6_P0_LIST_numeric_start_end=ranges_mf6,MF6_P0_production_matrix=np.asarray(p0,dtype='<f8'),MF3_event_vector=mf3['event'],MF3_own_flux=mf3['flux'],MF6_own_flux=np.asarray(ownflux,dtype='<f8'),MF6_P0_spectrum=spectrum,MF3_incident_present_mask=a,MF6_incident_present_mask=b,observed_common_incident_mask=common.astype('u1'),observed_union_incident_mask=union.astype('u1'),MF3_only_incident_mask=mf3_only.astype('u1'),MF6_only_incident_mask=mf6_only.astype('u1'),original_zero_initialized_reconstructed_production_minus_event=reconstructed_delta,original_zero_initialized_reconstructed_production_to_nonzero_event_ratio=reconstructed_ratio,reconstructed_nonzero_event_ratio_mask=reconstructed_ratio_mask.astype('u1'),reconstructed_zero_event_nonzero_production_mask=reconstructed_zero_event_nonzero_production.astype('u1'),MF6_P0_outgoing_order_row_sums=production,observed_production_minus_event=delta,observed_production_to_nonzero_event_ratio=ratio,observed_nonzero_event_ratio_mask=ratio_mask.astype('u1'),observed_zero_event_nonzero_production_mask=zero_sigma_nonzero_production.astype('u1'),MF3_LIST_dimensions=np.asarray(mf3['dimensions'],dtype='<i4'),MF6_LIST_dimensions=np.asarray(mf6['dimensions'],dtype='<i4'),original_MF1_sigma0_barn=np.asarray(grid['sigma0_barn'],dtype='<f8'),original_MF1_ascending_energy_eV=np.asarray(grid['ascending_energy_eV'],dtype='<f8'))
  stream.flush();os.fsync(stream.fileno())
 require(target.stat().st_size<2*2**20,'one selected operand NPZ2MiB hard bound')
 evidence=dict(nuclide=row['nuclide'],MT=mt,SCI_role=row['SCI_role'],temperature_K=grid['temperature_K'],original_temperature_index_one_based=grid['original_temperature_index_one_based'],original_declared_deck_temperature_K=row['original_source_deck_temperatures_K'][grid['original_temperature_index_one_based']-1],decoded_temperature_REAL32_hex=struct.pack('<f',grid['temperature_K']).hex(),original_MF3_nl=mf3['nl'],original_MF6_nl=mf6['nl'],actual_nz=1,original_MF3_compact_section_metadata=mf3['metadata'],original_MF6_compact_section_metadata=mf6['metadata'],original_MF3_selected_LIST_provenance=mf3['provenance'],original_MF6_selected_P0_LIST_provenance=mf6['provenance'],retained_operands_full_pin=pin(target),retained_matrix_dtype='<f8',matrix_axes=['descending_incident','descending_outgoing'],retained_matrix_shape=[370,370],original_fmatr_scalar_matrix_called_unchanged=True,original_fvect_first_flux_second_event_rows=True,own_flux_division_performed=False,second_formatter_quantization_performed=False,original_missing_LIST_promoted_to_observed_zero=False,MF6_spectrum_LIST_observed=mf6['spectrum'],raw_selected_LIST_numeric_arrays_duplicated=True,raw_selected_LIST_numbers_provenance_retained=True,MF3_observed_incident_rows=int(a.sum()),MF6_observed_incident_rows=int(b.sum()),jointly_observed_incident_rows=int(common.sum()),MF3_observed_event_nonzero_rows=int(np.count_nonzero(mf3['event'][a!=0])),jointly_observed_MF3_event_nonzero_rows=int(np.count_nonzero(mf3['event'][common])),MF6_observed_production_nonzero_rows=int(np.count_nonzero(production[b!=0])),jointly_observed_MF6_production_nonzero_rows=int(np.count_nonzero(production[common])),jointly_observed_production_minus_event_nonzero_rows=int(np.count_nonzero(delta[common])),jointly_observed_production_minus_event_max_abs=float(np.abs(delta[common]).max())if common.any()else None,negative_P0_matrix_entries=int(np.count_nonzero(p0<0)),nonzero_P0_matrix_entries=int(np.count_nonzero(p0)),production_minus_event_is_acceptance_test=False,selected_capture_only=True,**FALSE)
 evidence.update(reconstructed_vector_matrix_initialization_matches_original_FVECT_FMATR=True,reconstructed_absent_incident_rows_not_called_observed_zero=True,union_observed_incident_rows=int(union.sum()),MF3_only_incident_rows=int(mf3_only.sum()),MF6_only_incident_rows=int(mf6_only.sum()),MF3_only_nonzero_event_rows=int(scalar.np.count_nonzero(mf3['event'][mf3_only])),MF6_only_nonzero_production_rows=int(scalar.np.count_nonzero(production[mf6_only])),reconstructed_all370_production_minus_event_nonzero_rows=int(scalar.np.count_nonzero(reconstructed_delta)),reconstructed_all370_production_minus_event_max_abs=float(scalar.np.abs(reconstructed_delta).max()),reconstructed_all370_production_minus_event_negative_rows=int(scalar.np.count_nonzero(reconstructed_delta<0)),reconstructed_all370_production_minus_event_positive_rows=int(scalar.np.count_nonzero(reconstructed_delta>0)),reconstructed_all370_zero_event_nonzero_production_rows=int(reconstructed_zero_event_nonzero_production.sum()),reconstructed_nonzero_event_ratio_rows=int(reconstructed_ratio_mask.sum()),jointly_observed_nonzero_event_ratio_rows=int(ratio_mask.sum()),jointly_observed_nonzero_event_ratio_min=float(ratio[ratio_mask].min())if ratio_mask.any()else None,jointly_observed_nonzero_event_ratio_max=float(ratio[ratio_mask].max())if ratio_mask.any()else None,jointly_observed_zero_event_nonzero_production_rows=int(zero_sigma_nonzero_production.sum()),fixed_neutron_multiplicity_assumed=False,raw_original_matrix_before_Mo_ipflag1_diagonal_lumping=True)
 del matrix,flux,p0,ownflux,production,delta,ratio,reconstructed_delta,reconstructed_ratio,raw_mf3,raw_mf6
 return evidence
def extract(selected,scalar,streamer,budget,out):
 row=selected['input'];expected=selected['all_compact_metadata_sections'];selected_mts=selected['selected_MTs'];p=row['current_original_input_full_pin'];current(p);key=active=grid=None;cursor=0;grid_nz=None;grids=[];pending={};channels=[];boundaries={}
 def cohort_closed():require(not pending,'every observed selected MF3 paired with same original cohort MF6, no absence substitution')
 def close():
  nonlocal active,key,cursor
  if active is not None:
   require(cursor<len(expected),'original compact section count bound');e=expected[cursor]
   require((active['mf'],active['mt'],active['nl'],active['nz'],active['temperature_K'])==(e['mf'],e['mt'],e['nl'],e['nz'],e['temperature_K'])and active['header_sha256']==e['section_header_sha256']and active['LIST_records']==e['LIST_records']and active['dimension_digest'].hexdigest()==e['LIST_dimension_sequence_sha256']and bytes(active['mask']).hex()==e['incident_present_mask_hex']and active['spectrum']==e['spectrum_LIST_present'],'all original compact section identities/dimensions/masks/header agree actual all34 ledger')
   if active['selected']:
    active['metadata']=e
    if active['mf']==3:require(active['mt']not in pending,'one original MF3 per selected channel/cohort');pending[active['mt']]=active
    else:
     require(active['mt']in pending,'original MF3 precedes same-channel MF6');channels.append(retained_channel(row,grid,pending.pop(active['mt']),active,scalar,out));budget()
   cursor+=1
  active=key=None
 with Path(p['path']).open('rb')as raw:
  require(identity(os.fstat(raw.fileno()))==p['identity'],'opened current original primary7');compressed=streamer.Compressed(raw,p,budget)if row['input_encoding']=='gzip'else None
  with streamer.gzip.GzipFile(fileobj=compressed,mode='rb')if compressed is not None else contextlib.nullcontext(raw)as decoded:
   reader=streamer.Lines(decoded,budget)
   while True:
    line=reader.next()
    if line is None:break
    text=line[:-1].decode('ascii');k=scalar.identity(text);mat,mf,mt=k
    if mf==0 or mt==0:
     require(active is None or k==(row['mat'],active['mf'],0),'explicit original SEND');close();boundaries[str(k)]=boundaries.get(str(k),0)+1;continue
    require(mat==row['mat'],'original selected isotope MAT');h=scalar.fields(text)
    if key is None:
     key=k;require(mf in(1,3,5,6),'original GENDF LIST families')
     if(mf,mt)==(1,451):grid_nz=scalar.integer(h[3]);require(grid_nz==row['original_expected_nz'],'original MF1 dilution width')
     elif mf in(3,6):
      nl,nz,ng=scalar.integer(h[2]),scalar.integer(h[3]),scalar.integer(h[5]);require(1<=nl<=8 and nz in(1,grid_nz)and ng==370,'original complete reaction section dimensions');picked=mt in selected_mts
      if picked:require(nz==1 and nl==(1 if mf==3 or row['SCI_role']=='SCI2'else 2),'selected actual NZ1/NL declaration')
      active=dict(mf=mf,mt=mt,nl=nl,nz=nz,temperature_K=None,selected=picked,records={},dimensions=[],provenance=[],dimension_digest=hashlib.sha256(),mask=bytearray(370),spectrum=False,header_sha256=hashlib.sha256(line).hexdigest(),LIST_records=0)
      if picked and mf==3:active.update(event=scalar.np.zeros(370,dtype='<f8'),flux=scalar.np.zeros(370,dtype='<f8'))
     continue
    require(k==key,'explicit SEND before next section');npl=scalar.integer(h[4]);require(0<=npl<=88800,'original LIST bound');payload=[];payloadsha=hashlib.sha256()
    for _ in range((npl+5)//6):
     data=reader.next();require(data is not None and scalar.identity(data[:-1].decode('ascii'))==k,'complete original LIST data identity');payloadsha.update(data);payload.extend(scalar.fields(data[:-1].decode('ascii')))
    payload=payload[:npl];require(len(payload)==npl,'complete original NPL')
    if(mf,mt)==(1,451):
     cohort_closed();ng,ngg=scalar.integer(h[2]),scalar.integer(h[3]);require(ng==370 and ngg==0 and npl==1+grid_nz+ng+1+ngg+1,'original MF1 dimensions');i=len(grids);require(i<len(row['original_source_deck_temperatures_K'])and struct.pack('<f',h[0])==struct.pack('<f',row['original_source_deck_temperatures_K'][i])and h[0]not in grids,'original declared temperature REAL32 word/unique actual cohort');sigma=payload[1:1+grid_nz];mesh=payload[1+grid_nz:2+grid_nz+ng];require(all(v>0 for v in sigma)and len(set(sigma))==grid_nz and len(mesh)==371 and all(a<b for a,b in zip(mesh,mesh[1:])),'original sigma0/ascending371 mesh');grid=dict(temperature_K=h[0],original_temperature_index_one_based=i+1,sigma0_barn=sigma,ascending_energy_eV=mesh);grids.append(h[0]);continue
    if active is not None:
     ng2,lower,ig=[scalar.integer(h[j])for j in(2,3,5)];require(ng2>=1 and npl==ng2*active['nl']*active['nz']and 0<=ig<=370 and grid is not None and h[0]==grid['temperature_K'],'original LIST dimensions/same literal cohort');require(active['temperature_K']in(None,h[0]),'single reaction temperature');active['temperature_K']=h[0];dims=[ig,lower,ng2,npl];active['dimension_digest'].update(struct.pack('<4i',*dims));active['LIST_records']+=1
     if ig==0:require(not active['spectrum'],'unique spectrum LIST');active['spectrum']=True
     else:require(active['mask'][ig-1]==0,'unique incident LIST');active['mask'][ig-1]=1
     if active['selected']:
      active['dimensions'].append(dims);p0=scalar.np.asarray(payload[::active['nl']*active['nz']],dtype='<f8');active['provenance'].append(dict(dimensions=dims,raw_header_ascii=text,raw_header_sha256=hashlib.sha256(line).hexdigest(),whole_original_LIST_payload_ASCII_sha256=payloadsha.hexdigest(),whole_original_LIST_numeric_f8_sha256=hashlib.sha256(scalar.np.asarray(payload,dtype='<f8').tobytes()).hexdigest(),whole_original_LIST_numeric_values=npl,selected_P0_LIST_numeric_dtype='<f8',original_payload_NL=active['nl'],original_payload_NZ=active['nz'],selected_P0_stride=active['nl']*active['nz'],selected_P0_LIST_numeric_f8_sha256=hashlib.sha256(p0.tobytes()).hexdigest(),selected_P0_LIST_numeric_values=ng2))
      if mf==3:
       require(ig>0 and ng2==2,'FVECT exact one flux row and one event row');active['flux'][370-ig]=p0[0];active['event'][370-ig]=p0[1];active['records'][ig]=(lower,p0.reshape(ng2,1,1))
      else:
       require(ig not in active['records']and ng2<=371,'unique selected original370 matrix LIST NG2<=371');active['records'][ig]=(lower,p0.reshape(ng2,1,1))
   require(key is None,'complete original final boundary');cohort_closed();require(cursor==len(expected)and len(grids)==len(row['original_source_deck_temperatures_K'])and len(channels)==len(grids)*len(selected_mts),'exact selected archive/cohort/channel coverage');require(reader.bytes==row['original_ASCII_expected_size_bytes']and reader.digest.hexdigest()==row['original_ASCII_expected_sha256'],'whole original ASCII EOF SHA/size')
  if compressed is not None:require(compressed.read(1)==b''and compressed.bytes==p['size_bytes']and compressed.digest.hexdigest()==p['sha256'],'whole compressed primary EOF SHA/size')
  require(identity(os.fstat(raw.fileno()))==p['identity'],'final opened original primary7')
 current(p);return dict(nuclide=row['nuclide'],SCI_role=row['SCI_role'],current_original_input_full_pin=p,selected_MTs=selected_mts,actual_original_ASCII_EOF_sha256=reader.digest.hexdigest(),actual_decompressed_bytes=reader.bytes,actual_compressed_EOF_sha256=None if compressed is None else compressed.digest.hexdigest(),all_actual_MF3_MF6_compact_sections_verified=cursor,actual_native_temperature_records=len(grids),actual_selected_channel_temperature_records=channels,actual_GENDF_boundary_counts=boundaries,selected_capture_only=True,**FALSE)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--binding-pin',required=True);ap.add_argument('--expected-parent-pid',type=int,required=True);a=ap.parse_args();require(os.getppid()==a.expected_parent_pid and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in THREADS),'own original single-thread/unoptimized/unprofiled child');pb=json.loads(a.binding_pin);b=metadata(pb);require(b['schema']=='EXTRA21_REACTION_CAPTURE_EXECUTION_BINDING_V1'and b['original_caps']==CAPS and b['selected_original_primary_whole_PF_verified_by_original_parent_before_child']is True,'same owning binding/parent primary fullPF');budget=Budget(b['complete_joint_roots'],b['explicit_cumulative_metadata_file_pins']);budget.check();plan=metadata(b['control_plan_pin']);require(plan['original_caps']==CAPS and plan['complete_joint_roots']==b['complete_joint_roots'],'same original caps/cumulative60');scalar=module(plan['original_scalar_helper_source_copy_pin'],'original_extra21_scalar');streamer=module(plan['original_stream_helpers_copy_pin'],'original_extra21_stream');out=Path(b['output_directory']);require(out.is_dir(),'owning output exists');results=[]
 for selected in plan['selected_inputs']:budget.check();results.append(extract(selected,scalar,streamer,budget.check,out))
 for p in b['fixed_small_metadata_pins']:metadata(p)
 for p in (plan['original_scalar_helper_source_copy_pin'],plan['original_stream_helpers_copy_pin']):current(p);require(hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],'whole actual child imported Source unchanged after capture')
 for selected in plan['selected_inputs']:current(selected['input']['current_original_input_full_pin'])
 metadata(pb);budget.last=0;budget.check();pairs=[c for r in results for c in r['actual_selected_channel_temperature_records']];stamps=[(c['nuclide'],c['MT'],c['temperature_K'])for c in pairs];require(len(results)==17 and len(pairs)==131 and len(set(stamps))==131 and len({(c['nuclide'],c['MT'])for c in pairs})==21 and sum(r['actual_decompressed_bytes']for r in results)==92876787,'complete exact selected17/21/131 original archive scope');report=out/'ACTUAL_EXTRA21_ORIGINAL_ASCII_EVENT_PRODUCTION_CAPTURE.json';value=dict(schema='ACTUAL_EXTRA21_ORIGINAL_ASCII_EVENT_PRODUCTION_CAPTURE_V1',status='SELECTED21_CHANNEL_131T_MF3_EVENT_MF6_P0_OPERANDS_CAPTURED_ONLY',execution_binding_pin=pb,control_plan_pin=b['control_plan_pin'],source_freeze_pin=b['source_freeze_pin'],actual_extractions=results,captured_nuclides=17,captured_channel_pairs=21,captured_channel_temperature_records=131,captured_MF3_MF6_sections=262,retained_P0_dense_matrix_payload_bytes=143471200,native_engines_started=0,original_inputs_written=0,original_ASCII_files_written=0,original_caps=CAPS,selected_capture_only=True,**FALSE);write(report,value);budget.last=0;budget.check();print(json.dumps(dict(status=value['status'],report_pin=pin(report),**FALSE)),flush=True)
if __name__=='__main__':main()
