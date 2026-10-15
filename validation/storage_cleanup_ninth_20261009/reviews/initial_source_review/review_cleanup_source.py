import ast
import hashlib
import json
from pathlib import Path

BASE=Path('/private/tmp/spot_ninth_storage_review_20261009')
OUT=Path('/private/tmp/spot_ninth_cleanup_source_independent_review_20261009')
OLD=Path('/Users/wen/spot/validation/storage_cleanup_eighth_20261009')

def pin(p,wanted=None):
    p=Path(p);a=p.lstat();raw=p.read_bytes();b=p.lstat();before=[a.st_dev,a.st_ino,a.st_mode,a.st_size,a.st_mtime_ns,a.st_ctime_ns,a.st_nlink];after=[b.st_dev,b.st_ino,b.st_mode,b.st_size,b.st_mtime_ns,b.st_ctime_ns,b.st_nlink]
    assert before==after and not p.is_symlink()
    sha=hashlib.sha256(raw).hexdigest()
    if wanted:assert sha==wanted,(str(p),sha)
    return raw,dict(path=str(p),sha256=sha,size=len(raw),identity=before)

def main():
    new,np=pin(BASE/'cleanup_exact_files.py','7885cc2f6a29d2c60182d0c66c93eb500691992c444323f3e6845d281335fca7')
    parent,pp=pin(BASE/'cleanup_eighth_parent.py','be4e2c1e3a5c5bf2856a8d7bf5fa5e8620506d64b3779b57a2360d0e8d6a9f65')
    formal_parent,fpp=pin(OLD/'cleanup_exact_files.py',pp['sha256']);assert formal_parent==parent
    diff,dp=pin(BASE/'cleanup_eighth_to_ninth.diff','861a29bc09005c31243adf26949a5c228004eeb0c6a5df1903baa95fb6a842d5')
    restore,rp=pin(BASE/'restore_retired_work_copies.py','53a51f0f70c5194b13328d01b356d33260cd1b310753fda743b8ad6af6a687bd')
    oldrestore,orp=pin(OLD/'restore_retired_work_copies.py',rp['sha256']);assert restore==oldrestore
    s=new.decode();p=parent.decode();ast.parse(s);ast.parse(p);ast.parse(restore.decode())
    start=s.index("  elif c['category']=='TERMINAL_OLD_INTERMEDIATE_PAYLOAD':\n")
    end=s.index("  else:\n   primary=retained[c['retained_primary']]",start)
    insertion=s[start:end]
    inverse=s[:start]+s[end:]
    regions=[dict(kind='round_identity',old='storage_cleanup_eighth_20261009',new='storage_cleanup_ninth_20261009'),dict(kind='round_identity',old='SPOT_EIGHTH_ROOT_FRESH_EXACT_CONTENT_PREFLIGHT_V1',new='SPOT_NINTH_ROOT_FRESH_EXACT_CONTENT_PREFLIGHT_V1'),dict(kind='round_identity',old='SPOT_EIGHTH_ACTUAL_EXACT_OLD_WORK_RETIREMENT_V1',new='SPOT_NINTH_ACTUAL_EXACT_OLD_WORK_RETIREMENT_V1'),dict(kind='new_explicit_category',old="('EXACT_DUPLICATE_OLD_WORK_COPY','EXACT_RECONSTRUCTIBLE_REHEARSAL_TAR')",new="('EXACT_DUPLICATE_OLD_WORK_COPY','EXACT_RECONSTRUCTIBLE_REHEARSAL_TAR','TERMINAL_OLD_INTERMEDIATE_PAYLOAD')")]
    for r in regions:
        assert inverse.count(r['new'])==1 and p.count(r['old'])==1,r
        inverse=inverse.replace(r['new'],r['old'],1)
    assert inverse.encode()==parent
    assert ast.dump(ast.parse(inverse),include_attributes=False)==ast.dump(ast.parse(p),include_attributes=False)
    (OUT/'reconstructed_eighth_parent.py').write_bytes(inverse.encode())
    functions=[]
    ot=ast.parse(p);nt=ast.parse(s);it=ast.parse(inverse)
    for n in nt.body:
        if isinstance(n,ast.FunctionDef):
            oldnode=next(x for x in ot.body if isinstance(x,ast.FunctionDef) and x.name==n.name)
            invnode=next(x for x in it.body if isinstance(x,ast.FunctionDef) and x.name==n.name)
            oldbody=ast.get_source_segment(p,oldnode);newbody=ast.get_source_segment(s,n);invbody=ast.get_source_segment(inverse,invnode)
            assert invbody==oldbody
            functions.append(dict(name=n.name,line=n.lineno,new_sha256=hashlib.sha256(newbody.encode()).hexdigest(),old_sha256=hashlib.sha256(oldbody.encode()).hexdigest(),byte_exact_to_parent=newbody==oldbody,full_inverse_to_parent_byte_exact=True))
    assert {f['name'] for f in functions if not f['byte_exact_to_parent']}=={'verify_candidates','main'}
    unique_checks={
      'map_exact_one_historical_family':"relative.parts[0]=='axial-material-production-qualified-AB-compensated-20261004'" in insertion,
      'map_three_exact_maps':"relative.parts[2] in ('map001','map002','map003')" in insertion,
      'map_only_AAA_depth4_three_exact_basenames':"relative.parts[1]=='AAA'" in insertion and 'len(relative.parts)==4' in insertion and "relative.name in ('candidate_radial.xsm','candidate_snapshots.xsm','projected_proposal.xsm')" in insertion,
      'map_fresh_historic_SHA_and_adjacent_original_result_map':"historic=pin(proof['path']);assert historic['sha256']==proof['sha256']" in insertion and "Path(proof['path'])==p.parent/'result.json'" in insertion,
      'map_original_SEALED_STAGE_OUTPUTS_and_exact_output_SHA':"record['classification']=='SEALED_STAGE_OUTPUTS'" in insertion and "record['sha256'][proof['key']]==fresh['sha256']" in insertion,
      'tape_only_three_named_historical_families':"relative.parts[0] in ('d4a-final-four-fuel-temperature-run-20261002','d4a-remaining-fuel-temperature-run-20261001','d4a-remaining-temperature-run-20261001')" in insertion,
      'tape_only_tape30_under_pendf_or_groupr':"relative.name=='tape30' and relative.parent.name in ('pendf','groupr')" in insertion,
      'tape_original_adjacent_receipt_builtin_int_zero_output_SHA':"Path(proof['path'])==p.parent/'receipt.json'" in insertion and "type(record['returncode']) is int and record['returncode']==0 and record['output_sha256']==fresh['sha256']" in insertion,
      'tape_original_family_root_full_manifest_hash_and_same_exact_relative_entry':"seal['sha256']==proof['result_manifest_sha256']" in insertion and "owner==ROOT/'validation/artifacts'/relative.parts[0] and entries[str(p.relative_to(owner))]==fresh['sha256']" in insertion,
      'unknown_historical_proof_format_rejected':"raise ValueError('unrecognized historical payload proof')" in insertion}
    assert all(unique_checks.values()),unique_checks
    preserved_checks={
      'optimization_disabled':'if not __debug__:' in s,
      'canonical_artifact_and_parent_no_alias':'p.parent.resolve(strict=True)!=p.parent' in s,
      'selected_regular_stable_fresh_SHA_singlelink':"fresh=expected(c);assert fresh['identity'][-1]==1" in s,
      'current_whole_graph_all_strings_old_index_namespace_alias_and_critical_scope':"files=absolute|set(index['protected_files'])|set(index['inbound_alias_targets'])" in s and "set(m['critical_roots'])" in s,
      'future_cold_extra_exact_path_protection':"files |= set(m['current_cold_extra_protected_files'])" in s,
      'all_project_inbound_symlink_screen':"assert not any(Path(q)==target or Path(q).is_relative_to(target) for q in selected)" in s,
      'source_SHA_manifest_bound':"pin(Path(__file__))['sha256']==m['cleanup_source_sha256']" in s,
      'all_retained_primaries_and_review_sources_fresh':"kept=[expected(p) for p in m['retained_primaries']]" in s and "for p in m['source_and_review_pins']:expected(p)" in s,
      'preflight_full_nonselected_inventory_before_after':"before=inventory(selected);candidates=verify_candidates(m);after=inventory(selected);assert before==after" in s,
      'preflight_branch_returns_before_apply':"baseline=before)));return" in s,
      'apply_binds_manifest_preflight_independent_PASS_two_SHA':"rv['status']=='PASS' and rv['manifest_sha256']==mp['sha256'] and rv['preflight_sha256']==pp['sha256']" in s,
      'apply_rechecks_entire_baseline_and_full_candidate_before_unlink':"baseline=inventory(selected);assert baseline==pf['preservation_baseline']" in s and "actual=verify_candidates(m);assert actual==pf['verified_candidates']" in s,
      'exact_ledger_per_deleted_category_fsync':"category=c['category'],deleted=True" in s and 'os.fsync(ledger.fileno())' in s,
      'post_delete_all_absent_full_nonselected_and_full_kept_SHA':"after_inventory=inventory(selected);assert after_inventory==baseline" in s and "for p in m['retained_primaries']+m['source_and_review_pins']+[m['graph_pin'],m['old_index_pin']]:expected(p)" in s}
    assert all(preserved_checks.values()),preserved_checks
    restore_text=restore.decode();assert "rows = [row for row in manifest['candidates'] if row['category'] == 'EXACT_DUPLICATE_OLD_WORK_COPY']" in restore_text
    assert "raise ValueError('path is not an exact retired work copy')" in restore_text
    report=dict(status='PASS_SOURCE_ONLY_NINTH_CLEANUP_DRAFT',scope='Static complete inverse and explicit added unique old intermediate allowlist only; no preflight or apply executed.',audit_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),new_cleanup_source=np,parent_snapshot=pp,parent_formal=fpp,diff=dp,restoration_source=rp,restoration_parent_formal=orp,full_inverse_byte_exact=True,full_inverse_AST_equal=True,identity_and_category_inverse_regions=regions,inserted_unique_payload_proof_region=dict(sha256=hashlib.sha256(insertion.encode()).hexdigest(),source=insertion),all_function_source_inverse=functions,unique_payload_checks=unique_checks,all_original_safety_checks_preserved=preserved_checks,allowed_unique_map_paths=['/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-compensated-20261004/AAA/'+m+'/'+n for m in ('map001','map002','map003') for n in ('candidate_radial.xsm','candidate_snapshots.xsm','projected_proposal.xsm')],allowed_unique_tape_pattern=dict(families=['d4a-final-four-fuel-temperature-run-20261002','d4a-remaining-fuel-temperature-run-20261001','d4a-remaining-temperature-run-20261001'],parent_basename=['pendf','groupr'],basename='tape30',original_receipt_builtin_int0_and_output_SHA_required=True,original_family_root_result_manifest_full_SHA_and_relative_file_SHA_required=True),exact_restorer_byte_exact_to_eighth=True,unique_payloads_excluded_from_automatic_restore=True,preflight_binding_fields_not_available=dict(manifest_sha256=None,preflight_sha256=None,actual_cleanup_result_sha256=None),conditions_before_any_apply=['Root must create an exact final manifest and bind all current V8/cold6248/critical/source proof bytes, retained conclusions/main results and every original unique receipt/manifest.','Independent actual preflight must fresh-verify every selected and primary file and compare the whole nonselected inventory. Source-only PASS does not authorize apply or substitute for that report.','Unique intermediate retirement has no byte-exact automatic restore; retained reproducibility resources may require a newly declared numerical rebuild. Do not rewrite original sealed receipts or imply those whole historical verifiers continue passing after deletion.'],static_notes=['The map allowlist is exactly nine paths. The tape gate is a named three-family plus pendf/groupr/tape30 pattern, bounded further by the exact hash-bound final candidate manifest and original family result entry. No wildcard traversal/deletion is performed by this tool.','Malformed shallow map paths fail closed with an index error before deletion; no expansion of the accepted map path set results.','Original inherited parser/TOCTOU and receipt assumptions remain byte-exact; no new safety exception or arbitrary payload category was introduced.'],files_deleted=0,formal_or_ART_written=False,business_API_import_PREP_RUN_or_apply_executed=False)
    target=OUT/'independent_cleanup_source_review.json'
    with target.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status=report['status'],path=str(target),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),new_cleanup_source_sha256=np['sha256'],function_count=len(functions),all_inverse_byte_exact=True,restore_byte_exact=True,unique_automatic_restore=False,executed_preflight_or_apply=False)))

if __name__=='__main__':main()
