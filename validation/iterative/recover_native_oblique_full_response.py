"""Complete-track assembly, frozen input recovery, then common-white reclosure."""
import argparse
import json
import resource
import time
from pathlib import Path
import numpy as np
from qualify_native_directional import load_native
from exact_native_flight import compare
from native_oblique_streaming import ratio
from native_oblique_full_action import evaluate,close_white
from calibrate_native_oblique_streaming import read,save


def action_error(value,reference,scale=None):
    value,reference=np.broadcast_arrays(value,reference)
    amplitude=abs(reference) if scale is None else np.broadcast_to(scale,value.shape)
    amplitude=amplitude.max(axis=tuple(range(value.ndim-1)),keepdims=True)
    return float(ratio(value-reference,amplitude).max())


def comparison_summary(d,value,reference):
    metrics=compare(d,value,reference)
    row={key:float(v.max()) for key,v in metrics.items() if 'induced_relative' in key}
    return metrics,row


def recover(root,H,nz):
    plan=json.loads((root/'plan.json').read_text());cases=[c for c in plan['processes'] if c['H']==H and c['nz']==nz]
    accum={k:np.zeros((2,2,2,4,3,8,nz,14)) for k in ['volume','jx','abs_jx']}
    accum['boundary']=np.zeros((2,2,2,4,3,6,14));coverage=np.zeros((2,2,2,4,11364),np.uint8)
    for case in cases:
        folder=root/'analysis'/case['id'];row=json.loads((folder/'result.json').read_text());assert row['all_gates_passed']
        tracks=np.arange(case['first'],case['stop']);p=case['polar']
        for oi,o in enumerate([1,-1]):
            for zi,sign in enumerate([1,-1]):
                for qi,q in enumerate([8,16]):
                    with np.load(folder/f'o{o}_m{sign}_q{q}.npz') as f:
                        np.testing.assert_array_equal(f['original_tracks'],tracks);np.testing.assert_array_equal(f['multiplicity'],1)
                        coverage[qi,zi,oi,p,tracks]+=1
                        for key in accum:accum[key][qi,zi,oi,p]+=f[key]
    np.testing.assert_array_equal(coverage,1)
    d=load_native(root/'inputs/track_data.bin');target=root/'recovery'/f'h{int(H)}_n{nz}';target.mkdir();rows=[]
    np.savez_compressed(target/'coverage.npz',multiplicity=coverage,original_tracks=np.arange(11364))
    for qi,q in enumerate([8,16]):
        for gi,group in enumerate([51,61,98]):
            folder=target/f'q{q}_g{group}';folder.mkdir();a=next(a for a in d['group_data'] if a['group']==group)
            green={key:accum[key][qi,:,:,:,gi].sum(axis=-2) for key in ['volume','jx','abs_jx']}
            green['cell_volume']=accum['volume'][qi,:,:,:,gi];green['boundary']=accum['boundary'][qi,:,:,:,gi]
            with np.load(root/f'inputs/green_{group}.npz') as f:
                exact={key:f[key] for key in ['iso','own','jx','abs_jx','boundary']}
            reference_volume=exact['iso']+exact['own']
            operator=dict(volume=action_error(green['volume'],reference_volume),
                cell_volume=action_error(green['cell_volume'],reference_volume[...,None,:]/nz),
                jx=action_error(green['jx'],exact['jx'],exact['abs_jx']),
                abs_jx=action_error(green['abs_jx'],exact['abs_jx']),boundary=action_error(green['boundary'],exact['boundary']))
            inp=read(root/f'inputs/prepared_{group}.npz');fields=evaluate(d,a,green,inp['q'],inp['inflow'])
            metrics,comparison=comparison_summary(d,fields,read(root/f'inputs/fixed_{group}.npz'))
            positive=(inp['q'].min(axis=(0,1,2))>=0)&(inp['inflow'].min(axis=(0,1,2))>=0);assert positive.sum()==214
            row=dict(group=group,order=q,height=H,axial_cells=nz,operator=operator,fixed_input_comparison=comparison,
                fixed_cases=216,nonnegative_cases=214,minimum_positive_integral=float(fields['integral'][...,positive].min()),
                minimum_positive_boundary=float(fields['boundary'][...,positive].min()),
                signed_control_minimum_integral=float(fields['integral'][...,~positive].min()),
                even_balance_relative=float(fields['even_relative'].max()),odd_balance_relative=float(fields['odd_relative'].max()),
                integrated_gate_applies=q==16)
            row['recovery_passed']=bool(max(operator.values())<5e-12 and max(comparison.values())<5e-12
                and min(row['minimum_positive_integral'],row['minimum_positive_boundary'])>=0
                and max(row['even_balance_relative'],row['odd_balance_relative'])<1e-10)
            for name,data in [('green',green),('fixed',fields),('comparison',metrics)]:np.savez_compressed(folder/(name+'.npz'),**data)
            save(folder/'result.json',row);rows.append(row)
    save(target/'result.json',dict(rows=rows,all_original_indices_once=True,
        order16_recovery_passed=all(r['recovery_passed'] for r in rows if r['order']==16),
        order8_recovery_passed=all(r['recovery_passed'] for r in rows if r['order']==8),white_not_yet_solved=True))
    assert all(r['recovery_passed'] for r in rows if r['order']==16)


