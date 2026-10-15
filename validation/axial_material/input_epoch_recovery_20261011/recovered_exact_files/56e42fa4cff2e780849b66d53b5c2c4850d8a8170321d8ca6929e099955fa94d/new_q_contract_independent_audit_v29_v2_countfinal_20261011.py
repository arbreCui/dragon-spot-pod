import ast,gzip,hashlib,json,os,pathlib,stat,time
B=pathlib.Path('/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_wbh7cowp');START=time.monotonic();checks=[];seen={}
def ck(v,s):
 if type(v)is not bool or not v:raise AssertionError(s)
 checks.append({'name':s,'passed':True})
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=pathlib.Path(p);a=p.lstat();ck(stat.S_ISREG(a.st_mode) and a.st_nlink==1,'regular single-link '+str(p));h=hashlib.sha256();n=0
 for q in (p,*p.parents):ck(not q.is_symlink(),'no alias '+str(q))
 with p.open('rb') as f:
  ck(ids(os.fstat(f.fileno()))==ids(a),'open '+str(p))
  for block in iter(lambda:f.read(1048576),b''):h.update(block);n+=len(block)
  ck(ids(os.fstat(f.fileno()))==ids(a),'EOF '+str(p))
 ck(ids(p.lstat())==ids(a) and n==a.st_size,'after '+str(p));return dict(path=str(p),size_bytes=n,sha256=h.hexdigest(),identity=ids(a))
def verify(r):
 got=pin(r['path']);want={k:r[k] for k in got};ck(got==want,'expected EOF7ID '+r['path']);
 if got['path'] in seen:ck(seen[got['path']]==got,'same repeated pin '+got['path'])
 seen[got['path']]=got;return got
M=json.loads((B/'FINAL_SOURCE_ONLY_MANIFEST.json').read_bytes());S=json.loads((B/'ACTUAL_SAVED_CLOSED_EVIDENCE_SCHEMA_REVIEW.json').read_bytes())
for k in ('metadata_contract_Source','Q_writer_Source','UNREADY_factory_Source','actual_saved_schema_review','preparation_Source'):verify(M[k])
for r in M['complete_saved_metadata_input_pins']:verify(r)
ck(S['all_actual_metadata_inputs']==M['complete_saved_metadata_input_pins'],'all178 original saved inputs exactly same')
ck(len(seen)==183,'183 distinct complete EOF7ID Source and actual inputs')
F=(B/'UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py').read_bytes();old=pathlib.Path(M['actual_original_closed_endpoints']['old_immutable_factory']['path']).read_bytes();newconst=M['factory_added_constants'].encode();ck(F.count(newconst)==1,'one added constant block');restored=F.replace(newconst,b'',1)
for r in reversed(M['factory_forward_changes']):
 a,b=r['before'].encode(),r['after'].encode();ck(restored.count(b)==1,'one reverse factory replacement '+b[:60].decode());restored=restored.replace(b,a,1)
