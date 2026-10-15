import ast
import difflib
import hashlib
import json
from pathlib import Path

D=Path('/private/tmp/axmat_complete_graph_canonical_file_table_storage_source_draft_20261009')
P=Path('/Users/wen/spot/validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py')
N='combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
def sha(raw):return hashlib.sha256(raw).hexdigest()
parent=P.read_text();assert sha(parent.encode())=='1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643'
tree=ast.parse(parent);out=parent;edits=[]
def replace(name,a,b):
 global out
 assert out.count(a)==1,(name,out.count(a));out=out.replace(a,b,1);edits.append(dict(name=name,old=a,new=b))
doc=ast.get_source_segment(parent,tree.body[0])
replace('unready_source_only_docstring',doc,'"""UNREADY source-only complete graph canonical-file table storage helper.\n\nThe complete original graph values, canonical row sequence, requirements,\nowner/ns/alias/absence/trace scopes and original decoded content SHA survive\nexplicit fixed-column storage. Ordinary JSON and all original fresh-byte,\nverification and resource gates retain their original behavior. Both strict\nJSON wrappers decode the new exact storage schema after the original parse.\nNo business, native RSS, cold AAA or ABA admission is granted by this source.\n"""')
constants='''GRAPH_STORAGE_SOURCE_STATUS = "UNREADY_SOURCE_ONLY_PENDING_ROOT_REVIEW"
CANONICAL_FILE_TABLE_STORAGE_SCHEMA = "AXMAT_COMPLETE_INPUT_GRAPH_CANONICAL_FILE_TABLE_STORAGE_V1"
CANONICAL_FILE_TABLE_STORAGE_COLUMNS = ("path", "sha256", "size_bytes")

'''
replace('explicit_storage_constants','MAX_JSON_BYTES = 64 * 1024 * 1024',constants+'MAX_JSON_BYTES = 64 * 1024 * 1024')
codec='''def _canonical_file_storage_values(values):
    """Validate exactly the original three scalar pin values, never observe files."""
    _require(type(values) is list and len(values) == len(CANONICAL_FILE_TABLE_STORAGE_COLUMNS),
             "invalid canonical-file storage row shape")
    _require(type(values[0]) is str and type(values[1]) is str
             and type(values[2]) is int and values[2] >= 0,
             "invalid canonical-file storage row scalar types")
    _path(values[0])
    _sha(values[1])
    return values


def encode_canonical_file_table_storage(graph):
    """Return an explicit table view without modifying the caller's complete graph.

    Other graph values are borrowed unchanged. Each canonical pin becomes a new
    list of the same immutable scalars. Nothing is sorted, deduplicated or lost.
    This codec never reads files or claims a byte/resource/science admission.
    """
    _require(type(graph) is dict and graph.get("schema") == WIRE_GRAPH_SCHEMA
             and graph.get("scope") == INPUT_SCOPE,
             "canonical-file storage requires the complete original wire graph")
    original = graph.get("canonical_files")
    _require(type(original) is list, "canonical-file storage input must be a complete list")
    rows = []
    for pin in original:
        _require(type(pin) is dict and tuple(pin) == CANONICAL_FILE_TABLE_STORAGE_COLUMNS,
                 "canonical-file storage pin fields/order differ")
        rows.append(_canonical_file_storage_values([pin[key] for key in CANONICAL_FILE_TABLE_STORAGE_COLUMNS]))
    _require(_sha(graph.get("content_sha256")) == _content_digest(graph),
             "original graph content changed before storage encoding")
    view = dict(graph)
    view["canonical_files"] = {"columns": list(CANONICAL_FILE_TABLE_STORAGE_COLUMNS), "rows": rows}
    return {"schema": CANONICAL_FILE_TABLE_STORAGE_SCHEMA, "graph": view}


def decode_canonical_file_table_storage(storage):
    """Restore the whole original graph from one exact transparent table schema.

    Inputs are not modified. Restored canonical pin dicts are fresh and keep the
    original path/sha256/size_bytes order. Other complete graph values survive.
    Content SHA verification detects omitted, added or changed rows/fields.
    Fresh-file/math/resource eligibility remains the original caller's job.
    """
    _require(type(storage) is dict and set(storage) == {"schema", "graph"}
             and storage.get("schema") == CANONICAL_FILE_TABLE_STORAGE_SCHEMA,
             "invalid complete graph storage header")
    graph = storage["graph"]
    _require(type(graph) is dict and graph.get("schema") == WIRE_GRAPH_SCHEMA
             and graph.get("scope") == INPUT_SCOPE,
             "invalid original decoded graph schema/scope")
    table = graph.get("canonical_files")
    _require(type(table) is dict and set(table) == {"columns", "rows"}
             and type(table["columns"]) is list
             and table["columns"] == list(CANONICAL_FILE_TABLE_STORAGE_COLUMNS)
             and type(table["rows"]) is list,
             "invalid canonical-file table header/columns")
    pins = []
    for row in table["rows"]:
        values = _canonical_file_storage_values(row)
        pins.append({key: value for key, value in zip(CANONICAL_FILE_TABLE_STORAGE_COLUMNS, values)})
    restored = dict(graph)
    restored["canonical_files"] = pins
    _require(_sha(restored.get("content_sha256")) == _content_digest(restored),
             "decoded complete graph content changed")
    return restored


'''
replace('three_pure_storage_functions','def strict_json(path, expected_sha256=None, *, aliases=(), max_bytes=MAX_JSON_BYTES):',codec+'def strict_json(path, expected_sha256=None, *, aliases=(), max_bytes=MAX_JSON_BYTES):')
for name in ('strict_json','_parse_strict_json_payload'):
 node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
 a=ast.get_source_segment(parent,node);b=a.replace('    return _parse_strict_json_text(decoded, path)',
  '    result = _parse_strict_json_text(decoded, path)\n    del decoded\n    if type(result) is dict and result.get("schema") == CANONICAL_FILE_TABLE_STORAGE_SCHEMA:\n        return decode_canonical_file_table_storage(result)\n    return result')
 assert a!=b
 replace(name+'_parse_then_decode_exact_storage_schema',a,b)
