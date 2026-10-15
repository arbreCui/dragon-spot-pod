"""UNREADY Source: retire exact14 completed derived SQL/pool files only after new A closure."""
import argparse,hashlib,importlib.util,json,os,resource,shutil,stat,subprocess,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent
ART=Path('/Users/wen/spot/validation/artifacts')
TARGETS=[{'path': '/Users/wen/spot/validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence/A/000004_postmacro-LIBMIX/complete_native_original_path_index.sqlite', 'sha256': '0ad4ed0bc8624219b492a9d4a9592ea63b92059e8dc56e9de08b11e949ea39f1', 'size_bytes': 12185600, 'identity': [16777229, 50164708, 33188, 1, 12185600, 1791967921993319270, 1791967921993319270]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence/A/000004_postmacro-LIBMIX/complete_native_original_value_bytes.bin', 'sha256': '12fd5f80ca9f270f1123a348124489962d38eb6242aec59e5a533e103f2239b8', 'size_bytes': 9044736, 'identity': [16777229, 50164711, 33188, 1, 9044736, 1791967922259431282, 1791967922259431282]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence/A/000007_oldmacro-pre-LIBMIX/complete_native_original_path_index.sqlite', 'sha256': '0ad4ed0bc8624219b492a9d4a9592ea63b92059e8dc56e9de08b11e949ea39f1', 'size_bytes': 12185600, 'identity': [16777229, 50164716, 33188, 1, 12185600, 1791967922591058982, 1791967922591058982]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence/A/000007_oldmacro-pre-LIBMIX/complete_native_original_value_bytes.bin', 'sha256': '12fd5f80ca9f270f1123a348124489962d38eb6242aec59e5a533e103f2239b8', 'size_bytes': 9044736, 'identity': [16777229, 50164719, 33188, 1, 9044736, 1791967922858817954, 1791967922858817954]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence/A/000008_oldmacro-LIBDEN/complete_native_original_path_index.sqlite', 'sha256': '0ad4ed0bc8624219b492a9d4a9592ea63b92059e8dc56e9de08b11e949ea39f1', 'size_bytes': 12185600, 'identity': [16777229, 50164724, 33188, 1, 12185600, 1791967923184951225, 1791967923184951225]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence/A/000008_oldmacro-LIBDEN/complete_native_original_value_bytes.bin', 'sha256': '12fd5f80ca9f270f1123a348124489962d38eb6242aec59e5a533e103f2239b8', 'size_bytes': 9044736, 'identity': [16777229, 50164727, 33188, 1, 9044736, 1791967923450363818, 1791967923450363818]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence/A/000010_postmacro-LIBMIX/complete_native_original_path_index.sqlite', 'sha256': '945767ecab6454a925e38ac0b4a9791952d5fcd252358eda7bbe58f6af616a17', 'size_bytes': 12435456, 'identity': [16777229, 50164734, 33188, 1, 12435456, 1791967923784417939, 1791967923784417939]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence/A/000010_postmacro-LIBMIX/complete_native_original_value_bytes.bin', 'sha256': '98ba38536abde1da3bb87ba130e761915f8a31dd5d573f53d02a0cec35d074c0', 'size_bytes': 9056608, 'identity': [16777229, 50164737, 33188, 1, 9056608, 1791967924052368997, 1791967924052368997]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence/A/000051_oldmacro-pre-LIBMIX/complete_native_original_path_index.sqlite', 'sha256': '945767ecab6454a925e38ac0b4a9791952d5fcd252358eda7bbe58f6af616a17', 'size_bytes': 12435456, 'identity': [16777229, 50164742, 33188, 1, 12435456, 1791967924385435991, 1791967924385435991]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence/A/000051_oldmacro-pre-LIBMIX/complete_native_original_value_bytes.bin', 'sha256': '98ba38536abde1da3bb87ba130e761915f8a31dd5d573f53d02a0cec35d074c0', 'size_bytes': 9056608, 'identity': [16777229, 50164745, 33188, 1, 9056608, 1791967924657802391, 1791967924657802391]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence/A/000052_oldmacro-LIBDEN/complete_native_original_path_index.sqlite', 'sha256': '945767ecab6454a925e38ac0b4a9791952d5fcd252358eda7bbe58f6af616a17', 'size_bytes': 12435456, 'identity': [16777229, 50164750, 33188, 1, 12435456, 1791967924994098976, 1791967924994098976]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence/A/000052_oldmacro-LIBDEN/complete_native_original_value_bytes.bin', 'sha256': '98ba38536abde1da3bb87ba130e761915f8a31dd5d573f53d02a0cec35d074c0', 'size_bytes': 9056608, 'identity': [16777229, 50164753, 33188, 1, 9056608, 1791967925263881704, 1791967925263881704]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence/A/000054_postmacro-LIBMIX/complete_native_original_path_index.sqlite', 'sha256': '32c4d60fc6bd4f5268f4c098e081dfc07ed638af8bd7badd0129813476d94598', 'size_bytes': 12435456, 'identity': [16777229, 50164758, 33188, 1, 12435456, 1791967925596122905, 1791967925596122905]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence/A/000054_postmacro-LIBMIX/complete_native_original_value_bytes.bin', 'sha256': '44f4a5572f8ec1969d255fffc9c1a351b75438963f3c0d14144bbeeb91beb967', 'size_bytes': 9056608, 'identity': [16777229, 50164761, 33188, 1, 9056608, 1791967925866530759, 1791967925866530759]}]
FALSE=dict(business_executed=False,numerical_executed=False,compiler_executed=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def need(v,m):
 if v is not True:raise RuntimeError(m)
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 need(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'complete integer PF')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and s.st_size==p['size_bytes']and ident(s)==p['identity']and not any(a.is_symlink()for a in(q,*q.parents)),'same ordinary owned current7')
 return q
def current_identity(p):
 need(set(p)=={'path','size_bytes','identity'}and type(p['size_bytes'])is int and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'honest identity-only retained role')
 q=Path(p['path']);s=q.lstat();need(ident(s)==p['identity']and s.st_size==p['size_bytes']and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not any(a.is_symlink()for a in(q,*q.parents)),'retained identity-only7')
def current_metadata(p):
 q=Path(p['path'])
 if q==Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'):
  s=q.lstat();need(p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and p['identity'][3]==s.st_nlink==2 and ident(s)==p['identity']and s.st_size==p['size_bytes']and stat.S_ISREG(s.st_mode)and not any(a.is_symlink()for a in(q,*q.parents)),'sole immutable original compiler metadata exception, never a retirement target')
 else:current(p)
def full(p,budget,parse=False):
 q=current(p);need(not parse or p['size_bytes']<8*2**20,'bounded metadata8MiB')
 digest=hashlib.sha256();parts=[];size=0;fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  need(ident(os.fstat(fd))==p['identity'],'opened7')
  while True:
   raw=os.read(fd,2**20)
   if not raw:break
   digest.update(raw);size+=len(raw)
   if parse:parts.append(raw)
   budget()
  need(ident(os.fstat(fd))==p['identity'],'EOF7')
 finally:os.close(fd)
 current(p);need(size==p['size_bytes']and digest.hexdigest()==p['sha256'],'blind EOF SHA')
 return json.loads(b''.join(parts))if parse else None
def pin(q):
 s=q.lstat();p=dict(path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=ident(s));current(p);return p
def snapshot(f,d):
 raw=(json.dumps(d,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<8*2**20,'receipt8MiB')
 f.seek(0);f.write(raw);f.truncate();f.flush();os.fsync(f.fileno())
def module(p,name,budget):
 full(p,budget);spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current(p);return m

def contains(v,p):
 return v==p or type(v)is dict and any(contains(x,p)for x in v.values())or type(v)is list and any(contains(x,p)for x in v)
def genuine(v,key,expected,output_key):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None,'genuine new A Root/metadata post closed0')
 body=json.loads(t['output'].strip().splitlines()[-1]);need(body[output_key]==expected,'genuine stdout binds exact new closure PF by audited output role')
def admit_completed_new_A(plan,budget):
 need(plan['actual_new_A_business_completed']is True and plan['actual_new_A_post_complete']is True,'future actual new A closure and metadata post mandatory before any target IO')
 need(plan['actual_A_post_key_projection_audited']is True and type(plan['actual_A_post_schema'])is str and type(plan['actual_A_post_status'])is str and type(plan['actual_A_post_host_pin_field'])is str and type(plan['actual_A_post_Root_tools_pin_field'])is str,'actual post schema and exact field roles must be read and audited after genuine closure, no draft guesses')
 pins=plan['closure_pins']
 host=full(pins['new_A_host'],budget,True);root=full(pins['new_A_Root_tools'],budget,True)
 post=full(pins['new_A_post'],budget,True);tools=full(pins['new_A_post_tools'],budget,True)
 genuine(root,'actual_terminal_return',pins['new_A_host'],'report_pin');genuine(tools,'actual_review_return',pins['new_A_post'],'review_pin')
 need(root['actual_execution_permission_mode']=='require_escalated'and root['actual_retried']is False,'genuine completed A2 original permission route and no retry')
 need(host['schema']=='ACTUAL_CURRENT_A_FULL_AGGREGATE_AFTER_OVERV_CONTROL_GUARDED_REPORT_V1'and host['status']=='ACTUAL_CURRENT_A_FULL_MATH_CONTROL_EVIDENCE_EXIT2_CLOSED_ONLY'and host['failure']is None and host['current_source_gap_resolved']is True and host['final_report_resource_check_passed']is True and host['actual_child_evidence_only_integer_exit_code']==2 and host['original_runner_FAILED_record_not_reclassified']is True,'new actual complete A evidence Root0 with original child2/FAILED record retained')
 evidence=host['actual_evidence'];need(evidence['state_order']==['A']and len(evidence['states'])==1 and evidence['error']is None,'exact complete current A state')
 facts=evidence['states'][0]
 need(facts['original_context_event_count']==55 and facts['all_original_snapshot_count']==8 and facts['complete_source_field_comparisons']==19249 and facts['all_mismatching_elements']==0 and facts['unknown_macro_producers']==0 and facts['all_context_or_operand_issues']==0 and len(facts['phase_results'])==6 and all(p['computation_finished']is True for p in facts['phase_results']),'all8trees/55contexts/sixphase/19249 comparisons consumed and complete before retirement')
 control=evidence['current_OVERV_control_admission']
 need(control['status']=='PRIOR_ACTUAL_CURRENT_OVERV_CONTROL_PREADMITTED_METADATA_ONLY'and control['original_issue_fact']['category']=='SOURCE_CONTEXT_NOT_SAVED'and control['issue_count_adjustment_performed']is False,'actual OVERV control resolves only current gap, old issue fact retained')
 need(post['schema']==plan['actual_A_post_schema']and post['status']==plan['actual_A_post_status']and post['failure']is None and post[plan['actual_A_post_host_pin_field']]==pins['new_A_host']and post[plan['actual_A_post_Root_tools_pin_field']]==pins['new_A_Root_tools'],'actual separate metadata post binds true host and Root return by exact audited roles')
 need(post['metadata_only']is True and post['actual_Root_integer_exit_code']==0 and post['actual_child_integer_exit_code']==2 and post['original_FAILED_error2_record_retained']is True and post['actual_compared_source_fields']==19249 and post['actual_snapshot_count']==8 and post['actual_context_event_count']==55 and post['actual_all_mismatch_elements']==post['actual_unknown_macro_producers']==post['actual_context_or_operand_issues']==0 and post['current_source_gap_resolved']is True and post['old_issue1_report_not_rewritten']is True and post['prior_actual_v1_Root1_child1_preserved']is True and post['actual_execution_request_pin']==pins['new_A_execution_request'],'exact actual post facts, original failures and old issue1 preserved')
 request=full(pins['new_A_execution_request'],budget,True);old=full(request['historical_complete_input_request_pin'],budget,True)
 historical={p['path']:p for p in old['complete_input_pins']}
 live={p['path']:p for p in request['complete_input_pins']}
 pairs=request['aggregation_binding']['actual_context_states']['A']['all_snapshot_pairs']
 need(len(old['complete_input_pins'])==5937 and len(pairs)==8 and all(historical.get(p['path'])==p and live.get(p['path'])==p for p in TARGETS),'all exact14 were real historical/current mathematical input guards')
 captured=[]
 for pair in pairs:
  for key in('sqlite_pin','native_pool_pin'):
   if pair[key]in TARGETS:captured.append(pair[key])
 need(len(captured)==14 and{p['path']:p for p in captured}=={p['path']:p for p in TARGETS},'all seven earlier SQL/pool pairs actually consumed under original eight-tree model')
 completed_plan=full(plan['actual_completed_A_plan_pin'],budget,True)
 need(completed_plan['complete_joint_roots']==plan['complete_joint_roots']==request['joint_archive_roots']and len(plan['complete_joint_roots'])==64 and str(Path(pins['new_A_host']['path']).parent)==completed_plan['planned_actual_output_root'],'exact completed A full64 Source plan/resource prefix including failed63 and owning host namespace, never reset')
 for key in('physics_qualified','scientific_accuracy_qualified','complete_reaction_authority_qualified','AAA_qualified','ABA_admitted','goal_complete'):
  need(host[key]is False,'retirement is lifecycle only, no physical qualification')
 return dict(new_A_host_pin=pins['new_A_host'],new_A_Root_tools_pin=pins['new_A_Root_tools'],new_A_post_pin=pins['new_A_post'],new_A_post_tools_pin=pins['new_A_post_tools'],actual_old14_input_scope_consumed=True,old_historical_fullPF_table_unchanged=True,original_child_evidence_exit2_retained=True,byte_identical_regeneration_claim=False,physics_qualified=False)

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--mode',choices=['check','execute'],required=True)
 for role in('source','plan','review'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 ap.add_argument('--readonly-receipt-pin')
 a=ap.parse_args();started=time.monotonic();last=0.0;resources={};ps_samples={'sample_count':0,'sampled_peak_rss_bytes':None,'last_monotonic':0.0,'last_actual_return':None}
 need(all(os.environ.get(k)=='1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'))and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None,'original one-thread nonoptimized/unprofiled environment')
 def budget():
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  need(peak<512*2**20 and time.monotonic()-started<600,'original SELF512/stage600, also whole1800')
  own_bytes=0
  for q in BASE.rglob('*'):
   s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'retirement namespace has no aliases')
   if stat.S_ISREG(s.st_mode):own_bytes+=s.st_size
  need(own_bytes<16*2**20,'entire retirement Source/metadata/receipts16MiB component, unchanged cumulative2GiB')
  if time.monotonic()-ps_samples['last_monotonic']>=0.25:
   command=['/bin/ps','-o','rss=','-p',str(os.getpid())]
   sample=subprocess.run(command,capture_output=True,text=True,timeout=min(2.,max(.05,600-(time.monotonic()-started))))
   need(sample.returncode==0 and sample.stderr==''and len(sample.stdout)<1024 and sample.stdout.strip().isdigit(),'own same-PID original PS RSS command available')
   rss=int(sample.stdout.strip())*1024;need(rss<512*2**20,'unchanged original live PS512MiB cap')
   ps_samples['sample_count']+=1;ps_samples['sampled_peak_rss_bytes']=max(ps_samples['sampled_peak_rss_bytes']or 0,rss);ps_samples['last_monotonic']=time.monotonic();ps_samples['last_actual_return']=dict(argv=command,returncode=sample.returncode,stdout=sample.stdout,stderr=sample.stderr)
  if resources and time.monotonic()-resources['last']>=0.25:
   h=resources['history'].check();j=resources['joint'].check();extra=0
   for p in plan['explicit_cumulative_metadata_file_pins']:
    current_metadata(p)
    if not any(Path(p['path']).is_relative_to(Path(r))for r in plan['complete_joint_roots']):extra+=p['size_bytes']
   unlinked={}
   for fd in os.listdir('/dev/fd'):
    try:s=os.fstat(int(fd))
    except(ValueError,OSError):continue
    if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
   need(j['artifact_bytes']+extra+sum(unlinked.values())<2*2**30,'same complete cumulative2GiB')
   need(h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original history96/cold/meta/fresh2/free8 reservations')
   resources['last']=time.monotonic();resources['latest']=dict(history_bytes=h['artifact_bytes'],joint_bytes=j['artifact_bytes'],history_checked_unix=h['checked_unix'],joint_checked_unix=j['checked_unix'],external_metadata_bytes=extra,open_unlinked_bytes=sum(unlinked.values()),disk_free_bytes=j['disk_free_bytes'],SELF_peak_bytes=peak,elapsed_seconds=time.monotonic()-started)
 def arg(role):
  ids=json.loads(getattr(a,role+'_seven_id'));return dict(path=getattr(a,role+'_summary'),sha256=getattr(a,role+'_sha256'),size_bytes=ids[4],identity=ids)
 ps=arg('source');pp=arg('plan');pr=arg('review')
 need(ps['path']==str(Path(__file__).absolute())and pp['path']==str(BASE/'PLAN.json'),'literal Source/plan')
 receipt=BASE/('READONLY_RECEIPT.json'if a.mode=='check'else'EXECUTION_RECEIPT.json')
 d=dict(schema='LITERAL14_COMPLETED_A_EARLY_EXTRACT_SPOOL_RETIREMENT_RECEIPT_V1',mode=a.mode,status='STARTED',failure=None,source_pin=ps,plan_pin=pp,peer_review_pin=pr,exact_target_pins=TARGETS,actual_released_pins=[],actual_released_bytes=0,files_deleted=False,temporary_derived_SQL_pool_lifecycle_only=True,duplicate_byte_identity_claim=False,all_original_XSM_and_final55_pair_retained=True,original_A_aggregate_issue1_preserved=True,**FALSE)
 with receipt.open('xb')as f:
  try:
   snapshot(f,d);full(ps,budget);plan=full(pp,budget,True);review=full(pr,budget,True)
   need(plan['schema']=='LITERAL14_COMPLETED_A_EARLY_EXTRACT_SPOOL_RETIREMENT_PLAN_V1'and plan['target_pins']==TARGETS and plan['planned_released_bytes']==149659264,'only exact14 genuinely completed derived SQL/pool operands')
   need(review['status'].startswith('PASS')and review['failure']is None and review['source_pin']==ps and review['plan_pin']==pp,'peer same exact Source/plan')
   need(len(plan['complete_joint_roots'])==len(set(plan['complete_joint_roots']))==64,'complete original current64 prefix including failed63; retirement Source already counted in FTOP')
   inputs=module(plan['original_production_inputs_Source_pin'],'production_inputs',budget);need(Path(inputs.__file__).absolute()==Path(plan['original_production_inputs_Source_pin']['path']),'original exact production_inputs import origin')
   production=module(plan['original_production_resource_Source_pin'],'literal3_export_production',budget);factory=module(plan['original_history_resource_Source_pin'],'literal3_export_history',budget)
   resources.update(history=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30,production.ResourceFailure),joint=production.DiskResources(ART.parent,plan['complete_joint_roots'],8*2**30,2*2**30),last=0.0)
   budget();d['resources_before']=resources['latest']
   proof=admit_completed_new_A(plan,budget)
   d['actual_completed_new_A_closure']=proof
   for p in plan['retained_current7_pins']:current_metadata(p)
   for p in plan['retained_identity_only_roles']:current_identity(p)
   for p in TARGETS:full(p,budget)
   d['retained_current7_pins']=plan['retained_current7_pins'];d['closure_pins']=plan['closure_pins'];d['complete_joint_roots']=plan['complete_joint_roots']
   if a.mode=='execute':
    need(a.readonly_receipt_pin is not None,'true readonly receipt')
    pcheck=json.loads(a.readonly_receipt_pin);need(pcheck['path']==str(BASE/'READONLY_RECEIPT.json'),'literal readonly receipt')
    check=full(pcheck,budget,True);need(check['status']=='READONLY_READY_EXACT_LITERAL14_COMPLETED_A_DERIVED_SQL_POOLS'and check['failure']is None and check['source_pin']==ps and check['plan_pin']==pp and check['peer_review_pin']==pr and check['actual_released_pins']==[],'prior exact successful readonly check')
    command=['/usr/sbin/lsof','-n','-P','-Fpcfn','--']+[p['path']for p in TARGETS]
    r=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30,check=False)
    need(len(r.stdout)+len(r.stderr)<2*2**20,'bounded current open-owner check')
    d['actual_lsof_owner_check']=dict(argv=command,returncode=r.returncode,stdout=r.stdout.decode('utf-8'),stderr=r.stderr.decode('utf-8'))
    need(r.returncode==1 and r.stdout==b''and r.stderr==b'','no current open file owner; never unlink live SQLite/pool')
    budget();snapshot(f,d)
    for p in TARGETS:
     q=current(p);fd=os.open(q.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
     try:
      need(ident(os.stat(q.name,dir_fd=fd,follow_symlinks=False))==p['identity'],'immediate target7')
      os.unlink(q.name,dir_fd=fd);d['actual_released_pins'].append(p);d['actual_released_bytes']+=p['size_bytes'];d['files_deleted']=True;os.fsync(fd)
     finally:os.close(fd)
     d['status']='PARTIAL_EXACT_LITERAL14_COMPLETED_A_DERIVED_SQL_POOLS';snapshot(f,d);budget()
    need(d['actual_released_bytes']==149659264 and all(not os.path.lexists(p['path'])for p in TARGETS),'all exact14 derived spools retired')
    d['status']='RETIRED_EXACT_LITERAL14_COMPLETED_A_EARLY_EXTRACT_SPOOLS_ONLY'
   else:d['status']='READONLY_READY_EXACT_LITERAL14_COMPLETED_A_DERIVED_SQL_POOLS'
   for p in plan['retained_current7_pins']:current_metadata(p)
   for p in plan['retained_identity_only_roles']:current_identity(p)
   resources['last']=0.0;fresh_started_unix=time.time();budget()
   need(resources['latest']['history_checked_unix']>=fresh_started_unix and resources['latest']['joint_checked_unix']>=fresh_started_unix,'both unchanged original resource classes actually rescanned after final unlink/check')
   d['resources_after']=resources['latest'];d['resources_after_original_classes_forced_fresh']=True;d['resources_after_fresh_scan_started_unix']=fresh_started_unix;d['resources_after_measured_after_all_requested_unlinks']=a.mode=='execute';d['actual_same_PID_PS_RSS_samples']=dict(ps_samples);snapshot(f,d);budget()
  except BaseException as e:
   d['status']='FAILED_PARTIAL_EXACT_LITERAL14_COMPLETED_A_DERIVED_SQL_POOLS'if d['actual_released_pins']else'FAILED_BEFORE_UNLINK';d['failure']=repr(e);snapshot(f,d);raise
 print(json.dumps(dict(status=d['status'],receipt_pin=pin(receipt),actual_released_bytes=d['actual_released_bytes'],**FALSE)),flush=True)
if __name__=='__main__':main()

