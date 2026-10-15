"""Independent complete current ten-control Source admission; no OS children.

Imports original definitions and checks original read-only resource methods.
No executor/observer instance is constructed and no PS/lsof/compiler/business
command, numerical solver, deadline reset or old qualification is performed.
"""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import stat
import sys
import time

sys.dont_write_bytecode=True
R=Path('/Users/wen/spot');V=R/'validation/axial_material';ART=R/'validation/artifacts'
BASE=V/'complete_history_root_index_source_v15_20261010'
REC=V/'native_frame_encoder_epoch_recovery_20261011'
D=BASE/'actual_frame_encoder_current_epoch_monitor_controls_sources_20261011'
E=BASE/'actual_frame_encoder_current_epoch_monitor_controls_receipts_20261011'
BINDING=D/'Root_current_fresh_frame_controls_Source_binding.json'
OLD_D=BASE/'actual_invalid_prepost_d19_monitor_controls_sources_20261011'
START=time.monotonic()
FIELDS=('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
CHECKS=[]

def require(value,message):
    if type(value)is not bool or not value:raise ValueError(message)

def check(value,message):
    require(value,message);CHECKS.append(message)

def budget():
    require(time.monotonic()-START<600,'independent Source metadata600 cap')
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':peak*=1024
    require(peak<512*2**20,'independent Source self512MiB cap')

def identity(s):return [getattr(s,k)for k in FIELDS]

def pin(path,single=True):
    budget();path=Path(path);before=identity(path.lstat())
    require(path.is_absolute()and all(not p.is_symlink()for p in(path,*path.parents))and stat.S_ISREG(before[2])and(before[3]==1 if single else before[3]>=1),'actual noalias regular Source/tool pin')
    digest=hashlib.sha256();size=0
    with path.open('rb')as stream:
        require(identity(os.fstat(stream.fileno()))==before,'pin actual opened identity')
        while True:
            budget();raw=stream.read(2**20)
            if not raw:break
            digest.update(raw);size+=len(raw)
        require(identity(os.fstat(stream.fileno()))==before,'pin actual complete EOF identity')
    require(identity(path.lstat())==before and size==before[4],'pin actual closed identity')
    return dict(path=str(path),sha256=digest.hexdigest(),size_bytes=size,identity=before)

def strict(raw):
    def pairs(items):
        out={}
        for key,value in items:require(key not in out,'unique actual META keys');out[key]=value
        return out
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))

def verify(p,single=True):
    require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int
        and type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'four-field typed exact full pin')
    actual=pin(p['path'],single);check(actual==p,'exact actual current full EOF: '+p['path']);return actual

def load(path,sha,name):
    before=pin(path);check(before['sha256']==sha,'original definition Source SHA '+str(path))
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    check(Path(module.__file__).resolve()==Path(path).resolve()and pin(path)==before,'original actual import binding '+str(path));return module,before

def tree(folder):
    out=[];dirs=[]
    for parent,ds,ns in os.walk(folder,followlinks=False):
        budget()
        for name in ds:
            p=Path(parent)/name;s=p.lstat();require(stat.S_ISDIR(s.st_mode)and not p.is_symlink(),'ordinary frozen Source directory');dirs.append(dict(path=str(p),identity=identity(s)))
        for name in ns:out.append(pin(Path(parent)/name))
    return dict(files=sorted(out,key=lambda p:p['path']),directories=sorted(dirs,key=lambda p:p['path']))