inverse=out
for row in reversed(edits):
 assert inverse.count(row['new'])==1,row['name'];inverse=inverse.replace(row['new'],row['old'],1)
assert inverse==parent
ot=ast.parse(out)
pf={n.name:ast.get_source_segment(parent,n) for n in tree.body if isinstance(n,ast.FunctionDef)}
nf={n.name:ast.get_source_segment(out,n) for n in ot.body if isinstance(n,ast.FunctionDef)}
added=set(nf)-set(pf);changed=[n for n in pf if pf[n]!=nf[n]]
assert added=={'_canonical_file_storage_values','encode_canonical_file_table_storage','decode_canonical_file_table_storage'}
assert changed==['strict_json','_parse_strict_json_payload']
for name in ('verify_graph','_phase','_consumer_lineage','_parse_strict_json_text','_content_digest','_wire_semantic_content_digest','create_graph','create_wire_graph'):
 assert pf[name]==nf[name]
assert P.read_text()==parent
(D/N).write_text(out)
(D/'source_region_edits.json').write_text(json.dumps(edits,indent=2)+'\n')
(D/'source.diff').write_text(''.join(difflib.unified_diff(parent.splitlines(True),out.splitlines(True),fromfile=str(P),tofile=str(D/N))))
(D/'source_inverse_proof.json').write_text(json.dumps(dict(schema='AXMAT_COMPLETE_GRAPH_STORAGE_HELPER_COMPLETE_SOURCE_INVERSE_V1',status='UNREADY_SOURCE_ONLY',parent=dict(path=str(P),sha256=sha(parent.encode())),candidate=dict(path=str(D/N),sha256=sha(out.encode())),complete_byte_inverse=True,region_count=len(edits),original_top_function_count=len(pf),added_top_functions=sorted(added),changed_original_functions=changed,unchanged_original_functions=[dict(name=n,sha256=sha(pf[n].encode())) for n in pf if n not in changed],MAX_JSON_BYTES_original_67108864=True,original_parse_text_verify_graph_phase_lineage_math_fullbytes_and_limits_byteexact=True,ordinary_JSON_return_semantics_and_error_order_retained=True,no_graph_field_row_owner_scope_or_trace_filter=True,business_executed=False,compiled=False,project_written=False),indent=2)+'\n')
print(json.dumps(dict(status='UNREADY_SOURCE_ONLY',candidate_sha256=sha(out.encode()),regions=len(edits),original_functions=len(pf),added=sorted(added),changed=changed)))
