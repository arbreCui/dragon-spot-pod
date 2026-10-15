from pathlib import Path
import os,stat,json,hashlib,ast,math,re,datetime
ROOT=Path('/Users/wen/spot');A=ROOT/'validation/axial_material';B=ROOT/'validation/artifacts';R=A/'last_cprime_trim_combined_live_resource_v9_build_review_20261009';T=Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v9-root-execution-20261009');DST=Path('/private/tmp/spot_v9_actual_successful_RUN_source_witness_independent_review_20261009')
S=B/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-admission-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009';O=B/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009';TERM=B/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009'
F=A/'prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v9.py';F8=A/'prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v8.py';FS='44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46';DS='7bc3d176f58ad6ee92d640c799b3f8d79923c65b2bf27c3b545c511e282b53e0';PS='0297aa6543c36ca3f452b1948e0d034e218f71c253b08cd671c3c83cb01262fb';SS='ece13c5594c48bb22af8d507f1f40ef88457efa824e28200c6ddfced70cf3aed';TS='709a9592c8b4a56cba99c61b628db8fed91d0c49d76d75c360591f11fa1b9d27';RS='40ed15561767b5352e64ec45ecdc7f6110bef46335e1523d6dbfe6d3cb810bc3'
PINS={};COUNT=0
def chk(v,msg):
 global COUNT
 if not v:raise AssertionError(msg)
 COUNT+=1
def identity(p):
 x=p.lstat();chk(stat.S_ISREG(x.st_mode)and not p.is_symlink(),'regular '+str(p));return[x.st_dev,x.st_ino,x.st_mode,x.st_size,x.st_mtime_ns,x.st_ctime_ns,x.st_nlink]
def raw(p,h=None):
 p=Path(p);a=identity(p);v=p.read_bytes();chk(identity(p)==a,'stable '+str(p));s=hashlib.sha256(v).hexdigest();chk(h is None or s==h,'SHA '+str(p));PINS[str(p)]=dict(path=str(p),sha256=s,size=len(v),identity=a);return v
def pairs(rows):
 d={}
 for k,v in rows:
  if k in d:raise ValueError('duplicate key '+k)
  d[k]=v
 return d
def finite(v):
 if type(v)is float:chk(math.isfinite(v),'finitefloat')
 elif type(v)is dict:
  for k,x in v.items():chk(type(k)is str,'strkey');finite(x)
 elif type(v)is list:
  for x in v:finite(x)
 else:chk(type(v)in(str,int,bool,type(None)),'builtin JSON type')
def obj(p,h=None):
 x=json.loads(raw(p,h),object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in()).throw(ValueError(v)));finite(x);return x
def typed(x,y):
 if type(x)is not type(y):return False
 if type(x)is dict:return x.keys()==y.keys()and all(typed(x[k],y[k])for k in x)
 if type(x)is list:return len(x)==len(y)and all(typed(a,b)for a,b in zip(x,y))
 if type(x)is float:return x.hex()==y.hex()
 return x==y
def cd(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()).hexdigest()
def inventory(root):
 files={};dirs=[];links={}
 for folder,sub,names in os.walk(root,followlinks=False):
  for name in list(sub):
   p=Path(folder)/name
   if p.is_symlink():links[str(p.relative_to(root))]=os.readlink(p);sub.remove(name)
   else:dirs.append(str(p.relative_to(root)))
  for name in names:
   p=Path(folder)/name
   if p.is_symlink():links[str(p.relative_to(root))]=os.readlink(p)
   else:files[str(p.relative_to(root))]=hashlib.sha256(raw(p)).hexdigest()
 return dict(files=files,symlinks=links,directories=sorted(dirs))
