"""Root-only single presence archive Source preparation; no payload IO or gzip."""
import argparse,ast,importlib.util,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--binding-pin',required=True);a=ap.parse_args()
 with(BASE/'ROOT_SOURCE_PREPARATION_CLAIM.json').open('x')as f:json.dump(dict(schema='ROOT_SINGLE_BAGG_PRESENCE_SOURCE_PREPARATION_ONCE_CLAIM_V1',PID=os.getpid(),product_bytes_opened=False,gzip_executed=False),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 q=BASE/'presence_archive_common.UNREADY.py';spec=importlib.util.spec_from_file_location('single_presence_prepare_common',q);c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
 c.require(not any(os.path.lexists(BASE/n)for n in('PLAN.json','SOURCE_REVIEW_READY.json')),'Source preparation once/no overwrite')
 author=c.metadata(c.pin(BASE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json'))
 c.require(author['Source_only_frozen_before_Root_generation']is True and author['Source_preparer_or_publisher_executed_by_author']is False and author['product_byte_IO_gzip_or_compiler_executed_by_author']is False,'author Source only, Root sole executor')
 for p in author['whole_Source_file_pins']:c.require(c.pin(p['path'])==p,'whole author frozen Source')
 pb=json.loads(a.binding_pin);b=c.metadata(pb);template=c.metadata(author['whole_NULL_admission_binding_template_pin']);mutable=set(author['Root_final_binding_fields_filled_after_genuine_bridge0'])
 c.require(set(b)==set(template)and all(b[k]==v for k,v in template.items()if k not in mutable),'final Root binding changes only explicit future actual bridge/resource-table gate fields')
 out=c.admit(b);c.require(not os.path.lexists(out),'fresh single archive once output root')
 context=c.metadata_role_context(b);current=0
 for root in b['complete_joint_roots']:
  if not Path(root).exists():continue
  for p in Path(root).rglob('*'):
   s=p.lstat();c.require(not stat.S_ISLNK(s.st_mode),'entire dynamic prefix no aliases')
   if stat.S_ISREG(s.st_mode):current+=s.st_size
 for p in b['explicit_cumulative_metadata_file_pins']:
  c.current_metadata(p,b,context)
  if not any(Path(p['path']).is_relative_to(Path(root))for root in b['complete_joint_roots']):current+=p['size_bytes']
 c.require(current+c.OUT_CAP+c.SOURCE_CAP<2*2**30,'complete current prefix/actual bridge metadata plus worst32MiB archive andSource16 within original2GiB; no compression assumption')
 for p in author['whole_Source_file_pins']:
  if p['path'].endswith('.py'):ast.parse(Path(p['path']).read_text())
 table={Path(p['path']).name:p for p in author['whole_Source_file_pins']};plan=dict(b,Source_only_current_cumulative_bytes_before_reservations=current,Source_generation_product_payload_opened=False,Source_generation_gzip_executed=False)
 pp=c.write_new(BASE/'PLAN.json',plan,4*2**20);ready=dict(schema='CURRENT_BAGG_SINGLE_PRESENCE_ARCHIVE_SOURCE_REVIEW_READY_V1',source_only=True,execution_binding_pin=pp,Root_completed_admission_binding_pin=pb,complete_source_file_pins=author['whole_Source_file_pins'],host_source_pin=table['run_guarded_single_Bagg_presence_archive.UNREADY.py'],common_source_pin=table['presence_archive_common.UNREADY.py'],worker_source_pin=table['archive_single_Bagg_presence.UNREADY.py'],writer_source_pin=table['publish_single_Bagg_presence_archive_CLI.UNREADY.py'],original_caps=c.CAPS,product_payload_opened=False,gzip_executed=False)
 pr=c.write_new(BASE/'SOURCE_REVIEW_READY.json',ready,2*2**20);print(json.dumps(dict(status='CURRENT_SINGLE_BAGG_PRESENCE_ARCHIVE_SOURCE_PREPARED_ONLY',ready_pin=pr,product_payload_opened=False,gzip_executed=False)),flush=True)
if __name__=='__main__':main()
