#!/usr/bin/env python3
"""Exact nodal reformulation of the frozen S2-DD candidate, without truncation.

Nodal scalar f obeys (L*D + M*K + vacuum) f = rho M*F f. The midpoint
element mass is singular in its alternating mode; do not lump or invert it.
Simultaneous diagonalization is only a full-space removal preconditioner.
"""
from __future__ import annotations
import argparse
import json
import time
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import eigh,lu_factor,lu_solve
from scipy.sparse import csc_matrix,diags
from scipy.sparse.linalg import LinearOperator,gmres,eigs,splu
from qualify_native_multigroup_pod import load_data,full_operator
from qualify_native_axial_coupling import MU,fission_data,diagnostics,save


def axial_elements(heights):
    h=np.asarray(heights,dtype=float)
    if h.ndim!=1 or len(h)==0 or np.any(h<=0) or not np.isfinite(h).all():
        raise ValueError('positive finite axial cell heights required')
    n=len(h)+1;m=np.zeros((n,n));l=np.zeros((n,n))
    for z,hz in enumerate(h):
        m[z:z+2,z:z+2]+=hz/4*np.ones((2,2))
        l[z:z+2,z:z+2]+=np.array([[1.,-1.],[-1.,1.]])/hz
    return m,l


def energy_fission(nuf,chi):
    ng,nr,_=nuf.shape
    f=np.zeros((ng,nr,ng,nr))
    for i in range(nr):f[:,i,:,i]=chi[:,i,:]@nuf[:,i,:].T
    return csc_matrix(f.reshape(ng*nr,ng*nr))


