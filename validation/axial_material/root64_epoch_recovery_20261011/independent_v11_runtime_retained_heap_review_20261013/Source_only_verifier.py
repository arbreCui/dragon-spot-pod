from pathlib import Path
import ast,collections,gc,hashlib,json,os,resource,stat,sys,time
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';OUT=R/'validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v11';D=REC/'independent_v11_runtime_retained_heap_review_20261013';START=time.monotonic();pins=[]
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def source(p):
 p=Path(p);before=ident(p.lstat());assert stat.S_ISREG(before[2]);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();raw=bytearray()
 try:
  assert ident(os.fstat(fd))==before
  while True:
   b=os.read(fd,2**20)
   if not b:break
   h.update(b);raw.extend(b)
  assert ident(os.fstat(fd))==before
 finally:os.close(fd)
 assert ident(p.lstat())==before and len(raw)==before[4]
 q=dict(path=str(p),sha256=h.hexdigest(),size_bytes=len(raw),identity=before);pins.append(q);return bytes(raw),q
def read(p):b,q=source(p);d=json.loads(b);del b;return d,q
def children(v):
 if type(v)is dict:
  for k,x in v.items():yield k;yield x
 elif type(v)in(list,tuple):yield from v
def heap(v):
 seen=set();stack=[v];tot=0;bytype=collections.Counter();counts=collections.Counter();top=[]
 while stack:
  x=stack.pop();i=id(x)
  if i in seen:continue
  seen.add(i);n=sys.getsizeof(x);tot+=n;t=type(x).__name__;bytype[t]+=n;counts[t]+=1
  if n>=4096:top.append(dict(type=t,shallow_bytes=n,length=len(x)if hasattr(x,'__len__')else None))
  stack.extend(children(x))
 return dict(unique_shallow_sum_bytes=tot,unique_object_count=len(seen),bytes_by_type=dict(bytype),count_by_type=dict(counts),largest_shallow_objects=sorted(top,key=lambda q:q['shallow_bytes'],reverse=True)[:20])
def scalarheap(v):return heap(v)['unique_shallow_sum_bytes']
raw,rp=read(OUT/'Root_actual_complete_execution_record_before_final_publication.json');ledger,lp=read(OUT/'AAA3-streaming/stages.json');summary,sp=read(OUT/'Root_actual_three_plane_engineering_summary.json')
assert rp['size_bytes']==13161177 and lp['size_bytes']==11111562 and raw['records']==ledger['stages']and len(raw['records'])==45
assert summary['complete_unmodified_execution_records_pin']==rp and summary['status']=='FAILED_UNQUALIFIED_NO_RETRY'and summary['failure']=='RuntimeError: original SELF 512MiB cap'and summary['engineering_three_plane_closed0']is False
assert summary['SELF_peak_bytes']==548306944 and summary['SELF_peak_bytes']/2**20==522.90625
assert summary['records']==[{k:v for k,v in x.items()if k not in('resource_before','resource_after')}for x in raw['records']]
before_raw=heap(raw);ledger_heap=heap(ledger);summary_heap=heap(summary)
rawfields=sorted([dict(field=k,unique_bytes=scalarheap(v),items=len(v)if hasattr(v,'__len__')else None)for k,v in raw.items()],key=lambda q:q['unique_bytes'],reverse=True)
resource_fields=[];snapshots=[];complete_record_heap=scalarheap(raw['records']);without_resources=[{k:v for k,v in x.items()if k not in('resource_before','resource_after','resources')}for x in raw['records']]
for i,row in enumerate(raw['records']):
 for k,v in row.items():
  if k.startswith('resource'):
   snapshots.append(v);resource_fields.append(dict(stage=i,label=row['label'],slot=k,heap_bytes=scalarheap(v),largest_fields=sorted([dict(name=n,bytes=scalarheap(x))for n,x in v.items()],key=lambda q:q['bytes'],reverse=True)[:5]))
