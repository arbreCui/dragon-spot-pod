"""Run only after Root provides its genuine closed PREP witness; no business imports."""
import argparse
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import stat

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
SOURCE=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-combined-source-v12-20261009'
OUT=ART/'axial-material-owned-specs-identity-key-delta-graph-table-combined-runtime-v12-20261009'
FACTORY=ROOT/'validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py'
HELPER=ROOT/'validation/axial_material/combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
FACTORY_SHA='5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b'
HELPER_SHA='e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28'
SPECS=ROOT/'validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json'
SPECS_SHA='2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa'
PREFIX='AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_COMBINED_RUNTIME_V12'
GRAPH_SCHEMA='AXMAT_COMBINED_RUNTIME_VERIFIED_INPUT_GRAPH_REQUIREMENTS_VARINT_WIRE_V1'
STORAGE_SCHEMA='AXMAT_COMPLETE_INPUT_GRAPH_CANONICAL_FILE_TABLE_STORAGE_V1'
INPUT_SCOPE='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION'
CAP=67108864
COLS=['path','sha256','size_bytes']
FULL_SOURCE_NAMES={'historical_input_combined_runtime_factory.py','input_specs.json','source_admission.json','trim_component_admission_INPUT.json','trim_component_API_python_open_trace.json','trim_component_API_absence_INPUT.json','runtime/graph.py','runtime/codec.py','runtime/current.py','runtime/checks.py','runtime/ordinary.py'}

def sig(s):return (s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink)
def valid_sha(v):return type(v)is str and len(v)==64 and all(c in '0123456789abcdef'for c in v)
def normal(p):
 p=Path(p)
 assert p.is_absolute() and '..' not in p.parts
 for q in [*reversed(p.parents),p]:assert not q.is_symlink(),str(q)
 return p
def fresh(p,expected=None,collect=False,max_bytes=None):
 p=normal(p);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);parts=[] if collect else None;h=hashlib.sha256();n=0
 try:
  before=os.fstat(fd);assert stat.S_ISREG(before.st_mode)
  if max_bytes is not None:assert before.st_size<=max_bytes
  while True:
   b=os.read(fd,1048576)
   if not b:break
   n+=len(b)
   if max_bytes is not None:assert n<=max_bytes
   h.update(b)
   if collect:parts.append(b)
  after=os.fstat(fd);assert sig(before)==sig(after)==sig(p.stat()) and n==before.st_size
 finally:os.close(fd)
 digest=h.hexdigest()
 if expected is not None:assert valid_sha(expected) and digest==expected,str(p)
 return dict(path=str(p),sha256=digest,bytes=n,seven_identity=list(sig(after))),b''.join(parts)if collect else None
def bad_constant(v):raise ValueError('nonfinite JSON '+v)
def finite_float(v):
 v=float(v);assert math.isfinite(v);return v
def strict(p,expected=None,max_bytes=CAP):
 pin,raw=fresh(p,expected,True,max_bytes);text=raw.decode('utf-8');del raw
 strings={};integers={}
 def intern_values(v):
  if type(v)is str:return strings.setdefault(v,v)
  if type(v)is list:
   for i,x in enumerate(v):v[i]=intern_values(x)
  return v
 def pairs(items):
  value={}
  for k,v in items:
   assert k not in value,'duplicate JSON key'
   value[k]=v
  return {strings.setdefault(k,k):intern_values(value[k])for k in sorted(value)}
 def integer(s):
  v=int(s);return integers.setdefault(v,v)
 try:value=json.loads(text,object_pairs_hook=pairs,parse_int=integer,parse_float=finite_float,parse_constant=bad_constant)
 finally:strings.clear();integers.clear()
 del text
 return value,pin

import ast
import textwrap
import time
OLD=Path('/private/tmp/axmat_v12_graph_table_cold_source_only_20261009')
NEW=Path('/private/tmp/axmat_v12_cold_binding_authoritative_sources_and_callback_schema_fix_source_only_20261009')
V11=Path('/private/tmp/axmat_v11_cold_component_input_consumer_source_only_20261009')
DEST=Path('/private/tmp/axmat_v12_cold_callback_schema_independent_source_review_20261009')
F='prepare_owned_specs_identity_key_delta_graph_table_cold_runtime_v12.py'
C='cold_component_input_consumer_identity_key_delta_graph_table_own_pid_peak_v12.py'
B='cold_owned_specs_identity_key_delta_graph_table_component_input_intake_binding_v12_20261009.json'
NEWF='1941375f15d61b44c17ec11e2466048f646112c6c5939ce568c9fdffc84a93a6'
OLDF='ee7fc7ab17124fe110ec965829710a9cb4c9e19368991b806badbea18422cb3c'
CSHA='0e47a2084acc30085784c132eb480db7e53b10963db6c4ca85b66cc76cf557fa'
BSHA='563b3f7fa28c93427b9a4613bb7b958d998e56a66a2fe85d959c3ec88440abc0'
OBS={};CHECKS=[]
def check(name,condition):
 assert condition,name;CHECKS.append(name)
