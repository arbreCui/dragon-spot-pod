"""Pure Root postterminal receipt writer. No business imports or commands run.

UNEXECUTED: every future tool/SHA/observation in config starts None. Root alone
may fill genuine completed tool observations. File existence is never exit proof.
This writer does not independently admit scientific input, controls or cold AAA.
"""
from pathlib import Path
import hashlib,json,os,sys,time

BASE=Path(__file__).resolve().parent

def fail(message):raise ValueError(message)
def require(value,message):
    if not value:fail(message)
def pairs(items):
    d={}
    for k,v in items:
        if k in d:fail('duplicate JSON key')
        d[k]=v
    return d
def read(path):
    return json.loads(Path(path).read_text(),object_pairs_hook=pairs,
        parse_constant=lambda x:fail('nonfinite JSON'))
def stat_id(s):return tuple(getattr(s,'st_'+k) for k in ('dev','ino','mode','size','mtime_ns','ctime_ns','nlink'))
def pin(path):
    p=Path(path);require(p.is_file() and not p.is_symlink(),'regular source/output required')
    before=p.stat();b=p.read_bytes();require(stat_id(before)==stat_id(p.stat()),'file identity changed during pin')
    return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest())
def sha(s):
    require(type(s)is str and len(s)==64 and s!='0'*64 and all(c in '0123456789abcdef' for c in s),'unbound/nonzero SHA required')
    return s
def new_json(path,value):
    with Path(path).open('x') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

CFG=read(BASE/'Root_phase_config.json')
FORMAL_FACTORY=Path(CFG['factory']['path'])
def factory_source_descriptor():return dict(path=str(FORMAL_FACTORY),sha256=sha(CFG['factory']['sha256']))

# Exact original source body; only produces argv strings and never executes them.
def normal_factory_command(python,expression):
    # The factory is ordinarily imported, never installed under an invented file name.
    program=('import hashlib,sys,os; from pathlib import Path\n'
        'if sys.flags.optimize!=0 or \"PYTHONOPTIMIZE\" in os.environ: raise ValueError(\"nonoptimized cold source predicates required\")\n'
        'sys.dont_write_bytecode=True; '
        'p=Path('+repr(str(FORMAL_FACTORY))+'); assert hashlib.sha256(p.read_bytes()).hexdigest()=='+repr(factory_source_descriptor()['sha256'])+'; '
        'sys.path.insert(0,str(p.parent)); import '+Path(FORMAL_FACTORY).stem+' as f; '
        'assert Path(f.__file__).resolve()==p; '+expression)
    return [python,'-c',program]


def expected_commands(phase,values):
    python=CFG['python'];f=str(FORMAL_FACTORY);fsha=sha(CFG['factory']['sha256'])
    cli=[python,f,CFG['actions'][phase],'--factory-sha256',fsha]
    dt=values['declaration_terminal_sha256'];pr=values['prepared_sha256']
    if phase=='declaration':return cli,None
    dt=sha(dt)
    if phase=='prepare':
        d=sha(values['declaration_sha256']);cli+=['--sha256',d,'--declaration-terminal-sha256',dt]
        expression='c=f.normal_runtime_preload(f.SOURCE); r=c.prepare(f.SOURCE/"declaration.json",'+repr(d)+',f.OUTPUT); import json; print(json.dumps(r,sort_keys=True,allow_nan=False),flush=True)'
    elif phase=='binding':
        pr=sha(pr);cli+=['--sha256',pr,'--declaration-terminal-sha256',dt]
        expression='r=f.prepare_binding_in_clean_process('+repr(pr)+','+repr(dt)+'); import json; print(json.dumps(r,sort_keys=True,allow_nan=False),flush=True)'
    elif phase=='controls':
        b=sha(values['binding_sha256']);cli+=['--binding-sha256',b,'--declaration-terminal-sha256',dt]
        return cli,[python,CFG['work']+'/runtime/combined_cold_own_rss_controls.py','run-controls','--binding',CFG['work']+'/own_rss_binding.json','--binding-sha256',b]
    elif phase=='finalization':
        pr=sha(pr);b=sha(values['binding_sha256']);cs=sha(values['control_seal_sha256']);ct=sha(values['control_terminal_sha256'])
        cli+=['--sha256',pr,'--binding-sha256',b,'--control-seal-sha256',cs,'--control-terminal-sha256',ct,'--declaration-terminal-sha256',dt]
        expression='r=f.finalize_cold_in_clean_process('+','.join(repr(x) for x in (pr,b,cs,ct,dt))+'); import json; print(json.dumps(r,sort_keys=True,allow_nan=False),flush=True)'
    elif phase=='cold':
        pc=sha(values['prepared_cold_sha256']);cli+=['--sha256',pc,'--declaration-terminal-sha256',dt]
        expression='r=f.cold_launch_in_clean_process('+repr(pc)+','+repr(dt)+'); import json; print(json.dumps(r,sort_keys=True,allow_nan=False),flush=True)'
    else:fail('fixed phase required')
    return cli,normal_factory_command(python,expression)