def white(root,H,nz):
    # Full matrix recovery is a prerequisite, including every other height/grid.
    for h in [1.,20.]:
        for n in [1,2,4]:assert json.loads((root/f'recovery/h{int(h)}_n{n}/result.json').read_text())['order16_recovery_passed']
    d=load_native(root/'inputs/track_data.bin');target=root/'white'/f'h{int(H)}_n{nz}';target.mkdir();rows=[]
    for q in [8,16]:
        for group in [51,61,98]:
            source=root/f'recovery/h{int(H)}_n{nz}/q{q}_g{group}';recovery=json.loads((source/'result.json').read_text())
            # Preserve failed order-8 recovery without rebranding it as white
            # evidence; the order-16 admission is the contract's main gate.
            if not recovery['recovery_passed']:
                rows.append(dict(group=group,order=q,not_run='order-8 recovery failed',white_passed=False));continue
            folder=target/f'q{q}_g{group}';folder.mkdir();a=next(a for a in d['group_data'] if a['group']==group)
            green=read(source/'green.npz');fixed=read(source/'fixed.npz');tags=json.loads((root/f'inputs/cases_{group}.json').read_text())
            fields=close_white(d,a,green,fixed,tags);metrics,comparison=comparison_summary(d,fields,read(root/f'inputs/white_{group}.npz'))
            matrix=np.eye(6)-fields['tbb'];inverse_error=float(abs(matrix@fields['boundary_inverse']-np.eye(6)).max())
            solve=float(ratio(abs(fields['white_matrix_residual']).max(axis=0),abs(fields['white_rhs']).max(axis=0)).max())
            closure=float(ratio(abs(fields['white_closure_defect']).max(axis=0),abs(fields['white_amplitudes']).max(axis=0)).max())
            row=dict(group=group,order=q,height=H,axial_cells=nz,reclosed_cases=67,comparison=comparison,
                inverse_identity_relative=inverse_error,solve_relative=solve,closure_relative=closure,
                minimum_inverse=float(fields['boundary_inverse'].min()),minimum_integral=float(fields['integral'].min()),
                minimum_boundary=float(fields['boundary'].min()),minimum_inflow=float(fields['inflow'].min()),
                even_balance_relative=float(fields['even_relative'].max()),odd_balance_relative=float(fields['odd_relative'].max()),
                stored_net_current_absmax=float(abs(fields['stored_white_net_current']).max()),
                geometric_net_current_absmax=float(abs(fields['even_incoming']-fields['even_outgoing']).max()))
            row['white_passed']=bool(max(comparison.values())<5e-12 and max(inverse_error,solve,closure)<5e-12
                and min(row[k] for k in ['minimum_inverse','minimum_integral','minimum_boundary','minimum_inflow'])>=0
                and max(row['even_balance_relative'],row['odd_balance_relative'])<1e-10)
            np.savez_compressed(folder/'fields.npz',**fields);np.savez_compressed(folder/'comparison.npz',**metrics);save(folder/'result.json',row);rows.append(row)
    save(target/'result.json',dict(rows=rows,order16_white_passed=all(r['white_passed'] for r in rows if r['order']==16),
        order8_white_passed=all(r['white_passed'] for r in rows if r['order']==8),physical_axial_escape_qualified=False))
    assert all(r['white_passed'] for r in rows if r['order']==16)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('artifact',type=Path);parser.add_argument('phase',choices=['recover','white']);parser.add_argument('height',type=float);parser.add_argument('nz',type=int)
    args=parser.parse_args();tick=time.perf_counter();root=args.artifact.resolve()
    (recover if args.phase=='recover' else white)(root,args.height,args.nz)
    usage=dict(elapsed_seconds=time.perf_counter()-tick,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    save(root/f'runs/{args.phase}_h{int(args.height)}_n{args.nz}_resources.json',usage)
    assert usage['elapsed_seconds']<600 and usage['peak_rss_mib']<512
