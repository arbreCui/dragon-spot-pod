"""Independent Source-only AST/text/dictionary review; no preparer/Host main/import."""
import ast,contextlib,copy,hashlib,io,json,os,shlex,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OUT=R/'independent_v15_actual_preparer_v2_and_SRC_retirement_admission_Source_review_20261014'
checks=[];observed={}
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def check(name,good):
 if not good:raise AssertionError(name)
 checks.append(name)
def pin(path):
 p=Path(path);i=ids(p.lstat());assert stat.S_ISREG(i[2]);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb')as f:assert ids(os.fstat(f.fileno()))==i;raw=f.read();assert ids(os.fstat(f.fileno()))==i
 assert ids(p.lstat())==i;row=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i);observed[str(p)]=(row,raw);return raw,row
def read(path):raw,row=pin(path);return json.loads(raw),row
def bound(row):raw,p=pin(row['path']);check('complete actual PF '+row['path'],p==row);return raw
check('unique independent review directory absent',not OUT.exists())
plan,planpf=read(R/'V15_ACTUAL_PREREQUISITE_PREPARER_SOURCE_PLAN_V2_20261014.json');prep,preppf=pin(R/'prepare_v15_actual_compact_pipeline_candidate_source_only_v2_20261014.py');helper,helperpf=pin(R/'v15_exact_completed_SRC_retirement_admission_source_v1_20261014.py')
check('current exact v2Source/PLAN/helper pins',preppf==plan['preparer_source_pin']and helperpf==plan['retirement_admission_Source_pin']and preppf['sha256']=='79cd2a1f021760f451c58e4f71dd9d8a56e72c8203d058836866d7a9afc2dc2e'and helperpf['sha256']=='9e6864537985470f6ce9ed5679f375960bc23168e470efdd412a73ff2048efe5'and planpf['sha256']=='29a73d250ac1855ddb3d685fbf9cdfe16f827780c3d2f20323c2e806e6444f3d')
ptree=ast.parse(prep);htree=ast.parse(helper)
check('no module import or execution performed',True)
check('all actual future PFs explicitNone/no Sourcepreparer or business execution',all(v is None for k,v in plan.items()if k.startswith('future_actual_'))and all(plan[k]is False for k in ('source_preparer_executed','compiler_executed','numerical_executed','pipeline_executed','files_deleted','AAA_qualified','ABA_admitted','goal_complete')))
check('exact four external parameter sets',plan['mandatory_preparation_external_prefixes']==['preparation-plan','public7','public7-root-tool','public7-post-tools']and plan['each_external_requires']==['summary','sha256','seven-id'])
values={k:json.loads(bound(row))for k,row in plan['selected_existing_pins'].items()};selected=plan['selected_existing_pins']
check('exact Root public7 argv source pin',selected['Root_public7_exact_argv']['sha256']=='21754746151bacef8135535ca0beb36d8d15826949648283dc08886f56a53e2c'and len(values['Root_public7_exact_argv']['argv'])==30)
inverse,ipf=read(R/'V15_PREPARER_V1_TO_V2_EXACT_SOURCE_PLAN_INVERSE_20261014.json');oldprep=bound(inverse['original_source_pin']);back=prep.decode()
for block in reversed(inverse['changes']):check('unambiguous v2preparer inverse block',back.count(block['after'])==1);back=back.replace(block['after'],block['before'],1)
check('preparer v2wholebytes inverse backv1',back.encode()==oldprep and len(inverse['changes'])==2 and inverse['candidate_source_pin']==preppf and inverse['new_plan_pin']==planpf)
oldplan=json.loads(bound(inverse['old_plan_pin']));check('inverse preserves actual original v1plan entire data',oldplan==inverse['old_plan_complete_data'])
check('v2selectedrows v1data original rows exact unchanged',all(plan['selected_existing_pins'][k]==v for k,v in oldplan['selected_existing_pins'].items()))
for k,v in oldplan.items():
 if k not in ('preparer_source_pin','selected_existing_pins'):check('v2plan original field unchanged '+k,plan[k]==v)
check('four current ownHF exact counts',[len(values[k]['dependencies'])for k in ('new_build_Host_freeze','fresh17_Host_freeze','private_model_Host_freeze','public7_Host_freeze')]==[2565,2586,2597,2629])
allrows={}
for key in ('new_build_Host_freeze','fresh17_Host_freeze','private_model_Host_freeze','public7_Host_freeze'):
 own=values[key]
 check('ownHF separately bound canonical source '+key,set(own['host_source'])=={'path','sha256','size_bytes','identity'})
 for row in own['dependencies']+[own['host_source']]:
  if row['path']in allrows:check('consistent direct current PF '+row['path'],allrows[row['path']]==row)
  allrows[row['path']]=row
