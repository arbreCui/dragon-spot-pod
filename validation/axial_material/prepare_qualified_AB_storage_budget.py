"""Declare measured evidence-storage headroom, preserving all scientific gates."""
import json
import math
from pathlib import Path
import shutil

from production_runner import ROOT,dump_json,require_file,sha256
from qualified_snapshot_ingestion import descriptor


def main():
    art=ROOT/'validation/artifacts'
    old=art/'axial-material-production-qualified-AB-cleanup-20261004'
    source=art/'axial-material-qualified-AB-cleanup-admission-20261004'
    info=json.loads(require_file(old/'prepared.json','9b32fbde09da4b050b37c38568a9703d3b7d26f69e5313a7a438667a1afbbb04').read_text())
    for name,wanted in info['local_files'].items():require_file(old/name,wanted)
    failure=json.loads((old/'AAA/run_status.json').read_text())
    claim=json.loads((old/'AAA/run_claim.json').read_text())
    if failure['classification']!='FAIL_RESOURCE' or failure['completed_maps']!=0:
        raise ValueError('expected storage-only failed attempt required')
    resource=failure['resources']
    if resource['reason']!='experiment regular-file total exceeds declared artifact budget':
        raise ValueError('unexpected resource failure')
    spent=failure['finished_unix']-claim['started_unix']
    remaining=math.floor(info['budgets']['total_seconds']-spent)
    work=art/'axial-material-qualified-AB-storage-admission-20261004'
    output=art/'axial-material-production-qualified-AB-storage-20261004'
    work.mkdir(exist_ok=False)
    spec=json.loads(Path(info['case_spec']['path']).read_text())
    spec['experiment_id']='axial-material-qualified-AB-rank1-storage-20261004'
    spec['status']='PREDECLARED_STORAGE_RESOURCE_REVISION'
    spec['resource_caps']['new_case_artifact_budget_GiB']=24
    spec['resource_caps']['total_wall_s_per_spot_case']=remaining
    spec['storage_resource_revision']=dict(prior_failure=descriptor(old/'AAA/run_status.json'),
        measured_regular_file_bytes=resource['artifact_bytes'],measured_free_bytes=resource['disk_free_bytes'],
        prior_budget_GiB=12,new_budget_GiB=24,free_space_minimum_GiB=8,
        prior_wall_seconds=spent,remaining_case_wall_seconds=remaining,
        reason='All earlier sealed diagnostic and failed-trial copies remain counted in the disjoint roots. Their accumulated 12.187 GiB exceeded the 12 GiB apparent-byte cap during archive packaging. Additional bounded storage preserves evidence and allows the existing coupled trial to proceed; no scientific outcome is available or relabeled.',
        authority='User authorized automatic execution and routine approvals for the ordered goal; this separately declared bounded storage allocation changes no physical/numerical/statistical gate.')
    dump_json(work/'case_spec.json',spec)
    add=json.loads(Path(info['rank_addendum']['path']).read_text())
    add.update(case_spec_sha256=sha256(work/'case_spec.json'),experiment_id=spec['experiment_id'])
    dump_json(work/'rank_addendum.json',add)
    for name in ('production_runner_qualified.py','production_inputs.py','snapshot_control_preflight.py',
                 'qualified_snapshot_ingestion.py','analyze_r64_snapshot.py','analyze_r64_tracking_moments.py',
                 'check_r64_audit_rejections.py','check_r64_normalization_rejections.py'):
        shutil.copy2(source/name,work/name)
    declaration=json.loads((old/'declaration.json').read_text())
    declaration.update(experiment_id=spec['experiment_id'],case_spec=descriptor(work/'case_spec.json'),
        rank_addendum=descriptor(work/'rank_addendum.json'),
        resource_roots=sorted(str(p.resolve()) for p in art.glob('axial-material-*') if p.is_dir())+[str(output)])
    declaration['budgets']['total_seconds']=remaining
    declaration['storage_revision_helper']=descriptor(Path(__file__))
    dump_json(work/'declaration.json',declaration)
    print(json.dumps(dict(declaration=descriptor(work/'declaration.json'),output=str(output),
        prior_wall_seconds=spent,remaining_case_wall_seconds=remaining,storage_cap_GiB=24),indent=2))


if __name__=='__main__':main()