snapshot_total=heap(snapshots)
snapshot_roots=[v['resource_roots']for v in snapshots if type(v)is dict and 'resource_roots'in v];snapshot_declared=[v['declared_resource_roots']for v in snapshots if type(v)is dict and 'declared_resource_roots'in v]
snapshot_contract=[v['resource_scope_contract']for v in snapshots if type(v)is dict and 'resource_scope_contract'in v]
retention={k:heap(raw[k])for k in('actual_private_release_ledger','actual_closed_CLE_scratch_archival_ledger','actual_operator_refusals','actual_complete_readback_proofs','actual_direct_alias_build','fixed_current_pins','owned_runtime_pins')}
# JSON deserialization duplicates shared original references. Reconstruct only
# exact sharing explicitly assigned by the frozen host, without changing data.
sharing=[];live_ledger=[]
for i,item in enumerate(raw['actual_private_release_ledger']):
 e=item['complete_evidence'];matches=[p for p in raw['actual_complete_readback_proofs']+raw['actual_operator_refusals']if p==e]
 assert len(matches)==1
 fresh=dict(item,complete_evidence=matches[0]);live_ledger.append(fresh);sharing.append(dict(release_index=i,evidence_kind='proof'if matches[0]in raw['actual_complete_readback_proofs']else'case',evidence_serialized_heap_bytes=scalarheap(e)))
live_cases=[]
for c in raw['actual_operator_refusals']:
 if 'actual_closed_build_evidence'in c:
  assert c['actual_closed_build_evidence']==raw['actual_direct_alias_build'];live_cases.append(dict(c,actual_closed_build_evidence=raw['actual_direct_alias_build']))
 else:live_cases.append(c)
live_retained_graph=dict(records=raw['records'],ledger=live_ledger,cases=live_cases,proofs=raw['actual_complete_readback_proofs'],scratch=raw['actual_closed_CLE_scratch_archival_ledger'],direct_build=raw['actual_direct_alias_build'],fixed=raw['fixed_current_pins'],owned=raw['owned_runtime_pins'])
retained_reconstructed=heap(live_retained_graph)
hostraw,hp=source(REC/'aaa_three_plane_streaming_pipeline_source_v11/run_actual_three_plane_pipeline.py');host=hostraw.decode();del hostraw;tree=ast.parse(host);main=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
host_funcs={n.name:n for n in main.body if isinstance(n,ast.FunctionDef)}
functions=[]
for name in('stable','retain','copy','release','stash_closed_driver_scratch','run','refuse','direct_refuse','cleanup','storage_refuse'):
 node=host_funcs[name];text=ast.get_source_segment(host,node)
 functions.append(dict(name=name,start_line=node.lineno,end_line=node.end_lineno,whole_original_body=text,persistent_append_targets=sorted({ast.unparse(q.func.value)for q in ast.walk(node)if isinstance(q,ast.Call)and isinstance(q.func,ast.Attribute)and q.func.attr=='append'}),exception_captures=[dict(name=q.name,body=ast.unparse(q))for q in ast.walk(node)if isinstance(q,ast.ExceptHandler)]))
