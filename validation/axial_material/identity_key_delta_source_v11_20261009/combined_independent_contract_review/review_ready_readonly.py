import ast
import hashlib
import json
import os
from pathlib import Path

ROOT=Path('/Users/wen/spot')
DEST=Path('/private/tmp/axmat_v11_combined_independent_contract_review_20261009')
REVIEW=ROOT/'validation/axial_material/identity_key_delta_source_v11_20261009/combined_Root_source_admission'
P=REVIEW/'Root_READY_candidate_source_only_inverse_proof.json'
proof=json.loads(P.read_text())
candidate=Path(proof['candidate']['path'])
parent=Path('/private/tmp/axmat_v11_combined_actual_component_pins_unready_source_draft_20261009/prepare_historical_input_owned_specs_cross_group_identity_key_delta_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v11.UNREADY.py')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def funcs(t): return {n.name:ast.get_source_segment(t,n) for n in ast.walk(ast.parse(t)) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
ct=candidate.read_text();pt=parent.read_text();t=ct
assert sha(candidate)=='66d09b9c8a818e25c7c12acf10ba7551256d71f5fd60bde1c80da6d35d0d9481'
assert len(proof['ready_conversion_regions'])==2
assert [e['name'] for e in proof['ready_conversion_regions']]==['top_docstring','DRAFT_STATUS']
for e in reversed(proof['ready_conversion_regions']):
 assert t.count(e['new'])==1
 t=t.replace(e['new'],e['old'],1)
assert t==pt
assert funcs(ct)==funcs(pt) and len(funcs(ct))==70
assert "DRAFT_STATUS = 'READY_REVIEWED_TRIM_COMPONENT_INPUT_REUSE_FORMAL_FACTORY'" in ct
full_edits=json.loads((parent.parent/'complete_17_plus_6_region_edits.json').read_text())
for e in reversed(full_edits):
 assert t.count(e['new'])==1
 t=t.replace(e['new'],e['old'],1)
assert hashlib.sha256(t.encode()).hexdigest()=='711762b183d81189f4727e237f21e4c0aff30065bf7d58b0932c504fe2f39709'
ART=ROOT/'validation/artifacts'
OUT=ART/'axial-material-rank1-factor-cache-cross-group-identity-key-delta-build-v11-20261009'
SOURCE=ART/'axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-admission-v11-20261009'
TERM=ART/'axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-terminal-v11-20261009'
d=json.loads((OUT/'declaration.json').read_text());seal=json.loads((OUT/'seal.json').read_text());term=json.loads((TERM/'terminal_return.json').read_text())
assert d['schema']=='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_DECLARATION_V1'
assert d['family']=='RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_V11'
assert term['schema']=='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1'
assert type(term['returncode'])is int and term['returncode']==0
assert term['actual_tool_terminal_return_observed']is True and term['record_written_after_actual_terminal_return']is True
def inventory(root):
 files=set();links={};dirs=[]
 for current,sub,names in os.walk(root,followlinks=False):
  rel=Path(current).relative_to(root)
  if rel.parts: dirs.append(str(rel))
  for name in list(sub)+names:
   p=Path(current)/name;r=str(p.relative_to(root))
   if p.is_symlink():
    links[r]=os.readlink(p)
   elif p.is_file():files.add(r)
 return files,links,sorted(dirs)
of,ol,od=inventory(OUT)
assert of==set(seal['files'])|{'seal.json'} and not ol and od==seal['directories']
sf,sl,sd=inventory(SOURCE)
assert sf==set(d['source_inventory']['files']) and sl==d['source_inventory']['symlinks'] and sd==d['source_directories']
terminal_names=inventory(TERM)
report=dict(schema='AXMAT_V11_COMBINED_READY_CANDIDATE_INDEPENDENT_STATIC_REVIEW_V1',status='PASS_ROOT_READY_SOURCE_CONVERSION_ONLY',candidate=dict(path=str(candidate),sha256=sha(candidate)),parent=dict(path=str(parent),sha256=sha(parent)),actual_25_region_inverse_to711_verified=True,all70_function_bodies_retained=True,READY_conversion_exact_two_regions=True,obsolete_docstring_resolved=True,component_declaration_seal_source_and_terminal_schemas_match=True,actual_component_OUT_and_SOURCE_member_and_directory_sets_exact=True,actual_terminal_namespace=dict(file_count=len(terminal_names[0]),symlink_count=len(terminal_names[1]),directory_count=len(terminal_names[2])),initial_independent_review=dict(path=str(DEST/'REPORT.json'),sha256=sha(DEST/'REPORT.json')),new_combined_PREP_RUN_executed=False,new_combined_qualification_obtained=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,project_files_written=False,business_imports_or_execution=False)
(DEST/'READY_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],report=str(DEST/'READY_REPORT.json'),sha256=sha(DEST/'READY_REPORT.json')),ensure_ascii=False))
