"""Bound a declared compensated-flight replay and admit actual returned fields."""
import argparse
import json
from pathlib import Path
import re
import signal
import subprocess
import time

from production_runner import ROOT,DiskResources,SerialExecutor,check_dragon_log,dump_json,require_file,sha256


def main():
    p=argparse.ArgumentParser();p.add_argument('execution',type=Path);p.add_argument('--sha256',required=True);args=p.parse_args()
    execution=args.execution.resolve();work=execution.parent
    spec=json.loads(require_file(execution,args.sha256).read_text())
    if spec['schema']!='AXMAT_AAA_COMPENSATED_NATIVE_FLIGHT_REPLAY_V1' or spec['wall_seconds']!=300 or spec['threads']!=1 or spec['retries']!=0:
        raise ValueError('bounded declared arithmetic diagnostic required')
    for path,wanted in spec['files'].items():require_file(Path(path),wanted)
    admission=ROOT/'validation/artifacts/d4a-scattering-mesh12-picard-runtime-20260925/admit_candidate_radial'
    import production_runner as pr
    host=pr.pinned_runtime_files()['admit_candidate_radial']
    require_file(admission,host['sha256'],True)
    launch=dict(execution_sha256=args.sha256,runner_sha256=sha256(Path(__file__)),
        returned_state_host=host,transport_wall_seconds=300,host_wall_seconds=120,
        automatic_retries=0,declared_before_claim=True)
    with (work/'launch.json').open('x') as stream:json.dump(launch,stream,indent=2)
    with (work/'claim.json').open('x') as stream:json.dump(dict(execution_sha256=args.sha256,launch_sha256=sha256(work/'launch.json')),stream)
    resources=DiskResources(Path(spec['artifact_root']),spec['resource_roots'],8*2**30,24*2**30)
    runner=SerialExecutor(work,420,'AAA',resources)
    result=dict(classification='COMPENSATED_REPLAY_FAILED_NO_RETRY',production_qualified=False,AAA_qualified=False,resources_before=resources.check())
    start=time.monotonic();handlers={s:signal.signal(s,signal.default_int_handler) for s in (signal.SIGHUP,signal.SIGTERM,signal.SIGINT)}
    try:
        with (work/'AAA/picard_radial.x2m').open('rb') as source,(work/'AAA/replay.log').open('xb') as log:
            runner._process([str(work/'runtime/Dragon')],work/'AAA',source,log,300)
        text=(work/'AAA/replay.log').read_text(errors='replace')
        check_dragon_log(text,'AXMAT-PICARD-RADIAL-COMPLETE')
        require_file(work/'AAA/candidate_radial.xsm');require_file(work/'AAA/candidate_system.xsm')
        runner.execute(work/'AAA','admit_candidate_radial',[str(admission),'candidate_radial.xsm','route_contract.xsm'],120)
        result.update(classification='COMPENSATED_RADIAL_REPLAY_RETURNED_AND_ADMITTED',
            elapsed_seconds=time.monotonic()-start,acceptance_threshold_changed=False,
            physical_operator_coefficients_changed=False,summation_order_changed=True,
            diagnostic_failed_tuple_exists=(work/'AAA/failed_inner_tuple.bin').exists(),
            scope='Exact old second-map proposal replay completed all radial solves and unchanged native returned-state admission. Still requires a separately declared complete coupled trial and independent reference.')
    except BaseException as error:
        result['error']=repr(error)
        raise
    finally:
        for path,wanted in spec['files'].items():require_file(Path(path),wanted)
        require_file(admission,host['sha256'],True)
        result['frozen_inputs_unchanged']=True;result['elapsed_seconds']=time.monotonic()-start
        result['outputs']={p.name:sha256(p) for p in (work/'AAA').iterdir() if p.is_file() and not p.is_symlink() and p.name not in ('picard_radial.x2m','SpotStepR64.c2m')}
        result['resources_after']=resources.check()
        dump_json(work/'run_status.json',result)
        for s,h in handlers.items():signal.signal(s,h)
    print(json.dumps({k:v for k,v in result.items() if not k.startswith('resources')},indent=2))


if __name__=='__main__':main()
