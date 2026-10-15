"""Declare a fresh complete 48-cell/SN32 coupled AAA control, then guarded ABA.

The finest studied numerical setting is used without fitting the CE means.
All original physical inputs, coupling gates and independent accuracy gates
remain mandatory. Preparation never launches a transport solve.
"""
import ast
import copy
import difflib
import json
import math
from pathlib import Path
import shutil
import sys
import time

sys.dont_write_bytecode = True
import prepare_AAA_white_trace_angular_convergence as angular

ROOT, ART, OLD = angular.ROOT, angular.ART, angular.PROD
CLOSEOUT = ART / 'axial-material-AAA-white-trace-angular-closeout-20261005'
SOURCE = ART / 'axial-material-qualified-AB-white-trace-refined-admission-20261005'
OUTPUT = ART / 'axial-material-production-qualified-AB-white-trace-refined-20261005'
CLOSEOUT_SHA = 'a5b26a331d3b2dd1d3ebb12b80e63ffb0ca9e9a4aefe65aac244b38eb65a33dc'
ANGULAR_RESULT_SHA = '275b542018d35940159777b57f5f5269b206c3b2f685d0e46e181564b386e0df'
EXPERIMENT = 'axial-material-qualified-AB-rank1-white-trace-refined-20261005'


LAYOUT_HOST = '''"""Strict cold-evidence and common-basis admission for the exact new layout."""
import hashlib
import json
from pathlib import Path

ROOT = Path("/Users/wen/spot/validation/artifacts")
COLD = ROOT / "axial-material-AAA-white-trace-angular-convergence-20261005"
CLOSEOUT = ROOT / "axial-material-AAA-white-trace-angular-closeout-20261005"
SCOPE = dict(radial_regions=8,axial_cells=48,snapshots=3,rank=1,SN=32,SCAT=3,
             diamond_order=0,white_trace_row=1,physical_perimeter_cm=6*.61776479,
             axial_boundary="original vacuum")


def require(path,wanted):
    path = Path(path)
    with path.open("rb") as stream:
        actual = hashlib.file_digest(stream,"sha256").hexdigest()
    if actual != wanted:
        raise ValueError("refined layout evidence changed: "+str(path))
    return path


def admit_layout_variant(variant):
    revision = variant.get("numerical_layout_revision",{})
    if (revision.get("schema") != "AXMAT_REFINED_WHITE_48_SN32_LAYOUT_V1"
            or variant.get("native_model_scope") != SCOPE
            or revision.get("same_analytic_white_formula_as_parent") is not True
            or revision.get("physical_inputs_changed") is not False
            or revision.get("original_thresholds_changed") is not False
            or revision.get("full_coupling_required") is not True):
        raise ValueError("explicit exact 48-cell/SN32 numerical scope required")
    for name,wanted in variant["files"].items():
        require(name,wanted)
    seal = json.loads(require(CLOSEOUT / "seal.json",
        "a5b26a331d3b2dd1d3ebb12b80e63ffb0ca9e9a4aefe65aac244b38eb65a33dc").read_text())
    for name,wanted in seal["files"].items():
        require(CLOSEOUT / name,wanted)
    cold = json.loads(require(COLD / "result.json",
        "275b542018d35940159777b57f5f5269b206c3b2f685d0e46e181564b386e0df").read_text())
    if (cold["classification"] != "COMPLETE_WHITE_TRACE_FROZEN_ANGULAR_SENSITIVITY_ONLY"
            or cold["error"] is not None or cold["completed_new_cases"] != ["cold48_sn16","cold48_sn32"]
            or any(cold[k] for k in ("AAA_accuracy_qualified","ABA_admitted","shared_solver_promoted"))):
        raise ValueError("complete unpromoted cold numerical evidence required")
    if not cold["original_SN8_kernel"]["original_SN8_matrix_byte_exact"]:
        raise ValueError("same original compiled SN8 operator required")
    for case in ("cold48_sn16","cold48_sn32"):
        saved = json.loads((COLD / case / "saved_state_admission.json").read_text())
        if (any(v != "PASS" for v in saved["checks"].values())
                or not saved["all_group_scalar_entries_positive"]
                or saved["saved_scalar_entries"] != 142080):
            raise ValueError("original complete saved numerical checks required")
        kernel = json.loads((COLD / case / "kernel_receipt.json").read_text())
        if kernel["status"] != "PASS_COMPILED_UNCHANGED_ANGULAR_FORMULA_AND_CONTROLS" or kernel["malformed_controls_rejected"] != 8:
            raise ValueError("actual compiled formula and negative controls required")
    return dict(status="PASS_EXACT_NUMERICAL_LAYOUT_ONLY",scope=SCOPE,
                independent_accuracy_qualified=False,ABA_admitted=False)


def verify_common_basis(path):
    from snapshot_control_preflight import _open_xsm
    expected = COLD / "cold48_sn32/basis.xsm"
    count = 0
    with _open_xsm(expected) as old,_open_xsm(Path(path)) as new:
        active = set()
        def walk(previous,actual):
            nonlocal count
            if set(previous) != set(actual):
                raise ValueError("refined common basis record names changed")
            for name,p in previous.items():
                n = actual[name]
                if p[1:] != n[1:]:
                    raise ValueError("refined common basis type/length changed: "+name)
                if p[2] == 0:
                    pair = (p[0],n[0])
                    if pair in active:
                        raise ValueError("cyclic basis directory")
                    active.add(pair);walk(old.directory(p[0]),new.directory(n[0]));active.remove(pair)
                elif p[2] == 10:
                    for a,b in zip(old.integers(p[0],p[1]),new.integers(n[0],n[1]),strict=True):
                        pair = (a,b)
                        if pair in active:
                            raise ValueError("cyclic basis list")
                        active.add(pair);walk(old.directory(a),new.directory(b));active.remove(pair)
                else:
                    if old.read(p[0],p[1]) != new.read(n[0],n[1]):
                        raise ValueError("refined common basis words changed: "+name)
                    count += 1
        walk(old.root,new.root)
    if count < 3330:
        raise ValueError("incomplete common basis record verification")
    return dict(status="PASS_ALL_COMMON_BASIS_RECORD_WORDS_EXACT",records_verified=count,
        expected=str(expected),actual=str(Path(path)),storage_unknowns=1800,
        scope="Same frozen A/B/A basis data, with only the previously admitted storage word. "
              "No fitted, locally normalized or independently retrained case basis.")
'''


