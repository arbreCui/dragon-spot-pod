"""Retire precisely 24 reviewed duplicate libraries; preserve primary results."""
import argparse
import json
import stat
import time
from pathlib import Path
from exact_retire_utils import ROOT, OUT, identity, digest, save, inventory, capacity, symlink_check

SOURCE = OUT / 'duplicate_library_source_review.json'
SOURCE_SHA = '8a122bbd9b4f7a62fdfecd58b7827ae47d5ed2ff018692b950c6137d6380b524'
FAMILIES = (
    'native-radial-response-20260928', 'native-axial-coupling-20260928',
    'native-segment-composition-compact-20260929', 'native-segment-composition-20260929',
    'd4a-map6-physical-column-trace-20260928', 'native-directional-response-20260929',
)
LIBRARIES = ('libDragon.a', 'libTrivac.a', 'libUtilib.a', 'libGanlib.a')
EXACT_SELECTION = {str(ROOT / 'validation/artifacts' / f / 'build' / n)
                   for f in FAMILIES for n in LIBRARIES}


def absolute_strings(value):
    found = set()
    stack = [value]
    while stack:
        v = stack.pop()
        if isinstance(v, str):
            if v.startswith('/'):
                found.add(v)
        elif isinstance(v, dict):
            stack.extend(v.keys())
            stack.extend(v.values())
        elif isinstance(v, list):
            stack.extend(v)
    return found


def same_pinned_content(ref):
    z = digest(Path(ref['path']))
    if z['sha256'] != ref['sha256'] or ('bytes' in ref and z['bytes'] != ref['bytes']):
        raise ValueError('source or preservation evidence changed: ' + ref['path'])
    if 'identity' in ref and z['identity'] != ref['identity']:
        raise ValueError('source identity changed: ' + ref['path'])
    return z


def plan():
    source_pin = digest(SOURCE)
    if source_pin['sha256'] != SOURCE_SHA:
        raise ValueError('review source changed')
    s = json.loads(SOURCE.read_text())
    if s['candidate_count'] != 24 or not s['all_exact_duplicates_and_scope_checks_pass']:
        raise ValueError('incomplete exact candidate review')
    if {r['path'] for r in s['candidates']} != EXACT_SELECTION:
        raise ValueError('wrong exact selection')
    graph_pin = same_pinned_content(s['current_input_graph_pin'])
    index_pin = same_pinned_content(s['old_protection_index_pin'])
    g = json.loads(Path(graph_pin['path']).read_text())
    old = json.loads(Path(index_pin['path']).read_text())
    exact = absolute_strings(g) | set(old['protected_files']) | set(old['inbound_alias_targets'])
    directories = {n['canonical_root'] for n in g['namespaces']}
    directories |= set(old['protected_directories']) | set(s['critical_roots_excluded_wholesale'])
    for a in g['aliases']:
        if a['kind'] in ('dir', 'directory'):
            directories.update(a[k] for k in ('path', 'target'))
    metadata = {}
    fields = ('source_literal_evidence_pins', 'metadata_library_reference_evidence_pins',
              'retained_original_result_source_log_parameter_command_and_unique_executable_pins',
              'explicitly_preserved_signed_host_libraries')
    for ref in [s['critical_roots_source_pin'], *[r for k in fields for r in s[k]]]:
        z = same_pinned_content(ref)
        metadata[z['path']] = z
    for p in (Path(__file__).resolve(), OUT/'exact_retire_utils.py'):
        z = digest(p)
        metadata[z['path']] = z
    rows, kept = [], {}
    for r in s['candidates']:
        p = Path(r['path'])
        z = same_pinned_content(r)
        q = same_pinned_content(r['retained_primary'])
        i = z['identity']
        if p.resolve() != p or not stat.S_ISREG(i[2]) or i[6] != 1:
            raise ValueError('not an independent ordinary library')
        if str(p) in exact or any(p.is_relative_to(Path(d)) for d in directories):
            raise ValueError('current dependency intersects selection')
        if z['sha256'] != q['sha256'] or z['bytes'] != q['bytes'] or z['identity'][:2] == q['identity'][:2]:
            raise ValueError('library is not an exact independent duplicate')
        if p.stat().st_blocks*512 != r['allocated_bytes'] or not all(r['screen_checks'].values()):
            raise ValueError('candidate scope or allocation changed')
        rows.append({'path':str(p), 'retained_primary':q['path'], 'expected_sha256':z['sha256'],
                     'expected_bytes':z['bytes'], 'allocated_bytes':r['allocated_bytes'],
                     'identity':i, 'category':'OLD_PRIVATE_LINK_LIBRARY_COPY'})
        kept[q['path']] = q
    if len(rows) != 24 or len(kept) != 4 or EXACT_SELECTION & set(kept):
        raise ValueError('wrong retained selection')
    save('manifest.json', {'schema':'SPOT_SIXTH_EXACT_DUPLICATE_LIBRARIES_V1',
        'status':'ROOT_PLAN_NOT_DELETED', 'candidates':rows,
        'retained_primaries_and_critical_sources':list(kept.values()),
        'source_metadata_pins':list(metadata.values()), 'review_pins':[source_pin],
        'graph_pin':graph_pin, 'old_index_pin':index_pin,
        'latest_graph_screen':{'canonical_files':len(g['canonical_files']),
                              'namespaces':len(g['namespaces']), 'aliases':len(g['aliases']),
                              'critical_roots':len(s['critical_roots_excluded_wholesale']),
                              'all_selected_intersections':0, 'API_executed':False},
        'symlink_check':symlink_check(EXACT_SELECTION), 'selected_count':24,
        'logical_bytes':sum(r['expected_bytes'] for r in rows),
        'allocated_bytes':sum(r['allocated_bytes'] for r in rows),
        'all_documents_logs_sources_primary_results_retained':True,
        'old_duplicate_paths_require_restore_for_full_replay':True, 'files_deleted':0})
    print(json.dumps({'status':'EXACT_24_LIBRARIES_PLANNED', 'kept_primaries':4}))


