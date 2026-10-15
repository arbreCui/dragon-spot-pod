"""Bounded SOURCE-only review of original candidate; no reviewed code is imported/called."""
import ast,hashlib,json,pathlib,stat
P=pathlib.Path(__file__).parent
checks=[]
def pin(p):
 s=p.lstat();a=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 assert stat.S_ISREG(a[2]) and a[3]==1
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 t=p.lstat();b=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
 assert a==b;return dict(path=str(p),sha256=h,size_bytes=a[4],identity=a)
def check(x,label):
 assert x;checks.append(dict(check=label,passed=True))
w=pathlib.Path('/private/tmp/spot_v22_native_postclose_META_ROOT.py');i=pathlib.Path('/private/tmp/spot_install_v22_complete_native_ROOT.py')
wp=pin(w);ip=pin(i);ws=w.read_text();ins=i.read_text()
check(wp['sha256']=='5f302e44a094c20682e1708f3cd714f4e7bedf7da12de1c775ccca7b8338ea5b','fixed original writer SHA')
check(ip['sha256']=='355081f5464a4f9a6588673bb5e3b692457f53aba2a958f8b3d1d5ee95224506','fixed original installer SHA')
check(w.read_bytes()==(P/'original_5f302e_writer_SOURCE.py').read_bytes(),'full original writer Source preserved')
check(i.read_bytes()==(P/'original_355081_installer_SOURCE.py').read_bytes(),'full original installer Source preserved')
wt=ast.parse(ws);it=ast.parse(ins)
check(len([n for n in wt.body if isinstance(n,ast.FunctionDef)])==7,'seven writer definitions')
check(len([n for n in it.body if isinstance(n,ast.FunctionDef)])==1,'one original installer main definition')
check([n.name for n in wt.body if isinstance(n,ast.FunctionDef)]==['identity','pin','snapshot','read','write','bytes_in','main'],'complete standard metadata function layout')
check([n.module for n in wt.body if isinstance(n,ast.ImportFrom)]==['pathlib'],'writer no project module imports')
check("if __name__=='__main__':main()" in ws and "spec_from_file_location('Root_native_metadata_functions_only',WRITER)" in ins,'installer imports writer standard functions under nonmain name')
check('spec.loader.exec_module(support)' not in ws and 'subprocess' not in ws,'writer no native/guard subprocess execution')
check('original_XSM_memory_bits_verified=False' in ws and 'physical_neutron_balance_qualified=False' in ws and 'actual_native_byte_qualification_sha256=None' in ws,'scientific and future qualification remain false/unknown')
check("assert snapshot(D)==pre['complete_D_frozen']" in ws and "current_E['files'][k]==q" in ws,'D freeze and original E files revalidation retained')
check("for k,q in view['files'].items()" in ins and "assert m.snapshot(Path(view['root']))==view" in ins and 'frozen=m.snapshot(m.D);assert m.snapshot(m.E)==before_E' in ins,'installer complete actual files copied and source/E snapshots rechecked')
gap="host['actual_native']['report']" not in ws
check(gap and "report,_=read(O/'ACTUAL_COMPLETE_NATIVE_XSM_ASCII_EVIDENCE_REPORT.json')" in ws,'determinate success current report pin discarded and no actual stage report crosspin')
host=pathlib.Path('/private/tmp/axmat_complete_native_actual_BOUND_SOURCE_ROOT_20261010_503adf/Root_bound_complete_native_genuine_host.py');hs=host.read_text();hp=pin(host)
check("'report':support.pin(report_path)" in hs and "returned['report']['sha256']==support.pin(report_path)['sha256']" in hs,'genuine host explicitly records and validates actual report pin')
report=dict(schema='INDEPENDENT_ROOT_NATIVE_POSTCLOSE_METADATA_ORIGINAL_SOURCE_REVIEW_V1',status='SOURCE_BLOCKED_EXACT_REPORT_PIN_BINDING_GAP',all_checks_typed_true=True,checks=checks,check_count=len(checks),writer_pin=wp,installer_pin=ip,limited_genuine_host_Source_pin=hp,blockers=[dict(code='ACTUAL_REPORT_PIN_NOT_BOUND_IN_META_SUCCESS',evidence="writer discards read(report) pin; genuine host saves actual_native.report; writer checks no such pin",minimum_fix="retain report read pin and compare exact path/sha256/identity with host actual_native.report; installer writer SHA literal retarget only")],source_only=True,reviewer_imported_or_executed_candidate=False,reviewer_guard_or_native_or_numeric_executed=False,current_candidate_source_qualified=False,actual_native_byte_qualification_sha256=None,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,Root_has_authorized_minimum_source_v2_repair=True,whole_Source_and_META_scope_unchanged=True)
(P/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(P/'REPORT.txt').write_text('Original5f302e/355081 Source blocked by one exact output-report binding gap. Source copies and limited host record constructor proof retained.\nMinimum v2 repair only: keep report read pin and compare path/SHA/7ID against host actual_native.report; installer only retargets writer SHA.\nFixed bound89 and current E have no empty subdirectories; no new directory control or scientific guard requested. No candidate/guard/native/numeric program run or source qualification invented.\n')
assert pin(w)==wp and pin(i)==ip and pin(host)==hp
print(json.dumps(dict(status=report['status'],check_count=len(checks),one_determinate_Source_blocker=True,no_native_executed=True,review=str(P/'REVIEW.json'))))