def main():
    require(len(sys.argv)==2 and sys.argv[1] in CFG['observations'],'one reviewed fixed phase required')
    phase=sys.argv[1];obs=CFG['observations'][phase];actual=obs['actual_tool_result']
    require(type(actual)is dict and set(actual)=={'initial_chunk_id','session_id','terminal_chunk_id','exit_code'},'complete actual tool shape required')
    require(type(actual['exit_code'])is int and actual['exit_code']==0,'genuine builtin-int tool EXIT0 required')
    require(all(type(actual[k])is str and actual[k] for k in ('initial_chunk_id','terminal_chunk_id')),'genuine terminal chunks required')
    require(actual['session_id']is None or type(actual['session_id'])is int and actual['session_id']>0,'real optional session required')
    require(obs['actual_tool_terminal_return_observed']is True and obs['record_written_after_actual_terminal_return']is True and obs['tool_closed']is True,'Root actual closed terminal observed first')
    cli,handoff=expected_commands(phase,CFG['future_values'])
    require(obs['launch_command']==cli and obs['handoff_command']==handoff,'exact original CLI and actual execve argv required')
    require(pin(FORMAL_FACTORY)==factory_source_descriptor(),'known admitted canonical factory changed')
    work=Path(CFG['work']);terminal=Path(CFG['controlTerminal'] if phase=='controls' else CFG['terminal']);source=Path(CFG['source'])
    stdout=Path(obs['full_stdout_path']);stderr=Path(obs['full_stderr_path'])
    require(stdout!=stderr and stdout.is_absolute() and stderr.is_absolute(),'complete distinct Root stdout/stderr paths required')
    value=read(stdout);extra={};command=handoff if phase=='controls' else cli
    if phase=='declaration':
        d=pin(source/'declaration.json');seal=pin(source/'factory_seal.json');equiv=pin(source/'source_equivalence.json')
        require(value==dict(classification='DECLARED_COMBINED_PHYSICAL_DEDUP_FILE_SNAPSHOT_COLD_INPUT_ONLY',declaration=d,output=str(work),factory_seal=seal,source_equivalence=equiv),'entire declaration stdout differs')
        require(d['sha256']==sha(CFG['future_values']['declaration_sha256']),'actual declaration pin required')
        extra.update(declaration=d,factory_seal=seal,source_equivalence=equiv)
    elif phase=='prepare':
        p=pin(work/'prepared.json');d=read(p['path'])
        require(value==dict(classification='PREPARED_NO_TRANSPORT',prepared=p['path'],sha256=p['sha256']),'entire original prepare stdout differs')
        require(d['classification']=='PREPARED_NO_TRANSPORT' and 'own_child_supervision' not in d,'original INPUT-only prepared required')
        require(p['sha256']==sha(CFG['future_values']['prepared_sha256']),'real prepared pin required')
        extra['prepared']=p
    elif phase=='binding':
        b=pin(work/'own_rss_binding.json')
        require(value['classification']=='PREPARED_NEW_CANONICAL_BINDING_INPUT_ONLY_NO_FIXTURE_CREDIT' and value['new_binding_fixtures_executed']is False and value['scientific_qualification']is False and value['binding']==b,'entire actual binding stdout/pin required')
        require(b['sha256']==sha(CFG['future_values']['binding_sha256']),'real binding pin required')
        extra.update(binding=b,actual_stdout_result=value)
    elif phase=='controls':
        b=read(work/'own_rss_binding.json');result=value['result'];bd=pin(work/'own_rss_binding.json')
        require(result['classification']=='PASS_NEW_CANONICAL_OWN_RSS_BINDING_CONTROLS_ONLY' and result['binding']==bd and result['scientific_qualification']is False,'real controls result required')
        require(all(result[k]is True for k in ('positive_completed','actual_oversize_rejected','short_completed','own_children_no_longer_live')) and [x['mode'] for x in result['observations']]==['positive','oversize','short'],'three original actual controls required')
        require(command==[b['producer_environment']['executable'],b['controls_source']['path'],'run-controls','--binding',bd['path'],'--binding-sha256',bd['sha256']],'copied controls actual command differs')
        tail=('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')
        require(set(value)=={'result',*tail} and value['actual_tail_check']=='PASS' and 0<value['actual_elapsed_seconds']<120 and type(value['actual_archive_bytes'])is int and value['actual_archive_bytes']<64*2**20,'complete original controls tail required')
        require(pin(b['controls_source']['path'])==b['controls_source'] and b['controls_source']['sha256']==CFG['controls_source_sha256'],'reviewed copied controls source required')
        cs=pin(work/'binding_controls/seal.json');require(cs['sha256']==sha(CFG['future_values']['control_seal_sha256']),'actual control seal pin required')
        extra.update({k:value[k] for k in tail});extra.update(binding=bd,host=b['host'],control_seal=cs)
    elif phase=='finalization':
        p=pin(work/'prepared_cold.json');d=read(p['path']);old=read(work/'prepared.json');inverse=dict(d);supervision=inverse.pop('own_child_supervision',None)
        require(inverse==old and supervision is not None and d['classification']=='PREPARED_NO_TRANSPORT','only original own_child_supervision addition allowed')
        require(value==dict(classification='PREPARED_COLD_INPUT_AND_ACTUAL_NEW_BINDING_CONTROLS_ONLY',original_prepared=pin(work/'prepared.json'),prepared=p,scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False),'entire actual finalization stdout differs')
        require(p['sha256']==sha(CFG['future_values']['prepared_cold_sha256']),'actual prepared_cold pin required')
        extra.update(prepared_cold=p,actual_stdout_result=value)
    else:
        p=pin(work/'prepared_cold.json');require(p['sha256']==sha(CFG['future_values']['prepared_cold_sha256']),'actual cold prepared pin required')
        require(value['original_controller_return']==read(work/'AAA/run_status.json') and value['original_controller_return']['classification']=='WAITING_REFERENCE' and value['original_controller_return']['cases']['AAA']['classification']=='VALID_MET','actual cold controller stdout/status required')
        require(all(value[k]is False for k in ('scientific_qualification','AAA_accuracy_qualified','ABA_admitted')),'cold/input execution never certifies reference accuracy')
        tail=('full_closeout_tail_gate','actual_elapsed_seconds','actual_archive_bytes','actual_resources');r=value['actual_resources']
        require(value['full_closeout_tail_gate']=='PASS' and 0<value['actual_elapsed_seconds']<43200 and type(value['actual_archive_bytes'])is int and value['actual_archive_bytes']>0,'actual complete cold tails required')
        require(r['artifact_budget_bytes']==96*2**30 and r['min_free_bytes']==8*2**30 and r['artifact_bytes']<=96*2**30 and r['disk_free_bytes']>=8*2**30 and r['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and 'reason' not in r,'original cold resource tail required')
        seal=pin(work/'cold_closeout_seal.json');require(not (work/'cold_source_failure.json').exists(),'no success receipt for actual cold failure')
        extra.update({k:value[k] for k in tail});extra.update(prepared=p,cold_closeout_seal=seal,AAA_accuracy_qualified=False,ABA_admitted=False)
    # All checks precede new terminal writes. Controls/declaration get a fresh
    # independent root; later phase receipts reuse the admitted declaration root.
    if phase in ('declaration','controls'):terminal.mkdir(exist_ok=False)
    require(terminal.is_dir() and not terminal.is_symlink(),'independent terminal directory required')
    target=terminal/('declaration_terminal_return.json' if phase=='declaration' else 'terminal_return.json' if phase in ('controls','cold') else phase+'_terminal_return.json')
    require(not os.path.lexists(target),'one actual receipt, no overwrite')
    saved=[]
    for p in (stdout,stderr):
        q=terminal/(phase+('.stdout' if p==stdout else '.stderr'))
        with q.open('xb') as f:f.write(p.read_bytes())
        saved.append(pin(q))
    schema=CFG['declaration_schema'] if phase=='declaration' else CFG['cold_schema'] if phase=='cold' else 'AXMAT_COMBINED_PHYSICAL_MEMORY_CANONICAL_GUARD_ACTUAL_TERMINAL_V1' if phase=='controls' else 'AXMAT_ROOT_ACTUAL_COLD_'+phase.upper()+'_RETURN_V1'
    recorded_source=dict(path=CFG['work']+'/runtime/combined_cold_own_rss_controls.py',sha256=CFG['controls_source_sha256']) if phase=='controls' else factory_source_descriptor()
    record=dict(schema=schema,record_producer='root',actual_tool_terminal_return_observed=True,record_written_after_actual_terminal_return=True,actual_tool_result=actual,returncode=actual['exit_code'],command=command,source=recorded_source,full_stdout=saved[0],full_stderr=saved[1],scientific_qualification=False,transport_started=(phase=='cold'),observed_unix=time.time(),**extra)
    if phase!='declaration':record['input_declaration_terminal_evidence']=pin(Path(CFG['terminal'])/'declaration_terminal_return.json')
    if phase=='cold':record['handoff_command']=handoff
    new_json(target,record)
    print(json.dumps(dict(root_receipt=pin(target),**extra),allow_nan=False))

if __name__=='__main__':main()
