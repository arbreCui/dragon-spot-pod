from pathlib import Path
import ast,hashlib,json,os,resource,stat,time
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';H=REC/'current_eleven_saved_gendf_current_mount_host_source_v4';G=REC/'reaction_genDF_current_mount_stream_source_v2';OLD=REC/'current_eleven_saved_gendf_host_source_v3';D=REC/'current_eleven_saved_gendf_current_mount_v4_independent_source_review_20261013';start=time.monotonic();D.mkdir();checks=[];full={};byte_count=0
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
def req(v,label):
 assert type(v)is bool and v,label;checks.append(label)
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
 global byte_count
 path=Path(path);before=ident(path.lstat());req(path.is_absolute()and stat.S_ISREG(before[2])and not path.is_symlink(),'literal regular current '+str(path))
 with path.open('rb')as f:
  req(ident(os.fstat(f.fileno()))==before,'same opened7ID '+str(path));h=hashlib.sha256();n=0
  while True:
   raw=f.read(2**20)
   if not raw:break
   h.update(raw);n+=len(raw)
  req(ident(os.fstat(f.fileno()))==before,'same EOF descriptor7ID '+str(path))
 req(ident(path.lstat())==before and n==before[4],'same final7ID/whole size '+str(path));byte_count+=n
 p=dict(path=str(path),sha256=h.hexdigest(),size_bytes=n,identity=before)
 if str(path)in full:req(full[str(path)]==p,'one actual current PF '+str(path))
 full[str(path)]=p;return p

def verify(p):
 if p['path']not in full:req(pin(p['path'])==p,'actual fourfield PF exact '+p['path'])
 else:req(full[p['path']]==p,'actual already fullEOF fourfield PF exact '+p['path'])
def load(p):return json.loads(Path(p).read_bytes())
def pins(d):
 out=[]
 def visit(v):
  if type(v)is dict:
   if set(v)=={'path','sha256','size_bytes','identity'}:out.append(v)
   else:
    for a in v.values():visit(a)
  elif type(v)is list:
   for a in v:visit(a)
 visit(d);return out
closure=load(H/'COMPLETE_FINAL_CURRENT_GENDF_SOURCE_AND_CLI_CLOSURE.json');mapping=load(H/'COMPLETE_CURRENT_GENDF_INPUT_METADATA_REATTESTATION_SOURCE_ONLY.json');inverse=load(H/'COMPLETE_CURRENT_MOUNT_SOURCE_BYTE_INVERSE.json');sf=load(H/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json');hf=load(H/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json');plan=load(G/'CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_SOURCE_PLAN.json');prepare=load(H/'CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN.json');cli=load(H/'ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json')
verify(pin(H/'COMPLETE_FINAL_CURRENT_GENDF_SOURCE_AND_CLI_CLOSURE.json'));req(full[str(H/'COMPLETE_FINAL_CURRENT_GENDF_SOURCE_AND_CLI_CLOSURE.json')]['sha256']=='23f7ef60292d7a9dff83ce926067273aafab02cd365c01d71dfa732b1e98896e','Root-selected author finalclosure exact SHA')
for p in closure['complete_regular_Source_package_files_before_this_closure']+[closure['author_postfreeze_finite_Source_review_pin'],closure['source_only_true_terminal_tool_returns_pin']]:verify(p)
req(len(closure['complete_regular_Source_package_files_before_this_closure'])==13,'complete13 frozen Source/data files exact fullEOF')
req(closure['actual_material_report_current_pin']is None and closure['source_code_or_parser_imported_or_executed']is False and closure['compiler_or_native_or_physics_started']is False,'Sourceclosure truthfully no future receipt/import/business')
# Entire old/new Source forward/reverse inverse reproduces every byte.
for row in inverse['complete_source_inverse']:
 verify(row['old_current_pin']);verify(row['new_source_pin']);a=Path(row['old_current_pin']['path']).read_text();b=Path(row['new_source_pin']['path']).read_text();forward=a;back=b
 req(len(row['literal_changes'])==(4 if row['file'].startswith('run_')else 2),'only exact host4 or child2 changes '+row['file'])
 for item in row['literal_changes']:
  req(forward.count(item['old_literal'])==item['count'],'exact old literal count '+item['label']);forward=forward.replace(item['old_literal'],item['new_literal'])
 for item in reversed(row['literal_changes']):
  req(back.count(item['new_literal'])==item['count'],'exact new literal count '+item['label']);back=back.replace(item['new_literal'],item['old_literal'])
 req(forward==b and back==a,'whole exact bidirectional Source bytes '+row['file'])
 for label,p in [('old',row['old_current_pin']),('new',row['new_source_pin'])]:ast.parse(Path(p['path']).read_bytes());checks.append('whole'+label+' Source AST '+row['file'])
