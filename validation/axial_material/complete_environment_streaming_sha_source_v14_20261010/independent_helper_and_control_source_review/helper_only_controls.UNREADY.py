"""SOURCE-ONLY. Root must bind reviewed canonical helper SHA before execution.

This independent reader/IO protocol test is not a numerical component control,
raw cache audit, build retry, native RSS proof, or an AAA/ABA qualification.
No fixtures, imports of the tested module or files are created at import time.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import stat
import sys
import threading
import time

STATUS='UNREADY_CANONICAL_HELPER_FINAL_SOURCE_SHA_NOT_BOUND'
HELPER=Path('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_helper_v14.py')
HELPER_SHA256=None
ORIGINAL=Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_source_factor_production.py')
ORIGINAL_SHA256='619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
DECL=Path('/Users/wen/spot/validation/artifacts/axial-material-sender-contiguous-flux-window-build-v13-20261009/declaration.json')
DECL_SHA256='ccdbad6c0e6d767ee98b9e7287c5f3be8120604f57069730289bbd761b947b0f'
PROJECT=Path('/Users/wen/spot')
OUT_PREFIX='axial-material-complete-environment-streaming-sha-helper-only-controls-v14-'
MAX_ARCHIVE_BYTES=64*2**20
EXPECTED_BUFFER_BYTES=4*2**20
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')

def identity(path):
    x=Path(path).lstat()
    return [x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]

def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()

def write_json(path,value):
    with Path(path).open('x') as stream:
        json.dump(value,stream,indent=2,allow_nan=False)
        stream.write('\n')

def load_canonical(path,wanted,name):
    before=identity(path)
    assert stat.S_ISREG(before[2]) and sha(path)==wanted and identity(path)==before
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    assert Path(module.__file__)==path and Path(module.__file__).resolve()==path.resolve()
    assert module.ROOT==PROJECT
    assert identity(path)==before and sha(path)==wanted
    return module,{'path':str(path),'sha256':wanted,'identity':before}

class RealFDProbe:
    """Wrap an actual binary FD. No expected SHA is produced by this adapter."""
    def __init__(self,stream,event,plan):
        self.stream,self.event,self.plan=stream,event,plan
    def __enter__(self):
        self.stream.__enter__()
        return self
    def __exit__(self,*exc):return self.stream.__exit__(*exc)
    def __getattr__(self,name):return getattr(self.stream,name)
    def readinto(self,buffer):
        self.event['readinto_calls']+=1
        call=self.event['readinto_calls']
        if self.plan.get('invalid') is not None:
            token=self.plan['invalid']
            return {'bool':True,'none':None,'negative':-1,'too_large':len(buffer)+1}[token]
        if self.plan.get('premature_zero') and call==2:
            self.event['forced_premature_zero']=True
            return 0
        maximum=self.plan.get('max_piece',len(buffer))
        view=memoryview(buffer)[:min(maximum,len(buffer))]
        try:count=self.stream.readinto(view)
        finally:view.release()
        self.event['bytecount']+=count
        self.event['positive_reads']+=int(count>0)
        if count==0:self.event['EOF_observed']=True
        callback=self.plan.get('after_first_read')
        if call==1 and callback is not None:callback()
        return count

class NewHelperOpenProbe:
    """Instrument only the newly added private _env_stream_open adapter."""
    def __init__(self,module):
        self.module=module
        self.original=module._env_stream_open
        self.events=[]
        self.plans={}
    def __enter__(self):
        def opened(path):
            stream=self.original(path)
            event={'literal':str(path),'readinto_calls':0,'positive_reads':0,'bytecount':0,'EOF_observed':False,
                'fd_identity_before':identity(path),'opened_fd_size':os.fstat(stream.fileno()).st_size}
            self.events.append(event)
            return RealFDProbe(stream,event,self.plans.get(str(path),{}))
        self.module._env_stream_open=opened
        return self
    def __exit__(self,*exc):self.module._env_stream_open=self.original

def context_cleared(module):
    assert module._ENV_STREAM_ACTIVE_CONTEXT is None
    assert not module._ENV_STREAM_SCOPE_LOCK.locked()

def reject(call,contains=None):
    try:call()
    except (ValueError,OSError,RuntimeError) as error:
        if contains is not None:assert contains in str(error),str(error)
        return {'type':type(error).__name__,'message':str(error)}
    raise AssertionError('required guard unexpectedly accepted')

def make_file(path,size=257,marker=0):
    chunk=bytes((i*73+marker)%256 for i in range(65536))
    with path.open('xb') as stream:
        left=size
        while left:
            piece=chunk[:min(left,len(chunk))]
            stream.write(piece)
            left-=len(piece)
    return sha(path)

def environment_declaration(files,predecessors=(),aliases=None):
    return {'files':dict(files),'build_python_executable':str(Path(sys.executable).resolve()),
        'native_library_aliases':dict(aliases or {}),
        'numerical_loader_environment':{k:v for k,v in os.environ.items() if k.startswith('DYLD_') or k=='OPENBLAS_CORETYPE'},
        'preserved_predecessors':list(predecessors)}

def inside_environment(module,d):
    with module.complete_environment_digest_context(d['native_library_aliases']):
        module.environment(d)

def fixture_controls(module,out):
    records=[]
    def run(name,action):
        folder=out/name
        folder.mkdir()
        context_cleared(module)
        with NewHelperOpenProbe(module) as probe:
            result=action(folder,probe)
        context_cleared(module)
        record={'name':name,'status':'PASS_HELPER_PROTOCOL_ONLY','result':result,
            'actual_new_helper_open_stream_events':probe.events}
        write_json(folder/'case_result.json',record)
        records.append(record)
    def hashes(folder,probe):
        observations=[]
        for i,size in enumerate([0,1,EXPECTED_BUFFER_BYTES-1,EXPECTED_BUFFER_BYTES,EXPECTED_BUFFER_BYTES+1,2*EXPECTED_BUFFER_BYTES+17]):
            p=folder/('input_'+str(i)+'.bin');want=make_file(p,size,i)
            with module.complete_environment_digest_context({}):assert module.digest(p)==want
            event=probe.events[-1]
            assert event['bytecount']==size and event['EOF_observed']
            observations.append({'size':size,'oracle_sha256':want,'actual_sha256':module.digest(p)})
        return observations
    run('independent_SHA_empty_boundaries_multiblock_tail',hashes)
    def short(folder,probe):
        p=folder/'input.bin';want=make_file(p,10003)
        probe.plans[str(p)]={'max_piece':7}
        with module.complete_environment_digest_context({}):assert module.digest(p)==want
        assert probe.events[-1]['positive_reads']>1000 and probe.events[-1]['bytecount']==10003
        return {'oracle_sha256':want,'forced_short_piece_bytes':7}
    run('forced_positive_short_reads',short)
    def invalid(folder,probe):
        failures=[]
        for token in ['bool','none','negative','too_large','premature_zero']:
            p=folder/(token+'.bin');make_file(p,100)
            probe.plans[str(p)]=({'premature_zero':True,'max_piece':7} if token=='premature_zero' else {'invalid':token})
            def attempt():
                with module.complete_environment_digest_context({}):module.digest(p)
            failures.append({'token':token,'rejection':reject(attempt)})
            context_cleared(module)
        return failures
    run('invalid_stream_counts_and_premature_EOF',invalid)
    def duplicate(folder,probe):
        tree=folder/'namespace';tree.mkdir();p=tree/'input.bin';want=make_file(p,4097)
        d=environment_declaration({str(p):want},[{'root':str(tree),'inventory':{'files':{'input.bin':want},'symlinks':{}}}])
        start=len(probe.events);inside_environment(module,d)
        assert len(probe.events)-start==1
        return {'actual_full_reads':1,'expected_SHA_owner_checks':2,'original_complete_environment_predicates':True}
    run('same_literal_declared_owner_and_inventory',duplicate)
    def distinct(folder,probe):
        p=folder/'first.bin';q=folder/'second.bin';r=folder/'hardlink.bin'
        want=make_file(p,1025);make_file(q,1025);os.link(p,r)
        assert sha(q)==want and sha(r)==want and p.stat().st_ino!=q.stat().st_ino and p.stat().st_ino==r.stat().st_ino
        with module.complete_environment_digest_context({}):
            for path in [p,q,r]:assert module.digest(path)==want
        assert len(probe.events)==3
        return {'oracle_sha256':want,'distinct_literal_full_reads':3,'hardlink_nlink':p.stat().st_nlink}
    run('identical_SHA_distinct_files_and_hardlink_literals',distinct)
    def aliases(folder,probe):
        other=folder/'other';other.mkdir();nested=other/'nested';nested.mkdir()
        p=other/'input.bin';want=make_file(p,1225)
        first=folder/'one.link';first.symlink_to(Path('other/input.bin'))
        second=folder/'two.link';second.symlink_to('one.link')
        directory=folder/'dir.link';directory.symlink_to('other/nested',target_is_directory=True)
        spelling=directory/'..'/'input.bin'
        assert sha(spelling)==want
        with module.complete_environment_digest_context({str(first):str(p.resolve())}):
            for path in [p,first,second,spelling]:assert module.digest(path)==want
        assert len(probe.events)==4
        return {'oracle_sha256':want,'literal_paths':[str(x) for x in [p,first,second,spelling]],'separate_full_reads':4,'dotdot_OS_semantics_retained':True}
    run('allowed_relative_links_multihop_and_symlink_dotdot',aliases)
    def relative(folder,probe):
        p=folder/'input.bin';want=make_file(p,1441)
        link=folder/'relative.link';link.symlink_to(p.name)
        previous=os.getcwd()
        try:
            os.chdir(folder)
            with module.complete_environment_digest_context({}):
                assert module.digest(Path('relative.link'))==want
                assert module.digest(Path('relative.link'))==want
            assert len(probe.events)==1 and probe.events[0]['literal']=='relative.link'
        finally:os.chdir(previous)
        return {'oracle_sha256':want,'fixed_scope_cwd':str(folder),'relative_literal_fresh_full_read':1}
    run('original_relative_path_in_explicit_context',relative)
    def conflict(folder,probe):
        p=folder/'input.bin';want=make_file(p)
        def attempt():
            with module.complete_environment_digest_context({}):
                module.require(p,want);module.require(p,'0'*64)
        error=reject(attempt,'missing or changed declared file:')
        assert len(probe.events)==1
        return error
    run('same_literal_conflicting_expected_SHA',conflict)
    def missing(folder,probe):
        d=environment_declaration({str(folder/'absent.bin'):'0'*64},aliases={str(folder/'also_missing.link'):str(folder/'target.bin')})
        return reject(lambda:inside_environment(module,d),'missing or changed declared file:')
    run('missing_file_and_badalias_files_first_order',missing)
    def namespace(folder,probe):
        tree=folder/'namespace';tree.mkdir();p=tree/'input.bin';want=make_file(p)
        d=environment_declaration({str(p):want},[{'root':str(tree),'inventory':{'files':{'input.bin':want},'symlinks':{}}}])
        extra=tree/'extra.bin';make_file(extra)
        error=reject(lambda:inside_environment(module,d),'preserved predecessor namespace or hash changed:')
        return {'rejection':error,'unexpected_member':str(extra)}
    run('whole_original_namespace_unexpected_member',namespace)
    def alias_change(folder,probe):
        p=folder/'first.bin';q=folder/'second.bin';want=make_file(p);make_file(q)
        link=folder/'alias.link';link.symlink_to(p.name)
        def attempt():
            with module.complete_environment_digest_context({str(link):str(p.resolve())}):
                module.require(link,want);link.unlink();link.symlink_to(q.name);module.digest(link)
        return reject(attempt)
    run('same_SHA_alias_retarget_before_duplicate',alias_change)
    def native_exit(folder,probe):
        p=folder/'first.bin';q=folder/'second.bin';make_file(p);make_file(q)
        link=folder/'unhashed_native.link';link.symlink_to(p.name)
        d=environment_declaration({},aliases={str(link):str(p.resolve())})
        def attempt():
            with module.complete_environment_digest_context(d['native_library_aliases']):
                module.environment(d);link.unlink();link.symlink_to(q.name)
        error=reject(attempt)
        assert len(probe.events)==0
        return {'rejection':error,'alias_had_no_digest_owner':True}
    run('late_unhashed_native_alias_retarget',native_exit)
    def mutation(mode):
        def action(folder,probe):
            p=folder/'input.bin';make_file(p,10003)
            def change():
                if mode=='truncate':
                    with p.open('r+b') as stream:stream.truncate(3)
                elif mode=='replace':
                    q=folder/'replacement.bin';make_file(q,10003,1);os.replace(q,p)
                else:
                    with p.open('r+b') as stream:stream.seek(500);stream.write(b'changed')
                    before=p.stat();os.utime(p,ns=(before.st_atime_ns,before.st_mtime_ns+1000000))
            probe.plans[str(p)]={'max_piece':7,'after_first_read':change}
            def attempt():
                with module.complete_environment_digest_context({}):module.digest(p)
            return reject(attempt)
        return action
    for mode in ['truncate','replace','rewrite']:run('during_stream_'+mode,mutation(mode))
    def late_file(folder,probe):
        p=folder/'input.bin';make_file(p)
        def attempt():
            with module.complete_environment_digest_context({}):
                module.digest(p);v=p.stat();os.utime(p,ns=(v.st_atime_ns,v.st_mtime_ns+1000000))
        return reject(attempt)
    run('late_identity_change_at_context_exit',late_file)
    def reset(folder,probe):
        p=folder/'input.bin';want=make_file(p)
        for _ in range(2):
            with module.complete_environment_digest_context({}):assert module.digest(p)==want
            context_cleared(module)
        captured=[]
        class Marker(Exception):pass
        try:
            with module.complete_environment_digest_context({}):
                module.digest(p);captured.append(module._ENV_STREAM_ACTIVE_CONTEXT);raise Marker('original sentinel exception')
        except Marker as error:assert str(error)=='original sentinel exception'
        context_cleared(module)
        assert captured[0]['active'] is False and captured[0]['memo']=={} and captured[0]['buffer'] is None and captured[0]['view'] is None
        with module.complete_environment_digest_context({}):assert module.digest(p)==want
        assert len(probe.events)==4
        return {'fresh_scope_full_reads':4,'original_exception_preserved':True,'private_retained_buffer_and_memo_empty':True}
    run('success_and_exception_scope_reset',reset)
    def nested(folder,probe):
        p=folder/'input.bin';want=make_file(p)
        with module.complete_environment_digest_context({}):
            owner=module._ENV_STREAM_ACTIVE_CONTEXT
            def attempt():
                with module.complete_environment_digest_context({}):raise AssertionError('nested body must not run')
            error=reject(attempt,'nested or concurrent')
            assert module._ENV_STREAM_ACTIVE_CONTEXT is owner and module.digest(p)==want
        return error
    run('nested_scope_rejected_parent_stays_valid',nested)
    def foreign(folder,probe):
        p=folder/'input.bin';make_file(p);errors=[]
        with module.complete_environment_digest_context({}):
            worker=threading.Thread(target=lambda:errors.append(reject(lambda:module.digest(p))))
            worker.start();worker.join(timeout=2);assert not worker.is_alive()
        assert len(errors)==1 and not probe.events
        return errors[0]
    run('wrong_thread_access_rejected',foreign)
    def default(folder,probe):
        p=folder/'input.bin';old=make_file(p);assert module.digest(p)==old
        with p.open('r+b') as stream:stream.write(b'changed')
        want=sha(p);assert want!=old and module.digest(p)==want
        context_cleared(module)
        return {'oracle_before':old,'oracle_after':want,'default_no_context_fresh':True}
    run('default_outside_context_fresh',default)
    def no_namespace_skip(folder,probe):
        tree=folder/'namespace';tree.mkdir();p=tree/'input.bin';want=make_file(p)
        link=tree/'link';link.symlink_to(p.name)
        d=environment_declaration({str(p):want},[{'root':str(tree),'inventory':{'files':{'input.bin':want},'symlinks':{'link':'input.bin'}}}])
        inside_environment(module,d);link.unlink();link.symlink_to('missing.bin')
        return reject(lambda:inside_environment(module,d),'preserved predecessor namespace or hash changed:')
    run('preserved_namespace_link_word_change',no_namespace_skip)
    return {'schema':'AXMAT_V14_HELPER_ONLY_FIXTURE_RESULT_V1','status':'PASS_HELPER_PROTOCOL_ONLY','groups':records,
        'numeric_component_stage_count_increment':0,'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False}

def historical_environment_comparison(new,out):
    """Optional full old->new read, subject to SAME external120s/512MiB watchdog.

    No old module globals are patched. Python profile observes the unmodified
    stdlib file_digest complete FD stream, and the new private adapter is probed.
    Timing includes instrumentation and is not an unbiased isolated bandwidth test.
    """
    before=identity(DECL);assert sha(DECL)==DECL_SHA256
    full=json.loads(DECL.read_text())
    fields=('files','preserved_predecessors','build_python_executable','native_library_aliases','numerical_loader_environment')
    d={key:full[key] for key in fields}
    old,oldpin=load_canonical(ORIGINAL,ORIGINAL_SHA256,'axmat_v14_controls_original619_environment_only')
    events=[];active={}
    hashcode=hashlib.file_digest.__code__
    def profile(frame,event,arg):
        if frame.f_code is not hashcode:return
        if event=='call':
            stream=frame.f_locals['fileobj'];info=os.fstat(stream.fileno())
            active[id(frame)]={'path':str(stream.name),'opened_fd_size':info.st_size,'initial_tell':stream.tell(),'readinto_calls':0}
        elif event=='c_call' and getattr(arg,'__name__',None)=='readinto':
            active[id(frame)]['readinto_calls']+=1
        elif event=='return':
            item=active.pop(id(frame));stream=frame.f_locals['fileobj'];item['final_tell']=stream.tell()
            item['actual_complete_bytes']=item['final_tell']-item['initial_tell']
            assert item['actual_complete_bytes']==item['opened_fd_size']
            events.append(item)
    assert sys.getprofile() is None
    started=time.monotonic();sys.setprofile(profile)
    try:old.environment(d)
    finally:sys.setprofile(None)
    oldelapsed=time.monotonic()-started
    assert not active and events
    context_cleared(new)
    with NewHelperOpenProbe(new) as probe:
        started=time.monotonic();inside_environment(new,d);newelapsed=time.monotonic()-started
    context_cleared(new)
    assert identity(DECL)==before and sha(DECL)==DECL_SHA256
    return {'schema':'AXMAT_V14_OPTIONAL_ACTUAL_FULL_ENVIRONMENT_READING_COMPARISON_V1','status':'BOTH_COMPLETE_ENVIRONMENT_PREDICATES_RETURNED',
        'original619_source':oldpin,'declaration':{'path':str(DECL),'sha256':DECL_SHA256,'identity':before},
        'exact_environment_input_fields':list(fields),'original_preserved_namespace_count':len(d['preserved_predecessors']),
        'old_elapsed_seconds_including_profile':oldelapsed,'new_elapsed_seconds_including_open_probe':newelapsed,
        'old_actual_FD_full_EOF_stream_observations':events,'new_actual_FD_full_EOF_stream_observations':probe.events,
        'old_actual_full_byte_volume':sum(x['actual_complete_bytes'] for x in events),
        'new_actual_full_byte_volume':sum(x['bytecount'] for x in probe.events),
        'new_all_streams_EOF_and_total_size_equal':all(x['EOF_observed'] and x['bytecount']==x['opened_fd_size'] for x in probe.events),
        'old_helper_globals_unmodified':True,'helper_only_observer_overhead_not_removed':True,
        'not_V13_failed_audit_reexecution':True,'not_component_or_native_or_AAA_qualification':True}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--action',choices=('fixtures','historical-environment'),default='fixtures')
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    if STATUS!='READY_ROOT_BOUND_CANONICAL_HELPER_SOURCE_ONLY' or type(HELPER_SHA256) is not str or len(HELPER_SHA256)!=64:
        raise ValueError('UNREADY: reviewed canonical helper SHA and source admission must be explicitly bound by Root')
    assert sys.dont_write_bytecode and all(os.environ.get(k)=='1' for k in THREAD_KEYS)
    out=Path(args.out)
    assert out.is_absolute() and out.parent==PROJECT/'validation/artifacts' and out.name.startswith(OUT_PREFIX)
    assert not os.path.lexists(out)
    module,pin=load_canonical(HELPER,HELPER_SHA256,'axmat_v14_streaming_helper_unit_controls')
    assert hasattr(module,'_env_stream_open') and hasattr(module,'complete_environment_digest_context')
    assert module._ENV_STREAM_BUFFER_BYTES==EXPECTED_BUFFER_BYTES
    out.mkdir()
    started=time.monotonic()
    result=(fixture_controls(module,out) if args.action=='fixtures' else historical_environment_comparison(module,out))
    result.update(source=pin,action=args.action,elapsed_seconds=time.monotonic()-started,
        Root_external_watchdog_required={'wall_seconds':120,'rss_mib':512,'children_at_once':1,'retries':0,'threads':1},
        archive_cap_bytes=MAX_ARCHIVE_BYTES,numerical_controls_compiler_or_API_invoked=False)
    assert sum(p.stat().st_size for p in out.rglob('*') if p.is_file())<MAX_ARCHIVE_BYTES
    assert sha(HELPER)==HELPER_SHA256 and identity(HELPER)==pin['identity']
    write_json(out/'result.json',result)
    files={str(p.relative_to(out)):sha(p) for p in out.rglob('*') if p.is_file() and not p.is_symlink()}
    write_json(out/'raw_preservation_manifest.json',{'schema':'AXMAT_HELPER_ONLY_CONTROL_RAW_PRESERVATION_V1','files':files,
        'component_native_AAA_ABA_credit':False,'original86_stage_count_increment':0})
    print(json.dumps({'status':result['status'],'action':args.action,'result_sha256':sha(out/'result.json'),
        'Root_actual_child_terminal_required_before_admission':True},allow_nan=False),flush=True)

if __name__=='__main__':main()
