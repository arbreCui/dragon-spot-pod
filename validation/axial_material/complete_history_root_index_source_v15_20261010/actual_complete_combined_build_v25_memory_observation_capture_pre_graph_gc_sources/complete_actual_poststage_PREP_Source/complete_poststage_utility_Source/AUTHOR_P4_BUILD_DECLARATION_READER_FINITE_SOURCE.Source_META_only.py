"""Fresh P4 single-read-function Source derivative; no candidate/API execution."""
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile

OLD=Path('/private/tmp/axmat_V25_memory_observation_capture_namespace_ONLY_UNREADY_Source_20261011_13_9k38l')
FAILED=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_memory_observation_capture_BUILD_Source_binding_declaration_reader_failure_tool_terminal_return.json')
NAME='bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py'
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    before=ident(p.lstat());assert p.is_absolute()and stat.S_ISREG(before[2])and before[3]==1 and all(not q.is_symlink()for q in(p,*p.parents))
    with p.open('rb')as f:assert ident(os.fstat(f.fileno()))==before;h=hashlib.file_digest(f,'sha256').hexdigest();assert ident(os.fstat(f.fileno()))==before
    assert ident(p.lstat())==before
    return dict(path=str(p),sha256=h,size_bytes=before[4],identity=before)
def write(p,v):
    with p.open('x')as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
