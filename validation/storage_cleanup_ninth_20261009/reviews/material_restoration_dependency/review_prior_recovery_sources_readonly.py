"""Explicit eight-round restoration-source audit. Stdlib, read-only project.

Writes only a new TMP followup. No restore, compression, deletion or business API.
Previous 89-item report remains byte-exact prior-not-approved evidence.
"""
import ast
import collections
import hashlib
import json
import os
from pathlib import Path
import stat
import time

ROOT = Path('/Users/wen/spot')
V = ROOT / 'validation'
PRIOR = Path('/private/tmp/spot_ninth_material_intermediate_readonly_review_20261009')
OUT = PRIOR / 'prior_cleanup_restoration_dependency_review'
PINS = {}
START = time.monotonic()

def identity(p):
    s = p.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def pin(p, expected=None):
    p = Path(p)
    old = identity(p)
    assert stat.S_ISREG(old[2]), ('not regular', str(p))
    if str(p) not in PINS:
        h = hashlib.sha256()
        with p.open('rb') as f:
            s = os.fstat(f.fileno())
            assert [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink] == old
            for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
        assert identity(p) == old
        PINS[str(p)] = dict(path=str(p), identity=old, bytes=old[3], sha256=h.hexdigest(), stable_full_read=True)
    d = PINS[str(p)]
    assert d['identity'] == old
    if expected is not None: assert d['sha256'] == expected, ('SHA differs', str(p))
    return d

def load(p, expected=None):
    d = pin(p, expected)
    b = Path(p).read_bytes()
    assert hashlib.sha256(b).hexdigest() == d['sha256'] and identity(Path(p)) == d['identity']
    return json.loads(b)

def save(n,d):
    p = OUT/n
    assert not p.exists(), str(p)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

candidates = load(PRIOR/'exact_material_intermediate_retirement_candidates.json',
                  '29f7b50a905aef95dfd035a9c3bc5802606fafe7d5a5b76c3c83bf2589115fc7')
priorreport = pin(PRIOR/'independent_recommendation.json',
                  'e3d960219b3f9cb0ffd6aab20f71f45dcbbc2f9212f41f1b414eae2a3fbfd890')
pin(PRIOR/'REPORT.txt','dca4d6d82f8ee883ffce2cb330f3c29d167c050eee09203dda11e7e89b24abb5')
cs = {r['path']:r for r in candidates}
sources = []
documents = []
rounds = (
 (1,'storage_cleanup_20261008', ['storage_review_20261008/first_batch_24_files.json','storage_review_20261008/second_batch_replay_arrays.json']),
 (2,'storage_cleanup_more_20261008',['storage_review_more_20261008/exact_retirement_manifest.json']),
 (3,'storage_cleanup_third_20261008',[]),
 (4,'storage_cleanup_fourth_20261008',[]),
 (5,'storage_cleanup_fifth_20261009',[]),
 (6,'storage_cleanup_sixth_20261009',[]),
 (7,'storage_cleanup_seventh_20261009',['storage_cleanup_seventh_20261009/tar/candidate.json']),
 (8,'storage_cleanup_eighth_20261009',[]))

def add(raw, rnd, doc, selector, owner=None, kind='explicit_retained_primary'):
    if raw is None:return
    rows = raw if isinstance(raw,list) else [raw]
    for r in rows:
        if isinstance(r,str):path=r;sha=None;size=None
        elif isinstance(r,dict):
            path=r.get('path');sha=r.get('sha256',r.get('expected_sha256',r.get('historical_sha256')))
            size=r.get('size',r.get('bytes',r.get('expected_bytes')))
        else: continue
        if not isinstance(path,str) or not path.startswith('/'): continue
        p=Path(path)
        existence=os.path.lexists(p)
        sources.append(dict(round=rnd,source_document=str(doc),selector=selector,source_path=path,
                            expected_sha256=sha,expected_size=size,retired_target=owner,role=kind,
                            current_exists=existence,current_identity=identity(p) if existence else None,
                            overlaps_prior89=path in cs))