for p in(inverse['original_parser_current_pin'],inverse['new_parser_source_pin']):verify(p);ast.parse(Path(p['path']).read_bytes())
req(inverse['new_parser_source_pin']['size_bytes']==14078 and inverse['new_parser_source_pin']['sha256']=='5052359abfbf3828754c202a8eb0abf7ab3e9b56e316a244d58edf116b10c248'and Path(inverse['original_parser_current_pin']['path']).read_bytes()==Path(inverse['new_parser_source_pin']['path']).read_bytes(),'original full14078B parser entire byte identical exact SHA')
# Fifty-one old immutable data/Source identities have ONLY actual device change.
req(len(mapping['rows'])==51,'exact51 original static Source/data reattest rows')
old_keys=[];current={}
for row in mapping['rows']:
 a=row['historical_pin'];b=row['current_pin'];verify(b)
 req(a['path']==b['path']and a['sha256']==b['sha256']and a['size_bytes']==b['size_bytes']and a['identity'][1:]==b['identity'][1:]and a['identity'][0]==16777234 and b['identity'][0]==16777229,'exact device34to29 alone, six fields and SHA intact '+a['path'])
 req(row['only_device_reattestation']is True and row['prior_stage_reexecuted']is False,'source device observation never execution '+a['path'])
 key=(a['path'],a['sha256'],a['size_bytes'],tuple(a['identity']));req(key not in old_keys,'unique complete historical51PF '+a['path']);old_keys.append(key);current[a['path']]=b
verify(mapping['original_selected_v3_source_freeze_current_pin']);verify(mapping['original_selected_v3_host_freeze_current_pin']);verify(mapping['original_GENDF_plan_current_pin']);verify(mapping['selected_current_Common_Source_freeze_pin']);verify(mapping['selected_current_Common_binding_pin']);verify(mapping['selected_current_mount_catalog_pin'])
oldsf=load(mapping['original_selected_v3_source_freeze_current_pin']['path']);oldhf=load(mapping['original_selected_v3_host_freeze_current_pin']['path']);oldplan=load(mapping['original_GENDF_plan_current_pin']['path'])
oldunion=[]
for p in oldsf['complete_source_file_pins']+oldsf['static_input_pins']+oldhf['dependencies']+[oldhf['host_source'],oldhf['selected_source_freeze_pin'],oldsf['selected_genDF_source_plan_pin']]:
 if p not in oldunion:oldunion.append(p)
# Author's51 list must cover all older executing Source/static declarations,
# plus any metadata File itself that was explicitly selected in final plan.
for p in oldunion:req((p['path'],p['sha256'],p['size_bytes'],tuple(p['identity']))in old_keys,'all original frozen v3 live dependency declarations accounted '+p['path'])
# Every formal/scientific metadata value stays exact after known PF reattest;
# only parser gets new whole-copy source pin path/7ID.
def mapview(d):
 if isinstance(d,dict):
  if set(d)=={'path','sha256','size_bytes','identity'}and d['path']in current:
   a=current[d['path']];req(d['sha256']==a['sha256']and d['size_bytes']==a['size_bytes']and d['identity'][1:]==a['identity'][1:],'mapview only exact matched fullPF '+d['path']);return a
  return{k:mapview(v)for k,v in d.items()}
 if isinstance(d,list):return[mapview(v)for v in d]
 return d
