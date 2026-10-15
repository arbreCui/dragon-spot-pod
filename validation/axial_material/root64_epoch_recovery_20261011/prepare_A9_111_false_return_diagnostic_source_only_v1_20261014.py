"""Add failure-only stdout before original A9 okFalse returns; Source preparation only."""
import hashlib,json,os,re,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
ORIGINAL=R/'online_boot_native64_source_v1/ORIGINAL_COMPLETE_SPOR64_A9.f90'
ACTIVE=Path('/Users/wen/spot/src/SPOR64_A9.f90')
OUT=R/'boot_v16_A9_111_false_return_diagnostic_source_v1_20261014'
SCOPES={'FLU2DR64_CORE':55,'FLUBAL64':28,'FLU2AC64':11,'SCALAR_GROUP_NORM64':6,'VALIDATE_OFFGROUP32':11}
SUCCESS={('FLU2DR64_CORE',309),('FLU2AC64',490)}
EVENT_SCHEMA='ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1'
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
    original=ORIGINAL.read_text();originalpin=pin(ORIGINAL);activepin=pin(ACTIVE)
    if originalpin['sha256']!='08c67b99537771b16a27ae16933ef4d431499a79ea30f184a3d1c335e79d7705'or originalpin['size_bytes']!=23581 or ACTIVE.read_bytes()!=original.encode():raise RuntimeError('actual active A9 Source equals entire frozen original')
    lines=original.splitlines(keepends=True);scope=None;ranges={};returnrows=[];falseinit={};trueassign={};scope_start=None
    for i,line in enumerate(lines,1):
        m=re.match(r'\s*(?:pure\s+)?subroutine\s+(\w+)\(',line,re.I)
        if m:scope=m[1].upper();scope_start=i;ranges[scope]=[i,None];trueassign[scope]=[]
        if scope in SCOPES:
            if re.fullmatch(r'\s*ok\s*=\s*\.false\.\s*',line,re.I):
                if scope in falseinit:raise RuntimeError('one original unconditional okFalse initialization per scope')
                falseinit[scope]=i
            if re.fullmatch(r'\s*ok\s*=\s*\.true\.\s*',line,re.I):trueassign[scope].append(i)
            if not line.lstrip().startswith('!')and re.search(r'\breturn\s*$',line,re.I):
                start=i
                while start>scope_start and lines[start-2].rstrip().endswith('&'):start-=1
                returnrows.append(dict(scope=scope,original_statement_start_source_line=start,original_return_source_line=i,original_statement_complete=''.join(lines[start-1:i])))
        if re.match(r'\s*end\s+subroutine\b',line,re.I):
            if scope is not None:ranges[scope][1]=i
            scope=None
    expectedfalse={'FLU2DR64_CORE':82,'FLUBAL64':351,'FLU2AC64':464,'SCALAR_GROUP_NORM64':560,'VALIDATE_OFFGROUP32':588}
    expectedtrue={'FLU2DR64_CORE':[308,328],'FLUBAL64':[450],'FLU2AC64':[489,509],'SCALAR_GROUP_NORM64':[576],'VALIDATE_OFFGROUP32':[613]}
    if falseinit!=expectedfalse or {k:trueassign[k]for k in SCOPES}!=expectedtrue or len(returnrows)!=113:raise RuntimeError('actual original status assignment and explicit-return census')
    success=[r for r in returnrows if(r['scope'],r['original_return_source_line'])in SUCCESS];failed=[r for r in returnrows if(r['scope'],r['original_return_source_line'])not in SUCCESS]
    if len(success)!=2 or len(failed)!=111 or {s:sum(r['scope']==s for r in failed)for s in SCOPES}!=SCOPES:raise RuntimeError('only111 true okFalse return sites; two okTrue returns excluded')
    for r in success:
        i=r['original_return_source_line']
        if lines[i-2].strip().lower()!='ok = .true.'or r['original_statement_complete'].strip().lower()!='return':raise RuntimeError('excluded explicit successful return immediately follows original okTrue')
    mapping=[];changes=[]
    for r in failed:
        scope=r['scope'];i=r['original_return_source_line'];before=r['original_statement_complete'];indent=re.match(r'\s*',before.splitlines()[0]).group();pid='A9_'+scope+'_RETURN_L'+str(i).zfill(4)
        inline=before.strip().lower()!='return'
        if inline:
            if not re.match(r'\s*if\s*\(',before,re.I)or before.count('return')!=1:raise RuntimeError('original single-condition inline return only')
            offset=before.lower().rfind('return');condition=before[:offset]
            if not condition.rstrip().endswith(')'):raise RuntimeError('complete original single-evaluation IF expression')
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
        mapping.append(dict(**r,predicate_id=pid,boolean_result_expression='ok',original_unconditional_okFalse_assignment_source_line=falseinit[scope],original_success_assignment_sites=trueassign[scope],original_okFalse_dominance='Initialization is unconditional. Success assignments occur only in original terminating success sibling branches or after all failed return sites; the success branches cannot reach this failure return.',original_condition_prefix_complete=condition,original_condition_evaluated_once=True,actual_boolean_status_integer_expression='merge(1,0,ok)',required_false_integer=0,only_stdout_write_and_flush_added_before_original_return=True))
    current=original
    for c in sorted(changes,key=lambda x:x['original_return_source_line'],reverse=True):
        start=c['original_statement_start_source_line']-1;end=c['original_return_source_line'];prefix=''.join(lines[:start]);suffix=''.join(lines[end:]);before=c['before']
        # Positional original lines remain authoritative even when common IF text repeats.
        startchar=sum(len(x)for x in lines[:start]);endchar=sum(len(x)for x in lines[:end]);
        if current[startchar:endchar]!=before:raise RuntimeError('exact original positional return splice')
        current=current[:startchar]+c['after']+current[endchar:]
    back=current
    for c in changes:
        if back.count(c['after'])!=1:raise RuntimeError('unique failure-ID complete inverse')
        back=back.replace(c['after'],c['before'],1)
    if back.encode()!=ORIGINAL.read_bytes():raise RuntimeError('whole A9 Source exact byte inverse')
    excluded={}
    for name in('SPOR64_A9_TERMINAL64','SPOR64_A9_STATE_PROBE','SPOR64_A9_OPERATOR_PROBE','SPOR64_A9_COUNTER_PROBE'):
        a,z=ranges[name];block=''.join(lines[a-1:z]);
        if block not in current:raise RuntimeError('terminal acceptedFalse/probe wrapper wholebytes preserved')
        excluded[name]=dict(original_source_line_start=a,original_source_line_end=z,whole_bytes_sha256=hashlib.sha256(block.encode()).hexdigest(),whole_bytes_unchanged_and_no_event=True)
    for r in success:
        i=r['original_return_source_line'];block=''.join(lines[i-2:i]);
        if block not in current:raise RuntimeError('original successful okTrue return unchanged')
    normal='    accepted = .false.\n    ok = .true.\n  end subroutine FLU2DR64_CORE\n'
    if normal not in current:raise RuntimeError('normal MAXOUT unaccepted okTrue fallthrough unchanged')
    postpath=R/'independent_BIND47_strict_native17_consumer_v1_actual_failure_postverify_20261014/REVIEW.json';post=read(postpath);base=read(post['actual_report_pin']);table={p['path']:norm(p)for p in base['fixed_current_pins']+base['output_pins']};old70=[table[p]for p in base['actual_ordered70_link_inputs']];old2=old70[2]
    if not old2['sha256'].startswith('7f377598')or pin(Path(old2['path']))!=old2:raise RuntimeError('actual retained current slot2 A9 object complete PF')
    if old2['size_bytes']!=96472 or post['actual_BOOT_return_status']!=2 or post['actual_stage_statuses']!=['PASS','PASS','FAILED']:raise RuntimeError('actual CORE_FAILED2, not an assumed normal MAXOUT')
    if identity(Path(old2['path']).lstat())!=old2['identity']:raise RuntimeError('actual current A9 object7')
    OUT.mkdir();cp=OUT/'SPOR64_A9.f90';write(cp,current);ip=OUT/'COMPLETE_A9_111_FALSE_RETURN_SOURCE_WHOLE_BYTE_INVERSE.json'
    write(ip,dict(schema='COMPLETE_A9_111_FALSE_RETURN_DIAGNOSTIC_SOURCE_WHOLE_BYTE_INVERSE_V1',original_source_pin=originalpin,active_original_Source_pin=activepin,diagnostic_source_pin=pin(cp),changes=changes,whole_file_inverse_byte_equal=True,only111_original_okFalse_return_site_stdout_and_flush_added=True,all_original_condition_expressions_single_evaluation_unchanged=True,all_original_declarations_public_ABI_math_loops_allocations_status_assignments_and_write_order_unchanged=True,source_only=True,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False))
    pp=OUT/'SOURCE_ONLY_A9_111_FALSE_RETURN_DIAGNOSTIC_PLAN.json'
    plan=dict(schema='SOURCE_ONLY_SPOR64_A9_111_FALSE_RETURN_DIAGNOSTIC_PLAN_V1',event_schema=EVENT_SCHEMA,source_only=True,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False,original_source_pin=originalpin,active_original_Source_pin=activepin,diagnostic_source_pin=pin(cp),complete_byte_inverse_pin=pin(ip),Source_preparer_pin=pin(__file__),replacement_zero_based_link_index=2,actual_retained_A9_object2_pin=old2,current_actual_base_report_pin=post['actual_report_pin'],current_actual_base_post_review_pin=pin(postpath),current_actual_base_post_tools_pin=pin(postpath.with_name('TRUE_TOOL_RETURNS.json')),current_actual_base_Root_true_tool_pin=post['actual_Root_true_tool_return_pin'],current_actual_base_Host_freeze_pin=post['actual_Host_freeze_pin'],current_actual_ordered70_pins=old70,scope_counts=SCOPES,explicit_return_total_in_five_scopes=113,failed_original_okFalse_return_count=111,excluded_okTrue_success_returns=success,original_okFalse_initialization_lines=falseinit,original_okTrue_assignment_lines=expectedtrue,original_return_mapping=mapping,terminal_and_probe_wrapper_exclusions=excluded,normal_MAXOUT_okTrue_acceptedFalse_fallthrough_wholebytes_unchanged=True,normal_MAXOUT_would_original_BOOTB_NOT_ACCEPTED3_not_CORE_FAILED2=True,original_DOORFV64_A8_child_Source_not_instrumented_or_changed=True,no_new_helper_or_API_or_module_declaration=True,all_original_conditions_math_thresholds_resource_caps_and_acceptance_unchanged=True,callee_to_caller_failure_stdout_chain_only=True,actual_scope_failure_predicate_unknown=True,future_cleanup_manifest_pin=None,future_actual_Dragon_pin=None,future_actual_object_pin=None,future_actual_mod_pin=None,future_actual_Runtime_Host_freeze_pin=None,future_actual_BOOT_report_pin=None,future_actual_failed_predicate_ID=None,new_module_wholebytes_original_A9_ABI_equality_required=True,engineering_qualified=False,physics_qualified=False)
    write(pp,plan);ready=OUT/'READY.json';write(ready,dict(schema='SOURCE_ONLY_A9_111_FALSE_RETURN_DIAGNOSTIC_READY_V1',status='SOURCE_ONLY_A9_111_FALSE_RETURN_DIAGNOSTIC_READY_NO_RUNTIME',Source_pin=pin(cp),inverse_pin=pin(ip),PLAN_pin=pin(pp),Source_preparer_pin=pin(__file__),failed_return_count111=111,scope_counts=SCOPES,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False,future_actual_Runtime_Host_freeze_pin=None,future_actual_object_pin=None,future_actual_mod_pin=None,future_actual_Dragon_pin=None,future_actual_BOOT_report_pin=None))
    print(json.dumps(dict(status='SOURCE_ONLY_A9_111_FALSE_RETURN_DIAGNOSTIC_READY',Source_pin=pin(cp),inverse_pin=pin(ip),PLAN_pin=pin(pp),READY_pin=pin(ready),Source_preparer_pin=pin(__file__),original_return_count113=113,failed_return_count111=111,excluded_okTrue_returns2=2,scope_counts=SCOPES,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False)))
if __name__=='__main__':main()