for rnd,name,extras in rounds:
    directory=V/name
    docs=[directory/x for x in ['manifest.json','preflight.json','cleanup_result.json','cleanup_terminal_observation.json'] if (directory/x).is_file()]
    docs += [V/x for x in extras]
    for p in docs:
        d=load(p);documents.append(dict(round=rnd,**pin(p),schema=d.get('schema') if isinstance(d,dict) else None))
        if not isinstance(d,dict):continue
        rows=d.get('candidates',d.get('files',d.get('verified_candidates',[])))
        if isinstance(rows,list):
            for i,r in enumerate(rows):
                if not isinstance(r,dict):continue
                owner=r.get('path',r.get('candidate',{}).get('path'))
                for k in ['primary','retained_primary','duplicate_primary','retain_primary','retained_payload']:
                    if k in r:add(r[k],rnd,p,f'rows[{i}].{k}',owner)
                for k in ['retained_anchors']:
                    if k in r:add(r[k],rnd,p,f'rows[{i}].{k}',owner,'retained_anchor')
        for k in ['retained_primaries','retained_primaries_and_critical_sources','fresh_retained_primary_files','retained_stage_outputs','retained_fresh_contents','retained_closed_anchors']:
            if k in d:
                raw=d[k]
                if isinstance(raw,dict):raw=list(raw.values())
                add(raw,rnd,p,k,kind='declared_retained_payload_or_anchor')
        if 'members' in d:
            for i,m in enumerate(d['members']):
                add(m['retained_payload'],rnd,p,f'members[{i}].retained_payload',d['candidate']['path'],'exact_tar39_payload_source')
            assert len(d['members'])==39
    ledger=directory/'retirement_ledger.jsonl'
    if ledger.is_file():
        pin(ledger)
        for i,line in enumerate(ledger.read_text().splitlines()):
            r=json.loads(line)
            owner=r.get('path',r.get('candidate',{}).get('path'))
            for k in ['primary','retained_primary','duplicate_primary','retain_primary','retained_payload']:
                if k in r:add(r[k],rnd,ledger,f'ledger[{i}].{k}',owner,'actual_retirement_ledger_retained_primary')

second_manifest_path=V/'storage_review_more_20261008/exact_retirement_manifest.json'
second_preflight_path=V/'storage_cleanup_more_20261008/preflight.json'
second_result_path=V/'storage_cleanup_more_20261008/cleanup_result.json'
second_terminal_path=V/'storage_cleanup_more_20261008/cleanup_terminal_observation.json'
second_manifest=load(second_manifest_path)
second_preflight=load(second_preflight_path)
second_result=load(second_result_path)
second_terminal=load(second_terminal_path)
second_ledger_path=V/'storage_cleanup_more_20261008/retirement_ledger.jsonl'
second_ledger=[json.loads(line) for line in second_ledger_path.read_text().splitlines()]
assert second_result['status']=='PASS' and second_terminal['exit_code']==0
assert second_result['manifest_sha256']==pin(second_manifest_path)['sha256']
assert second_result['preflight_sha256']==pin(second_preflight_path)['sha256']
assert second_terminal['manifest_sha256']==pin(second_manifest_path)['sha256']
assert second_terminal['preflight_sha256']==pin(second_preflight_path)['sha256']
assert len(second_manifest['files'])==len(second_preflight['candidates'])==len(second_ledger)==460
primary_edges=[]
for i,(m,p,l) in enumerate(zip(second_manifest['files'],second_preflight['candidates'],second_ledger)):
    assert m['path']==p['candidate']['path']==l['candidate']['path'] and l['sequence']==i+1
    assert p['candidate']==l['candidate']
    assert m.get('duplicate_primary')==p.get('duplicate_primary')==l.get('duplicate_primary')
    primary=m.get('duplicate_primary')
    if not primary or primary['path'] not in cs:continue
    cand=cs[primary['path']]
    assert primary['expected_sha256']==m['expected_sha256']==p['candidate']['sha256']==cand['sha256']
    assert primary['identity'][3]==p['candidate']['bytes']==cand['bytes']
    primary_edges.append(dict(primary_path=primary['path'],retired_target=m['path'],original_sequence=i+1,
                              expected_sha256=cand['sha256'],bytes=cand['bytes'],
                              original_manifest_sha256=pin(second_manifest_path)['sha256'],
                              original_preflight_sha256=pin(second_preflight_path)['sha256'],
                              actual_ledger_sha256=pin(second_ledger_path)['sha256'],
                              actual_cleanup_result_sha256=pin(second_result_path)['sha256'],
                              actual_terminal_sha256=pin(second_terminal_path)['sha256'],
                              actual_retired_target_now_absent=not os.path.lexists(m['path']),
                              actual_second_cleanup_exit_code=0))
assert len(primary_edges)==120 and {r['primary_path'] for r in primary_edges}==set(cs)

