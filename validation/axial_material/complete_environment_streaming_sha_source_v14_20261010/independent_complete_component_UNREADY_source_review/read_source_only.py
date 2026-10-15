from pathlib import Path
import ast,hashlib,json,os,stat
D=Path(__file__).parent
C=Path('/private/tmp/axmat_v14_streaming_sha_component_source_draft_hardlink_fix_20261010')
P=Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py')
N=C/'prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14.py'
Q=C/'COMPLETE_INVERSE_PROOF.json'
seven=lambda x:[x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
sha=lambda b:hashlib.sha256(b).hexdigest()
pins=[]
def read(p):
 p=Path(p);first=p.lstat();fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  pre=os.fstat(fd);chunks=[]
  while True:
   b=os.read(fd,2**20)
   if not b:break
   chunks.append(b)
  blob=b''.join(chunks);post=os.fstat(fd)
 finally:os.close(fd)
 after=p.lstat();assert seven(first)==seven(pre)==seven(post)==seven(after) and len(blob)==pre.st_size and stat.S_ISREG(first.st_mode)
 pins.append(dict(path=str(p),sha256=sha(blob),size_bytes=len(blob),path_before=seven(first),fd_before=seven(pre),fd_after=seven(post),path_after=seven(after)));return blob
pb,nb,qb=read(P),read(N),read(Q)
assert sha(pb)=='d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633'
assert sha(nb)=='d5f4748391d6078efa530f9b7a91734af4d406a6749c46a9a60342215f06b846'
assert sha(qb)=='bc5c3b9187873a9f151be735a491622d65a3d25e67ec108435e3ccd0fd58a768'
p,n=pb.decode(),nb.decode();proof=json.loads(qb);inverse=n
for e in reversed(proof['edits']):
 assert inverse.count(e['new'])==e['count'];inverse=inverse.replace(e['new'],e['old'],e['count'])
assert inverse==p and len(proof['edits'])==27
pt,nt=ast.parse(p),ast.parse(n)
def defs(t,s):
 out={}
 def visit(node,prefix=''):
  for c in ast.iter_child_nodes(node):
   if isinstance(c,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef)):
    k=prefix+c.name;assert k not in out;out[k]=ast.get_source_segment(s,c);visit(c,k+'.')
   else:visit(c,prefix)
 visit(t);return out
pd,nd=defs(pt,p),defs(nt,n);assert set(pd)<=set(nd)
changed=sorted(k for k in pd if pd[k]!=nd[k]);added=sorted(set(nd)-set(pd))
assert changed==sorted(['require_ready','source_inputs','complete_archive_forecast','prepare_build','environment','declaration_admission','audit_build','run_build','production_admission'])
for k in ('helper','parent_factory','resources_for','history_roots','validate_history_roots','DynamicHistoryResources','stage_commands','stage_labels','stage_outcome_valid','check_watch','terminal_contract','external_terminal_admission','control_audit','component_controls_audit','archive_forecast','binary_audit','sender_source_admission','sender_control_contract','sender_raw_receipt','sender_controls_audit','sender_namespace_identities'):
 assert pd[k]==nd[k],k
oldprep=next(x for x in pt.body if isinstance(x,ast.FunctionDef) and x.name=='prepare_build');newprep=next(x for x in nt.body if isinstance(x,ast.FunctionDef) and x.name=='prepare_build')
for var in ('common','commands','compiler','link','restore'):
 def assignments(fn,src):return [ast.get_source_segment(src,x)for x in ast.walk(fn)if isinstance(x,ast.Assign)and any(isinstance(t,ast.Name)and t.id==var for t in x.targets)]
 assert assignments(oldprep,p)==assignments(newprep,n),var
