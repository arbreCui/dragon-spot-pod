import ast
import hashlib
import json
from pathlib import Path

BASE=Path('/Users/wen/spot/validation/storage_cleanup_ninth_20261009')
OUT=Path('/private/tmp/spot_ninth_lossless_archive_source_independent_review_20261009')

def pin(p,wanted=None):
    p=Path(p);a=p.lstat();raw=p.read_bytes();b=p.lstat();before=[a.st_dev,a.st_ino,a.st_mode,a.st_size,a.st_mtime_ns,a.st_ctime_ns,a.st_nlink];after=[b.st_dev,b.st_ino,b.st_mode,b.st_size,b.st_mtime_ns,b.st_ctime_ns,b.st_nlink]
    assert before==after and not p.is_symlink()
    h=hashlib.sha256(raw).hexdigest()
    if wanted:assert h==wanted,(str(p),h)
    return raw,dict(path=str(p),sha256=h,size=len(raw),identity=before)

def main():
    new,np=pin(BASE/'cleanup_exact_files.py','323a011638b5261419fed84ef6e85854a001bbe22b3a7067faca0a70d5f9e3ab')
    parent,pp=pin(BASE/'cleanup_ninth_before_lossless_archive.py','7885cc2f6a29d2c60182d0c66c93eb500691992c444323f3e6845d281335fca7')
    pack,pk=pin(BASE/'pack_old_material_intermediates.py','6125b048be62d76041cdcc3f0b307aff74115172d7cb0b1a10bd4e07a6d53e4a')
    restore,rp=pin(BASE/'restore_archived_material_intermediates.py','26a4c2616f6df2662a0ff69659eb9e0b05b5d98e8dfd6a67e37f4eec13f8adf1')
    duplicate_restore,drp=pin(BASE/'restore_retired_work_copies.py','53a51f0f70c5194b13328d01b356d33260cd1b310753fda743b8ad6af6a687bd')
    oldcopy,oldcp=pin(Path('/Users/wen/spot/validation/storage_cleanup_eighth_20261009/restore_retired_work_copies.py'),drp['sha256']);assert oldcopy==duplicate_restore
    diff,dp=pin(BASE/'cleanup_lossless_archive_transition.diff','feba7716dd9a570a02ab6636e88cd16bd9b2cae87ce96ee7253bdd1ffb40ae24')
    inputraw,ip=pin(BASE/'material_archive_input.json','dfb4c46ab3b9add27c4430dfadf932285841f5bcede40958c20c52203740702b')
    rows=json.loads(inputraw);assert len(rows)==len({r['path'] for r in rows})==89
    sources={'cleanup':new.decode(),'parent':parent.decode(),'pack':pack.decode(),'restore':restore.decode(),'duplicate_restore':duplicate_restore.decode()}
    for s in sources.values():ast.parse(s)
    s=sources['cleanup'];p=sources['parent']
    start=s.index('   if allowed_tape:\n')
    end=s.index("   proof=c['historical_payload_proof'];",start)
    insertion=s[start:end]
    inverse=s[:start]+s[end:]
    regions=[dict(old='import argparse, collections, hashlib,',new='import argparse, collections, gzip, hashlib,'),dict(old="elif c['category']=='TERMINAL_OLD_INTERMEDIATE_PAYLOAD':",new="elif c['category'] in ('TERMINAL_OLD_INTERMEDIATE_PAYLOAD','GZIP_ARCHIVED_OLD_MATERIAL_INTERMEDIATE'):"),dict(old="('EXACT_DUPLICATE_OLD_WORK_COPY','EXACT_RECONSTRUCTIBLE_REHEARSAL_TAR','TERMINAL_OLD_INTERMEDIATE_PAYLOAD')",new="('EXACT_DUPLICATE_OLD_WORK_COPY','EXACT_RECONSTRUCTIBLE_REHEARSAL_TAR','TERMINAL_OLD_INTERMEDIATE_PAYLOAD','GZIP_ARCHIVED_OLD_MATERIAL_INTERMEDIATE')")]
    for r in regions:
        assert inverse.count(r['new'])==1 and p.count(r['old'])==1
        inverse=inverse.replace(r['new'],r['old'],1)
    assert inverse.encode()==parent
    assert ast.dump(ast.parse(inverse),include_attributes=False)==ast.dump(ast.parse(p),include_attributes=False)
    (OUT/'reconstructed_pre_archive_cleanup.py').write_bytes(inverse.encode())
    functionproof=[]
    for n in ast.parse(s).body:
        if isinstance(n,ast.FunctionDef):
            o=next(x for x in ast.parse(p).body if isinstance(x,ast.FunctionDef) and x.name==n.name)
            i=next(x for x in ast.parse(inverse).body if isinstance(x,ast.FunctionDef) and x.name==n.name)
            body=ast.get_source_segment(s,n);ob=ast.get_source_segment(p,o);ib=ast.get_source_segment(inverse,i)
            assert ib==ob
            functionproof.append(dict(name=n.name,line=n.lineno,new_source_sha256=hashlib.sha256(body.encode()).hexdigest(),original_source_sha256=hashlib.sha256(ob.encode()).hexdigest(),unchanged_byte_exact=body==ob,full_inverse_byte_exact=True))
    assert {r['name'] for r in functionproof if not r['unchanged_byte_exact']}=={'main','verify_candidates'}
    pktext=sources['pack'];rt=sources['restore']
    cleanup_checks={
      'direct_unique_material_tape_category_rejected':"if allowed_tape:\n    assert c['category']=='GZIP_ARCHIVED_OLD_MATERIAL_INTERMEDIATE'" in insertion,
      'map9_still_only_unique_category':"else:assert c['category']=='TERMINAL_OLD_INTERMEDIATE_PAYLOAD'" in insertion,
      'canonical_archive_exact_PATH_required':"packed==OUT/'packed_material_intermediates'/(str(relative)+'.gz') and packed.parent.resolve(strict=True)==packed.parent" in insertion,
      'fresh_complete_compressed_identity_SHA_size_pin_first':'saved=expected(backup)' in insertion,
      'bounded_decompression_exact_raw_size_SHA_then_backup_identity':"length<=fresh['size']" in insertion and "length==fresh['size'] and digest.hexdigest()==fresh['sha256'] and identity(packed)==saved['identity']" in insertion,
      'original_receipt_and_root_seal_not_replaced':"type(record['returncode']) is int and record['returncode']==0 and record['output_sha256']==fresh['sha256']" in s and "entries[str(p.relative_to(owner))]==fresh['sha256']" in s,
      'whole_current_closure_cold_extra_and_whole_nonselected_gates_unchanged':"files |= set(m['current_cold_extra_protected_files'])" in s and "after_inventory=inventory(selected);assert after_inventory==baseline" in s,
      'apply_still_requires_preflight_and_independent_PASS_SHA':"rv['status']=='PASS' and rv['manifest_sha256']==mp['sha256'] and rv['preflight_sha256']==pp['sha256']" in s}
    pack_checks={
      'no_unlink_rmdir_delete_calls':not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('unlink','rmdir','rmtree','remove') for n in ast.walk(ast.parse(pktext))),
      'original_input_JSON_SHA_hash_bound_89_unique_paths':"pin(source)['sha256'] == args.input_sha256" in pktext and "len(rows) == 89 and len({r['path'] for r in rows}) == 89" in pktext,
      'original_canonical_named_families_pendf_groupr_tape30_only':"rel.parts[0] in FAMILIES and p.name == 'tape30' and p.parent.name in ('pendf', 'groupr')" in pktext and 'p.parent.resolve(strict=True) == p.parent' in pktext,
      'raw_exact_identity_regular_singlelink_before':"before == row['identity'] and stat.S_ISREG(before[2]) and before[-1] == 1" in pktext,
      'exclusive_new_PACK_and_canonical_backup_parents':'not PACK.exists()' in pktext and "target.open('xb')" in pktext and 'target.parent.resolve(strict=True) == target.parent' in pktext,
      'gzip6_empty_filename_mtime0':"gzip.GzipFile(filename='', mode='wb', compresslevel=6, mtime=0, fileobj=destination)" in pktext,
      'stream_complete_raw_SHA_size_and_same_identity_after':"identity(p) == before and size == row['size'] and h.hexdigest() == row['sha256']" in pktext,
      'backup_full_SHA_then_independent_gzip_decode_complete_SHA_size':"backup = pin(target)" in pktext and "verified = verify_gzip(target, row['size'], row['sha256'])" in pktext,
      'per_file_ledger_flush_fsync_and_PASS_report_only_after_all':"ledger.flush(); os.fsync(ledger.fileno())" in pktext and "originals_removed=0" in pktext}
    restore_checks={
      'default_lists_only_and_explicit_mutually_exclusive_restore':"if not args.restore_all and not args.path:" in rt and 'assert not (args.restore_all and args.path)' in rt,
      'only_exactlisted_GZIP_manifest_category':"r['category'] == 'GZIP_ARCHIVED_OLD_MATERIAL_INTERMEDIATE'" in rt and 'assert len(rows) == 1' in rt,
      'target_named_canonical_and_archive_exact_canonical_location':"target, rel = material_path(row['path'])" in rt and "backup == PACK / (str(rel) + '.gz') and backup.parent.resolve(strict=True) == backup.parent" in rt,
      'full_compressed_size_SHA_and_full_decompressed_SHA_before_any_write':"fresh['sha256'] == expected['sha256'] and fresh['size'] == expected['size']" in rt and "verify_gzip(backup, row['size'], row['sha256'])" in rt,
      'existing_target_must_equal_and_never_overwritten':"current['size'] == row['size'] and current['sha256'] == row['sha256']" in rt and "if target.exists():\n            continue" in rt and "target.open('xb')" in rt,
      'copy_stream_bounded_and_final_full_SHA_size':"size <= row['size']" in rt and "size == row['size'] and h.hexdigest() == row['sha256']" in rt,
      'failure_only_cleans_exclusively_created_current_file':'except BaseException:' in rt and 'destination.close(); target.unlink(); raise' in rt,
      'original_mode_and_mtime_restored':"os.chmod(target, stat.S_IMODE(row['identity'][2]))" in rt and "os.utime(target, ns=(row['identity'][4], row['identity'][4]))" in rt,
      'old_round_restore_order_explicit':'Restore archived material originals before using earlier rounds' in rt}
    for checks in (cleanup_checks,pack_checks,restore_checks):assert all(checks.values()),checks
    input_scope=[]
    for r in rows:
        p=Path(r['path']);rel=p.relative_to('/Users/wen/spot/validation/artifacts');assert rel.parts[0] in ('d4a-final-four-fuel-temperature-run-20261002','d4a-remaining-fuel-temperature-run-20261001','d4a-remaining-temperature-run-20261001') and p.name=='tape30' and p.parent.name in ('pendf','groupr');assert r['identity'][-1]==1 and r['identity'][3]==r['size'];assert r['historical_payload_proof']['format']=='NJOY_RECEIPT_OUTPUT';input_scope.append(r['path'])
    report=dict(status='PASS_SOURCE_ONLY_LOSSLESS_MATERIAL_ARCHIVE_AND_RESTORE',scope='Complete static cleanup inverse plus pack/restore source review; actual backup terminal/content, manifest and preflight are separate future witnesses.',audit_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cleanup_source=np,parent_cleanup=pp,pack_source=pk,archive_restore_source=rp,duplicate_restore_source=drp,duplicate_restore_parent=oldcp,transition_diff=dp,full_inverse_byte_exact=True,full_inverse_AST_equal=True,inverse_text_regions=regions,added_gzip_verification_region=dict(sha256=hashlib.sha256(insertion.encode()).hexdigest(),source=insertion),all_11_function_full_inverse_proof=functionproof,cleanup_checks=cleanup_checks,pack_checks=pack_checks,restore_checks=restore_checks,fixed_pack_input=ip,fixed_pack_input_path_count=89,fixed_pack_input_paths=input_scope,raw_logical_bytes=sum(r['size'] for r in rows),raw_allocated_bytes=sum(r['allocated_bytes'] for r in rows),direct_unique_tape_retirement_disabled=True,unique_map9_original_receipt_gate_unchanged=True,prior_round_restore_primary_preservation='Original 89 byte streams remain losslessly recoverable at the exact paths before invoking earlier duplicate-copy restore tools. Their original receipts/seals are immutable. No archive size/compression benefit is predicted from source alone.',actual_future_witnesses=dict(pack_terminal=None,pack_completed_report_sha256=None,all_89_backup_payloads_fresh_verified=None,manifest_sha256=None,preflight_sha256=None,actual_cleanup_result_sha256=None),limits=['No packing, restoration, cleanup preflight/apply, API, constructor, scientific solver or business PREP/RUN was invoked by this audit.','Only fixed pack input metadata was read; original 8.45GB payloads and live partial backups were intentionally not treated as terminal evidence. Actual completed pack must independently prove each full gzip plus lossless raw SHA/size before any retirement.','Restore provides exact original content/mode/mtime, not original inode/ctime. No historical whole replay or snapshot gate is credited as newly passed.','Packing failures can leave newly created partial backup files and an incomplete ledger, while original files remain untouched; fresh exclusive PACK creation prevents silent overwrite/retry.'],formal_or_ART_written=False,files_deleted=0)
    target=OUT/'independent_lossless_archive_source_review.json'
    with target.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status=report['status'],path=str(target),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),cleanup_sha256=np['sha256'],pack_sha256=pk['sha256'],restore_sha256=rp['sha256'],fixed_input_count=89,full_inverse_byte_exact=True,actual_pack_or_restore_or_delete_executed=False)))

if __name__=='__main__':main()
