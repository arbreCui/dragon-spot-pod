"""Independent strict single-gzip streaming and fresh raw SHA audit, TMP only.
No pack/restore business import, decompressed output file, unlink or preflight.
"""
import collections
import hashlib
import json
import os
from pathlib import Path
import stat
import time
import zlib

ROOT=Path('/Users/wen/spot')
R=ROOT/'validation/storage_cleanup_ninth_20261009'
PACK=R/'packed_material_intermediates'
OUT=Path('/private/tmp/spot_ninth_actual_lossless_material_backup_independent_review_20261009')
PRIOR=Path('/private/tmp/spot_ninth_material_intermediate_readonly_review_20261009')
CHUNK=4*1024**2
PINS={}
START=time.monotonic()

def ident(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def checked_path(raw,scope):
    p=Path(raw)
    assert p.is_absolute() and str(p)==raw and '..' not in p.parts and p.is_relative_to(scope)
    assert p.parent.resolve(strict=True)==p.parent
    return p

def pin(p,expected=None,expected_identity=None):
    p=Path(p);before=ident(p)
    assert stat.S_ISREG(before[2]) and before[-1]==1
    if str(p) not in PINS:
        h=hashlib.sha256();n=0
        with p.open('rb') as f:
            s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]==before
            for b in iter(lambda:f.read(CHUNK),b''):h.update(b);n+=len(b)
            s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]==before
        assert ident(p)==before and n==before[3]
        PINS[str(p)]=dict(path=str(p),identity=before,size=n,sha256=h.hexdigest(),allocated_bytes=p.stat().st_blocks*512,stable_full_read=True)
    d=PINS[str(p)];assert d['identity']==before
    if expected is not None:assert d['sha256']==expected,(str(p),d['sha256'],expected)
    if expected_identity is not None:assert before==expected_identity
    return d

def load(p,expected=None):
    d=pin(p,expected);b=Path(p).read_bytes()
    assert hashlib.sha256(b).hexdigest()==d['sha256'] and ident(Path(p))==d['identity']
    return json.loads(b)

def seal(p,expected):
    d=pin(p,expected);folder=p.parent;rows={}
    for l in p.read_text().splitlines():
        sha,relative=l.split(maxsplit=1);relative=relative.lstrip('*')
        assert not Path(relative).is_absolute() and '..' not in Path(relative).parts
        key=str(folder/relative);assert key not in rows;rows[key]=sha
    assert ident(p)==d['identity'];return rows

def strict_stream(backup,original):
    p=checked_path(backup['path'],PACK);before=ident(p)
    assert before==backup['identity'] and stat.S_ISREG(before[2]) and before[-1]==1
    compressed_h=hashlib.sha256();raw_h=hashlib.sha256();compressed_n=raw_n=0
    codec=zlib.decompressobj(31)  # gzip CRC/ISIZE checked by zlib; one member only.
    with p.open('rb') as stream:
        s=os.fstat(stream.fileno());assert [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]==before
        while block:=stream.read(CHUNK):
            assert not codec.eof, 'trailing byte/member after gzip EOF'
            compressed_h.update(block);compressed_n+=len(block)
            assert compressed_n<=backup['size']
            pending=block
            while pending:
                data=codec.decompress(pending,CHUNK)
                raw_h.update(data);raw_n+=len(data)
                assert raw_n<=original['size'], 'decompression beyond original byte count'
                pending=codec.unconsumed_tail
                assert not codec.unused_data, 'additional gzip member/trailing bytes'
                if codec.eof:
                    assert not pending
        assert codec.eof, 'truncated gzip member'
        final=codec.flush()
        raw_h.update(final);raw_n+=len(final)
        assert raw_n<=original['size']
        s=os.fstat(stream.fileno());assert [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]==before
    assert ident(p)==before and p.parent.resolve(strict=True)==p.parent
    assert compressed_n==backup['size']==before[3] and compressed_h.hexdigest()==backup['sha256']
    assert raw_n==original['size'] and raw_h.hexdigest()==original['sha256']
    row=dict(path=str(p),identity=before,size=compressed_n,sha256=compressed_h.hexdigest(),allocated_bytes=p.stat().st_blocks*512,stable_full_read=True)
    assert row['allocated_bytes']==backup['allocated_bytes'];PINS[str(p)]=row
    return dict(compressed_pin=row,decompressed_size=raw_n,decompressed_sha256=raw_h.hexdigest(),
                strict_single_member_gzip_CRC_ISIZE_EOF_passed=True,
                truncated_extra_member_trailing_bytes_and_size_overrun_rejected_by_audit_source=True,
                decompressed_payload_saved=False)

