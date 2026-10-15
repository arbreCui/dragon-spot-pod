#!/usr/bin/env python3
"""Independent, predeclared block analysis of CE statepoints; no transport.

The paired resampling unit is a contiguous block of all raw tally increments.
Every bootstrap replicate receives ONE global nu-fission denominator. The
stationarity/resolution rules below are engineering admission screens, not a
proof of source convergence or a universal confidence-coverage theorem.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re

import numpy as np

DEFAULT_SPEC = Path(__file__).with_name('case_spec.json')


class EvidenceError(ValueError):
    """Missing or inconsistent evidence: the comparison is inconclusive."""


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def predeclared_rules(spec_path=DEFAULT_SPEC):
    spec_path = Path(spec_path)
    spec = json.loads(spec_path.read_text())
    shape = spec['predeclared_decisions']['shape_targets']
    return dict(
        schema='AXMAT_CE_BLOCK_RULES_V1', case_spec_sha256=digest(spec_path),
        implementation_sha256=digest(Path(__file__)),
        intended_scope='CE total method-plus-data comparison; no POD-only attribution.',
        active_batches=spec['reference']['active_batches'],
        inactive_batches=spec['reference']['inactive_batches'],
        particles=spec['reference']['particles_per_batch'], generations_per_batch=1,
        seeds={case:spec['reference']['seed_'+case] for case in ['AAA','ABA']},
        block_lengths=[5,10], minimum_blocks=20,
        bootstrap_replicates=4000, bootstrap_seed=310037,
        lower_quantile=0.05, upper_quantile=0.95, quantile_method='higher',
        flux_l2_target=shape['fission_normalized_scalar_flux_volume_weighted_relative_l2_max'],
        fuel_fission_max_target=shape['normalized_nu_fission_max_relative_difference_in_fuel_bins'],
        k_sigma_pcm_max=spec['predeclared_decisions']['keff']['sigma_pcm_max'],
        k_base_allowance_pcm=500.0, k_sigma_multiplier=3.0,
        resolution_fraction_of_target=0.5,
        block_upper_difference_fraction_of_target=0.25,
        block_reference_uncertainty_ratio_max=1.5,
        near_zero_uncertainty_floor=1e-13,
        stationarity_welch_z_max=3.29,
        block_lag1_absolute_max=0.5,
        history_bridge_batches=50,
        volume_relative_tolerance=5e-6,
        independent_tally_relative_tolerance=1e-9,
        require_entropy=True,
        entropy_policy='The formal input declares a source entropy mesh. Require its finite full history; check the inactive/active bridge and active blocks jointly with k-generation and spatial fission/flux histories.',
        adequacy_rules=[
            'Exactly the declared active batches, consecutive realizations from one to N, one generation per batch; no missing batch, truncation, or post-result block choice.',
            'Every block length must divide N and provide at least 20 contiguous nonoverlapping blocks; retain all batches.',
            'Finite nonnegative raw flux and nu-fission increments, positive global nu-fission and every fuel-bin mean; preserve signed currents.',
            'Both block lengths must give reference-only 95% bootstrap error <= half its corresponding engineering target.',
            'The two shape upper limits must differ by <= one quarter of the engineering target; reference-only uncertainty ratios must be <=1.5, except values both <=1e-13.',
            'For each block length, k-generation, three-zone and all axial-cell globally normalized fission/flux proxies must have first-half/last-half Welch |z|<=3.29 and absolute lag-one correlation<=0.5.',
            'The declared source entropy history is required. The final 50 inactive and first 50 active k-generation and entropy values must satisfy the same drift screen.',
            'Combined-keff sigma in reactivity units must be <=50 pcm; k-generation diagnostics never replace the combined-keff estimator.',
            'Any inadequate reference statistics or incomplete input produces INCONCLUSIVE. Otherwise PASS requires both shape 95% upper limits below targets and the inherited k gate. FAIL requires a shape 5% lower limit above target for both block lengths, or a failed k gate; crossing intervals are INCONCLUSIVE.',
        ])


def incremental_batches(cumulative, realizations):
    """Recover individual batch scores, including the first active batch."""
    cumulative = np.asarray(cumulative, dtype=float)
    realizations = np.asarray(realizations)
    if cumulative.ndim < 2 or len(cumulative) != len(realizations):
        raise EvidenceError('cumulative tally shape and realization counts disagree')
    if not np.array_equal(realizations, np.arange(1,len(realizations)+1)):
        raise EvidenceError('require consecutive active realizations beginning at one')
    if not np.isfinite(cumulative).all():
        raise EvidenceError('nonfinite cumulative tally')
    return np.diff(cumulative, axis=0, prepend=np.zeros_like(cumulative[:1]))


def contiguous_blocks(values, length, minimum=20):
    values = np.asarray(values, dtype=float)
    if type(length) is not int or length <= 0 or len(values) % length:
        raise EvidenceError('block length must divide the full active history; no tail discarded')
    count = len(values)//length
    if count < minimum:
        raise EvidenceError(f'only {count} blocks, require at least {minimum}')
    return values.reshape(count,length,*values.shape[1:]).mean(axis=1)


def normalized_observables(rates, volumes):
    """Input: (..., bins, [integrated flux, integrated nu-fission])."""
    rates = np.asarray(rates, dtype=float)
    denominator = rates[...,1].sum(axis=-1)
    if not np.isfinite(rates).all() or np.any(denominator <= 0):
        raise EvidenceError('nonfinite rates or nonpositive global nu-fission')
    flux = rates[...,0]/np.asarray(volumes)/denominator[...,None]
    fission = rates[...,1]/denominator[...,None]
    return flux,fission,denominator


def discrepancy(reference, production, volumes, fuel):
    rf, rn = reference
    pf, pn = production
    norm = np.sum(volumes*rf*rf, axis=-1)
    if np.any(norm <= 0) or np.any(rn[...,fuel] <= 0):
        raise EvidenceError('nonpositive reference flux norm or fuel production')
    flux = np.sqrt(np.sum(volumes*(pf-rf)**2,axis=-1)/norm)
    fission = np.max(np.abs(pn[...,fuel]/rn[...,fuel]-1),axis=-1)
    return np.stack([flux,fission],axis=-1)


def bootstrap_block_means(blocks, replicates, seed):
    """Joint block weights preserve every inter-bin and denominator correlation."""
    count = len(blocks)
    rng = np.random.default_rng(seed)
    weights = rng.multinomial(count,np.full(count,1/count),size=replicates)
    flat = np.asarray(blocks).reshape(count,-1)
    samples = (weights@flat/count).reshape(replicates,*blocks.shape[1:])
    return samples,weights


def scalar_history_check(values, z_limit, lag_limit):
    x = np.asarray(values,dtype=float)
    if x.ndim != 1 or len(x)<4 or not np.isfinite(x).all():
        return dict(passed=False,reason='missing or nonfinite history')
    split = len(x)//2
    a,b = x[:split],x[split:]
    difference = float(b.mean()-a.mean())
    se = float(np.sqrt(a.var(ddof=1)/len(a)+b.var(ddof=1)/len(b)))
    zero_scale = np.finfo(float).eps*max(float(np.max(np.abs(x))),1)*16
    if se <= zero_scale:
        z = 0.0 if abs(difference)<=zero_scale else None
    else:
        z = abs(difference)/se
    centered = x-x.mean()
    variance = float(centered@centered)
    lag = 0.0 if variance<=len(x)*zero_scale**2 else float(centered[:-1]@centered[1:]/variance)
    return dict(passed=bool(z is not None and z<=z_limit and abs(lag)<=lag_limit),
                first_half_mean=float(a.mean()),last_half_mean=float(b.mean()),
                difference=difference,welch_z=z,lag1=lag,
                zero_variance_drift=bool(z is None))


def bridge_check(history, inactive, length, z_limit):
    x=np.asarray(history,dtype=float)
    if inactive<length or len(x)<inactive+length or not np.isfinite(x).all():
        return dict(passed=False,reason='missing complete inactive/active bridge')
    # Only the change in means is screened here. Serial dependence is checked
    # separately on the two active block lengths.
    combined=np.r_[x[inactive-length:inactive],x[inactive:inactive+length]]
    result=scalar_history_check(combined,z_limit,1.0)
    result['window_batches']=length
    return result


def stationarity(rates, volumes, zones, axial_cells, history, rules, length):
    blocks=contiguous_blocks(rates,length,rules['minimum_blocks'])
    flux,fission,_=normalized_observables(blocks,volumes)
    start=rules['inactive_batches'];stop=start+len(rates)
    k=np.asarray(history.get('k_generation',[]),dtype=float)
    checks={}
    if len(k)<stop:
        checks['k_generation']=dict(passed=False,reason='k-generation history missing')
    else:
        kb=contiguous_blocks(k[start:stop,None],length,rules['minimum_blocks']).ravel()
        checks['k_generation']=scalar_history_check(kb,rules['stationarity_welch_z_max'],rules['block_lag1_absolute_max'])
    for grouping,labels in [('zone',zones),('axial_cell',axial_cells)]:
        for label in sorted(set(labels.tolist())):
            mask=labels==label
            for name,series in [('fission',fission[:,mask].sum(axis=1)),
                                ('flux',(flux[:,mask]*volumes[mask]).sum(axis=1))]:
                checks[f'{grouping}_{label}_{name}_proxy']=scalar_history_check(series,rules['stationarity_welch_z_max'],rules['block_lag1_absolute_max'])
    entropy=np.asarray(history.get('entropy',[]),dtype=float)
    if len(entropy):
        if len(entropy)<stop:
            checks['entropy']=dict(passed=False,reason='entropy history truncated')
        else:
            eb=contiguous_blocks(entropy[start:stop,None],length,rules['minimum_blocks']).ravel()
            checks['entropy']=scalar_history_check(eb,rules['stationarity_welch_z_max'],rules['block_lag1_absolute_max'])
    elif rules['require_entropy']:
        checks['entropy']=dict(passed=False,reason='declared source entropy history missing')
    return dict(passed=all(row['passed'] for row in checks.values()),checks=checks,
                entropy_available=bool(len(entropy)),
                limitation='Active spatial fission/flux tally histories are source-convergence proxies, not source-bank measurements.')


def analyze_batches(batch_rates, volumes, regions, zones, axial_cells, production_rates, production_volumes,
                    k_reference, sigma_k_reference, k_production, history, rules,
                    batch_currents=None, batch_partial_currents=None):
    rates=np.asarray(batch_rates,dtype=float);volumes=np.asarray(volumes,dtype=float)
    regions=np.asarray(regions);zones=np.asarray(zones);axial_cells=np.asarray(axial_cells)
    production_rates=np.asarray(production_rates,dtype=float)
    production_volumes=np.asarray(production_volumes,dtype=float)
    if rates.ndim!=3 or rates.shape[2]!=2 or len(rates)!=rules['active_batches']:
        raise EvidenceError('require declared complete active history with separate flux/nu-fission scores')
    if rates.shape[1:]!=production_rates.shape or volumes.shape!=(rates.shape[1],) or production_volumes.shape!=volumes.shape:
        raise EvidenceError('reference/production bin shapes disagree')
    if any(labels.shape!=volumes.shape for labels in [regions,zones,axial_cells]):
        raise EvidenceError('region/zone/axial-cell labels disagree with tally bins')
    if not np.isfinite(rates).all() or np.any(rates<0):
        raise EvidenceError('nonfinite or negative CE batch rates; no clipping allowed')
    if not np.isfinite(production_rates).all() or np.any(production_rates<0):
        raise EvidenceError('nonfinite or negative production rates; no clipping allowed')
    if np.any(volumes<=0) or np.any(production_volumes<=0) or not np.isfinite(volumes).all() or not np.isfinite(production_volumes).all():
        raise EvidenceError('invalid physical volumes')
    if np.max(abs(volumes-production_volumes)/volumes)>rules['volume_relative_tolerance']:
        raise EvidenceError('independent geometry volume mismatch')
    if any(not np.isfinite(x) for x in [k_reference,sigma_k_reference,k_production]) or min(k_reference,k_production)<=0 or sigma_k_reference<0:
        raise EvidenceError('invalid eigenvalue evidence')
    fuel=np.isin(regions,[4,5,6,7])
    if not fuel.any() or np.any(rates[...,1].sum(axis=1)<=0):
        raise EvidenceError('missing fuel or nonpositive batch global production')
    if batch_currents is not None:
        current_array=np.asarray(batch_currents)
        if current_array.ndim!=2 or len(current_array)!=len(rates) or not np.isfinite(current_array).all():
            raise EvidenceError('invalid signed current batch history')
    ref_flux,ref_fission,denom=normalized_observables(rates.mean(axis=0),volumes)
    prod_flux,prod_fission,_=normalized_observables(production_rates,production_volumes)
    point=discrepancy((ref_flux,ref_fission),(prod_flux,prod_fission),volumes,fuel)
    sigma_pcm=1e5*sigma_k_reference/k_reference**2
    difference_pcm=1e5*(1/k_reference-1/k_production)
    allowance=rules['k_base_allowance_pcm']+rules['k_sigma_multiplier']*sigma_pcm
    reasons=[]
    if sigma_pcm>rules['k_sigma_pcm_max']:reasons.append('combined_keff_sigma_above_limit')
    bridges={'k_generation':bridge_check(history.get('k_generation',[]),rules['inactive_batches'],rules['history_bridge_batches'],rules['stationarity_welch_z_max'])}
    if len(history.get('entropy',[])):
        bridges['entropy']=bridge_check(history['entropy'],rules['inactive_batches'],rules['history_bridge_batches'],rules['stationarity_welch_z_max'])
    elif rules['require_entropy']:
        bridges['entropy']=dict(passed=False,reason='declared source entropy history missing')
    if not all(row['passed'] for row in bridges.values()):reasons.append('inactive_active_history_drift_or_missing')
    targets=np.array([rules['flux_l2_target'],rules['fuel_fission_max_target']])
    block_reports=[]
    for length in rules['block_lengths']:
        blocks=contiguous_blocks(rates,length,rules['minimum_blocks'])
        samples,weights=bootstrap_block_means(blocks,rules['bootstrap_replicates'],rules['bootstrap_seed']+length)
        rf,rn,rd=normalized_observables(samples,volumes)
        errors=discrepancy((rf,rn),(prod_flux,prod_fission),volumes,fuel)
        noise=discrepancy((ref_flux,ref_fission),(rf,rn),volumes,fuel)
        low=np.quantile(errors,rules['lower_quantile'],axis=0,method=rules['quantile_method'])
        upper=np.quantile(errors,rules['upper_quantile'],axis=0,method=rules['quantile_method'])
        noise_upper=np.quantile(noise,rules['upper_quantile'],axis=0,method=rules['quantile_method'])
        resolution=bool(np.all(noise_upper<=targets*rules['resolution_fraction_of_target']))
        source=stationarity(rates,volumes,zones,axial_cells,history,rules,length)
        if not resolution:reasons.append(f'block_{length}_statistical_resolution')
        if not source['passed']:reasons.append(f'block_{length}_source_history')
        report=dict(block_length=length,blocks=len(blocks),lower_05=low.tolist(),upper_95=upper.tolist(),
                    reference_only_error_upper_95=noise_upper.tolist(),resolution_passed=resolution,
                    source_stationarity=source,
                    normalized_reference_covariance_trace=dict(flux=float(np.var(rf,axis=0,ddof=1).sum()),nu_fission=float(np.var(rn,axis=0,ddof=1).sum())))
        if batch_currents is not None:
            cb=contiguous_blocks(np.asarray(batch_currents),length,rules['minimum_blocks'])
            current_samples=(weights@cb/len(blocks))/rd[:,None]
            report['current_per_global_nufission']=dict(lower_05=np.quantile(current_samples,0.05,axis=0,method=rules['quantile_method']).tolist(),upper_95=np.quantile(current_samples,0.95,axis=0,method=rules['quantile_method']).tolist(),
                                                       scope='Full cross-section per +z plane; not region currents.')
        block_reports.append(report)
    uppers=np.asarray([row['upper_95'] for row in block_reports]);lowers=np.asarray([row['lower_05'] for row in block_reports])
    noises=np.asarray([row['reference_only_error_upper_95'] for row in block_reports])
    spread=np.ptp(uppers,axis=0)
    floor=rules['near_zero_uncertainty_floor']
    ratio=noises.max(axis=0)/np.maximum(noises.min(axis=0),floor)
    ratio=np.where(noises.max(axis=0)<=floor,1,ratio)
    sensitive=bool(np.any(spread>targets*rules['block_upper_difference_fraction_of_target']) or np.any(ratio>rules['block_reference_uncertainty_ratio_max']))
    if sensitive:reasons.append('block_length_sensitivity')
    shape_status=[]
    for index in range(2):
        shape_status.append('PASS' if uppers[:,index].max()<=targets[index] else 'FAIL' if lowers[:,index].min()>targets[index] else 'INCONCLUSIVE')
    k_status='PASS' if abs(difference_pcm)<=allowance else 'FAIL'
    if reasons:status='INCONCLUSIVE'
    elif 'FAIL' in shape_status or k_status=='FAIL':status='FAIL'
    elif 'INCONCLUSIVE' in shape_status:status='INCONCLUSIVE'
    else:status='PASS'
    result=dict(status=status,reference_statistics_adequate=not reasons,inconclusive_reasons=reasons,
                metric_order=['volume_weighted_normalized_flux_l2','fuel_normalized_nufission_max_relative'],
                point_discrepancies=point.tolist(),targets=targets.tolist(),shape_status=shape_status,
                conservative_upper_95=uppers.max(axis=0).tolist(),conservative_lower_05=lowers.min(axis=0).tolist(),
                k=dict(reference=k_reference,sigma_k=sigma_k_reference,sigma_pcm=sigma_pcm,production=k_production,
                       reactivity_difference_pcm=difference_pcm,allowance_pcm=allowance,status=k_status),
                global_reference_nufission=float(denom),normalization='one global nu-fission integral, recomputed jointly for every replicate',
                reference_flux=ref_flux.tolist(),reference_nufission_fraction=ref_fission.tolist(),
                block_reports=block_reports,block_upper_spread=spread.tolist(),block_reference_uncertainty_ratio=ratio.tolist(),
                history_bridges=bridges,entropy_available=bool(len(history.get('entropy',[]))),
                caveat='Percentile block-bootstrap engineering screen conditional on observed stationarity and chosen block lengths; not a universal coverage/source-convergence theorem.')
    result['checks']=dict(
        source_convergence_screen='PASS' if all(row['passed'] for row in bridges.values()) and all(row['source_stationarity']['passed'] for row in block_reports) else 'INCONCLUSIVE',
        block_stability='PASS' if not sensitive else 'INCONCLUSIVE',
        statistical_resolution='PASS' if all(row['resolution_passed'] for row in block_reports) and sigma_pcm<=rules['k_sigma_pcm_max'] else 'INCONCLUSIVE',
        keff=k_status if sigma_pcm<=rules['k_sigma_pcm_max'] else 'INCONCLUSIVE',
        scalar_flux=shape_status[0] if not reasons else 'INCONCLUSIVE',
        nu_fission=shape_status[1] if not reasons else 'INCONCLUSIVE',
        input_equivalence='NOT_ASSESSED', production_fixed_point='NOT_ASSESSED',
        full_particle_balance='NOT_ASSESSED')
    if batch_currents is not None:
        currents=np.asarray(batch_currents,dtype=float).mean(axis=0)/denom
        result['currents']=dict(net_plus_z_per_nufission=currents.tolist(),bottom_outward=float(-currents[0]),top_outward=float(currents[-1]),
                                total_axial_escape=float(currents[-1]-currents[0]),telescoping_difference=float(np.diff(currents).sum()-(currents[-1]-currents[0])),
                                limitation='Telescoping is an interface accounting identity, not an independently measured neutron balance; no absorption tally is available.')
        if batch_partial_currents is not None:
            result['currents']['signed_directional_crossing_per_nufission']=(np.asarray(batch_partial_currents).mean(axis=0)/denom).tolist()
            result['currents']['directional_bin_order']=['negative_z','positive_z']
    return result


def extract_statepoints(directory, contract, rules):
    """Read OpenMC's cumulative SUM, never differences of cumulative means."""
    import openmc
    directory=Path(directory)
    direction=contract.get('directional_current_filter',{})
    if contract.get('schema')!='AXMAT_CE_INPUT_V2' or direction.get('type')!='polar' or direction.get('raw_bin_order')!=['positive_z','negative_z'] or direction.get('signed_score') is not True:
        raise EvidenceError('require V2 global-polar signed-current contract; MuSurface V1 is invalid directional evidence')
    case=contract['case'];inactive=rules['inactive_batches'];active=rules['active_batches']
    if not contract['statepoint_every_active_batch']:
        raise EvidenceError('every-active-batch statepoints are required')
    expected_cells=[row['cell_id'] for row in contract['region_layer_bins']]
    expected_layers=[row['cell_id'] for row in contract['layer_bins']]
    expected_surfaces=[row['surface_id'] for row in contract['plane_bins']]
    cumulative={name:[] for name in ['rates','layers','current','partial']}
    realizations=[];identities=[];history={};k=sigma=None
    paths={}
    for candidate in directory.glob('statepoint.*.h5'):
        match=re.fullmatch(r'statepoint\.(\d+)\.h5',candidate.name)
        if match:
            batch=int(match[1])
            if batch in paths:raise EvidenceError('ambiguous duplicate statepoint batch')
            paths[batch]=candidate
    for current in range(inactive+1,inactive+active+1):
        path=paths.get(current)
        if path is None:raise EvidenceError(f'missing active statepoint batch: {current}')
        with openmc.StatePoint(path,autolink=False) as sp:
            if sp.run_mode!='eigenvalue' or sp.current_batch!=current or sp.n_batches!=inactive+active or sp.n_inactive!=inactive or sp.n_particles!=rules['particles'] or sp.generations_per_batch!=1 or sp.seed!=rules['seeds'][case]:
                raise EvidenceError('statepoint runtime identity differs from frozen rules')
            realizations.append(int(sp.n_realizations))
            def values(name,score,bins,filter_type,filter_count=1):
                tally=sp.get_tally(id=contract['tally_ids'][name])
                if tally.num_realizations!=sp.n_realizations or tally.nuclides!=['total']:
                    raise EvidenceError('tally realization/nuclide schema mismatch')
                if len(tally.filters)!=filter_count or not isinstance(tally.filters[0],filter_type) or list(tally.filters[0].bins)!=bins:
                    raise EvidenceError('tally mapping differs from input contract')
                expected_scores=['flux','nu-fission'] if name in ['region_layer_rates','layer_rates'] else ['current']
                if tally.scores!=expected_scores:raise EvidenceError('tally score schema differs from the independent analysis contract')
                return np.array(tally.get_values(scores=[score],value='sum'),copy=True).reshape(-1)
            cumulative['rates'].append(np.stack([values('region_layer_rates',score,expected_cells,openmc.CellFilter) for score in ['flux','nu-fission']],axis=-1))
            cumulative['layers'].append(np.stack([values('layer_rates',score,expected_layers,openmc.CellFilter) for score in ['flux','nu-fission']],axis=-1))
            cumulative['current'].append(values('axial_plane_net_current','current',expected_surfaces,openmc.SurfaceFilter))
            partial=sp.get_tally(id=contract['tally_ids']['axial_plane_directional_current'])
            if len(partial.filters)!=2 or not isinstance(partial.filters[1],openmc.PolarFilter) or not np.array_equal(partial.filters[1].bins,[[0,np.pi/2],[np.pi/2,np.pi]]):
                raise EvidenceError('signed-current angular bins differ')
            raw_partial=values('axial_plane_directional_current','current',expected_surfaces,openmc.SurfaceFilter,filter_count=2).reshape(len(expected_surfaces),2)
            cumulative['partial'].append(raw_partial[:,[1,0]])  # Canonical negative_z, positive_z.
            if current==inactive+active:
                k=float(sp.keff.nominal_value);sigma=float(sp.keff.std_dev)
                history['k_generation']=np.asarray(sp.k_generation).tolist()
                try:history['entropy']=np.asarray(sp.entropy).tolist()
                except KeyError:history['entropy']=[]
        identities.append(dict(path=str(path),sha256=digest(path)))
    batches={name:incremental_batches(rows,realizations) for name,rows in cumulative.items()}
    rates=batches['rates'];layer_sum=np.stack([rates[:,row['region_tally_bins']].sum(axis=1) for row in contract['layer_bins']],axis=1)
    scale=np.maximum(abs(layer_sum),abs(batches['layers']))
    if np.max(abs(layer_sum-batches['layers'])/np.maximum(scale,1e-30))>rules['independent_tally_relative_tolerance']:
        raise EvidenceError('independent region/layer tally sums disagree')
    partial=batches['partial'];current=batches['current'];scale=abs(partial).sum(axis=-1)
    if not np.isfinite(partial).all() or np.max(abs(partial.sum(axis=-1)-current)/np.maximum(scale,1e-30))>rules['independent_tally_relative_tolerance']:
        raise EvidenceError('directional/net current tallies disagree')
    if np.any(partial[:,:,0]>0) or np.any(partial[:,:,1]<0) or np.any(partial[:,0,1]!=0) or np.any(partial[:,-1,0]!=0):
        raise EvidenceError('signed-current/vacuum-entry checks fail')
    return batches,k,sigma,history,identities


