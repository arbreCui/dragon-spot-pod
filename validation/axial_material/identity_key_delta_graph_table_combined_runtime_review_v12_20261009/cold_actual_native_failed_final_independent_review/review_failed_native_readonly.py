"""Read only actual evidence; no business import, execution, or session poll."""
import ast, hashlib, json, struct
from pathlib import Path

ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
W=ART/'axial-material-owned-specs-identity-key-delta-graph-table-cold-runtime-v12-20261009'
S=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-cold-source-v12-20261009'
T=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-cold-terminal-v12-20261009'
R=ROOT/'validation/axial_material/identity_key_delta_graph_table_combined_runtime_review_v12_20261009'
D=Path('/private/tmp/axmat_v12_actual_native_AAA_failure_readonly_review_20261009')
inventory={}
def pin(p,expected=None):
 p=Path(p);assert p.is_absolute() and p.is_file() and not p.is_symlink()
 if str(p) not in inventory:
  with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
  inventory[str(p)]={'sha256':h,'size_bytes':p.stat().st_size}
 if expected is not None:assert inventory[str(p)]['sha256']==expected,(str(p),expected,inventory[str(p)])
 return dict(path=str(p),sha256=inventory[str(p)]['sha256'])
def read(p,sha=None):
 pin(p,sha)
 def pairs(rows):
  v={}
  for k,a in rows:assert k not in v;v[k]=a
  return v
 return json.loads(Path(p).read_text(),object_pairs_hook=pairs)
def exact(a,b):
 assert type(a)is type(b),(type(a),type(b))
 if isinstance(a,dict):
  assert a.keys()==b.keys()
  for k in a:exact(a[k],b[k])
 elif isinstance(a,list):
  assert len(a)==len(b)
  for x,y in zip(a,b):exact(x,y)
 elif isinstance(a,float):assert struct.pack('!d',a)==struct.pack('!d',b)
 else:assert a==b,(a,b)

prepared=read(W/'prepared.json','ec3db7fcf10c2fc4b63b6dc89283f29b2067dc97aebb29b67e5aaa1731b5429c')
cold=read(W/'prepared_cold.json','a0bef1fdec73993e084876db89f5ea41fe8dc10304a3e38d6be17a5b68590368')
restored=dict(cold);supervision=restored.pop('own_child_supervision');exact(restored,prepared)
assert set(supervision)=={'binding','controls'} and set(supervision['controls'])=={'seal','terminal_evidence'}
for v in (supervision['binding'],*supervision['controls'].values()):pin(v['path'],v['sha256'])
assert supervision['binding']==pin(W/'own_rss_binding.json','ec966407b2a157d762c582241b82cc9c962ca93ae437e48289ef349c01ea4d35')
assert supervision['controls']['seal']==pin(W/'binding_controls/seal.json','b90f8a781dc8ad0044b7f30e6e7169077f0124fce3d77b83cbc650781ed9e4e3')
assert supervision['controls']['terminal_evidence']['sha256']=='5acffc484f1f78bc5df6520d98cc97f0234161ae8185b863384679d032a9e583'
for name,sha in cold['local_files'].items():pin(W/name,sha)
source_seal=read(S/'factory_seal.json','d182259bb17b580bbe45fe1853168c188515ef0b5ef654cfe7a72b668c32f3d5')
for name,sha in source_seal['files'].items():pin(S/name,sha)
assert len(source_seal['files'])==30 and len(cold['local_files'])==43
fpath=ROOT/'validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_cold_runtime_v12.py'
pin(fpath,'7037cf10b98e0f5098a87bb87808940a85132abce48e6156db7b136eddcfbf71')
pin(ROOT/'validation/axial_material/cold_component_input_consumer_identity_key_delta_graph_table_own_pid_peak_v12.py','6688e1fe2967bc63ff12900631e86ae18e30a0ee1bd0b98bb9fbcc4f0ac27823')
pin(ROOT/'validation/axial_material/cold_owned_specs_identity_key_delta_graph_table_component_input_intake_binding_v12_20261009.json','1e2b3c99e8f09c2716a5e44eca4cb9520339229c6e44a44ae6758d0dcd98d8db')
exact(cold['budgets'],dict(axial_seconds=4200,bootstrap_axial_seconds=4200,bootstrap_radial_seconds=600,
 host_seconds=120,max_maps=100,radial_seconds=300,setup_seconds=120,total_seconds=43200))
