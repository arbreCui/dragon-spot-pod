"""Read-only full EOF postseal validation; no candidate or payload replay."""
import hashlib,json,os,stat
from pathlib import Path
P=Path(__file__).parent
def ids(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ids(p);assert stat.S_ISREG(i[2]) and i[3]==1 and not p.is_symlink()
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ids(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
m=json.loads((P/'MANIFEST.json').read_bytes());r=json.loads((P/'REVIEW.json').read_bytes())
assert set(str(p.relative_to(P)) for p in P.rglob('*') if p.is_file())==set(m['members'])|{'MANIFEST.json'}
for rel,value in m['members'].items():assert value['path']==str(P/rel) and pin(P/rel)==value
assert {'.':ids(P),**{str(p.relative_to(P)):ids(p) for p in P.rglob('*') if p.is_dir()}}==m['directories']
assert pin(P/'REVIEW.json')==m['review'] and r['schema']=='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1' and r['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY'
assert r['source_only'] is True and r['all_checks_typed_true'] is True and r['blockers']==[] and type(r['check_count']) is int and r['check_count']==len(r['checks'])==21204 and all(type(v['passed']) is bool and v['passed'] is True for v in r['checks'])
for key in ('actual_PREP_closed_EXIT0_verified','actual_metadata_writer_closed_EXIT0_verified','all_complete_scope_verified','actual_PREP_metadata_only'):assert r[key] is True
for key in ('whole_combined_build_qualified','whole_combined_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','goal_complete'):assert r[key] is False
for value in r['complete_full_EOF_input_pins']:assert pin(Path(value['path']))==value
receipt=P.with_name(P.name+'_seal_receipt')/'ACTUAL_SAVED_PREP_SEAL_TOOL_RETURN.json'
s=json.loads(receipt.read_bytes());tr=s['terminal_tool_return']
assert s['closed'] is True and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr
observed=json.loads(tr['output']);assert observed['manifest_pin']==pin(P/'MANIFEST.json') and observed['review_pin']==pin(P/'REVIEW.json') and observed['actual_review_tool_receipt_pin']==m['actual_success_review_tool_receipt']
print(json.dumps(dict(source_only=True,status='POSTSEALED_ACTUAL_COMPLETE_PREP_ONLY_REVIEW_UNCHANGED',manifest_pin=pin(P/'MANIFEST.json'),review_pin=pin(P/'REVIEW.json'),actual_review_tool_receipt_pin=m['actual_success_review_tool_receipt'],actual_seal_tool_receipt_pin=pin(receipt),check_count=r['check_count'],member_count=len(m['members']),whole_INPUT_BUILD_native_RSS_physics_AAA_ABA_qualified=False)))
