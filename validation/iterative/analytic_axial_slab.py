"""Analytic S2 slab and the unchanged signed first-order upwind discretization."""
import numpy as np
from native_axial_streaming import upwind


def validate(total,scattering,height,mu,source):
    if not (0<=scattering<=total and height>0 and 0<mu<=1 and source>0):
        raise ValueError('invalid slab coefficients or geometry')


def sinhc_minus_one(x):
    x=np.asarray(x,float);small=abs(x)<.1
    y=x*x
    series=y*(1/6+y*(1/120+y*(1/5040+y*(1/362880+y/39916800))))
    safe=np.where(small,1.,x)
    return np.where(small,series,np.sinh(x)/safe-1)


def exponential_difference(z,kappa,height):
    # Small optical thickness needs expm1; a thick interior needs the small
    # exponentials themselves, not a subtraction of two values near one.
    if kappa*height<1:
        return np.expm1(-kappa*(height-z))-np.expm1(-kappa*z)
    return np.exp(-kappa*(height-z))-np.exp(-kappa*z)


def analytic_points(z,total,scattering,height,mu,source=1.):
    """Return phi and signed current; complex z supports independent derivatives."""
    validate(total,scattering,height,mu,source)
    z=np.asarray(z);absorption=total-scattering
    if absorption==0:
        phi=source*height/(2*mu)+total*source*z*(height-z)/(2*mu**2)
        current=source*(z-height/2)
    else:
        kappa=np.sqrt(total*absorption)/mu;beta=np.sqrt(absorption/total)
        den=(1+beta)+(1-beta)*np.exp(-kappa*height)
        u=-np.expm1(-kappa*z);v=-np.expm1(-kappa*(height-z));w=-np.expm1(-kappa*height)
        # This product form avoids subtracting two almost-equal coshes.
        phi=source/absorption*(u*v+beta*w)/den
        current=source/kappa*exponential_difference(z,kappa,height)/den
    return phi,current


def analytic_cell_averages(edges,total,scattering,height,mu,source=1.):
    validate(total,scattering,height,mu,source)
    edges=np.asarray(edges,float);h=np.diff(edges);mid=(edges[:-1]+edges[1:])/2
    if np.any(h<=0) or edges[0]<0 or edges[-1]>height:raise ValueError('invalid cell edges')
    absorption=total-scattering
    if absorption==0:
        phi=source*height/(2*mu)+total*source*(mid*(height-mid)-h*h/12)/(2*mu**2)
        current=source*(mid-height/2)
    else:
        kappa=np.sqrt(total*absorption)/mu;beta=np.sqrt(absorption/total)
        den=(1+beta)+(1-beta)*np.exp(-kappa*height)
        u=-np.expm1(-kappa*mid);v=-np.expm1(-kappa*(height-mid));w=-np.expm1(-kappa*height)
        correction=sinhc_minus_one(kappa*h/2)
        exponential_sum=np.exp(-kappa*mid)+np.exp(-kappa*(height-mid))
        phi=source/absorption*(u*v+beta*w-exponential_sum*correction)/den
        current=source/kappa*exponential_difference(mid,kappa,height)*(1+correction)/den
    angular=np.stack([phi+current/mu,phi-current/mu])
    return phi,current,angular


def analytic_checks(total,scattering,height,mu,source,n):
    z=np.linspace(0,height,101);phi,current=analytic_points(z,total,scattering,height,mu,source)
    pc,jc=analytic_points(z+1j*1e-25,total,scattering,height,mu,source)
    dp=pc.imag/1e-25;dj=jc.imag/1e-25;absorption=total-scattering
    even=float(np.max(abs(dj+absorption*phi-source))/source)
    odd=float(np.max(abs(mu**2*dp+total*current))/max(source*mu,total*source*height))
    boundary=max(abs(phi[0]+current[0]/mu),abs(phi[-1]-current[-1]/mu))
    boundary/=max(float(np.max(abs(phi))),source*height/mu)
    edges=np.linspace(0,height,n+1);h=np.diff(edges)
    avg,javg,angular=analytic_cell_averages(edges,total,scattering,height,mu,source)
    escape=np.array([-current[0],current[-1]])
    global_defect=abs(source*height-absorption*np.dot(h,avg)-escape.sum())/(source*height)
    nodes,weights=np.polynomial.legendre.leggauss(32)
    points=(edges[:-1,None]+edges[1:,None])/2+h[:,None]*nodes[None,:]/2
    qp,qj=analytic_points(points,total,scattering,height,mu,source)
    qphi=qp@weights/2;qcurrent=qj@weights/2
    quadrature=max(float(np.max(abs(avg-qphi))/np.max(abs(avg))),
                   float(np.max(abs(javg-qcurrent))/max(float(np.max(abs(javg))),source*height)))
    row=dict(even_identity_relative=even,odd_identity_relative=odd,boundary_relative=float(boundary),
             global_balance_relative=float(global_defect),cell_quadrature_relative=quadrature,
             minimum_analytic_cell_angular=float(angular.min()))
    return row,dict(reference_phi=avg,reference_current=javg,reference_angular=angular,
                    reference_escape=escape,reference_face_current=analytic_points(edges,total,scattering,height,mu,source)[1])


