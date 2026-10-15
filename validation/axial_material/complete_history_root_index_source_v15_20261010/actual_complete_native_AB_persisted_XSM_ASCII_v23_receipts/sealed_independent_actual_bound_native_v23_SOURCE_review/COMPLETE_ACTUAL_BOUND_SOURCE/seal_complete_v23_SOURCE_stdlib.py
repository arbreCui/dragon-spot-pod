"""Full bounded SOURCE EOF/SHA7ID/inverse seal only; no candidate execution."""
from pathlib import Path
import ast, hashlib, json
P=Path(__file__).parent
def identity(f):
 s=f.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(f):
 before=identity(f);raw=f.read_bytes();assert before==identity(f)and len(raw)==before[4]
 return {'path':str(f),'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw),'identity':before}
assert not(P/'MANIFEST.json').exists()
files=sorted([f for f in P.rglob('*')if f.is_file()])
before={str(f):pin(f)for f in files}
dirs={str(f):identity(f)for f in P.rglob('*')if f.is_dir()}
assert all(not f.is_symlink()for f in P.rglob('*'))
v=json.loads((P/'SOURCE_SELF_REVIEW.json').read_bytes())
assert v['source_only']is True and v['all_checks_typed_true']is True and v['blockers']==[]
assert v['check_count']==757==len(v['checks'])and len({c['check']for c in v['checks']})==757
assert all(type(c['passed'])is bool and c['passed']is True for c in v['checks'])
i=json.loads((P/'ONE_HUNK_COMPLETE_CHECKER_SOURCE_INVERSE.json').read_bytes())
h=i['hunks'];assert len(h)==1
new=(P/'complete_native_XSM_ASCII_checker_v4.UNREADY.py').read_text()
assert new.count(h[0]['new_utf8'])==1
old=new.replace(h[0]['new_utf8'],h[0]['old_utf8'],1).encode()
assert old==(P/'ORIGINAL_STRICT_SCOPE_V22_SOURCE/complete_native_XSM_ASCII_checker_v4.UNREADY.py').read_bytes()
assert hashlib.sha256(old).hexdigest()=='5c50b197032b8875b9b800c0b3d8301f922846871f9d90d3190960b1e62eaf1e'
for name,sha in [('complete_native_XSM_ASCII_genuine_host.UNREADY.py','9cd50de1033ee0c598500fc54e8b92137ecc746dd9b07dce4dd4c7f88686d42e'),('bind_complete_native_SOURCE_only.UNREADY.py','1ec6f89d00d4b72aa1a5ed70e7bdca95e8267ead7c07aa5351daa70ae64bc585')]:
 assert (P/name).read_bytes()==(P/'ORIGINAL_STRICT_SCOPE_V22_SOURCE'/name).read_bytes()
 assert pin(P/name)['sha256']==sha
for root,mname,count in [(P/'ORIGINAL_STRICT_SCOPE_V22_SOURCE','MANIFEST.json',82),(P/'ORIGINAL_ACTUAL_BOUND_V22_SOURCE','Root_actual_complete_bound_native_SOURCE_manifest.json',88)]:
 m=json.loads((root/mname).read_bytes());members=m['members']
 if type(members)is dict:members=[dict(relative_path=key,**item)for key,item in members.items()]
 assert len(members)==count
 assert {str(f.relative_to(root))for f in root.rglob('*')if f.is_file()}=={q.get('relative_path',q.get('relative'))for q in members}|{mname}
 for q in members:
  actual=pin(root/q.get('relative_path',q.get('relative')))
  assert actual['sha256']==q['sha256']and actual['size_bytes']==q.get('size_bytes',q.get('bytes'))
request=json.loads((P/'ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json').read_bytes())
assert request['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_BINDING_REQUEST_V1'
assert all(v is None for k,v in request.items()if k.endswith('_pin'))
assert all('v23' in value for value in request['namespaces'].values())
audit=json.loads((P/'ALL_STRICT_REQUIRE_SOURCE_CONDITION_AUDIT.json').read_bytes())
assert audit['condition_count']==194==len(audit['conditions'])
assert audit['Source_only_actual_pin_META_expression_demonstration']['new_result']is True
assert audit['Source_only_actual_pin_META_expression_demonstration']['new_result_type']=='bool'
assert all(case['result']is False and case['result_type']=='bool'for case in audit['Source_only_actual_pin_META_expression_demonstration']['empty_and_wrongtype_cases'])
py=0
for f in files:
 if f.suffix=='.py':ast.parse(f.read_bytes());py+=1
for f in (P/'ACTUAL_SOURCE_TOOL_RETURNS').glob('*.json'):
 actual=json.loads(f.read_bytes());tr=actual['terminal_tool_return']
 assert actual['source_only']is True and actual['closed']is True and actual['actual_tool_terminal_return_observed']is True
 assert type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr
assert before=={str(f):pin(f)for f in files}and dirs=={str(f):identity(f)for f in P.rglob('*')if f.is_dir()}
roles={key:pin(P/name)for key,name in [('host_template','complete_native_XSM_ASCII_genuine_host.UNREADY.py'),('checker_template','complete_native_XSM_ASCII_checker_v4.UNREADY.py'),('binder','bind_complete_native_SOURCE_only.UNREADY.py')]}
m={'schema':'SEALED_COMPLETE_NATIVE_V23_STRICT_BOOL_UNREADY_SOURCE_PACKAGE_V1','source_only':True,
   'status':'UNREADY_SOURCE_ONLY_NO_NATIVE_OR_PHYSICS_EXECUTION','members':[dict(relative_path=str(f.relative_to(P)),**before[str(f)])for f in files],
   'member_count':len(files),'total_member_bytes':sum(q['size_bytes']for q in before.values()),
   'subdirectories':[{'path':k,'identity':value}for k,value in dirs.items()],
   'Source_roles':roles,'original_complete_parent_files':83,'original_complete_actual_bound_files':89,
   'all129_original_input_pins_preserved':True,'strict_require_source_condition_count':194,'source_check_count':757,
   'parsed_python_file_count':py,'one_full_checker_hunk_inverse_to_5c50':True,'host_binder_complete_bytes_AST_unchanged':True,
   'fresh_v23_namespace_design':request['namespaces'],'Root_must_observe_fresh_namespaces':True,
   'actual_v23_Source_admission':None,'actual_v23_Source_admission_terminal':None,'actual_v23_bound_Source':None,
   'actual_v23_native_terminal':None,'actual_native_byte_qualification_sha256':None,'actual_scientific_qualification_sha256':None,
   'six_future_business_pins':[None]*6,'candidate_reader_guard_API_or_material_payload_executed':False,'science_qualified':False}
(P/'MANIFEST.json').write_text(json.dumps(m,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
assert before=={str(f):pin(f)for f in files}and dirs=={str(f):identity(f)for f in P.rglob('*')if f.is_dir()}
print(json.dumps({'source_only':True,'status':'SEALED_COMPLETE_NATIVE_V23_SOURCE_ONLY_UNREADY','manifest':pin(P/'MANIFEST.json'),
                  'four_Source_roles':dict(qualified_source_manifest=pin(P/'MANIFEST.json'),**roles),'package_directory_identity_after_manifest':identity(P),
                  'member_count':len(files),'total_member_bytes':m['total_member_bytes'],'source_check_count':757,'require_condition_count':194,
                  'all_Source_EOF_SHA7ID_before_after_unchanged':True,'all129_metadata_pins_preserved':True,
                  'candidate_executed':False,'new_Source_admission':None,'new_native_scientific_Q':None},separators=(',',':')))
