from pathlib import Path
import ast,hashlib,json,os,resource,stat,time
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';OLD=REC/'current_formal_material_authority_exact_cache70_source_v6';NEW=REC/'current_formal_material_authority_exact_cache70_source_v7';D=REC/'material_exact_cache70_v7_author_finite_source_review_20261013';START=time.monotonic();checks=0;full={}
def req(ok,why):
 global checks
 checks+=1
 if not ok:raise AssertionError(why)
 if time.monotonic()-START>=1800 or resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20:raise RuntimeError('original own512/whole1800 audit caps')
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,expected=None):
 p=Path(p);a=p.lstat();i=identity(a)
 req(stat.S_ISREG(a.st_mode)and i[0]==16777229,'ordinary currentDEV29 '+str(p))
 if expected is not None:req(i==expected['identity'],'all7ID selected before read')
 if str(p)in full:
  q=full[str(p)];req(q['identity']==i,'one immutable currentPF');req(expected is None or q==expected,'same completePF reused');return q
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();n=0
 try:
  req(identity(os.fstat(fd))==i,'sameFD opened7ID')
  while True:
   b=os.read(fd,2**20)
   if not b:break
   h.update(b);n+=len(b)
  req(identity(os.fstat(fd))==i,'sameFD all7ID at wholeEOF')
 finally:os.close(fd)
 req(identity(p.lstat())==i and n==i[4],'path all7ID at wholeEOF')
 q=dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,identity=i);req(expected is None or q==expected,'allPF selected SHA/stat exact');full[str(p)]=q;return q
def read(p):
 q=pin(p);raw=Path(p).read_bytes();req(hashlib.sha256(raw).hexdigest()==q['sha256']and identity(Path(p).lstat())==q['identity'],'wholeJSON currentPF');return json.loads(raw)
CAT=REC/'current_mount_identity_reattestation_20261012/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json';cat=read(CAT);req(len(cat['rows'])==3040,'complete currentCatalog3040')
def key(p):
 if type(p)is dict and all(k in p for k in('path','sha256','size_bytes','identity')):return p['path'],p['sha256'],p['size_bytes'],tuple(p['identity'])
def view(x):
 if type(x)is list:return[view(v)for v in x]
 if type(x)is dict:
  r={k:view(v)for k,v in x.items()};k=key(x)
  if k in mapping:r.update(mapping[k])
  return r
 return x
mapping={key(r['historical_pin']):r['current_pin']for r in cat['rows']}
for row in cat['rows']:
 a=row['historical_pin'];b=row['current_pin'];req(a['identity'][0]in(16777234,16777229)and b['identity'][0]==16777229 and a['identity'][1:]==b['identity'][1:]and a['sha256']==b['sha256']and a['size_bytes']==b['size_bytes']and a['path']==b['path'],'exact onlydevice transition old34/current29→actual29');pin(b['path'],b)