def definitions(s):return {n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def inverse(s,rows):
    for r in reversed(rows):assert s.count(r['new'])==r['count'],r['label'];s=s.replace(r['new'],r['old'])
    return s
def main():
    checks=[]
    def check(n,v):assert type(v)is bool and n not in{c['check']for c in checks};checks.append(dict(check=n,passed=v));assert v,n
    originalmfpin=pin(OLD/'MANIFEST.json');check('actual_frozen_P4_manifest_expected_SHA',originalmfpin['sha256']=='c100e191a6d841465fe9eb36999c7cbf2c45c7be94569bdc43b66f9cfc751538')
    mf=json.loads((OLD/'MANIFEST.json').read_bytes());check('P4_whole_member_and_directory_sets',set(mf['members'])=={str(q.relative_to(OLD))for q in OLD.rglob('*')if q.is_file()and q!=OLD/'MANIFEST.json'}and set(mf['directories'])=={'.'}|{str(q.relative_to(OLD))for q in OLD.rglob('*')if q.is_dir()})
    for rel,p in mf['members'].items():check('original_P4_complete_EOF_7ID:'+rel,pin(OLD/rel)==p)
    check('original_P4_complete_directory_freeze',{'.':ident(OLD.lstat()),**{str(q.relative_to(OLD)):ident(q.lstat())for q in OLD.rglob('*')if q.is_dir()}}==mf['directories'])
    failed=json.loads(FAILED.read_bytes());t=failed['terminal_tool_return'];check('actual_Source_binder_failure_CLOSED_int1_before_output',failed['closed']is True and failed['observed_terminal']is True and type(t['exit_code'])is int and t['exit_code']==1 and t['chunk_id']=='0b88da'and 'session_id'not in t and failed['actual_BUILD_or_candidate_executed']is False)
    P=Path(tempfile.mkdtemp(prefix='axmat_P4_BUILD_exact_declaration_reader_minimal_UNREADY_Source_',dir='/private/tmp'))
    for q in sorted(OLD.rglob('*')):
        target=P/q.relative_to(OLD)
        if q.is_dir():target.mkdir()
        elif q!=OLD/'MANIFEST.json':shutil.copy2(q,target)
    history=P/'DECLARATION_READER_P4_ORIGINAL_PROVENANCE';history.mkdir()
    for rel,label in [('MANIFEST.json','ORIGINAL_P4_MANIFEST.json'),(NAME,'ORIGINAL_P4_BUILD_BINDER.full.py'),('COMPLETE_SOURCE_INVERSES.json','ORIGINAL_P4_ACTUAL_CONSUMED_COMPLETE_SOURCE_INVERSES.json')]:shutil.copy2(OLD/rel,history/label)
    shutil.copy2(FAILED,history/FAILED.name)
    s=(OLD/NAME).read_text();old=definitions(s)['read']
    new="""def read(p):
    p=normal(p)
    declaration=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-20261010'/'declaration.json'
    if p==declaration:
        # This one declared META role is bounded before its first EOF read.
        # Graph, trace, gzip, material and other ART declaration paths remain
        # forbidden by the unchanged old whitelist below.
        before=identity(p)
        if not stat.S_ISREG(before[2])or before[3]!=1 or not 0<=before[4]<=16*2**20:raise ValueError('exact capture declaration regular singlelink META at most16MiB required')
        fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
        try:
            opened=os.fstat(fd)
            if [opened.st_dev,opened.st_ino,opened.st_mode,opened.st_nlink,opened.st_size,opened.st_mtime_ns,opened.st_ctime_ns]!=before:raise ValueError('capture declaration opened descriptor identity differs')
            with os.fdopen(fd,'rb')as stream:
                fd=None
                raw=stream.read(16*2**20+1)
                if len(raw)>16*2**20 or len(raw)!=before[4]or stream.read(1)!=b'':raise ValueError('complete bounded capture declaration EOF required')
                finished=os.fstat(stream.fileno())
                if [finished.st_dev,finished.st_ino,finished.st_mode,finished.st_nlink,finished.st_size,finished.st_mtime_ns,finished.st_ctime_ns]!=before:raise ValueError('capture declaration same descriptor changed across EOF')
        finally:
            if fd is not None:os.close(fd)
        if identity(p)!=before:raise ValueError('capture declaration path identity changed across EOF')
        actual=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=before[4],identity=before)
        E=BASE/'actual_complete_combined_prepare_v25_memory_observation_capture_receipts'
        summary_path=E/'Root_actual_complete_combined_prepare_summary.json';namespace_path=E/'Root_actual_complete_prepare_namespace_manifest.json'
        if str(summary_path)not in READ_PINS or str(namespace_path)not in READ_PINS:raise ValueError('original complete PREP summary and namespace must be pinned before declaration META')
        summary=read(summary_path);namespace=read(namespace_path)
        owners=[row for row in namespace['namespaces']if row['root']==str(declaration.parent)]
        if len(owners)!=1:raise ValueError('exact capture declaration namespace owner required')
        wanted=helper_Q_fullpin(summary['actual_declaration'])
        if helper_Q_fullpin(owners[0]['files']['declaration.json'])!=wanted or actual!=wanted:raise ValueError('capture declaration bounded EOF SHA7ID differs from actual complete PREP namespace and summary')
        if str(p)in READ_PINS and READ_PINS[str(p)]!=actual:raise ValueError('repeated Source/META differs')
        value=strict_json_bytes(raw)
        if identity(p)!=before:raise ValueError('capture declaration changed during strict META decode')
        READ_PINS[str(p)]=actual
        return value
    # Original three ART proof roles and original Source/META reader remain.
    if p.is_relative_to(ART)and p.name not in ('result.json','ACTUAL_REPORT.json','ACTUAL_PRIVATE_INACTIVE_AUDIT_SNAPSHOT_CONTROLS.json'):raise ValueError('no ART graph/trace/payload decoding in Source binding')
    before=source_pin(p);value=strict_json_bytes(p.read_bytes())
    if source_pin(p)!=before:raise ValueError('Source/META JSON changed')
    return value"""
    assert s.count(old)==1;s=s.replace(old,new,1);ast.parse(s);(P/NAME).write_text(s)
    proof=json.loads((OLD/'COMPLETE_SOURCE_INVERSES.json').read_bytes());row=dict(label='exact_current_capture_declaration_bounded_nofollow_SAME_FD_Source_META_read',old=old,new=new,count=1);proof['exact_finite_transforms']['build_binder'].append(row)
    entries=proof['definitions_by_role']['build_binder']['unchanged_original_definition_occurrences'];matched=[r for r in entries if r['name']=='read'];check('one_current_consumed_inverse_read_preservation_claim_updated',len(matched)==1 and matched[0]['whole_bytes_and_AST_unchanged']is True);matched[0]['whole_bytes_and_AST_unchanged']=False
    (P/'COMPLETE_SOURCE_INVERSES.json').write_text(json.dumps(proof,indent=2,allow_nan=False)+'\n')
    oldproof=json.loads((OLD/'COMPLETE_SOURCE_INVERSES.json').read_bytes());roles=proof['role_current_paths'];check('all_original_fourteen_role_paths_and_parent_fullpins',len(roles)==14 and roles==oldproof['role_current_paths']and proof['original_parent_fullpins']==oldproof['original_parent_fullpins'])
    records={};p3proof=json.loads((OLD/'CAPTURE_NAMESPACE_COMPLETE_14_ROLE_BYTE_AST_AND_JSON_INVERSES.json').read_bytes())
    for role,rel in roles.items():
        text=(P/rel).read_text();parent=(OLD/rel).read_text();rows=[row]if role=='build_binder'else[]
        recovered=inverse(text,rows);check('whole14_current_to_P4_byte_AST:'+role,recovered==parent and ast.dump(ast.parse(recovered),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False))
        p3=inverse(recovered,p3proof['roles'][role]['namespace_finite_transforms']);p3original=Path(p3proof['roles'][role]['actual_P3_role_pin']['path']).read_text();check('whole14_current_to_formal_V3_byte_AST:'+role,p3==p3original and ast.dump(ast.parse(p3),include_attributes=False)==ast.dump(ast.parse(p3original),include_attributes=False))
        base=inverse(text,proof['exact_finite_transforms'][role]);original=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text();check('whole14_actual_both_binder_consumed_proof_to_original_parent:'+role,base==original and ast.dump(ast.parse(base),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False))
        if role!='build_binder':check('thirteen_other_whole_role_Source_byteexact:'+role,text==parent)
        records[role]=dict(relative_path=rel,current_complete_Source_pin=pin(P/rel),actual_P4_role_pin=pin(OLD/rel),current_to_P4_exact_transforms=rows,P4_to_formally_reviewed_V3_namespace_transforms=p3proof['roles'][role]['namespace_finite_transforms'],actual_original_parent_retained_Source_pin=pin(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')),whole_P4_V3_original_parent_byte_AST_inverse=True)
    beforedefs,afterdefs=definitions((OLD/NAME).read_text()),definitions(s)
    check('only_one_build_binder_function_read_changes',set(beforedefs)==set(afterdefs)and all(beforedefs[k]==afterdefs[k]for k in beforedefs if k!='read')and beforedefs['read']!=afterdefs['read'])
    check('all_imports_globals_and_main_Source_byteexact',s.replace(new,old,1)==(OLD/NAME).read_text())
    check('exact_current_declaration_path_only_whitelist_extension',"if p==declaration:"in new and "ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-20261010'/'declaration.json'"in new and "p.name not in ('result.json','ACTUAL_REPORT.json','ACTUAL_PRIVATE_INACTIVE_AUDIT_SNAPSHOT_CONTROLS.json')"in new)
    check('initial_lstat_16MiB_before_open_or_any_decode',new.index('before=identity(p)')<new.index('before[4]<=16*2**20')<new.index('fd=os.open')<new.index('raw=stream.read'))
    check('one_nofollow_descriptor_bound_complete_size_and_EOF',"os.O_RDONLY|os.O_NOFOLLOW"in new and "raw=stream.read(16*2**20+1)"in new and "len(raw)!=before[4]or stream.read(1)!=b''"in new and 'os.fstat(stream.fileno())'in new and 'os.fdopen(fd' in new)
    check('exact7ID_open_samefd_postEOF_path_postdecode',all(x in new for x in('opened.st_dev','opened.st_ctime_ns','finished.st_dev','finished.st_ctime_ns','identity(p)!=before','during strict META decode')))
    check('strict_duplicate_and_nonfinite_reader_def_entire_byteexact',afterdefs['strict_json_bytes']==beforedefs['strict_json_bytes']and 'value=strict_json_bytes(raw)'in new)
    check('actual_summary_namespace_coupled_complete_SHA_size_7ID_required',all(x in new for x in("actual!=wanted","helper_Q_fullpin(owners[0]['files']['declaration.json'])!=wanted","summary['actual_declaration']","READ_PINS[str(p)]=actual")))
    for rel in mf['members']:
        if rel not in(NAME,'COMPLETE_SOURCE_INVERSES.json'):check('all_other_P4_members_byteexact:'+rel,(P/rel).read_bytes()==(OLD/rel).read_bytes())
    invpath=P/'COMPLETE_P4_DECLARATION_READER_SINGLE_FUNCTION_14_ROLE_BYTE_AST_INVERSES.json';write(invpath,dict(schema='COMPLETE_P4_DECLARATION_READER_SINGLE_FUNCTION_14_ROLE_BYTE_AST_INVERSES_V1',source_only=True,roles=records,actual_consumed_complete_inverse_pin=pin(P/'COMPLETE_SOURCE_INVERSES.json'),parent_actual_consumed_inverse_pin=pin(OLD/'COMPLETE_SOURCE_INVERSES.json'),original_P4_manifest_pin=originalmfpin,only_build_binder_read_function_changed=True,all_original13_other_roles_byteexact=True,all_whole_P4_V3_original_parent_inverses_verified=True,candidate_or_business_execution=False))
    py=[];allpins={}
    shutil.copy2(Path(__file__),P/'AUTHOR_P4_BUILD_DECLARATION_READER_FINITE_SOURCE.Source_META_only.py')
    for q in sorted(P.rglob('*')):
        if q.is_file():allpins[str(q.relative_to(P))]=pin(q)
        if q.suffix=='.py':ast.parse(q.read_bytes());py.append(str(q))
    check('complete_current_Source_EOF_and_Python_AST',len(allpins)>97 and len(py)>57)
    rolekeys=('canonical','prepare_binder','build_binder','prepare_host','prepare_writer','build_host','build_writer')
    report=dict(schema='AUTHOR_P4_BUILD_DECLARATION_READER_SINGLE_FUNCTION_SOURCE_REPORT_V1',status='UNREADY_SINGLE_DECLARATION_META_READER_SOURCE_ONLY_PENDING_DIFFERENT_AUTHOR_REVIEW',source_only=True,check_count=len(checks),checks=checks,all_checks_typed_true=True,blockers=[],qualified_role_Source_pins={k:pin(P/roles[k])for k in rolekeys},qualified_utility_Source_pins={k:pin(P/roles[k])for k in roles if k not in rolekeys},actual_consumed_complete_inverse_pin=pin(P/'COMPLETE_SOURCE_INVERSES.json'),complete_single_read_function_and14role_inverse_pin=pin(invpath),parent_manifest_pin=originalmfpin,actual_original_Source_binder_failure_tool_pin=pin(FAILED),retained_actual_original_Source_binder_failure_pin=pin(history/FAILED.name),actual_complete_frozen_parent_member_count=97,current_parent_members_all_retained_or_whole_inversed=True,old_P4_namespace_inverse_and_author_reports_are_lineage_only=True,actual_fixed_declaration_path='/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-20261010/declaration.json',exact_added_declaration_META_bound_bytes=16*2**20,not_an_execution_RSS_or_resource_cap_change=True,original_canonical_PREP_and_utilities_byteexact=True,existing_actual_PREP_reused_requires_actual_saved_peer_and_full_namespace_pins=True,new_PREP_or_business_namespace_required=False,all_actual_future_environment_business_or_Source_qualification_pins=None,candidate_BINDER_API_guard_resource_helper_material_numeric_or_business_executed=False,project_ART_old_Source_frozenD_or_old_results_written=False,whole_INPUT_BUILD_RSS_native_or_science_qualified=False,all_current_member_fullpins_before_own_report_append=allpins,current_complete_Python_Source_AST_count=len(py))
    reportpath=P/'AUTHOR_P4_BUILD_DECLARATION_READER_SINGLE_FUNCTION_SOURCE_REPORT.json';write(reportpath,report)
    print(json.dumps(dict(status=report['status'],source_only=True,path=str(P),check_count=len(checks),all_checks_typed_true=True,blockers=[],report_pin=pin(reportpath),actual_consumed_inverse_pin=pin(P/'COMPLETE_SOURCE_INVERSES.json'),whole14_inverse_pin=pin(invpath),BUILD_binder_Source_pin=pin(P/NAME),candidate_or_API_or_business_executed=False),allow_nan=False),flush=True)
if __name__=='__main__':main()
