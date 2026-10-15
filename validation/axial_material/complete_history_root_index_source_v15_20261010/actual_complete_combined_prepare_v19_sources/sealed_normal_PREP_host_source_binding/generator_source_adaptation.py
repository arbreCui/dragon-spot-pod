"""Finite SOURCE-only adaptation of Root V18 normal PREP host generator."""
import ast
import hashlib
import json
from pathlib import Path

P=Path('/private/tmp/axmat_v18_root_prepare_host_source_20261010/generate_prepare_host.py')
D=Path('/private/tmp/axmat_v19_normal_PREP_host_source_binding_20261010')
D.mkdir()
old=P.read_text()
text=old
edits=[]
def replace(before,after,count=1):
    global text
    assert text.count(before)==count,before[:100]
    text=text.replace(before,after)
    edits.append(dict(old=before,new=after,occurrences=count))
replace('Finite source retarget of the genuine V17 normal complete PREP host.','Finite source retarget of the frozen genuine V18 normal complete PREP host.')
replace("PARENT = BASE/'actual_complete_combined_prepare_v17_sources/combined_prepare_host.py'",
"PARENT = BASE/'actual_complete_combined_prepare_v18_sources/combined_prepare_host.py'")
replace("PARENT_SHA = '37d432b8c91ddec6816fed6f7cea11fbfcba7071655ea64bc0f3c562288185d3'",
"PARENT_SHA = 'bc5c6fa1118b84641a5a66232080354074b49ad2c59ac809e28ee99cc6faac98'")
replace("UNREADY = BASE/'next_complete_combined_v18_source_only_review/sealed_complete_UNREADY_candidate/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.UNREADY.py'",
"UNREADY = Path('/private/tmp/axmat_v19_complete_prepare_caller_last_use_source_only_20261010/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.UNREADY.py')")
replace("UNREADY_SHA = 'ecfdff36d99aa7ea6be8fdf592e3d9ff5018b8c6aeb7604f1ef00dda1ddc3583'",
"UNREADY_SHA = '585e450c5eb5d8748ff7dedfab28ddcf6163d89ca90f3cdeb5c9095ac93eed50'")
replace("SOURCE_ARCHIVE = BASE/'actual_complete_combined_prepare_v18_sources'",
"SOURCE_ARCHIVE = BASE/'actual_complete_combined_prepare_v19_sources'")
replace('READY_REVIEWED_V18_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY',
'READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY')
before=text[text.index('    changes = ['):text.index('    records = []')]
after=before
old_pairs=[
('axial-material-complete-combined-prepare-host-v17-20261010','axial-material-complete-combined-prepare-host-v18-20261010','axial-material-complete-combined-prepare-host-v19-20261010'),
('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py'),
('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v17-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v18-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v19-20261010'),
('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v17-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v18-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v19-20261010'),
('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v17-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v18-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v19-20261010'),
('actual_complete_combined_prepare_v17_sources','actual_complete_combined_prepare_v18_sources','actual_complete_combined_prepare_v19_sources'),
('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V17_DECLARATION_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V18_DECLARATION_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V19_DECLARATION_V1'),
('AXMAT_V17_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1','AXMAT_V18_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1','AXMAT_V19_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1')]
for a,b,c in old_pairs:
    assert after.count(repr(a)+','+repr(b))==1
    after=after.replace(repr(a)+','+repr(b),repr(b)+','+repr(c))
after=after.replace('feebcbb5894797d9f748a7b43e817b30da90e64068f17f141135121462ef234c','5c4b48399b2a04383fc0b736127925bfb0ed9dca7cf63f0c62bedc35a4b07240')
replace(before,after)
replace('ROOT_V18_COMPLETE_COMBINED_PREPARE_HOST_SOURCE_INVERSE_V1','ROOT_V19_COMPLETE_COMBINED_PREPARE_HOST_SOURCE_INVERSE_V1')
replace("formal_factory='/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py'",
"formal_factory='/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py'")
inverse=text
for e in reversed(edits):
    assert inverse.count(e['new'])==e['occurrences']
    inverse=inverse.replace(e['new'],e['old'])
assert inverse==old
compile(text,str(D/'generate_prepare_host.py'),'exec')
with (D/'generate_prepare_host.py').open('x') as f:f.write(text)
proof=dict(schema='AXMAT_V19_PREP_GENERATOR_FINITE_INVERSE_TO_ROOT_V18_V1',
parent_path=str(P),parent_sha256=hashlib.sha256(old.encode()).hexdigest(),
new_generator=str(D/'generate_prepare_host.py'),new_generator_sha256=hashlib.sha256(text.encode()).hexdigest(),
edits=edits,finite_change_count=len(edits),full_inverse_exact=True,
source_compile_only=True,business_executed=False,project_or_ART_written=False)
with (D/'generator_finite_inverse_proof.json').open('x') as f:json.dump(proof,f,indent=2);f.write('\n')
print(json.dumps(dict(source_only=True,generator=proof['new_generator'],generator_sha256=proof['new_generator_sha256'],finite_changes=len(edits),full_inverse_exact=True,business_executed=False)))