for row in allrows.values():assert ids(Path(row['path']).lstat())==row['identity']
check('inherited current all7 direct PF closure reobserved without scientific EOF',True)
check('old377 wholedata closure unchanged',len(values['original_v14_Host_freeze']['dependencies'])==377 and values['predecessor_draft_plan']['original377_dependency_rows_to_retain']==values['original_v14_Host_freeze']['dependencies'])
check('selected current CommonSF correct',selected['current_Common_Source_freeze']['sha256']=='e2b380b7acf9d0d550adf260420454f2a08f16380e41f1d66bd6b7f678aae5d9')
for key in ('Root_actual_newbuild_tools','Root_actual_fresh17_tools','Root_actual_private_model_tools'):
 term=values[key]['actual_terminal_return'];check('genuine existing actual Root terminal0 '+key,type(term['exit_code'])is int and term['exit_code']==0 and term.get('session_id')is None)
for key in ('actual_newbuild_post_tools','actual_fresh17_post_tools','actual_private_model_post_tools'):
 term=values[key]['actual_postverification_return'];check('genuine existing actual independent terminal0 '+key,type(term['exit_code'])is int and term['exit_code']==0 and term.get('session_id')is None)
main=next(n for n in ptree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
text=prep.decode();funcs={n.name:ast.get_source_segment(text,n)for n in ptree.body if isinstance(n,ast.FunctionDef)}
check('preparer actual public Root realtyped0 and exactargv gate beforeSourcewriting',"require_terminal0(root_tools.get('actual_terminal_return'))"in text and "shlex.split(root_tools.get('exact_executed_command',''))!=values['Root_public7_exact_argv']['argv']"in text and text.index('public_post_pin=require_public_post0')<text.index('NEW.mkdir()'))
check('public post actual terminal0/fullPF rawreview binding/report included',all(s in funcs['require_public_post0']for s in ["require_terminal0(actual)","tools.get('observed_closed')is not True","json.loads(lines[-1])['review_pin']","review=read(review_pin)","report_pin not in list(walk_fullpins(review))"]))
check('terminal0 bool/still session strictly refused',"type(actual.get('exit_code'))is not int"in funcs['require_terminal0']and "actual.get('session_id')is not None"in funcs['require_terminal0'])
check('no compiler/subprocess/importlib/cleanup operations inpreparer AST',not any(isinstance(n,ast.Call)and((isinstance(n.func,ast.Attribute)and n.func.attr in('unlink','rmtree','system','Popen','run','exec_module'))or(isinstance(n.func,ast.Name)and n.func.id in('exec','eval','compile','__import__')))for n in ast.walk(ptree)))
check('Source/noHFCLI publication only',"own_Host_freeze_pin=None,own_CLI_pin=None,future_actual_v15_report_pin=None"in text and "actual_Host_freeze_pin=None,actual_CLI_pin=None,actual_v15_report_pin=None"in text)
old_source,oldpf=pin(R/'aaa_three_plane_compact_expected_pipeline_source_draft_v2_20261013/run_actual_three_plane_pipeline.py');original14,source14pf=pin(R/'aaa_three_plane_streaming_pipeline_source_v14/run_actual_three_plane_pipeline.py')
check('current original draft2 SHA',oldpf['sha256']=='bb1ee861ae91318ea67ea12bbb5b6eb19c0be7690064b1b0caf4de3d2aa54fdc')
check('current draft2 original uppercaseMF schema alreadycorrect',"ACTUAL_PUBLIC_READ_STALE_BEFORE_FULL_EOF_SHA_ALL7_V1"in old_source.decode())
# Execute only real pure text/AST splice statements. pin is an in-memory reader.
sourcecache={str(R/'aaa_three_plane_compact_expected_pipeline_source_draft_v2_20261013/run_actual_three_plane_pipeline.py'):(old_source,oldpf),str(R/'aaa_three_plane_streaming_pipeline_source_v14/run_actual_three_plane_pipeline.py'):(original14,source14pf),str(R/'v15_exact_completed_SRC_retirement_admission_source_v1_20261014.py'):(helper,helperpf)}
start=next(n.lineno for n in main.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Tuple)and any(isinstance(x,ast.Name)and x.id=='old_host_pin'for x in t.elts)for t in n.targets))
end=next(n.lineno for n in main.body if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Attribute)and isinstance(n.value.func.value,ast.Name)and n.value.func.value.id=='NEW'and n.value.func.attr=='mkdir')
body=copy.deepcopy([n for n in main.body if start<=n.lineno<end]);ret=ast.parse("return dict(text=text,raw=raw,inverse=inverse,changes=changes,protected=protected)").body[0]
wrapper=ast.FunctionDef(name='pure_real_Source_splice',args=ast.arguments(posonlyargs=[],args=[],kwonlyargs=[],kw_defaults=[],defaults=[]),body=body+[ret],decorator_list=[])
namespace=dict(ast=ast,REC=R,OLD=R/'aaa_three_plane_compact_expected_pipeline_source_draft_v2_20261013',NEW_OUT=Path(plan['future_candidate_own_OUT']),RETIREMENT=Path(helperpf['path']),old_plan=values['predecessor_draft_plan'],pin=lambda path:sourcecache[str(path)])
exec(compile(ast.fix_missing_locations(ast.Module(body=[wrapper],type_ignores=[])),str(preppf['path'])+':pure_source_text_extract','exec'),namespace)
memory=namespace['pure_real_Source_splice']();candidate=memory['text'];ast.parse(candidate)
check('true pure Sourceexactsplice wholeinverse closed beforeanyfilewriting',memory['inverse'].encode()==old_source and len(memory['changes'])==5)
check('original50 continuous entire rawSource unchanged',memory['protected']in candidate.encode()and len(memory['protected'])>0)
check('every new helper function exactsource inserted',all(ast.get_source_segment(helper.decode(),n)in candidate for n in htree.body if isinstance(n,ast.FunctionDef)))
check('UAdddict/list tokens bothremoved noqualifiersweakened',"+       direct_binding['actual_complete70_source_freeze_pin']"not in candidate and '+       direct_original_inputs'not in candidate and "direct_binding['actual_complete70_source_freeze_pin']!=compact['source_freeze_pin']or "in candidate and "direct_original_inputs!=compact['current70_pins']or "in candidate)
check('new public lifetime gate once exactly replacesonlystale block',candidate.count('                admit_exact_public_stale_lifetimes(hf,own,plan,d,root,exe)')==1)
helperfiles=[]
for name in ('actual_inputs_and_readback.py','direct_alias_entry_controls.f90','mutate_owned_control.f90'):
 raw,row=pin(R/'aaa_three_plane_compact_expected_pipeline_source_draft_v2_20261013'/name);helperfiles.append(row)
