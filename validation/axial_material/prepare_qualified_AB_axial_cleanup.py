"""Declare a fresh trial fixing only deletion of absent bootstrap diagnostics."""
import json
import math
from pathlib import Path
import shutil

from production_runner import ROOT, dump_json, require_file, sha256
from qualified_snapshot_ingestion import descriptor


def main():
    art=ROOT/'validation/artifacts'
    old=art/'axial-material-production-qualified-AB-20261004'
    admission=art/'axial-material-qualified-AB-admission-v2-20261004'
    prepared=json.loads(require_file(old/'prepared.json','4b5729bac03e74d0327ab80769c4a582bc3108dfe956f674af2801035e97c8f1').read_text())
    for name,wanted in prepared['local_files'].items():require_file(old/name,wanted)
    status=json.loads((old/'AAA/run_status.json').read_text())
    claim=json.loads((old/'AAA/run_claim.json').read_text())
    log=old/'AAA/map001/picard_axial.log'
    if status['classification']!='FAILED_NO_RETRY' or status['completed_maps']!=0 or "UNABLE TO FIND BLOCK 'SPOT-X-RRHO'" not in log.read_text():
        raise ValueError('expected pre-axial absent-record failure required')
    prior_wall=status['finished_unix']-claim['started_unix']
    remaining=math.floor(prepared['budgets']['total_seconds']-prior_wall)
    work=art/'axial-material-qualified-AB-cleanup-admission-20261004'
    output=art/'axial-material-production-qualified-AB-cleanup-20261004'
    work.mkdir(exist_ok=False)
    spec=json.loads(Path(prepared['case_spec']['path']).read_text())
    spec['experiment_id']='axial-material-qualified-AB-rank1-cleanup-20261004'
    spec['status']='PREDECLARED_AXIAL_INPUT_CLEANUP_IMPLEMENTATION_FIX'
    spec['resource_caps']['total_wall_s_per_spot_case']=remaining
    spec['axial_cleanup_fix']=dict(prior_prepared=descriptor(old/'prepared.json'),
        prior_failure=descriptor(old/'AAA/run_status.json'),failure_log=descriptor(log),
        prior_elapsed_wall_seconds=prior_wall,remaining_case_wall_seconds=remaining,
        change="Delete only SPOT-X-STATE and SPOT-X-EPOCH before the axial solve. Bootstrap CLOSED/0 has no RRHO/RLEAK/DLEAK/RA. SPOXCONV unconditionally overwrites all four diagnostics after every successful new axial solve.",
        established_deck=descriptor(ROOT/'validation/iterative/d4a_rank2_picard_axial.x2m'),
        diagnostic_writer=descriptor(ROOT/'src/SPOXCONV.f90'),
        unchanged='All physical inputs, shared common rank1 rule, solver binaries, numerical/CE gates and no-retry rule. Old failure remains immutable; fresh execution only.')
    dump_json(work/'case_spec.json',spec)
    addendum=json.loads(Path(prepared['rank_addendum']['path']).read_text())
    addendum.update(case_spec_sha256=sha256(work/'case_spec.json'),experiment_id=spec['experiment_id'])
    dump_json(work/'rank_addendum.json',addendum)
    for name in ('production_runner_qualified.py','production_inputs.py','snapshot_control_preflight.py',
                 'qualified_snapshot_ingestion.py','analyze_r64_snapshot.py','analyze_r64_tracking_moments.py',
                 'check_r64_audit_rejections.py','check_r64_normalization_rejections.py'):
        shutil.copy2(admission/name,work/name)
    inputs=work/'production_inputs.py'
    text=inputs.read_text()
    faulty="  DEL 'SPOT-X-EPOCH'\n  DEL 'SPOT-X-RRHO'\n  DEL 'SPOT-X-RLEAK'\n  DEL 'SPOT-X-DLEAK'\n  DEL 'SPOT-X-RA' ;"
    if text.count(faulty)!=1:raise ValueError('unexpected deck generator layout')
    inputs.write_text(text.replace(faulty,"  DEL 'SPOT-X-EPOCH' ;"))
    declaration=json.loads((old/'declaration.json').read_text())
    declaration.update(experiment_id=spec['experiment_id'],case_spec=descriptor(work/'case_spec.json'),
        rank_addendum=descriptor(work/'rank_addendum.json'),
        resource_roots=sorted(str(p.resolve()) for p in art.glob('axial-material-*') if p.is_dir())+[str(output)])
    declaration['budgets']['total_seconds']=remaining
    declaration['implementation_fix']=dict(generator=descriptor(inputs),preparation_helper=descriptor(Path(__file__)),
        input_cleanup_only=True,no_completed_map_reused=True)
    dump_json(work/'declaration.json',declaration)
    print(json.dumps(dict(declaration=descriptor(work/'declaration.json'),output=str(output),
        prior_elapsed_wall_seconds=prior_wall,remaining_case_wall_seconds=remaining),indent=2))


if __name__=='__main__':main()
