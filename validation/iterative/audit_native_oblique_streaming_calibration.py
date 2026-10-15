"""Audit all calibration raw witnesses and publish measured full-work costs."""
import argparse
import json
import resource
import time
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from native_oblique_streaming import ratio,checks
from calibrate_native_oblique_streaming import save,read
from run_native_oblique_streaming_calibration import digest


def audit_fields(f,totals):
    m=f['metrics'];flat=m.reshape(-1,48)
    np.testing.assert_array_equal(m[...,7],m[...,5]-m[...,4]+m[...,10]*m[...,6]-m[...,9]*m[...,11])
    np.testing.assert_array_equal(m[...,8],m[...,4]+m[...,9]*m[...,11])
    np.testing.assert_array_equal(m[...,18],m[...,14]+m[...,15]-m[...,16]-m[...,17])
    np.testing.assert_array_equal(m[...,19],m[...,14]+m[...,15])
    np.testing.assert_array_equal(m[...,24],m[...,20]+m[...,21]-m[...,22]-m[...,23])
    np.testing.assert_array_equal(m[...,25],m[...,20]+m[...,21])
    np.testing.assert_array_equal(m[...,2],ratio(m[...,7],m[...,8]));np.testing.assert_array_equal(m[...,12],ratio(m[...,18],m[...,19]))
    for error,a,b in [(26,38,39),(28,41,42),(30,44,45)]:np.testing.assert_array_equal(m[...,error],abs(m[...,a]-m[...,b]))
    gn,gw=leggauss(64);maximum=0.
    for first in range(0,len(flat),512):
        x=flat[first:first+512];l=x[:,9];sig=x[:,10];src=x[:,11];s=l[:,None]*(gn+1)/2;w=l[:,None]*gw/2
        exponential=np.exp(-sig[:,None]*s);b=(exponential*w).sum(axis=1);d=(exponential*(l[:,None]-s)*w).sum(axis=1)
        out=np.exp(-sig*l)*x[:,4]+b*src;integ=b*x[:,4]+d*src
        maximum=max(maximum,float(ratio(x[:,5]-out,np.maximum(out,x[:,5])).max()),float(ratio(x[:,6]-integ,np.maximum(integ,x[:,6])).max()))
    assert maximum<5e-12,maximum
    regional=f['regional'].sum(axis=(2,3));assert ratio(regional-m[:,:,:14,32],m[:,:,:14,32]).max()<5e-12
    linear=0.
    for gi,total in enumerate(totals):
        alpha=np.array([np.r_[np.arange(1,9)/8,np.arange(1,7)/6],np.r_[total,np.ones(6)]])
        for key in [32,33]:
            prediction=m[:,gi,:14,key]@alpha.T;actual=m[:,gi,14:,key]
            linear=max(linear,float(ratio(actual-prediction,np.maximum(prediction,actual)).max()))
    assert linear<5e-12
    return maximum,linear,len(flat)