def discrete_slab(total,scattering,height,mu,source,n):
    validate(total,scattering,height,mu,source)
    if n<1:raise ValueError('positive number of cells required')
    h=height/n;identity=np.eye(n)
    plus=mu*upwind([h]*n,1)+(total-scattering/2)*identity
    minus=mu*upwind([h]*n,-1)+(total-scattering/2)*identity
    matrix=np.block([[plus,-scattering/2*identity],[-scattering/2*identity,minus]])
    rhs=np.full(2*n,source);solution=np.linalg.solve(matrix,rhs);angular=solution.reshape(2,n)
    phi=angular.sum(axis=0)/2;current=mu*(angular[0]-angular[1])/2
    fp=np.r_[0.,angular[0]];fm=np.r_[angular[1],0.]
    face_current=mu*(fp-fm)/2;face_second=mu**2*(fp+fm)/2
    even_cell=np.diff(face_current)+(total-scattering)*h*phi-source*h
    odd_cell=np.diff(face_second)+total*h*current
    incoming_scale=source*h+mu*(fp[:-1]+fm[1:])/2
    even_relative=abs(even_cell)/incoming_scale
    odd_relative=abs(odd_cell)/(mu*incoming_scale)
    escape=np.array([-face_current[0],face_current[-1]])
    matrix_residual=matrix@solution-rhs
    row=dict(matrix_residual_relative=float(np.max(abs(matrix_residual))/source),
             raw_global_balance_relative=float(abs(escape.sum()+(total-scattering)*h*phi.sum()-source*height)/(source*height)),
             even_cell_balance_relative=float(even_relative.max()),odd_cell_balance_relative=float(odd_relative.max()),
             minimum_angular=float(angular.min()),escape=escape.tolist(),total_escape=float(escape.sum()))
    fields=dict(matrix=matrix,edges=np.linspace(0,height,n+1),angular=angular,phi=phi,current=current,
                face_current=face_current,face_second_moment=face_second,escape=escape,
                matrix_residual=matrix_residual,even_cell_defect=even_cell,odd_cell_defect=odd_cell)
    return row,fields


def relative_l2(value,reference,widths,angular=False):
    weight=np.asarray(widths)*(0.5 if angular else 1.)
    return float(np.sqrt(np.sum(weight*(value-reference)**2)/np.sum(weight*reference**2)))


def errors_against_reference(fields):
    h=np.diff(fields['edges'])
    return dict(scalar_true_relative=relative_l2(fields['phi'],fields['reference_phi'],h),
        angular_true_relative=relative_l2(fields['angular'],fields['reference_angular'],h,True),
        current_true_relative=relative_l2(fields['current'],fields['reference_current'],h),
        escape_true_relative=(abs(fields['escape']-fields['reference_escape'])/fields['reference_escape']).tolist(),
        total_escape_true_relative=float(abs(fields['escape'].sum()-fields['reference_escape'].sum())/fields['reference_escape'].sum()))


def adjacent_errors(coarse,fine):
    n=len(coarse['phi'])
    if len(fine['phi'])!=2*n:raise ValueError('factor-two nested mesh required')
    rp=fine['phi'].reshape(n,2).mean(axis=1)
    ra=fine['angular'].reshape(2,n,2).mean(axis=2)
    return dict(scalar_adjacent_relative=relative_l2(coarse['phi'],rp,np.diff(coarse['edges'])),
        angular_adjacent_relative=relative_l2(coarse['angular'],ra,np.diff(coarse['edges']),True),
        escape_adjacent_relative=(abs(coarse['escape']-fine['escape'])/fine['escape']).tolist(),
        total_escape_adjacent_relative=float(abs(coarse['escape'].sum()-fine['escape'].sum())/fine['escape'].sum()))
