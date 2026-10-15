"""Source-only one real ray control. No native call, data-body read or deletion."""
import ast,base64,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';ART=R/'validation/artifacts'
BASE=Path(__file__).absolute().parent;REF=REC/'full370_unreduced_eigen_reference_source_v2'
PREVIOUS=REC/'full370_kernel_origin_component_control_source_v1_20261014'
RETIRE=REC/'literal4_completed_compare_spool_retirement_20261014_v1'
OUT=ART/'axial-material-one-actual-track-H150-NZ48-full370-component-20261014-v1'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(physics_qualified=False,historical_machine_bit_replay=False,historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,complete_reaction_authority_qualified=False,full_reference_qualified=False,formal_H150_NZ48_full_controls_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
 q=Path(path);s=q.lstat();require(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_size<64*2**20 and not any(p.is_symlink()for p in(q,*q.parents)),'bounded ordinary Source/metadata')
 raw=q.read_bytes();require(identity(q.lstat())==identity(s),'current7');return dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def current_data(p):
 q=Path(p['path']);s=q.lstat();require(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not any(a.is_symlink()for a in(q,*q.parents))and identity(s)==p['identity'],'exact already-current scientific input7, never body read');return p
def write(path,v):
 raw=v if type(v)is bytes else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with path.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(path)
WORKER=r'''"""One fully dimensioned actual ray: original white ABI and nine-moment transport."""
import argparse,ctypes,hashlib,importlib.util,json,os,resource,sqlite3,stat,sys,time
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
FALSE=FALSE_LITERAL
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();require(stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not any(a.is_symlink()for a in(q,*q.parents))and identity(s)==p['identity'],'exact ordinary current7')
def exact(p):
 current(p);raw=Path(p['path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==p['sha256'],'complete Source/metadata SHA');current(p);return raw
def digest(a):return dict(dtype=a.dtype.str,shape=list(a.shape),sha256=hashlib.sha256(memoryview(np.ascontiguousarray(a)).cast('B')).hexdigest())
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
'''

# V2 retains every V1 generated bytefile and truthful Sourcegen result.
# Every actual original track action is visited in original 4/2/2 order.
_start=WORKER.index(" polar,sign,orientation=0,-1,1;state=")
_stop=WORKER.index(" for row in plan['explicit_import_bindings']:exact(row['pin']);require",_start)
_action=WORKER[_start:_stop]
_action=_action.replace(" polar,sign,orientation=0,-1,1;state="," state=",1)
_action=_action.replace("entry,exit_surface=ray['entry_surface'],ray['exit_surface'];weight=", "entry,exit_surface=ray['entry_surface'],ray['exit_surface'];entry,exit_surface=(entry,exit_surface)if orientation==1 else(exit_surface,entry);weight=")
_action=_action.replace(" transport_comparisons=[];projected=", " global_error=np.divide(np.abs(transport['metrics'][:,24]),transport['metrics'][:,25],out=np.zeros(370),where=transport['metrics'][:,25]!=0);require(np.all((transport['metrics'][:,25]!=0)|(transport['metrics'][:,24]==0))and float(global_error.max())<=plan['physical_checks']['global'],'original per-group raw ray global arithmetic ceiling')\n transport_comparisons=[];projected=")
_action+=" allactions.append(dict(polar=polar,sign=sign,orientation=orientation,state_index=state,actual_track_angle=int(ray['angle']),original_track_weight=weight,source_fixture_digest=source_digest,all9_projection_digest=projection_digest,transport_comparisons_all370=transport_comparisons,white_comparisons_all370=white_comparisons,complete_weighted_white_array_digests=arrays))\n"
_loop=" allactions=[]\n for polar in range(4):\n  for sign in(-1,1):\n   for orientation in(1,-1):\n"+''.join('   '+line+'\n' for line in _action.splitlines())
_loop+=" require(len(allactions)==16 and [(row['polar'],row['sign'],row['orientation'])for row in allactions]==[(p,s,o)for p in range(4)for s in(-1,1)for o in(1,-1)],'one complete original track, all16 actions in exact order')\n"
WORKER=WORKER[:_start]+_loop+WORKER[_stop:]
WORKER=WORKER.replace('actual_actions_executed=1,','actual_actions_executed=16,')
WORKER=WORKER.replace('actual_native_state_index=state,polar=polar,sign=sign,orientation=orientation,actual_track_angle=int(ray[\'angle\']),','actual_action_order=[(p,s,o)for p in range(4)for s in(-1,1)for o in(1,-1)],actual_track_angle=int(ray[\'angle\']),')
WORKER=WORKER.replace('source_fixture_digest=source_digest,all9_projection_digest=projection_digest,original_track_weight=weight,','action_controls_all16=allactions,')
WORKER=WORKER.replace('transport_comparisons_all370=transport_comparisons,white_comparisons_all370=white_comparisons,complete_weighted_white_array_digests=arrays,actual_kernel_origin_pin=', 'all16_complete_dimension_actions_passed=True,actual_kernel_origin_pin=')
ast.parse(WORKER)

def main():
 require(sorted(p.name for p in BASE.iterdir())==[Path(__file__).name],'fresh single author Source')
 latestpin=pin(REC/'original_a11_NX_formatter_component_source_v1_20261014/PLAN.json');latest=json.loads(Path(latestpin['path']).read_bytes());oldplan=json.loads((PREVIOUS/'PLAN.json').read_bytes());saved=json.loads((REC/'saved_three_macro_exact_typed_path_join_source_v1_20261014/PLAN.json').read_bytes())
 origin=pin(ART/'axial-material-current-full370-kernel-origin-component-controls-20261014-v1/ACTUAL_FULL370_WHITE_ACCUMULATOR_LIBRARY_ORIGIN.json');originvalue=json.loads(Path(origin['path']).read_bytes());require(originvalue['original_caps']==CAPS,'same actual compiled origin caps')
 oldwhitebase=ART/'axial-material-layered-white-radial-transfer-analytic-void-20261011';oldwhitereport=pin(oldwhitebase/'RESULT.json');ow=json.loads(Path(oldwhitereport['path']).read_bytes());require(ow['new_library_pin']==pin(oldwhitebase/'component/liblayered_white_transfer.dylib')and ow['frozen_inputs_unchanged']is True,'actual retained original white library')
 require((oldwhitebase/'Source_at_run/native_layered_white_transfer.cpp').read_bytes()==(REF/'native_layered_white_transfer.cpp').read_bytes(),'retained old white ABI Source wholebytes equal to current origin include')
 formalplanpin=pin(REF/'CURRENT_FORMAL_FULL370_INPUT_PLAN_SOURCE_ONLY.json');formal=json.loads(Path(formalplanpin['path']).read_bytes());protectedpin=pin(formal['protected_formal_and_producer_plan_pin']['path']);protected=json.loads(Path(protectedpin['path']).read_bytes());oldtrack=protected['producers'][0]['radial_binary_track'];track=dict(oldtrack);s=Path(track['path']).lstat();require(identity(s)[1:]==oldtrack['identity'][1:]and s.st_dev==16777229 and oldtrack['identity'][0]==16777234,'only this declared historical track mount transition, no general missing');track['identity']=identity(s);current_data(track)
 bindings=[]
 for module,src in [('native_oblique_streaming',REF/'native_oblique_streaming.py'),('native_layered_transport',REF/'native_layered_transport.py'),('native_layered_multigroup',REF/'native_layered_multigroup.py'),('native_full_angular_p2',REF/'native_full_angular_p2.py'),('snapshot_control_preflight',REF/'snapshot_control_preflight.py'),('terminal_AB_and_current_track_inputs',REF/'terminal_AB_and_current_track_inputs.py'),('full370_unreduced_eigen',REF/'full370_unreduced_eigen.py'),('current_formal_input_authority',REF/'current_formal_input_authority.py'),('native_layered_zonal',R/'validation/iterative/native_layered_zonal.py'),('actual_track_white_transfer',R/'validation/iterative/native_layered_white_transfer.py'),('actual_track_saved_adapter',REC/'saved_three_macro_exact_typed_path_join_source_v1_20261014/saved_native_data_access_adapter.py')]:bindings.append(dict(module=module,pin=pin(src)))
 science=[saved['observed_pair']['sqlite_pin'],saved['observed_pair']['native_pool_pin'],saved['native_pairs'][0]['sqlite_pin'],saved['native_pairs'][0]['native_pool_pin'],track]
 for p in science:current_data(p)
 worker=WORKER.replace('FALSE_LITERAL',repr(FALSE));ast.parse(worker);workerpin=write(BASE/'run_one_actual_track_component.py',worker.encode())
 plan=dict(schema='ONE_ACTUAL_TRACK_H150_NZ48_FULL370_COMPONENT_SOURCE_ONLY_PLAN_V1',source_only=True,planned_actual_output_root=str(OUT),original_caps=CAPS,original_Common_Source_pin=oldplan['original_Common_Source_pin'],original_support_Source_pin=oldplan['original_support_Source_pin'],original_bounded_Source_pin=oldplan['original_bounded_Source_pin'],complete_joint_roots=latest['complete_joint_roots']+[str(RETIRE),str(BASE.parent),str(OUT),str(REC/'actual_four_original_ascii_gendf_streaming_source_v1_20261014'),str(ART/'axial-material-four-original-ASCII-GENDF-stream-inventory-20261014-v1')],explicit_cumulative_metadata_file_pins=latest['explicit_cumulative_metadata_file_pins'],original_cumulative38_plan_pin=latestpin,original_recipe_pin=pin(PREVIOUS/'ROOT_REVIEWABLE_FULL370_KERNEL_ORIGIN_COMPONENT_CONTROL_ARGV.json'),actual_kernel_origin_pin=origin,actual_kernel_library_pin=originvalue['library_pin'],actual_kernel_build_report_pin=originvalue['actual_build_report_pin'],actual_original_zonal_library_pin=oldplan['actual_original_zonal_library_pin'],actual_original_white_library_pin=ow['new_library_pin'],actual_original_white_report_pin=oldwhitereport,actual_original_white_Source_pin=pin(oldwhitebase/'Source_at_run/native_layered_white_transfer.cpp'),formal_case_checks_Source_plan_pin=formalplanpin,protected_formal_plan_pin=protectedpin,exact_v2_source_root=str(REF),explicit_import_bindings=bindings,observed_final55_SQLite_pin=science[0],observed_final55_pool_pin=science[1],native_A1_SQLite_pin=science[2],native_A1_pool_pin=science[3],current_original_radial_track_pin=track,historical_original_radial_track_pin=oldtrack,scientific_input_current7_pins=science,physical_checks=formal['physical_checks'],actual_native_action_order=[(p,s,o)for p in range(4)for s in(-1,1)for o in(1,-1)],worker_source_pin=workerpin,required_retirement_directory=str(RETIRE),exact_four_retired_intermediate_pins=[row[k]for row in saved['native_pairs'][1:]for k in('sqlite_pin','native_pool_pin')],exact_retained_native_archive_pins=[row['archive_pin']for row in saved['native_pairs'][1:]],actual_component_report_pin=None,actual_retirement_receipt_pin=None,component_only=True,actual_track_index=0,actual_tracks_to_execute=1,actual_actions_to_execute=16,full11364_track_sweep_executed=False,whole_white_cache_created=False,**FALSE)
 plan['expected_actual_retirement_post_pin']=pin(RETIRE/'actual_postverify_20261014/REVIEW.json')
 plan['expected_actual_retirement_post_tools_pin']=pin(RETIRE/'actual_postverify_20261014/TRUE_TOOL_RETURNS.json')
 plan['expected_actual_retirement_root_tools_pin']=pin(RETIRE/'ROOT_EXECUTION_TRUE_TOOL_RETURNS.json')
 plan['expected_actual_retirement_receipt_pin']=pin(RETIRE/'EXECUTION_RECEIPT.json')
 plan['explicit_cumulative_metadata_file_pins']+= [pin(REC/'ROOT_NX_ELEVEN_ORIGINAL_ASCII_PRODUCER_INPUT_LINEAGE_20261014.json'),pin(REC.parent/'SPOT_COMPLETED_COMPARE_SPOOL_RETIREMENT_RESULT_20261014.txt')]
 host=(PREVIOUS/'run_guarded_full370_kernel_origin_components.py').read_text();host=host.replace('FULL370_KERNEL_ORIGIN_COMPONENT_CONTROL','ONE_ACTUAL_TRACK_COMPONENT_CONTROL').replace('FULL370_KERNEL_ORIGIN_COMPONENT_CONTROL_HOST','ONE_ACTUAL_TRACK_COMPONENT_CONTROL_HOST')
 # Preserve the original guard/resource methods byte-for-byte. Only the
 # experiment-specific one-child command and report are replaced.
 host=host.replace("for p in hf['dependencies']:current7(p);c.same_pin(p['path'],p)","for p in hf['dependencies']:\n  current7(p)\n  if p not in plan['scientific_input_current7_pins']:c.same_pin(p['path'],p)")
 host=host.replace("for p in fixed:current7(p);c.same_pin(p['path'],p)","for p in fixed:\n   current7(p)\n   if p not in plan['scientific_input_current7_pins']:c.same_pin(p['path'],p)")
 begin=host.index(" library=out/'component/libcurrent_full370_white_accumulate.dylib'");end=host.index(" except BaseException as error:first.capture(error,'execute_or_component_report')",begin)
 host=host[:begin]+''' receipt=metadata(sf['actual_retirement_receipt_pin']);require(sf['actual_retirement_receipt_pin']==plan['expected_actual_retirement_receipt_pin'],'precise completed literal-four actual receipt fullPF')
 retpost=metadata(plan['expected_actual_retirement_post_pin']);rettools=metadata(plan['expected_actual_retirement_post_tools_pin']);roottools=metadata(plan['expected_actual_retirement_root_tools_pin'])
 rt=roottools['actual_execution_return'];pt=rettools['actual_terminal_return']
 require(type(rt['exit_code'])is int and rt['exit_code']==0 and rt.get('session_id')is None and type(pt['exit_code'])is int and pt['exit_code']==0 and pt.get('session_id')is None,'genuine closed typed retirement Root0 and postreview0')
 require(json.loads(rt['output'].strip().splitlines()[-1])['receipt_pin']==plan['expected_actual_retirement_receipt_pin']and json.loads(pt['output'].strip().splitlines()[-1])['review_pin']==plan['expected_actual_retirement_post_pin'],'genuine actual tool stdout binds exact receipt and postreview')
 require(rettools['observed_closed']is True and type(rettools['original_integer_exit_code'])is int and rettools['original_integer_exit_code']==0 and retpost['schema']=='LITERAL4_COMPLETED_COMPARE_SPOOL_RETIREMENT_ACTUAL_POSTVERIFICATION_V1'and retpost['status']=='PASS_ACTUAL_EXACT_LITERAL4_RETIREMENT_FINITE_POSTVERIFICATION'and retpost['failure']is None and retpost['actual_Root_integer_exit_code']==0 and retpost['actual_execution_receipt_fullpin']==plan['expected_actual_retirement_receipt_pin']and retpost['actual_Root_execution_tools_fullpin']==plan['expected_actual_retirement_root_tools_pin']and retpost['all_four_literal_paths_absent_twice']is True and retpost['A1_pair_and_original_three_XSM_preserved_current7']is True,'actual finite postverification of closed literal-four lifecycle')
 require(receipt['schema']=='LITERAL4_COMPLETED_COMPARE_SPOOL_RETIREMENT_RECEIPT_V1'and receipt['mode']=='execute'and receipt['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY'and receipt['failure']is None and receipt['actual_released_bytes']==405417320 and receipt['completed_temporary_file_lifecycle_only']is True and receipt['sameSHA_duplicate_claim']is False and receipt['old_reports_rewritten']is False and len(receipt['actual_released_pins'])==4 and sorted(receipt['actual_released_pins'],key=lambda p:p['path'])==sorted(plan['exact_four_retired_intermediate_pins'],key=lambda p:p['path']),'exact actual four retired fullPFs and preserved original result documents')
 require(all(receipt[k]is False and retpost[k]is False for k in('business_executed','compiler_executed','numerical_executed','physics_qualified','scientific_accuracy_qualified','AAA_qualified','ABA_admitted','goal_complete')),'precise scope of genuine retirement proof')
 require(Path(sf['actual_retirement_receipt_pin']['path']).parent==Path(plan['required_retirement_directory']),'only exact retirement receipt directory')
 def contains(v,p):return v==p or type(v)is dict and any(contains(x,p)for x in v.values())or type(v)is list and any(contains(x,p)for x in v)
 require(all(contains(receipt,p)and not os.path.lexists(p['path'])for p in plan['exact_four_retired_intermediate_pins']),'only four literal closed intermediary retirements')
 for p in plan['exact_retained_native_archive_pins']:current7(p)
 command=[str(support.PYTHON),'-B',plan['worker_source_pin']['path'],'--plan-pin',json.dumps(sf['control_plan_pin'],separators=(',',':')),'--report',str(out/'component/ONE_ACTUAL_TRACK_COMPONENT_REPORT.json'),'--expected-parent-pid',str(os.getpid())]
 try:
  run('one_actual_track',command);rp=c.pin(out/'component/ONE_ACTUAL_TRACK_COMPONENT_REPORT.json');owned.append(rp);result=metadata(rp)
  require(result['passed']is True and result['groups']==370 and result['retained_moments']==9 and result['nz']==48 and result['H']==150. and result['offset_order']==32 and result['actual_tracks_executed']==1 and result['actual_actions_executed']==16 and result['formal_H150_NZ48_full_controls_qualified']is False,'precise one complete actual track/all16 original actions full-dimension component scope')
  require(len(runner.records)==1 and runner.records[0]['status']=='PASS','one original guarded child PASS')
  actual=dict(actual_component_report_pin=rp,all_one_stage_PASS=True,actual_kernel_origin_pin=plan['actual_kernel_origin_pin'],actual_kernel_library_pin=plan['actual_kernel_library_pin'],all370_white_and_nine_moment_transport_compared=True,**FALSE);verified=True
'''+host[end:]
 host=host.replace('Root_actual_full370_kernel_origin_component_summary.json','Root_actual_one_actual_track_component_summary.json').replace('ACTUAL_FULL370_KERNEL_ORIGIN_COMPONENT_GUARDED_REPORT_V1','ACTUAL_ONE_REAL_TRACK_COMPONENT_GUARDED_REPORT_V1').replace('ACTUAL_FULL370_LIBRARY_AND_TWELVE_COMPONENT_CONTROLS_CLOSED0_ONLY','ACTUAL_ONE_REAL_TRACK_FULL_DIMENSION_COMPONENT_CLOSED0_ONLY').replace('ACTUAL_FULL370_KERNEL_COMPONENT_FAILED_UNQUALIFIED','ACTUAL_ONE_REAL_TRACK_COMPONENT_FAILED_UNQUALIFIED').replace("synthetic_fixture_scope='angular8azimuth128states; layeredH150NZ3; all370 columns'","actual_track_scope='one original complete track/all16 actions;H150NZ48;370groups;9moments;offset32'")
 begin=host.index('  if good:\n   origin=dict(');end=host.index('\n except BaseException as error:',begin);host=host[:begin]+host[end:]
 host=host.replace("origin_pin=c.pin(origin_path),library_pin=c.pin(library)","origin_pin=plan['actual_kernel_origin_pin'],library_pin=plan['actual_kernel_library_pin']")
 ast.parse(host);hostpin=write(BASE/'run_guarded_one_actual_track_component.py',host.encode())
 deps=[latestpin,origin,originvalue['library_pin'],originvalue['actual_build_report_pin'],oldwhitereport,ow['new_library_pin'],plan['actual_original_zonal_library_pin'],formalplanpin,protectedpin,plan['actual_original_white_Source_pin'],*science,*[row['pin']for row in bindings],*originvalue['complete_source_pins']]
 wanted=('original_Common_Source_pin','original_support_Source_pin','original_bounded_Source_pin')
 deps+=[oldplan[k]for k in wanted]
 names=('prepare_qualified_AB_source_factor_production.py','moment_order_complete_history_resource_trie_20261010.py','qualify_refined_AAA_layered_full.py','production_runner.py','production_inputs.py','guard_controls.json','tested_driver_source.py')
 deps+=[p for p in oldplan['source_dependency_pins']if Path(p['path']).name in names or '/preflight/live_guard/'in p['path']]
 table={}
 for p in deps:require(p['path']not in table or table[p['path']]==p,'one exact current inputPF');table[p['path']]=p
 plan['source_dependency_pins']=list(table.values())+plan['explicit_cumulative_metadata_file_pins']+[plan[k]for k in('expected_actual_retirement_receipt_pin','expected_actual_retirement_post_pin','expected_actual_retirement_post_tools_pin','expected_actual_retirement_root_tools_pin')]
 writer=(PREVIOUS/'write_once_full370_kernel_origin_components_SF_HF_CLI.py').read_text();writer=writer.replace("('peer-review','peer-tools','Source-generation-tools')","('peer-review','peer-tools','Source-generation-tools','retirement-receipt')")
 writer=writer.replace("'host_source_pin','component_launcher_Source_pin','angular_test_Source_pin','multigroup_test_Source_pin','plan_pin','inverse_pin','Source_author_pin','writer_source_pin'","'host_source_pin','worker_source_pin','plan_pin','inverse_pin','Source_author_pin','writer_source_pin'")
 writer=writer.replace("('actual_library_pin','actual_kernel_origin_pin','actual_component_control_report_pin')","('actual_component_report_pin','actual_retirement_receipt_pin')").replace('FULL370_KERNEL_ORIGIN_COMPONENT_CONTROL','ONE_ACTUAL_TRACK_COMPONENT_CONTROL').replace('FULL370_KERNEL_ORIGIN_COMPONENT_CONTROL_HOST','ONE_ACTUAL_TRACK_COMPONENT_CONTROL_HOST').replace('FULL370_KERNEL_ORIGIN_COMPONENT_SOURCE_SF_HF_CLI24_PUBLISHED_ONLY','ONE_ACTUAL_TRACK_COMPONENT_SOURCE_SF_HF_CLI24_PUBLISHED_ONLY').replace('same-round nine selected kernel component Source fullPFs','same-round seven exact one-track component Source fullPFs')
 marker=" deps=selected+list(proof.values())+plan['source_dependency_pins']"
 replacement=""" receipt=exact(proof['retirement-receipt']);require(proof['retirement-receipt']==plan['expected_actual_retirement_receipt_pin'],'precise completed literal-four actual receipt fullPF')
 retpost=exact(plan['expected_actual_retirement_post_pin']);rettools=exact(plan['expected_actual_retirement_post_tools_pin']);roottools=exact(plan['expected_actual_retirement_root_tools_pin'])
 rt=roottools['actual_execution_return'];pt=rettools['actual_terminal_return']
 require(type(rt['exit_code'])is int and rt['exit_code']==0 and rt.get('session_id')is None and type(pt['exit_code'])is int and pt['exit_code']==0 and pt.get('session_id')is None,'genuine closed typed retirement Root0 and postreview0')
 require(json.loads(rt['output'].strip().splitlines()[-1])['receipt_pin']==plan['expected_actual_retirement_receipt_pin']and json.loads(pt['output'].strip().splitlines()[-1])['review_pin']==plan['expected_actual_retirement_post_pin'],'genuine actual tool stdout binds exact receipt and postreview')
 require(rettools['observed_closed']is True and type(rettools['original_integer_exit_code'])is int and rettools['original_integer_exit_code']==0 and retpost['schema']=='LITERAL4_COMPLETED_COMPARE_SPOOL_RETIREMENT_ACTUAL_POSTVERIFICATION_V1'and retpost['status']=='PASS_ACTUAL_EXACT_LITERAL4_RETIREMENT_FINITE_POSTVERIFICATION'and retpost['failure']is None and retpost['actual_Root_integer_exit_code']==0 and retpost['actual_execution_receipt_fullpin']==plan['expected_actual_retirement_receipt_pin']and retpost['actual_Root_execution_tools_fullpin']==plan['expected_actual_retirement_root_tools_pin']and retpost['all_four_literal_paths_absent_twice']is True and retpost['A1_pair_and_original_three_XSM_preserved_current7']is True,'actual finite postverification of closed literal-four lifecycle')
 require(receipt['schema']=='LITERAL4_COMPLETED_COMPARE_SPOOL_RETIREMENT_RECEIPT_V1'and receipt['mode']=='execute'and receipt['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY'and receipt['failure']is None and receipt['actual_released_bytes']==405417320 and receipt['completed_temporary_file_lifecycle_only']is True and receipt['sameSHA_duplicate_claim']is False and receipt['old_reports_rewritten']is False and len(receipt['actual_released_pins'])==4 and sorted(receipt['actual_released_pins'],key=lambda p:p['path'])==sorted(plan['exact_four_retired_intermediate_pins'],key=lambda p:p['path']),'exact actual four retired fullPFs and preserved original result documents')
 require(all(receipt[k]is False and retpost[k]is False for k in('business_executed','compiler_executed','numerical_executed','physics_qualified','scientific_accuracy_qualified','AAA_qualified','ABA_admitted','goal_complete')),'precise scope of genuine retirement proof')
 require(Path(proof['retirement-receipt']['path']).parent==Path(plan['required_retirement_directory']),'literal four-intermediate retirement receipt directory')
 require(all(contains(receipt,p)and not os.path.lexists(p['path'])for p in plan['exact_four_retired_intermediate_pins']),'four exact completed intermediary identities, no general missing')
 for p in plan['exact_retained_native_archive_pins']:
  s=Path(p['path']).lstat();require(identity(s)==p['identity'],'retained original scientific producer archive7')
 deps=selected+list(proof.values())+plan['source_dependency_pins']"""
 require(marker in writer,'exact old writer splice');writer=writer.replace(marker,replacement).replace("sf=dict(component_only=True,","sf=dict(actual_retirement_receipt_pin=proof['retirement-receipt'],component_only=True,")
 ast.parse(writer);writerpin=write(BASE/'write_once_one_actual_track_component_SF_HF_CLI.py',writer.encode());planpin=write(BASE/'PLAN.json',plan)
 originalhost=(PREVIOUS/'run_guarded_full370_kernel_origin_components.py').read_text();tree=ast.parse(originalhost);hast=ast.parse(host);inverse=[]
 for name in('rewrite_summary','unique','safe_repr','FirstFailure'):
  a=ast.get_source_segment(originalhost,next(n for n in tree.body if getattr(n,'name',None)==name));b=ast.get_source_segment(host,next(n for n in hast.body if getattr(n,'name',None)==name));require(a==b,'original exact guard helper wholebytes');inverse.append(dict(name=name,UTF8_base64=base64.b64encode(a.encode()).decode(),sha256=hashlib.sha256(a.encode()).hexdigest()))
 inversepin=write(BASE/'COMPLETE_ONE_ACTUAL_TRACK_SOURCE_BINDING_PROOF.json',dict(schema='COMPLETE_ONE_ACTUAL_TRACK_SOURCE_BINDING_PROOF_V1',source_only=True,whole_exact_original_guard_definitions=inverse,original_host_Source_pin=pin(PREVIOUS/'run_guarded_full370_kernel_origin_components.py'),actual_white_Source_wholebytes_equal=True,retained_original_white_Source_pin=plan['actual_original_white_Source_pin'],current_white_Source_pin=pin(REF/'native_layered_white_transfer.cpp'),historical_track_pin=oldtrack,current_track_pin=track,only_literal_track_mount_device_34_to_29_changed=True,explicit_import_bindings=bindings,unchanged_original_caps=CAPS,original_joint38_roots_retained=True,complete_joint43_roots_count=len(plan['complete_joint_roots']),exact_four_retired_intermediate_pins=plan['exact_four_retired_intermediate_pins'],host_source_pin=hostpin,worker_source_pin=workerpin,fullscope_formal_control_executed=False,**FALSE))
 ready=write(BASE/'SOURCE_REVIEW_READY.json',dict(schema='ONE_ACTUAL_TRACK_FULL_DIMENSION_COMPONENT_SOURCE_ONLY_READY_V1',source_only=True,host_source_pin=hostpin,worker_source_pin=workerpin,plan_pin=planpin,inverse_pin=inversepin,Source_author_pin=pin(__file__),writer_source_pin=writerpin,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_CLI_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,**FALSE))
 print(json.dumps(dict(status='ONE_ACTUAL_TRACK_COMPONENT_SOURCE_ONLY_READY',ready_pin=ready,writer_source_pin=writerpin,plan_pin=planpin,host_source_pin=hostpin,Source_author_pin=pin(__file__),business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
