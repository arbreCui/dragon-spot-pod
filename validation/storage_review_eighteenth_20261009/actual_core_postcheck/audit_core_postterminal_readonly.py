from pathlib import Path
import os, stat, hashlib, json

R=Path('/Users/wen/spot')
PRE=Path('/private/tmp/spot_storage_review_eighteenth_build_cache_20261009')
ROOT=Path('/private/tmp/spot_storage_eighteenth_root_readonly_20261009')
OUT=Path('/private/tmp/spot_storage_review_eighteenth_core_postterminal_20261009')
KEYS=('dev','ino','mode','size','mtime_ns','ctime_ns','nlink')
read_pins=[]
def identity(p):
    s=Path(p).lstat();return [getattr(s,'st_'+k) for k in KEYS]
def pin(p,sha=None):
    p=Path(p);before=identity(p);assert stat.S_ISREG(before[2]) and not p.is_symlink()
    b=p.read_bytes();assert before==identity(p);h=hashlib.sha256(b).hexdigest()
    if sha is not None:assert h==sha,(str(p),h,sha)
    q={'path':str(p),'bytes':len(b),'sha256':h,'identity':before};read_pins.append(q);return b,q
def read(p,sha=None):return json.loads(pin(p,sha)[0])
def meta(p):
    p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)
    return {'path':str(p),'logical_bytes':s.st_size,'allocated_bytes':s.st_blocks*512,'identity':[getattr(s,'st_'+k) for k in KEYS]}
def stream(rows):
    h=hashlib.sha256()
    for q in sorted(rows,key=lambda q:q['path']):h.update(json.dumps([q['path'],q['identity']],ensure_ascii=False,separators=(',',':')).encode()+b'\n')
    return h.hexdigest()
