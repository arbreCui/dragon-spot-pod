"""Read-only actual v11 postclosure review; requires Root's real external receipts.

Preparing this file runs no business. The audit entry must be invoked only after
Root reports the genuine once-run terminal return. It never compiles, launches a
child, changes Source or business output, or grants formal AAA/ABA qualification.
"""
import argparse, ast, contextlib, hashlib, importlib.util, json, math, os
from pathlib import Path
import resource, shlex, shutil, stat, sys, time

R=Path('/Users/wen/spot')
REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
SOURCE=REC/'aaa_three_plane_streaming_pipeline_source_v11'
EXPECTED_OUT=R/'validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v11'
COMPILER=Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')
EXPECTED_HF=dict(path=str(SOURCE/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'),sha256='2597f653ebb8d24e454d0f129efb1db1f623073e4524b9ce0b560d54ade56736',size_bytes=163351,identity=[16777229,50017634,33188,1,163351,1791873144732798330,1791873144732798330])
EXPECTED_CLI=dict(path=str(REC/'ROOT_EXACT_ACTUAL_PIPELINE_V11_ARGV_20261013.json'),sha256='5a00c302d82b76ff7cb8776aa2bfc7db5aa126c9c4845e495f74ce5c776507d1',size_bytes=13380,identity=[16777229,50017635,33188,1,13380,1791873144733698750,1791873144733698750])
MI=2**20; GI=2**30; COLD=20971764748
START=time.monotonic();CHECKS=[];HASHED={};COMPILER_PIN=None
FORBIDDEN=['SPOR64_BOOTB64-CENSUS:','ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1',
 'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE','ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE',
 'SPOT-R64 B2I BOOTSTRAP COMMITTED','SPOT-X-REAL64-TERMINAL']
DIRECT={'pack_original_alias','initial_contract_alias','view_system_alias'}
MUTATIONS=['missing_seal','wrong_case','wrong_plane','wrong_epoch','flux32','source32','LPOD_only']
ORDER=[('build/direct_alias_compile','PASS'),('build/direct_alias_link','PASS')]
ORDER += [('AAA/'+n,'FAILED')for n in ['pack_missing_original','pack_memory_outputs','pack_original_alias','pack_wrong_order','pack_no_fake_options']]
ORDER += [('AAA/pack','PASS'),('build/mutator_0','PASS'),('build/mutator_1','PASS')]
ORDER += [('AAA/'+n,'FAILED')for n in ['initial_missing_rank','initial_duplicate_rank','initial_wrong_rank_type','initial_zero_rank','initial_missing_plane_contract','initial_contract_alias','initial_wrong_plane_order']]
for mutation in MUTATIONS:ORDER += [('AAA/mutate_'+mutation,'PASS'),('AAA/initial_'+mutation,'FAILED')]
ORDER += [('AAA/initial_positive','PASS'),('AAA/global_positive','PASS')]
ORDER += [('AAA/'+n,'FAILED')for n in ['project_missing_rank','project_rank_type','project_zero_rank','project_duplicate_rank','project_case_rank_mismatch','project_memory_output']]
ORDER += [('AAA/project_positive','PASS')]
ORDER += [('AAA/'+n,'FAILED')for n in ['view_missing_operand','view_memory_output','view_system_alias','pair_missing_rank','pair_rank_type','pair_case_rank_mismatch']]
ORDER += [('AAA/mutate_retained_global_case','PASS'),('AAA/lifecycle_mutated_retained_global','FAILED'),('AAA/lifecycle_no_private_archive_overwrite','FAILED'),('AAA/BOOT_positive','PASS')]
MARKERS={'pack':'ACTUAL-AAA3-INDEPENDENT-PACK-COMPLETE','initial_positive':'ACTUAL-AAA3-INITIAL-OPERATOR-COMPLETE',
 'global_positive':'ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE','project_positive':'ACTUAL-AAA3-SINGLE-PRIVATE-PROJECT-COMPLETE',
 'BOOT_positive':'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE'}

def need(ok,name):
    if not ok:raise RuntimeError(name)
    CHECKS.append(name)
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*MI:raise RuntimeError('independent readonly audit SELF512 cap')
    if time.monotonic()-START>=1800:raise RuntimeError('independent readonly audit whole1800 cap')

def identity(p):
    s=Path(p).lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def valid_pf(p):
    return isinstance(p,dict)and all(k in p for k in ('path','sha256','size_bytes','identity'))and \
      isinstance(p['path'],str)and Path(p['path']).is_absolute()and isinstance(p['sha256'],str)and \
      len(p['sha256'])==64 and all(x in '0123456789abcdef'for x in p['sha256'])and type(p['size_bytes'])is int and \
      p['size_bytes']>=0 and isinstance(p['identity'],list)and len(p['identity'])==7 and \
      all(type(x)is int for x in p['identity'])and p['identity'][4]==p['size_bytes']

def pin(path,wanted=None):
    path=Path(path);before=identity(path)
    need(stat.S_ISREG(before[2])and not any(p.is_symlink()for p in(path,*path.parents)),'literal regular path/no aliases:'+str(path))
    need(before[3]==1 or(path==COMPILER and COMPILER_PIN is not None and before==COMPILER_PIN['identity']),
         'nlink1 or unique exact unchanged immutable compiler role:'+str(path))
    if str(path)in HASHED:
        need(HASHED[str(path)]['identity']==before,'previous EOF identity remains exact:'+str(path));actual=HASHED[str(path)]
    else:
        fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
        try:
            s=os.fstat(fd);need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before,'opened full7:'+str(path))
            h=hashlib.sha256();offset=0
            while offset<before[4]:
                data=os.pread(fd,min(MI,before[4]-offset),offset)
                need(bool(data),'no short fullEOF:'+str(path));h.update(data);offset+=len(data)
            s=os.fstat(fd);need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before==identity(path),'post fullEOF same fd/path all7:'+str(path))
            actual=dict(path=str(path),sha256=h.hexdigest(),size_bytes=before[4],identity=before)
        finally:os.close(fd)
        HASHED[str(path)]=actual
    if wanted is not None:need(valid_pf(wanted)and actual=={k:wanted[k]for k in actual},'exact actual wholeEOF SHA/size/all7:'+str(path))
    return actual

