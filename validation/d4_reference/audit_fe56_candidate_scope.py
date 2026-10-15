"""Read-only full-group scope audit of the retained Fe56 paired experiment."""
import argparse
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PAIR = ROOT/'validation/artifacts/d4a-fe56-mt51-control-candidate-20260929'
PAIR_MANIFEST = 'a81fb4504793e40d86567ba70b4c13c30d5093bd5a79b5ebc132ce52af586843'
DRAGON = Path('/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/ce_compare')
PAPER = DRAGON/'mc2027_csd_rr_evidence_v1_20260909/paper_parallel_20260910'

def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def expand(counts,tops,values,groups,ss=None):
    """Dense observation only. Omitted correction tails must be outside SS."""
    assert len(counts)==len(tops)==groups
    assert all(0 <= n <= hi <= groups for n,hi in zip(counts,tops))
    assert 0 < len(values) <= sum(counts)
    assert np.isfinite(values).all()
    if ss is None:
        assert len(values)==sum(counts),'infinite matrix truncation'
    a=np.zeros((groups,groups),dtype=np.float64)
    cursor=omitted=0
    for dest,(n,hi) in enumerate(zip(counts,tops)):
        for source in range(hi,hi-n,-1):
            if cursor<len(values):
                a[dest,source-1]=values[cursor]
            else:
                assert ss is not None and not ss[0]<=source<=ss[1], 'omitted self-shielded entry'
                omitted+=1
            cursor+=1
    return a,omitted

def audit():
    assert sha(PAIR/'result.sha256')==PAIR_MANIFEST
    manifest={line.split('  ',1)[1]:line.split('  ',1)[0]
              for line in (PAIR/'result.sha256').read_text().splitlines()}
    sources=[Path(__file__),PAIR/'result.sha256']
    def frozen(relative):
        p=PAIR/relative;assert sha(p)==manifest[relative];sources.append(p);return p
    sys.path.insert(0,str(PAPER/'angular_tracking/p3_pilot'))
    import independent_audit as adapter
    sys.path.insert(0,str(DRAGON/'fullpitch_pnl_s30_b0_closure_v1_20260907'))
    import native_records as nr
    stream=module('existing_stream_reader',PAPER/'finegroup_acceptance/stream_records.py')
    sources += [Path(adapter.__file__),Path(nr.__file__),Path(stream.__file__)]
    observations=[];inventories=[]
    for lane in ('control','candidate'):
        log=frozen(f'{lane}/dragr/output').read_text()
        first=int(re.search(r'first group of unresolved resonance xs data\s*\.\s*(\d+)',log)[1])
        last=int(re.search(r'last group of resolved resonance xs data\s*\.*\s*(\d+)',log)[1])
        assert (first,last)==(25,281)
        raw,_=adapter.strict_xsm(frozen(f'{lane}/dragr/tape30').read_bytes())
        records=nr.decode(raw)
        other,stats=stream.decode_stream(io.BytesIO(raw))
        assert records==other,'independent reader disagreement'
        inventories.append(dict(lane=lane,**stats))
        def data(prefix,key):
            return np.asarray(nr.data(records,prefix+(key,)),dtype=np.float64)
        def mat(prefix,order,finite=False):
            suffix=f'{order:02d}'
            return expand(nr.data(records,prefix+('NJJS'+suffix,),1),
                nr.data(records,prefix+('IJJS'+suffix,),1),
                data(prefix,'SCAT'+suffix),370,(first,last) if finite else None)
        temperatures=nr.data(records,('Fe56','TEMPERATURE'),2)
        for it,t in enumerate(temperatures,1):
            prefix=('Fe56',f'SUBTMP{it:04d}')
            base=[mat(prefix,o)[0] for o in (0,1)]
            total0=data(prefix,'NTOT0')
            for iz,dilution in enumerate([None,*data(prefix,'DILUTION')]):
                total=total0.copy(); matrices=[a.copy() for a in base];tails=[0,0]
                if iz:
                    sub=prefix+(f'SUBMAT{iz:04d}',)
                    correction=data(sub,'NTOT0')
                    assert len(correction)==last
                    total[:last]+=correction
                    for order in (0,1):
                        delta,tails[order]=mat(sub,order,True)
                        matrices[order]+=delta
                p0=matrices[0];summed=p0.sum(axis=0);gap=summed-total
                ss=slice(first-1,last)
                violations=[dict(group=g+1,weighted_scatter_sum=float(summed[g]),
                    weighted_total=float(total[g]),excess=float(gap[g]))
                    for g in range(first-1,last) if gap[g]>0]
                observations.append(dict(lane=lane,temperature_K=t,sigma0_barn=dilution,
                    primary_groups=370,self_shielding_primary_groups=[first,last],
                    omitted_outside_SS_tail_lengths=tails,
                    P0_negative_entries=int((p0<0).sum()),P0_minimum=float(p0.min()),
                    SS_P0_negative_entries=int((p0[:,ss]<0).sum()),
                    SS_P0_minimum=float(p0[:,ss].min()),
                    signed_P1_negative_entries=int((matrices[1]<0).sum()),
                    SS_positive_scatter_minus_total=violations,
                    all_group_max_scatter_minus_total=float(gap.max()),
                    all_group_max_excess_group=int(gap.argmax())+1))
    before={str(p):sha(p) for p in sources}
    for p in sources:
        if p.is_relative_to(PAIR) and p.name!='result.sha256':
            assert sha(p)==manifest[str(p.relative_to(PAIR))]
    summary={}
    for lane in ('control','candidate'):
        rows=[r for r in observations if r['lane']==lane]
        positive=[dict(temperature_K=r['temperature_K'],sigma0_barn=r['sigma0_barn'],**v)
                  for r in rows for v in r['SS_positive_scatter_minus_total']]
        summary[lane]=dict(nodes=len(rows),group_nodes=370*len(rows),
            SS_positive_excess_count=len(positive),
            SS_positive_excess_groups=sorted({v['group'] for v in positive}),
            SS_largest_excess=max(positive,key=lambda x:x['excess']) if positive else None,
            full_P0_minimum=min(r['P0_minimum'] for r in rows),
            SS_P0_minimum=min(r['SS_P0_minimum'] for r in rows))
    for p,digest in before.items():assert sha(p)==digest
    return dict(status='SAVED_DATA_SCOPE_REPORTED_NOT_PRODUCTION_ACCEPTANCE',
        native_engines_started=0,library_writes=0,summary=summary,observations=observations,
        dual_parser_inventory=inventories,sources=before,
        method='Finite corrections added to infinite matrices in float64 for observation only; no file values changed or signed entries clipped.',
        limitations=['Finite nodes are flux-ratio-weighted, not new normalized self-consistent TONE states.',
            'Positive excess outside the SS interval may include neutron multiplication; no global nonmultiplication assumption.',
            'Signs are reported without a new tolerance; structural read success is not physical acceptance.',
            'This does not validate an underlying nonnegative continuous angular distribution from two moments.'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    assert not a.output.exists()
    result=audit()
    with a.output.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(result['summary'],indent=2))