def save(n,d):
    p=OUT/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

input_path=R/'material_archive_input.json'
inputs=load(input_path,'dfb4c46ab3b9add27c4430dfadf932285841f5bcede40958c20c52203740702b')
report_path=R/'packed_material_intermediate_backups.json'
report=load(report_path,'d5834da3209265f9d0f4ad571f4da0c8a570558cfe39b7120750f5dad156aec9')
assert report['status']=='PASS' and report['originals_removed']==0 and report['input_sha256']==pin(input_path)['sha256']
assert len(inputs)==len(report['records'])==89 and len({r['path'] for r in inputs})==89
assert [r['original'] for r in report['records']]==inputs
ledger_path=R/'backup_creation_ledger.jsonl'
pin(ledger_path);ledger=[json.loads(l) for l in ledger_path.read_text().splitlines()]
assert ledger==report['records']
terminal=load(R/'backup_terminal_observation.json','67a59baa8aa87be670e84c30c58c316c478aa4dfabb4955573be2e00f28849cb')
assert terminal['initial_chunk_id']=='5cd1ed' and terminal['session_id']==48986 and terminal['terminal_chunk_id']=='0daf01'
assert terminal['closed'] is True and terminal['exit_code']==0 and terminal['files_deleted']==0
assert terminal['backup_report_sha256']==pin(report_path)['sha256'] and terminal['stderr_bytes']==0
pin(R/'backup.stdout',terminal['stdout_sha256']);assert pin(R/'backup.stderr')['size']==0
stdoutsummary=json.loads((R/'backup.stdout').read_text().splitlines()[-1]);assert stdoutsummary==terminal['summary']
assert stdoutsummary['status']=='PASS' and stdoutsummary['backups']==89 and stdoutsummary['originals_removed']==0
packsource=pin(R/'pack_old_material_intermediates.py','6125b048be62d76041cdcc3f0b307aff74115172d7cb0b1a10bd4e07a6d53e4a')
restoresource=pin(R/'restore_archived_material_intermediates.py','26a4c2616f6df2662a0ff69659eb9e0b05b5d98e8dfd6a67e37f4eec13f8adf1')
priorrows=load(PRIOR/'exact_material_intermediate_retirement_candidates.json',
               '29f7b50a905aef95dfd035a9c3bc5802606fafe7d5a5b76c3c83bf2589115fc7')
priorby={r['path']:r for r in priorrows}
assert set(priorby)=={r['path'] for r in inputs}
priorR=PRIOR/'prior_cleanup_restoration_dependency_review'
evidence_manifest=load(priorR/'evidence_manifest.json','c5a684dde17188dc540572997f3db5e7c550910e9c620485ad6b4f0e87a03ad7')
evidencepins={r['path']:r['sha256'] for r in evidence_manifest['files']}
edges_path=priorR/'prior_actual_second_round_120_retirement_primary_edges.json'
edges=load(edges_path,evidencepins[str(edges_path)])
assert len(edges)==120 and {r['primary_path'] for r in edges}==set(priorby)

