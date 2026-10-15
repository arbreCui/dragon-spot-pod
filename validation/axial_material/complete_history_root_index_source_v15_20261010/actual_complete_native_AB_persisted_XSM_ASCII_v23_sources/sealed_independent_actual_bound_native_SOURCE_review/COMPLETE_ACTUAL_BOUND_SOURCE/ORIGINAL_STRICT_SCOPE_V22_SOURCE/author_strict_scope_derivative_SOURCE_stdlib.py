"""Author stdlib-only SOURCE derivative; no candidate import or execution."""
import ast, difflib, hashlib, json, os, stat
from pathlib import Path
P=Path(__file__).resolve().parent
OLD=P/'ORIGINAL_FIXED_HOST_BINDER_SOURCE'

def require(v,msg):
    if type(v)is not bool or not v:raise ValueError(msg)

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    s=p.lstat();require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'Source regular nlink1')
    with p.open('rb')as f:
        require(identity(os.fstat(f.fileno()))==identity(s),'open ID')
        h=hashlib.file_digest(f,'sha256').hexdigest()
        require(identity(os.fstat(f.fileno()))==identity(s),'EOF ID')
    require(identity(p.lstat())==identity(s),'path ID')
    return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=identity(s))

def replace_once(s,old,new):
    require(s.count(old)==1,'exact unique Source replacement');return s.replace(old,new,1)

def full_inverse(original,derived):
    a=original.splitlines(keepends=True);b=derived.splitlines(keepends=True)
    changes=[]
    for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if tag!='equal':changes.append(dict(tag=tag,original_zero_based_start=i,original_zero_based_end=j,derived_zero_based_start=k,derived_zero_based_end=l,original_full_lines=a[i:j],derived_full_lines=b[k:l]))
    reverse=b[:]
    for h in reversed(changes):
        require(reverse[h['derived_zero_based_start']:h['derived_zero_based_end']]==h['derived_full_lines'],'full hunk')
        reverse[h['derived_zero_based_start']:h['derived_zero_based_end']]=h['original_full_lines']
    require(''.join(reverse)==original,'all original bytes inverse')
    ast.parse(derived)
    return changes