class NodalProblem:
    def __init__(self,total,scatter,loss,nuf,chi,volume,heights,controls):
        self.total=total;self.scatter=scatter;self.loss=loss;self.nuf=nuf;self.chi=chi
        self.volume=volume;self.heights=np.array(heights);self.controls=controls
        self.ng,self.nr=total.shape;self.ne=total.size;self.nn=len(heights)+1
        self.m,self.l=axial_elements(heights)
        self.k=csc_matrix(full_operator(loss,scatter));self.f=energy_fission(nuf,chi)
        self.d=MU**2/total.ravel();self.shape=(self.nn*self.ne,)*2
        self.inverse_calls=0;self.inner_iterations=[];self.inner_residuals=[]
        self.preconditioner_calls=0
        # Every spatial mode is retained, including the singular-mass mode.
        self.preconditioner_alpha=1.0  # cm^-1; only the preconditioner is changed.
        robin=self.l.copy();robin[0,0]+=self.preconditioner_alpha;robin[-1,-1]+=self.preconditioner_alpha
        _,self.q=eigh(robin,self.m+robin)
        self.ell=np.sum(np.diff(self.q,axis=0)**2/self.heights[:,None],axis=0)
        self.ell+=self.preconditioner_alpha*(self.q[0]**2+self.q[-1]**2)
        self.mass=np.sum((self.q[:-1]+self.q[1:])**2*self.heights[:,None]/4,axis=0)
        self.factors=[splu(csc_matrix(m*self.k+diags(l*self.d))) for m,l in zip(self.mass,self.ell)]
        # Eliminate the two-end difference from the separable Robin operator.
        # Boundary matrices are full energy-region operators, without rank truncation.
        g00=np.zeros((self.ne,self.ne));g01=np.zeros_like(g00);g11=np.zeros_like(g00)
        eye=np.eye(self.ne)
        for j,factor in enumerate(self.factors):
            inv=factor.solve(eye)
            g00+=self.q[0,j]**2*inv;g01+=self.q[0,j]*self.q[-1,j]*inv
            g11+=self.q[-1,j]**2*inv
        self.boundary_delta=MU-self.preconditioner_alpha*self.d
        self.symmetric_mesh=bool(np.all(self.heights==self.heights[0]))
        if self.symmetric_mesh:
            self.boundary_factors=[lu_factor(eye+(g00+g01)*self.boundary_delta),
                                   lu_factor(eye+(g00-g01)*self.boundary_delta)]
        else:
            self.boundary_factors=[lu_factor(np.block([
                [eye+g00*self.boundary_delta,g01*self.boundary_delta],
                [g01*self.boundary_delta,eye+g11*self.boundary_delta]]))]
        self.aop=LinearOperator(self.shape,matvec=self.removal,dtype=float)
        self.preop=LinearOperator(self.shape,matvec=self.precondition,dtype=float)

    def removal(self,x):
        field=np.asarray(x).reshape(self.nn,self.ne)
        y=self.m@(self.k@field.T).T+self.l@(field*self.d)
        y[[0,-1]]+=MU*field[[0,-1]]
        return y.ravel()

    def birth(self,x):
        return (self.m@(self.f@np.asarray(x).reshape(self.nn,self.ne).T).T).ravel()

    def base_precondition(self,x):
        rhs=self.q.T@np.asarray(x).reshape(self.nn,self.ne)
        modes=np.stack([factor.solve(row) for factor,row in zip(self.factors,rhs)])
        return (self.q@modes).ravel()

    def precondition(self,x):
        self.preconditioner_calls+=1
        base=self.base_precondition(x).reshape(self.nn,self.ne)
        if self.symmetric_mesh:
            plus=lu_solve(self.boundary_factors[0],(base[0]+base[-1])/2)
            minus=lu_solve(self.boundary_factors[1],(base[0]-base[-1])/2)
            boundary=np.stack([plus+minus,plus-minus])
        else:
            boundary=lu_solve(self.boundary_factors[0],base[[0,-1]].ravel()).reshape(2,self.ne)
        correction=np.zeros_like(base);correction[[0,-1]]=boundary*self.boundary_delta
        return base.ravel()-self.base_precondition(correction)

    def inverse(self,rhs):
        self.inverse_calls+=1;iterations=[]
        sol,info=gmres(self.aop,rhs,M=self.preop,rtol=self.controls['inner_rtol'],atol=0.,
                       restart=self.controls['inner_restart'],maxiter=self.controls['inner_restart_cycles'],
                       callback=iterations.append,callback_type='pr_norm')
        residual=float(np.linalg.norm(self.removal(sol)-rhs)/np.linalg.norm(rhs))
        self.inner_iterations.append(len(iterations));self.inner_residuals.append(residual)
        if info!=0:raise RuntimeError(f'removal GMRES failed: info={info}, residual={residual}')
        return sol

    def normalize(self,nodal):
        cell=(nodal[:-1]+nodal[1:])/2
        nf=self.nuf.sum(axis=2).ravel()
        integral=np.sum(cell*nf*np.tile(self.volume,self.ng)*self.heights[:,None])
        if not np.isfinite(integral) or abs(integral)<np.finfo(float).tiny:
            raise ValueError('vanishing fission normalization')
        return nodal/integral

    def fields(self,nodal,k):
        cell=(nodal[:-1]+nodal[1:])/2
        removal=(self.k@cell.T-self.f@cell.T/k).T
        javg=-self.d*(nodal[1:]-nodal[:-1])/self.heights[:,None]
        jleft=javg+self.heights[:,None]*removal/2
        jright=javg-self.heights[:,None]*removal/2
        plus=(nodal[1:]+jright/MU)/2
        minus=(nodal[:-1]-jleft/MU)/2
        phi=cell.reshape(len(self.heights),self.ng,self.nr).transpose(1,0,2)
        faces=np.stack([plus,minus]).reshape(2,len(self.heights),self.ng,self.nr).transpose(2,0,1,3)
        continuity=float(np.max(abs(jright[:-1]-jleft[1:]))) if len(self.heights)>1 else 0.
        vacuum=float(max(np.max(abs(jleft[0]+MU*nodal[0])),np.max(abs(jright[-1]-MU*nodal[-1]))))
        return phi,faces,{'internal_current_mismatch':continuity,'vacuum_moment_residual':vacuum}

    def solve(self):
        op=LinearOperator(self.shape,matvec=lambda x:self.inverse(self.birth(x)),dtype=float)
        solutions=[];records=[]
        for label,seed in [('uniform',np.ones(self.shape[0])),('ramp',np.linspace(1.,2.,self.shape[0]))]:
            vals,vecs=eigs(op,k=self.controls['eigen_modes'],which='LM',v0=seed,
                           tol=self.controls['eigen_tolerance'],maxiter=self.controls['eigen_maxiter'])
            j=int(np.argmax(vals.real));value=vals[j]
            if value.real<=0 or abs(value.imag)>1e-11*abs(value.real):
                raise ValueError('leading mode is not positive real')
            if abs(value)<max(abs(vals))*(1-1e-10):raise ValueError('leading mode is not dominant magnitude')
            field=self.normalize(vecs[:,j].real.reshape(self.nn,self.ne));k=float(value.real)
            residual=self.removal(field)-self.birth(field)/k
            records.append({'start':label,'k':k,'rho':1/k,
                            'ritz_values':[[float(v.real),float(v.imag)] for v in vals],
                            'relative_spectral_separation':float(min(abs(np.delete(vals,j)-value))/abs(value)),
                            'nodal_equation_residual_relative':float(np.linalg.norm(residual)/np.linalg.norm(self.birth(field)/k))})
            solutions.append(field)
        nodal=solutions[0];k=records[0]['k'];phi,faces,current=self.fields(nodal,k)
        identity=np.broadcast_to(np.eye(self.nr),(self.ng,self.nr,self.nr))
        closure=self.loss.copy()
        for g in range(self.ng):closure[g]-=np.diag(self.total[g])
        result=diagnostics(self.total,self.scatter,closure,self.nuf,self.chi,self.volume,identity,self.heights,phi,faces,k)
        result.update(current)
        result.update(k=k,rho=1/k,starts=records,
                      initial_flux_difference=float(np.linalg.norm(solutions[0]-solutions[1])/np.linalg.norm(solutions[0])),
                      initial_k_difference=abs(records[0]['k']/records[1]['k']-1),
                      inverse_calls=self.inverse_calls,max_inner_iterations=max(self.inner_iterations),
                      max_inner_relative_residual=max(self.inner_residuals),
                      total_inner_iterations=sum(self.inner_iterations),preconditioner_calls=self.preconditioner_calls,
                      spatial_modes=self.nn,sparse_factor_nonzeros=sum(f.L.nnz+f.U.nnz for f in self.factors),
                      simultaneous_diagonalization_error=float(np.max(abs(self.q.T@self.m@self.q-np.diag(self.mass)))))
        failures=[]
        for key,limit in [('full_angular_residual_relative','full_angular_residual_relative'),
                          ('initial_flux_difference','initial_solution_agreement'),
                          ('initial_k_difference','initial_solution_agreement')]:
            if result[key]>self.controls[limit]:failures.append(key)
        if any(r['nodal_equation_residual_relative']>self.controls['eigen_residual_relative'] for r in records):
            failures.append('nodal_equation_residual_relative')
        if abs(result['global_nufission']-1)>1e-10:failures.append('normalization')
        if result['minimum_scalar_flux']<=0:failures.append('nonpositive_scalar_flux')
        if result['minimum_outgoing_angular_flux']<=0:failures.append('nonpositive_outgoing_angles')
        if abs(result['raw_balance_relative_to_birth'])>self.controls['raw_balance_relative_to_birth']:failures.append('raw_balance')
        result.update(failed_gates=failures,admitted=not failures)
        return result,phi,faces,nodal


