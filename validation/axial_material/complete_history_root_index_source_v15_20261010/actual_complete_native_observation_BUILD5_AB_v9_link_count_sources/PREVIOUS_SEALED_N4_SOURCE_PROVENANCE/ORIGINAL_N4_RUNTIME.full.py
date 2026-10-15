"""UNREADY complete five-group fresh native build and full A/B observer production.
Only a Root-bound reviewed genuine host may call run; no import-time work.
Original physical source bytes and original Darwin arm64 compiler flags retained.
No old binary/object/archive, no deck construction, no payload truncation.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import shutil
import stat
import struct
import subprocess
import sys
import tarfile
import time

SOURCE_STATUS='UNREADY_SOURCE_ONLY'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
FUTURE=dict(actual_runtime_qualification_sha256=None,actual_observer_native_controls_run=None,actual_native_Source_binary_linkage_qualification_sha256=None,actual_scientific_qualification_sha256=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_transport_executed=False,complete_context_aggregation_qualified=False)
# Complete selected original Makefile variables, preserving empty/undefined
# variables rather than inventing common flags. Original Darwin/arm64, GNU
# compilers, openmp/mpi/hdf5/intel/nvidia/llvm disabled. Relative INCLUDE is
# evaluated from each original component src directory in the fresh tree.
ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES = {
    'Ganlib': {'C':'c','CFLAGS':['-Wall','-fPIC'],'FLAGS':['-DLinux','-DUnix'],
        'F90':'fortran','FFLAGS':['-fPIC','-Wall','-Wno-maybe-uninitialized','-ffpe-summary=none'],
        'FFLAG77':['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],
        'INCLUDE':[], 'PREPRO':'cpp','FMPI':[], 'opt':['-O','-g'], 'COMP':[], 'LFLAGS':[],
        'lib_module':'Ganlib/lib/Darwin_arm64/modules','module_copy':True},
    'Utilib': {'C':'c','CFLAGS':['-Wall','-fPIC'],'FLAGS':[],
        'F90':'fortran','FFLAGS':['-fPIC','-Wall','-ffpe-summary=none'],
        'FFLAG77':['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],
        'INCLUDE':[], 'PREPRO':None,'FMPI':[], 'opt':['-O','-g'], 'COMP':[], 'LFLAGS':[],
        'lib_module':'Utilib/lib/Darwin_arm64/modules','module_copy':True},
    'Trivac': {'C':None,'CFLAGS':[],'FLAGS':[],
        'F90':'fortran','FFLAGS':['-fPIC','-ffpe-summary=none'],
        'FFLAG77':['-fPIC','-frecord-marker=4','-ffpe-summary=none'],
        'INCLUDE':['-I../../Ganlib/lib/Darwin_arm64/modules/'], 'PREPRO':None,'FMPI':[],
        'opt':['-O','-g'], 'COMP':[], 'LFLAGS':[], 'lib_module':None,'module_copy':False},
    'Dragon': {'C':'c','CFLAGS':['-Wall','-fPIC'],'FLAGS':['-DLinux','-DUnix'],
        'F90':'fortran','FFLAGS':['-fPIC','-Wall','-ffpe-summary=none'],
        'FFLAG77':['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],
        'INCLUDE':['-I../../Ganlib/lib/Darwin_arm64/modules/'], 'PREPRO':'cpp','FMPI':[],
        'opt':['-O','-g'], 'COMP':[], 'LFLAGS':[],
        'lib_module':'Dragon/lib/Darwin_arm64/modules','module_copy':True},
}

ROLE_LABELS={'LIBMIX_BEFORE':'oldmacro-pre-LIBMIX','LIBDEN_OLD_CONTEXT':'oldmacro-LIBDEN','LIBMIX_AFTER':'postmacro-LIBMIX','TONDRV_FINAL_AFTER_SHIBA':'final-complete-micro'}
LABELS=('LIBMIX_BEFORE','LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION','LIBMIX_AFTER','TONDRV_AFTER_REAL_MAT_ELIMINATION','TONDRV_ACTUAL_FINAL_LIBMIX_MASK','TONSPH_BEFORE_ACTUAL_TONCMI','TONDRV_ACTUAL_SPH_CALL_DECISION','TONDRV_FINAL_AFTER_SHIBA')

CANONICAL_OS_TOOL_PATHS = {'fortran': '/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15', 'c': '/usr/bin/gcc', 'cpp': '/usr/bin/cpp', 'ar': '/usr/bin/ar', 'lsof': '/usr/sbin/lsof', 'ps': '/bin/ps'}

def source_tool_nlink_allowed(path,nlink,tool_role=None):
    # Default stays the original single-link contract. Only an explicit one of
    # these six original OS tool roles may preserve a positive real hardlink
    # count. Paths, bytes, all seven identity integers and caller order stay real.
    if tool_role is None:return type(nlink)is int and nlink==1
    require(type(tool_role)is str and tool_role in CANONICAL_OS_TOOL_PATHS,'declared original canonical OS tool role only')
    return str(path)==CANONICAL_OS_TOOL_PATHS[tool_role]and type(nlink)is int and nlink>=1

def require(value,message):
    if type(value)is not bool or not value:raise ValueError(message)

def strict_json(raw):
    def pairs(items):
        d={}
        for k,v in items:require(k not in d,'duplicate metadata key');d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))

def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def fullpin(path,budget=lambda:None,tool_role=None):
    path=Path(path);before=identity(path.lstat())
    require(path.is_absolute()and all(not q.is_symlink()for q in(path,*path.parents))and stat.S_ISREG(before[2])and source_tool_nlink_allowed(path,before[3],tool_role),'regular nonalias full input; default single-link except explicit canonical OS tools')
    d=hashlib.sha256();size=0
    with path.open('rb')as f:
        require(identity(os.fstat(f.fileno()))==before,'open fullpin identity')
        while True:
            budget();raw=f.read(2**20)
            if not raw:break
            d.update(raw);size+=len(raw)
        require(identity(os.fstat(f.fileno()))==before,'EOF fullpin identity')
    require(identity(path.lstat())==before and size==before[4],'full EOF identity unchanged')
    return dict(path=str(path),sha256=d.hexdigest(),size_bytes=size,identity=before)

def pinshape(p,tool_role=None):
    require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'},'exact fullpin shape')
    require(type(p['path'])is str and Path(p['path']).is_absolute()and '..'not in Path(p['path']).parts and type(p['sha256'])is str and re.fullmatch('[0-9a-f]{64}',p['sha256'])is not None,'absolute path and SHA')
    require(type(p['size_bytes'])is int and p['size_bytes']>=0 and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int and x>=0 for x in p['identity'])and source_tool_nlink_allowed(p['path'],p['identity'][3],tool_role)and p['identity'][4]==p['size_bytes'],'strict integer 7ID and size')

def recheck(p,budget=lambda:None,tool_role=None):
    pinshape(p,tool_role=tool_role);require(fullpin(p['path'],budget,tool_role=tool_role)==p,'complete input SHA/7ID changed: '+p['path']);return p

def write_new(path,value):
    with Path(path).open('x',encoding='utf-8')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

def tree(path):
    path=Path(path);files=[];dirs={}
    require(path.is_dir()and not path.is_symlink(),'frozen real directory')
    for p in [path,*sorted(path.rglob('*'))]:
        s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'no aliases in complete namespace')
        if stat.S_ISDIR(s.st_mode):dirs[str(p)]=identity(s)
        else:
            require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'no unaccounted special/hardlink');files.append(fullpin(p))
    return dict(files=files,directories=dirs)

def frozen_sources(native,index,observation_source):
    overridden={'Dragon/src/LIBMIX.f':'LIBMIX.observe.UNREADY.f','Dragon/src/LIBDEN.f':'LIBDEN.observe.UNREADY.f','Dragon/src/TONDRV.f':'TONDRV.context_observe.UNREADY.f','Dragon/src/TONSPH.f':'TONSPH.observe.UNREADY.f'}
    expected={r['relative_path']:r['full_original_Source_pin']['sha256']for r in index['members']}
    expected.update({k:fullpin(observation_source/v)['sha256']for k,v in overridden.items()})
    expected['Dragon/src/AXMAT_CONTEXT_OBSERVATION_MOD.f90']=fullpin(observation_source/'AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90')['sha256']
    actual=[]
    for rel,wanted in expected.items():
        p=fullpin(native/rel);require(p['sha256']==wanted,'full native Source freeze differs: '+rel);actual.append(dict(relative_path=rel,input_pin=p))
    all_source={str(p.relative_to(native))for p in native.rglob('*')if p.is_file()and(p.name=='Makefile'or p.suffix in('.f','.F','.f90','.F90','.c','.h','.inc','.py'))}
    require(all_source==set(expected),'full compile Source namespace coverage; no skipped extra Source')
    return actual

def actual_scope(request,author):
    expected=request['actual_author_Source_contract']
    require(type(expected)is dict and expected==author,'exact whole observer author Source roles')
    for p in expected.values():recheck(p)
    peer=strict_json(Path(request['independent_observation_Source_review_pin']['path']).read_bytes())
    require(peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_BINDER_SOURCE_REVIEW_V1'and peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and peer['source_only']is True and peer['all_checks_passed']is True and peer['blockers']==[],'independent full observer Source pass required')
    checks=peer['checks'];require(type(checks)is list and type(peer['check_count'])is int and peer['check_count']==len(checks)>0 and all(type(c)is dict and set(c)=={'check','passed'}and type(c['check'])is str and bool(c['check'])and c['passed']is True for c in checks)and len({c['check']for c in checks})==len(checks),'independent aggregate checks strictly typed')
    admission=strict_json(Path(request['independent_observation_Source_admission_pin']['path']).read_bytes())
    require(admission['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_V1'and admission['status']=='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE'and admission['source_only']is True and admission['scientific_qualification_created']is False and admission['independent_Source_review_pin']==request['independent_observation_Source_review_pin'],'Root Source-only admission binds independent review')
    require(peer['actual_author_Source_contract']==expected and admission['actual_author_Source_contract']==expected,'whole Source body pins coupled to peer/admission')
    for k in FUTURE:require(admission[k]is FUTURE[k],'Root Source admission cannot invent actual future: '+k)
    truth=strict_json(Path(request['actual_Root_observation_Source_admission_tool_return_pin']['path']).read_bytes());terminal=truth['terminal_tool_return']
    require(truth['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1'and truth['closed']is True and truth['observed_terminal']is True and truth['session_repolled_after_close']is False and type(terminal['exit_code'])is int and terminal['exit_code']==0 and 'session_id'not in terminal and type(terminal['chunk_id'])is str and bool(terminal['chunk_id'])and truth['actual_terminal_chunk']==terminal['chunk_id'],'actual Root admission CLOSED typed zero')
    output=strict_json(terminal['output']);require(output['status']=='ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE'and output['source_only']is True and output['source_admission_pin']==request['independent_observation_Source_admission_pin'],'Root actual Source admission tool output exact coupling')
    return dict(schema='ACTUAL_COMPLETE_OBSERVATION_SOURCE_SCOPE_COUPLING_V1',source_only=True,actual_author_Source_contract=expected,independent_Source_review_pin=request['independent_observation_Source_review_pin'],independent_observation_Source_admission_pin=request['independent_observation_Source_admission_pin'],actual_Root_admission_tool_return_pin=request['actual_Root_observation_Source_admission_tool_return_pin'],independent_aggregate_check_count=len(checks),**FUTURE)

def validate_request(b,author):
    require(b['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_BUILD_BINDING_V1'and b['source_only']is True and b['Root_only_actual_execution']is True and b['scientific_qualification_created']is False,'strict Root observer Source binding')
    require(type(b['original_caps'])is dict and set(b['original_caps'])==set(CAPS)and all(type(v)is int for v in b['original_caps'].values())and b['original_caps']==CAPS,'unchanged typed caps')
    require(b['state_order']==['A','B']and b['build_stage_order']==['Ganlib','Utilib','Trivac','Dragon','Dragon_link']and b['SPOT_AXMAT_OBSERVATION']=='ADMITTED_SOURCE_ONLY','actual full ordered A then B/5groups')
    for k,v in FUTURE.items():require(b[k]is v,'unknown/false future flag '+k)
    seed_contract=strict_json(Path(author['original_material_seed_contract']['path']).read_bytes());require(b['original129_input_pins']==seed_contract['original129_input_pins'],'original129 complete pin contract unchanged');rows=b['original129_input_pins'];require(type(rows)is list and len(rows)==129 and len({p['path']for p in rows})==129,'complete original129 pins')
    extra=b['additional_actual_evidence_input_pins'];require(type(extra)is list and bool(extra)and len({p['path']for p in extra})==len(extra),'nonempty whole additional input list')
    allpins={p['path']:p for p in rows+extra}
    require(len(allpins)==len(rows+extra),'original129 and extra disjoint')
    require(type(b['tool_pins'])is dict and set(b['tool_pins'])==set(CANONICAL_OS_TOOL_PATHS),'complete fixed six OS tool roles before extra input shapes')
    for role,p in b['tool_pins'].items():pinshape(p,tool_role=role)
    tool_roles_by_path={p['path']:role for role,p in b['tool_pins'].items()}
    for p in rows:pinshape(p)
    for p in extra:pinshape(p,tool_role=tool_roles_by_path.get(p['path']))
    for k in ('independent_observation_Source_review_pin','independent_observation_Source_admission_pin','actual_Root_observation_Source_admission_tool_return_pin'):
        pinshape(b[k]);require(allpins.get(b[k]['path'])==b[k],'all admission evidence included in protected full inputs')
    require(type(b['tool_pins'])is dict and set(b['tool_pins'])=={'fortran','c','cpp','ar','lsof','ps'},'full native and accounting tool pins')
    for role,p in b['tool_pins'].items():pinshape(p,tool_role=role);require(allpins.get(p['path'])==p,'all actual tools in full protected input list')
    require(Path(b['tool_pins']['fortran']['path']).name.startswith('gfortran')and Path(b['tool_pins']['c']['path']).name.startswith('gcc'),'original GNU Fortran and Darwin C recipe required')
    required={'material.x2m','AxMatTone.c2m','geometry.dat','rnr_cc.c2m','rnr_interpol.c2m','DLIB_ACTUAL','DLIB8R1_370'}
    require(type(b['states'])is dict and list(b['states'])==['A','B'],'A/B source insertion order')
    for state in ('A','B'):
        inputs=b['states'][state]['native_stage_inputs'];require(type(inputs)is list and {row['destination']for row in inputs}==required and len(inputs)==len(required),'exact original complete material input set')
        for row in inputs:
            require(type(row)is dict and set(row)=={'destination','input_pin'},'exact immutable seed mapping');pinshape(row['input_pin']);require(allpins.get(row['input_pin']['path'])==row['input_pin'],'all original material inputs protected')
        require(b['states'][state]['original_material_deck_pin']==next(x['input_pin']for x in inputs if x['destination']=='material.x2m'),'exact original deck; no regenerated deck')
        for row in inputs:
            destination=row['destination'];expected=seed_contract['states'][state].get(destination)
            if expected is not None:require(row['input_pin']==expected,'original whole material input fullpin unchanged: '+destination)
            else:require(row['input_pin']['path']==seed_contract['libraries'][destination]['path']and row['input_pin']['sha256']==seed_contract['libraries'][destination]['generation_sha256'],'original material library path and generation SHA')
    return actual_scope(b,author)

def joint_bytes(roots,lsof_tool,ps_tool):
    total=0;seen=set()
    for root in roots:
        if not Path(root).exists():continue
        for p in Path(root).rglob('*'):
            s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'joint archive aliases forbidden')
            if stat.S_ISDIR(s.st_mode):continue
            require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'joint regular singlelink scope');key=(s.st_dev,s.st_ino);require(key not in seen,'joint hardlink aliases forbidden');seen.add(key);total+=s.st_size
    # Diagnostic scans have the same status as the original guard's /bin/ps:
    # they do not constitute additional material/build business children.
    ps=subprocess.run([ps_tool,'-axo','pid=,ppid='],capture_output=True,text=True,timeout=2,check=True)
    parents={int(a):int(b)for a,b in(line.split()for line in ps.stdout.splitlines())}
    selected={os.getpid()}
    while True:
        new={p for p,parent in parents.items()if parent in selected};expanded=selected|new
        if expanded==selected:break
        selected=expanded
    observed=subprocess.run([lsof_tool,'-nP','-F','pfnsiDt','-a','-p',','.join(map(str,sorted(selected)))],capture_output=True,text=True,timeout=2)
    require(observed.returncode==0,'full live own process file scan required')
    require(len(observed.stdout)<8*2**20,'finite complete lsof output; never truncated')
    records=[];row={}
    for line in observed.stdout.splitlines():
        if line.startswith('f'):
            if row:records.append(row)
            row={'f':line[1:]}
        elif line and line[0]in'nsiDt':row[line[0]]=line[1:]
    if row:records.append(row)
    unlinked=set();unlinked_bytes=0
    for row in records:
        name=row.get('n','')
        if not name.endswith(' (deleted)'):continue
        name=name[:-10]
        if any(Path(name).is_relative_to(Path(root))for root in roots):
            require(all(k in row for k in('s','i','D','t'))and row['t']=='REG'and row['s'].isdigit(),'complete open-unlinked live size/inode/device required')
            key=(row['D'],row['i']);
            if key not in unlinked:total+=int(row['s']);unlinked_bytes+=int(row['s']);unlinked.add(key)
    return dict(complete_joint_HOCDE_bytes=total,open_unlinked_files=len(unlinked),open_unlinked_bytes=unlinked_bytes,actual_open_regular_paths=[r['n']for r in records if 'n'in r and r['n'].startswith('/')and not r['n'].endswith(' (deleted)')],live_own_processes_observed=sorted(selected),all_regular_and_open_unlinked_counted=True)

def guarded(runner,support,resources,folder,label,argv,deadline,budget,deck=None,marker=None):
    budget();remaining=min(600,deadline-time.monotonic());require(remaining>0,'group600/whole1800 remaining')
    require(not os.path.lexists(folder/(label+'.log')),'fresh command log zero retry')
    runner.execute(folder,label,argv,remaining,deck=deck,marker=marker)
    watch_path=folder/(label+'.watchdog.json');watch=strict_json(watch_path.read_bytes())
    require(type(watch['pid'])is int and watch['pid']>0 and type(watch['returncode'])is int and watch['returncode']==0 and watch['command']==argv and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True,'genuine actual command closed zero and liveness cleanup')
    require(type(watch['sampled_peak_rss_mib'])in(int,float)and not isinstance(watch['sampled_peak_rss_mib'],bool)and math.isfinite(watch['sampled_peak_rss_mib'])and 0<=watch['sampled_peak_rss_mib']<512 and 0<=watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and watch['rss_cap_mib']==512,'original actual own-child RSS/wall scope')
    require(runner.records[-1]['status']=='PASS','actual genuine PASS stage')
    budget();return dict(label=label,command=argv,actual_watchdog_pin=fullpin(watch_path,budget),actual_merged_stdout_stderr_pin=fullpin(folder/(label+'.log'),budget),actual_child_PID=watch['pid'],watchdog=watch)

def compile_all(native,index,observation_source,tools,runner,support,resources,budget):
    require(platform.system()=='Darwin'and platform.machine()=='arm64','exact original selected Makefile platform, no inferred compiler flags')
    original=frozen_sources(native,index,observation_source);generator,generator_pin=support.load(native/'script/make_depend.py',next(r['input_pin']['sha256']for r in original if r['relative_path']=='script/make_depend.py'),'axmat_observation_original_native_make_depend')
    sources={r['relative_path']:r['input_pin']for r in original};stages=[];archives={};all_objects=[]
    require(list(ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES)==['Ganlib','Utilib','Trivac','Dragon'],'all original component-specific recipe variables')
    for component in ('Ganlib','Utilib','Trivac','Dragon'):
        started=time.monotonic();deadline=started+600;folder=native/component/'src';recipe=ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES[component]
        library_dir=native/component/'lib/Darwin_arm64';library_dir.mkdir(parents=True)
        if recipe['lib_module']is not None:(native/recipe['lib_module']).mkdir(parents=True)
        require(not any(p.suffix in('.o','.a','.mod')for p in folder.iterdir()),'all native objects/archives/modules fresh; no old build reuse')
        c=sorted(folder.glob('*.c'));f90=[*sorted(folder.glob('*.f90')),*sorted(folder.glob('*.F90'))];f77_lower=sorted(folder.glob('*.f'));f77_upper=sorted(folder.glob('*.F'));f77=[*f77_lower,*f77_upper]
        # The original default generator excludes module-contained include files.
        ordered90=[Path(v)for v in generator.build_dependency_order([str(p)for p in f90])]
        objects_order=[p.with_suffix('.o')for p in [*c,*ordered90,*f77]]
        require(len(set(objects_order))==len(objects_order),'original object basename uniqueness')
        units=generator.build_units([str(p)for p in [*f90,*f77]]);module_source={u.module:Path(u.name)for u in units if u.module};by_source={Path(u.name):u for u in units};pending=[*c,*ordered90,*f77];commands=[];objects=[];completed=set()
        while pending:
            chosen=None
            for p in pending:
                uses=[]if p not in by_source else by_source[p].uses
                dependencies={module_source[m]for m in uses if m in module_source and module_source[m]!=p}
                if dependencies<=completed:chosen=p;break
            require(chosen is not None,'original native module dependencies must be acyclic; never guess ordering');pending.remove(chosen);p=chosen;budget();sp=fullpin(p,budget);obj=p.with_suffix('.o');require(not os.path.lexists(obj),'new object required')
            src=p
            if p.suffix in('.F','.F90'):
                src=p.with_suffix('.pp.f90'if p.suffix=='.F90'else'.pp.f');require(not os.path.lexists(src),'fresh actual preprocessor output')
                require(recipe['PREPRO']is not None,'original selected Makefile PREPRO undefined for this suffix; no invented tool')
                argv=[tools[recipe['PREPRO']]['path'],'-P','-W','-traditional',*recipe['FLAGS']]
                if p.suffix=='.F':argv+=recipe['FMPI']
                argv+=[str(p),str(src)]
                commands.append(guarded(runner,support,resources,folder,'preprocess_'+p.stem,argv,deadline,budget));preprocessed=fullpin(src,budget)
            else:preprocessed=None
            if p.suffix=='.c':
                require(recipe['C']is not None,'original selected Makefile C undefined, no invented compiler')
                argv=[tools[recipe['C']]['path'],*recipe['CFLAGS'],*recipe['FLAGS'],*recipe['opt'],*recipe['COMP'],'-c',str(src),'-o',str(obj)]
            else:
                flags=recipe['FFLAG77']if p.suffix in('.f','.F')else recipe['FFLAGS']
                argv=[tools[recipe['F90']]['path'],*flags,*recipe['opt'],*recipe['COMP'],*recipe['INCLUDE'],'-c',str(src),'-o',str(obj)]
            stage=guarded(runner,support,resources,folder,'compile_'+p.stem,argv,deadline,budget);op=fullpin(obj,budget);require(fullpin(p,budget)==sp,'compiler Source unchanged')
            retained_preprocessed=None
            if preprocessed is not None:
                retained=native.parent/'retained_preprocessor_Source'/component/src.name;retained.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,retained);retained_preprocessed=fullpin(retained,budget);require(retained_preprocessed['sha256']==preprocessed['sha256']and retained_preprocessed['size_bytes']==preprocessed['size_bytes'],'lossless exact actual preprocessed compiler input kept');src.unlink()
            row=dict(original_source_pin=sp,preprocessor_output_pin=preprocessed,retained_complete_preprocessor_Source_pin=retained_preprocessed,actual_compile=stage,new_object_pin=op);objects.append(row);all_objects.append(row);commands.append(stage);completed.add(p)
        require({x['new_object_pin']['path']for x in objects}==set(map(str,objects_order)),'all original library objects compiled exactly once')
        archive=folder/('lib'+component+'.a');argv=[tools['ar']['path'],'rcs',str(archive),*map(str,objects_order)];archive_stage=guarded(runner,support,resources,folder,'archive_'+component,argv,deadline,budget);ap=fullpin(archive,budget)
        for row in objects:recheck(row['new_object_pin'],budget)
        # Original ar emits src/lib*.a, then original cp places the same fresh
        # archive into each component's own lib directory used by final link.
        library_copy=library_dir/archive.name;require(not os.path.lexists(library_copy),'fresh original recipe library copy')
        shutil.copy2(archive,library_copy);library_copy_pin=fullpin(library_copy,budget)
        require(library_copy_pin['sha256']==ap['sha256']and library_copy_pin['size_bytes']==ap['size_bytes'],'original library copy full bytes equal actual fresh ar output')
        module_copy_pins=[]
        if recipe['module_copy']:
            modules=native/recipe['lib_module'];generated_modules=list(folder.glob('*.mod'))
            require(component!='Utilib'or bool(generated_modules),'original Utilib unguarded cp *.mod requires actual modules')
            for p in generated_modules:
                target=modules/p.name;require(not os.path.lexists(target),'original per-library module namespace fresh')
                shutil.copy2(p,target);module_copy_pins.append(dict(original_generated_module_pin=fullpin(p,budget),original_recipe_module_copy_pin=fullpin(target,budget)))
        # Trivac's original library recipe never copies module files.
        require(time.monotonic()-started<600,'entire library compile/archive group600 cap')
        archives[component]=library_copy_pin;stages.append(dict(component=component,exact_original_selected_recipe=recipe,original_recipe_library_copy_pin=library_copy_pin,original_recipe_module_copy_pins=module_copy_pins,archive_object_source_suffix_group_order=['.c','original_dependency_order(.f90_then_.F90)','.f','.F'],stage_wall_cap_seconds=600,elapsed_seconds=time.monotonic()-started,all_object_inputs_in_original_archive_order=[r for p in objects_order for r in objects if r['new_object_pin']['path']==str(p)],all_commands=commands,actual_archive_command=archive_stage,new_archive_pin=ap))
        require(frozen_sources(native,index,observation_source)==original,'complete native Source freeze after whole group')
    link_started=time.monotonic();exe=native/'Dragon/src/Dragon';dragon_o=native/'Dragon/src/DRAGON.o';require(not os.path.lexists(exe),'new final executable required')
    link_inputs=[fullpin(dragon_o,budget),*[archives[k]for k in('Dragon','Trivac','Utilib','Ganlib')]]
    link_recipe=ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES['Dragon'];argv=[tools[link_recipe['F90']]['path'],*link_recipe['opt'],*link_recipe['COMP'],*[p['path']for p in link_inputs],*link_recipe['LFLAGS'],'-o',str(exe)];link=guarded(runner,support,resources,native/'Dragon/src','Dragon_link',argv,link_started+600,budget)
    ep=fullpin(exe,budget)
    for p in link_inputs:recheck(p,budget)
    for r in all_objects:recheck(r['new_object_pin'],budget)
    require(frozen_sources(native,index,observation_source)==original,'whole native Source-to-new-object/archive/link final freeze')
    evidence=dict(schema='ACTUAL_FROZEN_COMPLETE_NATIVE_SOURCE_OBJECT_ARCHIVE_LINK_EXECUTABLE_EVIDENCE_V1',source_only=False,frozen_all_compiled_and_include_Source=original,original_Source_index_pin=fullpin(index['_path'],budget),original_dependency_generator_pin=dict(generator_pin,size_bytes=generator_pin['identity'][4]),original_platform=dict(OS='Darwin',ARCH='arm64',openmp=0,mpi=0,hdf5=0,opt=['-O','-g']),stage_order=['Ganlib','Utilib','Trivac','Dragon','Dragon_link'],all_four_complete_library_build_stages=stages,actual_final_link_command=link,all_actual_link_input_pins=link_inputs,new_actual_executable_pin=ep,all_sources_objects_archives_checked_after_actual_link=True,no_old_binary_object_archive_used=True,compiler_descendant_RSS_scope_not_certified=True,original_own_child_guard_scope_preserved=True,whole5stage_executed=True,**FUTURE)
    return ep,evidence

def collect_state(folder,state,deck_pin,exe_pin,stage,budget):
    # Read headers in actual consecutive event number order, never native record
    # sorting. Every full event file reaches EOF in fullpin/extract_event.
    files={p.name:p for p in folder.glob('axobs-*')};events=[];snapshots=[];contexts=[];number=1;last_libmix=0;closed=[];all_observer_names=set()
    while True:
        name='axobs-'+format(number,'06d')+'.context.bin'
        if name not in files:break
        path=files[name];pp=fullpin(path,budget)
        with path.open('rb')as stream:
            require(stream.read(8)==b'AXOBSCTX','whole observer magic')
            raw=stream.read(16);require(len(raw)==16,'actual full event header');version,event,libmix,length=struct.unpack('<4i',raw)
            require(version==2 and event==number and libmix>=last_libmix and 1<=length<=256,'actual consecutive AXOBSCTXv2 event/libmix header')
            label=stream.read(length).decode('ascii');require(label in LABELS,'no unknown/omitted observer event')
        role=ROLE_LABELS.get(label);snapshot=None;all_observer_names.add(name);contexts.append(pp)
        if role is not None:
            n='axobs-'+format(event,'06d')+'-'+role+'.xsm'
            if n in files:
                snapshot=fullpin(files[n],budget);all_observer_names.add(n);snapshots.append(dict(event=event,role=role,root_prefix=[],logical_prefix=[]if role=='final-complete-micro'else['MACROLIB'],input_pin=snapshot))
            else:require(role not in('postmacro-LIBMIX','final-complete-micro'),'every postmacro and actual final micro snapshot mandatory')
        if label=='LIBMIX_BEFORE':require(libmix==last_libmix+1,'every actual LIBMIX begin counted')
        events.append(dict(event=event,libmix=libmix,label=label,complete_context_pin=pp,snapshot_role=role,actual_snapshot_pin=snapshot,actual_native_snapshot_root_prefix=[]if snapshot is not None else None,snapshot_logical_prefix=([]if role=='final-complete-micro'else['MACROLIB'])if snapshot is not None else None,actual_old_macro_absent_at_event=(role is not None and snapshot is None)))
        last_libmix=libmix;number+=1
    require(events and set(files)==all_observer_names,'full actual observer namespace no holes/unknown/leftover entries')
    require(any(e['label']=='TONDRV_FINAL_AFTER_SHIBA'for e in events)and any(e['label']=='TONDRV_ACTUAL_SPH_CALL_DECISION'for e in events),'complete final snapshot and true/false SPH decision events required')
    # The existing full context parser is separately bound/read by the context
    # host. Production manifest retains all bytes and original order now.
    outputs=[]
    for name in('material.xsm','microlib.ascii','macro.ascii','metadata.ascii'):outputs.append(fullpin(folder/name,budget))
    return dict(state=state,actual_material_deck_pin=deck_pin,actual_executable_pin=exe_pin,actual_genuine_material_stage=stage,actual_material_product_pins=outputs,actual_all_event_headers_in_original_execution_order=events,complete_context_pins=contexts,complete_state_snapshot_inputs=snapshots,legacy_context_source_snapshot_request_rows=[dict(event=item['event'],role=item['role'],root_prefix=item['logical_prefix'],input_pin=item['input_pin'])for item in snapshots],legacy_context_root_prefix_semantics='output_pool_logical_path_prefix_only_not_native_directory_lookup',actual_native_snapshot_root_prefix=[],selected_last_libmix_number=last_libmix,all_actual_events_and_snapshots_saved=True,actual_material_child_closed_before_manifest=True,all_producer_file_handles_closed_before_next_state=True,new_final_micro_from_actual_TONDRV_observer=True,native_snapshot_api_or_memory_bits_qualified=False,**FUTURE)

def run(host_module,support,b,author,started):
    require(SOURCE_STATUS=='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED','UNREADY observation runtime refuses native action')
    scope=validate_request(b,author);host,out,control,archive,receipts=[Path(b['namespaces'][k])for k in('host','output','control','source','receipts')];roots5=(host,out,control,archive,receipts)
    require(len(set(roots5))==5 and not any(a.is_relative_to(z)for a in roots5 for z in roots5 if a!=z),'nonoverlapping H/O/C/D/E')
    require(all(p.is_absolute()and p!=support.ART and p.is_relative_to(support.ART)and all(not q.is_symlink()for q in(p,*p.parents))for p in(host,out,control)),'fresh ART H/O/C')
    require(all(p.is_absolute()and p!=support.BASE and p.is_relative_to(support.BASE)for p in(archive,receipts)),'complete Source/receipt D/E separately underB')
    require(not any(os.path.lexists(p)for p in(host,out,control)),'fresh native namespaces zero retry')
    dfreeze,efreeze=tree(archive),tree(receipts);inputs=b['original129_input_pins']+b['additional_actual_evidence_input_pins']+list(author.values())
    tool_roles_by_path={p['path']:role for role,p in b['tool_pins'].items()}
    for p in inputs:recheck(p,tool_role=tool_roles_by_path.get(p['path']))
    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_observer_original619');resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'axmat_observer_original_ebbb');full,production=helper.modules();helper.guard_admission(full)
    require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'genuine unchanged supervisor classes/MRO/modules')
    genuine=[support.pin(support.FULL,support.FULL_SHA),support.pin(support.PARENT,support.PARENT_SHA),support.pin(support.BOUNDED,support.BOUNDED_SHA)]
    history=resource.history_roots([str(p)for p in(host,out,control,Path(support.OUT),Path(support.TERMINAL))],support.ART)
    class JointHistoryResources(resource.DynamicHistoryResources):
        def check(self):
            value=super().check()
            joint=joint_bytes(roots5,b['tool_pins']['lsof']['path'],b['tool_pins']['ps']['path']);require(joint['complete_joint_HOCDE_bytes']<2*2**30,'live full jointHOCDE including open-unlinked2GiB')
            require(tree(archive)==dfreeze and tree(receipts)==efreeze,'complete D/E and all directory/fullSource identities frozen while live')
            require(value['artifact_bytes']+sum(p['size_bytes']for p in dfreeze['files']+efreeze['files'])+joint['open_unlinked_bytes']<=96*2**30,'complete history plus external D/E')
            value.update(joint);return value
    resources=JointHistoryResources(support.ART,history,8*2**30,96*2**30,production.ResourceFailure);runner=None
    def budget():require(time.monotonic()-started<1800,'whole observation build+A/B+closure1800 cap')
    try:
        before=resources.check();require(before['artifact_bytes']+2*2**30<96*2**30 and before['disk_free_bytes']-2*2**30>=8*2**30,'original history/free complete reserve')
        host.mkdir();out.mkdir();control.mkdir();(host/'runtime').mkdir();(host/'OBSERVATION_BUILD').mkdir();shutil.copy2(support.BOUNDED,host/'runtime/run_bounded_dragon.py');require(fullpin(host/'runtime/run_bounded_dragon.py')['sha256']==support.BOUNDED_SHA,'original bounded guard Source bytes')
        runner=full.OwnRSSSerialExecutor(host,1800-(time.monotonic()-started),'OBSERVATION_BUILD',resources)
        require(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==host/'runtime/run_bounded_dragon.py','original genuine guarded runner')
        require(all(runner.env.get(k)=='1'for k in THREAD_KEYS),'all five actual one-thread env')
        runner.env['SPOT_AXMAT_OBSERVATION']='ADMITTED_SOURCE_ONLY'
        native=host/'native';native.mkdir();index=strict_json((archive/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json').read_bytes());index['_path']=str(archive/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json');members={r['relative_path']:r for r in index['members']}
        with tarfile.open(archive/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','r:gz')as t:
            require(len(t.getmembers())==len(members)and {m.name for m in t.getmembers()}==set(members),'whole original native Source archive unique indexed exact count')
            for member in t.getmembers():
                budget();require(member.isfile()and member.name in members and '..'not in Path(member.name).parts and not Path(member.name).is_absolute(),'only complete expected Source members')
                dest=native/member.name;dest.parent.mkdir(parents=True,exist_ok=True)
                with t.extractfile(member)as src,dest.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
                pp=fullpin(dest,budget);require(pp['sha256']==members[member.name]['full_original_Source_pin']['sha256']and pp['size_bytes']==members[member.name]['full_original_Source_pin']['size_bytes'],'all original Source fullEOF archive bytes')
        observer=archive/'OBSERVATION_SOURCE'
        for original,derived in [('LIBMIX.f','LIBMIX.observe.UNREADY.f'),('LIBDEN.f','LIBDEN.observe.UNREADY.f'),('TONDRV.f','TONDRV.context_observe.UNREADY.f'),('TONSPH.f','TONSPH.observe.UNREADY.f')]:
            require(fullpin(native/'Dragon/src'/original)['sha256']==members['Dragon/src/'+original]['full_original_Source_pin']['sha256'],'original physical source before observation overlay');(native/'Dragon/src'/original).write_bytes((observer/derived).read_bytes())
        shutil.copy2(observer/'AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90',native/'Dragon/src/AXMAT_CONTEXT_OBSERVATION_MOD.f90')
        ep,build=compile_all(native,index,observer,b['tool_pins'],runner,support,resources,budget);write_new(control/'ACTUAL_COMPLETE_NATIVE_SOURCE_BINARY_LINK_EVIDENCE.json',build);bp=fullpin(control/'ACTUAL_COMPLETE_NATIVE_SOURCE_BINARY_LINK_EVIDENCE.json',budget);states={}
        for state in('A','B'):
            budget();recheck(ep,budget);folder=out/state;folder.mkdir();seeds=b['states'][state]['native_stage_inputs'];seedCopies=[]
            for row in seeds:
                recheck(row['input_pin'],budget);dest=folder/row['destination'];require(not os.path.lexists(dest),'fresh immutable material input copy')
                with Path(row['input_pin']['path']).open('rb')as src,dest.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
                actual=fullpin(dest,budget);require(actual['sha256']==row['input_pin']['sha256']and actual['size_bytes']==row['input_pin']['size_bytes'],'original material seed bytes unchanged');seedCopies.append(actual)
            resources.check();stage=guarded(runner,support,resources,folder,'material',[ep['path']],time.monotonic()+600,budget,deck='material.x2m',marker='AXMAT-MATERIAL-'+state+'-COMPLETE')
            for p in seedCopies:recheck(p,budget)
            states[state]=collect_state(folder,state,b['states'][state]['original_material_deck_pin'],ep,stage,budget)
            states[state]['actual_material_seed_copy_pins']=seedCopies
            recheck(ep,budget)
            # This block has no open stream/SQLite/native handle. All host pins
            # and snapshot reads have exited their with blocks before B starts.
            closure=resources.check();require(not any(Path(v).is_relative_to(folder)for v in closure['actual_open_regular_paths']),'all own process material state handles closed before next state');states[state]['actual_no_open_state_handles_observation']=closure;write_new(control/('ACTUAL_'+state+'_CLOSED_OBSERVATION_CAPTURE.json'),states[state]);resources.check()
        manifest=dict(schema='ACTUAL_COMPLETE_AXOBSCTXv2_AB_OBSERVATION_MANIFEST_V1',source_only=False,state_order=['A','B'],states=states,complete_state_snapshot_inputs={k:v['complete_state_snapshot_inputs']for k,v in states.items()},complete_context_inputs={k:v['complete_context_pins']for k,v in states.items()},legacy_context_source_snapshot_request_rows={k:v['legacy_context_source_snapshot_request_rows']for k,v in states.items()},legacy_context_root_prefix_semantics='output_pool_logical_path_prefix_only_not_native_directory_lookup',actual_native_snapshot_root_prefix=[],all_A_handles_closed_before_B=True,actual_Source_binary_link_evidence_pin=bp,actual_observer_executable_pin=ep,independent_observation_Source_admission_pin=b['independent_observation_Source_admission_pin'],actual_Source_scope_coupling=scope,original_caps=CAPS,actual_material_build_and_observation_executed=True,Root_observed_tool_terminal=None,Root_postclose_coverage_contract=None,new_native_walker_controls_actual_run=None,new_complete_aggregation_controls_actual_run=None,actual_frozen_native_Source_object_link_exe_evidence_saved=True,**FUTURE)
        write_new(out/'ACTUAL_AB_AXOBSCTXv2_OBSERVATION_MANIFEST.json',manifest);mp=fullpin(out/'ACTUAL_AB_AXOBSCTXv2_OBSERVATION_MANIFEST.json',budget)
        for p in inputs:recheck(p,budget,tool_role=tool_roles_by_path.get(p['path']))
        after=resources.check();require(tree(archive)==dfreeze and tree(receipts)==efreeze,'whole D/E final freeze');budget()
        value=dict(schema='ACTUAL_COMPLETE_NATIVE_OBSERVATION_BUILD_GENUINE_HOST_RESULT_V1',status='ACTUAL_COMPLETE_FIVE_STAGE_BUILD_AND_AB_OBSERVATION_EVIDENCE_ONLY_EXTERNAL_ROOT_CLOSURE_REQUIRED',source_only=False,actual_host_PID=os.getpid(),original_caps=CAPS,original_helper_pin=hpin,resource_factory_pin=rpin,genuine_guard_pins=genuine,supervisor_class_or_MRO_modified=False,own_child_RSS_scope_only=True,compiler_descendant_RSS_scope_not_certified=True,actual_build_evidence_pin=bp,actual_observation_manifest_pin=mp,all_stage_records=runner.records,complete_input_pins_before_and_after=inputs,complete_Source_D_freeze=dfreeze,complete_receipt_E_freeze=efreeze,resources_before=before,resources_after=after,whole_seconds=time.monotonic()-started,actual_Source_scope_coupling=scope,actual_Root_observed_terminal=None,**FUTURE)
        write_new(host/'result.json',value);resources.check();budget();print(json.dumps(dict(status=value['status'],actual_host_result_pin=fullpin(host/'result.json'),actual_observation_manifest_pin=mp,actual_build_evidence_pin=bp,actual_external_Root_typed_CLOSED_required=True,**FUTURE),allow_nan=False),flush=True)
    except BaseException as error:
        if host.is_dir():
            freeze_errors=[];after_inputs=[];after_D_E=None;after_resources=None
            for p in inputs:
                try:after_inputs.append(recheck(p,tool_role=tool_roles_by_path.get(p['path'])))
                except BaseException as e:freeze_errors.append(dict(path=p['path'],error=repr(e)))
            try:
                after_D_E=dict(Source=tree(archive),receipts=tree(receipts));require(after_D_E==dict(Source=dfreeze,receipts=efreeze),'failed complete D/E differs');after_resources=resources.check()
            except BaseException as e:freeze_errors.append(dict(scope='failed_D_E_and_resource',error=repr(e)))
            write_new(host/'failed_host_result.json',dict(schema='FAILED_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_RESULT_V1',status='FAILED_NO_RETRY_NO_QUALIFICATION',error=repr(error),complete_input_pins_before=inputs,complete_input_pins_after_failure=after_inputs,complete_D_E_freeze_before=dict(Source=dfreeze,receipts=efreeze),complete_D_E_freeze_after_failure=after_D_E,full_postfailure_freeze_errors=freeze_errors,full_postfailure_freeze_checked=(freeze_errors==[]),actual_resources_after_failure=after_resources,all_stage_records=[]if runner is None else runner.records,actual_observation_manifest_pin_if_saved=fullpin(out/'ACTUAL_AB_AXOBSCTXv2_OBSERVATION_MANIFEST.json')if (out/'ACTUAL_AB_AXOBSCTXv2_OBSERVATION_MANIFEST.json').is_file()else None,whole_seconds=time.monotonic()-started,original_caps=CAPS,actual_Root_observed_terminal=None,**FUTURE))
        raise