def mapped_comparison_inputs(contract, batch_rates, production_csv):
    with Path(production_csv).open() as stream:
        rows=list(csv.DictReader(stream))
    lookup={(int(row['radial_region']),int(row['axial_cell'])):row for row in rows}
    if len(lookup)!=len(rows):raise EvidenceError('duplicate production region/cell')
    keys=sorted(lookup)
    grouped={key:[] for key in keys}
    for index,row in enumerate(contract['region_layer_bins']):
        key=(row['region'],row['production_axial_cell'])
        if key not in grouped:raise EvidenceError('production is missing a reference bin')
        grouped[key].append(index)
    if any(not indices for indices in grouped.values()):raise EvidenceError('production has unmatched bins')
    for key,indices in grouped.items():
        if any(contract['region_layer_bins'][i]['physical_zone']!=int(lookup[key]['physical_zone']) for i in indices):
            raise EvidenceError('reference/production physical-zone labels disagree')
    rates=np.stack([batch_rates[:,grouped[key]].sum(axis=1) for key in keys],axis=1)
    volumes=np.array([sum(contract['region_layer_bins'][i]['volume_cm3'] for i in grouped[key]) for key in keys])
    production=np.array([[float(lookup[key]['integrated_flux']),float(lookup[key]['integrated_nufission'])] for key in keys])
    pv=np.array([float(lookup[key]['volume_cm3']) for key in keys])
    zones=np.array([int(lookup[key]['physical_zone']) for key in keys])
    if any(int(lookup[key]['nonpositive_group_flux_count'])!=0 for key in keys):
        raise EvidenceError('production contains nonpositive energy-group scalar flux')
    return rates,volumes,np.array([key[0] for key in keys]),zones,np.array([key[1] for key in keys]),production,pv


