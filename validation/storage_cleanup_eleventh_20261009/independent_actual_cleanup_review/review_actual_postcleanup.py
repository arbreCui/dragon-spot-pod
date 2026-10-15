"""Pure stdlib readonly post-cleanup integrity reader. Never applies/restores or runs science."""
import argparse
import hashlib
import json
import math
import os
import re
import stat
from pathlib import Path
ROOT=Path('/Users/wen/spot')
R=ROOT/'validation/storage_cleanup_eleventh_20261009'
OUT=Path('/private/tmp/spot_storage_eleventh_actual_postcleanup_independent_review_20261009/evidence')
MANIFEST_SHA='5a2462cb67b387543e98607911d16100d0cf67ab347c0a555195b1390db7f853'
PREFLIGHT_SHA='35d3fc027c4d26a3de0e68859844047d106c872166cf9a1e8a240e72f20fc870'
BASELINE_SHA='605d019f617ffdb3208a346962aaefbb68a722c6fc558ffefe9ff99cae661d1b'
CLEANUP_SOURCE_SHA='8ee7ea6dd3b7162ce06f687167fcc035c0804ba9f0b9bf72444abb7ca32c2e8b'
DOCUMENT_BASELINE_SHA='cc44e60f886f2f15eaa6e33b96d05c18a542b53ab58fdcccb3c818834574c420'
PINS={}
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pairs(values):
 d={}
 for k,v in values:
  if k in d:raise ValueError('duplicate control metadata key')
  d[k]=v
 return d
def json_data(raw):
 d=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError('nonfinite control JSON')))
 def finite(x):
  if isinstance(x,float):assert math.isfinite(x)
  elif isinstance(x,dict):
   for v in x.values():finite(v)
  elif isinstance(x,list):
   for v in x:finite(v)
 finite(d);return d
def read(p,expected_sha=None,expected_identity=None,raw=True):
 p=Path(p);before=identity(p.lstat());assert p.is_absolute() and p.parent.resolve(strict=True)==p.parent and stat.S_ISREG(before[2])
 if expected_identity is not None:assert before==expected_identity,('identity changed',str(p))
 h=hashlib.sha256();chunks=[]
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
  assert identity(os.fstat(f.fileno()))==before
  while data:=f.read(4*1024**2):
   h.update(data)
   if raw:chunks.append(data)
  assert identity(os.fstat(f.fileno()))==before
 after=identity(p.lstat());assert after==before
 if expected_sha is not None:assert h.hexdigest()==expected_sha,('content changed',str(p))
 PINS[str(p)]=dict(path=str(p),size=before[3],sha256=h.hexdigest(),identity=before)
 return b''.join(chunks) if raw else PINS[str(p)]
def load(p,sha=None):return json_data(read(p,sha))
def snapshot():
 files,links,dirs={},{},[]
 for cur,sub,names in os.walk(ROOT,followlinks=False):
  base=Path(cur)
  if base==ROOT:sub[:]=[s for s in sub if s!='.git']
  sub[:]=[s for s in sub if base/s!=R]
  dirs.append(str(base.relative_to(ROOT)))
  for n in sub+names:
   p=base/n;s=p.lstat();rel=str(p.relative_to(ROOT))
   if stat.S_ISLNK(s.st_mode):links[rel]=[identity(s),os.readlink(p)]
   elif stat.S_ISREG(s.st_mode):files[rel]=identity(s)
 return dict(files=files,links=links,dirs=sorted(dirs))
