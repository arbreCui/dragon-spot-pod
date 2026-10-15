"""UNREADY independent Source-review primitives. Await real frozen retirement schemas."""
import hashlib,json,os,stat
from pathlib import Path

def need(v,m):
    if type(v) is not bool or not v:raise ValueError(m)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current7(p):
    need(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int and all(type(v)is int for v in p['identity'])and len(p['identity'])==7,'fullPF integer schema')
    q=Path(p['path']);s=q.lstat()
    need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes'],'exact current7')
def source_metadata(p):
    current7(p);need(p['size_bytes']<8*2**20,'Source/metadata8MiB')
    with Path(p['path']).open('rb')as f:
        need(ids(os.fstat(f.fileno()))==p['identity'],'opened metadata7');raw=f.read();need(ids(os.fstat(f.fileno()))==p['identity'],'EOF metadata7')
    need(len(raw)==p['size_bytes']and hashlib.sha256(raw).hexdigest()==p['sha256'],'whole Source/metadata SHA');current7(p);return raw

def known_actual_archive_post(review,tools,review_pin):
    need(review['schema']=='RECORDED_RESULT48_LOSSLESS_ARCHIVE_METADATA_POSTVERIFY_V1'and review['status']=='PASS_ACTUAL_ALL48_STREAMED_SHA_LENGTH_ARCHIVE_METADATA_ONLY_PLAINTEXT_RETAINED'and review['failure']is None and review['metadata_only']is True,'actual archive post schema/status')
    r=tools['actual_review_return']
    need(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and tools['original_integer_exit_code']==0 and r['chunk_id']=='3ab8b9'and type(r['exit_code'])is int and r['exit_code']==0 and not r.get('session_id'),'genuine original post0')
    need(json.loads(r['output'].strip().splitlines()[-1])['review_pin']==review_pin,'exact post stdoutfullPF')
    need(len(review['ordered48_original_plain_full_pins'])==len(review['ordered48_compressed_archive_full_pins'])==len(review['ordered48_entry_pins'])==48 and review['original_plain_bytes']==805236925 and review['gzip_bytes']==68959717,'actual complete48 retained plaintext and lossless byte archive proof')
    need(len(review['old30_historical_guard_pins'])==30 and len(review['new5_completed_A2_result_pins'])==5,'distinct historical role tables')

# Before formal completion: inspect frozen AUTHOR/PLAN/publisher/worker wrapper keys.
# Preserve all old nonzero raw records and real Root86373c0/post3ab8b90.
# Source/meta EOF/SHA only; target48/gzip48/SCI66 and other retained roles current7 only.
# Runtime worker must preserve owned501+nlink1, exact2 UID0 metadata exceptions,
# blindSHA+lsof1-empty+immediate dirfd7, original same-PID PS/resources/fresh final checks,
# readonly0 before execute, 65-root complete prefix, no new business OUT, no retries.
# No candidate paths, future pins or field aliases are assumed here.
if __name__=='__main__':raise SystemExit('UNREADY: waiting frozen retirement Source and exact schema/PFs')
