"""Root-only independent reconstruction from new captured P0 LIST operands.

No old science input and no capture-worker/scalar-helper import is permitted.
Original FVECT/FMATR associations are implemented directly with scalar f8
operations. Every reconstructed stored array must match bytes with zero bits.
This is captured-operand replay, never reaction/physics/AAA/ABA admission.
"""
import argparse,hashlib,json,math,os,re,resource,stat,struct,sys,time,zipfile
from pathlib import Path
import numpy as np
CAPS={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'fresh_bytes':2147483648,'history_bytes':103079215104,'cold_reserve_bytes':20971764748,'metadata_reserve_bytes':67108864,'free_floor_bytes':8589934592,'threads':1,'children_at_once':1,'retries':0}
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
FALSE=dict(physics_qualified=False,scientific_accuracy_qualified=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,MT5_partition_qualified=False,fission_producer_replayed=False,reaction_exclusive_partition_qualified=False,temperature_interpolation_replayed=False,current_SPH_MASK_context_applied=False,unreduced_reference_qualified=False,full_reference_qualified=False,original_evaluation_neutron_yield_branch_captured=False,MF6_GENDF_label_proves_original_processing_branch=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
MEMBERS=('MF3_original_P0_LIST_numeric_values','MF6_original_P0_LIST_numeric_values','MF3_P0_LIST_numeric_start_end','MF6_P0_LIST_numeric_start_end','MF6_P0_production_matrix','MF3_event_vector','MF3_own_flux','MF6_own_flux','MF6_P0_spectrum','MF3_incident_present_mask','MF6_incident_present_mask','observed_common_incident_mask','observed_union_incident_mask','MF3_only_incident_mask','MF6_only_incident_mask','original_zero_initialized_reconstructed_production_minus_event','original_zero_initialized_reconstructed_production_to_nonzero_event_ratio','reconstructed_nonzero_event_ratio_mask','reconstructed_zero_event_nonzero_production_mask','MF6_P0_outgoing_order_row_sums','observed_production_minus_event','observed_production_to_nonzero_event_ratio','observed_nonzero_event_ratio_mask','observed_zero_event_nonzero_production_mask','MF3_LIST_dimensions','MF6_LIST_dimensions','original_MF1_sigma0_barn','original_MF1_ascending_energy_eV')
PROVENANCE_KEYS={'MF3':'original_MF3_selected_LIST_provenance','MF6':'original_MF6_selected_P0_LIST_provenance'}
CONTEXTS=('MF3_original_P0_LIST_numeric_values','MF6_original_P0_LIST_numeric_values','MF3_P0_LIST_numeric_start_end','MF6_P0_LIST_numeric_start_end','MF3_LIST_dimensions','MF6_LIST_dimensions','original_MF1_sigma0_barn','original_MF1_ascending_energy_eV')
DERIVED=tuple(n for n in MEMBERS if n not in CONTEXTS)
def require(ok,message):
 if type(ok)is not bool or not ok:raise RuntimeError(message)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();compiler=q==Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and p['identity'][3]==2 and s.st_nlink==2;require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and(s.st_nlink==1 or compiler)and identity(s)==p['identity']and s.st_size==p['size_bytes'],'exact ordinary current7')
