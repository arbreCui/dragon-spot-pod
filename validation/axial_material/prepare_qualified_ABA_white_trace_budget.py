"""Freeze storage-only ABA execution without altering any sealed trial.

No reference receipt is fabricated and no transport is started. Actual original
AAA qualification remains mandatory before this control program can run ABA.
"""
import ast
import difflib
import json
from pathlib import Path
import shutil
import sys
import time

sys.dont_write_bytecode=True
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
PROD=ART/'axial-material-production-qualified-AB-white-trace-20261004'
CE=ART/'axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004'
OUT=ART/'axial-material-qualified-AAA-white-trace-reference-diagnostic-20261004/aba_budget'
PREPARED_SHA='88640bfd32cbca03d4e527b99760f99288528bb0ff5720c81f758bca60beffbf'
CE_SHA='17c4e48d4de450bc5e3232caf3238da519f23c3836bd54f0a91d122d300ae52c'
sys.path.insert(0,str(PROD/'runtime'))
import production_runner as base


def pin(p):p=Path(p).resolve();return dict(path=str(p),sha256=base.sha256(p))


def write_new(p,d):
    with p.open('x') as f:json.dump(d,f,indent=2);f.write('\n')


def main():
    info=base.verify_prepared(PROD/'prepared.json',PREPARED_SHA)
    base.require_file(CE/'AAA/execution.json',CE_SHA)
    if (PROD/'ABA').exists():raise ValueError('ABA already claimed: no new preparation')
    status=json.loads((PROD/'AAA/run_status.json').read_text())
    if status['classification']!='WAITING_REFERENCE' or status['cases']['AAA']['classification']!='VALID_MET':raise ValueError('actual completed numerical AAA required')
    spec=json.loads(Path(info['case_spec']['path']).read_text())
    if spec['resource_caps']['new_case_artifact_budget_GiB']!=40:raise ValueError('original frozen storage cap differs')
    OUT.mkdir(exist_ok=False);runtime=OUT/'runtime';runtime.mkdir()
    # Source only: native solver/host processes still use the original pinned runtime.
    for path in (PROD/'runtime').iterdir():
        if path.is_file() and path.suffix in ('.py','.json'):shutil.copy2(path,runtime/path.name)
    roots=sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir())
    roots.append(str(ART/'axial-material-ce-qualified-ABA-white-trace-precision-20261004'))
    before=base.DiskResources(ART,roots,8*2**30,64*2**30).check()
    actual_bytes=sum(p.stat().st_size for p in PROD.rglob('*') if p.is_file() and not p.is_symlink())
    forecast=before['artifact_bytes']+int(1.5*actual_bytes)+2*2**30
    if forecast>64*2**30:raise ValueError('forecast exceeds explicit new bound')
    addendum=dict(schema='AXMAT_ABA_ONLY_HISTORY_STORAGE_ADDENDUM_V1',declared_unix=time.time(),case='ABA',
        production_prepared=pin(PROD/'prepared.json'),case_spec=info['case_spec'],old_sealed_history_budget_GiB=40,ABA_history_budget_GiB=64,
        min_free_GiB=8,per_case_wall_seconds=info['budgets']['total_seconds'],max_maps=info['budgets']['max_maps'],threads=1,numeric_children_at_once=1,retries=0,
        current_regular_bytes=before['artifact_bytes'],measured_fresh_AAA_regular_bytes=actual_bytes,forecast_regular_bytes=forecast,
        forecast_policy='Retain all immutable history, allow 1.5 times measured complete fresh AAA size for ABA plus 2 GiB for independent ABA reference and reports.',
        resource_roots=roots,old_sealed_caps_changed=False,physical_inputs_changed=False,accuracy_thresholds_changed=False,
        source='Measured complete fresh AAA has 11 maps, exceeding the earlier forecast based on the four-map legacy AAA. This explicit ABA-only storage exception does not alter earlier executed caps.',
        admission='Actual original eight-gate AAA qualification and terminal independent full precision reference required before any ABA case/native claim.')
    write_new(runtime/'aba_resource_addendum.json',addendum)
    old=(PROD/'runtime/production_runner.py').read_text();tree=ast.parse(old)
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='resource_monitor')
    lines=old.splitlines(True)
    replacement='''def resource_monitor(info: dict) -> DiskResources:
    item = Path(__file__).with_name("aba_resource_addendum.json")
    addendum = json.loads(require_file(item, "ADDENDUM_SHA").read_text())
    if addendum.get("schema") != "AXMAT_ABA_ONLY_HISTORY_STORAGE_ADDENDUM_V1" or addendum.get("case") != "ABA":
        raise Refusal("explicit ABA-only storage addendum required")
    if info["case_spec"] != addendum["case_spec"] or info["artifact_root"] != str(ARTIFACTS_ROOT.resolve()):
        raise Refusal("storage addendum does not bind this unchanged frozen study")
    spec = json.loads(Path(info["case_spec"]["path"]).read_text())
    caps = spec["resource_caps"]
    if caps["new_case_artifact_budget_GiB"] != 40 or caps["disk_min_free_GiB"] != 8 or addendum["ABA_history_budget_GiB"] != 64:
        raise Refusal("declared storage-only bounds differ")
    if info["budgets"]["total_seconds"] != addendum["per_case_wall_seconds"] or info["budgets"]["max_maps"] != addendum["max_maps"]:
        raise Refusal("original per-case wall/map limits changed")
    return DiskResources(ARTIFACTS_ROOT, addendum["resource_roots"], 8*2**30, 64*2**30)
'''.replace('ADDENDUM_SHA',base.sha256(runtime/'aba_resource_addendum.json'))
    new=''.join(lines[:node.lineno-1])+replacement+''.join(lines[node.end_lineno:])
    anchor='    info = verify_prepared(prepared, expected_sha)\n    work = prepared.parent\n    if case not in ("AAA", "ABA"):'
    if new.count(anchor)!=1:raise ValueError('unique original case guard required')
    new=new.replace(anchor,'    info = verify_prepared(prepared, expected_sha)\n    work = prepared.parent\n    if case != "ABA":\n        raise Refusal("this resource addendum admits only ABA; earlier AAA caps remain frozen")\n    if case not in ("AAA", "ABA"):')
    anchor='              "resource_roots": info["resource_roots"],'
    if new.count(anchor)!=1:raise ValueError('unique case resource reporting anchor required')
    new=new.replace(anchor,'              "resource_roots": [str(p) for p in resources.roots],\n              "execution_resource_addendum": {"path": str(Path(__file__).with_name("aba_resource_addendum.json")), "sha256": "'+base.sha256(runtime/'aba_resource_addendum.json')+'"},')
    # The copied program has not been declared yet and is still a staging file.
    (runtime/'production_runner.py').write_text(new)
    (runtime/'production_runner.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='frozen_white_control',tofile='ABA_storage_only_control')))
    oldnodes={n.name:ast.dump(n,include_attributes=False) for n in ast.parse(old).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    newnodes={n.name:ast.dump(n,include_attributes=False) for n in ast.parse(new).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    if oldnodes.keys()!=newnodes.keys() or {k for k in oldnodes if oldnodes[k]!=newnodes[k]}!={'resource_monitor','run'}:raise ValueError('unexpected source change')
    launcher=ROOT/'validation/axial_material/run_qualified_ABA_white_trace_budget.py'
    paths=[Path(__file__).resolve(),launcher,PROD/'prepared.json',PROD/'AAA/run_status.json',CE/'AAA/execution.json',CE/'analysis_collection_declaration.json',
        PROD/'runtime/production_runner.py',Path(info['case_spec']['path']),*[runtime/n for n in ('production_runner.py','production_inputs.py','aba_resource_addendum.json','production_runner.patch')]]
    paths += [PROD/name for name in info['local_files']]
    paths += [Path(item['path']) for item in info['inputs'].values()]
    files={str(p.resolve()):base.sha256(p) for p in paths}
    files.update({str(p.resolve()):base.sha256(p) for p in runtime.iterdir() if p.is_file()})
    write_new(OUT/'source_lineage.json',dict(status='PASS_ONLY_ABA_STORAGE_CONSTRUCTOR_CASE_RESTRICTION_AND_RESOURCE_REPORT_CHANGED',
        unchanged_functions_and_classes=sorted(set(oldnodes)-{'resource_monitor','run'}),original_qualify_aba_byte_ast_unchanged=True,
        original_inner_outer_map_and_liveness_guards_unchanged=True,new_numeric_child_started=False,ABA_admitted=False))
    files[str(OUT/'source_lineage.json')]=base.sha256(OUT/'source_lineage.json')
    d=dict(schema='AXMAT_ABA_ONLY_FROZEN_STORAGE_EXECUTION_V1',declared_unix=time.time(),case='ABA',production_prepared=pin(PROD/'prepared.json'),
        old_sealed_history_budget_GiB=40,ABA_history_budget_GiB=64,resource_roots=roots,per_case_wall_seconds=info['budgets']['total_seconds'],max_maps=info['budgets']['max_maps'],
        reference_case=str(CE/'AAA'),reference_execution=pin(CE/'AAA/execution.json'),required_qualification=str(CE/'AAA/reference_qualification.json'),
        control_program=pin(runtime/'production_runner.py'),resource_addendum=pin(runtime/'aba_resource_addendum.json'),files=files,
        status='PREPARED_STORAGE_ONLY_PENDING_ACTUAL_AAA_ACCURACY',new_transport_launched=False,ABA_admitted=False)
    write_new(OUT/'declaration.json',d)
    print(json.dumps(dict(declaration=pin(OUT/'declaration.json'),resource_addendum=pin(runtime/'aba_resource_addendum.json'),source_lineage=pin(OUT/'source_lineage.json'),forecast_GiB=forecast/2**30),indent=2))


if __name__=='__main__':main()
