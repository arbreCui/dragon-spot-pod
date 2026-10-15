"""Source-only bounded validation refinement; preserve the first draft bytes."""
import ast
import hashlib
import json
from pathlib import Path
D=Path(__file__).parent
P=D/'complete_input_graph_fresh_wire_canonical_and_trace_tables.UNREADY.py'
old=P.read_text()
prior='''    pending = [value]
    while pending:
        part = pending.pop()
        kind = type(part)
        if kind is dict:
            _require(all(type(key) is str for key in part), "trace nested JSON object keys must be strings")
            pending.extend(part.values())
        elif kind is list:
            pending.extend(part)
'''
replacement='''    pending = [(value, False)]
    active = set()
    while pending:
        part, exit_container = pending.pop()
        if exit_container:
            active.remove(id(part))
            continue
        kind = type(part)
        if kind in (dict, list):
            _require(id(part) not in active, "trace nested JSON container cycle")
            active.add(id(part))
            pending.append((part, True))
            if kind is dict:
                _require(all(type(key) is str for key in part), "trace nested JSON object keys must be strings")
                pending.extend((child, False) for child in reversed(list(part.values())))
            else:
                pending.extend((child, False) for child in reversed(part))
'''
assert old.count(prior)==1
new=old.replace(prior,replacement)
assert new.count(replacement)==1 and new.replace(replacement,prior)==old
compile(new,'complete_input_graph_fresh_wire_canonical_and_trace_tables.CANDIDATE.py','exec')
target=D/'complete_input_graph_fresh_wire_canonical_and_trace_tables.CANDIDATE.py'
with target.open('x')as f:f.write(new)
proof=dict(schema='AXMAT_TRACE_TABLE_NESTED_JSON_CYCLE_SOURCE_REFINEMENT_V1',status='UNREADY_SOURCE_ONLY',
    parent=dict(path=str(P),sha256=hashlib.sha256(old.encode()).hexdigest()),
    candidate=dict(path=str(target),sha256=hashlib.sha256(new.encode()).hexdigest()),
    edits=[dict(old=prior,new=replacement)],complete_inverse_equal=True,
    reason='Direct pure decoder must reject cyclic mutable mappings instead of looping; parsed JSON cannot contain cycles. Shared acyclic nested values remain allowed after exit marker.',
    syntax_compile_only=True,no_helper_or_fixture_or_business_executed=True)
with (D/'nested_json_cycle_source_refinement.json').open('x')as f:json.dump(proof,f,indent=2);f.write('\n')
print(json.dumps(proof,separators=(',',':')))
