from pathlib import Path
import ast,difflib,hashlib,json
BASE=Path('/private/tmp/axmat-requirements-varint-wire-compact-phase-source-draft-20261009')
PARENT=Path('/Users/wen/spot/validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_owned_phase_owner_lifetimes_20261009.py')
CANDIDATE=BASE/'combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(PARENT)=='85551979317309cfa70bb27a4b0e04ae908bbd33865dc3edfbe6c7f4d70baf6c'
old=PARENT.read_text(); new=old; regions=[]
def replace(before,after,label):
 global new
 assert new.count(before)==1,(label,new.count(before))
 new=new.replace(before,after,1);regions.append(dict(label=label,original=before,replacement=after))
replace('import copy\n','import copy\nimport base64\nimport binascii\n','two-standard-library-codec-imports')
replace('\ndef _owner_table(owners, requirements):','\n'+(BASE/'wire_helpers_snippet.py').read_text()+'\n\ndef _owner_table(owners, requirements):','explicit-wire-codec-and-private-tuple-helpers')
replace('json_input=None, release_owned_owners=False):','json_input=None, release_owned_owners=False, compact_requirements=False):','private-phase-optional-flag-default-false')
replace('''        requirements.append({"path": path, "canonical_path": canonical,
                             "owner": owner, "category": category, "binding_role": role})''','''        if compact_requirements:
            requirements.append((path, canonical, owner, category, role))
        else:
            requirements.append({"path": path, "canonical_path": canonical,
                                 "owner": owner, "category": category, "binding_role": role})''','complete-phase-tuple-storage-only')
replace('    canonical_paths = {record["canonical_path"] for record in requirements}','    canonical_paths = ({record[1] for record in requirements} if compact_requirements\n                       else {record["canonical_path"] for record in requirements})','phase-canonical-set-retains-every-record')
replace('''    _require(isinstance(graph, Mapping) and graph.get("schema") in (SCHEMA, CONSUMER_SCHEMA) and graph.get("scope") == INPUT_SCOPE,
             "unknown or non-input graph schema")
    consumer = None''','''    _require(isinstance(graph, Mapping) and graph.get("schema") in (SCHEMA, CONSUMER_SCHEMA, WIRE_GRAPH_SCHEMA) and graph.get("scope") == INPUT_SCOPE,
             "unknown or non-input graph schema")
    wire = graph["schema"] == WIRE_GRAPH_SCHEMA
    consumer = None''','explicit-new-global-wire-schema')
replace('''    _require(_sha(graph.get("content_sha256")) == _content_digest(graph), "input graph content changed")
    _validate_requirement_table(graph["requirements"])
    owners = _owners''','''    _require(_sha(graph.get("content_sha256")) == _content_digest(graph), "input graph content changed")
    if wire:
        encoding = _wire_encoding_contract(graph)
        _validate_wire_requirement_table(graph["requirements"])
        _require(_wire_semantic_content_digest(graph) == encoding["decoded_content_sha256"],
                 "wire graph decoded semantic content changed")
    else:
        _validate_requirement_table(graph["requirements"])
    owners = _owners''','new-wire-layout-and-semantic-digest-before-original-owner-gates')
replace('''                                           release_owned_owners=consumer is None)
    if consumer is not None:''','''                                           release_owned_owners=consumer is None,
                                           compact_requirements=wire)
    if consumer is not None:''','wire-only-private-phase-flag')
replace('''    _require(_requirement_table(requirements) == graph["requirements"],
             "complete typed owner/canonical path requirement table changed")''','''    rebuilt_requirements = (_wire_requirement_table_compact(requirements) if wire
                            else _requirement_table(requirements))
    _require(rebuilt_requirements == graph["requirements"],
             "complete typed owner/canonical path requirement table changed")
    del rebuilt_requirements''','complete-table-rebuild-without-full-wire-integer-matrix')
replace('''    coverage = (_coverage if consumer is None else _consumer_coverage)(requirements, actual, graph["coverage_requirements"])''','''    coverage = (_coverage if consumer is None else _consumer_coverage)(
        _compact_requirement_dicts(requirements) if wire else requirements,
        actual, graph["coverage_requirements"])''','unchanged-coverage-body-fed-real-ephemeral-dicts')
replace('''    trace_coverage = _trace_coverage(_trace_records(graph["read_trace"]["records"] if consumer is not None else graph["read_trace"]), requirements, namespaces, aliases,''','''    trace_coverage = _trace_coverage(_trace_records(graph["read_trace"]["records"] if consumer is not None else graph["read_trace"]),
                                    _compact_requirement_dicts(requirements) if wire else requirements,
                                    namespaces, aliases,''','unchanged-trace-coverage-body-fed-real-ephemeral-dicts')
assert not CANDIDATE.exists(); CANDIDATE.write_text(new)
inverse=new
for r in reversed(regions):
 assert inverse.count(r['replacement'])==1,r['label']
 inverse=inverse.replace(r['replacement'],r['original'],1)
assert inverse.encode()==PARENT.read_bytes()
ot,nt=ast.parse(old),ast.parse(new)
defs=lambda text,tree:{n.name:ast.get_source_segment(text,n)for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
od,nd=defs(old,ot),defs(new,nt)
changed=sorted(k for k in od if od[k]!=nd[k]);added=sorted(set(nd)-set(od))
assert changed==['_phase','verify_graph'],changed
assert od['create_graph']==nd['create_graph'] and od['_requirement_table']==nd['_requirement_table']
assert od['_validate_requirement_table']==nd['_validate_requirement_table']
pin=lambda p:dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size)
proof=dict(schema='AXMAT_COMPLETE_WIRE_COMPACT_PHASE_SOURCE_INVERSE_V1',parent=pin(PARENT),candidate=pin(CANDIDATE),regions=regions,complete_inverse_byte_exact=True,
 original_changed_definitions=changed,added_definitions=added,all_other_original_definitions_byte_exact=True,public_create_graph_and_requirement_table_and_validator_byte_exact=True,
 ordinary_phase_default_compact_flag_false=True,no_business_import_API_constructor_PREP_RUN_ART_or_formal_source_write=True)
(BASE/'source_inverse.json').write_text(json.dumps(proof,indent=2,sort_keys=True)+'\n')
(BASE/'full.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=str(PARENT),tofile=str(CANDIDATE))))
print(json.dumps(dict(candidate=pin(CANDIDATE),inverse=pin(BASE/'source_inverse.json'),changed=changed,added=added,complete_inverse=True)))
