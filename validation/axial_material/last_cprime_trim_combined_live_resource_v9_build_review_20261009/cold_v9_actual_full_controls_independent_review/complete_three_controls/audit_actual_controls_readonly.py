"""Fixed V9 controls reader. No business import, child, callback or science credit.

The default SOURCE_ONLY config is unexecutable. Only Root's genuine closed
terminal observation and qualified actual binding pins may fill its null slots.
Large expected owners retain whole scope through the immutable identity stream
and the separately qualified complete binding; their science bytes are not read.
"""
from pathlib import Path
import ast,hashlib,json,math,os,shutil,stat,struct,sys,types

BASE=Path(__file__).resolve().parent
ART=Path('/Users/wen/spot/validation/artifacts')
KEYS=('dev','ino','mode','size','mtime_ns','ctime_ns','nlink')
CAPS=dict(rss_cap_mib=512,control_stage_seconds=60,control_total_seconds=120,
          control_archive_reserve_bytes=64*2**20,cold_total_seconds=43200,
          min_free_bytes=8*2**30,history_cap_bytes=96*2**30,threads=1,children_at_once=1,retries=0)
SCHEMA='AXMAT_COMBINED_PHYSICAL_MEMORY_CANONICAL_OWN_RSS_BINDING_V1'
CONTROL_SCHEMA='AXMAT_COMBINED_PHYSICAL_MEMORY_CANONICAL_GUARD_CONTROLS_V1'
SEAL_SCHEMA='AXMAT_COMBINED_PHYSICAL_MEMORY_CANONICAL_GUARD_SEAL_V1'
TERMINAL_SCHEMA='AXMAT_COMBINED_PHYSICAL_MEMORY_CANONICAL_GUARD_ACTUAL_TERMINAL_V1'
TAIL=('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')
CONTRACT='EXACT_OWN_PID_DARWIN_WAIT4_BYTES_AND_LIVE_PS_V1'
REASON='own-child 512 MiB RSS cap reached'
MARKER='POSITIVE_NEW_CANONICAL_OWN_CHILD_CONTROL_COMPLETE'
READ_PINS=[]
SOURCE_EXPECTED={}
def check(value,reason):
    if not value:raise ValueError(reason)
def sha(value):
    check(type(value)is str and len(value)==64 and value!='0'*64 and all(c in '0123456789abcdef' for c in value),'real SHA required');return value
def sid(p):return [getattr(p.lstat(),'st_'+k) for k in KEYS]
def regular(p):
    p=Path(p);check(p.is_absolute() and '..' not in p.parts,'absolute canonical path required')
    for q in (p,*p.parents):
        st=q.lstat();check(not stat.S_ISLNK(st.st_mode),'symlink input')
        check(stat.S_ISREG(st.st_mode) if q==p else stat.S_ISDIR(st.st_mode),'canonical regular endpoint/ancestors required')
    return p
def require(path):
    p=regular(path);check(str(p) in SOURCE_EXPECTED,'compile source lacks independently expected owner')
    data(p,SOURCE_EXPECTED[str(p)]);return p
def data(p,wanted=None):
    p=regular(p);before=sid(p);raw=p.read_bytes();check(sid(p)==before,'read identity changed')
    h=hashlib.sha256(raw).hexdigest()
    if wanted is not None:check(h==sha(wanted),'actual pin differs: '+str(p))
    READ_PINS.append(dict(path=str(p),sha256=h,bytes=len(raw)));return raw
def descriptor(d):
    check(type(d)is dict and set(d)=={'path','sha256'},'exact path/SHA descriptor required');sha(d['sha256']);data(d['path'],d['sha256']);return Path(d['path'])
def pairs(rows):
    result={}
    for k,v in rows:check(k not in result,'duplicate JSON key');result[k]=v
    return result
def strict(p,wanted=None):
    def number(t):
        v=float(t);check(math.isfinite(v),'nonfinite JSON float');return v
    def constant(t):raise ValueError('nonfinite JSON constant '+t)
    v=json.loads(data(p,wanted),object_pairs_hook=pairs,parse_float=number,parse_constant=constant)
    check(type(v)is dict,'JSON object required');return v
def ns(root):
    check(root.is_dir() and not root.is_symlink(),'whole archive directory required');files={};dirs=[]
    for folder,ds,names in os.walk(root,followlinks=False):
        check(not any((Path(folder)/n).is_symlink() for n in ds+names),'archive alias')
        dirs.extend(str((Path(folder)/n).relative_to(root)) for n in ds)
        for n in names:
            p=Path(folder)/n;raw=data(p);files[str(p.relative_to(root))]=hashlib.sha256(raw).hexdigest()
    return dict(files=files,directories=sorted(dirs))
