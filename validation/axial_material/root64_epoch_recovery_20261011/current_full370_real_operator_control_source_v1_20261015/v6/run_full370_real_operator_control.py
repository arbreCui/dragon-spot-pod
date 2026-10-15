"""One unadmitted full current-material white preparation and fixed-source action."""
import argparse, ctypes, json, os, resource, sys, time
from pathlib import Path
import numpy as np
import control_source_common as c
sys.dont_write_bytecode=True

def require(ok,message):
    if type(ok) not in (bool,np.bool_) or not bool(ok): raise RuntimeError(message)

def digest(value):
    a=np.ascontiguousarray(value)
    return dict(dtype=a.dtype.str,shape=list(a.shape),sha256=__import__('hashlib').sha256(memoryview(a).cast('B')).hexdigest())

def relative(defect,scale):
    out=np.zeros(np.shape(defect),dtype='d');np.divide(np.abs(defect),scale,out=out,where=scale!=0)
    require(np.all((scale!=0)|(defect==0)), 'nonzero defect with zero scale')
    require(np.isfinite(out).all(), 'finite control relative errors');return out

def fixture():
    a=1+(np.arange(8,dtype='d')[:,None]+1)/32+(np.arange(370,dtype='d')[None,:]+1)/2048
    t=(2*np.arange(48,dtype='d')+1-48)/48
    coefficient=np.empty((8,48,370,9));coefficient[:,:,:,0]=a[:,None,:]
    for m in range(1,9):
        coefficient[:,:,:,m]=a[:,None,:]*(m+1)/512*(t[None,:,None] if m in (2,5,7) else 1.)
    return coefficient

class DarwinSelfResident:
    """Exact installed primary-header MACH_TASK_BASIC_INFO ABI; no probe."""
    class TimeValue(ctypes.Structure):
        _pack_=4
        _fields_=[('seconds',ctypes.c_int32),('microseconds',ctypes.c_int32)]
    class BasicInfo(ctypes.Structure):
        _pack_=4
    BasicInfo._fields_=[('virtual_size',ctypes.c_uint64),('resident_size',ctypes.c_uint64),
        ('resident_size_max',ctypes.c_uint64),('user_time',TimeValue),('system_time',TimeValue),
        ('policy',ctypes.c_int32),('suspend_count',ctypes.c_int32)]
    def __init__(self):
        require(sys.platform=='darwin','installed Darwin task_info diagnostic only')
        self.library=ctypes.CDLL('/usr/lib/libSystem.B.dylib')
        self.task=ctypes.c_uint32.in_dll(self.library,'mach_task_self_').value
        self.function=self.library.task_info
        self.function.argtypes=[ctypes.c_uint32,ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_uint32)]
        self.function.restype=ctypes.c_int32
        self.info=self.BasicInfo();self.count=ctypes.c_uint32(12)
        self.info_pointer=ctypes.cast(ctypes.pointer(self.info),ctypes.POINTER(ctypes.c_int32))
        self.count_pointer=ctypes.pointer(self.count)
    def current(self):
        self.count.value=12
        result=self.function(self.task,20,self.info_pointer,self.count_pointer)
        require(result==0 and self.count.value==12,'Darwin SELF task_info returned exact primary-header record')
        return int(self.info.resident_size)

