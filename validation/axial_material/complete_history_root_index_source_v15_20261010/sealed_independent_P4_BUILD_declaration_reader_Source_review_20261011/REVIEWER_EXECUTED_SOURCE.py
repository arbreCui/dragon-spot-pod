"""Independent finite Source review of the single BUILD declaration-META reader.
No candidate/utility imports, function execution, API, physical payload or business.
The previously independently reviewed P4 namespace and V3 memory semantics are
explicit prerequisites; this review checks the one-function delta and complete
byte/AST preservation and actual consumed inverse, not a new memory qualification.
"""
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import sys
import tempfile

P=Path('/private/tmp/axmat_P4_BUILD_exact_declaration_reader_minimal_UNREADY_Source_66od7kgz')
EXPECTED='cedc1311c69b4e09d589a145a0757288658585c8939186a5cfc29fa682b506fe'
MAX=16*2**20
CHECKS=[]
BLOCKERS=[]
INPUT_PINS={}

def check(name,value,evidence=None):
    assert type(value)is bool and name not in {c['check']for c in CHECKS}
    c=dict(check=name,passed=value)
    if evidence is not None:c['evidence']=evidence
    CHECKS.append(c)
    if not value:BLOCKERS.append(dict(check=name,reason=evidence))
    return value
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def identity(p):return ids(Path(p).lstat())
def read(p):
    p=Path(p);before=identity(p)
    assert p.is_absolute()and p.resolve()==p and stat.S_ISREG(before[2])and before[3]==1 and 0<=before[4]<=MAX
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        assert ids(os.fstat(fd))==before
        remaining=MAX+1;parts=[]
        while remaining:
            b=os.read(fd,min(65536,remaining))
            if not b:break
            parts.append(b);remaining-=len(b)
        b=b''.join(parts)
        assert len(b)<=MAX and len(b)==before[4]and ids(os.fstat(fd))==before and identity(p)==before
    finally:os.close(fd)
    q=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=before)
    if str(p)in INPUT_PINS:assert INPUT_PINS[str(p)]==q
    INPUT_PINS[str(p)]=q
    return b,q
def strict(b):
    def pairs(rows):
        d={}
        for k,v in rows:
            if k in d:raise ValueError('duplicate key')
            d[k]=v
        return d
    def reject(v):raise ValueError('nonfinite '+v)
    d=json.loads(b.decode('utf8'),object_pairs_hook=pairs,parse_constant=reject)
    def finite(v):
        if type(v)is float:assert math.isfinite(v)
        elif type(v)is dict:
            for x in v.values():finite(x)
        elif type(v)is list:
            for x in v:finite(x)
    finite(d);return d
def jsonread(p):
    b,q=read(p);return strict(b),q
def exact(q):
    b,pin=read(q['path']);assert pin==q;return b
def dump_ast(text):return ast.dump(ast.parse(text),include_attributes=False)
def defs(text):
    t=ast.parse(text)
    return [(n.name,ast.get_source_segment(text,n),ast.dump(n,include_attributes=False))for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
def function(text,name):
    nodes=[n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)and n.name==name]
    assert len(nodes)==1;return ast.get_source_segment(text,nodes[0])
def inverse(text,rows):
    counts=[]
    for row in reversed(rows):
        assert set(row)=={'label','old','new','count'}and type(row['count'])is int and row['count']>0
        n=text.count(row['new']);counts.append(dict(label=row['label'],actual=n,expected=row['count']))
        if n!=row['count']:raise ValueError('actual consumed inverse count '+row['label'])
        text=text.replace(row['new'],row['old'])
    return text,counts
def complete_view(root):
    files={};directories={'.':identity(root)};asts={};raw={}
    for f in sorted(root.rglob('*')):
        i=identity(f);rel=str(f.relative_to(root));assert not stat.S_ISLNK(i[2])
        if stat.S_ISDIR(i[2]):directories[rel]=i
        else:
            b,q=read(f);files[rel]=q;raw[rel]=b
            if rel.endswith('.py'):asts[rel]=hashlib.sha256(dump_ast(b).encode()).hexdigest()
    for rel,i in directories.items():assert identity(root/rel)==i
    return dict(root=str(root),files=files,directories=directories,symlinks={},complete_python_AST_SHA256=asts),raw
def write(p,b):
    fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    try:
        off=0
        while off<len(b):
            n=os.write(fd,b[off:]);assert n>0;off+=n
        os.fsync(fd)
    finally:os.close(fd)
