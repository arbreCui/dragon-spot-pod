"""Stdlib-only stopped source identity/whole inverse check. Writes nothing."""
import ast,hashlib,json,os,sys
from pathlib import Path
if sys.flags.optimize!=0 or 'PYTHONOPTIMIZE'in os.environ:raise ValueError('pure checker requires optimize0')
D=Path('/private/tmp/axmat-cold-owned-specs-input-intake-path-stable-draft-20261007')
EXPECTED={
'prepare_historical_input_owned_specs_physical_dedup_file_snapshot_cold_AAA_full_draft_20261007.py':'6bd3a92cad22372de5fedb1439b73d9bf5461052b368c228d0bf79530a427bbc',
'cold_component_input_consumer.py':'81ceb9daac17747a35c8d874226f47ac5b459ea888df4e2948b229f9bd71bc76',
'full_33cd_source_inverse.json':'31131242767af932cc653688c8fc5a0b45003a805bb1ff5628d1ae03fb0b3843'}
for name,wanted in EXPECTED.items():
 raw=(D/name).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=wanted:raise ValueError('stopped source/proof changed: '+name)
 if name.endswith('.py'):ast.parse(raw)
proof=json.loads((D/'full_33cd_source_inverse.json').read_bytes())
candidate=Path(proof['candidate']['path']).read_text()
for row in reversed(proof['inverse_regions']):
 if candidate.count(row['candidate'])!=1:raise ValueError('inverse region is ambiguous')
 candidate=candidate.replace(row['candidate'],row['original'],1)
raw=Path(proof['original']['path']).read_bytes()
if hashlib.sha256(raw).hexdigest()!=proof['original']['sha256']or candidate.encode()!=raw:
 raise ValueError('whole inverse did not restore frozen33cd')
print(json.dumps(dict(status='PASS_STOPPED_SOURCE_INVERSE_ONLY',hashes=EXPECTED,regions=len(proof['inverse_regions']),
 project_import=False,API=False,constructor=False,native=False,ART_write=False)))
