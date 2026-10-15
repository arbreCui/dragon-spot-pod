"""Seal only authored SOURCE/text/AST/hash/META; no reviewed API imports."""
import ast
import hashlib
import json
from pathlib import Path
import stat

HERE=Path(__file__).absolute().parent

def require(value,message):
    if type(value)is not bool or not value:raise ValueError(message)

def pin(path):
    s=path.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    require(stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not path.is_symlink(),'complete ordinary SOURCE file required')
    with path.open('rb')as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    t=path.lstat();after=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
    require(before==after,'complete SOURCE EOF identity changed')
    return {'path':str(path),'sha256':sha,'size_bytes':s.st_size,'identity':before}

def main():
    manifest_path=HERE/'sealed_SOURCE_manifest.json';require(not manifest_path.exists(),'one finite new Source seal; existing seal never changed')
    c=json.loads((HERE/'SOURCE_CHECKS.json').read_text());require(c['source_only']is True and c['all_checks_passed']is True and c['check_count']==len(c['checks'])==273 and all(row['pass']is True for row in c['checks']),'all actual273 saved Source checks required')
    for name,p in c['final_source_pins'].items():require(pin(HERE/name)==p,'checked prototype Source SHA7ID unchanged')
    actual=json.loads((HERE/'actual_SOURCE_generation_final_tool_return.json').read_text());tr=actual['terminal_tool_return']
    require(actual['source_only']is True and actual['closed']is True and actual['actual_tool_terminal_return_observed']is True and type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr and tr['chunk_id']=='2dcc5f','actual Source generation true terminal0closed needed')
    files=[];directories=[]
    for p in sorted(HERE.rglob('*')):
        s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'no Source namespace aliases')
        if stat.S_ISDIR(s.st_mode):directories.append(str(p.relative_to(HERE)));continue
        require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'no omitted Source namespace special/hardlink entry')
        if p.suffix=='.py':ast.parse(p.read_bytes())
        elif p.suffix=='.json':json.loads(p.read_bytes(),parse_constant=lambda v:(_ for _ in()).throw(ValueError('nonfinite Source META')))
        row=pin(p);row['relative_path']=str(p.relative_to(HERE));files.append(row)
    require(bool(files)and sum(r['size_bytes']for r in files)<8*2**20,'finite full SOURCE package bound8MiB')
    value={'schema':'CURRENT150_AB_FULL_RAWRECORD_BINDING_GENUINEHOST_PROTOCOL_COMPLETE_UNREADY_SOURCE_SEAL_V1','status':'SOURCE_ONLY_STATIC_SELF_CHECKED_UNREADY_PENDING_NEW_INDEPENDENT_REVIEW_AND_ACTUAL_ROOT_BINDING','source_only':True,'package_path':str(HERE),'files':files,'directories':directories,'members_excluding_manifest':len(files),'bytes_excluding_manifest':sum(r['size_bytes']for r in files),'Source_checks':273,'complete_original_UNREADY_Source_package_and_manifest_preserved':True,'complete_original378_source_peer_preserved_no_newcredit':True,'original_wrapper_sha256':'098b2a463877767254441ad49dd61076c0adb3320adf2d6c521e7abebac44116','prototype_source_pins':c['final_source_pins'],'all_original_genuine_source_modules_copied_without_import':True,'full_genuine_host_adaptation_inverse_hunks':12,'actual_future_READY_wrapper_global_hunks':3,'actual_future_READY_protocol_status_hunks':1,'actual_future_READY_host_global_hunks':13,'future_declared_positive_controls':5,'future_declared_negative_controls':10,'all_real_material_Source_admission_and_success_SHA_fields_unknown':None,'original_caps':{'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_archive_bytes':2*2**30,'history_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children_at_once':1,'retries':0},'actual_source_generation_terminal_chunk':'2dcc5f','actual_source_generation_typed_integer_exit_code':0,'source_failures_preserved':['cae376','033a1c','c0e888'],'actual_material_payload_opened_decoded':False,'reviewed_api_import_call_compile_or_business_executed':False,'actual_Source_admission_created':False,'actual_READY_files_created':False,'actual_protocol_qualified':False,'actual_full_rawrecord_transfer_qualified':False,'actual_genuine_runtime_RSS_resource_or_Root_terminal_created':False,'original_XSM_memory_bits_verified':False,'reaction_multiplicity_verified':False,'physical_neutron_balance_qualified':False,'scientific_accuracy_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'canonical_project_D_E_or_oldsealed_written':False,'predicted_RSS_or_runtime_success':False}
    with manifest_path.open('x')as f:json.dump(value,f,allow_nan=False,ensure_ascii=True,indent=2);f.write('\n')
    result=pin(manifest_path)
    print(json.dumps({'source_only':True,'status':value['status'],'sealed_manifest':result,'members_excluding_manifest':len(files),'bytes_excluding_manifest':value['bytes_excluding_manifest'],'actual_runtime_or_science_qualification_created':False},allow_nan=False),flush=True)

if __name__=='__main__':main()
