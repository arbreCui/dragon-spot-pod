"""Final publication, metadata, and original live resource guard review only."""
import ast,hashlib,importlib.util,json,os,resource,stat,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('previous_frozen_source_metadata_primitives',BASE/'independent_source_review_20261014/review_source_only.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
require,current,whole,read,pin=old.require,old.current,old.whole,old.read,old.pin
FLAGS=old.FLAGS+old.PHYSICS
def module(p,name):
 whole(p);spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);whole(p);return m
def main():
 started=time.monotonic();failure=None;facts={};selected=[]
 try:
  ready=read(old.READY);gen=read(old.GEN);plan=read(ready['control_plan_pin'])
  selected=ready['selected_Source_pins']+[old.READY,old.GEN]
  require(len(ready['selected_Source_pins'])==191 and len(selected)==193,'all original selected191 plus ready/gen')
  for p in selected:whole(p)
  psf=pin(BASE/'FINAL_SOURCE_FREEZE.json');phf=pin(BASE/'FINAL_HOST_FREEZE.json');pcli=pin(BASE/'FINAL_ROOT_REVIEWABLE_CLI.json');ppub=pin(BASE/'FINAL_PUBLICATION_RECEIPT.json')
  ptools=pin(BASE/'ROOT_FINAL_ONCE_PUBLICATION_TRUE_TOOL_RETURNS.json');pargv=pin(BASE/'ROOT_EXACT_ACTUAL24_ARGV.json')
  sf,hf,cli,pub,pt,argv=[read(p)for p in(psf,phf,pcli,ppub,ptools,pargv)]
  require(all(ready[k]is False for k in FLAGS),'original complete false scope retained')
  final_flags=tuple(k for k in FLAGS if k!='current_SPH_MASK_context_applied')
  for d in(sf,hf,cli,pub):require(all(d[k]is False for k in final_flags),'same published explicit Source-only qualifiers stay false')
  require(sf['source_only']is True and hf['source_only']is True and sf['candidate_executed']is False and hf['candidate_executed']is False
    and sf['control_plan_pin']==ready['control_plan_pin'] and hf['selected_source_freeze_pin']==psf
    and hf['host_source_pin']==ready['host_source_pin'] and cli['source_freeze_pin']==psf and cli['host_freeze_pin']==phf
    and pub['final_source_freeze_pin']==psf and pub['final_host_freeze_pin']==phf and pub['final_CLI_pin']==pcli
    and sf['original_caps']==hf['original_caps']==ready['original_caps']==plan['original_caps']==old.CAPS,'exact final publication Source/Host/CLI crossbinds')
  proof=pub['peer_and_generation_proof'];require(proof==sf['Root_same_round_peer_and_generation_proof']==hf['Root_same_round_peer_and_generation_proof']==cli['Root_same_round_peer_and_generation_proof'],'same Root publication proof all4')
  peer=read(proof['peer_review_pin']);peerTools=read(proof['peer_true_tools_pin'])
  require(proof['Source_generation_true_tools_pin']==old.GEN and proof['selected_Source_only_ready_pin']==old.READY
    and pub['selected_Source_pins']==selected and peer['source_only']is True and peer['status'].startswith('PASS') and peer['failure']is None
    and peer['selected_Source_pins']==selected and all(peer[k]is False for k in FLAGS),'same true prepublication peer and generation complete scope')
  t=peerTools['actual_review_return'];require(peerTools['observed_closed']is True and type(peerTools['original_integer_exit_code'])is int and peerTools['original_integer_exit_code']==0
    and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None
    and json.loads(t['output'])['review_pin']==proof['peer_review_pin'],'genuine peer typedclosed0 stdout')
  g=gen['actual_Source_preparation_return'];require(gen['observed_closed']is True and type(g['exit_code'])is int and g['exit_code']==0 and g.get('session_id')is None
    and json.loads(g['output'])['ready_pin']==old.READY,'genuine Source-generation typedclosed0')
  t=pt['actual_publication_return'];require(type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None
    and json.loads(t['output'])['receipt_pin']==ppub and json.loads(t['output'])['status']=='ROOT_FINAL_FOUR_ORIGINAL_ASCII_INFINITE_SCAT_SOURCE_PUBLICATION_ONLY','genuine Root sole final publication typedclosed0')
  require(len(argv)==24 and argv==cli['argv'] and argv[:11]==ready['original_complete_ENV_Python_B_prefix']
    and argv[11]==ready['host_source_pin']['path']
    and argv[12:18]==['--source-freeze-summary',psf['path'],'--source-freeze-sha256',psf['sha256'],'--source-freeze-seven-id',json.dumps(psf['identity'],separators=(',',':'))]
    and argv[18:24]==['--host-freeze-summary',phf['path'],'--host-freeze-sha256',phf['sha256'],'--host-freeze-seven-id',json.dumps(phf['identity'],separators=(',',':'))],'exact24 original env/Python/-B/final SF/HF argv')
  require(sf['complete_source_file_pins']==ready['complete_source_file_pins']+[old.READY]
    and all(p in hf['dependencies']for p in ready['dependencies'])
    and all(p in hf['dependencies']for p in(old.READY,old.GEN,proof['peer_review_pin'],proof['peer_true_tools_pin']))
    and len(hf['dependencies'])==195 and len(hf['explicit_cumulative_metadata_file_pins'])==183,'complete final dependency and resource metadata scope')
  for p in hf['dependencies']:whole(p)
  for p in sf['complete_source_file_pins']:whole(p)
  roots=plan['complete_joint_roots'];prior=read(plan['selected_prior45_plan_pin'])
  require(len(roots)==47 and roots==prior['complete_joint_roots']+[str(BASE),plan['planned_actual_output_root']]
    and not Path(plan['planned_actual_output_root']).exists(),'original45 exact prefix47 and fresh OUT absent')
  for p in hf['explicit_cumulative_metadata_file_pins']:whole(p)
  retirement=read(hf['actual_precise_retirement_receipt_pin'])
  require(hf['actual_precise_retirement_receipt_pin']==plan['actual_precise_retirement_receipt_pin']
    and retirement['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY' and retirement['mode']=='execute'
    and retirement['failure']is None and retirement['actual_released_bytes']==405417320
    and retirement['actual_released_pins']==retirement['exact_target_pins'] and len(retirement['actual_released_pins'])==4
    and all(not os.path.lexists(p['path'])for p in retirement['actual_released_pins']),'same exact historical4 retirement receipt and absent paths')
  current(plan['actual_current_SCI1_pin'])
  for row in plan['inputs']:current(row['gzip_primary_current_full_pin'])
  for key in('actual_original_ASCII_evidence_pin','actual_original_ASCII_independent_post_pin','actual_original_ASCII_independent_post_tools_pin','completed_one_track_post_context_pin','completed_one_track_post_tools_context_pin'):read(plan[key])
  source=read(plan['original_whole_math_inverse_proof_pin']);sci_original=next(c for c in source['whole_original_source_copies']if Path(c['whole_unchanged_copy_full_pin']['path']).name=='original_bounded_SCI_helpers.py')
  raw=whole(sci_original['whole_unchanged_copy_full_pin']);require(raw==whole(sci_original['original_full_pin'])
    and b'0<=n<=262144' in raw and b'os.pread(self.fd,4*n,4*at)'in raw,'original raw/directory/lookup class unchanged and262144-word cap')
  host=whole(ready['host_source_pin']).decode();require("SCI1_whole_PF_verified_by_original_parent_before_child=True"in host
    and "c.same_pin(p['path'],p)"in host and "if p!=plan['actual_current_SCI1_pin']:c.same_pin(p['path'],p)"in host,'SCI1 fullSHA before initial child; subsequent stat exact7 distinct from initial SHA')
  support=module(plan['original_support_Source_pin'],'original_guard_support_final_light')
  helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'original_guard_helper_final_light')
  factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'original_resource_factory_final_light')
  full,production=helper.modules();guard_files=helper.guard_admission(full)
  require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)
    and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'live original owning class/MRO Source')
  joined=production.DiskResources(Path('/Users/wen/spot/validation'),roots,8*2**30,2*2**30).check()
  history=factory.DynamicHistoryResources(Path('/Users/wen/spot/validation/artifacts'),factory.history_roots([],Path('/Users/wen/spot/validation/artifacts')),8*2**30,96*2**30,production.ResourceFailure).check()
  outer=sum(p['size_bytes']for p in hf['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots))
  unlinked={}
  for fd in os.listdir('/dev/fd'):
   try:s=os.fstat(int(fd))
   except(ValueError,OSError):continue
   if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
  require(joined['artifact_bytes']+outer+sum(unlinked.values())<2*2**30
    and history['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30
    and joined['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'live original2GiB/cold20GiB/meta64MiB/history96/free8 reservations')
  facts=dict(final_source_freeze_pin=psf,final_host_freeze_pin=phf,final_CLI_pin=pcli,final_publication_receipt_pin=ppub,
    genuine_Root_final_publication_true_tools_pin=ptools,exact_Root_actual24_argv_pin=pargv,
    actual_SCI1_current7_only_pin=plan['actual_current_SCI1_pin'],actual_gzip_primary_current7_only_pins=[r['gzip_primary_current_full_pin']for r in plan['inputs']],
    original_source_review_pin=proof['peer_review_pin'],original_source_review_true_tools_pin=proof['peer_true_tools_pin'],
    original_source_generation_true_tools_pin=old.GEN,complete_joint_roots=roots,explicit_cumulative_metadata_file_pins=hf['explicit_cumulative_metadata_file_pins'],
    actual_live_original_joined_guard=joined,actual_live_original_complete_history_guard=history,
    actual_explicit_outer_metadata_bytes=outer,actual_open_unlinked_bytes=sum(unlinked.values()),
    actual_complete_cumulative_bytes=joined['artifact_bytes']+outer+sum(unlinked.values()),original_caps=old.CAPS,
    live_original_guard_class_MRO_current=True,initial_whole_SCI1_SHA_separate_from_subsequent_exact7_checks=True,
    original_BoundedSCI_raw262144_word_limit_unchanged=True,exact_actual24_matches_final_CLI=True,
    exact_four_retired_paths_still_absent=True,future_business_OUT_absent=True)
  for p in selected+[psf,phf,pcli,ppub,ptools,pargv]:whole(p)
 except BaseException as exc:failure=repr(exc)
 report=dict(schema='INDEPENDENT_FINAL_FOUR_ORIGINAL_ASCII_INFINITE_SCAT_LIGHT_REVIEW_V1',
   status='PASS_FINAL_ROOT_PUBLISHED_FOUR_ASCII_INFINITE_SCAT_METADATA_LIGHT_ONLY'if failure is None else'FAIL_FINAL_FOUR_ASCII_INFINITE_SCAT_METADATA_LIGHT',
   failure=failure,source_only=True,selected_Source_pins=selected,audit_source_pin=pin(Path(__file__)),
   scientific_payload_read=False,gzip_decompressed_by_peer=False,SCI_payload_read_by_peer=False,business_rerun_by_peer=False,
   **{k:False for k in FLAGS},**facts,elapsed_seconds=time.monotonic()-started)
 target=OUT/'REVIEW.json'
 with target.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=report['status'],review_pin=pin(target),source_only=True,**{k:False for k in FLAGS})),flush=True)
 require(failure is None,'final light review retained failure '+str(failure))
if __name__=='__main__':main()
