"""Independent full bound Source review; stdlib AST/hash, never Source execution."""
import ast,hashlib,json,math,os,re,stat
from pathlib import Path
P=Path('/private/tmp/axmat_v25_actual_Q_bound_complete_PREP_SOURCE_ROOT_20261010_c6efd7')
M=Path('/private/tmp/axmat_v25_complete_canonical_TRUE_snapshot_jointQ_UNREADY_SOURCE_bwo0x_85')
PR=Path('/private/tmp/axmat_v25_complete_canonical_TRUE_independent_Source_review_ua3qps8x')
OUT=Path(__file__).parent
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
T=B/'actual_joint_helper_admission_v25_receipts/Root_actual_Q_to_complete_PREP_Source_binding_tool_return.json'
checks=[];inputs={}
def ck(n,v,detail=None):
 assert type(v)is bool
 assert n not in [x['check']for x in checks]
 checks.append(dict(check=n,passed=v,evidence=detail))
 if not v:raise AssertionError(n)
def ids(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);before=ids(p);assert stat.S_ISREG(before[2])and not p.is_symlink()
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ids(p)==before
 v=dict(path=str(p),sha256=h,size_bytes=before[4],identity=before)
 if str(p)in inputs:assert inputs[str(p)]==v
 inputs[str(p)]=v;return v
def pairs(rows):
 d={}
 for k,v in rows:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=v
 return d
def read(p):
 pin(p);v=json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))
 def finite(x):
  if type(x)is float:assert math.isfinite(x)
  elif type(x)is list:
   for a in x:finite(a)
  elif type(x)is dict:
   for a in x.values():finite(a)
 finite(v);return v
def inventory(p):
 files={};dirs={}
 for folder,dnames,names in os.walk(p,followlinks=False):
  q=Path(folder);assert not q.is_symlink()and stat.S_ISDIR(q.lstat().st_mode);dirs[str(q.relative_to(p))]=ids(q)
  for n in names:files[str((q/n).relative_to(p))]=pin(q/n)
 return dict(files=files,directories=dirs)
def shape(v):
 i=v.get('identity',v.get('identity7'));assert type(v)is dict and type(v['path'])is str and type(v['sha256'])is str and re.fullmatch('[0-9a-f]{64}',v['sha256'])and type(i)is list and len(i)==7 and all(type(x)is int for x in i)
 if 'size_bytes'in v:assert type(v['size_bytes'])is int and v['size_bytes']==i[4]
 return dict(path=v['path'],sha256=v['sha256'],size_bytes=i[4],identity=i)
def defs(s):return {n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef))}
def reverse(s,rs):
 for r in reversed(rs):
  assert type(r['count'])is int and r['count']>0 and s.count(r['new'])==r['count']
  s=s.replace(r['new'],r['old'])
 return s