def data(p,sha=None):
 pin,raw=fresh(p,sha,True,CAP);OBS[str(p)]=pin
 def pairs(items):
  out={}
  for k,v in items:assert k not in out,'duplicate JSON field';out[k]=v
  return out
 return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_float=finite_float,parse_constant=bad_constant)
def text(p,sha=None):
 pin,b=fresh(p,sha,True);OBS[str(p)]=pin;return b.decode('utf-8')
def assigns(s):return {n.targets[0].id:n for n in ast.parse(s).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def defs(s):
 result={}
 def walk(nodes,prefix=''):
  for n in nodes:
   if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
    result[prefix+n.name]=ast.get_source_segment(s,n);walk(n.body,prefix+n.name+'.')
 walk(ast.parse(s).body);return result
def undo(s,edits,whole_literals=False):
 result=s
 for e in reversed(edits):
  count=result.count(e['new'])
  if whole_literals and e['name'].startswith('literal family identity '):assert count>0;result=result.replace(e['new'],e['old'])
  else:assert count==1,(e['name'],count);result=result.replace(e['new'],e['old'],1)
 return result
def literal(a,key):return ast.literal_eval(a[key].value)
def nones(a):return [k for k,n in a.items()if isinstance(n.value,ast.Constant)and n.value.value is None]
def nullpaths(d,prefix=()):
 out=[]
 if isinstance(d,dict):
  for k,v in d.items():out.extend(nullpaths(v,prefix+(k,)))
 elif isinstance(d,list):
  for i,v in enumerate(d):out.extend(nullpaths(v,prefix+(i,)))
 elif d is None:out.append(list(prefix))
 return out

def main():
 old=text(OLD/F,OLDF);new=text(NEW/F,NEWF);oc=text(OLD/C,CSHA);nc=text(NEW/C,CSHA);ob=data(OLD/B,BSHA);nb=data(NEW/B,BSHA)
 proof=data(NEW/'source_inverse_proof.json','99a4405448cd305be7e5c9eda2589ca12f529d588b8a0ae1ad70aeb0bf3834be');prior=data(OLD/'source_inverse_proof.json','3dca8c5e1f91be24df0fc671007783d5e316f9e7a9b5fb41052aabf3c3c8f8f7');mother=data(V11/'source_inverse_proof.json','e6ed4db3f137f7c50a99f7e27184877a14392a9f8af3b321c1418a28e6e1a4c1')
 check('consumer and binding exactly unmodified',nc==oc and nb==ob)
 check('one full ADMISSION_HOST assignment region inverse',len(proof['edits'])==1 and undo(new,proof['edits'])==old)
 oa=assigns(old);na=assigns(new);ca=assigns(nc)
 check('all 55 factory definitions byteexact to frozen Fee7',defs(new)==defs(old)and len(defs(new))==55)
 check('factory top assignment only generated admission template changed',set(oa)==set(na)and [k for k in oa if ast.get_source_segment(old,oa[k])!=ast.get_source_segment(new,na[k])]==['ADMISSION_HOST'])
 inverse_reports=[]
 for name,s in [(F,old),(C,nc)]:
  p=prior['proofs'][name];v11=text(p['parent_path'],p['parent_sha256']);inverse=undo(s,p['edits']);check(name+' complete V12 identity inverse exact to V11',inverse==v11)
  mp=mother['proofs'][Path(p['parent_path']).name];genuine=undo(inverse,mp['edits'],True);want=mp['parent_sha256'];check(name+' complete ancestral V10 hash inverse',hashlib.sha256(genuine.encode()).hexdigest()==want)
  genuine_name='prepare_historical_input_owned_specs_physical_factor_diagonal_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak_v10.py'if name==F else'cold_component_input_consumer_factor_diagonal_trim_own_pid_peak_v10.py'
  check(name+' genuine installed V10 full source byteexact',text(ROOT/'validation/axial_material'/genuine_name,want)==genuine)
  changed=[k for k,v in defs(s).items()if v!=defs(v11)[k]]
  check(name+' only permitted V12 function changes',set(changed)==({'render_controller','declare'}if name==F else set()))
  inverse_reports.append(dict(name=name,V12_regions=len(p['edits']),extra_callback_regions=1 if name==F else 0,V11_regions=len(mp['edits']),V11_sha256=p['parent_sha256'],genuine_V10_sha256=want,changed_V12_definitions=changed))
 bp=prior['proofs'][B];parent=data(bp['parent_path'],bp['parent_sha256']);restored=dict(nb)
 for e in bp['changed_top_level_fields']:restored[e['key']]=e['old']
 check('binding complete original JSON inverse byteexact',json.dumps(restored,indent=2)+'\n'==text(bp['parent_path'],bp['parent_sha256']))
 check('UNREADY source guard and no future credentials',literal(na,'DRAFT_STATUS')==literal(oa,'DRAFT_STATUS')=='UNREADY'and literal(ca,'STATUS')=='UNREADY'and nones(na)==nones(oa)and len(nones(na))==25 and len(nones(ca))==22 and nullpaths(nb)==nullpaths(ob))
 check('genuine V11 component ancestry assignments unchanged',all(ast.get_source_segment(new,na[k])==ast.get_source_segment(old,oa[k])for k in oa if k.startswith('TRIM_')))
 check('all original factory resource/physics/source contracts unchanged',all(ast.get_source_segment(new,na[k])==ast.get_source_segment(old,oa[k])for k in ['BUDGETS','CACHE_BUDGET_BYTES','CONSTRUCTOR_BEFORE','CONSTRUCTOR_AFTER','DECK_HOOK','ORIGINAL_COLD_RESERVE_BYTES','ORIGINAL_COMPLETE_12_MAP_CASE_BYTES','CORRECTION_SCOPE','HOST','HOST_SHA','CONTROLS','CONTROLS_SHA','SCIPY_HELPER','SCIPY_HELPER_SHA','OWN_PID_SUPERVISOR','OWN_PID_SUPERVISOR_SHA']))
 callback=literal(na,'CALLBACK_METADATA_SCHEMA');old_callback='AXMAT_HISTORICAL_INPUT_OWNED_SPECS_SCIPY_ENV_CROSS_GROUP_IDENTITY_KEY_DELTA_COMBINED_FILE_SNAPSHOT_COLD_INPUT_ADMISSION_V1'
 check('exact V12 callback schema identity',callback=='AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_SCIPY_ENV_COLD_INPUT_ADMISSION_V12'and old.count(old_callback)==1 and new.count(old_callback)==0)
 templates={k:n.value.value for k,n in na.items()if isinstance(n.value,ast.Constant)and isinstance(n.value.value,str)and '\n'in n.value.value};check('exact four generated template sites',set(templates)=={'CONSTRUCTOR_BEFORE','CONSTRUCTOR_AFTER','DECK_HOOK','ADMISSION_HOST'})
 templates_report=[]
 for k,t in templates.items():
  tree=ast.parse(textwrap.dedent(t));before=literal(oa,k)
  check(k+' exact permitted template delta',t==before if k!='ADMISSION_HOST'else t==before.replace(old_callback,callback,1))
  templates_report.append(dict(name=k,bytes=len(t.encode()),AST_parse_only=True,unchanged_from_Fee7=k!='ADMISSION_HOST',top_functions=[n.name for n in tree.body if isinstance(n,ast.FunctionDef)]))
 embedded=ast.parse(templates['ADMISSION_HOST']);metadata=next(n for n in embedded.body if isinstance(n,ast.FunctionDef)and n.name=='metadata')
 checks=[n for n in ast.walk(metadata)if isinstance(n,ast.Compare)and isinstance(n.left,ast.Subscript)and isinstance(n.left.value,ast.Name)and n.left.value.id=='data'and isinstance(n.left.slice,ast.Constant)and n.left.slice.value=='schema']
 check('generated metadata exact active schema equality',len(checks)==1 and len(checks[0].comparators)==1 and ast.literal_eval(checks[0].comparators[0])==callback)
 declare=next(n for n in ast.parse(new).body if isinstance(n,ast.FunctionDef)and n.name=='declare');producer=[n for n in ast.walk(declare)if isinstance(n,ast.keyword)and n.arg=='schema'and isinstance(n.value,ast.Name)and n.value.id=='CALLBACK_METADATA_SCHEMA']
 check('actual declaration producer uses same schema variable',len(producer)==1)
 check('installed V12 combined source identity only',literal(na,'COMBINED_FACTORY_SHA')==literal(ca,'API_SOURCE_SHA')==FACTORY_SHA and literal(ca,'GRAPH_SOURCE_SHA')==HELPER_SHA)
 text(FACTORY,FACTORY_SHA);text(HELPER,HELPER_SHA)
 plan=data(NEW/'BINDING_PLAN_AND_REPORT.json','77bab26cf4f399104a5f45c9723f5c1b3e88297f233fcca8ca5de1fa3810df1b')
 check('binding plan exact full future None coverage',set(plan['None_binding_authorities'][F])==set(nones(na))and set(plan['None_binding_authorities'][C])==set(nones(ca)))
 for k in ['future_actual_bounded_INPUT','future_actual_cold_declare','future_actual_PREP','future_actual_controls','future_actual_native']:check('future plan field empty '+k,plan[k]is None)
 receipt=data(NEW/'actual_source_fix_and_binding_plan_tool_return.json','fc97c966444ef2b4566f09b19c4e2df9c7927c89f3a3c681f0de3f96717f472b');originalreceipt=data(OLD/'source_generation_actual_tool_return.json')
 for label,r in [('original source generation',originalreceipt),('callback repair generation',receipt)]:check(label+' actual typed zero closed source-only',type(r['exit_code'])is int and r['exit_code']==0 and r['closed']is True and r['session_id']is None)
 check('new source proof exact generator pins',receipt['new_factory_sha256']==NEWF and receipt['report_sha256']==OBS[str(NEW/'BINDING_PLAN_AND_REPORT.json')]['sha256']and receipt['source_inverse_proof_sha256']==OBS[str(NEW/'source_inverse_proof.json')]['sha256']and receipt['business_executed']is False and receipt['fixture_or_compiler_executed']is False and receipt['project_written']is False and receipt['standalone_whole_INPUT_qualified']is False and receipt['native_RSS_or_science_credit']is False)
 report=dict(schema='AXMAT_V12_COLD_CALLBACK_SCHEMA_AND_COMPLETE_SOURCE_INDEPENDENT_STATIC_REVIEW_V1',status='PASS_UNREADY_SOURCE_ONLY_NOT_EXECUTED',checked_unix=time.time(),candidate_factory=OBS[str(NEW/F)],frozen_factory=OBS[str(OLD/F)],unchanged_consumer=OBS[str(NEW/C)],unchanged_binding=OBS[str(NEW/B)],checks=CHECKS,complete_source_inverses=inverse_reports,complete_F_regions_to_V11=23,all55_factory_definitions_byteexact_to_Fee7=True,consumer27_definitions_byteexact_to_V11=True,generated_templates=templates_report,callback_metadata_schema=callback,generated_schema_matches_declare=True,factory_future_None_fields=nones(na),consumer_future_None_fields=nones(ca),binding_unknown_null_paths=nullpaths(nb),binding_source_authority_map_complete=True,observed_fresh_files=OBS,original_producer_source_receipt=originalreceipt,callback_fix_source_receipt=receipt,initial_pure_readonly_discovery_errors=[dict(chunk_id='00a91b',exit_code=1,reason='Reader attempted literal_eval of nonconstant CONTROLS source path AST; no source execution.'),dict(chunk_id='c22237',exit_code=1,reason='Reader attempted parse of indented constructor snippet without dedent; no source execution.')],findings=[],business_module_imported=False,business_API_or_CLI_called=False,fixtures_or_compilers_executed=False,Root_sessions_polled=False,project_writes=False,standalone_whole_INPUT_qualification_granted=False,new_declare_or_PREP_claimed=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,limitations=['Source-only repair fixes an actual generated callback schema identity mismatch; it does not execute declare or any template.','Authoritative future C then B then F bindings require the actual unique bounded host typed0, durable nine payload plus Root tenth member, and independent complete whole INPUT admission before source readiness.','Complete thirty-key genuine V11 sealed component counts are separately checked by parallel peer; no fixed guessed replacement dictionary is minted here.'])
 p=DEST/'REPORT.json';assert not p.exists();p.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n');pin,_=fresh(p);print(json.dumps(dict(status=report['status'],report=pin,checks=len(CHECKS),factory_definitions=55,generated_templates=len(templates_report),factory_None=len(nones(na)),consumer_None=len(nones(ca)),findings=[]),ensure_ascii=False))
if __name__=='__main__':main()
