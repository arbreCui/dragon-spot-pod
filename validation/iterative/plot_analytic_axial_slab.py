#!/usr/bin/env python3
"""Show true error, misleading mesh changes and slow scattering convergence."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main(root):
    data=json.loads((root/'analysis/result.json').read_text())
    rows=lambda case:[r for r in data['cases'] if r['case']==case]
    fig,axes=plt.subplots(1,3,figsize=(14,4.6),constrained_layout=True)
    ax=axes[0];r=rows('st200_c000');adj=[r for r in data['adjacent'] if r['case']=='st200_c000']
    ax.plot([x['n'] for x in r],[100*x['scalar_true_relative'] for x in r],'-o',color='#b34437',label='True scalar error')
    ax.plot([x['fine_n'] for x in adj],[100*x['scalar_adjacent_relative'] for x in adj],'-s',color='#2869a4',label='Adjacent-grid change')
    bad=[x for x in adj if x['false_admission']]
    ax.scatter([x['fine_n'] for x in bad],[100*x['scalar_true_fine_relative'] for x in bad],s=110,facecolors='none',edgecolors='#8f1e20',linewidths=2)
    ax.set_title('Pure absorber: two false admissions');ax.axhline(1.,color='#777777',linestyle='--',label='1% comparison')
    ax=axes[1];r=rows('st200_c100')
    ax.plot([x['n'] for x in r],[100*x['scalar_true_relative'] for x in r],'-o',color='#b34437',label='True scalar error')
    ax.plot([x['n'] for x in r],[100*x['total_escape_true_relative'] for x in r],'-s',color='#26806a',label='True escape error')
    ax.set_title('No absorption: balance hides flux error')
    ax.annotate(f"256 cells: {100*r[-1]['scalar_true_relative']:.1f}% flux error",xy=(256,100*r[-1]['scalar_true_relative']),xytext=(38,35),arrowprops=dict(arrowstyle='->',color='#555555'),fontsize=9)
    ax=axes[2]
    for case,label,color in [('st200_c090','90% scattering','#2869a4'),('st200_c099','99% scattering','#26806a')]:
        r=rows(case);ax.plot([x['n'] for x in r],[100*x['total_escape_true_relative'] for x in r],'-o',color=color,label=label)
    ax.axhline(1.,color='#777777',linestyle='--',label='1% comparison');ax.set_title('Strong scattering: true escape error')
    for ax in axes:
        ax.set_xscale('log',base=2);ax.set_xticks([8,16,32,64,128,256],[8,16,32,64,128,256]);ax.set_xlabel('Axial cells')
        ax.set_ylabel('Relative error / change (%)');ax.grid(alpha=.2);ax.legend(fontsize=8)
    fig.suptitle('Analytic S2 slab: small residuals and mesh changes do not bound spatial error',fontsize=13)
    (root/'figures').mkdir(exist_ok=True);fig.savefig(root/'figures/analytic_errors.png',dpi=180);plt.close(fig)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);main(p.parse_args().artifact)
