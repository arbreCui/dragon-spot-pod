"""Two once-only finite serializer proofs; no Dragon, compiler, or pipeline.

Canonical mode actually calls the immutable original dump for all 45 prefixes.
Guard mode starts a separate process, admits the complete original metadata,
keeps the actual 45-record state, uses the honestly derived parent and original
OwnRSS class, and starts only one small Python marker child. No monkeypatch,
profiling, peak reset, looping GC, or numerical qualification is performed.
"""
import argparse, ast, gc, hashlib, importlib.util, json, os, resource, shutil
import stat, subprocess, sys, time
from pathlib import Path

ROOT = Path('/Users/wen/spot')
REC = ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
ART = ROOT/'validation/artifacts'
BUNDLE = REC/'streaming_full_ledger_serializer_min5_source_bundle_v1_20261013'
HERE = Path(__file__).resolve().parent
FINITE_FRESH_BOUND = 64*2**20
ACTUAL = ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v12'
OLD_PARENT = ART/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py'
V12CLI = REC/'ROOT_EXACT_ACTUAL_PIPELINE_V12_ARGV_20261013.json'
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
START = time.monotonic()
PF = {}
SAMPLES = []
sys.dont_write_bytecode = True

def identity(p):
    s=Path(p).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p, wanted=None, remember=True):
    p=Path(p); before=identity(p)
    assert stat.S_ISREG(before[2]) and not any(x.is_symlink() for x in (p,*p.parents))
    with p.open('rb') as f:
        s=os.fstat(f.fileno())
        assert [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before
        sha=hashlib.file_digest(f,'sha256').hexdigest();s=os.fstat(f.fileno())
        assert [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before==identity(p)
    row=dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
    if wanted is not None:
        assert all(row[k]==wanted[k] for k in row),'fullEOF/all7 mismatch: '+str(p)
    if remember:
        assert str(p) not in PF or PF[str(p)]==row
        PF[str(p)]=row
    return row

def module(p,name):
    before=pin(p);spec=importlib.util.spec_from_file_location(name,p)
    m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m)
    assert pin(p)==before
    return m

def write(p,d):
    with p.open('x') as f:
        json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

def metric(label,**extra):
    result=subprocess.run(['/bin/ps','-o','rss=','-p',str(os.getpid())],capture_output=True,text=True,timeout=2)
    assert result.returncode==0 and result.stdout.strip().isdigit()
    row=dict(label=label,current_RSS_bytes=int(result.stdout.strip())*1024,
        SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        allocated_blocks=sys.getallocatedblocks(),gc_count=list(gc.get_count()),
        elapsed_seconds=time.monotonic()-START,**extra)
    SAMPLES.append(row);print(json.dumps(row),flush=True)
    if row['SELF_peak_bytes']>=512*2**20:raise RuntimeError('original SELF512 cap reached')
    if row['elapsed_seconds']>=1800:raise RuntimeError('original whole1800 cap reached')
    return row

def compare_files(a,b):
    with a.open('rb') as x,b.open('rb') as y:
        while True:
            u=x.read(65536);v=y.read(65536)
            assert u==v,'full output byte comparison failed'
            if not u:break

def load_actual():
    stage=ACTUAL/'AAA3-streaming/stages.json'
    rawpath=ACTUAL/'Root_actual_complete_execution_record_before_final_publication.json'
    stagepin=pin(stage);rawpin=pin(rawpath)
    records=json.loads(stage.read_bytes())['stages'];raw=json.loads(rawpath.read_bytes())
    assert len(records)==45 and raw['records']==records
    for row in raw['fixed_current_pins']+raw['owned_runtime_pins']:pin(row['path'],row)
    return records,raw,stagepin,rawpin

def classes_equal(original,derived):
    a=original.read_text();b=derived.read_text();aa=ast.parse(a);bb=ast.parse(b)
    for old in aa.body:
        if isinstance(old,(ast.ClassDef,ast.FunctionDef)) and old.name!='dump_json':
            new=next(x for x in bb.body if type(x) is type(old) and x.name==old.name)
            assert ast.get_source_segment(a,old)==ast.get_source_segment(b,new)

def errors(fn,path,data):
    try:fn(path,data)
    except BaseException as e:return dict(type=type(e).__name__,message=str(e))
    raise AssertionError('expected encoding refusal did not occur')

def edge_cases(old,new,out):
    a=out/'canonical_edge.json';b=out/'derived_edge.json';results=[]
    values=[dict(floats=[0.0,-0.0,1.25,1e-100,1e100,float('nan'),float('inf'),-float('inf')],
                 unicode=['中文','é','\U0001f310','a\nb'],nested={'z':None,'a':[True,False,1]}),
            {'integer_keys':{2:'two',1:'one'},'tuple':(1,2),'empty':[]},{}]
    for i,value in enumerate(values):
        old(a,value);new(b,value);compare_files(a,b)
        results.append(dict(kind='valid_defaults_'+str(i),sha256=pin(a,remember=False)['sha256'],bytes=identity(a)[4]))
    circular={};circular['self']=circular
    invalid=[('unsupported_type',{'bad':object()}),('circular',circular),('mixed_sorted_keys',{1:'one','a':'letter'})]
    for label,value in invalid:
        # Existing target and .tmp bytes must survive encoding errors exactly.
        for p in (a,b):
            p.write_bytes(b'original-existing-target\n')
            p.with_suffix(p.suffix+'.tmp').write_bytes(b'original-existing-temporary\n')
        x=errors(old,a,value);y=errors(new,b,value);assert x==y
        for p in (a,b):
            assert p.read_bytes()==b'original-existing-target\n'
            assert p.with_suffix(p.suffix+'.tmp').read_bytes()==b'original-existing-temporary\n'
        results.append(dict(kind=label,error=x,existing_target_and_tmp_untouched=True))
    return results

def canonical(out):
    sys.path.insert(0,str(OLD_PARENT.parent))
    old=module(OLD_PARENT,'finite_original_parent_for_bytes')
    new=module(BUNDLE/'runtime/production_runner.py','finite_derived_parent_for_bytes')
    classes_equal(OLD_PARENT,Path(new.__file__))
    records,raw,stagepin,rawpin=load_actual();del raw
    factory=module(ROOT/'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py','finite_canonical_original_resource_factory')
    history=factory.DynamicHistoryResources(ART,factory.history_roots([str(out)],ART),8*2**30,96*2**30,old.ResourceFailure)
    fresh=old.DiskResources(ART,[str(out)],8*2**30,2*2**30)
    before=history.check();f=fresh.check()
    assert before['artifact_bytes']+20971764748+64*2**20+FINITE_FRESH_BOUND<96*2**30
    assert f['disk_free_bytes']-20971764748-2*2**30>=8*2**30
    assert f['artifact_bytes']<=FINITE_FRESH_BOUND
    metric('canonical_raw45_all_current_fixed_owned_live')
    out.mkdir();a=out/'original_prefix.json';b=out/'derived_prefix.json';prefixes=[]
    for i in range(1,46):
        data={'stages':records[:i]}
        old.dump_json(a,data);new.dump_json(b,data);compare_files(a,b)
        assert fresh.check()['artifact_bytes']<=FINITE_FRESH_BOUND
        row=pin(a,remember=False)
        prefixes.append(dict(stage_count=i,size_bytes=row['size_bytes'],sha256=row['sha256']))
        if i==1 or i%5==0:metric('original_and_new_byteexact_prefix_'+str(i),size_bytes=row['size_bytes'])
    compare_files(a,ACTUAL/'AAA3-streaming/stages.json')
    assert prefixes[-1]['sha256']==stagepin['sha256']
    edge=edge_cases(old.dump_json,new.dump_json,out)
    after=history.check();f=fresh.check()
    assert after['artifact_bytes']+20971764748+64*2**20<96*2**30
    assert f['disk_free_bytes']-20971764748-2*2**30>=8*2**30
    assert f['artifact_bytes']<=FINITE_FRESH_BOUND
    return dict(original_dump_actual_calls=45,derived_complete_prefix_actual_calls=45,
        all45_full_byte_comparison=True,canonical_prefixes=prefixes,default_and_error_contract=edge,
        original_stage_pin=stagepin,original_raw_pin=rawpin,
        original_dumps_memory_present_in_this_process=True,pure_streaming_memory_gain_claimed=False,
        before_resources=before,after_resources=after,original_caps_retained=True,finite_additional_fresh_limit_bytes=FINITE_FRESH_BOUND)

def guard(out,canonical_pin):
    canonical_report=json.loads(Path(canonical_pin['path']).read_bytes())
    pin(canonical_pin['path'],canonical_pin)
    assert canonical_report['status']=='FINITE_COMPLETE_NOT_BUSINESS_QUALIFICATION'
    expected=canonical_report['evidence']['canonical_prefixes'];assert len(expected)==45
    c=module(BUNDLE/'guarded_warm_A_common.py','finite_derived_current_common')
    # The real Common initializes the full catalog/guard lineage and original
    # complete resources. Output is still absent and no child is started here.
    binding,initial_fixed,support,helper,full,base_resources,before=c.initialize(out,START)
    assert before['artifact_bytes']+20971764748+64*2**20+FINITE_FRESH_BOUND<96*2**30
    production=sys.modules['production_runner']
    assert Path(production.__file__).resolve()==support.PARENT
    assert Path(full.__file__).resolve()==support.FULL
    assert full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)
    assert production.SerialExecutor.execute.__globals__['dump_json'] is production.dump_json
    classes_equal(OLD_PARENT,support.PARENT)
    for p in (c.BIND,support.OLD_HELPER,support.FULL,support.PARENT,support.BOUNDED,support.RESOURCE_FACTORY):pin(p)
    cli_pin=pin(V12CLI);cli=json.loads(V12CLI.read_bytes());objects={}
    catalog=c.current_catalog()
    for name,p in cli['mandatory_external_bindings'].items():
        d,p2=c.load_json_exact(p['path'],p['sha256'],json.dumps(p['identity']))
        assert p==p2;objects[name]=d;pin(p['path'],p)
        if name in ('a1','a2','a3'):c.closed_report(d,helper,Path(p['path']).parent,4)
    build=objects['build70'];c.closed_report(build,helper,Path(cli['mandatory_external_bindings']['build70']['path']).parent,3)
    for name,key in (('current69','original_actual69_handle_lifetime_report_pin'),('original69','original_actual69_v4_report_pin')):
        p=build[key];d,p2=c.load_json_exact(p['path'],p['sha256'],json.dumps(p['identity']))
        assert p==p2;objects[name]=d;pin(p['path'],p)
    eighteen,p17=c.admit17(cli['mandatory_external_bindings']['seventeen']['path'],
        cli['mandatory_external_bindings']['seventeen']['sha256'],json.dumps(cli['mandatory_external_bindings']['seventeen']['identity']),helper)
    objects['admitted17']=eighteen
    metric('complete_original_seven_metadata_69_17_admitted')
    cached=dict(compiler=build['records'][0]['command'][0],includes=tuple(x for x in build['records'][0]['command'] if x.startswith('-I')),
        archives=tuple(x for x in build['records'][-1]['command'] if x.endswith('.a')),
        exe=dict(next(x for x in build['output_pins'] if Path(x['path']).name=='Dragon')),
        link_command=build['records'][-1]['command'],bounded_sha256=binding['original_bounded']['sha256'])
    hf=objects['host-freeze'];objects.clear();del build,eighteen,binding,d,p2,p,cli,initial_fixed
    gc.collect()  # Original metadata-lifetime close; never GC inside measurement.
    records,raw,stagepin,rawpin=load_actual()
    fixed=raw['fixed_current_pins'];owned=raw['owned_runtime_pins'];proofs=raw['actual_complete_readback_proofs']
    cases=raw['actual_operator_refusals'];release=raw['actual_private_release_ledger'];scratch=raw['actual_closed_CLE_scratch_archival_ledger']
    del raw;gc.collect()  # Same existing raw decode closure as prior baseline.
    assert len(fixed)==2654 and len(owned)==163
    # Exact original PhaseResources declaration, no new observation hook or
    # replacement method. The enclosing Common Resources class is already real.
    host=REC/'aaa_three_plane_streaming_pipeline_source_v11/run_actual_three_plane_pipeline.py'
    pin(host);text=host.read_text();tree=ast.parse(text)
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='PhaseResources')
    env={'Path':Path,'WORK':out/'AAA','OUT':out,'MI':2**20}
    exec(compile(ast.Module(body=[cls],type_ignores=[]),'<exact immutable original PhaseResources declaration>','exec'),env)
    resources=env['PhaseResources'](base_resources);resources.phase='serializer_finite_guard_dummy'
    out.mkdir();(out/'runtime').mkdir();(out/'AAA').mkdir();(out/'AAA3-streaming').mkdir();(out/'guard_dummy').mkdir()
    shutil.copy2(support.BOUNDED,out/'runtime/run_bounded_dragon.py')
    assert pin(out/'runtime/run_bounded_dragon.py')['sha256']==cached['bounded_sha256']
    runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-START),'AAA3-streaming',resources)
    runner.records=records
    baseline=metric('derived_parent_complete_actual45_fixed_owned_live_baseline',fixed_count=len(fixed),owned_count=len(owned),records=len(runner.records))
    prefix_path=out/'finite_complete_prefix.json';prefixes=[]
    resources.check()
    for i in range(1,46):
        production.dump_json(prefix_path,{'stages':records[:i]})
        assert resources.check()['fresh_output']['artifact_bytes']<=FINITE_FRESH_BOUND
        actual=pin(prefix_path,remember=False);wanted=expected[i-1]
        assert actual['sha256']==wanted['sha256'] and actual['size_bytes']==wanted['size_bytes']
        prefixes.append(dict(stage_count=i,sha256=actual['sha256'],size_bytes=actual['size_bytes']))
        if i==1 or i%5==0:metric('derived_only_complete_prefix_'+str(i),size_bytes=actual['size_bytes'])
    compare_files(prefix_path,ACTUAL/'AAA3-streaming/stages.json')
    marker='STREAMING-SERIALIZER-FINITE-GUARD-DUMMY-PASS'
    text=runner.execute(out/'guard_dummy','one_python_marker',[str(support.PYTHON),'-B','-c','print('+repr(marker)+')'],600,marker=marker)
    assert text.splitlines()==[marker] and len(runner.records)==46
    assert runner.records[:45]==json.loads((ACTUAL/'AAA3-streaming/stages.json').read_bytes())['stages']
    last=runner.records[-1];assert last['status']=='PASS'
    helper.check_watch(out,last)
    watch_path=out/(last['label']+'.log');watch_path=watch_path.with_suffix('.watchdog.json')
    watch=json.loads(watch_path.read_bytes());assert watch['returncode']==0 and watch['limit_failure'] is None
    pid=watch['pid'];probe=subprocess.run(['/bin/ps','-p',str(pid),'-o','pid='],capture_output=True,text=True,timeout=2)
    assert probe.returncode!=0 and not probe.stdout.strip(),'guard child remains live'
    after=resources.check();assert after['fresh_output']['artifact_bytes']<=FINITE_FRESH_BOUND
    final=metric('derived_complete46_real_guard_closed',guard_status=last['status'],child_peak_MiB=watch['sampled_peak_rss_mib'])
    assert not subprocess._active
    return dict(original_stage_pin=stagepin,original_raw_pin=rawpin,actual_v12_cli_pin=cli_pin,
        selected_derived_parent_pin=pin(support.PARENT),selected_original_full_pin=pin(support.FULL),
        derived_parent_normal_import=True,original_OwnRSS_whole_class_and_parent_non_dump_methods_byteexact=True,
        new_module_identity_honestly_declared=True,canonical_report_pin=canonical_pin,all45_verified_prefixes=prefixes,
        full45_records_preserved=True,actual_new_guard_record=last,actual_watchdog=watch,child_no_longer_live=True,
        before_resources=before,after_resources=after,baseline=baseline,final=final,
        fixed_count=len(fixed),owned_count=len(owned),metadata_closed_before_measurement=True,
        large_original_dumps_not_executed_in_this_measurement_process=True,
        retained_state_names=['records','fixed','owned','proofs','cases','release','scratch','cached','hf','catalog'],
        original_caps_retained=dict(SELF=512*2**20,child=512*2**20,stage=600,whole=1800,history=96*2**30,fresh=2*2**30,cold=20971764748,metadata=64*2**20,free=8*2**30),
        finite_additional_fresh_limit_bytes=FINITE_FRESH_BOUND,pipeline_repair_or_engineering_qualification_proven=False)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=('canonical','guard'),required=True)
    parser.add_argument('--canonical-report');parser.add_argument('--canonical-sha');parser.add_argument('--canonical-seven')
    args=parser.parse_args()
    assert all(os.environ.get(k)=='1' for k in THREADS) and not sys.flags.optimize
    assert not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None
    own=HERE/args.mode;assert not own.exists();own.mkdir()
    out=ART/('axial-material-finite-min5-streaming-serializer-v2-'+args.mode+'-20261013')
    assert not out.exists() and not out.is_symlink()
    pin(__file__)
    for path in (BUNDLE/'runtime/production_runner.py',BUNDLE/'prepare_qualified_AB_source_factor_production.py',BUNDLE/'prepare_cli_host_v15.py',BUNDLE/'guarded_warm_A_common.py',BUNDLE/'COMPLETE_FOUR_SOURCE_BYTE_INVERSE.json'):pin(path)
    status='FINITE_COMPLETE_NOT_BUSINESS_QUALIFICATION';failure=None;evidence=None
    try:
        metric('initial')
        if args.mode=='canonical':evidence=canonical(out)
        else:
            assert args.canonical_report and args.canonical_sha and args.canonical_seven
            seven=json.loads(args.canonical_seven)
            canonical_pin=dict(path=args.canonical_report,sha256=args.canonical_sha,size_bytes=seven[4],identity=seven)
            evidence=guard(out,canonical_pin)
        # Every genuine input used above reaches EOF again with the same all7.
        for row in list(PF.values()):pin(row['path'],row)
        metric('all_current_fixed_owned_and_Source_fullEOF_after')
    except BaseException as error:
        status='FINITE_REFUSAL_NOT_BUSINESS_QUALIFICATION';failure=dict(type=type(error).__name__,message=str(error))
    report=dict(schema='TWO_ONCE_FINITE_ORIGINAL_CANONICAL_AND_DERIVED_STREAMING_GUARD_PROOF_V1',mode=args.mode,
        status=status,failure=failure,evidence=evidence,measurements=SAMPLES,complete_input_pins=list(PF.values()),
        whole_seconds=time.monotonic()-START,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        original_sources_modified=False,canonical_module_monkeypatch=False,numerical_or_pipeline_business_started=False,
        no_peak_reset=True,no_profiling=True,AAA_qualified=False,ABA_admitted=False,engineering_qualified=False,goal_complete=False)
    write(own/'REVIEW.json',report)
    print(json.dumps(dict(status=status,failure=failure,input_files=len(PF),review_pin=pin(own/'REVIEW.json'))),flush=True)
    if failure is not None:raise RuntimeError(failure)

if __name__=='__main__':main()