checked=[]
recovery=[]
seals={}
for i,r in enumerate(report['records'],1):
    original,backup=r['original'],r['backup'];p=checked_path(original['path'],ROOT/'validation/artifacts')
    assert p.name=='tape30' and p.parent.name in {'pendf','groupr'}
    prior=priorby[str(p)]
    assert original['identity']==prior['identity'] and original['sha256']==prior['sha256'] and original['size']==prior['bytes']
    rel=p.relative_to(ROOT/'validation/artifacts')
    assert backup['path']==str(PACK/(str(rel)+'.gz'))
    raw=pin(p,original['sha256'],original['identity'])
    assert raw['size']==original['size'] and raw['allocated_bytes']==original['allocated_bytes']
    proof=original['historical_payload_proof'];assert proof['format']=='NJOY_RECEIPT_OUTPUT'
    rec=load(proof['path'],proof['sha256'])
    assert rec['returncode']==0 and rec['output_sha256']==raw['sha256']
    sp=Path(proof['result_manifest_path'])
    if str(sp) not in seals:seals[str(sp)]=seal(sp,proof['result_manifest_sha256'])
    table=seals[str(sp)]
    assert table[str(p)]==raw['sha256'] and table[proof['path']]==proof['sha256']
    decoded=strict_stream(backup,original)
    assert r['verified_decompressed']==dict(size=decoded['decompressed_size'],sha256=decoded['decompressed_sha256'])
    targets=[e for e in edges if e['primary_path']==str(p)]
    assert targets and all(e['expected_sha256']==raw['sha256'] and e['bytes']==raw['size'] for e in targets)
    current_edges=[]
    for e in targets:
        current=dict(e,actual_retired_target_now_absent=not os.path.lexists(e['retired_target']))
        current_edges.append(current)
    metadata=dict(original_mode_octal=oct(stat.S_IMODE(raw['identity'][2])),original_mtime_ns=raw['identity'][4],
                  original_size=raw['size'],original_sha256=raw['sha256'],
                  original_inode_is_historical_provenance_not_recreated_identity=raw['identity'][1],
                  gzip_mode_octal=oct(stat.S_IMODE(decoded['compressed_pin']['identity'][2])),
                  gzip_mtime_ns=decoded['compressed_pin']['identity'][4],
                  recovery_mode_and_mtime_come_from_original_identity=True)
    checked.append(dict(original_fresh_pin=raw,archive_fresh_verification=decoded,
                        original_stage_receipt_pin=pin(proof['path']),original_stage_receipt=rec,
                        original_result_manifest_pin=pin(sp),original_result_entry_matches=True,
                        source_metadata=metadata,prior_backed_duplicate_count=len(targets)))
    recovery.append(dict(archive_path=backup['path'],archive_sha256=backup['sha256'],archive_size=backup['size'],
                         step1_restore_primary_raw_path=str(p),step1_restore_SHA256=raw['sha256'],step1_restore_size=raw['size'],
                         step1_restore_metadata=metadata,step2_original_prior_copy_restore_targets=current_edges,
                         order='Verify protected archive -> restore exact raw primary at original absolute path -> restore each earlier retired duplicate from raw primary using immutable old mapping.',
                         original_source_mode_required_for_restored_raw=metadata['original_mode_octal'],
                         no_old_ledger_or_result_manifest_changes=True,actual_restore_executed=False))
    if i%15==0 or i==89:print(json.dumps(dict(independently_fresh_raw_and_strict_gzip_verified=i,total=89,elapsed_s=time.monotonic()-START)),flush=True)

