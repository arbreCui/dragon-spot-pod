"""Seal this finite independent SOURCE review; no candidate execution."""
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT = Path(__file__).parent
AUTHOR = Path('/private/tmp/axmat_v21b_complete_fresh_verifier_old_constructor_oracle_SOURCE_ONLY_20261010_angular_qhs7_kjb')
EXPECTED_AUTHOR_SHA = '6a2495ae42e0cbabdb257a92347de7391451e7e93a9fc1530dbcc7badd787483'
EXPECTED_REPORT_SHA = 'a82e9787ec38ebaa3ea6a18d527bda4be72327d5a1c70270e5909d52075fee87'

def identity(path):
    s = path.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def read(path):
    before = identity(path)
    if not stat.S_ISREG(before[2]) or before[3] != 1 or path.is_symlink():
        raise ValueError('only private regular SOURCE/META')
    blocks = []
    digest = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        while True:
            block = stream.read(2**20)
            if not block:
                break
            blocks.append(block)
            digest.update(block)
            size += len(block)
    if before != identity(path) or size != before[4]:
        raise ValueError('full EOF SHA7ID changed')
    return b''.join(blocks), {'name':path.name,'path':str(path),'sha256':digest.hexdigest(),'size_bytes':size,'identity':before}

author_raw, author_pin = read(AUTHOR/'MANIFEST.json')
if author_pin['sha256'] != EXPECTED_AUTHOR_SHA:
    raise ValueError('author seal changed')
author = json.loads(author_raw)
names = sorted(x.name for x in AUTHOR.iterdir())
directory_before = identity(AUTHOR)
if names != sorted([x['name'] for x in author['members']]+['MANIFEST.json']):
    raise ValueError('author full SOURCE namespace changed')
for member in author['members']:
    _, pin = read(AUTHOR/member['name'])
    if any(pin[k] != member[k] for k in ('name','path','sha256','size_bytes','identity')):
        raise ValueError('author fullSOURCE SHA7ID changed')
if directory_before != identity(AUTHOR) or names != sorted(x.name for x in AUTHOR.iterdir()):
    raise ValueError('author SOURCE directory changed')

report_raw, report_pin = read(ROOT/'INDEPENDENT_REVIEW.json')
if report_pin['sha256'] != EXPECTED_REPORT_SHA:
    raise ValueError('independent review changed')
report = json.loads(report_raw)
if report['blockers'] != [] or report['source_only'] is not True or report['UNKNOWN_Q'] is not None or not all(type(c['value']) is bool and c['value'] is True for c in report['checks']):
    raise ValueError('independent Source contract changed')
receipt_raw, receipt_pin = read(ROOT/'actual_SOURCE_tool_returns.json')
receipt = json.loads(receipt_raw)
tr = receipt['actual_source_review_tool_return']
if type(tr['exit_code']) is not int or tr['exit_code'] != 0 or 'session_id' in tr or tr['chunk_id'] != '67a368':
    raise ValueError('true closed typed SOURCE review tool return required')
members = []
for path in sorted(ROOT.iterdir()):
    if path.name == 'sealed_manifest.json':
        raise ValueError('no reseal or retry')
    _, pin = read(path)
    members.append(pin)
for pin in members:
    _, after = read(Path(pin['path']))
    if after != pin:
        raise ValueError('review member changed')
manifest = {
    'schema':'AXMAT_V21B_INDEPENDENT_OLD_CONSTRUCTOR_ORACLE_SOURCE_REVIEW_MANIFEST_V1',
    'status':'SEALED_SOURCE_PASS_NOT_RUNTIME_QUALIFICATION',
    'source_only':True,'runtime_executed':False,
    'members':members,'member_count':len(members),
    'total_member_bytes':sum(x['size_bytes'] for x in members),
    'author_sealed_manifest':author_pin,
    'author_complete_member_count':27,'author_complete_member_bytes':371881,
    'independent_review':report_pin,'actual_SOURCE_tool_return':tr,
    'checks':len(report['checks']),'blockers':[],
    'helper_API_guard_business_executed':False,
    'current_graph_ART_witness_numeric_payload_read':False,
    'canonical_project_D_E_results_written':False,
    'actual_success_pins':None,'UNKNOWN_Q':None,'UNKNOWN_BUSINESS_PINS':None,
    'helper_metadata_qualified':False,'whole_business_INPUT_qualified':False,
    'native_RSS_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'physical_balance_qualified':False
}
with (ROOT/'sealed_manifest.json').open('x') as stream:
    json.dump(manifest,stream,indent=2,allow_nan=False)
    stream.write('\n');stream.flush();os.fsync(stream.fileno())
_, sealed = read(ROOT/'sealed_manifest.json')
print(json.dumps({'status':manifest['status'],'manifest':sealed,'review_sha256':report_pin['sha256'],'member_count':len(members),'checks':manifest['checks'],'blockers':[],'author_source_unchanged':True,'runtime_executed':False,'UNKNOWN_Q':None},allow_nan=False))