script_evidence=[]
for rnd,name,_ in rounds:
    directory=V/name
    for p in sorted(directory.glob('*.py')):
        d=pin(p)
        text=p.read_text();tree=ast.parse(text)
        row=dict(d,round=rnd,AST_parse_only_not_imported=True,
                 exact_source_text=text,
                 absolute_string_literals=[n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value.startswith('/')])
        script_evidence.append(row)
        for i,path in enumerate(row['absolute_string_literals']):
            if Path(path).is_file():add(path,rnd,p,f'AST_absolute_literal[{i}]',kind='source_literal_conservative_existing_file')

holds=[]
for path,r in sorted(cs.items()):
    fresh=pin(path,r['sha256'])
    assert fresh['identity']==r['identity']
    edges=[e for e in primary_edges if e['primary_path']==path]
    holds.append(dict(path=path,identity=fresh['identity'],size=fresh['bytes'],allocated_bytes=r['allocated_bytes'],sha256=fresh['sha256'],
                      status='HOLD_PRIOR_ACTUAL_RESTORATION_PRIMARY_MUST_REMAIN_AVAILABLE',
                      actual_retirement_edges=edges,
                      all_prior_source_mentions=[s for s in sources if s['source_path']==path],
                      current_dynamic_raw_read_intersection=any(r['protection_screen'].values()),
                      direct_deletion_approved=False))

tar=load(V/'storage_cleanup_seventh_20261009/tar/candidate.json')
tar_paths={m['retained_payload']['path'] for m in tar['members']}
assert not tar_paths.intersection(cs)
save('all_eight_rounds_explicit_restoration_source_paths_and_fresh_stat.json',sources)
save('all_eight_rounds_manifest_preflight_ledger_and_source_fresh_pins.json',list(PINS.values()))
save('all_eight_rounds_source_AST_and_full_restore_source_text.json',script_evidence)
save('prior_actual_second_round_120_retirement_primary_edges.json',primary_edges)
save('held_89_prior_actual_restoration_primaries.json',holds)
save('final_safe_direct_delete_candidates.json',[])

gzip_assessment=dict(
    status='SOURCE_ONLY_CONDITIONAL_ARCHIVE_DESIGN_NO_COMPRESSION_OR_RESTORE',
    current_dynamic_raw_path_blockers_observed=0,
    evidence_scope='Frozen V8 graph canonical/ns/alias, old normalized index, 88 critical roots, eighth6194/6248, source-derived actual1534 original cold business reads, accepted28 nuclear-source plan and library/material saved input tables. Current dynamic graph still must be fresh checked by Root before any action; unknown future CE implementation is not claimed covered.',
    candidate_raw_paths_have_no_observed_current_dynamic_business_read=True,
    old_restore_helpers={
      'round7_restore_retired_work_copies.py':'Existing primary ordinary regular file plus size and SHA required; no saved inode equality. Paths revalidated canonical before reads/writes. Target absent or exact same size/SHA; when restoring target mode/mtime from old target identity. This permits a raw primary recreated byte-exact from gzip with a new inode.',
      'round8_restore_retired_work_copies.py':'Same current ordinary-primary size/SHA/path contract, no old source inode match. SHA restored raw primary remains required before subsequent old copy restoration.',
      'round7_restore_retired_tar.py':'Every retained_payload ordinary project artifact path plus size/SHA, not historical source inode. 39 payload paths have zero intersection with 89 tapes; archive metadata patch also retained.',
      'round1_to6':'No standalone executable restore helper found in these round directories. Earlier manifests/preflights/ledgers explicitly bind expected payload SHA, bytes and historical identity. Historical cleanup/preflight functions require original identity for deletion/preservation verification; do not reinterpret rerunning them as restoration or claim their historical inode baseline can be regenerated. New recovery must verify old payload SHA/bytes at original raw paths before ordinary old immutable content-verifier/replay use.'},
    necessary_conditions=[
      'Before removing each raw primary, create project-retained lossless gzip payload from stable complete raw reads. Record original absolute path, SHA256, exact byte count, mode, mtime and archive path/SHA/identity; preserve all old1–8 documents, ledgers and mappings unchanged.',
      'Independently stream-decompress every completed compressed file to a sink and verify exact original byte count and SHA while checking compressed identity stability, gzip corruption/truncation and archive metadata. No credit or deletion on incomplete/failed verification.',
      'Root and independent reviewer must bind exact archive inventory/source pins/current scope and refresh candidate/preflight identity. Archive files become hard-protected recovery sources for future cleanup.',
      'New recovery first reconstructs absent original tape30 primary paths with no overwrite/alias escape, verifies original SHA/byte count and retained mode/mtime, then old1–8 mappings may restore their retired duplicates from those raw paths. Default new tool must not perform restoration.',
      'Old7/8 restore utilities do not read gzip directly and fail while a required raw primary is absent. Never label their default/raw restore checks PASS until the primary has actually been restored.',
      'Compression ratio, storage recovery and exact recovery execution have not been measured by this read-only source assessment; Root must obtain concrete independently verified archive before deleting any raw primary.' ],
    actual_archive=None,actual_compression=None,actual_restore=None,actual_deletion=None,
    claim_that_new_inode_matches_old_history=False)
