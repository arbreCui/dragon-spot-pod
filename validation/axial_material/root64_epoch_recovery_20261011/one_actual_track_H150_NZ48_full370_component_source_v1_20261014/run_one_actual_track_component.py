"""One fully dimensioned actual ray: original white ABI and nine-moment transport."""
import argparse,ctypes,hashlib,importlib.util,json,os,resource,sqlite3,stat,sys,time
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
FALSE={'physics_qualified': False, 'historical_machine_bit_replay': False, 'historical_native_RAM_bits_verified': False, 'original_XSM_memory_bits_verified': False, 'complete_reaction_authority_qualified': False, 'full_reference_qualified': False, 'formal_H150_NZ48_full_controls_qualified': False, 'AAA_qualified': False, 'ABA_admitted': False, 'goal_complete': False}
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();require(stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not any(a.is_symlink()for a in(q,*q.parents))and identity(s)==p['identity'],'exact ordinary current7')
def exact(p):
 current(p);raw=Path(p['path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==p['sha256'],'complete Source/metadata SHA');current(p);return raw
def digest(a):return dict(dtype=a.dtype.str,shape=list(a.shape),sha256=hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest())
def compare(a,b,limit):
 require(a.shape==b.shape and np.isfinite(a).all()and np.isfinite(b).all(),'complete finite equal shape')
 different=int(np.count_nonzero(a.view(np.uint64)!=b.view(np.uint64)));absolute=float(np.max(np.abs(a-b),initial=0));scale=float(np.max(np.abs(b),initial=0));relative=absolute/scale if scale else(0. if absolute==0 else float('inf'))
 require(different==0 or relative<=limit,'original unchanged arithmetic threshold')
 return dict(compared_values=int(a.size),bit_mismatches=different,maximum_absolute=absolute,maximum_relative=relative,limit=limit)
class Budget:
 def __init__(self):self.started=time.monotonic()
 def check(self):
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  require(peak<512*2**20 and time.monotonic()-self.started<600,'original childSELF512/stage600')
def small_vectors(sqlpin,poolpin,paths,adapter,temp,budget):
 current(sqlpin);current(poolpin);sf=os.open(sqlpin['path'],os.O_RDONLY|os.O_NOFOLLOW);pf=os.open(poolpin['path'],os.O_RDONLY|os.O_NOFOLLOW);db=None
 try:
  require(identity(os.fstat(sf))==sqlpin['identity']and identity(os.fstat(pf))==poolpin['identity'],'opened exact SQL/pool7');os.environ['SQLITE_TMPDIR']=str(temp)
  db=sqlite3.connect(Path(sqlpin['path']).as_uri()+'?mode=ro&immutable=1',uri=True);db.execute('PRAGMA query_only=ON');db.execute('PRAGMA cache_size=-8192');db.execute('PRAGMA mmap_size=0');db.execute('PRAGMA temp_store=FILE');db.set_progress_handler(lambda:(budget.check(),0)[1],1000)
  require(tuple(r[1]for r in db.execute('PRAGMA table_info(records)'))==adapter.SQL_COLUMNS,'saved native exact schema');validator=object.__new__(adapter.SavedNativeInput);validator.pool_pin=poolpin
  values=[];rows=[]
  for path,count in paths:
   budget.check();result=db.execute('SELECT row FROM records WHERE key=?',(adapter.path_key(path),)).fetchone();require(result is not None,'literal typed actual record')
   row=adapter.strict_json(result[0]);validator.validate_row(row);require(row['path']==list(path)and row['kind']==2 and row['declared_count']==count and row['original_word_count']==count,'exact REAL32 vector shape')
   raw=os.pread(pf,count*4,row['native_payload_begin_byte']);require(len(raw)==count*4 and hashlib.sha256(raw).hexdigest()==row['native_payload_sha256'],'complete original tiny record words')
   values.append(np.frombuffer(raw,dtype='<f4').copy());rows.append(row)
  require(identity(os.fstat(sf))==sqlpin['identity']and identity(os.fstat(pf))==poolpin['identity'],'after opened SQL/pool7');current(sqlpin);current(poolpin);return values,rows
 finally:
  if db is not None:db.close()
  os.close(sf);os.close(pf)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--plan-pin',required=True);ap.add_argument('--report',required=True);ap.add_argument('--expected-parent-pid',type=int,required=True);args=ap.parse_args();budget=Budget()
 require(os.getppid()==args.expected_parent_pid and not sys.flags.optimize and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')),'genuine original owning guard/singlethread child')
 planpin=json.loads(args.plan_pin);plan=json.loads(exact(planpin));sys.path.insert(0,plan['exact_v2_source_root'])
 for row in plan['explicit_import_bindings']:
  name=row['module'];p=row['pin'];exact(p);require(name not in sys.modules,'fresh actual Source module')
  spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);require(Path(m.__file__).absolute()==Path(p['path']),'explicit actual module binding')
 authority=sys.modules['current_formal_input_authority'];kernel=authority.KernelBinding(plan['actual_kernel_origin_pin'],budget);kernel.verify(plan['actual_kernel_library_pin']['path'])
 adapter=sys.modules['actual_track_saved_adapter'];totalrows=[(('MACROLIB','GROUP',g,'NTOT0'),8)for g in range(1,371)]
 temp=Path(args.report).parent/'sqlite_temp';temp.mkdir()
 vectors,materialrows=small_vectors(plan['observed_final55_SQLite_pin'],plan['observed_final55_pool_pin'],totalrows,adapter,temp,budget)
 total=np.repeat(np.stack(vectors,axis=1).astype('d')[:,None,:],48,axis=1);require(total.shape==(8,48,370)and np.isfinite(total).all()and np.all(total>=0),'all actual saved total words promoted exactly')
 angles,anglerows=small_vectors(plan['native_A1_SQLite_pin'],plan['native_A1_pool_pin'],[(('TRACK',1,k),4)for k in('XMU$MCCG','ZMU$MCCG','WZMU$MCCG')],adapter,temp,budget)
 track=sys.modules['terminal_AB_and_current_track_inputs'].native_track_inventory(plan['current_original_radial_track_pin']);states=sys.modules['native_full_angular_p2'].angular_states_from_native(*[v.astype('d')for v in angles],track['azimuth_xy'][:,0],track['azimuth_xy'][:,1])
 ray=track['tracks'][0];require(ray['original_track']==0 and len(track['tracks'])==11364 and states.azimuth_count==96 and len(states.keys)==1536,'whole actual inventory parsed, one original ray selected without sorting')
 polar,sign,orientation=0,-1,1;state=int(states.indices(polar,sign,orientation,ray['angle']));widths=np.ascontiguousarray(ray['planar_widths']*states.zmu[polar]);regions=np.ascontiguousarray(ray['regions'],dtype=np.int32);mu=float(sign*np.sqrt(1-1/states.zmu[polar]**2));entry,exit_surface=ray['entry_surface'],ray['exit_surface'];weight=float(ray['weight']*states.wzmu[polar]/2);harmonic=np.ascontiguousarray(states.harmonics[state]);require(weight>0 and harmonic.shape==(9,),'original unfitted positive WEI*WZMU/2 and all nine harmonics')
 # Independent signed nine-coefficient source fixture. These are not saved
 # observed mixed moments or a material-derived coupled reference source.
 coefficients=np.sin(np.arange(8*48*370*9,dtype='d')).reshape(8,48,370,9)*.01
 q=np.ascontiguousarray(np.einsum('m,rzgm->rzg',harmonic,coefficients).reshape(8*48,370));radial=np.zeros((288,370));axial=np.zeros((8,370))
 native=sys.modules['native_layered_multigroup'].transport_multigroup;old=sys.modules['native_layered_zonal'].transport_zonal
 transport=native(kernel.library_pin['path'],widths,regions,total,entry,150.,48,mu,orientation,32,q,radial,axial)
 require(float(transport['metrics'][:,2].max())<=plan['physical_checks']['primitive']and float(transport['metrics'][:,12].max())<=plan['physical_checks']['cell']and np.all(transport['metrics'][:,26]==0)and transport['geometry'][3]<=plan['physical_checks']['geometry']and transport['geometry'][5]<=plan['physical_checks']['represented_width'],'original complete physical ray arithmetic ceilings')
 transport_comparisons=[];projected=sys.modules['native_layered_transport'].aggregate(transport['fields'],regions,48,orientation,exit_surface)['volume'][...,None]*harmonic*weight
 projection_digests=[]
 for group in range(370):
  budget.check();reference=old(plan['actual_original_zonal_library_pin']['path'],widths,regions,total[:,:,group],entry,150.,48,mu,orientation,32,q[:,group:group+1],radial[:,group:group+1],axial[:,group:group+1]);row={'group':group+1}
  for field in('fields','geometry','metrics'):row[field]=compare(transport[field][...,group:group+1]if field=='fields'else transport[field]if field=='geometry'else transport[field][group:group+1],reference[field],plan['physical_checks']['geometry']if field=='geometry'else plan['physical_checks']['cell'])
  oldmoment=sys.modules['native_layered_transport'].aggregate(reference['fields'],regions,48,orientation,exit_surface)['volume'][...,None]*harmonic*weight;row['all9_projected_moments']=compare(projected[:,:,group:group+1,:],oldmoment,plan['physical_checks']['cell']);transport_comparisons.append(row)
 projection_digest=digest(projected);source_digest=digest(coefficients);del coefficients,q,radial,axial,transport,projected,reference,oldmoment
 budget.check();T=np.zeros((288,288,370));L=np.zeros((2,8,288,370));D=np.zeros(288);geometry=np.zeros(6);nodes,weights=sys.modules['native_layered_multigroup']._quadrature(32)
 function=ctypes.CDLL(kernel.library_pin['path']).layered_white_accumulate370;pointer=ctypes.c_void_p;function.argtypes=([ctypes.c_int]*3+[pointer]*3+[ctypes.c_int]*2+[ctypes.c_double]*2+[ctypes.c_int]*2+[pointer]*2+[ctypes.c_double]+[pointer]*4);function.restype=ctypes.c_int
 rc=function(len(widths),48,370,widths.ctypes.data,regions.ctypes.data,total.ctypes.data,entry,exit_surface,150.,mu,orientation,32,nodes.ctypes.data,weights.ctypes.data,weight,geometry.ctypes.data,T.ctypes.data,L.ctypes.data,D.ctypes.data);require(rc==0,'actual accumulator complete formal geometry ABI')
 white=sys.modules['actual_track_white_transfer'].white_radial_transfer;white_comparisons=[]
 for group in range(370):
  budget.check();ref=white(plan['actual_original_white_library_pin']['path'],widths,regions,np.ascontiguousarray(total[:,:,group:group+1]),entry,exit_surface,150.,48,mu,orientation,32)
  row=dict(group=group+1,transfer=compare(T[:,:,group:group+1],ref['transfer']*weight,plan['physical_checks']['white']),leakage=compare(L[:,:,:,group:group+1],ref['leakage']*weight,plan['physical_checks']['white']),incoming=compare(D,ref['incoming']*weight,plan['physical_checks']['white']),geometry=compare(geometry,ref['geometry'],plan['physical_checks']['geometry']));white_comparisons.append(row)
 require(np.isfinite(T).all()and np.isfinite(L).all()and np.isfinite(D).all()and np.all(T>=0)and np.all(L>=0)and np.all(D>=0),'complete actual one-ray weighted white arrays')
 arrays=dict(transfer=digest(T),leakage=digest(L),incoming=digest(D),geometry=digest(geometry));del T,L,D,ref
 for row in plan['explicit_import_bindings']:exact(row['pin']);require(Path(sys.modules[row['module']].__file__).absolute()==Path(row['pin']['path']),'same exact module Source at end')
 for p in plan['scientific_input_current7_pins']:current(p)
 kernel.verify(kernel.library_pin['path']);exact(planpin);budget.check()
 report=dict(schema='ACTUAL_ONE_REAL_TRACK_H150_NZ48_FULL370_NINE_MOMENT_COMPONENT_CONTROL_V1',passed=True,component_only=True,actual_original_track_index=0,actual_tracks_executed=1,actual_actions_executed=1,original_track_inventory_parsed=11364,original_native_angular_states=1536,actual_native_state_index=state,polar=polar,sign=sign,orientation=orientation,actual_track_angle=int(ray['angle']),H=150.,nz=48,groups=370,retained_moments=9,offset_order=32,source_is_independent_signed_nine_coefficient_fixture=True,source_fixture_digest=source_digest,all9_projection_digest=projection_digest,original_track_weight=weight,material_NTOT0_original_record_metadata=materialrows,angle_original_record_metadata=anglerows,transport_comparisons_all370=transport_comparisons,white_comparisons_all370=white_comparisons,complete_weighted_white_array_digests=arrays,actual_kernel_origin_pin=plan['actual_kernel_origin_pin'],actual_kernel_library_pin=kernel.library_pin,old_white_library_pin=plan['actual_original_white_library_pin'],old_zonal_library_pin=plan['actual_original_zonal_library_pin'],original_caps=plan['original_caps'],whole_white_cache_created=False,full_original_track_sweep_executed=False,formal_SN32_equivalence_claimed=False,child_elapsed_seconds=time.monotonic()-budget.started,child_SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,**FALSE)
 with Path(args.report).open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 budget.check();print(json.dumps(dict(status='ACTUAL_ONE_REAL_TRACK_COMPONENT_CLOSED0_ONLY',report=str(args.report),**FALSE)),flush=True)
if __name__=='__main__':main()
