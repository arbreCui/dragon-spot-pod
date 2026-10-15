import hashlib,json,stat
from pathlib import Path
ROOT=Path('/private/tmp/spot_v25_monitor_access_complete_PREP_SOURCE_ROOT_20261010')
OLD=Path('/private/tmp/axmat_v25_actual_bound_complete_PREP_independent_Source_review_h77n7fjk')
OUT=Path('/private/tmp/axmat_v25_monitor_access_directory_Source_independent_review_UNREADY_k67d42sg')
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=identity(p);assert stat.S_ISREG(i[2]) and i[3]==1
 with p.open('rb') as f:d=hashlib.file_digest(f,'sha256').hexdigest()
 assert identity(p)==i
 return dict(path=str(p),sha256=d,size_bytes=i[4],identity=i)
inv=json.loads((ROOT/'Root_complete_namespace_only_Source_inverse.json').read_bytes())
v=dict(schema='ROOT_V25_MONITOR_ACCESS_ACTUAL_DIRECTORY_SOURCE_REVIEW_INPUTS_V1',status='ACTUAL_SOURCE_DERIVATION_CLOSED_ONLY_NO_BUSINESS_EXECUTION',source_only=True,
 actual_derived_Source_manifest_pin=pin(ROOT/'MANIFEST.json'),
 actual_derived_Source_inverse_pin=pin(ROOT/'Root_complete_namespace_only_Source_inverse.json'),
 actual_Source_author_tool_return_pin=pin(ROOT/'Root_actual_namespace_Source_derivation_tool_return.json'),
 actual_Source_seal_tool_return_pin=pin(Path(str(ROOT)+'_seal_receipt')/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),
 prior_complete_bound_Source_peer_report_pin=pin(OLD/'REVIEW.json'),
 prior_complete_bound_Source_peer_manifest_pin=pin(OLD/'MANIFEST.json'),
 prior_complete_bound_Source_peer_seal_pin=pin(Path(str(OLD)+'_seal_receipt')/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),
 actual_derived_role_Source_pins={k:pin(Path(r['derived']['path'])) for k,r in inv['roles'].items()},
 actual_new_PREP_terminal=None,actual_new_PREP_summary=None,actual_new_BUILD_terminal=None)
assert v['actual_derived_Source_manifest_pin']['sha256']=='5f35e6913e8e86965bb84abbf15dc45f3302e8881fa211a7cfc26ddfe6b1e01a'
assert v['actual_derived_Source_inverse_pin']['sha256']=='d8193a116b2496a876e5f19d54842f4b4946cab57c18fc897292f40ae5cff6bd'
p=OUT/'ACTUAL_CLOSED_SOURCE_INPUTS.json'
with p.open('x') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(actual_inputs_pin=pin(p),reviewer_pin=pin(OUT/'review_directory_isolation_Source_stdlib.UNREADY.py'),source_only=True,new_PREP_build_or_science_executed=False)))