terminal='''def actual_terminal(expected, zero, expected_schema):
    typed_pin(expected)
    value=strict_json(Path(expected['path']).read_bytes())
    require(type(value)is dict and value['schema']==expected_schema
            and value['closed']is True and value['observed_terminal']is True
            and value['session_repolled_after_close']is False,
            'actual Root observed CLOSED family required; PREP cannot stand for BUILD')
    terminal=value['terminal_tool_return']
    require(type(terminal)is dict and type(terminal['exit_code'])is int
            and 'session_id'not in terminal and type(terminal['chunk_id'])is str and bool(terminal['chunk_id'])
            and type(value['actual_terminal_chunk'])is str
            and value['actual_terminal_chunk']==terminal['chunk_id'],
            'genuine Root typed CLOSED tool truth and exact observed terminal chunk required')
    require(not zero or terminal['exit_code']==0,'Source admission actual typedzero required')
    return value


def source_scope_contract(request, expected_sources, source_truth):
    for expected in expected_sources.values():typed_pin(expected)
    peer=strict_json(Path(request['independent_host_binder_Source_review_pin']['path']).read_bytes())
    require(type(peer)is dict and peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1'
            and peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'
            and peer['source_only']is True and peer['all_checks_passed']is True
            and type(peer['blockers'])is list and peer['blockers']==[],
            'actual independent full native host/binder Source review scope required')
    checks=peer['checks']
    require(type(checks)is list and type(peer['check_count'])is int and peer['check_count']==len(checks)>0
            and all(type(row)is dict and set(row)=={'check','passed'}
                    and type(row['check'])is str and bool(row['check'])and row['passed']is True for row in checks)
            and len({row['check']for row in checks})==len(checks),
            'all independent Source checks retained, exact count and typed PASS')
    admission=strict_json(Path(request['source_admission_pin']['path']).read_bytes())
    require(type(admission)is dict and admission['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_HOST_BINDER_SOURCE_ADMISSION_V1'
            and admission['status']=='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE'
            and admission['source_only']is True and admission['scientific_qualification_created']is False
            and admission['actual_native_byte_qualification_sha256']is None
            and admission['actual_scientific_qualification_sha256']is None,
            'actual Root Source admission must retain software-only scope and unknown qualifications')
    for key,expected in expected_sources.items():
        typed_pin(peer[key]);typed_pin(admission[key])
        require(peer[key]==expected and admission[key]==expected,
                'peer/admission fullpin must match actual complete author manifest and each Source body: '+key)
    typed_pin(admission['independent_Source_review_pin'])
    require(admission['independent_Source_review_pin']==request['independent_host_binder_Source_review_pin'],
            'Source admission must bind this same independently reviewed Source report')
    output=strict_json(source_truth['terminal_tool_return']['output'])
    require(type(output)is dict and output['source_only']is True
            and output['status']=='ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE',
            'genuine actual Source admission output scope required')
    typed_pin(output['source_admission_pin'])
    require(output['source_admission_pin']==request['source_admission_pin'],
            'actual Source admission tool output fullpin must equal actual admission record')
    return dict(schema='ACTUAL_COMPLETE_NATIVE_SOURCE_SCOPE_COUPLING_V1',source_only=True,
                all_four_actual_author_Source_fullpins_coupled=True,independent_full_Source_checks_count=len(checks),
                Source_admission_actual_tool_output_fullpin_coupled=True,PREP_is_not_BUILD=True,
                actual_Source_admission=request['source_admission_pin'],
                actual_independent_Source_review=request['independent_host_binder_Source_review_pin'],
                actual_author_Source_contract=expected_sources)


'''
binder_name='bind_complete_native_SOURCE_only.UNREADY.py'
binder_original=(OLD/binder_name).read_text()
binder=binder_original
start=binder.index('def actual_terminal(');end=binder.index('def bind_globals(',start)
binder=binder[:start]+terminal+binder[end:]
binder=replace_once(binder,"source_truth=actual_terminal(request['actual_Root_Source_admission_tool_return_pin'],True)\n    prior_truth=actual_terminal(request['prior_actual_V22_build_tool_return_pin'],False)","source_truth=actual_terminal(request['actual_Root_Source_admission_tool_return_pin'],True,'ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1')\n    prior_truth=actual_terminal(request['prior_actual_V22_build_tool_return_pin'],False,'ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1')\n    expected_sources=dict(qualified_source_manifest=mp,\n                          host_template=pin(P/'complete_native_XSM_ASCII_genuine_host.UNREADY.py'),\n                          checker_template=pin(P/'complete_native_XSM_ASCII_checker_v4.UNREADY.py'),\n                          binder=pin(Path(__file__).resolve()))\n    scope_coupling=source_scope_contract(request,expected_sources,source_truth)")
binder=replace_once(binder,"P/'PARENT_NATIVE_SOURCE/ROOT_BINDING_BLUEPRINT.UNREADY.json'","P/'ORIGINAL_FIXED_HOST_BINDER_SOURCE/PARENT_NATIVE_SOURCE/ROOT_BINDING_BLUEPRINT.UNREADY.json'")
binder=replace_once(binder,"binding.update(source_only=True,scientific_qualification_created=False,","binding.update(source_only=True,scientific_qualification_created=False,\n                   actual_author_Source_contract=expected_sources,actual_Source_scope_coupling=scope_coupling,")
binder=replace_once(binder,"actual_Source_admission_tool_truth=source_truth,prior_actual_closed_V22_build_tool_truth=prior_truth,","actual_Source_admission_tool_truth=source_truth,prior_actual_closed_V22_build_tool_truth=prior_truth,\n                actual_Source_scope_coupling=scope_coupling,actual_author_Source_contract=expected_sources,")
binder=replace_once(binder,"for m in members:typed_pin({key:m[key]for key in ('path','sha256','size_bytes','identity')})\n    print", "for m in members:typed_pin({key:m[key]for key in ('path','sha256','size_bytes','identity')})\n    for key in ('source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin','prior_actual_V22_build_tool_return_pin'):typed_pin(request[key])\n    require(source_scope_contract(request,expected_sources,actual_terminal(request['actual_Root_Source_admission_tool_return_pin'],True,'ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1'))==scope_coupling,'all Source admission/peer coupling unchanged after Source binding')\n    actual_terminal(request['prior_actual_V22_build_tool_return_pin'],False,'ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1')\n    print")

