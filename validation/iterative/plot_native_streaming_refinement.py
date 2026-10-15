#!/usr/bin/env python3
"""Plot the two declared spatial observables without changing any gate."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main(root):
    data=json.loads((root/'analysis/result.json').read_text())
    fig,axes=plt.subplots(2,2,figsize=(10,7),sharex=True,constrained_layout=True)
    colors={51:'#2764a5',61:'#ba4b23',98:'#26806a'}
    for i,boundary in enumerate(['vacuum','white']):
        for j,(key,label) in enumerate([('flux_relative','Restricted scalar flux'),('axial_escape_relative','Top + bottom escape')]):
            ax=axes[i,j]
            for g in [51,61,98]:
                rows=sorted((r for r in data['mesh_checks'] if r['kernel']=='native' and r['group']==g and r['boundary']==boundary),key=lambda r:r['fine_n'])
                ax.plot([r['fine_n'] for r in rows],[100*max(r[key]) for r in rows],marker='o',color=colors[g],label=f'Group {g}')
            ax.axhline(1.,color='#777777',linestyle='--',linewidth=1,label='1% gate' if (i,j)==(0,0) else None)
            ax.set_xscale('log',base=2);ax.set_yscale('log');ax.set_xticks([8,16,32,64],[8,16,32,64])
            ax.set_title(f'Radial {boundary}: {label}',fontsize=11)
            ax.set_ylabel('Adjacent-grid change (%)');ax.grid(True,which='major',alpha=.2)
            if i==1:ax.set_xlabel('Finer axial grid (cells)')
    axes[0,0].legend(fontsize=9,loc='best')
    fig.suptitle('Native-compatible streaming: spatial refinement\nMaximum of the two prescribed volume sources',fontsize=13)
    (root/'figures').mkdir(exist_ok=True)
    fig.savefig(root/'figures/mesh_changes.png',dpi=180)
    plt.close(fig)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path)
    main(p.parse_args().artifact)