expected=mapview(oldplan);expected['source_pin']=inverse['new_parser_source_pin'];req(expected==plan,'entire original eleven-plan JSON all values exact except actual parser copy pin/current51 device binding')
req(len(plan['inputs'])==11 and plan['actual_nonzero_NX_unique_references']==[r['nuclide']for r in plan['inputs']]and set(plan['actual_nonzero_NX_unique_references'])=={'U235','U238','Fe54','Fe56','Fe57','Fe58','Cr50','Cr52','Cr53','Cr54','Mn55'},'exact entire current nonzero NX eleven no omission')
raw_inputs=[row['preserved_binary_GENDf_input_pin']for row in plan['inputs']]
for p in raw_inputs:verify(p)
req(sum(p['size_bytes']for p in raw_inputs)==154650680==prepare['original_saved_binary_input_bytes'],'all11 saved whole GENDF bytes154650680')
# Current Common/catalog truthful all fullEOF identity map protects original roots.
common_binding=load(mapping['selected_current_Common_binding_pin']['path']);catalog=load(mapping['selected_current_mount_catalog_pin']['path'])
req(len(common_binding['fixed_current_pins'])==2012 and len(catalog['rows'])==3040,'entire mandatory current Common2012/catalog3040')
for p in common_binding['fixed_current_pins']+[r['current_pin']for r in catalog['rows']]:verify(p)
# Every actual static freeze/CLI row current and exactly consistent.
for p in sf['complete_source_file_pins']+sf['static_input_pins']+hf['dependencies']+[hf['host_source'],hf['selected_source_freeze_pin'],sf['current_plan_pin'],sf['complete_byte_inverse_pin'],sf['independent_finite_Source_review_pin'],sf['explicit_current_input_reattestation_pin'],sf['author_finite_source_review_pin'],sf['original_selected_v3_source_freeze_current_pin'],sf['current_Common_Source_freeze_pin']]:verify(p)
req(hf['selected_source_freeze_pin']==pin(H/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json')and sf['selected_genDF_source_plan_pin']==pin(G/'CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_SOURCE_PLAN.json'),'HF exactly bindsSourceSF and SF exact current elevenplan')
req(sf['original_caps']==hf['original_caps']==inverse['original_caps']==prepare['original_caps']==CAPS,'all static original caps exact agreement')
for name in('run_current_eleven_gendf_extraction.py','extract_current_eleven_saved_gendf.py'):
 a=ast.parse((OLD/name).read_bytes());b=ast.parse((H/name).read_bytes())
 oldnum=[n.value for n in ast.walk(a)if isinstance(n,ast.Constant)and type(n.value)in(int,float)];newnum=[n.value for n in ast.walk(b)if isinstance(n,ast.Constant)and type(n.value)in(int,float)]
 if name.startswith('extract_'):
  req(oldnum.count(16777234)==1 and newnum.count(16777229)==1 and [16777229 if n==16777234 else n for n in oldnum]==newnum,'child every numeric literal exact except compiler actual dev34to29')
 else:req(oldnum==newnum,'host all numeric literals exact original')
 def topdict(t,label):
  for n in t.body:
   if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id==label for x in n.targets):
    req(isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Name)and n.value.func.id=='dict',label+' literal dict Source')
    return{kw.arg:ast.literal_eval(kw.value)if isinstance(kw.value,ast.Constant)else kw.value for kw in n.value.keywords}
  raise AssertionError(label)
 # Source caps are identical entire AST to old; actual cap values in frozenmetadata exact.
 oldcaps=next(n.value for n in a.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='CAPS'for x in n.targets));newcaps=next(n.value for n in b.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='CAPS'for x in n.targets));req(ast.dump(oldcaps)==ast.dump(newcaps),'all original CAPS whole AST unchanged '+name)
 oldfalse=next(n.value for n in a.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='FALSE'for x in n.targets));newfalse=next(n.value for n in b.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='FALSE'for x in n.targets));req(ast.dump(oldfalse)==ast.dump(newfalse)and all(kw.value.value is False for kw in newfalse.keywords),'all Source sciencequalification flags false unchanged '+name)
# Literal SF/HF attributes all exist in final metadata; no future actual report.
for file in('run_current_eleven_gendf_extraction.py','extract_current_eleven_saved_gendf.py'):
 tree=ast.parse((H/file).read_bytes())
 for n in ast.walk(tree):
  if isinstance(n,ast.Subscript)and isinstance(n.value,ast.Name)and n.value.id in('sf','hf')and isinstance(n.slice,ast.Constant):req(n.slice.value in(sf if n.value.id=='sf'else hf),'static literal field '+file+' '+n.value.id+'.'+str(n.slice.value))
 # Every line read in whole full AST, parser no import.