status=read(W/'AAA/run_status.json','c67168ee73a4b50688f194483d3eb06afbc9f36ee2d948605630962d2e69b40d')
assert status['classification']=='FAILED_NO_RETRY' and status['case']=='AAA' and status['completed_maps']==0
assert status['cases']=={} and status['reference_qualification'] is None
assert status['prepared_sha256']==pin(W/'prepared_cold.json')['sha256']
assert status['case_spec_sha256']==cold['case_spec']['sha256'] and status['rank_addendum_sha256']==cold['rank_addendum']['sha256']
assert status['max_maps_per_case']==100 and status['wall_cap_seconds_per_case']==43200 and status['outer_gate']==5e-7
assert set(q.name for q in (W/'AAA').iterdir())=={'bootstrap','numerical_layout_basis_admission.json','stages.json','run_claim.json','run_status.json'}
assert not (W/'ABA').exists()
claim=read(W/'AAA/run_claim.json');assert claim['case']=='AAA' and claim['prepared_sha256']==status['prepared_sha256']
failure=read(W/'cold_source_failure.json','f04266c23ba33b18557baf64b36d9256dadd7b2d88ea069c344a07789c908ebf')
assert failure['classification']=='FAILED_COMBINED_COLD_NO_RETRY' and '512 MiB RSS cap reached' in failure['error']
for k in ('scientific_qualification','AAA_accuracy_qualified','ABA_admitted'):assert failure[k] is False
assert 0<failure['actual_elapsed_seconds']==422.9763723749784<43200
assert not (W/'cold_source_complete_result.json').exists() and not (W/'cold_closeout_seal.json').exists()
stages=read(W/'AAA/stages.json')['stages']
labels=['archives/pack_archives','training/common_basis','training/rank_precision','AAA/bootstrap/case_setup',
 'AAA/bootstrap/white_tracking','AAA/bootstrap/make_route_contract','AAA/bootstrap/bootstrap_axial']
assert [s['label']for s in stages]==labels and [s['status']for s in stages]==['PASS']*6+['FAILED']
assert [s['wall_cap_seconds']for s in stages]==[120.0]*6+[4200.0]
watches=[]
for i,s in enumerate(stages):
 directory,label=s['label'].rsplit('/',1)
 log=W/directory/(label+'.log');wp=log.with_suffix('.watchdog.json');watch=read(wp)
 assert watch['command']==s['command'] and watch['own_child_only'] is True and watch['rss_cap_mib']==512
 assert watch['liveness_group_cleanup'] is True
 assert 0<watch['elapsed_seconds']<=s['elapsed_seconds']<s['wall_cap_seconds']
 assert 0<watch['wall_cap_seconds']<=s['wall_cap_seconds']
 if i<6:
  pin(log,s['log_sha256']);assert watch['returncode']==0 and watch['limit_failure'] is None
  assert watch['observed_peak_rss_mib']<512
 else:
  pin(log);assert watch['pid']==62748 and watch['returncode']==-15
  assert watch['sampled_peak_rss_mib']==watch['observed_peak_rss_mib']==512.890625>512
  assert watch['elapsed_seconds']==122.09484879102092 and s['elapsed_seconds']==123.01200679200701
  assert watch['live_rss_sample_count']==460 and watch['own_pid_wait4_observed'] is False
  for k in ('own_pid_wait4_pid','own_pid_wait4_status','own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib'):assert watch[k] is None
  assert watch['limit_failure']==failure['error'] and s['error']==status['error']=='own-child 512 MiB RSS cap reached'
  text=log.read_text()
  completion_mentions=[line for line in text.splitlines() if 'AXMAT-BOOTSTRAP-AXIAL-COMPLETE' in line]
  assert len(completion_mentions)==1 and completion_mentions[0].lstrip().startswith('ECHO ')
  progress=[row for row in text.splitlines() if row.startswith('AXMAT-RANK1-CACHE PROGRESS')]
  assert len(progress)>0 and progress[-1].startswith('AXMAT-RANK1-CACHE PROGRESS 5 32 61')
  tail=text[-6500:];(D/'failed_bootstrap_axial_log_tail.txt').write_text(tail)
 watches.append({'label':s['label'],'watch':pin(wp),'log':pin(log),'own_pid':watch['pid'],
  'status':s['status'],'sampled_peak_rss_mib':watch['sampled_peak_rss_mib'],
  'observed_peak_rss_mib':watch['observed_peak_rss_mib'],'elapsed_seconds':watch['elapsed_seconds'],
  'stage_elapsed_seconds':s['elapsed_seconds'],'original_stage_cap_seconds':s['wall_cap_seconds']})