source=raw(F,FS).decode();parent=raw(F8,'4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4').decode()
def defs(s):return {x.name:(x,ast.get_source_segment(s,x))for x in ast.parse(s).body if isinstance(x,(ast.FunctionDef,ast.ClassDef))}
a,b=defs(source),defs(parent);chk(len(a)==len(b)==65 and a.keys()==b.keys(),'all65functions');
for n,(tree,s)in a.items():chk(s==b[n][1]and ast.dump(tree,include_attributes=False)==ast.dump(b[n][0],include_attributes=False),'byte AST '+n)
raw(T/'record_root_terminal.py','b534c49f046d3869dba07e4101e907bd08de8c61599bc3a05a688a0733de5d9e');d=obj(O/'declaration.json',DS);prep=obj(TERM/'declaration_terminal_return.json',PS);e=obj(TERM/'terminal_return.json',TS);rt=obj(R/'run_terminal_tool_return.json',RS);seal=obj(O/'seal.json',SS)
chk(obj(R/'run_terminal_return.json',TS)==e,'RootR actualrun receipt exactcopy')
PYcmd=d['python_command'];command=[PYcmd,str(F),'run-build','--sha256',DS,'--prep-sha256',PS];chk(rt['command']==e['command']==command,'exactstandardrootrun CLI');chk((rt['initial_chunk_id'],rt['session_id'],rt['terminal_chunk_id'])==('bace6e',37772,'d425ef'),'genuineRootrun handle');chk(type(rt['exit_code'])is int and rt['exit_code']==0 and rt['closed']is True and type(e['returncode'])is int and e['returncode']==0,'truebuiltinrootint0closed');chk(e['actual_tool_result']==rt and e['record_producer']=='root'and e['actual_tool_terminal_return_observed']is True and e['record_written_after_actual_terminal_return']is True,'exactexternalROOTreceiptwrittenaftertrue0')
chk(e['source']==rt['source']==dict(path=str(F),sha256=FS)and e['declaration']==dict(path=str(O/'declaration.json'),sha256=DS)and e['prep_terminal_evidence']==dict(path=str(TERM/'declaration_terminal_return.json'),sha256=PS)and e['build_seal']==dict(path=str(O/'seal.json'),sha256=SS),'completefixedsource/decl/prep/sealchain')
chk(e['schema'].endswith('_V9_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1'),'exactV9terminalschema');chk(e['successful_combined_link_completion_observed']is True and e['successful_new_runtime_build_observed']is True and e['production_admission_observed']is False,'buildsuccess nofutureAPI')
sourceinv=inventory(S);chk(sourceinv==d['source_inventory']and len(sourceinv['files'])==11 and sourceinv['directories']==['runtime']and sourceinv['symlinks']=={},'SOURCE11 fullSHAwholemembers');outinv=inventory(O);chk(outinv['directories']==seal['directories']and outinv['symlinks']==seal['symlinks']=={} and outinv['files'].keys()==seal['files'].keys()|{'seal.json'} and all(outinv['files'][k]==h for k,h in seal['files'].items()),'completeOUT21sealed+seal22fullSHAallnames');chk(seal['schema'].endswith('_V9_BUILD_SEAL_V1'),'newV9seal')
chk(obj(TERM/'declaration_source_inventory.json',prep['source_inventory']['sha256'])==sourceinv,'PREPsourceinventorywitnessstillwhole11');raw(TERM/'declaration_full_stdout.json',prep['full_stdout']['sha256']);chk(raw(TERM/'declaration_full_stderr.txt',prep['full_stderr']['sha256'])==b'','PREPrawemptyerr');chk(type(prep['returncode'])is int and prep['returncode']==0 and prep['build_seal']is None and all(prep[k]is None for k in('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')),'PREP4 witnesses frozen noRUNpromotion')
stdout=raw(e['full_stdout']['path'],e['full_stdout']['sha256']);stderr=raw(e['full_stderr']['path'],e['full_stderr']['sha256']);chk(stdout==raw(rt['full_stdout']['path'],rt['full_stdout']['sha256']) and stderr==raw(rt['full_stderr']['path'],rt['full_stderr']['sha256'])==b'','completeRoot/TERM/T stdoutstderrbyteequal');chk(e['full_stdout']['path']==str(TERM/'run_full_stdout.json')and e['full_stderr']['path']==str(TERM/'run_full_stderr.txt'),'separatefixedTERMstdio');body=json.loads(stdout,object_pairs_hook=pairs);finite(body)
result=obj(O/'driver_result.json');audit=obj(O/'audit/result.json');stages=obj(O/'HISTORICAL_INPUT_TRIM_COMBINED_RUNTIME_LINK_V9/stages.json')['stages'];bi=obj(O/'audit/binary_identity.json');claim=obj(O/'execution_claim.json')
labels=['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit'];chk([x['label']for x in stages]==labels and all(x['status']=='PASS'for x in stages),'exact5orderedPASS');objects=d['actual_production_objects'];old=B/'axial-material-rank1-factor-cache-build-20261007';physical=B/'axial-material-spoasm-physical-abi-serial-guarded-build-20261007';dedup=B/'axial-material-rank1-factor-cache-memory-dedup-build-20261007';trim=B/'axial-material-rank1-factor-cache-last-cprime-trim-build-20261008';targets=[str(x/'runtime/Dragon')for x in(O,old,physical,dedup,trim)]
commands=[d['production_link_command'],['/usr/bin/nm','-g',*objects],['/usr/bin/nm','-g',targets[0]],['/usr/bin/otool','-L',*targets],[PYcmd,str(F),'audit-build','--sha256',DS,'--prep-sha256',PS]];chk([x['command']for x in stages]==commands,'all5originalcommands')
watches=[]
for stage in stages:
 log=O/(stage['label']+'.log');w=obj(log.with_suffix('.watchdog.json'));raw(log,stage['log_sha256']);chk(w['command']==stage['command']and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512,'actualwatchcmdint0/strict512/limitnone');chk(type(w['pid'])is int and w['pid']>0 and w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<w['wall_cap_seconds']<=stage['wall_cap_seconds']<=600 and 0<=w['elapsed_seconds']<w['wall_cap_seconds'],'actualownPIDcleanup/timebounded');watches.append(w)