def read_json(path,wanted=None):
    p=pin(path,wanted);need(p['size_bytes']<=64*MI,'readonly metadata64MiB cap:'+str(path))
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
    try:
        with os.fdopen(fd,'rb',closefd=False)as stream:raw=stream.read(64*MI+1)
        s=os.fstat(fd);need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==p['identity']==identity(path),'metadata same opened fd/path7:'+str(path))
        need(len(raw)==p['size_bytes']and hashlib.sha256(raw).hexdigest()==p['sha256'],'metadata exact pinned bytes:'+str(path))
        return json.loads(raw),p
    finally:os.close(fd)

def external(args,prefix):
    seven=json.loads(getattr(args,prefix+'_seven_id'))
    need(isinstance(seven,list)and len(seven)==7 and all(type(x)is int for x in seven),'mandatory external all7 integers:'+prefix)
    wanted=dict(path=getattr(args,prefix),sha256=getattr(args,prefix+'_sha256'),size_bytes=seven[4],identity=seven)
    return read_json(wanted['path'],wanted)

def table(rows,name):
    out={}
    for row in rows:
        need(valid_pf(row),'complete PF row:'+name)
        need(row['path']not in out or out[row['path']]==row,'no ambiguous fullPF:'+name)
        out[row['path']]=row
    need(len(out)==len(rows),'unique exact fullPF rows:'+name)
    return out

