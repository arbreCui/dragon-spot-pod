"""Actual supplemental controls for the complete new-epoch pure run.

Preserves all67 fixture definitions, independently replays35 index attempts
under both real and forced-collision hashes, recreates all five cache-absence
cases and compares the whole238780-edge old/new/saved wire tables. Historical
wire memory measurements and old fresh observation are kept as historical data;
they never become a current performance or complete-current qualification.
"""
import ast
import gc
import hashlib
import json
from pathlib import Path
import sys
import time
import epoch_binding as binding
import cache_absence_controls as cache_controls

ROOT=Path('/Users/wen/spot')
REC=ROOT/'validation/axial_material/q_epoch_recovery_20261011'
META=ROOT/'validation/artifacts/axial-material-stable-wire-sort-original-pure-controls-v27-20261011-odcl3yl4'
INDEX_SOURCE=REC/'NEW_EPOCH_DATA_SUPPLEMENTS.py'
WIRE_SOURCE=REC/'candidate_source/wire67_original_fixture_definitions.py'
OLD_SOURCE=ROOT/'validation/axial_material/combined_runtime_complete_input_graph_read_open_short_index_20261011.py'
INVERSE=ROOT/'validation/artifacts/axial-material-stable-wire-sort-source-install-20261011/pure_wire_controls/SOURCE_ONLY_INVERSE_PROOF_V3.json'
SAVED_WIRE_RESULT=ROOT/'validation/artifacts/axial-material-stable-wire-sort-source-install-20261011/pure_wire_controls/ACTUAL_BOUNDED_COMPLETE_WIRE_SORT_CONTROL_RESULT.json'
HISTORICAL_FULL_GRAPH=ROOT/'validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-pre-graph-gc-20261010/input_graph.json'
F574=REC/'preserved_source_basis/HISTORICAL_EXACT_Q_CONTRACT.py'
ORDER_ENCODER=json.JSONEncoder(ensure_ascii=True,sort_keys=False,separators=(',',':'),allow_nan=False)

def require(value,message):binding.require(value,message)

def wanted(cfg,path):
    rows=[p for p in cfg['complete_supplement_input_pins']if p['path']==str(path)]
    require(len(rows)==1,'each full supplemental input must be explicitly bound once: '+str(path))
    binding.read_pinned(rows[0]);return rows[0]

