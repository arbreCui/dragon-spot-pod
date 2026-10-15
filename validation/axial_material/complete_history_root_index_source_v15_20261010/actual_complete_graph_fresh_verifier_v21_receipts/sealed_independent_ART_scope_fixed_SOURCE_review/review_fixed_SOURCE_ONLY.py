#!/usr/bin/env python3
"""Independently review one SOURCE root-domain fix and the entire sealed package."""
from pathlib import Path
import ast,hashlib,json,stat
DEST=Path(__file__).absolute().parent
NEW=Path('/private/tmp/axmat_v21_complete_fresh_verifier_ART_roots_SOURCE_fix_20261010_angular_ws815t4g')
OLD=Path('/private/tmp/axmat_v21_complete_fresh_verifier_binding_SOURCE_ONLY_20261010_angular_mc93u5rs')
OLD_REVIEW=Path('/private/tmp/axmat_v21_fresh_probe_0057_independent_SOURCE_review_20261010/INDEPENDENT_REVIEW.json')
NEW_MANIFEST_SHA='a459771501251a152ac596df26d2ffb93190a40386bb03f4a1b1f974e223316a'
OLD_MANIFEST_SHA='005722cf51b0f3869f7c621caa5617a751c3314fd52f4ea13dc59a0d0eb1c672'
OLD_REVIEW_SHA='0b2d99418c4844a239ac23be1fd8b0f0f3e0dd36947cb5f6675e6335181b03a9'
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
SUPPORT=ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py'
RESOURCE=ROOT/'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py'
PINS=[];CHECKS=[]
def sha(x):return hashlib.sha256(x).hexdigest()
def id7(path):
 s=path.lstat()
 if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1:raise ValueError('ordinary private fixed SOURCE required')
 return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(path,want=None):
 a=id7(path);raw=path.read_bytes();b=id7(path)
 if a!=b or len(raw)!=a[4] or (want is not None and sha(raw)!=want):raise ValueError('fixed full SOURCE EOF SHA7ID changed')
 p=dict(path=str(path),sha256=sha(raw),size_bytes=len(raw),identity7=a);PINS.append(p);return raw
def check(label,truth):
 if type(truth)is not bool or not truth:raise AssertionError(label)
 CHECKS.append(dict(name=label,typed_bool=True,value=True))
