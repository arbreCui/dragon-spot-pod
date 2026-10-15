"""Only stdlib Source sealing; reviewed candidates never executed."""
import ast, hashlib, json, os, stat
from pathlib import Path
P=Path(__file__).resolve().parent
S=P.with_name(P.name+'_seal_receipt')
def require(v,m):
    if type(v)is not bool or not v:raise ValueError(m)
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    s=p.lstat();require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'real Source no aliases')
    with p.open('rb')as f:
        require(ident(os.fstat(f.fileno()))==ident(s),'Source open7ID')
        h=hashlib.file_digest(f,'sha256').hexdigest();require(ident(os.fstat(f.fileno()))==ident(s),'Source EOF7ID')
    require(ident(p.lstat())==ident(s),'Source path7ID')
    return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=ident(s))
def inventory():
    rows=[]
    for f in sorted(P.rglob('*')):
        require(not f.is_symlink(),'all complete Source aliases forbidden')
        if f.is_dir():continue
        require(f.is_file(),'all complete Source specialfiles forbidden')
        if f==P/'MANIFEST.json':continue
        rows.append(dict(relative_path=str(f.relative_to(P)),**pin(f)))
    return rows
def dirs():
    return {str(f):ident(f.lstat())for f in[P,*sorted(P.rglob('*'))]if f.is_dir()}
report=json.loads((P/'STATIC_STRICT_SCOPE_NATIVE_HOST_BINDER_SOURCE_REVIEW.json').read_bytes())
require(report['source_only']is True and report['all_checks_passed']is True and report['blockers']==[],'author Source review only')
require(type(report['check_count'])is int and report['check_count']==len(report['checks'])==1816 and all(v['passed']is True for v in report['checks']),'full actual Source checks')
truth=json.loads((P/'actual_strict_scope_static_review_PASS_tool_return.json').read_bytes())
t=truth['terminal_tool_return'];require(truth['closed']is True and truth['observed_terminal']is True and truth['session_repolled_after_close']is False and truth['actual_terminal_chunk']==t['chunk_id']=='3f0f9d'and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t,'actual Source review typed0 CLOSED truth')
returned=json.loads(t['output'])
for key in('host_template','checker_template','binder'):require(pin(Path(report[key]['path']))==report[key]==returned[key],'all actualSourcebody fullpin truth')
require(returned['report']==pin(P/'STATIC_STRICT_SCOPE_NATIVE_HOST_BINDER_SOURCE_REVIEW.json'),'actual full reportpin')
for f in sorted(P.rglob('*.py')):ast.parse(f.read_bytes(),filename=str(f))
# Creating the excluded manifest before recording directories keeps root identity honest.
with(P/'MANIFEST.json').open('xb')as stream:
    rows=inventory();directory=dirs()
    value=dict(schema='COMPLETE_NATIVE_GENUINE_HOST_BINDER_STRICT_SCOPE_UNREADY_SOURCE_MANIFEST_V1',source_only=True,status='UNREADY_SOURCE_ONLY',member_count=len(rows),total_member_bytes=sum(v['size_bytes']for v in rows),members=rows,directories=directory,full_scope_retained=True,all_original129_inputs_retained=True,parent_source_full_copy_count=67,originalCaps=report['original_caps'],future_actual_Source_admission=None,future_actual_BUILD=None,future_actual_genuine_host=None,future_native_qualification_sha256=None,future_scientific_qualification_sha256=None,new_native_walker_controls_actual_run=None,original_XSM_memory_bits_verified=False,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,original_native_build_binary_Source_linkage_qualified=False,no_candidate_helper_API_guard_compile_business_or_material_payload_execution=True)
    stream.write((json.dumps(value,indent=2,allow_nan=False)+'\n').encode())
require(inventory()==rows and dirs()==directory,'entire Source package and directories unchanged')
mp=pin(P/'MANIFEST.json')
S.mkdir()
seal=dict(schema='ACTUAL_COMPLETE_NATIVE_STRICT_SCOPE_UNREADY_SOURCE_SEAL_V1',source_only=True,manifest=mp,member_count=len(rows),total_member_bytes=value['total_member_bytes'],all_full_EOF_SHA7ID_and_directories_unchanged=True,author_static_Source_actual_terminal_chunk='3f0f9d',author_static_Source_check_count=1816,review=pin(P/'STATIC_STRICT_SCOPE_NATIVE_HOST_BINDER_SOURCE_REVIEW.json'),host_template=report['host_template'],checker_template=report['checker_template'],binder=report['binder'],members=rows,directories=directory,no_candidate_execution=True,no_original_Source_project_ART_frozen_D_E_write=True,actual_native_execution=None,actual_native_or_science_qualification_sha256=None)
with(S/'SOURCE_SEAL.json').open('x')as f:json.dump(seal,f,indent=2,allow_nan=False);f.write('\n')
require(pin(P/'MANIFEST.json')==mp and inventory()==rows and dirs()==directory,'all fixed Source remains unchanged after seal')
print(json.dumps(dict(source_only=True,manifest=mp,member_count=len(rows),total_member_bytes=value['total_member_bytes'],seal=pin(S/'SOURCE_SEAL.json'),host_template=report['host_template'],checker_template=report['checker_template'],binder=report['binder'],all_full_EOF_SHA7ID_and_directories_unchanged=True,no_candidate_API_helper_guard_business_or_native_reader_execution=True),indent=2,allow_nan=False),flush=True)
