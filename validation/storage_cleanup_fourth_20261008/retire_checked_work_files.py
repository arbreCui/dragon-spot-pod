"""Retire only the reviewed 69-file list; preserve all other workspace identities."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, stat, time
from exact_retire_utils import ROOT,OUT,identity,digest,save,inventory,capacity,symlink_check
AX=OUT/'independent_axial_candidates_review.json'
NONAX=OUT/'nonaxial_candidate_source_review.json'
SCOPE=OUT/'independent_nonaxial_current_scope_review.json'

def historical_sha(ref):
 p=Path(ref['path']);s=Path(ref['historical_stage_result'])
 v=json.loads(s.read_text())
 if v['classification']!='SEALED_STAGE_OUTPUTS':raise ValueError('unsealed old stage')
 h=v['sha256'][p.name]
 if h!=ref['historical_stage_expected_sha256']:raise ValueError('historical stage SHA changed')
 return h

def manifest_sha(ref):
 for e in ref['expected_sha_source_manifests']:
  m=Path(e['manifest']);rows={}
  for line in m.read_text().splitlines():
   sha,member=line.split(maxsplit=1);rows[member.lstrip('*')]=sha
  if rows[e['literal']]!=e['sha256'] or e['sha256']!=ref['recorded_expected_sha256']:raise ValueError('historical manifest SHA changed')
 return ref['recorded_expected_sha256']

def plan():
 a=json.loads(AX.read_text());b=json.loads(NONAX.read_text());scope=json.loads(SCOPE.read_text())
 if len(a['selected_rows'])!=60 or len(b['candidates'])!=9:raise ValueError('wrong candidate counts')
 if scope['classification']!='CURRENT_V4_METADATA_DEPENDENCY_ZERO_INTERSECTION_ONLY' or scope['exact_path_count']!=9:raise ValueError('nonaxial scope not reviewed')
 if digest(NONAX)['sha256']!=scope['candidate_review']['sha256'] or digest(AX)['sha256']!=scope['prior_independent_v4_dependency_review']['sha256']:raise ValueError('independent scope binding mismatch')
 if {r['path'] for r in scope['rows']}!={r['path'] for r in b['candidates']} or any(any(r['current_v4_dependency_intersections'].values()) for r in scope['rows']):raise ValueError('nonaxial current dependency conflict')
 for key in ['current_graph','current_declaration']:
  if digest(Path(scope[key]['path']))['sha256']!=scope[key]['sha256']:raise ValueError('current dependency metadata changed')
 candidates=[];sources={**a['small_metadata_source_pins'],**b['source_document_pins']}
 for path,v in sources.items():
  if digest(Path(path))['sha256']!=v['sha256']:raise ValueError(f'metadata source changed {path}')
 for r in a['selected_rows']:
  p=Path(r['path']);z=r['dependency_exclusion']
  if any(z.values()):raise ValueError('axial dependency conflict')
  if p.name not in {'candidate_axial.xsm','candidate_system.xsm','parent_for_checker.xsm'}:raise ValueError('not agreed scratch leaf')
  family=p.relative_to(ROOT/'validation/artifacts').parts[0]
  if family not in {'axial-material-production-qualified-AB-rank1-factor-cache-20261007','axial-material-production-qualified-AB-white-trace-20261004'} or p.parent.name not in {f'map{i:03d}' for i in range(1,11)}:raise ValueError('outside old stage scope')
  st=r['identity'];expected=[st[k] for k in ['device','inode','mode','size','mtime_ns','ctime_ns','nlink']]
  if identity(p)!=expected:raise ValueError('candidate identity changed')
  candidates.append({'path':str(p),'identity':expected,'allocated_bytes':r['allocated_bytes'],'historical_sha256':historical_sha(r),'category':'old_axial_proposal_system_checker_work_file','historical_stage_result':r['historical_stage_result']})
 for r in b['candidates']:
  p=Path(r['path']);i=identity(p)
  if r['old_protection_file_match'] or r['old_protection_namespace_roots'] or r['fresh_project_symlink_inbound_targets'] or r['ancestor_or_leaf_aliases']:raise ValueError('nonaxial dependency conflict')
  if r['retirement_kind'] not in {'duplicate_replay_npz','duplicate_replay_native_stream','NJOY_intermediate_work_file'}:raise ValueError('unexpected retirement kind')
  candidates.append({'path':str(p),'identity':i,'allocated_bytes':r['allocated_bytes'],'historical_sha256':manifest_sha(r),'category':r['retirement_kind'],'retained_primary':r['retain_primary']})
 selected={x['path'] for x in candidates}
 if len(selected)!=69:raise ValueError('duplicate candidate paths')
 for r in candidates:
  p=Path(r['path']);i=identity(p)
  if not stat.S_ISREG(i[2]) or i[6]!=1 or p.resolve()!=p or not p.is_relative_to(ROOT/'validation/artifacts'):raise ValueError('non-ordinary candidate')
  if i!=r['identity'] or p.stat().st_blocks*512!=r['allocated_bytes']:raise ValueError('candidate allocation changed')
 links=symlink_check(selected)
 save('manifest.json',{'schema':'SPOT_FOURTH_EXACT_WORK_FILE_RETIREMENT_V1','candidates':candidates,'source_document_pins':sources,'candidate_source_reports':[digest(AX),digest(NONAX),digest(SCOPE)],'selected_count':69,'logical_bytes':sum(r['identity'][3] for r in candidates),'allocated_bytes':sum(r['allocated_bytes'] for r in candidates),'symlink_check':links,'retained_closed_anchors':a['retained_closed_anchor_rows'],'current_complete_INPUT_graph_unchanged':True,'all_result_documents_logs_source_and_final_data_retained':True,'old_full_intermediate_replay_retired':True,'files_deleted':0})
 print(json.dumps({'status':'EXACT_69_PLANNED','allocated_bytes':sum(r['allocated_bytes'] for r in candidates)}))

def preflight():
 m=json.loads((OUT/'manifest.json').read_text());selected={r['path'] for r in m['candidates']};before=inventory(selected)
 for path,v in m['source_document_pins'].items():
  if digest(Path(path))['sha256']!=v['sha256']:raise ValueError('metadata changed')
 for r in m['candidate_source_reports']:
  if digest(Path(r['path']))!=r:raise ValueError('source review changed')
 if symlink_check(selected)!=m['symlink_check']:raise ValueError('links changed')
 checked=[];retained={}
 for r in m['candidates']:
  d=digest(Path(r['path']))
  if d['identity']!=r['identity'] or d['sha256']!=r['historical_sha256']:raise ValueError(f'fresh candidate mismatch {r["path"]}')
  checked.append(d)
  if 'retained_primary' in r:
   q=r['retained_primary'];p=Path(q['path']);z=retained.setdefault(str(p),digest(p))
   if z['sha256']!=manifest_sha(q) or z['bytes']!=q['bytes']:raise ValueError('retained primary mismatch')
   if q['same_bytes_required'] and (z['sha256']!=d['sha256'] or z['bytes']!=d['bytes']):raise ValueError('duplicate differs from primary')
 for r in m['retained_closed_anchors']:
  v=r['identity'];expected=[v[k] for k in ['device','inode','mode','size','mtime_ns','ctime_ns','nlink']]
  if identity(Path(r['path']))!=expected:raise ValueError('closed anchor changed')
 if inventory(selected)!=before:raise ValueError('noncandidate files changed during preflight')
 save('preflight.json',{'schema':'SPOT_FOURTH_FRESH_CONTENT_PREFLIGHT_V1','status':'PASS','manifest_sha256':digest(OUT/'manifest.json')['sha256'],'verified_candidates':checked,'fresh_retained_primary_files':list(retained.values()),'preservation_baseline':before,'capacity_before':capacity(),'files_deleted':0,'complete_INPUT_API_rerun':False,'all_nonselected_file_identity_fingerprint_checked':True})
 print(json.dumps({'status':'PREFLIGHT_PASS','fresh_candidates':len(checked),'fresh_retained_primary':len(retained),'manifest_sha256':digest(OUT/'manifest.json')['sha256'],'preflight_sha256':digest(OUT/'preflight.json')['sha256']}))

def apply(msha,psha):
 start=time.monotonic()
 if digest(OUT/'manifest.json')['sha256']!=msha or digest(OUT/'preflight.json')['sha256']!=psha:raise ValueError('Root-observed evidence pins required')
 m=json.loads((OUT/'manifest.json').read_text());p=json.loads((OUT/'preflight.json').read_text());selected={r['path'] for r in m['candidates']}
 if p['status']!='PASS' or p['manifest_sha256']!=msha or len(selected)!=69 or [x['path'] for x in p['verified_candidates']]!=[x['path'] for x in m['candidates']]:raise ValueError('preflight selection mismatch')
 if inventory(selected)!=p['preservation_baseline'] or symlink_check(selected)!=m['symlink_check']:raise ValueError('preservation or links changed')
 for v in p['verified_candidates']+p['fresh_retained_primary_files']:
  if identity(Path(v['path']))!=v['identity']:raise ValueError('checked file changed after read')
 with (OUT/'retirement_ledger.jsonl').open('x') as f:
  for v in p['verified_candidates']:
   q=Path(v['path'])
   if identity(q)!=v['identity']:raise ValueError('candidate changed before unlink')
   q.unlink();f.write(json.dumps(dict(**v,deleted=True),ensure_ascii=False)+'\n');f.flush()
 after=inventory(selected)
 if after!=p['preservation_baseline']:raise ValueError('noncandidate preservation mismatch after deletion')
 if any(Path(q).exists() or Path(q).is_symlink() for q in selected):raise ValueError('selected leaf remains')
 save('cleanup_result.json',{'schema':'SPOT_FOURTH_ACTUAL_69_FILE_RETIREMENT_RESULT_V1','status':'PASS','deleted_files':69,'deleted_logical_bytes':m['logical_bytes'],'deleted_allocated_bytes':m['allocated_bytes'],'capacity_before':p['capacity_before'],'capacity_after':capacity(),'nonselected_before':p['preservation_baseline'],'nonselected_after':after,'symlink_check_after':symlink_check(selected),'complete_INPUT_API_rerun':False,'native_transport_executed':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'elapsed_seconds':time.monotonic()-start})
 print(json.dumps({'status':'CLEANUP_PASS','deleted_files':69,'deleted_allocated_bytes':m['allocated_bytes'],'nonselected_fingerprint':after}))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['plan','preflight','apply']);ap.add_argument('--manifest-sha');ap.add_argument('--preflight-sha');a=ap.parse_args()
 if a.action=='plan':plan()
 elif a.action=='preflight':preflight()
 else:apply(a.manifest_sha,a.preflight_sha)
