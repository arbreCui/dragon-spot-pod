"""Root-only B4 archive publication after real SourceGEN0 and independent Source0."""
import argparse,importlib.util,json,os,shlex,sys
from pathlib import Path
BASE=Path(__file__).absolute().parent
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('review-pin','review-tools-pin','generation-tools-pin'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();spec=importlib.util.spec_from_file_location('B4_publish_common',BASE/'B2_physical_directory_archive_common.UNREADY.py');c=importlib.util.module_from_spec(spec);sys.modules[spec.name]=c;spec.loader.exec_module(c)
 ready=c.metadata(c.pin(BASE/'SOURCE_REVIEW_READY.json'));b=c.metadata(ready['execution_binding_pin']);pr=json.loads(a.review_pin);pt=json.loads(a.review_tools_pin);pg=json.loads(a.generation_tools_pin);review=c.metadata(pr)
 c.true0(pt,'actual_review_return','review_pin',pr);c.true0(pg,'actual_Source_preparation_return','ready_pin',c.pin(BASE/'SOURCE_REVIEW_READY.json'))
 c.require(review['source_only']is True and review['status']=='PASS_SOURCE_ONLY_CURRENT_SINGLE_B2_PHYSICAL_DIRECTORY_LOSSLESS_ARCHIVE'and review['failure']is None and review['binding_pin']==ready['execution_binding_pin']and review['complete_source_file_pins']==ready['complete_source_file_pins'],'same-round genuine independent exact B2 physical directory Source review0')
 for p in ready['complete_source_file_pins']:c.require(c.pin(p['path'])==p,'whole frozen Source through publication')
 for n in('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json'):c.require(not os.path.lexists(BASE/n),'publication once/no overwrite')
 sf=dict(schema='CURRENT_B2_SINGLE_PHYSICAL_DIRECTORY_LOSSLESS_ARCHIVE_SOURCE_FREEZE_V1',source_only=True,candidate_executed=False,execution_binding_pin=ready['execution_binding_pin'],complete_source_file_pins=ready['complete_source_file_pins'],independent_Source_review_pin=pr,independent_Source_review_tools_pin=pt,Root_Source_generation_true_tools_pin=pg)
 psf=c.write_new(BASE/'FINAL_SOURCE_FREEZE.json',sf,2*2**20);hf=dict(schema='CURRENT_B2_SINGLE_PHYSICAL_DIRECTORY_LOSSLESS_ARCHIVE_HOST_FREEZE_V1',selected_source_freeze_pin=psf,source_only=True,host_source_pin=ready['host_source_pin'],common_source_pin=ready['common_source_pin'],original_caps=c.CAPS,independent_Source_review_pin=pr,independent_Source_review_tools_pin=pt,Root_Source_generation_true_tools_pin=pg,Root_actual_exec_command_sandbox_permissions_required='require_escalated')
 phf=c.write_new(BASE/'FINAL_HOST_FREEZE.json',hf,2*2**20);argv=b['original_complete_ENV_Python_B_prefix']+[ready['host_source_pin']['path']]
 for role,p in(('source-freeze',psf),('host-freeze',phf)):argv+=['--'+role+'-summary',p['path'],'--'+role+'-sha256',p['sha256'],'--'+role+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
 c.require(len(argv)==24,'complete exact24 owning Root argv');cli=dict(schema='CURRENT_SINGLE_B2_PHYSICAL_DIRECTORY_LOSSLESS_ARCHIVE_FINAL_REVIEWABLE_ROOT_CLI_V1',argv=argv,command=shlex.join(argv),source_freeze_pin=psf,host_freeze_pin=phf,original_caps=c.CAPS,Root_actual_exec_command_sandbox_permissions_required='require_escalated',gzip_executed=False,files_deleted=False)
 pc=c.write_new(BASE/'FINAL_ROOT_REVIEWABLE_CLI.json',cli,2*2**20);print(json.dumps(dict(status='CURRENT_SINGLE_B2_PHYSICAL_DIRECTORY_ARCHIVE_FINAL_CLI_PUBLISHED_ONLY',CLI_pin=pc,gzip_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
