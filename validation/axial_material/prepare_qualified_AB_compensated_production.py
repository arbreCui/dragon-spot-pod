"""Declare a fresh complete AAA/ABA trial with compensated native flight sums."""
import json
import math
from pathlib import Path
import shutil

from production_runner import ROOT,dump_json,require_file,sha256
from qualified_snapshot_ingestion import descriptor


def main():
    art=ROOT/'validation/artifacts'
    old=art/'axial-material-production-qualified-AB-storage-20261004'
    source=art/'axial-material-qualified-AB-storage-admission-20261004'
    candidate=art/'axial-material-AAA-compensated-flight-20261004'
    info=json.loads(require_file(old/'prepared.json','2c7fe827864095bea9ff07781f14ec4292b5c2829c04f5e9eafe4769011dfb17').read_text())
    for name,wanted in info['local_files'].items():require_file(old/name,wanted)
    status=json.loads((candidate/'run_status.json').read_text())
    if status['classification']!='COMPENSATED_RADIAL_REPLAY_RETURNED_AND_ADMITTED' or not status['frozen_inputs_unchanged']:
        raise ValueError('completed and admitted radial contrast required')
    for name,wanted in status['outputs'].items():require_file(candidate/'AAA'/name,wanted)
    if json.loads((candidate/'sum_test/result.json').read_text())['classification']!='PASS_SUBULP_ACCUMULATION_NUMERICAL_TEST':
        raise ValueError('compiled numerical sum check required')
    manifest=json.loads((candidate/'execution.json').read_text())
    for name,wanted in manifest['files'].items():require_file(Path(name),wanted)
    binary=descriptor(candidate/'runtime/Dragon')
    failure=json.loads((old/'AAA/run_status.json').read_text())
    claim=json.loads((old/'AAA/run_claim.json').read_text())
    prior_wall=failure['finished_unix']-claim['started_unix']
    # Charge both diagnostic caps conservatively, including the returned-state host.
    remaining=math.floor(info['budgets']['total_seconds']-prior_wall-300-420)
    work=art/'axial-material-qualified-AB-compensated-admission-20261004'
    output=art/'axial-material-production-qualified-AB-compensated-20261004'
    work.mkdir(exist_ok=False)
    for name in ('production_runner_qualified.py','production_inputs.py','snapshot_control_preflight.py',
                 'qualified_snapshot_ingestion.py','analyze_r64_snapshot.py','analyze_r64_tracking_moments.py',
                 'check_r64_audit_rejections.py','check_r64_normalization_rejections.py'):
        shutil.copy2(source/name,work/name)
    variant=dict(schema='AXMAT_COMPENSATED_FLIGHT_RECEIVER_VARIANT_V1',candidate_runtime=binary,
        parent_runtime=info['runtime_sources']['Dragon'],candidate_execution=descriptor(candidate/'execution.json'),
        replay_admission=descriptor(candidate/'run_status.json'),numerical_sum_test=descriptor(candidate/'sum_test/result.json'),
        original_AAA_failure=descriptor(old/'AAA/run_status.json'),
        scope='Only accumulated native flight contributions and batch sums use compensation; original integrands, material data, flight scheme, source rules, normalizations, ACA, KRYL=10, MAXI=20 and all inner/outer gates are unchanged. Candidate remains separate from the shared and canonical solver.',
        online_boot_ingress_implementation_unchanged=True,offline_r64_directly_consumed_by_boot=False)
    dump_json(work/'numerical_receiver_variant.json',variant)
    runner=work/'production_runner_qualified.py'
    text=runner.read_text().replace('DRAGON_SHA = "873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef"','DRAGON_SHA = "'+binary['sha256']+'"')
    before='    return result\n\n\ndef check_dragon_log'
    after='''    variant_path = Path(__file__).with_name("numerical_receiver_variant.json")
    variant = json.loads(require_file(variant_path).read_text())
    if variant.get("schema") != "AXMAT_COMPENSATED_FLIGHT_RECEIVER_VARIANT_V1":
        raise Refusal("explicit numerical receiver variant required")
    if variant["candidate_runtime"]["sha256"] != DRAGON_SHA:
        raise Refusal("receiver variant identity differs")
    item = variant["candidate_runtime"]
    require_file(Path(item["path"]), item["sha256"], True)
    replay = variant["replay_admission"]
    report = json.loads(require_file(Path(replay["path"]), replay["sha256"]).read_text())
    if report["classification"] != "COMPENSATED_RADIAL_REPLAY_RETURNED_AND_ADMITTED":
        raise Refusal("candidate radial replay was not admitted")
    result["Dragon"] = item
    return result


def check_dragon_log'''
    if text.count(before)!=1:raise ValueError('runtime identity anchor differs')
    text=text.replace(before,after)
    before='    for name in ("qualified_snapshot_ingestion.py", "analyze_r64_snapshot.py",'
    after='    shutil.copy2(Path(__file__).with_name("numerical_receiver_variant.json"), runtime / "numerical_receiver_variant.json")\n'+before
    if text.count(before)!=1:raise ValueError('prepare source anchor differs')
    runner.write_text(text.replace(before,after))
    ingestion=work/'qualified_snapshot_ingestion.py'
    text=ingestion.read_text().replace("ONLINE_SHA = '873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef'","ONLINE_SHA = '"+binary['sha256']+"'")
    ingestion.write_text(text)
    receipt=json.loads(Path(info['inputs']['material_results']['path']).read_text())
    receipt.update(online_receiver_sha256=binary['sha256'],numerical_receiver_variant=descriptor(work/'numerical_receiver_variant.json'),
        scope='Qualified offline producers admitted to the unchanged legacy BOOT ingress of this separately declared compensated-flight receiver. BOOT still promotes exact REAL32 mirrors once; the complete coupled candidate is unqualified before this trial.')
    dump_json(work/'producer_ingestion_receipt.json',receipt)
    spec=json.loads(Path(info['case_spec']['path']).read_text())
    spec['experiment_id']='axial-material-qualified-AB-rank1-compensated-flight-20261004'
    spec['status']='PREDECLARED_FRESH_COMPENSATED_FLIGHT_COUPLED_TRIAL'
    spec['production']['implementation']='Separate compensated native flight receiver, SHA256 '+binary['sha256']
    spec['resource_caps']['total_wall_s_per_spot_case']=remaining
    spec['qualified_snapshot_producers'].update(receiver_sha256=binary['sha256'],receipt=descriptor(work/'producer_ingestion_receipt.json'))
    spec['compensated_flight_trial']=dict(variant=descriptor(work/'numerical_receiver_variant.json'),
        previous_case_wall_seconds=prior_wall,diagnostic_caps_charged_seconds=720,remaining_case_wall_seconds=remaining,
        hypothesis='Uncompensated native term accumulation leaves a small physical-image error amplified by ACA. The targeted replay passed unchanged strict terminals after compensation. A full fresh coupled trial is still required; no irreducible-floor or CE-accuracy claim.',
        changed='Floating-point summation order only; no real-arithmetic operator coefficient change.',
        no_reused_completed_maps=True,source_precision='Unchanged original REAL32 nuclear coefficients and actual quadrature; REAL64 flight fields and compensated totals.',
        scope='Uniform rank1 sensitivity; parent rank2 remains inconclusive. All previous failures remain sealed and unchanged; independent AAA qualification still precedes ABA.')
    dump_json(work/'case_spec.json',spec)
    rank=json.loads(Path(info['rank_addendum']['path']).read_text())
    rank.update(case_spec_sha256=sha256(work/'case_spec.json'),experiment_id=spec['experiment_id'])
    dump_json(work/'rank_addendum.json',rank)
    decl=json.loads((old/'declaration.json').read_text())
    decl.update(experiment_id=spec['experiment_id'],case_spec=descriptor(work/'case_spec.json'),rank_addendum=descriptor(work/'rank_addendum.json'),
        resource_roots=sorted(str(p.resolve()) for p in art.glob('axial-material-*') if p.is_dir())+[str(output)])
    decl['inputs']['material_results']=descriptor(work/'producer_ingestion_receipt.json')
    decl['budgets']['total_seconds']=remaining
    decl['numerical_receiver_variant']=descriptor(work/'numerical_receiver_variant.json')
    decl['arithmetic_trial_helper']=descriptor(Path(__file__))
    dump_json(work/'declaration.json',decl)
    print(json.dumps(dict(declaration=descriptor(work/'declaration.json'),output=str(output),remaining_case_wall_seconds=remaining),indent=2))


if __name__=='__main__':main()
