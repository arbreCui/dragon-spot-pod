"""New Source only: split one CLE operand string; never import or run candidates."""
import ast,copy,hashlib,json,os,resource,stat,time
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'aaa_three_plane_streaming_pipeline_source_v9'
NEW=Path(__file__).resolve().parent.parent
OLD_CLI=REC/'ROOT_EXACT_ACTUAL_PIPELINE_V9_ARGV_20261013.json'
NEW_CLI=REC/'ROOT_EXACT_ACTUAL_PIPELINE_V10_ARGV_20261013.json'
CAUSE=REC/'ACTUAL_PIPELINE_V9_CLE_COLUMN_RANGE_FAILURE_CAUSE_20261013.json'
RETURNS=REC/'ACTUAL_PIPELINE_V9_AFTER_EXACT_TWO_RELEASE_TRUE_TOOL_RETURNS_20261013.json'
START=time.monotonic();checks=[]
def need(ok,name):
 if not ok:raise RuntimeError(name)
 checks.append(name)
def identity(p):
 s=Path(p).lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);before=identity(p)
 need(stat.S_ISREG(before[2])and not any(v.is_symlink()for v in(p,*p.parents)),'regular literal no-alias Source/provenance:'+str(p))
 with p.open('rb')as f:
  s=os.fstat(f.fileno());need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before,'opened7ID:'+str(p))
  sha=hashlib.file_digest(f,'sha256').hexdigest();s=os.fstat(f.fileno());need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before==identity(p),'fullEOF7ID:'+str(p))
 return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
def verify(p):need(pin(p['path'])==p,'actual exact SHA/all7ID:'+p['path'])
def write(p,v):
 raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode();save(p,raw)
def save(p,raw):
 if Path(p).exists():need(Path(p).read_bytes()==raw,'existing unfrozen draft bytes identical, never rewritten:'+str(p));return
 with Path(p).open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
