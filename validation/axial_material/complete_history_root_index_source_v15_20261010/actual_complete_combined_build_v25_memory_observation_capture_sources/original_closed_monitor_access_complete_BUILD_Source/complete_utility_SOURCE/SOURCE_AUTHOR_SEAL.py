import ast,hashlib,json,stat
from pathlib import Path
P=Path(__file__).parent
def ident(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ident(p);assert p.resolve()==p and stat.S_ISREG(i[2]) and i[3]==1
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ident(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def view():
 files={};dirs={'.':ident(P)}
 for p in sorted(P.rglob('*')):
  assert not p.is_symlink();i=ident(p);k=str(p.relative_to(P))
  if stat.S_ISREG(i[2]):files[k]=pin(p)
  else:assert stat.S_ISDIR(i[2]);dirs[k]=i
 for k,q in files.items():assert pin(P/k)==q
 for k,i in dirs.items():assert ident(P/k)==i
 return files,dirs
report=json.loads((P/'AUTHOR_SOURCE_CHECK.json').read_text())
assert report['source_only'] is True and report['check_count']==45 and report['all_checks_typed_true'] is True and report['blockers']==[] and all(type(v) is bool and v is True for v in report['checks'].values())
for q in report['all_parsed_Source_pins']:assert pin(Path(q['path']))==q
for q in (report['actual_installer_Source_pin'],report['actual_prelaunch_Source_pin'],report['complete_original_byte_inverse_pin'],report['complete_provenance_pin']):assert pin(Path(q['path']))==q
coverage=json.loads((P/'COMPLETE_275_PROVENANCE_COPY_FUTURE_D_BYTE_COVERAGE.json').read_text());assert coverage['complete_count']==275 and len(coverage['rows'])==275 and len({r['future_Root_D_destination_path'] for r in coverage['rows']})==275
for r in coverage['rows']:
 assert pin(Path(r['author_retained_byte_exact_Source_pin']['path']))==r['author_retained_byte_exact_Source_pin']
 assert r['author_retained_byte_exact_Source_pin']['sha256']==r['original_source_pin']['sha256'] and r['future_actual_destination_fullpin'] is None
inverse=json.loads((P/'COMPLETE_V22_UTILITY_SOURCE_BYTE_INVERSES.json').read_text())
for role,r in inverse['roles'].items():
 new=(P/role).read_text();back=new
 for h in reversed(r['hunks']):assert back.count(h['new'])==1;back=back.replace(h['new'],h['old'],1)
 assert back==(P/'ORIGINAL_ROLE_SOURCE'/role).read_text();ast.parse(new)
for p in sorted(P.rglob('*.py')):ast.parse(p.read_bytes(),filename=str(p))
mf=P/'MANIFEST.json';assert not mf.exists();mf.touch()
f,d=view();members={k:q for k,q in f.items() if k!='MANIFEST.json'}
m=dict(schema='V25_MONITOR_ACCESS_COMPLETE_INSTALLER_PRELAUNCH_UNREADY_SOURCE_MANIFEST_V1',status='SEALED_SOURCE_ONLY_UNREADY_REQUIRES_INDEPENDENT_ADMISSION_AND_ROOT_EXECUTION',source_only=True,member_count=len(members),complete_member_bytes=sum(q['size_bytes'] for q in members.values()),members=members,directories=d,author_Source_check_pin=pin(P/'AUTHOR_SOURCE_CHECK.json'),Source_installer_pin=pin(P/'Root_source_installer.py'),Source_prelaunch_pin=pin(P/'Root_prelaunch_checker.py'),complete_V22_role_byte_inverse_pin=pin(P/'COMPLETE_V22_UTILITY_SOURCE_BYTE_INVERSES.json'),complete275_future_D_byte_coverage_pin=pin(P/'COMPLETE_275_PROVENANCE_COPY_FUTURE_D_BYTE_COVERAGE.json'),actual_independent_Source_peer=None,actual_Root_installer_terminal=None,actual_Root_prelaunch_terminal=None,actual_BUILD_terminal=None,actual_native_binary=None,installer_prelaunch_or_guard_or_candidate_imported_or_executed=False,compiler_native_material_or_numeric_executed=False,project_D_E_C_ART_written=False,Source_or_science_qualification_self_granted=False,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
with mf.open('w') as fp:json.dump(m,fp,indent=2,allow_nan=False);fp.write('\n')
a,ad=view();assert set(a)==set(members)|{'MANIFEST.json'} and ad==d
for k,q in members.items():assert a[k]==q
print(json.dumps(dict(source_only=True,status=m['status'],manifest_pin=pin(mf),report_pin=pin(P/'AUTHOR_SOURCE_CHECK.json'),complete_files=len(a),complete_directories=len(d),all_members_full_EOF_SHA7ID_checked=True,actual_utility_executed=False,science_qualified=False)))
