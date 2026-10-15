"""UNREADY exact-four B product lifecycle admission; never skips arbitrary missing files."""
import json,os
from pathlib import Path
SCHEMA='CURRENT_B4_EXACT_ARCHIVED_RETIRED_PRODUCT_ROLES_ADMISSION_V1'
def need(v,m):
 if type(v)is not bool or not v:raise ValueError(m)
def closed(value,projection,expected):
 row=value[projection['return_field']]
 need(value['observed_closed']is True and type(value['original_integer_exit_code'])is int and value['original_integer_exit_code']==0 and type(row['exit_code'])is int and row['exit_code']==0 and row.get('session_id')is None and row['chunk_id']==projection['genuine_terminal_chunk_id'],'exact genuine closed original typed0 lifecycle return')
 need(json.loads(row['output'].strip().splitlines()[-1])[projection['output_artifact_field']]==expected,'lifecycle real stdout exact artifact PF')
def expected_document(value,projection):
 need(value['schema']==projection['schema']and value['status']==projection['status']and value['failure']is None,'exact actual schema/status/role projection, never a generic PASS prefix')
def admit(request,read,current):
 spec=request['exact_B4_product_lifecycle_binding']
 need(type(spec)is dict and spec['schema']==SCHEMA,'NULL exact four lifecycle bindings remain UNREADY')
 m=read(spec['actual_B_capture_manifest_pin']);original=m['states']['B']['actual_material_product_pins']
 need(m['state_order']==['B']and set(m['states'])=={'B'}and m['actual_B_observation_executed']is True and m['actual_A_observation_executed']is False and spec['actual_B_capture_manifest_pin']==request['actual_observation_manifest_pin'],'same genuine current B-only manifest')
 need(len(original)==len({p['path']for p in original})==4 and [Path(p['path']).name for p in original]==['m.xsm','u.asc','a.asc','t.asc']and spec['ordered_exact4_historical_product_pins']==original,'only exact four whole original captured products, never contexts/8 snapshot trees/SQL/pools')
 a=spec['archive'];r=spec['retirement']
 need(type(a)is dict and type(r)is dict and all(type(x)is dict for x in(a['actual_role_projection'],r['actual_role_projection'])),'real archive/retirement role projections must be inspected after actual closure')
 av={k:read(a[k])for k in('receipt_pin','Root_tools_pin','post_pin','post_tools_pin')};rv={k:read(r[k])for k in('receipt_pin','Root_tools_pin','post_pin','post_tools_pin')};ap=a['actual_role_projection'];rp=r['actual_role_projection']
 for rows,specification,projection in((av,a,ap),(rv,r,rp)):
  closed(rows['Root_tools_pin'],projection['Root_return'],specification['receipt_pin']);closed(rows['post_tools_pin'],projection['post_return'],specification['post_pin'])
  expected_document(rows['receipt_pin'],projection['receipt']);expected_document(rows['post_pin'],projection['post'])
  need(rows['post_pin'][projection['post']['receipt_pin_field']]==specification['receipt_pin']and rows['post_pin'][projection['post']['Root_tools_pin_field']]==specification['Root_tools_pin'],'independent actual post0 binds same genuine receipt and Root return')
 ar=av['receipt_pin'];post=av['post_pin'];rr=rv['receipt_pin'];rpost=rv['post_pin']
 need(ar[ap['receipt']['ordered_original_pins_field']]==original and post[ap['post']['ordered_original_pins_field']]==original and post[ap['post']['Root_streamed_decompressed_SHA_length_all_matched_field']]is True,'all four original byte SHA/length were streamed and independently postverified by actual archive; no decompression replay here')
 compressed=ar[ap['receipt']['ordered_archive_pins_field']]
 need(len(compressed)==len({p['path']for p in compressed})==4 and post[ap['post']['ordered_archive_pins_field']]==compressed and spec['ordered_exact4_current_archive_pins']==compressed,'only exact four actual compressed archives remain current')
 released=rr[rp['receipt']['released_pins_field']]
 need(len(released)==len({p['path']for p in released})==4 and {p['path']:p for p in released}=={p['path']:p for p in original}and rr[rp['receipt']['released_bytes_field']]==sum(p['size_bytes']for p in original)and rpost[rp['post']['ordered_original_pins_field']]==original and rpost[rp['post']['ordered_archive_pins_field']]==compressed,'exact four original fullPFs actually retired, all four byte-preserving archives retained; no release-order shortcut')
 retired={p['path']for p in original}
 need(all(not os.path.lexists(x)for x in retired),'only proven exact four historical product names absent')
 need(not retired&{p['path']for p in request['complete_input_pins']+request['explicit_cumulative_metadata_file_pins']},'retired historical roles never supplied as live pins')
 for p in compressed:current(p)
 allpairs=request['aggregation_binding']['actual_context_states']['B']['all_snapshot_pairs']
 protected=[p for row in allpairs for p in(row['input_pin'],row['sqlite_pin'],row['native_pool_pin'])]+request['aggregation_binding']['actual_context_states']['B']['complete_context_pins']
 need(len(allpairs)==8 and len(request['aggregation_binding']['actual_context_states']['B']['complete_context_pins'])==55 and not retired&{p['path']for p in protected},'all 8 native snapshots and SQL/pools and 55 contexts remain mathematical inputs')
 for p in protected:current(p)
 return dict(schema=SCHEMA,exact_four_historical_fullPFs_preserved=original,exact_four_current_archive_pins=compressed,retired_paths_exactly_absent=True,all8_native_tree_SQL_pool_pairs_and55_contexts_retained=True,scientific_arrays_recomputed=False)
