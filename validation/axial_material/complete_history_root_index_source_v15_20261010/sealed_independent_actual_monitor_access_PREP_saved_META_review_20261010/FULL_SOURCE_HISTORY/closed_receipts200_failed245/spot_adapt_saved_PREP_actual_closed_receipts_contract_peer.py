"""Source-only strict contract alignment with actual Root closed receipts."""
import ast,hashlib,json,os,stat
from pathlib import Path
OLD=Path('/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_ACTUAL_RECEIPT_ROUTE_UNREADY_20261010')
NEW=Path('/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_ACTUAL_CLOSED_RECEIPTS_SOURCE_UNREADY_20261010')
ADD='''def actual_closed_PREP_observations(doc,closed_result):
    need(doc['closed_session_not_repolled'] is True and doc['actual_tool_return_not_synthetic'] is True,'actual Root closed PREP no repoll and no synthetic tool return')
    events=doc['all_actual_tool_observations'];initial=doc['initial_tool_return']
    need(type(events) is list and len(events)>=2 and exact(events[0],initial) and exact(events[-1],closed_result),'all actual Root PREP observations bounded by exact first and final tool returns')
    sid=initial['session_id']
    need(type(sid) is int and sid>0 and initial['chunk_id']==doc['actual_initial_chunk'] and closed_result['chunk_id']==doc['actual_terminal_chunk'],'actual Root unique positive session and exact terminal chunks')
    for event in events[:-1]:need(type(event) is dict and event.get('session_id')==sid and type(event.get('session_id')) is int and 'exit_code' not in event,'every earlier genuine PREP observation is still live, no closed repoll')
    host_text,host_tree=source(D/'combined_prepare_host.py')
    guard="if len(sys.argv)!=1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:"
    need(host_text.count(guard)==1 and "raise ValueError('fixed unprofiled nonoptimized read-only admission host required')" in host_text,'byte-exact admitted host explicitly rejects optimized profiled invocation before actual PREP')


def actual_postclose_writer_terminal(doc,wanted):
    need(doc['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREP_METADATA_POSTCLOSE_WRITER_TOOL_RETURN_V1' and doc['closed'] is True and doc['record_written_after_true_closed_PREP'] is True and doc['Source_frozen_before_actual_PREP'] is True and doc['new_build_whole_INPUT_native_or_science_qualification_created'] is False,'actual metadata postclose writer schema Source freeze and no business credit')
    need(set(k for k in ('terminal_tool_return','actual_tool_return','exec_command_result') if k in doc)=={'terminal_tool_return','actual_tool_return'} and exact(doc['terminal_tool_return'],doc['actual_tool_return']),'actual writer exactly two tool aliases have same type order and float bits')
    selected={k:v for k,v in doc.items() if k!='actual_tool_return'}
    return terminal(selected,'Root actual frozen metadata writer',wanted)


'''
def ids(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ids(p);assert stat.S_ISREG(i[2]) and i[3]==1
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ids(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def segment(s,n):return ''.join(s.splitlines(keepends=True)[n.lineno-1:n.end_lineno])
def write(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
p=OLD/'review_actual_complete_PREP_saved_META_stdlib.py';op=pin(p);assert op['sha256']=='705cb4fdbb0362aafdf5d6caf350072e1f5e81fece0e328e2e0bdf3e6bcc11a6'
old=p.read_text();anchor='def terminal(doc,label,wanted=None):';assert old.count(anchor)==1
changes=[
 ("    need(trdoc['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREP_TOOL_TERMINAL_RETURN_V1' and trdoc['observed_terminal'] is True and trdoc['session_repolled_after_close'] is False,'true complete PREP receipt and no repoll')\n", "    need(trdoc['schema']=='ROOT_V25_ACTUAL_COMPLETE_PREP_TOOL_TERMINAL_RETURN_V1' and trdoc['observed_terminal'] is True and trdoc['closed_session_not_repolled'] is True,'true complete PREP receipt and no repoll')\n    actual_closed_PREP_observations(trdoc,rt)\n"),
 ("    wrdoc=meta(given['actual_PREP_metadata_writer_terminal_pin']['path']);wt=terminal(wrdoc,'Root actual frozen metadata writer',inputs['actual_terminal_chunks']['metadata_writer'])\n    need(wrdoc['metadata_only'] is True,'metadatawriter has no new native or science execution')\n", "    wrdoc=meta(given['actual_PREP_metadata_writer_terminal_pin']['path']);wt=actual_postclose_writer_terminal(wrdoc,inputs['actual_terminal_chunks']['metadata_writer'])\n"),
 ("    expected_cmd='env -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1", "    expected_cmd='env OMP_NUM_THREADS=1")]
new=old.replace(anchor,ADD+anchor,1)
for a,b in changes:assert new.count(a)==1;new=new.replace(a,b,1)
nt=ast.parse(new);ot=ast.parse(old);restored=new
for a,b in reversed(changes):assert restored.count(b)==1;restored=restored.replace(b,a,1)
assert restored.count(ADD)==1;restored=restored.replace(ADD,'',1)
assert restored==old and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ot,include_attributes=False)
od={n.name:n for n in ot.body if isinstance(n,ast.FunctionDef)};nd={n.name:n for n in nt.body if isinstance(n,ast.FunctionDef)}
assert len(od)==22 and set(nd)==set(od)|{'actual_closed_PREP_observations','actual_postclose_writer_terminal'}
assert all(segment(new,nd[k])==segment(old,v) for k,v in od.items() if k!='review')
assert all(ast.dump(n,include_attributes=False)==ast.dump(m,include_attributes=False) for n,m in zip([x for x in ot.body if not isinstance(x,ast.FunctionDef)],[x for x in nt.body if not isinstance(x,ast.FunctionDef)]))
at=ast.parse(ADD);assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('exec','eval','compile','__import__') for n in ast.walk(at))
assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('run','Popen','exec_module','unlink','rename','write_text','write_bytes') for n in ast.walk(at))
assert not os.path.lexists(NEW);NEW.mkdir();out=NEW/p.name;out.write_text(new)
(NEW/('original_'+p.name)).write_bytes(p.read_bytes());assert pin(p)==op
for n in ('ACTUAL_PREP_REVIEW_INPUTS.UNREADY.json','seal_actual_complete_PREP_saved_META_review_stdlib.py','COMPLETE_HISTORICAL_TRANSFER_CURRENT_RETENTION_SOURCE_INVERSE.json','SOURCE_ONLY_SEVEN_DIRECTORY_INVERSE.json','ACTUAL_WRITER_RECEIPT_BASENAME_SOURCE_INVERSE.json'):
 q=OLD/n;qp=pin(q);(NEW/n).write_bytes(q.read_bytes());assert pin(q)==qp
