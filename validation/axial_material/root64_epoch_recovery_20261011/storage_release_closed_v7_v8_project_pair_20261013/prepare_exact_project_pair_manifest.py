"""Prepare Source-only manifest. Does not execute unlink, compiler or transport."""
import ast
import json
from pathlib import Path
import project_pair_release_common as s

def main():
    if s.MANIFEST.exists():raise RuntimeError('manifest cannot be overwritten')
    for name in s.SOURCE_NAMES:ast.parse((s.PKG/name).read_text(),filename=name)
    source=[s.pin(s.PKG/name) for name in s.SOURCE_NAMES]
    protected,dag=s.protection();targets=[s.pin(p) for p in s.TARGETS]
    s.disjoint(targets,protected);proof=s.closed_proofs(targets);s.writer_gate();before=s.inventory()
    removed={r['path'] for r in targets}
    retained=[s.pin(path) for path in sorted(before['ordinary_file_identities']) if path not in removed]
    for row in retained:
        if row['identity']!=before['ordinary_file_identities'][row['path']]:raise RuntimeError('retained branch inventory changed')
    budget=s.budget()
    value=dict(schema='ROOT_REVIEWABLE_EXACT_TWO_CLOSED_FAILED_RUN_PROJECT_COPY_RELEASE_SOURCE_MANIFEST_V1',action_executed=False,compiler_or_numerical_business_executed=False,target_count=2,total_target_logical_bytes=s.BYTES,target_full_EOF_pins=targets,current_protected_full_EOF_pins=protected,Source_DAG_provenance=dag,closed_failed_overall_run_proofs=proof,retained_ordinary_full_EOF_pins=retained,complete_before_inventory=before,Source_pins=source,original_budget_before_preparation=budget,all_result_documents_logs_other_outputs_retained=True,only_old_private_PROJECT_replay_paths_removed=True,individual_GLOBAL_and_PROJECT_PASS_preserved=True,original_physical_producers_inputs_caps_math_tolerances_unchanged=True,no_success_receipt_prefilled=True,goal_complete=False)
    s.write_new(s.MANIFEST,value);mp=s.pin(s.MANIFEST)
    argv=['env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1','/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(s.PKG/'verify_or_execute_exact_project_pair.py'),'--manifest-sha256',mp['sha256'],'--manifest-seven-id',json.dumps(mp['identity'],separators=(',',':')),'--execute']
    cli=s.PKG/'ROOT_REVIEWABLE_EXACT_TWO_RELEASE_ARGV_SOURCE_ONLY.json';s.write_new(cli,dict(schema='EXACT_TWO_PRIVATE_PROJECT_SOURCE_ONLY_REVIEWABLE_EXECUTION_ARGV_V1',argv=argv,manifest_pin=mp,Source_prepared_only=True,deletion_executed=False,actual_success_receipt_not_predicted=True))
    print(json.dumps(dict(status='SOURCE_ONLY_EXACT_PAIR_MANIFEST_PREPARED',manifest_pin=mp,CLI_pin=s.pin(cli),protected_count=len(protected),retained_file_count=len(retained),candidate_bytes=s.BYTES,deletion_executed=False)))

if __name__=='__main__':main()