chk(len({w['pid']for w in watches})==5,'fiveactualchildidentitiesonce');chk(watches==result['watchdogs']and watches[:4]==audit['previous_stage_watchdogs'],'driverauditactualwatchdeepagree');chk(watches[-1]['pid']==17280 and watches[-1]['sampled_peak_rss_mib']==501.15625,'actualaudit17280sample501');chk(raw(O/'audit/audit.log')==b'AXMAT-COMBINED-RUNTIME-LINK-AUDITED\n','actualaudit success marker fullraw')
chk(result['classification']=='COMPLETE_COMBINED_RUNTIME_LINK_IDENTITY_ONLY'and result['error']is None and audit['classification']=='PASS_COMBINED_RUNTIME_LINK_IDENTITY_ONLY'and audit['binary_status']=='PASS'and audit['declaration_sha256']==DS and bi['status']=='PASS','onlylinkidentitydriverauditPASS');chk(claim['declaration_sha256']==DS and claim['prep_terminal_evidence']==e['prep_terminal_evidence']and type(claim['parent_pid'])is int and claim['parent_pid']>0 and type(claim['retries'])is int and claim['retries']==0,'singlezeroRetryexecutionclaim')
for k in('historical_whole_component_body','actual_last_cprime_trim_component_INPUT'):chk(audit[k]==d[k],'auditorfullINPUTbinding '+k)
for r in(result,audit,e):
 for k in('native_transport_executed','mathematical_controls_newly_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'):chk(r[k]is False,'actualscopefalse '+k)
chk(e['scientific_qualification']is False and result['fresh_cold_AAA_required']is True,'noqualification/numericalsolver newfuturecoldrequired')
tails=['actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources'];chk(set(body)=={'result',*tails}and typed(body['result'],result)and all(typed(body[k],e[k])for k in tails),'completefullstdoutdriverandall4tailsdeepagree');elapsed=e['actual_elapsed_seconds'];size=e['actual_archive_bytes'];resources=e['actual_resources'];chk(e['actual_tail_check']=='PASS'and type(elapsed)in(int,float)and math.isfinite(elapsed)and result['elapsed_seconds']<=elapsed<1800 and type(size)is int and 0<size<2*2**30,'actualtailsPASSfinite1800/strict2GiB');archive=sum(PINS[str(S/x)]['size']for x in sourceinv['files'])+sum(PINS[str(O/x)]['size']for x in outinv['files']);chk(archive==size==153579305,'actualwholeSOURCE+OUT153579305bytesnotBASEonly');chk(elapsed==307.69427295797504,'Rootactualelapsed307.694272')
for k,v in dict(total_wall_seconds=1800,stage_wall_seconds=600,rss_cap_mib=512,threads=1,numeric_children_at_once=1,retries=0,archive_reserve_bytes=2*2**30,artifact_budget_bytes=96*2**30,min_free_bytes=8*2**30).items():chk(type(d[k])is int and d[k]==v,'frozencap '+k)
for snapshot in [resources,result['resources'],*[s[k]for s in stages for k in('resource_before','resource_after')]]:
 chk(snapshot['artifact_budget_bytes']==96*2**30 and snapshot['min_free_bytes']==8*2**30 and snapshot['resource_scope_policy']==d['resource_scope_policy']and snapshot['resource_scope_contract']==d['resource_scope_contract']and snapshot['declared_resource_roots']==d['resource_roots']and set(d['resource_roots']).issubset(snapshot['resource_roots'])and 0<=snapshot['artifact_bytes']<=96*2**30 and snapshot['disk_free_bytes']>=8*2**30,'allretainedactualresourcesold96/free8/rootscomplete')
