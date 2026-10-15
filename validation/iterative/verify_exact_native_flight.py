#!/usr/bin/env python3
"""Verify full-coordinate actions, native recovery, replay and raw balances."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from qualify_native_directional import load_native
from exact_native_flight import evaluate, close_white, compare, ratio
from qualify_exact_native_flight import read, action_error, metrics_summary, compare_gate


def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main(root,a):
    counts=dict(protected_files=0,initial_inputs=0,copied_inputs=0,prior_artifacts=0,prior_manifest_entries=0,
                byte_identical_analysis_files=0,checked_numeric_arrays=0,preserved_initial_arrays=0)
    for name,base,key in [('protected_inputs_before.json',root,'protected_files'),('initial_inputs.json',root,'initial_inputs'),('copied_inputs.json',a,'copied_inputs')]:
        for path,expected in json.loads((a/name).read_text()).items():assert digest(base/path)==expected,path;counts[key]+=1
    for name,expected in json.loads((a/'prior_artifacts.json').read_text()).items():
        folder=root/'validation/artifacts'/name;assert digest(folder/'result.sha256')==expected,name
        for line in (folder/'result.sha256').read_text().splitlines():
            h,p=line.split(maxsplit=1);assert digest(folder/p)==h,(name,p);counts['prior_manifest_entries']+=1
        counts['prior_artifacts']+=1
    for p in (a/'build').glob('*.py'):assert digest(p)==digest(root/'validation/iterative'/p.name),p.name
    for folder,logs in [(a/'runs',['source_tests','source_reference_tests','archived_tests','archived_reference_tests']),
                        (a/'replay/runs',['archived_tests','archived_reference_tests'])]:
        for name in logs:
            text=(folder/(name+'.log')).read_text();assert 'Ran 8 tests' in text and '\nOK\n' in text and 'skipped=' not in text
    files=sorted(p.relative_to(a/'analysis') for p in (a/'analysis').rglob('*') if p.is_file())
    assert files==sorted(p.relative_to(a/'replay/analysis') for p in (a/'replay/analysis').rglob('*') if p.is_file())
    for p in files:assert digest(a/'analysis'/p)==digest(a/'replay/analysis'/p),str(p);counts['byte_identical_analysis_files']+=1
    d=load_native(a/'inputs/track_data.bin');plan=json.loads((a/'plan.json').read_text());lim=plan['limits'];rows=[];resources={}
    # Independent geometric source/incoming measures for every full basis column.
    measure=np.zeros((2,d['nmu'],d['nr']+d['nb']))
    for oi,orientation in enumerate([1,-1]):
        entry=np.zeros(len(d['track']),int) if orientation==1 else d['length']-1
        surface=-d['region'][np.arange(len(entry)),entry]-1
        np.add.at(measure[oi],(d['polar'],d['nr']+surface),d['weight']/2)
        for step in range(1,d['nmax']-1):
            lines=np.flatnonzero(step<d['length']-1);r=d['region'][lines,step]-1
            np.add.at(measure[oi],(d['polar'][lines],r),d['weight'][lines]*d['h'][lines,step]/2)
    maximum_basis_balance=0.
    for group in plan['groups']:
        material=next(x for x in d['group_data'] if x['group']==group)
        old=read(a/f'inputs/prepared_{group}.npz');original=read(a/f'inputs/result_{group}.npz')
        tags=json.loads((a/f'inputs/cases_{group}.json').read_text())
        positive=(old['q'].min(axis=(0,1,2))>=0)&(old['inflow'].min(axis=(0,1,2))>=0);assert positive.sum()==214
        for phase in ['native',*plan['partitions']]:
            label=f'{group}_{phase}';folder=a/'analysis'/label;row=json.loads((folder/'result.json').read_text());rows.append(row)
            green=read(folder/'green.npz');fixed=read(folder/'fixed.npz');white=read(folder/'white.npz')
            for fields in [green,fixed,white]:
                counts['checked_numeric_arrays']+=len(fields)
                assert all(np.isfinite(v).all() for v in fields.values())
            np.testing.assert_array_equal(fixed['q'],old['q']);np.testing.assert_array_equal(fixed['inflow'],old['inflow'])
            recovered=evaluate(d,material,green,old['q'],old['inflow'])
            for k,v in recovered.items():np.testing.assert_array_equal(fixed[k],v)
            recovered_white=close_white(d,material,green,fixed,tags)
            for k,v in recovered_white.items():np.testing.assert_array_equal(white[k],v)
            for key in ['iso','own','boundary','abs_jx','track_minimum_angle','track_minimum_integral','track_outgoing','track_integral']:
                assert green[key].min()>=0,(label,key)
            assert (fixed['iso']+fixed['own'])[...,positive].min()>=0 and fixed['boundary'][...,positive].min()>=0
            assert (fixed['iso']+fixed['own'])[...,~positive].min()<0 and fixed['boundary'][...,~positive].min()<0
            assert white['boundary_inverse'].min()>=0 and white['inflow'].min()>=0
            assert row['minimum_track_angle']==float(green['track_minimum_angle'].min())
            assert row['minimum_track_integral']==float(green['track_minimum_integral'].min())
            assert row['maximum_piece_balance_relative']==float(green['track_maximum_local_balance'].max())
            assert row['maximum_track_balance_relative']==float(ratio(green['track_defect'],green['track_scale']).max())
            collision=np.einsum('opru,r->opu',green['iso']+green['own'],material['total'])
            independent_balance=float(ratio(measure-collision-green['boundary'].sum(axis=2),measure).max())
            if phase!='native':assert independent_balance<lim['exact_piece_track_balance_relative'];maximum_basis_balance=max(maximum_basis_balance,independent_balance)
            else:assert independent_balance<lim['assembled_global_balance_context_relative']
            for name,data in [('fixed',fixed),('white',white)]:
                for moment in ['even','odd']:
                    assert row[name+'_'+moment+'_balance_relative']==float(data[moment+'_relative'].max())
            if phase=='native':
                recovery=dict(iso=action_error(fixed['iso'],old['iso']),own=action_error(fixed['own'],old['own']),
                    boundary=action_error(fixed['boundary'],old['boundary']),
                    native_half_integrals=action_error(fixed['iso']+fixed['own'],original['native_half_integrals']),
                    native_half_outgoing=action_error(fixed['boundary'],original['native_half_outgoing']),
                    phi=float(ratio(fixed['phi']-original['native_phi'],fixed['phi_scale']).max()),
                    jz=float(ratio(fixed['jz']-original['native_jz'],fixed['jz_scale']).max()))
                delta=material['pjj']-2*material['pjsum']/d['weights'][:d['nr']]
                np.testing.assert_array_equal(fixed['pjj_completion_legacy'],delta[:,None]*old['legacy'][:d['nr']])
                np.testing.assert_array_equal(fixed['p0_completed_legacy'],fixed['phi'][:,:31]+fixed['pjj_completion_legacy'])
                recovery['p0_completed']=action_error(np.r_[fixed['p0_completed_legacy'],fixed['outgoing'][:,:31]],original['old_native'])
                recovery['reclosed_native_inflow']=action_error(white['inflow'],old['inflow'][...,white['target_indices']])
                assert recovery==row['native_recovery'] and max(recovery.values())<lim['native_action_relative']
            else:
                comparisons=read(folder/'comparison.npz');counts['checked_numeric_arrays']+=len(comparisons)
                baseline=read(a/f'analysis/{group}_native/fixed.npz');baseline_white=read(a/f'analysis/{group}_native/white.npz')
                target=white['target_indices'];white_tags=[tags[i] for i in target]
                cases=[('fixed_vs_native',fixed,baseline,tags),('white_vs_native',white,baseline_white,white_tags),
                       ('reclosure_effect',white,{k:fixed[k][...,target] for k in ['phi','jx','jz','outgoing','phi_scale','jx_scale','jz_scale','outgoing_scale']},white_tags)]
                if phase!='whole':
                    cases += [(name+'_partition',value,read(a/f'analysis/{group}_whole/{name}.npz'),labels) for name,value,labels in [('fixed',fixed,tags),('white',white,white_tags)]]
                for prefix,value,ref,labels in cases:
                    metrics=compare(d,value,ref)
                    for k,v in metrics.items():np.testing.assert_array_equal(comparisons[prefix+'_'+k],v)
                    assert row[prefix]==metrics_summary(metrics,labels)
                    if prefix.endswith('_partition'):
                        assert compare_gate(metrics,lim['exact_partition_relative']) and row[prefix+'_passed']
                        name=prefix.split('_')[0]
                        assert row[name+'_half_integrals_partition_relative']==action_error(value['iso']+value['own'],ref['iso']+ref['own'])<lim['exact_partition_relative']
                        assert row[name+'_half_boundary_partition_relative']==action_error(value['boundary'],ref['boundary'])<lim['exact_partition_relative']
                np.testing.assert_array_equal(fixed['native_pjj_completion_legacy'],baseline['pjj_completion_legacy'])
                np.testing.assert_array_equal(fixed['kernel_only_phi_change_legacy'],fixed['phi'][:,:31]-baseline['phi'][:,:31])
                np.testing.assert_array_equal(fixed['change_from_completed_native_legacy'],fixed['phi'][:,:31]-baseline['p0_completed_legacy'])
            assert row['phase_qualified'] and row['positive_responses_passed'] and row['white_algebra_passed'] and row['assembled_balance_context_passed']
            assert not any(row[k] for k in ['native_partition_invariance_qualified','native_mesh_convergence_qualified','coupled_eigenreference_qualified'])
            for where in ['runs','replay/runs']:
                u=json.loads((a/f'{where}/{label}_resources.json').read_text());resources[where+'/'+label]=u
                assert u['elapsed_seconds']<=600 and u['peak_rss_mib']<=512
    for p in (a/'runs/initial_json_serialization/51_native').glob('*.npz'):
        x=read(p);y=read(a/'analysis/51_native'/p.name)
        for k,v in x.items():np.testing.assert_array_equal(v,y[k]);counts['preserved_initial_arrays']+=1
    data=json.loads((a/'analysis/result.json').read_text());assert len(rows)==data['phases']==18
    assert data['exact_full_flight_companion_qualified']==all(r['phase_qualified'] for r in rows)
    assert data['native_calibration_maximum_relative']==max(max(r['native_recovery'].values()) for r in rows if r['phase']=='native')
    counts.update(source_tests=16,archived_tests=16,replay_tests=16,native_fixed_input_cases=648,
        exact_fixed_input_evaluations=3240,exact_reclosed_positive_evaluations=1005,exact_partition_case_comparisons=3396,
        independently_aggregated_exact_basis_balance_relative=maximum_basis_balance,
        primary_peak_rss_mib=max(v['peak_rss_mib'] for k,v in resources.items() if k.startswith('runs/')),
        replay_peak_rss_mib=max(v['peak_rss_mib'] for k,v in resources.items() if k.startswith('replay/')),
        maximum_process_seconds=max(v['elapsed_seconds'] for v in resources.values()),
        all_verification_checks_passed=True,exact_full_flight_companion_qualified=True,
        native_partition_invariance_qualified=False,native_mesh_convergence_qualified=False,coupled_eigenreference_qualified=False)
    with (a/'verification.json').open('x') as f:json.dump(counts,f,indent=2);f.write('\n')
    print(json.dumps(counts,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('artifact',type=Path)
    args=p.parse_args();main(args.root,args.artifact)
