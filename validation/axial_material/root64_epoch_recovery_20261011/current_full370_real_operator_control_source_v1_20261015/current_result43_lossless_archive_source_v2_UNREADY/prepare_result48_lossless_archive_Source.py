"""Root-only metadata preparation. Requires real early14 closure PFs; never archives bytes."""
import argparse,ast,hashlib,importlib.util,json,os,stat,sys,time
from pathlib import Path

BASE=Path(__file__).absolute().parent
SOURCE_NAMES=('result43_archive_common.UNREADY.py','archive_result43_serial.UNREADY.py',
 'run_guarded_result43_lossless_archive.UNREADY.py','prepare_result48_lossless_archive_Source.py',
 'write_once_result48_archive_SF_HF_CLI.py')

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def bootstrap_metadata(p):
 q=Path(p['path']);s=q.lstat()
 if not(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()
  and identity(s)==p['identity']and p['size_bytes']==s.st_size<8*2**20
  and not any(x.is_symlink()for x in(q,*q.parents))):raise RuntimeError('strict bounded metadata PF')
 raw=q.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=p['sha256']or identity(q.lstat())!=p['identity']:raise RuntimeError('metadata wholeEOF SHA/current7')
 return json.loads(raw)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('author','latest-plan','early14-receipt','early14-root-tools','early14-post','early14-post-tools'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 for role in('schema','status','receipt-pin-field','root-tools-pin-field'):ap.add_argument('--early14-post-'+role,required=True)
 a=ap.parse_args();started=time.monotonic()
 with (BASE/'ROOT_SOURCE_PREPARATION_CLAIM.json').open('x')as f:
  json.dump(dict(schema='RESULT48_ARCHIVE_SOURCE_PREPARATION_EXCLUSIVE_ONCE_CLAIM_V1',PID=os.getpid(),started=started,argv=sys.argv,business_executed=False,retries=0),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 def argument(role):
  n=role.replace('-','_');ids=json.loads(getattr(a,n+'_seven_id'))
  return dict(path=getattr(a,n+'_summary'),sha256=getattr(a,n+'_sha256'),size_bytes=ids[4],identity=ids)
 pa=argument('author');author=bootstrap_metadata(pa)
 if not(author['schema']=='RESULT48_ARCHIVE_V2_PRE_ROOT_SOURCE_FREEZE_V1'
  and author['Source_files_frozen_before_Root_generation']is True
  and all(author[k]is False for k in('Source_preparation_executed_by_author','Source_publication_executed_by_author','business_executed_by_author','old_plain_payload_opened_by_author'))):raise RuntimeError('exact prior author Source-only freeze')
 table={p['path']:p for p in author['source_pins']};pc=table[str(BASE/'result43_archive_common.UNREADY.py')]
 q=Path(pc['path']);s=q.lstat();raw=q.read_bytes()
 if identity(s)!=pc['identity']or hashlib.sha256(raw).hexdigest()!=pc['sha256']:raise RuntimeError('whole frozen common Source bootstrap')
 spec=importlib.util.spec_from_file_location('result48_archive_preparation_common',q);c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c);c.current7(pc)
 c.require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None
  and all(os.environ.get(k)=='1'for k in c.THREADS)and Path(sys.executable).resolve()==c.PYTHON,'original Sourcegen interpreter/env/thread1')
 c.require(set(table)=={str(BASE/n)for n in SOURCE_NAMES},'exact complete5 owning Source files')
 for p in table.values():c.require(c.pin(p['path'])==p,'whole author frozen Source');ast.parse(Path(p['path']).read_text())
 seed=c.metadata(author['metadata_seed_pin']);c.require(seed['draft_unready']is True and seed['Source_admission_ready']is False
  and seed['actual_retired_early14_pins']is None and all(v is None for v in seed['early14_closure_pins'].values()),'preserved NULL unready seed; no invented future PF')
 old=c.metadata(seed['prior_frozen_archive_draft_pin'])
 c.require(old['status']=='UNREADY_DRAFT_FROZEN_STOP_WRITES_NOT_ADMITTED'
  and old['Source_admission_ready']is False and old['compression_executed']is False,'old immutable archive draft provenance')
 pLatest=argument('latest-plan');latest=c.metadata(pLatest);prefix=latest['complete_joint_roots']
 c.require(prefix[:64]==seed['completed_A2_complete64_roots']and len(prefix)>=64
  and latest['original_caps']==c.CAPS,'latest original full cumulative prefix/caps, not an independent ledger')
 ep={k:argument(role)for k,role in [('receipt','early14-receipt'),('Root_tools','early14-root-tools'),('post','early14-post'),('post_tools','early14-post-tools')]}
 c.require(all(p['path'].startswith(str(BASE.parent/'current_A_early14_extract_spool_retirement_source_v2')+'/')for p in ep.values()),'real fresh early14v2 closure roles, old failedv1 remains historical')
 receipt=c.metadata(ep['receipt']);post=c.metadata(ep['post'])
 c.require(a.early14_post_status.startswith('PASS')and a.early14_post_receipt_pin_field in post
  and a.early14_post_root_tools_pin_field in post,'actual post keys audited at Sourcegen, no field guesses')
 targets=receipt['actual_released_pins']
 projections=dict(schema=a.early14_post_schema,status=a.early14_post_status,
  receipt_pin_field=a.early14_post_receipt_pin_field,Root_tools_pin_field=a.early14_post_root_tools_pin_field)
 # The common admission re-reads actual receipt/post, checks typed original0 returns and exact14 PFs.
 plan=dict(seed,schema='RESULT43_LOSSLESS_ARCHIVE_EXECUTION_BINDING_V1',source_only=True,
  draft_unready=False,prerequisite_binding_complete=True,Source_admission_ready=False,
  actual_retired_early14_pins=targets,early14_closure_pins=ep,early14_post_actual_role_projection=projections,
  early14_actual_key_projection_Source_reviewed=True,early14_actual_retirement_and_post0_verified=True,
  inherited_latest_plan_pin=pLatest,inherited_latest_complete_joint_roots=prefix,
  complete_joint_roots=prefix+[seed['planned_actual_output_root']],Source_preparation_does_not_mint_final_peer_admission=True,
  Root_actual_exec_command_sandbox_permissions_required='require_escalated',formal_Source_peer_passed=False,
  Source_author_freeze_pin=pa,actual_early14_receipt_verified_at_Sourcegen=True)
 explicit=[];seen={}
 for p in latest['explicit_cumulative_metadata_file_pins']+[pa,pLatest]+list(ep.values()):
  if p['path']in seen:c.require(seen[p['path']]==p,'same historical metadata path exactPF')
  else:seen[p['path']]=p;explicit.append(p)
 plan['explicit_cumulative_metadata_file_pins']=explicit
 out=c.admit(plan)
 c.require(not os.path.lexists(out)and not any(os.path.lexists(BASE/n)for n in('PLAN.json','SOURCE_REVIEW_READY.json','FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json','FINAL_PUBLICATION_RECEIPT.json','ROOT_ARCHIVE_EXECUTION_CLAIM.json')),'fresh preparation/publication/business namespaces; no retry')
 for p in explicit:c.current_metadata(p)
 resources=c.Resources(plan,started,600);before=resources.check()
 c.require(before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']
  +before['own_open_unlinked_bytes']+c.OUT_CAP+c.SOURCE_CAP<2*2**30,'strict coexisting plain+192MiB archive+16MiB Source fit, no compression ratio')
 c.require(not any(os.path.lexists(Path(seed['prior_frozen_archive_draft_pin']['path']).parent/n)for n in('ROOT_ARCHIVE_EXECUTION_CLAIM.json','PLAN.json','SOURCE_REVIEW_READY.json','FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json')),'earlier archive draft never generated/published/executed; pending output reused honestly')
 def write_generated(name,value):
  raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
  c.require(len(raw)<8*2**20 and c.own_bytes(BASE)+len(raw)<c.SOURCE_CAP,'whole Source metadata each8MiB/entire Source16MiB before write')
  return c.write_new(BASE/name,value,8*2**20)
 pPlan=write_generated('PLAN.json',plan)
 cli=c.metadata(seed['completed_A2_CLI_pin']);envprefix=cli['argv'][:11]
 c.require(len(envprefix)==11 and envprefix[0]=='/usr/bin/env'and envprefix[-1]=='-B'
  and envprefix[-2]==str(c.PYTHON),'whole original ENV/Python/-B prefix from actual completed A2 CLI')
 meta=[pa,author['metadata_seed_pin'],seed['prior_frozen_archive_draft_pin'],seed['prior_metadata_seed_pin'],pLatest,
  seed['original_result43_registry_pin'],seed['original_result43_old_input_intersection_pin'],seed['completed_A2_plan_pin'],
  seed['completed_A2_host_pin'],seed['completed_A2_Root_tools_pin'],seed['completed_A2_post_pin'],seed['completed_A2_post_tools_pin'],
  seed['completed_A2_CLI_pin'],seed['retained_native_source_metadata_pin']]+list(ep.values())
 metadata_selection={p['path']:p for p in meta+list(table.values())+[pPlan]}
 for p in metadata_selection.values():c.require(c.pin(p['path'])==p,'selected Source/report metadata fullEOF/current7')
 ready=dict(schema='RESULT48_LOSSLESS_ARCHIVE_SOURCE_REVIEW_READY_V1',source_only=True,control_plan_pin=pPlan,
  execution_binding_pin=pPlan,host_source_pin=table[str(BASE/'run_guarded_result43_lossless_archive.UNREADY.py')],
  common_source_pin=pc,final_publisher_Source_pin=table[str(BASE/'write_once_result48_archive_SF_HF_CLI.py')],
  complete_source_file_pins=list(table.values()),selected_Source_pins=list(metadata_selection.values()),
  dependencies=list(metadata_selection.values()),old48_plain_and_retained66_current7_only_pins=plan['all48_plain_pins']+plan['retained_native_current7_pins'],
  original_complete_ENV_Python_B_prefix=envprefix,original_caps=c.CAPS,
  actual_business_started=False,Root_final_publication_executed=False,formal_Source_peer_passed=False,
  Root_actual_exec_command_sandbox_permissions_required='require_escalated',**c.FALSE)
 pReady=write_generated('SOURCE_REVIEW_READY.json',ready);resources.check()
 for p in metadata_selection.values():c.require(c.pin(p['path'])==p,'same metadata fullEOF after Source preparation')
 for p in ready['old48_plain_and_retained66_current7_only_pins']:c.current7(p)
 print(json.dumps(dict(status='RESULT48_LOSSLESS_ARCHIVE_SOURCE_PREPARATION_ONLY',ready_pin=pReady,plan_pin=pPlan,
  business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)

if __name__=='__main__':main()
