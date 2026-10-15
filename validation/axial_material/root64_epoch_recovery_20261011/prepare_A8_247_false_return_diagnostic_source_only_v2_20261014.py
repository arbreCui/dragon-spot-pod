"""Failure-only A8 Source preparation; no compiler, solver, deletion or science EOF."""
import hashlib,json,os,re,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
ORIGINAL=Path('/Users/wen/spot/validation/artifacts/axial-material-r64-system-normalization-20261003/build/SPOR64_A8.f90')
OUT=R/'boot_v16_A8_247_false_return_diagnostic_source_v1_20261014'
SCOPES={'MAP_INTEGER1':2,'MAP_REAL321':2,'MAP_INTEGER2':2,'MAP_INTEGER3':2,'DOORFV64':15,'MCCGF64':96,'MCGFCS64':19,'MCGFL164':62,'MCGFLX64':11,'MCGMRE64':36}
MAP_SCOPES={'MAP_INTEGER1','MAP_REAL321','MAP_INTEGER2','MAP_INTEGER3'}
SUCCESS={('MCGFL164',789),('MCGMRE64',1112)}
EVENT_SCHEMA='ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1'


def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def norm(p):return{k:p[k]for k in('path','sha256','size_bytes','identity')}

def pin(p):
    p=Path(p);s=p.lstat()
    if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('Source and metadata only')
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened Source7')
        d=f.read()
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('Source FD7')
    if identity(p.lstat())!=identity(s):raise RuntimeError('after Source7')
    return dict(path=str(p),sha256=hashlib.sha256(d).hexdigest(),size_bytes=len(d),identity=identity(s))

def read(p):
    if isinstance(p,dict):
        if pin(p['path'])!=norm(p):raise RuntimeError('exact current metadata PF')
        p=p['path']
    else:pin(p)
    return json.loads(Path(p).read_bytes())

def write(p,value):
    d=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()if isinstance(value,dict)else value.encode()
    with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(d);f.flush();os.fsync(f.fileno())