def preflight():
    m = json.loads((OUT/'manifest.json').read_text())
    selected = {r['path'] for r in m['candidates']}
    if selected != EXACT_SELECTION or m['selected_count'] != 24:
        raise ValueError('wrong exact selection')
    before = inventory(selected)
    for z in m['review_pins']+m['source_metadata_pins']+[m['graph_pin'],m['old_index_pin']]:
        if digest(Path(z['path'])) != z:
            raise ValueError('review or dependency evidence changed')
    if symlink_check(selected) != m['symlink_check']:
        raise ValueError('project links changed')
    candidates, kept = [], []
    for r in m['candidates']:
        z = digest(Path(r['path']))
        if z['identity'] != r['identity'] or z['sha256'] != r['expected_sha256'] or z['bytes'] != r['expected_bytes']:
            raise ValueError('fresh candidate content mismatch')
        candidates.append(z)
    for r in m['retained_primaries_and_critical_sources']:
        z = digest(Path(r['path']))
        if z != r:
            raise ValueError('fresh retained primary mismatch')
        kept.append(z)
    if inventory(selected) != before:
        raise ValueError('nonselected identity changed during read')
    save('preflight.json', {'schema':'SPOT_SIXTH_ROOT_FRESH_CONTENT_PREFLIGHT_V1',
        'status':'PASS', 'manifest_sha256':digest(OUT/'manifest.json')['sha256'],
        'verified_candidates':candidates, 'verified_kept':kept,
        'preservation_baseline':before, 'capacity_before':capacity(),
        'files_deleted':0, 'solver_or_API_executed':False})
    print(json.dumps({'status':'PREFLIGHT_PASS', 'manifest_sha256':digest(OUT/'manifest.json')['sha256'],
                      'preflight_sha256':digest(OUT/'preflight.json')['sha256'],
                      'candidate_count':len(candidates), 'kept_count':len(kept)}))


def apply(msha, psha, rsha):
    start = time.monotonic()
    if digest(OUT/'manifest.json')['sha256'] != msha or digest(OUT/'preflight.json')['sha256'] != psha or digest(OUT/'independent_preflight_review.json')['sha256'] != rsha:
        raise ValueError('Root-observed exact pins required')
    m = json.loads((OUT/'manifest.json').read_text())
    p = json.loads((OUT/'preflight.json').read_text())
    review = json.loads((OUT/'independent_preflight_review.json').read_text())
    if review['status'] != 'PASS' or review['manifest_sha256'] != msha or review['preflight_sha256'] != psha:
        raise ValueError('independent preflight review required')
    selected = {r['path'] for r in m['candidates']}
    if selected != EXACT_SELECTION or len(selected) != 24 or p['status'] != 'PASS' or p['manifest_sha256'] != msha:
        raise ValueError('preflight selection mismatch')
    if [r['path'] for r in p['verified_candidates']] != [r['path'] for r in m['candidates']]:
        raise ValueError('preflight candidate sequence mismatch')
    if inventory(selected) != p['preservation_baseline'] or symlink_check(selected) != m['symlink_check']:
        raise ValueError('preservation or links changed')
    for z in p['verified_candidates']+p['verified_kept']+m['source_metadata_pins']+m['review_pins']+[m['graph_pin'],m['old_index_pin']]:
        if identity(Path(z['path'])) != z['identity']:
            raise ValueError('checked file changed')
    with (OUT/'retirement_ledger.jsonl').open('x') as ledger:
        for z in p['verified_candidates']:
            q = Path(z['path'])
            if identity(q) != z['identity']:
                raise ValueError('candidate changed before unlink')
            q.unlink()
            ledger.write(json.dumps(dict(**z,deleted=True))+'\n')
            ledger.flush()
    after = inventory(selected)
    if after != p['preservation_baseline'] or any(Path(x).exists() or Path(x).is_symlink() for x in selected):
        raise ValueError('unexpected preservation or deletion result')
    save('cleanup_result.json', {'schema':'SPOT_SIXTH_ACTUAL_EXACT_DUPLICATE_RETIREMENT_V1',
        'status':'PASS', 'deleted_files':24, 'deleted_logical_bytes':m['logical_bytes'],
        'deleted_allocated_bytes':m['allocated_bytes'], 'capacity_before':p['capacity_before'],
        'capacity_after':capacity(), 'nonselected_before':p['preservation_baseline'],
        'nonselected_after':after, 'symlink_check_after':symlink_check(selected),
        'solver_or_API_executed':False, 'new_scientific_credit':False,
        'elapsed_seconds':time.monotonic()-start})
    print(json.dumps({'status':'CLEANUP_PASS', 'deleted_files':24,
                      'deleted_allocated_bytes':m['allocated_bytes'], 'nonselected_fingerprint':after}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['plan','preflight','apply'])
    parser.add_argument('--manifest-sha')
    parser.add_argument('--preflight-sha')
    parser.add_argument('--review-sha')
    a = parser.parse_args()
    if a.action == 'plan':
        plan()
    elif a.action == 'preflight':
        preflight()
    else:
        apply(a.manifest_sha,a.preflight_sha,a.review_sha)
