"""Actual R18 post-retirement metadata/bytes review; stdlib only, no business."""
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import stat
import time

D=Path('/private/tmp/spot_storage_review_eighteenth_graph_20261009')
R=Path('/private/tmp/spot_storage_eighteenth_root_readonly_20261009')
G=Path('/private/tmp/axmat_v9_actual_controls_graph_resource_scope_20261009')
B=Path('/private/tmp/axmat_v9_actual_cold_binding_graph_resource_independent_review_20261009')
P=Path('/private/tmp/spot_storage_eighteenth_native_layered_raw_independent_review_20261009')
ROOT=Path('/Users/wen/spot'); ART=ROOT/'validation/artifacts'; N=ART/'native-layered-full-20261001'
START=time.monotonic(); PINS={}

def identity(path):
    s=Path(path).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def digest(value):
    h=hashlib.sha256()
    for piece in json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).iterencode(value):h.update(piece.encode())
    return h.hexdigest()

def pin(path,wanted=None):
    path=Path(path); before=identity(path)
    assert stat.S_ISREG(before[2]) and path.resolve(strict=True)==path
    if str(path) in PINS:
        old=PINS[str(path)]; assert before==old['identity'] and (wanted is None or old['sha256']==wanted); return old
    h=hashlib.sha256()
    with path.open('rb')as f:
        s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino]==before[:2]
        while block:=f.read(4*2**20):h.update(block)
    assert identity(path)==before
    row=dict(path=str(path),identity=before,bytes=before[3],sha256=h.hexdigest())
    assert wanted is None or row['sha256']==wanted,str(path)
    PINS[str(path)]=row;return row

def read(path,wanted=None):
    row=pin(path,wanted)
    def pairs(items):
        result={}
        for k,v in items:assert k not in result;result[k]=v
        return result
    value=json.loads(Path(path).read_bytes(),object_pairs_hook=pairs)
    assert identity(path)==row['identity'];return value

candidate=read(D/'layered_raw_candidates.json','bd63441de3a04b90f8a5e8fa7369ab88445c669de998172a4bb3ecf91ab364cd')
selected={r['path']:r for r in candidate['candidates']};assert len(selected)==12960
root=read(R/'actual_cleanup_tool_return.json','c0d5c4ca68b48ebf4d909cc2cd80b9f3698d38c5b4217ae9e9b4fcf26e94e92e')
assert root['actual_tool_result']==dict(initial_chunk_id='67e2cd',session_id=90150,terminal_chunk_id='4cb679',exit_code=0)
assert type(root['actual_tool_result']['exit_code'])is int and root['closed']is True and root['record_written_after_actual_terminal']is True
for key in ('executed_source','plan','cleanup_result','stdout','stderr'):pin(root[key]['path'],root[key]['sha256'])
plan=read(root['plan']['path'],root['plan']['sha256']);result=read(root['cleanup_result']['path'],root['cleanup_result']['sha256'])
assert root['plan']['sha256']=='08f761505da86d66c76cf79240dc5ffcfeb98d05627f7062acd9e6d8e9d4eb31'
assert read(root['stdout']['path'],root['stdout']['sha256'])==result and Path(root['stderr']['path']).stat().st_size==0
assert result['files_deleted']==result['selected_count']==14332 and result['categories']=={'compiled':1372,'layered_raw':12960}
rawplan={r['path']:r for r in plan['selected']if r['category']=='layered_raw'}
assert set(rawplan)==set(selected)
for p,r in selected.items():assert rawplan[p]['identity']==r['identity'] and rawplan[p]['sha256']==r['sha256'] and not os.path.lexists(p)
assert all(not os.path.lexists(r['path'])for r in plan['selected'])

g=read(G/'REPORT.json','891ba5161ae1759187bd5f840419e2b1cc8125aba8865ffed4476121e30af0ba')
b=read(B/'REPORT.json','03ebde650f63e045ae7a35f1018e02f787aac47fef28812a9a7a7fd719760e3c')
peer=read(P/'REPORT.json','e6e1c65e9cb33307b911d7f9554aae71a62d12393d49f55faebe2347b8751418')
peerfinal=read(P/'FINAL_REPORT.json','f7729ebf938cdf7d0852a4c757d72d6a98139229e2630b614fd58fe3c47093c5')
assert all(v['status']=='PASS'for v in (g,b,peer,peerfinal))
source=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-admission-scipy-env-physical-basis-own-pid-peak-v9-20261009')
work=Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009')
base=read(D/'REPORT.json')
m=read(source/'rank1_factor_cache_admission.json','564592df0acffc7bbc2c0743cd1b4849db859ec7e83b6101def72ce4a5175742')
expected=dict(m['files']);expected.update(b['additional_expected_files'])
assert len(m['files'])==37339 and len(expected)==37395 and digest(expected)==g['expected_map_sha256']
assert set(selected).isdisjoint(expected)
beforemeta={p:identity(p)for p in m['files']};assert digest(beforemeta)==g['metadata37339_beforeafter_identity_digest']
additional_before={}
for p,sha in b['additional_expected_files'].items():additional_before[p]=pin(p,sha)['identity']
assert len(additional_before)==56 and digest(additional_before)==b['additional_before_after_identity_digest']
gp=g['graph_whole_pin'];graph=read(gp['path'],gp['sha256']);assert identity(gp['path'])==gp['identity']
canonical={r['path']:r['sha256']for r in graph['canonical_files']};assert len(canonical)==35647
beforecanon={p:identity(p)for p in canonical};assert digest(beforecanon)==g['canonical_full_seven_field_beforeafter_digest']
assert all(expected[p]==sha for p,sha in canonical.items())

