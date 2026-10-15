"""Independent source audit only. Never imports or starts either probe script."""
import ast
import hashlib
import json
import os
import stat
import symtable
import sys
from pathlib import Path

OUT = Path('/private/tmp/spot_v9_isolated_parser_watch_source_independent_review_20261009')
PLAN = Path('/private/tmp/axmat_v9_isolated_parser_metadata_watch_source_plan_20261009')
CANDIDATE_DIR = Path('/private/tmp/axmat_v9_strict_json_local_immutable_sharing_candidate_20261009')
EXPECTED = {
    PLAN/'parser_metadata_worker.py': '9039034ef548abc7ef02683c90e1b36fbaff5c99ebed91a873443fe843ad9552',
    PLAN/'root_owned_parser_watchdog.py': 'e5177791ee5c88e36aa5f161f917c8baa4106fc62556bb3e5b6e0d39eb6a9e63',
    PLAN/'source_plan.json': 'e2f9248874a427bd76de88beafe55c7d1210ee06dea3c85c37c4038ce9a66cb7',
    PLAN/'source_self_audit.json': 'ce73697c656b623bf86ec3d6e3ffda27c91f93d96515fb4fec55c41ab485be12',
    PLAN/'actual_source_audit_tool_return.json': '5a49df68c9d5ac39aab483b506c255c656ecb275f1e091c097ee9496198404d1',
    PLAN/'audit_source_plan_only.py': 'd560ffdae67fb8002fa6277171bb8c33f5895ed24d54b515cd4779e461d2c532',
    Path('/Users/wen/spot/validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v8.py'): '4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4',
    CANDIDATE_DIR/'strict_json_bytes_local_immutable_sharing_candidate.py': '15383b532973a9dc68fcdaeb7251723ee3379a075472bddadfb6bdbf9b9ec8d3',
    Path('/Users/wen/spot/validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009/declaration.json'): '3c7f3c1fc8f5ce73b15136442df2622aa30538c4f7806abf8f2fddd1da7387ae',
    Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json'): '2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa',
    CANDIDATE_DIR/'SEMANTIC_REPORT.json': '65246dc3e3afb1e901a521e4dfcb7342c604a96ea43c4a426c8c8979cc7f986c',
    CANDIDATE_DIR/'STOPPED_handoff.json': 'dbebd07ae915cf2650181c7d1f234ec00eae169a5b9bf6a0a49ab8f8d28c8013',
    Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'): 'ba725dca52e02b5382d6acf3e6ac92afb0d65662f1ce8820d75a59a095490860',
}

def identity(p):
    s=p.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def pin(p,expected=None):
    before=identity(p)
    assert p.is_absolute() and '..' not in p.parts and p.parent.resolve(strict=True)==p.parent
    assert stat.S_ISREG(before[2])
    h=hashlib.sha256();size=0
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as stream:
        s=os.fstat(stream.fileno());assert [s.st_dev,s.st_ino]==before[:2]
        while block:=stream.read(1024**2):
            h.update(block);size+=len(block)
    assert identity(p)==before and size==before[3]
    if expected is not None:assert h.hexdigest()==expected,(str(p),h.hexdigest(),expected)
    return {'path':str(p),'identity':before,'size':size,'sha256':h.hexdigest()}