def full_wire_controls(old,new,graph_pin,metadata,exact_value):
    before=binding.pin(graph_pin['path']);require(before==graph_pin,'historical whole wire graph current EOF pin differs')
    # This decodes the complete historical table. It never reads its37445
    # canonical payloads and never calls verify_graph on that historical graph.
    graph=old.strict_json(graph_pin['path'],graph_pin['sha256'])
    saved=graph['requirements'];old._validate_wire_requirement_table(saved)
    paths,names,categories,roles=(saved[k]for k in ('paths','owners','categories','binding_roles'))
    limits=(len(paths),len(paths),len(names),len(categories),len(roles))
    requirements=[];previous=None;duplicates=0
    for ids in old._decoded_requirement_rows(saved['rows'],limits):
        row=(paths[ids[0]],paths[ids[1]],names[ids[2]],categories[ids[3]],roles[ids[4]])
        require(type(row)is tuple and all(type(v)is str for v in row),'all full original wire rows must be exact builtin tuple/string')
        if row==previous:duplicates+=1
        requirements.append(row);previous=row
    require(len(requirements)==238780 and saved['rows']['column_count']==5,'original historical whole238780 five-column wire scope changed')
    row_identity=tuple(id(row)for row in requirements)
    del graph,previous,ids,row;gc.collect()
    old_table=old._wire_requirement_table_compact(requirements)
    candidate_table=new._wire_requirement_table_compact(requirements)
    exact_value(old_table,candidate_table,'full238780_old_new_wire_types_order_floatbits')
    exact_value(old_table,saved,'full238780_original_saved_wire_types_order_floatbits')
    old_encoded=old._canonical_json(old_table)
    new_encoded=new._canonical_json(candidate_table)
    saved_encoded=old._canonical_json(saved)
    require(old_encoded==new_encoded==saved_encoded,'whole wire EOF byte equality required')
    require(old_table['rows']['data']==candidate_table['rows']['data']==saved['rows']['data'],'complete encoded row data bytes differ')
    require(row_identity==tuple(id(row)for row in requirements),'all caller tuple identities/order changed')
    digest=hashlib.sha256(old_encoded).hexdigest()
    require(len(old_encoded)==metadata['complete_wire_table_bytes']==9793134 and digest==metadata['complete_wire_table_sha256']=='23be84aff01814dade96b9c6d833b04ea2f72ce2a80a1af43d7ab98ae6202003','entire historical wire expected byte count/SHA differs')
    data=old_table['rows']['data'].encode('ascii');row_digest=hashlib.sha256(data).hexdigest()
    require(len(data)==metadata['complete_encoded_row_data_ascii_bytes']==2852920 and row_digest==metadata['complete_encoded_row_data_sha256']=='000e309c36d680eed96e68d9dbc45af208b3a08d3fc1de800419627f02c0d1b0','complete full row bytes/SHA differ')
    require(duplicates==metadata['adjacent_full_duplicate_edges_retained']==0,'full duplicate-edge behavior changed')
    del old_table,candidate_table,saved,requirements,row_identity,old_encoded,new_encoded,saved_encoded,data;gc.collect()
    require(binding.pin(graph_pin['path'])==before,'historical full-wire graph changed through complete controls')
    return dict(schema='SPOT_NEW_EPOCH_ACTUAL_FULL238780_WIRE_EXACT_CONTROL_V1',logical_edges=238780,column_count=5,whole_wire_bytes=9793134,whole_wire_sha256=digest,complete_encoded_row_data_ascii_bytes=2852920,complete_encoded_row_data_sha256=row_digest,complete_return_types_order_floatbits_exact=True,all_caller_row_identity_order_unchanged=True,historical_full_graph_pin=before,historical_saved_memory_measurement_reexecuted=False,historical_37445_canonical_payloads_reexecuted=False,current_complete_fresh_qualified=False,new_Q_created=False)