# Reuse only five independently reviewed stdlib filesystem utility definitions.
# Do not import/execute any producer, graph helper, factory or business module.
utility=G/'review_actual_controls_graph_resources_readonly.py';upin=pin(utility);text=utility.read_text();tree=ast.parse(text)
want=('current_graph_namespace','aliases_and_absences','dynamic_roots','root_validation','resource_inventory')
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in want]
assert {n.name for n in nodes}==set(want)
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(utility),'exec'),globals())
ns=[current_graph_namespace(r,canonical)for r in graph['namespaces']];aa=aliases_and_absences(graph,canonical)
assert len(ns)==86 and ns==g['namespaces86_beforeafter'] and aa==g['aliases186_absences445_beforeafter']

# All remaining native family entries inherit peer's recent whole fullSHA through
# exactly unchanged seven-field identities; new whole numerical payload read=0.
seal=pin(N/'result.sha256','6ab0927cb9570715607c260873e907d6b6a429327773909ceb4b2e4f0af3ac2d');old={}
for line in (N/'result.sha256').read_text().splitlines():
    sha,rel=line.split('  ',1);assert rel not in old;old[rel]=sha
retained=[]
for rel,sha in old.items():
    p=N/rel
    if str(p)in selected:continue
    ids=identity(p);assert stat.S_ISREG(ids[2])and p.resolve(strict=True)==p
    retained.append(dict(path=str(p),sha256=sha,bytes=ids[3],identity=ids))
