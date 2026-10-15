from pathlib import Path
import ast,hashlib,json,os,resource,stat,time
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';S=REC/'current_formal_material_authority_exact_cache70_source_v6';OLD=REC/'current_formal_material_authority_handle_lifetime69_source_v2';start=time.monotonic();checks=[];full={};readbytes=0
out=REC/'material_exact_cache70_v6_author_finite_source_review_20261013';out.mkdir(exist_ok=True)
def req(v,msg):
 assert type(v)is bool and v,msg;checks.append(msg)
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def fullpin(p):
 global readbytes
 p=Path(p);before=ident(p.lstat());req(p.is_absolute()and stat.S_ISREG(before[2]),'regular fullEOF '+str(p))
 with p.open('rb')as f:
  req(ident(os.fstat(f.fileno()))==before,'opened7ID '+str(p));h=hashlib.sha256();size=0
  while True:
   b=f.read(2**20)
   if not b:break
   h.update(b);size+=len(b)
  req(ident(os.fstat(f.fileno()))==before,'fullEOF descriptor7ID '+str(p))
 req(ident(p.lstat())==before and size==before[4],'fullEOF path7ID/size '+str(p));readbytes+=size
 result=dict(path=str(p),sha256=h.hexdigest(),size_bytes=size,identity=before)
 if str(p)in full:req(full[str(p)]==result,'one current fullpin '+str(p))
 full[str(p)]=result;return result

def verify(p):req(fullpin(p['path'])==p,'all four fullPF fields exact '+p['path'])
def load(p):raw=Path(p).read_bytes();return json.loads(raw)
catpath=REC/'current_mount_identity_reattestation_20261012/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json';catalog=load(catpath)
req(catalog['schema']=='CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG_V1'and len(catalog['rows'])==3040,'exact current catalog3040 scope')
def key(p):
 if type(p)is dict and all(n in p for n in('path','sha256','size_bytes','identity'))and type(p['identity'])is list:
  return p['path'],p['sha256'],p['size_bytes'],tuple(p['identity'])
 return None
mapping={key(row['historical_pin']):row['current_pin']for row in catalog['rows']}
def view(d):
 if isinstance(d,dict):
  k=key(d);r={k1:view(v)for k1,v in d.items()}
  if k in mapping:r.update(mapping[k])
  return r
 if isinstance(d,list):return[view(v)for v in d]
 return d
for row in catalog['rows']:verify(row['current_pin'])
math=load(S/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json');hf=load(S/'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json');phf=load(S/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json');ehf=load(S/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json');esf=load(S/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json');cli=load(S/'ROOT_REVIEWABLE_CURRENT70_OBSERVER75_STATIC_ARGV_AND_REQUIRED_ACTUAL_GATES_SOURCE_ONLY.json');plan=load(S/'CURRENT_FORMAL_MATERIAL_AUTHORITY_SELECTED_CACHE70_PLAN.json');inverse=load(S/'COMPLETE_CURRENT70_CURRENT_MATERIAL_SOURCE_INVERSE.json')
for p in [hf['host_source'],phf['host_source'],ehf['host_source']]+hf['dependencies']+phf['dependencies']+ehf['dependencies']+esf['complete_source_file_pins']+math['files']+math['original_math_sources']+[math['current_plan_pin']]:
 if p['path']not in full:verify(p)
 else:req(full[p['path']]==p,'identical known fullPF '+p['path'])
