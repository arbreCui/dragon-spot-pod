#!/usr/bin/env python3
"""Limited read-only postverification of genuine cache336 build or bit controls.

This file is only a Source draft until Root supplies real completed authorities.
It never imports Hosts, starts a compiler/solver, deletes files, or rereads science.
All fixed and inherited inputs receive two current7 checks. Explicit Source,
object/archive, metadata, log/watch and owned output pins receive full EOF SHA.
The calling agent must preserve this script's genuine tool result separately.
"""
import argparse,hashlib,json,math,os,resource,shlex,shutil,stat,time
from pathlib import Path

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
BUILD=REC/'native_rank1_cache336_build_host_source_v1_20261014'
BIT=REC/'native_rank1_cache336_budget_bit_control_host_source_v1_20261014'
SOURCE=REC/'native_rank1_exact_cache336_source_v1_20261014'
SF=SOURCE/'COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_FREEZE.json'
CAPS=dict(original_stage_wall_cap_seconds=600,whole_wall_cap_seconds=1800,
  SELF_and_each_own_child_RSS_cap_bytes=512*2**20,threads=1,children_at_once=1,
  retries=0,fresh_output_cap_bytes=2*2**30,history_cap_bytes=96*2**30,
  filesystem_floor_bytes=8*2**30,original_cold_reserve_bytes=20971764748)
START=time.monotonic()

def guard():
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20:
        raise RuntimeError('postverification original SELF512 cap')
    if time.monotonic()-START>=1800:
        raise RuntimeError('postverification original whole1800 cap')

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def ancestors(path):
    p=Path(path)
    if not p.is_absolute()or '..'in p.parts:raise RuntimeError('canonical absolute path')
    for q in reversed(p.parents):
        if not stat.S_ISDIR(q.lstat().st_mode):raise RuntimeError('ordinary nonsymlink ancestor '+str(q))

def normalize(p):
    v={k:p[k]for k in ('path','sha256','size_bytes','identity')}
    if not isinstance(v['path'],str)or not isinstance(v['sha256'],str)or len(v['sha256'])!=64 or \
       type(v['size_bytes'])is not int or v['size_bytes']<0 or not isinstance(v['identity'],list)or \
       len(v['identity'])!=7 or any(type(x)is not int for x in v['identity'])or v['identity'][4]!=v['size_bytes']:
        raise RuntimeError('exact typed four-field PF')
    int(v['sha256'],16);return v

def current7(p):
    p=normalize(p);q=Path(p['path']);ancestors(q);s=q.lstat()
    if not stat.S_ISREG(s.st_mode)or identity(s)!=p['identity']:raise RuntimeError('current7 changed '+str(q))
    guard();return p

def fullpin(path):
    q=Path(path);ancestors(q);a=q.lstat()
    if not stat.S_ISREG(a.st_mode):raise RuntimeError('regular fullEOF file '+str(q))
    ident=identity(a);h=hashlib.sha256();n=0;fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd))!=ident:raise RuntimeError('fullEOF opened7 changed')
        while True:
            b=os.read(fd,1024*1024)
            if not b:break
            h.update(b);n+=len(b);guard()
        if identity(os.fstat(fd))!=ident:raise RuntimeError('fullEOF FD changed')
    finally:os.close(fd)
    if identity(q.lstat())!=ident or n!=ident[4]:raise RuntimeError('fullEOF after7 changed')
    return dict(path=str(q),sha256=h.hexdigest(),size_bytes=n,identity=ident)

def verify(p):
    p=normalize(p)
    if fullpin(p['path'])!=p:raise RuntimeError('fullEOF SHA/current7 mismatch '+p['path'])
    return p

def load(p):
    p=verify(p)
    if p['size_bytes']>32*2**20:raise RuntimeError('bounded report/Source metadata JSON32MiB')
    q=Path(p['path']);fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:
        if identity(os.fstat(f.fileno()))!=p['identity']:raise RuntimeError('JSON opened7 changed')
        raw=f.read()
        if identity(os.fstat(f.fileno()))!=p['identity']:raise RuntimeError('JSON FD changed')
    if identity(q.lstat())!=p['identity']or hashlib.sha256(raw).hexdigest()!=p['sha256']:raise RuntimeError('JSON after7 changed')
    return json.loads(raw)

