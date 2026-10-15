from pathlib import Path
import argparse,hashlib,json,os,stat
ROOT=Path('/Users/wen/spot');OUT=ROOT/'validation/storage_cleanup_fourth_20261008'
MANIFEST_SHA='b269c92b933523d781909108405adbd92bc1b3e94335b9782dddf1ed46dce32c'
PREFLIGHT_SHA='675d549186cf1434ce43d9fb2d8c933f7f688505d5f73872f215e54091b23817'
REPORT=Path('/private/tmp/spot_fourth_cleanup_actual_independent_review_20261008.json')
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def load(p):
 b=p.read_bytes();return json.loads(b),{'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def inventory(excluded):
 h=hashlib.sha256();counts={'regular_files':0,'symlinks':0,'directories':0}
 for parent,dirs,files in os.walk(ROOT,followlinks=False):
  dirs.sort();files.sort();dirs[:]=[n for n in dirs if Path(parent)/n!=OUT]
  for n in sorted(dirs+files):
   p=Path(parent)/n
   if str(p)in excluded:continue
   s=p.lstat();rel=str(p.relative_to(ROOT))
   if stat.S_ISLNK(s.st_mode):row=[rel,identity(p),os.readlink(p)];counts['symlinks']+=1
   elif stat.S_ISDIR(s.st_mode):row=[rel,'directory'];counts['directories']+=1
   elif stat.S_ISREG(s.st_mode):row=[rel,identity(p)];counts['regular_files']+=1
   else:raise ValueError(f'unsupported {p}')
   h.update(json.dumps(row,ensure_ascii=False,separators=(',',':')).encode()+b'\n')
 return dict(sha256=h.hexdigest(),**counts)
def symlink_check(selected):
 rows=[]
 for parent,dirs,files in os.walk(ROOT,followlinks=False):
  for n in dirs+files:
   p=Path(parent)/n
   if p.is_symlink():
    target=p.resolve()
    if str(target)in selected or any(Path(q).is_relative_to(target)for q in selected):raise ValueError(f'link enters candidate {p}')
    rows.append([str(p),os.readlink(p),str(target)])
 return {'count':len(rows),'sha256':hashlib.sha256(json.dumps(sorted(rows)).encode()).hexdigest()}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--terminal-chunk',required=True);ap.add_argument('--terminal-observation-sha256',required=True);args=ap.parse_args()
 # No whole filesystem review before Root's actual final observation exists.
 obs,op=load(OUT/'cleanup_terminal_observation.json');assert op['sha256']==args.terminal_observation_sha256
 assert obs['actual_tool_terminal_return_observed']is True
 tool=obs['root_actual_tool_result'];assert type(tool['exit_code'])is int and tool['exit_code']==0
 assert tool['initial_chunk_id']=='4d5dda'and type(tool['session_id'])is int and tool['session_id']==54442 and tool['terminal_chunk_id']==args.terminal_chunk
 m,mp=load(OUT/'manifest.json');p,pp=load(OUT/'preflight.json');r,rp=load(OUT/'cleanup_result.json')
 assert mp['sha256']==MANIFEST_SHA and pp['sha256']==PREFLIGHT_SHA
 assert obs['manifest_sha256']==mp['sha256']and obs['preflight_sha256']==pp['sha256']and obs['cleanup_result_sha256']==rp['sha256']
 assert p['status']=='PASS'and p['manifest_sha256']==MANIFEST_SHA and p['files_deleted']==0
 assert m['selected_count']==69 and len(m['candidates'])==len(p['verified_candidates'])==69
 selected={q['path']for q in m['candidates']};assert len(selected)==69
 assert [q['path']for q in m['candidates']]==[q['path']for q in p['verified_candidates']]
 assert all(not Path(q).exists()and not Path(q).is_symlink()for q in selected)
 for a,b in zip(m['candidates'],p['verified_candidates']):
  assert a['identity']==b['identity']and a['historical_sha256']==b['sha256']and b['bytes']==a['identity'][3]
 ledgerpath=OUT/'retirement_ledger.jsonl';lb=ledgerpath.read_bytes();rows=[json.loads(line)for line in lb.splitlines()]
 assert len(rows)==69 and len({q['path']for q in rows})==69
 assert rows==[dict(**q,deleted=True)for q in p['verified_candidates']]
 assert r['status']=='PASS'and r['deleted_files']==69 and r['deleted_logical_bytes']==m['logical_bytes'] and r['deleted_allocated_bytes']==m['allocated_bytes']
 assert sum(q['bytes']for q in rows)==m['logical_bytes'] and sum(q['allocated_bytes']for q in m['candidates'])==m['allocated_bytes']
 for field in ('complete_INPUT_API_rerun','native_transport_executed','AAA_accuracy_qualified','ABA_admitted'):assert r[field]is False
 assert len(p['fresh_retained_primary_files'])==7 and len(m['retained_closed_anchors'])==40
 for q in p['fresh_retained_primary_files']:assert identity(Path(q['path']))==q['identity']
 for q in m['retained_closed_anchors']:
  v=q['identity'];assert identity(Path(q['path']))==[v[k]for k in ('device','inode','mode','size','mtime_ns','ctime_ns','nlink')]
 current=inventory(selected);assert current==p['preservation_baseline']==r['nonselected_before']==r['nonselected_after']
 links=symlink_check(selected);assert links==m['symlink_check']==r['symlink_check_after']
 sourcepins={}
 for name in ('retire_checked_work_files.py','exact_retire_utils.py'):
  b=(OUT/name).read_bytes();sourcepins[name]=dict(path=str(OUT/name),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
 result={'schema':'SPOT_FOURTH_ACTUAL_69_RETIREMENT_INDEPENDENT_REVIEW_V1','classification':'PASS_ACTUAL_EXACT_69_LEAF_RETIREMENT_WITH_NONSELECTED_METADATA_PRESERVED',
  'actual_terminal_observation':op,'actual_tool':tool,'manifest':mp,'preflight':pp,'cleanup_result':rp,'retirement_ledger':{'path':str(ledgerpath),'sha256':hashlib.sha256(lb).hexdigest(),'bytes':len(lb)},
  'exact_deleted_count':69,'exact_missing_count':69,'historical_expected_hashes_match_fresh_preflight':True,'ledger_exact_complete_preflight_match':True,
  'deleted_logical_bytes':m['logical_bytes'],'deleted_allocated_bytes':m['allocated_bytes'],'fresh_retained_primary_identity_count':7,'fresh_retained_closed_anchor_identity_count':40,
  'independent_whole_nonselected_metadata_fingerprint':current,'independent_project_symlink_check':links,'source_pins':sourcepins,
  'limits':{'large_candidate_or_primary_payloads_rehashed_in_this_review':False,'fresh_candidate_primary_payload_hashes_were_preflight_facts':True,'nonselected_metadata_rescanned_independently':True,'project_or_business_API_or_native_executed':False,'ART_written':False,'files_deleted_by_reviewer':False,'AAA_ABA_or_native_RSS_credit_created':False}}
 REPORT.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps({'report':str(REPORT),'sha256':hashlib.sha256(REPORT.read_bytes()).hexdigest(),'deleted':69,'fingerprint':current}))
if __name__=='__main__':main()