assert 'h.environment(old)' in nd['prepare_build'] and "environment(d);write_new(OUT/'declaration.json',d)" in nd['prepare_build']
assert 'h.environment(d);write_new' not in nd['prepare_build']
assert 'with private_helper.complete_environment_digest_context(d["native_library_aliases"]):' in nd['environment']
assert 'private_helper.environment(d, require_build_interpreter=require_build_interpreter)' in nd['environment']
assert 'path.stat().st_nlink != 1' not in nd['stream_environment_helper_source_admission']
assert 'require(path, wanted); observed_files[relative] = wanted; actual_bytes += path.stat().st_size' in nd['stream_environment_helper_source_admission']
def assignments(t,s):
 out={}
 for x in t.body:
  if isinstance(x,ast.Assign):
   for target in x.targets:
    for y in ast.walk(target):
     if isinstance(y,ast.Name):out[y.id]=ast.get_source_segment(s,x)
 return out
pc,nc=assignments(pt,p),assignments(nt,n)
except_names={'SOURCE','OUT','TERMINAL','FAMILY','TERMINAL_SCHEMA','SOURCE_STATUS'}
assert all(pc[k]==nc[k] for k in pc if k not in except_names),[k for k in pc if k not in except_names and pc[k]!=nc[k]]
unknown=['STREAM_ENVIRONMENT_HELPER_SHA','STREAM_ENVIRONMENT_SOURCE_PROOF_SHA','STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA','FUTURE_ACTUAL_BUILD_TERMINAL_SHA','FUTURE_ACTUAL_BUILD_SEAL_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
for k in unknown:assert ast.literal_eval(next(x.value for x in nt.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id==k for t in x.targets))) is None,k
actualproof=read('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_source_v14_20261010/source_patch_proof.json')
assert sha(actualproof)=='c7984abe2579399cd6e158a53fe94052e074fec08c03cf596ed859b6fa9321a6'
hp=json.loads(actualproof);helperb=read(hp['candidate_helper']['path'])
assert sha(helperb)==hp['candidate_helper']['sha256']=='839ea8cc88e4f10d36b6bd8fcb283c9c774702e4c3688fc8a66831431c1cb5fa'
inv=helperb.decode()
for e in reversed(hp['edits']):
 assert inv.count(e['new'])==e['count'];inv=inv.replace(e['new'],e['old'],e['count'])
assert sha(inv.encode())=='619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
report=dict(schema='AXMAT_V14_FULL_COMPONENT_COMPLETE_STREAM_SHA_SOURCE_INDEPENDENT_PEER_V1',status='PASS_SOURCE_ONLY_UNREADY',parent_sha256=sha(pb),candidate_sha256=sha(nb),inverse_proof_sha256=sha(qb),region_count=27,complete_inverse_byteexact=True,original_definition_count=len(pd),byteexact_original_definition_count=len(pd)-len(changed),changed_original_definitions=changed,added_definitions=added,original86_commands_labels_outcomes_watch_gates_byteexact=True,original68_mathematical_raw_controls_and14_sender_controls_byteexact=True,compile_recipe_assignment_nodes_byteexact=True,all_original_nonidentity_globals_exact=True,all_RSS_wall_budget_and_genuine_MRO_owners_exact=True,old_prepare_environment_onecall_original=True,final_prepare_factory_environment_complete_private_scope=True,explicit_all_native_aliases_context_normalcanonical_helper=True,hardlink_fixture_semantics_corrected=True,c798_sourceproof_full_inverse_619_and_helper839_match=True,unknown_future_pins_none=unknown,source7ID_before_after=pins,helper_imported_or_called=False,compiled=False,fixtures_executed=False,project_written=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,limits=['Actual21 helper controls admission and Root closed terminal remain future unknown; draft cannot claim actual controls qualification.','Root must bind only actual new3 source/control SHA and READY status, then execute all86 in exclusive fresh V14 namespace. No V13 partial success borrowed.','Pure source review does not prove speed improvement or original1800 completion.'])
with (D/'REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write(chr(10))
print(json.dumps(dict(status=report['status'],report_sha256=sha((D/'REPORT.json').read_bytes()),candidate_sha256=sha(nb),original_defs=len(pd),unchanged_defs=len(pd)-len(changed),changed_defs=changed,added_defs=added,source_count=len(pins),business_executed=False)))