def dump(x):return ast.dump(x,include_attributes=False)
def calls(tree,name):return [x for x in ast.walk(tree) if isinstance(x,ast.Call) and ast.unparse(x.func)==name]
def defs(tree):return {x.name:x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def assigns(tree):
 return {n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def write(name,value):
 raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
 with (DEST/name).open('xb') as f:f.write(raw)
 return dict(path=str(DEST/name),sha256=sha(raw),size_bytes=len(raw),identity7=id7(DEST/name))
def main():
 mraw=read(NEW/'MANIFEST.json',NEW_MANIFEST_SHA);m=json.loads(mraw)
 old_mraw=read(OLD/'MANIFEST.json',OLD_MANIFEST_SHA);om=json.loads(old_mraw)
 review_raw=read(OLD_REVIEW,OLD_REVIEW_SHA);prior=json.loads(review_raw)
 check('prior independent review contains exactly real root-domain blocker',prior['status']=='SOURCE_BLOCKED_DO_NOT_BIND_OR_RUN_0057' and len(prior['blockers'])==1 and prior['blockers'][0]['id']=='HISTORY_ROOT_DOMAIN_SOURCE_BLOCKER' and prior['check_count']==88 and all(x['value'] is True for x in prior['independent_static_checks']))
 check('new actual Root sealed SOURCE manifest schema/count',m['schema']=='AXMAT_V21_FRESH_VERIFIER_BINDING_SOURCE_PACKAGE_MANIFEST_V1' and m['source_only'] is True and m['runtime_executed'] is False and m['member_count']==len(m['members'])==17)
 check('full new flat package members',len({x['name'] for x in m['members']})==17 and set(x.name for x in NEW.iterdir())=={x['name'] for x in m['members']}|{'MANIFEST.json'})
 members={}
 for x in m['members']:
  check('flat Source member '+x['name'],Path(x['name']).name==x['name'])
  raw=read(NEW/x['name'],x['sha256'])
  check('member complete EOF7ID '+x['name'],len(raw)==x['size_bytes'] and PINS[-1]['identity7']==x['identity'])
  members[x['name']]=raw
  if x['name'].endswith('.py'):ast.parse(raw);compile(raw,str(NEW/x['name']),'exec',dont_inherit=True,optimize=0)
 check('whole17 member total',sum(len(x) for x in members.values())==m['member_bytes']==214851)
 check('exact old0057 manifest copy preserved',members['previous_0057_MANIFEST_exact.json']==old_mraw)
 oldmembers={}
 for x in om['members']:
  raw=read(OLD/x['name'],x['sha256'])
  check('unchanged original0057 Source member '+x['name'],len(raw)==x['size_bytes'] and PINS[-1]['identity7']==x['identity'])
  oldmembers[x['name']]=raw
 hostraw=members['fresh_verifier_host.UNREADY.py'];oldhost=oldmembers['fresh_verifier_host.UNREADY.py']
 check('new exact host source SHA',sha(hostraw)=='c43052504e34238a25746aa41d8a7120d9a4d48fdda090d98735322acd0e3150')
 for name,want in [('fresh_verifier_controls.UNREADY.py','41d49ac418b6bfe9403a600edc111ff9faa2abd4b146edfce759ffcbbe9cb327'),('bind_fresh_verifier_sources.py','76c516aa1965ce6316062df6806a9616e4dccff1bc239d37b52c542234c491c4'),('host_extra_definitions.txt','68c4d4d32036bf5b1c23f0f4bd038404a2043332ac40a7df1f52d49d7260ed8a')]:
  check('entire previously independently reviewed core SOURCE unchanged '+name,members[name]==oldmembers[name] and sha(members[name])==want)
 fix=json.loads(members['ROOT_SCOPE_SOURCE_FIX_REVIEW.json'])
 h=fix['one_host_root_scope_hunk']
 check('exact unique Source root fix region',oldhost.decode().count(h['before'])==hostraw.decode().count(h['after'])==1)
 restored=hostraw.decode().replace(h['after'],h['before'],1).encode()
 check('whole Source fix inverse old0057 bytes and AST exact',restored==oldhost and dump(ast.parse(restored))==dump(ast.parse(oldhost)))
 ht=ast.parse(hostraw);ot=ast.parse(oldhost);hd=defs(ht);od=defs(ot)
 check('all original host definition names/order exact',list(hd)==list(od))
 for name in hd:
  if name!='main':check('full original independent host function AST exact '+name,dump(hd[name])==dump(od[name]))
 for name in ('helper.modules','helper.guard_admission','resource.DynamicHistoryResources','support.load','full.OwnRSSSerialExecutor','runner.execute','resources.check','support.archive_bytes'):
  check('all unchanged genuine Source call AST and order '+name,[dump(n) for n in calls(ht,name)]==[dump(n) for n in calls(ot,name)])
 hp=json.loads(members['host_template_complete_source_inverse.json']);whole=hostraw.decode()
 check('complete original genuine de72 inverse remains23',len(hp['ordered_hunks'])==23)
 for i,hunk in reversed(list(enumerate(hp['ordered_hunks']))):
  check('complete23 original host inverse anchor '+str(i),whole.count(hunk['after'])==1)
  whole=whole.replace(hunk['after'],hunk['before'],1)
 genuine=read(Path(hp['original_path']),'de72db68baa9b91fee8aad1965605ab25c9cb11ed2ea3013c3a1f04d52a41fb2')
 check('entire23 inverse actual genuine original bytes AST',whole.encode()==genuine==members['pure_helper_controls_host.original.txt'] and dump(ast.parse(whole))==dump(ast.parse(genuine)))
 dp=json.loads(members['driver_template_complete_source_inverse.json']);whole=members['fresh_verifier_controls.UNREADY.py'].decode()
 check('whole original driver two inverse hunks',len(dp['ordered_hunks'])==2)
 for hunk in reversed(dp['ordered_hunks']):
  check('complete original driver inverse unique',whole.count(hunk['after'])==1);whole=whole.replace(hunk['after'],hunk['before'],1)
 check('entire prior UNREADY driver bytes AST exact',whole.encode()==members['fresh_verifier_controls.original_UNREADY.txt'] and dump(ast.parse(whole))==dump(ast.parse(members['fresh_verifier_controls.original_UNREADY.txt'])))
 main=hd['main']
 rootassign=[x for x in main.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='declared_history_roots' for t in x.targets)]
 check('one exact original five history root tuple',len(rootassign)==1 and isinstance(rootassign[0].value,ast.Tuple) and [ast.unparse(x) for x in rootassign[0].value.elts]==['HOST','OUT','support.SOURCE','support.OUT','support.TERMINAL'])
 rootcall=calls(ht,'resource.history_roots')
 check('one real dynamic history union sameART called over every declared path',len(rootcall)==1 and ast.unparse(rootcall[0].args[0])=='[str(path) for path in declared_history_roots]' and ast.unparse(rootcall[0].args[1])=='support.ART')
 check('new lexical fast domain guard matches real original resource constraint','if len(declared_history_roots)!=5 or any(path==support.ART or not path.is_relative_to(support.ART) for path in declared_history_roots):' in hostraw.decode())
 sraw=read(SUPPORT,'3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7');st=ast.parse(sraw);sg=assigns(st)
 roots=[ART/'axial-material-complete-graph-fresh-verifier-host-v21-20261010',ART/'axial-material-complete-graph-fresh-verifier-v21-20261010']
 for name in ('SOURCE','OUT','TERMINAL'):
  value=sg[name];check('actual support input root exact ART/suffix expression '+name,isinstance(value,ast.BinOp) and isinstance(value.op,ast.Div) and isinstance(value.left,ast.Name) and value.left.id=='ART' and isinstance(value.right,ast.Constant) and type(value.right.value)is str)
  roots.append(ART/value.right.value)
 check('all5 static lexical roots are strict ART descendants',len(roots)==5 and len(set(roots))==5 and all(x.is_absolute() and x!=ART and x.is_relative_to(ART) and '..' not in x.parts for x in roots))
 rraw=read(RESOURCE,'ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022');rt=ast.parse(rraw);rd=defs(rt)
 history=rd['history_roots'];constructor=[x for x in rd['DynamicHistoryResources'].body if isinstance(x,ast.FunctionDef) and x.name=='__init__'][0];resourcecheck=[x for x in rd['DynamicHistoryResources'].body if isinstance(x,ast.FunctionDef) and x.name=='check'][0]
 check('full original resource dynamic family glob unchanged and present','axial-material-*' in ast.get_source_segment(rraw.decode(),history) and len(calls(history,'artifacts_root.glob'))==1)
 check('actual resource constructor original root validator remains',len(calls(constructor,'validate_history_roots'))==1)
 check('actual resource check fresh dynamic reunion and validator remain',len(calls(resourcecheck,'history_roots'))>=1 and len(calls(resourcecheck,'validate_history_roots'))>=1)
 check('both full joint64 archive calls unchanged after/final',len(calls(ht,'support.archive_bytes'))==2 and all(isinstance(n.args[0],ast.Tuple) and [ast.unparse(x) for x in n.args[0].elts]==['HOST','OUT','SOURCE_ARCHIVE','RECEIPTS'] for n in calls(ht,'support.archive_bytes')))
 check('original before96/free8 reserve retained without inventing independentbefore64',all(x in hostraw.decode() and x in oldhost.decode() for x in ("before['artifact_bytes']+ARCHIVE_CAP>=96*2**30 or before['disk_free_bytes']-ARCHIVE_CAP<8*2**30",'if not elapsed<WHOLE_CAP or not archived<ARCHIVE_CAP','if support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))>=ARCHIVE_CAP')) and fix['preflight_independent_joint_archive_measurement_was_not_added'] is True)
 check('full Source namespace and all guard scope remain unchanged',all(x in hostraw.decode() for x in ('source_after!=source_before','for entry in inputs+[hpin,rpin]','len(sys.argv)!=1','WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,64*2**20','threads=1,children_at_once=1,retries=0','UNKNOWN_Q=None','UNKNOWN_BUSINESS_PINS=None')))
 # Reuse exact earlier full 27-return/private/GZIP/37111+1 observations only
 # after matching entire driver/binder/extras and restoring whole original host.
 for p in prior['full_SOURCE_pins_before_after']:
  if str(OLD) in p['path']:continue
  raw=read(Path(p['path']),p['sha256'])
  check('earlier fixed actual Source unchanged '+p['path'],PINS[-1]['identity7']==p['identity7'])
 for p in list(PINS):
  q=Path(p['path']);a=id7(q);raw=q.read_bytes();b=id7(q)
  if a!=b or b!=p['identity7'] or sha(raw)!=p['sha256'] or len(raw)!=p['size_bytes']:raise ValueError('complete Source after-analysis pin changed')
 # Count real definitions rather than assume a prior unrelated runtime count.
 inventories={}
 for name in ('fresh_verifier_controls.UNREADY.py','fresh_verifier_host.UNREADY.py','bind_fresh_verifier_sources.py'):
  tr=ast.parse(members[name]);inventories[name]=dict(top_level_defs=len(defs(tr)),all_function_nodes=sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) for n in ast.walk(tr)),all_class_nodes=sum(isinstance(n,ast.ClassDef) for n in ast.walk(tr)))
 report=dict(schema='AXMAT_V21_ART_ROOTS_COMPLETE_FRESH_PROBE_INDEPENDENT_SOURCE_REVIEW_V1',status='SOURCE_PASS_FOR_ROOT_METADATA_BINDING_ONLY_NOT_RUNTIME_QUALIFICATION',
  author_manifest_sha256=NEW_MANIFEST_SHA,author_members=17,author_complete_bytes=214851,entire_new_author_package_full_EOF_SHA7ID_before_after=True,
  independent_checks=CHECKS,independent_check_count=len(CHECKS),prior88_source_observations_reused_by_entire_core_SOURCE_byte_match=True,prior_independent_review_sha256=OLD_REVIEW_SHA,
  previous0057_real_resource_Source_blocker_resolved=True,blockers=[],one_complete_source_fix_hunk=h,
  new_Source_change='Remove only two external Source/receipt roots from declared history tuple and add a lexical strict-ART guard; no original resource class/guard/runtime definition is changed.',
  full_previous0057_bytes_AST_inverse=True,full23_original_genuine_host_bytes_AST_inverse=True,full2_prior_UNREADY_driver_inverse=True,
  driver_and_binder_and_all_extra_host_control_Source_bytes_exact=True,actual_definition_inventories=inventories,
  all27_return_fields_types_order_floatbits_whole_contract_retained=True,full37111plus1_actual_read_open_contract_retained=True,
  full_unfiltered_gzip_trace_and_return_contract_retained=True,private4positives3rejects_and_full_calleridentity_contract_retained=True,
  all_Source_graph_driver_helper_before_after_full_SHA7ID_contract_retained=True,
  exact_integer_Root_install_schema_and_bool_typed0_contract_retained=True,normal_host_extra_argv=0,
  original600stage1800whole512RSS64MiB96GiBfree8_thread1child1retry0=True,all5_declared_history_roots_static_strict_ART_descendants=[str(x) for x in roots],original_full_dynamic_family_glob_reunion_unchanged=True,
  full_HOST_OUT_SOURCE_receipts_archive_checked_after_and_final=True,independent_before_joint64_measurement_in_host=False,
  Root_actual_external_prelaunch_joint_D_E_measurement_required_as_already_planned=True,
  actual_binding_candidate_finite_Source_recheck_required_after_Root_binding=True,
  full_SOURCE_pins_before_after=PINS,Root_witness_Q_current_graph_ART_directory_numeric_or_business_payload_read=False,
  helper_guard_API_author_generator_business_import_or_execution=False,canonical_ART_frozen_or_results_modified=False,
  actual_new_helper_Q=None,actual_controls_run=False,actual_512MiB_RSS_or_memory_improvement_proven=False,
  helper_metadata_qualified=False,whole_business_INPUT=False,native=False,AAA=False,ABA=False,physics_balance=False)
 rp=write('INDEPENDENT_REVIEW.json',report)
 print(json.dumps(dict(status=report['status'],review=rp,independent_checks=len(CHECKS),blockers=0,source_only=True,actual_runtime_executed=False),ensure_ascii=False))
if __name__=='__main__':main()

