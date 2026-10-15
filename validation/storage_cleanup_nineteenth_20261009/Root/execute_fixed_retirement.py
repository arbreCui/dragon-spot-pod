from pathlib import Path
import json, hashlib, os, runpy

OUT = Path('/private/tmp/spot_storage_nineteenth_root_20261009')
PLAN = OUT / 'fixed_candidate_plan.json'
EXPECTED = 'b0cf9e8577d91ee6c3be70eada54d3f7f20078335e60db08a43ed1b3a093b79a'
review = runpy.run_path(str(OUT / 'prepare_review.py'), run_name='pure_metadata_helpers_only')
sha, identity, inventory = review['sha'], review['identity'], review['inventory']

def main():
    assert sha(PLAN) == EXPECTED
    p = json.loads(PLAN.read_text())
    assert len(p['regular']) == len(p['symlinks']) == 18
    selected = {x['path'] for x in p['regular'] + p['symlinks']}
    assert len(selected) == 36
    before = json.loads((OUT / 'protected_before.json').read_text())
    current = inventory(selected)
    assert current['counts'] == before['counts'] and current['fingerprints'] == before['fingerprints'], 'protected remainder changed before deletion'
    for key in ['current_binding', 'current_graph']:
        assert sha(Path(p[key]['path'])) == p[key]['sha256']
    for x in p['regular']:
        q = Path(x['path'])
        assert q.name == 'closed_snapshots.xsm' and q.parent.name.startswith('map')
        assert q.is_relative_to(review['ART']) and not q.is_symlink()
        assert identity(q) == x['identity'] and x['identity'][6] == 1
        assert sha(q) == x['sha256'] and identity(q) == x['identity']
        assert sha(Path(x['original_stage_seal'])) == x['original_stage_seal_sha256']
    for x in p['symlinks']:
        q = Path(x['path'])
        assert q.name == 'parent_snapshots_closed.xsm' and q.is_symlink()
        assert identity(q) == x['identity'] and os.readlink(q) == x['link_text'] and str(q.resolve()) == x['target']
    for x in p['kept_last_three_closed_and_last_two_parent_links']:
        q = Path(x['path'])
        assert identity(q) == x['identity']
        if 'sha256' in x:
            assert sha(q) == x['sha256']
        else:
            assert os.readlink(q) == x['link_text'] and str(q.resolve()) == x['target'] and q.resolve().is_file()
    for path, digest in before['control_document_pins'].items():
        assert sha(Path(path)) == digest
    result = {'schema': 'SPOT_ACTUAL_FIXED_OLD_MAP_RETIREMENT_V1', 'plan_sha256': EXPECTED, 'status': 'DELETION_STARTED', 'all_prechecks_passed_before_first_unlink': True, 'deleted_regular': [], 'deleted_symlinks': [], 'logical_bytes': 0, 'allocated_bytes': 0, 'business_executed': False, 'scientific_qualification': False}
    def save():
        (OUT / 'cleanup_result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    save()
    try:
        for x in p['symlinks']:
            q = Path(x['path'])
            assert identity(q) == x['identity'] and os.readlink(q) == x['link_text']
            q.unlink()
            result['deleted_symlinks'].append(x['path'])
            save()
        for x in p['regular']:
            q = Path(x['path'])
            assert identity(q) == x['identity']
            q.unlink()
            result['deleted_regular'].append(x['path'])
            result['logical_bytes'] += x['identity'][3]
            result['allocated_bytes'] += x['allocated_bytes']
            save()
        result['status'] = 'COMPLETE_EXACT_18_EARLY_STATES_AND_18_DEPENDENT_LINKS_RETIREMENT'
        save()
    except BaseException:
        result['status'] = 'PARTIAL_RETIREMENT_EXCEPTION_PRESERVED_NO_RETRY'
        save()
        raise
    print(json.dumps({'status': result['status'], 'deleted_regular': len(result['deleted_regular']), 'deleted_symlinks': len(result['deleted_symlinks']), 'allocated_gib': result['allocated_bytes']/2**30}, ensure_ascii=False))

if __name__ == '__main__':
    main()
