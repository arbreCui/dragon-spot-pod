#!/usr/bin/env python3
"""Root independent source/evidence review; no candidate import or deletion."""
import ast,hashlib,json,os,stat
from pathlib import Path

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
SRC=REC/'storage_release_curated66_old_private_copies_source_v2_20261013'
OUT=REC/'ROOT_CURATED66_V2_SOURCE_ONLY_REVIEW_20261013.json'

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(p,wanted=None,body=False):
    p=Path(p);before=identity(p.lstat());assert stat.S_ISREG(before[2])
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        assert identity(os.fstat(fd))==before
        h=hashlib.sha256();pieces=[]if body else None
        while True:
            chunk=os.read(fd,2**20)
            if not chunk:break
            h.update(chunk)
            if body:pieces.append(chunk)
        assert identity(os.fstat(fd))==before
    finally:os.close(fd)
    assert identity(p.lstat())==before
    row=dict(path=str(p),sha256=h.hexdigest(),size_bytes=before[4],identity=before)
    if wanted is not None:assert row==wanted,str(p)
    return row,b''.join(pieces)if body else None

def main():
    assert not OUT.exists()
    sf,raw=read(SRC/'COMPLETE_CURATED66_OLD_PRIVATE_RELEASE_SOURCE_FREEZE.json',body=True)
    assert sf['sha256']=='c564a1de028286ec3fa5d29fbbde3d4e70776b5fe63831974916ac01aaaea73c'
    d=json.loads(raw);checks=[];pins=[]
    def check(name,condition):assert condition,name;checks.append(name)
    check('source_only_not_manifest_or_delete',d['manifest_prepared']is False and d['deletion_executed']is False and d['compiler_or_numerical_executed']is False)
    texts={}
    for row in d['Source_pins']+d['immutable_readonly_evidence_pins']+[d['original_resource_factory_pin']]:
        pin,data=read(row['path'],row,True);pins.append(pin)
        if str(Path(row['path']).parent)==str(SRC)and Path(row['path']).suffix=='.py':
            tree=ast.parse(data);compile(tree,row['path'],'exec');texts[Path(row['path']).name]=data.decode()
    common=texts['curated66_release_common.py'];tree=ast.parse(common)
    values={}
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name)and target.id in('TARGET_SELECTED_PINS','CAPS','BYTES'):
                    values[target.id]=ast.literal_eval(node.value)
    targets=values['TARGET_SELECTED_PINS'];paths={r['path']for r in targets}
    check('literal66_and_exact_bytes',len(targets)==len(paths)==66 and sum(r['size_bytes']for r in targets)==1751559764 and d['literal66_fullpins']==targets)
    check('unique_physical66',len({tuple(r['identity'][:2])for r in targets})==66)
    check('only_12_owners',len(d['literal12_owner_roots'])==12 and all(any(r['path'].startswith(root+'/')for root in d['literal12_owner_roots'])for r in targets))
    check('no_latest_v14_v12_ax_current_v3PACK',all('/20261013-v14/'not in p and '20261013-v12/'not in p and Path(p).name!='ax_current.xsm'and not('20261012-v3/AAA/initial_pack.xsm'in p)for p in paths))
    for row in targets:
        s=Path(row['path']).lstat();check('target7UID_'+str(len(checks)),identity(s)==row['identity']and s.st_uid==os.getuid()and s.st_nlink==1 and stat.S_ISREG(s.st_mode))
    check('all_original_caps',values['CAPS']==dict(SELF_mib=512,whole_seconds=1800,stage_seconds=600,threads=1,children_at_once=1,fresh_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20))
    verify=texts['verify_or_execute_curated66.py'];prepare=texts['prepare_curated66_manifest.py']
    check('no_abbreviation_and_one_literal_execute',"allow_abbrev=False"in verify and "sys.argv[1:].count('--execute')!=(1 if a.execute else 0)"in verify)
    check('readonly_default_before_unlink',verify.index('if not a.execute:')<verify.index('os.unlink(target.name,dir_fd=fd)'))
    check('exact_target_names_dirfd_no_glob',verify.count('os.unlink(')==1 and 'for target,row in zip(s.TARGETS,s.TARGET_SELECTED_PINS):'in verify and 'os.O_DIRECTORY|os.O_NOFOLLOW'in verify and 'os.stat(target.name,dir_fd=fd,follow_symlinks=False)'in verify)
    check('current_UID_nlink_all7_before_unlink',"s.identity(actual)!=row['identity']or actual.st_uid!=os.getuid()or actual.st_nlink!=1"in verify)
    check('fsynced_intent_before_unlink',verify.index("value['next_target_intent']=")<verify.index('rp=s.update_owned(rp_path,value,rp)')<verify.index('os.unlink(target.name,dir_fd=fd)'))
    check('actual_return_record_fsync_before_later_checks',verify.index('os.unlink(target.name,dir_fd=fd)')<verify.index("value['deletion_records'].append")<verify.index('now=s.identity(os.fstat(fd))'))
    check('same_receipt_all7_inode_fsync',all(s in common for s in ["receipt_pin(p)!=old",'os.O_RDWR|os.O_NOFOLLOW',"before!=old['identity']",'os.fsync(f.fileno())','after[:4]!=before[:4]']))
    check('same_parent_current7_each_file',"expected[str(target.parent)]=now"in verify and 'now[3]!=previous[3]-1'in verify and 'now[4]!=previous[4]-32'in verify)
    check('full_retained_other12_v14_v12_inventory_postcheck',all(s in verify for s in ["new['ordinary_file_identities']!=",'elif now!=old:','s.inventory([s.V14_OUT])','s.inventory([s.V12_OUT])']))
    check('history_exact_delta_and_fullfresh_reserve',"before['artifact_bytes']-after['artifact_bytes']!=s.BYTES"in verify and "after['original_initial_reserve_admitted']is not True"in verify)
    check('exact_old5625_minus30_no_target_double_role',all(s in common for s in ['len(oldrows)!=5625','explicit_after_migration5595_paths','target cannot also become protected','remaining5595_exact_rows_retained=True']))
    check('new2532_and_v14_377_preserved',"len(nh['dependencies'])!=2532"in common and "len(hf['dependencies'])!=377"in common and "entire_latest_v14_failed299_including_bothBQ_preserved"in common)
    check('closed_failure_is_failure_not_pass',"s['engineering_three_plane_closed0']is not False"in common and "s['actual_terminal']is not None"in common and "s['AAA_qualified']is not False"in common)
    check('real_no_writer_ps_lsof',"['/bin/ps','-axo','pid=,command=']"in common and "['/usr/sbin/lsof','-nP','+D',str(branch)]"in common and 'new build OUT must remain absent'in common)
    check('prepare_and_execute_recheck_scope',all(s in prepare for s in ['s.current_protection(sf,reviews)','s.closed_proofs()','s.writer_gate(protected)','s.inventory()!=before'])and 's.current_protection(sf,reviews)'in verify)
    report=dict(schema='ROOT_CURATED66_V2_INDEPENDENT_SOURCE_ONLY_REVIEW_V1',Source_freeze_pin=sf,
      failure=None,business_executed=False,candidate_imported=False,manifest_prepared=False,deletion_executed=False,
      compile_or_numerical_executed=False,checks=checks,actual_Source_evidence_full_EOF_pins=pins,
      target_count=66,target_logical_bytes=1751559764,target_current_all7_UID_single_link_checked=True,
      target_scientific_EOF_not_repeated_by_Source_review=True,MF_requires_all_protected_and_targets_current_full_EOF=True,
      no_new_build_or_reader_or_physics_qualification=True)
    with OUT.open('x',encoding='utf-8')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status='ROOT_CURATED66_SOURCE_ONLY_REVIEW_PASS',review_pin=read(OUT)[0],checks=len(checks),business_executed=False)))

if __name__=='__main__':main()
