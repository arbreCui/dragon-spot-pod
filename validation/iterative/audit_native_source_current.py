#!/usr/bin/env python3
"""Signed source/current identities and the limits of a steady scalar inverse.

No eigenproblem is solved and no transport coefficient is changed. A native
steady response is not assumed to be an angular propagation generator.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from qualify_native_multigroup_pod import load_data
from qualify_native_axial_coupling import MU,fission_data,save


def angular_moments(faces,heights):
    h=np.asarray(heights)[None,:,None]
    incoming=np.zeros_like(faces)
    incoming[:,0,1:]=faces[:,0,:-1];incoming[:,1,:-1]=faces[:,1,1:]
    averages=(incoming+faces)/2
    scalar=averages[:,0]+averages[:,1]
    current=MU*(averages[:,0]-averages[:,1])
    divergence=MU*np.sum(faces-incoming,axis=1)/h
    return scalar,current,divergence,incoming


def weighted_norm(x,weights):
    return float(np.sqrt(np.sum(weights*x*x)))


def scalar_generator_audit(h,response,weights,total,steps):
    ng,nr,_=h.shape;identity=np.eye(nr);off=~np.eye(nr,dtype=bool)
    exponential=np.empty((len(steps),ng,nr,nr));implicit=np.empty_like(exponential)
    rows=[]
    for g in range(ng):
        norm=float(np.linalg.norm(h[g],np.inf))
        pos=np.where(off,h[g],-np.inf);i,j=np.unravel_index(np.argmax(pos),pos.shape)
        maximum=float(pos[i,j]);ratio=max(maximum,0.)/norm
        row={'group':g+1,'steady_response_minimum':float(response[g].min()),
             'positive_offdiagonal_count':int(np.sum(h[g][off]>0)),
             'significant_positive_offdiagonal_count':int(np.sum(h[g][off]>1e-12*norm)),
             'largest_positive_offdiagonal':maximum,'scaled_positive_offdiagonal':ratio,
             'target_region':int(i+1),'input_region':int(j+1),'steps':[]}
        # A finite Taylor/Neumann bound supplements the derivative argument.
        if ratio>0:
            theta=min(1e-6,ratio/4);tau=theta/norm
            exact=expm(-tau*h[g]);euler=np.linalg.solve(identity+tau*h[g],identity)
            first=-theta*ratio
            exp_tail=.5*theta**2*np.exp(theta)
            inv_tail=theta**2/(1-theta)
            row['certified_witness']={'theta':theta,'tau_cm':tau,'axial_step_cm':MU*tau,
                                      'first_order_entry':first,'exponential_upper_bound':first+exp_tail,
                                      'implicit_upper_bound':first+inv_tail,
                                      'exponential_entry':float(exact[i,j]),'implicit_entry':float(euler[i,j])}
            assert first+exp_tail<0 and first+inv_tail<0
            assert exact[i,j]<0 and euler[i,j]<0
        c=h[g]-np.diag(total[g])
        row['weighted_radial_column_defect']=float(np.max(abs(weights@c)))
        row['weighted_radial_column_defect_scaled']=float(np.max(abs(weights@c)/(weights@abs(h[g])+weights*abs(total[g]))))
        for t,theta in enumerate(steps):
            tau=theta/norm
            exponential[t,g]=expm(-tau*h[g])
            implicit[t,g]=np.linalg.solve(identity+tau*h[g],identity)
            row['steps'].append({'theta':theta,'tau_cm':tau,'axial_step_cm':MU*tau,
                                 'exact_minimum':float(exponential[t,g].min()),
                                 'exact_negative_entries':int(np.sum(exponential[t,g]<0)),
                                 'implicit_minimum':float(implicit[t,g].min()),
                                 'implicit_negative_entries':int(np.sum(implicit[t,g]<0))})
        rows.append(row)
    return rows,exponential,implicit


def conservative_counterexample():
    r=np.array([[1.,.3,.01],[.3,1.,.3],[.01,.3,1.]])
    h=np.linalg.solve(r,np.eye(3));total=h@np.ones(3);c=h-np.diag(total)
    audit,exact,euler=scalar_generator_audit(h[None],r[None],np.ones(3),total[None],[1e-6,1e-3,.1,1.])
    return {'steady_response':r.tolist(),'inverse':h.tolist(),'positive_total':total.tolist(),
            'closure':c.tolist(),'constant_radial_action':(c@np.ones(3)).tolist(),
            'column_balance_defect':(np.ones(3)@c).tolist(),'audit':audit[0]}


def case_audit(data,operator,nuf,chi,record,fields):
    phi=fields['phi'];faces=fields['faces'];h=np.array(record['heights_cm']);ng,nz,nr=phi.shape
    total=data['total_r'];w=h[None,:,None]*data['v'];rho=1/record['k']
    scalar,current,div,incoming=angular_moments(faces,h)
    p=np.einsum('ghi,hzi->gzi',data['scatter'],phi,optimize=True)
    p+=rho*np.einsum('gic,zic->gzi',chi,np.einsum('gic,gzi->zic',nuf,phi,optimize=True),optimize=True)
    hphi=np.einsum('gij,gzj->gzi',operator['loss'],phi,optimize=True)
    radial=hphi-total[:,None,:]*phi
    inferred=p-div
    qangle=p-radial
    nodal=fields['nodal'].reshape(nz+1,ng,nr).transpose(1,0,2)
    face_scalar_left=incoming[:,0]+faces[:,1]
    face_scalar_right=faces[:,0]+incoming[:,1]
    current_left=MU*(incoming[:,0]-faces[:,1])
    current_right=MU*(faces[:,0]-incoming[:,1])
    net_axial=float(np.sum(data['v']*(current_right[:,-1]-current_left[:,0])))
    grad=np.diff(nodal,axis=1)/h[None,:,None]
    collision_current=total[:,None,:]*current
    hcurrent=np.einsum('gij,gzj->gzi',operator['loss'],current,optimize=True)
    odd_base=MU**2*grad+collision_current
    cj=hcurrent-collision_current
    source_scale=max(float(np.max(abs(p))),np.finfo(float).tiny)
    current_scale=max(float(np.max(abs(total[:,None,:]*phi*MU))),np.finfo(float).tiny)
    # Use p-div independently of H*phi for the raw-flight matrix replay.
    outgoing=np.einsum('gsi,gzi->gzs',operator['outgoing'],inferred,optimize=True)
    source=np.concatenate([inferred,outgoing],axis=2)  # Stored return is identity/white.
    prediction=np.einsum('gab,gzb->gza',operator['flight'],source,optimize=True)
    surface=data['weights'][nr:]
    raw_defect=np.einsum('i,gzi->gz',data['v'],inferred-total[:,None,:]*prediction[:,:,:nr])
    raw_defect+=np.einsum('s,gzs->gz',surface,outgoing-prediction[:,:,nr:])
    birth=rho*float(np.sum(w*np.einsum('gic,zic->gzi',chi,np.einsum('gic,gzi->zic',nuf,phi,optimize=True),optimize=True)))
    cn=weighted_norm(collision_current,w);reference_scale=weighted_norm(total[:,None,:]*phi*MU,w)
    odd_ratio=weighted_norm(cj,w)/cn if cn>1e-12*reference_scale else None
    plus_radial=radial/2+cj/(2*MU);minus_radial=radial/2-cj/(2*MU)
    result={'cells':nz,'k':record['k'],
            'scalar_face_consistency_relative':float(np.max(abs(scalar-phi))/np.max(abs(phi))),
            'nodal_angular_face_consistency_relative':float(max(np.max(abs(face_scalar_left-nodal[:,:-1])),
                                                               np.max(abs(face_scalar_right-nodal[:,1:])))/np.max(abs(phi))),
            'axial_net_current':net_axial,'axial_telescope_error':float(np.sum(w*div)-net_axial),
            'even_moment_residual_relative':float(np.max(abs(div+hphi-p))/source_scale),
            'odd_moment_residual_scaled':float(np.max(abs(odd_base))/current_scale),
            'odd_directionwise_lift_defect_relative_l2':odd_ratio,
            'odd_directionwise_lift_defect_absolute_l2':weighted_norm(cj,w),
            'source_negative_counts':{'scattering_plus_fission':int(np.sum(p<0)),
                                      'inferred_radial_p_minus_divJ':int(np.sum(inferred<0)),
                                      'effective_axial_p_minus_Cphi':int(np.sum(qangle<0))},
            'native_replayed_scalar_relative_l2':weighted_norm(prediction[:,:,:nr]-phi,w)/weighted_norm(phi,w),
            'native_replayed_boundary_relative':float(np.max(abs(prediction[:,:,nr:]-outgoing))/np.max(abs(outgoing))),
            'native_inferred_radial_outgoing_negative_count':int(np.sum(outgoing<0)),
            'white_boundary_net_current':0.,
            'native_integrated_raw_flight_defect_relative_to_birth':float(np.sum(raw_defect*h)/birth),
            'candidate_integrated_radial_defect_relative_to_birth':float(np.sum(w*radial)/birth),
            'radial_odd_split_sum_error':float(np.max(abs(plus_radial+minus_radial-radial))),
            'raw_flight_boundary_net_current_from_output':float(np.sum(h*np.einsum('s,gzs->gz',surface,prediction[:,:,nr:]-outgoing)))}
    arrays=dict(phi=phi,scalar_from_faces=scalar,current=current,divergence=div,
                physical_scattering_fission_source=p,inferred_radial_source=inferred,
                radial_source_from_inverse=hphi,effective_axial_source=qangle,radial_term=radial,
                odd_base_residual=odd_base,odd_directionwise_extra=cj,
                native_boundary_outgoing=outgoing,native_replayed_field=prediction,
                directionwise_radial_plus=plus_radial,directionwise_radial_minus=minus_radial)
    return result,arrays


def main(artifact):
    a=Path(artifact);plan=json.loads((a/'plan.json').read_text());data=load_data(a/'inputs/multigroup_data.bin')
    for g in range(370):data['scatter'][g,g]=data['physical_r'][g]
    nuf,chi=fission_data(a/'inputs/fission.bin');operator=dict(np.load(a/'inputs/operator_fields.npz'))
    rows,exponential,implicit=scalar_generator_audit(operator['loss'],operator['response'],data['v'],data['total_r'],plan['dimensionless_propagation_steps'])
    save(a/'analysis/generator_audit.json',rows)
    np.savez_compressed(a/'analysis/generator_fields.npz',exponential=exponential,implicit=implicit)
    toy=conservative_counterexample();save(a/'analysis/conservative_counterexample.json',toy)
    assert max(abs(x) for x in toy['column_balance_defect'])<plan['thresholds']['toy_exact_conservation_absolute']
    cases=[]
    for n in plan['meshes']:
        label={1:'one_cell',2:'two_equal'}.get(n,str(n))
        record=json.loads((a/f'inputs/case_{label}.json').read_text());fields=np.load(a/f'inputs/case_{label}.npz')
        result,arrays=case_audit(data,operator,nuf,chi,record,fields);cases.append(result)
        save(a/f'analysis/current_{n}.json',result)
        np.savez_compressed(a/f'analysis/current_{n}.npz',**arrays)
        print(json.dumps(result),flush=True)
    thresholds=plan['thresholds'];controls=['scalar_face_consistency_relative','nodal_angular_face_consistency_relative','even_moment_residual_relative',
                                          'odd_moment_residual_scaled','native_replayed_scalar_relative_l2','native_replayed_boundary_relative']
    for key in controls:assert max(c[key] for c in cases)<thresholds['moment_and_native_action_relative'],key
    summary={'scope':plan['scope'],'cases':cases,'native_groups':370,
             'groups_with_positive_offdiagonal_inverse':sum(r['positive_offdiagonal_count']>0 for r in rows),
             'groups_with_significant_positive_offdiagonal_inverse':sum(r['significant_positive_offdiagonal_count']>0 for r in rows),
             'total_positive_offdiagonal_entries':sum(r['positive_offdiagonal_count'] for r in rows),
             'minimum_native_steady_response':min(r['steady_response_minimum'] for r in rows),
             'groups_with_certified_negative_propagation':sum('certified_witness' in r for r in rows),
             'worst_scaled_radial_column_defect':max(r['weighted_radial_column_defect_scaled'] for r in rows),
             'step_results':[{'theta':theta,
                              'exact_negative_groups':int(np.sum(np.any(exponential[i]<0,axis=(1,2)))),
                              'implicit_negative_groups':int(np.sum(np.any(implicit[i]<0,axis=(1,2)))),
                              'exact_minimum':float(exponential[i].min()),'implicit_minimum':float(implicit[i].min())}
                             for i,theta in enumerate(plan['dimensionless_propagation_steps'])],
             'identity_checks_passed':True,'directionwise_H_lift_has_positivity_guarantee':False}
    save(a/'analysis/result.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k!='cases'},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);main(p.parse_args().artifact)