def write_json(p,d):write(p,(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def closed(d,code=0):
    t=d.get('terminal_tool_return',d.get('actual_tool_return',d.get('exec_command_result')))
    return d.get('closed')is True and d.get('observed_terminal')is True and type(t)is dict and type(t.get('exit_code'))is int and t['exit_code']==code and 'session_id'not in t and d.get('session_repolled_after_close',False)is False

def review():
    root=Path(tempfile.mkdtemp(prefix='axmat_P4_BUILD_DECLARATION_READER_INDEPENDENT_',dir='/private/tmp'))
    source,sourcepin=read(Path(__file__));write(root/'REVIEWER_EXECUTED_SOURCE.py',source)
    results={};v={};mf=None;roles={};utilities={}
    try:
        m,mf=jsonread(P/'MANIFEST.json');v,raw=complete_view(P)
        check('current_manifest_actual_expected_full_EOF_SHA',mf['sha256']==EXPECTED,mf)
        check('complete_current_member_domain',set(v['files'])==set(m['members'])|{'MANIFEST.json'})
        check('complete_current_directory7IDs',v['directories']==m['directories']and len(v['directories'])==10)
        check('exact_dynamic_file_and_AST_counts',type(m['member_count'])is int and m['member_count']==106 and len(v['files'])==107 and len(v['complete_python_AST_SHA256'])==60)
        check('manifest_source_only_true_and_no_execution',m['source_only']is True and m['candidate_or_business_executed']is False)
        for rel,q in m['members'].items():check('full_EOF_SHA_same7ID_member:'+rel,v['files'][rel]==q,q)
        check('exact_total_member_bytes',type(m['total_member_bytes'])is int and m['total_member_bytes']==sum(q['size_bytes']for rel,q in v['files'].items()if rel!='MANIFEST.json'))
        proof=strict(raw['COMPLETE_SOURCE_INVERSES.json']);whole=strict(raw['COMPLETE_P4_DECLARATION_READER_SINGLE_FUNCTION_14_ROLE_BYTE_AST_INVERSES.json']);capture=strict(raw['CAPTURE_NAMESPACE_COMPLETE_14_ROLE_BYTE_AST_AND_JSON_INVERSES.json'])
        check('current_actual_consumed_proof_expected_SHA',v['files']['COMPLETE_SOURCE_INVERSES.json']['sha256']=='8522e90ddd18d625fa3aaa9d26f15930fec27a5dc4aa85bc72927db63690d10c')
        check('current_whole14_inverse_expected_SHA',v['files']['COMPLETE_P4_DECLARATION_READER_SINGLE_FUNCTION_14_ROLE_BYTE_AST_INVERSES.json']['sha256']=='02626b9880f61f55b96f44d6b60a6b76fcdeec31830a6c0286a8766c6f363198')
        check('exact14roles_current_proof_and_whole_inverse',set(proof['exact_finite_transforms'])==set(proof['role_current_paths'])==set(whole['roles'])==set(capture['roles'])and len(whole['roles'])==14)
        parent_mf_bytes=exact(whole['original_P4_manifest_pin']);parent_mf=strict(parent_mf_bytes)
        check('original_P4_manifest_byteexact_saved',raw['DECLARATION_READER_P4_ORIGINAL_PROVENANCE/ORIGINAL_P4_MANIFEST.json']==parent_mf_bytes)
        parent_root=Path(whole['original_P4_manifest_pin']['path']).parent
        p4proof_bytes=exact(whole['parent_actual_consumed_inverse_pin']);p4proof=strict(p4proof_bytes)
        check('original_P4_consumed_proof_byteexact_saved',p4proof_bytes==raw['DECLARATION_READER_P4_ORIGINAL_PROVENANCE/ORIGINAL_P4_ACTUAL_CONSUMED_COMPLETE_SOURCE_INVERSES.json'])
        v3proof_bytes=exact(capture['actual_consumer_proof_parent_pin']);v3proof=strict(v3proof_bytes)
        for rel,q in parent_mf['members'].items():
            old=exact(q)
            check('all_original_P4_member_bytes_retained_except_two_declared_deltas:'+rel,rel in {'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py','COMPLETE_SOURCE_INVERSES.json'}or old==raw[rel])
        current_source=raw['bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py'].decode();old_source=raw['DECLARATION_READER_P4_ORIGINAL_PROVENANCE/ORIGINAL_P4_BUILD_BINDER.full.py'].decode()
        check('current_binder_expected_fullpin',v['files']['bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py']['sha256']=='7240518c9cb74d9cf7ed4a570e4671dbfff32f2c69cfbe07d9fa63d038c92adc')
        row=whole['roles']['build_binder']['current_to_P4_exact_transforms']
        check('one_whole_function_hunk_only',len(row)==1 and row[0]['count']==1 and row[0]['old']==function(old_source,'read')and row[0]['new']==function(current_source,'read'))
        restored,counts=inverse(current_source,row)
        check('entire_binder_restored_to_original_P4_bytes_and_AST',restored==old_source and dump_ast(restored)==dump_ast(old_source),counts)
        olddefs=defs(old_source);curdefs=defs(current_source)
        check('all_other_binder_functions_complete_bytes_and_AST_unchanged',[d for d in curdefs if d[0]!='read']==[d for d in olddefs if d[0]!='read'])
        reader=function(current_source,'read');oldreader=function(old_source,'read');main=function(current_source,'main')
        check('exact_capture_declaration_path_only',"declaration=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-20261010'/'declaration.json'"in reader and 'if p==declaration:'in reader)
        check('normal_absolute_noalias_precedes_branch',reader.index('p=normal(p)')<reader.index('if p==declaration:')and function(current_source,'normal')==function(old_source,'normal'))
        check('regular_singlelink_16MiB_bound_before_open_and_EOF',reader.index('not stat.S_ISREG(before[2])or before[3]!=1 or not 0<=before[4]<=16*2**20')<reader.index('fd=os.open')<reader.index('raw=stream.read(16*2**20+1)'))
        check('O_RDONLY_O_NOFOLLOW_open_same_descriptor_fstat7ID_before_read',"fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)"in reader and 'opened=os.fstat(fd)'in reader and 'opened.st_dev,opened.st_ino,opened.st_mode,opened.st_nlink,opened.st_size,opened.st_mtime_ns,opened.st_ctime_ns' in reader and reader.index('opened=os.fstat(fd)')<reader.index('raw=stream.read'))
        check('bounded_API_read_size_exact_length_and_EOF',"raw=stream.read(16*2**20+1)"in reader and "len(raw)>16*2**20 or len(raw)!=before[4]or stream.read(1)!=b''"in reader)
        check('same_descriptor_fstat7ID_after_EOF',"finished=os.fstat(stream.fileno())"in reader and 'finished.st_dev,finished.st_ino,finished.st_mode,finished.st_nlink,finished.st_size,finished.st_mtime_ns,finished.st_ctime_ns' in reader and reader.index('finished=os.fstat')>reader.index('stream.read(1)'))
        check('descriptor_close_and_IO_control_errors_not_suppressed','finally:\n            if fd is not None:os.close(fd)'in reader and 'except'not in reader)
        check('path7ID_after_EOF_and_after_strict_decode',reader.count('if identity(p)!=before:raise ValueError')==2 and reader.index('hashlib.sha256(raw).hexdigest()')>reader.index('same descriptor changed across EOF'))
        check('complete_SHA_size_same7ID_fullpin_from_actual_bytes','actual=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=before[4],identity=before)'in reader)
        check('summary_and_namespace_already_pinned_before_declaration_decode',"str(summary_path)not in READ_PINS or str(namespace_path)not in READ_PINS"in reader and 'summary=read(summary_path);namespace=read(namespace_path)'in reader and reader.index('summary=read(summary_path)')<reader.index('value=strict_json_bytes(raw)'))
        check('unique_exact_output_owner_and_two_frozen_fullpins_coupled',"owners=[row for row in namespace['namespaces']if row['root']==str(declaration.parent)]"in reader and 'len(owners)!=1'in reader and "wanted=helper_Q_fullpin(summary['actual_declaration'])"in reader and "helper_Q_fullpin(owners[0]['files']['declaration.json'])!=wanted or actual!=wanted"in reader)
        check('repeated_declaration_pin_rejects_changes_and_remains_READ_PINS_input',"if str(p)in READ_PINS and READ_PINS[str(p)]!=actual"in reader and 'READ_PINS[str(p)]=actual'in reader and "for path,wanted in tuple(READ_PINS.items()):helper_Q_check(source_pin(path)==wanted"in main)
        tail=reader[reader.index("    if p.is_relative_to(ART)"):]
        oldtail=oldreader[oldreader.index("    if p.is_relative_to(ART)"):]
        check('original_three_ART_whitelist_and_other_reader_tail_byteexact',tail==oldtail)
        strictfun=function(current_source,'strict_json_bytes')
        check('strict_duplicate_constant_and_recursive_overflow_nonfinite_rejection_unchanged',strictfun==function(old_source,'strict_json_bytes')and 'object_pairs_hook=pairs,parse_constant=reject'in strictfun and 'if k in d:raise ValueError'in strictfun and 'math.isfinite(v)'in strictfun)
        check('whole_main_original_before_declaration_summary_namespace_read_order',main==function(old_source,'main')and main.index("s=read(sp['path']);terminal=read(tp['path']);namespace=read(np['path'])")<main.index("declaration_body=read(outrefs['declaration']['path'])"))
        for br in ('build_binder','prepare_binder'):
            text=raw[proof['role_current_paths'][br]].decode()
            check('actual_fixed_COMPLETE_SOURCE_INVERSES_consumer:'+br,"proof=read(HERE/'COMPLETE_SOURCE_INVERSES.json')"in function(text,'main')and "proof['exact_finite_transforms'][role]"in function(text,'source_verify_original_inverse'))
        for role,q in whole['roles'].items():
            rel=q['relative_path'];text=raw[rel].decode();currentpin=v['files'][rel]
            assert q['current_complete_Source_pin']==currentpin and proof['role_current_paths'][role]==rel
            p4_bytes=exact(q['actual_P4_role_pin']);p4=text
            p4,delta_counts=inverse(p4,q['current_to_P4_exact_transforms'])
            v3,namespace_counts=inverse(p4,q['P4_to_formally_reviewed_V3_namespace_transforms'])
            realv3=exact(capture['roles'][role]['actual_P3_role_pin']).decode()
            parent_bytes=raw['ORIGINAL_PARENT_SOURCE/'+role+'.full.py'];parent=parent_bytes.decode()
            orig,current_counts=inverse(text,proof['exact_finite_transforms'][role])
            p4orig,p4_counts=inverse(p4,p4proof['exact_finite_transforms'][role])
            v3orig,v3_counts=inverse(v3,v3proof['exact_finite_transforms'][role])
            check('whole_current_to_P4_byte_AST_inverse:'+role,p4.encode()==p4_bytes and dump_ast(p4)==dump_ast(p4_bytes),delta_counts)
            check('whole_P4_to_formal_V3_byte_AST_inverse:'+role,v3==realv3 and dump_ast(v3)==dump_ast(realv3),namespace_counts)
            check('actual_consumed_current_to_originalParent_byte_AST_inverse:'+role,orig==parent and dump_ast(orig)==dump_ast(parent),current_counts)
            check('all_intermediate_proofs_to_originalParent_byte_AST_inverse:'+role,p4orig==v3orig==parent and dump_ast(p4orig)==dump_ast(v3orig)==dump_ast(parent))
            if role!='build_binder':check('other13roles_P4_complete_bytes_unchanged:'+role,text.encode()==p4_bytes)
            original_defs=defs(parent);new_defs=defs(text);dm=proof['definitions_by_role'][role]
            records=dm['unchanged_original_definition_occurrences'];actual_records=[]
            for ix,d in enumerate(original_defs):
                matches=[e for e in new_defs if e[0]==d[0]]
                actual=bool(matches and matches[0][1:]==d[1:])
                actual_records.append(dict(name=d[0],occurrence=ix,whole_bytes_and_AST_unchanged=actual))
            check('actual_consumed_definition_metadata_honest_complete_occurrences:'+role,dm['original_count']==len(original_defs)and dm['new_count']==len(new_defs)and records==actual_records)
            results[role]=dict(relative_path=rel,current_Source_pin=currentpin,original_P4_Source_pin=q['actual_P4_role_pin'],formal_V3_Source_pin=capture['roles'][role]['actual_P3_role_pin'],originalParent_retained_pin=v['files']['ORIGINAL_PARENT_SOURCE/'+role+'.full.py'],current_to_P4_counts=delta_counts,P4_to_V3_counts=namespace_counts,actual_consumer_current_to_original_counts=current_counts,whole_byte_AST_inverses=True)
            if role.endswith('.py'):utilities[role]=currentpin
            else:roles[role]=currentpin
        readmeta=[q for q in proof['definitions_by_role']['build_binder']['unchanged_original_definition_occurrences']if q['name']=='read']
        check('modified_read_honestly_false_in_actual_consumed_definition_metadata',len(readmeta)==1 and readmeta[0]['whole_bytes_and_AST_unchanged']is False)
        canonical=raw['canonical.V25.UNREADY.full.py'].decode();assignments={n.targets[0].id:n.value for n in ast.parse(canonical).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
        business=('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
        check('all_six_future_business_pins_remain_None',all(isinstance(assignments[k],ast.Constant)and assignments[k].value is None for k in business))
        check('new_actual_future_environment_business_qualification_not_fabricated',m['all_actual_future_environment_business_or_Source_qualification_pins']is None and m['only_runtime_change_single_BUILD_binder_read_function']is True)
        check('old_nine_caps_and_Q_witness_PREP_guard_contract_preserved_as_P4_bytes',"expected_caps=(1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0)"in main and all(raw[proof['role_current_paths'][role]]==exact(whole['roles'][role]['actual_P4_role_pin'])for role in whole['roles']if role!='build_binder'))
        check('original_helper_full_Source_SHA_unchanged',v['files']['SOURCE_AND_ACTUAL_SMALL_META/SOURCE_01_combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py']['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092')
        failed=strict(raw['DECLARATION_READER_P4_ORIGINAL_PROVENANCE/Root_actual_memory_observation_capture_BUILD_Source_binding_declaration_reader_failure_tool_terminal_return.json'])
        check('true_original_0b88da_failure_preserved_not_credited_PASS',closed(failed,1)and failed['terminal_tool_return']['chunk_id']=='0b88da'and failed['actual_BUILD_or_candidate_executed']is False and 'no ART graph/trace/payload decoding'in failed['terminal_tool_return']['output'])
        original_failed=jsonread(Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_memory_observation_capture_BUILD_Source_binding_declaration_reader_failure_tool_terminal_return.json'))
        check('retained_failure_full_bytes_match_actual_Root_failure',raw['DECLARATION_READER_P4_ORIGINAL_PROVENANCE/Root_actual_memory_observation_capture_BUILD_Source_binding_declaration_reader_failure_tool_terminal_return.json']==read(original_failed[1]['path'])[0])
        author=strict(raw['AUTHOR_P4_BUILD_DECLARATION_READER_SINGLE_FUNCTION_SOURCE_REPORT.json'])
        check('current_author_all14_fullpins_match_independent_actual_reads',author['qualified_role_Source_pins']==roles and author['qualified_utility_Source_pins']==utilities)
        ss=Path(str(P)+'_seal_receipt')
        for name in ('ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json'):
            d,qp=jsonread(ss/name);check('author_true_closed0_lineage:'+name,closed(d),qp)
            o=strict(d['terminal_tool_return']['output'].encode());check('author_saved_manifest_is_current_source:'+name,o['manifest_pin']==mf)
        check('full_candidate_recheck_EOF_SHA7IDs_after_source_analysis',complete_view(P)[0]==v)
    except Exception as exc:
        check('finite_review_completed_without_unhandled_validation_exception',False,dict(type=type(exc).__name__,message=str(exc)))
    passed=not BLOCKERS and all(type(c['passed'])is bool and c['passed']is True for c in CHECKS)
    report=dict(schema='INDEPENDENT_V25_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_REVIEW_V1',status='PASS_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_ONLY_UNREADY_NO_EXECUTION'if passed else 'FAIL_SINGLE_BUILD_DECLARATION_READER_SOURCE_ONLY_BLOCKED',source_only=True,scope='Single BUILD binder read() Source delta only; complete current members, AST, 14-role byte/AST inverses and actual consumed proof. Previously independently reviewed P4 namespace206 and formal V3 memory186 semantics are explicit prerequisites and are not requalified.',check_count=len(CHECKS),checks=CHECKS,all_checks_typed_true=passed,blockers=BLOCKERS,qualified_complete_Source_manifest_pin=mf,qualified_role_Source_pins=roles,qualified_utility_Source_pins=utilities,complete_current_candidate_Source_small_META_view=v,whole_14_role_independent_inverse_results=results,all_independently_read_Source_small_META_input_pins=INPUT_PINS,reviewer_original_Source_pin=sourcepin,prior_independent_P4_namespace206_and_formal_V3_memory186_are_relied_on=True,candidate_BINDER_API_guard_resource_helper_material_numeric_or_business_executed=False,actual_ART_declaration_graph_trace_gzip_material_payload_read=False,project_candidate_or_business_inputs_written=False,whole_INPUT_BUILD_RSS_native_or_science_qualified=False,old_runtime_caps_and_scientific_gates_changed=False)
    write_json(root/'REVIEW.json',report)
    write_json(root/'COMPLETE_CURRENT_SOURCE_AND_14_ROLE_INVERSE_RESULTS.json',dict(source_only=True,complete_candidate_view=v,whole14results=results))
    print(json.dumps(dict(root=str(root),review_pin=read(root/'REVIEW.json')[1],source_only=True,status=report['status'],check_count=len(CHECKS),blockers=BLOCKERS,qualified_complete_Source_manifest_pin=mf),sort_keys=True,allow_nan=False))
    return 0 if passed else 1

if __name__=='__main__':
    assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')
    sys.exit(review())
