"""Source/META-only N9 derivative/check/seal/postseal. Never imports candidates."""
import argparse
import ast
import difflib
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile

OLD=Path('/private/tmp/axmat_N8_four_blocker_minimal_complete_UNREADY_Source_ekd9i0c_')
ACCEPTED=Path('/private/tmp/spot_N8_actual_link_count_minimal_UNADMITTED_candidate_20261011_ruknor67/PROPOSAL_AND_STATIC_SOURCE_CHECK.json')
ACCEPTED_SHA='6e3d177531e79dabefc911c7b0e0fc7ba6621c4ee1d2a663c382bf17580ce1f2'
OLD_MF_SHA='cdaed7cd53d2b22ec3891a7f82064eea9505ae974f8ac284e6d76fe5ae7ae267'
RT='complete_observation_BUILD5_AB_runtime.UNREADY.py'
DR='N8_genuine_integrated_controls_driver.UNREADY.py'
WR='Root_observation_postclose_META_writer.UNREADY.py'
RQ='Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py'
BI='bind_complete_observation_SOURCE_only.UNREADY.py'
CB='N8_bind_monitor_controls_SOURCE_META_only.UNREADY.py'
PR='N8_TWELVE_GENUINE_CONTROL_PROTOCOL.UNREADY.json'
CHANGED=(RT,DR,WR,RQ,BI,CB,PR)
REPORT='AUTHOR_COMPLETE_N9_LINK_COUNT_SOURCE_ONLY_REPORT.json'
CHECK_TOOL='ACTUAL_AUTHOR_N9_LINK_COUNT_SOURCE_CHECK_TOOL_RETURN.json'
REVISION='CURRENT_N9_LINK_COUNT_SOURCE_REVISION_CONTRACT.UNREADY.json'
INVERSE='COMPLETE_N9_LINK_COUNT_ALL_CHANGED_ROLE_BYTE_AST_INVERSE.json'
HISTORY='PREVIOUS_SEALED_N8_V2_LINK_COUNT_BASELINE_PROVENANCE'
GENERATOR='AUTHOR_N9_LINK_COUNT_COMPLETE_Source_META_only.py'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)

def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(path):
    p=Path(path);before=p.lstat()
    assert p.is_absolute()and stat.S_ISREG(before.st_mode)and before.st_nlink==1 and all(not q.is_symlink()for q in(p,*p.parents))
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        assert ident(os.fstat(fd))==ident(before);chunks=[]
        while True:
            part=os.read(fd,1024*1024)
            if not part:break
            chunks.append(part)
        raw=b''.join(chunks);assert ident(os.fstat(fd))==ident(before)
    finally:os.close(fd)
    assert ident(p.lstat())==ident(before)and len(raw)==before.st_size
    return raw,dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ident(before))
def pin(path):return read(path)[1]
def strict(raw):
    def pairs(items):
        d={}
        for k,v in items:assert k not in d;d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in()).throw(ValueError(v)))
def data(path):return strict(read(path)[0])
def write(path,value):
    with path.open('x')as stream:json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n')
def directories(root):
    found={str(root):ident(root.lstat())}
    for p in sorted(root.rglob('*')):
        s=p.lstat();assert not stat.S_ISLNK(s.st_mode)
        if stat.S_ISDIR(s.st_mode):found[str(p)]=ident(s)
        else:assert stat.S_ISREG(s.st_mode)and s.st_nlink==1
    return found
def baseline():
    mf=data(OLD/'MANIFEST.json');assert pin(OLD/'MANIFEST.json')['sha256']==OLD_MF_SHA
    assert mf['source_only']is True and mf['files_including_manifest']==288 and mf['directory_count']==33
    assert directories(OLD)==mf['directories']
    files={str(p.relative_to(OLD))for p in OLD.rglob('*')if p.is_file()}
    assert files=={r['relative_path']for r in mf['members']}|{'MANIFEST.json'}
    for row in mf['members']:assert pin(OLD/row['relative_path'])==row['fullpin']
    return mf
def accepted():
    d=data(ACCEPTED);assert pin(ACCEPTED)['sha256']==ACCEPTED_SHA
    assert d['source_only']is True and d['patch_applied']is False and d['all_Source_AST_checks_passed']is True
    assert set(d['edits'])=={RT,DR,WR}
    for name,p in d['original_Source_fullpins'].items():
        actual=pin(OLD/name);assert {k:p[k]for k in actual}==actual
    return d
