"""Source/metadata-only once writer; does not run the scientific child or host."""
import ast,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent;REC=BASE.parent;ART=REC.parents[1]/'artifacts'
OLD=REC/'saved_three_macro_exact_typed_path_join_source_v1_20261014'
KERNEL=REC/'full370_kernel_origin_component_control_source_v1_20261014/PLAN.json'
EVIDENCE=ART/'axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence/ACTUAL_ELEVEN_SAVED_GENDF_EXTRACTION_EVIDENCE.json'
FINDINGS=REC/'reaction_genDF_stream_source_v1/READONLY_RAW_NX_ALL_TEMPERATURE_SOURCE_FINDINGS.json'
OUT=ART/'axial-material-saved-MT5-NX-raw32-producer-yield-diagnostic-20261014-v1'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,
 history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
 free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(business_executed=False,numerical_executed=False,compiler_executed=False,
 files_deleted=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,
 unreduced_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def require(ok,msg):
 if type(ok)is not bool or not ok:raise RuntimeError(msg)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();require(p.is_absolute()and not any(a.is_symlink()for a in(p,*p.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1,'regular literal Source/metadata one-link')
 with p.open('rb')as f:
  require(identity(os.fstat(f.fileno()))==identity(s),'Source/metadata opened7')
  h=hashlib.file_digest(f,'sha256').hexdigest();require(identity(os.fstat(f.fileno()))==identity(s),'Source/metadata EOF7')
 require(identity(p.lstat())==identity(s),'Source/metadata path7')
 return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=identity(s))
def read(p):
 p=pin(p);require(p['size_bytes']<8*2**20,'bounded Source metadata document');d=json.loads(Path(p['path']).read_bytes());require(pin(p['path'])==p,'same fullmetadataPF');return d,p
def current_only(p):
 q=Path(p['path']);s=q.lstat();require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and q.is_absolute()and not any(a.is_symlink()for a in(q,*q.parents))and stat.S_ISREG(s.st_mode)and identity(s)==p['identity']and s.st_nlink==1,'declared actual producer input fullcurrent7; payload not read during Source generation')
def write(p,v):
 with Path(p).open('x')as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def unique(rows):
 table={}
 for p in rows:
  if p['path']in table:require(table[p['path']]==p,'same path inconsistent fullPF')
  table[p['path']]=p
 return list(table.values())
def segment(p,start,end):
 raw=Path(p).read_bytes();lines=raw.splitlines(keepends=True);part=b''.join(lines[start-1:end]);require(bool(part),'original Source segment')
 return dict(original_source_pin=pin(p),first_line=start,last_line=end,exact_original_statement_bytes_hex=part.hex(),exact_original_statement_sha256=hashlib.sha256(part).hexdigest())
def main():
 targets=[BASE/n for n in('PLAN.json','ORIGINAL_STATEMENT_BYTE_PROOF.json','SOURCE_FREEZE.json','HOST_FREEZE.json','ROOT_REVIEWABLE_CLI.json','SOURCE_REVIEW_READY.json')]
 require(not any(os.path.lexists(p)for p in targets)and not os.path.lexists(OUT),'fresh Source-only once writer; no retry/overwrite')
 old,pold=read(OLD/'PLAN.json');kernel,pkernel=read(KERNEL);e,pe=read(EVIDENCE);find,pfind=read(FINDINGS)
 require(old['schema']=='SAVED_THREE_MACRO_TYPED_PATH_COMPARISON_SOURCE_ONLY_PLAN_V1'and old['source_only']is True and len(old['complete_joint_roots'])==30 and len(old['explicit_cumulative_metadata_file_pins'])==4,'actual latest complete30 plus four explicit metadata roles')
 require(e['schema']=='ACTUAL_CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_EXTRACTION_EVIDENCE_V1'and e['status']=='ACTUAL_ALL_ELEVEN_SAVED_MT5_EXTRACTIONS_CLOSED0_ONLY'and e['complete_reaction_authority_qualified']is False,'actual saved GF11 closed0 only')
 require(tuple(r['nuclide']for r in e['actual_extractions'])==('U235','U238','Fe54','Fe56','Fe57','Fe58','Cr50','Cr52','Cr53','Cr54','Mn55'),'all eleven actual GF references')
 observed,pobserved=read(e['actual_material_observation_report_pin']['path']);require(pobserved==e['actual_material_observation_report_pin'],'same actual formal consumer report fullPF')
 sci=[]
 for name,sha,size in(('DLIB_ACTUAL','e78b87094b67bd4d1bcdc3a5dd2beeb168318853a48321473bb9b86df5ba19cc',210627112),('DLIB8R1_370','66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9',769113024)):
  matches=[p for p in observed['fixed_current_pins']if p['path']==str(ART/'axial-material-inputs-20261003/A'/name)and p['sha256']==sha and p['size_bytes']==size]
  require(len(matches)==1,'one exact actual consumer SCI role '+name);current_only(matches[0]);sci.append(matches[0])
 for r in e['actual_extractions']:current_only(r['actual_complete_extraction_pin'])
 for p in old['explicit_cumulative_metadata_file_pins']:current_only(p)
 dragr=Path('/Users/wen/NJOY2016/src/dragr.f90');groupr=Path('/Users/wen/NJOY2016/src/groupr.f90')
 original_host=OLD/'run_saved_three_macro_typed_path_compare_original_guard.py';host=BASE/'run_saved_MT5_NX_raw32_yield_original_guard.py';child=BASE/'check_saved_MT5_NX_raw32_and_yield.py'
 for p in(child,host,Path(__file__).absolute()):ast.parse(p.read_text(),filename=str(p))
 prior=original_host.read_bytes();candidate=host.read_bytes()
 reused=[]
 for name,end in(('rewrite_summary','def unique'),('unique','def safe_repr'),('safe_repr','class FirstFailure'),('FirstFailure','def main')):
  token=('class 'if name=='FirstFailure'else'def ')+name
  start=prior.index(token.encode());stop=prior.index(end.encode(),start);part=prior[start:stop]
  require(part in candidate,'complete original host helper statement bytes '+name)
  reused.append(dict(original_host_source_pin=pin(original_host),statement=name,original_begin_byte=start,original_end_byte=stop,whole_original_statement_sha256=hashlib.sha256(part).hexdigest(),whole_original_statement_exactly_reused=True))
 proof=dict(schema='SAVED_MT5_NX_ORIGINAL_SOURCE_STATEMENT_BYTES_V1',source_only=True,original_formula_segments=[segment(dragr,728,741),segment(dragr,993,1008),segment(dragr,1010,1044),segment(dragr,2219,2258),segment(groupr,8025,8035),segment(groupr,8082,8095)],original_guard_helpers=reused,original_native_byte_extractor_source_pin=pin(REC/'current_material_evidence_compare_three_after_GENDF_cumulative_resources_source_v7_20261014/complete_observed_old_post_final_XSM_extractor.UNREADY.py'),producer_rounding='source REAL default binary32 cast after original binary64 nonzero tail test; no fit/no renormalization',selective_SCI_decoder='original xsmdir 8-word header plus cap*6-word arrays; chosen named directory extents only; no complete walk',**FALSE)
 write(targets[1],proof);pproof=pin(targets[1])
 roots=kernel['complete_joint_roots']+[str(BASE),str(OUT)]
 require(len(kernel['complete_joint_roots'])==32 and set(old['complete_joint_roots']).issubset(kernel['complete_joint_roots'])and len(roots)==34 and len(set(roots))==34,'exact actual kernel32 plus NX Source/output, all prior30 preserved')
 explicit=unique(kernel['explicit_cumulative_metadata_file_pins'])
 for p in explicit:current_only(p)
 plan=dict(schema='SAVED_MT5_NX_RAW32_YIELD_SOURCE_ONLY_PLAN_V1',source_only=True,planned_actual_output_root=str(OUT),actual_GENDF_evidence_pin=pe,original_NX_findings_pin=pfind,actual_formal_SCI_consumer_report_pin=pobserved,actual_current_SCI1_pin=sci[0],actual_current_SCI2_context_only_pin=sci[1],historical_NX_inventory_content_correspondence_only=True,historical_identity_not_reissued=True,selected_original_guard_plan_pin=pold,selected_current_kernel_cumulative_plan_pin=pkernel,original_Common_Source_pin=old['original_Common_Source_pin'],original_support_Source_pin=old['original_support_Source_pin'],original_bounded_Source_pin=old['original_bounded_Source_pin'],complete_joint_roots=roots,explicit_cumulative_metadata_file_pins=explicit,original_caps=CAPS,original_statement_byte_proof_pin=pproof,expected_unique_nuclides=11,expected_temperature_records=79,scope='NX original producer all-temperature raw32 only, saved MF6-MF3 MT5 yield diagnostic; no dilution/SPH/MASK/kernel/reference qualification',**FALSE)
 write(targets[0],plan);pplan=pin(targets[0])
 sources=unique([pin(child),pin(host),pin(Path(__file__).absolute()),pin(dragr),pin(groupr),proof['original_native_byte_extractor_source_pin'],pin(original_host),pproof])
 deps=unique([pold,pkernel,pe,pfind,pobserved,pplan,pproof]+sci+[r['actual_complete_extraction_pin']for r in e['actual_extractions']]+explicit+[old['original_Common_Source_pin'],old['original_support_Source_pin'],old['original_bounded_Source_pin']]+sources)
 sf=dict(schema='SAVED_MT5_NX_RAW32_YIELD_SOURCE_ONLY_FREEZE_V1',candidate_executed=False,source_only=True,control_plan_pin=pplan,child_source_pin=pin(child),complete_source_file_pins=sources,original_caps=CAPS,**FALSE);write(targets[2],sf);psf=pin(targets[2])
 hf=dict(schema='SAVED_MT5_NX_RAW32_YIELD_HOST_SOURCE_ONLY_FREEZE_V1',candidate_executed=False,source_only=True,selected_source_freeze_pin=psf,host_source_pin=pin(host),dependencies=deps,original_caps=CAPS,**FALSE);write(targets[3],hf);phf=pin(targets[3])
 argv=[str(host),'--source-freeze-summary',psf['path'],'--source-freeze-sha256',psf['sha256'],'--source-freeze-seven-id',json.dumps(psf['identity'],separators=(',',':')),'--host-freeze-summary',phf['path'],'--host-freeze-sha256',phf['sha256'],'--host-freeze-seven-id',json.dumps(phf['identity'],separators=(',',':'))]
 support=Path(old['original_support_Source_pin']['path']).read_text();require("PYTHON"in support,'original support declaration available')
 # The interpreter is copied from the actual existing recipe; no inferred binary.
 recipe,precipe=read(OLD/'ROOT_REVIEWABLE_SAVED_THREE_MACRO_TYPED_PATH_ACTUAL24_ARGV.json');require(type(recipe['argv'])is list and recipe['argv'].count(str(original_host))==1,'actual prior complete guard argv');argv=recipe['argv'][:recipe['argv'].index(str(original_host))]+argv
 cli=dict(schema='SAVED_MT5_NX_RAW32_YIELD_REVIEWABLE_CLI_SOURCE_ONLY_V1',argv=argv,original_guard_recipe_pin=precipe,source_freeze_pin=psf,host_freeze_pin=phf,planned_actual_output_root=str(OUT),**FALSE);write(targets[4],cli)
 ready=dict(schema='SAVED_MT5_NX_RAW32_YIELD_SOURCE_REVIEW_READY_V1',source_only=True,selected_Source_pins=[pin(p)for p in targets[:-1]],core_AST_parsed=True,host_AST_parsed=True,science_payload_read=False,original_SCI_directory_or_NX_read=False,actual_business_started=False,**FALSE);write(targets[5],ready)
 print(json.dumps(dict(status='SOURCE_ONLY_SAVED_MT5_NX_RAW32_YIELD_READY',ready_pin=pin(targets[5]),**FALSE)))
if __name__=='__main__':main()