def main():
    check(os.environ.get('PYTHONDONTWRITEBYTECODE')=='1'and all(os.environ.get(k)=='1'for k in THREADS)
        and not sys.flags.optimize and sys.gettrace()is None and sys.getprofile()is None,'original one-thread/nonoptimized/unprofiled Source review environment')
    check(not(E/'Source_prelaunch_review.json').exists(),'fresh independent review output')
    binding_pin=pin(BINDING);check(binding_pin['sha256']=='e015b9e73e6dcfabaf6541cddb48909194bf970705516ae163f08fb658cc3f70','exact Root-created current Source binding SHA')
    b=strict(BINDING.read_bytes());old_pin=pin(OLD_D/'Root_fresh_frame_controls_Source_binding.json');old=strict(Path(old_pin['path']).read_bytes())
    oldbase_path=Path(old['original_N9_controls_Source_binding_pin']['path']);oldbase_pin=pin(oldbase_path);oldbase=strict(oldbase_path.read_bytes())
    old_before=[old_pin,oldbase_pin]
    dfreeze=tree(D);efreeze=tree(E)
    check(b['schema']=='ROOT_FRESH_FRAME_MONITOR_CONTROLS_SOURCE_BINDING_V1'and b['source_only']is True
        and b['policy']==old['policy']=='FRESH_COMPLETE_CURRENT_CENSUS_TOTAL_2S_V1','exact fresh-frame Source-only schema/policy')
    check(b['original_caps']==CAPS and all(type(v)is int for v in b['original_caps'].values())and b['original_caps_changed']is False,'all nine exact typed original caps')
    check(b['actual_control_execution']is None and b['old_controls_qualification_inherited']is False
        and b['Native_or_scientific_qualification_created']is False and b['current_device_observed_not_normalized']is True,'new current Source only/no old Q or device normalization')
    ap=verify(b['adapter_Source_pin']);cp=verify(b['control_entry_Source_pin']);bp=verify(b['original_N9_controls_Source_binding_pin'])
    check(ap['path']==str(D/'fresh_frame_observation_adapter.py')and cp['path']==str(D/'fresh_frame_genuine_controls.py'),'exact new durable installed runtime/entry paths')
    check(ap['sha256']=='70d2a5abb8379e825d186b933ac4a55c7434b90984f9ca89c23dc442c8e857af'
        and cp['sha256']=='05adf2836e260c56e5ab2b39ee146eae1e1c2082b1a7843f0a59f7f191c5ffe6','exact independently reviewed encoder and complete ten-control bytes')
    original_adapter=(OLD_D/'fresh_frame_observation_adapter.py').read_text();adapter=Path(ap['path']).read_text();helper=(REC/'added_pure_encoder_Source.py').read_text()
    oldloop="""            raw=None
            for serialization in range(8):
                budget()
                candidate=(json.dumps(event,ensure_ascii=False,allow_nan=False)+'\\n').encode('utf-8')
                size=len(candidate)
                if account['additional_record_bytes']==size:
                    raw=candidate;break
                account['additional_record_bytes']=size
"""
    newcall='            raw=complete_frame_self_accounted_UTF8(event,account,budget)\n'
    check(adapter.count(helper)==1 and adapter.count(newcall)==2 and adapter.replace(helper,'',1).replace(newcall,oldloop)==original_adapter,'full installed adapter byte inverse: sole pure helper/two loops/all OS-account-fsync-2s/MRO code unchanged')
    original_control=(OLD_D/'fresh_frame_genuine_controls.py').read_text();control=Path(cp['path']).read_text()
    old_sha='a2b507e0f5e5470c227484f1d8a1e63367aed2313cb15695a9c46b57a2d444cc'
    newliteral="ADAPTER_SHA='"+ap['sha256']+"'";oldliteral="ADAPTER_SHA='"+old_sha+"'"
    check(control.count(newliteral)==1 and control.replace(newliteral,oldliteral,1)==original_control,'full installed ten-control byte inverse: sole adapter SHA change')
    ast.parse(adapter);ast.parse(control)
    for name in('ACTUAL_PURE_SERIALIZATION_REVIEW.json','INDEPENDENT_ENCODER_REVIEW.json'):
        expected=b['actual_pure_review_current_pin']if name.startswith('ACTUAL_')else b['actual_independent_encoder_review_current_pin']
        verify(expected);review=strict(Path(expected['path']).read_bytes())
        check(review['actual_goal_achieved']is False and(review.get('actual_native_complete_build_qualified',review.get('actual_native_build_qualified'))is False),'saved encoder review scope limited '+name)
    base=strict(Path(bp['path']).read_bytes());author=base['actual_author_Source_contract'];oldauthor=oldbase['actual_author_Source_contract']
    check(base['schema']=='ROOT_ACTUAL_N8_MONITOR_CONTROLS_SOURCE_BINDING_V1'and base['source_only']is True
        and base['original_caps']==CAPS and base['actual_control_execution']is None and base['old_qualification_inherited']is False,'new original21 Source-only base contract')
    check(set(author)==set(oldauthor)and len(author)==21,'all exact original 21 author roles retained')
    lineages={row['role']:row for row in base['complete_Source_lineage']}
    check(set(lineages)==set(author)and len(base['complete_Source_lineage'])==21,'one complete current/historical lineage per author role')
    for role,p in author.items():
        actual=verify(p);historical=oldauthor[role];lineage=lineages[role]
        check(actual['sha256']==historical['sha256']and actual['size_bytes']==historical['size_bytes'],'actual original full author bytes preserved '+role)
        check(Path(actual['path']).is_relative_to(D/'original_author_sources')and lineage['historical_pin']==historical
            and lineage['new_current_pin']==actual,'original author historical/current identity explicitly separated '+role)
        recovered=verify(lineage['actual_recovered_pin']);check(recovered['sha256']==actual['sha256']and recovered['size_bytes']==actual['size_bytes'],'same-byte real recovered source '+role)
    check(b['owner_helper_Source_pin']==author['owner_scope_helper'],'current exact owner helper from actual author')
    for role,p in b['tool_pins'].items():
        actual=verify(p,False);check(actual['sha256']==oldbase['tool_pins'][role]['sha256']and actual['size_bytes']==oldbase['tool_pins'][role]['size_bytes'],'actual original OS/compiler tool full bytes preserved '+role)
    check(set(b['tool_pins'])==set(oldbase['tool_pins'])and b['tool_pins']==base['tool_pins'],'all tool roles equal new current base')
    std=verify(b['actual_stdlib_subprocess_Source_pin'],False)
    check(std==base['actual_stdlib_subprocess_Source_pin']and std['path']==oldbase['actual_stdlib_subprocess_Source_pin']['path']
        and std['sha256']==oldbase['actual_stdlib_subprocess_Source_pin']['sha256']and std['size_bytes']==88747,'exact positive-link-count current original subprocess Source')
    verify(b['historical_d19_binding_current_pin']);verify(base['historical_original_binding_current_pin']);verify(base['actual_same_byte_recovery_report_pin'])
    check(b['historical_d19_binding_current_pin']==old_pin and base['historical_original_binding_current_pin']==oldbase_pin,'original bindings unchanged/read as historical lineage')
    order=['closed-before-first','exit7','transient','unlinked-duplicates','escaped','echild','unobserved-cache','deadline','persistent-topology','journal-failure']
    check(b['case_execution_order']==old['case_execution_order']==order and set(b['case_namespaces'])==set(order),'all ten original cases in original serial order')
    check(b['all_actual_cases_serial']is True and b['shared_new_Source_and_receipts_frozen_before_any_case']is True,'one shared durable D/E/serial cases contract')
    all_hoc=[]
    for case in order:
        ns=b['case_namespaces'][case];roots=tuple(Path(ns[k])for k in('host','output','control','source','receipts'))
        check(set(ns)=={'host','output','control','source','receipts'}and roots[3:]==(D,E),'exact current shared D/E '+case)
        check(len(set(roots))==5 and not any(p.is_relative_to(q)for p in roots for q in roots if p!=q),'all HOCDE nonoverlapping '+case)
        check(all(p.is_absolute()and p!=ART and p.is_relative_to(ART)and all(not q.is_symlink()for q in(p,*p.parents))
            and not os.path.lexists(p)for p in roots[:3]),'all real fresh HOC absent/no aliases/zero retry '+case)
        all_hoc.extend(roots[:3])
    check(len(set(all_hoc))==30,'distinct real fresh HOC for all ten cases')
    support_path=BASE/'actual_prepare_sources/prepare_cli_host_v15.py'
    support,support_pin=load(support_path,'3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7','independent_controls_original_support')
    check(Path(sys.executable).resolve()==support.PYTHON,'exact original Python interpreter')
    h,hp=load(support.OLD_HELPER,support.OLD_HELPER_SHA,'independent_controls_original_helper')
    resource_factory,rp=load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'independent_controls_original_resource_factory')
    full,production=h.modules();guard_paths=h.guard_admission(full)
    guard_pins=[pin(p)for p in guard_paths]
    check(Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT
        and full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,), 'loaded genuine original OwnRSSSerialExecutor/SerialExecutor MRO and actual source paths')
    guard_sources=[support_pin,hp,rp,pin(support.FULL),pin(support.PARENT),pin(support.BOUNDED)]
    for p,sha in((support.FULL,support.FULL_SHA),(support.PARENT,support.PARENT_SHA),(support.BOUNDED,support.BOUNDED_SHA)):
        check(pin(p)['sha256']==sha,'genuine full unchanged guard Source '+str(p))
    owner,op=load(author['owner_scope_helper']['path'],author['owner_scope_helper']['sha256'],'independent_controls_original_owner')
    check(owner.actual_stdlib_Source(std)==std,'actual original owner helper verifies true current loaded subprocess Source')
    methods=[]
    for cls,names in((full.OwnRSSSerialExecutor,['_process']),(production.SerialExecutor,['_process','execute']),
        (production.DiskResources,['check']),(resource_factory.DynamicHistoryResources,['check'])):
        for name in names:
            fn=getattr(cls,name);methods.append(dict(class_name=cls.__name__,method=name,
                actual_code_filename=fn.__code__.co_filename,first_line=fn.__code__.co_firstlineno))
    check(all(Path(row['actual_code_filename']).resolve()in{support.FULL,support.PARENT,support.RESOURCE_FACTORY}for row in methods),'loaded original process/execute/disk/history method Source filenames')
    roots=resource_factory.history_roots([str(p)for p in all_hoc]+[str(support.OUT),str(support.TERMINAL)],ART)
    resources=resource_factory.DynamicHistoryResources(ART,roots,8*2**30,96*2**30,production.ResourceFailure)
    actual_resource=resources.check();external=sum(p['size_bytes']for p in dfreeze['files']+efreeze['files'])
    check(actual_resource['artifact_bytes']+external+2*2**30<96*2**30,'original complete-history reserve for genuine controls within 96GiB')
    check(actual_resource['artifact_bytes']+external+20971764748+64*2**20<96*2**30,'retained original cold-storage reserve/current D-E/metadata64MiB within history96GiB')
    check(actual_resource['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original entire-filesystem free8GiB/cold/fresh joint reserves')
    check(tree(D)==dfreeze and tree(E)==efreeze,'all D/E full Source and directory identities unchanged throughout review')
    check([pin(p['path'])for p in old_before]==old_before and pin(BINDING)==binding_pin,'old bindings and exact new binding unchanged after original imports/read-only checks')
    budget()
    result=dict(schema='INDEPENDENT_FRESH_FRAME_MONITOR_CONTROLS_SOURCE_PRELAUNCH_REVIEW_V1',
        source_only=True,all_checks_passed=True,blockers=[],new_Source_binding_pin=binding_pin,
        adapter_Source_pin=ap,control_entry_Source_pin=cp,original_N9_current_Source_binding_pin=bp,
        reviewer_Source_pin=pin(Path(__file__).resolve()),all_actual_checks=CHECKS,check_count=len(CHECKS),
        complete_original21_current_author_pins=author,current_tool_pins=b['tool_pins'],current_stdlib_Source_pin=std,
        original_guard_Source_pins=guard_sources,original_readonly_guard_admission_input_pins=guard_pins,
        loaded_original_method_Source_bindings=methods,original_caps=CAPS,original_case_order=order,
        all_thirty_HOC_namespaces_fresh=True,complete_D_freeze_before_review=dfreeze,
        complete_E_freeze_before_own_review=efreeze,actual_original_readonly_resource_check=actual_resource,
        actual_D_E_bytes_before_own_review=external,cold_storage_reserve_bytes=20971764748,
        pure_encoder_scope_limited_to_actual_owned_single_account_callers=True,
        actual_PS_lsof_or_child_executed=False,actual_compiler_or_numeric_solver_executed=False,
        old_controls_qualification_inherited=False,actual_genuine_controls_qualified=False,
        actual_fixed2s_window_qualified=False,actual_native_build_qualified=False,
        scientific_qualification_created=False,actual_goal_achieved=False,
        actual_elapsed_seconds=time.monotonic()-START,actual_self_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    path=E/'Source_prelaunch_review.json'
    with path.open('x',encoding='utf-8')as stream:json.dump(result,stream,ensure_ascii=False,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    print(json.dumps(dict(status='INDEPENDENT_CURRENT_TEN_CONTROL_SOURCE_PRELAUNCH_PASS_NO_EXECUTION',review_pin=pin(path),
        checks=len(CHECKS),original_author_roles=len(author),original_MRO_and_guard_readonly_admission=True,
        all_HOC_fresh=True,actual_genuine_controls_qualified=False),allow_nan=False),flush=True)

if __name__=='__main__':main()