def astvalue(node):return ast.dump(node,include_attributes=False)
def hunks(old,new):
    a,b=old.splitlines(True),new.splitlines(True);result=[]
    for op,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if op!='equal':result.append(dict(old_start_line0=i,old_end_line0=j,new_start_line0=k,new_end_line0=l,old_text=''.join(a[i:j]),new_text=''.join(b[k:l])))
    assert restore(new,result)==old
    return result
def restore(text,rows):
    lines=text.splitlines(True)
    for r in reversed(rows):
        assert ''.join(lines[r['new_start_line0']:r['new_end_line0']])==r['new_text']
        lines[r['new_start_line0']:r['new_end_line0']]=r['old_text'].splitlines(True)
    return ''.join(lines)
def namespace_values():
    tree=ast.parse(read(OLD/RT)[0]);node=next(n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='REQUIRED_N8_FRESH_NAMESPACES'for t in n.targets))
    old=ast.literal_eval(node.value);new={}
    for k,v in old.items():
        value=v.replace('-v8-','-v9-link-count-').replace('_v8_','_v9_link_count_')
        if k in('host','output','control'):assert value.endswith('-20261010');value=value[:-8]+'20261011'
        assert value!=v;new[k]=value
    base=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
    controls=dict(source=str(base/'actual_complete_native_observation_BUILD5_AB_v9_link_count_monitor_controls_sources'),receipts=str(base/'actual_complete_native_observation_BUILD5_AB_v9_link_count_monitor_controls_receipts'))
    return old,new,controls
def expected_role(name,raw,proposal):
    text=raw.decode('utf-8')
    if name in proposal['edits']:
        for e in proposal['edits'][name]:assert text.count(e['old'])==e['count'];text=text.replace(e['old'],e['new'])
    oldns,newns,_=namespace_values()
    if name in(RT,WR,RQ,BI):
        for k,value in oldns.items():assert text.count(value)==1;text=text.replace(value,newns[k])
        assert text.count('new fixed v8 ')==1;text=text.replace('new fixed v8 ','new fixed v9-link-count ')
    if name==CB:
        assert text.count('_v8_')==2 and text.count('-v8-')==1
        text=text.replace('_v8_','_v9_link_count_').replace('-v8-','-v9-link-count-')
        for kind in('host','runtime','control'):
            old='-'+kind+'-20261010';assert text.count(old)==1;text=text.replace(old,'-'+kind+'-20261011')
    return text
def expected_protocol(original):
    d=strict(json.dumps(original));oldargv=d['new_instrumentation']['lsof_argv_original'];assert oldargv[3]=='pfnsiDt'
    actual=list(oldargv);actual[3]='pfnsiDtk'
    instr=d['new_instrumentation']
    instr['lsof_argv_original_is_historical_parent_only']=True
    instr['lsof_argv_original_unchanged']=False
    instr['lsof_argv_actual_required']=actual
    instr['lsof_link_count_field_explicitly_added']=True
    instr['actual_open_unlinked_regular_definition']=dict(type_field='t',required_type='REG',link_count_field='k',required_link_count=0,link_count_ASCII_decimal_and_unique_per_file_required=True,missing_REG_link_count_refused=True,zero_link_missing_type_refused=True,original_size_inode_device_and_actual_absolute_name_required=True,n_field_is_raw_namespace_attribution_only=True,deleted_filename_suffix_is_not_used_or_manufactured=True,device_inode_physical_dedup_unchanged=True,actual_new_k_output_observed=None)
    for idx in(1,4):d['cases'][idx]['source_required_behavior']+=' Current canonical field selection is pfnsiDtk. Only a real REG record with an explicit unique nonnegative ASCII decimal k equal to zero and complete actual size/inode/device/name is counted as open-unlinked; n is raw HOCDE namespace attribution, without a fabricated deleted suffix. Missing/invalid fields refuse; all selected PIDs/FDs, canonical strict0/2s/complete8MiB streams and physical device/inode dedup remain mandatory.'
    _,ns,cns=namespace_values();ids=d['case_ids'];cases={}
    art=Path('/Users/wen/spot/validation/artifacts')
    for i,caseid in enumerate(ids,1):
        prefix='axial-material-complete-native-observation-BUILD5-AB-v9-link-count-monitor-controls-case'+str(i).zfill(2)
        cases[caseid]=dict(host=str(art/(prefix+'-host-20261011')),output=str(art/(prefix+'-runtime-20261011')),control=str(art/(prefix+'-control-20261011')),**cns)
    d['current_link_count_Source_revision']=dict(status='UNREADY_SOURCE_ONLY_NOT_ROOT_ADMITTED_OR_EXECUTED',revision='v9-link-count',parent_field_selection='pfnsiDt',parent_argv_explicitly_historical=True,current_field_selection='pfnsiDtk',future_native_namespaces=ns,future_controls_Source_namespaces=cns,future_case_namespaces=cases,actual_monitor_controls_qualification=None,actual_native_AB_execution=None,scientific_qualification_created=False)
    return d