(NEW/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
checks=[dict(check=k,passed=True) for k in ('complete_original705_full_Source_EOF_unchanged','exact_three_saved_receipt_contract_blocks_only','two_new_readonly_stdlib_Metadata_Source_validators','all21_other_original_functions_full_byte_unchanged','all_original_globals_thresholds_physics_caps_MRO_Q_helper_andcredit_logic_unchanged','whole_byte_and_AST_inverse705','actual_saved_reviewer_not_executed_by_Source_author')]
v=dict(schema='INDEPENDENT_V25_SAVED_PREP_ACTUAL_CLOSED_ROOT_RECEIPTS_SOURCE_CONTRACT_INVERSE_V1',status='SOURCE_ONLY_ACTUAL_RECEIPTS_CONTRACT_READY_SAVED_REVIEW_NOT_EXECUTED',source_only=True,all_checks_typed_true=True,check_count=len(checks),checks=checks,blockers=[],original_reviewer_pin=op,derived_reviewer_pin=pin(out),full_original_copy_pin=pin(NEW/('original_'+p.name)),complete_byte_inverse=True,complete_AST_inverse=True,added_full_readonly_Source=ADD,exact_finite_replacements=[dict(old=a,new=b,count=1) for a,b in changes],candidate_helper_API_compiler_native_material_numeric_or_saved_PREP_reviewer_executed=False,actual_saved_PREP_review_terminal=None,actual_saved_PREP_PASS_report=None,whole_INPUT_BUILD_native_RSS_physics_AAA_ABA_qualified=False)
write(NEW/'ACTUAL_CLOSED_RECEIPTS_COMPLETE_SOURCE_CONTRACT_INVERSE.json',v)
print(json.dumps(dict(source_only=True,reviewer_pin=pin(out),inverse_pin=pin(NEW/'ACTUAL_CLOSED_RECEIPTS_COMPLETE_SOURCE_CONTRACT_INVERSE.json'),check_count=len(checks),all_checks_typed_true=True,saved_PREP_reviewer_executed=False)))