def save(p,v):
    with p.open('xb') as f:
        f.write((json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())

assert sys.version_info[:2]==(3,12) and __debug__ and sys.dont_write_bytecode
assert OUT.parent.resolve(strict=True)==OUT.parent
initial={str(p):pin(p,h) for p,h in EXPECTED.items()}
initial[str(Path('/bin/ps'))]=pin(Path('/bin/ps'))
plan=json.loads((PLAN/'source_plan.json').read_text())
author=json.loads((PLAN/'source_self_audit.json').read_text())
receipt=json.loads((PLAN/'actual_source_audit_tool_return.json').read_text())
assert receipt['chunk_id']=='2d2479' and receipt['exit_code']==0 and receipt['closed'] is True and receipt['session_id'] is None
assert receipt['worker_or_watch_execution'] is False and receipt['scope']=='SOURCE_ONLY_NO_PROBE'
assert receipt['source_plan_sha256']==EXPECTED[PLAN/'source_plan.json'] and receipt['source_report_sha256']==EXPECTED[PLAN/'source_self_audit.json']
assert author['status']=='PASS_SOURCE_ONLY' and author['actual_worker_or_watch_execution'] is False
for k in ('actual_output','actual_child_PID','actual_tool_terminal','actual_measurements','actual_business_RUNNING_stage'):
    assert plan[k] is None
assert plan['actual_watch_started'] is False
assert plan['planned_cases']==['original_DECL','candidate_DECL','original_FULL_SEVEN_INPUT','candidate_FULL_SEVEN_INPUT']
assert plan['caps']==dict(PYTHONOPTIMIZE_absent=True,PYTHONPATH_absent=True,bytecode_disabled=True,numeric_workers_at_once=1,own_PID_ps_RSS_MiB=512,per_child_seconds=120,retries=0,threads=1)
for k in ('worker_source','watchdog_source','frozen_original_source','known_candidate_source'):
    assert plan[k]==initial[plan[k]['path']]
for record in plan['data_pins']:
    assert record==initial[record['path']]
for p,record in author['source_pins'].items():assert record==initial[p]
for record in author['data_pins']:assert record==initial[record['path']]

sources={};trees={};inventory={}
allowed={'argparse','ast','gc','hashlib','json','math','os','resource','stat','sys','time','pathlib','signal','subprocess'}
for name in ('parser_metadata_worker.py','root_owned_parser_watchdog.py','audit_source_plan_only.py'):
    p=PLAN/name;source=p.read_text();tree=ast.parse(source);compile(tree,str(p),'exec')
    sources[name]=source;trees[name]=tree;imports=[]
    for n in ast.walk(tree):
        if isinstance(n,ast.Import):
            imports.extend(a.name for a in n.names);assert all(a.name in allowed for a in n.names)
        elif isinstance(n,ast.ImportFrom):
            assert n.level==0 and n.module in allowed;imports.append(n.module)
    inventory[name]={'imports':imports,'compile_only_not_execute':True,'functions':[[n.name,n.lineno,n.end_lineno] for n in tree.body if isinstance(n,ast.FunctionDef)]}

worker=sources['parser_metadata_worker.py'];watch=sources['root_owned_parser_watchdog.py']
worker_tokens=["ast.Module(body=[node],type_ignores=[])","namespace={'json':json,'math':math,'__builtins__':SAFE_BUILTINS}","set(namespace)=={'json','math','__builtins__','strict_json_bytes'}",'os.O_RDONLY|os.O_NOFOLLOW',"sys.version_info[:2]==(3,12) and __debug__ and sys.dont_write_bytecode", "'PYTHONPATH' not in os.environ and 'PYTHONOPTIMIZE' not in os.environ",'del source_payload','value=function(raw)','del raw','del value;gc.collect()',"json.JSONEncoder(sort_keys=False,separators=(',',':'),ensure_ascii=True,allow_nan=False).iterencode(value)","business_import_or_API_or_constructor_or_PREP_RUN=False,native_or_science_credit=False"]
for token in worker_tokens:assert token in worker,token
watch_tokens=['CAP_SECONDS=120;CAP_MIB=512;SAMPLE_SECONDS=.02','candidate==CANDIDATE and a.candidate_sha==CANDIDATE_SHA',"'PYTHONDONTWRITEBYTECODE']='1'",'for k in THREAD_KEYS:env[k]=\'1\'','env.pop(\'PYTHONPATH\',None);env.pop(\'PYTHONOPTIMIZE\',None)', 'start_new_session=True','os.getpgid(proc.pid)==proc.pid','os.killpg(proc.pid,sig)',"(signal.SIGTERM,'SIGTERM'),(signal.SIGKILL,'SIGKILL')",'proc.wait(timeout=2)','rss>=CAP_MIB','remaining<=0','now-started>=CAP_SECONDS','phase_before==phase_after','phase_transition_ambiguous',"if receipt['status']!='PASS_ISOLATED_PARSER_DIAGNOSTIC_ONLY':failure=True;break",'out.mkdir(exist_ok=False)',"out.is_relative_to(Path('/private/tmp'))",'one_worker_at_once=True,retries=0','actual_V8_allocating_line_localized=False,Root_tool_terminal_observation=None','if failure:raise SystemExit(1)']
for token in watch_tokens:assert token in watch,token
thread_keys=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
for key in thread_keys:assert key in worker and key in watch
functions={n.name:n for n in trees['parser_metadata_worker.py'].body if isinstance(n,ast.FunctionDef)}
main=functions['main'];phases=[]
for n in ast.walk(main):
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='event':
        assert len(n.args)==3;phases.append([ast.literal_eval(n.args[1]),ast.literal_eval(n.args[2])])
assert [row[1] for row in phases]==list(range(1,11))
calls=[n for n in ast.walk(trees['root_owned_parser_watchdog.py']) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='subprocess']
assert sorted(n.func.attr for n in calls)==['Popen','run']
rss_call=next(n for n in calls if n.func.attr=='run')
assert isinstance(rss_call.args[0],ast.List)
assert [ast.literal_eval(n) for n in rss_call.args[0].elts[1:5]]==['-o','pid=','-o','rss=']

parsers=[]
restricted_names={'ValueError','TypeError','OverflowError','RecursionError','RuntimeError','KeyError','Exception','str','bool','int','float','dict','list','tuple','set','frozenset','isinstance','type','len','all','any','enumerate','sorted','sum','zip','min','max','abs','bytes','range','id'}
for record in plan['parser_inventory']:
    p=Path(record['path']);source=p.read_text();tree=ast.parse(source)
    matches=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='strict_json_bytes'];assert len(matches)==1
    fn=matches[0];assert fn.returns is None and not fn.decorator_list
    assert len(fn.args.args)==1 and fn.args.args[0].arg=='raw' and fn.args.args[0].annotation is None
    assert not fn.args.posonlyargs and not fn.args.kwonlyargs and fn.args.vararg is None and fn.args.kwarg is None and not fn.args.defaults
    assert not any(isinstance(n,(ast.Import,ast.ImportFrom,ast.Global,ast.Nonlocal,ast.ClassDef,ast.AsyncFunctionDef,ast.Await,ast.Yield,ast.YieldFrom)) for n in ast.walk(fn))
    function_source=''.join(source.splitlines(keepends=True)[fn.lineno-1:fn.end_lineno])
    assert hashlib.sha256(function_source.encode()).hexdigest()==record['function_with_source_line_ending_sha256']
    assert hashlib.sha256(function_source.rstrip('\n').encode()).hexdigest()==record['function_without_trailing_newline_sha256']
    table=symtable.symtable(function_source,str(p),'exec');scopes=[]
    def walk_scope(scope):
        names=sorted(s.get_name() for s in scope.get_symbols() if s.is_global() and s.is_referenced())
        assert set(names)<=restricted_names|{'json','math'},(scope.get_name(),names)
        scopes.append({'scope':scope.get_name(),'referenced_globals':names})
        for child in scope.get_children():walk_scope(child)
    walk_scope(table)
    compile(ast.Module(body=[fn],type_ignores=[]),'<independent parser AST syntax only>','exec')
    parsers.append(dict(record,global_scope_inventory=scopes,definition_compiled_not_executed=True))