def load_problem(a,heights):
    d=load_data(a/'inputs/multigroup_data.bin')
    for g in range(370):d['scatter'][g,g]=d['physical_r'][g]
    loss=np.load(a/'inputs/operator_fields.npz')['loss'];nuf,chi=fission_data(a/'inputs/fission.bin')
    plan=json.loads((a/'plan.json').read_text())
    return NodalProblem(d['total_r'],d['scatter'],loss,nuf,chi,d['v'],heights,plan['numerical_controls'])


def main(artifact,case):
    a=Path(artifact);plan=json.loads((a/'plan.json').read_text());start=time.monotonic()
    if case in plan['calibration']:heights=plan['calibration'][case]
    else:
        n=int(case)
        if n not in plan['meshes']:raise ValueError('mesh is not predeclared')
        heights=[plan['height_cm']/n]*n
    problem=load_problem(a,heights);result,phi,faces,nodal=problem.solve()
    result.update(case=case,heights_cm=heights,numpy_version=np.__version__,scipy_version=scipy.__version__)
    if case in plan['calibration']:
        ref=json.loads((a/f'inputs/reference_{case}.json').read_text())
        fields=np.load(a/f'inputs/reference_{case}.npz');w=np.array(heights)[None,:,None]*problem.volume
        result['calibration_relative_k']=abs(result['k']/ref['k']-1)
        result['calibration_relative_phi']=float(np.sqrt(np.sum(w*(phi-fields['phi'])**2)/np.sum(w*fields['phi']**2)))
        result['calibration_relative_faces']=float(np.linalg.norm(faces-fields['faces'])/np.linalg.norm(fields['faces']))
        if max(result[k] for k in ['calibration_relative_k','calibration_relative_phi','calibration_relative_faces'])>plan['numerical_controls']['calibration_relative']:
            raise RuntimeError('dense-to-nodal calibration failed')
    save(a/f'analysis/case_{case}.json',result)
    np.savez_compressed(a/f'analysis/case_{case}.npz',phi=phi,faces=faces,nodal=nodal)
    print(json.dumps(result),flush=True)
    print(f'elapsed_seconds={time.monotonic()-start:.3f}',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);p.add_argument('case')
    args=p.parse_args();main(args.artifact,args.case)
