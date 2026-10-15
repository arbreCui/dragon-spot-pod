#!/usr/bin/env python3
"""Seal numerical conclusions only after independent reference/POD controls."""
import argparse
import json
from pathlib import Path
import numpy as np
from qualify_native_axial_coupling import fission_data,save


def main(artifact):
    a=Path(artifact);plan=json.loads((a/'plan.json').read_text())
    refs=[json.loads((a/f'analysis/reference_{n}.json').read_text()) for n in plan['meshes_cm']]
    rows=[json.loads(p.read_text()) for p in sorted((a/'analysis').glob('pod_*.json'))]
    assert all(r['admitted'] for r in refs), 'current report expects all three reference cases admitted'
    assert len(rows)==48
    assert max(r['projected_angular_residual_relative'] for r in rows)<plan['thresholds']['equation_residual']
    assert max(r['relative_flux_l2'] for r in rows if r['rank']==8)<plan['thresholds']['full_rank_recovery']
    assert max(abs(r['k']/next(ref['k'] for ref in refs if ref['name']==r['name'])-1)
               for r in rows if r['rank']==8)<plan['thresholds']['full_rank_recovery']
    assert max(r.get('oblique_flux_difference',0) for r in rows)<plan['thresholds']['full_rank_recovery']
    assert max(r.get('oblique_k_difference',0) for r in rows)<plan['thresholds']['full_rank_recovery']
    conditioning=[json.loads((a/f'analysis/invertibility_{n}.json').read_text()) for n in plan['meshes_cm']]
    nuf,chi=fission_data(a/'analysis/fission.bin');active=np.any(nuf>0,axis=0)
    table=[];negative_locations=[]
    for family in ['plain','enriched']:
        for rank in range(1,9):
            cases=[r for r in rows if r['family']==family and r['rank']==rank]
            table.append({'family':family,'rank':rank,
                          'max_relative_flux_error':max(r['relative_flux_l2'] for r in cases),
                          'max_abs_delta_rho_pcm':max(abs(r['delta_rho_pcm']) for r in cases),
                          'negative_scalar_cases':sum(r['negative_scalar_count']>0 for r in cases),
                          'negative_angular_cases':sum(r['negative_angular_count']>0 for r in cases)})
    for r in rows:
        fields=np.load(a/f"analysis/pod_{r['name']}_{r['family']}_{r['rank']}.npz")
        phi,faces=fields['phi'],fields['faces']
        assert np.sum(phi<0)==r['negative_scalar_count']
        assert np.sum(faces<0)==r['negative_angular_count']
        if np.any(faces<0):
            loc=np.unravel_index(np.argmin(faces),faces.shape)
            negative_locations.append({'case':r['name'],'family':r['family'],'rank':r['rank'],
                                       'worst_face_group':int(loc[0]+1),'direction':['plus','minus'][loc[1]],
                                       'cell':int(loc[2]+1),'region':int(loc[3]+1),'value':float(faces[loc]),
                                       'negative_groups':(np.unique(np.where(faces<0)[0])+1).tolist(),
                                       'negative_regions':(np.unique(np.where(faces<0)[3])+1).tolist()})
    result={'scope':plan['scope'],'references':refs,'conditioning':conditioning,'rank_table':table,
            'active_fission_components':int(active.sum()),'chi_active_sum_min':float(chi.sum(axis=0)[active].min()),
            'chi_active_sum_max':float(chi.sum(axis=0)[active].max()),
            'negative_scalar_cases':sum(r['negative_scalar_count']>0 for r in rows),
            'negative_angular_cases':sum(r['negative_angular_count']>0 for r in rows),
            'negative_face_locations':negative_locations,
            'max_full_rank_flux_error':max(r['relative_flux_l2'] for r in rows if r['rank']==8),
            'max_projected_angular_residual':max(r['projected_angular_residual_relative'] for r in rows),
            'max_oblique_flux_difference':max(r.get('oblique_flux_difference',0) for r in rows),
            'max_enriched_weighted_residual':max(abs(r['weighted_angular_residual']) for r in rows if r['family']=='enriched'),
            'max_balance_identity_error':max(abs(r['balance_identity_error']) for r in rows),
            'max_enriched_abs_raw_balance_relative':max(abs(r['raw_balance_relative_to_birth']) for r in rows if r['family']=='enriched'),
            'max_plain_abs_raw_balance_relative':max(abs(r['raw_balance_relative_to_birth']) for r in rows if r['family']=='plain')}
    save(a/'analysis/result.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['references','rank_table','negative_face_locations']},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);main(p.parse_args().artifact)