after={p:pin(Path(p),record['sha256']) for p,record in initial.items()}
assert initial==after
report={
    'schema':'AXMAT_V9_ISOLATED_PARSER_WATCH_INDEPENDENT_SOURCE_REVIEW_V1',
    'status':'PASS',
    'approval_scope':'SOURCE_CONTRACT_ONLY_FOR_EXACT_PINNED_FOUR_CASE_ROOT_OWNED_DIAGNOSTIC; no worker/watch run or memory measurement performed by this review',
    'source_plan_sha256':EXPECTED[PLAN/'source_plan.json'],
    'worker_source_sha256':EXPECTED[PLAN/'parser_metadata_worker.py'],
    'watchdog_source_sha256':EXPECTED[PLAN/'root_owned_parser_watchdog.py'],
    'candidate_source_sha256':EXPECTED[CANDIDATE_DIR/'strict_json_bytes_local_immutable_sharing_candidate.py'],
    'source_and_data_full_sha_identity_before':initial,
    'source_and_data_full_sha_identity_after':after,
    'total_unique_fresh_full_sha_files':len(initial),
    'total_unique_fresh_full_sha_bytes':sum(r['size'] for r in initial.values()),
    'source_AST_inventory':inventory,
    'exact_parser_AST_inventory':parsers,
    'manual_source_review':{
        'fixed_complete_inputs':'DECL8162042B and original whole19356767B; neither was parsed by this independent source review. Both full file SHA and seven-field lstat identities were verified twice.',
        'execution_separation':'Worker lines53–71 extracts the sole strict_json_bytes FunctionDef, with no annotations/defaults/decorators/imports and only actual json/math/restricted builtin globals. Full F8 text is read and parsed into AST, but factory top-level/body code is never imported or executed.',
        'serial_boundary':'Watch lines143–148 fixes original_DECL, candidate_DECL, original_FULL_SEVEN_INPUT, candidate_FULL_SEVEN_INPUT in a nested serial loop. run_case completes or fails and cleans its owned child before return. Any failure stops with zero retries; a failed experiment may truthfully complete fewer than four cases.',
        'limits_and_environment':'Python executable fixed to actual3.12 SHA ba725..., worker asserts3.12/__debug__/dont_write_bytecode. Exactly five thread keys are1, PYTHONPATH/PYTHONOPTIMIZE/PYTHONSTARTUP/PYTHONHOME removed.120s/512MiB own child gates unchanged.',
        'own_process_observation':'Watch66–71 invokes /bin/ps only for exact Popen PID and requires matching numeric PID/RSS. Live observation failure fails closed; no alternative ps bypass or fabricated RSS. Watch81–108 admits own new session PID=group and termination sends own-group SIGTERM then SIGKILL with waits, recording real returncode and exit races.',
        'output_boundary':'Root chooses a new canonical /private/tmp directory with mkdir(exist_ok=False), excluded from source PLAN. Each case is freshly created. Logs, receipts, report and summary use x/xb/exclusive hard-link publication; only case latest_phase.json is deliberately atomically replaced. Project/formal/ART source/results are read only.',
        'complete_semantic_comparison':'Worker73–89 checks exact builtin value/container/key types, finite floats, dict iteration order and no shared mutable dict/list IDs.116–118 emits all parsed fields through complete insertion-order compact ASCII finite JSONEncoder intoSHA. Root151–155 requires type counts, complete shape/insertion hash, complete JSON digest/bytecount and mutable independence equality for both full inputs.',
        'phases':phases,
        'raw_and_value_lifetimes':'Source payload deleted after AST extraction; raw preserved across parse and returned-value sampling, then explicitly deleted while whole parsed value stays live. Full type/digest validation and fresh inputs are separately labelled before wholevalue deletion and explicitgc. Type-validation nested closure does not capture input root; mutable ID set is cleared.',
        'sampling_limits':'Watch89–100 brackets each ps sample by phase reads and labels transitions ambiguous. Required retained stable phase coverage is enforced119–122. This remains sampled process RSS with diagnostic pauses/checking overhead, not exact allocation-line attribution or business-caller RSS.',
        'rusage_limits':'Worker91–94 and107/110/123 record supplemental historical whole-process high-water using Darwin bytes/LinuxKiB conversions. Root123–124 refuses diagnostic success when this supplement reaches512; it is not a replacement for own-PID ps. Honest actual child0 with a later supplemental or equivalence failure remains child0 and Root1, never altered into a fictional nonzero child receipt.',
        'failure_evidence':'Child parser exceptions naturally produce actual nonzero worker stderr/returncode; wall/RSS/ps failures terminate owned child and Root summary records genuine returncode. Failed stages/absent childreport never receive PASS. If a pin/cleanup assertion aborts before summary, genuine Root nonzero/stdio must be retained; no source contract promises receipt construction after arbitrary assertion failure.',
        'frozen_science':'All source-plan actual PID/output/measurement/tool/business stage fields None, watch_startedFalse; Root terminal summary placeholderNone. Every report classifies isolated metadata only, no combined/native/AAA/ABA/science or actualV8 allocating-line credit.',
    },
    'limitations':['Source review and pinning only; no worker/watch invocation, no memory/elapsed test, no data parser execution here.','Exact candidate semantic fixtures/full-metadata comparison report is a separately pinned earlier author result, not rerun or treated as memory evidence.','Local str/int pools may increase parse peak due to pool dictionaries for unique immutable values; benefit is unknown until the one authorized Root diagnostic.','Only the exact worker/watch/candidate/mother/data pins reviewed here are admitted; revisions require new source review.','Process RSS after explicit gc is not proof that allocator pages were returned or a full application peak has fallen.'],
    'future_actual_watch_tool_terminal':None,
    'future_actual_measurements':None,
    'no_worker_or_watch_execution':True,
    'no_business_factory_import_API_constructor_PREP_RUN':True,
    'no_combined_runtime_native_AAA_ABA_science_credit':True,
    'actual_V8_failure_line_localized':False,
    'independent_tool_receipt':'actual_independent_source_review_tool_return.json is written only after real exec_command termination',
}
save(OUT/'REPORT.json',report)
text=('独立源码审查通过，仅批准这些固定源码的四案例独立解析器诊断契约。\n'
      '未启动 worker/watch、未加载业务模块、未解析业务输入、未测量内存。\n'
      '四案例完整输入、单子进程串行、120秒/512MiB、线程1、零重试、真实失败退出和 own-group 清理均保留。\n'
      '两份数据、母源码、候选、工具及封存证据已完整 SHA 和七字段身份前后复核一致。\n'
      '局部共享可能增加峰值；测量结果仍未知。任何后续结果只能记为独立元数据解析器诊断，不能给 combined/native/AAA/ABA 或 V8 失败行定位信用。\n')
with (OUT/'REPORT.txt').open('x') as f:f.write(text)
print(json.dumps({'status':'PASS','report':str(OUT/'REPORT.json'),'report_sha256':pin(OUT/'REPORT.json')['sha256'],'fresh_files':len(initial),'fresh_bytes':report['total_unique_fresh_full_sha_bytes'],'no_execution':True}))
