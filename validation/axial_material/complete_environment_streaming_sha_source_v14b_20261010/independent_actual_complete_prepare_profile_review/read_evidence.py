"""Standard-library read-only evidence review. Does not import or call business code."""
from pathlib import Path
import ast, hashlib, json, os, stat
ROOT=Path('/Users/wen/spot')
HERE=Path(__file__).parent
REC=ROOT/'validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/actual_complete_prepare_profile_receipts'
SOURCECODE=ROOT/'validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/actual_complete_prepare_profile_sources'
ledger={}
def readpin(path, wanted=None, identity=None):
    p=Path(path)
    s=p.lstat()
    seven=lambda t:[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
    before=seven(s)
    assert stat.S_ISREG(s.st_mode) and s.st_size<8*2**20,(str(p),s.st_size)
    data=p.read_bytes()
    after=seven(p.lstat())
    assert before==after
    sha=hashlib.sha256(data).hexdigest()
    assert wanted is None or sha==wanted,(str(p),sha,wanted)
    assert identity is None or before==identity,(str(p),before,identity)
    ledger[str(p)]=dict(path=str(p),sha256=sha,size_bytes=len(data),identity_before=before,identity_after=after)
    return data
def jp(path, wanted=None, identity=None):
    return json.loads(readpin(path,wanted,identity))
def bound(record):
    return readpin(record['path'],record['sha256'],record.get('identity'))
receipt=jp(REC/'Root_actual_complete_prepare_profile_tool_terminal_return.json','dd6227960ed35aa63f8b32d495161e4ba326007f1d288a9212fd28cead4bcc53')
assert receipt['initial']['chunk_id']=='9a4ceb' and receipt['initial']['session_id']==2813
assert receipt['terminal']['chunk_id']=='062389' and type(receipt['terminal']['exit_code']) is int and receipt['terminal']['exit_code']==0
assert receipt['actual_tool_terminal_return_observed'] is True and receipt['session_closed'] is True and type(receipt['returncode']) is int and receipt['returncode']==0
assert 'session_id' not in receipt['terminal']
stdout=jp(receipt['input']['stdout'])
stderr=readpin(receipt['input']['stderr'])
assert stderr==b''
assert stdout['status']=='ACTUAL_COMPLETE_PREPARE_CLOSED_EXTERNAL_ROOT_REQUIRED' and stdout['actual_external_Root_terminal_still_required'] is True
host=json.loads(bound(stdout['host_result']))
assert host['status']==stdout['status']
child=json.loads(bound(host['actual_child_profile']))
watch=json.loads(bound(host['actual_watchdog']))
decl=json.loads(bound(host['actual_declaration']))
admission=json.loads(bound(host['actual_source_admission']))
log=json.loads(bound(host['actual_full_merged_stdout_stderr']))
assert host['watchdog']==watch
assert log==dict(declaration=host['actual_declaration']['path'],declaration_sha256=host['actual_declaration']['sha256'],source_root=decl['source_root'],classification='DECLARED_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_ONLY_V14B')
assert len(host['stage_records'])==1 and host['stage_records'][0]['status']=='PASS'
stage=host['stage_records'][0]
assert stage['command']==host['actual_command']==watch['command']
assert stage['log_sha256']==host['actual_full_merged_stdout_stderr']['sha256']
assert stage['wall_cap_seconds']==600 and type(watch['returncode']) is int and watch['returncode']==0
assert type(watch['pid']) is int and watch['pid']>0
assert watch['limit_failure'] is None and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
assert 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=stage['wall_cap_seconds']
assert watch['rss_cap_mib']==512 and 0<watch['sampled_peak_rss_mib']<512
caps=dict(whole_wall_cap_seconds=1800,stage_wall_cap_seconds=600,rss_cap_mib=512,archive_cap_bytes=2*2**30,threads=1,children_at_once=1,retries=0,supervisor_class_or_MRO_modified=False)
for k,v in caps.items(): assert host[k]==v,(k,host[k])
assert 0<host['whole_elapsed_seconds']<1800 and 0<host['whole_archive_bytes']<2*2**30
for rr in (host['resources_before'],host['resources_after'],stage['resource_before'],stage['resource_after']):
    assert rr['artifact_budget_bytes']==96*2**30 and rr['min_free_bytes']==8*2**30
    assert rr['artifact_bytes']<96*2**30 and rr['disk_free_bytes']>=8*2**30
    assert rr['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
assert host['canonical_prepare_completed'] is True and receipt['canonical_prepare_completed'] is True
for obj in (host,child,receipt):
    for k in ('full86_executed','compilation_or_transport_launched','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'):
        assert obj[k] is False,(k,obj[k])
assert child['status']=='COMPLETE_PREPARE_RETURNED' and child['failure'] is None
assert child['complete_source_pins_before']==child['complete_source_pins_after']
for rec in [*host['input_sources'],host['original_helper'],host['resource_factory'],*child['complete_source_pins_before']]: bound(rec)
drivertext=readpin(SOURCECODE/'prepare_profile_driver.py','e14182d3020361499faf9fb9e56bc41ad258f98a4c07d5357723131973ba6237').decode()
hosttext=readpin(SOURCECODE/'prepare_profile_host.py','85b62eb8f1092331b0cc69cf04935380cc501ce73ff0defbd3228fa07d8757ff').decode()
ast.parse(drivertext);ast.parse(hosttext)
target=ROOT/'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py'
targettext=readpin(target,'4fbd1b054c6516b410181144f088d540a64a8ab793d480fb2c89de0d1252199c').decode()
ast.parse(targettext)
assert "runpy.run_path(str(TARGET), run_name='__main__')" in drivertext
assert "if code.co_name != 'digest':" in drivertext and 'sys.setprofile(None)' in drivertext
assert "full.OwnRSSSerialExecutor(HOST_OUT,remaining" in hosttext.replace(' ','')
assert "'DynamicHistoryResources'" not in drivertext
oldreceipt=jp(child['complete_source_pins_before'][1]['path'],child['complete_source_pins_before'][1]['sha256'])
argv=list(oldreceipt['input']['argv']); argv[1]=str(target)
assert child['actual_canonical_argv']==argv and len(argv)==23 and argv[2]=='prepare-build'
for k,v in dict(original_stage_count=68,complete_stage_count=86,total_wall_seconds=1800,stage_wall_seconds=600,rss_cap_mib=512,threads=1,numeric_children_at_once=1,retries=0,archive_reserve_bytes=2*2**30,artifact_budget_bytes=96*2**30,min_free_bytes=8*2**30).items():
    assert decl[k]==v,(k,decl[k])
assert len(decl['build_commands'])==12 and decl['production_link_command']==decl['build_commands'][2]
assert len(decl['files'])==12697 and len(decl['preserved_predecessors'])==8
for rec in host['input_sources'][1:]:
    if str(rec['path']) in decl['files']: assert decl['files'][rec['path']]==rec['sha256']
src=Path(decl['source_root'])
assert decl['source_inventory']['symlinks']=={} and decl['source_directories']==[]
actual_files={p.name for p in src.iterdir() if p.is_file()}
assert actual_files==set(decl['source_inventory']['files'])
assert all(p.is_file() and not p.is_symlink() for p in src.iterdir())
for name,wanted in decl['source_inventory']['files'].items():readpin(src/name,wanted)
assert len(actual_files)==18
assert admission['actual_new_sender_source']==dict(path=str(src/'FLU2DR64.f'),sha256='cd8e419c19f3a473beb6ded27705c513a07363a1a37e003c64266c5ef9cf5fb1')
assert admission['whole_link_inverse_restoration_exact'] is True and admission['scientific_qualification'] is False
assert admission['sole_new_production_objects']==['SPOT1P64.o','FLU2DR64.o']
assert admission['control_contract']==decl['control_contract']
assert admission['sender_wrapper_control_contract']==decl['sender_control_contract']
assert admission['stream_environment_helper_admission']==decl['stream_environment_helper_admission']
stream=admission['stream_environment_helper_admission']
for k in ('helper','source_patch_proof','actual_helper_controls_admission','original_helper','component_factory_parent'):bound(stream[k])
assert stream['supervisor_class_and_MRO_unchanged'] is True and stream['original_cache_and_sender_math_and_raw_controls_unchanged'] is True
for obj in (decl,admission,stream):
    for k in ('native_RSS_proof_obtained','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted','native_RSS_verified'):
        if k in obj:assert obj[k] is False,(k,obj[k])
out=Path(host['actual_declaration']['path']).parent
assert not any((out/'build').iterdir())
assert {p.name for p in (out/'runtime').iterdir()}=={'run_bounded_dragon.py'}
readpin(out/'runtime/run_bounded_dragon.py','bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09')
summary={}
for label,profile in (('child',child['profile']),('host',host['host_profile'])):
    assert profile['open_selected_frames']==0 and profile['forbidden_calls']==[] and profile['profiler_cleared'] is True
    assert profile['sha_or_guard_calls_skipped'] is False and profile['callable_or_class_replaced'] is False
    assert profile['timing_includes_profile_overhead'] is True
    assert all(r['calls']==r['returns'] for r in profile['rows'])
    assert all(s['name']!='digest' for s in profile['spans'])
    assert sum(r['returns'] for r in profile['rows'] if r['name']!='digest')==len(profile['spans'])
    summary[label]=dict(rows=len(profile['rows']),spans=len(profile['spans']),selected_calls=sum(r['calls'] for r in profile['rows']),digest_calls=sum(r['calls'] for r in profile['rows'] if r['name']=='digest'),profile_flags={k:v for k,v in profile.items() if k not in ('rows','spans')},highest_inclusive_rows=sorted(profile['rows'],key=lambda r:r['inclusive_seconds'],reverse=True)[:15])
assert summary['child']['spans']==293 and summary['host']['spans']==141
def selected(name,fileend):
    return next(r for r in child['profile']['rows'] if r['name']==name and r['file'].endswith(fileend))
for n,f,c in [('prepare_build',target.name,1),('production_admission','prepare_qualified_AB_rank1_cache_production.py',2),('production_admission','prepare_qualified_AB_rank1_cache_memory_production.py',1),('production_admission','prepare_qualified_AB_moment_order_production.py',2),('production_admission','prepare_qualified_AB_source_factor_production.py',2),('capture_admission','prepare_qualified_AB_source_factor_production.py',2),('control_audit','prepare_qualified_AB_rank1_cache_production.py',2),('control_audit','prepare_qualified_AB_rank1_cache_memory_production.py',1),('memory_controls_audit','prepare_qualified_AB_rank1_cache_memory_production.py',1),('check','prepare_qualified_AB_moment_order_production.py',7),('environment',target.name,1),('environment','complete_environment_streaming_sha_helper_v14b.py',1),('environment','prepare_qualified_AB_source_factor_production.py',8)]:
    assert selected(n,f)['calls']==c,(n,f)
momenttext=readpin(ROOT/'validation/axial_material/prepare_qualified_AB_moment_order_production.py','fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41').decode()
assert 'if any(path == old or path.is_relative_to(old) or old.is_relative_to(path) for old in roots):' in momenttext
assert 'validate_history_roots(snapshot["resource_roots"], self.artifacts_root)' in momenttext
report=dict(schema='AXMAT_V14B_ACTUAL_COMPLETE_PREPARE_INDEPENDENT_READONLY_REVIEW_V1',status='PASS_ACTUAL_PREPARATION_ONLY',actual_root_terminal=dict(initial=receipt['initial'],terminal=receipt['terminal'],session_closed=True),input_evidence_scope='Only current modest raw streams, JSON declarations, frozen source and source18 were read in full. No business imports/calls, Root polling or huge historical payload reads.',result_pins=ledger,timings=dict(child_prepare_inclusive_seconds=selected('prepare_build',target.name)['inclusive_seconds'],child_elapsed_seconds=child['actual_child_elapsed_seconds'],watch_elapsed_seconds=watch['elapsed_seconds'],stage_elapsed_seconds=stage['elapsed_seconds'],host_whole_elapsed_seconds=host['whole_elapsed_seconds'],sampled_own_PID_peak_rss_mib=watch['sampled_peak_rss_mib']),caps=caps,prepared_scope=dict(source_files=18,declared_unique_files=len(decl['files']),preserved_inventories=8,build_commands=12,original_stages=68,complete_future_stages=86,build_directory_empty=True,runtime_namespace_only_original_bounded_runner=True),profile_summary=summary,actual_call_scope='Recursive parent admissions, original complete file verification/inventories, legacy numeric raw audits and full dynamic history checks returned normally; digest calls are observed aggregates, not unique file-read counts. Current full declaration and source gates are retained. Independent reviewer did not rehash huge historical inputs.',cost_interpretation=['validate_history_roots is an original complete root guard with pairwise lexical ancestry checks, O(number_of_roots squared), plus fresh directory/ancestor metadata checks. It is invoked repeatedly before and after each complete history scan.','Child39 calls151.543625s and host56 calls375.501074s are observed inclusive selected times. Host/child execute concurrently; do not add their times. Parent wrapper timings overlap the same inner validator.','sys.setprofile receives all Python events, including unselected pathlib/generator activity. 293child+141host saved spans and sampled194.546875MiB show no million-span list, but CPU observation overhead is neither measured nor removed. These elapsed times do not establish normal speed.','If a future observer must be smaller, use exact code-identity high-level aggregates and bounded outer-call timing; narrower selection alone does not avoid the all-event sys.setprofile callback. No active source or original checks were changed.'],qualification=dict(canonical_prepare_completed=True,full86_executed=False,compilation_or_transport_launched=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False),earlier_read_only_reader_type_error='b5c3f1 exited1 while formatting preserved_predecessors as dict instead of actual list; 11beb5 exited1 because reader initially assumed runtime empty. Actual prepare intentionally copies the original bounded runner there. Both reader-only assumptions were corrected; no project/evidence/business changed. All original tool returns are retained in the external reader receipt.')
(HERE/'REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],report=str(HERE/'REPORT.json'),pins_read=len(ledger),future_stages=86,source18=True,spans=dict(child=293,host=141),qualifications=report['qualification']),ensure_ascii=False))
