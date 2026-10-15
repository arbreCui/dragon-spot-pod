"""Seal only existing source artifacts and observed own source tool terminals."""
import ast
import hashlib
import json
from pathlib import Path
BASE=Path(__file__).parent
TRACE=Path('/private/tmp/axmat_v15_complete_wire_and_trace_table_source_only_20261010')
COLD=Path('/private/tmp/axmat_v15_whole_input_cold_unready_source_candidates_20261010')
A=Path('/Users/wen/spot/validation/axial_material')
P=A/'combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
    s=p.lstat();return dict(dev=s.st_dev,ino=s.st_ino,mode=s.st_mode,nlink=s.st_nlink,size_bytes=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
def pin(p):
    x=ident(p);b=p.read_bytes();y=ident(p);assert x==y
    return dict(path=str(p),sha256=sha(b),size_bytes=len(b),identity=x)
def doc(p,v):
    with p.open('x')as f:json.dump(v,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
def funcs(text):
    ls=text.splitlines(keepends=True)
    return {n.name:''.join(ls[n.lineno-1:n.end_lineno])for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def terminal(path,initial,session,last,stdout,stderr):
    assert Path(stderr).stat().st_size==0
    v=dict(schema='AXMAT_ACTUAL_SOURCE_ONLY_TOOL_TERMINAL_RETURN_V1',record_producer='source_author',
           actual_tool_terminal_return_observed=True,actual_tool_closed=True,
           actual_tool_result=dict(initial_chunk_id=initial,session_id=session,terminal_chunk_id=last,exit_code=0),
           full_stdout=pin(Path(stdout)),full_stderr=pin(Path(stderr)),scope='SOURCE_AND_COMPILE_SOURCE_ONLY_NO_PROJECT_EXECUTION',
           business_or_fixture_or_native_execution=False)
    doc(path,v);return pin(path)
memreceipt=terminal(BASE/'actual_source_tool_return.json','773318',None,'773318',BASE/'generate.stdout',BASE/'generate.stderr')
tracereceipt=terminal(TRACE/'actual_trace_source_tool_return.json','c1dd28',None,'c1dd28',BASE/'generate_trace.stdout',BASE/'generate_trace.stderr')
refine_receipt=terminal(TRACE/'actual_nested_guard_source_tool_return.json','2bdea1',None,'2bdea1',TRACE/'refine.stdout',TRACE/'refine.stderr')
coldreceipt=terminal(COLD/'actual_final_source_tool_return.json','25314b',78606,'76b5d1',COLD/'generate.stdout',COLD/'generate.stderr')

parent=P.read_text();final=TRACE/'complete_input_graph_fresh_wire_canonical_and_trace_tables.CANDIDATE.py'
text=final.read_text()
old='    if type(result) is dict and result.get("schema") == CANONICAL_FILE_TABLE_STORAGE_SCHEMA:\n        return decode_canonical_file_table_storage(result, _consume=True)\n    return result'
new='    if type(result) is dict and result.get("schema") == CANONICAL_FILE_TABLE_STORAGE_SCHEMA:\n        return decode_canonical_file_table_storage(result, _consume=True)\n    if type(result) is dict and result.get("schema") == COMPLETE_GRAPH_TRACE_TABLE_STORAGE_SCHEMA:\n        return decode_complete_graph_table_storage(result, _consume=True)\n    return result'
assert text.count(new)==2
back=text.replace(new,old)
assert back.startswith(parent)
append=back[len(parent):]
assert back[:-len(append)]==parent
pf=funcs(parent);ff=funcs(text)
for name,body in pf.items():
    if name not in {'strict_json','_parse_strict_json_payload'}:assert ff[name]==body
    else:assert ff[name].replace(new,old)==body
compile(text,str(final),'exec')
proof=dict(schema='AXMAT_COMPLETE_FRESH_WIRE_TRACE_TABLE_FINAL_INVERSE_V1',status='UNREADY_SOURCE_ONLY',
    parent=pin(P),candidate=pin(final),parent_functions_and_classes=len(pf),
    original_functions_and_classes_exact_except_two_parser_routes=len(pf)-2,
    full_source_inverse_equal=True,regions=[dict(kind='two_exact_parser_wrapper_routes',old=old,new=new,occurrences=2),
        dict(kind='append_only_complete_fresh_producer_and_trace_codec',old='',new=append)],
    syntax_compile_without_exec=True,original_limits_public_graphs_math_verify_phase_resources_unchanged=True)
doc(TRACE/'FINAL_complete_source_inverse_proof.json',proof)
prior=json.loads((TRACE/'REPORT.json').read_text())
prior['helper']=pin(final)
prior['final_source_inverse_proof']=pin(TRACE/'FINAL_complete_source_inverse_proof.json')
prior['actual_source_receipts']=[tracereceipt,refine_receipt]
prior['source_refinement']=pin(TRACE/'nested_json_cycle_source_refinement.json')
prior['current_qualification']='UNREADY_SOURCE_ONLY_REQUIRES_ROOT_BOUNDED_PURE_CODEC_PROTOCOL'
doc(TRACE/'FINAL_REPORT.json',prior)

for directory in (BASE,TRACE,COLD):
    rows=[pin(p)for p in sorted(directory.iterdir())if p.is_file() and p.name not in ('sealed_manifest.json',)]
    doc(directory/'sealed_manifest.json',dict(schema='AXMAT_SOURCE_ONLY_SMALL_EVIDENCE_MANIFEST_V1',
        status='SOURCE_ONLY_UNREADY',files=rows,project_written=False,source_functions_executed=False))
print(json.dumps(dict(status='SOURCE_ONLY_UNREADY',cold_report=pin(COLD/'REPORT.json'),cold_receipt=coldreceipt,
    cold_manifest=pin(COLD/'sealed_manifest.json'),memory_report=pin(BASE/'REPORT.json'),memory_receipt=memreceipt,
    final_trace_source=pin(final),final_trace_report=pin(TRACE/'FINAL_REPORT.json'),
    trace_manifest=pin(TRACE/'sealed_manifest.json')),separators=(',',':')))