def write(name,data):
    p=OUT/name
    with p.open('x') as f:json.dump(data,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

obs=read(ROOT/'actual_cleanup_tool_return.json','c0d5c4ca68b48ebf4d909cc2cd80b9f3698d38c5b4217ae9e9b4fcf26e94e92e')
actual=obs['actual_tool_result']
assert actual=={'initial_chunk_id':'67e2cd','session_id':90150,'terminal_chunk_id':'4cb679','exit_code':0}
assert type(actual['exit_code']) is int and obs['closed'] is True and obs['record_written_after_actual_terminal'] is True
plan=read(ROOT/'approved_fixed_plan.json','08f761505da86d66c76cf79240dc5ffcfeb98d05627f7062acd9e6d8e9d4eb31')
result=read(obs['cleanup_result']['path'],obs['cleanup_result']['sha256'])
stdout=read(obs['stdout']['path'],obs['stdout']['sha256'])
assert stdout==result
assert pin(obs['stderr']['path'],obs['stderr']['sha256'])[0]==b''
assert result['plan_sha256']==obs['plan']['sha256'] and result['files_deleted']==plan['selected_count']
assert result['no_directories_removed'] is True and result['no_other_project_file_written'] is True
assert result['scientific_business_executed'] is False
prior=read(PRE/'REPORT.json','501c2257acb1f25b6278028dec7432d3c7644a8ccc6d0918c66c9fe6f212206f')
candidates=read(PRE/'compiled_candidate_screen.json','4023b780e79414db91a238e3c169f0e78d6b9c211dd03f74049246221ea04ae5')
selected={q['path']:q for q in plan['selected'] if q['category']=='compiled'}
assert set(selected)=={q['path'] for q in candidates['candidates']}
assert all(selected[q['path']]['identity']==q['identity'] for q in candidates['candidates'])
assert all(not os.path.lexists(p) for p in selected)

# Reconstruct the prior finite core identity stream using only declared absent candidates.
# This verifies all surviving core files (including modules, bin, source and libraries),
# without copying an old large metadata baseline or traversing artifacts/Git.
core=[];links=[]
for stem in ('src','Trivac','Ganlib','Utilib','lib','bin','data','SPOT_doc','script','.ruff_cache'):
    top=R/stem
    if not top.exists():continue
    for folder,ds,ns in os.walk(top,followlinks=False):
        for name in ds+ns:
            p=Path(folder)/name;s=p.lstat()
            if stat.S_ISREG(s.st_mode):core.append(meta(p))
            elif stat.S_ISLNK(s.st_mode):links.append({'path':str(p),'target':os.readlink(p),'identity':identity(p)})
for p in R.iterdir():
    if p.is_file() and not p.is_symlink():core.append(meta(p))
assert not set(q['path'] for q in core)&set(selected)
reconstructed=core+[{'path':q['path'],'identity':q['identity']} for q in candidates['candidates']]
assert stream(reconstructed)==prior['core_identity_stream_sha256']
assert len(reconstructed)==prior['core_current_summary']['regular_paths']
assert links==prior['core_symlink_metadata']
hold=candidates['frozen_object_HOLD']+candidates['current_source_reference_context_HOLD']
assert all(meta(q['path'])['identity']==q['identity'] for q in hold)
hold_paths={q['path'] for q in hold}
assert {q['path'] for q in core if Path(q['path']).suffix=='.o'}==hold_paths
assert {q['path'] for q in core if Path(q['path']).suffix=='.a'}=={q['retained_master']['path'] for q in candidates['candidates'] if q['path'].endswith('.a')}

# All retained source/Makefile/master bytes in Root's exact plan are genuinely fresh.
# Pre-review seven-field pins independently match every source identity as well.
pre_pins={q['path']:q for q in prior['full_input_pins']}
source_stream=hashlib.sha256();source_identity_stream=hashlib.sha256()
source_count=0
for path,sha in sorted(plan['source_pins'].items()):
    b,q=pin(path,sha);assert q['identity']==pre_pins[path]['identity']
    source_stream.update(json.dumps([path,sha],separators=(',',':')).encode()+b'\n')
    source_identity_stream.update(json.dumps([path,q['identity']],separators=(',',':')).encode()+b'\n')
    source_count+=1

W=R/'validation/artifacts/axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
binding=read(W/'own_rss_binding.json','4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930')
gp=R/'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/input_graph.json'
graph=read(gp,'0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3')
assert not set(selected)&set(binding['files'])
assert not set(selected)&{q['path'] for q in graph['canonical_files']}
expected_current=[]
for path in binding['files']:
    q=meta(path);expected_current.append(q)
canonical_current=[]
for q in graph['canonical_files']:
    m=meta(q['path']);assert m['logical_bytes']==q['size_bytes'];canonical_current.append(m)
prepared=pin(W/'prepared.json','35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7')[1]
prepared_cold=pin(W/'prepared_cold.json','1290a19501ba7801deafe351407b244bd32f71a6cf0d010d4a14fd64e61d8b3e')[1]
for q in prior['full_input_pins']:
    p=Path(q['path'])
    if str(p) in selected or str(p) in plan['source_pins']:continue
    if p.is_relative_to(R):
        pin(p,q['sha256']);assert identity(p)==q['identity']

# Whole-project protected before/after was separately run by Root; bind its real
# completed observation, compare its fields, and independently verify its small docs.
before=read(ROOT/'protected_before.json');after=read(ROOT/'protected_after.json')
for key in ('counts','metadata_identity_sha256','logical_regular_bytes','unique_inode_allocated_bytes','document_sha256','cache_like','fixed_plan_sha256'):
    assert before[key]==after[key],key
assert after['preservation_status']=='PASS_ALL_NONSELECTED_IDENTITIES_AND_ORIGINAL_DIR_PATHS_LINKS_DOCUMENT_SHA_UNCHANGED'
assert after['approved_exact_selected_absent_count']==plan['selected_count']
docs=[]
for path,sha in after['document_sha256'].items():docs.append(pin(R/path,sha)[1])
assert all(identity(q['path'])==q['identity'] for q in core+expected_current+canonical_current)
out={'schema':'SPOT_R18_ACTUAL_CORE_RETIREMENT_INDEPENDENT_POSTCHECK_V1','status':'PASS_EXACT_CORE_RETIREMENT_AND_RETAINED_CURRENT_INPUT_METADATA','Root_cleanup_actual_tool':actual,'Root_cleanup_closed':True,'Root_whole_protected_after_actual_tool_reported_by_parent':{'initial_chunk_id':'b37a8f','session_id':29496,'terminal_chunk_id':'fd3e7d','exit_code':0,'closed':True},'retired_core_count':len(selected),'retired_core_absent':True,'Root_total_retirement_count':plan['selected_count'],'raw_retirement_byte_review_delegated_to_other_peers':True,'core_surviving_regular_count':len(core),'core_reconstructed_original_seven_identity_stream_sha256':stream(reconstructed),'core_reconstructed_R18_before_exact':True,'remaining_o_exact15_paths':sorted(hold_paths),'all_mod_bin_four_Darwin_libraries_and_source_regular_metadata_R18_exact':True,'full_SHA_retained_source_Makefile_master_count':source_count,'retained_full_SHA_stream_sha256':source_stream.hexdigest(),'retained_source_seven_identity_stream_sha256':source_identity_stream.hexdigest(),'expected_owner_paths_present':len(expected_current),'canonical_paths_present_and_sizes_exact':len(canonical_current),'expected_current_metadata_stable_during_read':True,'expected_metadata_precleanup_for_project_paths_preserved_by_Root_whole_project_witness_not_new_science_content_hash':True,'prepared':prepared,'prepared_cold':prepared_cold,'Root_whole_project_protected_before_after_fields_exact':True,'Root_protected_counts':after['counts'],'Root_protected_identity_fingerprints':after['metadata_identity_sha256'],'original_documents_SHA_checked':docs,'source_plan_descriptors':[q for q in read_pins if q['path'] in {str(ROOT/'actual_cleanup_tool_return.json'),str(ROOT/'approved_fixed_plan.json'),str(PRE/'REPORT.json'),str(PRE/'compiled_candidate_screen.json'),str(ROOT/'protected_before.json'),str(ROOT/'protected_after.json'),str(W/'own_rss_binding.json'),str(gp)}],'files_deleted_by_reader':0,'project_written':False,'git_written':False,'business_import_API_constructor_solver_native_build_executed':False,'scientific_credit':False,'large_scientific_content_or_Git_history_not_read':True,'no_APFS_exclusive_free_space_claim':True}
report=write('REPORT.json',out)
with (OUT/'REPORT.txt').open('x') as f:
    f.write('第十八轮真实core清理独立后验：PASS。1372指定core路径全部缺席；15保留.o全身份保持，全部138模块/bin/4 Darwin主库/源码路径通过重构原有限core七身份指纹验证。\n')
    f.write(f'保留source/Makefile/master共{source_count}路径全文SHA与原身份fresh一致；current binding {len(expected_current)} expected路径和graph {len(canonical_current)} canonical路径仍在，canonical大小保持。binding4e/graph0e365/原prepared35f/preparedcold1290及小原证据SHA保持。\n')
    f.write('Root真实cleanup67e2cd/session90150→4cb679 EXIT0 CLOSED，固定计划08f761；另外12960 raw由互补代理审核，本reader未读取其大原始内容。Root保护余集before/after160363regular/687links/7058dirs指纹和10文档SHA相同，本readerfresh验证小文档并绑定Root真实fd3e7d EXIT0观察，不冒称本reader全项目重扫。\n')
    f.write('仅TMP写报告，删除0，项目/Git写入False，无编译/native/科学业务/35GB内容读。目录因批准unlink可有时间变化；只验证原目录paths和剩余文件身份，不虚构父目录时间不变。\n')
print(json.dumps({'status':out['status'],'report':report,'retired_core_absent':len(selected),'remaining_o':len(hold_paths),'retained_full_SHA_paths':source_count,'expected_owner_paths':len(expected_current),'canonical_paths':len(canonical_current),'project_written':False,'files_deleted_by_reader':0},ensure_ascii=False))
