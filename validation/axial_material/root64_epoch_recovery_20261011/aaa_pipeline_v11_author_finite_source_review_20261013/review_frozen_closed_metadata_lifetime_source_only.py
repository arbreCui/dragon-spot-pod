"""Finite read-only Source review. No candidate imports or business execution."""
import ast, collections, hashlib, json, os, resource, stat, time
from pathlib import Path
R = Path('/Users/wen/spot')
REC = R/'validation/axial_material/root64_epoch_recovery_20261011'
OLD = REC/'aaa_three_plane_streaming_pipeline_source_v10'
NEW = REC/'aaa_three_plane_streaming_pipeline_source_v11'
OUT = Path(__file__).resolve().parent
COMPILER = Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')
START = time.monotonic()
checks=[]; hashed={}
def need(ok,name):
    if not ok: raise RuntimeError(name)
    checks.append(name)
def identity(p):
    s=Path(p).lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p); before=identity(p)
    need(stat.S_ISREG(before[2]) and not any(x.is_symlink() for x in (p,*p.parents)), 'literal regular no-alias:'+str(p))
    need(before[3]==1 or (p==COMPILER and before[3]==2), 'exact immutable compiler only nlink2:'+str(p))
    with p.open('rb') as f:
        need(identity(p)==before, 'pre-open path7 unchanged:'+str(p))
        s=os.fstat(f.fileno());need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before,'opened7:'+str(p))
        sha=hashlib.file_digest(f,'sha256').hexdigest();s=os.fstat(f.fileno())
        need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before==identity(p),'wholeEOF all7 unchanged:'+str(p))
    result=dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
    need(str(p) not in hashed or hashed[str(p)]==result,'same immutable PF:'+str(p));hashed[str(p)]=result
    return result
def verify(p):need(pin(p['path'])==p,'exact all fields:'+p['path'])
def write(path,v):
    raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
    with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())

