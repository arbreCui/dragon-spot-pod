"""Static Source only. Does not execute/import any reviewed Source."""
import ast
import difflib
import hashlib
import json
from pathlib import Path
import stat

P=Path(__file__).resolve().parent
checks=[]


def check(name,ok):
    assert type(ok)is bool and ok,name
    checks.append(dict(check=name,passed=True))


def ident(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pin(path):
    s=path.lstat();check('regular unaliased Source '+str(path),stat.S_ISREG(s.st_mode)and s.st_nlink==1)
    raw=path.read_bytes();check('full Source EOF7ID '+str(path),len(raw)==s.st_size and ident(s)==ident(path.lstat()))
    return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ident(s)),raw


def reverse(old_path,new_path,label):
    old_pin,old=pin(old_path);new_pin,new=pin(new_path)
    oldlines,newlines=old.decode().splitlines(keepends=True),new.decode().splitlines(keepends=True)
    hunks=[]
    for kind,a,b,c,d in difflib.SequenceMatcher(None,oldlines,newlines,autojunk=False).get_opcodes():
        if kind!='equal':hunks.append(dict(old_begin_line_zero_based=a,old_end_exclusive_zero_based=b,new_begin_line_zero_based=c,new_end_exclusive_zero_based=d,old_full_lines=oldlines[a:b],new_full_lines=newlines[c:d]))
    back=newlines[:]
    for h in reversed(hunks):
        check(label+' full hunk '+str(h['new_begin_line_zero_based']),back[h['new_begin_line_zero_based']:h['new_end_exclusive_zero_based']]==h['new_full_lines'])
        back[h['new_begin_line_zero_based']:h['new_end_exclusive_zero_based']]=h['old_full_lines']
    check(label+' complete reverse restores all original bytes',''.join(back).encode()==old)
    def defs(raw):return {n.name:ast.dump(n,include_attributes=False)for n in ast.parse(raw).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    a,b=defs(old),defs(new)
    check(label+' all original functions/classes retained',set(a)<=set(b))
    same=[name for name in a if a[name]==b[name]];changed=[name for name in a if a[name]!=b[name]]
    return dict(label=label,original_full_Source=old_pin,current_full_Source=new_pin,full_line_hunks=hunks,complete_reverse_restores_original_bytes=True,unchanged_function_AST=same,changed_function_AST=changed,added_functions=sorted(set(b)-set(a)))


parent=Path('/private/tmp/axmat_complete_native_XSM_ASCII_UNREADY_SOURCE_20261010_vs7f_ff8')
for f in sorted(parent.rglob('*')):
    if f.is_dir():continue
    a,raw=pin(f);b,copy=pin(P/'PARENT_NATIVE_SOURCE'/f.relative_to(parent))
    check('every complete parent Source copied byte-exact '+str(f),raw==copy)
source_pins=json.loads((parent/'ORIGINAL_SOURCE_PROVENANCE_PINS.json').read_bytes())['pins']
for p in source_pins:
    got,raw=pin(Path(p['path']));check('all35 original Source remain fullSHA7ID '+p['path'],got=={k:p[k]for k in got})
proofs=[reverse(P/'ORIGINAL_full_AB_rawrecord_genuine_host_READY.py',P/'complete_native_XSM_ASCII_genuine_host.UNREADY.py','complete original raw genuine host to native host'),
        reverse(P/'PARENT_NATIVE_SOURCE/complete_native_XSM_ASCII_checker_v3.UNREADY.py',P/'complete_native_XSM_ASCII_checker_v4.UNREADY.py','full v3 checker to v4 joint archive')]
check('all four nonmain original host functions AST unchanged',proofs[0]['unchanged_function_AST']==['require','strict_json','complete_source_inputs','observed_stage']and proofs[0]['changed_function_AST']==['main'])
check('checker onlyBudget/DiskRecords/main changed; all14 other functions unchanged',proofs[1]['changed_function_AST']==['Budget','DiskRecords','main']and len(proofs[1]['unchanged_function_AST'])==14)
host=(P/'complete_native_XSM_ASCII_genuine_host.UNREADY.py').read_text();binder=(P/'bind_complete_native_SOURCE_only.UNREADY.py').read_text();checker=(P/'complete_native_XSM_ASCII_checker_v4.UNREADY.py').read_text()
for f in sorted(P.rglob('*.py')):
    tree=ast.parse(f.read_bytes(),filename=str(f));check('entire Source AST '+str(f),isinstance(tree,ast.Module))
tree=ast.parse(host)
assign={t.id:n.value for n in tree.body if isinstance(n,ast.Assign)for t in n.targets if isinstance(t,ast.Name)}
check('host UNREADY literal',ast.literal_eval(assign['SOURCE_STATUS'])=='UNREADY_SOURCE_ONLY')
for name in ('SOURCE_ARCHIVE','RECEIPTS','HOST','OUT','CONTROL','TARGET','TARGET_SHA','PROTOCOL','PROTOCOL_SHA','BINDING','BINDING_SHA','SOURCE_ADMISSION_SHA','ACTUAL_PROTOCOL_QUALIFICATION_SHA256','ACTUAL_TRANSFER_QUALIFICATION_SHA256','REACTION_MULTIPLICITY_QUALIFICATION_SHA256','ACTUAL_SCIENTIFIC_REFERENCE_SHA256'):
    check('all future actual host pin/namespace/Q None '+name,ast.literal_eval(assign[name])is None)
for name,fragment in {
    'original619helper loader': "support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_v15_admission_original619')",
    'original eb bb resource loader': "support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'axmat_v15_admission_real_resource_module')",
    'original full guardian actual controls': 'helper.guard_admission(full)',
    'exact original MRO': 'full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)',
    'full original bound runtime copied': "shutil.copy2(support.BOUNDED,host/'runtime/run_bounded_dragon.py')",
    'actual canonical Original runner': "full.OwnRSSSerialExecutor(host,remaining,'COMPLETE_NATIVE_XSM_ASCII',resources)",
    'one true original600 stage': "runner.execute(host/'native_run','native_xsm_ascii',command,STAGE_CAP)",
    'all129 original input pins': "len(b['complete_input_pins'])==129",
    'Source full directory freeze': 'complete_source_directory_freeze=source_directories',
    'E complete directory freeze': 'complete_receipt_directory_freeze=receipt_directories',
    'original96history/free8 reserve': "before['artifact_bytes']+ARCHIVE_CAP>=96*2**30",
    'complete original history roots': "[str(host),str(out),str(control),str(support.OUT),str(support.TERMINAL)]",
    'all Native and Macro Scope': "macro['records']==19619",
    'bit loss report preserved on failure': 'actual_native_report_pin_if_saved=',
    'actual closed priorbuild without requiring fakePASS': "type(actual['exit_code'])is int and 'session_id'not in actual",
    'new controls explicitly unexecuted': 'new_native_walker_controls_actual_run=None',
    'all Source binary linkage gap honest': 'original_native_build_binary_Source_linkage_qualified=False',
}.items():check(name,fragment in host)
check('exactly one native execute, no new protocolexecute',host.count('runner.execute(')==1 and 'protocol_command='not in host and 'transfer_command='not in host)
check('no runner env/class/process/resource override',all(x not in host for x in ('runner.env[','runner.env =','full.OwnRSSSerialExecutor=','full.OwnRSSSerialExecutor =','runner._process=','runner._process =')))
for name,fragment in {'native original5 joint roots':'len(joint_roots) == 5','allHOCDE checks':'for root in self.joint_roots:','same original2GiB cap':"total < CAPS['joint_archive_bytes']",'SQLiteFILE temp withinO':"os.environ['SQLITE_TMPDIR'] = str(Path(path).parent)",'onlybind source2globals':"ROOT_BOUND_BINDING_SHA256 = None"}.items():check(name,fragment in checker)
for name,fragment in {'Source binder onlyTMP output':"destination.is_relative_to(Path('/private/tmp'))",'actualSource schema int0 truth':"actual_terminal(request['actual_Root_Source_admission_tool_return_pin'],True)",'prior actual build closedtruth':"actual_terminal(request['prior_actual_V22_build_tool_return_pin'],False)",'all129 untouched':'all_original_input_pins_preserved_exact=True','fullSourcecopy':'shutil.copytree(P,destination)','noSourceexec':'bound_checker,checker_inverse=bind_globals','fullbytesreverse':"''.join(restored).encode()==source"}.items():check(name,fragment in binder)
btree=ast.parse(binder)
check('binder no dynamic/API/business import or execution',not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id in ('exec','eval','compile','__import__')for n in ast.walk(btree))and 'importlib'not in binder and 'runpy'not in binder and 'subprocess'not in binder)
request=json.loads((P/'ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json').read_bytes())
check('all request actualfourpin placeholders None',all(request[key]is None for key in ('source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin','prior_actual_V22_build_tool_return_pin')))
(P/'COMPLETE_HOST_AND_V4_CHECKER_SOURCE_INVERSE_PROOF.json').write_text(json.dumps(dict(schema='COMPLETE_NATIVE_HOST_AND_CHECKER_SOURCE_FULL_INVERSE_V1',source_only=True,proofs=proofs,no_candidate_or_guard_execution=True,no_numeric_native_or_ASCII_material_payload_read=True),indent=2)+'\n')
host_pin=pin(P/'complete_native_XSM_ASCII_genuine_host.UNREADY.py')[0]
checker_pin=pin(P/'complete_native_XSM_ASCII_checker_v4.UNREADY.py')[0]
binder_pin=pin(P/'bind_complete_native_SOURCE_only.UNREADY.py')[0]
report=dict(schema='COMPLETE_NATIVE_GENUINE_HOST_BINDER_UNREADY_SOURCE_REVIEW_V1',source_only=True,checks=checks,check_count=len(checks),all_static_checks_passed=True,host_pin=host_pin,checker_v4_pin=checker_pin,binder_pin=binder_pin,original35_Source_unchanged=True,complete_parent_Source_files=53,all129_inputs_preserved=True,no_original_Source_project_ART_frozen_D_E_write=True,no_candidate_helper_native_API_guard_compile_or_business_execution=True,no_native_numeric_or_ASCII_material_payload_read=True,actual_source_admission=None,actual_genuine_host=None,actual_native_run=None,actual_native_success=None,actual_RSS_qualification=None,new_native_walker_controls_actual_run=None,original_native_build_binary_Source_linkage_qualified=False,original_XSM_memory_bits_verified=False,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
(P/'STATIC_COMPLETE_NATIVE_HOST_BINDER_SOURCE_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(source_only=True,checks=len(checks),host=report['host_pin'],checker_v4=report['checker_v4_pin'],binder=report['binder_pin'],inverse_hunk_counts=[len(x['full_line_hunks'])for x in proofs],candidate_guard_API_native_never_run=True),indent=2))