assert len(checked)==89 and sum(x['prior_backed_duplicate_count'] for x in checked)==120
assert report['raw_allocated_bytes']==sum(x['original_fresh_pin']['allocated_bytes'] for x in checked)==8454860800
assert report['compressed_allocated_bytes']==sum(x['archive_fresh_verification']['compressed_pin']['allocated_bytes'] for x in checked)==2640285696
for p,d in PINS.items():assert ident(Path(p))==d['identity'] and Path(p).parent.resolve(strict=True)==Path(p).parent
summary=dict(status='PASS_ACTUAL_89_LOSSLESS_GZIP_FRESH_RAW_AND_PRIOR_120_RECOVERY_BINDING_ONLY',
             packed_material_intermediate_backups_sha256=pin(report_path)['sha256'],
             material_archive_input_sha256=pin(input_path)['sha256'],backup_creation_ledger_sha256=pin(ledger_path)['sha256'],
             root_actual_backup_terminal_pin=pin(R/'backup_terminal_observation.json'),root_actual_backup_terminal=terminal,
             fresh_original_count=89,fresh_compressed_count=89,strict_complete_single_member_gzip_verified_count=89,
             all_original_SHA_size_identity_unchanged=True,all_original_result_and_EXIT0_receipts_bound=True,
             original_raw_logical_bytes=sum(x['original_fresh_pin']['size'] for x in checked),
             original_raw_allocated_bytes=report['raw_allocated_bytes'],
             compressed_logical_bytes=sum(x['archive_fresh_verification']['compressed_pin']['size'] for x in checked),
             compressed_allocated_bytes=report['compressed_allocated_bytes'],
             prospective_raw_minus_compressed_allocated_bytes=report['raw_allocated_bytes']-report['compressed_allocated_bytes'],
             prospective_raw_minus_compressed_GiB=(report['raw_allocated_bytes']-report['compressed_allocated_bytes'])/1024**3,
             actual_raw_deletion_count=0,actual_space_recovered_by_deletion=None,
             prior_actual_duplicate_restore_edges=120,explicit_restore_order_maps=89,
             observed_original_mode_counts=dict(collections.Counter(x['source_metadata']['original_mode_octal'] for x in checked)),
             pack_source_pin=packsource,restore_source_pin=restoresource,
             independent_fullread_pin_count=len(PINS),independent_fullread_physical_source_bytes=sum(x['size'] for x in PINS.values()),
             independent_decoded_byte_count=sum(x['archive_fresh_verification']['decompressed_size'] for x in checked),
             saved_decompressed_payload_bytes=0,restore_or_compression_executed=False,
             formal_project_or_ART_writes=False,business_import_API_ctor_PREP_RUN=False,
             any_new_science_accuracy_RSS_memory_admission_qualification=False,
             review_elapsed_s=time.monotonic()-START,
             limits=['Independent verification is actual archive integrity and reconstruction bytes to a hash sink only. No restoration, deletion, preflight/apply, production API, native solver or scientific admission ran.',
                     'Original89 raw primary paths remain present and independently fresh-full-SHA identical. Direct retirement without protected verified archives remains prohibited; any Root actual removal needs final manifest/preflight and independent review.',
                     'Archives must be permanently hard-protected recovery sources, with new restoration first recreating original raw89 before earlier120 duplicate mappings. No old manifest or retirement ledger is rewritten; recreated inode cannot be claimed identical to historical inode.',
                     'The original stage receipts say EXIT0; remaining-fuel and remaining-temperature overall FAILED_NO_RETRY facts from prior report remain unchanged. Archive integrity does not relabel any historical science result.',
                     'Prospective allocation difference is measured original/raw minus gzip leaf allocation; no deletion capacity credit or exclusive physical extent recovery is claimed. Source static review of final restoration and cleanup tools is a separate review.'])
save('independent_actual_lossless_backup_review.json',summary)
save('all_89_fresh_raw_strict_gzip_and_original_receipt_result_checks.json',checked)
save('all_89_archives_to_raw_primaries_to_prior_120_retired_copy_recovery_order.json',recovery)
save('all_actual_fullread_SHA_identity_pins.json',list(PINS.values()))
(OUT/'REPORT.txt').write_text(
 '实际89份归档独立完整核验通过：每份compressed SHA/size/identity/普通单链接/真实父路径均匹配，严格单gzip流式CRC/ISIZE/EOF及解压后原size/SHA完全匹配。\n'
 '89正本仍在：fresh全部原SHA/size/identity不变，原result.sha256条目与成功stage receipt完全对应；两批整体FAILED_NO_RETRY事实不改。\n'
 'Root真实归档工具5cd1ed/session48986→0daf01 CLOSED EXIT0绑定报告d5834da3/inputdfb4；没有删除。\n'
 f"raw名义分配8454860800B，gzip2640285696B；差{summary['prospective_raw_minus_compressed_allocated_bytes']}B/{summary['prospective_raw_minus_compressed_GiB']:.9f}GiB仅为拟议raw退役后的容量差，本次实际释放0。\n"
 '保存89 archive→原raw primary→120前轮被删copy完整恢复顺序及原mode/mtime/SHA/size。恢复原raw后才可用旧映射；归档须硬保护，不改旧结果/ledger，不声称恢复旧inode。\n'
 '只证明lossless备份字节资格；不证明实际restore、新512MiB/API/科学/CE资格。未业务import/PREP/RUN/restore/delete/正式写。\n')
print(json.dumps({k:summary[k] for k in ['status','fresh_original_count','strict_complete_single_member_gzip_verified_count','prior_actual_duplicate_restore_edges','original_raw_logical_bytes','compressed_logical_bytes','prospective_raw_minus_compressed_GiB','independent_fullread_pin_count','independent_fullread_physical_source_bytes','review_elapsed_s']},ensure_ascii=False),flush=True)
