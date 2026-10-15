"""Bounded source-only inspection. Never imports or executes project modules."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
HERE = Path(__file__).parent
BASE = ROOT / 'validation/axial_material/complete_history_root_index_source_v15_20261010'
HOST = BASE / 'actual_prepare_sources/prepare_cli_host_v15.py'
DRIVER = BASE / 'actual_prepare_sources/prepare_cli_driver_v15.py'
OLD_HOST = ROOT / 'validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/actual_complete_prepare_profile_sources/prepare_profile_host.py'
TARGET = ROOT / 'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_root_index_production_v15.py'
RESOURCE = ROOT / 'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py'
ORIGINAL_RESOURCE = ROOT / 'validation/axial_material/prepare_qualified_AB_moment_order_production.py'
FULL = ROOT / 'validation/axial_material/qualify_refined_AAA_layered_full.py'
PRODUCTION = ART / 'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py'
BOUNDED = PRODUCTION.parent / 'run_bounded_dragon.py'
OLD_HELPER = ROOT / 'validation/axial_material/prepare_qualified_AB_source_factor_production.py'
OLD_RECEIPT = ROOT / 'validation/axial_material/sender_contiguous_flux_window_source_v13_20261009/actual_component_execution_receipts/Root_actual_prepare_tool_return.json'
QUALIFICATION = BASE / 'Root_actual_resource_module_admission.json'
INSTALL = BASE / 'Root_complete_factory_source_only_install_receipt.json'
WANTED = {
    HOST:'3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7',
    DRIVER:'c6984b157ff92b4ec7be9cda54f42e6d1ff0fd4391d25a0a85ab7bb2b2ca9c08',
    TARGET:'cc4b0fda4ab63d11debee532fdfbc399f5f7a68f753e20d1cff928e607a47447',
    RESOURCE:'ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022',
    ORIGINAL_RESOURCE:'fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41',
    FULL:'70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6',
    PRODUCTION:'38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128',
    BOUNDED:'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09',
    OLD_HELPER:'619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743',
    OLD_RECEIPT:'d69437dc3f3df2fc8b36adb7c3077410e6d3052e153d4568ea7e0b52ac856f82',
    QUALIFICATION:'5a0b2c1870ba1f0cced713bb3528fb9c13928aaf436859763c97edb19afd7676',
}

def identity(path):
    s = path.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def read_pin(path,wanted=None):
    before = identity(path)
    assert stat.S_ISREG(before[2]), str(path)
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert identity(path) == before and len(raw) == before[4]
    assert wanted is None or digest == wanted, str(path)
    return raw.decode(),dict(path=str(path),sha256=digest,size_bytes=len(raw),identity=before)

sources = {}; pins = []
for path in list(WANTED) + [OLD_HOST,INSTALL,Path(__file__)]:
    source,pin = read_pin(path,WANTED.get(path));sources[path]=source;pins.append(pin)

checks = {}
def check(name,condition):
    checks[name] = bool(condition)
    assert condition, name

h = sources[HOST]; d = sources[DRIVER]; old = sources[OLD_HOST]
ht = ast.parse(h); dt = ast.parse(d); ot = ast.parse(old)
compile(h,str(HOST),'exec');compile(d,str(DRIVER),'exec')
check('both_entry_sources_parse_and_compile_without_execution',True)
def segments(text,tree):
    return {n.name:ast.get_source_segment(text,n) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
hs,osrc = segments(h,ht),segments(old,ot)
for name in ['identity','pin','write_new','load','archive_bytes']:
    check('original_support_function_byte_exact_'+name,hs[name] == osrc[name])
check('host_resource_constructor_real_new_class_exact_caps_failure_type',
    'resources = resource_factory.DynamicHistoryResources(ART,roots,8*2**30,96*2**30,production.ResourceFailure)' in h
    and 'resource_factory.resources_for' not in h)
rs = segments(sources[RESOURCE],ast.parse(sources[RESOURCE]))
ors = segments(sources[ORIGINAL_RESOURCE],ast.parse(sources[ORIGINAL_RESOURCE]))
check('resource_class_check_init_and_true_object_MRO_source_unchanged',rs['DynamicHistoryResources'] == ors['DynamicHistoryResources'])
check('resource_scope_contract_and_dynamic_full_history_union_unchanged',
    rs['resource_scope_contract'] == ors['resource_scope_contract'] and rs['history_roots'] == ors['history_roots'])
check('new_resource_module_has_history_roots_but_no_resources_for','history_roots' in rs and 'resources_for' not in rs)
check('root_index_formal_actual_resource_qualification_bound',
    WANTED[QUALIFICATION] in h and WANTED[RESOURCE] in h)
q = json.loads(sources[QUALIFICATION]);i = json.loads(sources[INSTALL])
check('actual_resource_only_qualification_and_original_caps',q['status']=='PASS_RESOURCE_MODULE_ONLY'
    and q['qualified_caps']==dict(history_bytes=96*2**30,free_floor_bytes=8*2**30,host_wall_seconds=120,rss_mib=512,archive_bytes=64*2**20,threads=1,children=1,retries=0)
    and q['fresh_complete_history_checks'] is True and q['original_caps_changed'] is False)
check('installed_component_binding_current_exact_source',i['canonical_factory']==dict(path=str(TARGET),sha256=WANTED[TARGET]))
check('original_1800_600_512_2GiB_host_limits',
    'WHOLE_CAP, STAGE_CAP, RSS_CAP = 1800, 600, 512' in h and 'ARCHIVE_CAP = 2 * 2**30' in h)
check('before_run_reserve_history96GiB_free8GiB_and_full_after_scan',
    "before = resources.check()" in h and "after = resources.check()" in h
    and "before['artifact_bytes']+ARCHIVE_CAP >= 96*2**30" in h
    and "before['disk_free_bytes']-ARCHIVE_CAP < 8*2**30" in h)
check('genuine_original_OwnRSS_direct_constructor_MRO_and_runtime_binding',
    'full,production = h.modules()' in h and 'h.guard_admission(full)' in h
    and 'full.OwnRSSSerialExecutor.__bases__ != (production.SerialExecutor,)' in h
    and "runner = full.OwnRSSSerialExecutor(HOST_OUT,remaining,'COMPLETE_PREPARE',resources)" in h
    and 'type(runner) is not full.OwnRSSSerialExecutor' in h and 'runner.resources is not resources' in h
    and "Path(runner.bounded.__file__).resolve() != HOST_OUT/'runtime/run_bounded_dragon.py'" in h)
check('whole_deadline_starts_before_prechecks_and_child_stage600',
    h.index('started = time.monotonic()') < h.index('inputs = [pin(')
    and 'remaining = WHOLE_CAP-(time.monotonic()-started)' in h
    and "runner.execute(HOST_OUT/'run','prepare',command,STAGE_CAP)" in h)
host_execute_calls=[n for n in ast.walk(ht) if isinstance(n,ast.Call) and ast.unparse(n.func)=='runner.execute']
runpy_calls=[n for n in ast.walk(dt) if isinstance(n,ast.Call) and ast.unparse(n.func)=='runpy.run_path']
check('one_child_execute_and_one_canonical_prepare_runpy_no_retry',len(host_execute_calls)==1 and len(runpy_calls)==1)
check('unprofiled_entry_preconditions_and_no_setprofile',
    'sys.getprofile() is not None' in h and 'sys.getprofile() is not None' in d
    and 'sys.setprofile' not in h+d and 'PassiveProfile' not in h+d)
check('single_thread_python_no_optimization_and_no_bytecode_host',
    "('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')" in h
    and "any(os.environ.get(k) != '1' for k in THREAD_KEYS)" in h
    and 'Path(sys.executable).resolve() != PYTHON' in h
    and 'sys.flags.optimize' in h and 'sys.flags.optimize' in d
    and 'sys.dont_write_bytecode = True' in h and "command = [str(PYTHON),'-B',str(DRIVER)]" in h)
receipt = json.loads(sources[OLD_RECEIPT]);argv = receipt['input']['argv']
flags = ['--rank1-cache-build-seal-sha256','--rank1-cache-terminal-evidence','--rank1-cache-terminal-evidence-sha256',
    '--failed-capture-terminal-evidence-sha256','--memory-build-seal-sha256','--memory-terminal-evidence',
    '--memory-terminal-evidence-sha256','--failed-memory-capture-terminal-evidence-sha256','--patch-helper-sha256','--controls-source-sha256']
check('closed_actual_original_receipt23items10parameters_exact_order',
    type(receipt['terminal']['exit_code']) is int and receipt['terminal']['exit_code']==0
    and receipt['session_closed'] is True and len(argv)==23 and argv[2]=='prepare-build' and argv[3::2]==flags)
check('immutable_original_CLI_values_copied_only_target_replaced',
    "argv=list(receipt['input']['argv'])" in d and "argv[1]=str(TARGET)" in d
    and 'sys.argv=argv[1:]' in d and "runpy.run_path(str(TARGET),run_name='__main__')" in d)
retargeted=list(argv);retargeted[1]=str(TARGET)
targettree=ast.parse(sources[TARGET])
declared_flags=[n.args[0].value for n in ast.walk(targettree) if isinstance(n,ast.Call)
    and isinstance(n.func,ast.Attribute) and n.func.attr=='add_argument' and n.args
    and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str)]
check('canonical_cli_accepts_all_original_prepare_flags',all(f in declared_flags for f in flags))
write_calls=[n for n in ast.walk(dt) if isinstance(n,ast.Call) and ast.unparse(n.func)=='stream.write']
check('driver_child_JSON_has_real_LF_not_literal_backslash_n',len(write_calls)==1 and ast.literal_eval(write_calls[0].args[0])=='\n')
check('complete_decl86_build12_original_future_caps_and_false_science_gates',
    "d['complete_stage_count'] != 86" in h and "len(d['build_commands']) != 12" in h
    and "(1800,600,512,2*2**30)" in h and "d['AAA_accuracy_qualified'] or d['ABA_admitted']" in h)
check('strict_actual_integer_child_exit0_positivePID_wall_RSS_watch_checks',
    "type(watch['returncode']) is not int" in h and "watch['returncode'] != 0" in h
    and "type(watch['pid']) is not int" in h and "watch['pid'] <= 0" in h
    and "watch['own_child_only'] is not True" in h and "watch['liveness_group_cleanup'] is not True" in h
    and "watch['rss_cap_mib'] != RSS_CAP" in h and "watch['sampled_peak_rss_mib'] < RSS_CAP" in h)
check('both_whole_archive_time_checks_and_exclusive_preparation_science_boundary',
    "not elapsed < WHOLE_CAP" in h and 'not archived < ARCHIVE_CAP' in h
    and 'time.monotonic()-started >= WHOLE_CAP' in h
    and 'archive_bytes((HOST_OUT,PROFILE_OUT,SOURCE,OUT)) >= ARCHIVE_CAP' in h
    and 'os.path.lexists(TERMINAL)' in h
    and 'full86_executed=False,compilation_or_transport_launched=False' in h)
check('every_pinned_input_reverified_before_host_success_outside_loop',
    'for entry in inputs+[hpin,rpin]:' in h and h.index('\n        value = dict(schema=') > h.index('complete preparation input source identity changed'))
check('no_business_class_or_module_global_monkeypatch',not any(isinstance(n,(ast.Assign,ast.AugAssign,ast.AnnAssign))
    and any(isinstance(a,ast.Attribute) and isinstance(a.value,ast.Name) and a.value.id in {'full','production','resource_factory','h','diagnostic'}
        for a in (n.targets if isinstance(n,ast.Assign) else [n.target])) for n in ast.walk(ht)))
freshnames=[ART/x for x in ['axial-material-complete-prepare-host-v15-20261010','axial-material-complete-prepare-evidence-v15-20261010',
    'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-admission-v15-20261010',
    'axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010',
    'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-terminal-v15-20261010']]
check('five_fresh_namespaces_absent_at_readonly_source_review',all(not os.path.lexists(p) for p in freshnames))
for pin in pins:
    _,after=read_pin(Path(pin['path']),pin['sha256']);assert pin==after
value=dict(schema='AXMAT_V15_COMPLETE_PREPARE_ENTRY_FINAL_READONLY_SOURCE_REVIEW_V1',
    status='PASS_SOURCE_ONLY_READY_FOR_ROOT_ACTUAL_PREPARE',review_scope='fixed source and small existing receipts only; no project import, resource scan, business CLI, fixture, compiler process or numeric calculation',
    checks=checks,all_checks_passed=True,source_input_pins=pins,original_canonical_argv=argv,
    authorized_retargeted_canonical_argv=retargeted,fresh_namespace_paths=[str(p) for p in freshnames],
    caps=dict(host_wall_seconds=1800,child_stage_seconds=600,child_rss_mib=512,archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0),
    original5supportfunctions_byte_exact=True,actual_resource_module_qualification_consumed_as_pinned_evidence_only=True,
    genuine_supervisor_source_and_class_MRO_preserved=True,normal_new_resource_class_source_unchanged_except_qualified_validator=True,
    canonical_prepare_executed_by_this_review=False,resource_scan_performed=False,canonical_source_changed=False,
    full86_executed=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
with (HERE/'REPORT.json').open('x') as stream:json.dump(value,stream,indent=2,ensure_ascii=False,allow_nan=False);stream.write('\n')
print(json.dumps(dict(status=value['status'],checks=len(checks),all_passed=True,report=str(HERE/'REPORT.json'),report_sha256=hashlib.sha256((HERE/'REPORT.json').read_bytes()).hexdigest(),business_executed=False,resource_scan=False),allow_nan=False))