host_name='complete_native_XSM_ASCII_genuine_host.UNREADY.py'
host_original=(OLD/host_name).read_text();host=host_original
host_terminal='''def actual_closed_prior(pin_value, zero=False, expected_schema='ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1'):
    typed_full_pin(pin_value)
    value=strict_json(Path(pin_value['path']).read_bytes())
    require(type(value)is dict and value['schema']==expected_schema
            and value['closed']is True and value['observed_terminal']is True
            and value['session_repolled_after_close']is False,
            'prior Root actual observed CLOSED family required; PREP cannot stand for BUILD')
    actual=value['terminal_tool_return']
    require(type(actual)is dict and type(actual['exit_code'])is int and 'session_id'not in actual
            and type(actual['chunk_id'])is str and bool(actual['chunk_id'])
            and type(value['actual_terminal_chunk'])is str and value['actual_terminal_chunk']==actual['chunk_id'],
            'prior Root exact observed typed CLOSED tool truth required; any honest build exit allowed')
    require(not zero or actual['exit_code']==0,'actual Root Source admission typedzero required')
    return value


'''+terminal[terminal.index('def source_scope_contract('):].replace('typed_pin(', 'typed_full_pin(')
start=host.index('def actual_closed_prior(');end=host.index('def main(',start)
host=host[:start]+host_terminal+host[end:]
host=replace_once(host,"prior=actual_closed_prior(b['prior_actual_V22_build_tool_return_pin'])", "prior=actual_closed_prior(b['prior_actual_V22_build_tool_return_pin'])\n    expected_sources=b['actual_author_Source_contract']\n    require(type(expected_sources)is dict and set(expected_sources)=={'qualified_source_manifest','host_template','checker_template','binder'},'all four exact original author Source contract pins required')\n    for p in expected_sources.values():inputs.append(recheck_full_pin(support,p))\n    source_truth=actual_closed_prior(b['actual_Root_Source_admission_tool_return_pin'],True,'ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1')\n    scope_coupling=source_scope_contract(b,expected_sources,source_truth)\n    require(scope_coupling==b['actual_Source_scope_coupling'],'all Source admission/peer coupling equals actual binder record')")
host=replace_once(host,"prior_actual_V22_build_terminal=prior,external_actual_Root_typed_EXIT0_CLOSED_required=True", "prior_actual_V22_build_terminal=prior,actual_Source_scope_coupling=scope_coupling,actual_author_Source_contract=expected_sources,external_actual_Root_typed_EXIT0_CLOSED_required=True")
proof=dict(schema='FULL_NATIVE_HOST_BINDER_STRICT_SCOPE_SOURCE_DERIVATIVE_ALL_HUNKS_INVERSE_V1',source_only=True,zero_based_line_ranges=True,
           parent_manifest=pin(OLD/'MANIFEST.json'),
           host=dict(original=pin(OLD/host_name),hunks=full_inverse(host_original,host),all_parent_bytes_restored=True),
           binder=dict(original=pin(OLD/binder_name),hunks=full_inverse(binder_original,binder),all_parent_bytes_restored=True),
           checker_v4_full_bytes_unchanged=(P/'complete_native_XSM_ASCII_checker_v4.UNREADY.py').read_bytes()==(OLD/'complete_native_XSM_ASCII_checker_v4.UNREADY.py').read_bytes(),
           no_candidate_execution=True,no_helper_API_guard_business_or_native_read=True,no_project_or_original_Source_write=True)
