"""Narrow read-only prior1-8 recovery source cross for proposed ninth176.
No candidate full-payload rereview, compression, deletion, restore or business.
"""
import collections
import hashlib
import json
import os
from pathlib import Path
import stat
import time

OUT=Path('/private/tmp/spot_ninth_prior_restore_cross_union_review_20261009')
PRIOR=Path('/private/tmp/spot_ninth_material_intermediate_readonly_review_20261009/prior_cleanup_restoration_dependency_review')
START=time.monotonic()
PINS={}

def ident(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def read(p,expected):
    p=Path(p);before=ident(p);b=p.read_bytes()
    assert ident(p)==before and stat.S_ISREG(before[2])
    sha=hashlib.sha256(b).hexdigest();assert sha==expected,(str(p),sha,expected)
    PINS[str(p)]={'path':str(p),'identity':before,'sha256':sha,'bytes':len(b),'stable_full_read':True}
    return json.loads(b)

def save(n,d):
    p=OUT/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

sourcepath=PRIOR/'all_eight_rounds_explicit_restoration_source_paths_and_fresh_stat.json'
sources=read(sourcepath,'2825c67d9c42077be4956935493ca383be41148a15edde38efc76ce74a2b305f')
priorpins_path=PRIOR/'all_eight_rounds_manifest_preflight_ledger_and_source_fresh_pins.json'
# Bind the unmodified preceding evidence-manifest entry, then fresh-pin source docs.
manifest_path=PRIOR/'evidence_manifest.json'
manifest=read(manifest_path,'c5a684dde17188dc540572997f3db5e7c550910e9c620485ad6b4f0e87a03ad7')
manifest_by_path={r['path']:r for r in manifest['files']}
priorpins=read(priorpins_path,manifest_by_path[str(priorpins_path)]['sha256'])
original_source_doc_fresh_pins=[]
original_source_identity_only=[]
for r in priorpins:
    p=Path(r['path']);assert ident(p)==r['identity'],('prior source identity changed',str(p))
    if p.is_relative_to(Path('/Users/wen/spot/validation')) and '/artifacts/' not in str(p):
        b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==r['sha256'] and ident(p)==r['identity']
        original_source_doc_fresh_pins.append(dict(r,fresh_read_now=True))
    else:
        original_source_identity_only.append(dict(path=str(p),identity=r['identity'],SHA_not_repeated_in_cross_only_review=True))

groups=(
 ('unique_compensated9','/private/tmp/spot_ninth_storage_review_20261009/root_old_compensated_intermediate_proposal.json',
  '120c4e0fc45fc97dc042907a64f461298c29adc5b4bad9529d46e24112233eb3','candidates',False,9),
 ('legacy_exact8','/private/tmp/spot_storage_ninth_legacy_snapshot_candidate_review_20261009/REPORT.json',
  '382caff4880e69bb550df544c189097bdef79da822a1332409726abd70182bf1','candidates',True,8),
 ('exact_replay_npz159','/private/tmp/spot_ninth_storage_build_cache_independent_review_20261009/exact_replay_npz_source_proof.json',
  'db3e8bc3bebc453be977516a28bc4b96b1482159157301cd0a0bfe5cc12f0df2','selected',False,159))
candidate_rows=[]
new_recovery_edges=[]
for name,p,sha,key,nested,count in groups:
    d=read(p,sha);rows=d[key];assert len(rows)==count
    for r in rows:
        c=r['candidate'] if nested else r
        path=Path(c['path']);now=ident(path)
        assert now==c['identity'] and stat.S_ISREG(now[2]) and now[-1]==1 and path.resolve()==path
        candidate_rows.append(dict(group=name,path=str(path),identity=now,
                                   size=now[3],allocated_bytes=c['allocated_bytes'],input_claimed_sha256=c['sha256'],
                                   source_report_path=p,source_report_sha256=sha,
                                   fresh_full_candidate_SHA_not_repeated_in_cross_only_review=True))
        primary=r.get('retained_primary')
        if primary:
            pp=Path(primary['path'] if isinstance(primary,dict) else primary)
            assert pp.is_file()
            if isinstance(primary,dict) and 'identity' in primary:assert ident(pp)==primary['identity']
            new_recovery_edges.append(dict(candidate=str(path),primary=str(pp),primary_canonical=str(pp.resolve()),
                                           primary_fresh_identity=ident(pp),group=name))
assert len(candidate_rows)==len({r['path'] for r in candidate_rows})==176
cpaths={r['path'] for r in candidate_rows}
old_index=collections.defaultdict(list)
for s in sources:old_index[s['source_path']].append(s)
existing={p for p,rows in old_index.items() if any(r['current_exists'] for r in rows)}
fresh_sources=[]
resolved_index=collections.defaultdict(list)
directory_index=[]
for p in sorted(existing):
    path=Path(p)
    assert os.path.lexists(path),('prior restoration source missing now',p)
    info=ident(path);resolved=str(path.resolve())
    fresh_sources.append(dict(path=p,identity=info,resolved=resolved,source_mentions=len(old_index[p])))
    resolved_index[resolved].append(p)
    if stat.S_ISDIR(path.stat().st_mode):directory_index.append(p)
cross=[]
for r in candidate_rows:
    p=r['path']
    direct=old_index.get(p,[])
    aliaspaths=[x for x in resolved_index.get(p,[]) if x!=p]
    dirs=[x for x in directory_index if Path(p).is_relative_to(Path(x))]
    hit=bool(direct or aliaspaths or dirs)
    cross.append(dict(**r,explicit_prior_source_mentions=direct,prior_resolved_source_aliases=aliaspaths,
                      prior_source_directory_ancestor_matches=dirs,
                      status='HOLD_PRIOR_RESTORE_SOURCE' if hit else 'PASS_PRIOR_RECOVERY_SOURCE_CROSS_ONLY',
                      no_new_cleanup_or_physics_approval=True))
new_edge_candidate_primary_intersections=[r for r in new_recovery_edges if r['primary'] in cpaths or r['primary_canonical'] in cpaths]
assert not new_edge_candidate_primary_intersections
holds=[r for r in cross if r['status']=='HOLD_PRIOR_RESTORE_SOURCE']
safe=[r for r in cross if r['status']!='HOLD_PRIOR_RESTORE_SOURCE']
bygroup=[]
for name,*_ in groups:
    rows=[r for r in cross if r['group']==name]
    bygroup.append(dict(group=name,count=len(rows),prior_restoration_source_overlap_count=sum(r['status']=='HOLD_PRIOR_RESTORE_SOURCE' for r in rows),
                        candidate_allocated_bytes=sum(r['allocated_bytes'] for r in rows)))
summary=dict(status='PASS_PRIOR_1_TO_8_RECOVERY_SOURCE_CROSS_ONLY_ZERO_OVERLAPS',
             proposed_groups=bygroup,candidate_union_count=176,prior_source_mentions=len(sources),
             prior_distinct_existing_source_paths=len(existing),prior_existing_source_directory_count=len(directory_index),
             exact_or_resolved_alias_or_directory_overlap_count=len(holds),
             proposed_new_retained_primary_edges=len(new_recovery_edges),
             proposed_new_primary_also_selected_or_restore_cycles_detected=len(new_edge_candidate_primary_intersections),
             prior_original_source_documents_full_SHA_fresh_count=len(original_source_doc_fresh_pins),
             prior_full_read_payloads_identity_only_count=len(original_source_identity_only),
             all_candidate_source_identity_fresh=True,full_candidate_payload_SHA_repeated=False,
             source_binding_pins=list(PINS.values()),files_deleted=0,project_or_ART_writes=False,
             compression_restore_API_ctor_PREP_RUN=False,
             original89_hold_unchanged=True,current89_gzip_execution_not_observed_or_modified=True,
             review_elapsed_s=time.monotonic()-START,
             limits=['This checks only old1–8 explicit restoration sources and new primary-to-candidate recursion. It is not complete independent source/candidate/content preflight review and grants no deletion credit.',
                     'Previously audited current graph/cold/critical exclusions are not rerun here. Root must fresh-pin final union and preserve all reviewed new retained primaries and old restoration sources.',
                     'No full business payload reads, solver/API or native calls. Existing candidate author SHA claims are bound to exact report and fresh inode/size/mtime/ctime; Root still needs final full SHA preflight.',
                     'Old89 tape primary HOLD is unaffected. No gzip artifact qualification, compression progress or eventual success is inferred from this review.'])
assert len(holds)==0
save('exact_176_candidates_prior_restore_source_cross.json',cross)
save('all_9124_existing_old_restoration_sources_fresh_stat_canonical_paths.json',fresh_sources)
save('new_167_retained_primary_edges_no_selected_primary_or_cycle.json',new_recovery_edges)
save('fresh_original_1_to8_source_document_SHA_pins.json',original_source_doc_fresh_pins)
save('prior_payload_source_identity_only_screen.json',original_source_identity_only)
save('prior_restore_overlap_HOLD_candidates.json',holds)
save('PASS_cross_only_candidates.json',safe)
save('independent_prior_restore_cross_report.json',summary)
(OUT/'REPORT.txt').write_text('前1–8轮恢复来源独立交叉：本轮unique9/legacy8/NPZ159共176项，exactpath/解析后alias/来源目录祖先交叉均0；167条新retained_primary边无primary落入候选、无候选间恢复环。\n原89材料tape全部HOLD保持。本报告只验证恢复来源闭包，不替代最终完整SHA预检/业务依赖独审、不批准删除。本次未压缩、恢复、删除或运行业务。\n')
print(json.dumps({k:summary[k] for k in ['status','candidate_union_count','prior_distinct_existing_source_paths','prior_existing_source_directory_count','exact_or_resolved_alias_or_directory_overlap_count','proposed_new_retained_primary_edges','prior_original_source_documents_full_SHA_fresh_count','review_elapsed_s']},ensure_ascii=False),flush=True)