def main(root,project):
    tick=time.perf_counter();d=read(root/'inputs/inventory.npz');plan=json.loads((root/'calibration_plan.json').read_text())
    maxima={};witness=linear=0.;ninputs=0;nfiles=0;nrays=0;measurements=[];estimates=[]
    for case in plan['cases']:
        pid=case['id'];primary=root/'calibration'/pid;replay=root/'replay/calibration'/pid
        receipt=json.loads((root/'replay/receipts'/(pid+'.json')).read_text());assert receipt['all_byte_identical']
        names=sorted(p.name for p in primary.iterdir());assert names==sorted(receipt['files'])==sorted(p.name for p in replay.iterdir())
        report=json.loads((primary/'result.json').read_text());assert report['implementation_calibration_passed']
        for name in names:
            h=digest(primary/name);assert h==digest(replay/name)==receipt['files'][name]['sha256'];nfiles+=1
            if not name.endswith('.npz'):continue
            f=read(primary/name);order=int(name.split('_q')[-1].removesuffix('.npz'));row=checks({k:f[k] for k in ['geometry','metrics','regional']},order);assert row['passed']
            expected=next(x for x in report['configurations'] if x['label']==name.removesuffix('.npz'))
            for key,value in row.items():assert expected[key]==value
            tracks=f['original_tracks'];block='largest_batch' if name.startswith('largest') else 'ranked'
            target=np.arange(case['batch_first'],case['batch_stop']) if block=='largest_batch' else np.array(case['ranked_tracks'])
            np.testing.assert_array_equal(tracks,target);nrays+=len(tracks)*3
            a,b,n=audit_fields(f,d['group_totals']);witness=max(witness,a);linear=max(linear,b);ninputs+=n
            for key,value in row.items():
                if key.endswith('relative'):maxima[key]=max(maxima.get(key,0.),value)
        times=[]
        for base in [root,root/'replay']:
            usage=json.loads((base/'runs'/(pid+'_resources.json')).read_text());measurements.append(usage)
            watchdog=json.loads((base/'runs'/(pid+'_watchdog.json')).read_text())
            assert watchdog['returncode']==0 and watchdog['limit_failure'] is None and watchdog['sampled_peak_rss_mib']<512 and watchdog['elapsed_seconds']<600
            assert usage['peak_rss_mib']<512 and usage['elapsed_seconds']<600
            large=[r for r in usage['timing'] if r['label'].startswith('largest')]
            times.append(dict(kernel=sum(t['kernel_seconds'] for t in large),write=sum(t['write_seconds'] for t in large),
                reference=sum(max(t['reference_seconds_per_orientation'] for t in large if f'_o{o}_' in t['label']) for o in [1,-1])))
        work=read(root/'inputs'/f'counts_{pid}.npz')['work'];worst={key:max(t[key] for t in times) for key in times[0]}
        rate=case['largest_batch_piece_columns']/worst['kernel'];count=int(np.ceil(11364/512))
        # Twofold measured work/serialization/reference cost plus one second
        # per child; freeze this complete primary-plus-replay bound before any
        # full response is admitted. Every remaining group/state is included.
        seconds=2*(int(work.sum())/rate+count*(worst['write']+worst['reference']))+count
        estimates.append(dict(case=pid,measured_updates_per_second=rate,maximum_observed_batch=worst,
            complete_primary_plus_replay_seconds=2*seconds,processes_per_pass=count,
            largest_process_budget_seconds=2*sum(worst.values())+1))
    for base in [root,root/'replay']:
        log=(base/'runs/tests.log').read_text();assert 'Ran 8 tests' in log and log.rstrip().endswith('OK')
    identities={}
    for name,base in [('protected_inputs_before.json',project),('initial_inputs.json',root),('calibration_inputs.json',root),('replay_inputs.json',root),('verification_inputs.json',root)]:
        values=json.loads((root/name).read_text())
        for path,h in values.items():assert digest(base/path)==h,(name,path)
        identities[name]=len(values)
    prior=json.loads((root/'prior_artifacts.json').read_text());entries=0
    for name,h in prior.items():
        folder=project/'validation/artifacts'/name;assert digest(folder/'result.sha256')==h
        for line in (folder/'result.sha256').read_text().splitlines():
            sha,path=line.split('  ',1);assert digest(folder/path)==sha,(name,path);entries+=1
    save(root/'verification/measured_full_costs.json',dict(cases=estimates,
        complete_primary_plus_replay_seconds=sum(x['complete_primary_plus_replay_seconds'] for x in estimates),
        maximum_process_budget_seconds=max(x['largest_process_budget_seconds'] for x in estimates),
        observed_peak_rss_mib=max(x['peak_rss_mib'] for x in measurements),
        full_execution_admitted=False,pending='Freeze output schema/bounds and full plan; calibrate independent flight on every original track before the oblique matrix.'))
    result=dict(identities=identities,prior_artifacts=len(prior),prior_manifest_entries=entries,
        byte_identical_files=nfiles,tests_per_pass=8,track_group_configurations=nrays,input_evaluations=ninputs,
        gates=maxima,independent_primitive_witness_relative=witness,independent_whole_track_source_assembly_relative=linear,
        observed_peak_rss_mib=max(x['peak_rss_mib'] for x in measurements),maximum_process_seconds=max(x['elapsed_seconds'] for x in measurements),
        implementation_calibration_qualified=True,full_native_operator_qualified=False,
        elapsed_seconds=time.perf_counter()-tick,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
    assert result['elapsed_seconds']<600 and result['peak_rss_mib']<512
    save(root/'verification/result.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);p.add_argument('project',type=Path);a=p.parse_args();main(a.artifact.resolve(),a.project.resolve())
