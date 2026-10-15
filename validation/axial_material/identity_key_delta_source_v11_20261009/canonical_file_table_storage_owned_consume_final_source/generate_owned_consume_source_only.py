import ast
import difflib
import hashlib
import json
from pathlib import Path

D=Path('/private/tmp/axmat_complete_graph_canonical_file_table_owned_consume_source_draft_20261009')
BASE=Path('/private/tmp/axmat_complete_graph_canonical_file_table_storage_source_draft_20261009')
N='combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
old=(BASE/N).read_text()
def sha(raw):return hashlib.sha256(raw).hexdigest()
assert sha(old.encode())=='abb5aef91e6a2032c708c87a14fddf3a89e9798cf37d3e153233d8062c41920f'
tree=ast.parse(old);out=old;edits=[]
def replace(name,a,b):
 global out
 assert out.count(a)==1,(name,out.count(a));out=out.replace(a,b,1);edits.append(dict(name=name,old=a,new=b))
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='decode_canonical_file_table_storage')
a=ast.get_source_segment(old,node);b=a
b=b.replace('def decode_canonical_file_table_storage(storage):','def decode_canonical_file_table_storage(storage, *, _consume=False):',1)
b=b.replace('    Inputs are not modified. Restored canonical pin dicts are fresh and keep the',
 '    Default inputs are not modified. Private consume is used only on each strict\n    wrapper\'s new parsed container, clearing rows after complete scalar transfer.\n    Restored canonical pin dicts are fresh and keep the',1)
b=b.replace('    _require(type(storage) is dict and set(storage) == {"schema", "graph"}',
 '    _require(type(_consume) is bool, "invalid private canonical-file storage consume flag")\n    _require(type(storage) is dict and set(storage) == {"schema", "graph"}',1)
b=b.replace('    pins = []\n    for row in table["rows"]:\n        values = _canonical_file_storage_values(row)\n        pins.append({key: value for key, value in zip(CANONICAL_FILE_TABLE_STORAGE_COLUMNS, values)})',
 '    pins = []\n    rows = table["rows"]\n    for index, row in enumerate(rows):\n        values = _canonical_file_storage_values(row)\n        pins.append({key: value for key, value in zip(CANONICAL_FILE_TABLE_STORAGE_COLUMNS, values)})\n        if _consume:\n            rows[index] = None\n    if _consume:\n        rows.clear()\n    del rows\n    if pins:\n        del row, values',1)
assert a!=b
replace('private_consuming_decoder',a,b)
for name in ('strict_json','_parse_strict_json_payload'):
 node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
 a=ast.get_source_segment(old,node);b=a.replace('return decode_canonical_file_table_storage(result)','return decode_canonical_file_table_storage(result, _consume=True)',1)
 assert a!=b;replace(name+'_consume_owned_new_parse_only',a,b)
inverse=out
for row in reversed(edits):assert inverse.count(row['new'])==1;inverse=inverse.replace(row['new'],row['old'],1)
assert inverse==old
first=json.loads((BASE/'source_region_edits.json').read_text());assert len(first)==5
all_inverse=inverse
for row in reversed(first):assert all_inverse.count(row['new'])==1;all_inverse=all_inverse.replace(row['new'],row['old'],1)
parent=Path('/Users/wen/spot/validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py')
assert all_inverse==parent.read_text() and sha(all_inverse.encode())=='1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643'
of={n.name:ast.get_source_segment(old,n) for n in tree.body if isinstance(n,ast.FunctionDef)}
nf={n.name:ast.get_source_segment(out,n) for n in ast.parse(out).body if isinstance(n,ast.FunctionDef)}
changed=[name for name in of if of[name]!=nf[name]]
assert set(changed)=={'decode_canonical_file_table_storage','strict_json','_parse_strict_json_payload'}
assert len(of)==len(nf)==72
assert of['encode_canonical_file_table_storage']==nf['encode_canonical_file_table_storage']
(D/N).write_text(out)
(D/'owned_consume_region_edits.json').write_text(json.dumps(edits,indent=2)+'\n')
(D/'complete_5_plus_3_source_region_edits.json').write_text(json.dumps(first+edits,indent=2)+'\n')
(D/'owned_consume.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),out.splitlines(True),fromfile=str(BASE/N),tofile=str(D/N))))
proof=dict(schema='AXMAT_COMPLETE_GRAPH_TABLE_OWNED_CONSUME_SOURCE_INVERSE_V1',status='UNREADY_SOURCE_ONLY',parent_abb5=dict(path=str(BASE/N),sha256=sha(old.encode())),original_1d7=dict(path=str(parent),sha256=sha(all_inverse.encode())),candidate=dict(path=str(D/N),sha256=sha(out.encode())),three_region_inverse_to_abb5_byteexact=True,eight_region_inverse_to_1d7_byteexact=True,changed_functions_vs_abb5=changed,other_69_functions_vs_abb5_byteexact=True,original_67_functions_parse_text_verify_graph_phase_lineage_math_byteexact_to_1d7=True,encoder_default_and_schema_columns_content_and_all_limits_byteexact_to_abb5=True,private_consume_default_false=True,two_strict_wrappers_true_only_after_their_own_new_parse=True,business_executed=False,project_written=False,native_RSS_qualified=False)
(D/'source_inverse_proof.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(dict(status=proof['status'],source_sha256=sha(out.encode()),new_regions=3,all_regions=8,changed=changed)))