def owner_identity_stream(b):
    mapping=dict(b['files'])
    for p,w in b['producer_environment']['files'].items():
        check(p not in mapping or mapping[p]==w,'environment owner conflict');mapping[p]=w
    for owners in (b['runtime_module_owners'],b['module_owners']):
        check(type(owners)is dict,'whole module owner map required')
        for d in owners.values():check(set(d)=={'path','sha256'} and mapping.get(d['path'])==d['sha256'],'module owner not in complete files')
    h=hashlib.sha256(); filemap=hashlib.sha256()
    for p,w in sorted(mapping.items()):
        sha(w);ep=regular(p)
        h.update(json.dumps([p,w,sid(ep)],separators=(',',':'),ensure_ascii=False).encode()+b'\n')
        filemap.update(json.dumps([p,w],separators=(',',':'),ensure_ascii=False).encode()+b'\n')
    return dict(paths=len(mapping),expected_filemap_sha256=filemap.hexdigest(),seven_field_identity_sha256=h.hexdigest())
def definition(path,name):
    text=data(path).decode();matches=[n for n in ast.parse(text).body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name==name]
    check(len(matches)==1,'unique source definition required');return ast.get_source_segment(text,matches[0])

# Pure code encoding functions are inserted byte-exact from the reviewed host.
# compile() derives code only; no code object or business module is executed.

CODE_IDENTITY_ENCODING = 'AXMAT_TYPED_COMPLETE_CODETYPE_CONSTRUCTOR_FIELDS_V1'


CODE_CONSTRUCTOR_FIELDS = (
    'co_argcount','co_posonlyargcount','co_kwonlyargcount','co_nlocals',
    'co_stacksize','co_flags','co_code','co_consts','co_names','co_varnames',
    'co_filename','co_name','co_qualname','co_firstlineno','co_linetable',
    'co_exceptiontable','co_freevars','co_cellvars')


def compiled_code(path, class_name, member):
    """Derive code from pinned source without executing the compiled module."""
    source = require(path).read_text()
    code = compile(source, str(path), 'exec', dont_inherit=True, optimize=0)
    constants = code.co_consts
    if class_name is not None:
        classes = [n for n in constants if isinstance(n, types.CodeType) and n.co_name == class_name]
        if len(classes) != 1:
            raise ValueError('one pinned class code object required')
        constants = classes[0].co_consts
    functions = [n for n in constants if isinstance(n, types.CodeType) and n.co_name == member]
    if len(functions) != 1:
        raise ValueError('one pinned callable code object required')
    return functions[0]


def canonical_code_value(value):
    """Exact constructor fields and typed constants, without reference flags."""
    if type(value) is types.CodeType:
        return ['code',[[name,canonical_code_value(getattr(value,name))]
                        for name in CODE_CONSTRUCTOR_FIELDS]]
    if value is None:return ['None']
    if value is Ellipsis:return ['Ellipsis']
    if type(value) is bool:return ['bool',value]
    if type(value) is int:return ['int',str(value)]
    if type(value) is float:return ['float',struct.pack('!d',value).hex()]
    if type(value) is complex:
        return ['complex',struct.pack('!d',value.real).hex(),struct.pack('!d',value.imag).hex()]
    if type(value) is str:return ['str',value]
    if type(value) is bytes:return ['bytes',value.hex()]
    if type(value) is tuple:return ['tuple',[canonical_code_value(v)for v in value]]
    if type(value) is frozenset:
        items=[canonical_code_value(v)for v in value]
        return ['frozenset',sorted(items,key=lambda item:json.dumps(item,ensure_ascii=True,
                                    sort_keys=True,separators=(',',':'),allow_nan=False))]
    if type(value) is slice:
        return ['slice',canonical_code_value(value.start),canonical_code_value(value.stop),
                canonical_code_value(value.step)]
    raise ValueError('unsupported independently compiled code constant kind')


def canonical_code_bytes(code):
    if type(code) is not types.CodeType:
        raise ValueError('a genuine complete compiled code object required')
    return json.dumps([CODE_IDENTITY_ENCODING,canonical_code_value(code)],ensure_ascii=True,
                      sort_keys=True,separators=(',',':'),allow_nan=False).encode('ascii')