chk(size<=resources['artifact_bytes'],'archive includedresource tail')
# Independent raw text parsing only; no nm/otool/Fortran or business source execution.
def symbols(text):
 out=[]
 for line in text.splitlines():
  if not line.strip():continue
  m=re.fullmatch(r'\s*([0-9a-fA-F]+)\s+([A-Za-z])\s+(\S+)\s*',line)
  if m:
   if m[2].upper()!='U':out.append(dict(address=m[1],kind=m[2],name=m[3]))
  else:chk(re.fullmatch(r'\s*U\s+\S+\s*',line)is not None,'literalnmrecord')
 return out
objlog=raw(O/'metadata/objects.log').decode();sections={};which=None;aliases={p:p for p in objects}|{Path(p).name:p for p in objects}
for line in objlog.splitlines():
 if line.endswith(':')and line[:-1]in aliases:
  which=aliases[line[:-1]];chk(which not in sections,'uniquesection');sections[which]=[]
 elif line.strip():chk(which is not None,'nmsection owner');sections[which].append(line)
chk(set(sections)==set(objects),'all4objects actualnmsections');ex=symbols(raw(O/'metadata/executable.log').decode());definitions={}
for p,name in zip(objects,('_spot1p64_','_spoasm_','_flu2dr64_','_flu_')):
 o=symbols('\n'.join(sections[p]));h=[x for x in o if x['name']==name and x['kind'].upper()=='T'];q=[x for x in ex if x['name']==name and x['kind'].upper()=='T'];chk(len(h)==len(q)==1,'onegenuineactualsymbol '+name);raw(p,d['files'][p]);definitions[name]=dict(object=dict(path=p,sha256=d['files'][p]),object_symbol=h[0],executable_symbol=q[0])
chk(definitions==bi['actual_object_definitions'],'fullraw fourobject/executabledefinitions independentlyequal')
for x in ex:chk(not any(w in x['name'].lower()for w in('axmat_capture','axmat_rank1_capture','spot1p64_original','spot1p64_dense','original_cache_mod','dense_cache_mod','physical_unit')),'observer/reference exclusion')
deps={};current=None
for line in raw(O/'metadata/dependencies.log').decode().splitlines():
 if line.endswith(':')and line[:-1]in targets:current=line[:-1];chk(current not in deps,'distinctdepsection');deps[current]=[]
 elif line.strip():chk(current is not None and line.startswith(('\t',' ')),'literaldependencyrecord');deps[current].append(line.strip())
