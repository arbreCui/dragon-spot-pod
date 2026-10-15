"""Finite SOURCE-only V20 retarget of the frozen genuine V19 normal PREP host; real reviewed READY path and SHA required."""
import ast
import hashlib
import json
from pathlib import Path
import sys

BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
PARENT = BASE/'actual_complete_combined_prepare_v19_sources/combined_prepare_host.py'
PARENT_SHA = 'f5c947297b3bd0a82b2e76099d9d8412892455c37bef4034d71b4157ad098580'
KNOWN_SOURCE_ANCESTOR = Path('/private/tmp/axmat_v19_complete_prepare_caller_last_use_source_only_20261010/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.UNREADY.py')
KNOWN_SOURCE_ANCESTOR_SHA = '585e450c5eb5d8748ff7dedfab28ddcf6163d89ca90f3cdeb5c9095ac93eed50'
DEST = Path(__file__).parent
SOURCE_ARCHIVE = BASE/'actual_complete_combined_prepare_v20_sources'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    if len(sys.argv) != 3:
        raise ValueError('actual independently reviewed V20 READY candidate path and full SHA required')
    ready = Path(sys.argv[1])
    ready_sha = sys.argv[2]
    if not ready.is_absolute() or ready.resolve() != ready:
        raise ValueError('absolute ordinary reviewed SOURCE path required')
    if len(ready_sha) != 64 or any(c not in '0123456789abcdef' for c in ready_sha) or ready_sha == '0'*64:
        raise ValueError('real full lowercase reviewed SOURCE SHA required')
    source = ready.read_bytes()
    if sha(source) != ready_sha:
        raise ValueError('actual READY whole SOURCE SHA must match required reviewed argument')
    ready_ast = ast.parse(source.decode())
    vals = {}
    for n in ready_ast.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            try:
                vals[n.targets[0].id] = ast.literal_eval(n.value)
            except (ValueError, TypeError):
                pass
    if vals['DRAFT_STATUS'] != 'READY_REVIEWED_V20_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY':
        raise ValueError('source-only READY binding required')
    future = ['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
    if any(vals[k] is not None for k in future):
        raise ValueError('all future business success pins must remain None')
    if sha(KNOWN_SOURCE_ANCESTOR.read_bytes()) != KNOWN_SOURCE_ANCESTOR_SHA or sha(PARENT.read_bytes()) != PARENT_SHA:
        raise ValueError('fixed known SOURCE ancestor and genuine parent host required')
    original = PARENT.read_text()
    text = original
    changes = [
        ('axial-material-complete-combined-prepare-host-v19-20261010','axial-material-complete-combined-prepare-host-v20-20261010'),
        ('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.py'),
        ('34efcc340b87257929e9d4cb06631455549327436d2bbdc5561639b6535e140b',ready_sha),
        ('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v19-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v20-20261010'),
        ('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v19-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v20-20261010'),
        ('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v19-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v20-20261010'),
        ('actual_complete_combined_prepare_v19_sources','actual_complete_combined_prepare_v20_sources'),
        ('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V19_DECLARATION_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V20_DECLARATION_V1'),
        ('AXMAT_V19_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1','AXMAT_V20_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1'),
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
    proof = dict(schema='ROOT_V20_COMPLETE_COMBINED_PREPARE_HOST_SOURCE_INVERSE_V1',status='SOURCE_ONLY_NOT_EXECUTED',factory_candidate=str(ready),factory_sha256=ready_sha,formal_factory='/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.py',host_candidate=str(outputs[0]),host_sha256=sha(text.encode()),parent_host=str(PARENT),parent_host_sha256=PARENT_SHA,known_SOURCE_ancestor=str(KNOWN_SOURCE_ANCESTOR),known_SOURCE_ancestor_sha256=KNOWN_SOURCE_ANCESTOR_SHA,independent_actual_V20_READY_SOURCE_review_required=True,changes=records,full_inverse_exact=True,source_archive=str(SOURCE_ARCHIVE),whole_wall_cap_seconds=1800,stage_wall_cap_seconds=600,rss_mib=512,archive_reserve_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0,genuine_supervisor_class_or_MRO_modified=False,business_executed=False,native_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    outputs[1].write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps({'host_candidate':str(outputs[0]),'host_sha256':proof['host_sha256'],'ready_source_sha256':proof['factory_sha256'],'full_inverse_exact':True,'business_executed':False}))

if __name__ == '__main__':
    main()
