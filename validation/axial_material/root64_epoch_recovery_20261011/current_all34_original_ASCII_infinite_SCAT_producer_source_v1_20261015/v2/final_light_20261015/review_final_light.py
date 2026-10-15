"""Final LIGHT same-round Source/metadata check; never launch the actual host."""
import ast,hashlib,json,os,shutil,stat,time
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
ART=Path('/Users/wen/spot/validation/artifacts')
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
FLAGS=('business_executed','numerical_executed','compiler_executed','files_deleted')
QUALIFIERS=('finite18_replayed','temperature_interpolation_replayed','physics_qualified','scientific_accuracy_qualified','complete_reaction_authority_qualified','physical_neutron_balance_qualified','unreduced_reference_qualified','AAA_qualified','ABA_admitted','goal_complete')
SCIENCE=set()
def require(ok,msg):
 if type(ok) is not bool or not ok:raise RuntimeError(msg)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();compiler=str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15' and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492' and p['identity'][3]==2
 require(q.is_absolute() and not any(a.is_symlink() for a in(q,*q.parents)) and stat.S_ISREG(s.st_mode) and s.st_nlink==(2 if compiler else 1) and identity(s)==p['identity'] and s.st_size==p['size_bytes'],'exact final current7 '+str(q))
def whole(p):
 current(p);require(p['path'] not in SCIENCE and p['size_bytes']<8*2**20,'bounded final Source/metadata only')
 with Path(p['path']).open('rb') as f:
  require(identity(os.fstat(f.fileno()))==p['identity'],'opened final metadata7');raw=f.read();require(identity(os.fstat(f.fileno()))==p['identity'],'EOF final metadata7')
 require(len(raw)==p['size_bytes'] and hashlib.sha256(raw).hexdigest()==p['sha256'],'whole final Source/metadata SHA');current(p);return raw
def pin(q):
 q=Path(q);s=q.lstat();require(str(q) not in SCIENCE and s.st_size<8*2**20,'only bounded final metadata pin');p=dict(path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=identity(s));current(p);return p
def read(p):return json.loads(whole(p))
def false_scope(v):require(all(v[k] is False for k in FLAGS+QUALIFIERS),'all four execution flags and qualification flags false')
def contains(v,p):return v==p or type(v) is dict and any(contains(x,p) for x in v.values()) or type(v) is list and any(contains(x,p) for x in v)
def tree_bytes(roots,reject_alias):
 total=count=0;stack=list(map(Path,roots))
 while stack:
  q=stack.pop()
  if not q.exists():continue
  require(q.is_dir() and not q.is_symlink(),'literal resource directory')
  with os.scandir(q) as it:
   for e in it:
    s=e.stat(follow_symlinks=False)
    if reject_alias:require(not stat.S_ISLNK(s.st_mode),'no joint namespace alias')
    if stat.S_ISDIR(s.st_mode):stack.append(Path(e.path))
    elif stat.S_ISREG(s.st_mode):total+=s.st_size;count+=1
 return total,count
