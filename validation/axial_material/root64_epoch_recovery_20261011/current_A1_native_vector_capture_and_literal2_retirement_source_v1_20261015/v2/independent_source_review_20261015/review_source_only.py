"""Independent frozen Source/metadata audit. No candidate imports or science body reads."""
import ast,hashlib,json,os,resource,stat,sys,time
from pathlib import Path

BASE=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/v2')
ART=Path('/Users/wen/spot/validation/artifacts')
REPORT=Path(__file__).parent/'REVIEW.json'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
FALSE=dict(business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,physics_qualified=False,scientific_accuracy_qualified=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,full_reference_qualified=False,formal_H150_NZ48_full_controls_qualified=False,historical_machine_bit_replay=False,historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,finite18_replayed=False,temperature_interpolation_replayed=False,current_SPH_MASK_context_applied=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
SCI={str(ART/'axial-material-current-three-plane-raw-macro-compare-after-GENDF-cumulative25-20261014-v1-evidence/A1'/n) for n in ('original_archive_index.sqlite','original_words.bin')}
LARGE={str(ART/(prefix+'/'+name)) for prefix,names in (
 ('axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1',('Root_actual_all34_original_ASCII_infinite_SCAT_summary.json','inventories/ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_EVIDENCE.json')),
 ('axial-material-current-eight-fuel-finite18-SCAT-producer-20261015-v2',('Root_actual_eight_fuel_finite18_SCAT_summary.json','inventories/ACTUAL_EIGHT_FUEL_FINITE18_SCAT_EVIDENCE.json'))) for name in names}
started=time.monotonic();checks=[];fullpins={};statpins={}
def need(ok,msg):
 if type(ok) is not bool or not ok:raise RuntimeError(msg)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();compiler=str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15' and p.get('sha256')=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492' and p['identity'][3]==2
 need(q.is_absolute() and '..' not in q.parts and stat.S_ISREG(s.st_mode) and s.st_nlink==(2 if compiler else 1) and s.st_uid==os.getuid() and not any(x.is_symlink() for x in(q,*q.parents)) and all(type(v) is int for v in p['identity']) and len(p['identity'])==7 and ids(s)==p['identity'] and s.st_size==p['size_bytes'],'current exact7 '+str(q));return q
def allowed(q):
 return str(q) not in SCI and q.suffix.lower() not in ('.xsm','.sci','.gz','.sqlite','.jsonl') and q.name!='original_words.bin'
def read(p,retain=True):
 q=current(p);need(allowed(q) and p['size_bytes']<(64 if str(q) in LARGE else 8)*2**20,'Source/bounded metadata only '+str(q));h=hashlib.sha256();size=0;parts=[]
 fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  need(ids(os.fstat(fd))==p['identity'],'opened exact7')
  while True:
   chunk=os.read(fd,2**20)
   if not chunk:break
   h.update(chunk);size+=len(chunk)
   if retain:parts.append(chunk)
  need(ids(os.fstat(fd))==p['identity'],'after EOF exact7')
 finally:os.close(fd)
 current(p);need(size==p['size_bytes'] and h.hexdigest()==p['sha256'],'full EOF SHA/size '+str(q));fullpins[str(q)]=p
 return b''.join(parts) if retain else None
def fresh(q):
 q=Path(q);s=q.lstat();need(allowed(q) and s.st_size<(64 if str(q) in LARGE else 8)*2**20,'new Source/metadata PF role');p=dict(path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=ids(s));current(p);return p
def doc(p):return json.loads(read(p))
def onlystat(p):current(p);statpins[p['path']]=p
def unique(rows):
 d={}
 for p in rows:
  need(p['path'] not in d or d[p['path']]==p,'consistent one PF per path');d[p['path']]=p
 return list(d.values())
def contains(v,p):return v==p or isinstance(v,dict) and any(contains(x,p) for x in v.values()) or isinstance(v,list) and any(contains(x,p) for x in v)
def closed(v,key,p,outkey):
 t=v[key];need(v['observed_closed'] is True and type(v['original_integer_exit_code']) is int and v['original_integer_exit_code']==0 and type(t['exit_code']) is int and t['exit_code']==0 and t.get('session_id') is None and json.loads(t['output'].strip().splitlines()[-1])[outkey]==p,'genuine typed integer closed0 exact stdout PF')
def function(raw,name):
 lines=raw.decode().splitlines(keepends=True)
 for n in ast.parse(raw).body:
  if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name:return ''.join(lines[n.lineno-1:n.end_lineno]).encode()
 raise RuntimeError('missing original definition '+name)
def text_has(text,rows,label):need(all(x in text for x in rows),label)
def inverse(p):
 a=read(p['original_full_pin']);b=read(p['candidate_full_pin']);need(len(p['edit_map'])==1,'single complete Source inverse span');e=p['edit_map'][0];ab,ae=e['original_begin_byte'],e['original_end_byte'];bb,be=e['candidate_begin_byte'],e['candidate_end_byte'];old=bytes.fromhex(e['original_bytes_hex']);new=bytes.fromhex(e['candidate_bytes_hex']);need(a[ab:ae]==old and b[bb:be]==new and b[:bb]+old+b[be:]==a and p['complete_inverse_reconstructed_original'] is True and hashlib.sha256(a).hexdigest()==p['whole_original_reconstructed_sha256'],'complete exact Source inverse');return dict(original_pin=p['original_full_pin'],candidate_pin=p['candidate_full_pin'],original_byte_span=[ab,ae],candidate_byte_span=[bb,be],complete_original_reconstructed=True)
def mark(s):checks.append(s)
result=dict(schema='INDEPENDENT_A1_NATIVE_VECTOR_CAPTURE_LITERAL2_FROZEN_SOURCE_REVIEW_V1',status='STARTED',failure=None,source_only=True,scope='Frozen Source and bounded metadata: current A1 original four REAL32 records (26 words/104 bytes), then exact two-file retirement after actual capture/post0/read-only0. No actual capture or retirement performed by this reviewer.',scientific_input_body_read=False,original_XSM_body_read=False,science_imported_or_executed=False,candidate_modules_imported=False,numerical_benchmark_executed=False,publication_executed=False,actual_capture_qualified=False,actual_retirement_qualified=False,**FALSE)
try:
 readypin=fresh(BASE/'SOURCE_REVIEW_READY.json');genpin=fresh(BASE/'ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json')
 need(readypin['sha256']=='30ebf80b26196e8ee21fc33ffbfd51bf4eecb271c7102632ebd8a2fb7cf3288f' and readypin['size_bytes']==213745 and genpin['sha256']=='50d92c8f0f2c06e9f3b112537ddf343ef7941c0bd39b10127ab95b70c02e380b' and genpin['size_bytes']==1482,'same genuine Root generation frozen round')
 ready=doc(readypin);gen=doc(genpin);closed(gen,'actual_Source_preparation_return',readypin,'ready_pin')
 need(ready['schema']=='A1_NATIVE_VECTOR_CAPTURE_SOURCE_REVIEW_READY_V1' and ready['source_only'] is True and ready['source_preparation_only'] is True,'actual READY schema');plan=doc(ready['plan_pin']);author=doc(ready['author_source_freeze_pin']);proof=doc(ready['original_Source_proof_pin'])
 need(plan['schema']=='A1_NATIVE_VECTOR_CAPTURE_AND_LITERAL2_RETIREMENT_SOURCE_ONLY_PLAN_V1' and author['stop_writes_after_this_freeze'] is True and ready['source_pins']==author['source_pins'] and len(ready['source_pins'])==10 and len(ready['selected_metadata_pins'])==457 and len(plan['source_dependency_pins'])==48 and ready['selected_metadata_pins']==plan['explicit_cumulative_metadata_file_pins'],'actual10/457/48 fields and schema')
 for d in (ready,plan,author,proof):need(all(d.get(k,False) is False for k in FALSE),'Source science/boundary flags false')
 need(plan['original_caps']==author['original_caps']==CAPS and plan['expected_vector_record_count']==4 and plan['expected_REAL32_words']==26 and plan['expected_capture_bytes']==104 and plan['expected_vector_offsets_bytes']==[0,16,32,48] and plan['native_XSM_redecode_required'] is False,'unchanged caps and exact compact vectors')
 selected=unique(ready['selected_metadata_pins']+ready['source_pins']+plan['source_dependency_pins']+[ready['plan_pin'],ready['author_source_freeze_pin'],ready['original_Source_proof_pin'],readypin,genpin])
 for p in selected:
  if p['path'] in SCI:onlystat(p)
  else:read(p,False)
 source={Path(p['path']).name:read(p) for p in ready['source_pins']}
 for p in ready['source_pins']:ast.parse(source[Path(p['path']).name],filename=p['path'])
 for p in selected:
  if p['path'].endswith('.py') and p['path'] not in [x['path'] for x in ready['source_pins']]:ast.parse(read(p),filename=p['path'])
 mark('Full EOF/hash/exact7 selected Source/metadata, ten author ASTs and external Source syntax checked without imports; A1 pair stat only.')
 roots=plan['complete_joint_roots'];inherited=doc(plan['inherited_finite_plan_pin'])
 need(len(roots)==54 and len(set(roots))==54 and roots[:-2]==plan['inherited_complete_joint_roots']==inherited['complete_joint_roots'] and len(roots[:-2])==52 and roots[-2:]==[str(BASE.parent),plan['planned_actual_output_root']] and not any(Path(x).is_relative_to(Path(y)) for x in roots for y in roots if x!=y) and inherited['original_caps']==CAPS and not os.path.lexists(plan['planned_actual_output_root']),'preserved original52 prefix + whole SourceTOP/output54 fresh no reset')
 result.update(original_caps=CAPS,complete_joint_roots=roots,inherited_finite_plan_pin=plan['inherited_finite_plan_pin'],ready_pin=readypin,genuine_Root_Source_generation_pin=genpin,author_source_freeze_pin=ready['author_source_freeze_pin'],control_plan_pin=ready['plan_pin'],original_Source_proof_pin=ready['original_Source_proof_pin'],actual_author_Source_pins=ready['source_pins'],selected_metadata_pins=ready['selected_metadata_pins'],selected_source_dependency_pins=plan['source_dependency_pins'])
 mark('Cumulative original 52 roots retained with whole Source TOP and fresh output; original54/caps unchanged.')
 science=plan['scientific_input_current7_pins'];need(len(science)==2 and {p['path'] for p in science}==SCI and science==plan['target_pins']==[plan['native_A1_SQLite_pin'],plan['native_A1_pool_pin']] and sum(p['size_bytes'] for p in science)==plan['planned_released_bytes']==202708660,'only exact two literal A1 roles')
 mother=doc(fresh(BASE.parent.parent/'one_actual_track_H150_NZ48_full370_component_source_v1_20261014/v6/PLAN.json'))
 need(science==[mother['native_A1_SQLite_pin'],mother['native_A1_pool_pin']],'original v6 A1 full provenance pins preserved')
 for p in science+plan['preserved_current7_pins']+plan['preserved_full_provenance_pins']:onlystat(p)
 result.update(scientific_inputs_current7_only=science,planned_released_bytes=202708660,preserved_current7_pins=plan['preserved_current7_pins'],preserved_full_provenance_pins=plan['preserved_full_provenance_pins'])
 copies=[]
 for pair in proof['whole_original_source_copies']:
  a,b=pair['original_full_pin'],pair['whole_unchanged_copy_full_pin'];need(read(a)==read(b),'whole unchanged original copied Source');copies.append(pair)
 need(len(copies)==4,'exact four whole Source provenance copies');result['verified_whole_original_Source_copies']=copies
 result['verified_complete_byte_inverses']={k:inverse(proof[k]) for k in ('host_complete_byte_inverse','retirement_complete_byte_inverse','publisher_complete_byte_inverse')}
 helper=read(plan['original_v6_vector_helper_pin']);original=read(plan['original_v6_vector_helper_provenance_pin']);need(helper==original and hashlib.sha256(helper[helper.index(b'def small_vectors('):helper.index(b'def main():')]).hexdigest()==proof['original_small_vectors_function_sha256']=='f036027ee8db20139817d715a4f981e5b4beca2cdf191c56677af635e348c794','whole exact original small_vectors helper');sv=function(helper,'small_vectors').decode()
 text_has(sv,["?mode=ro&immutable=1","PRAGMA query_only=ON","PRAGMA cache_size=-8192","PRAGMA mmap_size=0","PRAGMA temp_store=FILE","db.set_progress_handler","object.__new__(adapter.SavedNativeInput)","row['kind']==2","row['declared_count']==count","row['original_word_count']==count","os.pread(pf,count*4,row['native_payload_begin_byte'])","np.frombuffer(raw,dtype='<f4').copy()"],'original literal selective typed lookup and raw REAL32 copy')
 common=source['capture_source_common.py'].decode();worker=source['capture_A1_native_vectors.py'].decode();host=source['run_guarded_A1_native_vector_capture.py'].decode();retire=source['retire_literal2_completed_A1_compare_spools.py'].decode();writer=source['write_once_A1_native_vector_capture_SF_HF_CLI.py'].decode()
 text_has(common,["(('TRACK',1,name),count)","(('XMU$MCCG',4),('ZMU$MCCG',4),('WZMU$MCCG',4),('V$MCCG',14))","return 64*2**20 if Path(q) in large else 8*2**20"],'exact vectors and role-specific metadata bound')
 text_has(worker,["helper.small_vectors(plan['native_A1_SQLite_pin'],plan['native_A1_pool_pin'],c.VECTOR_PATHS,adapter,temp,budget)","values.dtype.str=='<f4'","values.view(helper.np.uint8).tobytes(order='C')","sha==row['native_payload_sha256']","offset==len(payload)==104","captured_REAL32_words=26","original_XSM_redecoded=False","native_engines_started=0","rawpath.open('xb')"],'104B four original vectors, no recast/fitted arithmetic/redecode/native engine')
 calls=[ast.unparse(n.func) for n in ast.walk(ast.parse(worker)) if isinstance(n,ast.Call)]
 need('helper.main' not in calls and not any('CDLL' in x or x.endswith('transport_multigroup') or x.endswith('transport_zonal') for x in calls),'capture cannot call original main/transport/kernel')
 need(plan['saved_adapter_import_bindings']==[x for x in mother['explicit_import_bindings'] if x['module']=='actual_track_saved_adapter'],'only original saved-data adapter import binding')
 text_has(host,["full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)","runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'vector-capture',resources)","runner.execute(inventories,'A1_native_26R4_104B_capture',cmd,600)","len(runner.records)==1", "for p in fixed:current7(p);c.same_pin(p['path'],p)","if p['path'] not in science:c.same_pin(p['path'],p)","resources=Resources();before=resources.check()"],'unchanged original owning serial600/whole1800 and exact parent fullhash once/current7 later')
 oldhost=source['original_all34_guard_host.py'].decode();start=' class Resources:';end=' resources=Resources();';need(oldhost[oldhost.index(start):oldhost.index(end)]==host[host.index(start):host.index(end)],'whole original Resources class byte unchanged')
 originalret=source['original_retire_literal4_completed_compare_spools.py'];need(function(originalret,'closure')==function(source['retire_literal2_completed_A1_compare_spools.py'],'closure'),'whole original literal4 closure function unchanged')
 mark('Four original Source copies and three complete inverses checked; whole small_vectors/Resources/closure unchanged; exact Source-only 4/26/104 scope and original owning guard retained.')
 depnames={p['path']:p for p in plan['source_dependency_pins']};fullpath='/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py';parentpath='/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/streaming_full_ledger_serializer_min5_source_bundle_v1_20261013/runtime/production_runner.py'
 full=read(depnames[fullpath]);parent=read(depnames[parentpath]);own=function(full,'OwnRSSSerialExecutor').decode();serial=function(parent,'SerialExecutor').decode();need(ast.parse(function(full,'OwnRSSSerialExecutor')).body[0].bases[0].id=='SerialExecutor','original guard MRO class')
 text_has(own,["self.resources.check()","if now-started>=limit:","if peak>=512:","self.bounded.terminate_group(process)","liveness_group_cleanup=True","no retry"],'unchanged actual watchdog/resource/512/noRetry Source');text_has(serial,["limit = min(float(cap), remaining)","self.deadline = time.monotonic() + total_seconds","self.stages_path = work / case / \"stages.json\""],'original runner stage/whole and persisted stage path')
 proofpins=plan['finite_prerequisite_pins'];need(proofpins==ready['finite_actual_completed_prerequisite_pins'],'finite completed prerequisites same READY/PLAN');fh=doc(proofpins['host']);fe=doc(proofpins['child']);fp=doc(proofpins['post']);closed(doc(proofpins['root_tools']),'actual_terminal_return',proofpins['host'],'report_pin');closed(doc(proofpins['post_tools']),'actual_review_return',proofpins['post'],'review_pin')
 need(fh['status']=='ACTUAL_EIGHT_FUEL_64T_FINITE18_P0_WORDS_CLOSED0_ONLY' and fh['failure'] is None and fh['secondary_failures']==[] and fh['final_report_resource_check_passed'] is True and fh['actual_evidence']==fe and fh['original_caps']==CAPS and len(fh['records'])==len(fh['actual_child_receipts'])==8 and all(x['status']=='PASS' for x in fh['records']),'genuine completed eight child Root0 finite prerequisite')
 need(fe['status']=='EIGHT_FUEL_64T_FINITE18_P0_RAW_WORDS_EQUAL' and fe['aggregation_metadata_only'] is True and [fe[k] for k in ('compared_completed_child_reports','compared_original_archives','compared_unique_nuclides','compared_temperature_records','compared_finite_dilution_nodes','compared_original_leaf_records')]==[8,16,8,64,1152,3456] and fp['schema']==plan['finite_post_schema'] and fp['status']==plan['finite_post_status']=='PASS_ACTUAL_EIGHT_FUEL_64T_128LANET_1152NODES_3456_FINITE_P0_LEAF_WORDS' and fp['failure'] is None and all(contains(fp,proofpins[k]) for k in ('host','child','root_tools')) and not any(p['path'] in SCI for p in fh['fixed_current_pins']),'actual finite post0 complete prerequisite and no ongoing A1 pair dependency')
 for d in (fh,fe,fp):need(all(d.get(k,False) is False for k in ('physics_qualified','full_reference_qualified','AAA_qualified','ABA_admitted','goal_complete')),'no inherited physics qualification')
 result['genuine_completed_finite_Root0_and_corrected_post0_pins']=proofpins;del fh,fe,fp
 mark('Real completed finite Root0 and corrected argument identity post0 are bound; producer metadata alone confers no broader qualification.')
 targetnode=next(n for n in ast.parse(retire).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='LITERALS' for t in n.targets));literal=ast.literal_eval(targetnode.value);actual=[dict(path=str(Path('/Users/wen/spot/validation/artifacts/axial-material-current-three-plane-raw-macro-compare-after-GENDF-cumulative25-20261014-v1-evidence')/name),sha256=sha,size_bytes=i[4],identity=i) for name,sha,i in literal];need(actual==science,'exact retirement literal2 Source fullpins')
 text_has(retire,["with path.open('xb') as file:","a.mode=='execute'","readonly['status']=='READONLY_READY_EXACT_LITERAL2_A1'","readonly['actual_released_pins']==[]","readonly['actual_released_bytes']==0","readonly['files_deleted'] is False","c.closed0(c.read(rt),'actual_terminal_return',rp,'receipt_pin')","host,child=c.check_capture(capture,a.capture_post_schema,a.capture_post_status)","child['original_A1_SQLite_pin']==TARGETS[0]","child['original_A1_pool_pin']==TARGETS[1]","host['actual_initial_parent_science_fullhash_pins']==TARGETS","closure(plan)","for p in TARGETS:full(p);resource_check()","fresh_process_preflight(a.mode,1)","fresh_process_preflight(a.mode,2)","os.O_DIRECTORY|os.O_NOFOLLOW","identity(os.stat(q.name,dir_fd=directory,follow_symlinks=False))==p['identity']","os.unlink(q.name,dir_fd=directory)","FAILED_PARTIAL_EXACT_LITERAL2_A1","FAILED_BEFORE_UNLINK"],'actual capture/post0 + genuine readonly0 + fresh process twice + both EOF + immediate directory FD7 only two unlink + partial facts')
 main=function(source['retire_literal2_completed_A1_compare_spools.py'],'main').decode();need(main.index('host,child=c.check_capture')<main.index('for p in TARGETS:full(p)')<main.index("fresh_process_preflight(a.mode,2)")<main.index('os.unlink('),'mandatory success/EOF/process gates precede unlink')
 text_has(retire,["subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=30,check=False)","['/bin/ps','-axo','pid=,ppid=,stat=,command=']","['/usr/sbin/lsof','-nP','-Fpcfn']+[p['path'] for p in TARGETS]","lsof['original_integer_exit_code']==1 and lsof['stdout']==lsof['stderr']==''","blocked==[]","peak<512*2**20 and time.monotonic()-started<600","f['artifact_bytes']+extra+sum(opened.values())<2*2**30","for p in plan['preserved_current7_pins']+plan['preserved_full_provenance_pins']:c.current(p)"],'fresh exact literal handle/process closure and unchanged retirement caps/preservation')
 oldreceipt=doc(plan['actual_original_literal4_receipt_pin']);need(oldreceipt['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY' and oldreceipt['failure'] is None and oldreceipt['actual_released_bytes']==405417320 and oldreceipt['actual_released_pins']==oldreceipt['exact_target_pins'] and all(not os.path.lexists(p['path']) for p in oldreceipt['actual_released_pins']),'old literal4 historical receipt/absent targets unchanged')
 oldplan=doc(plan['actual_original_literal4_plan_pin']);need(plan['original_native_pairs']==oldplan['original_native_pairs'] and plan['closure_pins']==oldplan['closure_pins'] and {p['path'] for p in plan['preserved_current7_pins']}=={p['path'] for p in oldplan['preserved_current7_pins'] if p['path'] not in SCI},'all original XSM/jsonl/results/failed history preserved except exact target2')
 draft=doc(author['preserved_unready_draft_freeze_pin']);need(draft['ready'] is False and draft['source_preparation_executed'] is False and draft['files_deleted'] is False,'unready draft not retroactively reclassified')
 for p in draft['selected_source_pins']:read(p,False)
 result.update(preserved_unready_draft_freeze_pin=author['preserved_unready_draft_freeze_pin'],preserved_unready_draft_Source_pins=draft['selected_source_pins'],original_literal4_history_receipt_pin=plan['actual_original_literal4_receipt_pin'],unchanged_original_literal4_closure_checked=True)
 text_has(common,["h['status']=='ACTUAL_A1_NATIVE_VECTOR_CAPTURE_26R4_104B_CLOSED0_ONLY'","h['failure'] is None","e['captured_original_record_count']==4","e['captured_REAL32_words']==26","e['captured_bytes']==104","d['captured_payload_sha256']==d['native_payload_sha256']==d['original_native_row']['native_payload_sha256']==hashlib.sha256(raw[offset:offset+4*count]).hexdigest()","closed0(read(proof['root_tools']),'actual_terminal_return',proof['host'],'report_pin')","closed0(read(proof['post_tools']),'actual_review_return',proof['post'],'review_pin')"],'capture4 typed rows/raw slices and genuine owning Root0/post0 enforced')
 text_has(writer,["selected=c.unique([ready_pin,ready['plan_pin'],ready['author_source_freeze_pin'],ready['original_Source_proof_pin']]+ready['source_pins']+ready['selected_metadata_pins'])","all(c.contains(peer,p) for p in selected+[generation_pin])","c.closed0(c.read(peer_tools),'actual_review_return',peer_pin,'review_pin')","c.closed0(c.read(generation_pin),'actual_Source_preparation_return',ready_pin,'ready_pin')","dependencies=c.unique(plan['source_dependency_pins']+selected+[peer_pin,peer_tools,generation_pin])","len(argv)==24","receipt_path.open('xb')"],'complete selected peer proof and genuine gen0 gates before exclusive once24 publication')
 mark('Exact literal2 retirement requires actual current104B capture/Root0/post0 and readonly0, two fresh ps/lsof checks, both full target EOFs and immediate directory FD7; original closure/failed/draft/literal4 history preserved.')
 for p in list(fullpins.values()):read(p,False)
 for p in list(statpins.values()):current(p)
 need(time.monotonic()-started<600 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)<512*2**20,'bounded independent Source audit SELF512/time600')
 result.update(status='PASS_FROZEN_A1_26_REAL32_104B_CAPTURE_AND_EXACT_LITERAL2_RETIREMENT_SOURCE_ONLY',failure=None,verified_full_Source_metadata_pins=list(fullpins.values()),verified_full_Source_metadata_count=len(fullpins),verified_dual_current7_only_pins=list(statpins.values()),metadata_large64MiB_exact_paths=sorted(LARGE),selected_metadata_count=457,author_Source_count=10,plan_Source_dependency_count=48,original_small_vectors_helper_sha256=proof['original_small_vectors_function_sha256'],exact_planned_vector_records=[dict(path=['TRACK',1,name],kind=2,words=count,offset_bytes=offset,captured_bytes=count*4) for name,count,offset in [('XMU$MCCG',4,0),('ZMU$MCCG',4,16),('WZMU$MCCG',4,32),('V$MCCG',14,48)]],actual_capture_not_started=True,actual_retirement_not_started=True,original_resources_class_whole_byte_identical=True,original_OwnRSS_guard_and_SerialExecutor_Source_MRO_verified=True)
except BaseException as error:
 result.update(status='FAILED_FROZEN_A1_CAPTURE_LITERAL2_SOURCE_REVIEW',failure=repr(error),verified_full_Source_metadata_pins=list(fullpins.values()),verified_current7_only_pins=list(statpins.values()))
finally:
 result.update(audit_source_pin=fresh(Path(__file__).absolute()),checks_completed=checks,elapsed_seconds=time.monotonic()-started,auditor_SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024))
 with REPORT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=result['status'],review_pin=fresh(REPORT),failure=result['failure'],Source_metadata_count=len(fullpins),current7_only_count=len(statpins),**FALSE)),flush=True)
if result['failure'] is not None:sys.exit(1)
