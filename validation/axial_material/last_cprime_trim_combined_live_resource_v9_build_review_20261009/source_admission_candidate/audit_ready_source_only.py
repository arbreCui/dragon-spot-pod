"""Static fresh admission-candidate audit; no factory, recorder or business execution."""
import ast
import hashlib
import json
import os
from pathlib import Path

assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
P=Path('/private/tmp/axmat_last_cprime_trim_v9_identity_source_draft_20261009')
O=Path('/private/tmp/axmat_last_cprime_trim_v9_ready_source_admission_candidate_20261009')
T=Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v9-root-execution-20261009')
N='prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v9.py'
def sha(path):
 return hashlib.sha256(Path(path).read_bytes()).hexdigest()
assert sha(P/N)=='f700f43b411904f002a59cddcd879e1aa4e92fa632417e7be0bd7292fbc32ada'
assert sha(O/N)=='44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46'
mother=(P/N).read_text();candidate=(O/N).read_text()
inverse=json.loads((O/'ready_vs_f700_complete_byte_inverse.json').read_text())
assert len(inverse['operations'])==2
restored=candidate
for op in reversed(inverse['operations']):
 assert restored[op['candidate_start']:op['candidate_end']]==op['candidate_text']
 restored=restored[:op['candidate_start']]+op['mother_text']+restored[op['candidate_end']:]
assert restored.encode()==mother.encode()
A=ast.parse(mother);B=ast.parse(candidate)
compile(candidate,str(O/N),'exec')
def is_status(node):
 return isinstance(node,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='DRAFT_STATUS' for x in node.targets)
assert ast.literal_eval(next(x.value for x in B.body if is_status(x)))=='READY_REVIEWED_TRIM_COMPONENT_INPUT_REUSE_FORMAL_FACTORY'
def unchanged(tree):
 return [ast.dump(x,include_attributes=False) for x in tree.body[1:] if not is_status(x)]
assert unchanged(A)==unchanged(B)
fa={x.name:x for x in A.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))}
fb={x.name:x for x in B.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))}
assert len(fa)==len(fb)==65 and list(fa)==list(fb)
def source(text,node):
 return ''.join(text.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
for name,node in fa.items():
 assert source(mother,node)==source(candidate,fb[name])
 assert ast.dump(node,include_attributes=False)==ast.dump(fb[name],include_attributes=False)
F8=Path('/Users/wen/spot/validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v8.py')
assert sha(F8)=='4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4'
f8=F8.read_text();f8_parser=next(x for x in ast.parse(f8).body if isinstance(x,ast.FunctionDef) and x.name=='strict_json_bytes')
assert source(f8,f8_parser)==source(candidate,fb['strict_json_bytes'])
gate=source(candidate,fb['require_ready'])
assert "if Path(__file__).absolute()!=FORMAL_FACTORY:" in gate and "raise ValueError('TMP draft cannot perform a business action')" in gate
assert sha(O/'record_root_terminal.py')==sha(P/'record_root_terminal.py')==sha(T/'record_root_terminal.py')=='b534c49f046d3869dba07e4101e907bd08de8c61599bc3a05a688a0733de5d9e'
assert sha(O/'config.json')==sha(T/'config.json')=='afc40f7a08839839eb724b8a3c6722f66f5d07cf71129a032ac065c0b7be634e'
c=json.loads((O/'config.json').read_text());old=json.loads((P/'config.json').read_text())
future=('declarationSha','prepSha','sealSha','terminalSha','terminalPath','failed_terminal_sha')
assert all(c[k] is None for k in future) and c['factorySha']==sha(O/N)
assert {k:v for k,v in c.items() if k not in ('factorySha','source_review_status')}=={k:v for k,v in old.items() if k not in ('factorySha','source_review_status')}
assert sorted(x.name for x in T.iterdir())==['config.json','record_root_terminal.py']
for k in ('F','R','SOURCE','OUT','TERM'):
 assert not Path(c[k]).exists() and not Path(c[k]).is_symlink()
guards=json.loads((O/'prepared_path_guards_and_source_before_after_pins.json').read_text())
assert guards['source_before']==guards['source_after']
for p in guards['source_before']:
 assert sha(p['path'])==p['sha256']
assert guards['source_before'][3]['sha256']=='fd3bdb5543044fc71f0acb9799b1c6fcf7709cbbf22342f0931a299af59cee19'
assert guards['source_before'][4]['sha256']=='1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643'
print(json.dumps(dict(status='PASS_READY_SOURCE_ONLY_FRESH_STATIC_ADMISSION_AUDIT',source_sha256=sha(O/N),config_sha256=sha(O/'config.json'),inverse_two_regions=True,all_65_defs_source_AST_exact=True,original_F8_strict_json_bytes_exact=True,formal_helper_source_pin_verified=True,six_future_fields_None=True,formal_and_ART_outputs_absent=True,factory_recorder_or_business_executed=False)))