def main():
 started=time.monotonic();failure=None;facts={};selected=[]
 try:
  pins={name:pin(BASE/name) for name in('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json','FINAL_PUBLICATION_RECEIPT.json','ROOT_FINAL_ONCE_PUBLICATION_TRUE_TOOL_RETURNS.json','ROOT_EXACT_ACTUAL24_ARGV.json')}
  sf=read(pins['FINAL_SOURCE_FREEZE.json']);hf=read(pins['FINAL_HOST_FREEZE.json']);cli=read(pins['FINAL_ROOT_REVIEWABLE_CLI.json']);pub=read(pins['FINAL_PUBLICATION_RECEIPT.json']);pt=read(pins['ROOT_FINAL_ONCE_PUBLICATION_TRUE_TOOL_RETURNS.json']);argv=read(pins['ROOT_EXACT_ACTUAL24_ARGV.json']);proof=sf['Root_same_round_peer_and_generation_proof'];ready=read(proof['selected_Source_only_ready_pin']);gen=read(proof['Source_generation_true_tools_pin']);peer=read(proof['peer_review_pin']);peert=read(proof['peer_true_tools_pin']);plan=read(sf['control_plan_pin'])
  SCIENCE.update([plan['actual_current_SCI1_pin']['path'],plan['actual_current_SCI2_pin']['path']]+[r['current_original_input_full_pin']['path'] for r in plan['inputs']])
  for v in(sf,hf,cli,pub,ready,peer,plan):false_scope(v)
  require(sf['source_only'] is True and sf['candidate_executed'] is False and hf['source_only'] is True and hf['candidate_executed'] is False and ready['actual_business_started'] is False and ready['Root_final_publication_executed'] is False and pub['source_only'] is True,'Source-only package never started business')
  require(sf['schema']=='ALL34_ORIGINAL_ASCII_INFINITE_SCAT_SOURCE_ONLY_FREEZE_V1' and hf['schema']=='ALL34_ORIGINAL_ASCII_INFINITE_SCAT_HOST_SOURCE_ONLY_FREEZE_V1' and cli['schema']=='ALL34_ORIGINAL_ASCII_INFINITE_SCAT_REVIEWABLE_CLI_SOURCE_ONLY_V1','exact final schemas')
  require(sf['original_caps']==hf['original_caps']==ready['original_caps']==plan['original_caps']==CAPS,'exact original resource caps')
  require(hf['selected_source_freeze_pin']==cli['source_freeze_pin']==pub['final_source_freeze_pin']==pins['FINAL_SOURCE_FREEZE.json'] and cli['host_freeze_pin']==pub['final_host_freeze_pin']==pins['FINAL_HOST_FREEZE.json'] and pub['final_CLI_pin']==pins['FINAL_ROOT_REVIEWABLE_CLI.json'],'same exact final SF/HF/CLI fullPFs')
  require(hf['Root_same_round_peer_and_generation_proof']==cli['Root_same_round_peer_and_generation_proof']==pub['peer_and_generation_proof']==proof and proof['root_same_round_Source_only_publication'] is True and all(proof[k] is False for k in FLAGS),'same-round Root proof')
  require(type(pt['exit_code']) is int and pt['exit_code']==0 and pt.get('session_id') is None and type(pt['output']) is str,'original once publication typed closed0');pubout=json.loads(pt['output'].strip().splitlines()[-1]);require(pubout['status']=='ROOT_FINAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_SOURCE_PUBLICATION_ONLY' and pubout['receipt_pin']==pins['FINAL_PUBLICATION_RECEIPT.json'],'original publication stdout exact receipt PF');false_scope(pubout)
  rt=peert['actual_review_return'];require(peer['status']=='PASS_FROZEN_ALL34_ORIGINAL_ASCII_234T_INFINITE_P0_SOURCE_ONLY' and peer['failure'] is None and peer['source_only'] is True and peer['scientific_payload_read'] is False and peert['observed_closed'] is True and type(peert['original_integer_exit_code']) is int and peert['original_integer_exit_code']==0 and type(rt['exit_code']) is int and rt['exit_code']==0 and rt.get('session_id') is None and json.loads(rt['output'])['review_pin']==proof['peer_review_pin'],'passing genuine original Source review typed0 and exact PF')
  gt=gen['actual_Source_preparation_return'];require(gen['observed_closed'] is True and type(gen['original_integer_exit_code']) is int and gen['original_integer_exit_code']==0 and type(gt['exit_code']) is int and gt['exit_code']==0 and gt.get('session_id') is None and json.loads(gt['output'])['ready_pin']==proof['selected_Source_only_ready_pin'],'genuine same-round Source generation typed0 and exact READY');false_scope(json.loads(gt['output']))
  selected=ready['selected_Source_pins']+[proof['selected_Source_only_ready_pin'],proof['Source_generation_true_tools_pin']];require(len(selected)==309 and len(ready['selected_Source_pins'])==307 and pub['selected_Source_pins']==selected and all(contains(peer,p) for p in selected) and all(p in hf['dependencies'] for p in selected),'final package contains all307 selected plus READY/GEN and reviewed fullPF scope')
  for p in hf['dependencies']+hf['explicit_cumulative_metadata_file_pins']:current(p)
  require(hf['host_source_pin']==ready['host_source_pin'] and sf['control_plan_pin']==ready['control_plan_pin'] and sf['complete_source_file_pins']==ready['complete_source_file_pins']+[proof['selected_Source_only_ready_pin']],'reviewed final host/control/full Source set')
  for p in sf['complete_source_file_pins']:whole(p)
  host=whole(hf['host_source_pin']).decode();ast.parse(host);require("runner.execute(stage,'all34_original_ASCII_234T_infinite_P0_SCAT',cmd,600)" in host and "len(runner.records)==1" in host and "full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)" in host,'reviewed original guard, onechild600 and no retries retained')
  require(type(argv) is list and len(argv)==24 and all(type(x) is str for x in argv) and argv==cli['argv'] and argv[:11]==ready['original_complete_ENV_Python_B_prefix'] and argv[11]==hf['host_source_pin']['path'],'exact complete ENV/Python/-B host CLI24 without precision roundtrip')
  require(argv[12:]==['--source-freeze-summary',pins['FINAL_SOURCE_FREEZE.json']['path'],'--source-freeze-sha256',pins['FINAL_SOURCE_FREEZE.json']['sha256'],'--source-freeze-seven-id',json.dumps(pins['FINAL_SOURCE_FREEZE.json']['identity'],separators=(',',':')),'--host-freeze-summary',pins['FINAL_HOST_FREEZE.json']['path'],'--host-freeze-sha256',pins['FINAL_HOST_FREEZE.json']['sha256'],'--host-freeze-seven-id',json.dumps(pins['FINAL_HOST_FREEZE.json']['identity'],separators=(',',':'))],'CLI24 exact source/host fullPF argument triples')
  prior=read(plan['selected_prior47_plan_pin']);roots=plan['complete_joint_roots'];require(len(roots)==49 and len(set(roots))==49 and roots==prior['complete_joint_roots']+[str(BASE.parent),plan['planned_actual_output_root']] and not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a!=b),'exact prior47 plus TOP/output49 disjoint roots')
  require(plan['expected_nuclides']==34 and plan['expected_temperature_records']==234 and plan['expected_leaf_records']==702 and plan['original_decompressed_payload_expected_bytes']==746505396,'frozen exact all34 nativeT scope')
  output=Path(plan['planned_actual_output_root']);require(cli['planned_actual_output_root']==str(output) and output.parent==ART and not os.path.lexists(output),'actual output absent and original once fresh namespace')
  for p in[plan['actual_current_SCI1_pin'],plan['actual_current_SCI2_pin']]+[r['current_original_input_full_pin'] for r in plan['inputs']]:current(p)
  retirement=read(hf['actual_precise_retirement_receipt_pin']);require(hf['actual_precise_retirement_receipt_pin']==proof['actual_precise_retirement_receipt_pin']==plan['actual_precise_retirement_receipt_pin'] and retirement['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY' and retirement['failure'] is None and retirement['actual_released_bytes']==405417320 and retirement['actual_released_pins']==retirement['exact_target_pins'] and len(retirement['actual_released_pins'])==4 and all(not os.path.lexists(p['path']) for p in retirement['actual_released_pins']),'precise old four retirement edge only')
  joint,count=tree_bytes(roots,True);outer=sum(p['size_bytes'] for p in hf['explicit_cumulative_metadata_file_pins'] if not any(Path(p['path']).is_relative_to(Path(r)) for r in roots));require(joint+outer<CAPS['fresh_bytes'],'all49 joint roots plus explicit metadata below original2GiB')
  family=sorted(str(p) for p in ART.glob('axial-material-*'));history,hcount=tree_bytes(family,False);require(family==sorted(str(p) for p in ART.glob('axial-material-*')),'dynamic history root set unchanged');require(history+CAPS['cold_reserve_bytes']+CAPS['metadata_reserve_bytes']+CAPS['fresh_bytes']<CAPS['history_bytes'],'original96GiB history with full cold/meta/fresh reservation')
  free=shutil.disk_usage(ART).free;require(free-CAPS['cold_reserve_bytes']-CAPS['fresh_bytes']>=CAPS['free_floor_bytes'],'original global8GiB free floor after cold/fresh reservation')
  for p in pins.values():whole(p)
  for p in selected:current(p)
  facts=dict(final_source_freeze_pin=pins['FINAL_SOURCE_FREEZE.json'],final_host_freeze_pin=pins['FINAL_HOST_FREEZE.json'],final_CLI_pin=pins['FINAL_ROOT_REVIEWABLE_CLI.json'],final_publication_receipt_pin=pins['FINAL_PUBLICATION_RECEIPT.json'],genuine_Root_once_publication_true_tools_pin=pins['ROOT_FINAL_ONCE_PUBLICATION_TRUE_TOOL_RETURNS.json'],Root_exact_actual24_argv_pin=pins['ROOT_EXACT_ACTUAL24_ARGV.json'],Root_same_round_peer_and_generation_proof=proof,reviewed_exact_argv=argv,selected_Source_pins=selected,actual_selected307_plus_READY_GEN_scope_contained=True,complete_joint_roots=roots,final_dependencies_current7_count=len(hf['dependencies']),observed_joint_regular_file_bytes=joint,observed_explicit_outer_metadata_bytes=outer,observed_total_cumulative_bytes=joint+outer,joint2GiB_headroom_bytes=CAPS['fresh_bytes']-joint-outer,observed_dynamic_history_regular_file_bytes=history,observed_dynamic_history_regular_file_count=hcount,history96GiB_reserved_headroom_bytes=CAPS['history_bytes']-history-CAPS['cold_reserve_bytes']-CAPS['metadata_reserve_bytes']-CAPS['fresh_bytes'],observed_filesystem_free_bytes=free,free8GiB_reserved_headroom_bytes=free-CAPS['cold_reserve_bytes']-CAPS['fresh_bytes']-CAPS['free_floor_bytes'],actual_output_absent_before_launch=True,exact_original_guard_onechild600_noRetry_retained=True,original_caps=CAPS)
 except BaseException as exc:failure=repr(exc)
 report=dict(schema='ALL34_ORIGINAL_ASCII_INFINITE_SCAT_FINAL_LIGHT_SOURCE_METADATA_REVIEW_V1',status='PASS_FINAL_LIGHT_ALL34_234T_CLI24_SOURCE_METADATA_ONLY' if failure is None else 'FAIL_FINAL_LIGHT_ALL34_SOURCE_METADATA_ONLY',source_only=True,metadata_only=True,failure=failure,audit_source_pin=pin(Path(__file__)),scientific_payload_read=False,SCI_payload_read_by_peer=False,gzip_payload_read_by_peer=False,candidate_imported_or_executed_by_peer=False,actual24_executed_by_peer=False,native_engines_started_by_peer=0,current_SPH_MASK_context_applied=False,historical_machine_bit_replay=False,full_reference_qualified=False,**{k:False for k in FLAGS+QUALIFIERS},**facts,elapsed_seconds=time.monotonic()-started)
 target=OUT/'REVIEW.json'
 with target.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=report['status'],review_pin=pin(target),source_only=True,**{k:False for k in FLAGS+QUALIFIERS})),flush=True);require(failure is None,'final LIGHT retained actual failure: '+str(failure))
if __name__=='__main__':main()