class BoundedBudgetDiagnostic:
    """Duck-typed delegate; original Budget instance/check/start stay unchanged."""
    def __init__(self,inner,original_class,path,source_pin):
        require(type(inner) is original_class and original_class.__bases__==(object,), 'exact original private Budget type/MRO')
        self.inner=inner;self.path=Path(path);self.source_pin=source_pin
        self.phase='SETUP';self.check_count_in_phase=0;self.check_count_total=0
        self.failure_checkpoint_attempted=False;self.checkpoint_write_error=None
        self.resident_reader=None;self.resident_error=None;self.white_baseline_record=None;self.white_arrays_record=None
        self.live_array_bytes={};self.array_aliases={};self.native_boundary=None
        try:self.resident_reader=DarwinSelfResident()
        except BaseException as error:self.resident_error=repr(error)[:256]
    @property
    def started(self):return self.inner.started
    def set_phase(self,phase):
        require(phase in ('SETUP','SOURCE_POSITIVITY','WHITE_PREPARATION','SOURCE_RECREATE','OPERATOR_APPLY','OUTPUT_PUBLICATION'),'bounded diagnostic phase')
        self.phase=phase;self.check_count_in_phase=0
    def memory_sample(self):
        # Failures of optional diagnostics never replace original Budget/math.
        current=None
        if self.resident_reader is not None:
            try:current=self.resident_reader.current()
            except BaseException as error:
                if self.resident_error is None:self.resident_error=repr(error)[:256]
        raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        factor=1 if sys.platform=='darwin' else 1024
        return dict(current_SELF_resident_bytes=current,original_SELF_ru_maxrss_bytes=raw*factor,
            elapsed_seconds=time.monotonic()-self.inner.started)
    def bind_white_context(self,total,operator,rays,states,vectors,angles,state,area,dz,mat,volume,ncode,formal,surface,parity,last_harmonic,last_compact_value):
        # Explicit existing arrays only: no recursive walker, word access/hash,
        # retained ndarray references, or newly computed transport data.
        named=(('worker_total',total),('operator_volume64',operator.volume),
            ('state',state),('area',area),('dz',dz),('mat',mat),('volume_original_f4',volume),
            ('ncode',ncode),('stored_surface64',surface),('parity',parity),
            ('last_harmonic_view_logical',last_harmonic),('last_compact_value_logical',last_compact_value))
        self.live_array_bytes={key:int(value.nbytes) for key,value in named}
        self.live_array_bytes.update(original_total_record_vectors=sum(int(v.nbytes) for v in vectors),
            compact_angle_surface_vectors=sum(int(v.nbytes) for v in angles),
            original_formal_U_W_PL=sum(int(formal[key].nbytes) for key in ('U','W','PL')),
            angular_state_arrays=sum(int(value.nbytes) for value in
                (states.keys,states.directions,states.streaming_directions,states.harmonics,
                 states.xmu,states.zmu,states.wzmu)),azimuth_xy=int(rays['azimuth_xy'].nbytes))
        for key in ('planar_widths','regions','all_original_nom','all_original_h2'):
            self.live_array_bytes['retained_rays_'+key]=sum(int(ray[key].nbytes) for ray in rays['tracks'])
        self.array_aliases=dict(worker_total_is_operator_total=total is operator.total,
            worker_surface_is_operator_stored_surface=surface is operator.stored_surface,
            worker_rays_is_operator_ray_inventory=rays is operator.ray_inventory,
            worker_track_list_is_operator_rays=rays['tracks'] is operator.rays,
            retained_original_track_count=len(rays['tracks']),validated_coefficient_released=True,
            unused_last_q_released=True,last_harmonic_shares_state_harmonics=bool(np.shares_memory(last_harmonic,states.harmonics)),
            last_compact_value_is_last_angle_vector=last_compact_value is angles[-1])
    def white_baseline(self):self.white_baseline_record=self.memory_sample()
    def white_arrays(self,T,L,D,total,total_is_operator_total,nodes,weights):
        self.live_array_bytes.update(white_T=int(T.nbytes),white_L=int(L.nbytes),white_D=int(D.nbytes),
            white_total_logical=int(total.nbytes),quadrature_nodes=int(nodes.nbytes),quadrature_weights=int(weights.nbytes))
        self.array_aliases['white_total_is_operator_total']=bool(total_is_operator_total)
        self.array_aliases['logical_bytes_include_named_aliases_not_RSS_or_native_heap']=True
        self.white_arrays_record=self.memory_sample()
    def white_observed(self,observed):
        if self.phase=='WHITE_PREPARATION':self.live_array_bytes['actions_observed']=int(observed.nbytes)
    def white_native_before(self,completed,ray,state,key,widths,regions,geometry):
        self.native_boundary=dict(successful_native_calls_before=int(completed),successful_native_calls_after=None,
            attempted_native_call=int(completed)+1,original_track_zero_based=int(ray['original_track']),
            polar=int(key[0]),axial_sign=int(key[1]),orientation=int(key[2]),angle_zero_based=int(ray['angle']),
            angular_state=int(state),nr=len(widths),nz=48,groups=370,offset_order=32,
            native_return_code=None,geometry_break_intervals=None,geometry_chords=None,geometry_pieces=None,
            existing_geometry_scalars=None,before_native=self.memory_sample(),after_native=None)
        self.live_array_bytes.update(current_scaled_widths=int(widths.nbytes),current_regions_logical=int(regions.nbytes),
            current_geometry_output=int(geometry.nbytes))
        self.array_aliases.update(current_regions_is_retained_ray_regions=regions is ray['regions'],
            current_scaled_widths_is_planar_widths=widths is ray['planar_widths'])
    def white_native_after(self,completed,return_code,geometry):
        record=self.native_boundary;record['after_native']=self.memory_sample();record['native_return_code']=int(return_code)
        record['successful_native_calls_after']=int(completed)+(1 if return_code==0 else 0)
        if return_code==0:
            record['geometry_break_intervals']=int(geometry[0]);record['geometry_chords']=int(geometry[1]);record['geometry_pieces']=int(geometry[2])
            record['existing_geometry_scalars']=[float(geometry[index]) for index in range(6)]
    def check(self):
        self.check_count_in_phase+=1;self.check_count_total+=1
        before_raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        before_elapsed=time.monotonic()-self.inner.started
        try:return self.inner.check()
        except BaseException as original:
            if not self.failure_checkpoint_attempted:
                self.failure_checkpoint_attempted=True
                try:
                    after_raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                    factor=1 if sys.platform=='darwin' else 1024
                    record=dict(schema='ACTUAL_ORIGINAL_BUDGET_ONCE_FAILURE_CHECKPOINT_V1',status='ORIGINAL_BUDGET_EXCEPTION_UNQUALIFIED',phase=self.phase,check_count_in_phase=self.check_count_in_phase,check_count_total=self.check_count_total,count_scope='ORIGINAL_BUDGET_CHECK_INVOCATIONS_ONLY_NOT_NATIVE_ACTIONS',native_action_count_claimed=False,original_elapsed_seconds_before_check=before_elapsed,original_elapsed_seconds_on_exception=time.monotonic()-self.inner.started,original_started_monotonic_unchanged=self.inner.started,SELF_ru_maxrss_raw_before_original_check=before_raw,SELF_ru_maxrss_bytes_before_original_check=before_raw*factor,SELF_ru_maxrss_raw_on_original_exception=after_raw,SELF_ru_maxrss_bytes_on_original_exception=after_raw*factor,SELF_ru_maxrss_unit='bytes' if factor==1 else 'KiB',measurement_scope='Original check metrics plus one latest explicit native boundary; logical array bytes and returned geometry sizes are not native capacity/allocator attribution',white_baseline_before_array_allocation=self.white_baseline_record,white_after_array_allocation=self.white_arrays_record,latest_white_native_boundary=self.native_boundary,live_array_logical_bytes=self.live_array_bytes,live_array_aliases=self.array_aliases,current_SELF_resident_reader='Darwin task_info MACH_TASK_BASIC_INFO=20 packed4 count12 from installed primary headers; original ru_maxrss retained separately',current_SELF_resident_reader_error=self.resident_error,live_array_scope='Explicit worker/operator/generator numeric arrays; Python container/object overhead, allocator-retained pages and native vector capacities not measured' ,original_exception_type=type(original).__name__,original_exception_repr=repr(original),original_helper_source_pin=self.source_pin,original_budget_instance_type_unchanged=True,original_budget_check_delegated_every_time=True,original_caps=c.CAPS,physics_qualified=False,goal_complete=False)
                    raw=(json.dumps(record,indent=2,allow_nan=False)+'\n').encode();require(len(raw)<=8192,'once diagnostic checkpoint8KiB ceiling')
                    with self.path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
                except BaseException as diagnostic_error:
                    self.checkpoint_write_error=repr(diagnostic_error)[:512]
                    try:os.write(2,('Original Budget failure checkpoint could not be saved: '+self.checkpoint_write_error+'\n').encode()[:1024])
                    except BaseException:pass
            raise

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--plan-pin',required=True);ap.add_argument('--report',required=True)
    ap.add_argument('--expected-parent-pid',type=int,required=True);args=ap.parse_args()
    require(os.getppid()==args.expected_parent_pid and not sys.flags.optimize and sys.getprofile() is None
        and all(os.environ.get(k)=='1' for k in c.THREADS), 'genuine owning singlethread child')
    pp=json.loads(args.plan_pin);plan=c.read(pp);c.check_finite(plan)
    sys.path.insert(0,plan['exact_v2_source_root'])
    for row in plan['explicit_import_bindings']: c.load(row['pin'],row['module'])
    helpers=c.load(plan['original_v6_vector_helper_pin'],'full_operator_original_v6_vectors')
    original_budget=helpers.Budget();budget=BoundedBudgetDiagnostic(original_budget,helpers.Budget,Path(args.report).parent/'ORIGINAL_BUDGET_FAILURE_CHECKPOINT.json',plan['original_v6_vector_helper_pin']);started=original_budget.started;phases={}
    authority=sys.modules['current_formal_input_authority']
    binding=authority.KernelBinding(plan['actual_kernel_origin_pin'],budget)
    binding.verify(plan['actual_kernel_library_pin']['path'])
    adapter=sys.modules['actual_track_saved_adapter'];out=Path(args.report).parent
    tmp=out/'sqlite_temp';tmp.mkdir()
    vectors,rows=helpers.small_vectors(plan['observed_final55_SQLite_pin'],plan['observed_final55_pool_pin'],
        [(('MACROLIB','GROUP',g,'NTOT0'),8) for g in range(1,371)],adapter,tmp,budget)
    total=np.repeat(np.stack(vectors,axis=1).astype('d')[:,None,:],48,axis=1)
    # New actual capture preserves only the four original REAL32 records.
    # Their old SQL/pool identities are historical closed consumption; they
    # are not reopened, current-checked, regenerated or used as live inputs.
    capture=c.read(plan['actual_compact_capture_report_pin'])
    vector_pin=plan['compact_native_vector_pin'];qpath=c.current(vector_pin)
    with qpath.open('rb') as stream:
        require(c.identity(os.fstat(stream.fileno()))==vector_pin['identity'],'compact vector opened7')
        raw=stream.read(105)
        require(len(raw)==104 and stream.read(1)==b'' and
            c.identity(os.fstat(stream.fileno()))==vector_pin['identity'],'original compact104B fullEOF')
    require(__import__('hashlib').sha256(raw).hexdigest()==vector_pin['sha256'],'compact104B exact SHA')
    c.current(vector_pin);angles=[];angle_rows=[]
    for descriptor in capture['native_vector_record_descriptors']:
        offset=descriptor['offset_bytes'];count=descriptor['words'];payload=raw[offset:offset+count*4]
        require(len(payload)==count*4 and __import__('hashlib').sha256(payload).hexdigest()
            ==descriptor['native_payload_sha256']==descriptor['captured_payload_sha256'],'four original record bits preserved')
        value=np.frombuffer(payload,dtype='<f4').copy()
        require(value.shape==(count,) and np.isfinite(value).all(),'original finite REAL32 vector shape')
        angles.append(value);angle_rows.append(descriptor['original_native_row'])
    budget.check()
    support=sys.modules['terminal_AB_and_current_track_inputs']
    rays=support.native_track_inventory(plan['current_original_radial_track_pin'])
    states=sys.modules['native_full_angular_p2'].angular_states_from_native(
        *[v.astype('d') for v in angles[:3]],rays['azimuth_xy'][:,0],rays['azimuth_xy'][:,1])
    axial_pin=plan['current_axial_track_pin'];c.current(axial_pin)
    axial_records={}
    with sys.modules['snapshot_control_preflight']._open_xsm(axial_pin['path']) as archive:
        d=archive.root
        def record(name,dtype,count):
            value,meta=support.array(archive,d,name,dtype,count);axial_records[name]=meta;return value
        state=record('STATE-VECTOR','<i4',40);area=record('AREA2D','<f4',8)
        dz=record('VOL1D','<f4',48);mat=record('MAT1D','<i4',48)
        volume=record('VOLUME','<f4',384).reshape(8,48);ncode=record('NCODE','<i4',2)
        formal={k:record(k,'<f4',n) for k,n in (('U',32),('W',32),('PL',96))}
    c.current(axial_pin)
    require(state[0]==384 and state[5]==8 and state[6]==48 and state[7]==3 and state[14]==32
        and np.array_equal(mat,np.repeat([1,2,3],16)) and np.array_equal(dz,np.full(48,np.float32(150/48)))
        and np.all(area>0) and np.all(volume>0) and np.all(ncode==1), 'actual formal H150/NZ48/SN32 grid/vacuum')
    require(np.all(np.abs(volume.astype('d')-area.astype('d')[:,None]*dz.astype('d')[None,:])
        <=np.spacing(volume).astype('d')/2), 'original actual halfULP extrusion check')
    surface=np.repeat(angles[3][8:].astype('d')[:,None],48,axis=1)*dz
    budget.set_phase('SOURCE_POSITIVITY');coefficient=fixture();parity=np.array([1,1,-1,1,1,-1,1,-1,1])
    require(np.array_equal(coefficient[:,::-1,:,:]*parity,coefficient), 'predeclared z-reflected fixture parity')
    source_min=np.inf
    for h in states.harmonics:
        budget.check();q=np.einsum('m,rzgm->rzg',h,coefficient);source_min=min(source_min,float(q.min()))
    require(source_min>0 and len(rays['tracks'])==11364 and len(states.keys)==1536
        and states.azimuth_count==96, 'positive independent nine-coefficient source and complete native bins')
    Operator=sys.modules['current_formal_full370_ray_operator'].WholeRayOperator
    operator=Operator(binding.library_pin['path'],rays,states,total,volume.astype('d'),out/'white_cache',
        32,1,plan['physical_checks'],'GEOMETRIC_LAYER_LOCAL_WHITE',surface,budget,binding)
    validated_fixture_digest=digest(coefficient);released_fixture_bytes=int(coefficient.nbytes);released_last_q_bytes=int(q.nbytes);del coefficient,q
    budget.bind_white_context(total,operator,rays,states,vectors,angles,state,area,dz,mat,volume,ncode,formal,surface,parity,h,value)
    phases['setup_seconds']=time.monotonic()-started;t=time.monotonic();budget.set_phase('WHITE_PREPARATION')
    operator.prepare_white();phases['prepare_white_seconds']=time.monotonic()-t
    require(operator.prepared is True, 'one complete original white preparation')
    budget.set_phase('SOURCE_RECREATE');coefficient=fixture();require(digest(coefficient)==validated_fixture_digest,'complete recreated original REAL64 fixture exactly equals first validated fixture')
    t=time.monotonic();budget.set_phase('OPERATOR_APPLY');result=operator.apply(coefficient);phases['apply_seconds']=time.monotonic()-t
    require(operator.operator_calls==1 and result['complete_coverage'] is True
        and result['action_calls']==363648 and result['actions_per_complete_group_sweep']==181824
        and result['original_tracks']==11364, 'exactly one full two-sweep action, no retry')
    arrays={k:v for k,v in result.items() if isinstance(v,np.ndarray)}
    require(all(np.isfinite(v).all() for v in arrays.values()) and result['minimum_angular_flux64']>=0
        and result['minimum_angular_integral64']>=0, 'complete finite output and positive angular survival')
    require(np.all(result['unfitted_physical_white_relative64']<=plan['physical_checks']['global']),
        'unfitted current physical white conservation, no rescaling')
    end=result['axial_outgoing_current64'];signed=np.stack([-end[0],end[1]])
    require(np.all(end>=0), 'outward end currents nonnegative for positive source')
    reflection=relative(signed[0]+signed[1],np.maximum(np.abs(signed[0]),np.abs(signed[1])))
    moment_scale=np.broadcast_to(np.max(np.abs(result['moments64']),axis=(0,1),keepdims=True),
        result['moments64'].shape)
    moment_reflection=relative(result['moments64'][:,::-1,:,:]*parity-result['moments64'],moment_scale)
    require(np.max(reflection)<=plan['physical_checks']['global']
        and np.max(moment_reflection)<=plan['physical_checks']['global'], 'original global ceiling for fixture reflection')
    arrays.update(signed_two_end_plus_z_current64=signed,two_end_reflection_relative64=reflection,
        nine_moment_reflection_relative64=moment_reflection,geometric_incoming64=operator.denominator,
        stored_native_surface64=surface,geometric_minus_stored_surface64=operator.denominator.reshape(6,48)-surface)
    budget.set_phase('OUTPUT_PUBLICATION');budget.check();data=out/'FULL370_REAL_OPERATOR_CONTROL_ARRAYS.npz'
    with data.open('xb') as f:np.savez(f,**arrays);f.flush();os.fsync(f.fileno())
    cache=[c.pin(p) for p in sorted(operator.cache.glob('white_g*.npz'))]
    require(len(cache)==370 and [Path(p['path']).name for p in cache]==[
        f'white_g{g:04d}.npz' for g in range(1,371)], 'all370 fresh white files retained')
    for p in plan['scientific_input_current7_pins']:c.current(p)
    for row in plan['explicit_import_bindings']:c.exact(row['pin'])
    binding.verify(binding.library_pin['path']);c.read(pp);budget.check()
    report=dict(schema='ACTUAL_FULL370_REAL_CURRENT_MATERIAL_OPERATOR_CONTROL_V1',
        status='ACTUAL_FULL370_REAL_OPERATOR_ONE_PREPARATION_ONE_APPLY_CLOSED0_ONLY',passed=True,
        current_case_spec_pin=plan['current_case_spec_pin'],complete_original_tracks=11364,
        white_preparation_actions=181824,actions_per_group_sweep=181824,transport_action_calls=363648,
        prepare_white_calls=1,apply_calls=1,groups=370,axial_cells=48,retained_moments=9,H=150.,
        offset_order=32,working_group_chunk=1,boundary_model='GEOMETRIC_LAYER_LOCAL_WHITE',
        original_native_polar_count=4,original_azimuth_count=96,native_angular_states=1536,
        extra_times96_factor=False,formal_SN32_equivalence_claimed=False,
        signed_current_scope='TWO_OUTWARD_END_FACES_CONVERTED_TO_PLUS_Z; NO49FACE_PROFILE',
        source_is_independent_positive_nine_coefficient_fixture=True,observed_six_missing_capture_moments_used=False,
        source_fixture_formula=plan['source_fixture_formula'],source_fixture_digest=digest(coefficient),
        minimum_reconstructed_source=source_min,input_array_digests=dict(total=digest(total),volume=digest(volume.astype('d')),
            stored_surface=digest(surface),harmonics=digest(states.harmonics),
            complete_original_ray_inventory=authority.complete_value_digest(rays),
            complete_native_angular_state_fields=authority.complete_states_digest(states),
            formal_SN32={k:digest(v) for k,v in formal.items()}),
        actual_original_total_record_metadata=rows,actual_original_angle_surface_record_metadata=angle_rows,
        actual_original_axial_record_metadata=axial_records,actual_output_array_digests={k:digest(v) for k,v in arrays.items()},
        complete_output_array_pin=c.pin(data),complete_white_cache_pins=cache,
        physical_checks=plan['physical_checks'],maximum_physical_white_relative=float(np.max(result['unfitted_physical_white_relative64'])),
        maximum_white_matrix_relative=float(np.max(result['white_matrix_residual_relative64'])),
        maximum_axial_source_return_relative=float(np.max(result['axial_source_return_assembly_relative64'])),
        maximum_two_end_reflection_relative=float(np.max(reflection)),maximum_nine_moment_reflection_relative=float(np.max(moment_reflection)),
        moment_reflection_scale='complete region/layer maximum per original group and moment; zero-scale nonzero refused',
        minimum_angular_flux64=result['minimum_angular_flux64'],minimum_angular_integral64=result['minimum_angular_integral64'],
        original_per_action_shared_faces_exact_zero=True,actual_kernel_origin_pin=plan['actual_kernel_origin_pin'],
        actual_kernel_library_pin=binding.library_pin,actual_kernel_build_report_pin=binding.report_pin,
        complete_kernel_source_pins=binding.source_pins,original_caps=c.CAPS,phase_timings=phases,
        child_elapsed_seconds=time.monotonic()-started,child_SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        all_control_assertions_passed=True,validated_original_fixture_digest=validated_fixture_digest,recreated_fixture_digest_equal=True,released_during_white_fixture_bytes=released_fixture_bytes,released_during_white_unused_q_bytes=released_last_q_bytes,original_Budget_check_delegated_every_time=True,original_Budget_started_unchanged=True,bounded_budget_failure_checkpoint_path=str(budget.path),original_Budget_check_count_total=budget.check_count_total,budget_count_scope='CHECK_INVOCATIONS_NOT_NATIVE_ACTIONS',**c.FALSE)
    rp=c.write(args.report,report);budget.check()
    print(json.dumps(dict(status=report['status'],report_pin=rp,**c.FALSE)),flush=True)

if __name__=='__main__':main()