retained_digest=hashlib.sha256(json.dumps(retained,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
assert len(retained)==12753 and retained_digest==peer['retained_seal_evidence_digest']
actual_family={str(p.relative_to(N))for p in N.rglob('*')if p.is_file()and not p.is_symlink()}
assert actual_family=={rel for rel in old if str(N/rel)not in selected}|{'result.sha256'}
preflight=[]
for p in peer['retained_preflight_raw_paths']:
    assert p not in selected
    preflight.append(pin(p,old[str(Path(p).relative_to(N))]))
assert len(preflight)==12

# Freeze every current SOURCE/WORK/TERM/CT leaf against independent precleanup
# SHA witnesses, then freshly hash the small four-root complete byte inventory.
beforepins={}
for proof in (g,b):beforepins.update(proof['full_read_pins'])
beforepins.update(base['evidence_small_pins'])
for row in base['current_held_duplicate_working_pairs']:beforepins[row['path']]=dict(identity=row['identity'],sha256=row['whole_SHA256_inherited_with_unchanged_seven_identity'])
prepared=read(work/'prepared.json','35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7')
cold=read(work/'prepared_cold.json','1290a19501ba7801deafe351407b244bd32f71a6cf0d010d4a14fd64e61d8b3e')
binding=read(work/'own_rss_binding.json','4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930')
term=Path(base['current_source31_work56_TERM12_CT3'][2]['path'])
final_receipt=read(term/'finalization_terminal_return.json','ea33c7159edf82ce4ac1ba3682cc013c013431961a7ef7ad2e6f4dc0efd5bdb4')
stream_expected={final_receipt[k]['path']:final_receipt[k]['sha256']for k in ('full_stdout','full_stderr')}
fullroots=[]
for r in base['current_source31_work56_TERM12_CT3']:
    path=Path(r['path']);files=sorted(p for p in path.rglob('*')if p.is_file()and not p.is_symlink());assert len(files)==r['files']
    for p in files:
        key=str(p)
        if key in expected:sha=expected[key]
        elif key in beforepins:sha=beforepins[key]['sha256']
        elif key in stream_expected:sha=stream_expected[key]
        else:raise AssertionError(('missing independent precleanup SHA witness',key))
        observed=pin(p,sha)
        if key in beforepins:assert observed['identity']==beforepins[key]['identity'],key
    fullroots.append(dict(path=str(path),files=len(files),whole_fresh_SHA=True))
roots=dynamic_roots(prepared['resource_roots'],ART)
assert len(roots)==236 and roots==prepared['resource_roots']==binding['resource_info']['resource_roots']
resources_before=resource_inventory(roots,ART)
free_before=shutil.disk_usage(ART).free
assert resources_before['artifact_bytes']<96*2**30 and free_before>8*2**30
reserve=g['original_future_AAA_reserve_bytes']
assert resources_before['artifact_bytes']+reserve<96*2**30 and free_before-reserve>8*2**30
assert all(not os.path.lexists(work/name)for name in ('AAA','ABA','training','archives','cold_failure.json','cold_complete.json','cold_seal.json'))

assert beforemeta=={p:identity(p)for p in m['files']}
assert additional_before=={p:identity(p)for p in b['additional_expected_files']}
assert beforecanon=={p:identity(p)for p in canonical}
assert ns==[current_graph_namespace(r,canonical)for r in graph['namespaces']]
assert aa==aliases_and_absences(graph,canonical)
assert all(identity(row['path'])==row['identity']for row in retained)
resources_after=resource_inventory(roots,ART);assert resources_after==resources_before
assert all(not os.path.lexists(r['path'])for r in plan['selected'])
for p,row in PINS.items():assert identity(p)==row['identity']

report=dict(schema='SPOT_R18_ACTUAL_LAYERED_RAW_RETIREMENT_CURRENT_GRAPH_AND_RETAINED_RESULTS_POSTCHECK_V1',status='PASS',
    Root_actual_tool=root['actual_tool_result'],Root_closed=True,Root_cleanup_result=PINS[root['cleanup_result']['path']],
    fixed_plan_sha256=root['plan']['sha256'],Root_exact14332_absent=True,selected_layered12960_absent=True,
    selected_layered_original_fullSHA_before_retirement_inherited=True,old12960_deleted_payload_bytes_read_after_retirement=0,
    canonical35647_seven_identity_digest=digest(beforecanon),inherited_canonical35803098221_fullSHA=True,new_35GB_content_reads=0,
    current_metadata37339_seven_identity_digest=digest(beforemeta),current_expected37395_complete_sha256=digest(expected),
    extra56_fresh_fullSHA_and_seven_identity_digest=digest(additional_before),requirement235528_wire_source_pin_unchanged=True,
    exhaustive_namespaces86=ns,aliases186_absences445=aa,current_SOURCE31_WORK56_TERM12_CT3_fullSHA=fullroots,
    native_retained12753_identity_and_prior_fullSHA_digest=retained_digest,inherited_native_retained_fullSHA_bytes=819870861,
    new_whole_native_results_payload_rehashed=False,preflight12_fresh_fullSHA=preflight,old_native_family_expected_remainder_exact=True,
    original_numeric_operators_controls_results_source_inputs_logs_seal_kept=True,
    current_dynamic236_resource_roots=roots,current_resource_before_after=resources_after,disk_free_before=free_before,
    history_cap96GiB_and_free8GiB_retained=True,original_AAA_reserve_bytes=reserve,strong_future_reservation_passed=True,
    old_resource_observation_not_a_frozen_future_count_gate=True,native_future_outputs_absent=True,
    old_native_per_raw_reverification_requires_isolated_recomputation=True,
    reconstruction_source_recipe_inherited=D.as_posix()+'/LAYERED_RAW_REVIEW.json',
    business_imported_or_executed=False,files_deleted_by_this_reader=0,project_written=False,
    new_scientific_credit=False,native_RSS_credit=False,AAA_accuracy_credit=False,ABA_credit=False,
    small_fullSHA_pins=PINS,elapsed_seconds=time.monotonic()-START)
out=D/'ACTUAL_POST_RETIREMENT_REPORT.json'
with out.open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
txt=D/'ACTUAL_POST_RETIREMENT_REPORT.txt'
with txt.open('x')as f:f.write('R18 清理实际终态独立核验：PASS。\n12960 个历史 full_jobs raw 中间文件缺席；Root 固定14332项全缺席。\n当前35647 canonical、37339 原metadata及37395完整owner集合身份保持，86 namespace、186 aliases、445 absence保持。\n最终 operators、controls、结果/日志/原seal保留：12753项继承刚完整819870861B全文SHA，现全7字段身份一致；12份预检raw重新全文SHA通过。\nSOURCE31、WORK56、TERM12、CT3逐完整文件鲜SHA通过；236动态resource roots及原96GiB/free8GiB/未来reserve保持。\n旧逐raw全验和replay必须按保留源码输入在隔离位置重算，不能直接运行原primary覆盖最终输出。\n本核验未执行科学业务、未重读35GB、未改项目或删文件；不授予native/AAA/ABA信用。\n')
print(json.dumps(dict(status='PASS',report=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),selected_raw_absent=12960,Root_total_absent=14332,new_35GB_read=0,elapsed_seconds=report['elapsed_seconds'])))