def create():
    mf=baseline();proposal=accepted()
    P=Path(tempfile.mkdtemp(prefix='axmat_N9_link_count_complete_UNREADY_Source_',dir='/private/tmp'))
    for q in sorted(OLD.rglob('*')):
        target=P/q.relative_to(OLD)
        if q.is_dir():target.mkdir()
        elif q.name!='MANIFEST.json'or q.parent!=OLD:
            raw,_=read(q)
            with target.open('xb')as f:f.write(raw)
    history=P/HISTORY;history.mkdir();(history/'ORIGINAL_COMPLETE_CHANGED_ROLE_SOURCE').mkdir()
    with (history/'ORIGINAL_N8_V2_MANIFEST.json').open('xb')as f:f.write(read(OLD/'MANIFEST.json')[0])
    sibling=Path(str(OLD)+'_seal_receipt');oldreceipts={}
    for name in('ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json','FULL_SOURCE_POSTSEAL_VERIFICATION.json'):
        raw,oldreceipts[name]=read(sibling/name)
        with (history/('ORIGINAL_N8_V2_'+name)).open('xb')as f:f.write(raw)
    for name in CHANGED:
        raw,_=read(OLD/name)
        with (history/'ORIGINAL_COMPLETE_CHANGED_ROLE_SOURCE'/name).open('xb')as f:f.write(raw)
        target=P/name
        value=json.dumps(expected_protocol(strict(raw)),indent=2,allow_nan=False)+'\n'if name==PR else expected_role(name,raw,proposal)
        assert value.encode()!=raw
        with target.open('w')as f:f.write(value)
        if name.endswith('.py'):ast.parse(value)
        else:strict(value)
    roles=data(P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json')['required_author_Source_roles'];assert len(roles)==21
    inverse=[]
    for name in CHANGED:
        old=read(OLD/name)[0].decode();new=read(P/name)[0].decode();hs=hunks(old,new)
        if name.endswith('.py'):assert astvalue(ast.parse(restore(new,hs)))==astvalue(ast.parse(old))
        else:assert strict(restore(new,hs))==strict(old)
        inverse.append(dict(role_basename=name,parent_original_fullpin=pin(OLD/name),retained_original_fullpin=pin(history/'ORIGINAL_COMPLETE_CHANGED_ROLE_SOURCE'/name),new_complete_Source_pin=pin(P/name),hunks=hs,whole_byte_inverse=True,whole_AST_inverse=True if name.endswith('.py')else None,whole_JSON_inverse=True if name==PR else None))
    write(P/INVERSE,dict(schema='COMPLETE_N9_LINK_COUNT_MINIMAL_ROLE_BYTE_AST_INVERSE_V1',source_only=True,parent_manifest_pin=pin(OLD/'MANIFEST.json'),roles=inverse,actual_candidate_or_API_execution=False))
    retention=[]
    for row in mf['members']:
        name=row['relative_path'];new=pin(P/name);old=row['fullpin']
        retention.append(dict(relative_path=name,parent_original_fullpin=old,current_copy_fullpin=new,changed_in_this_revision=name in CHANGED,entire_bytes_unchanged=(new['sha256'],new['size_bytes'])==(old['sha256'],old['size_bytes'])))
    write(P/'COMPLETE_N9_ALL_N8_V2_PARENT_MEMBER_RETENTION.Source_META.json',dict(schema='COMPLETE_N9_LINK_COUNT_ALL_PARENT_MEMBER_RETENTION_V1',source_only=True,parent_manifest_pin=pin(OLD/'MANIFEST.json'),parent_manifest_retained_fullpin=pin(history/'ORIGINAL_N8_V2_MANIFEST.json'),original_member_count=len(retention),members=retention,changed_role_basenames=list(CHANGED),all_original_parent_members_preserved_or_whole_inversed=True,original_parent_seal_receipt_pins=oldreceipts))
    with (P/GENERATOR).open('xb')as f:f.write(read(Path(__file__))[0])
    with (P/'ACCEPTED_MINIMAL_LINK_COUNT_CANDIDATE.Source_META.json').open('xb')as f:f.write(read(ACCEPTED)[0])
    oldns,newns,cns=namespace_values()
    write(P/REVISION,dict(schema='CURRENT_N9_LINK_COUNT_MINIMAL_SOURCE_REVISION_CONTRACT_V1',status='UNREADY_SOURCE_ONLY_NOT_ADMITTED_BOUND_CONTROLLED_EXECUTED_OR_QUALIFIED',source_only=True,parent_manifest_pin=pin(OLD/'MANIFEST.json'),parent_manifest_retained_fullpin=pin(history/'ORIGINAL_N8_V2_MANIFEST.json'),accepted_minimal_candidate_fullpin=pin(ACCEPTED),changed_complete_Source_roles=list(CHANGED),only_accepted_three_logic_Source_roles=[RT,DR,WR],namespace_only_additional_roles=[RQ,BI,CB],required_complete_author_Source_roles=roles,required_complete_author_Source_role_count=21,current_role_Source_pins_before_manifest={k:pin(P/v)for k,v in roles.items()if v!='MANIFEST.json'},current_inverse=INVERSE,current_retention='COMPLETE_N9_ALL_N8_V2_PARENT_MEMBER_RETENTION.Source_META.json',historical_original_N8_V2_author_reports_tool_terminals_inverses_and_absolute_pins_are_parent_history=True,historical_original_author_scripts_must_not_be_executed=True,historical_argv_is_not_current_argv=True,all_old_N8_V2_four_blocker_fixes_retained=True,original_guard_classes_MRO_caps_physics_owner_helper_unchanged=True,original_native_Source_archive_member_count=1365,old_native_namespaces_historical=oldns,future_native_namespaces=newns,future_controls_Source_namespaces=cns,future_case_namespaces=data(P/PR)['current_link_count_Source_revision']['future_case_namespaces'],actual_new_k_output_observed=None,actual_independent_Source_review=None,actual_Root_Source_admission=None,actual_controls_Source_binding=None,actual_monitor_controls_qualification=None,actual_native_AB_execution=None,scientific_qualification_created=False))
    assert baseline()==mf
    print(json.dumps(dict(status='FRESH_N9_LINK_COUNT_COMPLETE_SOURCE_CREATED_UNREADY',source_only=True,path=str(P),changed_role_basenames=list(CHANGED),parent_manifest_pin=pin(OLD/'MANIFEST.json'),current_revision_contract_pin=pin(P/REVISION),actual_candidate_or_API_execution=False),allow_nan=False),flush=True)

def check(P):
    mf=baseline();proposal=accepted();revision=data(P/REVISION);checks=[];records=[];py=[]
    def ck(name,value):assert type(value)is bool and name not in{c['check']for c in checks};checks.append(dict(check=name,passed=value))
    ck('exact_seven_source_protocol_changed_roles_only',revision['changed_complete_Source_roles']==list(CHANGED))
    ck('original_N8_V2_parent_manifest_fullpin',pin(OLD/'MANIFEST.json')==revision['parent_manifest_pin'])
    ck('complete_retained_parent_manifest_byteexact',read(P/HISTORY/'ORIGINAL_N8_V2_MANIFEST.json')[0]==read(OLD/'MANIFEST.json')[0])
    for row in mf['members']:
        name=row['relative_path'];a=pin(OLD/name);b=pin(P/name)
        ck('complete_parent_current_fullEOF_7ID:'+name,a==row['fullpin'])
        if name not in CHANGED:ck('whole_parent_member_byteexact:'+name,(a['sha256'],a['size_bytes'])==(b['sha256'],b['size_bytes']))
    inverse=data(P/INVERSE);ck('complete_changed_role_inverse_set',{r['role_basename']for r in inverse['roles']}==set(CHANGED))
    for row in inverse['roles']:
        name=row['role_basename'];old=read(OLD/name)[0].decode();new=read(P/name)[0].decode();restored=restore(new,row['hunks'])
        ck('whole_current_to_NV2_bytes:'+name,restored==old)
        ck('current_original_retained_fullpins:'+name,pin(OLD/name)==row['parent_original_fullpin']and pin(P/name)==row['new_complete_Source_pin']and pin(row['retained_original_fullpin']['path'])==row['retained_original_fullpin']and read(row['retained_original_fullpin']['path'])[0]==old.encode())
        if name.endswith('.py'):
            ck('whole_current_to_NV2_AST:'+name,astvalue(ast.parse(restored))==astvalue(ast.parse(old)))
            ck('only_exact_accepted_patch_and_namespace_substitution:'+name,new==expected_role(name,old.encode(),proposal))
        else:ck('only_exact_link_count_protocol_and_fresh_namespace_metadata',strict(new)==expected_protocol(strict(old)))
    roles=data(P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json')['required_author_Source_roles']
    ck('original_complete_21_role_contract_unchanged',len(roles)==21 and roles==mf['required_author_Source_roles'])
    rolepins={k:pin(P/v)for k,v in roles.items()if v!='MANIFEST.json'}
    ck('all_20_nonmanifest_current_fullpins_match_revision',rolepins==revision['current_role_Source_pins_before_manifest'])
    rt=read(P/RT)[0].decode();driver=read(P/DR)[0].decode();writer=read(P/WR)[0].decode()
    ck('all_three_operational_lsof_fixed_argv_synchronized',rt.count("'pfnsiDtk'")==2 and driver.count("'pfnsiDtk'")==1 and "'pfnsiDt'"not in rt and "'pfnsiDt'"not in driver)
    ck('explicit_REG_k0_strict_numeric_unique_missing_refusals',all(x in rt for x in("single actual link-count field per file record required","row['k'].isascii()and row['k'].isdigit()","zero-link actual file type required","complete actual regular-file link count required","if row.get('t')!='REG':continue","if int(row['k'])!=0:continue","complete actual open-unlinked name for namespace attribution required")))
    ck('no_fabricated_deleted_suffix_in_current_runtime','(deleted)'not in rt)
    for text in ["require(observed.returncode==0,'full live own process file scan required')","require(len(observed.stdout)<8*2**20 and len(observed.stderr)<8*2**20,'finite complete lsof streams; never truncated')","require(set(returned_pids)==selected and len(returned_pids)==len(set(returned_pids)),'single strict lsof0 complete selected PID coverage; no absent-PID acceptance')","selected.discard(ps_diagnostic_pid)","selected=owner_observer.expand_selection(ps_rows,selected,ps_diagnostic_pid,ps_started_monotonic)","key=(row['D'],row['i']);","if key not in unlinked:total+=int(row['s']);unlinked_bytes+=int(row['s']);unlinked.add(key)"]:
        ck('original_strong_gate_byte_content:'+text,rt.count(text)==read(OLD/RT)[0].decode().count(text)>0)
    call=next(n for n in ast.walk(ast.parse(rt))if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='observed'for t in n.targets)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Attribute)and n.value.func.attr=='run')
    argv=call.value.args[0];literal=[n.value for n in argv.elts if isinstance(n,ast.Constant)]
    ck('single_lsof_scope_no_L1_X_or_FD_selection_filter',literal==['-nP','-F','pfnsiDtk','-a','-p']and next(k.value.value for k in call.value.keywords if k.arg=='timeout')==2)
    ck('honest_argv_changed_declaration_and_postclose_consumer',"original_lsof_argv_and_single_strict_zero_timeout_unchanged=False"in rt and "diagnostic['original_lsof_argv_and_single_strict_zero_timeout_unchanged']is False"in writer and all(k in rt and k in writer for k in('lsof_link_count_field_explicitly_added','lsof_selected_PID_and_FD_scope_strict_zero_timeout_and_full_stream_limits_unchanged')))
    oldns,newns,cns=namespace_values()
    for name in(RT,WR,RQ,BI):
        tree=ast.parse(read(P/name)[0]);nsnode=next(n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='REQUIRED_N8_FRESH_NAMESPACES'for t in n.targets))
        ck('exact_shared_fresh_future_native_namespace:'+name,ast.literal_eval(nsnode.value)==newns)
    for name in(RT,DR,WR,RQ,BI,CB,'N8_Root_controls_postclose_META.UNREADY.py','N8_actual_controls_qualification_gate.Source_META_only.py'):
        a=ast.parse(read(OLD/name)[0]);b=ast.parse(read(P/name)[0]);oldcap=next(n for n in a.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='CAPS'for t in n.targets));newcap=next(n for n in b.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='CAPS'for t in n.targets))
        ck('original_nine_cap_exact_AST:'+name,astvalue(oldcap)==astvalue(newcap))
    for name in('N8_exact_owner_scope_observer.UNREADY.py','N8_private_control_child.UNREADY.py','N8_actual_controls_qualification_gate.Source_META_only.py','N8_Root_controls_postclose_META.UNREADY.py','complete_observation_genuine_host.UNREADY.py','COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz'):
        ck('whole_owner_guard_MRO_fixture_gates_or_native_unchanged:'+name,read(P/name)[0]==read(OLD/name)[0])
    for func in('guarded','build_exact_owner_resources','attach_exact_owner_observer'):
        a=next(n for n in ast.parse(read(OLD/RT)[0]).body if isinstance(n,ast.FunctionDef)and n.name==func);b=next(n for n in ast.parse(rt).body if isinstance(n,ast.FunctionDef)and n.name==func)
        ck('original_runtime_full_def_AST:'+func,astvalue(a)==astvalue(b))
    q=data(P/PR);oldq=data(OLD/PR)
    ck('protocol_schemas_consumers_12_cases_and_None_execution_preserved',q['schema']==oldq['schema']and q['case_ids']==oldq['case_ids']and len(q['cases'])==12 and q['root_interfaces']==oldq['root_interfaces']and all(c['actual_execution']is None and c['actual_root_closed_terminal']is None and c['actual_independent_saved_review']is None for c in q['cases']))
    ck('protocol_old_argv_historical_current_actual_k_required',q['new_instrumentation']['lsof_argv_original']==oldq['new_instrumentation']['lsof_argv_original']and q['new_instrumentation']['lsof_argv_original_is_historical_parent_only']is True and q['new_instrumentation']['lsof_argv_original_unchanged']is False and q['new_instrumentation']['lsof_argv_actual_required'][3]=='pfnsiDtk')
    targets=[*newns.values(),*cns.values()]+[ns[k]for ns in q['current_link_count_Source_revision']['future_case_namespaces'].values()for k in('host','output','control')]
    ck('all_future_native_and_12_control_namespaces_declared_fresh_absent',len(set(targets))==43 and all(not os.path.lexists(v)for v in targets))
    ck('future_actual_k_controls_root_native_science_unknown',revision['actual_new_k_output_observed']is None and all(revision[k]is None for k in('actual_independent_Source_review','actual_Root_Source_admission','actual_controls_Source_binding','actual_monitor_controls_qualification','actual_native_AB_execution'))and revision['scientific_qualification_created']is False)
    for p in sorted(P.rglob('*')):
        if p.is_file():
            records.append(pin(p))
            if p.suffix=='.py':ast.parse(read(p)[0]);py.append(str(p))
    ck('all_current_whole_Source_fullEOF_and_all_Python_AST',len(records)>288 and len(py)>96)
    ck('original_baseline_full_directory_freeze_still_matches',directories(OLD)==mf['directories'])
    blockers=[c['check']for c in checks if c['passed']is not True]
    result=dict(schema='AUTHOR_COMPLETE_N8_V2_FOUR_BLOCKER_MINIMAL_SOURCE_REPORT_V1',current_revision='N9_LINK_COUNT',status='AUTHOR_SOURCE_ONLY_PASS_UNREADY_REQUIRES_DIFFERENT_AUTHOR_REVIEW'if not blockers else'AUTHOR_SOURCE_ONLY_FAIL_BLOCKED',source_only=True,parent_manifest_pin=pin(OLD/'MANIFEST.json'),required_complete_author_Source_roles=roles,current_complete_role_Source_pins_before_manifest=rolepins,check_count=len(checks),checks=checks,check_evidence={},all_checks_passed=not blockers,all_checks_typed_boolean=True,blockers=blockers,all_current_Source_and_small_META_fullpin_records_before_own_report_append=records,complete_Python_Source_AST_count_before_own_report_append=len(py),complete_original_native_Source_member_count=1365,complete_native_Source_archive_byteexact_transitive_parent_fullEOF=True,changed_complete_role_basenames=list(CHANGED),original_caps=CAPS,actual_candidate_or_controls_or_guard_or_API_or_PS_lsof_wait_poll_compile_material_numeric_execution=False,actual_monitor_controls_qualification=None,actual_root_Source_admission=None,actual_bound_control_Source=None,actual_native_AB_execution=None,actual_new_k_output_observed=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,limits=['Source/AST/full EOF only; no candidate/binder/control/guard/OS/resource/API/native/business execution.','Existing old parent author checks, reports, actual source terminals and inverse chains are byteexact historical lineage; this report and N9 inverse/MF are current.','New actual k output, complete actual controls, Root Q/native and scientific qualification remain unknown.'])
    write(P/REPORT,result)
    print(json.dumps(dict(status=result['status'],source_only=True,check_count=len(checks),passed_checks=sum(c['passed']is True for c in checks),blockers=blockers,actual_report_pin=pin(P/REPORT),complete_Python_Source_AST_count=len(py),actual_candidate_or_API_execution=False),allow_nan=False),flush=True)
    return 0 if not blockers else 1