def metadata(p):
 current(p);require(p['size_bytes']<8*2**20,'bounded new metadata');raw=Path(p['path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==p['sha256'],'whole new metadata SHA');current(p);return json.loads(raw)
def pin(q):
 q=Path(q);s=q.lstat()
 with q.open('rb')as f:digest=hashlib.file_digest(f,'sha256').hexdigest();require(identity(os.fstat(f.fileno()))==identity(s),'opened new output7')
 p=dict(path=str(q),sha256=digest,size_bytes=s.st_size,identity=identity(s));current(p);return p
def write(q,v):
 raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode();require(len(raw)<8*2**20,'independent child report8MiB hard bound')
 with Path(q).open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
class Budget:
 def __init__(self,roots,explicit):
  require(len(roots)==62 and len(set(roots))==62 and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'complete inherited61 plus freshthinreplayOUT62');self.roots=[Path(q)for q in roots];self.explicit=explicit;self.started=time.monotonic();self.last=0.0
 def check(self):
  now=time.monotonic();peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);require(now-self.started<600 and peak<512*2**20,'original child600/SELF512')
  if now-self.last<0.25:return
  total=0
  for root in self.roots:
   if not root.exists():continue
   for q in root.rglob('*'):
    s=q.lstat();require(not stat.S_ISLNK(s.st_mode),'no cumulative namespace alias')
    if stat.S_ISREG(s.st_mode):total+=s.st_size
  nodes=set()
  for p in self.explicit:
   current(p);node=tuple(p['identity'][:2]);require(node not in nodes,'distinct explicit metadata inode');nodes.add(node)
   if not any(Path(p['path']).is_relative_to(root)for root in self.roots):total+=p['size_bytes']
  unlinked={}
  for fd in os.listdir('/dev/fd'):
   try:s=os.fstat(int(fd))
   except(ValueError,OSError):continue
   if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
  require(total+sum(unlinked.values())<2*2**30,'original cumulative2GiB including open-unlinked');self.last=time.monotonic()
def exact_array(name,array,dtype,shape):
 require(isinstance(array,np.ndarray)and array.dtype.str==dtype and list(array.shape)==shape and array.flags.c_contiguous,name+': exact dtype/shape/order')
 if dtype=='<f8':require(bool(np.isfinite(array).all()),name+': finite parsed f8')
 elif dtype=='|u1':require(bool(((array==0)|(array==1)).all()),name+': literal present-mask01')
 return array
def zero_bits(name,actual,expected):
 require(actual.dtype.str==expected.dtype.str and actual.shape==expected.shape,name+': reconstructed type/shape')
 a=actual.tobytes(order='C');b=expected.tobytes(order='C');words=actual.size;itemsize=actual.dtype.itemsize;different=0;bits=0;samples=[]
 if a!=b:
  for i in range(words):
   x=a[i*itemsize:(i+1)*itemsize];y=b[i*itemsize:(i+1)*itemsize]
   if x!=y:
    different+=1;bits+=sum((u^v).bit_count()for u,v in zip(x,y))
    if len(samples)<8:samples.append(dict(word_one_based=i+1,captured_hex=x.hex(),reconstructed_hex=y.hex()))
 return dict(array_name=name,dtype=actual.dtype.str,shape=list(actual.shape),compared_values=int(words),different_values=different,different_bits=bits,exact_bytes_equal=a==b,captured_bytes_sha256=hashlib.sha256(a).hexdigest(),reconstructed_bytes_sha256=hashlib.sha256(b).hexdigest(),bounded_mismatch_samples=samples)
def raw_records(role,arrays,evidence):
 flat=exact_array(role+'_raw',arrays[role+'_original_P0_LIST_numeric_values'],'<f8',[arrays[role+'_original_P0_LIST_numeric_values'].size]);dimensions=arrays[role+'_LIST_dimensions'];ranges=arrays[role+'_P0_LIST_numeric_start_end'];n=len(evidence[PROVENANCE_KEYS[role]]);exact_array(role+'_dimensions',dimensions,'<i4',[n,4]);exact_array(role+'_ranges',ranges,'<i4',[n,2]);require(n==evidence['original_'+role+'_compact_section_metadata']['LIST_records'],'original selected LIST count matches canonical captured section');cursor=0;records=[];seen=set();dimension_digest=hashlib.sha256();incident_mask=bytearray(370);spectrum_present=False;original_nl=evidence['original_'+role+'_nl'];require(original_nl==(1 if role=='MF3'or evidence['SCI_role']=='SCI2'else 2)and evidence['actual_nz']==1,'exact selected original NL/NZ1')
 for i,(dimension,span,proof)in enumerate(zip(dimensions,ranges,evidence[PROVENANCE_KEYS[role]])):
  ig,lower,ng2,npl=map(int,dimension);start,end=map(int,span);require(start==cursor and end-start==ng2 and end<=flat.size and 1<=ng2<=371 and npl==ng2*original_nl and list(map(int,dimension))==proof['dimensions'],'original P0 span/dimension/NPL association');require(ig not in seen and 0<=ig<=370,'unique original selected LIST IG');seen.add(ig);values=flat[start:end];numeric_sha=hashlib.sha256(values.tobytes()).hexdigest();require(proof['selected_P0_LIST_numeric_dtype']=='<f8'and proof['original_payload_NL']==original_nl and proof['original_payload_NZ']==1 and proof['selected_P0_stride']==original_nl and proof['selected_P0_LIST_numeric_values']==ng2 and numeric_sha==proof['selected_P0_LIST_numeric_f8_sha256'],'original retained decoded P0 numeric hash/stride provenance')
  header=proof['raw_header_ascii'];require(type(header)is str and len(header)==80 and hashlib.sha256((header+'\n').encode('ascii')).hexdigest()==proof['raw_header_sha256'],'new retained original LIST header exact80 ASCII hash')
  h=[]
  for column in range(6):
   field=header[column*11:(column+1)*11].strip();value=float(re.sub(r'(?<=[0-9.])([+-][0-9]+)$',r'e\1',field))if field else 0.0;require(math.isfinite(value),'finite retained original LIST header');h.append(value)
  canonical=evidence['original_'+role+'_compact_section_metadata'];require((int(header[66:70]),int(header[70:72]),int(header[72:75]))==(canonical['mat'],canonical['mf'],evidence['MT'])and h[0]==evidence['temperature_K']and all(h[j]==int(h[j])for j in(2,3,4,5))and [int(h[5]),int(h[3]),int(h[2]),int(h[4])]==[ig,lower,ng2,npl],'new original header exact MF/MT/T/LIST dimensions')
  require(proof['whole_original_LIST_numeric_values']==npl,'original full numeric payload count kept separately from P0 count')
  if original_nl==1:require(numeric_sha==proof['whole_original_LIST_numeric_f8_sha256'],'NL1 retained P0 contains all original numeric columns; hash exact')
  dimension_digest.update(struct.pack('<4i',ig,lower,ng2,npl))
  if ig==0:spectrum_present=True
  else:incident_mask[ig-1]=1
  records.append((ig,lower,values));cursor=end
 canonical=evidence['original_'+role+'_compact_section_metadata'];require(cursor==flat.size and dimension_digest.hexdigest()==canonical['LIST_dimension_sequence_sha256']and bytes(incident_mask).hex()==canonical['incident_present_mask_hex']and spectrum_present==canonical['spectrum_LIST_present'],'all captured P0 values/order/dimensions/masks/spectrum exact canonical section metadata');return records
def reconstruct(records3,records6):
 event=np.zeros(370,dtype='<f8');flux3=np.zeros(370,dtype='<f8');flux6=np.zeros(370,dtype='<f8');matrix=np.zeros((370,370),dtype='<f8');spectrum=np.zeros(370,dtype='<f8');mask3=np.zeros(370,dtype='u1');mask6=np.zeros(370,dtype='u1')
 for ig,lower,data in records3:
  require(1<=ig<=370 and len(data)==2,'original FVECT oneflux/oneevent P0 LIST');g=370-ig;flux3[g]=data[0];event[g]=data[1];mask3[g]=1
 for ig,lower,data in records6:
  if ig==0:
   require(1<=lower and lower+len(data)-1<=370,'original FMATR spectrum bounds')
   for k in range(len(data)):spectrum[lower-1+k]=data[k]
   continue
  g=370-ig;flux6[g]=data[0];mask6[g]=1
  for k in range(1,len(data)):
   if lower!=0:
    require(1<=lower and lower+len(data)-2<=370,'original FMATR direct outgoing bounds');outgoing=370-(lower+k-1);matrix[g,outgoing]=float(matrix[g,outgoing])+float(data[k])
   else:
    for outgoing in range(370):
     product=float(spectrum[369-outgoing])*float(data[k]);matrix[g,outgoing]=float(matrix[g,outgoing])+product
 production=np.zeros(370,dtype='<f8')
 for g in range(370):
  total=0.0
  for outgoing in range(370):total+=float(matrix[g,outgoing])
  production[g]=total
 common=(mask3!=0)&(mask6!=0);union=(mask3!=0)|(mask6!=0);only3=(mask3!=0)&(mask6==0);only6=(mask3==0)&(mask6!=0);delta=np.zeros(370,dtype='<f8');ratio=np.zeros(370,dtype='<f8');ratio_mask=common&(event!=0);recon_delta=np.zeros(370,dtype='<f8');recon_ratio=np.zeros(370,dtype='<f8');recon_ratio_mask=event!=0
 for g in range(370):
  recon_delta[g]=float(production[g])-float(event[g])
  if common[g]:delta[g]=float(production[g])-float(event[g])
  if ratio_mask[g]:ratio[g]=float(production[g])/float(event[g])
  if recon_ratio_mask[g]:recon_ratio[g]=float(production[g])/float(event[g])
 return dict(MF6_P0_production_matrix=matrix,MF3_event_vector=event,MF3_own_flux=flux3,MF6_own_flux=flux6,MF6_P0_spectrum=spectrum,MF3_incident_present_mask=mask3,MF6_incident_present_mask=mask6,observed_common_incident_mask=common.astype('u1'),observed_union_incident_mask=union.astype('u1'),MF3_only_incident_mask=only3.astype('u1'),MF6_only_incident_mask=only6.astype('u1'),original_zero_initialized_reconstructed_production_minus_event=recon_delta,original_zero_initialized_reconstructed_production_to_nonzero_event_ratio=recon_ratio,reconstructed_nonzero_event_ratio_mask=recon_ratio_mask.astype('u1'),reconstructed_zero_event_nonzero_production_mask=((event==0)&(production!=0)).astype('u1'),MF6_P0_outgoing_order_row_sums=production,observed_production_minus_event=delta,observed_production_to_nonzero_event_ratio=ratio,observed_nonzero_event_ratio_mask=ratio_mask.astype('u1'),observed_zero_event_nonzero_production_mask=(common&(event==0)&(production!=0)).astype('u1'))
def scalar_statistics(v):
 event=v['MF3_event_vector'];production=v['MF6_P0_outgoing_order_row_sums'];matrix=v['MF6_P0_production_matrix'];a=v['MF3_incident_present_mask']!=0;b=v['MF6_incident_present_mask']!=0;common=a&b;union=a|b;only3=a&~b;only6=~a&b;delta=v['observed_production_minus_event'];recon_delta=v['original_zero_initialized_reconstructed_production_minus_event'];ratio=v['observed_production_to_nonzero_event_ratio'];ratio_mask=v['observed_nonzero_event_ratio_mask']!=0
 return dict(MF3_observed_incident_rows=int(a.sum()),MF6_observed_incident_rows=int(b.sum()),jointly_observed_incident_rows=int(common.sum()),MF3_observed_event_nonzero_rows=int(np.count_nonzero(event[a])),jointly_observed_MF3_event_nonzero_rows=int(np.count_nonzero(event[common])),MF6_observed_production_nonzero_rows=int(np.count_nonzero(production[b])),jointly_observed_MF6_production_nonzero_rows=int(np.count_nonzero(production[common])),jointly_observed_production_minus_event_nonzero_rows=int(np.count_nonzero(delta[common])),jointly_observed_production_minus_event_max_abs=float(np.abs(delta[common]).max())if common.any()else None,negative_P0_matrix_entries=int(np.count_nonzero(matrix<0)),nonzero_P0_matrix_entries=int(np.count_nonzero(matrix)),union_observed_incident_rows=int(union.sum()),MF3_only_incident_rows=int(only3.sum()),MF6_only_incident_rows=int(only6.sum()),MF3_only_nonzero_event_rows=int(np.count_nonzero(event[only3])),MF6_only_nonzero_production_rows=int(np.count_nonzero(production[only6])),reconstructed_all370_production_minus_event_nonzero_rows=int(np.count_nonzero(recon_delta)),reconstructed_all370_production_minus_event_max_abs=float(np.abs(recon_delta).max()),reconstructed_all370_production_minus_event_negative_rows=int(np.count_nonzero(recon_delta<0)),reconstructed_all370_production_minus_event_positive_rows=int(np.count_nonzero(recon_delta>0)),reconstructed_all370_zero_event_nonzero_production_rows=int(np.count_nonzero(v['reconstructed_zero_event_nonzero_production_mask'])),reconstructed_nonzero_event_ratio_rows=int(np.count_nonzero(v['reconstructed_nonzero_event_ratio_mask'])),jointly_observed_nonzero_event_ratio_rows=int(ratio_mask.sum()),jointly_observed_nonzero_event_ratio_min=float(ratio[ratio_mask].min())if ratio_mask.any()else None,jointly_observed_nonzero_event_ratio_max=float(ratio[ratio_mask].max())if ratio_mask.any()else None,jointly_observed_zero_event_nonzero_production_rows=int(np.count_nonzero(v['observed_zero_event_nonzero_production_mask'])))
def compare_scalar_metadata(actual,evidence):
 results=[]
 for key,value in actual.items():
  expected=evidence[key]
  if type(value)is float:equal=type(expected)is float and struct.pack('<d',value)==struct.pack('<d',expected)
  else:equal=type(value)is type(expected)and value==expected
  results.append(dict(key=key,reconstructed=value,captured_report=expected,exact_metadata_value_equal=equal))
 return results
def replay(evidence,budget,expected_MF1_nz):
 p=evidence['retained_operands_full_pin'];current(p);require(p['identity'][3]==1 and p['size_bytes']<2*2**20,'ordinary new operand NPZ2MiB bound');budget()
 with Path(p['path']).open('rb')as raw:
  require(identity(os.fstat(raw.fileno()))==p['identity'],'opened new NPZ7');require(hashlib.file_digest(raw,'sha256').hexdigest()==p['sha256'],'whole new NPZ EOF SHA');raw.seek(0)
  with zipfile.ZipFile(raw)as zipped:
   records=zipped.infolist();require(len(records)==28 and {r.filename for r in records}=={n+'.npy'for n in MEMBERS}and sum(r.file_size for r in records)<2*2**20 and all(r.compress_type==zipfile.ZIP_STORED and r.flag_bits&1==0 and r.file_size<2*2**20 for r in records),'exact original28 uncompressed pickle-free bounded numpy members')
  raw.seek(0)
  with np.load(raw,allow_pickle=False)as archive:
   require(len(archive.files)==28 and set(archive.files)==set(MEMBERS),'literal original stored member schema');arrays={name:archive[name]for name in MEMBERS}
  require(identity(os.fstat(raw.fileno()))==p['identity'],'new NPZ opened7 unchanged after independent read')
 current(p);records3=raw_records('MF3',arrays,evidence);records6=raw_records('MF6',arrays,evidence);expected=reconstruct(records3,records6);comparisons=[]
 for name in DERIVED:
  dtype='|u1'if name.endswith('_mask')else'<f8';shape=[370,370]if name=='MF6_P0_production_matrix'else[370];exact_array(name,arrays[name],dtype,shape);exact_array(name+'_reconstructed',expected[name],dtype,shape);comparisons.append(zero_bits(name,arrays[name],expected[name]))
 energy=exact_array('original_MF1_energy',arrays['original_MF1_ascending_energy_eV'],'<f8',[371]);sigma=arrays['original_MF1_sigma0_barn'];exact_array('original_MF1_sigma0',sigma,'<f8',[expected_MF1_nz]);require(bool((sigma>0).all())and len(set(map(float,sigma)))==len(sigma)and bool((energy[1:]>energy[:-1]).all()),'retained original M1 context finite positive sigma0/ascendingenergy shape only');stats=compare_scalar_metadata(scalar_statistics(expected),evidence);budget();return dict(nuclide=evidence['nuclide'],MT=evidence['MT'],temperature_K=evidence['temperature_K'],original_temperature_index_one_based=evidence['original_temperature_index_one_based'],captured_operand_full_pin=p,compared_derived_arrays=len(comparisons),array_comparisons=comparisons,scalar_statistic_comparisons=stats,all_derived_arrays_exact_bytes_equal=all(r['exact_bytes_equal']for r in comparisons),all_recomputed_scalar_statistics_exact=all(r['exact_metadata_value_equal']for r in stats),different_values=sum(r['different_values']for r in comparisons),different_bits=sum(r['different_bits']for r in comparisons),captured_original_P0_LIST_numeric_hashes_revalidated=True,original_ASCII_or_full_NL2_payload_hash_independently_replayed=False,raw_original_inputs_opened=False,original_capture_worker_or_scalar_matrix_imported=False,**FALSE)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--binding-pin',required=True);ap.add_argument('--expected-parent-pid',type=int,required=True);a=ap.parse_args();require(os.getppid()==a.expected_parent_pid and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in THREADS),'original parent/single thread/no profile or optimization');pb=json.loads(a.binding_pin);binding=metadata(pb);require(binding['schema']=='EXTRA21_CAPTURED_OPERAND_INDEPENDENT_REPLAY_EXECUTION_BINDING_V1'and binding['original_caps']==CAPS and binding['prior_capture_actual0_and_independent_post0_admitted']is True,'exact original capture0/post0 owning binding');budget=Budget(binding['complete_joint_roots'],binding['explicit_cumulative_metadata_file_pins']);budget.check();plan=metadata(binding['control_plan_pin']);require(plan['complete_joint_roots']==binding['complete_joint_roots']and plan['original_caps']==CAPS,'same original cumulative62 andcaps');report=metadata(plan['actual_captured_operands_report_pin']);require(report['schema']=='ACTUAL_EXTRA21_ORIGINAL_ASCII_EVENT_PRODUCTION_CAPTURE_V1'and report['status']=='SELECTED21_CHANNEL_131T_MF3_EVENT_MF6_P0_OPERANDS_CAPTURED_ONLY'and all(report[k]is False for k in FALSE),'exact selected-only currentcapture report');rows=[e for r in report['actual_extractions']for e in r['actual_selected_channel_temperature_records']];require(len(rows)==131 and len({(e['nuclide'],e['MT'],e['temperature_K'])for e in rows})==131 and len({(e['nuclide'],e['MT'])for e in rows})==21,'complete selected131/21 capturecohorts');results=[]
 for row in rows:results.append(replay(row,budget.check,plan['actual_original_MF1_nz_by_nuclide'][row['nuclide']]))
 for p in binding['fixed_small_metadata_pins']:metadata(p)
 for row in rows:current(row['retained_operands_full_pin'])
 metadata(pb);budget.last=0;budget.check();out=Path(binding['output_directory']);require(out.is_dir(),'owning replay output exists');exact=all(r['all_derived_arrays_exact_bytes_equal']and r['all_recomputed_scalar_statistics_exact']for r in results);value=dict(schema='ACTUAL_EXTRA21_NEW_CAPTURED_OPERAND_INDEPENDENT_REPLAY_V1',status='ALL131_NEW_CAPTURED_P0_OPERANDS_20_DERIVED_ARRAYS_ZERO_BIT_DIFFERENCE'if exact else'NEW_CAPTURED_P0_OPERAND_INDEPENDENT_REPLAY_MISMATCH_NO_RETRY',execution_binding_pin=pb,control_plan_pin=binding['control_plan_pin'],source_freeze_pin=binding['source_freeze_pin'],captured_operand_report_pin=plan['actual_captured_operands_report_pin'],replays=results,replayed_operand_files=131,replayed_unique_channels=21,replayed_unique_nuclides=17,compared_derived_arrays=131*20,compared_original_P0_LIST_records=768+576,different_values=sum(r['different_values']for r in results),different_bits=sum(r['different_bits']for r in results),independent_replay_only_new_captured_numeric_operands=True,original_science_inputs_opened_or_hashed=False,original_capture_worker_or_scalar_matrix_imported=False,native_engines_started=0,original_caps=CAPS,**FALSE);target=out/'ACTUAL_NEW_CAPTURED_EXTRA21_OPERAND_INDEPENDENT_REPLAY.json';write(target,value);budget.last=0;budget.check();print(json.dumps(dict(status=value['status'],report_pin=pin(target),**FALSE)),flush=True);require(exact,'strict zero-bit new-operand reconstruction mismatch retained, no retry')
if __name__=='__main__':main()
