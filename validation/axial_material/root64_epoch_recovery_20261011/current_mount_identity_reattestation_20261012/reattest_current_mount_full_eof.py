"""Finite read-only identity catalog; no imported project code or business child."""
import collections
import datetime
import hashlib
import json
import os
from pathlib import Path
import plistlib
import resource
import stat
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
OUT = Path(__file__).resolve().parent
FIELDS = ('path', 'sha256', 'size_bytes', 'identity')
OLD_DEVICE, CURRENT_DEVICE = 16777234, 16777229
START = time.monotonic()
observed = {}
json_bytes = {}
full_eof_bytes = 0

def seven(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]

def full_pin(path):
    global full_eof_bytes
    p = Path(path)
    before = seven(p.lstat())
    if not stat.S_ISREG(before[2]):
        raise RuntimeError('regular non-symlink file required: ' + str(p))
    fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW)
    parts = []
    capture = p.suffix == '.json'
    if capture and before[4] > 64 * 2**20:
        raise RuntimeError('finite JSON parsing bound exceeded: ' + str(p))
    h = hashlib.sha256()
    read_bytes = 0
    try:
        if seven(os.fstat(fd)) != before:
            raise RuntimeError('same-fd opened identity differs: ' + str(p))
        while True:
            b = os.read(fd, 2**20)
            if not b:
                break
            h.update(b)
            read_bytes += len(b)
            if capture:
                parts.append(b)
        if read_bytes != before[4] or seven(os.fstat(fd)) != before:
            raise RuntimeError('same-fd EOF identity/length differs: ' + str(p))
    finally:
        os.close(fd)
    if seven(p.lstat()) != before:
        raise RuntimeError('after EOF path identity differs: ' + str(p))
    actual = dict(path=str(p), sha256=h.hexdigest(), size_bytes=read_bytes,
                  identity=before)
    if str(p) in observed:
        if observed[str(p)] != actual:
            raise RuntimeError('current path changed during finite catalog: ' + str(p))
    else:
        observed[str(p)] = actual
        full_eof_bytes += read_bytes
    if capture:
        json_bytes[str(p)] = b''.join(parts)
    return actual

def get_actual(path):
    p = str(path)
    if p not in observed:
        return full_pin(p)
    if seven(Path(p).lstat()) != observed[p]['identity']:
        raise RuntimeError('previously read path changed: ' + p)
    return observed[p]

def exact_json(path):
    get_actual(path)
    return json.loads(json_bytes[str(path)])

def is_pin(v):
    return (isinstance(v, dict) and all(k in v for k in FIELDS)
            and isinstance(v['path'], str) and Path(v['path']).is_absolute()
            and isinstance(v['sha256'], str) and len(v['sha256']) == 64
            and type(v['size_bytes']) is int
            and isinstance(v['identity'], list) and len(v['identity']) == 7
            and all(type(x) is int for x in v['identity'])
            and v['identity'][4] == v['size_bytes'])

def clean_pin(v):
    if not is_pin(v):
        raise RuntimeError('complete original PF required')
    return {k: v[k] for k in FIELDS}

def pin_key(v):
    return (v['path'], v['sha256'], v['size_bytes'], tuple(v['identity']))

def walk_pins(v):
    if is_pin(v):
        yield clean_pin(v)
    if isinstance(v, dict):
        for c in v.values():
            yield from walk_pins(c)
    elif isinstance(v, list):
        for c in v:
            yield from walk_pins(c)

declarations = {}
pending = collections.deque()
parsed_jsons = set()
historical = []
failures = []
rows = []

def add(row, role, mandatory=False):
    row = clean_pin(row)
    key = pin_key(row)
    if key in declarations:
        d = declarations[key]
        d['mandatory'] = d['mandatory'] or mandatory
        d['declaration_occurrence_count'] += 1
        if mandatory or len(d['roles']) < 3:
            d['roles'].add(role)
    else:
        declarations[key] = dict(historical_pin=row, mandatory=mandatory,
                                 roles={role}, processed=False,
                                 declaration_occurrence_count=1)
        pending.append(key)