def unique(rows):
    table={}
    for row in rows:
        p=normalize(row)
        if p['path']in table and table[p['path']]!=p:raise RuntimeError('inconsistent repeated fullPF '+p['path'])
        table[p['path']]=p
    return list(table.values())

def number(v):return type(v)in(int,float)and math.isfinite(v)

def resource_snapshot(s,root,require_aux=False):
    if s['artifact_budget_bytes']!=96*2**30 or s['min_free_bytes']!=8*2**30 or \
       type(s['artifact_bytes'])is not int or not 0<=s['artifact_bytes']<=96*2**30 or \
       type(s['disk_free_bytes'])is not int or s['disk_free_bytes']<8*2**30:
        raise RuntimeError('original whole-family96/free8 snapshot')
    f=s['fresh_output']
    if f['artifact_budget_bytes']!=2*2**30 or f['min_free_bytes']!=8*2**30 or \
       f['resource_roots']!=[str(root)]or type(f['artifact_bytes'])is not int or \
       not 0<=f['artifact_bytes']<=2*2**30 or f['disk_free_bytes']<8*2**30:
        raise RuntimeError('original same-OUT fresh2/free8 snapshot')
    if require_aux:
        a=s['control_direct_auxiliary']
        if a['pending_bytes']!=8*2**20 or a['cap_bytes']!=128*2**20 or \
           type(a['auxiliary_bytes'])is not int or not 0<=a['auxiliary_bytes'] or \
           a['auxiliary_bytes']+a['pending_bytes']>a['cap_bytes']:
            raise RuntimeError('direct auxiliary128+pending8 exact snapshot')

def argv_bindings(argv,prefix):
    if len(argv)!=30 or argv[:12]!=prefix:raise RuntimeError('exact30 Root CLI prefix/arguments')
    result={}
    for i in range(12,30,6):
        token,path,sha_token,sha,seven_token,seven=argv[i:i+6]
        if not token.startswith('--')or not token.endswith('-summary'):raise RuntimeError('exact argument triplets')
        key=token[2:-8]
        if key in result or sha_token!='--'+key+'-sha256'or seven_token!='--'+key+'-seven-id':raise RuntimeError('ordered unique external PF triplet')
        pf=fullpin(path)
        if pf['sha256']!=sha or pf['identity']!=json.loads(seven):raise RuntimeError('Root actual argv external fullPF')
        result[key]=pf
    return result

