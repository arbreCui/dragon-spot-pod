"""Summarize explicit printed convergence observations, including partial logs."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re

NUMBER = r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?'
TRACE = re.compile(r'MCGMRE-TRACE ITER=\s*(\d+) PHASE=(INITIAL|KRYLOV)\s+ACTIVE-AFTER=\s*(\d+) MAX-REPS=\s*('+NUMBER+r') EPSI=\s*('+NUMBER+r')')
GROUP = re.compile(r'^\s*GROUP \(\s*(\d+)\) :')
ACCURACY = re.compile(r'MCCGF: NUMBER OF MCCG ITERATIONS=\s*(\d+)\s+ACCURACY=\s*('+NUMBER+r')\.')
OUTER = re.compile(r'OUT\(\s*(\d+)\) (EIG|FLX): PRC=\s*('+NUMBER+r') TAR=\s*('+NUMBER+r')')


def number(text):
    value = float(text.replace('D', 'E').replace('d', 'e'))
    if not math.isfinite(value) or value < 0:
        raise ValueError('invalid printed residual')
    return value


def analyze(text):
    calls, outer, errors = [], {}, []
    call = None
    group = None
    preceding_outer = None
    for lineno, line in enumerate(text.splitlines(), 1):
        match = OUTER.search(line)
        if match:
            iteration, kind, val, target = match.groups()
            iteration = int(iteration)
            preceding_outer = iteration
            row = outer.setdefault(iteration, {'iteration':iteration, 'eig':None, 'flux':None})
            key = 'eig' if kind == 'EIG' else 'flux'
            if row[key] is not None:
                errors.append(f'duplicate outer {key} at line {lineno}')
            row[key] = {'value':number(val), 'target':number(target), 'line':lineno}
        match = TRACE.search(line)
        if match:
            iteration, phase, active, residual, eps = match.groups()
            if iteration == '1' and phase == 'INITIAL':
                call = {'id':len(calls)+1, 'preceding_completed_outer':preceding_outer,
                        'trace':[], 'groups':[], 'summary_header_seen':False}
                calls.append(call)
            if call is None:
                errors.append(f'trace before initial record at line {lineno}')
                continue
            call['trace'].append({'iteration':int(iteration), 'phase':phase,
                                  'active_after':int(active), 'max_reported_residual':number(residual),
                                  'epsi':number(eps), 'line':lineno})
        if 'M O C PARAMETERS:' in line and call is not None:
            call['summary_header_seen'] = True
        match = GROUP.match(line)
        if match:
            if group is not None:
                errors.append(f'group {group} missing accuracy before line {lineno}')
            group = int(match.group(1))
        match = ACCURACY.search(line)
        if match:
            if group is None or call is None:
                errors.append(f'accuracy without group/call at line {lineno}')
                continue
            if not 1 <= group <= 370 or any(r['group'] == group for r in call['groups']):
                errors.append(f'invalid or duplicate group {group} in call {call["id"]}')
            iterations, accuracy = match.groups()
            call['groups'].append({'group':group, 'iterations':int(iterations),
                                   'reported_accuracy':number(accuracy), 'line':lineno})
            group = None
    completed = [c for c in calls if c['summary_header_seen'] and c['groups']]
    records = [g for c in completed for g in c['groups']]
    unresolved = [c['id'] for c in completed if c['trace'][-1]['active_after'] != 0]
    above = [dict(call=c['id'], **g) for c in completed for g in c['groups']
             if g['reported_accuracy'] > c['trace'][-1]['epsi']]
    flux = [v['flux']['value'] for v in outer.values() if v['flux'] is not None]
    return {'classification':'PRINTED_RESIDUAL_OBSERVATIONS_ONLY', 'parser_errors':errors,
            'calls_with_group_summaries':len(completed), 'all_started_calls':len(calls),
            'group_summaries':len(records), 'completed_calls_with_active_groups':unresolved,
            'printed_group_residuals_above_epsi':above,
            'maximum_printed_group_accuracy':max((r['reported_accuracy'] for r in records), default=None),
            'maximum_reported_group_iterations':max((r['iterations'] for r in records), default=None),
            'outer':list(outer.values()), 'minimum_printed_outer_flux_change':min(flux, default=None),
            'unpaired_final_group':group, 'calls':calls,
            'limitation':'Printed GMRES accuracy may be a Krylov recurrence estimate; no independent post-update residual, precision-floor proof, snapshot or physics acceptance is inferred. Missing outer flux observations remain null.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log',type=Path)
    parser.add_argument('output',type=Path)
    args = parser.parse_args()
    raw = args.log.read_bytes()
    result = analyze(raw.decode(errors='replace'))
    result['log'] = {'path':str(args.log.resolve()), 'sha256':hashlib.sha256(raw).hexdigest()}
    with args.output.open('x') as stream:
        json.dump(result,stream,indent=2,allow_nan=False)
        stream.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('calls','outer','printed_group_residuals_above_epsi')},indent=2))


if __name__ == '__main__':
    main()