ck(restored==old,'entire factory original byte inverse')
ot=ast.parse(old);nt=ast.parse(F)
def funcs(t):return {n.name:ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
of,nf=funcs(ot),funcs(nt);ck(set(of)==set(nf),'all factory definition names unchanged');changed=[k for k in of if of[k]!=nf[k]];ck(changed==['helper_Q_admission'],'only helper_Q_admission AST changed')
W=(B/'WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py').read_bytes();pre=M['Q_writer_original_prefix_before'].encode();newpre=M['Q_writer_original_prefix_after'].encode();src=pathlib.Path(M['actual_original_closed_endpoints']['original_resource_prefix_Source']['path']).read_bytes();ck(src.startswith(pre),'whole original prefix direct bytes');ck(W.count(newpre)==1,'one unchanged original resourceprefix except output');ck(hashlib.sha256(pre).hexdigest()==M['Q_writer_prefix_original_full_inverse_sha256'],'prefix expected SHA');ck(newpre.replace(b'axial-material-installed6a-helper-metadata-admission-v29-20261011',b'axial-material-stable-wire-sort-fullfresh-root-closure-v28-20261011')==pre,'only resourceprefix output binding changed')
ct=ast.parse((B/'installed6a_closed_metadata_admission_contract.py').read_bytes());fixed=next(ast.literal_eval(n.value) for n in ct.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FIXED_ENDPOINTS' for t in n.targets));ck(fixed==M['actual_original_closed_endpoints'],'contract actual endpoint constants match final Source manifest')
wt=ast.parse(W);const={}
for n in wt.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
  try:const[n.targets[0].id]=ast.literal_eval(n.value)
  except (ValueError,TypeError):pass
ck(const['CONTRACT_PIN']==M['metadata_contract_Source'],'Qwriter exact contract Source pin')
ck(const['ORIGINAL_PREFIX_PIN']==fixed['original_resource_prefix_Source'],'Qwriter exact original prefix Source pin')
# Match true closed tool objects independently; do not execute package Source.
def readfixed(key):return json.loads(pathlib.Path(fixed[key]['path']).read_bytes())
for key,initial,session,closed in [('pure_protocol_tools','68ece3',62042,'3a9510'),('fresh_protocol_tools','81e3f4',25973,'98d67b'),('pure_root_tools','9ffe85',53728,'afeb52'),('fresh_root_tools','89d121',29061,'4aa325')]:
 d=readfixed(key);ck(d['initial']['chunk_id']==initial and type(d['initial']['session_id'])is int and d['initial']['session_id']==session,'true initial '+key);c=d['closed'];ck(c['chunk_id']==closed and type(c['exit_code'])is int and c['exit_code']==0 and 'session_id' not in c,'true closed0 '+key)
ck(readfixed('pure_root_tools')['closed_output_truncated_by_tool'] is True,'pure Root truncated stdout flag retained, no full parse')
for key in ('pure_protocol_tools','fresh_protocol_tools','fresh_root_tools'):
 c=readfixed(key)['closed'];j=json.loads(c['output']);ck(type(j)is dict,'complete actual stdout independently parses '+key)
PB=readfixed('pure_binding');FB=readfixed('fresh_binding');P=json.loads(pathlib.Path(PB['actual_control_report']['path']).read_bytes());T=json.loads(pathlib.Path(FB['actual_complete_control_report']['path']).read_bytes())
ck(P['helper']['sha256']==fixed['installed_helper']['sha256'] and P['helper']['identity']==fixed['installed_helper']['identity'],'pure original controls actually ran installed6a')
ck(P['status']=='ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION','pure true control success')
ck(len(P['stages'])==5 and P['small_codecs']['rejections']==61,'all original pure stages / 61rejects')
ck([len(P['private_owner_consume_controls'][k]) for k in ('positive_controls','private_guard_rejections','accepted_str_subclass_equivalence_controls','partial_invalid_second_owner_rejections')]==[4,3,2,2],'full owner4/3/2/2')
ck([len(P['private_inactive_audit_snapshot_controls'][k]) for k in ('positive_controls','private_guard_rejections','last_use_failure_controls')]==[5,13,3],'snapshot all5/13/3')
I=P['read_open_short_index_state_controls'];ck((I['actual_attempts'],I['unique_records'],I['exception_count_bearing_markers'])==(35,9,2),'index collision/nonempty full35/9/2');ck(I['standard_and_forced_collision_full_nine_field_snapshot_exact'] is True,'forced collision full9exact')
K=P['saved_wire67_complete_fields_review'];ck((K['fixture_count'],K['returns'],K['raises'])==(67,14,53),'all67 complete saved wire controls');ck(K['complete_saved_fixture_fields_preserved'] is True,'wire67 all fixture fields retained')
ck(len(T['complete_return_fields_retained'])==27 and T['actual_complete_trace_counts']==dict(records=37446,attempts=37446,canonical_files=37445,external_graph_reads=1,no_subprocess_reexecuted=True),'fresh full27fields all37446realreads');ck(len(T['private_trace_controls']['positive_controls'])==4 and len(T['private_trace_controls']['rejections'])==3,'fresh full4positive3rejects')
G={k:T[k] for k in ('expected_complete_return_contract','actual_complete_verifier_return','actual_complete_ReadOpenAudit_trace')};decompressed={}
for k,r in G.items():
 verify(r);h=hashlib.sha256();n=0
 with gzip.open(r['path'],'rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block);n+=len(block)
 ck(h.hexdigest()==r['uncompressed_JSON_sha256'],'full gzip decompressed EOF SHA '+k);decompressed[k]={'bytes':n,'sha256':h.hexdigest()}
ck(decompressed['expected_complete_return_contract']==decompressed['actual_complete_verifier_return'],'all27 complete return gzip uncompressed SHA / length exactly same')
with gzip.open(G['expected_complete_return_contract']['path'],'rb') as a,gzip.open(G['actual_complete_verifier_return']['path'],'rb') as b:
 while True:
  x,y=a.read(1048576),b.read(1048576);ck(x==y,'complete27 actual expected full byte block')
  if not x:break
FC=T['private_full_inactive_audit_snapshot_controls'];ck(FC['all37446_actual_reads_from_same_genuine_phase'] is True and FC['no_second_graph_or_input_phase_substituted'] is True and FC['all_nine_fields_full_type_order_value_floatbits_and_counts_equal'] is True,'same phase all9full snapshot');ck(FC['default_complete_descriptor_type_order_floatbit_pin']==FC['consumed_complete_descriptor_type_order_floatbit_pin'],'all snapshot nested types / order / bits descriptor identical');ck(FC['complete_consumed_vs_default_wire']['every_default_and_consumed_wire_byte_compared'] is True and FC['complete_consumed_vs_default_wire']['full_gzip_EOF_verified'] is True,'same phase full9 wire EOF actual Root bound');ck(FB['full_same_phase_default_consume_snapshot_controls']==FC and FB['complete_three_lossless_gzip_artifacts']==G,'actual Root closure exact full three gzips / samephase scope')
# Original five guards and whole D/E current namespace, without production imports.
TP=pathlib.Path('/private/tmp/Root_current_original_account_phase_timing_m9t382tr/CURRENT_ACCOUNT_TIMING.json');T0=json.loads(TP.read_bytes());ck(hashlib.sha256(TP.read_bytes()).hexdigest()=='4f07c5d192d6417ca3f989f1fec2e57a135eb4abfa7d4a91106374f3e8005da8','original timing guard anchor')
for r in T0['original_five_guard_pins']:verify(r)
for d in T0['current_complete_D_E_freeze'].values():
 for r in d['files']:verify(r)
 for p,want in d['directories'].items():ck(ids(pathlib.Path(p).lstat())==want and not pathlib.Path(p).is_symlink(),'D/E exact directory7ID '+p)
 root=pathlib.Path(min(d['directories'],key=lambda p:len(pathlib.Path(p).parts)));ck({str(root),*(str(p) for p in root.rglob('*'))}=={r['path'] for r in d['files']}|set(d['directories']),'D/E full pathset '+str(root))
verify(T0['original_failed_provenance_pin']);ck(not pathlib.Path(M['candidate_Q_future_path']).parent.exists(),'Q endpoint not created');ck(M['actual_Q_pin'] is None and M['actual_Q_writer_closed_receipt'] is None and M['actual_factory_installed'] is False,'Q and factory all honest pending')
for p in tuple(seen.values()):ck(pin(p['path'])==p,'complete exact pins after audit '+p['path'])
# Review scope states these missed roots explicitly; no predicate or raw data task was executed.
J=next(n for n in wt.body if isinstance(n,ast.FunctionDef) and n.name=='joint');roots=ast.unparse(J)
blockers=[{'action':'Run new6a metadata Q writer','finding':'joint() keeps original v28 fresh roots but does not include its new Q Source package, v27 original pure H/O/Source, or the actual v27/v28 Root closure families. TrainingResources fresh roots also exclude them. Its joint_bytes therefore does not measure the complete new Q evidence family. Global96 policy itself remains original. Extend the new family accounting separately while retaining exact original prefix and caps; preserve synthetic alias lstat rule when accounting v27 fixture namespaces.','line':96,'category':'complete_joint_accounting'}]
Source_manifest_pin=pin(B/'FINAL_SOURCE_ONLY_MANIFEST.json')
frozen_checks=list(checks)
R=dict(schema='SPOT_V29_NEW6A_Q_CONTRACT_INDEPENDENT_SOURCE_ONLY_AUDIT_V1',status='BLOCKED_Q_WRITER_COMPLETE_JOINT_ACCOUNTING_SCOPE',Source_only=True,writer_factory_helper_production_Native_or_PS_executed=False,elapsed_seconds=time.monotonic()-START,check_count=len(frozen_checks),all_checks_typed_true=all(x['passed'] is True for x in frozen_checks),checks=frozen_checks,blockers=blockers,all_verified_inputs=list(seen.values()),Source_manifest=Source_manifest_pin,decompressed_gzips=decompressed,factory_only_changed_function=changed,factory_full_original_inverse_sha256=hashlib.sha256(restored).hexdigest(),original_resource_prefix_sha256=hashlib.sha256(pre).hexdigest(),original_caps_and_guards_preserved_in_Source=True,Q_and_factory_unexecuted=True,no_whole_INPUT_native_BOOT_AAA_ABA_admission=True)
p=pathlib.Path('/private/tmp/new_q_contract_independent_audit_v29_v2_countfinal_20261011.json');p.write_text(json.dumps(R,ensure_ascii=False,indent=2)+'\n');print(json.dumps(dict(report=pin(p),status=R['status'],verified_distinct_inputs=len(seen),check_count=R['check_count'],elapsed_seconds=R['elapsed_seconds'],blockers=blockers)))
