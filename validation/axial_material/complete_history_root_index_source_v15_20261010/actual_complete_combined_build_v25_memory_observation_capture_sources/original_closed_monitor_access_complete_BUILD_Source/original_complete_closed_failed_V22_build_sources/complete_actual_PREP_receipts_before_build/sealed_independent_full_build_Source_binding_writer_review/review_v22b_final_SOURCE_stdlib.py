"""Static finite source review only; never runs either binder or project code."""
from pathlib import Path
import ast,hashlib,json,os,stat
OUT=Path('/private/tmp/axmat_v22_fullbuild_Root_Source_binder_independent_review_05fs3v3d')
NEW=Path('/private/tmp/spot_bind_v22_original_full_build_host_ROOT_v22b.py')
OLD=Path('/private/tmp/spot_bind_v22_original_full_build_host_ROOT.py')
PROOF=Path('/private/tmp/spot_v22_full_build_binder_peer_scope_Source_inverse.json')
checks=[];pins={}
def check(k,v):
 assert type(v)is bool
 checks.append(dict(check=k,passed=v))
 if not v:raise ValueError(k)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(p):
 s=p.lstat();i=identity(s);check('regular explicit SOURCE/META '+str(p),stat.S_ISREG(s.st_mode)and s.st_nlink==1)
 with p.open('rb')as f:
  check('original fd seven integer identity '+str(p),identity(os.fstat(f.fileno()))==i)
  b=f.read();check('complete EOF bytes '+str(p),len(b)==s.st_size and f.read(1)==b'')
  check('fd after unchanged '+str(p),identity(os.fstat(f.fileno()))==i)
 check('path after unchanged '+str(p),identity(p.lstat())==i)
 pins[str(p)]=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=i)
 return b
parent_report=json.loads(read(OUT/'ORIGINAL_DRAFT_REVIEW.json'))
check('complete prior scope Source checks pass',parent_report['all_nonblocker_checks_passed']is True and len(parent_report['checks'])==185 and all(c['passed']is True for c in parent_report['checks']))
check('sole prior missing peer scope blocker',len(parent_report['blockers'])==1 and parent_report['blockers'][0]['id']=='saved_PREP_peer_not_bound_to_this_actual_PREP')
for p in parent_report['full_SOURCE_META_reads'].values():
 read(Path(p['path']));check('all exact original Source/META remain full-pin '+p['path'],pins[p['path']]==p)
before=read(OLD);after=read(NEW);proofraw=read(PROOF);proof=json.loads(proofraw)
check('new fixed Source170fc2',pins[str(NEW)]['sha256']=='170fc2abf3d3f1ba47e6aef233845d6335f844cdcdf89ce9786ce382c8231cd2')
check('old fixed44316 preserved',pins[str(OLD)]['sha256']=='44316f47416c5973c417a3ad07261cd1704bd091ebbb1f1a19ba9713ec7bf15a')
check('whole true Source inverse pins',proof['original_sha256']==pins[str(OLD)]['sha256']and proof['new_sha256']==pins[str(NEW)]['sha256'])
check('one finite exact hunk',len(proof['finite_hunks'])==1)
h=proof['finite_hunks'][0];a=before.decode();b=after.decode()
check('original unique anchor',a.count(h['before'])==h['count']==1)
check('new unique anchor',b.count(h['after'])==1)
check('only finite Source hunk',a.replace(h['before'],h['after'])==b)
back=b.replace(h['after'],h['before']);check('complete Source byte inverse',back.encode()==before)
check('complete Source AST inverse',ast.dump(ast.parse(back),include_attributes=False)==ast.dump(ast.parse(before),include_attributes=False))
oldtree=ast.parse(before);newtree=ast.parse(after)
defs=lambda t:{n.name:n for n in t.body if isinstance(n,ast.FunctionDef)}
olddefs,newdefs=defs(oldtree),defs(newtree)
check('all actual six Source function names remain',list(olddefs)==list(newdefs)and len(olddefs)==6)
for name in olddefs:
 check('all original Source function AST unchanged '+name,ast.dump(olddefs[name],include_attributes=False)==ast.dump(newdefs[name],include_attributes=False))
 check('all original Source function bytes unchanged '+name,ast.get_source_segment(a,olddefs[name])==ast.get_source_segment(b,newdefs[name]))
def assignment(t,name):return next(n.value for n in t.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name)
check('all21 true host substitutions unchanged',ast.dump(assignment(oldtree,'changes'),include_attributes=False)==ast.dump(assignment(newtree,'changes'),include_attributes=False))
required_schema='INDEPENDENT_V22_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1'
check('exact savedPREP review schema Source',"assert peer['schema']=='"+required_schema+"'"in b)
check('honest PREP-only actual scope Source',"assert peer['actual_PREP_metadata_only'] is True"in b)
flags=('whole_combined_build_qualified','whole_combined_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified')
loop=next(n for n in newtree.body if isinstance(n,ast.For)and isinstance(n.target,ast.Name)and n.target.id=='field')
check('all6 exact false scope keys Source',tuple(ast.literal_eval(loop.iter))==flags and ast.unparse(loop.body[0])=='assert peer[field] is False')
required_pins={
 'actual_Root_PREP_summary_pin':"sp",
 'actual_Root_PREP_terminal_pin':"pin(E / 'Root_actual_prepare_tool_terminal_return.json')",
 'actual_complete_namespace_manifest_pin':"pin(E / 'Root_actual_complete_prepare_namespace_manifest.json')",
}
comparisons={}
for n in newtree.body:
 if isinstance(n,ast.Assert)and isinstance(n.test,ast.Compare)and isinstance(n.test.left,ast.Subscript)and isinstance(n.test.left.value,ast.Name)and n.test.left.value.id=='peer'and isinstance(n.test.left.slice,ast.Constant):
  comparisons[n.test.left.slice.value]=(type(n.test.ops[0]).__name__,ast.unparse(n.test.comparators[0]))
