"""Finite source retarget of the genuine V17 normal complete PREP host."""
import ast
import hashlib
import json
from pathlib import Path
import sys

BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
PARENT = BASE/'actual_complete_combined_prepare_v17_sources/combined_prepare_host.py'
PARENT_SHA = '37d432b8c91ddec6816fed6f7cea11fbfcba7071655ea64bc0f3c562288185d3'
UNREADY = BASE/'next_complete_combined_v18_source_only_review/sealed_complete_UNREADY_candidate/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.UNREADY.py'
UNREADY_SHA = 'ecfdff36d99aa7ea6be8fdf592e3d9ff5018b8c6aeb7604f1ef00dda1ddc3583'
DEST = Path(__file__).parent
SOURCE_ARCHIVE = BASE/'actual_complete_combined_prepare_v18_sources'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    if len(sys.argv) != 2:
        raise ValueError('one finite reviewed READY candidate path required')
    ready = Path(sys.argv[1])
    source = ready.read_bytes()
    ready_ast = ast.parse(source.decode())
    vals = {}
    for n in ready_ast.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            try:
                vals[n.targets[0].id] = ast.literal_eval(n.value)
            except (ValueError, TypeError):
                pass
    if vals['DRAFT_STATUS'] != 'READY_REVIEWED_V18_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY':
        raise ValueError('source-only READY binding required')
    future = ['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
    if any(vals[k] is not None for k in future):
        raise ValueError('all future business success pins must remain None')
    if sha(UNREADY.read_bytes()) != UNREADY_SHA or sha(PARENT.read_bytes()) != PARENT_SHA:
        raise ValueError('fixed complete source and genuine parent host required')
    original = PARENT.read_text()
    text = original
    changes = [
        ('axial-material-complete-combined-prepare-host-v17-20261010','axial-material-complete-combined-prepare-host-v18-20261010'),
        ('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py'),
        ('feebcbb5894797d9f748a7b43e817b30da90e64068f17f141135121462ef234c',sha(source)),
        ('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v17-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v18-20261010'),
        ('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v17-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v18-20261010'),
        ('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v17-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v18-20261010'),
        ('actual_complete_combined_prepare_v17_sources','actual_complete_combined_prepare_v18_sources'),
        ('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V17_DECLARATION_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V18_DECLARATION_V1'),
        ('AXMAT_V17_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1','AXMAT_V18_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1'),
    ]
    records = []
    for old, new in changes:
        if text.count(old) != 1:
            raise ValueError('unique finite source substitution required: '+old)
        text = text.replace(old,new,1)
        records.append(dict(old=old,new=new,occurrences=1))
    inverse = text
    for r in reversed(records):
        if inverse.count(r['new']) != 1:
            raise ValueError('unique exact inverse required')
        inverse = inverse.replace(r['new'],r['old'],1)
    if inverse != original:
        raise ValueError('entire genuine parent inverse required')
    ast.parse(text)
    outputs = (DEST/'combined_prepare_host.py',DEST/'Root_finite_host_source_inverse.json')
    if any(p.exists() for p in outputs):
        raise ValueError('source-generation outputs must be fresh')
    outputs[0].write_text(text)
    proof = dict(schema='ROOT_V18_COMPLETE_COMBINED_PREPARE_HOST_SOURCE_INVERSE_V1',status='SOURCE_ONLY_NOT_EXECUTED',factory_candidate=str(ready),factory_sha256=sha(source),formal_factory='/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py',host_candidate=str(outputs[0]),host_sha256=sha(text.encode()),parent_host=str(PARENT),parent_host_sha256=PARENT_SHA,unready_full_scope_source=str(UNREADY),unready_source_sha256=UNREADY_SHA,changes=records,full_inverse_exact=True,source_archive=str(SOURCE_ARCHIVE),whole_wall_cap_seconds=1800,stage_wall_cap_seconds=600,rss_mib=512,archive_reserve_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0,genuine_supervisor_class_or_MRO_modified=False,business_executed=False,native_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    outputs[1].write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps({'host_candidate':str(outputs[0]),'host_sha256':proof['host_sha256'],'ready_source_sha256':proof['factory_sha256'],'full_inverse_exact':True,'business_executed':False}))

if __name__ == '__main__':
    main()
