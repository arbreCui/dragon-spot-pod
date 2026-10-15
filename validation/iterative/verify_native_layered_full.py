"""Verify full inventory, exact replay, independent audits and immutable inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
from calibrate_native_oblique_streaming import save


def digest(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main(root):
    tick=time.perf_counter();plan=json.loads((root/'plan.json').read_text());admit=json.loads((root/'admission.json').read_text())
    assert admit['full_execution_admitted'] and admit['plan_sha256']==digest(root/'plan.json')
    cases=[c for c in plan['batches'] if not c['preflight']];assert len(cases)==1080
    rows=[];replay={};usage=[];count_keys=['physical_states','physical_coordinate_evaluations','physical_piece_column_updates','matched_regression_states','matched_regression_input_evaluations'];counts={k:0 for k in count_keys}
    for c in cases:
        name=c['id'];folder=root/'primary'/name;r=json.loads((folder/'result.json').read_text());assert r['case']==c
        assert r['all_checks_passed'] and r['full_cell_face_regression_byte_exact'];rows.append(r)
        nt=c['stop']-c['first'];assert r['original_records']==nt
        assert r['physical_states']==nt*24 and r['physical_coordinate_evaluations']==nt*24*(14*c['nz']+10)
        assert r['matched_regression_states']==nt*24 and r['matched_regression_input_evaluations']==nt*24*14
        for key in counts:counts[key]+=r[key]
        first=json.loads((root/'receipts/primary'/f'{name}.json').read_text());second=json.loads((root/'receipts/replay'/f'{name}.json').read_text())
        assert second['all_scientific_bytes_identical'] and first['files']==second['files'] and len(first['files'])==15
        assert set(first['files'])=={f.name for f in folder.iterdir() if f.is_file()}
        for filename,identity in first['files'].items():
            path=folder/filename;assert path.stat().st_size==identity['bytes'] and digest(path)==identity['sha256']
            replay[f'{name}/{filename}']=identity
        for phase in ['primary','replay']:
            u=json.loads((root/'runs'/f'{phase}_{name}_resources.json').read_text());usage.append(u)
            assert u['elapsed_seconds']<600 and u['peak_rss_mib']<512
    expected=dict(physical_states=6545664,physical_coordinate_evaluations=279281664,physical_piece_column_updates=2453859601920,
        matched_regression_states=6545664,matched_regression_input_evaluations=91639296)
    assert counts==expected,(counts,expected)
    families=sorted({c['id'].rsplit('_b',1)[0] for c in cases});audits=[]
    for family in families:
        a=json.loads((root/'verification'/family/'result.json').read_text());assert a['all_checks_passed'] and a['all_original_indices_once']
        assert a['original_tracks']==11364 and a['raw_files']==540 and a['physical_states']==11364*12 and len(a['independent_traces'])==12
        nz=next(c['nz'] for c in cases if c['id'].rsplit('_b',1)[0]==family)
        assert a['source_coordinates']==11364*12*(14*nz+10);audits.append(a)
    white=[]
    for family in sorted({f[3:] for f in families}):
        a=json.loads((root/'white'/family/'result.json').read_text());assert a['all_checks_passed'] and a['original_tracks']==11364
        assert a['physical_axial_incoming_zero'] and a['geometric_normalizer_used'] and len(a['groups'])==3;white.append(a)
    assert len(audits)==24 and len(white)==6
    cache=[]
    for family in families:
        a=json.loads((root/'preflight'/f'cache_{family}.json').read_text());assert a['all_fields_metrics_geometry_byte_exact'];cache.append(a)
    assert sum(a['states'] for a in cache)==57888
    assert json.loads((root/'preflight/action_test.json').read_text())['passed']
    assert json.loads((root/'preflight/preflight_max256_audit/result.json').read_text())['all_checks_passed']
    watchdogs=[]
    for jobfile in ['preflight_jobs.json','audit_preflight_jobs.json','action_preflight_jobs.json','full_jobs.json']:
        for job in json.loads((root/jobfile).read_text()):
            if job['script']=='verify_native_layered_full.py':continue
            w=json.loads((root/'runs'/f'{job["name"]}_watchdog.json').read_text());watchdogs.append(w)
            assert w['returncode']==0 and w['limit_failure'] is None and w['elapsed_seconds']<600 and w['sampled_peak_rss_mib']<512
    for a in audits+white:assert a['elapsed_seconds']<600 and a['peak_rss_mib']<512
    frozen=json.loads((root/'frozen_inputs.json').read_text())
    for path,sha in frozen.items():assert digest(root/path)==sha,path
    project=root.parents[2];protected=json.loads((root/'protected_inputs_before.json').read_text())
    for path,sha in protected.items():assert digest(project/path)==sha,path
    prior=json.loads((root/'prior_artifacts.json').read_text());entries=0
    for name,sha in prior.items():
        folder=project/'validation/artifacts'/name;assert digest(folder/'result.sha256')==sha
        for line in (folder/'result.sha256').read_text().splitlines():
            h,path=line.split('  ',1);assert digest(folder/path)==h,(name,path);entries+=1
    save(root/'verification/replay.json',dict(files=replay,all_scientific_bytes_identical=True,replay_storage='recomputed and serialized in memory, independently hashed against primary bytes'))
    result=dict(full_native_physical_operator_qualified=True,full_native_white_qualified=True,full_previous_zero_gradient_regression_completed=True,
        production_changed=False,coupled_eigenproblem_qualified=False,original_tracks=11364,counts=counts,full_batches=len(cases),
        scientific_replay_files=len(replay),independent_audits=len(audits),independent_full_traces=288,native_white_cases=18,
        physical_gate_maxima={key:max(r['physical_gate_maxima'][key] for r in rows) for key in rows[0]['physical_gate_maxima']},
        maximum_order_disagreement=max(r['full_coordinate_order16_order32_relative'] for r in rows),
        maximum_wholeflight_reference=max(r['independent_wholeflight_relative'] for r in rows),
        independent_response_error=max(t['independent_response_error'] for a in audits for t in a['independent_traces']),
        independent_full_field_error=max(t['independent_full_field_error'] for a in audits for t in a['independent_traces']),
        maximum_white_physical_defect=max(o['geometric_white']['physical'] for a in white for g in a['groups'] for o in g['orders']),
        maximum_white_closure=max(o['geometric_white']['closure'] for a in white for g in a['groups'] for o in g['orders']),
        stored_normalizer_comparison_maximum_physical_defect=max(o['stored_normalizer_comparison']['physical'] for a in white for g in a['groups'] for o in g['orders']),
        watchdog_processes=len(watchdogs),maximum_sampled_rss_mib=max(w['sampled_peak_rss_mib'] for w in watchdogs),
        maximum_worker_seconds=max(w['elapsed_seconds'] for w in watchdogs),frozen_files=len(frozen),protected_inputs=len(protected),
        prior_artifacts=len(prior),prior_manifest_entries=entries,elapsed_seconds=time.perf_counter()-tick,
        peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    assert result['elapsed_seconds']<600 and result['peak_rss_mib']<512
    save(root/'verification/result.json',result);print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);a=p.parse_args();main(a.root.resolve())