def write_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as stream:
        json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    freeze=sub.add_parser('rules');freeze.add_argument('output',type=Path);freeze.add_argument('--case-spec',type=Path,default=DEFAULT_SPEC)
    analyze=sub.add_parser('analyze');analyze.add_argument('--rules',type=Path,required=True);analyze.add_argument('--case-spec',type=Path,default=DEFAULT_SPEC)
    analyze.add_argument('--contract',type=Path,required=True);analyze.add_argument('--statepoints',type=Path,required=True)
    analyze.add_argument('--production-regions',type=Path,required=True);analyze.add_argument('--production-summary',type=Path,required=True);analyze.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.command=='rules':write_json(args.output,predeclared_rules(args.case_spec));return
    contract={}
    try:
        rules=json.loads(args.rules.read_text());contract=json.loads(args.contract.read_text())
        if rules!=predeclared_rules(args.case_spec):raise EvidenceError('rules/code/case_spec differs from frozen statistical declaration')
        batches,k,sigma,history,identities=extract_statepoints(args.statepoints,contract,rules)
        inputs=mapped_comparison_inputs(contract,batches['rates'],args.production_regions)
        summary=dict(line.split('=',1) for line in args.production_summary.read_text().splitlines() if '=' in line)
        result=analyze_batches(*inputs,k,sigma,float(summary['k64']),history,rules,
                               batch_currents=batches['current'],batch_partial_currents=batches['partial'])
        result['statepoint_identities']=identities
    except (ValueError,OSError,KeyError) as error:
        result=dict(status='INCONCLUSIVE',reference_statistics_adequate=False,inconclusive_reasons=[str(error)])
    result['input_identities']={str(path):digest(path) for path in [args.case_spec,args.rules,args.contract,args.production_regions,args.production_summary] if path.exists()}
    result['classification']='STATISTICAL_COMPARISON_'+result['status']
    result['qualification_scope']='Statistics and shape/keff comparison only; not a full AAA_REFERENCE_QUALIFIED receipt. Input equivalence, production lineage/fixed point and independent current/balance/symmetry qualification remain external.'
    result['case']=contract.get('case')
    result['method']='independent_continuous_energy_openmc'
    result['transport_executed']=False
    write_json(args.output,result)
    print(json.dumps(dict(status=result['status'],output=str(args.output))))


if __name__=='__main__':main()
