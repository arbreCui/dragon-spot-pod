"""Independent finite stdlib SOURCE/AST/hash review; never execute reviewed writer/reviewers."""
from pathlib import Path
import ast
import hashlib
import json
import stat

PACKAGE=Path('/private/tmp/axmat_v21_complete_build_postclose_META_SOURCE_design_20261010_zfmkxh40')
OUT=Path(__file__).parent
MANIFEST_SHA='d9d1dd0c81ed2683c8f5adcb7bc4f7e47748e4dac00e7550e771ee4e225aae5b'
WRITER_SHA='7cbe4b7e2dfee381cf6b60fd720c38d1f4a38119d8b48506a3d330a1789ec6e9'
checks=[]

def check(name,value):
    if type(value)is not bool or not value:raise ValueError(name)
    checks.append(dict(name=name,value=True))

def pin_source(path):
    for component in [*reversed(path.parents),path]:
        check('no SOURCE alias '+str(component),not stat.S_ISLNK(component.lstat().st_mode))
    s=path.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    check('bounded ordinary singlelink SOURCE '+path.name,stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_size<=2*2**20)
    with path.open('rb')as f:
        raw=f.read();check('full SOURCE EOF '+path.name,f.read(1)==b'')
    t=path.lstat();after=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
    check('SOURCE stable seven-part identity '+path.name,before==after and len(raw)==before[4])
    return raw,dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),identity=before)

manifest_raw,manifest_pin=pin_source(PACKAGE/'sealed_manifest.json')
check('given complete manifest SHA exact',manifest_pin['sha256']==MANIFEST_SHA)
manifest=json.loads(manifest_raw)
check('whole ten-member inventory plus manifest',manifest['member_count']==10 and len(manifest['members'])==10 and sorted(p.name for p in PACKAGE.iterdir())==sorted([*manifest['members'],'sealed_manifest.json']))
raws={};pins={};trees={};small_meta={}
for name,expected in manifest['members'].items():
    raw,pin=pin_source(PACKAGE/name)
    check('complete SOURCE member SHA/exact7ID '+name,pin==expected)
    check('member frozen readonly '+name,pin['identity'][2]&0o222==0)
    raws[name]=raw;pins[name]=pin
    if name.endswith('.py'):
        trees[name]=ast.parse(raw,filename=name)
        check('full Python SOURCE AST parsed '+name,isinstance(trees[name],ast.Module))
    elif name.endswith('.json'):
        small_meta[name]=json.loads(raw)
        check('complete bounded META decoded '+name,type(small_meta[name])is dict)
check('exact failure-only SOURCE SHA',pins['write_actual_failed_build_postclose_META.py']['sha256']==WRITER_SHA)
check('seal failure-only and general-reference scope honest',manifest['failure_only_writer']=='write_actual_failed_build_postclose_META.py'and manifest['failure_only_writer_sha256']==WRITER_SHA and manifest['successful_general_writer_only_unexecuted_Source_reference']is True)

ftext=raws['write_actual_failed_build_postclose_META.py'].decode()
gtree=trees['write_actual_build_postclose_META.py'];ftree=trees['write_actual_failed_build_postclose_META.py']
fdefs={n.name:n for n in ftree.body if isinstance(n,ast.FunctionDef)}
gdefs={n.name:n for n in gtree.body if isinstance(n,ast.FunctionDef)}
end=gdefs['finite_number'].lineno-1
common=b''.join(raws['write_actual_build_postclose_META.py'].splitlines(keepends=True)[:end])
check('whole common pin/inventory/terminal/SOURCE-freeze prefix byte exact',raws['write_actual_failed_build_postclose_META.py'].startswith(common))
check('failure-only excludes all success contract entrypoints',not {'success_checks','expected_commands','watch_ok','finite_number'}&set(fdefs))
imports=[]
for n in ast.walk(ftree):
    if isinstance(n,ast.Import):imports.extend(v.name for v in n.names)
    if isinstance(n,ast.ImportFrom):imports.append(n.module)
    if isinstance(n,ast.Call)and isinstance(n.func,ast.Name):
        check('no dynamic execution builtin at line '+str(n.lineno),n.func.id not in {'eval','exec','compile','__import__'})
    if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute):
        check('no business/process/cleanup API at line '+str(n.lineno),n.func.attr not in {'unlink','rmdir','remove','rmtree','rename','Popen','run','execute','exec_module','setprofile','sleep'})
        if n.func.attr=='replace':check('replace only argument key spelling',isinstance(n.func.value,ast.Name)and n.func.value.id=='key')
