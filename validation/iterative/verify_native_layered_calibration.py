"""Final artifact, replay, isolation and full-matrix cost verification."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import shutil
import time
import numpy as np
from calibrate_native_oblique_streaming import read,save


def digest(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main(root,project):
    tick=time.perf_counter();plan=json.loads((root/'calibration_plan.json').read_text());d=read(root/'inputs/inventory.npz')
    allrows=[];audits=[];resources=[];states=coordinates=0;ranked_states=0;costrows=[]
    for case in plan['cases']:
        name=case['id'];nz=case['nz']
        for phase in ['primary','replay']:
            for mode in ['ranked','batch']:
                summary=json.loads((root/phase/mode/name/'result.json').read_text());rows=summary['rows']
                tracks=case['ranked_tracks'] if mode=='ranked' else list(range(case['batch_first'],case['batch_stop']))
                expected={(t,g,o,s,q) for t in tracks for g in [51,61,98] for o in [1,-1] for s in [-1,1] for q in [8,16,32]}
                actual={(r['track'],r['group'],r['orientation'],r['sign'],r['order']) for r in rows}
                assert actual==expected and len(rows)==len(expected) and summary['raw_checks_passed']
                assert all(r['passed'] for r in rows)
                if mode=='ranked':assert summary['independent_accuracy_passed']
                if phase=='primary':
                    allrows.extend(rows);states+=len(rows);coordinates+=len(rows)*(14*nz+10)
                    if mode=='ranked':ranked_states+=len(rows)//3
                usage=json.loads((root/'runs'/f'{phase}_{mode}_{name}_resources.json').read_text());resources.append(usage)
                assert usage['elapsed_seconds']<600 and usage['peak_rss_mib']<512
                if phase=='primary' and mode=='batch':
                    q32=[t for t in usage['timing'] if t['order']==32];measured_seconds=sum(t['seconds'] for t in q32)
                    measured_updates=sum(t['updates'] for t in q32)
                    cnt=read(root/f'inputs/counts_{name}.npz')['counts']
                    full_updates=int(cnt[:,:,1,:,2].sum())*2*3*(14*nz+10)
                    costrows.append(dict(case=name,largest_batch_q32_seconds=measured_seconds,
                        largest_batch_q32_updates=measured_updates,full_q32_updates=full_updates,
                        kernel_work_scaled_seconds=measured_seconds*full_updates/measured_updates,
                        conservative_all_orders_elapsed_scaled_seconds=usage['elapsed_seconds']*full_updates/measured_updates))
        audit=json.loads((root/'verification'/name/'result.json').read_text());audits.append(audit)
        assert audit['all_checks_passed'] and audit['lossless_storage_roundtrips']==audit['transport_states']==(len(case['ranked_tracks'])+64)*36
        assert audit['adaptive_report']['estimated_normalized_error']<2e-13 and audit['adaptive_agreement']<2e-13
    assert len(plan['cases'])==24 and states==57888 and ranked_states==864
    assert sum(a['transport_states'] for a in audits)==states
    scientific=sorted(p.relative_to(root/'primary') for p in (root/'primary').rglob('*') if p.is_file())
    assert scientific==sorted(p.relative_to(root/'replay') for p in (root/'replay').rglob('*') if p.is_file())
    replay={}
    for name in scientific:
        first=digest(root/'primary'/name);second=digest(root/'replay'/name);assert first==second,name
        replay[str(name)]=first
    save(root/'verification/replay.json',dict(files=replay,all_byte_identical=True))
    white=json.loads((root/'primary/white/result.json').read_text());assert white['all_checks_passed'] and len(white['rows'])==18
    for phase in ['primary','replay']:
        text=(root/'runs'/f'{phase}_tests.log').read_text();assert 'Ran 10 tests' in text and text.rstrip().endswith('OK')
    watchdogs=[]
    for filename in ['primary_jobs.json','replay_jobs.json','audit_jobs.json']:
        for job in json.loads((root/filename).read_text()):
            w=json.loads((root/'runs'/f'{job["name"]}_watchdog.json').read_text());watchdogs.append(w)
            assert w['returncode']==0 and w['limit_failure'] is None and w['sampled_peak_rss_mib']<512 and w['elapsed_seconds']<600
    for phase in ['development_tests','development_tests2']:
        assert json.loads((root/'runs'/f'{phase}_watchdog.json').read_text())['returncode']==1
    failure=json.loads((root/'calibration_attempt1/primary/ranked/p3_h1_n4/result.json').read_text())
    assert not failure['independent_accuracy_passed'] and failure['raw_checks_passed']
    failure2=json.loads((root/'calibration_attempt2/primary/ranked/p3_h1_n4/result.json').read_text())
    assert not failure2['independent_accuracy_passed'] and failure2['raw_checks_passed']
    assert max(r['independent_response_relative'] for r in failure2['rows'] if r['order']==32)>5e-12
    assert (root/'runs/vendor_rebuild_tests.log').read_text().rstrip().endswith('OK')
    identities={}
    for name,base in [('protected_inputs_before.json',project),('frozen_inputs.json',root),('audit_inputs.json',root),('verification_inputs.json',root)]:
        files=json.loads((root/name).read_text())
        for filename,sha in files.items():assert digest(base/filename)==sha,(name,filename)
        identities[name]=len(files)
    prior=json.loads((root/'prior_artifacts.json').read_text());entries=0
    for name,sha in prior.items():
        folder=project/'validation/artifacts'/name;assert digest(folder/'result.sha256')==sha
        for line in (folder/'result.sha256').read_text().splitlines():
            h,path=line.split('  ',1);assert digest(folder/path)==h,(name,path);entries+=1
    # A full run is not launched by this estimate. Store exact original-track
    # structural cardinalities and a conservative uncompressed format budget.
    nr=d['nseg']-2;unique=np.array([len(set(d['nom'][i,1:n+1])) for i,n in enumerate(nr)])
    dense=compact=records=fullcoordinates=0
    for nz in [1,2,4]:
        k=14*nz+10;nout=14*nz+16;cols=unique*(nz+1)+nz+2;rows=cols-2
        factor=2*4*3*4 # heights, polars, groups, independent sign/orientation
        dense+=int(len(nr)*(nout*k+27*k+6)*8)*factor
        # Planned flat ragged arrays per <=64-record batch: all geometry,
        # coordinate indices, inactive witness, ids/shapes/offsets; an extra
        # 64 KiB header allowance per uncompressed archive. This bound does
        # not depend on compression ratio or dropping physical coordinates.
        compact+=int(((rows*cols+27*cols+27+6+rows+cols+12)*8).sum())*factor
        compact+=((len(nr)+63)//64)*65536*factor
        records+=len(nr)*factor;fullcoordinates+=len(nr)*factor*k
    budget=dict(scope='One full-native GL32 physical open-boundary pass, all 11364 records, 3 groups, 4 polars, independent axial and planar signs, H1/20 and Nz1/2/4',
        track_group_states=records,coordinate_evaluations_with_controls=fullcoordinates,
        piece_column_updates=sum(c['full_q32_updates'] for c in costrows),
        dense_primary_array_bytes=dense,lossless_primary_uncompressed_bound_bytes=compact,
        lossless_primary_plus_replay_and_reserve_bytes=2*compact+1024**3,
        free_bytes_at_verification=shutil.disk_usage(root).free,
        measured_kernel_work_scaled_seconds=sum(c['kernel_work_scaled_seconds'] for c in costrows),
        conservative_all_orders_elapsed_scaled_seconds=sum(c['conservative_all_orders_elapsed_scaled_seconds'] for c in costrows),cases=costrows,
        estimate_limits='Measured largest 64-track batches; full run cost and compressed output are estimates. The complete prior matched-inflow regression, reconstruction/white operators, independent audits and final verification require their own counted execution plan and additional budget.',
        full_execution_admitted=False,next_step='Freeze the complete native physical-source schedule and regression/white audit budget using the calibrated lossless schema, then qualify the open operator before native white closure.')
    assert budget['piece_column_updates']==plan['full_order32_piece_column_updates']
    save(root/'verification/full_execution_preflight.json',budget)
    maximum={}
    for key in ['primitive_relative','cell_relative','global_relative','geometry_relative','represented_width_relative','source_assembly_relative','constant_relative','shared_face_absolute','vacuum_axial_incoming_absolute']:
        maximum[key]=max(r[key] for r in allrows)
    byorder={str(q):max(r['independent_response_relative'] for r in allrows if r['order']==q and 'independent_response_relative' in r) for q in [8,16,32]}
    result=dict(implementation_calibration_passed=True,full_native_physical_operator_qualified=False,
        full_native_white_qualified=False,full_previous_zero_gradient_regression_completed=False,
        production_changed=False,coupled_eigenproblem_qualified=False,
        tests_per_pass=10,calibration_families=24,ranked_independent_states=ranked_states,
        primary_transport_states=states,primary_coordinate_evaluations_with_controls=coordinates,
        scientific_replay_files=len(replay),independent_audits=len(audits),manufactured_white_cases=18,
        maxima=maximum,independent_response_relative_by_order=byorder,
        independent_reference_convergence=max(r['reference_accuracy'] for r in allrows if 'reference_accuracy' in r),
        adaptive_reference_agreement=max(a['adaptive_agreement'] for a in audits),
        adaptive_reference_error_estimate=max(a['adaptive_report']['estimated_normalized_error'] for a in audits),
        independent_audit_maxima={k:max(a['maxima'][k] for a in audits) for k in audits[0]['maxima']},
        lossless_roundtrips=sum(a['lossless_storage_roundtrips'] for a in audits),
        white_maximum_independent_error=max(max(r['independent_errors'].values()) for r in white['rows']),
        white_maximum_balance=max(r['checks']['source_collision_escape'] for r in white['rows']),
        watchdog_processes=len(watchdogs),maximum_watchdog_rss_mib=max(w['sampled_peak_rss_mib'] for w in watchdogs),
        maximum_watchdog_seconds=max(w['elapsed_seconds'] for w in watchdogs),
        maximum_worker_rss_mib=max(u['peak_rss_mib'] for u in resources),
        identities=identities,prior_artifacts=len(prior),prior_manifest_entries=entries,
        elapsed_seconds=time.perf_counter()-tick,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    save(root/'verification/result.json',result)
    assert result['elapsed_seconds']<600 and result['peak_rss_mib']<512
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('project',type=Path)
    a=p.parse_args();main(a.root.resolve(),a.project.resolve())