def run_additional(new,artifacts,exact_value,cfg):
    started=time.monotonic()
    paths=[INDEX_SOURCE,WIRE_SOURCE,OLD_SOURCE,INVERSE,SAVED_WIRE_RESULT,HISTORICAL_FULL_GRAPH,F574,META/'ACTUAL_READ_OPEN_SHORT_INDEX_STATE_CONTROLS.json',META/'ACTUAL_SAVED_WIRE67_COMPLETE_FIELDS_REVIEW.json',REC/'small_data_actual_v2/ACTUAL_SYNTHETIC_INDEX_CONTROLS.json',REC/'small_data_actual_v2/ACTUAL_ALL67_WIRE_TINY_FIXTURES.json']
    pins=[wanted(cfg,path)for path in paths]
    before=list(pins)
    bypath={p['path']:p for p in pins}
    old=binding.load(bypath[str(OLD_SOURCE)],'new_epoch_actual_original_c6e_wire_helper')
    index=binding.load(bypath[str(INDEX_SOURCE)],'new_epoch_complete_actual_index_controls')
    wire=binding.load(bypath[str(WIRE_SOURCE)],'new_epoch_complete_actual_67_wire_fixture_controls')
    inverse=json.loads(binding.read_pinned(bypath[str(INVERSE)]))
    a=Path(OLD_SOURCE).read_bytes();b=Path(cfg['helper']['path']).read_bytes()
    require(a.count(inverse['exact_before'].encode())==1 and b==a.replace(inverse['exact_before'].encode(),inverse['exact_after'].encode()) and a==b.replace(inverse['exact_after'].encode(),inverse['exact_before'].encode()),'whole original/current helper Source forward inverse bytes differ')
    aa,bb=ast.parse(a),ast.parse(b)
    require(len(aa.body)==len(bb.body),'whole helper AST length differs')
    changed=[getattr(x,'name',type(x).__name__)for x,y in zip(aa.body,bb.body)if ast.dump(x,include_attributes=False)!=ast.dump(y,include_attributes=False)]
    require(changed==['_wire_requirement_table_compact'],'only reviewed complete wire function may differ')
    del a,b,aa,bb
    index_metadata=json.loads(binding.read_pinned(bypath[str(META/'ACTUAL_READ_OPEN_SHORT_INDEX_STATE_CONTROLS.json')]))
    index_result=index.index_controls(new,index_metadata)
    prior_index=json.loads(binding.read_pinned(bypath[str(REC/'small_data_actual_v2/ACTUAL_SYNTHETIC_INDEX_CONTROLS.json')]))
    exact_value(index_result,prior_index,'whole_new_and_actual_small_index_result')
    index_pin=artifacts.write_json('ACTUAL_NEW_EPOCH_FULL_INDEX_STATE_CONTROLS.json',index_result,encoder=ORDER_ENCODER)
    fixtures=wire.wire_fixture_controls(old,new)
    prior_wire=json.loads(binding.read_pinned(bypath[str(REC/'small_data_actual_v2/ACTUAL_ALL67_WIRE_TINY_FIXTURES.json')]))
    exact_value(fixtures,prior_wire['fixture_results'],'whole_new_and_actual_small_all67_fixture_results')
    metadata=json.loads(binding.read_pinned(bypath[str(SAVED_WIRE_RESULT)]))
    historical_review=json.loads(binding.read_pinned(bypath[str(META/'ACTUAL_SAVED_WIRE67_COMPLETE_FIELDS_REVIEW.json')]))
    exact_value(fixtures,metadata['fixture_results'],'whole_new_and_original_all67_complete_fixture_fields')
    exact_value(fixtures,historical_review['complete_saved_wire_control_result']['fixture_results'],'all67_historical_saved_review_fields_preserved')
    require(len(fixtures)==67 and sum(v['original_complete_evidence']['outcome']['kind']=='return'for v in fixtures)==14 and sum(v['original_complete_evidence']['outcome']['kind']=='raise'for v in fixtures)==53,'all67/14/53 original cases required')
    fixture_pin=artifacts.write_json('ACTUAL_NEW_EPOCH_ALL67_COMPLETE_WIRE_FIXTURES.json',dict(fixture_results=fixtures,fixtures=67,returns=14,raises=53),encoder=ORDER_ENCODER)
    full_wire=full_wire_controls(old,new,bypath[str(HISTORICAL_FULL_GRAPH)],metadata,exact_value)
    absence=cache_controls.run_controls(new,artifacts.root/'cache_absence_fixtures',bypath[str(F574)],exact_value)
    # Artifacts tracks every new cache fixture's bytes as well as reports.
    for path in (artifacts.root/'cache_absence_fixtures').rglob('*'):
        if path.is_file()and not path.is_symlink():artifacts.sizes[str(path.relative_to(artifacts.root))]=path.stat().st_size
    absence_pin=artifacts.write_json('ACTUAL_NEW_EPOCH_CACHE_ABSENCE_FIVE_CASES.json',absence,encoder=ORDER_ENCODER)
    require([binding.pin(p['path'])for p in before]==before,'all whole supplemental Source/data EOF pins changed')
    return dict(schema='SPOT_NEW_EPOCH_COMPLETE_PURE_SUPPLEMENT_ACTUAL_V1',index=index_pin,index_attempts=35,index_unique_records=9,index_markers=2,index_both_standard_and_forced_collision=True,index_private_guards=13,index_last_use_failures=3,wire67=fixture_pin,wire67_fixtures=67,wire67_returns=14,wire67_raises=53,full_historical238780_wire=full_wire,cache_absence=absence_pin,cache_absence_cases=cache_controls.CASE_NAMES,complete_supplement_input_pins_before_after=before,complete27_future_fresh_return_fields=binding.RETURN_FIELDS,complete9_snapshot_fields=binding.SNAPSHOT_FIELDS,all480_production_absences_actual=False,original37590_missing_canonical_endpoints_still_blocking_fullfresh=53,elapsed_seconds=time.monotonic()-started,current_complete_fresh_qualified=False,new_Q_created=False,whole_INPUT_admitted=False,science_or_BOOT_admitted=False)
