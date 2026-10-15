#!/usr/bin/env python3
"""Standalone scientific plot of measured mesh changes and signed angles."""
import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main(artifact):
    a=Path(artifact);r=json.loads((a/'analysis/result.json').read_text())
    n=np.array([x['cells'] for x in r['meshes']]);k=[x['k'] for x in r['meshes']]
    angle=[x['minimum_outgoing_angular_flux'] for x in r['meshes']]
    fig,ax=plt.subplots(1,3,figsize=(12.6,3.7),layout='constrained')
    ax[0].plot(n,k,'o-',color='#24678f');ax[0].set_ylabel('k');ax[0].set_title('Full-space eigenvalue')
    ax[1].plot(n,angle,'o-',color='#b83b32');ax[1].axhline(0,color='0.35',lw=.8)
    ax[1].set_ylabel('Minimum outgoing angular flux');ax[1].set_title('Positive scalar flux at every mesh')
    fine=[x['to_cells'] for x in r['refinements']]
    ax[2].semilogy(fine,[x['relative_k_change'] for x in r['refinements']],'o-',label='Relative k change')
    ax[2].semilogy(fine,[x['restricted_flux_relative_l2'] for x in r['refinements']],'s-',label='Restricted scalar-flux change')
    ax[2].axhline(1e-4,color='0.4',ls='--',lw=.9,label='k-change threshold')
    ax[2].set_title('Changes between adjacent meshes');ax[2].legend(fontsize=8)
    for axis in ax:
        axis.set_xscale('log',base=2);axis.set_xticks(n,labels=[str(x) for x in n])
        axis.set_xlabel('Axial cells (20 cm total)');axis.grid(alpha=.2)
        axis.spines[['top','right']].set_visible(False)
    fig.suptitle('Frozen native P0 / S2-DD candidate: refinement does not pass angular positivity',fontsize=12)
    fig.savefig(a/'mesh_refinement.png',dpi=180);fig.savefig(a/'mesh_refinement.pdf')
    plt.close(fig)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);main(p.parse_args().artifact)
