"""One unadmitted full current-material white preparation and fixed-source action."""
import argparse, json, os, resource, sys, time
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
    budget=helpers.Budget();started=budget.started;phases={}
    authority=sys.modules['current_formal_input_authority']
    binding=authority.KernelBinding(plan['actual_kernel_origin_pin'],budget)
    binding.verify(plan['actual_kernel_library_pin']['path'])
    adapter=sys.modules['actual_track_saved_adapter'];out=Path(args.report).parent
    tmp=out/'sqlite_temp';tmp.mkdir()
    vectors,rows=helpers.small_vectors(plan['observed_final55_SQLite_pin'],plan['observed_final55_pool_pin'],
        [(('MACROLIB','GROUP',g,'NTOT0'),8) for g in range(1,371)],adapter,tmp,budget)
    total=np.repeat(np.stack(vectors,axis=1).astype('d')[:,None,:],48,axis=1)
    angles,angle_rows=helpers.small_vectors(plan['native_A1_SQLite_pin'],plan['native_A1_pool_pin'],
        [(('TRACK',1,k),4) for k in ('XMU$MCCG','ZMU$MCCG','WZMU$MCCG')]
        +[(('TRACK',1,'V$MCCG'),14)],adapter,tmp,budget)
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
    coefficient=fixture();parity=np.array([1,1,-1,1,1,-1,1,-1,1])
    require(np.array_equal(coefficient[:,::-1,:,:]*parity,coefficient), 'predeclared z-reflected fixture parity')
    source_min=np.inf
    for h in states.harmonics:
        budget.check();q=np.einsum('m,rzgm->rzg',h,coefficient);source_min=min(source_min,float(q.min()))
    require(source_min>0 and len(rays['tracks'])==11364 and len(states.keys)==1536
        and states.azimuth_count==96, 'positive independent nine-coefficient source and complete native bins')
    Operator=sys.modules['current_formal_full370_ray_operator'].WholeRayOperator
    operator=Operator(binding.library_pin['path'],rays,states,total,volume.astype('d'),out/'white_cache',
        32,1,plan['physical_checks'],'GEOMETRIC_LAYER_LOCAL_WHITE',surface,budget,binding)
    phases['setup_seconds']=time.monotonic()-started;t=time.monotonic()
    operator.prepare_white();phases['prepare_white_seconds']=time.monotonic()-t
    require(operator.prepared is True, 'one complete original white preparation')
    t=time.monotonic();result=operator.apply(coefficient);phases['apply_seconds']=time.monotonic()-t
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
    budget.check();data=out/'FULL370_REAL_OPERATOR_CONTROL_ARRAYS.npz'
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
        all_control_assertions_passed=True,**c.FALSE)
    rp=c.write(args.report,report);budget.check()
    print(json.dumps(dict(status=report['status'],report_pin=rp,**c.FALSE)),flush=True)

if __name__=='__main__':main()