toolrows={}
for phase in ('declare','prepare','prepare_binding','controls','finalize'):
 r=read(R/f'Root_actual_cold_{phase}_tool_terminal_return.json')
 i=read(R/f'Root_actual_cold_{phase}_tool_input.json')
 for k in ('actual_initial_tool_result','actual_terminal_tool_result'):exact(r[k],i[k])
 assert r['actual_terminal_tool_result']['exit_code']==0 and r['session_closed'] is True
 assert r['actual_tool_terminal_return_observed'] is True
 toolrows[phase]=r['actual_tool']
finalize=read(R/'Root_actual_cold_finalize_tool_terminal_return.json')
for k in ('full_stdout','full_stderr'):pin(finalize[k]['path'],finalize[k]['sha256'])
fs=read(finalize['full_stdout']['path']);assert fs['classification']=='PREPARED_COLD_INPUT_AND_ACTUAL_NEW_BINDING_CONTROLS_ONLY'
exact(fs['original_prepared'],pin(W/'prepared.json'));exact(fs['prepared'],pin(W/'prepared_cold.json'))
for k in ('scientific_qualification','AAA_accuracy_qualified','ABA_admitted'):assert fs[k] is False
assert (R/'cold_AAA.stdout').read_bytes()==b''
pin(R/'cold_AAA.stdout');pin(R/'cold_AAA.stderr')
stderr=(R/'cold_AAA.stderr').read_text()
for token in ('cold_launch_in_clean_process','bootstrap_axial.x2m','OwnRSSSerialExecutor',"RuntimeError: own-child 512 MiB RSS cap reached"):
 if token=='OwnRSSSerialExecutor':assert str(ROOT/'validation/axial_material/cold_own_pid_peak_supervisor_20261008/qualify_refined_AAA_layered_full.py') in stderr
 else:assert token in stderr
ownpath=ROOT/'validation/axial_material/cold_own_pid_peak_supervisor_20261008/qualify_refined_AAA_layered_full.py'
pin(ownpath,'ac51e68866f96547fa620fd971a911f93841a824412c3fe0a050bdbce00ae76b')
ot=ownpath.read_text();assert "if effective >= 512:" in ot and 'self.bounded.terminate_group(process);raise' in ot
assert 'process.pid' in ot and "['/bin/ps','-o','rss=','-p',str(process.pid)]" in ot
assert 'wait4_pid=None;wait4_status=None' in ot and 'wait4_raw_maxrss=None;wait4_peak=None;wait4_observed=False' in ot
report={'status':'PASS_READONLY_ACTUAL_NATIVE_FAILURE_BODY_ROOT_FAILURE_TERMINAL_PENDING',
 'classification':'ACTUAL_RSS_CAP_FAILURE_NO_RETRY','root_failure_terminal_review_pending':True,
 'source_factory':pin(fpath),'prepared_cold':pin(W/'prepared_cold.json'),
 'prepared_cold_only_supervision_added_inverse_exact':True,'source31_current_namespace_and_hashes_unchanged':True,
 'prepared43_current_local_hashes_unchanged':True,'complete_7stage_statuses':['PASS']*6+['FAILED'],
 'stages':watches,'zero_completed_maps':True,'native_entry_executed_but_bootstrap_failed':True,
 'coupled_convergence_completed':False,'partial_cache_iterations_are_not_full_completion':True,
 'failure':pin(W/'cold_source_failure.json'),'run_status':pin(W/'AAA/run_status.json'),
 'missing_kernel_fields_preserved_None':True,'actual_group_cleanup_observation':True,
 'original_production_budgets':cold['budgets'],'prior_actual_zero_exits':toolrows,
 'raw_bootstrap_partial_log_tail':pin(D/'failed_bootstrap_axial_log_tail.txt'),
 'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,
 'precision_assessment_not_started':True,'not_an_INCONCLUSIVE_precision_result':True,
 'old_namespace_permanent_no_retry':str(W),'business_import_call_execution':False,
 'Root_session_poll':False,'project_write':False,'35GB_union_rehash':False,'current_small_evidence_inventory':inventory}
q=D/'REPORT_FAILURE_BODY.json';q.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':report['status'],'report':pin(q),'failed_pid':62748,'sampled_RSS_MiB':512.890625,
 'zero_maps':True,'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False},sort_keys=True))
