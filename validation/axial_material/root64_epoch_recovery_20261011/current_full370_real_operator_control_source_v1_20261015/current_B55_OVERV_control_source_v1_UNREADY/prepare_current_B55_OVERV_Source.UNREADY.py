"""Root-only current B55 Source preparation; no SQL/science/helper/compiler/native stage."""
import argparse,ast,importlib.util,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
def need(v,m):
 if v is not True:raise RuntimeError(m)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--admission-packet-pin',required=True);a=ap.parse_args()
 need(not any(os.path.lexists(BASE/n)for n in('PLAN.json','SOURCE_REVIEW_READY.json')),'Source generation once/no overwrite')
 q=BASE/'B55_owning_Source_contract.UNREADY.py';spec=importlib.util.spec_from_file_location('B55_prepare_contract',q);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 author=m.metadata(m.pin(BASE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json'));need(author['Source_only_frozen_before_Root_generation']is True and author['native_or_compiler_executed_by_author']is False and author['Source_preparer_or_publisher_executed_by_author']is False,'author Source only; Root sole executor')
 for p in author['whole_Source_file_pins']:need(m.pin(p['path'])==p,'whole author-frozen Source')
 packet=m.metadata(json.loads(a.admission_packet_pin));build,bm,descriptor,selected,bridge,capture_binding,latest=m.admit(packet)
 need(all(packet[k]is None for k in('actual_B_native_control_report_pin','actual_B_integer_control_report_pin','actual_B_control_Root_tools_pin','actual_B_control_post_pin','actual_B_control_post_tools_pin')),'no actual current B controls invented before execution')
 before=0
 for root in packet['complete_joint_roots']:
  if not Path(root).exists():continue
  for p in Path(root).rglob('*'):
   s=p.lstat();need(not stat.S_ISLNK(s.st_mode),'whole latest namespace no aliases')
   if stat.S_ISREG(s.st_mode):before+=s.st_size
 for p in packet['explicit_cumulative_metadata_file_pins']:
  bm.current_metadata_role(p,build)
  if not any(Path(p['path']).is_relative_to(Path(root))for root in packet['complete_joint_roots']):before+=p['size_bytes']
 need(before+m.OUTPUT_BOUND+m.SOURCE_BOUND<2*2**30,'whole current prefix plus complete control16MiB+Source16MiB under original2GiB; actual Root checks open-unlinked')
 for p in author['whole_Source_file_pins']:
  if p['path'].endswith('.py'):ast.parse(Path(p['path']).read_text())
 table={Path(p['path']).name:p for p in author['whole_Source_file_pins']};plan=dict(packet,source_only=True,Source_only_current_cumulative_bytes_before_reservations=before,Source_generation_SQL_pool_or_science_body_opened=False,Source_generation_compiler_or_native_executed=False)
 m.write(BASE/'PLAN.json',plan);pp=m.pin(BASE/'PLAN.json');ready=dict(schema='CURRENT_B55_OVERV_CONTROL_SOURCE_REVIEW_READY_V1',source_only=True,control_plan_pin=pp,complete_source_file_pins=author['whole_Source_file_pins'],host_source_pin=table['run_guarded_current_B55_OVERV_control.UNREADY.py'],contract_Source_pin=table['B55_owning_Source_contract.UNREADY.py'],control_Fortran_Source_pin=table['OVERV_original_mixed_precision_control.f'],integer_oracle_Source_pin=table['OVERV_integer_rounding_oracle.py'],dependencies=m.unique([json.loads(a.admission_packet_pin),pp]+packet['explicit_control_metadata_pins']),original_caps=m.CAPS,SQL_pool_science_compiler_or_native_executed=False)
 m.write(BASE/'SOURCE_REVIEW_READY.json',ready);print(json.dumps(dict(status='CURRENT_B55_OVERV_SOURCE_PREPARED_ONLY',ready_pin=m.pin(BASE/'SOURCE_REVIEW_READY.json'),compiler_executed=False,native_executed=False)),flush=True)
if __name__=='__main__':main()
