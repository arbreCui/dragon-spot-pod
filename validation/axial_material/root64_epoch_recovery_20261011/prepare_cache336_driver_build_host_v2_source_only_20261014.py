"""Only prepare unique Driver Host v2 Source/plan/inverse; never execute Host or compiler."""
import ast,copy,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'native_rank1_cache336_build_host_source_v1_20261014'
OUT=R/'native_rank1_cache336_build_host_source_v2_20261014'
seen={}
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    p=Path(path);s=p.lstat();i=ids(s);assert stat.S_ISREG(s.st_mode);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:assert ids(os.fstat(f.fileno()))==i;b=f.read();assert ids(os.fstat(f.fileno()))==i
    assert ids(p.lstat())==i;v=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=i);seen[str(p)]=(v,b);return v,b
def read(p):
    v,b=pin(p);return json.loads(b),v
def put(n,v):
    b=v.encode()if isinstance(v,str)else(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode();p=OUT/n;fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb')as f:f.write(b);f.flush();os.fsync(f.fileno())
    return pin(p)[0]
assert not OUT.exists()
original,raw=pin(OLD/'build_native_rank1_cache336_driver_runtime.py')
old_block="""                if sorted(p.name for p in (OUT/'build').iterdir()) != ['SPOT_GLOBAL_NATIVE_DRIVER64.o']:
                    raise RuntimeError('Driver-only compile must create exactly one object, no module or other outputs')
"""
new_block="""                expected_compile_files = ['SPOT_GLOBAL_NATIVE_DRIVER64.o','compile_Driver.log','compile_Driver.watchdog.json']
                if sorted(p.name for p in (OUT/'build').iterdir()) != expected_compile_files:
                    raise RuntimeError('Driver-only compile requires exact object/log/watch, no module or other outputs')
                for name in expected_compile_files:
                    path = OUT/'build'/name
                    state = path.lstat()
                    if not stat.S_ISREG(state.st_mode) or state.st_nlink != 1 or state.st_uid != os.getuid():
                        raise RuntimeError('own compile object/log/watch ordinary UID/single-link files')
                    actual_pin = c.pin(path)
                    if actual_pin['identity'] != [state.st_dev,state.st_ino,state.st_mode,state.st_nlink,state.st_size,state.st_mtime_ns,state.st_ctime_ns]:
                        raise RuntimeError('compile object/log/watch fullEOF all7 unchanged')
"""
blocks=[dict(old="OUT = R/'validation/artifacts/axial-material-new-native-rank1-cache336-driver-complete70-build-only-20261014-v1'\n",new="OUT = R/'validation/artifacts/axial-material-new-native-rank1-cache336-driver-complete70-build-only-20261014-v2'\n"),dict(old=old_block,new=new_block)]
body=raw.decode()
for b in blocks:assert body.count(b['old'])==1;body=body.replace(b['old'],b['new'])
rec=body
for b in reversed(blocks):assert rec.count(b['new'])==1;rec=rec.replace(b['new'],b['old'])
assert rec.encode()==raw;ast.parse(body)
plan,oldplan=read(OLD/'EXACT_COMPACT70_TO_CACHE336_DRIVER_BUILD_PLAN.json');newplan=copy.deepcopy(plan)
old_hf,old_hf_pin=read(OLD/'COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_FREEZE.json')
old_cli,old_cli_pin=read(OLD/'ROOT_REVIEWABLE_EXACT_CACHE336_DRIVER_BUILD_ARGV.json')
failed,pfailed=read('/Users/wen/spot/validation/artifacts/axial-material-new-native-rank1-cache336-driver-complete70-build-only-20261014-v1/Root_actual_build_only_summary.json')
tool,ptool=read(R/'ROOT_ACTUAL_CACHE336_DRIVER_BUILD_V1_FAILURE_TRUE_TOOL_RETURNS_20261014.json')
post,ppost=read(R/'independent_cache336_driver_v1_compile_inventory_failure_postverify_20261014/REVIEW.json')
posttool,pposttool=read(R/'independent_cache336_driver_v1_compile_inventory_failure_postverify_20261014/TRUE_TOOL_RETURNS.json')
terminal=tool['actual_build_return'];proof=posttool['actual_review_return']
assert type(terminal['exit_code'])is int and terminal['exit_code']==1 and terminal.get('session_id')is None and tool['observed_closed']is True
assert type(proof['exit_code'])is int and proof['exit_code']==0 and proof.get('session_id')is None and posttool['observed_closed']is True and json.loads(proof['output'].strip().splitlines()[-1])['review_pin']==ppost
assert post['failure']is None and post['actual_report_pin']==pfailed and post['actual_Root_true_tool_return_pin']==ptool and post['actual_compiler_integer_returncode']==0 and post['link_started']is False
assert len(failed['records'])==1 and len(failed['output_pins'])==6 and failed['Dragon_linked']is False and failed['actual_host_Source_freeze_pin']==old_hf_pin
for p in old_hf['dependencies']+failed['fixed_current_pins']+failed['output_pins']:
    s=Path(p['path']).lstat();assert stat.S_ISREG(s.st_mode)and ids(s)==p['identity']
newout='/Users/wen/spot/validation/artifacts/axial-material-new-native-rank1-cache336-driver-complete70-build-only-20261014-v2';assert not Path(newout).exists()
OUT.mkdir();host=put('build_native_rank1_cache336_driver_runtime.py',body)
inverse=put('COMPLETE_CACHE336_DRIVER_BUILD_HOST_V1_TO_V2_BYTE_INVERSE.json',dict(schema='CACHE336_DRIVER_BUILD_HOST_V1_TO_V2_EXACT_TWO_BLOCK_INVERSE_V1',source_only=True,original_host_pin=original,candidate_host_pin=host,blocks=blocks,whole_original_recovery=True,all_remaining_Host_math_guard_FirstFailure_bytes_unchanged=True,compiler_executed=False,numerical_executed=False))
newplan.update(planned_output_root=newout,Source_Host_pin=host,Source_inverse_pin=inverse,preparer_pin=pin(Path(__file__).absolute())[0])
oldvalues={k:plan[k]for k in ('planned_output_root','Source_Host_pin','Source_inverse_pin','preparer_pin')}
restored=copy.deepcopy(newplan);restored.update(oldvalues);assert restored==plan
planpin=put('EXACT_COMPACT70_TO_CACHE336_DRIVER_BUILD_PLAN.json',newplan)
planinv=put('COMPLETE_CACHE336_DRIVER_PLAN_V1_TO_V2_CANONICAL_DATA_INVERSE.json',dict(schema='CACHE336_DRIVER_PLAN_V1_TO_V2_EXACT_FOUR_FIELDS_INVERSE_V1',original_plan_pin=oldplan,candidate_plan_pin=planpin,exact_changed_fields=list(oldvalues),old_exact_values=oldvalues,new_exact_values={k:newplan[k]for k in oldvalues},whole_canonical_data_inverse_restores_original=True,old_original70_core9_archives_caps_and_source_pins_unchanged=True))
failurepins=dict(old_v1_Host_freeze_pin=old_hf_pin,old_v1_CLI_pin=old_cli_pin,old_v1_failed_report_pin=pfailed,old_v1_Root_true_tool_pin=ptool,independent_v1_failure_postreview_pin=ppost,independent_v1_failure_posttools_pin=pposttool,old_v1_Host_Source_pin=original,old_v1_PLAN_pin=oldplan)
failureplan=put('EXACT_OLD_DRIVER_V1_FAILED_SCENE_KEEP_SOURCE_PLAN.json',dict(schema='EXACT_OLD_DRIVER_V1_COMPILE_INVENTORY_FAILURE_SCENE_KEEP_SOURCE_PLAN_V1',source_only=True,evidence_pins=failurepins,old_Host_dependencies=old_hf['dependencies'],old_actual_fixed_pins=failed['fixed_current_pins'],old_actual_output_pins=failed['output_pins']+[pfailed],old_first_successful_compiler_not_new_complete_build_qualification=True,old_scene_not_deleted_or_rewritten=True,future_actual_v2_report_pin=None,compiler_executed=False,numerical_executed=False,deletion_executed=False))
ready=put('SOURCE_ONLY_READY.json',dict(status='READY_FOR_INDEPENDENT_DRIVER_BUILD_HOST_V2_SOURCE_REVIEW',failure=None,source_only=True,compiler_executed=False,numerical_executed=False,Host_pin=host,plan_pin=planpin,whole_byte_inverse_pin=inverse,plan_inverse_pin=planinv,failed_scene_keep_plan_pin=failureplan,preparer_pin=pin(Path(__file__).absolute())[0],final_Host_freeze_pin=None,actual_new_build_report_pin=None))
for p,b in seen.values():assert ids(Path(p['path']).lstat())==p['identity']
print(json.dumps(dict(status='SOURCE_ONLY_DRIVER_BUILD_HOST_V2_TWO_BLOCK_PACKAGE_CLOSED0',Host_pin=host,plan_pin=planpin,inverse_pin=inverse,ready_pin=ready,failed_scene_keep_plan_pin=failureplan,compiler_executed=False,numerical_executed=False,deletion_executed=False),ensure_ascii=False))
