import hashlib,json,os,stat
from pathlib import Path
B=Path('/private/tmp/spot_storage_twelfth_current_v9_graph_protection_boundary_20261009')
G=Path('/Users/wen/spot/validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/input_graph.json')
I=Path('/private/tmp/spot_storage_twelfth_root_inventory_20261009.json')
data=G.read_bytes();assert hashlib.sha256(data).hexdigest()=='0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3';g=json.loads(data);inv=json.loads(I.read_text());assert len(inv['cache_files'])==223
canon={x['path']for x in g['canonical_files']};ns=sorted(set(x[k]for x in g['namespaces']for k in ('root','canonical_root')));alias={x[k]for x in g['aliases']for k in ('path','target')};adir=sorted(set(x[k]for x in g['aliases']if x['kind']=='directory'for k in ('path','target')));roots=g['live_resource_roots'];assert len(roots)==231
strings=set()
def visit(v):
 if isinstance(v,str):strings.add(v)
 elif isinstance(v,list):
  for x in v:visit(x)
 elif isinstance(v,dict):
  for k,x in v.items():strings.add(k);visit(x)
visit(g)
def under(p,rs):return any(p==r or p.startswith(r+'/')for r in rs)
rows=[]
for x in inv['cache_files']:
 p=x['path'];s=Path(p).lstat();assert stat.S_ISREG(s.st_mode) and s.st_size==x['size'];ident=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
 v=dict(x,current_identity=ident,in_current_canonical=p in canon,in_exhaustive_namespace=under(p,ns),explicit_alias=p in alias,in_directory_alias=under(p,adir),exact_graph_literal=p in strings,in_current_resource_root=under(p,roots))
 v['current_graph_dependency_hit']=any(v[k]for k in ('in_current_canonical','in_exhaustive_namespace','explicit_alias','in_directory_alias','exact_graph_literal'))
 v['root_scope_cautious_HOLD']=v['in_current_resource_root']
 v['current_graph_and_resource_membership_clear']=not v['current_graph_dependency_hit']and not v['root_scope_cautious_HOLD']
 rows.append(v)
clear=[x for x in rows if x['current_graph_and_resource_membership_clear']]
r=dict(schema='SPOT_TWELFTH_223_CACHE_CURRENT_V9_CLOSURE_METADATA_INTERSECTION_V1',status='PASS_INTERSECTION_ONLY',graph_sha256=hashlib.sha256(data).hexdigest(),inventory_sha256=hashlib.sha256(I.read_bytes()).hexdigest(),cache_count=223,current_canonical_hits=[x for x in rows if x['in_current_canonical']],exhaustive_namespace_hits=[x for x in rows if x['in_exhaustive_namespace']],resource_root_hits=[x for x in rows if x['in_current_resource_root']],all_current_graph_dependency_hits=[x for x in rows if x['current_graph_dependency_hit']],clear_current_graph_and231resources=clear,clear_count=len(clear),clear_bytes=sum(x['size']for x in clear),clear_allocated_path_bytes=sum(x['allocated_bytes']for x in clear),no_dependency_admission_claim_beyond_current_graph_and_resources=True,cold_and_old_restore_source_exclusion_requires_other_report=True,all_bytes_not_rehashed=True,no_business_or_delete_or_formal_ART_write=True)
with (B/'cache_223_current_closure_intersection.json').open('x')as f:json.dump(r,f,indent=2);f.write('\n')
print(json.dumps(dict(status=r['status'],canonical_hits=[x['path']for x in r['current_canonical_hits']],namespace_hit_count=len(r['exhaustive_namespace_hits']),root_hit_count=len(r['resource_root_hits']),all_graph_hit_count=len(r['all_current_graph_dependency_hits']),clear_count=len(clear),clear_bytes=r['clear_bytes'],report_sha256=hashlib.sha256((B/'cache_223_current_closure_intersection.json').read_bytes()).hexdigest())))
