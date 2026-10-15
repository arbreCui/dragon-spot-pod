"""UNREADY Source-only review skeleton. No candidate access before final freeze/RootGEN0."""
import ast, hashlib, json, os, stat
from pathlib import Path

def need(v, message):
    if v is not True: raise ValueError(message)
def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current7(p):
    q=Path(p['path']);s=q.lstat()
    need(q.is_absolute() and not any(x.is_symlink() for x in (q,*q.parents)), 'literal absolute path')
    need(stat.S_ISREG(s.st_mode) and identity(s)==p['identity'] and s.st_size==p['size_bytes'], 'exact current7')
def full_Source_metadata(p):
    current7(p);need(p['size_bytes']<8*2**20,'bounded Source/metadata8MiB')
    with Path(p['path']).open('rb') as f:
        need(identity(os.fstat(f.fileno()))==p['identity'],'opened metadata7')
        raw=f.read()
        need(identity(os.fstat(f.fileno()))==p['identity'],'EOF metadata7')
    need(len(raw)==p['size_bytes'] and hashlib.sha256(raw).hexdigest()==p['sha256'],'whole metadata SHA')
    current7(p);return raw

def complete_selected_union(ready, ready_pin, generation_pin):
    unique={}
    for p in ready['selected_Source_pins']+[ready_pin,generation_pin]:
        need(p['path'] not in unique or unique[p['path']]==p,'consistent fullPF role union')
        unique[p['path']]=p
    return list(unique.values())

def original_v2_failed_review_proof(review, tools, exact_review_pin):
    need(review['schema']=='INDEPENDENT_RESULT48_LOSSLESS_ARCHIVE_FORMAL_SOURCE_REVIEW_V1', 'v2 schema')
    need(review['status']=='FAIL_SOURCE_ONLY' and type(review['failure']) is dict, 'original failed classification')
    need(review['failure']['kind']=='TWO_OWNING_HOST_METADATA_PATHS_OMIT_ORIGINAL_STAGE_PREFIX' and len(review['failure']['blockers'])==2,'original two failures')
    r=tools['actual_review_return']
    need(tools['observed_closed'] is True and type(tools['original_integer_exit_code']) is int and tools['original_integer_exit_code']==0,'original completion0')
    need(r['chunk_id']=='bc7d7a' and type(r['exit_code']) is int and r['exit_code']==0 and not r.get('session_id'),'genuine original auditor0')
    output=json.loads(r['output'].strip().splitlines()[-1])
    need(output['status']=='FAIL_SOURCE_ONLY' and output['review_pin']==exact_review_pin,'original failure stdoutPF')
    need(review['publisher_admission_refused'] is True and review['business_admission_refused'] is True,'no prior admission')

def corrected_owning_host_paths(host_Source):
    need("runner.execute(stage,'serial_result48_byte_archive'" in host_Source,'same original serial stage')
    need("watchpath=out/(runner.records[0]['label']+'.watchdog.json')" in host_Source,'watch exact original record label')
    need("log=out/(runner.records[0]['label']+'.log')" in host_Source,'log exact original record label')
    need("stage=out/'archive-stage'" in host_Source,'original owning stage')

# Final actual READY/PLAN/GEN/prior-proof projection must be inspected before completing main.
# Never use a fixed selected count. Old48 plain + retained66: current7 only, twice.
# Compare five Source whole inverse; only the two host metadata paths may differ.
# Freeze complete auditor after AST, then execute once with supplied exact RootGEN0 pins.
if __name__=='__main__':
    raise SystemExit('UNREADY: awaiting author freeze and Root genuine SourceGEN0; do not execute')
