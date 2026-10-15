"""Sole completed-runtime metadata postverification; no scientific-body reads."""
import hashlib,importlib.util,json,os,stat,time
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
ART=Path('/Users/wen/spot/validation/artifacts/axial-material-four-original-ASCII-infinite-SCAT-producer-20261014-v1')
spec=importlib.util.spec_from_file_location('frozen_SCAT_metadata_primitives',BASE/'independent_source_review_20261014/review_source_only.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
require,current,whole,read,pin=m.require,m.current,m.whole,m.read,m.pin
FALSE=m.FLAGS+m.PHYSICS
H=dict(path=str(ART/'Root_actual_four_original_ASCII_infinite_SCAT_summary.json'),
 sha256='4b985fe28662618d666a8416d0e100dc302074b0df08794beabae519c8903e19',
 size_bytes=1346509,identity=[16777229,50397925,33188,1,1346509,1791994663005075712,1791994663005075712])
def main():
 started=time.monotonic();failure=None;facts={}
 try:
  h=read(H);pRootTools=pin(BASE/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json');tools=read(pRootTools)
  t=tools['actual_terminal_return'];require(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and tools['original_integer_exit_code']==0
    and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None
    and json.loads(t['output'])['report_pin']==H,'genuine Root runtime typedclosed0/current original H')
  require(h['schema']=='ACTUAL_FOUR_ORIGINAL_ASCII_INFINITE_SCAT_GUARDED_REPORT_V1'
    and h['status']=='ACTUAL_FOUR_ORIGINAL_ASCII_32T_INFINITE_P0_WORDS_CLOSED0_ONLY'
    and h['failure']is None and h['secondary_failures']==[] and h['final_report_resource_check_passed']is True
    and h['original_guard_MRO_unchanged']is True and h['original_caps']==m.CAPS
    and all(h[k]is False for k in m.PHYSICS),'complete actual owning report/caps/false qualification scope')
  sf=read(h['source_freeze_pin']);hf=read(h['host_freeze_pin']);ready=read(m.READY);plan=read(sf['control_plan_pin'])
  require(h['source_freeze_pin']==pin(BASE/'FINAL_SOURCE_FREEZE.json')
    and h['host_freeze_pin']==pin(BASE/'FINAL_HOST_FREEZE.json') and hf['selected_source_freeze_pin']==h['source_freeze_pin']
    and sf['control_plan_pin']==ready['control_plan_pin'] and sf['original_caps']==hf['original_caps']==plan['original_caps']==m.CAPS,'same genuinely published owning source/context')
  pubpin=pin(BASE/'FINAL_PUBLICATION_RECEIPT.json');pub=read(pubpin);pubToolsPin=pin(BASE/'ROOT_FINAL_ONCE_PUBLICATION_TRUE_TOOL_RETURNS.json');pubTools=read(pubToolsPin)
  require(type(pubTools['actual_publication_return']['exit_code'])is int and pubTools['actual_publication_return']['exit_code']==0
    and json.loads(pubTools['actual_publication_return']['output'])['receipt_pin']==pubpin
    and pub['final_source_freeze_pin']==h['source_freeze_pin'] and pub['final_host_freeze_pin']==h['host_freeze_pin'],'actual sole publication closed0')
  proof=pub['peer_and_generation_proof'];peer=read(proof['peer_review_pin']);peerTools=read(proof['peer_true_tools_pin']);gen=read(proof['Source_generation_true_tools_pin'])
  require(peer['status'].startswith('PASS') and peer['failure']is None and peer['source_only']is True
    and peerTools['actual_review_return']['exit_code']==0 and type(peerTools['actual_review_return']['exit_code'])is int
    and json.loads(peerTools['actual_review_return']['output'])['review_pin']==proof['peer_review_pin']
    and gen['actual_Source_preparation_return']['exit_code']==0 and type(gen['actual_Source_preparation_return']['exit_code'])is int
    and json.loads(gen['actual_Source_preparation_return']['output'])['ready_pin']==m.READY,'true Source0/peer0/generation0 proof still intact')
  lightPin=pin(BASE/'final_light_review_20261014/REVIEW.json');light=read(lightPin);lightToolsPin=pin(BASE/'final_light_review_20261014/TRUE_TOOL_RETURNS.json');lightTools=read(lightToolsPin)
  require(light['status'].startswith('PASS') and light['failure']is None
    and lightTools['actual_review_return']['exit_code']==0 and type(lightTools['actual_review_return']['exit_code'])is int
    and json.loads(lightTools['actual_review_return']['output'])['review_pin']==lightPin,'genuine necessary finalLIGHT closed0 precedes actual')
  argvPin=pin(BASE/'ROOT_EXACT_ACTUAL24_ARGV.json');argv=read(argvPin);cli=read(pub['final_CLI_pin'])
  require(argv==cli['argv'] and len(argv)==24,'exact actual24 published CLI retained')
  outputs=h['complete_output_pins']+[H];actualPaths={str(p)for p in ART.rglob('*')if p.is_file()}
  require(len(outputs)==7 and len({p['path']for p in outputs})==7 and actualPaths=={p['path']for p in outputs},'all seven actual output files exact closed inventory')
  for p in outputs:whole(p)
  fixed=h['fixed_current_pins'];require(len(fixed)==204 and len({p['path']for p in fixed})==204,'all204 fixed actual inputs unique')
  for p in fixed:current(p)
  dualBefore=hashlib.sha256(json.dumps(fixed,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  child=h['actual_child_receipt'];e=read(child['report_pin']);require(e==h['actual_evidence']
    and e['schema']=='ACTUAL_FOUR_ORIGINAL_ASCII_INFINITE_SCAT_PRODUCER_COMPARISON_V1'
    and e['status']==child['status']=='ALL_FOUR_ORIGINAL_ASCII_32T_INFINITE_P0_RAW_WORDS_EQUAL'
    and e['source_freeze_pin']==h['source_freeze_pin'] and e['control_plan_pin']==sf['control_plan_pin']
    and e['actual_current_SCI1_pin']==plan['actual_current_SCI1_pin']
    and e['compared_unique_nuclides']==4 and e['compared_temperature_records']==32 and e['compared_original_leaf_records']==96
    and e['actual_infinite_P0_producer_all32T_raw_words_equal']is True and e['original_caps']==m.CAPS
    and all(e[k]is False for k in m.PHYSICS),'same actual complete child evidence and exact32T/96 infinity scope')
  binding=read(e['execution_binding_pin']);require(binding['source_freeze_pin']==h['source_freeze_pin']
    and binding['control_plan_pin']==sf['control_plan_pin'] and binding['SCI1_whole_PF_verified_by_original_parent_before_child']is True
    and binding['complete_joint_roots']==plan['complete_joint_roots'] and binding['original_caps']==m.CAPS,'actual exact binding/parent SCI preverification')
  require(len(h['records'])==1 and h['records'][0]['status']=='PASS' and h['records'][0]['wall_cap_seconds']==600.0
    and len(h['actual_watchdog_checks'])==1,'exact one actual child, original600/noRetry')
  stage=h['records'][0];watchPin=pin(ART/(stage['label']+'.watchdog.json'));watch=read(watchPin)
  require(watch['command']==stage['command'] and type(watch['returncode'])is int and watch['returncode']==0
    and watch['limit_failure']is None and watch['own_child_only']is True and watch['rss_cap_mib']==512
    and watch['sampled_peak_rss_mib']<512 and watch['elapsed_seconds']<600
    and h['actual_watchdog_checks'][0]['path']==watchPin['path'] and h['actual_watchdog_checks'][0]['sha256']==watchPin['sha256'],'actual genuine watchdog closed0/original caps')
  logfile=pin(ART/(stage['label']+'.log'));require(logfile['sha256']==stage['log_sha256'] and json.loads(whole(logfile))==child,'actual one-line child stdout exact retained')
  stages=read(pin(ART/'gendf-stage/stages.json'));require(stages['stages']==h['records'],'complete actual stage ledger agrees owning summary')
  totalWords=0;totalLeaves=0;summary=[]
  require([r['nuclide']for r in e['actual_extractions']]==['Am241','Pu238','Pu239','Pu240'],'all4 nuclei original order')
  for r,row in zip(e['actual_extractions'],plan['inputs']):
   current(row['gzip_primary_current_full_pin']);inv=read(row['actual_complete_inventory_pin'])
   require(r['actual_complete_inventory_pin']==row['actual_complete_inventory_pin']
     and r['full_compressed_primary_pin']==row['gzip_primary_current_full_pin']
     and r['actual_compressed_EOF_SHA256']==row['gzip_primary_current_full_pin']['sha256']
     and r['actual_original_ASCII_EOF_SHA256']==row['historical_original_ASCII_sha256']
     and r['actual_decompressed_bytes']==row['historical_original_ASCII_size_bytes']
     and r['all_actual_MF3_MF6_sections_verified']==len(inv['actual_sections'])
     and r['original_formatter_already_applied']is True and r['second_quantization_performed']is False,'actual current original gzip/ASCII EOF reports source-bound; no peer payload reread')
   ts=r['temperature_comparisons'];require(len(ts)==8 and [q['actual_original_ASCII_temperature_K']for q in ts]==[g['temperature_K']for g in inv['original8_MF1_grids']],'all8 original temperature records metadata mapping')
   words=0
   for q in ts:
    require(q['nuclide']==row['nuclide'] and q['mat']==row['mat'] and q['original_strict47_MTs']==[2,5,16,17,28,37,*range(51,92)]
      and q['actual_thermal_MTs_descending']==[221] and q['original_thermal_cutoff_eV']==4.0
      and q['original_igrest']==q['original_ngther']==85 and q['actual_elastic_NL']==2 and q['actual_elastic_NZ']==10
      and q['exact_infinite_P0_three_leaf_raw_words_equal']is True and q['compact_P0_z0_LIST_only']is True
      and q['no_dense_field_spool']is True and all(q[k]is False for k in m.PHYSICS),'encoded original order/thermal85/P0 projection/false scope for everyT')
    require(set(q['comparisons'])=={'SCAT00','NJJS00','IJJS00'},'exact original3 infinite P0 leaf roles')
    for name,c in q['comparisons'].items():
     leaf=c['original_leaf'];require(leaf['name']==name and leaf['words']==c['original_words']==c['replayed_words']
       and leaf['kind']==c['original_kind']==(2 if name=='SCAT00'else 1)
       and c['original_byte_offset']==4*leaf['offset_words'] and c['original_raw_sha256']==c['replayed_raw_sha256']
       and c['exact_raw_words_equal']is True and type(c['mismatching_raw_words'])is int and c['mismatching_raw_words']==0
       and c['bounded_mismatch_samples']==[] and 0<leaf['words']<=(370*370 if name=='SCAT00'else 370),'all actual96 original leaf lengths/kinds/offsets/hash equality/zero word mismatches')
     words+=c['original_words'];totalLeaves+=1
   totalWords+=words;summary.append(dict(nuclide=r['nuclide'],temperature_records=8,target_leaf_records=24,original_words=words,word_mismatches=0,actual_original_ASCII_bytes=r['actual_decompressed_bytes'],actual_MF3_MF6_sections=r['all_actual_MF3_MF6_sections_verified']))
  require(totalWords==1926639 and totalLeaves==96 and sum(r['actual_decompressed_bytes']for r in e['actual_extractions'])==284814387
    and e['selective_SCI_read_bytes']==7887164 and e['original_SCI_ENERGY_leaf']['kind']==2 and e['original_SCI_ENERGY_leaf']['words']==371,'complete actual captured count/bytes consistency only; no matrix recomputation')
  roots=plan['complete_joint_roots'];require(len(roots)==47 and binding['explicit_cumulative_metadata_file_pins']==hf['explicit_cumulative_metadata_file_pins'],'same all47 and complete183 outer metadata closure')
  for k in('resources_before','resources_after','resources_after_including_summary_bytes'):
   res=h[k];j=res['complete_joint'];hist=res['original_history'];require(j['resource_roots']==roots and j['artifact_budget_bytes']==2*2**30
     and hist['artifact_budget_bytes']==96*2**30 and res['host_SELF_peak_bytes']<512*2**20 and res['whole_elapsed_seconds']<1800
     and j['artifact_bytes']+res['explicit_external_metadata_bytes']+res['host_open_unlinked_bytes']<2*2**30
     and hist['artifact_bytes']+20971764748+64*2**20<96*2**30
     and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual preserved original cap checks before/after/report-inclusive')
  require(h['resources_before']['original_history']['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'original wholefresh2GiB initial history reservation')
  currentTotal=0
  for root in roots:
   p=Path(root)
   if not p.exists():continue
   for q in p.rglob('*'):
    s=q.lstat();require(not stat.S_ISLNK(s.st_mode),'all47 current output/resource roots no aliases')
    if stat.S_ISREG(s.st_mode):currentTotal+=s.st_size
  outer=sum(p['size_bytes']for p in hf['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots))
  require(currentTotal+outer<2*2**30,'current all47/outer metadata remains original2GiB')
  retirement=read(h['actual_precise_retirement_receipt_pin']);require(retirement['actual_released_bytes']==405417320
    and retirement['actual_released_pins']==retirement['exact_target_pins'] and len(retirement['actual_released_pins'])==4
    and all(not os.path.lexists(p['path'])for p in retirement['actual_released_pins']),'exact original4 released paths still absent')
  for p in fixed:current(p)
  for row in plan['inputs']:current(row['gzip_primary_current_full_pin'])
  for p in outputs:whole(p)
  require(read(H)==h,'same immutable Root summary after all postchecks')
  facts=dict(Root_actual_runtime_true_tools_pin=pRootTools,actual_Root_report_pin=H,actual_child_evidence_pin=child['report_pin'],
   actual_execution_binding_pin=e['execution_binding_pin'],actual_watchdog_pin=watchPin,all_actual_output_full_pins=outputs,
   original_source_review_pin=proof['peer_review_pin'],original_source_review_tools_pin=proof['peer_true_tools_pin'],original_generation_tools_pin=proof['Source_generation_true_tools_pin'],
   actual_Root_publication_receipt_pin=pubpin,actual_Root_publication_tools_pin=pubToolsPin,necessary_final_LIGHT_review_pin=lightPin,necessary_final_LIGHT_tools_pin=lightToolsPin,
   actual_unique_nuclides=4,actual_temperature_records=32,actual_target_leaf_records=96,actual_original_compared_words=totalWords,actual_bit_word_mismatches=0,
   actual_cohort_summaries=summary,actual_original_ASCII_total_bytes=284814387,actual_selective_SCI_bytes=7887164,
   actual_fixed_input_current7_count=204,actual_fixed_input_dual_current7_checks=True,original_fixed_input_fullpin_inventory_SHA256=dualBefore,
   exact_original47_MTs_and_all32_thermal221_igrest_ngther85_metadata_verified=True,
   original_default_REAL32_imported_ENERGY_branch_source_proof_retained=True,original_all32_T96_leaf_raw_hash_type_offset_count_equality_verified=True,
   original_caps=m.CAPS,actual_watchdog_sampled_peak_rss_mib=watch['sampled_peak_rss_mib'],actual_whole_wall_seconds=h['wall_seconds'],
   complete_joint_roots=roots,actual_current_joint_root_bytes=currentTotal,actual_current_explicit_outer_metadata_bytes=outer,actual_current_cumulative_bytes=currentTotal+outer,
   all_output_bytes_independently_EOF_current7_checked=True)
 except BaseException as exc:failure=repr(exc)
 report=dict(schema='INDEPENDENT_FOUR_ORIGINAL_ASCII_INFINITE_SCAT_ACTUAL_RUNTIME_METADATA_POSTVERIFY_V1',
  status='PASS_ACTUAL_FOUR_ASCII_32T_96_INFINITE_P0_TARGET_RECORDS_1926639_WORDS_EXACT_ONLY'if failure is None else'FAIL_ACTUAL_FOUR_ASCII_INFINITE_SCAT_POSTVERIFY',
  failure=failure,metadata_only=True,audit_source_pin=pin(Path(__file__)),gzip_payload_read_by_peer=False,SCI_payload_read_by_peer=False,
  sciencebody_imported_or_executed=False,business_rerun_by_peer=False,native_engines_started_by_peer=0,matrix_math_recomputed_by_peer=False,
  **{k:False for k in FALSE},**facts,elapsed_seconds=time.monotonic()-started)
 target=OUT/'REVIEW.json'
 with target.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=report['status'],review_pin=pin(target),**{k:False for k in FALSE})),flush=True)
 require(failure is None,'actual solepost retained failure '+str(failure))
if __name__=='__main__':main()