oldhf=json.loads((OLD/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json').read_text());oldcli=json.loads(OLD_CLI.read_text())
need(len(oldhf['dependencies'])==257,'complete original v9 257 dependency rows')
for p in oldhf['dependencies']+[oldhf['host_source']]+list(oldcli['mandatory_external_bindings'].values()):verify(p)
original=(OLD/'run_actual_three_plane_pipeline.py').read_text()
oldview="viewops='PROJECT AX AXTRACK AXSYSTEM AXMACRO GRCON SYS1 SYS2 SYS3 TRACK_f1 TRACK_f2 TRACK_f3'"
newview="viewops='PROJECT AX AXTRACK AXSYSTEM AXMACRO GRCON\\n  SYS1 SYS2 SYS3 TRACK_f1 TRACK_f2 TRACK_f3'"
changes=[('fresh_output_namespace',"-20261012-v9'","-20261012-v10'"),('exact_host_freeze_schema','COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V9','COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V10'),('CLE_operand_whitespace_only',oldview,newview)]
text=original
for name,a,b in changes:need(text.count(a)==1,'one exact original Source literal:'+name);text=text.replace(a,b,1)
ast.parse(text);restored=text
for name,a,b in reversed(changes):need(restored.count(b)==1,'one exact new Source literal:'+name);restored=restored.replace(b,a,1)
need(restored==original,'entire old host bytes restored except exactly two version literals and operand whitespace')
save(NEW/'run_actual_three_plane_pipeline.py',text.encode())
for name in ('actual_inputs_and_readback.py','mutate_owned_control.f90','direct_alias_entry_controls.f90'):
 save(NEW/name,(OLD/name).read_bytes());need((NEW/name).read_bytes()==(OLD/name).read_bytes(),'three complete helper bytes unchanged:'+name)

# Only compile metadata paths move; every selected real producer/object pin
# retains its complete existing SHA, size and genuine current seven fields.
alias=json.loads((OLD/'DIRECT_ALIAS_ENTRY_BINDING.json').read_text());alias['new_probe_source']=str(NEW/'direct_alias_entry_controls.f90');write(NEW/'DIRECT_ALIAS_ENTRY_BINDING.json',alias)
interface=json.loads((OLD/'DECLARED_EXECUTION_INTERFACE.json').read_text());interface.update(schema='DECLARED_ACTUAL_AAA3_STREAMING_ONE_SERIAL_50_STAGE_INTERFACE_V10',host_source=str(NEW/'run_actual_three_plane_pipeline.py'),output_root='/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v10')
interface['view_operand_card_whitespace_fix_only']=True;write(NEW/'DECLARED_EXECUTION_INTERFACE.json',interface)
for name in ('CORRECTED_SOURCE_LIFECYCLE_EVIDENCE.json','COMPLETE_V8_TO_V9_OWNED_COPY_LIFECYCLE_BYTE_INVERSE.json','AUTHOR_FINITE_OWNED_COPY_LIFECYCLE_SOURCE_REVIEW.json','README.txt'):
 save(NEW/name,(OLD/name).read_bytes())

# Restricted static AST evaluation: no import, execution of candidate function,
# compiler, CLE or solver. Evaluate only literal string construction syntax.
def literal(node,env):
 if isinstance(node,ast.Constant):return node.value
 if isinstance(node,ast.Name):return env[node.id]
 if isinstance(node,ast.List):return[literal(n,env)for n in node.elts]
 if isinstance(node,ast.Tuple):return tuple(literal(n,env)for n in node.elts)
 if isinstance(node,ast.BinOp)and isinstance(node.op,ast.Add):return literal(node.left,env)+literal(node.right,env)
 if isinstance(node,ast.Subscript):return literal(node.value,env)[literal(node.slice,env)]
 if isinstance(node,ast.Call)and isinstance(node.func,ast.Attribute)and node.func.attr in('replace','rsplit'):
  target=literal(node.func.value,env);need(isinstance(target,str),'static string method only')
  return getattr(target,node.func.attr)(*[literal(a,env)for a in node.args])
 raise RuntimeError('unsupported static AST syntax:'+ast.dump(node))
def decks(source):
 tree=ast.parse(source);env={};main=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
 for n in tree.body:
  if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id=='BOOT_PREFIX':env['BOOT_PREFIX']=literal(n.value,env)
 for n in ast.walk(main):
  if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id in('precheck','viewops','bootdeck'):
   name=n.targets[0].id
   if name=='bootdeck'and 'BOOT_PREFIX'in env:env[name]=literal(n.value,env)
   elif name!='bootdeck':env[name]=literal(n.value,env)
 result={};oracles={};direct=[]
 for n in ast.walk(main):
  if isinstance(n,ast.For)and isinstance(n.target,ast.Tuple):
   names=[v.id for v in n.target.elts]
   if names==['label','head','ops','message']:
    for label,head,ops,message in literal(n.iter,env):
     if label=='view_system_alias':direct.append(dict(case=label,expected_abort=message,CLE_card_generated=False));continue
     result[label]=head+'AXOUT ARCOUT := SPOBVX64: '+ops+' :: RANK 1 EDIT 0 ;\nEND: ; QUIT "LIST" .\n';oracles[label]=message
   elif names==['label','params','message']:
    rows=literal(n.iter,env)
    if rows and rows[0][0]=='pair_missing_rank':
     for label,params,message in rows:result[label]=env['precheck']+'AXOUT ARCOUT := SPOBVX64: '+env['viewops']+' :: '+params+' ;\nEND: ; QUIT "LIST" .\n';oracles[label]=message
  if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='refuse'and n.args and isinstance(n.args[0],ast.Constant)and str(n.args[0].value).startswith('lifecycle_'):
   label=n.args[0].value;result[label]=literal(n.args[1],env);oracles[label]=literal(n.args[2],env)
 result['BOOT_positive']=env['bootdeck']
 return result,oracles,direct,env['viewops']
before,before_oracles,before_direct,view_before=decks(original)
after,after_oracles,after_direct,view_after=decks(text)
need(set(before)==set(after)and len(after)==8,'all five CLE-negative plus two lifecycle plus one positive decks')
need(before_oracles==after_oracles and before_direct==after_direct and len(after_direct)==1,'all exact original eight strict view/lifecycle families including direct alias retained')
need(view_before.split()==view_after.split()and len(view_after.split())+2==14,'fourteen ordered operand tokens exact including AXOUT ARCOUT')
need(view_before.rsplit(' ',1)[0].split()==view_after.rsplit(' ',1)[0].split()and len(view_after.rsplit(' ',1)[0].split())+2==13,'exact rsplit missing-final-operand negative remains thirteen including AXOUT ARCOUT')
cards=[]
for name,new in after.items():
 old=before[name];need(old.split()==new.split(),'full CLE deck tokens identical:'+name)
 need(all(len(line)<=120 for line in new.splitlines()),'every generated CLE card <=120:'+name)
 cards.append(dict(case=name,old_max_card_columns=max(map(len,old.splitlines())),new_max_card_columns=max(map(len,new.splitlines())),all_tokens_identical=True,expected_abort=after_oracles.get(name),new_complete_CLE_deck=new))
need(before['BOOT_positive']==after['BOOT_positive'],'positive two-line BOOT literal whole bytes unchanged')
cause=json.loads(CAUSE.read_text());need(cause['actual_exit_code']==-5 and cause['exact_expected_operator_message_absent']is True and cause['engineering_three_plane_closed0']is False,'actual failed v9 cause retained without qualification')
provenance=[pin(CAUSE),pin(RETURNS),pin(OLD/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'),pin(OLD_CLI)]
for key in('actual_summary_pin','Root_true_terminal_receipt_pin','actual_failed_stage_watchdog_pin','actual_log_pin','actual_input_deck_pin','original_lexer_source_pin'):
 verify(cause[key]);provenance.append(cause[key])
write(NEW/'COMPLETE_V9_TO_V10_VIEW_OPERAND_WHITESPACE_BYTE_INVERSE.json',dict(schema='COMPLETE_V9_TO_V10_ONLY_CLE_WHITESPACE_SOURCE_BYTE_INVERSE_V1',old_host_source_pin=oldhf['host_source'],new_host_source_pin=pin(NEW/'run_actual_three_plane_pipeline.py'),literal_changes=[dict(label=n,old_literal=a,new_literal=b,count=1)for n,a,b in changes],complete_inverse_equal=True,BOOT_PREFIX_full_bytes_unchanged=True,all_three_helper_complete_bytes_identical=True,all50_17positive_33negative_oracles_caps_math_physics_Sources_and_native_binary_unchanged=True,Source_only=True,candidate_imported_or_executed=False,compiler_or_CLE_or_physics_executed=False))
inverse_pin=pin(NEW/'COMPLETE_V9_TO_V10_VIEW_OPERAND_WHITESPACE_BYTE_INVERSE.json')
write(NEW/'FINITE_ALL_VIEW_DECK_TOKEN_AND_CLE_CARD_SOURCE_REVIEW.json',dict(schema='FINITE_V10_ALL_GENERATED_VIEW_DECK_TOKEN_AND_CLE120_CARD_REVIEW_ONLY',status='SOURCE_ONLY_ALL_FULL_DECK_TOKENS_EXACT_AND_CARDS_LE120',cards=cards,direct_alias_family=after_direct,viewops_generated_CLE_negative_cases=5,viewops_generated_CLE_lifecycle_cases=2,positive_BOOT_literal_unchanged=True,all14_operand_tokens_preserved=True,missing_operand_rsplit_preserves13=True,exact_original_oracles_unchanged=True,restricted_static_AST_string_evaluation_only=True,CLE_or_compiler_or_native_or_candidate_executed=False,actual_v9_failed_source_provenance_pin=pin(CAUSE),trap_mechanism_claimed=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False))
review_pin=pin(NEW/'FINITE_ALL_VIEW_DECK_TOKEN_AND_CLE_CARD_SOURCE_REVIEW.json')
deps=[]
for p in oldhf['dependencies']:
 target=NEW/Path(p['path']).relative_to(OLD)if Path(p['path']).is_relative_to(OLD)else Path(p['path'])
 deps.append(pin(target));need(p['sha256']==deps[-1]['sha256']or target.name in('DIRECT_ALIAS_ENTRY_BINDING.json','DECLARED_EXECUTION_INTERFACE.json'),'old257 entire bytes unchanged except required new metadata paths:'+target.name)
derived_count=len(deps);need(derived_count==257,'derive complete original257 without omissions')
deps+=provenance+[inverse_pin,review_pin,pin(__file__)]+[p for p in oldhf['dependencies']if Path(p['path']).is_relative_to(OLD)]
table={}
for p in deps:need(p['path']not in table or table[p['path']]==p,'no current dependency ambiguity');table[p['path']]=p
hf=copy.deepcopy(oldhf);hf.update(schema='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V10',host_source=pin(NEW/'run_actual_three_plane_pipeline.py'),dependencies=list(table.values()),predecessor_host_freeze=pin(OLD/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'),Source_revision_scope='V9 to V10 only: fresh namespace and exact host freeze schema; one viewops operand whitespace break after GRCON. All tokens/33 expected exit1 oracles,50 stages,17 positive controls,6 DELETE lifecycle statements,physics Sources/native complete70 runtime/math/caps unchanged.',helper_byte_equality_predecessor='pipeline_source_v9',complete_V9_to_V10_byte_inverse_pin=inverse_pin,all_generated_view_deck_token_and_CLE_card_source_review_pin=review_pin,actual_closed_v9_CLE_card_failure_cause_pin=pin(CAUSE),actual_closed_v9_true_tool_returns_pin=pin(RETURNS),complete_original_v9_dependency_rows_derived=257,strict_CLE_card_columns_maximum=120,operand_string_whitespace_only=True,all_generated_view_operand_deck_tokens_identical=True,trap_mechanism_claimed=False,compiler_executed_by_this_prepare=False,candidate_imported_by_this_prepare=False)
write(NEW/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json',hf);hfp=pin(NEW/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')
cli=copy.deepcopy(oldcli);cli.update(schema='ROOT_REVIEWABLE_EXACT_ACTUAL_PIPELINE_V10_CLE_CARD_WHITESPACE_COMPLETE70_ARGV_V1',Source_revision_scope=hf['Source_revision_scope'],actual_v9_failure_cause_pin=pin(CAUSE),actual_v9_true_tool_returns_pin=pin(RETURNS),complete_v9_to_v10_byte_inverse_pin=inverse_pin)
argv=cli['argv'];index=argv.index(str(OLD/'run_actual_three_plane_pipeline.py'));argv[index]=str(NEW/'run_actual_three_plane_pipeline.py')
for suffix,value in(('summary',hfp['path']),('sha256',hfp['sha256']),('seven-id',json.dumps(hfp['identity'],separators=(',',':')))):argv[argv.index('--host-freeze-'+suffix)+1]=value
cli['mandatory_external_bindings']['host-freeze']=hfp
write(NEW_CLI,cli);clip=pin(NEW_CLI)
for p in hf['dependencies']+[hf['host_source'],hfp]+list(cli['mandatory_external_bindings'].values()):verify(p)
need(not Path(interface['output_root']).exists()and not Path(interface['output_root']).is_symlink(),'fresh actual v10 output namespace remains absent')
print(json.dumps(dict(status='V10_ONLY_VIEW_OPERAND_WHITESPACE_SOURCE_FROZEN_NOT_EXECUTED',source_namespace=str(NEW),host_Source_freeze_pin=hfp,actual_reviewable_CLI_pin=clip,inverse_pin=inverse_pin,full_view_card_source_review_pin=review_pin,original_dependency_count=257,current_frozen_dependency_count=len(hf['dependencies']),successful_Source_checks=len(checks),candidate_or_CLE_or_compiler_or_physics_executed=False,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),allow_nan=False))