(P/host_name).write_text(host);(P/binder_name).write_text(binder)
proof['host']['derived']=pin(P/host_name);proof['binder']['derived']=pin(P/binder_name)
(P/'STRICT_SCOPE_FULL_SOURCE_INVERSE_PROOF.json').write_text(json.dumps(proof,indent=2,allow_nan=False)+'\n')
request=json.loads((OLD/'ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json').read_bytes())
request['schema']='ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_BINDING_REQUEST_V1'
request['source_admission_pin']=None
request['actual_Root_Source_admission_tool_return_pin']=None
request['independent_host_binder_Source_review_pin']=None
request['prior_actual_V22_build_tool_return_pin']=None
request['Source_admission_contract']=dict(schema='ROOT_ACTUAL_COMPLETE_NATIVE_HOST_BINDER_SOURCE_ADMISSION_V1',status='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE',source_only=True,scientific_qualification_created=False,actual_native_byte_qualification_sha256=None,actual_scientific_qualification_sha256=None,qualified_source_manifest=None,host_template=None,checker_template=None,binder=None,independent_Source_review_pin=None)
request['actual_Source_admission_tool_contract']=dict(schema='ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1',closed=None,observed_terminal=None,session_repolled_after_close=None,actual_terminal_chunk=None,terminal_tool_return=None,required_actual_terminal_output=dict(source_only=True,status='ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE',source_admission_pin=None))
request['actual_prior_BUILD_tool_contract']=dict(schema='ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1',closed=None,observed_terminal=None,session_repolled_after_close=None,actual_terminal_chunk=None,terminal_tool_return=None,PREP_cannot_substitute_BUILD=True,any_actual_typed_int_exit_retained=True)
(P/'ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json').write_text(json.dumps(request,indent=2,allow_nan=False)+'\n')
(P/'ROOT_EXECUTION_SEQUENCE_AND_REQUIRED_PINS.md').write_text('''# Root-only sequence for complete native persisted byte evidence\n\nAll code remains UNREADY. The original 30958 Source package is preserved in full under ORIGINAL_FIXED_HOST_BINDER_SOURCE. This derivative strengthens only genuine terminal observation and exact Source-family coupling. Complete v4 checker bytes are unchanged. There has been no candidate, API, guard, compile, helper, payload or business execution.\n\n1. Complete independent Source review of this entire fixed package. Required peer schema is INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1; status SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE; source_only/all_checks_passed true; blockers []; exact check_count and complete unique checks [{check, passed:true}]; qualified_source_manifest, host_template, checker_template, binder each exact path/SHA/size/7 typed-int pin to THIS package.\n2. Root saves genuine Source-only admission record with schema ROOT_ACTUAL_COMPLETE_NATIVE_HOST_BINDER_SOURCE_ADMISSION_V1, status SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE, source_only true, scientific_qualification_created false, future native/science Q SHA None, the same four full Source pins and independent_Source_review_pin pointing to that same peer record. Root's genuine observed admission tool output must be JSON {source_only:true,status:ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE,source_admission_pin:<actual fullpin>}.\n3. Root preserves original actual admission terminal in a normalized observation wrapper ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1: closed:true, observed_terminal:true, session_repolled_after_close:false, actual_terminal_chunk equal terminal_tool_return.chunk_id, exact integer exit0 and no session_id. Normalized observation metadata must be Root-observed; it does not rewrite original output.\n4. Root executes complete V22 build serially. BUILD has not run at authoring time. Its separate future actual receipt schema must be ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1, with closed/observed_terminal true, repoll false, actual terminal chunk equal genuine terminal chunk, exact integer actual exit and no session_id. Any honest build exit is retained, without claiming build PASS. The copied ACTUAL_ROOT_PREP_RECEIPT_SHAPE_ONLY_NOT_BUILD.json (SHA566ef...) only demonstrates actual observation keys; PREP cannot authorize BUILD or substitute its receipt. A build/source-binary link gap remains false; it is not an extra native-byte-read blocker.\n5. Root fills ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json with these four actual META pins and five fresh H/O/C/D/E namespaces; computes request SHA. Run only this stdlib Source binder with --source-manifest-sha256 <THIS fixed manifest SHA> --request <real Root request> --request-sha256 <real SHA> --output-source-dir <fresh /private/tmp derivative>. No candidate imported or executed by binder. It copies the full package, binds exact globals, preserves all129 original pins, writes actual Source-binding record and full inverse. Root saves genuine typed0 CLOSED binder tool truth separately.\n6. Independently review full bound Source. Root installs complete bound Source into fresh D, preserves original D files/directories and existing E snapshots, then separately admits the actual genuine host. Future Source installation and native qualification remain unknown until observed.\n7. Root runs genuine native host once, after the separate build is CLOSED, never concurrently with a numerical child. The host preserves original619/705/38de/bc4/ebbb guard/MRO, whole1800/stage600/RSS512MiB/jointHOCDE2GiB/history96GiB/free8GiB/thread1/child1/retry0. All129 original inputs plus actual Source/peer/admission/build pins are fullEOF/SHA/7ID checked before and after. D/E complete files/directories stay frozen; host/runtime/stdout/stderr/watchdogs, all output spools/SQLite/journal/temp files count under joint caps. A's complete SQLite/cache/file state is closed before B.\n8. Save actual success OR nonzero native mismatch/loss/structural failure and complete existing report honestly. REAL64/character/logical export loss remains a real failure. New native walker malformed controls are unexecuted (None); old raw5positive10reject only describe their separate saved scope. Persisted native XSM byte equality does not prove historical RAM bit identity, reaction/transport balance, coupled reference, AAA/ABA or scientific accuracy. All those flags remain false and future Q pins None. No Source audit is physics qualification.\n''')
print(json.dumps(dict(source_only=True,host=pin(P/host_name),binder=pin(P/binder_name),checker=pin(P/'complete_native_XSM_ASCII_checker_v4.UNREADY.py'),full_inverse_proof=pin(P/'STRICT_SCOPE_FULL_SOURCE_INVERSE_PROOF.json'),host_hunks=len(proof['host']['hunks']),binder_hunks=len(proof['binder']['hunks']),no_candidate_execution=True),indent=2),flush=True)
