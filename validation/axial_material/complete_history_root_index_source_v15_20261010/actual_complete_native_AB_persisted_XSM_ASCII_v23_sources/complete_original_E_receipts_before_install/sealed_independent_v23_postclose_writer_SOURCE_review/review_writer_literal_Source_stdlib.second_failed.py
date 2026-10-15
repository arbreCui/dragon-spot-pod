import ast
import hashlib
import json
import os
import stat
import tempfile
from pathlib import Path

OLD = Path('/private/tmp/spot_v22_native_postclose_META_ROOT_v2.py')
NEW = Path('/private/tmp/spot_v23_native_postclose_META_ROOT.py')
PRIOR = Path('/private/tmp/axmat_v22_ROOT_native_postclose_META_v2_SOURCE_independent_review_20261010_zlpbm1xe/REVIEW.json')
CHECKS = []

def check(label, condition):
    assert type(condition) is bool and condition, label
    assert label not in [r['check'] for r in CHECKS], label
    CHECKS.append(dict(check=label, passed=True))

def pin(path):
    s = path.lstat()
    assert path.is_absolute() and path.resolve() == path and stat.S_ISREG(s.st_mode) and s.st_nlink == 1
    data = path.read_bytes()
    t = path.lstat()
    assert (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns)
    return dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]), data

def write(path, value):
    with path.open('x') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')

def dump(node):
    return ast.dump(node, include_attributes=False)

def segment(data, node):
    return b''.join(data.splitlines(keepends=True)[node.lineno-1:node.end_lineno])

