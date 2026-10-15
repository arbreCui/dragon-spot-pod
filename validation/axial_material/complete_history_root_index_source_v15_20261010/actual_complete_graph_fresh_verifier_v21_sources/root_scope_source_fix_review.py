"""One finite SOURCE-only history-root fix proof; no resource/API import/call."""
import ast
import hashlib
import json
from pathlib import Path
OUT=Path(__file__).parent
OLD=Path('/private/tmp/axmat_v21_complete_fresh_verifier_binding_SOURCE_ONLY_20261010_angular_mc93u5rs')
ART=Path('/Users/wen/spot/validation/artifacts')
RESOURCE=Path('/Users/wen/spot/validation/axial_material/moment_order_complete_history_resource_trie_20261010.py')
SUPPORT=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py')
checks=[];sourcepins=[]
def check(label,condition):
 if type(condition) is not bool or not condition:raise AssertionError(label)
 checks.append(dict(name=label,value=True,type='bool'))
def read(path,sha=None):
 s=path.lstat();id7=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];raw=path.read_bytes();a=path.lstat()
 check('full SOURCE EOF7identity '+path.name,len(raw)==s.st_size and id7==[a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns])
 digest=hashlib.sha256(raw).hexdigest()
 if sha is not None:check('fixed SOURCE SHA '+path.name,digest==sha)
 sourcepins.append(dict(path=str(path),sha256=digest,identity=id7));return raw
