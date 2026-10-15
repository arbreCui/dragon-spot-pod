"""Current-data complete finite-height physical-source response, one family.

The complete H20/Nz4 inventory is measured and exactly replayed at the original
physical/operator gates before common geometric white return. This is a fixed
source reference for three preselected groups, not coupled AAA qualification.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import time

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'validation/axial_material'))
import qualify_refined_AAA_layered_input_pilot as pilot
from probe_refined_AAA_white_odd_response import (
    ART, GROUPS, DiskResources, SerialExecutor, digest, read, write_new, verify, require_file,
)
OUT=ART/'axial-material-AAA-white-trace-refined-layered-full-20261005'
PILOT=pilot.OUT
PILOT_SEAL='f487824093f7d145ed919b0db736d1d7d1bdc66f7148f228f2f67199685b7cf0'
FAMILY='h20_n4'
WORKER=ROOT/'validation/axial_material/run_refined_AAA_layered_full_batch.py'
AUDITOR=ROOT/'validation/axial_material/audit_refined_AAA_layered_full.py'
ACTION=ROOT/'validation/iterative/native_layered_full_action.py'
ANALYTIC=ROOT/'validation/iterative/test_native_layered_full_action.py'
GUARD_PROOF=Path('/private/tmp/axmat_refined_full_live_guard_host_20261005')


class OwnRSSSerialExecutor(SerialExecutor):
    """Original own-group liveness/disk/wall guard, with live own-child RSS."""
    def _process(self,command,directory,stdin,out,limit):
        import os
        process=subprocess.Popen(command,cwd=directory,stdin=stdin,stdout=out,
            stderr=subprocess.STDOUT,env=self.env,start_new_session=True)
        started=time.monotonic();peak=0.;failure=None;last_disk=0.
        read_fd,write_fd=os.pipe()
        try:watchdog=self.bounded.start_liveness_watchdog(read_fd,process.pid,self.bounded.TERM_GRACE_SECONDS)
        except BaseException:
            os.close(read_fd);os.close(write_fd);self.bounded.terminate_group(process);raise
        os.close(read_fd)
        try:
            try:
                while process.poll() is None:
                    now=time.monotonic()
                    if now-last_disk>=5:
                        self.resources.check();last_disk=now
                    if now-started>=limit:raise RuntimeError('own-child wall cap reached')
                    sample=subprocess.run(['/bin/ps','-o','rss=','-p',str(process.pid)],
                        capture_output=True,text=True,timeout=min(2.,max(.05,limit-(now-started))))
                    if sample.returncode and process.poll() is None:raise RuntimeError('own-child RSS unavailable')
                    if sample.stdout.strip():peak=max(peak,float(sample.stdout.strip())/1024)
                    if peak>=512:raise RuntimeError('own-child 512 MiB RSS cap reached')
                    try:process.wait(timeout=min(.2,max(.001,limit-(time.monotonic()-started))))
                    except subprocess.TimeoutExpired:pass
                self.resources.check()
            except BaseException as error:
                failure=repr(error);self.bounded.terminate_group(process);raise
        finally:
            self.bounded.finish_liveness_watchdog(write_fd,watchdog)
            write_new(Path(out.name).with_suffix('.watchdog.json'),dict(
                command=command,pid=process.pid,returncode=process.poll(),
                elapsed_seconds=time.monotonic()-started,sampled_peak_rss_mib=peak,
                limit_failure=failure,wall_cap_seconds=limit,rss_cap_mib=512,
                own_child_only=True,liveness_group_cleanup=True))
        if process.returncode:raise RuntimeError('own-child stage failed; no retry')


def verify_pilot():
    require_file(PILOT/'seal.json',PILOT_SEAL)
    verify({str(PILOT/n):h for n,h in read(PILOT/'seal.json')['files'].items()})
    verify(read(PILOT/'declaration.json')['files']);pilot.verify_angular()
    r=read(PILOT/'result.json')
    if r['classification']!='COMPLETE_CURRENT_DATA_FINITE_HEIGHT_INPUT_PILOT_ONLY' or not r['all_selected_physical_checks_passed']:
        raise ValueError('complete current-data input pilot required')


def supplemental_angles():
    import numpy as np
    from probe_refined_AAA_white_odd_response import _open_xsm,field
    old=pilot.OLD/'inputs/track_data.bin'
    require_file(old,'b5358f120d402b97084f68893b002d90f70c96d3d40359017774224e42a9efda')
    with old.open('rb') as handle:
        handle.seek(160);old_xmu=handle.read(16)
        handle.seek(208);old_x=np.frombuffer(handle.read(768),'<f8').copy();old_y=np.frombuffer(handle.read(768),'<f8').copy()
        old_harm=handle.read(4608)
    with (pilot.ANGULAR/'inputs/rays.bin').open('rb') as handle:
        def record():
            marker=handle.read(4)
            if len(marker)!=4:raise ValueError('missing original ray metadata')
            n=struct.unpack('<i',marker)[0];raw=handle.read(n)
            if len(raw)!=n or handle.read(4)!=marker:raise ValueError('invalid original ray metadata')
            return raw
        _,ncom,_,_=struct.unpack('<4siii',record())
        for _ in range(ncom):record()
        record();metadata=[record() for _ in range(6)]
    if [len(x) for x in metadata]!=[60,60,24,24,1536,768]:raise ValueError('original metadata dimensions differ')
    values=np.frombuffer(metadata[4],'<f8');azx,azy=values[0::2].copy(),values[1::2].copy()
    with _open_xsm(pilot.ANGULAR/'inputs/track.xsm') as archive:
        xmu=field(archive,archive.root,'XMU$MCCG','<f4',4)
    if xmu.tobytes()!=old_xmu or azx.tobytes()!=old_x.tobytes() or azy.tobytes()!=old_y.tobytes():
        raise ValueError('current native polar/azimuth identity differs')
    sine=np.sqrt(1-xmu.astype(float)**2);harm=np.ones((4,3,96),dtype='<f4')
    harm[:,1,:]=sine[:,None]*azy[None,:];harm[:,2,:]=sine[:,None]*azx[None,:]
    with np.load(PILOT/'inputs/current_inventory.npz') as z:actual=z['harm'].astype('<f4')
    if harm.tobytes(order='F')!=old_harm or actual.tobytes(order='F')!=old_harm:
        raise ValueError('native in-plane harmonic reconstruction differs')
    return dict(current_XMU_byte_exact=True,current_96_azimuth_pairs_byte_exact=True,
        current_MOCCHR_harmonics_byte_exact=True,XMU_used_directly=True,
        native_export_sha256=digest(old),ray_metadata_lengths=[len(x) for x in metadata],
        formula='NDIM2/NANI1: [1, sqrt(1-XMU^2)*azy, sqrt(1-XMU^2)*azx], REAL32 final storage. '
                'Do not infer native XMU from ZMU for jx.')


def prepare():
    import numpy as np
    verify_pilot()
    guard=read(GUARD_PROOF/'guard_controls.json')
    tested=GUARD_PROOF/'tested_driver_source.py';require_file(tested,guard['source_sha256'])
    def guard_source(path):
        code=path.read_text()
        return next(ast.get_source_segment(code,n) for n in ast.parse(code).body
                    if isinstance(n,ast.ClassDef) and n.name=='OwnRSSSerialExecutor')
    if (guard_source(tested)!=guard_source(Path(__file__).resolve())
            or not guard['positive_child_completed'] or not guard['actual_oversize_child_rejected']
            or not guard['terminated_own_child_not_live'] or guard['rss_cap_mib']!=512):
        raise ValueError('actual live own-child guard positive/negative controls required')
    verify({str(GUARD_PROOF/n):h for n,h in guard['control_files'].items()})
    identity=supplemental_angles()
    for source in [Path(__file__).resolve(),WORKER,AUDITOR]:compile(source.read_text(),str(source),'exec')
    old_manifest={n.lstrip('*'):h for h,n in (line.split(None,1) for line in (pilot.OLD/'result.sha256').read_text().splitlines())}
    counts=[]
    for p in range(4):
        file=pilot.OLD/f'inputs/counts_p{p}_h20_n4.npz';require_file(file,old_manifest[str(file.relative_to(pilot.OLD))])
        with np.load(file) as z:
            if not np.array_equal(z['original_tracks'],np.arange(11364)) or z['counts'].shape!=(2,2,2,11364,3):
                raise ValueError('sealed geometric count inventory differs')
            counts.append(z['counts'].copy())
    prior_bound=pilot.OLD/'resource_admission.json'
    require_file(prior_bound,old_manifest['resource_admission.json'])
    bounds=read(prior_bound)['per_batch_bound_bytes']
    cases=[]
    for p in range(4):
        for first in range(0,11364,256):
            stop=min(first+256,11364)
            score=int(counts[p][:,:,1,first:stop,2].sum())*3*3*66
            cases.append(dict(id=f'p{p}_{FAMILY}_b{first:05d}',polar=p,height=20.,nz=4,
                first=first,stop=stop,preflight=False,geometric_piece_column_proxy=score))
    if len(cases)!=180:raise ValueError('complete 180-batch inventory required')
    preflight=max(cases,key=lambda c:c['geometric_piece_column_proxy'])['id']
    OUT.mkdir(exist_ok=False)
    for name in ['runtime','inputs','AAA','runs','primary','receipts','preflight','verification','white']:(OUT/name).mkdir()
    (OUT/'preflight/live_guard').mkdir()
    for name in ['guard_controls.json','tested_driver_source.py',*guard['control_files']]:
        shutil.copy2(GUARD_PROOF/name,OUT/'preflight/live_guard'/name)
    shutil.copy2(PILOT/'runtime/cached.dylib',OUT/'runtime/cached.dylib')
    shutil.copy2(PILOT/'runtime/run_bounded_dragon.py',OUT/'runtime/run_bounded_dragon.py')
    shutil.copy2(PILOT/'inputs/current_inventory.npz',OUT/'inputs/inventory.npz')
    for p in range(4):
        shutil.copy2(pilot.OLD/f'inputs/counts_p{p}_h20_n4.npz',OUT/f'inputs/counts_p{p}_h20_n4.npz')
    write_new(OUT/'angular_identity.json',identity)
    source_bound=sum(bounds[c['id']] for c in cases)
    added_arrays=180*256*3*2*2*10*8
    # Preserve the prior same-topology uncompressed source-coordinate bound;
    # separately allow new control arrays, 1 MiB/batch headers and 10% growth.
    primary_bound=int(1.1*(source_bound+added_arrays+180*2**20))+1
    write_new(OUT/'plan.json',dict(schema='AXMAT_CURRENT_LAYERED_FULL_FAMILY_PLAN_V1',batches=cases,
        preflight_batch_ids=[preflight],groups=GROUPS,family=FAMILY,expected_primary_batches=180,
        expected_replay_batches=180,expected_physical_states_per_phase=1090944,
        expected_input_coordinate_evaluations_per_phase=72002304,
        state_order='polar-major, negative then positive axial sign; planar orientations summed before white.',
        worker_orders=[16,32],complete_original_record_count=11364,
        white_source_coordinates=256,white_positive_controls=2,common_face_layer_amplitudes=24,
        primary_uncompressed_bound_bytes=primary_bound,prior_source_bound_bytes=source_bound,
        added_control_array_bound_bytes=added_arrays,
        audit_white_receipt_reserve_bytes=2593062912,reserve_bytes=2**30,
        replay_duplicate_scientific_bytes=0))
    files=dict(read(PILOT/'declaration.json')['files'])
    paths=[Path(__file__).resolve(),WORKER,AUDITOR,ACTION,ANALYTIC,PILOT/'seal.json',
        pilot.OLD/'inputs/track_data.bin',prior_bound,ROOT/'src/MOCCHR.f',Path('/bin/ps'),
        ROOT/'validation/iterative/audit_native_layered_full.py',
        *[ROOT/'validation/iterative'/n for n in ['native_layered_batch_storage.py','native_layered_storage.py',
          'native_layered_full_action.py','native_layered_transport.py','calibrate_native_oblique_streaming.py']],
        *[pilot.OLD/f'inputs/counts_p{p}_h20_n4.npz' for p in range(4)],
        *[OUT/f'inputs/counts_p{p}_h20_n4.npz' for p in range(4)],
        OUT/'runtime/cached.dylib',OUT/'runtime/run_bounded_dragon.py',OUT/'inputs/inventory.npz',
        OUT/'angular_identity.json',OUT/'plan.json']
    paths += [p for p in (OUT/'preflight/live_guard').iterdir() if p.is_file()]
    files.update({str(p.resolve()):digest(p) for p in paths});verify(files)
    roots=sorted(set(read(PILOT/'declaration.json')['resource_roots'])|{str(OUT)})
    resource=DiskResources(ART,roots,8*2**30,96*2**30)
    write_new(OUT/'declaration.json',dict(schema='AXMAT_CURRENT_LAYERED_FULL_FAMILY_V1',files=files,
        plan_sha256=digest(OUT/'plan.json'),total_wall_seconds=21600,
        batch_wall_seconds=600,audit_wall_seconds=600,action_wall_seconds=600,final_wall_seconds=600,
        resource_roots=roots,min_free_bytes=8*2**30,artifact_budget_bytes=96*2**30,resources_before=resource.check(),
        threads=1,numeric_children_at_once=1,retries=0,rss_cap_mib=512,rss_poll_seconds=.2,
        requires_host_process_metadata_access=True,
        live_guard_controls='Actual short positive child completed; actual oversized own child rejected at 512 MiB, '
                            'terminated and confirmed not live. Tested live-guard class is byte-exact in this driver. '
                            'A prior sandbox-denied positive control is preserved separately in /private/tmp; '
                            'no scientific experiment had been created or started in that denied control.',
        numeric_environment=read(PILOT/'declaration.json')['numeric_environment'],
        preflight='One maximum geometric-workload batch is executed primary and replay first. '
                  'It is charged and counted once, never rerun in the main inventory. '
                  'Full admission uses actual elapsed time plus remaining work-scaled wall forecast with factor 1.5. '
                  'Disk uses sealed same-topology full uncompressed bounds, new-array/header allowances and reserve.',
        full_inventory='All 11364 original records; 4 native polar nodes, both planar orientations and both independent '
                       'axial signs, current totals for groups 51/61/98, H20/Nz4, all 66 source/control coordinates, '
                       'orders 16/32; independent full in-memory byte replay.',
        white='24 common face-layer amplitudes mix all eight angular states. Geometric incoming measure is '
              'the physical closure denominator. Stored native surface normalizer is retained only as a separate comparison.',
        gates=dict(raw_physical_balance=1e-10,geometry_action_and_order=5e-12,independent_reference=2e-13,
                   shared_face_absolute=0.,vacuum_axial_incoming_absolute=0.,positive_fields_required=True),
        independent_checks='Lossless structural-zero raw responses for every order32 record; independent primitive/cell/global '
                           'witnesses and tensordot operator/current assembly; coverage exactly one in every group/orientation/sign; '
                           '48 worst-order independent decimal rectangle/adaptive full-field references; analytic white negative controls.',
        prior_zero_gradient_regression_claimed=False,original_accuracy_thresholds_changed=False,
        production_solver_changed=False,CE_data_used=False,AAA_accuracy_qualified=False,
        scattering_fission_iteration_qualified=False,local_inverse_propagation_qualified=False,ABA_admitted=False,
        decision='Qualify only this current-data full discrete physical-source and geometric-white family. '
                 'Next compare predeclared local propagation candidates at identical source/grid/boundaries, '
                 'then advance coupled reference; no AAA or ABA qualification follows from this family.'))
    print(json.dumps(dict(declaration_sha256=digest(OUT/'declaration.json'),preflight_batch=preflight,batches=180)))


def check_receipt(case,phase):
    receipt=read(OUT/'receipts'/phase/(case+'.json'))
    expected={f'raw_g{g}_o{o}_m{s}.npz' for g in GROUPS for o in [1,-1] for s in [-1,1]}|{'operators.npz','controls.npz','result.json'}
    if set(receipt['files'])!=expected:raise ValueError('all 15 complete scientific files required')
    for name,entry in receipt['files'].items():
        path=OUT/'primary'/case/name
        if path.stat().st_size!=entry['bytes']:raise ValueError('scientific receipt length changed')
        require_file(path,entry['sha256'])
    if phase=='replay':
        if receipt.get('all_scientific_bytes_identical') is not True or receipt['files']!=read(OUT/'receipts/primary'/(case+'.json'))['files']:
            raise ValueError('complete replay receipt differs')
    return receipt


def admit():
    declaration=read(OUT/'declaration.json');plan=read(OUT/'plan.json');probe=plan['preflight_batch_ids'][0]
    for phase in ['primary','replay']:check_receipt(probe,phase)
    usage=[read(OUT/'runs'/f'{phase}_{probe}_resources.json') for phase in ['primary','replay']]
    elapsed=max(u['elapsed_seconds'] for u in usage)
    probe_case=next(c for c in plan['batches'] if c['id']==probe)
    proxy=sum(c['geometric_piece_column_proxy'] for c in plan['batches'])/probe_case['geometric_piece_column_proxy']
    elapsed_total=time.monotonic()-read(OUT/'run_claim.json')['started_monotonic']
    remaining_worker_forecast=2*elapsed*(proxy-1)*1.5
    forecast_wall=elapsed_total+remaining_worker_forecast+6*600+600
    resource=DiskResources(ART,declaration['resource_roots'],declaration['min_free_bytes'],declaration['artifact_budget_bytes'])
    now=resource.check();probe_bytes=sum(x['bytes'] for x in check_receipt(probe,'primary')['files'].values())
    # Charge the complete bound again, including the preflight already saved:
    # this deliberately errs conservatively and does not rely on compression.
    forecast_disk=(now['artifact_bytes']+plan['primary_uncompressed_bound_bytes']
        +plan['audit_white_receipt_reserve_bytes']+plan['reserve_bytes'])
    ok=(forecast_wall<declaration['total_wall_seconds']
        and forecast_disk<declaration['artifact_budget_bytes']
        and now['disk_free_bytes']-(forecast_disk-now['artifact_bytes'])>declaration['min_free_bytes'])
    write_new(OUT/'admission.json',dict(full_execution_admitted=ok,plan_sha256=digest(OUT/'plan.json'),
        measured_preflight_batch=probe,measured_max_worker_seconds=elapsed,geometric_proxy_ratio=proxy,
        elapsed_total_at_admission=elapsed_total,remaining_worker_forecast_seconds=remaining_worker_forecast,
        remaining_audit_white_final_wall_reserve_seconds=3600,admission_parent_overhead_reserve_seconds=600,
        forecast_wall_seconds=forecast_wall,forecast_artifact_bytes=forecast_disk,
        measured_primary_batch_bytes=probe_bytes,preflight_charged_to_total=True,
        preflight_counted_once=True,resources=now))
    if not ok:raise ValueError('actual full-family resource admission refused; no full inventory started')
    print('AXMAT-CURRENT-FULL-FAMILY-ADMITTED')


def finalize():
    import numpy as np
    plan=read(OUT/'plan.json');declaration=read(OUT/'declaration.json');verify(declaration['files']);verify_pilot()
    observed={}
    for phase in ['primary','replay']:
        states=coordinates=records=0
        for c in plan['batches']:
            check_receipt(c['id'],phase)
            summary=read(OUT/'primary'/c['id']/'result.json');nt=c['stop']-c['first']
            if (summary['case']!=c or summary['original_records']!=nt
                    or summary['physical_states']!=nt*24 or summary['physical_coordinate_evaluations']!=nt*24*66
                    or not summary['current_totals_used'] or not summary['all_checks_passed']):
                raise ValueError('actual complete original-coordinate batch counters required')
            states+=summary['physical_states'];coordinates+=summary['physical_coordinate_evaluations'];records+=summary['original_records']
        if (states,coordinates,records)!=(1090944,72002304,4*11364):
            raise ValueError('observed full scientific coverage differs')
        observed[phase]=dict(physical_states=states,coordinate_evaluations=coordinates,polar_records=records)
    results=[]
    for p in range(4):
        folder=OUT/'verification'/f'p{p}_{FAMILY}';r=read(folder/'result.json')
        if not r['all_checks_passed'] or not r['all_original_indices_once'] or r['original_tracks']!=11364 or r['physical_states']!=11364*12:
            raise ValueError('complete current-data per-polar coverage/audit required')
        with np.load(folder/'operators.npz') as z:
            if z['coverage'].shape!=(3,2,2,11364) or not np.all(z['coverage']==1):raise ValueError('full original coordinate coverage differs')
        if len(r['independent_traces'])!=12:raise ValueError('all 48 independent reference traces required')
        results.append(r)
    white=read(OUT/'white'/FAMILY/'result.json')
    if (not white['all_checks_passed'] or white['original_tracks']!=11364 or not white['geometric_normalizer_used']
            or white['independent_angular_states']!=8 or white['white_source_coordinates']!=256
            or white['physical_axial_incoming_zero'] is not True or [g['group'] for g in white['groups']]!=GROUPS
            or any([o['order'] for o in g['orders']]!=[16,32] for g in white['groups'])):
        raise ValueError('full current-data physical white qualification required')
    if not read(OUT/'preflight/action_test.json')['passed']:raise ValueError('analytic white controls not passed')
    stages=read(OUT/'AAA/stages.json')['stages']
    if (len(stages)!=368 or stages[-1]['label']!='verification' or stages[-1]['status']!='RUNNING'
            or any(s['status']!='PASS' for s in stages[:-1])):
        raise ValueError('all preceding declared actual stages and current verifier required')
    watchdogs=[]
    for stage in stages[:-1]:
        watch=read((OUT/(stage['label']+'.log')).with_suffix('.watchdog.json'))
        if (watch['returncode']!=0 or watch['limit_failure'] is not None or watch['sampled_peak_rss_mib']>=512
                or watch['elapsed_seconds']>=600 or not watch['own_child_only']):
            raise ValueError('all live own-child resource receipts required')
        watchdogs.append(watch)
    result=dict(classification='COMPLETE_CURRENT_DATA_H20_N4_FULL_FIXED_SOURCE_WHITE_ONLY',
        groups=GROUPS,original_tracks=11364,primary_batches=180,exact_replay_batches=180,
        actual_stages=len(stages),physical_states_per_phase=1090944,coordinate_evaluations_per_phase=72002304,
        observed_scientific_counters=observed,verified_preceding_live_watchdogs=len(watchdogs),
        maximum_sampled_rss_mib=max(w['sampled_peak_rss_mib'] for w in watchdogs),
        complete_coverage=True,complete_scientific_replay=True,independent_full_field_traces=48,
        angular_identity=read(OUT/'angular_identity.json'),
        independent_maxima={key:max(r['independent_maxima'][key] for r in results) for key in results[0]['independent_maxima']},
        independent_full_field_relative=max(t['independent_full_field_error'] for r in results for t in r['independent_traces']),
        maximum_white_physical_defect=max(o['geometric_white']['physical'] for g in white['groups'] for o in g['orders']),
        maximum_white_closure=max(o['geometric_white']['closure'] for g in white['groups'] for o in g['orders']),
        stored_normalizer_comparison_is_separate=True,
        full_current_discrete_fixed_source_qualified=True,full_current_geometric_white_qualified=True,
        AAA_accuracy_qualified=False,scattering_fission_iteration_qualified=False,
        local_inverse_propagation_qualified=False,ABA_admitted=False)
    write_new(OUT/'result.json',result)
    with (OUT/'REPORT.txt').open('x') as handle:
        handle.write('AAA 当前数据全轨迹有限高度响应（2026-10-05）\n\n')
        handle.write('当前三个预选能群、全部 11,364 条原始轨迹，20 cm 高度/4 层；180 主批及180独立字节重放批。\n')
        handle.write('全部源/面坐标、原始物理账目、完整覆盖、48 项独立整字段参考和几何白返回通过原门槛。\n')
        handle.write(f"独立整字段最大误差 {result['independent_full_field_relative']:.3e}；白返回物理平衡最大缺陷 {result['maximum_white_physical_defect']:.3e}。\n")
        handle.write('\n仅资格所声明三群 H20/Nz4 的完整离散固定源及几何白返回。\n')
        handle.write('尚未资格局部轴向传播闭合、370 群/150 cm 散射裂变耦合或 AAA 完整物理精度；ABA 未准入。\n')
    print('AXMAT-CURRENT-FULL-FAMILY-VERIFIED')


def run(expected):
    declaration=read(require_file(OUT/'declaration.json',expected));verify(declaration['files']);verify_pilot()
    plan=read(OUT/'plan.json');resource=DiskResources(ART,declaration['resource_roots'],declaration['min_free_bytes'],declaration['artifact_budget_bytes'])
    write_new(OUT/'run_claim.json',dict(declaration_sha256=expected,started_unix=time.time(),started_monotonic=time.monotonic()))
    runner=OwnRSSSerialExecutor(OUT,declaration['total_wall_seconds'],'AAA',resource);started=time.monotonic()
    result=dict(classification='FAILED_CURRENT_FULL_FAMILY_NO_RETRY',error=None)
    probe=plan['preflight_batch_ids'][0]
    def batch(case,phase):
        runner.execute(OUT/'runs',f'{phase}_{case}',[sys.executable,str(WORKER),str(OUT),case,phase],600)
        check_receipt(case,phase)
    try:
        runner.execute(OUT/'preflight','analytic_white',[sys.executable,str(ANALYTIC),str(OUT)],600)
        for phase in ['primary','replay']:batch(probe,phase)
        runner.execute(OUT,'admission',[sys.executable,str(Path(__file__).resolve()),'admit'],600,'AXMAT-CURRENT-FULL-FAMILY-ADMITTED')
        for phase in ['primary','replay']:
            for case in plan['batches']:
                if case['id']!=probe:batch(case['id'],phase)
        for p in range(4):
            runner.execute(OUT/'runs',f'audit_p{p}',[sys.executable,str(AUDITOR),str(OUT),f'p{p}_{FAMILY}'],600)
        runner.execute(OUT/'runs','white',[sys.executable,str(ACTION),str(OUT),FAMILY],600)
        # The verifier's own RUNNING stage is added to the final 368-stage receipt after completion.
        runner.execute(OUT,'verification',[sys.executable,str(Path(__file__).resolve()),'finalize'],600,'AXMAT-CURRENT-FULL-FAMILY-VERIFIED')
        completed=read(OUT/'AAA/stages.json')['stages']
        if len(completed)!=368 or any(s['status']!='PASS' for s in completed):
            raise ValueError('complete parent-observed stage receipt required')
        last_watch=read(OUT/'verification.watchdog.json')
        if last_watch['returncode']!=0 or last_watch['limit_failure'] is not None or last_watch['sampled_peak_rss_mib']>=512:
            raise ValueError('final actual own-child resource receipt required')
        result.update(classification='COMPLETE_BOUNDED_CURRENT_FULL_FIXED_SOURCE_WHITE_ONLY',ABA_admitted=False)
    except BaseException as error:
        result['error']=repr(error);raise
    finally:
        verify(declaration['files']);verify_pilot()
        result.update(elapsed_seconds=time.monotonic()-started,resources=resource.check())
        write_new(OUT/'driver_result.json',result)
    write_new(OUT/'seal.json',dict(schema='AXMAT_CURRENT_FULL_FIXED_SOURCE_WHITE_SEAL_V1',
        files={str(p.relative_to(OUT)):digest(p) for p in OUT.rglob('*') if p.is_file()}))
    print(json.dumps(dict(classification=read(OUT/'result.json')['classification'],elapsed_seconds=result['elapsed_seconds'])))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['prepare','run','admit','finalize'])
    parser.add_argument('--sha256');a=parser.parse_args()
    dict(prepare=prepare,run=lambda:run(a.sha256),admit=admit,finalize=finalize)[a.action]()