chk(set(deps)==set(targets)and all(deps[p]==deps[targets[0]]and deps[p]for p in targets)and deps==bi['dependencies'],'all5completedependencylists rawexact');runtimepin=dict(path=str(O/'runtime/Dragon'),sha256=outinv['files']['runtime/Dragon']);chk(runtimepin==result['corrected_runtime']==bi['actual_runtime'],'actualnewlinkedruntimebytepin')
olddecl=obj(old/'declaration.json');link=list(d['production_link_command']);link.remove(objects[1]);link[link.index(objects[0])]=str(old/'build/SPOT1P64.o');link[-1]=str(old/'runtime/Dragon');chk(link==olddecl['build_commands'][2]==d['link_inverse']['original_link_command'],'wholeoriginal92literalinverse')
rawmeta=obj(O/'raw_metadata_receipt.json');chk(rawmeta['files']=={x+'.log':outinv['files'][x+'.log']for x in labels[:4]}and rawmeta['before_binary_identity_gates']is True and rawmeta['complete_raw_tools_and_link_stdout']is True,'beforegatesrawmetadata4receiptfullSHA');chk(bi['raw_metadata']=={x:dict(path=str(O/(x+'.log')),sha256=outinv['files'][x+'.log'])for x in labels[1:4]},'binaryrawmetadata pinsagree');chk(bi['exact_original92_token_inverse']is True and bi['sole_object_changes']==['SPOT1P64.o','SPOASM.o']and bi['all_other_original_link_inputs_unchanged']is True and bi['production_references_and_observers_excluded']is True and bi['whole_instruction_equivalence_claimed']is False,'binaryexactscope nospeculativedisassembly')
encoded=obj(S/'input_specs.json','2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa');original=obj(A/'combined_runtime_complete_historical_input_specs_20261007.json','2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa');historical=obj(B/'axial-material-physical-dedup-combined-runtime-build-20261007/declaration.json','aa3e33a10b64deb947f82fd9f8b19559f9f700f58396e641a4e66def5d4b46a4');chk(typed(encoded,original)and typed(encoded['metadata']['historical_actual_components'],historical['actual_components']),'whole19356767 sevenBODY fulltyped originaldeep equality');component=encoded['metadata']['historical_actual_components'];chk(len(component)==7 and cd(component)=='a0b0445e79f91f5d3767ee57719937a5188608f6a22f77d62b17c5036950e130','originalwhole7bodydigest')
trimbody=obj(S/'trim_component_admission_INPUT.json','a4662b853831357c299de0c28d1d19e2a869f81c6308081f6fa1d7833fd797bb');trimoriginal=obj(A/'last_cprime_trim_build_review_20261008/actual_complete_production_admission.json','fed2090ee0db4bb718c6c3fbbc9ed520ed9eeddda3fca6b2cadc2f4623edb114');chk(typed(trimbody,trimoriginal)and len(trimbody)==73,'fulloriginal73trimfed209typevalueequal');chk(d['actual_last_cprime_trim_component_INPUT']['trim_native_RSS_proof_obtained']is False and d['actual_last_cprime_trim_component_INPUT']['old_capture_RSS_transferred']is False,'trimINPUTonlynomemorytransfer')
config=obj(T/'config.json');chk(config['factorySha']==FS and config['declarationSha']==DS and config['prepSha']==PS and config['sealSha']==SS and config['terminalSha']==TS and config['terminalPath']==str(TERM/'terminal_return.json')and config['failed_terminal_sha']is None,'actualrecorderliveconfigsuccesschainonly');chk(not os.path.lexists(O/'closeout_failure.json'),'noactualpostsealfailure')
chk(set(p.name for p in TERM.iterdir())=={'declaration_full_stderr.txt','declaration_full_stdout.json','declaration_source_inventory.json','declaration_terminal_return.json','run_full_stdout.json','run_full_stderr.txt','terminal_return.json'},'exactTERM7PREPplusRUNrawreceipt')
prior=obj(Path('/private/tmp/spot_v9_actual_PREP_source_witness_independent_review_20261009/REPORT.json'),'22498a7e2e1eedc0aaa3709d1b8e851e3345a14d87f41626907a37492f9abe57');
for v in prior['full_fresh_reviewed_pins']:
 path=Path(v['path'])
 if path==T/'config.json':continue
 raw(path,v['sha256']);chk(identity(path)==v['identity'],'frozen44PREPsource metadata identity '+str(path))
