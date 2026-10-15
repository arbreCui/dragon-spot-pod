"""Exact two closed-v12 input-copy Source preparation; no body EOF or execution."""
import ast, hashlib, json, os, stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'storage_release_literal3_before_saved370_old_pack_and_macro_source_v2_20261014'
OUT=R/'storage_release_literal2_before_material75_v12_input_duplicates_source_v1_20261014'
NAMES=('literal11_release_common.py','prepare_literal11_manifest.py','verify_or_execute_literal11.py')
LABEL='LITERAL2_BEFORE_MATERIAL75_V12_INPUT_DUPLICATES'
OLD_LABEL='LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO'
INDICES=[2319,2320]
TOTAL=45167892
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k]for k in('path','sha256','size_bytes','identity')}
def pin(p):
 p=Path(p);s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('bounded ordinary Source metadata only')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened7')
  raw=f.read()
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('EOF7')
 if identity(p.lstat())!=identity(s):raise RuntimeError('after7')
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def read(p):
 if isinstance(p,dict):
  if pin(p['path'])!=norm(p):raise RuntimeError('exact metadata fullPF')
  p=p['path']
 else:pin(p)
 return json.loads(Path(p).read_bytes())
def write(p,v):
 raw=v.encode()if isinstance(v,str)else v if isinstance(v,bytes)else(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(p)
def inventory(roots):
 out=dict(ordinary_file_identities={},directory_identities={},symlinks={});stack=list(roots)
 while stack:
  p=stack.pop();s=p.lstat();before=identity(s)
  if not stat.S_ISDIR(s.st_mode):raise RuntimeError('ordinary closed owner directory')
  out['directory_identities'][str(p)]=before;fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:
   if identity(os.fstat(fd))!=before:raise RuntimeError('dirfd7')
   with os.scandir(fd)as it:
    for e in it:
     q=p/e.name;t=e.stat(follow_symlinks=False)
     if stat.S_ISDIR(t.st_mode):stack.append(q)
     elif stat.S_ISREG(t.st_mode):out['ordinary_file_identities'][str(q)]=identity(t)
     else:raise RuntimeError('ordinary owner entries only')
   if identity(os.fstat(fd))!=before or identity(p.lstat())!=before:raise RuntimeError('directory after7')
  finally:os.close(fd)
 return out
SAVED_PROOF="""def saved370_closed_proof():
 d=read(CLOSED_SAVED['summary_pin']);t=read(CLOSED_SAVED['Root_true_tool_pin']);a=read(CLOSED_SAVED['Root_exact_argv_pin']);p=read(CLOSED_SAVED['independent_postreview_pin']);pt=read(CLOSED_SAVED['independent_posttools_pin']);hf=read(CLOSED_SAVED['Host_freeze_pin']);cli=read(CLOSED_SAVED['exact_cli_pin']);q=t['actual_terminal_return']
 if t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=0 or type(q['exit_code'])is not int or q['exit_code']!=0 or q.get('session_id')is not None or shlex.split(t['exact_executed_command'])!=a['exact_argv']or a['exact_argv']!=cli['exact_reviewable_argv']or len(a['exact_argv'])!=16:raise RuntimeError('actual saved370 Root0 exact16')
 if pt['observed_closed']is not True or type(pt['original_integer_exit_code'])is not int or pt['original_integer_exit_code']!=0:raise RuntimeError('independent saved370 actual closed0')
 for key in('actual_review_return','actual_postverification_return'):
  q=pt[key]
  if type(q['exit_code'])is not int or q['exit_code']!=0 or q.get('session_id')is not None or b.norm(json.loads(q['output'].strip().splitlines()[-1])['review_pin'])!=CLOSED_SAVED['independent_postreview_pin']:raise RuntimeError('saved370 genuine post stdout0')
 if p['schema']!='INDEPENDENT_SAVED370_AFTER_V18_V3_ACTUAL_DIAGNOSTIC_POSTVERIFICATION_V1'or p['status']!='PASS_ACTUAL_SAVED370_AFTER_V18_V3_ORIGINAL_SCOPE_DIAGNOSTIC_POSTVERIFICATION'or p['failure']is not None:raise RuntimeError('exact actual saved370 independent protocol')
 for k,v in(('actual_report_pin','summary_pin'),('actual_Root_true_tool_return_pin','Root_true_tool_pin'),('actual_Root_argv_pin','Root_exact_argv_pin'),('actual_Host_freeze_pin','Host_freeze_pin'),('actual_CLI_pin','exact_cli_pin')):
  if p[k]!=CLOSED_SAVED[v]:raise RuntimeError('exact saved370 canonical '+k)
 if any(p[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted','new_three_plane_inputs_audited','new_v18_pair_scientific_validation_performed')):raise RuntimeError('saved370 original diagnostic scope only')
 if d['schema']!='ACTUAL_ROOT_GUARDED_SAVED_FULL370_TERMINAL_SOURCE_DIAGNOSTIC_V2'or d['status']!='ACTUAL_SAVED_FULL370_THREE_AXIAL_MOMENT_DIAGNOSTIC_CLOSED0_ONLY'or d['failure']is not None or d['after_check_error']is not None or len(d['records'])!=1 or d['records'][0]['status']!='PASS'or len(d['fixed_current_pins'])!=3349 or len(d['actual_TMP_output_pins'])!=24 or d['new_three_plane_inputs_audited']is not False or any(d[k]is not False for k in('full_neutron_balance_qualified','full_eigen_reference_qualified','AAA_qualified','ABA_admitted','goal_complete'))or CLOSED_SAVED['Host_freeze_pin']not in d['fixed_current_pins']:raise RuntimeError('saved370 actual3349 original three-moment scope kept')
 v=read(CLOSED_OWNER_V12['summary_pin']);raw=read(CLOSED_OWNER_V12['complete_raw_pin'])
 compact=lambda rows:[{k:x for k,x in r.items()if k not in('resource_before','resource_after')}for r in rows]
 if v['schema']!='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1'or v['status']!='FAILED_UNQUALIFIED_NO_RETRY'or v['failure']!='RuntimeError: original SELF 512MiB cap'or v['after_check_error']!='RuntimeError: original SELF 512MiB cap'or v['engineering_three_plane_closed0']is not False or v['actual_terminal']is not None or len(v['records'])!=45 or compact(v['records'])!=compact(raw['records']):raise RuntimeError('closed failed v12 owner exact45 original failure retained')
 return CLOSED_SAVED"""
def main():
 if OUT.exists():raise RuntimeError('one unique new Source package')
 oldsfpin=pin(OLD/'COMPLETE_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_SOURCE_FREEZE.json');oldsf=read(oldsfpin)
 mfpin=pin(OLD/'EXACT_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_MANIFEST.json');mf=read(mfpin);rows=mf['current_protected_full_EOF_pins'];targets=[norm(rows[i])for i in INDICES]
 if len(rows)!=9163 or sum(p['size_bytes']for p in targets)!=TOTAL or len({tuple(p['identity'][:2])for p in targets})!=2:raise RuntimeError('exact2 MF9163 selected completePF')
 paths={p['path']for p in targets};root=Path(targets[0]['path']).parents[1]
 if root!=Path(targets[1]['path']).parents[1]or root.name!='axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v12':raise RuntimeError('two exact same closed v12 owner')
 for q in targets:
  s=Path(q['path']).lstat()
  if identity(s)!=q['identity']or not stat.S_ISREG(s.st_mode)or s.st_uid!=os.getuid()or s.st_nlink!=1:raise RuntimeError('exact targets current7 UID ordinary singlelink')
 savedpostdir=R/'independent_saved370_after_v18_v3_actual_diagnostic_postverify_20261014';rp=pin(savedpostdir/'REVIEW.json');tp=pin(savedpostdir/'TRUE_TOOL_RETURNS.json');post=read(rp)
 if rp['sha256']!='0068a143f70de9ad63bc4dccd69ceeda68b2046c31536197f540ad33e6bc0dac'or tp['sha256']!='6bc34125dac4ba4b958ea0faa8cb39d3a8e09cc2f1ebf248225dfce46cf08db8':raise RuntimeError('same actual saved370 post0')
 saved=dict(summary_pin=post['actual_report_pin'],Root_true_tool_pin=post['actual_Root_true_tool_return_pin'],Root_exact_argv_pin=post['actual_Root_argv_pin'],Host_freeze_pin=post['actual_Host_freeze_pin'],exact_cli_pin=post['actual_CLI_pin'],independent_postreview_pin=rp,independent_posttools_pin=tp)
 sd=read(saved['summary_pin']);source=(OLD/NAMES[0]).read_text();current=source;changes=[]
 def change(a,z):
  nonlocal current
  if current.count(a)!=1:raise RuntimeError('one complete Source splice')
  current=current.replace(a,z,1);changes.append(dict(before=a,after=z))
 def node(name):return next(n for n in ast.parse(current).body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name)
 def const(name):return ast.literal_eval(node(name).value)
 def assign(name,v):change(ast.get_source_segment(current,node(name)),name+'='+repr(v))
 def fn(name):return ast.get_source_segment(current,next(n for n in ast.parse(current).body if isinstance(n,ast.FunctionDef)and n.name==name))
 latest=const('CLOSED_FULL50');hf=read(latest['Host_freeze_pin']);full=read(latest['summary_pin']);keep=const('ROLE_KEEP_PINS');binding=read(R/'saved_full370_after_latest_full50_source_v3_20261014/CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json')
 direct=[hf['dependencies'],full['fixed_current_pins'],full['output_pins'],sd['fixed_current_pins'],sd['output_pins'],sd['actual_TMP_output_pins'],binding['science_original_input_pins']]
 for origin in const('DOWNSTREAM_ORIGINS'):direct.append(origin['current_pins'])
 if any(paths&{p['path']for p in x}for x in direct):raise RuntimeError('no target live full50/saved/science/material/GENDF direct authority')
 matches=[]
 for target in targets:
  same=next(p for p in keep if Path(p['path']).name==Path(target['path']).name)
  if same['sha256']!=target['sha256']or same['size_bytes']!=target['size_bytes']or same['identity'][:2]==target['identity'][:2]:raise RuntimeError('same completeSHA/size retained science distinctnode')
  if identity(Path(same['path']).lstat())!=same['identity']:raise RuntimeError('retained science current7')
  matches.append(dict(target_pin=target,retained_scientific_original_pin=same))
 before=inventory([root]);ownerfiles=len(before['ordinary_file_identities']);ownerdirs=len(before['directory_identities'])
 ownsummary=pin(root/'Root_actual_three_plane_engineering_summary.json');ownraw=pin(root/'Root_actual_complete_execution_record_before_final_publication.json');owner=dict(summary_pin=ownsummary,complete_raw_pin=ownraw)
 hist=dict(const('HISTORICAL_PINS'));hist.update(previous9163_manifest=mfpin,predecessor_cleanup_Source_freeze=oldsfpin,latest_saved_report=saved['summary_pin'],latest_saved_HF=saved['Host_freeze_pin'],latest_saved_CLI=saved['exact_cli_pin'],latest_saved_Root=saved['Root_true_tool_pin'],latest_saved_Root_argv=saved['Root_exact_argv_pin'],latest_saved_post=rp,latest_saved_post_tools=tp,closed_v12_owner_summary=ownsummary,closed_v12_owner_complete_raw=ownraw)
 sourcepins=list(const('BIND_NEW_SOURCE_PINS'))+list(saved.values())
 sourcepins+=[pin(R/'prepare_material75_GENDF_after_latest_full50_source_only_v4_20261014.py'),pin(R/'MATERIAL75_GENDF_AFTER_LATEST_FULL50_PREPARER_SOURCE_SPEC_V4_20261014.json')]
 sourcepins=list({p['path']:p for p in sourcepins}.values())
 for k,v in [('HISTORICAL_PINS',hist),('TARGET_SELECTED_PINS',targets),('HISTORICAL_TARGET_INDICES',INDICES),('HISTORICAL_HF_TARGET_INDICES',[]),('BASELINE_OWNED_INVENTORIES',before),('BIND_NEW_SOURCE_PINS',sourcepins),('BYTES',TOTAL),('OWNER_FILE_COUNT',ownerfiles),('OWNER_DIRECTORY_COUNT',ownerdirs)]:assign(k,v)
 change(ast.get_source_segment(current,node('BRANCHES')),'BRANCHES=[Path(p)for p in '+repr([str(root)])+']')
 change(ast.get_source_segment(current,node('RECEIPTS')),"RECEIPTS=REC/'storage_release_literal2_before_material75_v12_input_duplicates_actual_receipts_20261014'\nCLOSED_SAVED="+repr(saved)+'\nCLOSED_OWNER_V12='+repr(owner))
 for k,v in [('SF','COMPLETE_LITERAL2_BEFORE_MATERIAL75_V12_INPUT_DUPLICATES_SOURCE_FREEZE.json'),('FINAL','EXACT_LITERAL2_BEFORE_MATERIAL75_V12_INPUT_DUPLICATES_MANIFEST.json')]:change(ast.get_source_segment(current,node(k)),k+'=PKG/'+repr(v))
 g=fn('source_gate');change(g,g.replace(OLD_LABEL,LABEL).replace('len(TARGETS)!=3','len(TARGETS)!=2').replace('len(TARGET_PATHS)!=3','len(TARGET_PATHS)!=2').replace("f['closed_latest_full50_authority']!=CLOSED_FULL50","f['closed_latest_full50_authority']!=CLOSED_FULL50 or f['closed_latest_saved370_authority']!=CLOSED_SAVED or f['closed_v12_owner_authority']!=CLOSED_OWNER_V12"))
 change(fn('disjoint'),fn('disjoint').replace('!=3','!=2'))
 change(fn('closed_proofs'),fn('closed_proofs').replace('full50_closed_proof()]','full50_closed_proof(),saved370_closed_proof()]')+'\n\n'+SAVED_PROOF)
 protection=fn('current_protection').replace("HISTORICAL_PINS['previous8811_manifest']","HISTORICAL_PINS['previous9163_manifest']").replace('8811','9163').replace('8808','9161').replace('[2605,4177,4467]','[2319,2320]').replace('OWNER_FILE_COUNT-3','OWNER_FILE_COUNT-2').replace('only3','only2').replace('exact3','exact2').replace('exact3','exact2').replace('EXACT_THREE_OLD_PRIVATE_BODY_HISTORICAL','EXACT_TWO_V12_PRIVATE_COPY_BODIES_HISTORICAL').replace('MF3_indices','MF2_indices').replace('all_other_v3_v14_v15_owner_files_kept','all_other_v12_owner_files_kept')
 anchor=" for p in ROLE_KEEP_PINS:add(p,'all_original_scientific9_current')"
 insertion=" saved_actual=read(CLOSED_SAVED['summary_pin'])\n for p in list(CLOSED_SAVED.values())+saved_actual['fixed_current_pins']+saved_actual['output_pins']+saved_actual['actual_TMP_output_pins']:add(p,'latest_saved370_current_ART_and_live_TMP24')\n"
 if protection.count(anchor)!=1:raise RuntimeError('one saved closure protection block')
 protection=protection.replace(anchor,insertion+anchor)
 change(fn('current_protection'),protection);ast.parse(current)
 others=[]
 for name in NAMES[1:]:
  beforetext=(OLD/name).read_text();after=beforetext.replace(OLD_LABEL,LABEL).replace('target_count=3','target_count=2').replace("m['target_count']!=3","m['target_count']!=2").replace("before['regular_files']-after['regular_files']!=3","before['regular_files']-after['regular_files']!=2").replace('deleted_files=3','deleted_files=2');ast.parse(after);others.append((name,beforetext,after))
 funcs=lambda s:{n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
 low=['_base','external','inventory','receipt_pin','update_owned','budget','review_gate']
 if any(funcs(source)[n]!=funcs(current)[n]for n in low):raise RuntimeError('seven low-level methods wholebytes')
 start='                os.unlink(target.name,dir_fd=fd)';end="        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)";a=others[1][1];z=others[1][2]
 if a[a.index(start):a.index(end)]!=z[z.index(start):z.index(end)]:raise RuntimeError('exact unlink-returnreceipt-fsync-dirFirstFailure bytes')
 namespace={'read':read,'CLOSED_SAVED':saved,'CLOSED_OWNER_V12':owner,'shlex':__import__('shlex'),'json':json,'b':type('B',(),{'norm':staticmethod(norm)})()}
 exec(compile(SAVED_PROOF,'<Source-only-saved-and-closed-v12-metadata-proof>','exec'),namespace);namespace['saved370_closed_proof']()
 OUT.mkdir();write(OUT/NAMES[0],current)
 for name,_,after in others:write(OUT/name,after)
 pp=write(OUT/'EXACT_LITERAL2_BEFORE_MATERIAL75_V12_INPUT_DUPLICATES_ROLE_SOURCE_PLAN.json',dict(schema='EXACT_LITERAL2_BEFORE_MATERIAL75_V12_INPUT_DUPLICATES_ROLE_SOURCE_PLAN_V1',source_only=True,literal2_fullpins=targets,target_count=2,target_bytes=TOTAL,previous9163_manifest_pin=mfpin,exact_current_MF2_indices_migrated_to_history=INDICES,all_other9161_PF_rows_data_retained=True,kept_sameSHA_original_science_nodes=matches,no_direct_current_HF3955_Saved3349_science1129_material33_GENDF51_or11_target_role=True,complete_owner_inventory=before,owner_file_count=ownerfiles,owner_directory_count=ownerdirs,retained_other_file_count=ownerfiles-2,closed_latest_saved370_authority=saved,closed_v12_owner_authority=owner,live_saved_TMP24_kept=True,original_caps=oldsf['original_caps'],future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_Root_tools_pin=None,future_actual_postreview_pin=None,future_original_current_fullfresh2_budget_admission=None,predicted_margin_not_admission=True,compiler_executed=False,numerical_executed=False,business_executed=False,deletion_executed=False))
 entries=[dict(predecessor_pin=pin(OLD/NAMES[0]),candidate_pin=pin(OUT/NAMES[0]),changes=changes)]+[dict(predecessor_pin=pin(OLD/n),candidate_pin=pin(OUT/n),changes=[dict(before=a,after=z)])for n,a,z in others]
 for entry in entries:
  back=Path(entry['candidate_pin']['path']).read_text()
  for c in reversed(entry['changes']):
   if back.count(c['after'])!=1:raise RuntimeError('exact one complete inverse')
   back=back.replace(c['after'],c['before'],1)
  if back.encode()!=Path(entry['predecessor_pin']['path']).read_bytes():raise RuntimeError('three complete byte inverses')
 ip=write(OUT/'COMPLETE_LITERAL3_TO_LITERAL2_BEFORE_MATERIAL75_WHOLE_BYTE_INVERSE.json',dict(schema='COMPLETE_LITERAL3_TO_LITERAL2_BEFORE_MATERIAL75_WHOLE_BYTE_INVERSE_V1',entries=entries,seven_lowlevel_methods_wholebytes_equal=low,sequential_unlink_returnreceipt_dirfsync_FirstFailure_wholebytes_equal=True,source_only=True))
 sf=dict(oldsf);sf.update(schema='COMPLETE_LITERAL2_BEFORE_MATERIAL75_V12_INPUT_DUPLICATES_SOURCE_ONLY_FREEZE_V1',literal11_fullpins=targets,literal3_fullpins=targets,literal2_fullpins=targets,target_count=2,target_bytes=TOTAL,historical_evidence_pins=hist,closed_latest_saved370_authority=saved,closed_v12_owner_authority=owner,Source_pins=[pin(OUT/n)for n in NAMES],exact_role_plan_pin=pp,strict_low_level_Source_provenance_pin=ip,Source_preparer_pin=pin(__file__),predecessor_Source_freeze_pin=oldsfpin,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_probe_Host_freeze_pin=None,future_original_current_fullfresh2_budget_admission=None,source_only=True,manifest_prepared=False,deletion_executed=False,compiler_or_business_executed=False)
 sp=write(OUT/'COMPLETE_LITERAL2_BEFORE_MATERIAL75_V12_INPUT_DUPLICATES_SOURCE_FREEZE.json',sf);fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='EXACT2_BEFORE_MATERIAL75_SOURCE_ONLY_NO_MF_NO_DELETE',Source_freeze_pin=sp,Source_pins=sf['Source_pins'],plan_pin=pp,inverse_pin=ip,preparer_pin=pin(__file__),target_count=2,target_bytes=TOTAL,owner_file_count=ownerfiles,owner_directory_count=ownerdirs,retained_other_file_count=ownerfiles-2,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False)),flush=True)
if __name__=='__main__':main()