check('failure-only standard library imports',set(imports)<={'argparse','ast','hashlib','json','math','os','pathlib','stat','time'})
globals_ast={n.targets[0].id:n.value for n in ftree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
check('complete original five labels unchanged',ast.literal_eval(globals_ast['LABELS'])==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit'])
caps_assignment=next(n for n in ftree.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='WHOLE' for target in n.targets for x in ast.walk(target)))
expected_caps=ast.parse('(1800,600,512,2*2**30,96*2**30,8*2**30)',mode='eval').body
check('all original wall/RSS/archive/history/free caps exact AST',ast.dump(caps_assignment.value,include_attributes=False)==ast.dump(expected_caps,include_attributes=False))
check('all native/wholeINPUT/AAA/ABA/scientific false fields kept',ast.literal_eval(globals_ast['FALSE_FIELDS'])==('whole_combined_INPUT_admitted','production_admission_API_executed','new_native_transport_executed','native_RSS_qualified','combined_runtime_native_RSS_proved','mathematical_controls_newly_executed','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted','physics_qualified','goal_complete'))
main_text=ast.get_source_segment(ftext,fdefs['main'])
check('EXIT0 rejection before any copy or receipt write',main_text.index("if terminal['exit_code']==0:")<main_text.index('copy_exact(paths[key]')<main_text.index('write_new(receipt,proof)'))
check('no success receipt construction',"receipt=T/'terminal_return.json'"not in ftext and "receipt=T/'failed_build_terminal_return.json'"in ftext and 'successful_new_runtime_build_observed=True'not in ftext and 'all_five_original_stages_passed=True'not in ftext)
check('all write opens exclusive/no overwrite',"Path(p).open('x')"in ftext and "Path(dst).open('xb')"in ftext and not any(isinstance(n,ast.Constant)and type(n.value)is str and n.value in ('w','wb','a','ab','r+')for n in ast.walk(ftree)))

anchors={
 'strict real Root integer CLOSED':"type(terminal.get('exit_code')) is not int or 'session_id' in terminal",
 'closed original observations required':"record.get('closed') is not True or record.get('observed_after_actual_terminal_return') is not True",
 'closed session not repolled':"record.get('session_repolled_after_close') is not False",
 'immutable all-source file set':"set(view['files'])!=set(freeze['complete_files'])",
 'immutable all-source directory identity dict':"view['directories']!=freeze['complete_directories']",
 'SOURCE no append':"freeze['no_SOURCE_append_after_freeze'] is not True",
 'dynamic Source count':"freeze['actual_complete_SOURCE_file_count']!=len(view['files'])",
 'ordered all fixed input pins incl repeats':"for index,q in enumerate(fixed)",
 'root preflight fixed pins rather than declared PREP list':"fixed=preflight['fixed_input_pins']",
 'original S/T complete set':"set(now['files'])!=set(original['files'])",
 'original prepared S/T all file pins':"for key,p in original['files'].items():",
 'original PREP O4':"expected_o4=('declaration.json','input_graph.json','input_creation_python_open_trace.json','runtime/run_bounded_dragon.py')",
 'full namespaces H/S/O/T/D':"ROOTS = (H,S,O,T,D)",
 'all current H/S/O/T/D/E':"for root in (*ROOTS,E)",
 'full stream copying without clipping':"while True:\n            chunk=source.read(1024*1024)",
 'parent stdout copy':"('parent-stdout','actual_build_external_host_stdout.json')",
 'parent stderr copy':"('parent-stderr','actual_build_external_host_stderr.txt')",
 'original child merged stream':"copies['actual-child-merged']=copy_exact(merged,T/'actual_build_child_merged_stdout_stderr.json')",
 'child stream scope honest':"full_stdout_scope='ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR'",
 'external host stderr scope honest':"full_stderr_scope='ACTUAL_EXTERNAL_ROOT_HOST_STDERR'",
 'child stderr never invented':"separate_child_stderr_captured=False,independent_child_stderr_empty_verified=False",
 'stage dynamically from actual table':"actual_stages=observed.get('inner_stage_table',{}).get('stages',[])",
 'dynamic stage prefix':"actual_prefix=observed_labels==LABELS[:len(observed_labels)]",
 'dynamic real PASS labels':"pass_labels=[stage.get('label') for stage in actual_stages if stage.get('status')=='PASS']",
 'all existing stage logs and watchdogs referenced':"raw=O/(stage['label']+'.log');watch=raw.with_suffix('.watchdog.json')",
 'missing successful closeout is observation':"actual_success_closeout_files_absent=absent_success",
 'host final input never granted':"original_host_final_input_revalidation_observed=False",
 'Root postclose pins never replace host final PASS':"Root_postclose_pin_checks_do_not_replace_unreached_host_input_finalpass=True",
 'full physical declared input PASS never granted':"full_declared_physical_input_finalpass_claimed=False",
 'all original namespaces stable across capture':"if root!=T and views[index]!=before[index]",
 'all original T entries unchanged':"new_t['files'].get(key)!=p for key,p in old_t['files'].items()",
 'all fixed successful pins checked again':"for value in unchanged:\n        exact_pin(value['pin'])",
 'original SOURCE checked again':"if source_ok: compare_source_freeze(freeze)",
 'current joint bytes include H/S/O/T/D/E plus factory/writer':"namespace_bytes([snapshot(root,missing_allowed=True) for root in (*ROOTS,E)])+FACTORY.stat().st_size+writer_pin['identity'][4]",
 'metadata reserve within original2GiB':"namespace_bytes(current)+reserve+FACTORY.stat().st_size+writer_pin['identity'][4]>=ARCHIVE",
 'E snapshot timing scope explicit':"E_root_complete_snapshot_before_this_manifest_and_summary=True",
 'E directory stability not falsely asserted':"E_root_directory_full7stable_after_metadata_append_required=False",
 'threads/child/retries unchanged':"threads=1,children_at_once=1,retries=0",
}
for name,fragment in anchors.items():check('full failure-META SOURCE obligation: '+name,fragment in ftext)

usage=raws['ROOT_NEXT_STEPS.txt'].decode()
for argument in ('writer-sha256','root-terminal','root-terminal-sha256','source-freeze','source-freeze-sha256','prelaunch-pins','prelaunch-pins-sha256','parent-stdout','parent-stdout-sha256','parent-stderr','parent-stderr-sha256'):
    check('ROOT_NEXT_STEPS supplies required argv '+argument,'--'+argument+' 'in usage)
for sha in (WRITER_SHA,'38815705e9e27c62e423dd4501ff41308d6ec1c219ea8ab9c264a27807420791','0825b81036f1f7ad71a41444e4a87384a518f7d8ed7e9e38ee659f916e42909b','a9024656df7debc840a8f5f1394bae05ba31360c542e5a8b9d2da3d749164b42'):
    check('ROOT_NEXT_STEPS true supplied Source/META SHA '+sha,sha in usage)
check('usage supplies real stdout/stderr placeholders and no invented child stderr','<actual_root_parent_stdout_full_EOF_SHA>'in usage and '<actual_root_parent_stderr_full_EOF_SHA>'in usage and '不得造空文件或子进程独立 stderr'in usage)
actual_tools=small_meta['actual_SOURCE_design_tool_returns.json']
final_review=[r['actual']for r in actual_tools['records']if r['actual'].get('chunk_id')=='d70d63']
check('original final failure Source self-review typed EXIT0 CLOSED captured',len(final_review)==1 and type(final_review[0].get('exit_code'))is int and final_review[0]['exit_code']==0 and 'session_id'not in final_review[0])
check('captured Source self-review binds same final failure writer SHA',json.loads(final_review[0]['output'])['writer_sha256']==WRITER_SHA)
check('author Source tool returns declare all writers unexecuted',actual_tools['all_writer_scripts_unexecuted']is True)
for name,pin in pins.items():
    _,after=pin_source(PACKAGE/name);check('final unchanged original Source '+name,after==pin)
_,after_manifest=pin_source(PACKAGE/'sealed_manifest.json')
check('final unchanged complete original manifest',after_manifest==manifest_pin)

report=dict(schema='INDEPENDENT_V21_FAILED_BUILD_POSTCLOSE_META_SOURCE_PEER_REVIEW_V1',
 status='SOURCE_ONLY_REVIEW_COMPLETE_NO_WRITER_EXECUTION_OR_ACTUAL_BUILD_ADMISSION',
 manifest_pin=manifest_pin,member_pins=pins,read_complete10members_plus_manifest=True,
 all_four_Python_SOURCE_complete_AST_parsed=True,common_prefix_byte_exact=True,all_checks=checks,
 source_blockers_for_Root_actual_failure_META_save=[],ROOT_NEXT_STEPS_argv_complete=True,
 actual_fixed62_and_PREP67_scope_not_conflated=True,
 Root_announced_actual_run_not_independently_read=dict(terminal_chunk='875da7',exit_code=1,closed=True,root_terminal_sha='38815705e9e27c62e423dd4501ff41308d6ec1c219ea8ab9c264a27807420791',canonical_seconds=170.787905792,peak_RSS_MiB=514.203125,child_returncode=-15,cleanup=True,stage_PASS_count=2,stages_total=5,postclose_check_chunk='a0f7fd'),
 original_Source_selfreview_d70d63_closed_int0_from_saved_package=True,
 original_Source_seal_e581c6_closed_int0='Root-reported; the sealing tool return itself is not a member of this manifest; no contrary Source evidence',
 writer_or_reviewed_reviewer_imported_executed_or_compiled=False,project_API_guard_business_or_numeric_executed=False,
 live_or_closed_actual_ART_or_material_payload_read=False,old_sessions_polled=False,
 existing_Source_package_project_DE_canonical_changed=False,
 actual_failure_META_writer_execution_success=None,whole_INPUT_native_AAA_ABA_science_success=None,
 limitations=[
  'This review checks the entire finite Source design only. Root actual run metrics, thirty frozen files/three directory identities, sixty-two fixed pins and original S11/T6/O4 correctness remain Root actual saved-evidence observations.',
  'Only the failure-only writer is admissible for the reported int1 build; the general success writer stays an unexecuted Source reference.',
  'The dedicated writer can only construct failed_build_terminal_return, copies and failure manifest/summary. It cannot construct successful seal/driver/audit/rawreceipt or T/terminal_return.',
  'ROOT_NEXT_STEPS argv still needs Root true complete EOF SHA values for both real parent stream files. The child original merged stream is a third preserved scope and no independent child stderr is invented.',
  'Stage observations are dynamic saved metadata; they never establish all five stages PASS or replace the unreached original host final input revalidation.',
  'All SOURCE/D original bytes and directory pins must be checked without append. E manifest/summary/actual later META-tool receipts append after an explicitly bounded snapshot, so final E root identity stability is not claimed.',
  'Root retains actual metadata-writer terminal and partial metadata on failure; this Source review grants no runtime success or retry authorization.',
 ])
with(OUT/'SOURCE_PEER_REVIEW.json').open('x')as stream:json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n')
print(json.dumps(dict(status=report['status'],report=str(OUT/'SOURCE_PEER_REVIEW.json'),static_checks=len(checks),manifest_sha256=manifest_pin['sha256'],writer_sha256=WRITER_SHA,members=10,source_blockers=[],reviewed_code_executed=False,actual_ART_read=False)))
