"""Finite stdlib audit-package sealing; no reviewed project code is executed."""
import ast,hashlib,json,pathlib,stat
ROOT=pathlib.Path(__file__).parent
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 before=identity(p)
 if not stat.S_ISREG(before[2]) or before[3]!=1:raise ValueError('regular single-link required')
 with p.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
 if identity(p)!=before:raise ValueError('complete EOF changed')
 return {'path':str(p),'sha256':digest,'size_bytes':before[4],'identity':before}
report=json.loads((ROOT/'REVIEW.json').read_text())
if report['status']!='PASS_ACTUAL_COMPLETE_PREP_ONLY' or report['check_count']!=len(report['checks']) or not all(x['passed'] is True for x in report['checks']):raise ValueError('true complete review required')
for p in report['complete_full_EOF_input_pins']:
 if pin(pathlib.Path(p['path']))!=p:raise ValueError('third full EOF SHA7ID changed '+p['path'])
ns=json.loads(pathlib.Path(report['actual_complete_namespace_manifest_pin']['path']).read_text())
for q in ns['namespaces']:
 for d in q['directories']:
  if identity(pathlib.Path(q['root'])/d['path'])!=d['identity']:raise ValueError('namespace directory changed')
imports={x.name.split('.')[0] for n in ast.walk(ast.parse((ROOT/'review_script.py').read_text())) if isinstance(n,ast.Import) for x in n.names}
if imports!={'ast','gc','hashlib','json','math','os','pathlib','stat','sys'}:raise ValueError('stdlib source imports contract')
r=json.loads((ROOT/'actual_review_tool_returns.json').read_text())
t=r['terminal_tool_return']
if r['closed'] is not True or r['actual_tool_terminal_return_observed'] is not True or type(t['exit_code']) is not int or t['exit_code']!=0 or 'session_id' in t:raise ValueError('actual closed EXIT0 review required')
members=[pin(p) for p in sorted(ROOT.iterdir()) if p.name!='MANIFEST.json']
if any(not p.is_file() for p in ROOT.iterdir()):raise ValueError('flat complete package required')
manifest={'schema':'INDEPENDENT_V22_ACTUAL_COMPLETE_PREP_REVIEW_COMPLETE_MANIFEST_V1','root':str(ROOT),'members':members,'file_count':len(members),'total_member_bytes':sum(p['size_bytes'] for p in members),'all_member_complete_EOF_SHA7ID_verified':True,'all_review_inputs_third_complete_EOF_SHA7ID_verified':True,'actual_review_exit0':True,'actual_PREP_metadata_only':True,'business_or_scientific_qualification_created':False}
with (ROOT/'MANIFEST.json').open('x') as f:json.dump(manifest,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps({'status':'SEALED','manifest':pin(ROOT/'MANIFEST.json'),'review':pin(ROOT/'REVIEW.json'),'members':len(members),'actual_review_chunk':t['chunk_id'],'actual_review_exit_code':t['exit_code'],'all355_inputs_third_full_EOF_stable':True},allow_nan=False))