for name,value in required_pins.items():check('same actual PREP complete pin Source '+name,comparisons.get(name)==('Eq',value))
check('peer pin checks before output mkdir',b.index("assert peer['actual_Root_PREP_summary_pin']==sp")<b.index('dest.mkdir()'))
check('whole source inverse before output mkdir',b.index('assert restored.encode()==old')<b.index('dest.mkdir()'))
check('never invoke any business stage',not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in ('execute','run','exec_module','Popen','system')for n in ast.walk(newtree)))
check('no reviewed dynamic imports',not any(isinstance(n,ast.Import)and any(v.name in ('importlib','subprocess','ctypes')for v in n.names)for n in ast.walk(newtree)))
check('explicit Source guard excludesART',"not p.is_relative_to(ART)"in ast.get_source_segment(b,newdefs['read']))
check('metadata destination freshTMP',"str(dest).startswith('/private/tmp/')"in b and 'not dest.exists()'in b)
check('frozen genuine fullhost remainsunique5stages',parent_report['actual_caps']==[1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0])
for p,v in list(pins.items()):read(Path(p));check('complete explicit Source/META end unchanged '+p,pins[p]==v)
(OUT/'FIXED_170fc2_ROOT_BINDER.py').write_bytes(after)
(OUT/'ROOT_ACTUAL_ONE_HUNK_PEER_SCOPE_INVERSE.byte_exact.json').write_bytes(proofraw)
report=dict(schema='INDEPENDENT_V22_FIXED_ORIGINAL_FULL_BUILD_ROOT_BINDER_SOURCE_REVIEW_V1',
 status='SOURCE_ONLY_PASS_REQUIRES_ACTUAL_SAVED_PREP_PEER_BEFORE_BINDING',source_only=True,
 PASS=True,all_checks_passed=True,blockers=[],checks=checks,check_count=len(checks),
 complete_prior_source_checks=parent_report['checks'],complete_prior_source_check_count=185,
 fixed_generator=pins[str(NEW)],original_generator=pins[str(OLD)],single_hunk_source_inverse=pins[str(PROOF)],
 all_original_six_functions_byte_AST_unchanged=True,all_original_21_host_literal_substitutions_unchanged=True,
 complete_original_host=parent_report['full_original_host'],complete_21_host_inverse=parent_report['complete_21_changes'],
 independent_static_expected_host_sha256=parent_report['independent_static_expected_host_sha256'],
 original_caps=parent_report['actual_caps'],full_explicit_SOURCE_META_reads=pins,
 actual_saved_PREP_peer_authenticated_here=False,actual_bound_source_generated_here=False,
 actual_build_or_INPUT_or_native_or_scientific_qualification=None,
 no_reviewed_generator_host_helper_guard_reader_API_or_business_execution=True,no_ART_numeric_payload_read=True,
 old_original_blocker_preserved=True,old_original_blocker_resolved_by_exact_new_source_predicates=True,
 future_actual_source_binding_cli=[
 '/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(NEW),
 '--saved-prep-peer-report','ACTUAL_FIXED_SAVED_PREP_PEER_REPORT_PATH',
 '--saved-prep-peer-report-sha256','ACTUAL_FIXED_SAVED_PREP_PEER_REPORT_SHA256',
 '--destination','NEW_ABSENT_FRESH_TMP_ROOT_SOURCE_OUTPUT'],
 actual_execution_gates=[
 'Root waits for sealed actual savedPREP peer PASS; its exact schema, PREP-only flags and same actual summary/terminal/complete namespace pins must match the source contract.',
 'Run metadata-only binder in unoptimized Python; no -O or PYTHONOPTIMIZE because this stdlib binder uses assert.',
 'Independently review actual generated complete host Source and full inverse; install/freeze complete dynamic Source inventory before business launch.',
 'Root prelaunch fresh H and no prior build outputs; full fixed source and original input alias/SHA7ID checks plus unchanged resources.',
 'One genuine whole full5stage build under original1800/600/512/2GiB/96history/free8/1thread/1child/0retry; all raw4tools, full OUTseal and fourtails preserved.',
 'Actual fullbuild PASS, formal Root closedinteger0 and savedreview remain future. WholeINPUT/native/RSS science/AAA/ABA are distinct subsequent qualifications.'
 ])
(OUT/'REVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(source_only=True,Source_PASS=True,checks=len(checks),prior_source_checks=185,
 new_generator_sha256=pins[str(NEW)]['sha256'],review_sha256=hashlib.sha256((OUT/'REVIEW.json').read_bytes()).hexdigest(),
 actual_saved_PREP_peer_authenticated_here=False,business_executed=False),indent=2))
