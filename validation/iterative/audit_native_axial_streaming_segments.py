#!/usr/bin/env python3
"""Disclose raw segment balance of the two frozen coefficient kernels."""
import argparse
import json
from pathlib import Path
import numpy as np
from qualify_native_directional import load_native,save_json
from qualify_native_signed_axial import axial_mu
from native_axial_streaming import polynomial_coefficients


def main(root):
    plan=json.loads((root/'plan.json').read_text());d=load_native(root/'inputs/track_data.bin')
    line,seg=np.where(d['region']>0);region=d['region'][line,seg]-1
    length=d['h'][line,seg];mu=axial_mu(d)[d['polar'][line]];rows=[]
    for a in d['group_data']:
        total=a['total'][region]
        for kind in ['exact','native']:
            for n in plan['meshes']:
                rate=mu*n/plan['height_cm'];alpha=total+rate
                t,b,own=polynomial_coefficients(length,total,rate,n,kind,a['b'][line,seg],a['self_d'][line,seg])
                # Coefficients of T + A B - I and B + A D - L I.
                incoming=t+alpha[:,None]*b;source=b+alpha[:,None]*own
                incoming[:,0]-=1;source[:,0]-=length
                incoming[:,1:]-=rate[:,None]*b[:,:-1]
                source[:,1:]-=rate[:,None]*own[:,:-1]
                # Max row sum is the induced infinity norm of the triangular
                # shift matrix: last row contains all coefficients (reversed
                # for the other axial sign). No residual cancellation is used.
                ri=np.sum(abs(incoming),axis=1)
                rq=np.sum(abs(source),axis=1)/length
                i=int(np.argmax(ri));j=int(np.argmax(rq))
                rows.append(dict(group=a['group'],kernel=kind,n=n,
                    segment_polar_samples=len(line),incoming_defect_inf=float(ri[i]),
                    source_defect_inf_over_length=float(rq[j]),
                    incoming_worst_line=int(line[i]),incoming_worst_segment=int(seg[i]),
                    source_worst_line=int(line[j]),source_worst_segment=int(seg[j])))
    save_json(root/'analysis/segment_balance.json',dict(
        scope='Raw segment operator identities, all original segments and polar nodes. Both axial signs and planar orders have the same primitive norms.',
        incoming='||T + A B - I||_inf',source='||B + A D - L I||_inf / L',
        qualification='Descriptive raw defects; no new acceptance threshold, correction or clipping.',records=rows))
    print(json.dumps({kind:dict(incoming=max(x['incoming_defect_inf'] for x in rows if x['kernel']==kind),
                               source=max(x['source_defect_inf_over_length'] for x in rows if x['kernel']==kind))
                      for kind in ['exact','native']},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path)
    main(p.parse_args().artifact)
