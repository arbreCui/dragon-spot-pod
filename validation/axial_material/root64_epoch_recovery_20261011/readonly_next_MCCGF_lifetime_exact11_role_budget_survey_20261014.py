"""Read-only role and budget survey; no scientific body hashing or deletion."""
import hashlib
import importlib.util
import json
import os
import stat
import time
import sys
from pathlib import Path

R = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
ART = Path('/Users/wen/spot/validation/artifacts')
OUT = R / 'readonly_next_MCCGF_lifetime_exact11_role_budget_survey_20261014'
NATIVE = ART / 'axial-material-new-one-BOOT-A8-false-return-diagnostic-20261014-v1'
HOST = R / 'boot_v16_A8_247_false_return_diagnostic_host_source_v1_20261014'
RELEASE = R / 'storage_release_literal11_next_A8_core_duplicates_source_v1_20261014'


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def pin(p):
    p = Path(p)
    s = p.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_size <= 64 * 2**20
    with os.fdopen(os.open(p, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as f:
        assert identity(os.fstat(f.fileno())) == identity(s)
        b = f.read()
        assert identity(os.fstat(f.fileno())) == identity(s)
    assert identity(p.lstat()) == identity(s)
    return dict(path=str(p), sha256=hashlib.sha256(b).hexdigest(), size_bytes=len(b), identity=identity(s))


def load(p, sha=None):
    q = pin(p)
    if sha is not None:
        assert q['sha256'] == sha
    return json.loads(Path(q['path']).read_bytes()), q


def same7(p):
    s = Path(p['path']).lstat()
    assert stat.S_ISREG(s.st_mode) and identity(s) == p['identity'] and s.st_size == p['size_bytes']


def fullpin_rows(v):
    if isinstance(v, dict):
        if {'path', 'sha256', 'size_bytes', 'identity'} <= set(v):
            yield {k: v[k] for k in ('path', 'sha256', 'size_bytes', 'identity')}
        for x in v.values():
            yield from fullpin_rows(x)
    elif isinstance(v, list):
        for x in v:
            yield from fullpin_rows(x)


def main():
    assert not OUT.exists()
    d, dp = load(NATIVE / 'Root_actual_one_BOOT_status_diagnostic_summary.json', 'cd1b5ded09155087ee0b66b2cd55548d2b927f08d573d1d3e3eb06af86bd3aff')
    root, rp = load(R / 'ROOT_ACTUAL_ONE_A8_247_FALSE_RETURN_DIAGNOSTIC_V1_TRUE_TOOL_RETURNS_20261014.json', '0ae851bba7eec9b5e6591a7725ea00952342fd79edd2f7358fe716c1231c93d9')
    post, pp = load(Path(sys.argv[1]))
    tools, tp = load(Path(sys.argv[2]))
    assert root['observed_closed'] is True and type(root['original_integer_exit_code']) is int and root['original_integer_exit_code'] == 1
    assert type(root['actual_terminal_return']['exit_code']) is int and root['actual_terminal_return']['exit_code'] == 1
    assert root['actual_terminal_return'].get('session_id') is None
    assert post['failure'] is None and tools['observed_closed'] is True
    assert post['actual_report_pin'] == dp and post['actual_Root_true_tool_return_pin'] == rp
    assert json.loads(tools['actual_review_return']['output'].strip().splitlines()[-1])['review_pin'] == pp
    assert d['actual_outcome']['actual_A9_first_false_return']['predicate_id'] == 'A9_FLU2DR64_CORE_RETURN_L0233'
    assert d['actual_outcome']['actual_A8_first_false_return']['predicate_id'] == 'A8_MCCGF64_RETURN_L0442'
    assert tools['actual_review_return']['exit_code'] == 0 and type(tools['actual_review_return']['exit_code']) is int
    assert d['status'] == 'FAILED_DIAGNOSTIC_UNQUALIFIED' and d['first_failure_secondary_errors'] == []
    assert d['actual_outcome']['actual_diagnostic']['actual_return_status'] == 2
    plan, planp = load(HOST / 'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json')
    hf, hfp = load(HOST / 'COMPLETE_GUARDED_ONE_BOOT_A8_247_FALSE_RETURN_DIAGNOSTIC_HOST_SOURCE_FREEZE.json', 'd16fd1c681c03da5980d454f383dc894c1523cfb65332a545519798ad2dbc571')
    mf, mfp = load(RELEASE / 'EXACT_LITERAL11_NEXT_A8_CORE_DUPLICATES_MANIFEST.json', '2514ce1f5893ae3bc810cbef2e288a2b37c648e9e940de9d8c2825764992cdc8')
    old_survey, _ = load(R / 'readonly_next_native17_BIND_probe_exact11_private_role_and_current_budget_survey_20261014/REVIEW.json')
    current18 = plan['retained_current18_original9_latest_A9_nine_input_pins']
    original9 = plan['retained_original_v16_nine_input_pins']
    latest9 = [x['owned_readonly_copy_pin'] for x in d['exact_owned_readonly_input_copy_proofs']]
    previous9 = [x['original_readonly_pin'] for x in d['exact_owned_readonly_input_copy_proofs']]
    assert len(current18) == 18 and len(original9) == len(latest9) == len(previous9) == 9
    assert previous9 == plan['retained_latest_A9_nine_input_copy_pins']
    old9 = previous9
    qmac = [next(x for x in d['output_pins'] if Path(x['path']).name == n) for n in ('BOOT-Q-1.xsm', 'BOOT-MAC-1.xsm')]
    targets = qmac + old9
    keep18 = original9 + latest9
    assert len({x['path'] for x in targets}) == 11 and len({x['path'] for x in keep18}) == 18
    assert {x['path'] for x in current18} == {x['path'] for x in original9 + old9}
    assert not {x['path'] for x in targets} & {x['path'] for x in keep18}
    new_by_name = {Path(x['path']).name: x for x in latest9}
    assert len(new_by_name) == 9
    roles = []
    for i, p in enumerate(targets):
        same7(p)
        assert p['identity'][3] == 1 and Path(p['path']).lstat().st_uid == os.getuid()
        if i >= 2:
            mirror = new_by_name[Path(p['path']).name]
            assert (p['sha256'], p['size_bytes']) == (mirror['sha256'], mirror['size_bytes'])
            # Older probe input copies have their original writable mode.
            # Their immutable fullpin and closed input role establish no writes;
            # do not invent a permission-bit requirement for a historical role.
            assert p['identity'][:2] != mirror['identity'][:2]
            role = 'closed_ordinary_readonly_input_duplicate_retire_current_role'
        else:
            mirror = None
            role = 'closed_failed_generated_Q_or_MAC_no_current_scientific_role'
        roles.append(dict(ordinal=i + 1, role=role, target_pin=p, retained_identical_latest_native_input_pin=mirror))
    for p in keep18:
        same7(p)
    assert len({tuple(p['identity'][:2]) for p in targets + keep18}) == 29
    def indices(rows):
        result = []
        for p in old9:
            ids = [i for i, x in enumerate(rows) if x['path'] == p['path']]
            assert len(ids) == 1 and rows[ids[0]] == p
            result += ids
        assert len(set(result)) == 9
        return result
    mi = indices(mf['current_protected_full_EOF_pins'])
    hi = indices(hf['dependencies'])
    assert all(p['path'] not in {x['path'] for x in mf['current_protected_full_EOF_pins']} for p in qmac)
    assert all(p['path'] not in {x['path'] for x in hf['dependencies']} for p in qmac)
    retained_catalogs = {}
    for key in ('current_CAT3030_pin', 'current_BIND2012_pin'):
        p = old_survey[key];v, actual = load(p['path'], p['sha256']);assert actual == p
        assert not {p['path'] for p in targets} & {x['path'] for x in fullpin_rows(v)}
        retained_catalogs[key] = p
    branches = sorted({str(Path(x['path']).parents[1]) for x in targets})
    inventories = []
    for branch in branches:
        b = Path(branch);files = [];dirs = []
        for p in sorted(b.rglob('*')):
            s = p.lstat();assert not stat.S_ISLNK(s.st_mode)
            if stat.S_ISDIR(s.st_mode):dirs.append(str(p))
            else:assert stat.S_ISREG(s.st_mode);files.append(dict(path=str(p),identity=identity(s),size_bytes=s.st_size))
        inventories.append(dict(root=branch,regular_files=files,directories=dirs))
    commonp = pin(RELEASE / 'literal11_release_common.py')
    s = importlib.util.spec_from_file_location('readonly_native27_original_budget_helper', commonp['path'])
    c = importlib.util.module_from_spec(s);s.loader.exec_module(c)
    budget = c.budget()
    total = sum(x['size_bytes'] for x in targets)
    assert budget['original_cold_reserve_bytes'] == 20971764748 and budget['initial_fresh_reserve_bytes'] == 2 * 2**30
    margin = budget['remaining_after_original_initial_reserves_bytes']
    for p in targets + keep18:
        same7(p)
    report = dict(schema='READONLY_NEXT_MCCGF_LIFETIME_EXACT11_PRIVATE_ROLE_AND_CURRENT_BUDGET_SURVEY_V1',status='PASS_READONLY_EXACT11_CURRENT_ROLES_ORIGINAL_BUDGET_ONLY_NO_DELETION',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,deletion_executed=False,current_original_resource_snapshot=budget,current_original_full_reserve_margin_bytes=margin,current_original_full_reserve_admitted=budget['original_initial_reserve_admitted'],ordered_literal_candidate_role_rows=roles,candidate_count=11,candidate_logical_bytes=total,predicted_after_exact11_full_reserve_margin_bytes=margin+total,predicted_margin_is_not_actual_admission=True,current_MF8608_exact9_candidate_indices=mi,current_HF3787_exact9_candidate_indices=hi,current_MF8608_pin=mfp,current_HF3787_pin=hfp,current_Host_PLAN_pin=planp,retained_current18_original9_latest_A8_nine_input_pins=keep18,next_exact_nine_source_input_copy_pins=latest9,exact_historical_retired9_old_input_pins=old9,current_two_generated_failed_stage_history_Q_MAC_pins=qmac,all11_target_and18_retained_input_seven_fields_twice_verified=True,all_body_SHA_evidence_reused_no_science_body_EOF_repeat=True,current_owner_complete_inventory_scope=inventories,all_existing_Source_HF_MF_reports_results_logs_objects_modules_and_science_must_stay=True,genuine_latest_failed_summary_pin=dp,genuine_latest_Root_tools_pin=rp,genuine_latest_actual_post_review_pin=pp,genuine_latest_actual_post_true_tool_pin=tp,original_budget_helper_pin=commonp,original_resource_factory_pin=old_survey['original_resource_factory_pin'],all_handles_closed=True,checked_unix=time.time(),**retained_catalogs)
    OUT.mkdir()
    p = OUT / 'REVIEW.json'
    with p.open('x') as f:
        json.dump(report, f, indent=2, ensure_ascii=False, allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(review_pin=pin(p),candidate_count=11,candidate_logical_bytes=total,current_original_full_reserve_margin_bytes=margin,predicted_after_exact11_full_reserve_margin_bytes=margin+total,files_deleted=False,business_executed=False)))


if __name__ == '__main__':
    main()