def globals(s):return {n.targets[0].id:n.value for n in ast.parse(s).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def collect(v,refs):
 if type(v)is dict:
  if 'path'in v and 'sha256'in v and ('identity'in v or'identity7'in v):
   r=shape(v);assert r['path']not in refs or refs[r['path']]==r;refs[r['path']]=r
  for a in v.values():collect(a,refs)
 elif type(v)is list:
  for a in v:collect(a,refs)
mp=pin(P/'MANIFEST.json');m=read(P/'MANIFEST.json');before=inventory(P)
ck('actual bound manifest exact final SHA',mp['sha256']=='b7fc58ae49704441acfb2eafef0fe52ed05c85f786019683eccf6e799590cbe1')
ck('complete five members plus manifest all EOF seven identities',m['member_count']==5 and type(m['member_count'])is int and set(before['files'])==set(m['members'])|{'MANIFEST.json'}and all(before['files'][n]==shape(v)for n,v in m['members'].items()))
ck('complete bound directories stable exact',before['directories']==m['directories'])
ck('bound package genuine Sourceonly not project execution',m['schema']=='V25_ROOT_ACTUAL_Q_BOUND_COMPLETE_PREP_SOURCE_PACKAGE_V1'and m['source_only']is True and m['executed_project']is False)
t=read(T);tp=pin(T);tr=t['terminal_tool_return'];stdout=json.loads(tr['output']);ck('actual Root b4bd6d observed closed typed zero no session no repoll',t['schema']=='ROOT_V25_ACTUAL_Q_TO_COMPLETE_PREP_SOURCE_BINDING_TOOL_TERMINAL_RETURN_V1'and t['source_only']is True and t['closed']is True and t['observed_terminal']is True and t['actual_tool_terminal_return_observed']is True and t['session_repolled_after_close']is False and type(tr['exit_code'])is int and tr['exit_code']==0 and tr['chunk_id']=='b4bd6d'and 'session_id'not in tr)
ck('binding output actual full manifest and no business',shape(stdout['manifest'])==mp and stdout['source_only']is True and stdout['business_or_science_executed']is False and t['candidate_guard_API_or_numeric_executed']is False and t['new_actual_PREP_or_BUILD_or_INPUT_or_science_qualified']is False)
rolepaths={'canonical':'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25.py','prepare_host':'combined_prepare_host.py','prepare_writer':'write_actual_prepare_terminal.py'}
rolepins={k:pin(P/n)for k,n in rolepaths.items()};texts={k:(P/n).read_text()for k,n in rolepaths.items()}
ck('actual raw tool full three role pins exact',rolepins=={'canonical':shape(stdout['canonical']),'prepare_host':shape(stdout['host']),'prepare_writer':shape(stdout['writer'])})
prior=read(PR/'REVIEW.json');prior_mp=pin(PR/'MANIFEST.json');mother_mp=pin(M/'MANIFEST.json')
ck('previous sealed independent mother79 manifest same family',prior['schema']=='INDEPENDENT_V25_COMPLETE_CANONICAL_TRUE_SNAPSHOT_PREP_BUILD_SOURCE_REVIEW_V1'and prior['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_BUSINESS_QUALIFICATION'and prior['source_only']is True and prior['all_checks_typed_true']is True and prior['blockers']==[] and prior['check_count']==len(prior['checks'])==79 and prior['qualified_template_manifest_pin']==mother_mp and mother_mp['sha256']=='9e9a77669309071065c189ad02ee455709ca81db376de818825d99d8cf22f6e9')
proof=read(P/'Root_actual_Q_bound_complete_PREP_Source_inverse.json');baseproof=read(M/'COMPLETE_SOURCE_INVERSES.json')
ck('actual full inverse metadata truthful exact SHA',pin(P/'Root_actual_Q_bound_complete_PREP_Source_inverse.json')['sha256']=='e2a124b89b44967dc15380f1e89c1d4eff699b386a7908e567eccb8a8d50bd40'and proof['schema']=='V25_ROOT_ACTUAL_Q_BOUND_COMPLETE_PREP_SOURCE_INVERSE_V1'and proof['source_only']is True and proof['candidate_guard_API_compiler_or_numeric_executed']is False and proof['installed']is False)
for role in rolepaths:
 rows=proof['complete_original_source_inverses'][role];template=Path(prior['qualified_role_Source_pins'][role]['path']);ts=template.read_text();pin(template)
 ck(role+' exact READY to UNREADY inverse',reverse(texts[role],rows['READY_to_UNREADY'])==ts,dict(hunks=len(rows['READY_to_UNREADY'])))
 ck(role+' every function and class body unchanged in actual binding',defs(texts[role])==defs(ts))
 ck(role+' inherited finite inverse exactly mother proof',rows['UNREADY_to_original']==baseproof['exact_finite_transforms'][role])
 parent=(M/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text();pin(M/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py'))
 restored=reverse(reverse(texts[role],rows['READY_to_UNREADY']),rows['UNREADY_to_original'])
 ck(role+' whole original bytes AST and definitions restored',restored==parent and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False)and defs(restored)==defs(parent))
ck('all original70 canonical definitions complete',len(defs((M/'ORIGINAL_PARENT_SOURCE/canonical.full.py').read_text()))==70)
canon=texts['canonical'];a=globals(canon)
business=list(proof['all_six_future_business_pins'])
ck('all six exact business slots unknown retained',len(business)==6 and all(proof['all_six_future_business_pins'][k]is None and isinstance(a[k],ast.Constant)and a[k].value is None for k in business))
ck('actual canonical READY only Q binding and exact fixed basename',ast.literal_eval(a['DRAFT_STATUS'])=='READY_REVIEWED_V25_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'and P.name.startswith('axmat_v25_actual_Q_bound_')and 'TMP draft cannot perform a business action'in canon)
Q=B/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json';q=read(Q);qp=pin(Q)
ck('real Q original full saved bytes and tool pin agree',qp==shape(proof['actual_Q'])==shape(stdout['actual_Q'])and qp['sha256']=='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b'and(P/'ACTUAL_V25_HELPER_ONLY_JOINT_Q.byte_exact.json').read_bytes()==Q.read_bytes()and ast.literal_eval(a['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'])==qp['sha256'])
E=B/'actual_joint_helper_admission_v25_receipts';external_names={'FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN':'Root_actual_joint_helper_META_admission_writer_tool_terminal_return.json','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN':'sealed_independent_actual_joint_Q_saved_META_review/REVIEW.json','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN':'Root_actual_joint_Q_saved_META_peer_retention_record.json'}
external={}
for key,n in external_names.items():
 expected=ast.literal_eval(a[key]);actual=pin(E/n);external[key]=read(E/n)
 ck(key+' actual independent full pin bound as builtin typed literal',shape(expected)==actual and set(expected)=={'path','sha256','size_bytes','identity'})
qterm=external['FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN'];qpeer=external['FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN'];ret=external['FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN']
ck('actual external Qwriter94520a and saved48 metadata only',qterm['closed']is True and qterm['actual_tool_terminal_return_observed']is True and qterm['terminal_tool_return']['chunk_id']=='94520a'and type(qterm['terminal_tool_return']['exit_code'])is int and qterm['terminal_tool_return']['exit_code']==0 and qpeer['check_count']==len(qpeer['checks'])==48 and qpeer['whole_build_qualified']is False and qpeer['whole_INPUT_admitted']is False and qpeer['Root_actual_Q_pin']==qp)
refs={};collect(q,refs);refs[str(Q)]=qp
for v in [*map(lambda k:ast.literal_eval(a[k]),external_names),qpeer,ret,json.loads(qterm['terminal_tool_return']['output'])]:collect(v,refs)
owners=proof['all_Q_and_proof_explicit_typed_owner_expected_files']
ck('all340 ownership endpoints exactly full Q plus complete actual external proof refs',len(owners)==340 and type(owners)is dict and owners=={p:r['sha256']for p,r in refs.items()},dict(all_payload_rehashed=False,Source_ownership_only=True))
ck('all originally declared310 owners retained no filtering',len(q['Root_finite_joint_META_full_EOF_SHA7ID_verified_unique_inputs'])==310 and all(owners[shape(r)['path']]==shape(r)['sha256']for r in q['Root_finite_joint_META_full_EOF_SHA7ID_verified_unique_inputs']))
ck('all actual proof reads remain typed extra owners and ordinary paths',"**helper_Q_admission()"in defs(canon)['prepare_build']and"expected_files=extra"in defs(canon)['create_complete_input_graph']and"owner='NEW SOURCE-owned historical INPUT reuse implementation'"in defs(canon)['create_complete_input_graph']and'*helper_Q_admission()'in defs(canon)['current_new_owned_paths'])
reads=proof['all_read_Source_META_fullpins'];ck('69 actual Source and small META read registry unique fullpins',len(reads)==69 and len({shape(r)['path']for r in reads})==69)
# Rehash only exactly registered Source/small META used by stdlib binder; no graph/trace/gzip/material payloads occur in this list.
allowed_art={'result.json','ACTUAL_REPORT.json','ACTUAL_PRIVATE_INACTIVE_AUDIT_SNAPSHOT_CONTROLS.json'}
for r in reads:
 rr=shape(r);p=Path(rr['path'])
 assert not p.name.endswith(('.gz','.sqlite','.bin','.ascii','.xsm','.log'))
 assert not p.is_relative_to(Path('/Users/wen/spot/validation/artifacts'))or p.name in allowed_art
 assert pin(p)==rr
ck('all69 registered Source smallMETA full EOF beforeafter exact typed pins',True)
ck('exact literal future PREP host canonical and Q hashes',ast.literal_eval(globals(texts['prepare_host'])['FUTURE_V25_CANONICAL_SHA'])==rolepins['canonical']['sha256']and ast.literal_eval(globals(texts['prepare_host'])['FUTURE_V25_ACTUAL_Q_SHA'])==qp['sha256']and ast.literal_eval(globals(texts['prepare_writer'])['FUTURE_V25_CANONICAL_SHA'])==rolepins['canonical']['sha256'])
ck('all original snapshot contract and three last-use points unchanged',canon.count('audit.snapshot(_consume=True)')==3 and defs(canon)['helper_Q_admission']==defs(Path(prior['qualified_role_Source_pins']['canonical']['path']).read_text())['helper_Q_admission'])
ck('original PREP caps genuine serial MRO and child guard intact',all(x in texts['prepare_host']for x in ['1800,600,512,2*2**30','OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)','8*2**30,96*2**30','children_at_once=1','retries=0']))
ck('bound three roles no physical arithmetic or function modified',all(defs(texts[r])==defs(Path(prior['qualified_role_Source_pins'][r]['path']).read_text())for r in rolepaths))
ck('all bound six members original full EOF namespace beforeafter stable',inventory(P)==before)
ck('mother Source and original real Q proof unchanged',pin(M/'MANIFEST.json')==mother_mp and pin(Q)==qp and pin(T)==tp)
ck('Source review no candidate guard API compilation numeric project or large payload execution',True)
report=dict(schema='INDEPENDENT_V25_ACTUAL_BOUND_COMPLETE_PREP_SOURCE_REVIEW_V1',status='SOURCE_ONLY_PASS_NO_EXECUTION_OR_BUSINESS_QUALIFICATION',source_only=True,all_checks_typed_true=True,blockers=[],check_count=len(checks),checks=checks,qualified_bound_manifest_pin=mp,qualified_role_Source_pins=rolepins,qualified_helper_SHA='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092',actual_Root_binding_terminal_pin=tp,qualified_template_manifest_pin=mother_mp,prior_independent_mother79_Source_report_pin=pin(PR/'REVIEW.json'),prior_independent_mother79_Source_manifest_pin=prior_mp,actual_bound_namespace_before_after=before,actual_Q_pin=qp,actual_Source_only_bound_owner_count=340,actual_Source_only_binder_fullpin_read_count=69,explicit_Source_smallMETA_input_pins=list(inputs.values()),all_six_future_business_pins=proof['all_six_future_business_pins'],candidate_helper_guard_API_compiler_or_numeric_executed=False,large_graph_trace_gzip_SQLite_material_or_Source_archive_payloads_read=False,whole_INPUT_build_native_science_qualified=False,limits=['Only actual Source binding admitted here. No PREP execution, full five-stage build, physical/native/science credit.','All340 owners retained; their future full business fresh phases remain mandatory. This reviewer rehashes only69 registered Source/smallMETA reads and the fixed bound files.'])
with (OUT/'REVIEW.json').open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
(OUT/'REPORT.txt').write_text('Actual V25 bound canonical/PREP host/PREP writer Source-only independent PASS. Full70 original definitions and all3 role function bodies retained; realQ94520a/saved48 proof bindings exact,340 typed owners/69 actual Source-META reads intact, six future business pins None. No candidate/API/guard/numeric execution, no large graph/material payload reads. Root real Source install and full PREP/build gates remain.\n')
print(json.dumps(dict(source_only=True,status=report['status'],check_count=len(checks),review_pin=pin(OUT/'REVIEW.json'),qualified_bound_manifest_pin=mp,qualified_role_Source_pins=rolepins,candidate_helper_guard_API_compiler_or_numeric_executed=False)))