def inventory(root):
    ancestors(root);s=root.lstat()
    if not stat.S_ISDIR(s.st_mode):raise RuntimeError('ordinary actual OUT root')
    files={};dirs={};stack=[root]
    while stack:
        q=stack.pop();before=identity(q.lstat());dirs[str(q)]=before
        fd=os.open(q,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            if identity(os.fstat(fd))!=before:raise RuntimeError('OUT directory opened7 changed')
            with os.scandir(fd)as entries:
                for e in entries:
                    p=q/e.name;t=e.stat(follow_symlinks=False)
                    if stat.S_ISDIR(t.st_mode):stack.append(p)
                    elif stat.S_ISREG(t.st_mode):
                        if t.st_nlink!=1 or t.st_uid!=os.getuid():raise RuntimeError('actual owning output UID/nlink1')
                        files[str(p)]=identity(t)
                    else:raise RuntimeError('actual OUT symlink/special entry')
            if identity(os.fstat(fd))!=before or identity(q.lstat())!=before:raise RuntimeError('OUT directory after7 changed')
        finally:os.close(fd)
        guard()
    return dict(files=files,directories=dirs)

def watch(root,record,expected):
    if record['command']!=expected or record['status']!='PASS'or record['wall_cap_seconds']!=600 or \
       not number(record['elapsed_seconds'])or not 0<record['elapsed_seconds']<600:
        raise RuntimeError('exact actual stage command/PASS600')
    wp=fullpin(root/(record['label']+'.watchdog.json'));w=load(wp);lp=fullpin(root/(record['label']+'.log'))
    if lp['sha256']!=record['log_sha256']or w['command']!=expected or type(w['returncode'])is not int or w['returncode']!=0 or \
       w['limit_failure']is not None or w['rss_cap_mib']!=512 or w['own_child_only']is not True or \
       w['liveness_group_cleanup']is not True or not number(w['sampled_peak_rss_mib'])or \
       not 0<=w['sampled_peak_rss_mib']<512 or not number(w['elapsed_seconds'])or not 0<w['elapsed_seconds']<600 or \
       not number(w['wall_cap_seconds'])or not 0<w['wall_cap_seconds']<=600:
        raise RuntimeError('true closed0 watch/noLimit/own-child512/liveness')
    return dict(record_label=record['label'],watch_pin=wp,log_pin=lp,actual_watch=w)

def bit_json(root,record):
    lp=fullpin(root/(record['label']+'.log'));rows=[]
    with Path(lp['path']).open('r',encoding='utf-8',errors='strict')as f:
        for line in f:
            if len(line)>65536:raise RuntimeError('actual JSON/log line cap')
            line=line.strip()
            if line.startswith('{')and line.endswith('}'):
                d=json.loads(line)
                if isinstance(d,dict)and d.get('status')=='ACTUAL_GENERIC_RANK1_CACHE336_BUDGET_COMPONENT_BIT_CONTROLS_COMPLETED_ONLY':rows.append(d)
    verify(lp)
    if len(rows)!=1:raise RuntimeError('one actual bit terminal JSON')
    d=rows[0]
    if type(d.get('actual_assertions'))is not int or d['actual_assertions']!=338 or \
       type(d.get('actual_SPOT1P64_calls'))is not int or d['actual_SPOT1P64_calls']!=121 or \
       any(d.get(k)is not False for k in ('formal_SN32_quadrature_equivalence','genuine_solver_qualified',
         'physics_qualified','AAA_qualified','ABA_admitted','goal_complete')):
        raise RuntimeError('338/121 exact bit terminal and unqualified scope')
    return d,lp

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--role',choices=('build','bit'),required=True)
    for name in ('report','Root-tools','Root-argv','Host-freeze','Source-freeze'):
        for suffix in ('summary','sha256','seven-id'):ap.add_argument('--'+name+'-'+suffix,required=True)
    ap.add_argument('--review-directory',required=True);a=ap.parse_args()
    def external(name):
        field=name.replace('-','_');pf=fullpin(getattr(a,field+'_summary'))
        if pf['sha256']!=getattr(a,field+'_sha256')or pf['identity']!=json.loads(getattr(a,field+'_seven_id')):raise RuntimeError('exact external '+name+' PF')
        return pf
    supplied={n:external(n)for n in ('report','Root-tools','Root-argv','Host-freeze','Source-freeze')}
    report_pin=supplied['report'];d=load(report_pin);rt=load(supplied['Root-tools']);ra=load(supplied['Root-argv']);hf=load(supplied['Host-freeze']);sf=load(supplied['Source-freeze']);root=Path(report_pin['path']).parent
    folder=BUILD if a.role=='build'else BIT
    hpath=folder/('COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_FREEZE.json'if a.role=='build'else'COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json')
    cli_path=folder/('ROOT_REVIEWABLE_EXACT_CACHE336_DRIVER_BUILD_ARGV.json'if a.role=='build'else'DECLARED_EXECUTION_INTERFACE.json')
    if supplied['Host-freeze']['path']!=str(hpath)or supplied['Source-freeze']['path']!=str(SF)or \
       d['actual_host_Source_freeze_pin']!=supplied['Host-freeze']or \
       d['original_caps']!=CAPS or d['failure']is not None or d['after_check_error']is not None or d['secondary_failures']!=[]or \
       d['final_report_resource_check_passed']is not True or d['original_guard_class']!='OwnRSSSerialExecutor'or d['original_guard_MRO_unchanged']is not True or \
       type(d['SELF_peak_bytes'])is not int or not 0<=d['SELF_peak_bytes']<512*2**20 or \
       not number(d['wall_seconds'])or not 0<d['wall_seconds']<1800:
        raise RuntimeError('exact selected actual report/HF/SF/caps/firstfailureNone')
    expected_hschema='COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_ONLY_FREEZE_V1'if a.role=='build'else'COMPLETE_NATIVE_RANK1_CACHE336_BUDGET_BIT_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1'
    if hf['schema']!=expected_hschema or hf['compiler_executed']is not False or hf['numerical_executed']is not False or \
       hf['Host_imported_or_executed']is not False or hf['selected_new_Fortran_Source_freeze_pin']!=supplied['Source-freeze']or \
       root!=Path(hf['planned_output_root'])or sf['schema']!='COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_ONLY_FREEZE_V1'or \
       sf['source_only']is not True or sf['compiled']is not False or sf['numerical_executed']is not False or \
       sf['Driver_single_literal_368_to336']is not True or sf['public_Driver_ABI_unchanged']is not True or sf['original_math_modified']is not False or \
       sf['internal_exact_cache_working_set_bytes']!=336*2**20 or sf['new_control_expected_assertions']!=338 or sf['new_control_expected_calls']!=121:
        raise RuntimeError('frozen exact Driver/control Source contract')
    terminal=rt['actual_terminal_return'];initial=rt['actual_initial_return']
    if type(terminal['exit_code'])is not int or terminal['exit_code']!=0 or terminal.get('session_id')is not None or \
       not isinstance(terminal['output'],str)or not isinstance(initial['output'],str)or \
       shlex.split(rt['exact_executed_command'])!=ra['argv']:
        raise RuntimeError('genuine actual Root terminal integer0/no session/exactargv; raw preserved')
    cli_pin=fullpin(cli_path);cli=load(cli_pin)
    prefix=cli['argv'][:12]if a.role=='build'else cli['python_environment_and_Host_prefix']
    if prefix[:9]!=['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1',
      'OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1']or \
       prefix[9:11]!=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B']or prefix[11]!=hf['host_source']['path']:
        raise RuntimeError('exact original environment/interpreter/own Host prefix')
    args=argv_bindings(ra['argv'],prefix)
    if args.get('source-freeze')!=supplied['Source-freeze']or args.get('host-freeze')!=supplied['Host-freeze']:
        raise RuntimeError('Root executed owning Source and Host actual PFs')
    if a.role=='build'and ra['argv']!=cli['argv']:raise RuntimeError('exact frozen build30 argv')
    if a.role=='bit'and(cli['planned_total_argv_count']!=30 or cli['mandatory_source_bindings']!={'source_freeze':supplied['Source-freeze'],'host_freeze':supplied['Host-freeze']}):raise RuntimeError('bit Source CLI exact bindings/30argv')
    fixed=unique(d['fixed_current_pins']);ft={p['path']:p for p in fixed};deps=unique(hf['dependencies'])
    mandatory=unique(deps+[hf['host_source'],supplied['Host-freeze'],supplied['Source-freeze']]+sf['files']+sf['original_source_pins'])
    for p in mandatory:
        if ft.get(p['path'])!=p:raise RuntimeError('whole HF/ownHost/SF selected row absent or altered in actual fixed')
    for p in fixed:current7(p)
    output=unique(d['output_pins']);owned=unique(d['owned_runtime_pins']);ot={p['path']:p for p in output}
    for p in owned:
        if ot.get(p['path'])!=p:raise RuntimeError('each actual owned fullPF retained in complete output')
    before_inventory=inventory(root)
    if set(before_inventory['files'])!={p['path']for p in output}|{report_pin['path']}:
        raise RuntimeError('complete actual OUT equals all published output plus actual summary')
    plan_field='build_plan_pin'if a.role=='build'else'control_host_plan_pin'
    # Explicit own/source authorities only. Neither a suffix scan nor every
    # inherited JSON is promoted to a fresh scientific-body SHA requirement.
    full_rows=unique(output+[report_pin,cli_pin]+list(supplied.values())+
      [hf['host_source'],hf[plan_field]]+sf['files']+sf['original_source_pins']+sf['exact_source_evidence_pins'])
    for p in full_rows:verify(p)
    bplan_pin=fullpin(BUILD/'EXACT_COMPACT70_TO_CACHE336_DRIVER_BUILD_PLAN.json');bp=load(bplan_pin)
    old70=bp['original_ordered70_input_pins'];current9=bp['current_nine_core_object_pins'];historical9=bp['historical_original_nine_core_object_pins']
    if len(old70)!=70 or len({p['path']for p in old70})!=70 or len(current9)!=9 or len(historical9)!=9 or \
       old70[40]!=bp['retained_current_BOOTQ_object_pin']or old70[57]!=bp['unchanged_SPOT1P64_object_pin']or \
       current9[:5]+current9[6:]!=historical9[:5]+historical9[6:]or current9[5]!=old70[40]:raise RuntimeError('exact original70/current9/historical9 role map')
    # Objects/archives are full EOF evidence; no scientific input body is read here.
    for p in unique(old70+current9+historical9):verify(p)
    expected_build=Path(bp['planned_output_root']);driver=expected_build/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o'
    new70=[p['path']for p in old70];new70[37]=str(driver)
    buildcmd=[bp['original_compiler_pin']['path'],*bp['original_compile_flags'],'-I'+str(expected_build/'build'),
      *bp['original_compile_include_arguments'],'-J'+str(expected_build/'build'),'-c',str(SOURCE/'SPOT_GLOBAL_NATIVE_DRIVER64.f'),'-o',str(driver)]
    linkcmd=[bp['original_compiler_pin']['path'],'-O2','-ffp-contract=off',*new70,'-o',str(expected_build/'runtime/Dragon')]
    control_terminal=None;control_log=None;control_plan_pin=None;new_build_report_pin=None
    if a.role=='build':
        if set(args)!={'original70','source-freeze','host-freeze'}or args['original70']!=bp['original_actual_complete70_report_pin']or \
           d['schema']!='ACTUAL_NATIVE_RANK1_CACHE336_DRIVER_COMPLETE70_BUILD_ONLY_V1'or \
           d['status']!='ACTUAL_ONE_CACHE336_DRIVER_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'or \
           d['Dragon_linked']is not True or d['actual_new_Source_freeze_pin']!=supplied['Source-freeze']or \
           d['replacement_zero_based_complete70_input_index']!=37 or d['original_ordered70_input_pins']!=old70 or \
           d['actual_complete70_link_inputs']!=new70 or d['original_nine_core_object_pins']!=current9 or \
           d['historical_original_nine_core_object_pins']!=historical9 or \
           any(d[k]is not True for k in ('original69_other_inputs_identical_and_retained','original_four_archives_identical_and_retained','current_nine_core_objects_identical_and_retained'))or \
           any(d[k]is not False for k in ('transport_executed','new_entry_controls_executed','new_reader_control_qualification','new_cache_budget_component_control_qualification')):
            raise RuntimeError('actual Driver37 only, closed2, all original current objects and false qualifications')
        source_row=next(p for p in sf['files']if p['path']==str(SOURCE/'SPOT_GLOBAL_NATIVE_DRIVER64.f'))
        if d['actual_new_Source_pin']!=source_row or sorted(p.name for p in (root/'build').iterdir())!=['SPOT_GLOBAL_NATIVE_DRIVER64.o']:
            raise RuntimeError('one exact Driver Source/object and no module output')
        expected=[buildcmd,linkcmd];labels=['compile_Driver','link_Dragon']
        new_driver_pin=fullpin(driver);new_dragon_pin=fullpin(root/'runtime/Dragon')
        if ot.get(new_driver_pin['path'])!=new_driver_pin or ot.get(new_dragon_pin['path'])!=new_dragon_pin:raise RuntimeError('actual new Driver and Dragon full output PFs')
    else:
        if set(args)!={'new-build70','source-freeze','host-freeze'}:raise RuntimeError('bit exact three external roles')
        control_plan_pin=fullpin(BIT/'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json');p=load(control_plan_pin)
        if hf['control_host_plan_pin']!=control_plan_pin or d['actual_Source_freeze_pin']!=supplied['Source-freeze']or \
           d['schema']!='ACTUAL_NATIVE_RANK1_CACHE336_BUDGET_BIT_GUARDED_CONTROL_REPORT_V1'or \
           d['status']!='ACTUAL_CACHE336_ENABLED_STORE_REJECT_MIXED_GROUP_BIT_CONTROLS_CLOSED0_ONLY'or \
           d['actual_cache336_budget_bit_controls_passed']is not True or d['actual_model_controls_passed']is not False or \
           d['actual_seven_genuine_public_READ_controls_passed']is not False or d['logical_control_count']!=1 or d['actual_run_phase_count']!=1 or \
           d['original_aux_cap_bytes']!=128*2**20 or d['original_pending_metadata_bytes']!=8*2**20:
            raise RuntimeError('actual exact3 bit role/report/aux scope')
        new_build_report_pin=args['new-build70'];base=load(new_build_report_pin)
        if d['actual_new_build70_report_pin']!=new_build_report_pin or base['actual_host_Source_freeze_pin']!=hf['selected_new_build_Host_freeze_pin']or \
           base['actual_new_Source_freeze_pin']!=supplied['Source-freeze']or base['actual_complete70_link_inputs']!=new70 or \
           base['schema']!='ACTUAL_NATIVE_RANK1_CACHE336_DRIVER_COMPLETE70_BUILD_ONLY_V1'or \
           base['status']!='ACTUAL_ONE_CACHE336_DRIVER_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'or base['Dragon_linked']is not True or \
           base['failure']is not None or base['after_check_error']is not None or base['final_report_resource_check_passed']is not True or \
           [r['command']for r in base['records']]!=[buildcmd,linkcmd]or any(r['status']!='PASS'for r in base['records']):
            raise RuntimeError('same actual prior Driver-only closed2, selected HF/SF and exact70')
        compiler=p['original_compiler_pin']['path'];obj=str(root/'build/control.o');exe=str(root/'runtime/control_unqualified')
        includes=['-I'+str(root/'build'),'-I'+p['new_build_expected_build_directory'],*p['original_compile_include_arguments']]
        cc=[compiler,*p['original_compile_flags'],*includes,'-J'+str(root/'build'),'-c',p['control_Source_pin']['path'],'-o',obj]
        lc=[compiler,'-O2','-ffp-contract=off',obj,p['unchanged_math_object_pin']['path'],*p['original_four_archive_paths'],'-o',exe]
        if p['unchanged_math_object_pin']!=old70[57]or p['original_four_archive_paths']!=[x['path']for x in old70 if x['path'].endswith('.a')]or \
           d['actual_compile_command']!=cc or d['actual_link_command']!=lc or d['actual_link_core_paths']!=[old70[57]['path']]or \
           d['actual_control_Source_pin']!=p['control_Source_pin']or p['control_Source_pin']not in sf['files']or \
           sorted(q.name for q in (root/'build').iterdir())!=['control.o']:
            raise RuntimeError('control-only exact compile/no MOD and unchanged math57/four archives link')
        expected=[cc,lc,[exe]];labels=['compile_control','link_control','run_budget_bits']
        control_terminal,control_log=bit_json(root,d['records'][-1])
        results=d['actual_control_results']
        if len(results)!=1 or results[0]['actual_terminal']!=control_terminal or results[0]['actual_log_pin']!=control_log or \
           results[0]['actual_assertions']!=338 or results[0]['actual_SPOT1P64_calls']!=121 or d['actual_stale_host_evidence']!=[]:
            raise RuntimeError('actual control terminal and report results identical')
        new_driver_pin=fullpin(driver);new_dragon_pin=fullpin(expected_build/'runtime/Dragon')
        for row in (new_driver_pin,new_dragon_pin):
            if row not in base['output_pins']:raise RuntimeError('actual prior new build output fullPF')
        if d['actual_new_Driver_object_pin']!=new_driver_pin:raise RuntimeError('same exact new Driver body in bit report')
    if len(d['records'])!=len(expected)or [Path(r['label']).name for r in d['records']]!=labels:raise RuntimeError('exact ordered actual2/3 stage labels')
    watches=[watch(root,r,cmd)for r,cmd in zip(d['records'],expected)]
    resource_snapshot(d['resources_before'],root,False)
    for s in (d['resources_after'],d['resources_after_including_summary_bytes']):resource_snapshot(s,root,a.role=='bit')
    reserve=96*2**30-d['resources_before']['artifact_bytes']-20971764748-64*2**20-2*2**30
    if reserve<=0:raise RuntimeError('original initial cold/meta/fullfresh2 reserve not admitted')
    actual_bytes=sum(i[4]for i in before_inventory['files'].values())
    if actual_bytes>2*2**30 or shutil.disk_usage(root).free<8*2**30:raise RuntimeError('actual physical fresh2/current filesystem floor8')
    if a.role=='bit'and actual_bytes+8*2**20>128*2**20:raise RuntimeError('current direct auxiliary128+8')
    for p in fixed:current7(p)
    for p in full_rows:current7(p)
    if inventory(root)!=before_inventory:raise RuntimeError('actual OUT inventory changed during independent postverification')
    directory=Path(a.review_directory);ancestors(directory)
    if directory.parent!=REC or directory.exists():raise RuntimeError('unique direct REC review directory, no overwrite')
    guard();directory.mkdir()
    result=dict(schema='LIMITED_ACTUAL_CACHE336_BUILD_OR_BIT_POSTVERIFICATION_V1',status='PASS_LIMITED_ACTUAL_CACHE336_'+a.role.upper()+'_POSTVERIFICATION',failure=None,role=a.role,
      readonly=True,source_only=False,postverification_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False,
      independent_business_executed=False,independent_compiler_executed=False,independent_numerical_executed=False,independent_deletion_executed=False,
      actual_report_pin=report_pin,actual_Root_tools_pin=supplied['Root-tools'],actual_Root_argv_pin=supplied['Root-argv'],actual_Host_freeze_pin=supplied['Host-freeze'],
      actual_Root_true_tool_return_pin=supplied['Root-tools'],
      actual_Source_freeze_pin=supplied['Source-freeze'],actual_CLI_pin=cli_pin,actual_Host_Source_pin=hf['host_source'],
      Root_actual_initial_return=initial,Root_actual_terminal_return=terminal,Root_exact_executed_command=rt['exact_executed_command'],
      actual_new_Driver_object_pin=new_driver_pin,actual_new_Dragon_pin=new_dragon_pin,actual_preceding_new_build_report_pin=new_build_report_pin,
      actual_stage_count=len(d['records']),actual_ordered_commands=expected,actual_watch_and_log_evidence=watches,
      actual_control_terminal=control_terminal,actual_control_log_pin=control_log,actual_control_plan_pin=control_plan_pin,
      actual_fixed_current_count=len(fixed),actual_HF_dependency_count=len(deps),all_fixed_and_dependencies_current7_checked_twice=True,
      all_fixed_scientific_SHA_not_repeated=True,limitation='Limited postverify: all fixed/dependencies receive current7 twice; explicit objects/archives/Source/metadata/logs/all outputs receive complete EOF SHA. No fresh scientific-body SHA claim.',
      actual_full_EOF_output_pins=output+[report_pin],actual_explicit_full_EOF_Source_metadata_pins=full_rows,
      retained_original70_object_archive_pins=old70,retained_current9_core_pins=current9,retained_historical9_pins=historical9,
      original69_other_inputs_and_math57_BOOTQ40_four_archives_full_EOF_retained=True,original_caps=CAPS,
      initial_fullfresh2_cold_metadata_reserve_remaining_bytes=reserve,actual_output_physical_file_count=len(before_inventory['files']),actual_output_physical_bytes=actual_bytes,
      all_actual_outputs_full_EOF_SHA_current7=True,actual_inventory=before_inventory,actual_control338_121_completed=a.role=='bit',
      cache_stats_assertions_observed_via_exact_frozen_program_complete338=a.role=='bit',raw_cache_stat_values_not_separately_printed=True,
      reader_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,
      all_file_descriptors_closed=True,postverification_SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      postverification_wall_seconds=time.monotonic()-START,postverification_Source_pin=fullpin(Path(__file__).absolute()))
    path=directory/'REVIEW.json';fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'w')as f:json.dump(result,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    rp=fullpin(path);guard();print(json.dumps(dict(status=result['status'],review_pin=rp,failure=None,role=a.role,limited_readonly_postverification=True),ensure_ascii=False),flush=True)

if __name__=='__main__':main()