BIND=REC/'current_mount_full_identity_common_source_v1/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json';bind=read(BIND)
req(len(bind['fixed_current_pins'])==2012,'complete Common2012 inputs')
for q in bind['fixed_current_pins']:pin(q['path'],q)
pin(REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py')
inv=read(OLD/'COMPLETE_CURRENT70_CURRENT_MATERIAL_SOURCE_INVERSE.json');req(len(inv['entire_byte_copy_pins'])==18,'full18 immutable math/numerical Source copies')
for row in inv['entire_byte_copy_pins']:
 pin(row['original']['path'],row['original']);pin(row['copy']['path'],row['copy']);a=Path(row['copy']['path']);b=NEW/a.name;pin(b);req(a.read_bytes()==b.read_bytes(),'complete18 old→new mathcopy byte exact')
for p in sorted(OLD.rglob('*')):
 if p.is_file():pin(p)
for p in OLD.glob('*.py'):
 a=p.read_bytes();b=(NEW/p.name).read_bytes();ast.parse(a);ast.parse(b)
 if p.name=='build_current_observation_runtime.py':x=b"SOURCE=REC/'current_formal_material_authority_exact_cache70_source_v6'";z=b"SOURCE=REC/'current_formal_material_authority_exact_cache70_source_v7'"
 elif p.name=='current_material_prerequisite_admission.py':x=b'actual prerequisite must consume exact frozen v10 host Source';z=b'actual prerequisite must consume exact frozen v11 host Source'
 else:req(a==b,'allothercompletePythonSource byte exact '+p.name);continue
 req(a.count(x)==b.count(z)==1 and a.replace(x,z)==b and b.replace(z,x)==a,'sole2 precise literal Source deltas '+p.name)
 req([n.value for n in ast.walk(ast.parse(a))if isinstance(n,ast.Constant)and type(n.value)in(int,float)]==[n.value for n in ast.walk(ast.parse(b))if isinstance(n,ast.Constant)and type(n.value)in(int,float)],'every numeric cap/math ASTvalue exact '+p.name)
V11=REC/'aaa_three_plane_streaming_pipeline_source_v11';hf=read(V11/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json');vp=pin(V11/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')
req(vp['sha256']=='2597f653ebb8d24e454d0f129efb1db1f623073e4524b9ce0b560d54ade56736'and vp['identity']==[16777229,50017634,33188,1,163351,1791873144732798330,1791873144732798330],'real immutable v11HF allPF')
req(len(hf['dependencies'])==308,'complete308v11 Sources/dependencies')
for q in [hf['host_source']]+hf['dependencies']:pin(q['path'],q)
oldhf=read(OLD/'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json');bp=oldhf['selected_actual_build70_report'];pin(bp['path'],bp);build=view(read(bp['path']))
req(build['status']=='ACTUAL_TWO_CACHE_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'and len(build['records'])==3 and build['failure']is None and build['after_check_error']is None,'actual70 true3stage buildauthority')
reports=[build]+[view(read(build[k]['path']))for k in('original_actual69_handle_lifetime_report_pin','original_actual69_v4_report_pin')]
for d in reports:
 for q in d['fixed_current_pins']+d['output_pins']:pin(q['path'],q)
 req(d['failure']is None and d['after_check_error']is None and d['Dragon_linked']is True,'original complete69/70 truebuild closed0')
 for r in d['records']:req(r['status']=='PASS','no reclassified oldbuild failure')
l70=build['records'][-1]['command'][3:-2];l69=reports[1]['records'][-1]['command'][3:-2];o69=reports[2]['records'][-1]['command'][3:-2]
req(len(l70)==70 and len(l69)==len(o69)==69 and l70==build['actual_complete70_link_inputs'],'allcomplete actual70/69 order')
req([i for i,(a,b)in enumerate(zip(o69,l69))if a!=b]==[37],'actual69 only original driver37 changed')
req(Path(l70[57]).name=='SPOT1P64.o'and[i for i,(a,b)in enumerate(zip(l69,l70[:57]+l70[58:]))if a!=b]==[37],'original69→actual70 only cachehelper57 plusdriver37')
at=next(i for i,p in enumerate(l70)if p.endswith('.a'));req(at==58,'fourarchives firstat58')
order=['AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90','LIBMIX.observe.UNREADY.f','LIBDEN.observe.UNREADY.f','TONDRV.context_observe.UNREADY.f','TONSPH.observe.UNREADY.f'];out=R/'validation/artifacts/axial-material-new-current-material-observer-complete75-build-only-20261013-v7';added=[str(out/'build'/(Path(n).stem+'.o'))for n in order];l75=l70[:58]+added+l70[58:]
req(len(l75)==75 and l75[58:63]==added and[p for p in l75 if p not in added]==l70 and[p for p in l75 if p.endswith('.a')]==[p for p in l70 if p.endswith('.a')],'full70→75 complete order/math preservation')
compiler=pin(build['records'][0]['command'][0]);req(compiler==inv['compiler_exact_immutable_role_pin'],'compiler exact fullPF/nlink2 role unchanged')
for q in full.values():req(q['identity'][3]==1 or q==compiler,'only compiler immutable nlink2 exact role')
for n in('COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json','COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json','COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json'):
 d=read(OLD/n)
 for q in[d['host_source']]+d['dependencies']:pin(q['path'],q)
sf=read(OLD/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json');seed=read(OLD/'CURRENT_FORMAL_COMPLETE_AB_ORIGINAL_MATERIAL_SEED_PLAN_SOURCE_ONLY.json')
for st in('A','B'):
 for row in seed['states'][st]['native_stage_inputs']:pin(row['input_pin']['path'],row['input_pin'])
field=read(D/'PRE_FREEZE_ACTUAL_FIELD_AND_FINAL_GUARD_REVIEW.json');req(field['check_count']==181 and field['actual_genuine_expected_negative_count_observed']==26 and field['whole_finalguard_control_flow_verified_not_just_numericconstants']is True,'allactualv9negativefield/finalguard controlflow reviewed before Sourcefreeze')
for p in NEW.iterdir():
 if p.is_file():pin(p)
report=dict(schema='AUTHOR_PREFREEZE_MATERIAL_V7_COMPLETE_CURRENT_EOF_SOURCE_AND_MATH_ORDER_REVIEW_V1',status='PREFREEZE_COMPLETE_STATIC_CURRENT_PF_MATH_70_TO_75_PASS',checks=checks,unique_full_EOF_files=len(full),unique_full_EOF_bytes=sum(q['size_bytes']for q in full.values()),all_verified_current_file_pins=list(full.values()),old_v6_full_tree_unchanged=True,complete_old_new_AST_read_no_import=True,complete18math_byte_exact=True,Source_code_delta_count=2,selected_real_v11_HF_pin=vp,complete70_order=l70,planned75_order=l75,original_caps=sf['original_caps'],actual_negative_field_and_finalguard_review_pin=pin(D/'PRE_FREEZE_ACTUAL_FIELD_AND_FINAL_GUARD_REVIEW.json'),future_actual_report_pins_not_predicted=True,Source_frozen_by_this_audit=False,candidate_imported=False,compiler_or_business_executed=False,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-START,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
with(D/'PRE_FREEZE_COMPLETE_CURRENT_PF_AND_MATH_ORDER_REVIEW.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=report['status'],checks=checks,unique_EOF=len(full),unique_bytes=report['unique_full_EOF_bytes'],review_pin=pin(D/'PRE_FREEZE_COMPLETE_CURRENT_PF_AND_MATH_ORDER_REVIEW.json'),wall_seconds=time.monotonic()-START)))
