"""Pending actual-run metadata audit; no original SCI/GENDF bytes or mathematics."""
import argparse,ast,hashlib,json,math,os,resource,stat,struct,sys,time
from pathlib import Path
HERE=Path(__file__).absolute().parent
BASE=HERE.parent
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-current-remaining-Cr52-Fe56-finite9-SCAT-producer-20261015-v1')
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
ELEVEN_SCIENCE_DOCUMENT_PINS=[{'path': '/Users/wen/spot/validation/artifacts/axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence/U235_actual_saved_MT5_P0.json', 'sha256': 'e66adad132fb01b44f4f812da9a0072292a0a555138c01d102ba54e4c8696113', 'size_bytes': 392417, 'identity': [16777229, 50185721, 33188, 1, 392417, 1791978645282341273, 1791978645282341273]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence/U238_actual_saved_MT5_P0.json', 'sha256': '9a3f5a548079d2fd14db52ae601857503e6942a94f06fa240b3612398ec63225', 'size_bytes': 388028, 'identity': [16777229, 50185722, 33188, 1, 388028, 1791978645875993718, 1791978645875993718]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence/Fe54_actual_saved_MT5_P0.json', 'sha256': 'e545750beeb04a8dd8a73aae2c92cf03390cab4a93fb59eb78a5112f2f5aee36', 'size_bytes': 311283, 'identity': [16777229, 50185723, 33188, 1, 311283, 1791978646077849263, 1791978646077849263]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence/Fe56_actual_saved_MT5_P0.json', 'sha256': '67712019830579849dd138582c39e43bb62d7929fea0d373f2d710d70d77990d', 'size_bytes': 313568, 'identity': [16777229, 50185724, 33188, 1, 313568, 1791978646288197157, 1791978646288197157]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence/Fe57_actual_saved_MT5_P0.json', 'sha256': '275be3e0f3a4289aed4d9cc93a4a280768f8c739c0b21cf0aa8b637866ee2b5e', 'size_bytes': 311342, 'identity': [16777229, 50185725, 33188, 1, 311342, 1791978646511274366, 1791978646511274366]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence/Fe58_actual_saved_MT5_P0.json', 'sha256': '1ff9a19c4023567ae67f3abdb69118ae946204ab687f6a9eab96877284970006', 'size_bytes': 297472, 'identity': [16777229, 50185726, 33188, 1, 297472, 1791978646675955216, 1791978646675955216]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence/Cr50_actual_saved_MT5_P0.json', 'sha256': 'cc2e883bb863aa609468ddcb5d4bfb1bf2ea51ae865887e29e263b9af528b67d', 'size_bytes': 299674, 'identity': [16777229, 50185727, 33188, 1, 299674, 1791978646874203379, 1791978646874203379]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence/Cr52_actual_saved_MT5_P0.json', 'sha256': '7f6fd3dd0e7cd7302bb78fcd3927a2567c9ba383cc550592be40445cd07c441a', 'size_bytes': 297413, 'identity': [16777229, 50185728, 33188, 1, 297413, 1791978647048226371, 1791978647048226371]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence/Cr53_actual_saved_MT5_P0.json', 'sha256': '00640367ab4abbea3a0a0bdb34d1af30893206bc053548b2321f087d0c8cb88c', 'size_bytes': 294422, 'identity': [16777229, 50185729, 33188, 1, 294422, 1791978647191032847, 1791978647191032847]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence/Cr54_actual_saved_MT5_P0.json', 'sha256': 'a1616a1b41181a222cced79d8e1f2a1b0344c7b7d7bdbec9e9208ebdae916fa4', 'size_bytes': 297537, 'identity': [16777229, 50185732, 33188, 1, 297537, 1791978647361194666, 1791978647361194666]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11-evidence/Mn55_actual_saved_MT5_P0.json', 'sha256': 'dd57969cd315af804df54b9c34d7a9685d17c617dc83c10d7d4cd114370c1aae', 'size_bytes': 298962, 'identity': [16777229, 50185733, 33188, 1, 298962, 1791978647564541546, 1791978647564541546]}]
SCIENCE={p['path']:p for p in ELEVEN_SCIENCE_DOCUMENT_PINS}
READ_PINS={}
START=time.monotonic()
QUALIFIERS=('physics_qualified','scientific_accuracy_qualified','complete_reaction_authority_qualified','physical_neutron_balance_qualified','full_reference_qualified','unreduced_reference_qualified','finite9_replayed','temperature_interpolation_replayed','current_SPH_MASK_context_applied','P1_replayed','AAA_qualified','ABA_admitted','goal_complete')
def require(ok,message):
 if type(ok)is not bool or not ok:raise ValueError(message)
