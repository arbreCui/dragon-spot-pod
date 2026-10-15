"""UNREADY complete aggregate-only reservation; no original resource helper import."""
import os
from pathlib import Path
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
AGGREGATE_OUTPUT_BOUND=320*2**20;SOURCE_BOUND=16*2**20
def need(v,m):
 if type(v)is not bool or not v:raise ValueError(m)
def reserve(latest,complete_roots,operation_root,resources_before,B4_lifecycle_admitted):
 need(B4_lifecycle_admitted['retired_paths_exactly_absent']is True and B4_lifecycle_admitted['all8_native_tree_SQL_pool_pairs_and55_contexts_retained']is True,'genuine exact B4 archive/retirement/post0 closure first')
 root=Path(operation_root);prefix=latest['complete_joint_roots']
 need(root.is_absolute()and str(root)==operation_root and root.parent==Path('/Users/wen/spot/validation/artifacts')and not os.path.lexists(root)and complete_roots==prefix+[operation_root]and len(complete_roots)==len(set(complete_roots))and not any(Path(a).is_relative_to(Path(b))for a in complete_roots for b in complete_roots if a!=b),'one distinct fresh complete aggregate root after entire genuine latest prefix, including failures')
 r=resources_before;j=r['complete_joint'];h=r['original_history']
 need(j['resource_roots']==complete_roots and r['host_SELF_peak_bytes']<512*2**20 and r['whole_elapsed_seconds']<1800,'actual original controller counted entire new stage scope')
 existing=j['artifact_bytes']+r['explicit_external_metadata_bytes']+r['host_open_unlinked_bytes']
 need(existing+AGGREGATE_OUTPUT_BOUND+SOURCE_BOUND<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'current measured full prefix+aggregate320+Source16 within original2GiB/cold/meta/history/free limits; no future stage budget')
 return dict(complete_joint_roots=complete_roots,original_caps=CAPS,stage_output_reservations=dict(aggregate=AGGREGATE_OUTPUT_BOUND),new_Source_metadata_reservation_bytes=SOURCE_BOUND,existing_measured_total_bytes=existing,only_current_stage='aggregate',original_cumulative_fresh_bound_bytes=2*2**30,other_stages_not_reserved_or_reduced=True)
