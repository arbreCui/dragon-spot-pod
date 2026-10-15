from pathlib import Path
import ast,hashlib,json,os,time,resource
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011');V4=REC/'current_formal_material_authority_exact_cache70_source_v5';V5=REC/'current_formal_material_authority_exact_cache70_source_v6';O=REC/'current_formal_material_authority_handle_lifetime69_source_v2';D=REC/'material_exact_cache70_v6_author_finite_source_review_20261013';D.mkdir(exist_ok=True);checks=[];start=time.monotonic()
def req(x,label):assert type(x)is bool and x,label;checks.append(label)
def pin(p):
 s=p.lstat()
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns])
def funcs(p):
 b=p.read_text();return{n.name:ast.get_source_segment(b,n)for n in ast.parse(b).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
for p in V5.glob('*.py'):ast.parse(p.read_bytes())
for p in V5.glob('*.py'):
    old=(V4/p.name).read_text();new=p.read_text()
    if p.name=='build_current_observation_runtime.py':
        a="SOURCE=REC/'current_formal_material_authority_exact_cache70_source_v5'";z="SOURCE=REC/'current_formal_material_authority_exact_cache70_source_v6'"
        req(old.count(a)==new.count(z)==1 and old.replace(a,z)==new and new.replace(z,a)==old,'sole precise executing build namespace changes complete forward/reverse')
    elif p.name=='current_material_prerequisite_admission.py':
        a='actual prerequisite must consume exact frozen v9 host Source';z='actual prerequisite must consume exact frozen v10 host Source'
        req(old.count(a)==new.count(z)==1 and old.replace(a,z)==new and new.replace(z,a)==old,'sole precise guard error text current v10 Source binding inverse')
    else:req(old==new,'all other complete9 numerical/gate/host byte identities preserved '+p.name)
req(funcs(V4/'current_material_prerequisite_admission.py')['check_original_host_limits']==funcs(V5/'current_material_prerequisite_admission.py')['check_original_host_limits'],'full original v5 finalwhole1800/SELF512 guard function byte exact')
req(funcs(V4/'current_material_prerequisite_admission.py')['replace_owned_failure_summary']==funcs(V5/'current_material_prerequisite_admission.py')['replace_owned_failure_summary'],'full original sameownedFD honest failure publisher byte exact')

inv=json.loads((V4/'COMPLETE_CURRENT70_CURRENT_MATERIAL_SOURCE_INVERSE.json').read_bytes())
for row in inv['entire_byte_copy_pins']:
 p=Path(row['copy']['path']);req(p.read_bytes()==(V5/p.name).read_bytes(),'whole exact original copiedmath/18Source '+p.name)
for file,names in [('produce_current_formal_material_observations.py',['original_shared_libraries','prepare_shared_libraries','recheck_shared_libraries','derive_original_procedure','copy_state_seeds','collect_state','release_closed_owned_library_copies']),('current_material_lineage_evidence.py',['Budget','extract','aggregate','compare_raw_macro','source_admission','admit_owning_stage'])]:
 a=funcs(O/file);b=funcs(V5/file)
 for name in names:req(a[name]==b[name],'whole original science/library/capture body exact '+name)
for file in('build_current_observation_runtime.py','produce_current_formal_material_observations.py','run_current_material_lineage_evidence.py','current_material_lineage_evidence.py','prepare_current_material_evidence_requests.py'):
 a=ast.parse((V4/file).read_bytes());b=ast.parse((V5/file).read_bytes());req([n.value for n in ast.walk(a)if isinstance(n,ast.Constant)and type(n.value)in(int,float)]==[n.value for n in ast.walk(b)if isinstance(n,ast.Constant)and type(n.value)in(int,float)],'all existing original numeric constants exact v4→v5 '+file)
 if file in('current_material_lineage_evidence.py','prepare_current_material_evidence_requests.py'):req((V4/file).read_bytes()==(V5/file).read_bytes(),'whole metadata/science entry unchanged v4→v5 '+file)
# Inspect authoritative actual completed v8 data field contract. The failed
# aggregate is deliberately not prerequisite-admitted or changed to PASS.
p=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v9/Root_actual_three_plane_engineering_summary.json');real=json.loads(p.read_bytes());table={p['path']:p for p in real['output_pins']};cases={c['original_execution_record_index']:c for c in real['actual_operator_refusals']};observed=[]
for i,r in enumerate(real['records']):
 if r['status']=='PASS':req('log_sha256'in r,'real actual positive record owns log_sha256 '+r['label'])
 elif i in cases:
  req('log_sha256'not in r,'real actual expected-negative record has no fabricated log_sha256 '+r['label']);c=cases[i]
  lp=str(p.parent/(r['label']+'.log'));wp=str(p.parent/(r['label']+'.watchdog.json'))
  req(c['original_execution_record_label']==r['label']and c['actual_log_pin']==table[lp]and c['actual_watchdog_pin']==table[wp],'true actual expected-negative matched originalindex label/full logwatchPF '+r['label'])
  req(r['error']=='own-child stage failed; no retry'and c['actual_exit_code']==1 and c['actual_abort_message_exact']is True,'true actual expected-negative originalrecord/refusalverdict '+r['label'])
  req(pin(Path(lp))==c['actual_log_pin']and pin(Path(wp))==c['actual_watchdog_pin']and Path(lp).read_text().count(c['expected_abort'])==1,'true readonly fullEOF logwatch and one originalexpectedabort '+r['label'])
  observed.append(dict(actual_record_index=i,original_record_keys=list(r),refusal_keys=list(c),original_stage_label=r['label']))
req(len(observed)>20,'real v9 genuineexpectednegative field shape broadly observed; final unexpectedfailure not admitted')
helper=(V5/'current_material_prerequisite_admission.py').read_text();tree=ast.parse(helper)
# Only PASS branch may access the absent-on-FAILED original log_sha256.
def log_keys(n):return[a for a in ast.walk(n)if isinstance(a,ast.Subscript)and isinstance(a.value,ast.Name)and a.value.id=='compact'and isinstance(a.slice,ast.Constant)and a.slice.value=='log_sha256']
lognodes=log_keys(tree);req(len(lognodes)==1,'one sole originalcompact.logsha access')
branches=[n for n in ast.walk(tree)if isinstance(n,ast.If)and ast.unparse(n.test)=="compact['status'] == 'PASS'"]
req(len(branches)==1 and len(log_keys(ast.Module(body=branches[0].body,type_ignores=[])))==1 and len(log_keys(ast.Module(body=branches[0].orelse,type_ignores=[])))==0,'PASS only guards solecompact.logsha; FAILED never accessesmissing field')
req("case['actual_log_pin']==table[str(lp)]and case['actual_watchdog_pin']==table[str(wp)]"in helper and "set(refusals)=={i for i,r in enumerate(boot['records'])if r['status']=='FAILED'}"in helper,'all33 FAILED exactindex cover and wholePF logwatch authority retained')
req("time.monotonic()-start<1800"in funcs(V5/'current_material_prerequisite_admission.py')['check_original_host_limits']and 'ru_maxrss<512*2**20'in funcs(V5/'current_material_prerequisite_admission.py')['check_original_host_limits'],'actual elapsedwhole1800 and SELF512 exact postpublication guard function')
# Actual control-flow Source checks: after final successful write/scan call,
# guard is inside same try whose except writes failure through exact owned FD.
for file in('build_current_observation_runtime.py','run_current_material_lineage_evidence.py'):
 b=(V5/file).read_text();t=ast.parse(b);main=next(n for n in t.body if isinstance(n,ast.FunctionDef)and n.name=='main')
 final=next(n for n in reversed(main.body)if isinstance(n,ast.Try));calls=[ast.unparse(n)for n in final.body]
 req(calls[-1]=='check_original_host_limits(c, start)'and any('resources.check()'in v for v in calls[:-1]),'final literal elapsed/RSS guard follows resource scan '+file)
 exceptbody='\n'.join(ast.unparse(n)for handler in final.handlers for n in handler.body)
 req('FAILED'in exceptbody and 'replace_owned_failure_summary'in exceptbody,'finalcap failure publishes truthful sameownedFD FAILED '+file)
prod=(V5/'produce_current_formal_material_observations.py').read_text();main=next(n for n in ast.parse(prod).body if isinstance(n,ast.FunctionDef)and n.name=='main');final=next(n for n in reversed(main.body)if isinstance(n,ast.Try))
req(ast.unparse(final.body[-1])=='check_original_host_limits(c, start)'and 'replace_owned_failure_summary'in'\n'.join(ast.unparse(n)for h in final.handlers for n in h.body),'producer final manifest forces elapsed/RSS guard and truthful sameFD FAILED owningphase')
budget=next(n for n in ast.walk(main)if isinstance(n,ast.FunctionDef)and n.name=='budget');req(ast.unparse(budget.body[-1])=='check_original_host_limits(c, start)'and ast.unparse(budget.body[-2])=='resources.check()','producer phase-budget postscan guard covers summarypublication as well')
phasechecks=[n for n in main.body if isinstance(n,ast.Try)and any(isinstance(q,ast.Expr)and isinstance(q.value,ast.Call)and isinstance(q.value.func,ast.Name)and q.value.func.id=='budget'for q in n.body)and 'replace_owned_failure_summary'in'\n'.join(ast.unparse(v)for h in n.handlers for v in h.body)];req(len(phasechecks)==1 and 'replace_owned_failure_summary'in'\n'.join(ast.unparse(n)for h in phasechecks[0].handlers for n in h.body),'producer phase-finalcheck uses guardedbudget under honestfailurepublisher')
result=dict(schema='AUTHOR_PREFREEZE_MATERIAL_V6_ACTUAL_RECORD_SHAPE_AND_FINAL_GUARD_SOURCE_REVIEW',status='PRE_FREEZE_PRECISE_SOURCE_REVIEW_PASS_NO_IMPORT_OR_BUSINESS',check_count=len(checks),all_checks=checks,all10_python_whole_AST_read=True,whole18_mathcopies_and_original13_science_capture_functions_equal=True,actual_v9_failed_aggregate_pin=pin(p),actual_v9_failure_deliberately_not_admitted=True,actual_genuine_expected_negative_count_observed=len(observed),actual_negative_record_fields=observed,whole_finalguard_control_flow_verified_not_just_numericconstants=True,new_physical_or_numerical_sources_changed=False,candidate_imported_or_executed=False,compiler_or_material_or_science_business_started=False,Source_frozen_by_this_review=False,wall_seconds=time.monotonic()-start,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
with(D/'PRE_FREEZE_ACTUAL_FIELD_AND_FINAL_GUARD_REVIEW.json').open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(status=result['status'],checks=len(checks),actual_v9_expected_negative_shapes=len(observed),review_pin=pin(D/'PRE_FREEZE_ACTUAL_FIELD_AND_FINAL_GUARD_REVIEW.json'))))
