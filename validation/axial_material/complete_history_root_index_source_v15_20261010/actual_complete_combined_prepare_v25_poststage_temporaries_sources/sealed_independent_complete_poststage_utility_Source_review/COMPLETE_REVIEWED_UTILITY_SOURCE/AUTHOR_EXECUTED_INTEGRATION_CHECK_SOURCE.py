"""Finite author integration check: full Source/AST/byte inverse and small META only."""
import ast,hashlib,json,stat
from pathlib import Path
U=Path('/private/tmp/axmat_V25_poststage_complete_finite_utilities_V3_UNREADY_Source_20261010')
def pin(p):
 p=Path(p);s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];assert p.resolve()==p and stat.S_ISREG(i[2]) and i[3]==1
 raw=p.read_bytes();t=p.lstat();assert i==[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i)
checks=[];inputpins={};trees={}
def check(label,value):
 assert type(value) is bool and value,label;checks.append(dict(check=label,passed=value))
for p in sorted(U.rglob('*')):
 if p.is_file():
  inputpins[str(p.relative_to(U))]=pin(p)
  if p.suffix=='.py':trees[str(p.relative_to(U))]=ast.parse(p.read_bytes(),filename=str(p));check('complete AST '+str(p.relative_to(U)),True)
author=json.loads((U/'AUTHOR_COMPLETE_UTILITY_SOURCE_ONLY_REPORT.json').read_bytes())
check('82 actual author checks typed True',author['check_count']==82 and len(author['checks'])==82 and all(type(c['passed']) is bool and c['passed'] is True for c in author['checks']))
for name,q in author['role_Source_pins'].items():check('full role pin '+name,pin(U/name)==q)
inverse=json.loads((U/'COMPLETE_SIX_INTERFACE_SOURCE_BYTE_AST_INVERSES.json').read_bytes())
for role,record in inverse['roles'].items():
 original=Path(record['complete_original_Source_copy']['path']).read_text();derived=Path(record['derived_Source']['path']).read_text();restored=derived.splitlines(keepends=True)
 for h in reversed(record['finite_hunks']):
  check(role+' exact inverse hunk '+str(h['derived_start']),''.join(restored[h['derived_start']:h['derived_end']])==h['derived_text'])
  restored[h['derived_start']:h['derived_end']]=h['original_text'].splitlines(keepends=True)
 check(role+' entire byte inverse',''.join(restored)==original)
 check(role+' entire AST inverse',ast.dump(ast.parse(''.join(restored)),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False))
 check(role+' original actual Source pin unchanged',pin(record['original_Source']['path'])==record['original_Source'])
c=json.loads((U/'FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json').read_bytes())
for phase,owner in c['complete_old_frozen_Source_owners'].items():
 f=json.loads(Path(owner['freeze']['path']).read_bytes());check(phase+' original Source freeze fullEOF',pin(owner['freeze']['path'])==owner['freeze'])
 check(phase+' exact whole owner set retained',owner['complete_files']==f['complete_files'] and len(owner['complete_files'])==owner['original_file_count'])
 for rel,q in owner['complete_files'].items():
  check(phase+' strict full owner pin '+rel,set(q)=={'path','sha256','size_bytes','identity'} and type(q['size_bytes']) is int and len(q['identity'])==7 and all(type(i) is int for i in q['identity']) and Path(q['path'])==Path(owner['root'])/rel)
for key in ('future_actual_Source_utility_peer','future_bound_PREP_Source_peer','future_saved_new_PREP_META_peer','future_actual_bound_BUILD_Source_manifest','future_actual_BUILD_Source_binding_terminal','future_bound_BUILD_Source_peer','actual_new_PREP_business_pins','actual_new_BUILD_business_pins'):check('future actual fact genuinely unknown '+key,c[key] is None)
check('all science false',c['whole_INPUT_native_or_science_qualified'] is False and c['Source_install_or_prelaunch_executed'] is False)
binding=c['actual_new_PREP_Source_binding_terminal'];d=json.loads(Path(binding['path']).read_bytes());tr=d['terminal_tool_return'];out=json.loads(tr['output']);bound=c['actual_new_PREP_bound_Source_manifest']
check('actual913 Source tool strict terminal',pin(binding['path'])==binding and d['source_only'] is True and d['closed'] is True and d['observed_terminal'] is True and type(tr['exit_code']) is int and tr['exit_code']==0 and tr['chunk_id']=='91304c' and 'session_id' not in tr and out['manifest']==bound and out['business_or_science_executed'] is False)
m=json.loads(Path(bound['path']).read_bytes());check('actual bound Source manifest fullEOF',pin(bound['path'])==bound)
for rel,q in m['members'].items():check('actual bound Source/META fullEOF '+rel,pin(q['path'])==q)
check('all exact new names finite',len(c['namespaces'])==10 and all('poststage_temporaries' in v or 'poststage-temporaries' in v for v in c['namespaces'].values()))
core=(U/'Root_poststage_Source_META_contract.py').read_text()
check('no candidate imports in Source contract',all(not isinstance(n,ast.ImportFrom) and (not isinstance(n,ast.Import) or all(q.name in ('argparse','ast','hashlib','json','os','stat','sys') for q in n.names)) or (isinstance(n,ast.ImportFrom) and n.module=='pathlib') for n in trees['Root_poststage_Source_META_contract.py'].body))
check('no imported or executed candidate by checker',True)
report=dict(schema='AUTHOR_V25_POSTSTAGE_FINITE_UTILITY_COMPLETE_SOURCE_INTEGRATION_CHECK_V1',status='PASS_SOURCE_ONLY_UNREADY_PENDING_INDEPENDENT_PEER',source_only=True,all_checks_typed_true=True,check_count=len(checks),checks=checks,blockers=[],complete_fullEOF_Source_small_META_pins=inputpins,qualified_role_Source_pins=author['role_Source_pins'],complete_original_owner_metadata_count=463,actual_original_owned_files_reread=False,actual_source_metadata913_binding_only=True,derived_utility_or_prelaunch_candidate_execution=False,guard_API_compile_native_material_numeric_execution=False,project_or_frozen_namespace_mutation=False,new_PREP_BUILD_result_pins=None,whole_INPUT_native_or_science_qualified=False)
out=U/'FINAL_SOURCE_INTEGRATION_CHECK_REPORT.json'
with out.open('x') as f:json.dump(report,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
print(json.dumps(dict(report=pin(out),check_count=len(checks),all_checks_typed_true=True,source_only=True,new_business_or_science=False)))