oldhf=json.loads((OLD/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json').read_text())
hf=json.loads((NEW/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json').read_text())
oldcli=json.loads((REC/'ROOT_EXACT_ACTUAL_PIPELINE_V10_ARGV_20261013.json').read_text())
cli=json.loads((REC/'ROOT_EXACT_ACTUAL_PIPELINE_V11_ARGV_20261013.json').read_text())
need(len(oldhf['dependencies'])==278 and len(hf['dependencies'])==308,'complete old278/new308 dependency rows')
for p in oldhf['dependencies']+[oldhf['host_source']]+hf['dependencies']+[hf['host_source']]+list(cli['mandatory_external_bindings'].values()):verify(p)
hfp=pin(NEW/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json');clip=pin(REC/'ROOT_EXACT_ACTUAL_PIPELINE_V11_ARGV_20261013.json')
verify(hf['predecessor_host_freeze'])
need(hfp==cli['mandatory_external_bindings']['host-freeze'],'CLI exact frozen HF SHA and all7')
need(hf['schema']=='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V11','exact v11 schema')
need(hf['host_source']==pin(NEW/'run_actual_three_plane_pipeline.py'),'complete actual new host full PF')
deps={p['path']:p for p in hf['dependencies']}
need(len(deps)==308,'unique exact full dependency paths')
derived=[]
for p in oldhf['dependencies']:
    oldpath=Path(p['path']);newpath=NEW/oldpath.relative_to(OLD) if oldpath.is_relative_to(OLD) else oldpath
    need(str(newpath) in deps, 'original dependency mapped with no omission:'+str(oldpath))
    newpin=deps[str(newpath)];derived.append(newpin)
    if oldpath.is_relative_to(OLD) and oldpath.name in ('DIRECT_ALIAS_ENTRY_BINDING.json','DECLARED_EXECUTION_INTERFACE.json'):
        olddata=json.loads(oldpath.read_text());newdata=json.loads(newpath.read_text())
        if oldpath.name=='DIRECT_ALIAS_ENTRY_BINDING.json':
            olddata['new_probe_source']=str(NEW/'direct_alias_entry_controls.f90')
        else:
            olddata.update(schema='DECLARED_ACTUAL_AAA3_STREAMING_ONE_SERIAL_50_STAGE_INTERFACE_V11',host_source=str(NEW/'run_actual_three_plane_pipeline.py'),
                           output_root=str(R/'validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v11'),
                           closed_admission_metadata_lifetime_only=True,original_raw_execution_records_and_resource_snapshots_unchanged=True,
                           readonly_memory_fixture_is_not_actual_50_stage_qualification=True)
        need(newdata==olddata,'exact only mandated namespace/interface metadata changes:'+oldpath.name)
    elif oldpath.is_relative_to(OLD):
        need(oldpath.read_bytes()==newpath.read_bytes(),'whole copied helper/proof bytes:'+str(oldpath))
    else:need(newpin==p,'all external complete PF values byte-identical:'+p['path'])
need(hf['complete_original_v10_dependency_rows_derived']==278,'declared exact derivation matches real original count')
need(not any(Path(p).name in ('projected_boot.xsm','negative_project.xsm') for p in deps),'no old PROJECT or clone pinned')
compilerpin=next(p for p in oldhf['dependencies'] if p['path']==str(COMPILER))
need([p for p in hf['dependencies'] if p['identity'][3]!=1]==[compilerpin],'unique compiler exact old immutable nlink2 role')
inverse=json.loads(Path(hf['complete_V10_to_V11_byte_inverse_pin']['path']).read_text())
verify(hf['complete_V10_to_V11_byte_inverse_pin']);verify(hf['finite_closed_metadata_lifetime_and_command_equivalence_source_review_pin'])
original=(OLD/'run_actual_three_plane_pipeline.py').read_bytes();candidate=(NEW/'run_actual_three_plane_pipeline.py').read_bytes()
need(inverse['old_host_source_pin']==oldhf['host_source'] and inverse['new_host_source_pin']==hf['host_source'],'inverse binds exact old/new Source PF')
restored=candidate.decode();changes=inverse['exact_ordered_changes'];need(len(changes)==9,'only exact nine authorized Source blocks')
expected_labels=['fresh_output_namespace','exact_host_freeze_schema','import_standard_cyclic_gc','close_metadata_only_after_complete_fixed_EOF',
                 'use_previously_cached_exact_executable_pin','use_previously_cached_original_bounded_SHA',
                 'direct_compile_uses_exact_cached_compiler_and_includes','mutator_compile_uses_exact_cached_compiler_and_includes','mutator_link_uses_exact_cached_archive_order']
need([d['label'] for d in changes]==expected_labels,'exact allowed delta order')
for d in reversed(changes):
    need(d['count']==1 and restored.count(d['new_block'])==1,'one precise new delta:'+d['label'])
    restored=restored.replace(d['new_block'],d['old_block'],1)
need(restored.encode()==original,'ENTIRE original Source byte inverse exact, no other mutation')
oldtree=ast.parse(original);tree=ast.parse(candidate)
main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
oldmain=next(n for n in oldtree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
deletes=[n for n in main.body if isinstance(n,ast.Delete)]
deleted=[n.id for d in deletes for n in d.targets]
need(deleted==inverse['exact_deleted_names'] and len(deletes)==2,'exact declared deleted metadata names and two statements')
enddel=deletes[-1].lineno
for name in deleted:
    if name!='row':need(not any(isinstance(n,ast.Name)and n.id==name and isinstance(n.ctx,ast.Load)and n.lineno>enddel for n in ast.walk(main)), 'no future deleted name load:'+name)
def scope_nodes(n):
    if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.Lambda,ast.ListComp,ast.SetComp,ast.DictComp,ast.GeneratorExp)):return
    yield n
    for child in ast.iter_child_nodes(n):yield from scope_nodes(child)
row_future=sorted((n.lineno,isinstance(n.ctx,ast.Store)) for stmt in main.body for n in scope_nodes(stmt) if isinstance(n,ast.Name)and n.id=='row'and n.lineno>enddel)
need(row_future and row_future[0][1],'later main producer row explicitly reassigned; function/comprehension scopes independent')
def main_assignment(t,name):
    m=next(n for n in t.body if isinstance(n,ast.FunctionDef)and n.name=='main')
    return [n for n in m.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id==name for x in n.targets)]
need(ast.dump(main_assignment(oldtree,'fixed')[-1],include_attributes=False)==ast.dump(main_assignment(tree,'fixed')[-1],include_attributes=False),'ENTIRE fixed PF admission expression and order unchanged')
fixed_line=main_assignment(tree,'fixed')[-1].lineno
verifies=[n.lineno for n in ast.walk(main) if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)and n.func.value.id=='c'and n.func.attr=='verify_rows'and len(n.args)==1 and isinstance(n.args[0],ast.Name)and n.args[0].id=='fixed']
need(fixed_line<min(verifies)<deletes[0].lineno,'existing full fixed EOF verification precedes metadata deletion')
gcalls=[n for n in ast.walk(main)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)and n.func.value.id=='gc']
need(len(gcalls)==1 and gcalls[0].func.attr=='collect'and not gcalls[0].args and gcalls[0].lineno>enddel,'exact one standard GC after complete closed admission')
runner_assign=main_assignment(tree,'runner')[0]
need(gcalls[0].lineno<runner_assign.lineno,'GC completes before genuine original supervisor and first business stage')
for retained in ('link_command','direct_original_inputs','plan','fixed','hf'):
    need(retained not in deleted,'necessary future authority retained:'+retained)
olddefs={n.name:n for n in oldtree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name!='main'}
newdefs={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name!='main'}
need(set(olddefs)==set(newdefs),'all other original functions and classes retained')
for name in olddefs:need(ast.dump(olddefs[name],include_attributes=False)==ast.dump(newdefs[name],include_attributes=False),'complete other definition AST unchanged:'+name)
oldtext=original.decode();text=candidate.decode()
need(oldtext[oldtext.index('    def stable():'):oldtext.index('    def retain(')]==text[text.index('    def stable():'):text.index('    def retain(')],'stable fullPF/SELF/resources/whole1800 guard exact bytes')
need(oldtext[oldtext.index('    # Complete unmodified original execution records'):]==text[text.index('    # Complete unmodified original execution records'):],'all complete raw/compact publication source bytes identical')
for helper in ('actual_inputs_and_readback.py','mutate_owned_control.f90','direct_alias_entry_controls.f90'):
    need((OLD/helper).read_bytes()==(NEW/helper).read_bytes(),'ENTIRE scientific/reader/Fortran helper unchanged:'+helper)
oldargv=oldcli['argv'];expected=list(oldargv);expected[expected.index(str(OLD/'run_actual_three_plane_pipeline.py'))]=str(NEW/'run_actual_three_plane_pipeline.py')
for suffix,v in (('summary',hfp['path']),('sha256',hfp['sha256']),('seven-id',json.dumps(hfp['identity'],separators=(',',':')))):
    expected[expected.index('--host-freeze-'+suffix)+1]=v
need(cli['argv']==expected,'ENTIRE executable argv changes only source path and actual host-freeze 3 flags')
for k,v in oldcli['mandatory_external_bindings'].items():
    if k!='host-freeze':need(cli['mandatory_external_bindings'][k]==v,'all genuine actual external three-producer/build70/17/Fortran PF unchanged:'+k)
buildpin=cli['mandatory_external_bindings']['build70'];build=json.loads(Path(buildpin['path']).read_text());cached=inverse['actual_cached_command_authority']
need(cached['actual_closed_build70_pin']==buildpin,'cache provenance actual build70 binding exact')
need(cached['exact_compiler']==build['records'][0]['command'][0]==str(COMPILER),'actual exact compiler unchanged')
need(cached['exact_ordered_includes']==[x for x in build['records'][0]['command']if x.startswith('-I')],'actual entire include argument order unchanged')
need(cached['exact_ordered_archives']==[x for x in build['records'][-1]['command']if x.endswith('.a')],'actual entire archive argument order unchanged')
need(cached['exact_runtime_executable_pin']==next(x for x in build['output_pins']if Path(x['path']).name=='Dragon'),'exe shallow exact PF authority unchanged')
need(cached['original_full_compile_command']==build['records'][0]['command']and cached['original_full_ordered70_link_command']==build['records'][-1]['command'],'all actual original complete command values unchanged')
verify(cached['exact_runtime_executable_pin'])
for p in build['original_current69_ordered_input_pins']:verify(p)
need(len(build['actual_complete70_link_inputs'])==70 and len(set(build['actual_complete70_link_inputs']))==70 and build['replacement_zero_based_current69_input_index']==37,'actual native current70 unique order and driver37 unchanged')
interface=json.loads((NEW/'DECLARED_EXECUTION_INTERFACE.json').read_text())
need(not Path(interface['output_root']).exists()and not Path(interface['output_root']).is_symlink(),'new actual v11 output namespace still absent')
cause=json.loads(Path(hf['actual_closed_v10_original_SELF_failure_cause_pin']['path']).read_text())
need(cause['actual_parent_peak_bytes']==541753344 and cause['original_parent_cap_bytes']==536870912 and cause['engineering_three_plane_closed0']is False,'real original cap failure preserved; no inferred qualification')
actual=json.loads(Path(cause['actual_summary_pin']['path']).read_text())
rawpin=next(p for p in hf['dependencies']if Path(p['path']).name=='Root_actual_complete_execution_record_before_final_publication.json')
raw=json.loads(Path(rawpin['path']).read_text())
stagespin=next(p for p in hf['dependencies']if p['path'].endswith('/v10/AAA3-streaming/stages.json')) if any(p['path'].endswith('/v10/AAA3-streaming/stages.json')for p in hf['dependencies'])else next(p for p in hf['dependencies']if '-20261012-v10/AAA3-streaming/stages.json'in p['path'])
stage_container=json.loads(Path(stagespin['path']).read_text())
need(set(stage_container)=={'stages'},'original genuine SerialExecutor ledger container shape')
stage_raw=stage_container['stages']
need(len(raw['records'])==len(stage_raw)==len(actual['records'])==46,'actual failed v10 full46 stage evidence retained')
need(raw['records']==stage_raw,'ENTIRE v10 saved unmodified resource_before/after/raw stage values identical')
need(raw['engineering_three_plane_closed0']is False and actual['engineering_three_plane_closed0']is False,'full failed v10 evidence never promoted to successful runtime authority')
preparepin=pin(OUT/'TRUE_PREPARE_TOOL_RETURN.json');prepare=json.loads(Path(preparepin['path']).read_text())
need(prepare['actual_prepare']['exit_code']==0 and prepare['actual_prepare']['chunk_id']=='48f966','real Source-only preparation tool return retained')
report=dict(schema='PIPELINE_V11_AUTHOR_COMPLETE_POSTFREEZE_FINITE_SOURCE_ONLY_REVIEW_V1',
            status='SOURCE_ONLY_COMPLETE_BYTE_INVERSE_NAME_LIVENESS_REAL_COMMAND_ORDER_AND_FULL_PF_REVIEW_PASS',
            host_freeze_pin=hfp,CLI_pin=clip,complete_inverse_pin=hf['complete_V10_to_V11_byte_inverse_pin'],
            successful_checks=len(checks),unique_fullEOF_files=len(hashed),unique_fullEOF_bytes=sum(x['size_bytes']for x in hashed.values()),
            complete_original_v10_278_dependencies_derived=True,current_dependencies=308,all_external_actual_binding_PFs_unchanged=True,
            exact_nine_authorized_blocks_only=True,whole_v10_host_byte_inverse_equal=True,
            deleted_metadata_names=deleted,necessary_authority_names_retained=['link_command','direct_original_inputs','plan','fixed','hf'],
            all_deleted_metadata_names_have_no_later_load=True,final_main_row_reassigned_before_later_load=True,
            original_full_admission_and_entire_fixed_PF_expression_and_EOF_before_deletion=True,
            actual_compiler_includes_archives_exe_command_order_all_exact=True,
            original_unique_compiler_immutable_nlink2_role_pin=compilerpin,
            full_stable_guard_and_all_raw_record_resource_snapshot_and_final_publication_bytes_unchanged=True,
            all_original50_17positive_33strictnegative_oracles_6DELETE_BOOT_math_native70_and_caps_unchanged=True,
            all_three_complete_helpers_unchanged=True,Common_original_class_MRO_and_all_immutable_original_files_unchanged=True,
            explicit_gc_count=1,gc_only_after_closed_admission_before_first_stage=True,
            actual_v10_failed_full46_raw_and_compact_records_pinned_and_not_promoted=True,
            actual_prepare_true_tool_return_pin=preparepin,reader_measurement_pin=hf['readonly_production_scope_bounded_reader_memory_measurement_pin'],
            metadata_measurement_pin=hf['readonly_parent_metadata_memory_measurement_pin'],
            readonly_fixture_and_reader_probes_not_actual_50_stage_proof=True,actual_v11_guarded_business_execution_required=True,
            candidate_imported_or_executed=False,compiler_CLE_or_physics_executed=False,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            wall_seconds=time.monotonic()-START,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
write(OUT/'FINAL_POSTFREEZE_REVIEW.json',report)
print(json.dumps(dict(status=report['status'],report_pin=pin(OUT/'FINAL_POSTFREEZE_REVIEW.json'),successful_checks=len(checks),
                      unique_fullEOF_files=len(hashed),unique_fullEOF_bytes=sum(x['size_bytes']for x in hashed.values()),
                      SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,candidate_or_compiler_or_physics_executed=False),allow_nan=False))