def resource_snapshot(row,baseline,phase=True):
    need(isinstance(row,dict)and row.get('reason')is None,'actual complete resource snapshot successful')
    need(row['min_free_bytes']==8*GI and row['artifact_budget_bytes']==96*GI,'original history96/free8 cap values')
    need(type(row['artifact_bytes'])is int and row['artifact_bytes']+COLD+64*MI<96*GI,'original history cold+metadata reserve actually fits')
    need(type(row['disk_free_bytes'])is int and row['disk_free_bytes']>=8*GI,'actual snapshot disk free floor')
    need(row['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'and row['resource_scope_contract']==baseline['resource_scope_contract'],'original complete dynamic history scope contract exact')
    for key in ('declared_resource_roots','resource_roots'):
        roots=row[key]
        need(isinstance(roots,list)and roots and len(roots)==len(set(roots))and all(isinstance(p,str)and Path(p).is_absolute()for p in roots),'complete unique literal root array:'+key)
        need(set(baseline[key]).issubset(roots),'all initial historical roots preserved:'+key)
    need(set(row['declared_resource_roots']).issubset(row['resource_roots']),'no declared resource root omitted')
    fresh=row['fresh_output']
    need(fresh['min_free_bytes']==8*GI and fresh['artifact_budget_bytes']==2*GI and fresh['resource_roots']==[str(EXPECTED_OUT)],'original exact fresh namespace2GiB scope')
    need(type(fresh['artifact_bytes'])is int and 0<=fresh['artifact_bytes']<2*GI,'original fresh cap actually passes')
    need(fresh['disk_free_bytes']-COLD-2*GI>=8*GI,'actual disk retains original cold+fresh/free8 reserves')
    if phase:
        reserve=row['publication_reserved_bytes']
        need(reserve in(0,8*MI)and fresh['artifact_bytes']+reserve<2*GI,'actual publication reserve inside original fresh2GiB')
        need(type(row['observed_fresh_peak_bytes'])is int and fresh['artifact_bytes']<=row['observed_fresh_peak_bytes']<2*GI,'recorded phase peak finite under original fresh cap')

def source_oracles(source):
    tree=ast.parse(source);oracle={}
    for n in ast.walk(tree):
        if isinstance(n,ast.For)and isinstance(n.iter,(ast.List,ast.Tuple)):
            for value in n.iter.elts:
                if isinstance(value,ast.Tuple)and len(value.elts)>=3 and isinstance(value.elts[0],ast.Constant)and isinstance(value.elts[-1],ast.Constant):
                    name,message=value.elts[0].value,value.elts[-1].value
                    if isinstance(name,str)and isinstance(message,str)and message.startswith(('APACKX64:','SPO','BPROJX64:')):oracle[name]=message
        if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='refuse'and n.args and isinstance(n.args[0],ast.Constant)and str(n.args[0].value).startswith('lifecycle_'):
            need(isinstance(n.args[-1],ast.Constant),'literal frozen lifecycle oracle');oracle[n.args[0].value]=n.args[-1].value
    for name in MUTATIONS:oracle['initial_'+name]='SPOASM: INVALID OFFLINE REAL64 SOURCE ITEM.'if name=='source32'else'SPOASMP64: GENUINE COMPLETE NATIVE INPUT REQUIRED.'
    need(set(oracle)=={label.split('/',1)[1]for label,status in ORDER if status=='FAILED'},'complete33 exact declared negative Source oracles')
    need("for mutation in ['missing_seal','wrong_case','wrong_plane','wrong_epoch','flux32','source32','LPOD_only']:"in source,'frozen exact original seven mutation order')
    return oracle

def current_view(raw,catalog):
    mapping={}
    for row in catalog['rows']:
        old,new=row['historical_pin'],row['current_pin']
        need(valid_pf(old)and valid_pf(new),'complete original/current catalog roles')
        need(old['path']==new['path']and old['sha256']==new['sha256']and old['size_bytes']==new['size_bytes']and old['identity'][1:]==new['identity'][1:]and old['identity'][0]in(16777234,16777229)and new['identity'][0]==16777229,'catalog legal device-only transition preserving all other6 and SHA')
        pin(new['path'],new);key=(old['path'],old['sha256'],old['size_bytes'],tuple(old['identity']))
        need(key not in mapping or mapping[key]==new,'no oldPF current mapping ambiguity');mapping[key]=new
    def visit(v):
        if isinstance(v,dict):
            key=(v['path'],v['sha256'],v['size_bytes'],tuple(v['identity']))if valid_pf(v)else None
            result={k:visit(x)for k,x in v.items()}
            if key in mapping:result.update(mapping[key])
            return result
        return[visit(x)for x in v]if isinstance(v,list)else v
    return visit(raw)

def main():
    global COMPILER_PIN
    parser=argparse.ArgumentParser(description=__doc__)
    for prefix in ('actual-summary','root-true-receipt','host-freeze','execution-cli'):
        for suffix in ('','-sha256','-seven-id'):parser.add_argument('--'+prefix+suffix,required=True)
    parser.add_argument('--review-output',required=True)
    args=parser.parse_args();review_path=Path(args.review_output)
    need(review_path.parent.resolve()==Path(__file__).resolve().parent and not review_path.exists()and not review_path.is_symlink(),'new independent review result only, no Source/business write')
    hf,phf=external(args,'host_freeze');cli,pcli=external(args,'execution_cli')
    need(phf==EXPECTED_HF and pcli==EXPECTED_CLI,'exact previously frozen v11 HF and CLI pins required')
    need(hf['schema']=='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V11'and len(hf['dependencies'])==308,'complete exact owning v11 HF schema/dependency closure')
    COMPILER_PIN=next(p for p in hf['dependencies']if p['path']==str(COMPILER))
    need(COMPILER_PIN['identity'][3]==2 and [p for p in hf['dependencies']if p['identity'][3]!=1]==[COMPILER_PIN],'unique existing compiler immutable exact nlink2 role')
    pin(hf['host_source']['path'],hf['host_source'])
    for p in hf['dependencies']:pin(p['path'],p)
    for p in cli['mandatory_external_bindings'].values():pin(p['path'],p)
    need(cli['mandatory_external_bindings']['host-freeze']==phf and str(SOURCE/'run_actual_three_plane_pipeline.py')in cli['argv'],'actual selected CLI binds exact owning Source/HF')
    receipt,preceipt=external(args,'root_true_receipt');summary,psummary=external(args,'actual_summary')
    need(receipt['schema']=='ROOT_ACTUAL_PIPELINE_V11_TRUE_TOOL_RETURNS_V1'and receipt['observed_closed']is True and type(receipt['original_integer_exit_code'])is int and receipt['original_integer_exit_code']==0,'Root real observed closed integer exit0 required')
    need(type(receipt['terminal']['exit_code'])is int and receipt['terminal']['exit_code']==0 and isinstance(receipt['terminal']['chunk_id'],str)and receipt['terminal']['chunk_id']and 'session_id'not in receipt['terminal'],'actual terminal tool completed, not a yielded cell')
    need(isinstance(receipt['initial']['chunk_id'],str)and type(receipt['initial']['session_id'])is int and receipt['initial']['session_id']>0,'actual initial Root business tool/session receipt')
    need(receipt['executed_exact_cli_pin']==pcli and receipt['actual_summary_pin']==psummary and receipt['original_SELF512_limit_not_relaxed']is True,'Root receipt binds actual exact CLI/summary and unchanged original SELF')
    need(receipt['executed_command']==shlex.join(cli['argv']),'real Root execution command exactly matches all reviewed CLI arguments')
    need(psummary['path']==str(EXPECTED_OUT/'Root_actual_three_plane_engineering_summary.json'),'actual v11 own final summary namespace')
    need(summary['schema']=='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1'and summary['status']=='ACTUAL_THREE_PLANE_ENGINEERING_CLOSED0_ONLY'and summary['engineering_three_plane_closed0']is True,'actual full engineering closed0 only')
    need(summary['failure']is None and summary['after_check_error']is None and summary['original_guard_class']=='OwnRSSSerialExecutor'and summary['original_guard_MRO_unchanged']is True,'actual unchanged original supervisor closure without failure')
    need(type(summary['SELF_peak_bytes'])is int and 0<=summary['SELF_peak_bytes']<512*MI and 0<summary['wall_seconds']<1800,'actual original SELF512/whole1800 reporting guard')
    for key in ('three_plane_qualified','GLOBAL_qualified','rank_qualified','online_BOOT_qualified','AAA_qualified','ABA_admitted','goal_complete','independent_reference_physics_assessment_executed'):
        need(summary[key]is False,'engineering scope does not grant formal/physics authority:'+key)
    need(summary['angular_moments_status']=='UNKNOWN'and summary['all_new_storage_entry_controls_closed']is True,'all storage entry guards closed while angular authority unknown')
    fixed=table(summary['fixed_current_pins'],'fixed');outputs=table(summary['output_pins'],'outputs');owned=table(summary['owned_runtime_pins'],'owned')
    for rows in(fixed,outputs,owned):
        for p in rows.values():pin(p['path'],p)
    need(fixed[phf['path']]==phf and fixed[hf['host_source']['path']]==hf['host_source'],'current fixed binds exact actual owning complete Source')
    need(all(fixed[p['path']]==p for p in hf['dependencies']),'all308 Source dependencies retained in actual full fixed pins')
    need(all(outputs[p]==v for p,v in owned.items()),'all owning live/runtime files included in complete output inventory')
    need(not set(tuple(p['identity'][:2])for p in fixed.values()).intersection(tuple(p['identity'][:2])for p in outputs.values()),'all current outputs physically independent of protected fixed inputs')
    need(all(p['identity'][3]==1 and Path(p['path']).is_relative_to(EXPECTED_OUT)for p in outputs.values()),'output namespace exclusive regular nlink1 roles')
    actual_files={str(p)for p in EXPECTED_OUT.rglob('*')if p.is_file()}
    need(not any(p.is_symlink()for p in EXPECTED_OUT.rglob('*'))and actual_files==set(outputs)|{psummary['path']},'complete final publication inventory plus final summary, no omitted live file')
    need(psummary['size_bytes']<8*MI and summary['final_publication_reserved_bytes']==8*MI,'actual final summary inside original independently reserved8MiB')
    need(sum(p['size_bytes']for p in outputs.values())+psummary['size_bytes']<2*GI and shutil.disk_usage(EXPECTED_OUT).free-COLD-2*GI>=8*GI,'current final publication fresh2GiB/free8 and original cold reserves')
    rawpin=summary['complete_unmodified_execution_records_pin'];need(outputs[rawpin['path']]==rawpin,'final inventory pins complete raw execution proof')
    raw,_=read_json(rawpin['path'],rawpin);stagepath=str(EXPECTED_OUT/'AAA3-streaming/stages.json');stages,_=read_json(stagepath,outputs[stagepath])
    need(set(stages)=={'stages'}and raw['records']==stages['stages'],'all50 original unmodified raw resource records exactly equal genuine serial ledger')
    records=raw['records'];need(len(ORDER)==50 and [(x['label'],x['status'])for x in records]==ORDER,'exact ordered50 stages with17 PASS and33 intended FAILED')
    need(summary['records']==[{k:v for k,v in x.items()if k not in('resource_before','resource_after')}for x in records],'compact receipt is exact projection of all50 original records')
    need(raw['failure']is None and raw['after_check_error']is None and raw['engineering_three_plane_closed0']is False and raw['exact_publication_pending']is True,'raw prepublication evidence honestly remains pending; true Root exit0 establishes later publication')
    need(raw['fixed_current_pins']==summary['fixed_current_pins']and raw['owned_runtime_pins']+[rawpin]==summary['owned_runtime_pins'],'raw-to-final exact fixed and own-runtime publication relation')
    baseline=summary['resources_before'];resource_snapshot(baseline,baseline,False);resource_snapshot(summary['resources_after'],baseline)
    need(baseline['artifact_bytes']+COLD+64*MI+2*GI<96*GI,'initial original full fresh/history reserve admitted')
    source=Path(hf['host_source']['path']).read_text();oracles=source_oracles(source)
    cases=summary['actual_operator_refusals'];case_by={x['case']:x for x in cases}
    need(len(cases)==len(case_by)==33 and set(case_by)==set(oracles),'all33 unique actual refusal cases exactly cover Source oracles')
    need(raw['actual_operator_refusals']==cases,'complete raw and compact original refusal proofs agree')
    scratch=summary['actual_closed_CLE_scratch_archival_ledger'];need(scratch==raw['actual_closed_CLE_scratch_archival_ledger'],'all original scratch receipts preserved in raw and compact proof')
    scratch_by={x['actual_stage_index']:x for x in scratch};expected_scratch={i for i,(label,status)in enumerate(ORDER)if label.startswith('AAA/')and label.split('/',1)[1]not in DIRECT and not label.split('/',1)[1].startswith('mutate_')}
    need(len(scratch_by)==len(scratch)and set(scratch_by)==expected_scratch,'every actual Dragon stage has one closed scratch receipt; direct/mutator stages do not forge CLE receipts')
    for i,record in enumerate(records):
        label=record['label'];folder,name=label.split('/',1);wp=str(EXPECTED_OUT/folder/(name+'.watchdog.json'));lp=str(EXPECTED_OUT/folder/(name+'.log'))
        watch,_=read_json(wp,outputs[wp]);pin(lp,outputs[lp]);text=Path(lp).read_text()
        need(type(watch.get('pid'))is int and watch['pid']>0 and type(watch['returncode'])is int and watch['returncode']==(0 if record['status']=='PASS'else 1),'actual child pid and exact terminal exit:'+label)
        need(watch['command']==record['command']and watch['limit_failure']is None and watch['rss_cap_mib']==512 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True,'actual unchanged own-child supervisor and cleanup:'+label)
        need(0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=record['wall_cap_seconds']<=600 and 0<=watch['sampled_peak_rss_mib']<512 and 0<record['elapsed_seconds']<600,'actual original stage600/ownchild512 limits:'+label)
        resource_snapshot(record['resource_before'],baseline)
        if record['status']=='PASS':
            resource_snapshot(record['resource_after'],baseline)
            need(record['log_sha256']==outputs[lp]['sha256'],'PASS-only original log digest field matches fullEOF:'+label)
            # The original positive gate requires presence; CLE logs may also
            # echo the input card. Exact-once remains mandatory for refusals.
            if name in MARKERS:need(MARKERS[name]in text,'original exact positive completion marker present:'+name)
        else:
            need('resource_after'not in record and 'log_sha256'not in record and record['error']=='own-child stage failed; no retry','honest original FAILED record shape, no fabricated PASS-only fields:'+label)
            case=case_by[name];need(case['expected_abort']==oracles[name]and case['actual_exit_code']==1 and case['original_execution_record_index']==i and case['original_execution_record_label']==label,'exact negative oracle and genuine stage binding:'+label)
            need(case['actual_log_pin']==outputs[lp]and case['actual_watchdog_pin']==outputs[wp],'actual FAILED proof pins match entire output EOF table:'+label)
            for key in('actual_abort_message_exact','pre_transport_abort_at_frozen_validation_branch','no_positive_solver_or_seal_trace','all_actual_assertions_completed'):need(case[key]is True,'completed exact negative assertion:'+label+':'+key)
            need(text.count(oracles[name])==1 and not any(mark in text for mark in FORBIDDEN),'exact intended negative target message once and no positive transport trace:'+label)
            if name in DIRECT:
                need(text.count('ACTUAL-AAA3-DIRECT-ALIAS-CONTROL: '+name)==1 and case['CLE_dispatch_executed']is False and case['transport_executed']is False and case['component_structural_guard_only']is True,'genuine distinct-name duplicate-pointer component entry only:'+name)
                need(not any(mark in text for mark in('kernel error','INCONSISTENT CALL','TARGET GUARD RETURNED')),'direct alias reaches exact frozen target guard:'+name)
        if i in scratch_by:
            item=scratch_by[i];need((item['actual_stage_label'],item['actual_pid'],item['actual_returncode'])==(label,watch['pid'],watch['returncode'])and item['actual_log_full_pin']==outputs[lp]and item['actual_watchdog_full_pin']==outputs[wp],'scratch receipt owns the exact closed child/log/watch:'+label)
            need(item['scratch_protocol_sources']==hf['scratch_protocol_sources']and item['no_qualification_from_archival']is True,'scratch protocol Source and scope unchanged:'+label)
            receipt_path=str(EXPECTED_OUT/('Root_actual_closed_CLE_scratch_stash_'+str(i+1).zfill(3)+'.json'));receipt_value,_=read_json(receipt_path,outputs[receipt_path]);need(receipt_value==item,'complete persisted scratch receipt exact:'+label)
            for pair in item['exact_preserved_scratch_files']:
                before,after=pair['before_full_pin'],pair['after_full_pin'];need(valid_pf(before)and valid_pf(after)and before['sha256']==after['sha256']and before['size_bytes']==after['size_bytes']and before['identity'][:6]==after['identity'][:6],'same physical scratch inode/raw bytes across rename:'+label)
                need(pair['ctime_may_change_during_rename']is True and pair['exact_physical_raw_replay_retained']is True and outputs[after['path']]==after,'current archived scratch exact retained PF:'+label)
    for name in('_main001','_DUMMY'):need(not(EXPECTED_OUT/'AAA'/name).exists()and not(EXPECTED_OUT/'AAA'/name).is_symlink(),'actual final original CLE scratch paths absent:'+name)
    need(summary['actual_direct_structural_alias_control_names']==['pack_original_alias','initial_contract_alias','view_system_alias']and raw['actual_direct_alias_build']==summary['actual_direct_alias_build'],'all three exact direct structural modes and original build proof')
    direct=summary['actual_direct_alias_build'];buildpin=cli['mandatory_external_bindings']['build70'];build,_=read_json(buildpin['path'],buildpin)
    inputs=build['records'][-1]['command'][3:-2];need(len(inputs)==70 and len(set(inputs))==70 and [x['path']for x in direct['original_ordered_70_inputs']]==inputs,'original exact ordered70 component/archive inputs preserved')
    newobj=direct['actual_new_main_full_pin'];probe=direct['actual_new_executable_full_pin'];need(outputs[newobj['path']]==newobj and outputs[probe['path']]==probe,'actual direct compile/link outputs fullEOF current')
    expected_inputs=[newobj['path']if Path(p).name=='DRAGON.o'else p for p in inputs]
    need(direct['actual_compile_link_record_indices']==[0,1]and direct['only_main_replaced']is True and direct['physics_qualification']is False and direct['retained_original_component_and_archive_count']==69,'direct probe exact one-main scope')
    need(records[1]['command']==[*build['records'][-1]['command'][:3],*expected_inputs,'-o',probe['path']],'actual direct link command preserves complete original70 order')
    commonsource=Path(hf['current_Common_Source_pin']['path'])if 'current_Common_Source_pin'in hf else Path(hf['current_Common_source_pin']['path'])if 'current_Common_source_pin'in hf else REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py'
    commonpin=next(x for x in hf['dependencies']if x['path']==str(commonsource));pin(commonsource,commonpin)
    commontree=ast.parse(commonsource.read_text());flags=ast.literal_eval(next(n.value for n in commontree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='FLAGS'for t in n.targets)))
    compiler=build['records'][0]['command'][0];includes=[x for x in build['records'][0]['command']if x.startswith('-I')];archives=[x for x in build['records'][-1]['command']if x.endswith('.a')]
    expected_compile=[compiler,*flags,*includes,'-J'+str(EXPECTED_OUT/'build'),'-c',str(SOURCE/'direct_alias_entry_controls.f90'),'-o',newobj['path']]
    need(records[0]['command']==direct['actual_compile_command']==expected_compile and records[1]['command']==direct['actual_link_command'],'actual direct compile and complete link argv exactly match original flags/order')
    need(direct['actual_new_main_frozen_source_pin']==next(x for x in hf['dependencies']if x['path']==str(SOURCE/'direct_alias_entry_controls.f90')),'direct executable built from exact frozen Fortran main')
    obj=str(EXPECTED_OUT/'build/mutate_owned_control.o');mut=str(EXPECTED_OUT/'runtime/mutate_owned_control')
    need(records[8]['command']==[compiler,*flags,*includes,'-J'+str(EXPECTED_OUT/'build'),'-c',str(SOURCE/'mutate_owned_control.f90'),'-o',obj]and records[9]['command']==[compiler,'-O2','-ffp-contract=off',obj,*archives,'-o',mut],'actual mutator compile/link all original cached argument values exact')
    for label,record in zip(ORDER,records):
        name=label[0].split('/',1)[1]
        if label[0].startswith('AAA/'):
            command=[probe['path'],name]if name in DIRECT else[mut,'negative_project.xsm','global_case']if name=='mutate_retained_global_case'else[mut,'negative_pack.xsm',name[len('mutate_'):]]if name.startswith('mutate_')else[str(EXPECTED_OUT/'runtime/Dragon')]
            need(record['command']==command,'every positive/negative/mutator actual child command matches exact original plan:'+name)
    dragon=outputs[str(EXPECTED_OUT/'runtime/Dragon')];actual_exe=next(x for x in build['output_pins']if Path(x['path']).name=='Dragon');need(dragon['sha256']==actual_exe['sha256']and dragon['size_bytes']==actual_exe['size_bytes'],'actual runtime entire native70 bytes unchanged')
    bounded=outputs[str(EXPECTED_OUT/'runtime/run_bounded_dragon.py')];binding,_=read_json(hf['current_Common_binding_pin']['path'],hf['current_Common_binding_pin']);need(bounded['sha256']==binding['original_bounded']['sha256'],'original bounded runner bytes unchanged')
    releases=raw['actual_private_release_ledger'];need(len(releases)==len(summary['actual_private_release_ledger'])and raw['private_release_ledger_scope']==summary['private_release_ledger_scope']=='HOST_OWNED_UNLINK_ONLY','all private release evidence retained and scoped honestly')
    whitelist={'native_A1.xsm','native_A2.xsm','native_A3.xsm','initial_pack.xsm','global.xsm','negative_pack.xsm','negative_project.xsm','negative_system.xsm','negative_output.xsm','negative_packout.xsm','negative_rcon1.xsm','negative_rcon2.xsm','negative_rcon3.xsm','negative_ax.xsm','negative_archive.xsm','BOOT-SOLVED-STAGE.xsm'}
    for index,(full,compact)in enumerate(zip(releases,summary['actual_private_release_ledger']),1):
        old=full['released_full_pin'];need(valid_pf(old)and Path(old['path']).parent==EXPECTED_OUT/'AAA'and Path(old['path']).name in whitelist and old['identity'][3]==1 and not Path(old['path']).exists(),'released historical owned PF remains explicitly non-live:'+str(index))
        need(compact==dict(released_full_pin=old,reason=full['reason'],complete_evidence_in_unmodified_execution_record=True,exact_intermediate_XSM_raw_replay_retained=False,original_producer_files_retained=True),'compact release is exact honest raw-proof projection:'+str(index))
        rp=str(EXPECTED_OUT/('Root_actual_private_release_'+str(index).zfill(3)+'.json'));actual_release,_=read_json(rp,outputs[rp]);need(actual_release==full,'whole persisted private release receipt:'+str(index))
    need({'native_A1.xsm','native_A2.xsm','native_A3.xsm','initial_pack.xsm','global.xsm'}.issubset(Path(x['released_full_pin']['path']).name for x in releases),'obsolete copies released only after complete proof')
    # Import only the full-pinned passive bounded data reader after true Root
    # closure. Never import/run the pipeline, compile, CLE or any solver.
    readerpin=next(x for x in hf['dependencies']if x['path']==str(SOURCE/'actual_inputs_and_readback.py'));pin(readerpin['path'],readerpin)
    sys.dont_write_bytecode=True;spec=importlib.util.spec_from_file_location('readonly_actual_v11_data',readerpin['path']);data=importlib.util.module_from_spec(spec);spec.loader.exec_module(data)
    catalog,_=read_json(hf['current_mount_full_identity_catalog_pin']['path'],hf['current_mount_full_identity_catalog_pin']);rawplan,planpin=read_json(data.PLAN,next(x for x in hf['dependencies']if x['path']==str(data.PLAN)));plan=current_view(rawplan,catalog)
    proofs=summary['actual_complete_readback_proofs'];need(proofs==raw['actual_complete_readback_proofs']and [x['stage']for x in proofs]==['pack','independent_complete_transfer'],'original independent pack+transfer logical proofs fully retained')
    project=EXPECTED_OUT/'AAA/projected_boot.xsm';pin(project,outputs[str(project)]);need(proofs[1]['project_full_pin']==outputs[str(project)],'independent transfer owning retained PROJECT physical fullPF')
    pack=proofs[0]['actual_full_items'];transfer=proofs[1]['actual_tree_proof'];need(len(pack)==18 and len(transfer['original_three_planes'])==18 and len(transfer['independent_six_contexts'])==6,'complete eighteen independent plane fields and six GLOBAL contexts')
    with contextlib.ExitStack()as stack:
        p=stack.enter_context(data._open_xsm(project));pg=data.node(p,p.root,['GLOBAL64']);archive=data.node(p,pg,['ARCHIVE'])
        need(data.tree_digest(p,pg)==transfer['complete_global'],'entire retained PROJECT/GLOBAL64 tree matches independent pre-release GLOBAL proof')
        need(data.tree_digest(p,archive)==transfer['complete_archive']==transfer['retained_complete_archive'],'entire retained packed archive matches independent pre-release full tree')
        roots={'AX':'ax_current.xsm','AXTRACK':'axial_track.xsm','AXSYSTEM':'initial_system.xsm','AXMACRO':'axial_macro.xsm','RCON':'global_rcon.xsm'}
        for name,filename in roots.items():
            path=EXPECTED_OUT/'AAA'/filename;pin(path,outputs[str(path)]);q=stack.enter_context(data._open_xsm(path));digest=data.exact_tree(p,data.node(p,pg,[name]),q,q.root)
            need(next(x['complete_tree']for x in transfer['independent_six_contexts']if x['field']==name)==digest,'complete original independent GLOBAL context replay:'+name)
        for plane,row in enumerate(plan['producers'],1):
            pin(row['archive']['path'],row['archive']);q=stack.enter_context(data._open_xsm(row['archive']['path']))
            for name in ['TRACK','MICROLIB2','SYSTEM','FLUX','RCONTRACT','BOOT_BIND']:
                digest=data.exact_tree(p,data.node(p,archive,[name,plane]),q,data.node(q,q.root,[name,1]))
                need(next(x['complete_tree']for x in pack if(x['plane'],x['field'])==(plane,name))==digest and next(x['complete_tree']for x in transfer['original_three_planes']if(x['plane'],x['field'])==(plane,name))==digest,'every independent original packed plane/field tree replay:'+str(plane)+':'+name)
    terminal=summary['actual_terminal'];need(terminal==raw['actual_terminal'],'raw/final entire actual terminal proof unchanged')
    ax=terminal['AX_full_pin'];archive=terminal['ARCHIVE_full_pin'];need(outputs[ax['path']]==ax and outputs[archive['path']]==archive,'closed final axial/archive fullEOF inventory pins')
    replay=data.final_readback(ax['path'],archive['path']);need(json.loads(json.dumps(replay))==terminal['actual_terminal'],'complete physical370×3 native terminal types/bits/32 mirrors/system/fission/eigenvalue/tree replay exact')
    need(replay['rank_values']==370 and replay['rank1_all_groups']is True and len(replay['planes'])==3 and [x['plane']for x in replay['planes']]==[1,2,3],'all370 rank1/three actual ordered plane states')
    need(all(x['groups']==370 and x['unknowns']==14 and x['flux_values']==x['source_values']==5180 and x['fission_components']==32 for x in replay['planes']),'complete full non-scalar native flux/source coverage, no shortened group sample')
    need(replay['angular_sixmoments_status']=='UNKNOWN_NOT_AVAILABLE_IN_SCALAR_NATIVE_READBACK'and replay['independent_reference_physics_assessment']is False,'unknown angular moments not manufactured as physics qualification')
    bootlog=Path(EXPECTED_OUT/'AAA/BOOT_positive.log').read_text();sealed=[json.loads(line)for line in bootlog.splitlines()if line.startswith('{"schema":"ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1"')]
    need(len(sealed)==1 and sealed[0]==terminal['actual_Fortran_complete_copy_readback']and sealed[0]['status']=='PASS'and sealed[0]['all_payload_bits_equal']is True,'actual complete sealed-pair native Fortran readback before disposal')
    rp=str(EXPECTED_OUT/'Root_actual_complete_BOOT_terminal_readback.json');saved,_=read_json(rp,outputs[rp]);need(saved==terminal,'entire persisted terminal proof exact')
    for path,p in HASHED.items():need(identity(path)==p['identity'],'final readonly EOF identity closure:'+path)
    result=dict(schema='INDEPENDENT_ACTUAL_PIPELINE_V11_POSTCLOSURE_READONLY_ENGINEERING_REVIEW_V1',status='ACTUAL_V11_ALL50_ORIGINAL_GUARDS_AND_COMPLETE_READONLY_EVIDENCE_ENGINEERING_CLOSED0_ONLY',
      actual_summary_pin=psummary,Root_true_tool_receipt_pin=preceipt,executed_exact_CLI_pin=pcli,host_Source_freeze_pin=phf,
      complete_unmodified_execution_records_pin=rawpin,actual_final_summary_publication_closed_by_Root_exit0=True,
      actual_ordered_stage_count=50,actual_PASS_count=17,actual_exact_intended_exit1_refusal_count=33,
      complete_raw_resource_records_preserved=True,original_failed_record_shape_not_forged=True,
      all33_Source_oracles_watchdogs_case_indices_scratch_and_release_receipts_verified=True,
      all_fixed_Source_and_current_outputs_EOF_all7_identity_verified=True,unique_fullEOF_files=len(HASHED),unique_fullEOF_bytes=sum(x['size_bytes']for x in HASHED.values()),
      reported_business_SELF_peak_bytes=summary['SELF_peak_bytes'],reported_business_wall_seconds=summary['wall_seconds'],
      final_guard_Source_and_real_Root_exit0_required_in_addition_to_reported_peak=True,
      actual_complete370_threeplane_native_terminal_and_independent_original_tree_replay_verified=True,
      original_caps_math_guard_MRO_native70_and_rawrecords_unchanged=True,
      unknown_angular_moments_preserved=True,formal_AAA_qualified=False,ABA_admitted=False,physics_assessment=False,goal_complete=False,
      readonly_auditor_SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,readonly_auditor_wall_seconds=time.monotonic()-START,
      readonly_audit_checks=len(CHECKS),business_or_compiler_CLE_solver_launched_by_audit=False)
    with review_path.open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status=result['status'],review_pin=pin(review_path),checks=len(CHECKS),unique_fullEOF_files=len(HASHED),unique_fullEOF_bytes=sum(x['size_bytes']for x in HASHED.values()),formal_AAA_qualified=False,ABA_admitted=False,goal_complete=False),allow_nan=False))

if __name__=='__main__':main()