def patch_text(original,replacements):
    text = original
    for old,new in replacements:
        text = angular.mesh.replace_once(text,old,new)
    restored = text
    for old,new in reversed(replacements):
        restored = angular.mesh.replace_once(restored,new,old)
    if restored != original:
        raise ValueError('source changed beyond declared integration anchors')
    return text


def ready():
    info,final = angular.ready()
    angular.mesh.require_file(angular.OUT / 'result.json',ANGULAR_RESULT_SHA)
    angular.mesh.require_file(CLOSEOUT / 'seal.json',CLOSEOUT_SHA)
    seal = angular.read(CLOSEOUT / 'seal.json')
    for name,wanted in seal['files'].items():
        angular.mesh.require_file(CLOSEOUT / name,wanted)
    if angular.read(CLOSEOUT / 'result.json')['classification'] != 'COMPLETE_COLD_ANGULAR_CLOSEOUT_UNQUALIFIED':
        raise ValueError('completed original-rule angular closeout required')
    return info,final


def main():
    info,final = ready()
    binary = angular.mesh.base.pin(angular.OUT / 'runtime/Dragon')
    marker = angular.mesh.base.pin(angular.OUT / 'runtime/tracking')
    identity = angular.read(angular.OUT / 'build_identity.json')
    if binary != identity['binaries']['Dragon'] or marker != identity['binaries']['tracking']:
        raise ValueError('actual compiled extended-scope receiver identity differs')
    SOURCE.mkdir(exist_ok=False)
    names = ['production_runner.py','production_inputs.py','snapshot_control_preflight.py',
        'qualified_snapshot_ingestion.py','analyze_r64_snapshot.py','analyze_r64_tracking_moments.py',
        'check_r64_audit_rejections.py','check_r64_normalization_rejections.py']
    for name in names:
        shutil.copy2(OLD / 'runtime' / name,SOURCE / name)
    (SOURCE / 'numerical_layout_admission.py').write_text(LAYOUT_HOST)
    old_tracking = (OLD / 'runtime/white_receiver_tracking.py').read_text()
    tracking = patch_text(old_tracking,[('!=(8,12,3,1,8,3)','!=(8,48,3,1,32,3)')])
    (SOURCE / 'white_receiver_tracking.py').write_text(tracking)
    (SOURCE / 'white_receiver_tracking.patch').write_text(''.join(difflib.unified_diff(
        old_tracking.splitlines(True),tracking.splitlines(True),fromfile='parent-tracking',tofile='exact-48-SN32-tracking')))
    runner = SOURCE / 'production_runner.py'
    original = runner.read_text()
    replacements = [
        ('DRAGON_SHA = "'+info['runtime_sources']['Dragon']['sha256']+'"',
         'DRAGON_SHA = "'+binary['sha256']+'"'),
        ('    parent_item = variant["parent_compensated_variant"]',
         '    from numerical_layout_admission import admit_layout_variant\n'
         '    admit_layout_variant(variant)\n    parent_item = variant["parent_compensated_variant"]'),
        ('    shutil.copy2(Path(__file__).with_name("white_receiver_tracking.py"), runtime / "white_receiver_tracking.py")',
         '    shutil.copy2(Path(__file__).with_name("white_receiver_tracking.py"), runtime / "white_receiver_tracking.py")\n'
         '    shutil.copy2(Path(__file__).with_name("numerical_layout_admission.py"), runtime / "numerical_layout_admission.py")'),
        ('    if data.get("classification") != "PREPARED_NO_TRANSPORT":',
         '    from numerical_layout_admission import admit_layout_variant\n'
         '    layout_variant = json.loads(require_file(prepared.parent / "runtime/conditional_white_receiver_variant.json").read_text())\n'
         '    admit_layout_variant(layout_variant)\n    if data.get("classification") != "PREPARED_NO_TRANSPORT":'),
        ('        common_sha = sha256(common)\n        result["common_basis_sha256"] = common_sha',
         '        common_sha = sha256(common)\n'
         '        from numerical_layout_admission import verify_common_basis\n'
         '        basis_words = verify_common_basis(common)\n'
         '        dump_json(directory / "numerical_layout_basis_admission.json", basis_words)\n'
         '        result["common_basis_sha256"] = common_sha')]
    text = patch_text(original,replacements)
    old_ast,new_ast = ast.parse(original),ast.parse(text)
    allowed = {'pinned_runtime_files','prepare','verify_prepared','run'}
    old_functions = {n.name:ast.dump(n,include_attributes=False) for n in old_ast.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    new_functions = {n.name:ast.dump(n,include_attributes=False) for n in new_ast.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    if set(old_functions) != set(new_functions) or any(old_functions[n] != new_functions[n] for n in old_functions if n not in allowed):
        raise ValueError('original controller, child supervisor or scientific admission changed')
    runner.write_text(text)
    (SOURCE / 'production_runner.patch').write_text(''.join(difflib.unified_diff(
        original.splitlines(True),text.splitlines(True),fromfile='frozen-white-controller',tofile='numerical-layout-controller')))
    ingestion = SOURCE / 'qualified_snapshot_ingestion.py'
    old_ingestion = ingestion.read_text()
    new_ingestion = patch_text(old_ingestion,[
        ("ONLINE_SHA = '"+info['runtime_sources']['Dragon']['sha256']+"'",
         "ONLINE_SHA = '"+binary['sha256']+"'")])
    ingestion.write_text(new_ingestion)
    (SOURCE / 'qualified_snapshot_ingestion.patch').write_text(''.join(difflib.unified_diff(
        old_ingestion.splitlines(True),new_ingestion.splitlines(True),fromfile='parent-ingestion',tofile='same-ingress-refined-receiver')))
    roots = sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir())+[str(OUTPUT)]
    resources = angular.mesh.DiskResources(ART,roots,8*2**30,96*2**30)
    before = resources.check()
    parent_bytes = sum(p.stat().st_size for p in OLD.rglob('*') if p.is_file() and not p.is_symlink())
    parent_maps = angular.read(OLD / 'AAA/run_status.json')['cases']['AAA']['completed_maps']
    new_axial_bytes = (angular.OUT / 'cold48_sn32/axial.xsm').stat().st_size
    old_axial_bytes = (final / 'candidate_axial.xsm').stat().st_size
    # Four stored axial states per epoch plus bootstrap, with 50% growth margin.
    axial_growth = math.ceil(1.5*4*(parent_maps+1)*max(0,new_axial_bytes-old_axial_bytes))
    estimated_refined_case = parent_bytes+axial_growth
    forecast = before['artifact_bytes']+3*estimated_refined_case+16*2**30
    if forecast > 96*2**30 or forecast-before['artifact_bytes'] > before['disk_free_bytes']-8*2**30:
        raise ValueError('conservative two-case/reference storage forecast exceeds new bound or free space')
    angular.mesh.base.write_new(SOURCE / 'resource_addendum.json',dict(
        schema='AXMAT_WHITE_REFINED_FULL_TRIAL_RESOURCE_V1',declared_unix=time.time(),
        prior_storage_budget_GiB=40,new_storage_budget_GiB=96,min_free_GiB=8,
        resources_before=before,parent_completed_maps=parent_maps,parent_full_case_bytes=parent_bytes,
        measured_old_axial_state_bytes=old_axial_bytes,measured_refined_axial_state_bytes=new_axial_bytes,
        refined_axial_growth_reservation_bytes=axial_growth,estimated_refined_case_bytes=estimated_refined_case,
        forecast_regular_file_bytes=forecast,independent_reference_reservation_bytes=16*2**30,
        forecast_policy='All existing immutable history plus two fresh refined cases at 1.5 times the measured '
                        'parent full-case footprint, augmented by measured axial-state growth with 50% margin; '
                        'reserve 16 GiB for a later independent ABA reference. Fail closed at the fixed cap.',
        prior_full_AAA_calendar_seconds=angular.read(OLD / 'AAA/run_status.json')['finished_unix']-
            angular.read(OLD / 'AAA/run_claim.json')['started_unix'],
        completed_mesh_elapsed_seconds=angular.read(angular.MESH / 'result.json')['elapsed_seconds'],
        completed_angular_elapsed_seconds=angular.read(angular.OUT / 'result.json')['elapsed_seconds'],
        measured_refined_cold_solve_seconds=2532.7542030839977,
        new_case_wall_seconds=43200,new_axial_child_seconds=4200,
        wall_policy='The fresh total cap exceeds seventeen measured refined cold-solve durations; '
                    'all radial, host and setup stages share that same deadline. The prior eleven-map '
                    'case is a planning observation only. This is a maximum, not an ETA or convergence guarantee. '
                    'All previous claims, caps, results and elapsed work remain preserved.',
        original_max_maps=100,threads=1,numeric_children_at_once=1,retries=0,
        physical_inputs_or_scientific_thresholds_changed=False,old_sealed_caps_changed=False,
        authority='User-authorized automatic execution and routine approvals for the ordered goal; '
                  'this new numerical refinement has separately frozen resource bounds.'))
    old_variant = angular.read(OLD / 'runtime/conditional_white_receiver_variant.json')
    variant = copy.deepcopy(old_variant)
    files = dict(old_variant['files'])
    cold_decl = angular.read(angular.OUT / 'declaration.json')
    files.update(cold_decl['files'])
    files.update({str(angular.OUT / n):h for n,h in angular.read(angular.OUT / 'result.json')['outputs'].items()})
    extra = [Path(__file__).resolve(),angular.OUT / 'declaration.json',angular.OUT / 'run_claim.json',
        angular.OUT / 'result.json',CLOSEOUT / 'seal.json',
        *[CLOSEOUT / n for n in angular.read(CLOSEOUT / 'seal.json')['files']],
        ROOT / 'validation/iterative/make_route_contract.f90',ROOT / 'validation/iterative/check_one_map_xsm.f90',
        *[p for p in SOURCE.iterdir() if p.is_file()]]
    files.update({str(p.resolve()):angular.mesh.base.digest(p) for p in extra})
    for name,wanted in files.items():
        angular.mesh.require_file(Path(name),wanted)
    variant.update(candidate_runtime=binary,white_tracking_host=marker,files=files,
        native_model_scope=dict(radial_regions=8,axial_cells=48,snapshots=3,rank=1,SN=32,SCAT=3,
            diamond_order=0,white_trace_row=1,physical_perimeter_cm=6*.61776479,axial_boundary='original vacuum'),
        numerical_layout_revision=dict(schema='AXMAT_REFINED_WHITE_48_SN32_LAYOUT_V1',
            same_analytic_white_formula_as_parent=True,physical_inputs_changed=False,
            original_thresholds_changed=False,full_coupling_required=True,
            parent_variant=angular.mesh.base.pin(OLD / 'runtime/conditional_white_receiver_variant.json'),
            completed_angular_closeout=angular.mesh.base.pin(CLOSEOUT / 'seal.json'),
            choice='Finest setting of the completed predeclared grid/order studies. '
                   'Not chosen by smaller CE discrepancy; no coefficient or threshold is fitted.'))
    angular.mesh.base.write_new(SOURCE / 'conditional_white_receiver_variant.json',variant)
    receipt = angular.read(Path(info['inputs']['material_results']['path']))
    old_receipt = copy.deepcopy(receipt)
    receipt.update(online_receiver_sha256=binary['sha256'],
        conditional_white_receiver_variant=angular.mesh.base.pin(SOURCE / 'conditional_white_receiver_variant.json'),
        scope='Same independently qualified offline A/B producers, unchanged physical material data and '
              'legacy REAL32 BOOT mirror promotion once. Only the online axial numerical layout is refined; '
              'complete coupled convergence and independent original-rule accuracy are still required.')
    angular.mesh.base.write_new(SOURCE / 'producer_ingestion_receipt.json',receipt)
    parent_spec = angular.read(Path(info['case_spec']['path']))
    spec = copy.deepcopy(parent_spec)
    spec.update(experiment_id=EXPERIMENT,status='PREDECLARED_REFINED_WHITE_TRACE_COUPLED_TRIAL')
    spec['geometry']['cells_per_zone'] = 16
    spec['production']['sn'] = 32
    spec['production']['implementation'] = 'Same conditional white trace formula and compensated radial flight, refined numerical scope; SHA256 '+binary['sha256']
    spec['resource_caps'].update(axial_wall_s=4200,total_wall_s_per_spot_case=43200,new_case_artifact_budget_GiB=96)
    spec['qualified_snapshot_producers'].update(receiver_sha256=binary['sha256'],
        receipt=angular.mesh.base.pin(SOURCE / 'producer_ingestion_receipt.json'))
    spec['conditional_white_trace_trial'].update(
        variant=angular.mesh.base.pin(SOURCE / 'conditional_white_receiver_variant.json'),
        resource_addendum=angular.mesh.base.pin(SOURCE / 'resource_addendum.json'),
        scope='Fresh complete 48-cell/SN32 AAA control with the same approximate analytic white model; '
              'unchanged strict independent AAA qualification is mandatory before ABA.')
    spec['numerical_refinement_trial'] = dict(physical_inputs_changed=False,original_thresholds_changed=False,
        same_common_A_B_A_training_inputs=True,same_analytic_angular_formula=True,
        fresh_bootstrap_and_maps_required=True,reused_completed_maps=False,
        native_scope_only_extended_to_declared_mesh_and_orders=True,
        original_observation_bins=12,comparison='Complete fine-cell integrals must be mapped conservatively '
            'into the same original physical observation bins. No local normalization or bin removal.',
        source_closeout=angular.mesh.base.pin(CLOSEOUT / 'seal.json'),
        reference_reuse='A retained complete independent AAA reference can be assessed only after exact '
            'physical-input and observation-bin equivalence, with all original statistical and accuracy rules. '
            'No new CE source sample or accuracy qualification is implied by this declaration.')
    angular.mesh.base.write_new(SOURCE / 'case_spec.json',spec)
    rank = angular.read(Path(info['rank_addendum']['path']))
    rank.update(case_spec_sha256=angular.mesh.base.digest(SOURCE / 'case_spec.json'),experiment_id=EXPERIMENT)
    angular.mesh.base.write_new(SOURCE / 'rank_addendum.json',rank)
    declaration = angular.read(OLD / 'declaration.json')
    config = copy.deepcopy(declaration['production_config'])
    config.update(cells_per_zone=16,sn=32)
    budget = copy.deepcopy(declaration['budgets'])
    budget.update(axial_seconds=4200,bootstrap_axial_seconds=4200,total_seconds=43200)
    declaration.update(experiment_id=EXPERIMENT,production_config=config,budgets=budget,
        case_spec=angular.mesh.base.pin(SOURCE / 'case_spec.json'),
        rank_addendum=angular.mesh.base.pin(SOURCE / 'rank_addendum.json'),resource_roots=roots,
        conditional_white_receiver_variant=angular.mesh.base.pin(SOURCE / 'conditional_white_receiver_variant.json'),
        helper=angular.mesh.base.pin(Path(__file__)),
        numerical_refinement='Fresh finest-studied full coupled AAA, then original eight-gate guard before ABA.')
    declaration['inputs']['material_results'] = angular.mesh.base.pin(SOURCE / 'producer_ingestion_receipt.json')
    angular.mesh.base.write_new(SOURCE / 'declaration.json',declaration)
    restored = copy.deepcopy(spec)
    for key in ('experiment_id','status','resource_caps','qualified_snapshot_producers','conditional_white_trace_trial'):
        restored[key] = parent_spec[key]
    restored['geometry']['cells_per_zone'] = parent_spec['geometry']['cells_per_zone']
    restored['production']['sn'] = parent_spec['production']['sn']
    restored['production']['implementation'] = parent_spec['production']['implementation']
    del restored['numerical_refinement_trial']
    if restored != parent_spec:
        raise ValueError('undeclared physical or scientific gate changed')
    restored_receipt = copy.deepcopy(receipt)
    for key in ('online_receiver_sha256','conditional_white_receiver_variant','scope'):
        restored_receipt[key] = old_receipt[key]
    if restored_receipt != old_receipt:
        raise ValueError('offline producer evidence or material state changed')
    angular.mesh.base.write_new(SOURCE / 'input_and_gate_equivalence.json',dict(
        status='PASS_ONLY_DECLARED_NUMERICAL_LAYOUT_METADATA_AND_RESOURCE_FIELDS',
        parent_case_spec=angular.mesh.base.pin(Path(info['case_spec']['path'])),
        candidate_case_spec=angular.mesh.base.pin(SOURCE / 'case_spec.json'),
        all_other_case_spec_fields_exact=True,offline_material_and_producer_records_exact=True,
        original_controller_functions_AST_exact=sorted(set(old_functions)-allowed),
        original_changed_function_text_restored_exactly=True,
        original_qualify_aba_AST_exact=old_functions['qualify_aba']==new_functions['qualify_aba'],
        AAA_accuracy_qualified=False,ABA_admitted=False,new_coupled_map=False))
    print(json.dumps(dict(status='DECLARED_FRESH_REFINED_COUPLED_TRIAL_NOT_RUN',
        declaration=angular.mesh.base.pin(SOURCE / 'declaration.json'),output=str(OUTPUT),
        resource_addendum=angular.mesh.base.pin(SOURCE / 'resource_addendum.json'),
        numerical_source_equivalence=angular.mesh.base.pin(SOURCE / 'input_and_gate_equivalence.json')),indent=2))


if __name__ == '__main__':
    main()