def terminal(path):
    w=data(path);t=w['terminal_tool_return'];assert w['closed']is True and w['observed_terminal']is True and w['session_repolled_after_close']is False and w['actual_terminal_chunk']==t['chunk_id']and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t
    assert w['candidate_or_API_or_controls_or_business_executed']is False
    return w,strict(t['output'])
def seal(P):
    r=data(P/REPORT);assert r['all_checks_passed']is True and r['blockers']==[] and r['check_count']==len(r['checks'])and all(type(c['passed'])is bool and c['passed']is True for c in r['checks'])
    _,out=terminal(P/CHECK_TOOL);assert out['actual_report_pin']==pin(P/REPORT)and out['blockers']==[]
    members=[];py=0
    for p in sorted(P.rglob('*')):
        if p.is_file():
            if p.suffix=='.py':ast.parse(read(p)[0]);py+=1
            members.append(dict(relative_path=str(p.relative_to(P)),fullpin=pin(p)))
    assert not(P/'MANIFEST.json').exists();(P/'MANIFEST.json').write_text('{}\n');dirs=directories(P)
    roles=data(P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json')['required_author_Source_roles']
    value=dict(schema='COMPLETE_NATIVE_OBSERVATION_BUILD5_AB_UNREADY_SOURCE_MANIFEST_V1',revision_schema='COMPLETE_N8_V2_FOUR_BLOCKER_MINIMAL_SOURCE_MANIFEST_V1',current_revision='N9_LINK_COUNT',current_revision_schema='COMPLETE_N9_LINK_COUNT_MINIMAL_SOURCE_MANIFEST_V1',status='UNREADY_SOURCE_ONLY_REQUIRES_INDEPENDENT_REVIEW',source_only=True,members=members,directories=dirs,member_count=len(members),files_including_manifest=len(members)+1,directory_count=len(dirs),complete_Python_Source_AST_count=py,required_author_Source_roles=roles,parent_manifest_pin=pin(OLD/'MANIFEST.json'),current_revision_contract_pin=pin(P/REVISION),current_full_inverse_pin=pin(P/INVERSE),original_N8_parent_member_count=239,original_N8_V2_parent_member_count=287,original_N7_source_member_count=181,original_native_Source_member_count=1365,actual_author_report_pin=pin(P/REPORT),actual_author_Source_check_tool_return_pin=pin(P/CHECK_TOOL),actual_candidate_or_controls_or_guard_or_API_or_PS_lsof_wait_poll_compile_material_numeric_execution=False,actual_new_k_output_observed=None,actual_independent_Source_review=None,actual_Root_Source_admission=None,actual_monitor_controls_qualification=None,actual_native_AB_execution=None,scientific_qualification_created=False,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    with (P/'MANIFEST.json').open('w')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
    assert directories(P)==dirs and all(pin(P/r['relative_path'])==r['fullpin']for r in members)
    author={k:pin(P/v)for k,v in roles.items()};assert len(author)==21
    print(json.dumps(dict(status='SEALED_AUTHOR_UNREADY_SOURCE_ONLY_NOT_ROOT_ADMITTED_OR_EXECUTED',source_only=True,manifest_pin=pin(P/'MANIFEST.json'),review_pin=pin(P/REPORT),members=len(members),files=len(members)+1,directories=len(dirs),Source_AST_count=py,actual_author_Source_contract=author,blockers=[],actual_candidate_execution=False,scientific_qualification_created=False),allow_nan=False),flush=True)
def postseal(P):
    S=Path(str(P)+'_seal_receipt');truth,out=terminal(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json');mfpin=pin(P/'MANIFEST.json');assert out['manifest_pin']==mfpin
    mf=data(P/'MANIFEST.json');checks=[]
    def ck(name,value):assert type(value)is bool and name not in{r['check']for r in checks};checks.append(dict(check=name,passed=value))
    files={str(p.relative_to(P))for p in P.rglob('*')if p.is_file()}
    ck('complete_full_Source_member_set',files=={r['relative_path']for r in mf['members']}|{'MANIFEST.json'})
    ck('complete_actual_directory_freeze',directories(P)==mf['directories']);py=0
    for row in mf['members']:
        p=P/row['relative_path'];ck('fullEOF_SHA_size_7ID:'+row['relative_path'],pin(p)==row['fullpin'])
        if p.suffix=='.py':ast.parse(read(p)[0]);py+=1
    ck('source_only_no_actual_k_controls_native_science',mf['actual_new_k_output_observed']is None and mf['actual_monitor_controls_qualification']is None and mf['actual_native_AB_execution']is None and mf['scientific_qualification_created']is False and mf['actual_candidate_or_controls_or_guard_or_API_or_PS_lsof_wait_poll_compile_material_numeric_execution']is False)
    ck('actual_current_author_report_coupling',out['review_pin']==pin(P/REPORT))
    ck('exact_complete_counts',len(files)==mf['files_including_manifest']and len(mf['directories'])==mf['directory_count']and py==mf['complete_Python_Source_AST_count'])
    ck('all21_full_role_pins_match_true_seal',out['actual_author_Source_contract']=={k:pin(P/v)for k,v in mf['required_author_Source_roles'].items()})
    ck('original_parent_full_directory_freeze_unchanged',directories(OLD)==data(OLD/'MANIFEST.json')['directories'])
    blockers=[c['check']for c in checks if c['passed']is not True];assert blockers==[];reviewtruth,_=terminal(P/CHECK_TOOL)
    result=dict(schema='AUTHOR_COMPLETE_N8_V2_SOURCE_FULL_POSTSEAL_V1',current_revision='N9_LINK_COUNT',status='FULL_SOURCE_POSTSEAL_VERIFIED_SOURCE_ONLY_NOT_ROOT_ADMITTED',source_only=True,manifest_pin=mfpin,review_pin=out['review_pin'],files=len(files),directories=len(mf['directories']),complete_Python_Source_AST_count=py,check_count=len(checks),checks=checks,all_checks_passed=True,blockers=[],actual_review_terminal_chunk=reviewtruth['actual_terminal_chunk'],actual_seal_terminal_chunk=truth['actual_terminal_chunk'],actual_candidate_guard_API_compile_native_or_numeric_executed=False,actual_new_k_output_observed=None,scientific_qualification_created=False)
    path=S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json';write(path,result)
    print(json.dumps(dict(status=result['status'],source_only=True,manifest_pin=mfpin,postseal_verification_pin=pin(path),files=len(files),directories=len(mf['directories']),blockers=[],actual_candidate_execution=False),allow_nan=False),flush=True)

if __name__=='__main__':
    cli=argparse.ArgumentParser();cli.add_argument('--mode',choices=('create','check','seal','postseal'),required=True);cli.add_argument('--package');a=cli.parse_args()
    if a.mode=='create':assert a.package is None;create()
    else:
        P=Path(a.package);assert P.is_absolute()and P.resolve()==P and P.name.startswith('axmat_N9_link_count_complete_UNREADY_Source_')
        result={'check':check,'seal':seal,'postseal':postseal}[a.mode](P)
        if result is not None:raise SystemExit(result)