def main():
    if OUT.exists():raise RuntimeError('unique diagnostic Source only')
    originalpin=pin(ORIGINAL);original=ORIGINAL.read_text()
    if originalpin['sha256']!='4b80957573c9dfa3986a659dc5b150c65d7288bbadb7a215be24b30e63e5c739'or originalpin['size_bytes']!=51807:raise RuntimeError('only actual compiled normalization A8 complete original Source')
    lines=original.splitlines(keepends=True);scope=None;ranges={};returnrows=[];falseassign={};trueassign={};matchassign={};scope_start=None
    for i,line in enumerate(lines,1):
        m=re.match(r'\s*(?:pure\s+)?subroutine\s+(\w+)\(',line,re.I)
        if m:scope=m[1].upper();scope_start=i;ranges[scope]=[i,None];trueassign[scope]=[];falseassign[scope]=[];matchassign[scope]=[]
        if scope in SCOPES:
            if re.fullmatch(r'\s*ok\s*=\s*\.false\.\s*',line,re.I):falseassign[scope].append(i)
            if re.fullmatch(r'\s*ok\s*=\s*\.true\.\s*',line,re.I):trueassign[scope].append(i)
            if re.match(r'\s*ok\s*=\s*RECORD_MATCHES\(',line,re.I):matchassign[scope].append(i)
            if not line.lstrip().startswith('!')and re.search(r'\breturn\s*$',line,re.I):
                start=i
                while start>scope_start and lines[start-2].rstrip().endswith('&'):start-=1
                returnrows.append(dict(scope=scope,original_statement_start_source_line=start,original_return_source_line=i,original_statement_complete=''.join(lines[start-1:i])))
        if re.match(r'\s*end\s+subroutine\b',line,re.I):
            if scope is not None:ranges[scope][1]=i
            scope=None
    expectedfalse={'MAP_INTEGER1':[209],'MAP_REAL321':[229],'MAP_INTEGER2':[249],'MAP_INTEGER3':[270],'DOORFV64':[303],'MCCGF64':[419],'MCGFCS64':[676],'MCGFL164':[765],'MCGFLX64':[990],'MCGMRE64':[1075]}
    expectedtrue={'MAP_INTEGER1':[],'MAP_REAL321':[],'MAP_INTEGER2':[],'MAP_INTEGER3':[],'DOORFV64':[374],'MCCGF64':[657],'MCGFCS64':[712],'MCGFL164':[788,948],'MCGFLX64':[1026],'MCGMRE64':[1111,1315]}
    expectedmatch={'MAP_INTEGER1':[205],'MAP_REAL321':[225],'MAP_INTEGER2':[245],'MAP_INTEGER3':[266]}
    if {k:falseassign[k]for k in SCOPES}!=expectedfalse or {k:trueassign[k]for k in SCOPES}!=expectedtrue or {k:matchassign[k]for k in MAP_SCOPES}!=expectedmatch or len(returnrows)!=249:raise RuntimeError('actual original boolean assignment and return census')
    success=[r for r in returnrows if(r['scope'],r['original_return_source_line'])in SUCCESS];failed=[r for r in returnrows if(r['scope'],r['original_return_source_line'])not in SUCCESS]
    if len(success)!=2 or len(failed)!=247 or {k:sum(r['scope']==k for r in failed)for k in SCOPES}!=SCOPES:raise RuntimeError('only247 actual okFalse returns; two normal True returns excluded')
    for r in success:
        i=r['original_return_source_line']
        if lines[i-2].strip().lower()!='ok = .true.'or r['original_statement_complete'].strip().lower()!='return':raise RuntimeError('original successful return immediately follows okTrue')
    mapping=[];changes=[]
    for r in failed:
        scope=r['scope'];i=r['original_return_source_line'];before=r['original_statement_complete'];indent=re.match(r'\s*',before.splitlines()[0]).group();pid='A8_'+scope+'_RETURN_L'+str(i).zfill(4)
        inline=before.strip().lower()!='return'
        if inline:
            if not re.match(r'\s*if\s*\(',before,re.I)or before.lower().count('return')!=1:raise RuntimeError('one original inline IF failure return')
            offset=before.lower().rfind('return');condition=before[:offset]
            condition_tail=condition.rstrip()
            if condition_tail.endswith('&'):condition_tail=condition_tail[:-1].rstrip()
            if not condition_tail.endswith(')'):raise RuntimeError('complete original single-evaluation IF expression with original free-form continuation')
            prefix=condition+'then\n';bodyindent=indent+'  '
        else:prefix='';bodyindent=indent;condition=None
        output=(bodyindent+"write(6,'(A,I0,A)') &\n"+
            bodyindent+'  '+"'{\"schema\":\""+EVENT_SCHEMA+"\",'// &\n"+
            bodyindent+'  '+"'\"scope\":\""+scope+"\",'// &\n"+
            bodyindent+'  '+"'\"predicate_id\":\""+pid+"\",'// &\n"+
            bodyindent+'  '+"'\"original_return_source_line\":"+str(i)+",'// &\n"+
            bodyindent+'  '+"'\"actual_boolean_status_integer\":',merge(1,0,ok),'}'\n"+
            bodyindent+'flush(6)\n')
        after=prefix+output+(bodyindent+'return\n'+indent+'end if\n'if inline else before)
        changes.append(dict(**r,predicate_id=pid,before=before,after=after))
        if scope in MAP_SCOPES:
            if inline:
                if before.strip().lower()!='if (.not. ok) return'or i!=expectedmatch[scope][0]+1:raise RuntimeError('MAP original RECORD_MATCHES false result return')
                dominance='Original RECORD_MATCHES result is assigned to ok once, and this original .not.ok branch proves false; no extra condition or record read.'
            else:
                if i!=expectedfalse[scope][0]+1 or lines[i-2].strip().lower()!='ok = .false.':raise RuntimeError('MAP pointer-null original explicit false assignment immediately before return')
                dominance='Original pointer-null branch explicitly assigns okFalse immediately before this original return.'
        else:dominance='Original unconditional okFalse initialization; successful True sibling branches terminate at excluded success returns, or True assignment is after every remaining failed return.'
        mapping.append(dict(**r,predicate_id=pid,boolean_result_expression='ok',original_okFalse_assignment_source_lines=expectedfalse[scope],original_RECORD_MATCHES_result_assignment_source_lines=expectedmatch.get(scope,[]),original_success_assignment_sites=expectedtrue[scope],original_okFalse_dominance=dominance,original_condition_prefix_complete=condition,original_condition_evaluated_once=True,actual_boolean_status_integer_expression='merge(1,0,ok)',required_false_integer=0,only_stdout_write_and_flush_added_before_original_return=True))
    current=original
    for c in sorted(changes,key=lambda x:x['original_return_source_line'],reverse=True):
        start=c['original_statement_start_source_line']-1;end=c['original_return_source_line'];startchar=sum(len(x)for x in lines[:start]);endchar=sum(len(x)for x in lines[:end])
        if current[startchar:endchar]!=c['before']:raise RuntimeError('exact original positional return splice')
        current=current[:startchar]+c['after']+current[endchar:]
    back=current
    for c in changes:
        if back.count(c['after'])!=1:raise RuntimeError('unique original ID complete inverse block')
        back=back.replace(c['after'],c['before'],1)
    if back.encode()!=ORIGINAL.read_bytes():raise RuntimeError('complete original active A8 Source byte inverse')
    excluded={}
    for name in('SPOR64_A8_MUTABLE_PROBE','SPOR64_A8_CAPTURE_PROBE','SPOR64_A8_RANK_PROBE','SPOR64_A8_OPERATOR_PROBE'):
        a,z=ranges[name];block=''.join(lines[a-1:z])
        if block not in current:raise RuntimeError('probe wrapper complete bytes retained')
        excluded[name]=dict(original_source_line_start=a,original_source_line_end=z,whole_bytes_sha256=hashlib.sha256(block.encode()).hexdigest(),whole_bytes_unchanged_and_no_event=True)
    for r in success:
        i=r['original_return_source_line'];block=''.join(lines[i-2:i])
        if block not in current:raise RuntimeError('successful True return whole bytes retained')
    normalization=''.join(lines[485:488])
    if normalization not in current or 'epsi64 = min(epsi64, 2.5e-10_real64)'not in normalization:raise RuntimeError('active normalization486-488 strict work target and stdout exactly retained')
    declarations=original[:original.index('contains\n')+len('contains\n')]
    if not current.startswith(declarations):raise RuntimeError('all module declarations public ABI and interfaces complete bytes retained')
    if any(len(l)>132 for l in current.splitlines()):raise RuntimeError('free form source original and added lines <=132')
    summarypath=Path('/Users/wen/spot/validation/artifacts/axial-material-new-one-BOOT-A9-false-return-diagnostic-20261014-v1/Root_actual_one_BOOT_status_diagnostic_summary.json');basepin=pin(summarypath);base=read(basepin);table={p['path']:norm(p)for p in base['fixed_current_pins']+base['output_pins']};old70=[table[p]for p in base['actual_ordered70_link_inputs']];old1=old70[1]
    modulepin=table[str(Path(old1['path']).with_name('spor64_a8.mod'))]
    if old1['sha256']!='fe8f3d61ef1abc12f0eae22da3ef8e79685c5166bdfec73bcebbed48d796081e'or pin(old1['path'])!=old1 or pin(modulepin['path'])!=modulepin or modulepin['sha256']!='2d1878cbfbf324af67c2be7980946b26244f9b7d59594abbbb4bad167ccc2203'or modulepin['size_bytes']!=6092 or table.get(str(ORIGINAL))!=originalpin:raise RuntimeError('actual selected object1/compiled Source and original6092 module exact PF')
    rootpath=R/'ROOT_ACTUAL_ONE_A9_111_FALSE_RETURN_DIAGNOSTIC_V1_TRUE_TOOL_RETURNS_20261014.json';rootpin=pin(rootpath);root=read(rootpin);terminal=root['actual_terminal_return'];outcome=base['actual_outcome'];event=outcome['actual_A9_first_false_return']
    if root['observed_closed']is not True or type(root['original_integer_exit_code'])is not int or root['original_integer_exit_code']!=1 or type(terminal['exit_code'])is not int or terminal['exit_code']!=1 or terminal.get('session_id')is not None or event!=dict(schema='ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1',scope='FLU2DR64_CORE',predicate_id='A9_FLU2DR64_CORE_RETURN_L0233',original_return_source_line=233,actual_boolean_status_integer=0)or outcome['actual_A9_failed_return_chain']!=[event]or outcome['actual_diagnostic']['boot_plane']!=1 or outcome['actual_diagnostic']['actual_return_status']!=2:raise RuntimeError('real closed A9 CORE233 childFalse without guessed A8 inner predicate')
    originalbuildpath=Path('/Users/wen/spot/validation/artifacts/axial-material-new-REAL64-native-route-build-only-20261011/Root_actual_build_only_summary.json');originalbuildpin=pin(originalbuildpath);originalbuild=read(originalbuildpin)
    compilematches=[r for r in originalbuild['records']if isinstance(r.get('command'),list)and '-c'in r['command']and str(ORIGINAL)in r['command']and old1['path']in r['command']]
    if len(compilematches)!=1 or compilematches[0]['status']!='PASS':raise RuntimeError('actual original object1 compiler source binding')
    internal_edges=[dict(caller='DOORFV64',callee='MCCGF64',caller_failed_guard_source_line=359),dict(caller='MCCGF64',callee='MCGFLX64',caller_failed_guard_source_line=645),dict(caller='MCGFLX64',callee='MCGMRE64',caller_failed_guard_source_line=1024),*[dict(caller='MCGMRE64',callee='MCGFL164',caller_failed_guard_source_line=i)for i in(1132,1186,1212)],dict(caller='MCGFL164',callee='MCGFCS64',caller_failed_guard_source_line=830)]
    map_edges=[]
    for sc in('MCCGF64','MCGFL164'):
        a,z=ranges[sc]
        for i in range(a-1,z):
            m=re.match(r'\s*call\s+(MAP_\w+)\(',lines[i],re.I)
            if not m:continue
            end=i
            while lines[end].rstrip().endswith('&'):end+=1
            if lines[end+1].strip()!='if (.not. map_ok) return':raise RuntimeError('actual private MAP call must directly precede original map_ok failure guard')
            map_edges.append(dict(caller=sc,callee=m[1].upper(),call_source_line=i+1,caller_failed_guard_source_line=end+2))
    if len(map_edges)!=29:raise RuntimeError('actual29 private typed MAP call failure guards')
    OUT.mkdir();cp=OUT/'SPOR64_A8.f90';write(cp,current);ip=OUT/'COMPLETE_A8_247_FALSE_RETURN_SOURCE_WHOLE_BYTE_INVERSE.json'
    write(ip,dict(schema='COMPLETE_A8_247_FALSE_RETURN_DIAGNOSTIC_SOURCE_WHOLE_BYTE_INVERSE_V1',original_source_pin=originalpin,active_original_Source_pin=originalpin,diagnostic_source_pin=pin(cp),changes=changes,whole_file_inverse_byte_equal=True,only247_original_okFalse_return_site_stdout_and_flush_added=True,all_original_condition_expressions_single_evaluation_unchanged=True,all_original_declarations_public_ABI_math_loops_allocations_status_assignments_and_write_order_unchanged=True,active_normalization486_488_strict_work_target_and_stdout_wholebytes_unchanged=True,source_only=True,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False))
    pp=OUT/'SOURCE_ONLY_A8_247_FALSE_RETURN_DIAGNOSTIC_PLAN.json'
    plan=dict(schema='SOURCE_ONLY_SPOR64_A8_247_FALSE_RETURN_DIAGNOSTIC_PLAN_V1',event_schema=EVENT_SCHEMA,source_only=True,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False,original_source_pin=originalpin,active_original_Source_pin=originalpin,diagnostic_source_pin=pin(cp),complete_byte_inverse_pin=pin(ip),Source_preparer_pin=pin(__file__),replacement_zero_based_link_index=1,actual_retained_A8_object1_pin=old1,original_module_pin=modulepin,current_actual_base_report_pin=basepin,current_actual_base_Root_true_tool_pin=rootpin,current_actual_base_Host_freeze_pin=base['actual_host_Source_freeze_pin'],current_actual_ordered70_pins=old70,actual_original_object1_compile_binding_report_pin=originalbuildpin,actual_original_object1_compile_command=compilematches[0]['command'],scope_counts=SCOPES,explicit_return_total_in_ten_scopes=249,failed_original_okFalse_return_count=247,excluded_okTrue_success_returns=success,original_okFalse_assignment_lines=expectedfalse,original_okTrue_assignment_lines=expectedtrue,original_RECORD_MATCHES_assignment_lines=expectedmatch,original_return_mapping=mapping,probe_wrapper_exclusions=excluded,normal_success789_1112_okTrue_return_wholebytes_unchanged=True,active_normalization486_488_strict_work_target_and_stdout_wholebytes_unchanged=True,active_normalization486_488_complete_original_statement=normalization,external_ACA0_Source_and_void_sweeps_not_instrumented_or_changed=True,external_ACA0_false_caller_guard=dict(scope='MCGFL164',source_line=946,callee='SPOR64_A8_ACA.MCGFCA64',no_inner_ACA_predicate_claim=True),actual_same_module_direct_child_failed_guard_edges=internal_edges,actual_private_MAP_failed_guard_edges=map_edges,maximum_A8_module_failed_scope_chain_length=6,A8_chain_must_end_DOORFV64_then_actual_A9_CORE233_then_outer_status2=True,no_new_helper_or_API_or_module_declaration=True,all_original_conditions_math_thresholds_resource_caps_and_acceptance_unchanged=True,callee_to_caller_failure_stdout_chain_only=True,actual_A8_scope_failure_predicate_unknown=True,current_other69_including_A9actual2_Native47_BOOTB49_BOXX68_Driver37_BOOTQ40_math57_and_archives_retained=True,future_cleanup_manifest_pin=None,future_actual_Dragon_pin=None,future_actual_object_pin=None,future_actual_mod_pin=None,future_actual_Runtime_Host_freeze_pin=None,future_actual_BOOT_report_pin=None,future_actual_failed_predicate_ID=None,future_actual_independent_base_post_tools_pin=None,new_module_wholebytes_original_A8_ABI_equality_required=True,engineering_qualified=False,physics_qualified=False)
    write(pp,plan);ready=OUT/'READY.json';write(ready,dict(schema='SOURCE_ONLY_A8_247_FALSE_RETURN_DIAGNOSTIC_READY_V1',status='SOURCE_ONLY_A8_247_FALSE_RETURN_DIAGNOSTIC_READY_NO_RUNTIME',Source_pin=pin(cp),inverse_pin=pin(ip),PLAN_pin=pin(pp),Source_preparer_pin=pin(__file__),failed_return_count247=247,scope_counts=SCOPES,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False,future_actual_Runtime_Host_freeze_pin=None,future_actual_object_pin=None,future_actual_mod_pin=None,future_actual_Dragon_pin=None,future_actual_BOOT_report_pin=None))
    if pin(ORIGINAL)!=originalpin or pin(modulepin['path'])!=modulepin or pin(old1['path'])!=old1:raise RuntimeError('all original Source/object/module complete EOF current7 preserved')
    fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)
    print(json.dumps(dict(status='SOURCE_ONLY_A8_247_FALSE_RETURN_DIAGNOSTIC_READY',Source_pin=pin(cp),inverse_pin=pin(ip),PLAN_pin=pin(pp),READY_pin=pin(ready),Source_preparer_pin=pin(__file__),original_return_count249=249,failed_return_count247=247,excluded_okTrue_returns2=2,scope_counts=SCOPES,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False)))
if __name__=='__main__':main()