def compare(h, a):
    bad = []
    for k in ('path', 'sha256', 'size_bytes'):
        if h[k] != a[k]:
            bad.append(k)
    if h['identity'][1:] != a['identity'][1:]:
        bad.append('other_six_identity_fields')
    if a['identity'][0] != CURRENT_DEVICE:
        bad.append('current_device_not_16777229')
    if h['identity'][0] not in (OLD_DEVICE, CURRENT_DEVICE):
        bad.append('historical_device_not_explicit_old_or_current')
    return bad

def write_new(path, value):
    with Path(path).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())

def run():
    if sys.flags.optimize or sys.getprofile() is not None:
        raise RuntimeError('unprofiled nonoptimized finite verification required')
    for name in ('CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json',
                 'CURRENT_MOUNT_IDENTITY_REATTESTATION_REPORT.json',
                 'ACTUAL_APFS_VOLUME_INFO.plist'):
        if (OUT / name).exists() or (OUT / name).is_symlink():
            raise RuntimeError('fresh once-only output required: ' + name)
    v = subprocess.run(['/usr/sbin/diskutil', 'info', '-plist',
                        '/System/Volumes/Data'], capture_output=True, check=True)
    volume = plistlib.loads(v.stdout)
    expected_volume = dict(FilesystemType='apfs', MountPoint='/System/Volumes/Data',
                           DeviceIdentifier='disk3s5', DeviceNode='/dev/disk3s5',
                           VolumeUUID='7A39AB88-95E2-4E32-91BF-B80F4735F6B8')
    if any(volume.get(k) != value for k, value in expected_volume.items()):
        raise RuntimeError('true current APFS volume differs from explicit selected identity')
    with (OUT / 'ACTUAL_APFS_VOLUME_INFO.plist').open('xb') as f:
        f.write(v.stdout)
        f.flush()
        os.fsync(f.fileno())
    volume_pin = full_pin(OUT / 'ACTUAL_APFS_VOLUME_INFO.plist')
    own_source_pin = full_pin(Path(__file__).resolve())
    plan_path = REC / 'native_rank1_exact_block_cache_build_host_source_v1/CURRENT_ORIGINAL69_TO_COMPLETE70_BUILD_DRAFT_PLAN.json'
    plan = exact_json(plan_path)
    binding_pin = clean_pin(plan['original_common_binding_pin'])
    add(binding_pin, 'mandatory_common_binding_itself', True)
    binding = exact_json(binding_pin['path'])
    for p in binding['fixed_current_pins']:
        add(p, 'mandatory_common_binding_fixed_current_pins', True)
    add(plan['original_common_Source_pin'], 'mandatory_original_common_source', True)
    add(plan['original_actual69_handle_lifetime_report_pin'], 'mandatory_current69_report_itself', True)
    add(plan['original_actual69_v4_report_pin'], 'mandatory_original69_v4_report_itself', True)
    add(binding['selected_actual_current17_report'], 'mandatory_current17_report_itself', True)
    interface_path = REC / 'aaa_three_plane_streaming_pipeline_source_v6/DECLARED_EXECUTION_INTERFACE.json'
    interface = exact_json(interface_path)
    producer_pins = interface['selected_actual_producer_report_pins']
    if len(producer_pins) != 3:
        raise RuntimeError('exact three A producer pin declarations required')
    for p in producer_pins:
        add(p, 'mandatory_actual_A_producer_report_itself', True)
    b_review_path = REC / 'ROOT_INDEPENDENT_CURRENT_B_V3_FULLFILE_REVIEW_20261012.json'
    b_review = exact_json(b_review_path)
    b_pin = clean_pin(b_review['actual_report_pin'])
    if b_pin['sha256'] != '48d3704a6bd7e6ac451bc81997ca1de46a26f9ae1552ced084ebdc6f332f2014':
        raise RuntimeError('explicit selected real B producer SHA differs')
    add(b_pin, 'mandatory_actual_B_producer_report_itself', True)
    report_pins = [plan['original_actual69_handle_lifetime_report_pin'],
                   plan['original_actual69_v4_report_pin'],
                   binding['selected_actual_current17_report'],
                   *producer_pins, b_pin]
    report_scopes = []
    for p in report_pins:
        d = exact_json(p['path'])
        if d.get('failure') is not None or d.get('after_check_error') is not None:
            raise RuntimeError('selected prerequisite terminal report has failure')
        report_scopes.append(dict(path=p['path'], historical_report_status=d.get('status'),
                                 fixed_row_count=len(d['fixed_current_pins']),
                                 output_row_count=len(d['output_pins']),
                                 historical_qualification_unchanged=True))
        for field in ('fixed_current_pins', 'output_pins'):
            for row in d[field]:
                add(row, 'mandatory_' + Path(p['path']).parent.name + ':' + field, True)
    sf_review_path = REC / 'independent_native_rank1_cache_source_review_20261012/INDEPENDENT_SOURCE_REVIEW.json'
    sf_review = exact_json(sf_review_path)
    sf_pin = clean_pin(sf_review['source_freeze_observed_pin'])
    if sf_pin['sha256'] != 'c8be0de885e792c09cddf4d168a095f7410e674e3c47c33208ef58a2969e8843':
        raise RuntimeError('explicit selected current rank1 Source freeze SHA differs')
    add(sf_pin, 'mandatory_new_rank1_source_freeze_itself', True)
    sf = exact_json(sf_pin['path'])
    for row in walk_pins(sf):
        add(row, 'mandatory_new_rank1_source_freeze_all_complete_PF', True)
    for seed in (plan_path, interface_path, b_review_path, sf_review_path):
        for row in walk_pins(exact_json(seed)):
            add(row, 'finite_seed_json_declaration:' + str(seed))
    while pending:
        key = pending.popleft()
        d = declarations[key]
        if d['processed']:
            continue
        d['processed'] = True
        h = d['historical_pin']
        try:
            a = get_actual(h['path'])
            differences = compare(h, a)
        except FileNotFoundError:
            a, differences = None, ['path_absent']
        except RuntimeError as e:
            a, differences = None, [str(e)]
        if differences:
            d['differences'] = differences
            d['observed_current_pin'] = a
            if d['mandatory']:
                failures.append(d)
                break
            historical.append(d)
            continue
        d['current_pin'] = a
        rows.append(d)
        if Path(h['path']).suffix == '.json' and h['path'] not in parsed_jsons:
            parsed_jsons.add(h['path'])
            for row in walk_pins(exact_json(h['path'])):
                add(row, 'recursive_full_PF_from_current_JSON:' + h['path'])
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss >= 512 * 2**20:
            raise RuntimeError('finite verifier SELF 512MiB cap')
        if time.monotonic() - START >= 600:
            raise RuntimeError('finite verifier 600 second cap')
    # Reclassify mandatory flags after the complete declaration graph is closed.
    for d in historical:
        if d['mandatory'] and d not in failures:
            failures.append(d)
    for p, actual in observed.items():
        if seven(Path(p).lstat()) != actual['identity']:
            raise RuntimeError('observed file changed before catalog closure: ' + p)
    def serial(d, qualified=False):
        r = dict(historical_pin=d['historical_pin'], mandatory=d['mandatory'],
                 roles=sorted(d['roles']),
                 declaration_occurrence_count=d['declaration_occurrence_count'])
        if qualified:
            r['current_pin'] = d['current_pin']
            r['device_transition'] = ('16777234_TO_16777229'
                                      if d['historical_pin']['identity'][0] == OLD_DEVICE
                                      else 'ALREADY_CURRENT_16777229')
        else:
            r['differences'] = d.get('differences', ['unverified_mandatory'])
            r['observed_current_pin'] = d.get('observed_current_pin')
            r['historical_only_not_rebound'] = True
        return r
    qualified_rows = [serial(d, True) for d in sorted(rows, key=lambda d: pin_key(d['historical_pin']))]
    historical_rows = [serial(d) for d in sorted(historical, key=lambda d: pin_key(d['historical_pin']))]
    failure_rows = [serial(d) for d in failures]
    mandatory_unique = {d['historical_pin']['path'] for d in declarations.values() if d['mandatory']}
    report = dict(schema='CURRENT_MOUNT_IDENTITY_REATTESTATION_REPORT_V1',
                  status='ACTUAL_CURRENT_MOUNT_COMPLETE_PF_CATALOG_CLOSED0_ONLY' if not failures else 'MANDATORY_IDENTITY_DIFFERENCE_FAILED_NO_REBIND',
                  current_data_identity_qualified=not failures,
                  current_device=CURRENT_DEVICE, explicit_original_device=OLD_DEVICE,
                  volume_info_selected_fields=expected_volume, volume_info_pin=volume_pin,
                  verifier_source_pin=own_source_pin,
                  actual_diskutil_returncode=v.returncode,
                  mandatory_unique_paths=len(mandatory_unique),
                  mandatory_complete_PF_declarations=sum(d['mandatory'] for d in declarations.values()),
                  qualified_rows=len(qualified_rows),
                  qualified_unique_paths=len({d['historical_pin']['path'] for d in rows}),
                  historical_only_rows=len(historical_rows), failures=failure_rows,
                  full_EOF_unique_regular_files=len(observed), full_EOF_unique_bytes=full_eof_bytes,
                  parsed_current_JSON_files=len(parsed_jsons), elapsed_seconds=time.monotonic() - START,
                  SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  selected_historical_report_scopes=report_scopes,
                  source_only=True, compiler_executed=False, numerical_or_business_child_executed=False,
                  old_reports_sources_freezes_modified=False, future_file_pins_invented=False,
                  original_guards_MRO_caps_modified=False, existing_math_and_qualification_upgraded=False,
                  AAA_qualified=False, ABA_admitted=False, goal_complete=False)
    catalog = dict(schema='CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG_V1',
                   status=report['status'], current_data_identity_qualified=not failures,
                   generated_at_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   explicit_device_transition=dict(historical=OLD_DEVICE, current=CURRENT_DEVICE,
                                                   only_device_field_may_change=True),
                   volume_info_selected_fields=expected_volume, volume_info_pin=volume_pin,
                   full_EOF_unique_regular_files=len(observed), full_EOF_unique_bytes=full_eof_bytes,
                   mandatory_unique_paths=len(mandatory_unique), mandatory_complete_PF_declarations=report['mandatory_complete_PF_declarations'],
                   rows=qualified_rows, historical_non_live_declarations=historical_rows,
                   mandatory_failures=failure_rows,
                   Source_only=True, numerical_or_business_execution=False,
                   historical_reports_sources_unmodified=True, mathematical_or_physics_qualification_promoted=False,
                   future_file_pins_invented=False, goal_complete=False)
    write_new(OUT / 'CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json', catalog)
    report['actual_catalog_pin'] = full_pin(OUT / 'CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json')
    write_new(OUT / 'CURRENT_MOUNT_IDENTITY_REATTESTATION_REPORT.json', report)
    print(json.dumps(dict(status=report['status'], mandatory_unique_paths=report['mandatory_unique_paths'],
                          qualified_rows=report['qualified_rows'], historical_only_rows=report['historical_only_rows'],
                          failure_count=len(failures), full_EOF_unique_regular_files=report['full_EOF_unique_regular_files'],
                          full_EOF_unique_bytes=report['full_EOF_unique_bytes'], elapsed_seconds=report['elapsed_seconds'],
                          actual_catalog_pin=report['actual_catalog_pin']), ensure_ascii=False))
    return 1 if failures else 0

if __name__ == '__main__':
    raise SystemExit(run())
