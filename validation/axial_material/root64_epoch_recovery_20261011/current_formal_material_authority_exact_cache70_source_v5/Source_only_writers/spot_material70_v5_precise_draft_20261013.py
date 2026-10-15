from pathlib import Path
import ast,hashlib,json,os,shutil
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011');OLD=REC/'current_formal_material_authority_exact_cache70_source_v4';NEW=REC/'current_formal_material_authority_exact_cache70_source_v5';NEW.mkdir()
def pin(p):
 s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert [getattr(p.lstat(),k)for k in('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')]==i
 return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=i)
def write(p,d):
 with p.open('x')as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def save(n,b):
 with(NEW/n).open('xb')as f:f.write(b)
def replace(b,a,z):assert b.count(a)==1,(a[:100],b.count(a));return b.replace(a,z)
baseinverse=json.loads((OLD/'COMPLETE_CURRENT70_CURRENT_MATERIAL_SOURCE_INVERSE.json').read_bytes())
for row in baseinverse['entire_byte_copy_pins']:
 p=Path(row['copy']['path']);save(p.name,p.read_bytes())
helper=(OLD/'current_material_prerequisite_admission.py').read_text()
helper=replace(helper,"    table={p['path']:p for p in boot['output_pins']}\n    for original,compact in zip(raw['records'],boot['records']):", "    table={p['path']:p for p in boot['output_pins']}\n    refusals={case['original_execution_record_index']:case for case in boot['actual_operator_refusals']}\n    require(len(refusals)==33 and set(refusals)=={i for i,r in enumerate(boot['records'])if r['status']=='FAILED'},\n      'one exact full refusal authority for every actual negative stage')\n    for index,(original,compact)in enumerate(zip(raw['records'],boot['records'])):")
helper=replace(helper,"          0<=watch['sampled_peak_rss_mib']<512 and table[str(lp)]['sha256']==compact['log_sha256'],\n          'each actual original successful or intended-refusal child fully closed')", "          0<=watch['sampled_peak_rss_mib']<512,\n          'each actual original successful or intended-refusal child fully closed')\n        if compact['status']=='PASS':\n            require(table[str(lp)]['sha256']==compact['log_sha256'],\n              'actual positive complete log digest from original successful record')\n        else:\n            case=refusals[index]\n            require(compact['error']=='own-child stage failed; no retry'and\n              case['original_execution_record_label']==compact['label']and\n              case['actual_log_pin']==table[str(lp)]and case['actual_watchdog_pin']==table[str(wp)],\n              'actual FAILED record has exact same full log/watch PF refusal authority; no synthetic record fields')")
helper=replace(helper,"def replace_owned_failure_summary(c,path,wanted,value):", "def check_original_host_limits(c,start):\n    require(type(start)in(int,float)and time.monotonic()-start<1800 and\n      c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss<512*2**20,\n      'original owning whole1800 and SELF512 must pass after final publication and resources scan')\n\n\ndef replace_owned_failure_summary(c,path,wanted,value):")
save('current_material_prerequisite_admission.py',helper.encode())
for name in('build_current_observation_runtime.py','produce_current_formal_material_observations.py','run_current_material_lineage_evidence.py','current_material_lineage_evidence.py','prepare_current_material_evidence_requests.py'):
 b=(OLD/name).read_text()
 if name=='build_current_observation_runtime.py':
  b=replace(b,"SOURCE=REC/'current_formal_material_authority_exact_cache70_source_v4'","SOURCE=REC/'current_formal_material_authority_exact_cache70_source_v5'")
  b=replace(b,'from current_material_prerequisite_admission import admit_prerequisites,replace_owned_failure_summary','from current_material_prerequisite_admission import admit_prerequisites,replace_owned_failure_summary,check_original_host_limits')
  b=replace(b,'    try:c.check_full_current(fixed,owned);resources.check()\n    except BaseException as error:', '    try:c.check_full_current(fixed,owned);resources.check();check_original_host_limits(c,start)\n    except BaseException as error:')
 elif name=='produce_current_formal_material_observations.py':
  b=replace(b,'from current_material_prerequisite_admission import replace_owned_failure_summary','from current_material_prerequisite_admission import replace_owned_failure_summary,check_original_host_limits')
  b=replace(b,"        require(time.monotonic()-start<1800,'original whole1800');resources.check()", "        require(time.monotonic()-start<1800,'original whole1800');resources.check();check_original_host_limits(c,start)")
  b=replace(b,'    try:c.check_full_current(fixed,owned);resources.check()\n    except BaseException as error:', '    try:c.check_full_current(fixed,owned);resources.check();check_original_host_limits(c,start)\n    except BaseException as error:')
 elif name=='run_current_material_lineage_evidence.py':
  b=replace(b,'from current_material_prerequisite_admission import replace_owned_failure_summary','from current_material_prerequisite_admission import replace_owned_failure_summary,check_original_host_limits')
  b=replace(b,'    try:c.check_full_current(fixed,owned);resources.check()\n    except BaseException as error:', '    try:c.check_full_current(fixed,owned);resources.check();check_original_host_limits(c,start)\n    except BaseException as error:')
 save(name,b.encode())
for p in NEW.glob('*.py'):ast.parse(p.read_bytes())
write(NEW/'UNFROZEN_PRECISE_V5_DRAFT_SCOPE.json',dict(schema='UNFROZEN_CURRENT70_MATERIAL_V5_PRECISE_GATE_REPAIR_DRAFT_ONLY',base_v4_namespace=str(OLD),old_v4_fullpins=[pin(p)for p in sorted(OLD.iterdir())if p.is_file()],precise_scope=['PASS uses real log_sha256; all33 original FAILED require their exact fullPF actual_operator_refusal log/watch/recordIndex/label, no fake log_sha field','final build summary, producer phase+manifest and evidence summary force whole1800 and SELF512 after current pin/resources checks, same owned FD FAILURE publication','build executing Source namespace v5'],old_numerical_or_mathematical_Source_changed=False,new_source_frozen=False,new_source_or_host_imported=False,compiler_or_material_or_science_business_executed=False))
print(json.dumps(dict(status='UNFROZEN_V5_PRECISE_DRAFT_WRITTEN_AWAIT_FULL_FIELD_REVIEW',directory=str(NEW),Python_Source_count=len(list(NEW.glob('*.py'))))))
