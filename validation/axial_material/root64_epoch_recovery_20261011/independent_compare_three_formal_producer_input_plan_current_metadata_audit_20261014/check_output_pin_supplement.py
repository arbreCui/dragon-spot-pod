from pathlib import Path
import hashlib,json,os,stat
D=Path(__file__).parent
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()and s.st_size<64*2**20
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  assert ids(os.fstat(f.fileno()))==ids(s);sha=hashlib.file_digest(f,'sha256').hexdigest();assert ids(os.fstat(f.fileno()))==ids(s)
 assert ids(p.lstat())==ids(s);return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ids(s))
def load(p):
 if isinstance(p,dict):assert pin(p['path'])==p;p=p['path']
 return json.loads(Path(p).read_bytes())
def seven(p):
 q=Path(p['path']);s=q.lstat();assert stat.S_ISREG(s.st_mode)and not q.is_symlink()and ids(s)==p['identity']and s.st_size==p['size_bytes']
assert not(D/'OUTPUT_PIN_SUPPLEMENT_REVIEW.json').exists()and not(D/'OUTPUT_PIN_SUPPLEMENT_TRUE_TOOL_RETURNS.json').exists()
ap=pin(D/'REVIEW.json');a=load(ap);atp=pin(D/'TRUE_TOOL_RETURNS.json');at=load(atp)
assert ap['sha256']=='73c3ec7351a15bad5e25d7e2b64b4f8dbf308dc17c1b7ca80b82f7bb17ed59e7'and a['failure']is None
z=at['actual_review_return'];assert type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'])['review_pin']==ap
assert at['observed_closed']is True and type(at['original_integer_exit_code'])is int and at['original_integer_exit_code']==0
plan=load(a['actual_original_plan_pin']);catalog=load(a['actual_current_catalog_pin']);mf=load(a['actual_latest_MF9914_pin'])
crows={r['current_pin']['path']:r['current_pin']for r in catalog['rows']};mrows={p['path']:p for p in mf['current_protected_full_EOF_pins']}
old={r['historical_pin']['path']:r for r in a['exact_rebinding_enumeration']};assert len(old)==2345
outputs={};new={};counts={};reports=[]
for producer in plan['producers']:
 reportpin=pin(producer['report']['path']);report=load(reportpin);reports.append(reportpin);rows=report['output_pins'];assert len(rows)==21
 plane=producer['plane'];outputs[str(plane)]=rows;covered=0
 for p in rows:
  actual=crows[p['path']];assert actual==mrows[p['path']]and actual['path']==p['path']and actual['sha256']==p['sha256']and actual['size_bytes']==p['size_bytes']
  assert p['identity'][0]==16777234 and actual['identity'][0]==16777229 and actual['identity'][1:]==p['identity'][1:]
  seven(actual)
  if p['path']in old:assert old[p['path']]['historical_pin']==p and old[p['path']]['canonical_current_full_EOF_pin']==actual;covered+=1
  else:
   assert p['path']not in new
   new[p['path']]=dict(historical_pin=p,canonical_current_full_EOF_pin=actual,changed_identity_indices=[0],producer_plane=plane,exact_source_catalog_match=True,exact_latest_MF9914_match=True)
 counts[str(plane)]=dict(actual_report_output_pin_count=len(rows),already_covered_by_original2345=covered,new_supplement_count=len(rows)-covered,current_catalog_exact_match_count=len(rows),current_MF9914_exact_match_count=len(rows))
assert counts['1']['already_covered_by_original2345']==21 and counts['2']['already_covered_by_original2345']==counts['3']['already_covered_by_original2345']==2
assert len(new)==38 and len(set(old)|set(new))==2383
for rows in outputs.values():
 for p in rows:seven(crows[p['path']])
for p in [ap,atp,a['actual_original_plan_pin'],a['actual_current_catalog_pin'],a['actual_latest_MF9914_pin']]+reports:seven(p)
result=dict(schema='INDEPENDENT_COMPARE_THREE_PRODUCER_OUTPUT_PIN_CURRENT_METADATA_SUPPLEMENT_V1',status='PASS_COMPARE_THREE_PRODUCER_OUTPUT_PIN_CURRENT_METADATA_SUPPLEMENT',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,formal_plan_or_projection_written=False,
 original_metadata_audit_pin=ap,original_metadata_audit_tools_pin=atp,actual_current_catalog_pin=a['actual_current_catalog_pin'],actual_latest_MF9914_pin=a['actual_latest_MF9914_pin'],actual_producer_report_current_pins=reports,reviewer_source_pin=pin(__file__),actual_output_pin_declarations_by_plane=outputs,actual_per_plane_counts=counts,actual_total_output_pin_declarations=63,actual_already_covered_output_declarations=25,actual_new_distinct_output_paths=38,actual_combined_distinct_rebinding_paths=2383,
 exact_rebinding_enumeration=[new[p]for p in sorted(new)],all63_outputs_exact_dev34_to29_only=True,all_other6_identity_fields_and_original_SHA_and_size_preserved=True,all63_current7_verified_twice=True,all63_catalog_and_current_MF9914_full_EOF_proofs_exact=True,absent_paths=[],non_dev_only_changed_paths=[],current_SHA_proof_missing_paths=[],additional_specific_large_EOF_needed=[],original73c3_metadata_audit_preserved=True,large_scientific_payload_or_tree_EOF_read_by_reviewer=False,no_generic_device_rule_or_missing_skip=True,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
p=D/'OUTPUT_PIN_SUPPLEMENT_REVIEW.json'
with p.open('x')as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(p),actual_new_distinct_output_paths=38,actual_combined_distinct_rebinding_paths=2383,additional_specific_large_EOF_needed=0)),flush=True)