def fingerprint(d):return hashlib.sha256(json.dumps(d,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def write(name,d):
 with (OUT/name).open('x') as f:json.dump(d,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
def check_actual_closed0(tool):
 assert tool['closed'] is True and type(tool['exit_code']) is int and tool['exit_code']==0
 if 'completion_tool' in tool:
  terminal=tool['completion_tool'];assert type(terminal['exit_code']) is int and terminal['exit_code']==0
  assert type(tool['initial_tool']['session_id']) is int and type(terminal['chunk_id']) is str
  return dict(initial_chunk_id=tool['initial_tool']['chunk_id'],session_id=tool['initial_tool']['session_id'],terminal_chunk_id=terminal['chunk_id'],exit_code=0,closed=True)
 assert type(tool['session_id']) is int and type(tool['initial_chunk_id']) is str and type(tool['terminal_chunk_id']) is str
 if 'actual_deletion_completed' in tool:assert tool['actual_deletion_completed'] is True
 return {k:tool[k] for k in ('initial_chunk_id','session_id','terminal_chunk_id','exit_code','closed')}
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--actual-tool-sha',required=True)
 ap.add_argument('--actual-result-sha',required=True)
 ap.add_argument('--tool-path',type=Path,default=R/'cleanup_terminal_observation.json')
 ap.add_argument('--stdout-path',type=Path,default=R/'cleanup.stdout')
 ap.add_argument('--stderr-path',type=Path,default=R/'cleanup.stderr')
 args=ap.parse_args()
 for value in (args.actual_tool_sha,args.actual_result_sha):assert re.fullmatch('[0-9a-f]{64}',value)
 for p in (args.tool_path,args.stdout_path,args.stderr_path):assert p.parent==R
 assert not OUT.exists(), 'never overwrite an earlier independent outcome'
 # Only true Root terminal0 and its fixed completed result can enable this reader.
 tool=load(args.tool_path,args.actual_tool_sha);actual_tool=check_actual_closed0(tool)
 result=load(R/'cleanup_result.json',args.actual_result_sha)
 assert result['status']=='PASS_ACTUAL_EXACT_DUPLICATE_CLEANUP' and result['scientific_credit'] is False
 stdout=read(args.stdout_path);stderr=read(args.stderr_path);assert stderr==b'' and json_data(stdout)==result
 if 'stdout_sha256' in tool:assert tool['stdout_sha256']==PINS[str(args.stdout_path)]['sha256']
 if 'stderr_sha256' in tool:assert tool['stderr_sha256']==PINS[str(args.stderr_path)]['sha256']
 if 'manifest_sha256' in tool:assert tool['manifest_sha256']==MANIFEST_SHA
 if 'cleanup_result_sha256' in tool:assert tool['cleanup_result_sha256']==args.actual_result_sha
 if 'solver_or_API_executed' in tool:assert tool['solver_or_API_executed'] is False
 m=load(R/'manifest.json',MANIFEST_SHA)
 pre=load(R/'preflight.json',PREFLIGHT_SHA)
 assert pre['status']=='PASS_FIXED_FULL_SHA_PREFLIGHT' and pre['executed'] is False and pre['manifest_sha256']==MANIFEST_SHA and pre['untouched_snapshot_sha256']==BASELINE_SHA
 pretool=load(R/'preflight_terminal_observation.json','b4cd9ef027df1c6204a6f5b9fb73452445da5fbe13f85e0cff148d91e3305474')
 assert pretool['closed'] is True and type(pretool['exit_code']) is int and pretool['exit_code']==0 and pretool['initial_chunk_id']=='3cf8b4' and pretool['terminal_chunk_id']=='55000b' and pretool['session_id']==84533
 assert pretool['preflight_sha256']==PREFLIGHT_SHA and pretool['manifest_sha256']==MANIFEST_SHA
 assert json_data(read(R/'preflight.stdout',pretool['stdout_sha256']))==pre and read(R/'preflight.stderr',pretool['stderr_sha256'])==b''
 assert m['cleanup_source_sha256']==CLEANUP_SOURCE_SHA and m['result_document_baseline_sha256']==DOCUMENT_BASELINE_SHA and m['scientific_credit'] is False
 read(R/'cleanup_fixed_duplicates.py',CLEANUP_SOURCE_SHA,raw=False)
 docs=load(R/'result_document_full_sha_baseline.json',DOCUMENT_BASELINE_SHA)
 assert m['exact_count']==len(m['candidates'])==15 and len(m['retained_primaries'])==17 and len(m['source_and_review_pins'])==4164
 assert len(docs['rows'])==32585 and docs['bytes']==3797135364 and docs['whole_project_content_hashed'] is False
 paths=[r['path'] for r in m['candidates']];assert len(set(paths))==15
 assert result['manifest_sha256']==MANIFEST_SHA and result['removed_count']==15 and result['removed_paths']==paths
 assert result['removed_logical_bytes']==sum(r['size'] for r in m['candidates'])==m['logical_bytes']
 assert result['removed_allocated_bytes']==sum(r['allocated_bytes'] for r in m['candidates'])==m['allocated_bytes']
 assert all(result[k] is True for k in ('all_other_regular_paths_and_identities_unchanged','all_symlinks_and_directory_paths_unchanged','all_retained_primaries_and_source_pins_full_sha_unchanged'))
 assert result['result_documents_full_sha_checked_before_and_after']==32585
 for r in m['candidates']:
  p=Path(r['path']);assert p.is_relative_to(ART:=ROOT/'validation/artifacts') and p.parent.resolve(strict=True)==p.parent and not os.path.lexists(p)
 ledger_raw=read(R/'retirement_ledger.jsonl');ledger=[json_data(line) for line in ledger_raw.splitlines() if line]
 assert len(ledger)==15
 for actual,original in zip(ledger,m['candidates']):
  assert set(actual)==set(original)|{'removed_at'} and {k:actual[k] for k in original}==original
  assert type(actual['removed_at']) in (int,float) and result['started']<=actual['removed_at']<=result['finished']
 expected={};roles={}
 for role,rows in [('retained_primary',m['retained_primaries']),('source_and_review',m['source_and_review_pins']),('result_document',docs['rows'])]:
  for row in rows:
   p=str(ROOT/row['path']) if role=='result_document' else row['path']
   assert p not in paths
   normalized={**row,'path':p}
   if p in expected:assert (expected[p]['size'],expected[p]['sha256'],expected[p]['identity'])==(normalized['size'],normalized['sha256'],normalized['identity'])
   else:expected[p]=normalized
   roles.setdefault(p,[]).append(role)
 # Independent full reads, not reuse of author hashes or a 35GB scientific input gate.
 for p,row in expected.items():
  read(p,row['sha256'],row['identity'],False);assert PINS[p]['size']==row['size']
 after=snapshot()
 assert len(after['links'])==687
 assert all(str(ROOT/p) not in paths for p in after['files'])
 restored={**after,'files':dict(after['files'])}
 for row in m['candidates']:
  rel=str(Path(row['path']).relative_to(ROOT));assert rel not in restored['files'];restored['files'][rel]=row['identity']
 assert fingerprint(restored)==BASELINE_SHA, 'nonselected project identity or path snapshot changed'
 for p,row in PINS.items():assert identity(Path(p).lstat())==row['identity']
 again=snapshot();assert again==after, 'project snapshot changed during independent audit'
 OUT.mkdir()
 write('all_fresh_retained_source_document_FULL_SHA_identity.json',[dict(**PINS[p],roles=roles[p]) for p in sorted(expected)])
 write('full_project_actual_after_snapshot_metadata_only.json',after)
 write('actual_15_ledger_exact_manifest_comparison.json',dict(all_15_original_candidate_full_records_exact=True,all_15_paths_absent=True,ledger_sha256=PINS[str(R/'retirement_ledger.jsonl')]['sha256'],manifest_sha256=MANIFEST_SHA,rows=ledger))
 write('control_receipts_and_metadata_fresh_pins.json',[v for p,v in PINS.items() if p not in expected])
 report=dict(schema='SPOT_ELEVENTH_ACTUAL_POSTCLEANUP_INDEPENDENT_READONLY_REVIEW_V1',status='PASS',scope='ACTUAL_POSTCLEANUP_FILE_INTEGRITY_ONLY',manifest_sha256=MANIFEST_SHA,preflight_sha256=PREFLIGHT_SHA,expected_whole_baseline_sha256=BASELINE_SHA,cleanup_result_sha256=args.actual_result_sha,actual_Root_cleanup_tool_receipt_sha256=args.actual_tool_sha,actual_Root_cleanup_tool=actual_tool,removed_count=15,removed_logical_bytes=m['logical_bytes'],removed_allocated_unique_single_inode_bytes=m['allocated_bytes'],all15_selected_paths_actually_absent=True,all15_ledger_entries_equal_original_manifest_rows_and_SHA=True,retained17_primaries_full_SHA_identity_unchanged=True,source_and_review4164_pins_full_SHA_identity_unchanged=True,result_documents32585_paths_full_SHA_identity_unchanged=True,result_document_bytes=3797135364,independent_unique_full_SHA_file_count=len(expected),independent_unique_full_SHA_bytes=sum(r['size'] for r in expected.values()),actual_other_regular_file_count=len(after['files']),actual_symlink_count=len(after['links']),actual_directory_count=len(after['dirs']),reinsert_original15_identity_reconstructs_preflight_digest=True,reconstructed_preflight_snapshot_sha256=fingerprint(restored),post_snapshot_sha256=fingerprint(after),all_nonselected_snapshot_repeated_equal=True,actual_Root_stdout_stderr_FULL_SHA_validated=True,original_preflight_true0_receipt_and_streams_validated=True,source_cleanup8ee7_and_original_document_baseline_pinned=True,Root_before_capacity=result['before_capacity'],Root_after_capacity=result['after_capacity'],capacity_is_actual_Root_observation_not_system_free_space_attribution=True,old_scientific_results_or_seals_rewritten=False,retained_work_copy_restore_sources_kept=True,current_canonical_physics_union_not_rerun=True,business_import_API_constructor_PREP_RUN_restore_apply_native=False,formal_ART_project_written=False,new_RSS_science_AAA_ABA_credit=False,actual_independent_reader_tool_terminal=None,limitations=['Only declared retained/source/document files were fully SHA-read; all other regular paths were independently compared by the original seven-field identity snapshot.','Root actual closed0 and completed cleanup metadata are mandatory. No deletion or restoration is implemented by this reader.','R11 and .git are excluded using the exact source preflight snapshot convention; original source/candidate reports are preserved.','Observed project allocations and shared free-space figures are reported as observations and do not establish dedicated disk-space release.'])
 write('REPORT.json',report)
 print(json.dumps(dict(status='PASS',scope=report['scope'],manifest_sha256=MANIFEST_SHA,cleanup_result_sha256=args.actual_result_sha,removed_count=15,independent_FULL_SHA_files=len(expected),independent_FULL_SHA_bytes=report['independent_unique_full_SHA_bytes'],actual_regulars=len(after['files']),actual_links=687,actual_dirs=len(after['dirs']),preflight_baseline_reconstructed=BASELINE_SHA,report_sha256=hashlib.sha256((OUT/'REPORT.json').read_bytes()).hexdigest(),files_deleted_by_reader=0,no_business=True)))
if __name__=='__main__':main()