sources=[R/'validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py',R/'validation/axial_material/qualify_refined_AAA_layered_full.py',R/'validation/axial_material/prepare_qualified_AB_source_factor_production.py',REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py']
source_text={}
for p in sources:
 b,q=source(p);source_text[str(p)]=b.decode();ast.parse(b)
parent=source_text[str(sources[0])];pt=ast.parse(parent);cls=next(n for n in pt.body if isinstance(n,ast.ClassDef)and n.name=='SerialExecutor');execute=next(n for n in cls.body if isinstance(n,ast.FunctionDef)and n.name=='execute');execute_text=ast.get_source_segment(parent,execute)
assert 'record["error"] = str(error)'in execute_text and 'record["resource_before"] = self.resources.check()'in execute_text and 'record["resource_after"] = self.resources.check()'in execute_text
assert 'return text'in execute_text and 'log_sha256'in execute_text
assert all(not isinstance(v,BaseException)for v in raw.values())
maxlog=[]
for row in raw['records']:
 path=OUT/(row['label']+'.log');b,q=source(path);maxlog.append(dict(label=row['label'],file_pin=q,text_heap_bytes=sys.getsizeof(b.decode(errors='replace'))));del b
newcases=summary['actual_new_storage_control_names'];assert len(summary['actual_operator_refusals'])==29 and raw['records'][-1]['label']=='AAA/pair_rank_type'
lastw,wp=read(OUT/'AAA/pair_rank_type.watchdog.json');lastb,last_log_pin=source(OUT/'AAA/pair_rank_type.log');lastlog=lastb.decode();del lastb
assert lastw['returncode']==1 and lastw['limit_failure']is None and lastlog.count('SPOBOOX64: EXPLICIT POSITIVE RANK REQUIRED.')==1
report=dict(schema='INDEPENDENT_V11_RUNTIME_RETAINED_HEAP_AND_REFERENCE_LIFETIME_DIAGNOSTIC_V1',status='READONLY_DIAGNOSTIC_PASS_NO_SOURCE_CHANGE_OR_BUSINESS',original_input_fullpins=pins,actual_raw_and_ledger_records_equal=True,actual_original_record_count=45,all_resource_records_preserved=True,actual_accepted_refusal_count=29,actual_FAILURE='RuntimeError: original SELF 512MiB cap',actual_PARENT_SELF_peak_bytes=summary['SELF_peak_bytes'],actual_PARENT_SELF_peak_MiB=summary['SELF_peak_bytes']/2**20,actual_whole_seconds=summary['wall_seconds'],last_stage='AAA/pair_rank_type',last_child_exit1_exact_expected_abort_observed=True,raw_deserialized_heap=before_raw,original_stages_deserialized_heap=ledger_heap,summary_deserialized_heap=summary_heap,largest_raw_fields=rawfields,resource_snapshot_count=len(snapshots),raw_records_total_heap_bytes=complete_record_heap,raw_records_without_resource_snapshot_heap_bytes=scalarheap(without_resources),resource_snapshot_unique_heap=snapshot_total,all_snapshot_resource_roots_heap_bytes=scalarheap(snapshot_roots),all_snapshot_declared_resource_roots_heap_bytes=scalarheap(snapshot_declared),all_snapshot_scope_contracts_heap_bytes=scalarheap(snapshot_contract),all_snapshot_fields=resource_fields,persistent_host_collection_heaps=retention,exact_original_shared_proof_case_assignments=sharing,reconstructed_original_explicit_shared_reference_retained_heap=retained_reconstructed,source_function_complete_bodies=functions,original_execute_complete_body=execute_text,largest_actual_stage_log_text_heap=sorted(maxlog,key=lambda q:q['text_heap_bytes'],reverse=True)[:10],actual_new_storage_case_count=len(newcases),findings=[
 'runner.records permanently retains original resource_before and resource_after dictionaries; these are required raw historical records and are the largest measured decoded subtree.',
 'release ledger retains evidence references to existing proof/case objects; live assignments share those objects. JSON output repeats these shared structures and decoded heap overestimates their live contribution.',
 'scratch_ledger retains 30 small receipts and pins; scratch file payload stays on disk, not in persistent Python collections.',
 'refuse/direct_refuse stringify caught RuntimeError; neither cases nor ledger retains an exception or traceback. Local watchdog/log text leaves the function after stable succeeds or the failure unwinds.',
 'run temporarily retains an exception object in its local error until rethrow, but successful positive calls keep error None; no persistent container stores it. Nested local functions form ordinary main closure cycles whose referenced containers remain legitimately live during main.',
 'original execute returns transient text only on PASS; host caller discards the return. Permanent record stores SHA/status/error string and original resource snapshots, not full log text.',
 'guard_admission/class_text parses AST locally during initial admission and returns only source Paths; fixed stores compact physical pins. No source AST/text object is appended to fixed.',
 'This is a byte-pinned saved-JSON object-size diagnostic and static reference review, not a snapshot of the terminated live process heap. sys.getsizeof totals exclude interpreter/allocator overhead; explicit sharing reconstruction is partial and no future 512MiB success is inferred.'
],factory_repeated_check_or_dump_json_fixture_run=False,candidate_imported=False,new_pipeline_Source_written=False,compiler_or_numerical_business_executed=False,original_math_guards_caps_records_unchanged=True,SELF_review_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-START,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
for q in pins:
 assert ident(Path(q['path']).lstat())==q['identity']
D.mkdir()
with(D/'REVIEW.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=report['status'],review_pin=source(D/'REVIEW.json')[1],raw_heap_bytes=before_raw['unique_shallow_sum_bytes'],stage_ledger_heap_bytes=ledger_heap['unique_shallow_sum_bytes'],snapshots_heap_bytes=snapshot_total['unique_shallow_sum_bytes'],reconstructed_explicit_shared_runtime_graph_heap_bytes=retained_reconstructed['unique_shallow_sum_bytes'],resource_snapshots=len(snapshots),top_fields=rawfields[:7],persistent_heap_bytes={k:v['unique_shallow_sum_bytes']for k,v in retention.items()},SELF_review_peak_bytes=report['SELF_review_peak_bytes'],elapsed_seconds=report['wall_seconds'])))