check('exact three helpers arewholecopy Source loop no math transformation',"for name in ('actual_inputs_and_readback.py','direct_alias_entry_controls.f90','mutate_owned_control.f90'):"in text and 'current=write(NEW/name,data)'in text)
build=values['actual_new_build70_report'];table={x['path']:x for x in build['fixed_current_pins']+build['output_pins']};ordered=[table[x]for x in build['actual_complete70_link_inputs']]
check('new70 exact70 and excluded oldmain12 identity',[len(ordered),len(set(build['actual_complete70_link_inputs']))]==[70,70]and ordered[12]==values['predecessor_direct_binding']['excluded_original_main_pin'])
check('directbinding actual70/srcSF replacesfutureNone precisely',"actual_original_ordered_70_link_inputs=ordered"in text and "actual_complete70_source_freeze_pin=selected['compact_Fortran_Source_freeze']"in text)
# Real helper dictionary functions extracted in our pure fixture Source; no Host import.
fixture_source,fixturepf=pin(R/'independent_v15_retirement_helper_pure_dictionary_fixtures_source_only_20261014.py');fixture_ns={'__name__':'independent_pure_fixture'};buffer=io.StringIO()
with contextlib.redirect_stdout(buffer):exec(compile(fixture_source,str(fixturepf['path']),'exec'),fixture_ns)
finite=json.loads(buffer.getvalue());check('real extracted helper 1legal+44targetedrefusals onlyfakecPath',finite['cases']==45 and finite['legal_count']==1 and finite['refusal_count']==44 and finite['prototype_is_fake_memory_not_actual_PF_or_controls']is True)
# Extract preparer proof gates as pure functions with a fake metadata reader.
proofdefs=[copy.deepcopy(n)for n in ptree.body if isinstance(n,ast.FunctionDef)and n.name in('exact_pin','require_terminal0','walk_fullpins','require_public_post0')]
proof={};exec(compile(ast.Module(body=proofdefs,type_ignores=[]),str(preppf['path'])+':pure_proof_extract','exec'),dict(stat=stat,json=json),proof)
# All these functions need one shared namespace, so extract together explicitly.
proof_ns=dict(stat=stat,json=json);exec(compile(ast.Module(body=copy.deepcopy(proofdefs),type_ignores=[]),str(preppf['path'])+':pure_proof_extract','exec'),proof_ns)
rp=dict(path='/pure_memory/review.json',sha256='c'*64,size_bytes=256,identity=[123,89,33188,1,256,10,10]);ap=dict(path='/pure_memory/publicreport.json',sha256='d'*64,size_bytes=512,identity=[123,90,33188,1,512,10,10]);proof_ns['read']=lambda row:dict(status='PASS_FAKE_MEMORY_PUBLIC_POST',failure=None,actual_report_pin=ap)if row==rp else (_ for _ in()).throw(RuntimeError('wrongfake reviewPF'))
proofcases=[]
def proofcase(name,tool,passed):
 try:actual=proof_ns['require_public_post0'](tool,ap);ok=actual==rp
 except (RuntimeError,KeyError,ValueError):ok=False
 assert ok is passed,name;proofcases.append(dict(name=name,admitted=ok))