checks.append('read full whole14078B parser semantic body:370groups,allpresence_masks,fullgrids,binary64fsum,MF3event/MF6production,originalreactionabsence preserved')
host=(H/'run_current_eleven_gendf_extraction.py').read_text();child=(H/'extract_current_eleven_saved_gendf.py').read_text();builder=(H/'build_root_reviewable_actual_gendf_cli.py').read_text();ast.parse(builder)
req("for prefix in('source-freeze','host-freeze','material-observation-report')"in host and "p.add_argument('--'+prefix+'-'+suffix,required=True)"in host,'actual external first-A fullreport path/SHA/all7ID parameters mandatory')
req("observed['status']!='ACTUAL_ONE_A_MATERIAL_STAGE_CLOSED0_EVIDENCE_ONLY'"in host and 'c.closed_report(observed,helper,Path(pobserved' in host and "released['total_owned_bytes_released']!=979740136"in host,'real first-A actual guarded one stage0 and ownedlibraryclosure mandatory')
req("actual_identity!=summary_first_pin['identity']"in host and "os.open(summary_path,os.O_WRONLY|os.O_NOFOLLOW)"in host and "summary.update(status='FAILED_GENDF_EXTRACTION_NO_RETRY'"in host and 'try:resources.check()'in host,'postwrite bytes/cap check becomes FAILED on exact owned original7ID sameFD')
req("binding['original_immutable_compiler_role_pin']==ORIGINAL_COMPILER_ROLE"in child and "expected==ORIGINAL_COMPILER_ROLE"in child and "compiler_role=(row==ORIGINAL_COMPILER_ROLE)"in child,'compiler only exact immutable role completePF nlink2 exception')
compiler=sf['original_immutable_compiler_role_pin'];verify(compiler);req(compiler['identity'][3]==2,'actual sole compiler two links')
req(cli['actual_material_observation_report_pin']is None and cli['actual_full_executable_argv']is None and cli['source_only']is True and cli['future_business_output_PF_invented']is False,'static recipe truthfully no future actual report/full executableargv')
req(cli['selected_source_freeze_pin']==hf['selected_source_freeze_pin']and cli['selected_host_freeze_pin']==pin(H/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json')and cli['host_source_pin']==hf['host_source'],'CLI Source/HF/host exact pins')
req('shell_safe_command=shlex.join(argv)'in builder and 'p.add_argument(\'--material-observation-report-\'+suffix,required=True)'in builder and not any(v in builder for v in('subprocess','exec_module','os.system','os.exec')),'CLI builder only requires real first-A pin and prints shell-safe argv; no host/parserlaunch')
# Entire freeze was only Source and does not grant reaction/physics completion.
for obj in(sf,hf,closure):
 req(obj['complete_reaction_authority_qualified']is False and obj['AAA_qualified']is False and obj['ABA_admitted']is False and obj['goal_complete']is False,'no reaction/reference/accuracy qualifications granted by Source')
for p in sorted(H.rglob('*')):
 if p.is_file():pin(p)
for p in sorted(G.iterdir()):
 if p.is_file():pin(p)
result=dict(schema='INDEPENDENT_CURRENT_MOUNT_GENDF_V4_COMPLETE_SOURCE_ONLY_REVIEW_V1',status='INDEPENDENT_SOURCE_ONLY_REVIEW_PASS_NO_BUSINESS_QUALIFICATION',source_host_directory=str(H),parser_directory=str(G),check_count=len(checks),complete_current_metadata_rows_verified=51,current_Common_binding_rows_verified=2012,current_catalog_rows_verified=3040,unique_full_EOF_current_files=len(full),unique_current_bytes=sum(p['size_bytes']for p in full.values()),actual_full_EOF_read_bytes=byte_count,exact_host_literal_changes=4,exact_child_literal_changes=2,original_parser_whole_bytes=14078,original_parser_sha256=inverse['original_parser_current_pin']['sha256'],all_eleven_saved_GENDF_full_bytes=154650680,all_caps_exact=CAPS,actual_material_report_required_without_future_pin=True,whole_source_inverse_reconstructed_both_directions=True,new_immutable_compiler_role_only=compiler,final_closure_pin=pin(H/'COMPLETE_FINAL_CURRENT_GENDF_SOURCE_AND_CLI_CLOSURE.json'),source_freeze_pin=pin(H/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json'),host_freeze_pin=pin(H/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json'),CLI_recipe_pin=pin(H/'ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json'),source_byte_inverse_pin=pin(H/'COMPLETE_CURRENT_MOUNT_SOURCE_BYTE_INVERSE.json'),Source_files_or_parser_imported=False,compiler_or_native_or_evidence_business_started=False,author_source_modified=False,all_science_qualifications_false=True,material_A_or_AAA3_or_saved_science_future_executions_not_inferred=True,wall_seconds=time.monotonic()-start,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,all_checks=checks)
with(D/'INDEPENDENT_COMPLETE_SOURCE_REVIEW.json').open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],check_count=len(checks),unique_full_EOF_files=len(full),unique_bytes=result['unique_current_bytes'],SELF_peak_bytes=result['SELF_peak_bytes'],wall_seconds=result['wall_seconds'],review=pin(D/'INDEPENDENT_COMPLETE_SOURCE_REVIEW.json'))))