def expected_mro(b):
    c=Path(b['controller']['path']);full=Path(b['own_rss_source']['path']);probe=Path(b['module_owners']['probe_refined_AAA_white_odd_response']['path'])
    codes={}
    for label,path,cls,member in [*( (n,c,'SerialExecutor',n) for n in ('__init__','execute','_process')),('OwnRSS._process',full,'OwnRSSSerialExecutor','_process'),('write_new',probe,None,'write_new'),*((n,c,None,n) for n in ('resource_monitor','run','qualify_aba','dump_json','check_dragon_log','sha256'))]:
        codes[label]=hashlib.sha256(canonical_code_bytes(compiled_code(path,cls,member))).hexdigest()
    return dict(controller=b['controller'],serial_baseline=b['serial_baseline'],own_rss_source=b['own_rss_source'],canonical_controller_name='production_runner',actual_direct_bases=['production_runner.SerialExecutor'],inherited_original_init=True,inherited_original_execute=True,entire_SerialExecutor_source_byte_exact=True,actual_compiled_callable_sha256=codes,actual_original_process_globals_identity=True,existing_guard_is_prior_proof_only=True,new_binding_fixture_pass_claimed=False,module_global_or_class_overlay=False)
def peak(w,mode):
    required={'pid','returncode','sampled_peak_rss_mib','limit_failure','rss_cap_mib','own_pid_wait4_observed','own_pid_wait4_pid','own_pid_wait4_status','own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib','observed_peak_rss_mib','live_rss_sample_count','rss_peak_observation_contract'}
    check(required.issubset(w) and sys.platform=='darwin' and w['rss_cap_mib']==512 and type(w['pid'])is int and w['pid']>0 and type(w['returncode'])is int and type(w['own_pid_wait4_observed'])is bool and w['rss_peak_observation_contract']==CONTRACT,'ownPID contract')
    sampled=w['sampled_peak_rss_mib'];observed=w['observed_peak_rss_mib'];count=w['live_rss_sample_count'];kernel=w['own_pid_wait4_peak_rss_mib']
    check(all(type(x)in(int,float) and math.isfinite(x) and x>=0 for x in (sampled,observed)) and type(count)is int and count>=0 and not(count==0 and sampled!=0),'finite own samples')
    if w['own_pid_wait4_observed']:
        pid=w['own_pid_wait4_pid'];status=w['own_pid_wait4_status'];raw=w['own_pid_wait4_ru_maxrss_bytes']
        check(type(pid)is int and pid==w['pid'] and type(status)is int and 0<=status<=65535 and (os.WIFEXITED(status) or os.WIFSIGNALED(status)) and os.waitstatus_to_exitcode(status)==w['returncode'],'exact own wait4 terminal PID/status')
        check(type(raw)in(int,float) and math.isfinite(raw) and raw>0 and raw==int(raw) and type(kernel)in(int,float) and math.isfinite(kernel) and kernel>0 and kernel==raw/(1024.*1024.),'Darwin ownPID integer BYTES/kernelMiB')
    else:check(all(w[k]is None for k in ('own_pid_wait4_pid','own_pid_wait4_status','own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib')),'missing receipt carries invented values')
    check(observed==max(sampled,kernel if kernel is not None else 0.),'observed is not exact maximum')
    if mode in ('positive','short'):
        check(w['returncode']==0 and w['limit_failure']is None and w['own_pid_wait4_observed']is True and 0<observed<512,'normal ownPID completion proof')
        if mode=='short':check(kernel>=16,'short actual16MiB own kernel proof')
    else:check(w['returncode']in(-15,-9) and sampled>=512 and observed>=512 and w['limit_failure']==repr(RuntimeError(REASON)),'original actual oversize RSS rejection')
    return dict(pid=w['pid'],sampled_peak_rss_mib=sampled,own_pid_wait4_peak_rss_mib=kernel,observed_peak_rss_mib=observed,own_pid_wait4_observed=w['own_pid_wait4_observed'])
