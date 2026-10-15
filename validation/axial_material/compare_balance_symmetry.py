#!/usr/bin/env python3
"""Independent signed-current, telescoping and axial-symmetry admission.

No transport is launched. Telescoping tests conservation of shared face accounts,
not a complete neutron balance with independently scored absorption and sources.
The bootstrap band is simultaneous across the entire declared mirror family;
it remains an engineering inference conditional on the saved batch history.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

import reference_statistics as rs


def predeclared_rules(spec_path=rs.DEFAULT_SPEC):
    spec=json.loads(Path(spec_path).read_text())
    return dict(schema='AXMAT_CURRENT_BALANCE_SYMMETRY_RULES_V1',
        case_spec_sha256=rs.digest(spec_path), implementation_sha256=rs.digest(__file__),
        statistics_implementation_sha256=rs.digest(rs.__file__),
        intended_cases=spec['cases'], radial_regions=spec['geometry']['radial_regions'],
        axial_cells=3*spec['geometry']['cells_per_zone'], groups=spec['production']['groups'],
        height_cm=spec['geometry']['physical_z_edges_cm'][-1],
        symmetry_relative_tolerance=50*spec['production']['outer_gate_each'],
        production_symmetry_definition='For each radial profile separately, max(abs(f-mirror(f)))/max(abs(f)); for +z current use f+mirror(f), including the middle face. Identically zero profiles require exactly zero residual.',
        production_symmetry_scope='New deterministic numerical symmetry screen; not a cross-method accuracy target.',
        epsilon64=float(np.finfo(np.float64).eps), telescoping_epsilon_multiplier=64,
        telescoping_bound='64*epsilon64*sum(abs(already group-summed region-face currents)); same stored face appears at both neighboring cells, so group accumulation errors cancel in this accounting identity and are not added as a physical balance allowance.',
        normalization_sum_bound='For n nonnegative exported integrals, gamma(n+2)*sum(abs(integrals)), gamma(m)=m*u/(1-m*u), u=epsilon64/2. This checks the independently resummed denominator against the exporter summary.',
        independent_tally_relative_tolerance=1e-9,
        physical_volume_relative_tolerance=5e-6,
        block_lengths=[5,10], minimum_blocks=20,
        active_batches=spec['reference']['active_batches'],
        bootstrap_replicates=4000, bootstrap_seed=310041,
        simultaneous_quantile=0.95, quantile_method='higher',
        simultaneous_family='All CE region-by-tally-layer scalar-flux and nu-fission mirror pairs, all unique full-section net-current antisymmetric face pairs including the middle face, and signed negative/positive directional mirror pairs at every face; one joint family across all scores.',
        simultaneous_method='Resample joint contiguous blocks; recompute one global nu-fission denominator per draw; residual draws minus observed residual vector are centered bootstrap errors. Divide each component by its bootstrap standard deviation and take the 95% quantile of the maximum absolute standardized error over the entire family. Simultaneous intervals are observed residual +/- q95*standard_deviation. A zero-variance component uses the maximum absolute centered error as its roundoff width. Both block lengths must contain the all-zero vector.',
        ce_symmetry_failure_status='INCONCLUSIVE_SOURCE_SYMMETRY',
        cross_method_current_gate=None,
        cross_method_policy='Report signed differences of full-section plane currents and real bottom/top/total escapes only. No current-accuracy threshold was declared in case_spec.',
        full_neutron_balance='NOT_ASSESSED: no independent absorption/source tally; telescoping alone is not a neutron-balance proof.',
        qualification_scope='PASS applies only to complete sign, telescoping-accounting and symmetry checks here. Input equivalence, fixed-point validity, source-history stability and shape/keff accuracy are separate prerequisites.')


def gamma(operations, epsilon):
    product=operations*epsilon/2
    if product>=1:raise rs.EvidenceError('invalid roundoff operation bound')
    return product/(1-product)


def rows_from_csv(path):
    with Path(path).open() as stream:return list(csv.DictReader(stream))


def read_production(regions_path, faces_path, summary_path, rules):
    """Parse the saved REAL64 exporter, preserving every current sign."""
    region_rows=rows_from_csv(regions_path);face_rows=rows_from_csv(faces_path)
    summary=dict(line.split('=',1) for line in Path(summary_path).read_text().splitlines() if '=' in line)
    nr=rules['radial_regions'];nz=rules['axial_cells']
    if [int(summary[key]) for key in ['radial_regions','axial_cells','groups']]!=[nr,nz,rules['groups']]:
        raise rs.EvidenceError('production dimensions differ from frozen case')
    regions={(int(r['radial_region']),int(r['axial_cell'])):r for r in region_rows}
    faces={(int(r['radial_region']),int(r['face'])):r for r in face_rows}
    if len(regions)!=len(region_rows) or set(regions)!={(r,z) for r in range(1,nr+1) for z in range(1,nz+1)}:
        raise rs.EvidenceError('duplicate or incomplete region/cell map')
    if len(faces)!=len(face_rows) or set(faces)!={(r,z) for r in range(1,nr+1) for z in range(nz+1)}:
        raise rs.EvidenceError('duplicate or incomplete region/face map')
    def region_array(key):return np.array([[float(regions[r,z][key]) for z in range(1,nz+1)] for r in range(1,nr+1)])
    def face_array(key):return np.array([[float(faces[r,z][key]) for z in range(nz+1)] for r in range(1,nr+1)])
    rates=np.stack([region_array('integrated_flux'),region_array('integrated_nufission')],axis=-1)
    volumes=region_array('volume_cm3');currents=face_array('integrated_net_current_plus_z')
    z=face_array('z_cm');area=face_array('area_cm2')
    expected=np.linspace(0,rules['height_cm'],nz+1)
    if np.max(abs(z-expected))>64*rules['epsilon64']*max(1,rules['height_cm']):
        raise rs.EvidenceError('production axial faces differ from declared geometry')
    if not all(np.isfinite(a).all() for a in [rates,volumes,currents,z,area]) or np.any(volumes<=0) or np.any(area<=0):
        raise rs.EvidenceError('nonfinite production values or invalid physical volumes/areas')
    if np.any(rates<0) or np.any(rates[:,:,0]<=0):raise rs.EvidenceError('nonpositive production scalar flux or negative production rate')
    if np.max(abs(area-area[:,:1])/area)>64*rules['epsilon64']:
        raise rs.EvidenceError('radial face areas vary axially')
    if np.max(abs(volumes-area[:,:-1]*np.diff(z,axis=1))/volumes)>rules['physical_volume_relative_tolerance']:
        raise rs.EvidenceError('region volumes and face areas/heights disagree')
    if any(int(regions[r,k]['physical_zone'])!=(k-1)//(nz//3)+1 for r,k in regions):
        raise rs.EvidenceError('production physical-zone labels differ')
    denominator=math.fsum(rates[:,:,1].ravel())
    stated=float(summary['global_nufission'])
    if not math.isfinite(stated) or min(denominator,stated)<=0:
        raise rs.EvidenceError('nonpositive global nu-fission')
    norm_bound=gamma(nr*nz+2,rules['epsilon64'])*denominator
    if abs(denominator-stated)>norm_bound:raise rs.EvidenceError('production global normalization summary disagrees with independent sum')
    for raw,stored in [(rates[:,:,0],region_array('flux_per_global_nufission')),
                       (rates[:,:,1],region_array('nufission_fraction')),
                       (currents,face_array('current_per_global_nufission'))]:
        expected_values=raw/stated
        if not np.isfinite(stored).all() or np.any(abs(stored-expected_values)>8*rules['epsilon64']*np.maximum(abs(stored),abs(expected_values))):
            raise rs.EvidenceError('exported normalized column differs from its single global denominator')
    return dict(rates=rates,volumes=volumes,current=currents,z=expected,summary=summary,
                denominator=denominator,exporter_denominator=stated,
                normalization_difference=denominator-stated,normalization_bound=norm_bound,
                nonpositive_group_count=sum(int(row['nonpositive_group_flux_count']) for row in region_rows))


def relative_mirror_profiles(values, antisymmetric=False):
    values=np.asarray(values,dtype=float)
    residual=values+values[:,::-1] if antisymmetric else values-values[:,::-1]
    scale=abs(values).max(axis=1)
    numerator=abs(residual).max(axis=1)
    # A zero profile also has exactly zero numerator; no fitted floor is used.
    relative=np.divide(numerator,scale,out=np.zeros_like(numerator),where=scale>0)
    return dict(max_relative=float(relative.max()),per_radial_region_relative=relative.tolist(),
                per_radial_region_scale=scale.tolist(),max_absolute=float(abs(residual).max()))


def evaluate_production(production, rules):
    p=production;j=p['current'];d=p['denominator'];summary=p['summary']
    current_scale=math.fsum(abs(j).ravel())
    bound=rules['telescoping_epsilon_multiplier']*rules['epsilon64']*current_scale
    escape=math.fsum(j[:,-1])-math.fsum(j[:,0])
    divergence=math.fsum(np.diff(j,axis=1).ravel())
    reported_residual=float(summary['current_telescoping_difference'])*p['exporter_denominator']
    reported_escape=float(summary['escape_per_nufission'])*p['exporter_denominator']
    if not all(math.isfinite(x) for x in [reported_residual,reported_escape]):
        raise rs.EvidenceError('nonfinite exporter balance summary')
    balance_ok=abs(divergence-escape)<=bound and abs(reported_residual)<=bound and abs(reported_escape-escape)<=bound
    signs_ok=bool(np.all(j[:,0]<=0) and np.all(j[:,-1]>=0) and int(summary['negative_outward_end_region_group_currents'])==0)
    positivity_ok=p['nonpositive_group_count']==0 and int(summary['nonpositive_scalar_entries'])==0 and float(summary['minimum_group_scalar_flux'])>0
    sym={
        'scalar_flux':relative_mirror_profiles(p['rates'][:,:,0]/p['volumes']/d),
        'nu_fission':relative_mirror_profiles(p['rates'][:,:,1]/d),
        'net_current_plus_z':relative_mirror_profiles(j/d,antisymmetric=True)}
    symmetry_ok=all(row['max_relative']<=rules['symmetry_relative_tolerance'] for row in sym.values())
    checks=dict(production_end_current_signs='PASS' if signs_ok else 'FAIL',
                production_scalar_positivity='PASS' if positivity_ok else 'FAIL',
                production_telescoping='PASS' if balance_ok else 'FAIL',
                production_mirror_symmetry='PASS' if symmetry_ok else 'FAIL')
    return dict(checks=checks,symmetry=sym,symmetry_relative_tolerance=rules['symmetry_relative_tolerance'],
        accounting=dict(raw_telescoping_residual=divergence-escape,exporter_raw_telescoping_residual=reported_residual,
                        raw_escape_summary_difference=reported_escape-escape,roundoff_bound=bound,sum_absolute_region_face_currents=current_scale,
                        limitation=rules['full_neutron_balance']),
        normalized_net_plus_z_by_region=(j/d).tolist(),normalized_net_plus_z_full_section=(j.sum(axis=0)/d).tolist(),
        bottom_outward_per_nufission=float(-math.fsum(j[:,0])/d),top_outward_per_nufission=float(math.fsum(j[:,-1])/d),
        total_escape_per_nufission=escape/d,global_nufission=d)


def mirror_layout(contract, rules):
    cells=contract['region_layer_bins'];planes=contract['plane_bins']
    nl=len(contract['layer_bins']);nr=rules['radial_regions'];height=rules['height_cm']
    lookup={(row['region'],row['layer']):i for i,row in enumerate(cells)}
    if len(lookup)!=len(cells) or set(lookup)!={(r,l) for r in range(1,nr+1) for l in range(1,nl+1)}:
        raise rs.EvidenceError('CE mirror-cell map is incomplete or duplicated')
    if len(planes)!=nl+1 or any(row['positive_normal']!='+z' for row in planes):
        raise rs.EvidenceError('CE plane map must contain every fixed +z face')
    z=np.array([row['z_cm'] for row in planes],dtype=float)
    geom_tol=64*rules['epsilon64']*max(1,height)
    if not np.isfinite(z).all() or np.any(np.diff(z)<=0) or abs(z[0])>geom_tol or abs(z[-1]-height)>geom_tol or np.max(abs(z+z[::-1]-height))>geom_tol:
        raise rs.EvidenceError('CE face geometry is not reflection symmetric')
    pairs=[];labels=[]
    for r in range(1,nr+1):
        for l in range(1,(nl+1)//2+1):
            m=nl+1-l;a=lookup[r,l];b=lookup[r,m]
            ca,cb=cells[a],cells[b]
            if ca['composition']!=cb['composition'] or abs(ca['volume_cm3']-cb['volume_cm3'])>geom_tol*max(ca['volume_cm3'],cb['volume_cm3']):
                raise rs.EvidenceError('CE material/volume mirror mapping is asymmetric')
            pairs.append((a,b));labels.append(f'R{r}:L{l}-L{m}')
    return np.asarray(pairs),labels,z


def mirror_residual_vector(rates, volumes, currents, partials, pairs):
    flux,fission,d=rs.normalized_observables(rates,volumes)
    j=np.asarray(currents)/d[...,None];partial=np.asarray(partials)/d[...,None,None]
    count=(j.shape[-1]+1)//2
    parts=[flux[...,pairs[:,0]]-flux[...,pairs[:,1]],
           fission[...,pairs[:,0]]-fission[...,pairs[:,1]],
           (j+j[...,::-1])[...,:count],partial[...,0]+partial[...,::-1,1]]
    return np.concatenate(parts,axis=-1)


def simultaneous_centered_band(observed, replicates, rules):
    """One max statistic for the joint family, never marginal 95% intervals."""
    observed=np.asarray(observed,dtype=float);replicates=np.asarray(replicates,dtype=float)
    if replicates.ndim!=2 or replicates.shape[1:]!=observed.shape or len(replicates)<2 or not np.isfinite(replicates).all():
        raise rs.EvidenceError('invalid simultaneous bootstrap residual array')
    errors=replicates-observed
    sigma=errors.std(axis=0,ddof=1)
    nonzero=sigma>0
    maxima=np.max(abs(errors[:,nonzero])/sigma[nonzero],axis=1) if nonzero.any() else np.zeros(len(errors))
    quantile=float(np.quantile(maxima,rules['simultaneous_quantile'],method=rules['quantile_method']))
    width=quantile*sigma
    width[~nonzero]=np.max(abs(errors[:,~nonzero]),axis=0)
    lower=observed-width;upper=observed+width
    contains=(lower<=0)&(upper>=0)
    return dict(zero_vector_in_simultaneous_band=bool(contains.all()),
        critical_max_standardized_error=quantile,observed=observed.tolist(),
        lower=lower.tolist(),upper=upper.tolist(),standard_deviation=sigma.tolist(),
        outside_component_indices=np.flatnonzero(~contains).tolist(),
        family_size=len(observed),zero_variance_components=int((~nonzero).sum()),
        interpretation='Joint 95% centered block-bootstrap band conditional on observed history; not an exact finite-sample coverage guarantee or proof of source convergence.')


def evaluate_ce(batches, contract, rules):
    rates=np.asarray(batches['rates']);j=np.asarray(batches['current']);partial=np.asarray(batches['partial'])
    pairs,cell_labels,z=mirror_layout(contract,rules)
    volumes=np.array([row['volume_cm3'] for row in contract['region_layer_bins']])
    if rates.shape!=(rules['active_batches'],len(volumes),2) or j.shape!=(len(rates),len(z)) or partial.shape!=(*j.shape,2):
        raise rs.EvidenceError('CE complete formal batch/score/plane shapes required')
    if not all(np.isfinite(a).all() for a in [rates,j,partial,volumes]) or np.any(rates<0) or np.any(volumes<=0):
        raise rs.EvidenceError('nonfinite or negative CE rates/volumes')
    # Per-batch equality is stronger than checking only the final total.
    mismatch=abs(partial.sum(axis=-1)-j)
    partial_ok=bool(np.all(mismatch<=rules['independent_tally_relative_tolerance']*abs(partial).sum(axis=-1)))
    signs_ok=bool(np.all(partial[:,:,0]<=0) and np.all(partial[:,:,1]>=0) and np.all(partial[:,0,1]==0) and np.all(partial[:,-1,0]==0) and np.all(j[:,0]<=0) and np.all(j[:,-1]>=0))
    residual=np.diff(j,axis=1).sum(axis=1)-(j[:,-1]-j[:,0])
    bounds=rules['telescoping_epsilon_multiplier']*rules['epsilon64']*abs(j).sum(axis=1)
    balance_ok=bool(np.all(abs(residual)<=bounds))
    mean=rates.mean(axis=0);d=float(mean[:,1].sum())
    if d<=0 or np.any(rates[:,:,1].sum(axis=1)<=0):raise rs.EvidenceError('CE global nu-fission must be positive in every batch')
    observed=mirror_residual_vector(mean,volumes,j.mean(axis=0),partial.mean(axis=0),pairs)
    labels=[f'flux:{label}' for label in cell_labels]+[f'nu_fission:{label}' for label in cell_labels]
    labels += [f'net:F{i}+F{len(z)-1-i}' for i in range((len(z)+1)//2)]
    labels += [f'partial:negative_F{i}+positive_F{len(z)-1-i}' for i in range(len(z))]
    reports=[]
    for length in rules['block_lengths']:
        blocks=rs.contiguous_blocks(rates,length,rules['minimum_blocks'])
        samples,weights=rs.bootstrap_block_means(blocks,rules['bootstrap_replicates'],rules['bootstrap_seed']+length)
        jb=rs.contiguous_blocks(j,length,rules['minimum_blocks']);pb=rs.contiguous_blocks(partial,length,rules['minimum_blocks'])
        js=weights@jb/len(blocks)
        ps=(weights@pb.reshape(len(blocks),-1)/len(blocks)).reshape(len(samples),len(z),2)
        draws=mirror_residual_vector(samples,volumes,js,ps,pairs)
        band=simultaneous_centered_band(observed,draws,rules)
        band.update(block_length=length,blocks=len(blocks));reports.append(band)
    symmetry_ok=all(report['zero_vector_in_simultaneous_band'] for report in reports)
    checks=dict(ce_signed_partials_and_vacuum='PASS' if signs_ok else 'FAIL',
                ce_net_equals_signed_partials='PASS' if partial_ok else 'FAIL',
                ce_telescoping='PASS' if balance_ok else 'FAIL',
                ce_simultaneous_mirror_symmetry='PASS' if symmetry_ok else 'INCONCLUSIVE_SOURCE_SYMMETRY')
    net=j.mean(axis=0)/d
    return dict(checks=checks,simultaneous_family_labels=labels,block_reports=reports,
        normalized_net_plus_z_full_section=net.tolist(),
        normalized_signed_partials=(partial.mean(axis=0)/d).tolist(),directional_bin_order=['negative_z','positive_z'],
        bottom_outward_per_nufission=float(-net[0]),top_outward_per_nufission=float(net[-1]),total_escape_per_nufission=float(net[-1]-net[0]),
        z_cm=z.tolist(),global_nufission=d,max_partial_net_absolute_difference=float(mismatch.max()),
        max_raw_telescoping_residual=float(abs(residual).max()),
        full_particle_balance=rules['full_neutron_balance'])


def compare(production, batches, contract, rules):
    if contract['case'] not in rules['intended_cases'] or rules['intended_cases'][contract['case']]!=rules['intended_cases'][contract['case']][::-1]:
        raise rs.EvidenceError('case is not a declared reflection-symmetric AAA/ABA recipe')
    p=evaluate_production(production,rules);ce=evaluate_ce(batches,contract,rules)
    ce_z=np.array(ce['z_cm']);indices=[]
    tolerance=64*rules['epsilon64']*max(1,rules['height_cm'])
    for position in production['z']:
        found=np.flatnonzero(abs(ce_z-position)<=tolerance)
        if len(found)!=1:raise rs.EvidenceError('CE plane map lacks an exact production comparison face')
        indices.append(int(found[0]))
    pc=np.array(p['normalized_net_plus_z_full_section']);cc=np.array(ce['normalized_net_plus_z_full_section'])[indices]
    checks={**p['checks'],**ce['checks']}
    status='FAIL' if 'FAIL' in checks.values() else 'INCONCLUSIVE_SOURCE_SYMMETRY' if 'INCONCLUSIVE_SOURCE_SYMMETRY' in checks.values() else 'PASS'
    escape_keys=['bottom_outward_per_nufission','top_outward_per_nufission','total_escape_per_nufission']
    return dict(status=status,case=contract['case'],checks=checks,production=p,ce=ce,
        comparison=dict(report_only=True,accuracy_gate=None,z_cm=production['z'].tolist(),
            production_net_plus_z=pc.tolist(),ce_net_plus_z=cc.tolist(),signed_production_minus_ce=(pc-cc).tolist(),
            escape={key:dict(production=p[key],ce=ce[key],signed_production_minus_ce=p[key]-ce[key]) for key in escape_keys}),
        qualification_scope=rules['qualification_scope'],full_particle_balance=rules['full_neutron_balance'])


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    freeze=sub.add_parser('rules');freeze.add_argument('output',type=Path);freeze.add_argument('--case-spec',type=Path,default=rs.DEFAULT_SPEC)
    run=sub.add_parser('compare')
    for name in ['rules','statistics-rules','contract','statepoints','production-regions','production-faces','production-summary','output']:
        run.add_argument('--'+name,type=Path,required=True)
    run.add_argument('--case-spec',type=Path,default=rs.DEFAULT_SPEC)
    args=parser.parse_args()
    if args.command=='rules':rs.write_json(args.output,predeclared_rules(args.case_spec));return
    contract={};paths=[args.rules,args.statistics_rules,args.case_spec,args.contract,args.production_regions,args.production_faces,args.production_summary]
    try:
        rules=json.loads(args.rules.read_text());stats_rules=json.loads(args.statistics_rules.read_text());contract=json.loads(args.contract.read_text())
        if rules!=predeclared_rules(args.case_spec) or stats_rules!=rs.predeclared_rules(args.case_spec):
            raise rs.EvidenceError('frozen rules, implementation or case_spec identity differs')
        production=read_production(args.production_regions,args.production_faces,args.production_summary,rules)
        batches,k,sigma,history,identities=rs.extract_statepoints(args.statepoints,contract,stats_rules)
        result=compare(production,batches,contract,rules);result['statepoint_identities']=identities
    except (ValueError,OSError,KeyError) as error:
        result=dict(status='INCONCLUSIVE',reason=str(error),case=contract.get('case'))
    result['classification']='CURRENT_BALANCE_SYMMETRY_'+result['status']
    result['input_identities']={str(path):rs.digest(path) for path in paths if path.is_file()}
    result['transport_executed']=False
    rs.write_json(args.output,result)
    print(json.dumps(dict(status=result['status'],output=str(args.output))))


if __name__=='__main__':main()