def tree(raw):return ast.parse(raw)
def same(a,b):return ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False)
def function(module,name):return next(n for n in module.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
oldhost=read(OLD/'fresh_verifier_host.UNREADY.py','abf7129b627a0aa06e6ca42a88ab80f809f7badc478454555ff5069c4cf02222')
newhost=read(OUT/'fresh_verifier_host.UNREADY.py')
before='    roots=resource.history_roots([str(HOST),str(OUT),str(SOURCE_ARCHIVE),str(RECEIPTS),str(support.SOURCE),str(support.OUT),str(support.TERMINAL)],support.ART)'
after="    declared_history_roots=(HOST,OUT,support.SOURCE,support.OUT,support.TERMINAL)\n    if len(declared_history_roots)!=5 or any(path==support.ART or not path.is_relative_to(support.ART) for path in declared_history_roots):\n        raise ValueError('all five declared history roots must remain strict ART descendants')\n    roots=resource.history_roots([str(path) for path in declared_history_roots],support.ART)"
check('one bounded old outsideART root block',oldhost.decode().count(before)==1 and newhost.decode().count(after)==1)
restored=newhost.decode().replace(after,before,1)
check('full previous0057 host bytes inverse',restored.encode()==oldhost)
check('full previous0057 host AST inverse',same(tree(restored),tree(oldhost)))
check('driver exactly unchanged from blocked0057',read(OUT/'fresh_verifier_controls.UNREADY.py')==read(OLD/'fresh_verifier_controls.UNREADY.py','41d49ac418b6bfe9403a600edc111ff9faa2abd4b146edfce759ffcbbe9cb327'))
check('Root binding generator exactly unchanged',read(OUT/'bind_fresh_verifier_sources.py')==read(OLD/'bind_fresh_verifier_sources.py','76c516aa1965ce6316062df6806a9616e4dccff1bc239d37b52c542234c491c4'))
check('host extra controls definitions exactly unchanged',read(OUT/'host_extra_definitions.txt')==read(OLD/'host_extra_definitions.txt'))
newtree=tree(newhost);main=function(newtree,'main')
assignment=next(n for n in main.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='declared_history_roots' for t in n.targets))
check('exact original five ART root symbols retained',[ast.unparse(n) for n in assignment.value.elts]==['HOST','OUT','support.SOURCE','support.OUT','support.TERMINAL'])
roots=[ART/'axial-material-complete-graph-fresh-verifier-host-v21-20261010',ART/'axial-material-complete-graph-fresh-verifier-v21-20261010',ART/'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-admission-v15-20261010',ART/'axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010',ART/'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-terminal-v15-20261010']
supporttree=tree(read(SUPPORT,'3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'))
supportassign={n.targets[0].id:n.value for n in supporttree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
for name,path in zip(('SOURCE','OUT','TERMINAL'),roots[2:]):
 check('fixed support SOURCE expression '+name,ast.unparse(supportassign[name])=="ART / "+repr(path.name))
rootfacts=[]
for path in roots:
 check('static lexical strict ART descendant '+str(path),path.is_absolute() and path!=ART and path.is_relative_to(ART) and '..' not in path.parts)
 rootfacts.append(dict(path=str(path),Path_is_relative_to_ART=True,path_is_not_ART=True,no_filesystem_query_performed=True))
check('runtime strict ART range guard declared','path==support.ART or not path.is_relative_to(support.ART)' in newhost.decode())
rootcalls=[n for n in ast.walk(main) if isinstance(n,ast.Call) and ast.unparse(n.func)=='resource.history_roots']
check('one genuine history_roots call',len(rootcalls)==1 and ast.unparse(rootcalls[0].args[0])=='[str(path) for path in declared_history_roots]' and ast.unparse(rootcalls[0].args[1])=='support.ART')
rr=read(RESOURCE,'ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022');rt=tree(rr)
scope=function(rt,'history_roots');classnode=function(rt,'DynamicHistoryResources');checkmethod=next(n for n in classnode.body if isinstance(n,ast.FunctionDef) and n.name=='check')
check('original dynamic full axial family glob remains in unchanged resource SOURCE',any(isinstance(n,ast.Call) and ast.unparse(n.func)=='artifacts_root.glob' and len(n.args)==1 and ast.unparse(n.args[0])=='pattern' for n in ast.walk(scope)) and 'axial-material-*' in ast.get_source_segment(rr.decode(),scope))
check('original resource check re-expands history roots and validates scope',any(isinstance(n,ast.Call) and ast.unparse(n.func)=='history_roots' and [ast.unparse(a) for a in n.args]==['self.declared_roots','self.artifacts_root'] for n in ast.walk(checkmethod)) and any(isinstance(n,ast.Call) and ast.unparse(n.func)=='validate_history_roots' for n in ast.walk(checkmethod)))
check('outsideART SOURCE and receipts stay in joint archive counting','support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))' in newhost.decode() and newhost.decode().count('support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))')==oldhost.decode().count('support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))')==2)
check('original preflight reserve and after final joint cap remain byte exact',all(part in newhost.decode() and part in oldhost.decode() for part in ("before['artifact_bytes']+ARCHIVE_CAP>=96*2**30 or before['disk_free_bytes']-ARCHIVE_CAP<8*2**30",'if not elapsed<WHOLE_CAP or not archived<ARCHIVE_CAP','if support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))>=ARCHIVE_CAP or time.monotonic()-started>=WHOLE_CAP')))
check('all complete namespace before after7id unaffected','source_after!=source_before' in newhost.decode() and 'for entry in inputs+[hpin,rpin]' in newhost.decode())
check('unchanged600 1800 512 64 96 free8 1 1 0','WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,64*2**20' in newhost.decode() and '8*2**30,96*2**30,production.ResourceFailure' in newhost.decode() and 'threads=1,children_at_once=1,retries=0' in newhost.decode())
proof=dict(schema='AXMAT_V21_FRESH_VERIFIER_HISTORY_ROOT_SCOPE_FINITE_SOURCE_FIX_V1',status='SOURCE_FIX_ONLY_UNREADY_NOT_EXECUTED',checks=checks,all_checks_typed_true=True,previous_blocked_package_manifest_SHA='005722cf51b0f3869f7c621caa5617a751c3314fd52f4ea13dc59a0d0eb1c672',old0057_pack_preserved=True,old0057_must_not_bind_or_run=True,one_host_root_scope_hunk=dict(before=before,after=after),full_previous0057_host_bytes_AST_inverse=True,driver_and_binder_byte_exact_unchanged=True,declared_history_roots=rootfacts,all_five_static_strict_ART_descendants=True,unchanged_resource_SOURCE_pin=sourcepins[-1],unchanged_dynamicglob_retains_all_current_axial_family=True,SOURCE_receipts_excluded_from_history_roots_only=True,joint_HOST_OUT_SOURCE_receipts64MiB_caps_unchanged=True,original_preflight_resource_reserve_unchanged=True,preflight_independent_joint_archive_measurement_was_not_added=True,all_source_namespace7id_unchanged=True,sourcepins=sourcepins,resource_guard_API_import_or_call=False,Root_witness_graph_ART_directory_numeric_read=False,runtime_executed=False,helper_metadata_qualified=False,whole_business_INPUT=False,native=False,AAA=False,ABA=False,physics_balance=False)
(OUT/'ROOT_SCOPE_SOURCE_FIX_REVIEW.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(dict(status=proof['status'],all_checks_typed_true=True,checks=len(checks),full_previous0057_bytes_AST_inverse=True,driver_binder_unchanged=True,all_five_declared_roots_static_strict_ART_descendants=True,resource_guard_API_graph_ART_directory_read=False)))