save('lossless_gzip_archive_conditional_source_assessment.json',gzip_assessment)
summary=dict(
    status='HOLD_ALL_89_FINAL_SAFE_DIRECT_DELETE_SUBSET_EMPTY',
    prior_report_pin=priorreport,prior_report_kept_byteexact=True,
    prior_report_approval_status='PRIOR_NOT_APPROVED_DIRECT_DELETE_RECOMMENDATION_SUPERSEDED_BY_RECOVERY_PRIMARY_HOLD',
    candidate_original_count=89,held_count=89,final_safe_direct_delete_count=0,
    final_safe_logical_bytes=0,final_safe_allocated_bytes=0,
    held_logical_bytes=sum(r['size'] for r in holds),held_allocated_bytes=sum(r['allocated_bytes'] for r in holds),
    held_allocated_GiB=sum(r['allocated_bytes'] for r in holds)/1024**3,
    eight_rounds_scanned=list(range(1,9)),
    explicit_restoration_source_mentions=len(sources),distinct_existing_restoration_source_paths=len({r['source_path'] for r in sources if r['current_exists']}),
    original_actual_second_round_edges=120,all_89_have_actual_prior_retained_primary_binding=True,
    original_second_round_manifest=pin(second_manifest_path),original_second_round_preflight=pin(second_preflight_path),
    original_second_round_ledger=pin(second_ledger_path),original_second_round_cleanup_result=pin(second_result_path),
    original_second_round_terminal=pin(second_terminal_path),
    tar39_payload_sources=len(tar_paths),tar39_intersection=0,
    fresh_full_read_pin_count=len(PINS),fresh_full_read_bytes=sum(x['bytes'] for x in PINS.values()),
    review_elapsed_s=time.monotonic()-START,files_deleted=0,project_or_ART_writes=False,
    business_import_API_PREP_RUN_ctor=False,compression_or_restore=False,
    final_action='Keep all89 raw tapes unless separately authorized and independently verified byte-exact archival-and-restore migration is completed; never apply old direct-delete shortlist.',
    limitations=['Initial89 review omitted all prior restoration-source closure; parent requested additional necessary crosscheck before manifest/preflight/deletion. The omission is explicit and the original report is preserved, not rewritten as fully approved.',
                 'All89 are still-present certified retained primaries for120 actually retired second-round duplicate files. Deleting them without equivalent lossless recovery would break existing exact-byte restoration promises.',
                 'Conditional gzip source assessment is not an archive, restore test, cleanup execution or measured recovered capacity. Raw-primary restoration must precede old tools. Historical inode equality is not promised.'])
save('final_recovery_dependency_hold_and_safe_subset_report.json',summary)
(OUT/'REPORT.txt').write_text(
    '最终直接删除建议：0项，0B。原89项、7.874202728GiB清单仅为prior-notapproved，不可执行。\n'
    '89项全部是第二轮已实际删除120个重复NJOY工作输入的retained duplicate_primary；原manifest、preflight、实际ledger、EXIT0结果完全对应。\n'
    '逐项完整primary路径、SHA、identity、旧被删owner及所有1–8恢复来源交叉见held_89_prior_actual_restoration_primaries.json。原89报告保持字节不变。\n'
    '当前业务读scope仍为零交集，可评估lossless gzip迁移；此处没有压缩或删除。必须先归档全部原bytes并独立流式解压核验原SHA/size；归档成为硬保护；新工具先恢复原raw primary，再由旧恢复映射恢复旧副本。\n'
    '旧7/8 standalone恢复工具对primary检查普通路径、size/SHA，不要求旧inode；旧1–6清理预检里的identity严格比较是历史删除/保留基线，不可声称重建inode后能重新通过旧preflight。原文档/ledger不改。\n')
print(json.dumps({k:summary[k] for k in ['status','held_count','final_safe_direct_delete_count','held_allocated_GiB','original_actual_second_round_edges','explicit_restoration_source_mentions','distinct_existing_restoration_source_paths','fresh_full_read_pin_count','fresh_full_read_bytes','review_elapsed_s']},ensure_ascii=False),flush=True)
