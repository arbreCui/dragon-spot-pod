"""Declare a fresh full coupled AAA/ABA conditional angular-model trial.

The receiver changes an approximate angular operator, not nuclear inputs or
accuracy gates. Cold-state numerical admission cannot substitute for either
the fresh coupled fixed point or the independent original-rule AAA gate.
"""
import argparse
import ast
import copy
import difflib
import json
import math
from pathlib import Path
import shutil
import struct
import sys
import time

sys.dont_write_bytecode=True
import audit_AAA_white_trace_saved_states as audit
base=audit.base
ROOT,ART,OLD=base.ROOT,base.ART,base.PROD
SOURCE=ART / 'axial-material-qualified-AB-white-trace-admission-20261004'
OUTPUT=ART / 'axial-material-production-qualified-AB-white-trace-20261004'
TOOLS=ROOT / 'validation/axial_material'


def replace_once(text,old,new):
    if text.count(old)!=1:raise ValueError('ambiguous receiver integration anchor: '+old[:80])
    return text.replace(old,new,1)


RUNTIME_ADMISSION='''    variant_path = Path(__file__).with_name("conditional_white_receiver_variant.json")
    variant = json.loads(require_file(variant_path).read_text())
    if variant.get("schema") != "AXMAT_CONDITIONAL_WHITE_TRACE_RECEIVER_VARIANT_V1":
        raise Refusal("explicit conditional angular receiver variant required")
    if variant.get("coefficients_fitted_to_CE") is not False or variant.get("ideal_angular_operator_changed") is not True:
        raise Refusal("conditional angular model scope differs")
    for filename, wanted in variant["files"].items():
        require_file(Path(filename), wanted)
    parent_item = variant["parent_compensated_variant"]
    parent = json.loads(require_file(Path(parent_item["path"]), parent_item["sha256"]).read_text())
    if parent.get("schema") != "AXMAT_COMPENSATED_FLIGHT_RECEIVER_VARIANT_V1":
        raise Refusal("unchanged parent compensated flight implementation required")
    replay = parent["replay_admission"]
    report = json.loads(require_file(Path(replay["path"]), replay["sha256"]).read_text())
    if report["classification"] != "COMPENSATED_RADIAL_REPLAY_RETURNED_AND_ADMITTED":
        raise Refusal("parent compensated radial replay was not admitted")
    saved_item = variant["saved_state_original_accounting_audit"]
    saved = json.loads(require_file(Path(saved_item["path"]), saved_item["sha256"]).read_text())
    if (saved["classification"] != "PASS_SAVED_COLD_STATES_AT_ORIGINAL_ACCOUNTING_RULES_ONLY"
            or saved["original_controller_rejection_preserved"] is not True
            or saved["native_run_repeated"] is not False
            or saved["new_coupled_map"] is not False):
        raise Refusal("separate original-rule cold-state accounting audit required")
    for case in ("off", "on"):
        if any(value != "PASS" for value in saved["states"][case]["current_checks"].values()):
            raise Refusal("cold-state original current checks failed")
    cold_item = variant["cold_controller_result"]
    cold = json.loads(require_file(Path(cold_item["path"]), cold_item["sha256"]).read_text())
    if (cold["classification"] != "FAILED_CONDITIONAL_WHITE_TRACE_NATIVE_NO_RETRY"
            or cold["error"] != "ValueError('saved scalar/current admission failed')"
            or cold["off_compatibility"]["relative_k"] != 0
            or cold["off_compatibility"]["max_relative_scalar_group_flux"] != 0
            or cold["compiled_kernel"]["status"] != "PASS_COMPILED_WHITE_KERNEL_ONLY"
            or cold["native_application"]["groups"] != 370):
        raise Refusal("original rejected controller and exact OFF control must be preserved")
    item = variant["candidate_runtime"]
    if item["sha256"] != DRAGON_SHA:
        raise Refusal("conditional receiver identity differs")
    require_file(Path(item["path"]), item["sha256"], True)
    result["Dragon"] = item
    marker = variant["white_tracking_host"]
    require_file(Path(marker["path"]), marker["sha256"], True)
    result["white_tracking"] = marker
    return result'''