def resources(r,b):
    check(r['artifact_budget_bytes']==96*2**30 and r['min_free_bytes']==8*2**30 and type(r['artifact_bytes'])is int and r['artifact_bytes']<=96*2**30 and type(r['disk_free_bytes'])is int and r['disk_free_bytes']>=8*2**30 and r['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and 'reason' not in r,'original whole history/free resource tail')
    check(r['declared_resource_roots']==b['resource_info']['resource_roots'],'declared extras narrowed')
    roots=sorted(set(r['declared_resource_roots'])|{str(p) for p in ART.glob('axial-material-*')})
    # CT is created only by the record-after-terminal Root writer. All old
    # roots remain mandatory; only that independently witnessed new CT may
    # be absent from the earlier actual controls tail when not declared.
    earlier_without_CT=[p for p in roots if p!=b['control_terminal_root'] or p in r['declared_resource_roots']]
    check(r['resource_roots']==roots or r['resource_roots']==earlier_without_CT,'dynamic complete roots differ beyond post-tool CT')
    for p in roots:
        q=Path(p);check(q.is_absolute() and q!=ART and q.is_relative_to(ART) and '..' not in q.parts,'strict history root');cursor=q
        while cursor!=ART:
            check(not cursor.is_symlink() and (not cursor.exists() or cursor.is_dir()),'history root alias');cursor=cursor.parent
    return roots
def current_resources(roots):
    total=count=0
    for root in roots:
        q=Path(root)
        if not q.exists():continue
        for folder,ds,ns_ in os.walk(q,followlinks=False):
            ds[:]=[n for n in ds if not (Path(folder)/n).is_symlink()]
            for n in ns_:
                try:s=(Path(folder)/n).lstat()
                except FileNotFoundError:continue
                if stat.S_ISREG(s.st_mode):total+=s.st_size;count+=1
    free=shutil.disk_usage(ART).free;check(total<=96*2**30 and free>=8*2**30,'fresh metadata96/free8 refusal')
    return dict(artifact_bytes=total,regular_files=count,disk_free_bytes=free,resource_scope_policy='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1',recorded_tail_not_required_to_equal_later_Root_receipt_growth=True)
def main():
    check(BASE==Path('/private/tmp/axmat_v9_cold_actual_controls_postterminal_reader_20261009'),'fixed TMP-only actual report destination required')
    check(len(sys.argv)==2,'fixed actual bound config path required');cfg=strict(sys.argv[1]);f=cfg['future_actual']
    check(cfg['status']=='ROOT_ACTUAL_CONTROLS_EXIT0_READY_FOR_INDEPENDENT_READONLY_REVIEW' and f['Root_explicit_closed_controls_EXIT0_observed']is True and f['actual_tool_result']is not None,'SOURCE_ONLY / real controls terminal not supplied')
    actual=f['actual_tool_result'];check(type(actual)is dict and set(actual)=={'initial_chunk_id','session_id','terminal_chunk_id','exit_code'} and type(actual['exit_code'])is int and actual['exit_code']==0 and all(type(actual[k])is str and actual[k] for k in ('initial_chunk_id','terminal_chunk_id')) and (actual['session_id']is None or type(actual['session_id'])is int and actual['session_id']>0),'genuine Root four-key tool EXIT0')
    check(sys.version_info[:3]==(3,14,4) and sys.flags.optimize==0 and 'PYTHONOPTIMIZE' not in os.environ,'original Py3144 compiled-code environment required')
    for p,w in cfg['known_source_pins'].items():data(p,w)
    joint_path=descriptor(f['qualified_binding_joint_review']);joint=strict(joint_path)
    check(joint.get('schema')=='AXMAT_ROOT_V9_ACTUAL_COLD_BINDING_FULL_COMPLEMENTARY_ADMISSION_V1' and f['qualified_binding_joint_review']['sha256']==cfg['known_Root_qualified_binding_joint_sha256'],'exact genuinely admitted whole binding source/graph/joint witness required')
    work=Path(cfg['work']);binding=dict(path=str(work/'own_rss_binding.json'),sha256=cfg['known_binding_sha256']);b=strict(binding['path'],binding['sha256'])
    check(b['schema']==SCHEMA and b['caps']==CAPS and b['work_root']==str(work) and b['control_terminal_root']==cfg['control_terminal'] and b['scientific_qualification']is False and b['module_global_or_class_overlay']is False and b['canonical_controller_name']=='production_runner','whole new binding')
    check(owner_identity_stream(b)==cfg['immutable_complete_owner_identity'],'whole expected binding/environment owner identity changed')
    SOURCE_EXPECTED.update(b['files'])
    for key in ('controller','host','controls_source','bounded_helper','serial_baseline','own_rss_source','guard_factory','resource_class_source'):
        descriptor(b[key]);check(b['files'].get(b[key]['path'])==b[key]['sha256'],'binding owner not declared')
    for d in b['tested_guard_files']:descriptor(d);check(b['files'].get(d['path'])==d['sha256'],'guard owner omitted')
    runtime=ns(work/'runtime');check(runtime['directories']==[] and runtime['files']==b['runtime_namespace']['files'] and b['runtime_namespace']['directories']==[],'complete runtime changed')
    base=Path(b['serial_baseline']['path']);c=Path(b['controller']['path'])
    for name in ('SerialExecutor','resource_monitor','qualify_aba'):check(definition(base,name)==definition(c,name),'original full class/resource/science definition changed')
    root=work/'binding_controls';whole=ns(root);seal=strict(root/'seal.json',f['control_seal_sha256'])
    check(seal['schema']==SEAL_SCHEMA and whole['directories']==seal['namespace_directories'] and set(whole['files'])==set(seal['files'])|{'seal.json'} and all(whole['files'][p]==w for p,w in seal['files'].items()) and 'failure.json' not in whole['files'],'whole sealed actual controls')
    result=strict(root/'result.json',f['control_result_sha256']);claim=strict(root/'claim.json');stages=strict(root/'stages.json')['stages']
    check(set(claim)=={'schema','pid','binding','started_unix','retries','scientific_qualification'} and claim['schema']==CONTROL_SCHEMA and type(claim['pid'])is int and claim['pid']>0 and type(claim['started_unix'])in(int,float) and math.isfinite(claim['started_unix']) and claim['started_unix']>0 and type(claim['retries'])is int and claim['retries']==0 and claim['binding']==binding and claim['scientific_qualification']is False,'exclusive actual claim')
    check(result['schema']==CONTROL_SCHEMA and result['classification']=='PASS_NEW_CANONICAL_OWN_RSS_BINDING_CONTROLS_ONLY' and result['binding']==binding and result['caps']==CAPS and all(result[k]is True for k in ('positive_completed','actual_oversize_rejected','short_completed','own_children_no_longer_live')) and all(result[k]is False for k in ('scientific_qualification','Dragon_started','transport_started','new_assembly_or_linear_solve','AAA_accuracy_qualified','ABA_admitted')) and result['short_allocation_bytes']==16*2**20 and result['rss_peak_observation_contract']==CONTRACT,'actual three controls result only')
    source_identity=expected_mro(b);binding_stdout=strict(descriptor(f['binding_stdout']))
    check(binding_stdout['binding']==binding and binding_stdout['classification']=='PREPARED_NEW_CANONICAL_BINDING_INPUT_ONLY_NO_FIXTURE_CREDIT' and binding_stdout['new_binding_fixtures_executed']is False and binding_stdout['scientific_qualification']is False and binding_stdout['actual_source_identity']==source_identity and result['source_identity']==source_identity,'actual same canonical MRO/source/callable witness')
    helper=Path(b['bounded_helper']['path']);expected_helper=dict(source=b['bounded_helper'],actual_compiled_callable_sha256={n:hashlib.sha256(canonical_code_bytes(compiled_code(helper,None,n))).hexdigest() for n in ('start_liveness_watchdog','finish_liveness_watchdog','terminate_group','process_group_exists')},original_bounded_group_cleanup_code_identity=True,helper_globals_or_callable_overlay=False)
    check(result['actual_bounded_helper']==expected_helper,'actual original bounded cleanup callable proof')
    builder=Path(b['module_owners']['prepare_qualified_AB_rank1_cache_production']['path']);data(builder,b['files'][str(builder)])
    parent=next(n for n in ast.parse(builder.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='parent_factory')
    resource_alias=ast.literal_eval(parent.body[0].value.args[1])
    check(b['module_owners'][resource_alias]==b['resource_class_source'],'actual lazy resource alias owner lineage')
    check(result['actual_resource_class']==dict(class_module=resource_alias,class_source=b['resource_class_source'],class_name='DynamicHistoryResources',no_class_or_resource_overlay=True),'actual original resource class')
    modes=['positive','oversize','short'];check([q['mode'] for q in result['observations']]==modes and [q['label'] for q in stages]==['binding_controls/'+m+'/execute' for m in modes] and [q['status'] for q in stages]==['PASS','FAILED','PASS'],'exact original ordered three stages')
    peaks=[]
    for mode,stage,obs in zip(modes,stages,result['observations']):
        cmd=[b['producer_environment']['executable'],b['controls_source']['path'],'fixture',mode];wp=descriptor(obs['watchdog']);lp=descriptor(obs['raw_log']);w=strict(wp)
        check(wp==root/mode/'execute.watchdog.json' and lp==root/mode/'execute.log' and w==obs['watch'],'raw evidence identity')
        check(stage['command']==obs['command']==w['command']==cmd and w['own_child_only']is True and w['liveness_group_cleanup']is True and obs['actual_group_no_longer_live']is True and 0<w['wall_cap_seconds']<=stage['wall_cap_seconds']<=60 and 0<=w['elapsed_seconds']<w['wall_cap_seconds'],'actual own command/stage limits/cleanup')
        lines=data(lp).decode().splitlines();check(lines,'allocation intent missing');allocation=json.loads(lines[0],object_pairs_hook=pairs)
        check(allocation==dict(kind='ACTUAL_OWN_CHILD_ALLOCATION_INTENT',mode=mode,pid=w['pid'],requested_bytes=576*2**20 if mode=='oversize' else 16*2**20),'actual own child allocation')
        if mode=='oversize':check(stage['error']==REASON and obs['actual_expected_rejection']==REASON,'actual original RSS rejection reason')
        else:check(MARKER in lines and stage['log_sha256']==obs['raw_log']['sha256'] and obs['actual_expected_rejection']is None,'positive/short raw marker and normal log')
        peaks.append(dict(mode=mode,**peak(w,mode)))
    terminal=Path(cfg['control_terminal']);check(terminal.parent==ART and not terminal.is_relative_to(work),'independent fixed CT root');e=strict(terminal/'terminal_return.json',f['control_terminal_sha256'])
    command=[b['producer_environment']['executable'],b['controls_source']['path'],'run-controls','--binding',binding['path'],'--binding-sha256',binding['sha256']]
    check(e['schema']==TERMINAL_SCHEMA and e['record_producer']=='root' and e['actual_tool_terminal_return_observed']is True and e['record_written_after_actual_terminal_return']is True and e['actual_tool_result']==actual and type(e['returncode'])is int and e['returncode']==0 and e['command']==command and e['binding']==binding and e['source']==b['controls_source'] and e['host']==b['host'] and e['control_seal']==dict(path=str(root/'seal.json'),sha256=f['control_seal_sha256']),'actual independent Root terminal')
    stdout=descriptor(e['full_stdout']);stderr=descriptor(e['full_stderr']);check(stdout.parent==stderr.parent==terminal and len({stdout,stderr,terminal/'terminal_return.json'})==3,'complete independent distinct stdio');returned=strict(stdout);tail={k:returned[k] for k in TAIL}
    archive=sum(regular(root/q).stat().st_size for q in whole['files'])+sum(regular(b[k]['path']).stat().st_size for k in ('host','controls_source'))+regular(binding['path']).stat().st_size
    check(returned==dict(result=result,**tail) and all(e[k]==tail[k] for k in TAIL) and tail['actual_tail_check']=='PASS' and type(tail['actual_elapsed_seconds'])in(int,float) and math.isfinite(tail['actual_elapsed_seconds']) and 0<tail['actual_elapsed_seconds']<120 and result['elapsed_before_closeout']<=tail['actual_elapsed_seconds'] and type(tail['actual_archive_bytes'])is int and tail['actual_archive_bytes']==archive<64*2**20,'exact whole stdout/four tail/archive<64MiB/whole<120s')
    roots=resources(tail['actual_resources'],b);resources(result['actual_resource_snapshot'],b);fresh_resource=current_resources(roots)
    check(owner_identity_stream(b)==cfg['immutable_complete_owner_identity'],'whole owners changed during independent review')
    report=dict(status='PASS_ACTUAL_NEW_CANONICAL_THREE_CONTROLS_ONLY',binding=binding,control_seal=e['control_seal'],Root_terminal=dict(path=str(terminal/'terminal_return.json'),sha256=f['control_terminal_sha256']),actual_Root_tool=actual,whole_namespace_files=len(whole['files']),expected_owner_paths=cfg['immutable_complete_owner_identity']['paths'],control_peaks=peaks,actual_four_tail=tail,dynamic_resource_roots=roots,fresh_independent_metadata_resources=fresh_resource,expected_oversize_FAILED_is_correct=True,scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_or_business_executed_by_reader=False,large_expected_science_bytes_not_rehashed=True,read_pins=READ_PINS)
    out=BASE/'actual_readonly_REPORT.json';check(not out.exists(),'one actual report no overwrite');out.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n');print(json.dumps(dict(status=report['status'],report=dict(path=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest()),science_credit=False),sort_keys=True))

if __name__=='__main__':main()