def budget():
 peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);require(peak<512*2**20 and time.monotonic()-START<600,'post-auditor SELF512/stage600');return peak
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 budget();require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['path'])is str and Path(p['path']).is_absolute()and type(p['sha256'])is str and len(p['sha256'])==64 and all(x in'0123456789abcdef'for x in p['sha256'])and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])and p['identity'][4]==p['size_bytes'],'exact fullPF with Python integer IDs');q=Path(p['path']);s=q.lstat();require(stat.S_ISREG(s.st_mode)and identity(s)==p['identity']and not any(a.is_symlink()for a in(q,*q.parents)),'same exact current7');return q
def permitted(q,size):
 require(str(q)not in SCIENCE,'original scientific input or original11 extraction document body forbidden')
 require(q.is_relative_to(OUT)or q.suffix in('.py','.json','.jsonl','.txt','.in','.f','.f90','.cpp','.hpp','.log','.sha256','.make')or q.name.startswith(('file_data_gendf_','file_data_dendf_')),'explicit new output or Source/report metadata only')
 require(size<(64*2**20 if q.is_relative_to(OUT)or q.name=='Root_actual_eight_fuel_finite18_SCAT_summary.json'else 8*2**20),'bounded report metadata body')
def full(p,retain=False):
 q=current(p);permitted(q,p['size_bytes']);digest=hashlib.sha256();size=0;parts=[]
 with q.open('rb')as f:
  require(identity(os.fstat(f.fileno()))==p['identity'],'opened7 exact')
  while True:
   budget();raw=f.read(2**20)
   if not raw:break
   digest.update(raw);size+=len(raw)
   if retain:parts.append(raw)
  require(identity(os.fstat(f.fileno()))==p['identity'],'EOF7 exact')
 require(size==p['size_bytes']and digest.hexdigest()==p['sha256'],'whole EOF/size/SHA exact');current(p)
 if p['path']in READ_PINS:require(READ_PINS[p['path']]==p,'one consistent wholePF per read role')
 READ_PINS[p['path']]=p
 return b''.join(parts)if retain else None
def pin(q):
 q=Path(q);s=q.lstat();permitted(q,s.st_size);p=dict(path=str(q),sha256='0'*64,size_bytes=s.st_size,identity=identity(s));current(p)
 with q.open('rb')as f:
  require(identity(os.fstat(f.fileno()))==p['identity'],'pin opened7 exact');p['sha256']=hashlib.file_digest(f,'sha256').hexdigest();require(identity(os.fstat(f.fileno()))==p['identity'],'pin EOF7 exact')
 current(p);return p
def read(p):return json.loads(full(p,True))
def get(q):p=pin(q);return read(p),p
def unique(rows):
 result={}
 for p in rows:
  require(p['path']not in result or result[p['path']]==p,'consistent complete fixed PF');result[p['path']]=p
 return list(result.values())
def genuine(v,key,code,p=None,outkey=None):
 t=v[key];require(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==code and type(t['exit_code'])is int and t['exit_code']==code and t.get('session_id')is None,'genuine original typed closed integer')
 if p is not None:require(json.loads(t['output'].strip().splitlines()[-1])[outkey]==p,'genuine stdout exact fullPF')
 return t