def main():
    info,_=base.prepared()
    audit_decl=json.loads((audit.OUT / 'declaration.json').read_text())
    audit.check(base.digest(audit.OUT / 'declaration.json'))
    saved=json.loads((audit.OUT / 'result.json').read_text())
    driver=json.loads((audit.OUT / 'driver_result.json').read_text())
    base.require_file(Path(driver['result']['path']),driver['result']['sha256'])
    if saved['classification']!='PASS_SAVED_COLD_STATES_AT_ORIGINAL_ACCOUNTING_RULES_ONLY' or saved['AAA_accuracy_qualified']:
        raise ValueError('numerically admitted cold states without accuracy promotion required')
    cold=audit.control.OUT
    binary=base.pin(cold / 'runtime/Dragon')
    identity=json.loads((cold / 'build_identity.json').read_text())
    if binary!=identity['binaries']['Dragon']:raise ValueError('actual compiled receiver differs')
    native_cold=json.loads((cold / 'result.json').read_text())
    previous_status=json.loads((OLD / 'AAA/run_status.json').read_text())
    previous_claim=json.loads((OLD / 'AAA/run_claim.json').read_text())
    charged_previous=math.ceil(previous_status['finished_unix']-previous_claim['started_unix'])
    charged_diagnostic=json.loads((cold / 'declaration.json').read_text())['wall_seconds']
    remaining=info['budgets']['total_seconds']-charged_previous-charged_diagnostic
    if remaining<=0:raise ValueError('remaining declared case budget exhausted')
    existing_roots=sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir())
    current=base.DiskResources(ART,existing_roots,8*2**30,40*2**30).check()
    prior_size=base.DiskResources(ART,[str(OLD)],8*2**30,40*2**30).check()['artifact_bytes']
    # Two fresh cases plus 50% storage headroom, with preserved prior archives.
    projected=current['artifact_bytes']+3*prior_size+2*2**30
    if projected>40*2**30:raise ValueError('conservative full-case storage forecast exceeds new bound')
    SOURCE.mkdir(exist_ok=False)
    names=['production_runner.py','production_inputs.py','snapshot_control_preflight.py','qualified_snapshot_ingestion.py',
        'analyze_r64_snapshot.py','analyze_r64_tracking_moments.py','check_r64_audit_rejections.py','check_r64_normalization_rejections.py']
    for name in names:shutil.copy2(OLD / 'runtime' / name,SOURCE / name)
    shutil.copy2(TOOLS / 'white_receiver_tracking.py',SOURCE / 'white_receiver_tracking.py')
    base.write_new(SOURCE / 'resource_addendum.json',dict(schema='AXMAT_CONDITIONAL_WHITE_FULL_TRIAL_RESOURCE_V1',
        declared_unix=time.time(),old_storage_budget_GiB=24,new_storage_budget_GiB=40,min_free_GiB=8,
        current_regular_file_bytes=current['artifact_bytes'],parent_full_case_regular_file_bytes=prior_size,
        forecast_regular_file_bytes=projected,forecast_policy='Existing immutable history plus two fresh cases at 1.5 times the measured parent full-case size, plus 2 GiB for further independent reference statistics. Runtime monitor still fails closed at the declared bound.',
        old_case_wall_seconds=info['budgets']['total_seconds'],previous_AAA_seconds_charged=charged_previous,
        native_diagnostic_full_cap_seconds_charged=charged_diagnostic,new_case_wall_seconds=remaining,
        threads=1,numeric_children_at_once=1,retries=0,original_max_maps_unchanged=info['budgets']['max_maps'],
        physical_or_accuracy_thresholds_changed=False,old_sealed_caps_changed=False,resources_before=current))
    files=[Path(__file__).resolve(),TOOLS / 'white_receiver_tracking.py',SOURCE / 'resource_addendum.json',
        cold / 'declaration.json',cold / 'result.json',cold / 'kernel_receipt.json',cold / 'build_identity.json',
        audit.OUT / 'declaration.json',audit.OUT / 'result.json',audit.OUT / 'driver_result.json',
        audit.control.ALGEBRA / 'declaration.json',audit.control.ALGEBRA / 'result.json',
        OLD / 'prepared.json',OLD / 'runtime/numerical_receiver_variant.json',
        *[Path(name) for name in audit_decl['files']]]
    variant=dict(schema='AXMAT_CONDITIONAL_WHITE_TRACE_RECEIVER_VARIANT_V1',candidate_runtime=binary,
        parent_compensated_variant=base.pin(OLD / 'runtime/numerical_receiver_variant.json'),
        cold_controller_result=base.pin(cold / 'result.json'),original_controller_rejection_preserved=True,
        saved_state_original_accounting_audit=base.pin(audit.OUT / 'result.json'),
        white_tracking_host=base.pin(cold / 'runtime/tracking'),ideal_angular_operator_changed=True,
        coefficients_fitted_to_CE=False,offline_r64_directly_consumed_by_boot=False,
        model='Fixed geometry P/(pi*A) conservative angular exchange, constant outer-sodium trace from the same rank1 basis, uniform transverse azimuth. Conditional approximate operator; not an exact heterogeneous 3D boundary trace.',
        native_model_scope=dict(radial_regions=8,axial_cells=12,snapshots=3,rank=1,SN=8,SCAT=3,diamond_order=0,
            white_trace_row=1,physical_perimeter_cm=6*.61776479,axial_boundary='original vacuum'),
        full_trial_required=True,AAA_accuracy_qualified=False,ABA_admitted=False,shared_solver_promoted=False,
        files={str(p.resolve()):base.digest(p) for p in files})
    base.write_new(SOURCE / 'conditional_white_receiver_variant.json',variant)
    runner=SOURCE / 'production_runner.py'
    original=runner.read_text()
    text=replace_once(original,'DRAGON_SHA = "'+info['runtime_sources']['Dragon']['sha256']+'"','DRAGON_SHA = "'+binary['sha256']+'"')
    start=text.index('    variant_path = Path(__file__).with_name("numerical_receiver_variant.json")')
    end=text.index('    return result',start)+len('    return result')
    text=text[:start]+RUNTIME_ADMISSION+text[end:]
    text=replace_once(text,'    shutil.copy2(Path(__file__).with_name("numerical_receiver_variant.json"), runtime / "numerical_receiver_variant.json")',
        '    shutil.copy2(Path(__file__).with_name("conditional_white_receiver_variant.json"), runtime / "conditional_white_receiver_variant.json")\n    shutil.copy2(Path(__file__).with_name("white_receiver_tracking.py"), runtime / "white_receiver_tracking.py")')
    before='        deck(setup, "case_setup.x2m", budget.setup_seconds, "AXMAT-CASE-SETUP-COMPLETE")\n        host(setup, "make_route_contract", config.contract_arguments(case))'
    after='''        deck(setup, "case_setup.x2m", budget.setup_seconds, "AXMAT-CASE-SETUP-COMPLETE")
        # Only this fresh, unsealed generated TRACK gains the declared markers.
        unmarked = setup / "initial_axial_track_unmarked.xsm"
        if unmarked.exists():
            raise Refusal("existing unmarked tracking output; no overwrite")
        (setup / "initial_axial_track.xsm").rename(unmarked)
        host(setup, "white_tracking", ["initial_axial_track_unmarked.xsm", "initial_axial_track.xsm"],
             "AXMAT-WHITE-TRACKING-COMPLETE")
        from white_receiver_tracking import verify_white_tracking_copy
        marker_admission = verify_white_tracking_copy(unmarked, setup / "initial_axial_track.xsm")
        dump_json(setup / "white_tracking_admission.json", marker_admission)
        host(setup, "make_route_contract", config.contract_arguments(case))'''
    text=replace_once(text,before,after)
    ast.parse(text)
    runner.write_text(text)
    (SOURCE / 'production_runner.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),text.splitlines(True),fromfile='parent-frozen-runner',tofile='conditional-angular-model-runner')))
    ingestion=SOURCE / 'qualified_snapshot_ingestion.py'
    original=ingestion.read_text()
    text=replace_once(original,"ONLINE_SHA = '"+info['runtime_sources']['Dragon']['sha256']+"'","ONLINE_SHA = '"+binary['sha256']+"'")
    ingestion.write_text(text)
    (SOURCE / 'qualified_snapshot_ingestion.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),text.splitlines(True),fromfile='parent-frozen-ingestion',tofile='same-ingress-new-axial-receiver')))
    receipt=json.loads(Path(info['inputs']['material_results']['path']).read_text())
    receipt.update(online_receiver_sha256=binary['sha256'],conditional_white_receiver_variant=base.pin(SOURCE / 'conditional_white_receiver_variant.json'),
        scope='Same qualified offline producers and unchanged legacy BOOT ingress, with REAL32 mirror promotion once. The separate receiver adds a declared approximate angular white trace only in axial FLU; a new complete coupled run and independent AAA qualification remain required.')
    base.write_new(SOURCE / 'producer_ingestion_receipt.json',receipt)
    spec=json.loads(Path(info['case_spec']['path']).read_text())
    spec['experiment_id']='axial-material-qualified-AB-rank1-white-trace-20261004'
    spec['status']='PREDECLARED_CONDITIONAL_WHITE_TRACE_COUPLED_TRIAL'
    spec['production']['implementation']='Separate conservative conditional side-white angular trace receiver, SHA256 '+binary['sha256']
    spec['resource_caps']['total_wall_s_per_spot_case']=remaining
    spec['resource_caps']['new_case_artifact_budget_GiB']=40
    spec['qualified_snapshot_producers'].update(receiver_sha256=binary['sha256'],receipt=base.pin(SOURCE / 'producer_ingestion_receipt.json'))
    spec['conditional_white_trace_trial']=dict(variant=base.pin(SOURCE / 'conditional_white_receiver_variant.json'),
        resource_addendum=base.pin(SOURCE / 'resource_addendum.json'),physical_inputs_changed=False,
        original_scientific_thresholds_changed=False,approximate_angular_operator_changed=True,coefficients_fitted_to_CE=False,
        fresh_bootstrap_and_completed_maps=True,reused_completed_maps=False,original_controller_failure_preserved=True,
        scope='Full fresh AAA numerical trial, then unchanged strict independent AAA guard before ABA. Cold-state numerical checks and reference sample means do not qualify accuracy.')
    base.write_new(SOURCE / 'case_spec.json',spec)
    rank=json.loads(Path(info['rank_addendum']['path']).read_text())
    rank.update(case_spec_sha256=base.digest(SOURCE / 'case_spec.json'),experiment_id=spec['experiment_id'])
    base.write_new(SOURCE / 'rank_addendum.json',rank)
    declaration=json.loads((OLD / 'declaration.json').read_text())
    declaration.update(experiment_id=spec['experiment_id'],case_spec=base.pin(SOURCE / 'case_spec.json'),rank_addendum=base.pin(SOURCE / 'rank_addendum.json'),
        resource_roots=existing_roots+[str(SOURCE),str(OUTPUT)],conditional_white_receiver_variant=base.pin(SOURCE / 'conditional_white_receiver_variant.json'),
        helper=base.pin(Path(__file__)))
    declaration.pop('numerical_receiver_variant',None)
    declaration['inputs']['material_results']=base.pin(SOURCE / 'producer_ingestion_receipt.json')
    declaration['budgets']['total_seconds']=remaining
    base.write_new(SOURCE / 'declaration.json',declaration)
    # Verify only explicitly declared metadata/model/resource fields changed.
    restored=copy.deepcopy(spec);parent=json.loads(Path(info['case_spec']['path']).read_text())
    for key in ('experiment_id','status'):restored[key]=parent[key]
    restored['production']['implementation']=parent['production']['implementation']
    restored['resource_caps']=parent['resource_caps']
    restored['qualified_snapshot_producers']=parent['qualified_snapshot_producers']
    del restored['conditional_white_trace_trial']
    if restored!=parent:raise ValueError('undeclared physical or accuracy field changed')
    base.write_new(SOURCE / 'input_and_gate_equivalence.json',dict(status='PASS_ONLY_DECLARED_RECEIVER_METADATA_AND_RESOURCE_FIELDS',
        parent_case_spec=base.pin(Path(info['case_spec']['path'])),new_case_spec=base.pin(SOURCE / 'case_spec.json'),
        all_other_case_spec_fields_exact=True,new_coupled_map=False,AAA_accuracy_qualified=False))
    print(json.dumps(dict(declaration=base.pin(SOURCE / 'declaration.json'),output=str(OUTPUT),remaining_case_wall_seconds=remaining,
        resource_addendum=base.pin(SOURCE / 'resource_addendum.json'),status='DECLARED_NEW_COUPLED_TRIAL_NOT_RUN'),indent=2))


if __name__=='__main__':main()
