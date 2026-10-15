#!/usr/bin/env python3
"""Plot true analytic errors for the fixed strongest-scattering comparisons."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main(root):
    data = json.loads((root/'analysis/result.json').read_text())
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.5), layout='constrained')
    panels = [('st200_c100', 'scalar_true_relative', 'Conservative scattering: scalar cell means'),
              ('st200_c099', 'total_escape_true_relative', '99% scattering: total escape')]
    for ax, (case, key, title) in zip(axes, panels):
        rows = [r for r in data['cases'] if r['case'] == case]
        n = [r['n'] for r in rows]
        ax.plot(n, [100*r['upwind'][key] for r in rows], 'o--', color='#b85b23', label='Previous upwind')
        ax.plot(n, [100*r[key] for r in rows], 'o-', color='#176b9b', label='Cell characteristic')
        ax.axhline(1., color='#767676', linestyle=':', linewidth=1.2, label='Frozen 1% target')
        ax.set_xscale('log', base=2); ax.set_yscale('log')
        ax.set_xticks(n, [str(x) for x in n]); ax.set_xlabel('Axial cells')
        ax.set_ylabel('True relative error (%)'); ax.set_title(title, fontsize=11)
        ax.grid(True, alpha=.18); ax.legend(loc='lower left', fontsize=9)
    fig.suptitle('Same analytic S2 slabs, same grids: $\\Sigma_t=2$ cm$^{-1}$, H=20 cm', fontsize=13)
    fig.savefig(root/'figures/true_errors.png', dpi=180)
    plt.close(fig)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('artifact', type=Path)
    main(p.parse_args().artifact)
