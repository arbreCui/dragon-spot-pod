import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D=B/'actual_complete_combined_build_v17_sources'
HP=D/'combined_build_host.py'
PP=D/'Root_finite_build_host_source_inverse.json'
C=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py')
A=Path('/Users/wen/spot/validation/artifacts')
O=A/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v17-20261010'
T=A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v17-20261010'
S=A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v17-20261010'
def pin(path,wanted=None):
 p=Path(path);s=p.lstat();assert stat.S_ISREG(s.st_mode)
 before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 with p.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
 q=p.lstat();assert before==[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
 assert wanted is None or digest==wanted,(str(p),digest,wanted)
 return dict(path=str(p),sha256=digest,identity=before)
proof=json.loads(PP.read_text());host=HP.read_bytes();parent=Path(proof['parent_path']).read_bytes()
pins=[pin(HP,'cf2c3fd0e9404a3c2858c398d0457a2a6ece38b675e74c143564dac5894002f9'),pin(PP),pin(proof['parent_path'],'37d432b8c91ddec6816fed6f7cea11fbfcba7071655ea64bc0f3c562288185d3'),pin(C,'feebcbb5894797d9f748a7b43e817b30da90e64068f17f141135121462ef234c'),pin(O/'declaration.json','cb1984ee991230e9b56a9783acafe36bfb9063b4b641ebe64387d3e60c29fb30'),pin(T/'declaration_terminal_return.json','c743c01c3f40ac32e06a4f3371c82dfa4b84314b0c85509aa1710216afe569b2')]
assert len(proof['changes'])==proof['finite_change_count']==13
forward=parent;occurrences=[]
for index,c in enumerate(proof['changes'],1):
 before,after=c['before'].encode(),c['after'].encode();count=forward.count(before);assert count==c['count']
 occurrences.append(dict(index=index,forward_occurrences=count));forward=forward.replace(before,after)
assert forward==host
inverse=host
for index,c in reversed(list(enumerate(proof['changes'],1))):
 before,after=c['before'].encode(),c['after'].encode();count=inverse.count(after);assert count==c['count']
 occurrences[index-1]['inverse_occurrences']=count;inverse=inverse.replace(after,before)
assert inverse==parent and hashlib.sha256(inverse).hexdigest()==proof['parent_sha256']
assert proof['business_executed'] is False and proof['native_executed'] is False
ht=host.decode();ct=C.read_text();htree=ast.parse(ht);ctree=ast.parse(ct)
def literal_bindings(tree,names):
 values={}
 for n in tree.body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in names:values[n.targets[0].id]=ast.literal_eval(n.value)
 return values
literal=literal_bindings(htree,{'EXPECTED_COMMANDS','EXPECTED_LABELS','INNER_FAMILY','DECLARATION_SHA','PREP_SHA','TARGET_SHA'})
cliteral=literal_bindings(ctree,{'FAMILY'})
d=json.loads((O/'declaration.json').read_text())
assert literal['INNER_FAMILY']==cliteral['FAMILY']
assert literal['EXPECTED_LABELS']==d['stages']==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']
constants={}
for n in ctree.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('OLD','PHYSICAL','DEDUP','TRIM'):
  value=n.value;assert isinstance(value,ast.BinOp) and isinstance(value.op,ast.Div) and isinstance(value.left,ast.Name) and value.left.id=='ART' and isinstance(value.right,ast.Constant)
  constants[n.targets[0].id]=A/value.right.value
expected=[d['production_link_command'],['/usr/bin/nm','-g',*d['actual_production_objects']],['/usr/bin/nm','-g',str(O/'runtime/Dragon')],['/usr/bin/otool','-L',str(O/'runtime/Dragon')]+[str(constants[k]/'runtime/Dragon') for k in ('OLD','PHYSICAL','DEDUP','TRIM')],[d['python_command'],str(C),'audit-build','--sha256',literal['DECLARATION_SHA'],'--prep-sha256',literal['PREP_SHA']]]
assert literal['EXPECTED_COMMANDS']==expected
funcs={n.name:ast.get_source_segment(ct,n) for n in ctree.body if isinstance(n,ast.FunctionDef)}
run=funcs['run_build'];audit=funcs['audit_build'];check_watch=funcs['check_watch']
full_path=Path('/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py');parent_path=A/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py'
pins += [pin(full_path,'70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'),pin(parent_path,'38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'),pin(B/'actual_prepare_sources/prepare_cli_host_v15.py','3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'),pin(Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_source_factor_production.py'),'619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'),pin(Path('/Users/wen/spot/validation/axial_material/moment_order_complete_history_resource_trie_20261010.py'),'ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022')]
checks={
 'whole13_forward_inverse_exact':forward==host and inverse==parent,
 'guard_and_MRO_original':"full,production=helper.modules();helper.guard_admission(full)" in ht and "full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)" in ht and "Path(full.__file__).resolve()!=support.FULL" in ht and "Path(production.__file__).resolve()!=support.PARENT" in ht,
 'real_resource_factory_and_runner_binding':"resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)" in ht and "runner.resources is not resources" in ht,
 'original_outer1800_inner600_rss512_archive2g':"WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30" in ht and "runner.execute(HOST/'run','build',command,WHOLE_CAP)" in ht and 'outer_command_wall_cap_seconds=WHOLE_CAP,inner_original_stage_wall_cap_seconds=STAGE_CAP' in ht,
 'canonical_inner_stage_algorithms_unmodified':"runner.execute(OUT/directory,stem,command,STAGE_WALL)" in run and "runner.execute(OUT/'audit','audit',commands[-1],STAGE_WALL" in run,
 'whole_cap_reduced_to_remaining_original_deadline':"remaining=WHOLE_CAP-(time.monotonic()-started)" in ht and "full.OwnRSSSerialExecutor(HOST,remaining,'COMPLETE_COMBINED_BUILD',resources)" in ht,
 'all_five_labels_family_commands_literal_source_equal':literal['EXPECTED_COMMANDS']==expected and literal['INNER_FAMILY']==cliteral['FAMILY'],
 'fresh_host_existing_prepared_source_out_terminal':"if os.path.lexists(HOST)" in ht and "if not all(p.is_dir() for p in (SOURCE,OUT,TERMINAL))" in ht,
 'no_prior_numeric_build_or_retry_artifacts':all(x in ht for x in ["'execution_claim.json'","'seal.json'","'driver_result.json'","'closeout_failure.json'","'raw_metadata_receipt.json'","'audit/binary_identity.json'","'audit/result.json'","INNER_FAMILY+'/stages.json'","'runtime/Dragon'"]),
 'all_declared_immutable_inputs_full_pin_before_after':"inputs += [support.pin(p) for root in (SOURCE,TERMINAL)" in ht and "for entry in inputs+[hpin,rpin]:" in ht and "support.pin(entry['path'],entry['sha256'])!=entry" in ht,
 'complete_source_review_archive_full_pins':"[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]" in ht,
 'all_five_stage_status_and_watchdog_checks':"len(inner)!=5" in ht and "[s['command'] for s in inner]!=EXPECTED_COMMANDS" in ht and "any(s['status']!='PASS' for s in inner)" in ht and "type(iw['returncode']) is not int" in ht and "not 0<iw['wall_cap_seconds']<=stage['wall_cap_seconds']<=600" in ht and "support.pin(raw_log)['sha256']!=stage['log_sha256']" in ht,
 'watchdog_fields_source_matches_original_producer':all(x in full_path.read_text() for x in ['sampled_peak_rss_mib=peak','own_child_only=True','liveness_group_cleanup=True','returncode=process.poll()']),
 'all5_and_prior4_watchdog_reports_agree':"inner_watches!=result['watchdogs'] or inner_watches[:-1]!=audit['previous_stage_watchdogs']" in ht and "watchdogs=[check_watch(s) for s in stages]" in run and "previous_stage_watchdogs=watches" in audit,
 'result_raw_audit_producer_shape_matches':"fresh_cold_AAA_required=True" in run and "complete_raw_tools_and_link_stdout=True" in run and "before_binary_identity_gates=True" in run and "classification='PASS_COMBINED_RUNTIME_LINK_IDENTITY_ONLY'" in audit and "binary_status='PASS'" in audit,
 'source_and_out_actual_tail_size_exact':"actual_size=support.archive_bytes((SOURCE,OUT))" in ht and "admission['actual_archive_bytes']!=actual_size" in ht and "actual_archive_bytes=size" in run,
 'all4_tail_fields_preserved_verified':"('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')" in ht and "tail_resources['declared_resource_roots']!=d['resource_roots']" in ht and "tail_resources['resource_scope_contract']!=d['resource_scope_contract']" in ht,
 'complete_seal_schema_files_dirs_no_symlinks':"set(files)!=set(seal['files'])|{'seal.json'}" in ht and "seal['directories']!=sorted(directories)" in ht and "seal['symlinks']!={}" in ht and "complete=inventory(OUT);write_new(OUT/'seal.json'" in run,
 'runtime_pin_shape_path_sha_only_matches_canonical':"for k in ('path','sha256')" in ht and "corrected_runtime=pin(OUT/'runtime/Dragon')" in run and "def pin(path):return dict(path=str(require(path)),sha256=digest(path))" in ct,
 'outer_guard_typed0_rss_ownchild_cleanup':all(x in ht for x in ["type(watch['returncode']) is not int","watch['returncode']!=0","watch['limit_failure'] is not None","watch['own_child_only'] is not True","watch['liveness_group_cleanup'] is not True","not 0<=watch['sampled_peak_rss_mib']<RSS_CAP"]),
 'full_root_archive_counts_host_source_out_terminal_and_hostsource_twice':ht.count('support.archive_bytes((HOST,SOURCE,OUT,TERMINAL,SOURCE_ARCHIVE))')==2,
 'five_thread_keys_single_child_no_retry':"any(os.environ.get(k)!='1' for k in support.THREAD_KEYS)" in ht and 'children_at_once=1,retries=0' in ht,
 'no_profile_or_optimization':"sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None" in ht,
 'whole_INPUT_native_science_credit_still_false':all(x in ht for x in ['whole_combined_INPUT_admitted=False','native_RSS_verified=False','AAA_accuracy_qualified=False','ABA_admitted=False']),
}
assert all(checks.values()),{k:v for k,v in checks.items() if not v}
assert not any(isinstance(n,ast.ClassDef) for n in htree.body)
assert not any(isinstance(n,ast.Assign) and any(isinstance(t,ast.Attribute) and t.attr in ('__bases__','__file__','_process') for t in n.targets) for n in ast.walk(htree))
for q in pins:assert pin(q['path'],q['sha256'])==q
out=Path(tempfile.mkdtemp(prefix='axmat_v17_combined_build_host_finite_source_review_20261010_',dir='/private/tmp'))
report=dict(schema='INDEPENDENT_FINITE_V17_COMBINED_BUILD_HOST_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_EXECUTION_REQUIRED',host_sha256=pins[0]['sha256'],parent_sha256=pins[2]['sha256'],finite_changes=13,whole_byte_forward_inverse_exact=True,occurrence_checks=occurrences,checks=checks,source_and_metadata_inputs_full_sha7id_before_after=pins,all_five_expected_commands_match_source_and_declaration=True,no_blocking_shape_or_API_issue_found=True,outer_whole_command_wall_seconds=1800,inner_original_stage_wall_seconds=600,rss_mib=512,archive_cap_bytes=2*2**30,full_archive_scope=['HOST','SOURCE','OUT','TERMINAL','SOURCE_ARCHIVE'],existing_prepared_namespaces_are_inputs=True,normal_original_stage_algorithms_unchanged=True,business_or_helper_or_module_API_imported_or_executed=False,numeric_payload_read=False,actual_success_pins=None,original_five_stage_build_executed=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,material_limit='Source-only approval proves no source shape error found; actual complete whole build can still fail original wall/RSS/disk/identity gates. Original merged child stdout/stderr semantics remain.')
(out/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(out/'REPORT.txt').write_text('cf2c3f… 新host有限 SOURCE 审查通过，无 shape / API 阻塞。\n13 项有限变更正向生成当前host，逆向全字节还原原37d PREPhost，genuine guard、类/MRO、真实resource绑定保持。\n原SOURCE静态5命令、family/labels、driver_result/audit/raw receipt/stages/seal及全部watchdog字段匹配；完整5项及4tail均检查。\n外层 whole1800、内层原每stage600，RSS512、完整 HOST+SOURCE+OUT+TERM+hostSource 2GiB、history96/free8、单线程、单numeric child / 0 retry保持。\n只读源码/声明/凭证，不运行或导入host、helper、API、numeric；实际5stage / whole INPUT / native / AAA / ABA尚未授成功资格。\n')
print(json.dumps(dict(status=report['status'],directory=str(out),review_sha256=hashlib.sha256((out/'REVIEW.json').read_bytes()).hexdigest(),checks=len(checks),finite_changes=13,blocker=False,business_executed=False),allow_nan=False))