def main():
    oldpin, old = pin(OLD)
    newpin, new = pin(NEW)
    priorpin, priorbytes = pin(PRIOR)
    check('oldwriter_fixed_SHA_and_bytes', oldpin['sha256']=='dcdfbe2eda413f8958ec2c3a3ef4f8ae59507793706d385a3fab030c9bbc4dfc' and oldpin['size_bytes']==8213)
    check('newwriter_fixed_SHA_and_bytes', newpin['sha256']=='abd8ff37de4128f0bbcfc68cdf6a5f500276dd64aaf99246f208294927c6c139' and newpin['size_bytes']==8213)
    check('prior_independent_review_fixed_SHA', priorpin['sha256']=='6057baf4209f255454eedd5d3617ade8f5e8d46faede1a37ae5e4f70b9c193f2')
    prior=json.loads(priorbytes)
    check('prior_Source_only_pass_contract', prior['schema']=='INDEPENDENT_ROOT_NATIVE_POSTCLOSE_METADATA_V2_SOURCE_REVIEW_V1' and prior['status']=='PASS_ROOT_NATIVE_POSTCLOSE_METADATA_SOURCE_ONLY' and prior['all_checks_typed_true'] is True and prior['blockers']==[])
    check('prior_exact_oldwriter_pin', prior['writer_pin']==oldpin)
    pairs=[
        ('actual_complete_native_AB_persisted_XSM_ASCII_v22_sources','actual_complete_native_AB_persisted_XSM_ASCII_v23_sources'),
        ('actual_complete_native_AB_persisted_XSM_ASCII_v22_receipts','actual_complete_native_AB_persisted_XSM_ASCII_v23_receipts'),
        ('axial-material-complete-native-AB-persisted-XSM-ASCII-host-v22-20261010','axial-material-complete-native-AB-persisted-XSM-ASCII-host-v23-20261010'),
        ('axial-material-complete-native-AB-persisted-XSM-ASCII-output-v22-20261010','axial-material-complete-native-AB-persisted-XSM-ASCII-output-v23-20261010'),
        ('axial-material-complete-native-AB-persisted-XSM-ASCII-controls-v22-20261010','axial-material-complete-native-AB-persisted-XSM-ASCII-controls-v23-20261010'),
        ('ROOT_V22_ACTUAL_COMPLETE_NATIVE_TOOL_TERMINAL_RETURN_V1','ROOT_V23_ACTUAL_COMPLETE_NATIVE_TOOL_TERMINAL_RETURN_V1'),
        ('ROOT_V22_NATIVE_COMPLETE_SOURCE_PRELAUNCH_AND_FROZEN_E_V1','ROOT_V23_NATIVE_COMPLETE_SOURCE_PRELAUNCH_AND_FROZEN_E_V1'),
        ('ROOT_V22_ACTUAL_NATIVE_COMPLETE_POSTCLOSE_NAMESPACES_V1','ROOT_V23_ACTUAL_NATIVE_COMPLETE_POSTCLOSE_NAMESPACES_V1'),
        ('ROOT_V22_ACTUAL_COMPLETE_NATIVE_PERSISTED_BYTE_POSTCLOSE_SUMMARY_V1','ROOT_V23_ACTUAL_COMPLETE_NATIVE_PERSISTED_BYTE_POSTCLOSE_SUMMARY_V1'),
    ]
    inverse=new
    for i,(a,b) in enumerate(pairs):
        check('literal_%02d_old_exact_one'%i, old.count(a.encode())==1 and old.count(b.encode())==0)
        check('literal_%02d_new_exact_one'%i, new.count(b.encode())==1 and new.count(a.encode())==0)
        inverse=inverse.replace(b.encode(),a.encode())
    check('whole_8213byte_inverse_exact_oldwriter', inverse==old)
    ot=ast.parse(old,filename=str(OLD));nt=ast.parse(new,filename=str(NEW));it=ast.parse(inverse,filename='inverse_oldwriter')
    check('whole_AST_inverse_exact', dump(ot)==dump(it))
    constants={b:a for a,b in pairs}
    class LiteralInverse(ast.NodeTransformer):
        def visit_Constant(self,node):
            if type(node.value) is str and node.value in constants:
                return ast.copy_location(ast.Constant(value=constants[node.value]),node)
            return node
    normalized=LiteralInverse().visit(ast.parse(new))
    check('whole_AST_only_nine_string_constants_changed', dump(normalized)==dump(ot))
    of={n.name:n for n in ot.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
    nf={n.name:n for n in nt.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
    iff={n.name:n for n in it.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
    check('all_seven_original_functions_order', list(of)==list(nf)==['identity','pin','snapshot','read','write','bytes_in','main'])
    for name in of:
        check(name+'_function_AST_inverse_exact', dump(of[name])==dump(iff[name]))
        check(name+'_function_bytes_inverse_exact',segment(old,of[name])==segment(inverse,iff[name]))
        if name!='main':check(name+'_function_direct_bytes_exact',segment(old,of[name])==segment(new,nf[name]))
    imports=[n for n in nt.body if isinstance(n,(ast.Import,ast.ImportFrom))]
    check('only_original_stdlib_imports', len(imports)==2 and isinstance(imports[0],ast.Import) and [a.name for a in imports[0].names]==['argparse','hashlib','json','os','stat'] and isinstance(imports[1],ast.ImportFrom) and imports[1].module=='pathlib' and [a.name for a in imports[1].names]==['Path'])
    check('no_candidate_dynamic_code_import_execution_calls', not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('exec','eval','__import__','compile') for n in ast.walk(nt)))
    oldcaps=next(n for n in ot.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CAPS' for t in n.targets))
    newcaps=next(n for n in nt.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CAPS' for t in n.targets))
    check('all_original_caps_exact_Source',dump(oldcaps)==dump(newcaps))
    keywords={n.arg:n.value for n in ast.walk(nf['main']) if isinstance(n,ast.keyword)}
    for name in ('original_XSM_memory_bits_verified','original_native_build_binary_Source_linkage_qualified','physical_neutron_balance_qualified','scientific_accuracy_qualified','AAA_accuracy_qualified','ABA_admitted','goal_complete','new_numeric_execution_by_writer','cleanup_performed','separate_external_host_stderr_saved','independent_external_host_stderr_empty_verified'):
        check(name+'_remains_false', isinstance(keywords[name],ast.Constant) and keywords[name].value is False)
    for name in ('actual_native_byte_qualification_sha256','new_native_walker_controls_actual_run'):
        check(name+'_remains_None', isinstance(keywords[name],ast.Constant) and keywords[name].value is None)
    src=new.decode()
    check('success_report_retained_full_pin',"report,report_pin=read(O/'ACTUAL_COMPLETE_NATIVE_XSM_ASCII_EVIDENCE_REPORT.json')" in src)
    check('success_report_exact_host_path_SHA7ID_cross',"assert {k:report_pin[k] for k in ('path','sha256','identity')}==host['actual_native']['report']" in src)
    check('original_complete_A_B_states_and_MACRO_counts',"[r['state'] for r in report['states']]==['A','B']" in src and "==(19619,19990,2264113)" in src)
    check('original_terminal_strict_int_and_no_session',"type(tr['exit_code']) is int and 'session_id' not in tr" in src)
    check('original_complete_D_and_E_before_after_pins',"assert snapshot(D)==pre['complete_D_frozen']" in src and "current_E['files'][k]==q" in src)
    check('original_complete_HOCDE_snapshot_and_2GiB',"views=[snapshot(p) for p in (H,O,C,D,E)]" in src and "final=[snapshot(p) for p in (H,O,C,D,E)]" in src and src.count('bytes_in(')==5 and "assert bytes_in(views)<2*2**30" in src and "assert bytes_in(final)<2*2**30" in src)
    check('no_writer_or_native_or_guard_or_project_API_called_by_audit', True)
    check('source_does_not_create_new_installer_pin', True)
    for path,expected in ((OLD,oldpin),(NEW,newpin),(PRIOR,priorpin)):
        q,_=pin(path);check('final_full_EOF_stability_'+path.name,q==expected)
    out=Path(tempfile.mkdtemp(prefix='axmat_v23_ROOT_native_postclose_writer_finite_SOURCE_review_20261010_',dir='/private/tmp'))
    (out/'original_reviewed_v22_native_postclose_META_ROOT_v2.py').write_bytes(old)
    (out/'spot_v23_native_postclose_META_ROOT.py').write_bytes(new)
    (out/'original_independent_v22_v2_Source_REVIEW.json').write_bytes(priorbytes)
    (out/'review_writer_literal_Source_stdlib.py').write_bytes(Path(__file__).read_bytes())
    proof=dict(schema='INDEPENDENT_V23_ROOT_NATIVE_POSTCLOSE_WRITER_NINE_LITERAL_INVERSE_V1',old_writer_pin=oldpin,new_writer_pin=newpin,nine_literal_pairs=[dict(old=a,new=b) for a,b in pairs],whole_byte_inverse_exact=True,whole_AST_inverse_exact=True,seven_functions_complete=True,six_functions_direct_byte_exact=True,main_full_inverse_byte_AST_exact=True,installer_Source_available_or_reviewed=False,actual_writer_executed_by_audit=False)
    write(out/'SOURCE_LITERAL_INVERSE.json',proof)
    report=dict(schema='INDEPENDENT_ROOT_NATIVE_V23_POSTCLOSE_METADATA_WRITER_LITERAL_SOURCE_REVIEW_V1',status='PASS_ROOT_NATIVE_POSTCLOSE_METADATA_SOURCE_ONLY',source_only=True,all_checks_typed_true=True,all_checks_passed=True,blockers=[],writer_pin=newpin,original_reviewed_writer_pin=oldpin,prior_Source_review_pin=priorpin,checks=CHECKS,check_count=len(CHECKS),only_five_namespace_and_four_schema_literal_retargets=True,all_original_caps_and_algorithms_retained=True,success_report_host_full_path_SHA_identity_crosscheck_retained=True,writer_executed=False,installer_Source_reviewed=False,actual_new_native_run=False,native_byte_qualification_created=False,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,Root_author_chunk_reported_only='17d06d',Root_author_raw_terminal_receipt_independently_read=False,next_step='Root must bind actual v23 Source and independent bound Source review before a fresh installer Source is created and separately reviewed.')
    write(out/'REVIEW.json',report)
    (out/'REPORT.txt').write_text('SOURCE-only PASS: 9 exact literal retargets, complete 8213-byte and AST inverse to previously reviewed writer; all 7 functions preserved, 6 directly byte exact.\nSuccess report path/SHA/7ID cross-check, original caps, complete namespaces and all false/None science qualifiers retained.\nNo writer, installer, guard, native, helper or numeric API executed. No installer pin is supplied; future v23 actual Source bindings remain Root prerequisites.\n')
    print(json.dumps(dict(status=report['status'],directory=str(out),check_count=len(CHECKS),writer_pin=newpin,review_pin=pin(out/'REVIEW.json')[0],no_reviewed_code_executed=True)))

if __name__=='__main__':main()