for path,v in PINS.items():chk(identity(Path(path))==v['identity'],'allsmallreviewedpinsstableclose')
report=dict(schema='AXMAT_V9_ACTUAL_SUCCESSFUL_RUN_SOURCE_SEAL_WITNESS_INDEPENDENT_REVIEW_V1',status='PASS',scope='ACTUAL_V9_SOURCE11_PREP4_OUT22_WATCH5_RAWLOGS_BINARY_TEXT_4TAILS_TRUE_ROOT0_FULL_SEVEN_AND_TRIM_ONLY',factory_sha256=FS,declaration_sha256=DS,PREP_sha256=PS,seal_sha256=SS,terminal_sha256=TS,Root_actual_tool_observation_sha256=RS,Root_actual_handle=dict(initial_chunk_id='bace6e',session_id=37772,terminal_chunk_id='d425ef',exit_code=0,closed=True),actual_independent_review_tool_terminal=None,observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),allSOURCE11_fullfreshSHA_and_membernames=True,allPREP4_bytefrozen=True,wholeOUTseal21plusseal22_freshSHA_namespace=True,whole5orderedPASS_originalCLI_once=True,all5ownPID_trueint0_watch512guard_cleanup_andcaps=True,audit_watch_actual=dict(pid=watches[-1]['pid'],elapsed_seconds=watches[-1]['elapsed_seconds'],sampled_peak_rss_mib=watches[-1]['sampled_peak_rss_mib'],rss_cap_mib=512,own_child_only=True,cleanup=True),fast4sampledRSS0_is_not_true_zero_memory=True,watch_summaries=[{k:w[k]for k in('pid','returncode','elapsed_seconds','sampled_peak_rss_mib','limit_failure','wall_cap_seconds','rss_cap_mib','own_child_only','liveness_group_cleanup')}for w in watches],RootrawstdioandTERMraw_exact=True,all_four_actual_tails=dict(actual_tail_check=e['actual_tail_check'],actual_elapsed_seconds=elapsed,actual_archive_bytes=size,resource_scope_policy=resources['resource_scope_policy'],declared_resource_roots_count=len(resources['declared_resource_roots']),dynamic_complete_resource_roots_count=len(resources['resource_roots']),family_artifact_bytes=resources['artifact_bytes'],disk_free_bytes=resources['disk_free_bytes']),wholeSOURCE_OUTlogicalbytes=size,original65sourcefnAST_byteexact=True,original_parser_retained_no153adoption=True,original512_600_1800_thread1_onechild_zeroRetry_2GiB_96GiB_free8_caps_unchanged=True,independently_reparsed_raw_nm_and_otool_text_identity_equals_saved_binary_identity=True,whole_original92_link_token_inverse=True,whole19356767sevenINPUT_fulltyped_original_bodyequal=True,whole73trimfed209fulltypedequal=True,actual_trim_top_level_key_count=73,prior_PREP_report74label_was_inexact_not_a_field_filter=True,preexisting_source_MRO_and_unit_physicalcontrols_pins_bytefrozen=True,all_compilation_identity_scopes_false_native_transport_FLU_AAA_ABA=True,oldV7_V8failure_not_promoted=True,prior_source_and_PREP_audit_report_SHA='22498a7e2e1eedc0aaa3709d1b8e851e3345a14d87f41626907a37492f9abe57',allfresh_fullSHA_pins=list(PINS.values()),checks_passed=COUNT,reviewer_business_module_API_constructor_admit_audit_build_RUN_called=False,reviewer_formal_ART_written=False,limitations=['True PASS is scoped to the actual bounded build/link identity chain and preserved full INPUT metadata, not new native full FLU or cold accuracy or combined transport RSS qualification.','Audit peak501.15625MiB is a sampled own-child ps measurement under the unchanged guard, not exact continuous peak or whole host RSS. Fast child sampled0 does not prove physical0MB.','This run passing does not establish the two private last-use del statements as its causal memory improvement; no attribution to parser pooling or allocation line is made.','Complete35647canonical/35GB bytes, graph235528rows/86namespaces/186aliases/445absences and live dynamic231resource union are independently covered by graph auditor, not duplicated here. Whole PREP/RUN input admission waits for that true separate PASS.','No original or new production_admission or other business API, constructor, PREP/RUN, native solver, compiler/nm/otool/watch/probe was invoked by the independent reviewer. Pure STDlib parsed retained raw text/JSON and hashed files only.'])
with (DST/'REPORT.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
with (DST/'REPORT.txt').open('x')as f:f.write('PASS：V9唯一实际RUN Root bace6e/session37772→d425ef EXIT0 CLOSED。独审SOURCE11/PREP4、完整OUT21封存+seal自身共22、5阶段PASS/5原watch/完整rawstdoutstderr及四真实tails，全部一致。audit ownPID17280采样501.15625MiB<原512，43.255408625s；全tail307.694272958s，SOURCE+OUT153579305B<2GiB。原65函数/原parser/全2cad七BODY及73项fed209 trim全深类型保持；原512/600/1800/thread1/onechild/0retry/96GiB/free8不变。仅build/link identity通过，不声称新native/FLU/AAA/ABA或fd3因果RSS改善；完整35GB图与231根由另一独立审查者核，需该真实PASS后Root准入。未调用任何业务API或程序。\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status='PASS',scope=report['scope'],pins=len(PINS),checks=COUNT,SOURCE11=True,OUT22=True,PREP4=True,stage5PASS=True,audit_sampled_RSS=501.15625,elapsed=elapsed,archive=size,report_sha256=hashlib.sha256((DST/'REPORT.json').read_bytes()).hexdigest(),no_business=True)))
