"""Summarize REAL64 iteration logs without equating printed values to a saved-terminal audit."""
import argparse
import json
import math
from pathlib import Path
import re


def analyze(text):
    begin = re.compile(r' MCCGF64-CENSUS: BEGIN TITLE="[^"]+" NUN=(\d+) NGEFF=(\d+) KRYL=(\d+) MAXI=(\d+)')
    number = r'[+\-\d.]+[ED][+\-]\d+'
    outer = re.compile(r' OUT\(\s*(\d+)\) (EIG|FLX): PRC=\s*('+number+r') TAR=\s*('+number+r')')
    active = None; complete = []; traces = []; started = 0; parsing_eps = False
    for line in text.splitlines():
        match = begin.fullmatch(line)
        if match:
            if active is not None:
                raise ValueError('overlapping radial calls')
            nu, ng, kryl, cap = map(int,match.groups())
            if nu!=14 or not 0<ng<=370 or kryl!=10 or cap!=20:
                raise ValueError('undeclared radial call shape')
            active=dict(groups=ng,eps=[]);started+=1;parsing_eps=False
        if line.startswith(' EPS64'):
            if active is None:
                raise ValueError('orphan epsilon vector')
            parsing_eps=True
        if parsing_eps:
            values = re.findall(number,line)
            if values:
                active['eps'].extend(float(x.replace('D','E')) for x in values)
            elif not line.startswith(' EPS64'):
                parsing_eps=False
        if line.startswith(' MCCGF64-CENSUS: END'):
            if active is None or len(active['eps'])!=active['groups']:
                raise ValueError('incomplete completed radial call')
            if any(not math.isfinite(x) or x<0 for x in active['eps']):
                raise ValueError('invalid epsilon')
            complete.append(active);active=None;parsing_eps=False
        match = outer.fullmatch(line.split(' KEFF=')[0].split(' FNOR=')[0])
        if match:
            iteration,kind,value,target=match.groups()
            traces.append(dict(iteration=int(iteration),kind=kind,value=float(value),target=float(target)))
    values=[e for call in complete for e in call['eps']]
    changes=[x['value'] for x in traces if x['kind']=='FLX']
    return dict(started_radial_calls=started,completed_radial_calls=len(complete),
        printed_group_terminals=len(values),maximum_printed_inner_residual=max(values,default=None),
        printed_inner_values_above_declared_2p5e8=sum(e>2.5000005e-8 for e in values),
        incomplete_final_radial_call=active is not None,
        minimum_printed_outer_flux_change=min(changes,default=None),outer=traces,
        strict_terminal_marker=' FLU2DR-TERM OUTER-GATE=PASS' in text,
        snapshot_marker_count=len(re.findall(r'^>\|AXMAT-SNAPSHOT-A-COMPLETE(?:\s|$)',text,re.M)),
        scope='Printed iteration observations only; never a serialized-terminal or accuracy qualification.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args()
    result=analyze(args.log.read_text())
    with args.output.open('x') as stream:
        json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='outer'},indent=2))


if __name__=='__main__':
    main()