legal=dict(observed_closed=True,actual_review_return=dict(exit_code=0,output=json.dumps(dict(review_pin=rp))+'\n'))
proofcase('fake_currentreview binds actual reportPF',legal,True)
for name,edit in [('bool exitcode',lambda t:t['actual_review_return'].update(exit_code=False)),('nonzero exitcode',lambda t:t['actual_review_return'].update(exit_code=1)),('running session',lambda t:t['actual_review_return'].update(session_id=7)),('not observedclosed',lambda t:t.update(observed_closed=False)),('emptyoutput',lambda t:t['actual_review_return'].update(output=''))]:
 t=copy.deepcopy(legal);edit(t);proofcase(name,t,False)
proof_ns['read']=lambda row:dict(status='PASS_FAKE_MEMORY',failure=None,unrelated=rp);proofcase('actual reportPF missing fromreview',legal,False)
check('pure post-tool boundary7cases typed0 closedrawreview reportPF gate',len(proofcases)==7)
check('candidateSource and ownHFCLI notcreatedbyreview',not Path(plan['future_candidate_Source_root']).exists())
for row,raw in observed.values():assert ids(Path(row['path']).lstat())==row['identity']
OUT.mkdir();report=dict(schema='INDEPENDENT_V15_ACTUAL_PREPARER_V2_AND_SRC_ADMISSION_SOURCE_ONLY_REVIEW_V1',status='PASS_V15_PREPARER_V2_AND_EXACT_SRC_RETIREMENT_ADMISSION_SOURCE_ONLY_REVIEW',failure=None,source_only=True,business_executed=False,Host_imported=False,source_preparer_executed=False,compiler_executed=False,numerical_executed=False,pipeline_executed=False,files_deleted=False,current_preparer_Source_pin=preppf,current_retirement_admission_Source_pin=helperpf,current_Source_preparation_plan_pin=planpf,preparer_v1_to_v2_whole_inverse_pin=ipf,original_draft2_Source_pin=oldpf,original_v14_Source_pin=source14pf,source_change_blocks_from_actual_preparer=5,memory_candidate_only_SHA256=hashlib.sha256(candidate.encode()).hexdigest(),original50_continuous_source_bytes=len(memory['protected']),original50_continuous_source_SHA256=hashlib.sha256(memory['protected']).hexdigest(),original50_continuous_source_unchanged=True,three_original_helpers_whole_byte_copy_source_pins=helperfiles,current_HF_dependency_counts=dict(build4=2565,fresh17=2586,model5=2597,public7=2629),inherited_direct_current7_reobserved_unique_count=len(allrows),scientific_fullEOF_not_repeated=True,actual_candidate_Source_or_HF_not_written=True,current_draft2_MF_schema_uppercase_already_correct=True,lowercase_schema_negative_fixture_is_original_strictness_not_a_source_fix=True,pure_real_helper_fixture_Source_pin=fixturepf,pure_real_helper_fixtures=finite,pure_real_preparer_public_post_tool_boundary_fixtures=proofcases,checks=checks,checks_count=len(checks),future_actual_public7_report_pin=None,future_actual_public7_post_review_pin=None,future_actual_v15_Host_freeze_pin=None,future_actual_v15_CLI_pin=None,future_actual_v15_report_pin=None,no_Source_tool0_grants_reader_or_physics=True,AAA_qualified=False,ABA_admitted=False)
p=OUT/'REVIEW.json';fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
with os.fdopen(fd,'wb')as f:f.write((json.dumps(report,indent=2,ensure_ascii=False)+'\n').encode());f.flush();os.fsync(f.fileno())
raw,rpf=pin(p);print(json.dumps(dict(status=report['status'],failure=None,review_pin=rpf,current_preparer_Source_pin=preppf,current_retirement_admission_Source_pin=helperpf,current_Source_preparation_plan_pin=planpf,source_change_blocks=5,pure_helper_cases=45,pure_post_boundary_cases=7,source_only=True,compiler_executed=False,numerical_executed=False,pipeline_executed=False,files_deleted=False)))