def contains(value,p):return value==p or isinstance(value,dict)and any(contains(v,p)for v in value.values())or isinstance(value,list)and any(contains(v,p)for v in value)
def canonical(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def compact_resources(value):
 result={k:v for k,v in value.items()if k not in('original_history','complete_joint')}
 for role in('original_history','complete_joint'):
  original=value[role];selected={k:v for k,v in original.items()if k not in('resource_roots','declared_resource_roots','resource_scope_contract')}
  for key in('resource_roots','declared_resource_roots','resource_scope_contract'):
   if key in original:
    selected[key+'_sha256']=canonical(original[key]);selected[key+'_count']=len(original[key])
  result[role]=selected
 return result
def compact_record(value):
 result=dict(value)
 for key in('resource_before','resource_after'):
  if isinstance(result.get(key),dict):result[key]=compact_resources(result[key])
 return result
def false_qual(value):require(all(value[k]is False for k in QUALIFIERS),'narrow producer evidence, every broad qualification false')
def word(value):return struct.pack('<f',value).hex()
def sha(value):return type(value)is str and len(value)==64 and all(c in'0123456789abcdef'for c in value)
def reported_counts(part,row,sci_size):
 require(part['nuclide']==row['nuclide']and part['compared_original_archives']==part['compared_unique_nuclides']==1 and part['compared_temperature_records']==part['compared_archive_temperature_records']==7 and part['compared_finite_dilution_nodes']==63 and part['compared_original_leaf_records']==189,'recorded per-nuclide1archive/7T/63node/189leaf')
 results=part['actual_extractions'];require(len(results)==1,'one original archive report');r=results[0];false_qual(r)
 require(r['nuclide']==row['nuclide']and r['lane']==row['lane']=='single'and r['SCI_role']==row['SCI_role']=='SCI1'and r['current_original_input_full_pin']==row['current_original_input_full_pin']and r['input_encoding']==row['input_encoding']and r['actual_original_ASCII_EOF_SHA256']==row['original_ASCII_expected_sha256']and r['actual_decompressed_bytes']==row['original_ASCII_expected_size_bytes'],'recorded original archive EOF facts, original body not read')
 require(r['actual_compressed_EOF_SHA256']==(row['current_original_input_full_pin']['sha256']if row['input_encoding']=='gzip'else None),'recorded gzip/ASCII route facts')
 ts=r['temperature_comparisons'];require(len(ts)==7 and[word(x['actual_original_ASCII_temperature_K'])for x in ts]==[word(x)for x in row['original_source_deck_temperatures_K']],'recorded seven source-temperature REAL32 identities')
 nodes=set();words=leaves=0;membership=[]
 for t in ts:
  false_qual(t);require(t['nuclide']==row['nuclide']and t['lane']=='single'and t['mat']==row['mat']and t['selected_temperature_raw32_hex']==word(t['actual_original_ASCII_temperature_K'])and t['exact_finite9_lane_P0_raw_words_equal']is True,'recorded own single lane/nativeT equality flag')
  require(t['original_temperature_leaf']['name']=='TEMPERATURE'and t['original_temperature_leaf']['kind']==2 and t['original_temperature_leaf']['words']==7 and t['original_dilution_leaf']['name']=='DILUTION'and t['original_dilution_leaf']['kind']==2 and t['original_dilution_leaf']['words']==9 and sha(t['original_temperature_leaf_raw_sha256'])and sha(t['original_dilution_leaf_raw_sha256']),'recorded TEMPERATURE7/DILUTION9 metadata')
  finite=t['finite_comparisons'];require(len(finite)==9 and len({x['original_SCI_SUBMAT']for x in finite})==9,'nine recorded unique finite members');members=[]
  for z,v in enumerate(finite,1):
   require(v['original_GENDF_dilution_index_zero_based']==z and v['selected_dilution_raw32_hex']==word(v['original_sigma0_barn_binary64'])==word(v['SCI_dilution_REAL32'])and v['exact_finite_P0_three_leaf_raw_words_equal']is True and set(v['comparisons'])=={'SCAT00','NJJS00','IJJS00'},'recorded finite node identity and three P0 roles')
   stamp=(row['nuclide'],t['selected_temperature_raw32_hex'],v['selected_dilution_raw32_hex']);require(stamp not in nodes,'unique recorded node');nodes.add(stamp);members.append(v['original_SCI_SUBMAT'])
   for name,c in v['comparisons'].items():
    leaf=c['original_leaf'];limit=370*370 if name=='SCAT00'else 370
    require(leaf['name']==name and leaf['words']==c['original_words']==c['replayed_words']and leaf['kind']==c['original_kind']==(2 if name=='SCAT00'else 1)and type(leaf['offset_words'])is int and c['original_byte_offset']==4*leaf['offset_words']and 0<c['original_words']<=limit and 0<=c['original_byte_offset']and c['original_byte_offset']+4*c['original_words']<=sci_size and(name=='SCAT00'or c['original_words']==370)and sha(c['original_raw_sha256'])and c['original_raw_sha256']==c['replayed_raw_sha256']and c['exact_raw_words_equal']is True and type(c['mismatching_raw_words'])is int and c['mismatching_raw_words']==0 and c['bounded_mismatch_samples']==[],'recorded types/counts/offsets/hash equality and zero mismatch facts; no raw science recomparison')
    words+=c['original_words'];leaves+=1
  membership.append(dict(nuclide=row['nuclide'],temperature_raw32_hex=t['selected_temperature_raw32_hex'],reported_original_SUBMATs=members))
 require(len(nodes)==63 and leaves==189 and words>0,'recorded per-child counters close')
 return dict(nuclide=row['nuclide'],reported_temperature_records=7,reported_finite_nodes=63,reported_leaf_records=189,reported_original_words=words,reported_word_mismatches=0,reported_original_ASCII_bytes=r['actual_decompressed_bytes'],recorded_memberships=membership)
def inspect(binding):
 root_tools_pin=binding['Root_actual_tools_pin'];tools=read(root_tools_pin);code=binding['Root_original_integer_exit_code'];require(type(code)is int and code in(0,1),'original Root integer0 or1 only');genuine(tools,'actual_terminal_return',code)
 hp=binding['actual_Host_report_pin'];require(hp is not None or code==1,'successful Root requires exact host PF')
 if hp is None:return dict(status='PASS_FAILURE_FACTS_ONLY',actual_Root_original_integer_exit_code=1,actual_Root_tools_pin=root_tools_pin,actual_Host_report_present=False,reported_full_comparison_complete=False)
 require(hp['path']==str(OUT/'Root_actual_remaining_Cr52_Fe56_finite9_SCAT_summary.json'),'literal owning Host report role');h=read(hp);require(h['schema']=='ACTUAL_REMAINING_CR52_FE56_FINITE9_SCAT_GUARDED_REPORT_V1'and h['original_caps']==CAPS and h['original_guard_MRO_unchanged']is True,'actual Host schema/original caps');false_qual(h)
 sf=read(h['source_freeze_pin']);hf=read(h['host_freeze_pin']);plan=read(sf['control_plan_pin'])
 science=unique([plan['actual_current_SCI1_pin'],plan['actual_current_SCI2_pin']]+[r['current_original_input_full_pin']for r in plan['inputs']]+ELEVEN_SCIENCE_DOCUMENT_PINS)
 for p in science:SCIENCE[p['path']]=p;current(p)
 require(hf['selected_source_freeze_pin']==h['source_freeze_pin']and sf['original_caps']==hf['original_caps']==plan['original_caps']==CAPS and plan['execution_nuclides']==['Cr52','Fe56']and len(plan['complete_joint_roots'])==58,'published exact Source/caps/58 roots')
 proof=sf['Root_same_round_peer_and_generation_proof'];require(hf['Root_same_round_peer_and_generation_proof']==proof,'same Source publication proof')
 peer=read(proof['peer_review_pin']);peer_tools=read(proof['peer_true_tools_pin']);gen=read(proof['Source_generation_true_tools_pin']);ready=read(proof['selected_Source_only_ready_pin'])
 require(peer['status'].startswith('PASS')and peer['failure']is None and peer['source_only']is True and ready['control_plan_pin']==sf['control_plan_pin'],'same passing Source peer');genuine(peer_tools,'actual_review_return',0,proof['peer_review_pin'],'review_pin');genuine(gen,'actual_Source_preparation_return',0,proof['selected_Source_only_ready_pin'],'ready_pin')
 require(gen['actual_Source_preparation_return']['chunk_id']=='af73a2'and gen['wrapper_field_adapter_only']is True and gen['Source_preparation_reexecuted']is False and gen['actual_Source_preparation_return']==gen['actual_terminal_return'],'canonical generation key adapter retains exact original0 without rerun');original_gen=read(gen['original_wrapper_pin']);require(original_gen['actual_terminal_return']==gen['actual_terminal_return'],'original generation wrapper preserved')
 require(all(contains(peer,p)for p in ELEVEN_SCIENCE_DOCUMENT_PINS),'all exact authoritative11 scientific document pins retained in formal Source peer; original bodies remain denylisted')
 fixed=h['fixed_current_pins'];required=unique(hf['dependencies']+[h['source_freeze_pin'],h['host_freeze_pin'],hf['host_source_pin'],plan['actual_current_SCI1_pin']]+[r['current_original_input_full_pin']for r in plan['inputs']]);require(all(p in fixed for p in required),'complete actual Source/fixed science coverage')
 for p in fixed:
  current(p)
  if p['path']not in SCIENCE:full(p)
 outputs=unique(h['complete_output_pins']+[hp]);actual={str(p)for p in OUT.rglob('*')if p.is_file()};require({p['path']for p in outputs}==actual,'complete actual new output inventory')
 for p in outputs:require(Path(p['path']).is_relative_to(OUT),'new output only');full(p)
 claim,claim_pin=get(BASE/'ROOT_EXECUTION_CLAIM_RECEIPT.json');require(claim['schema']=='ROOT_EXCLUSIVE_REMAINING_CR52_FE56_FINITE9_EXECUTION_CLAIM_V1'and claim['claim_before_metadata_fullEOF_or_business']is True and type(claim['Root_PID'])is int and claim['Root_PID']>0 and claim['original_caps']==CAPS,'exclusive original Root claim retained')
 records=h['records'];stage_pin=h['original_stage_ledger_pin'];full_records=[];watch_pins=[];log_pins=[];require(stage_pin is not None or records==[],'actual records require original stage ledger')
 if stage_pin is not None:
  require(stage_pin['path']==str(OUT/'gendf-stage/stages.json'),'literal original stage ledger');stages=read(stage_pin);full_records=stages['stages'];require([compact_record(x)for x in full_records]==records and len(records)<=2,'original full stage records match compact Host; no third child')
 for i,(record,full_record)in enumerate(zip(records,full_records)):
  name=plan['execution_nuclides'][i];command=record['command'];require(command[:3]==[ready['original_complete_ENV_Python_B_prefix'][-2],'-B',str(BASE/'compare_remaining_Cr52_Fe56_finite9_SCAT.py')]and command[3]=='--binding-pin'and command[5]=='--expected-parent-pid'and int(command[6])==claim['Root_PID']and command[7:]==['--nuclide',name]and 0<record['wall_cap_seconds']<=600,'literal worker/binding/Root PID/unique original nuclide command')
  if i:require(full_record['started_unix']>=full_records[i-1]['started_unix']+full_records[i-1]['elapsed_seconds'],'original two children serial without overlap')
  watch,pw=get(OUT/(record['label']+'.watchdog.json'));watch_pins.append(pw);require(watch['command']==command and type(watch['pid'])is int and watch['pid']>0 and type(watch['returncode'])is int and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['rss_cap_mib']==512 and 0<=watch['sampled_peak_rss_mib'] and 0<watch['wall_cap_seconds']<=record['wall_cap_seconds']and 0<=watch['elapsed_seconds'],'actual raw original guarded child metadata, failure limit observations retained')
  if code==0:require(watch['sampled_peak_rss_mib']<512 and watch['elapsed_seconds']<watch['wall_cap_seconds'],'successful raw watchdog caps')
  log,pLog=get_log(OUT/(record['label']+'.log'));log_pins.append(pLog);require(pLog['sha256']==record.get('log_sha256',pLog['sha256']),'actual original child log fullPF')
  if code==0:require(record['status']=='PASS'and watch['returncode']==0 and watch['limit_failure']is None and len(log)==1 and json.loads(log[0])==h['actual_child_receipts'][i],'actual two original child0 receipts')
 retirement=read(h['actual_precise_retirement_receipt_pin']);require(retirement['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY'and retirement['failure']is None,'old precise retirement retained')
 for p in retirement['actual_released_pins']:require(not os.path.lexists(p['path']),'old released roles still absent; no deletion by auditor')
 for p in plan['inherited_metadata_current7_pins']:current(p)
 common=dict(actual_Root_tools_pin=root_tools_pin,actual_Root_original_integer_exit_code=code,actual_Host_report_pin=hp,actual_Source_freeze_pin=h['source_freeze_pin'],actual_Host_freeze_pin=h['host_freeze_pin'],actual_Source_peer_pin=proof['peer_review_pin'],actual_Source_peer_tools_pin=proof['peer_true_tools_pin'],canonical_generation_wrapper_pin=proof['Source_generation_true_tools_pin'],original_generation_wrapper_pin=gen['original_wrapper_pin'],actual_exclusive_claim_pin=claim_pin,actual_new_output_full_pins=outputs,actual_stage_ledger_pin=stage_pin,actual_raw_watchdog_pins=watch_pins,actual_original_child_log_pins=log_pins,actual_fixed_current7_pins=fixed,scientific_input_and_document_current7_only_pins=science,inherited_metadata_current7_only_pins=plan['inherited_metadata_current7_pins'],complete_joint_roots=plan['complete_joint_roots'],original_caps=CAPS,saved_actual_resource_checks={k:h[k]for k in('resources_before','resources_after','resources_after_including_summary_bytes')if k in h})
 if code==1:
  require(h['failure']is not None and h['status']=='FAILED_REMAINING_CR52_FE56_FINITE9_SCAT_NO_RETRY','original actual1 retains failed Host status');return dict(status='PASS_FAILURE_FACTS_ONLY',failure_location=h['failure'],reported_full_comparison_complete=False,actual_original_stage_statuses=[x['status']for x in records],**common)
 genuine(tools,'actual_terminal_return',0,hp,'report_pin');require(h['status']=='ACTUAL_REMAINING_CR52_FE56_14T_FINITE9_P0_WORDS_CLOSED0_ONLY'and h['failure']is None and h['secondary_failures']==[]and h['final_report_resource_check_passed']is True and len(records)==len(h['actual_child_receipts'])==len(h['actual_watchdog_checks'])==2,'actual Root0/complete two closed original children')
 aggregate_pin=h['actual_child_receipt']['report_pin'];aggregate=read(aggregate_pin);require(aggregate==h['actual_evidence']and aggregate['schema']=='ACTUAL_REMAINING_CR52_FE56_FINITE9_SCAT_PRODUCER_COMPARISON_V1'and aggregate['status']==h['actual_child_receipt']['status']=='REMAINING_CR52_FE56_14T_FINITE9_P0_RAW_WORDS_EQUAL'and aggregate['aggregation_metadata_only']is True and aggregate['compared_completed_child_reports']==2 and aggregate['remaining_Cr52_Fe56_finite9_P0_producer_raw_words_replayed']is True,'same actual aggregate of original two child reports');false_qual(aggregate)
 binding_pin=aggregate['execution_binding_pin'];execution=read(binding_pin);require(execution['schema']=='REMAINING_CR52_FE56_FINITE9_SCAT_EXECUTION_BINDING_V1'and execution['source_freeze_pin']==h['source_freeze_pin']and execution['control_plan_pin']==sf['control_plan_pin']and execution['complete_joint_roots']==plan['complete_joint_roots']and execution['original_caps']==CAPS,'same original owning child binding')
 parts=[];cohorts=[];part_pins=[]
 for i,(receipt,row)in enumerate(zip(h['actual_child_receipts'],plan['inputs'])):
  pp=receipt['report_pin'];require(pp==aggregate['original_completed_child_report_pins'][i]and pp['path']==str(OUT/'inventories'/('ACTUAL_'+row['nuclide']+'_FINITE9_SCAT_EVIDENCE.json')),'literal complete child report pin');part=read(pp);false_qual(part);require(part['schema']=='ACTUAL_SINGLE_REMAINING_FINITE9_SCAT_PRODUCER_COMPARISON_V1'and part['status']==receipt['status']=='SINGLE_REMAINING_7T_FINITE9_P0_RAW_WORDS_EQUAL'and part['execution_binding_pin']==binding_pin and part['source_freeze_pin']==h['source_freeze_pin']and part['control_plan_pin']==sf['control_plan_pin']and part['actual_current_SCI1_pin']==plan['actual_current_SCI1_pin']and part['single_remaining_finite9_P0_producer_raw_words_replayed']is True,'two original own-nuclide child reports');parts.append(part);part_pins.append(pp);cohorts.append(reported_counts(part,row,plan['actual_current_SCI1_pin']['size_bytes']))
 require(aggregate['actual_extractions']==[r for x in parts for r in x['actual_extractions']]and [aggregate[k]for k in('compared_original_archives','compared_unique_nuclides','compared_temperature_records','compared_archive_temperature_records','compared_finite_dilution_nodes','compared_original_leaf_records')]==[2,2,14,14,126,378]and sum(x['reported_original_ASCII_bytes']for x in cohorts)==plan['original_decompressed_payload_expected_bytes']==26790912,'all reported2archives/14T/126nodes/378P0records close')
 return dict(status='PASS_ACTUAL_REMAINING_CR52_FE56_FINITE9_RECORDED_COMPARISON_METADATA_ONLY',reported_full_comparison_complete=True,actual_aggregate_report_pin=aggregate_pin,actual_original_child_report_pins=part_pins,reported_comparison_cohorts=cohorts,reported_original_archives=2,reported_native_temperature_records=14,reported_finite_nodes=126,reported_P0_leaf_records=378,reported_original_compared_words=sum(x['reported_original_words']for x in cohorts),reported_raw_word_mismatches=0,**common)
def get_log(q):p=pin(q);return full(p,True).decode().splitlines(),p
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--input-binding-pin',required=True);a=ap.parse_args();freeze,freeze_pin=get(HERE/'AUDITOR_SOURCE_ONLY_FREEZE.json');require(freeze['auditor_Source_AST_parsed_before_freeze_and_execution']is True and freeze['auditor_source_pin']==pin(Path(__file__).absolute()),'frozen AST-reviewed Source before execution');ast.parse(full(freeze['auditor_source_pin'],True));bp=json.loads(a.input_binding_pin);require(bp['path']==str(HERE/'POST_INPUT_BINDING.json'),'one explicit post-input binding after Root terminal');binding=read(bp);require(binding['schema']=='REMAINING_CR52_FE56_ACTUAL_POST_INPUT_BINDING_V1'and binding['Root_terminal_observed_closed']is True,'actual Root completed before post run');facts=inspect(binding)
 for p in list(READ_PINS.values()):full(p)
 for p in SCIENCE.values():current(p)
 for p in facts.get('actual_fixed_current7_pins',[]):current(p)
 for p in facts.get('inherited_metadata_current7_only_pins',[]):current(p)
 report=dict(schema='INDEPENDENT_REMAINING_CR52_FE56_ACTUAL_RECORDED_COMPARISON_METADATA_POSTVERIFY_V1',failure=None,metadata_only=True,auditor_source_pin=freeze['auditor_source_pin'],auditor_source_freeze_pin=freeze_pin,actual_post_input_binding_pin=bp,metadata_and_new_output_full_EOF_PF_verified_twice=list(READ_PINS.values()),eleven_scientific_extraction_document_pins=ELEVEN_SCIENCE_DOCUMENT_PINS,scientific_extraction_document_count=11,scientific_extraction_document_bodies_opened_hashed_or_decoded=False,old_SCI_GENDF_ASCII_or_compressed_payload_bodies_read=False,old_science_bodies_hashed=False,original_science_raw_bits_independently_recompared=False,matrix_arithmetic_recomputed=False,reported_comparison_counts_hashes_and_metadata_consistency_only=True,limitation='This post audit checks the recorded comparison counts, types, offsets, digests and equality flags. It does not reread original SCI/GENDF bytes or independently repeat their raw-bit comparison.',source_or_helpers_imported=False,native_children_reexecuted=False,retry_executed=False,fresh_runtime_budget_admission_issued=False,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,**{k:False for k in QUALIFIERS},**facts,post_auditor_SELF_peak_bytes=budget(),elapsed_seconds=time.monotonic()-START)
 raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();require(len(raw)<8*2**20,'own post report bounded8MiB')
 with(HERE/'REVIEW.json').open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 rp=pin(HERE/'REVIEW.json');print(json.dumps(dict(status=report['status'],review_pin=rp),separators=(',',':')),flush=True)
if __name__=='__main__':main()
