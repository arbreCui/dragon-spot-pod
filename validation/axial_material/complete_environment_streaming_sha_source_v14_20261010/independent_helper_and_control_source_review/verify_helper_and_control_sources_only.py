from pathlib import Path
import ast,hashlib,json,stat
D=Path('/private/tmp/axmat_v14_complete_environment_streaming_helper_controls_source_only_20261010')
C=Path('/private/tmp/axmat_v14_complete_environment_streaming_sha_helper_compatible_source_draft_20261010')
new=C/'complete_environment_streaming_sha_helper_v14.py'
old=Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_source_factor_production.py')
driver=D/'helper_only_controls.UNREADY.py'
def identity(p):
 x=p.lstat();return [x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
pins={}
for p in [new,old,driver,C/'source_complete_inverse_proof.json']:
 i=identity(p);b=p.read_bytes();assert identity(p)==i and stat.S_ISREG(i[2]);pins[str(p)]={'sha256':hashlib.sha256(b).hexdigest(),'size_bytes':len(b),'identity':i}
assert pins[str(new)]['sha256']=='839ea8cc88e4f10d36b6bd8fcb283c9c774702e4c3688fc8a66831431c1cb5fa'
assert pins[str(old)]['sha256']=='619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
ns=new.read_text();os=old.read_text();nt=ast.parse(ns);ot=ast.parse(os)
original={n.name:n for n in ot.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
candidate={n.name:n for n in nt.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
assert set(original)<=set(candidate)
changed=[name for name in original if ast.get_source_segment(os,original[name])!=ast.get_source_segment(ns,candidate[name])]
assert changed==['digest'],changed
unchanged={name:hashlib.sha256(ast.get_source_segment(ns,candidate[name]).encode()).hexdigest() for name in original if name!='digest'}
prefix=0
while prefix<min(len(os),len(ns)) and os[prefix]==ns[prefix]:prefix+=1
suffix=0
while suffix<min(len(os)-prefix,len(ns)-prefix) and os[-suffix-1]==ns[-suffix-1]:suffix+=1
original_region=os[prefix:len(os)-suffix]
candidate_region=ns[prefix:len(ns)-suffix]
assert ns[:prefix]+original_region+ns[len(ns)-suffix:]==os
assert original_region.count('def digest(')==1
assert not any(ast.get_source_segment(os,n) in original_region for k,n in original.items() if k!='digest')
assert 'with Path(path).open("rb") as stream:\n        return hashlib.file_digest(stream, "sha256").hexdigest()' in ast.get_source_segment(ns,candidate['digest'])
assert '_env_stream_absolute_literal(path, allow_relative=True)' in ast.get_source_segment(ns,candidate['_env_stream_full_digest'])
assert 'path = Path(os.getcwd()) / path' in ns
assert 'followlinks=False' in ast.get_source_segment(ns,candidate['inventory'])
assert "if type(count) is not int or not 0 <= count <= len(buffer)" in ns
assert "total != before.st_size" in ns and "_env_stream_identity7(after) != _env_stream_identity7(before)" in ns
assert "if _env_stream_path_snapshot(literal) != entry['snapshot']" in ns
assert "current['target_path'] != state['native_alias_expected'][name]" in ns
assert "state['pid'] != os.getpid()" in ns and "state['cwd'] != os.getcwd()" in ns
assert "state['view'].release()" in ns and "state['memo'].clear()" in ns
assert "alias_observation_errors[name] = (type(error).__name__, str(error))" in ns
assert "_ENV_STREAM_SCOPE_LOCK.release()" in ns

ds=driver.read_text();dt=ast.parse(ds)
assignments={}
for n in dt.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):assignments[n.targets[0].id]=n.value
assert ast.literal_eval(assignments['HELPER_SHA256']) is None
assert ast.literal_eval(assignments['STATUS']).startswith('UNREADY')
assert 'if __name__==' in ds and 'if STATUS!=' in ds
assert "self.module._env_stream_open=opened" in ds and "self.module._env_stream_open=self.original" in ds
assert 'Path.open=' not in ds and 'old.digest=' not in ds and 'old.environment=' not in ds
assert "return Path(path).open('rb', buffering=0)" in ast.get_source_segment(ns,candidate['_env_stream_open'])
assert "--action" in ds and "historical-environment" in ds
assert "normal" not in ast.unparse(dt.body[-1]).lower() or isinstance(dt.body[-1],ast.If)
# Entire program parsed, never imported, compiled, or invoked as a control.
cases=[]
for n in ast.walk(dt):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='run' and n.args and isinstance(n.args[0],ast.Constant):cases.append(n.args[0].value)
assert len(cases)==18 and len(set(cases))==18
# Source for-loop adds the three distinct actual mutation cases at execution.
assert "for mode in ['truncate','replace','rewrite']" in ds
assert len(cases)+3==21
evidence={'schema':'AXMAT_V14_HELPER_COMPATIBLE_SOURCE_AND_DRIVER_STATIC_EVIDENCE_V1',
 'full_source_SHA_and_7identity_before_after':pins,'original_complete_function_count':len(original),
 'old_unchanged_full_function_source_SHA':unchanged,'changed_original_functions':changed,
 'new_private_functions':sorted(set(candidate)-set(original)),
 'whole_single_region_inverse_to619':{'original_start':prefix,'old_region_characters':len(original_region),'candidate_region_characters':len(candidate_region),'complete_old_source_sha256':pins[str(old)]['sha256'],'old_region':original_region,'candidate_region_sha256':hashlib.sha256(candidate_region.encode()).hexdigest(),'restored_entire_source_exact':True},
 'SOURCE_default_digest_oldfresh_file_digest_restored':True,
 'relative_paths_and_symlink_dotdot_original_open_semantics_preserved':True,
 'all_environment_verify_inventory_modules_guard_source_byteexact':True,
 'helper_only_fixture_groups':cases+['during_stream_truncate','during_stream_replace','during_stream_rewrite'],
 'fixture_controls_executed':False,'historical_environment_action_executed':False,
 'optional_history_action':'normal original619 and new canonical helper only; 5 exact environment fields retain whole owner/namespace scopes, profile original stdlib file_digest without monkeypatch and local new _env_stream_open realFD probe; old->new complete reads under Root120/512; overhead explicitly included',
 'mandatory_Root_future_integration':'New factory passes native_library_aliases explicitly inside each complete_environment_digest_context; new helper source/addition fully declared/pinned; genuine helper/modules/MRO unchanged; frozen failed V13 not rerun; full fresh86 and wholeINPUT still required'}
for p,v in pins.items():assert identity(Path(p))==v['identity']
(D/'complete_helper_source_inverse_and_driver_static_evidence.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+'\n')
report={'schema':'AXMAT_V14_COMPLETE_STREAMING_HELPER_AND_ISOLATED_CONTROL_DRIVER_SOURCE_REVIEW_V1',
 'status':'PASS_HELPER_SOURCE_AND_UNREADY_CONTROL_DRIVER_ONLY','helper_candidate_sha256':pins[str(new)]['sha256'],
 'helper_parent_sha256':pins[str(old)]['sha256'],'whole_single_region_inverse_to619':True,
 'original_functions':len(original),'all_original_except_digest_byteexact':True,
 'default_outside_context_original_file_digest_source_restored':True,
 'stable_alias_hardlink_relative_semantics_source_preserved':True,
 'whole_EOF_length_seven_identity_and_each_alias_hop_source_guards_present':True,
 'native_alias_entry_observation_deferred_and_normalexit_complete_checks_present':True,
 'normal_and_exception_context_cleanup_and_owner_source_guards_present':True,
 'source_blockers':[],'runtime_controls_remain_required':True,'driver_source_sha256':pins[str(driver)]['sha256'],
 'driver_STATUS':'UNREADY_CANONICAL_HELPER_FINAL_SOURCE_SHA_NOT_BOUND','driver_canonical_helper_SHA':None,
 'meaningful_helper_fixture_groups':21,'optional_real_history_action_separate':True,
 'original86_or68_mathematical_stage_count_increment':0,
 'Root_external_child_limits_required':{'wall_seconds':120,'OwnRSS_MiB':512,'threads':1,'children_at_once':1,'retries':0,'control_archive_bytes':67108864,'history_budget_bytes':103079215104,'min_free_bytes':8589934592},
 'actual_helper_control_results':None,'actual_optional_history_timing_results':None,
 'business_imported_or_called':False,'new_helper_imported_or_called':False,'fixture_files_created':False,
 'compiled':False,'benchmark_executed':False,'Root_polled':False,'project_written':False,
 'complete_component_qualified':False,'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,
 'evidence_files':['complete_helper_source_inverse_and_driver_static_evidence.json','helper_only_controls.UNREADY.py'],
 'actual_readonly_tool_receipt':None}
(D/'REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
(D/'REPORT.txt').write_text('V14 兼容 helper 839ea8 源码及独立控制驱动草稿只读核对通过。原619只有digest区域变化，全部其它原函数整段字节不变，完整单区域逆回原源。\n'
 '外部默认摘要恢复原fresh file_digest；ctx支持固定cwd相对path且保留symlink/..打开语义，nativealias初读失败延后到原guard/normalexit，全部链/目标/fd七身份、全EOF/长度、上下文清理与owner源约束保持。\n'
 '驱动仅正常加载未来正式canonical helper，SHA仍None且UNREADY。21组独立helper-only控制和可选old619→new完整环境计时动作只写源码，未创建fixture、未执行helper/控制/benchmark。\n'
 '必须Root先绑定最终SHA并用真实120秒/512MiB/64MiB收集器执行。可选计时含profile/openhook开销，不保证真实full86节时；不增加原数学控制计数，不授native/AAA/ABA资格。\n')
print(json.dumps({'status':report['status'],'REPORT_path':str(D/'REPORT.json'),'REPORT_sha256':hashlib.sha256((D/'REPORT.json').read_bytes()).hexdigest(),'driver_sha256':pins[str(driver)]['sha256'],'helper_sha256':pins[str(new)]['sha256'],'source_before_after_identity_equal':True,'fixture_group_count':21,'actual_helper_results':None},ensure_ascii=False))
