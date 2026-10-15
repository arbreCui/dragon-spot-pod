"""Print a concrete Root CLI only with an actual closed first-A report fullpin.
Never launches the host, parser, compiler or native solver.
"""
import argparse,hashlib,json,os,shlex,stat
from pathlib import Path
BASE=Path(__file__).resolve().parent
def pin(p):
 p=Path(p);s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 if not p.is_absolute()or not stat.S_ISREG(s.st_mode)or s.st_nlink!=1 or any(v.is_symlink()for v in(p,*p.parents)):raise RuntimeError('literal regular fullpin')
 with p.open('rb')as f:
  s=os.fstat(f.fileno());opened=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
  if opened!=before:raise RuntimeError('open7ID')
  sha=hashlib.file_digest(f,'sha256').hexdigest();s=os.fstat(f.fileno());after=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 if after!=before or [getattr(p.lstat(),k)for k in('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')]!=before:raise RuntimeError('fullEOF7ID')
 return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
p=argparse.ArgumentParser()
for suffix in('summary','sha256','seven-id'):p.add_argument('--material-observation-report-'+suffix,required=True)
a=p.parse_args();actual=pin(a.material_observation_report_summary)
if actual['sha256']!=a.material_observation_report_sha256 or actual['identity']!=json.loads(a.material_observation_report_seven_id):raise RuntimeError('externally supplied actual material report fullpin')
d=json.loads(Path(actual['path']).read_text())
if d.get('schema')!='ACTUAL_CURRENT_FORMAL_A_MATERIAL_OBSERVATION_EXECUTION_V1'or d.get('status')!='ACTUAL_ONE_A_MATERIAL_STAGE_CLOSED0_EVIDENCE_ONLY'or d.get('failure')is not None or d.get('after_check_error')is not None or d.get('actual_full_A_observation_executed')is not True or d.get('actual_B_observation_executed')is not False:raise RuntimeError('one actual closed first A observation report required')
recipe=json.loads((BASE/'ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json').read_text())
for wanted in(recipe['selected_source_freeze_pin'],recipe['selected_host_freeze_pin'],recipe['host_source_pin']):
 if pin(wanted['path'])!=wanted:raise RuntimeError('frozen current Source exact fullpin')
argv=recipe['argv_prefix']+['--material-observation-report-summary',actual['path'],'--material-observation-report-sha256',actual['sha256'],'--material-observation-report-seven-id',json.dumps(actual['identity'],separators=(',',':'))]+recipe['final_output_option']
print(json.dumps(dict(schema='CONCRETE_CURRENT_GENDF_V4_ROOT_CLI_ONLY_NOT_EXECUTED',argv=argv,shell_safe_command=shlex.join(argv),actual_material_observation_report_pin=actual,requires_Root_true_BOOT_saved_science_and_full_actual_material_review=True,host_or_parser_launched=False),indent=2))
