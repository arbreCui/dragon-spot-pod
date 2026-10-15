"""Seal checks for the full geometry preflight, preserving failed audit evidence."""
import argparse
import json
import resource
import time
from pathlib import Path
import numpy as np
from native_oblique_full_preflight import digest,read,save


def main(root,project):
    tick=time.perf_counter();result={}
    for name,base in [('protected_inputs_before.json',project),('source_inputs.json',project),
        ('initial_inputs.json',root),('copied_inputs.json',root),('audit_inputs.json',root),('bounded_audit_inputs.json',root),
        ('bounded_audit_v3_inputs.json',root),('verification_inputs.json',root),('verification_v3_inputs.json',root)]:
        mapping=json.loads((root/name).read_text())
        for key,value in mapping.items():assert digest(base/key)==value,(name,key)
        result[name]=len(mapping)
    prior=json.loads((root/'prior_artifacts.json').read_text());entries=0
    for name,value in prior.items():
        folder=project/'validation/artifacts'/name;manifest=folder/'result.sha256';assert digest(manifest)==value,name
        for line in manifest.read_text().splitlines():
            h,path=line.split('  ',1);assert digest(folder/path)==h,(name,path);entries+=1
    result.update(prior_artifacts=len(prior),prior_manifest_entries=entries)
    from qualify_native_directional import load_native
    native=load_native(root/'inputs/track_data.bin');inventory=read(root/'inputs/inventory.npz')
    for key in ['nseg','angle','nom','h2','wei','zmu','wzmu','weights','harm','groups']:
        np.testing.assert_array_equal(inventory[key],native[key])
    np.testing.assert_array_equal(inventory['group_totals'],np.stack([a['total'] for a in native['group_data']]))
    np.testing.assert_array_equal(inventory['original_track'],np.arange(11364))
    np.testing.assert_array_equal(inventory['original_record_multiplicity'],1)
    for track,nr in enumerate(native['nseg']-2):
        np.testing.assert_array_equal(inventory['planar_widths'][track,:nr],native['h2'][track,1:nr+1])
        np.testing.assert_array_equal(inventory['planar_widths'][track,nr:],0)
        assert inventory['entry_surface'][track]==-native['nom'][track,0]-1
        assert inventory['exit_surface'][track]==-native['nom'][track,nr+1]-1
    del native,inventory
    exact=project/'validation/artifacts/exact-native-flight-20260929'
    reference_copies=0
    for group in [51,61,98]:
        for key in ['green','fixed','white']:
            assert digest(root/f'inputs/{key}_{group}.npz')==digest(exact/f'analysis/{group}_whole/{key}.npz');reference_copies+=1
        for name in [f'prepared_{group}.npz',f'cases_{group}.json']:
            assert digest(root/'inputs'/name)==digest(exact/'inputs'/name);reference_copies+=1
    result.update(inventory_original_records_verified=11364,exact_reference_copies_verified=reference_copies)
    plan=json.loads((root/'plan.json').read_text());n=0
    for case in plan['preflight_processes']:
        pid=case['id'];receipt=json.loads((root/'replay/receipts'/(pid+'.json')).read_text());assert receipt['all_byte_identical']
        names=sorted(p.name for p in (root/'analysis'/pid).iterdir())
        assert names==sorted(receipt['files'])==sorted(p.name for p in (root/'replay/analysis'/pid).iterdir())
        for name,info in receipt['files'].items():
            p=root/'analysis'/pid/name;q=root/'replay/analysis'/pid/name
            assert digest(p)==info['sha256']==digest(q);assert p.stat().st_size==info['bytes']==q.stat().st_size;n+=1
    primary=json.loads((root/'preflight/result.json').read_text());replay=json.loads((root/'replay/preflight/result.json').read_text())
    for key in primary:
        if key not in ['elapsed_seconds','peak_rss_mib']:assert primary[key]==replay[key],key
    for name in ['geometric_ledgers.npz','normalizer_ledgers.json','worst_geometry.json','worst_literal_geometry.npz']:
        assert digest(root/'preflight'/name)==digest(root/'replay/preflight'/name),name
    costs=json.loads((root/'preflight/response_costs_and_batches.json').read_text())
    other=json.loads((root/'replay/preflight/response_costs_and_batches.json').read_text())
    for key in costs:
        if key!='free_bytes_at_summary':assert costs[key]==other[key],key
    assert not costs['response_execution_admitted'] and costs['process_estimates_within_caps'] and costs['storage_estimate_admitted']
    # Every frozen scheduling batch covers a contiguous original-index slice.
    for case in plan['preflight_processes']:
        batches=[b for b in costs['processes'] if b['case']==case['id']];start=0
        for b in batches:assert b['first']==start and start<b['stop']<=11364;start=b['stop']
        assert start==11364
    failed=root/'preflight/resource_limited_audit';old=json.loads((failed/'result.json').read_text())
    assert old['peak_rss_mib']>512 and json.loads((failed/'status.json').read_text())['status']=='resource_cap_failed'
    for key in old:
        if key not in ['elapsed_seconds','peak_rss_mib']:assert old[key]==primary[key]
    for name in ['geometric_ledgers.npz','normalizer_ledgers.json','worst_geometry.json','worst_literal_geometry.npz']:
        assert digest(failed/name)==digest(root/'preflight'/name),name
    released=root/'preflight/resource_limited_view_release_audit'
    assert json.loads((released/'status.json').read_text())['status']=='resource_cap_failed_on_replay'
    for label in ['primary','replay']:
        prior_result=json.loads((released/label/'result.json').read_text())
        for key in primary:
            if key not in ['elapsed_seconds','peak_rss_mib']:assert prior_result[key]==primary[key]
        for name in ['geometric_ledgers.npz','normalizer_ledgers.json','worst_geometry.json','worst_literal_geometry.npz']:
            assert digest(released/label/name)==digest(root/'preflight'/name)
    usage=[]
    for base in [root,root/'replay']:
        for case in plan['preflight_processes']:
            row=json.loads((base/'runs'/(case['id']+'_resources.json')).read_text());usage.append(row)
            wd=json.loads((base/'runs'/(case['id']+'_watchdog.json')).read_text())
            assert wd['returncode']==0 and wd['limit_failure'] is None and wd['sampled_peak_rss_mib']<512 and wd['elapsed_seconds']<600
        assert 'Ran 7 tests' in (base/'runs/tests.log').read_text() and (base/'runs/tests.log').read_text().rstrip().endswith('OK')
    for row in usage+[primary,replay]:assert row['peak_rss_mib']<512 and row['elapsed_seconds']<600
    for name in ['native_oblique_full_geometry_count.cpp','native_oblique_full_preflight.py','test_native_oblique_full_preflight.py','run_native_oblique_full_preflight.py']:
        assert digest(project/'validation/iterative'/name)==digest(root/'build'/name)
    assert digest(project/'validation/iterative/summarize_native_oblique_full_preflight.py')==digest(root/'audit_v3_build/summarize_native_oblique_full_preflight.py')
    assert digest(project/'validation/iterative/verify_native_oblique_full_preflight.py')==digest(root/'build/verify_native_oblique_full_preflight_v3.py')
    assert primary['geometry_measure_audit_passed'] and primary['source_responses_computed']==0
    result.update(byte_identical_replay_analysis_files=n,byte_identical_replay_audit_files=4,
        geometry_configurations=primary['geometry_configurations'],geometry_files_audited=primary['geometry_files_audited'],
        primitive_pieces_counted=primary['pieces'],geometry_relative=primary['maximum_geometry_relative'],tests_per_pass=7,
        preserved_resource_failures=2,preserved_resource_failure_peak_rss_mib=old['peak_rss_mib'],
        preserved_view_release_replay_peak_rss_mib=578.734375,bounded_audit_peak_rss_mib=max(primary['peak_rss_mib'],replay['peak_rss_mib']),
        peak_geometry_worker_rss_mib=max(u['peak_rss_mib'] for u in usage),maximum_geometry_worker_seconds=max(u['elapsed_seconds'] for u in usage),
        geometry_measure_audit_qualified=True,zero_gradient_operator_qualified=False,common_white_qualified=False,
        physical_axial_escape_qualified=False,all_verification_checks_passed=True,
        elapsed_seconds=time.perf_counter()-tick,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    assert result['peak_rss_mib']<512 and result['elapsed_seconds']<600
    save(root/'verification/result.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);p.add_argument('project',type=Path)
    a=p.parse_args();main(a.artifact.resolve(),a.project.resolve())