req(hf['required_actual_AAA3_output_directory']=='/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v10','exact Root-selected future actual v10 output directory, no predicted PF')
v10pin=hf['required_actual_AAA3_host_freeze_pin'];verify(v10pin)
req(v10pin['sha256']=='aa75076e2ff7819eb164cecfd927b9485559b2282b0f7ac5ea9c8a5d9ead6861'and v10pin['identity']==[16777229,50013648,33188,1,146046,1791870345211171880,1791870345211171880],'exact current actual v10 SourceHF SHA/all7ID')
v10sf=load(v10pin['path']);req(len(v10sf['dependencies'])==278,'complete current frozen v10 Source278 dependencies')
for row in [v10sf['host_source']]+v10sf['dependencies']:verify(row)
req(v10pin in hf['dependencies']and v10sf['host_source']in hf['dependencies'],'material whole buildSource freeze protects exact selected v10 host/HF current pins')
req(hf['selected_source_freeze_pin']==fullpin(S/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json'),'buildHF owns exact complete mathSF')
req(math['current_plan_pin']==fullpin(S/'CURRENT_FORMAL_MATERIAL_AUTHORITY_SELECTED_CACHE70_PLAN.json'),'mathSF owns exact current70 plan')
req(plan['current_seed_plan_pin']==phf['selected_seed_plan_pin']==fullpin(S/'CURRENT_FORMAL_COMPLETE_AB_ORIGINAL_MATERIAL_SEED_PLAN_SOURCE_ONLY.json'),'plan and producerHF own exact unchanged physical seed plan')
req(phf['selected_build_host_freeze_pin']==fullpin(S/'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json'),'producer binds whole actual75 owning buildHF Source only')
req(ehf['host_source']['path']==str(S/'run_current_material_lineage_evidence.py')and esf['schema']=='COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_ONLY_FREEZE_V1','evidence schemas exact original protocol retained')
for p in inverse['old_frozen_package_fullpins']:verify(p)
for row in inverse['entire_byte_copy_pins']:
 verify(row['original']);verify(row['copy']);req(Path(row['original']['path']).read_bytes()==Path(row['copy']['path']).read_bytes(),'entire18 math and numerical helper copies unchanged '+Path(row['copy']['path']).name)
# Full old/new AST and complete function/class source equality.
asts={}
for directory in(OLD,S):
 for p in directory.glob('*.py'):asts[str(p)]=ast.parse(p.read_bytes());checks.append('entire PythonAST parsed '+str(p))
req(len(list(S.glob('*.py')))==10,'all10 complete current Python Sources parsed without import')
def funcs(p):
 raw=p.read_text();return{n.name:ast.get_source_segment(raw,n)for n in ast.parse(raw).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
pold=funcs(OLD/'produce_current_formal_material_observations.py');pnew=funcs(S/'produce_current_formal_material_observations.py')
for name in('original_shared_libraries','prepare_shared_libraries','recheck_shared_libraries','derive_original_procedure','copy_state_seeds','collect_state','release_closed_owned_library_copies'):req(pold[name]==pnew[name],'entire original actual capture/library lifecycle body unchanged '+name)
fold=funcs(OLD/'current_material_lineage_evidence.py');fnew=funcs(S/'current_material_lineage_evidence.py')
for name in('Budget','extract','aggregate','compare_raw_macro','source_admission','admit_owning_stage'):req(fold[name]==fnew[name],'entire original fullscope science/budget body unchanged '+name)
req((OLD/'prepare_current_material_evidence_requests.py').read_bytes()==(S/'prepare_current_material_evidence_requests.py').read_bytes(),'entire original actual evidence request producer unchanged')
def nums(p):return{n.value for n in ast.walk(asts[str(p)])if isinstance(n,ast.Constant)and type(n.value)in(int,float)}
for name in('produce_current_formal_material_observations.py','run_current_material_lineage_evidence.py'):
 req(nums(OLD/name)==nums(S/name),'all numeric constants preserved exact '+name)
oldnums=nums(OLD/'build_current_observation_runtime.py');newnums=nums(S/'build_current_observation_runtime.py')
req(oldnums-newnums=={74}and newnums-oldnums=={3,9,70,75},'build numeric differences only actual70 count75 three cache stages and old9 retention')
for name in('build_current_observation_runtime.py','produce_current_formal_material_observations.py','run_current_material_lineage_evidence.py'):
 req('20971764748'in(S/name).read_text()and'20971764758'not in(S/name).read_text(),'exact original cold20971764748 no draft10B mutation '+name)
# Validate all statically referenced literal HF fields exist.
for name,data in [('build_current_observation_runtime.py',hf),('produce_current_formal_material_observations.py',phf),('run_current_material_lineage_evidence.py',ehf),('current_material_prerequisite_admission.py',hf)]:
 for n in ast.walk(asts[str(S/name)]):
  if isinstance(n,ast.Subscript)and isinstance(n.value,ast.Name)and n.value.id=='hf'and isinstance(n.slice,ast.Constant):req(n.slice.value in data,'hostHF literal field present '+name+' '+str(n.slice.value))
# Genuine current70 + predecessor69 fullEOF & actual stages/log/watch, no candidate import.
bp=hf['selected_actual_build70_report'];b=view(load(bp['path']));verify(bp)
req(b['schema']=='ACTUAL_NATIVE_RANK1_EXACT_BLOCK_CACHE_COMPLETE70_BUILD_ONLY_V2'and b['status']=='ACTUAL_TWO_CACHE_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'and len(b['records'])==3 and b['final_report_resource_check_passed']is True,'true actual current70 three-stage closure selected')
records=[]
for d,p,cnt in [(b,bp,3)]+[(view(load(b[k]['path'])),b[k],n)for k,n in [('original_actual69_handle_lifetime_report_pin',2),('original_actual69_v4_report_pin',10)]]:
 verify(p);req(d['failure']is None and d['after_check_error']is None and d['Dragon_linked']is True and len(d['records'])==cnt,'actual ordered build report closure '+p['path'])
 for q in d['fixed_current_pins']+d['output_pins']:
  if q['path']not in full:verify(q)
  else:req(full[q['path']]==q,'prerequisite complete current PF '+q['path'])
 root=Path(p['path']).parent
 for r in d['records']:
  wp=root/(r['label']+'.watchdog.json');lp=root/(r['label']+'.log');w=load(wp);fullpin(wp);actual=fullpin(lp)
  req(r['status']=='PASS'and w['command']==r['command']and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and 0<=w['sampled_peak_rss_mib']<512 and actual['sha256']==r['log_sha256'],'genuine actual closed0 command/log/watch '+r['label'])
 records.append(d)
current69=records[1];original69=records[2];l70=b['records'][-1]['command'][3:-2];l69=current69['records'][-1]['command'][3:-2];o69=original69['records'][-1]['command'][3:-2]
req(len(l70)==70 and l70==b['actual_complete70_link_inputs']and len(l69)==69 and len(o69)==69,'exact actual70/current69/original69 full order')
req([i for i,(a,z)in enumerate(zip(o69,l69))if a!=z]==[37],'original69 to handle69 only actual driver37 changed')
req(Path(l70[57]).name=='SPOT1P64.o'and next(i for i,p in enumerate(l69)if p.endswith('.a'))==57,'true cache helper insertion before first original archive57')
strip=l70[:57]+l70[58:];req([i for i,(a,z)in enumerate(zip(l69,strip))if a!=z]==[37],'remove actual cache helper and restoredriver37 gives exact69')
req([q['path']for q in b['original_current69_ordered_input_pins']]==l69,'actual70 full current69 pinned inverse exact')
req(inverse['complete70_order']==l70 and inverse['observer_insertion_zero_based_index_in70']==58 and len(inverse['observer_objects'])==5 and len(inverse['complete75_order'])==75,'complete new75 full ordered input plan exact')
req([p for p in inverse['complete75_order']if p not in inverse['observer_objects']]==l70 and [p for p in inverse['complete75_order']if p.endswith('.a')]==[p for p in l70 if p.endswith('.a')],'exact all70 and same4 archive order in75')
req(inverse['complete75_order'][57]==l70[57]and inverse['complete75_order'][58:63]==inverse['observer_objects']and inverse['complete75_order'][63:67]==[p for p in l70 if p.endswith('.a')],'SPOT1P64 helper retained at57 five observers58:62 before same4archives63:66')
req(plan['current_actual70_build_report_pin']==bp==phf['selected_actual_build70_report']and hf['new_link_input_count']==75 and hf['planned_stage_count']==6,'all plan/HF actual70+fivecompile+75link counts agree')
# The dynamic future gates are required but no success values/7ID guessed.
source=(S/'build_current_observation_runtime.py').read_text();gates=(S/'current_material_prerequisite_admission.py').read_text();psrc=(S/'produce_current_formal_material_observations.py').read_text()
req("['current70','source-freeze','host-freeze','aaa3','saved-audit']"in source and "parser.add_argument('--'+prefix+'-'+suffix,required=True)"in source,'mandatory external actual AAA3 and saved audit SHA/all7ID flags')
req(cli['is_complete_executable_argv']is False and cli['incomplete_until_Root_supplies_actual_completed_receipts']is True and len(cli['mandatory_actual_arguments_to_append'])==6,'Source-only static CLI honestly incomplete until true receipts exist')
req(hf['future_actual_receipts_not_predicted_or_pinned']is True and phf['future_actual75_report_not_predicted_or_pinned']is True and 'selected_observer75_report_pin'not in phf,'no future actual report identity guessed')
req("load('observer75')"in psrc and "build['fixed_current_pins'].count(hf['selected_build_host_freeze_pin'])==1"in psrc and "build['current70_actual_origin']==hf['selected_actual_build70_report']"in psrc,'dynamic actual75 report authentic complete current70 and whole buildSource origin')
req("len(raw['records'])==50"in gates and "sum(r['status']=='PASS'for r in boot['records'])==17"in gates and "sum(r['status']=='FAILED'for r in boot['records'])==33"in gates and 'all_payload_bits_equal'in gates,'actual future AAA3 gate validates full50/17/33 and sealedpair bits')
req("(result['groups'],result['regions'],result['axial_cells'])==(370,8,48)"in gates and "result['axes']['unknown_NDIM3_R_indices_0based']==[1,3,4,5,7,8]"in gates,'actual future audit scopefull370/48 unchanged unknownsix')
req('replace_owned_failure_summary'in source and 'replace_owned_failure_summary'in psrc and 'replace_owned_failure_summary'in(S/'run_current_material_lineage_evidence.py').read_text(),'all3 hosts force postsummary resourcecheck with honest same-owned-FD failure publication')
compiler=fullpin(b['records'][0]['command'][0]);req(compiler['identity'][3]==2 and compiler==inverse['compiler_exact_immutable_role_pin'],'sole immutable compiler exact original nlink2 fullPF')
child=(S/'current_material_lineage_evidence.py').read_text();req('expected==COMPILER_EXACT_ROLE_PIN'in child and 'identity(before)==COMPILER_EXACT_ROLE_PIN'in child,'nlink2 exception restricted to complete exact compiler role, owned singlelink unchanged')
req([(p['path'],p['identity'][3])for p in b['fixed_current_pins']if p['identity'][3]!=1]==[(compiler['path'],2)],'compiler only linked immutable actual70 input')
# Every current fullPF source declaration was actually verified; historical
# embedded old JSON annotations are not silently reissued as live inputs.
for p in sorted(S.iterdir()):
 if p.is_file():fullpin(p)
review=dict(schema='AUTHOR_FINITE_CURRENT70_OBSERVER75_COMPLETE_SOURCE_ONLY_REVIEW_V6',status='AUTHOR_SOURCE_ONLY_FULL_EOF_AND_FIELDS_PASS_PENDING_ROOT_INDEPENDENT_REVIEW',check_count=len(checks),unique_full_EOF_current_files=len(full),unique_current_bytes=sum(p['size_bytes']for p in full.values()),actual_read_bytes=readbytes,complete_AST_Source_count=10,complete_original_byte_copy_count=18,complete70_order=l70,complete75_order=inverse['complete75_order'],planned_actual_build_stages=6,source_package=str(S),compiler_only_exact_nlink2_pin=compiler,root_required_actual_AAA3_and_saved_full370_gate_receipts_unavailable_at_source_time=True,future_actual_pins_not_predicted=True,all_numeric_math_and_original_caps_preserved=True,actual_PREFREEZE_field_and_finalguard_review_pin=fullpin(out/'PRE_FREEZE_ACTUAL_FIELD_AND_FINAL_GUARD_REVIEW.json'),actual_prefreeze_true_tool_chunk='53b226',actual_prefreeze_exit_code=0,all_checks=checks,whole_old_new_Source_inverse_pin=fullpin(S/'COMPLETE_CURRENT70_CURRENT_MATERIAL_SOURCE_INVERSE.json'),build_host_freeze_pin=fullpin(S/'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json'),math_source_freeze_pin=fullpin(S/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json'),CLI_Source_pin=fullpin(S/'ROOT_REVIEWABLE_CURRENT70_OBSERVER75_STATIC_ARGV_AND_REQUIRED_ACTUAL_GATES_SOURCE_ONLY.json'),SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-start,candidate_Source_imported=False,compiler_executed=False,material_job_executed=False,evidence_or_science_executed=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
with(out/'AUTHOR_COMPLETE_FINITE_SOURCE_REVIEW.json').open('x')as f:json.dump(review,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(status=review['status'],check_count=len(checks),unique_full_EOF_current_files=len(full),unique_current_bytes=review['unique_current_bytes'],SELF_peak_bytes=review['SELF_peak_bytes'],wall_seconds=review['wall_seconds'],review=fullpin(out/'AUTHOR_COMPLETE_FINITE_SOURCE_REVIEW.json'))))
