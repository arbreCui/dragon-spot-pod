import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT = Path('/private/tmp/axmat_single_pre_graph_gc_ACTUAL_BOUND_BUILD_Source_INDEPENDENT_1wtqalhh')

def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def strict(raw):
    def pairs(items):
        d = {}
        for k, v in items:
            if k in d: raise ValueError('duplicate key')
            d[k] = v
        return d
    def reject(v): raise ValueError('nonfinite JSON')
    return json.loads(raw.decode(), object_pairs_hook=pairs, parse_constant=reject)

def read(path):
    s = path.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink == 1 and 0 <= s.st_size <= 16*2**20
    before = identity(s)
    fd = os.open(path, os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd, 'rb', buffering=0) as f:
        assert identity(os.fstat(f.fileno())) == before
        raw = f.read(s.st_size+1)
        assert len(raw) == s.st_size and f.read(1) == b'' and identity(os.fstat(f.fileno())) == before
    assert identity(path.lstat()) == before
    return raw, dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), size_bytes=len(raw), identity=before)

def view():
    members, dirs = {}, {}
    for path in [ROOT, *sorted(ROOT.rglob('*'))]:
        rel = str(path.relative_to(ROOT)); s = path.lstat()
        if stat.S_ISDIR(s.st_mode): dirs[rel] = identity(s)
        else:
            assert stat.S_ISREG(s.st_mode) and s.st_nlink == 1
            if rel != 'MANIFEST.json': members[rel] = read(path)[1]
    return members, dirs

def dump(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode()

def write_new(path, raw):
    fd = os.open(path, os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    return read(path)[1]

def main():
    ap = argparse.ArgumentParser();ap.add_argument('--mode', choices=['seal','postseal'], required=True);ap.add_argument('--report');a=ap.parse_args()
    review_raw, review_pin = read(ROOT/'REVIEW.json'); review = strict(review_raw)
    assert review['schema'] == 'INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_MEMORY_OBSERVATION_POSTCLOSE_META_SOURCE_REVIEW_V1'
    assert review['status'] == 'PASS_ACTUAL_BOUND_FULL_BUILD_MEMORY_OBSERVATION_AND_POSTCLOSE_META_SOURCE_ONLY'
    assert review['source_only'] is True and review['all_checks_typed_true'] is True and review['blockers'] == []
    assert type(review['check_count']) is int and review['check_count'] == len(review['checks']) == 545
    assert all(type(c['passed']) is bool and c['passed'] is True for c in review['checks'])
    assert len({c['check'] for c in review['checks']}) == 545
    receipt = strict(read(ROOT/'ACTUAL_SOURCE_REVIEW_TOOL_TERMINAL_RETURN.json')[0]);t=receipt['terminal_tool_return']
    assert receipt['closed'] is True and receipt['observed_terminal'] is True and receipt['session_repolled_after_close'] is False
    assert type(t['exit_code']) is int and t['exit_code'] == 0 and t['chunk_id'] == 'db0853' and 'session_id' not in t
    observed = strict(t['output'].encode()); assert observed['review_pin'] == review_pin and observed['check_count'] == 545 and observed['blockers'] == []
    for q in review['full_EOF_Source_and_small_META_pins'].values():
        assert read(Path(q['path']))[1] == q
    for path, info in review['Root_actual_full_EOF_payload_pins_verified_current7ID_only'].items():
        assert identity(Path(path).lstat()) == info['current7ID']
    for rel, q in review['actual_bound_complete_package_view']['files'].items():
        assert read(Path(q['path']))[1] == q
    for rel, i in review['actual_bound_complete_package_view']['directories'].items():
        assert identity(Path(review['qualified_actual_bound_Source_manifest_pin']['path']).parent.joinpath(rel).lstat()) == i
    assert all(review[k] is False for k in ['candidate_API_guard_resource_helper_BUILD_native_or_science_executed','whole_BUILD_INPUT_RSS_native_or_science_qualified','AAA_accuracy_qualified','ABA_admitted','goal_complete'])
    if a.mode == 'seal':
        fd = os.open(ROOT/'MANIFEST.json', os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600);os.close(fd)
        members, dirs = view()
        for rel in members:
            if rel.endswith('.py'): ast.parse(read(ROOT/rel)[0], filename=rel)
        mf = dict(schema='INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_MEMORY_OBSERVATION_SOURCE_REVIEW_MANIFEST_V1',source_only=True,status='SEALED_SOURCE_ONLY_PASS_NO_RUNTIME_OR_SCIENCE',member_count=len(members),members=members,directories=dirs,check_count=545,no_future_append=True,no_candidate_or_business_executed=True)
        with (ROOT/'MANIFEST.json').open('wb') as f: f.write(dump(mf));f.flush();os.fsync(f.fileno())
        assert view() == (members,dirs)
        mp = read(ROOT/'MANIFEST.json')[1]
        print(json.dumps(dict(manifest_pin=mp,review_pin=review_pin,check_count=545,all_checks_typed_true=True,source_only=True,files=len(members)+1,directories=len(dirs),no_Runtime_RSS_or_science_credit=True),sort_keys=True))
    else:
        raw, mp = read(ROOT/'MANIFEST.json');mf=strict(raw);members,dirs=view()
        assert members == mf['members'] and dirs == mf['directories'] and len(members) == mf['member_count']
        assert not a.report is None
        report = dict(schema='INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_MEMORY_OBSERVATION_POSTSEAL_FULL_EOF_REREAD_V1',source_only=True,manifest_pin=mp,review_pin=review_pin,complete_members=members,complete_directories=dirs,all_full_EOF_SHA_and_directory_7ID_equal=True,check_count=545,no_runtime_or_science_qualification=True)
        report_pin=write_new(Path(a.report),dump(report))
        assert read(ROOT/'MANIFEST.json')[1] == mp and view() == (members,dirs)
        print(json.dumps(dict(manifest_pin=mp,review_pin=review_pin,postseal_report_pin=report_pin,source_only=True,check_count=545,all_full_EOF_SHA_and_directory_7ID_equal=True,no_Runtime_RSS_or_science_credit=True),sort_keys=True))

if __name__ == '__main__': main()
