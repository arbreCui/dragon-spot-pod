"""Read-only reproduction of Fe56 negative P0 entries; no library/solver writes."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import runpy
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'validation/artifacts'
RUN=A/'d4a-fe56-ganlib-tone650-run-20260929'
PAIR=A/'d4a-fe56-mt51-control-candidate-20260929'
OLD=A/'d4a-fe56-library-path-audit-20260929'
F=np.float32

def weights(temperatures, temperature, order=3):
    """LIBLEX positive-NOTX arithmetic, including its existing node recognition."""
    t=np.asarray(temperatures,dtype=F); q=F(temperature); n=len(t)
    assert n>=order+1 and order in (1,3) and np.all(np.diff(t)>0)
    i1,i2=1,n; w=np.zeros(n,dtype=np.float64)
    for i,node in enumerate(t,1):
        if q==node:w[i-1]=1.;return w.astype(F)
        if q>node:i1=max(i-(order-1)//2,i1)
        else:i2=min(i+(order-1)//2,i2)
    if i1==1:i2=min(n,order+1)
    elif i2==n:i1=max(1,n-order)
    x=np.sqrt(t).astype(np.float64); xx=float(np.sqrt(q)); factor=1.
    for i in range(i1-1,i2):
        if abs(F(q-t[i]))<=F(F(1e-5)*abs(q)):w[i]=1.;return w.astype(F)
        factor*=xx-x[i]
    for i in range(i1-1,i2):
        term=factor/(xx-x[i])
        for j in range(i1-1,i2):
            if i!=j:term/=x[i]-x[j]
        w[i]=term
    return w.astype(F)

def mix_nodes(nodes,w):
    out=np.zeros_like(nodes[0],dtype=F)
    for coefficient,node in zip(w,nodes):
        out=(out+coefficient*node).astype(F)
    return out

def audit():
    api=runpy.run_path(str(RUN/'run_once.py'),run_name='read_only')
    sha,verify,decode,nr=api['sha'],api['verify'],api['decode'],api['nr']
    pins={}
    for directory,digest in ((RUN,'26770010b089c335a791499e4353b7443c6c3c8b9ac5e5b70a53403e2e330b5f'),
                            (PAIR,'a81fb4504793e40d86567ba70b4c13c30d5093bd5a79b5ebc132ce52af586843'),
                            (OLD,'eb3dd8a0a26a1f278d8f1ec4117d2adb7253b72343f618081aefd710857bd0cc')):
        assert sha(directory/'result.sha256')==digest
        pins[str(directory/'result.sha256')]=digest
        names=['run_once.py','material/metadata.ascii','material/fe56_aim1.ascii','material/fe56_em10.ascii'] if directory==RUN else (
            ['candidate/dragr/tape30'] if directory==PAIR else ['analyze.py','analysis.json','p1m2.ascii','p1m6.ascii'])
        manifest={s.split(maxsplit=1)[1]:s.split(maxsplit=1)[0]
                  for s in (directory/'result.sha256').read_text().splitlines()}
        for name in names:pins[str(directory/name)]=manifest[name]
    verify(pins)
    helper=runpy.run_path(str(OLD/'analyze.py'),run_name='read_only')['lookup']
    pins[str(Path(helper.__file__))]=sha(Path(helper.__file__))
    # Physics source identity was recorded by the earlier exact D4 lookup audit.
    recorded=json.loads((OLD/'analysis.json').read_text())['sources']
    for name in ('LIBLEX.f','LIBDRA.f','LIBDRB.f'):
        p=ROOT/'src'/name; rec=[r for r in recorded if r['path']==str(p)]
        assert len(rec)==1 and sha(p)==rec[0]['sha256'];pins[str(p)]=rec[0]['sha256']
    pins[str(Path(__file__))]=sha(Path(__file__))
    lib=decode(PAIR/'candidate/dragr/tape30',True)
    temps=nr.data(lib,('Fe56','TEMPERATURE'));assert temps==(293.,550.,900.,1200.,2000.)
    nodes=[]
    for i in range(1,6):
        prefix=('Fe56',f'SUBTMP{i:04d}')
        fields={k[2]:v[1] for k,v in lib.items() if len(k)==3 and k[:2]==prefix}
        nodes.append(nr.cpo_scatter(fields,0,370).astype(F))
    assert all(float(x.min())>=0 for x in nodes)
    meta=decode(RUN/'material/metadata.ascii'); results=[]
    for index,mix,filename in ((12,2,'fe56_aim1.ascii'),(35,6,'fe56_em10.ascii')):
        temperature=nr.data(meta,('ISOTOPESTEMP',))[index-1]
        r=decode(RUN/'material'/filename); old=decode(OLD/f'p1m{mix}.ascii')
        fields=lambda rec:{k[0]:v[1] for k,v in rec.items() if len(k)==1}
        actual=nr.cpo_scatter(fields(r),0,370).astype(F)
        prior=nr.cpo_scatter(fields(old),0,370).astype(F)
        w=weights(temps,temperature); existing=helper.temp_weights(temperature)
        assert w[:4].tobytes()==existing.tobytes() and w[4]==0
        replay=mix_nodes(nodes,w); tail=slice(281,370)
        assert replay[:,tail].tobytes()==actual[:,tail].tobytes()
        assert actual[:,tail].tobytes()==prior[:,tail].tobytes()
        negative=np.argwhere(actual<0)
        assert np.all(negative[:,1]>=281)
        assert replay[actual<0].tobytes()==actual[actual<0].tobytes()
        # Offline diagnostic only. Do not write this alternative to any library.
        wl=weights(temps,temperature,1)
        assert np.all(wl>=0) and np.count_nonzero(wl)==2
        linear=mix_nodes(nodes,wl)
        assert np.all(linear[:,tail]>=0)
        worst=np.unravel_index(actual.argmin(),actual.shape)
        results.append(dict(mix=mix,temperature_K=float(F(temperature)),
            actual_cubic_sqrt_weights=[float(x) for x in w],
            matched_existing_weight_implementation=True,primary_groups=[282,370],
            exact_float32_replay_entries=370*89,negative_count=len(negative),
            all_negative_values_exactly_reproduced=True,
            worst=dict(destination=int(worst[0])+1,source=int(worst[1])+1,
                node_values=[float(n[worst]) for n in nodes],saved=float(actual[worst]),
                replay=float(replay[worst]),weighted_terms=[float(F(c*n[worst])) for c,n in zip(w,nodes)]),
            offline_linear_sqrt_diagnostic=dict(status='NOT_A_VALIDATED_REPLACEMENT',
                weights=[float(x) for x in wl],negative_count=int((linear[:,tail]<0).sum()),
                minimum=float(linear[:,tail].min()),
                maximum_change_from_cubic=float(abs(linear[:,tail].astype(float)-replay[:,tail]).max()))))
    verify(pins)
    return dict(status='SAVED_FE56_NEGATIVE_P0_REPRODUCED_BY_TEMPERATURE_INTERPOLATION',
        tables_K=list(temps),all_five_node_P0_matrices_nonnegative=True,
        source_interpolation='LIBDRA NOTX=3 -> LIBLEX cubic Lagrange in sqrt(T)',
        exact_replay_entries=65860,negative_entries_reproduced=843,rows=results,
        sources=pins,native_engines_started=0,production_files_modified=0,
        limits=['Proof covers these two Fe56 temperatures and all G282-370 incident columns, not every isotope or material.',
                'No new TONE or transport solution; no k or CE bias attribution.',
                'Offline order-1 comparison is not enabled and is not a production acceptance.',
                'Negative scalar weights demonstrate cubic overshoot; no negative entries are clipped.',
                'The separate macro mix4/G240 imbalance is not explained by this thermal Fe56 audit.'])

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    result=audit()
    with args.output.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='sources'},indent=2))
