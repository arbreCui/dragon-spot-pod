"""Bound one declared diagnostic and analyze its actual failing native tuple."""
import argparse
import json
import math
from pathlib import Path
import re
import signal
import subprocess

import numpy as np

from production_runner import DiskResources,SerialExecutor,dump_json,require_file,sha256


def main():
    p=argparse.ArgumentParser();p.add_argument('execution',type=Path);p.add_argument('--sha256',required=True);args=p.parse_args()
    execution=args.execution.resolve();work=execution.parent
    spec=json.loads(require_file(execution,args.sha256).read_text())
    if spec['schema']!='AXMAT_AAA_FAILED_RADIAL_INNER_TUPLE_DIAGNOSTIC_V1' or spec['wall_seconds']!=300 or spec['threads']!=1 or spec['retries']!=0:
        raise ValueError('declared bounded diagnostic required')
    for name,wanted in spec['files'].items():require_file(Path(name),wanted)
    with (work/'claim.json').open('x') as stream:json.dump(dict(execution_sha256=args.sha256),stream)
    resources=DiskResources(Path(spec['artifact_root']),spec['resource_roots'],8*2**30,24*2**30)
    runner=SerialExecutor(work,300,'AAA',resources)
    result=dict(classification='DIAGNOSTIC_FAILED_NO_RETRY',production_qualified=False,AAA_qualified=False,
        resources_before=resources.check())
    handlers={s:signal.signal(s,signal.default_int_handler) for s in (signal.SIGHUP,signal.SIGTERM,signal.SIGINT)}
    try:
        try:
            with (work/'AAA/picard_radial.x2m').open('rb') as source,(work/'AAA/replay.log').open('xb') as log:
                runner._process([str(work/'runtime/Dragon')],work/'AAA',source,log,300)
        except RuntimeError as error:
            result['native_error']=str(error)
        text=(work/'AAA/replay.log').read_text(errors='replace')
        if 'AXMAT-FAILED-INNER-TUPLE-EXPORTED' not in text.splitlines() or 'MCGMRE64: STRICT INNER TERMINAL FAILED; GROUPS=1 ARNOLDI=20' not in text:
            raise ValueError('declared native failure was not captured')
        raw=(work/'AAA/failed_inner_tuple.bin').read_bytes()
        header=np.frombuffer(raw,'<i4',6).tolist()
        version,nun,ngeff,nfailed,iteration,arnoldi=header
        if version!=1 or nun!=14 or nfailed!=1 or arnoldi!=20 or len(raw)!=32+nfailed*(4+8*(2+5*nun)):
            raise ValueError('unexpected tuple format or incomplete export')
        threshold=float(np.frombuffer(raw,'<f8',1,24)[0]);offset=32;groups=[]
        if threshold!=1e-13:raise ValueError('strict gate changed')
        for _ in range(nfailed):
            group=int(np.frombuffer(raw,'<i4',1,offset)[0]);offset+=4
            values=np.frombuffer(raw,'<f8',2+5*nun,offset).copy();offset+=8*len(values)
            if not np.isfinite(values).all():raise ValueError('nonfinite failed tuple')
            denominator,reported=values[:2];qfr,phi,source,bare,accelerated=values[2:].reshape(5,nun)
            norm=lambda v:math.sqrt(math.fsum(float(x)*float(x) for x in v))
            qfr_norm=norm(qfr)
            actual=norm(accelerated-phi)/qfr_norm
            physical=norm(bare-phi)/qfr_norm
            if not math.isclose(qfr_norm,denominator,rel_tol=5e-15) or not math.isclose(actual,reported,rel_tol=5e-15):
                raise ValueError('saved tuple does not reconstruct failed strict residual')
            groups.append(dict(group=group,strict_threshold=threshold,reported_residual=reported,
                independently_resummed_accelerated_TRUE_residual=actual,bare_transport_image_residual=physical,
                bare_and_accelerated_difference=norm(accelerated-bare)/qfr_norm,
                acceleration_ratio=actual/physical if physical else None,source_and_iterate_finite=True,
                strict_terminal_pass=actual<threshold))
        original=next(Path(path) for path in spec['files'] if path.endswith('/map002/picard_radial.log'))
        census=lambda value:re.findall(r'^ (?:SPOR64_B2B|MCCGF64|MCGMRE64)-CENSUS:.*$',value,re.M)
        same=census(text)==census(original.read_text())
        result.update(classification='NATIVE_FAILED_INNER_TUPLE_CAPTURED_AND_RECONSTRUCTED',
            original_rounded_census_identical=same,iteration=iteration,Arnoldi_work=arnoldi,groups=groups,
            failure_preserved=True,acceptance_threshold_changed=False,algorithm_changed=False,
            scope='Actual failed accelerated TRUE check and pre-ACA bare image at its final attempted iterate. Census equality is limited to rounded printed diagnostics, not complete numerical identity. No evidence of an irreducible precision floor or physical accuracy failure.')
    finally:
        for name,wanted in spec['files'].items():require_file(Path(name),wanted)
        result['frozen_inputs_unchanged']=True
        result['outputs']={q.name:sha256(q) for q in (work/'AAA').iterdir() if q.is_file() and not q.is_symlink() and q.name not in ('picard_radial.x2m','SpotStepR64.c2m')}
        result['resources_after']=resources.check()
        dump_json(work/'run_status.json',result)
        for s,h in handlers.items():signal.signal(s,h)
    print(json.dumps({k:v for k,v in result.items() if not k.startswith('resources')},indent=2))


if __name__=='__main__':main()
