"""Root-only member0 byte restoration control. Never opens original m.xsm data.

This is UNREADY Source. It requires genuine failed-archive Root1/child1 and a
separate failure-facts post0. It emits no restored product and starts no child.
"""
import argparse,json,os,time
from pathlib import Path

BASE=Path(__file__).absolute().parent

def main():
    started=time.monotonic()
    ap=argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--binding-pin',required=True);ap.add_argument('--source-pin',required=True)
    args=ap.parse_args()
    with(BASE/'ROOT_MEMBER0_CONTROL_CLAIM.json').open('x')as f:
        json.dump(dict(schema='ROOT_EXCLUSIVE_B4_MEMBER0_RESTORE_BYTE_CONTROL_CLAIM_V1',Root_PID=os.getpid(),started_monotonic=started,argv=__import__('sys').argv,claim_before_project_import_or_product_IO=True,children_started=0,retries=0),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    import gzip,hashlib,importlib.util,resource,shlex,stat,sys
    def need(v,m):
        if v is not True:raise RuntimeError(m)
    def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    def own_source_bytes():
        total=0
        for q in BASE.rglob('*'):
            s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'new Source has no alias')
            if stat.S_ISREG(s.st_mode):total+=s.st_size
        return total
    def light():
        peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
        need(peak<512*2**20 and time.monotonic()-started<600,'Root SELF512MiB/stage600s from initial claim')
        need(own_source_bytes()<16*2**20,'entire new Source/metadata16MiB')
        return peak
    def current(p):
        light();need(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int and len(p['identity'])==7 and all(type(n)is int for n in p['identity']),'exact integer four-field fullPF')
        q=Path(p['path']);s=q.lstat()
        need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1 and ids(s)==p['identity']and s.st_size==p['size_bytes'],'exact owned ordinary metadata/member current7')
        return q
    def metadata(p):
        q=current(p);need(p['size_bytes']<8*2**20,'small control metadata8MiB')
        with q.open('rb')as f:
            need(ids(os.fstat(f.fileno()))==p['identity'],'opened metadata7');raw=f.read();need(ids(os.fstat(f.fileno()))==p['identity'],'metadata EOF7')
        need(len(raw)==p['size_bytes']and hashlib.sha256(raw).hexdigest()==p['sha256'],'metadata fullEOF SHA');current(p);return json.loads(raw)
    def source_bytes(p):
        q=current(p);need(q.suffix=='.py'and p['size_bytes']<2*2**20,'explicit bounded Python Source only')
        raw=q.read_bytes();need(hashlib.sha256(raw).hexdigest()==p['sha256'],'whole frozen Source SHA');current(p);return raw
    def genuine(v,key,code):
        r=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==code and type(r['exit_code'])is int and r['exit_code']==code and r.get('session_id')is None,'genuine original closed integer tool return')
        return r
    light();binding_pin=json.loads(args.binding_pin);self_pin=json.loads(args.source_pin)
    need(Path(self_pin['path'])==Path(__file__).absolute(),'explicit exact executing Source role');source_bytes(self_pin)
    b=metadata(binding_pin)
    need(b['schema']=='ROOT_CURRENT_B4_MEMBER0_RESTORATION_BYTE_CONTROL_BINDING_V1'and b['actual_preconditions_closed']is True and b['actual_failed_archive_and_post_roles_audited']is True,'NULL draft cannot authorize member byte IO')
    need(b['only_member0_restore_bytes_control']is True and b['all4_archive_completed']is False and b['original_m_xsm_body_must_not_be_opened']is True and b['Root_stage_seconds']==600 and b['new_Source_metadata_hard_bound_bytes']==16*2**20 and b['new_owning_ledger_root_created']is False,'only bounded member0 control, no whole4 completion or new output root')
    common_pin=b['frozen_B4_common_Source_pin'];source_bytes(common_pin)
    spec=importlib.util.spec_from_file_location('B4_member0_original_frozen_common',common_pin['path']);c=importlib.util.module_from_spec(spec);sys.modules[spec.name]=c;spec.loader.exec_module(c);current(common_pin)
    need(c.CAPS==b['original_caps']and c.CAPS==dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0),'all unchanged original caps')
    need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and Path(sys.executable).resolve()==c.PYTHON and all(os.environ.get(k)=='1'for k in c.THREADS),'original interpreter/thread1/unoptimized/unprofiled')
    archive_binding=metadata(b['original_B4_execution_binding_pin']);roots=archive_binding['complete_joint_roots'];out=Path(archive_binding['planned_actual_output_root'])
    need(roots==b['complete_joint_roots']and roots[-1]==str(out)and any(BASE.is_relative_to(Path(r))for r in roots)and len(roots)==len(set(roots))and out.is_dir(),'entire existing73-root binding retained; no c.admit fresh-output gate')
    cp=b['actual_failed_archive_closure_pins'];host=metadata(cp['Host']);raw=metadata(cp['Root_tools']);first=metadata(cp['first_failure']);watch=metadata(cp['watchdog']);post=metadata(cp['post']);posttools=metadata(cp['post_tools']);supplement=metadata(cp['supplement']);supplementtools=metadata(cp['supplement_tools'])
    actual=genuine(raw,'actual_terminal_return',1);pt=genuine(posttools,'actual_review_return',0)
    need(raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False,'original failed archive guard permission/no retry')
    cli=metadata(b['original_B4_final_CLI_pin']);need(shlex.split(raw['exact_executed_command'])==cli['argv']and len(cli['argv'])==24,'genuine failed Root command is exact original published24 argv')
    need(json.loads(pt['output'].strip().splitlines()[-1])['review_pin']==cp['post'],'genuine separate failure-facts post0 binds exact review PF')
    st=genuine(supplementtools,'actual_review_return',0);need(json.loads(st['output'].strip().splitlines()[-1])['review_pin']==cp['supplement'],'genuine independent child1/entry0 supplement post0')
    need(host['schema']=='ACTUAL_CURRENT_B4_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1'and host['status']=='FAILED_ARCHIVE_NO_RETRY_ALL_ORIGINALS_RETAINED'and host['failure']is not None and host['archive_complete']is False and host['all4_original_products_current7_retained']is True and host['binding_pin']==b['original_B4_execution_binding_pin']and host['complete_joint_roots']==roots and host['original_caps']==c.CAPS,'original failed archive is still failed, whole4 originals retained')
    need(len(host['records'])==1 and host['records'][0]['status']=='FAILED'and host['records'][0]['error']=='own-child stage failed; no retry'and host['actual_watchdog']is None,'actual original failed child record and absent Host watchdog preserved, no synthetic child0/child1 insertion')
    record=host['records'][0]
    need(cp['watchdog']['path']==str(out/(record['label']+'.watchdog.json'))and watch['command']==record['command']and type(watch['returncode'])is int and watch['returncode']==1 and watch['limit_failure']is None and watch['rss_cap_mib']==512 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600,'actual original child1/logical payload failure within unchanged original guard')
    ep=b['retained_member0_entry_pin'];entry=metadata(ep);original=b['original_member0_saved_full_pin'];pgz=b['complete_member0_gzip_pin']
    need(cp['first_failure']['path']==str(out/'FIRST_ARCHIVE_FAILURE.json')and ep['path']==str(out/'archive_entry_000.json')and first['phase']=='ARCHIVE_1'and first['failure']=="RuntimeError('all4 gzip payload below56MiB; no compression assumption')"and first['completed_entry_pins']==[ep]and first['original_product_files_deleted']is False and first['retry_performed']is False,'exact real phase1 cap failure and sole completed entry0')
    need(entry['ordinal']==0 and entry['original_plain_full_pin']==original==archive_binding['all4_product_pins'][0]and entry['compressed_archive_full_pin']==pgz and original['path']==str(Path(archive_binding['all4_product_pins'][0]['path']))and Path(original['path']).name=='m.xsm'and pgz['path']==str(out/'archives/000_m.xsm.gz'),'only exact original member0 and complete compressed member0')
    need(entry['compression_input_SHA']==entry['streamed_decompressed_SHA']==original['sha256']and entry['compression_input_length']==entry['streamed_decompressed_length']==original['size_bytes']==76594248 and pgz['size_bytes']==33559716 and entry['exact_original_plain_bytes_recoverable']is True and entry['original_plain_preserved']is True,'original saved member0 stream proof matches exact declared fullPF')
    k=b['actual_failure_post_key_projection'];need(all(type(v)is str for v in k.values()),'actual independent failure-post field roles audited after real closure')
    need(post['schema']==k['schema']and post['status']==k['status']and post['failure']is None and post['metadata_only']is True and post[k['Host_pin_field']]==cp['Host']and post[k['Root_tools_pin_field']]==cp['Root_tools']and type(post[k['Root_integer_exit_code_field']])is int and post[k['Root_integer_exit_code_field']]==1 and post[k['recorded_child_codes_field']]==[]and all(p in post[k['all_new_output_pins_field']]for p in(ep,pgz,cp['first_failure'],cp['watchdog'])),'original truthful limited post0 preserves recorded child-codes empty; binds ten new output PFs without inventing child1')
    sk=b['actual_failure_supplement_key_projection'];need(all(type(v)is str for v in sk.values()),'supplement actual schema/field roles audited after genuine closure')
    need(supplement['schema']==sk['schema']and supplement['status']==sk['status']and supplement['failure']is None and supplement['metadata_only']is True and supplement[sk['Host_pin_field']]==cp['Host']and supplement[sk['Root_tools_pin_field']]==cp['Root_tools']and supplement[sk['original_failure_post_pin_field']]==cp['post']and supplement[sk['original_failure_post_tools_pin_field']]==cp['post_tools']and supplement[sk['first_failure_pin_field']]==cp['first_failure']and supplement[sk['watchdog_pin_field']]==cp['watchdog']and supplement[sk['entry0_pin_field']]==ep and supplement[sk['gzip0_pin_field']]==pgz and supplement[sk['original0_pin_field']]==original and type(supplement[sk['child_integer_exit_code_field']])is int and supplement[sk['child_integer_exit_code_field']]==1,'new independent supplement explicitly binds actual child1/firstfailure/entry0 after preserving original limited post')
    for p in archive_binding['all4_product_pins']+archive_binding['retained_native_current7_pins']+archive_binding['original_B_native_and_readonly_input_current7_pins']:current(p)
    # c.Resources preloads the original production_inputs before original
    # production/history modules, without invoking any compiler/production main.
    # It keeps the entire original joint/history/cold/meta/free/open-unlinked
    # accounting and the original B4 output/Source component bounds.
    resources=c.Resources(archive_binding,started,600);last_full_completed=0.0;snapshots=[]
    def compact_snapshot(v):
        # Keep the original classes' actual scalar facts, including all byte,
        # free-space and checked-time fields. Root topology is separately bound
        # in complete_joint_roots; repeated directory inventories are omitted.
        scalar=(str,int,float,bool,type(None));r={k:x for k,x in v.items()if isinstance(x,scalar)}
        for k in('original_history','complete_joint'):r[k]={n:x for n,x in v[k].items()if isinstance(x,scalar)}
        r['complete_joint_root_count']=len(roots);r['non_scalar_resource_inventories_omitted']=True
        return r
    def budget(force=False):
        nonlocal last_full_completed
        light();resources.light()
        if force or time.monotonic()-last_full_completed>=5.0:
            v=resources.check();light();last_full_completed=time.monotonic();saved=compact_snapshot(v);snapshots.append(saved);return saved
    before=budget(True)
    # Original m.xsm remains only a current7 role. Neither metadata() nor
    # source_bytes() is ever called with original or a product input pin.
    original_ids_before=ids(Path(original['path']).lstat());current(original)
    def blind_gzip_sha():
        q=current(pgz);h=hashlib.sha256();n=0
        with os.fdopen(os.open(q,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
            need(ids(os.fstat(f.fileno()))==pgz['identity'],'opened complete gzip7')
            while True:
                budget();chunk=f.read(2**20)
                if not chunk:break
                n+=len(chunk);need(n<=pgz['size_bytes'],'complete gzip compressed length bounded');h.update(chunk)
            need(ids(os.fstat(f.fileno()))==pgz['identity'],'complete gzip fullEOF7')
        need(n==pgz['size_bytes']and h.hexdigest()==pgz['sha256'],'complete gzip fullEOF SHA/length exactPF');current(pgz);return dict(sha256=h.hexdigest(),size_bytes=n)
    gzip_before=blind_gzip_sha();budget(True);decompressed_sha=hashlib.sha256();decompressed_length=0;complete=False
    q=current(pgz)
    with os.fdopen(os.open(q,os.O_RDONLY|os.O_NOFOLLOW),'rb')as raw_gzip:
        need(ids(os.fstat(raw_gzip.fileno()))==pgz['identity'],'opened decompression gzip7')
        with gzip.GzipFile(fileobj=raw_gzip,mode='rb')as stream:
            while True:
                budget();chunk=stream.read(2**20)
                if not chunk:complete=True;break
                decompressed_length+=len(chunk);need(decompressed_length<=original['size_bytes'],'decompression bounded by saved original byte length');decompressed_sha.update(chunk)
        need(ids(os.fstat(raw_gzip.fileno()))==pgz['identity'],'after gzip complete member EOF7')
    need(complete and decompressed_length==original['size_bytes']and decompressed_sha.hexdigest()==original['sha256'],'full member0 decompressed bytes SHA/length equal saved original fullPF; no numerical decode')
    budget(True);gzip_after=blind_gzip_sha();need(gzip_before==gzip_after,'gzip whole bytes unchanged before/after independent restoration proof')
    for p in archive_binding['all4_product_pins']+archive_binding['retained_native_current7_pins']+archive_binding['original_B_native_and_readonly_input_current7_pins']:current(p)
    need(ids(Path(original['path']).lstat())==original_ids_before,'original member0 current7 unchanged, its body never read')
    for p in(binding_pin,ep,cp['Host'],cp['Root_tools'],cp['first_failure'],cp['watchdog'],cp['post'],cp['post_tools'],cp['supplement'],cp['supplement_tools']):metadata(p)
    source_bytes(self_pin);source_bytes(common_pin);after=budget(True)
    report=dict(schema='ROOT_CURRENT_B4_MEMBER0_INDEPENDENT_RESTORATION_BYTE_CONTROL_REPORT_V1',status='PASS_CURRENT_B4_MEMBER0_COMPLETE_GZIP_RESTORABLE_ORIGINAL_BYTES_ONLY',failure=None,binding_pin=binding_pin,Source_pin=self_pin,frozen_original_B4_common_Source_pin=common_pin,original_B4_execution_binding_pin=b['original_B4_execution_binding_pin'],actual_failed_archive_closure_pins=cp,retained_member0_entry_pin=ep,original_member0_saved_full_pin=original,complete_member0_gzip_pin=pgz,gzip_blind_SHA_length_before=gzip_before,gzip_blind_SHA_length_after=gzip_after,streamed_decompressed_SHA=decompressed_sha.hexdigest(),streamed_decompressed_length=decompressed_length,streamed_complete_member0_verified=True,all4_original_products_current7_retained=True,original_member0_body_opened=False,original_member0_format_or_numeric_values_decoded=False,restored_product_file_written=False,children_started=0,original_private_guard_Source_or_class_modified=False,original_failed_Root_integer_exit_code=1,original_failed_child_integer_exit_code=1,original_limited_failure_post_recorded_child_codes=[],original_failed_archive_still_failed=True,all4_archive_complete=False,complete_joint_roots=roots,new_owning_ledger_root_created=False,original_caps=c.CAPS,Root_SELF_peak_bytes=light(),Root_elapsed_seconds=time.monotonic()-started,resources_before=before,resources_after=after,original_resource_scalar_snapshots=snapshots,new_Source_metadata_hard_bound_bytes=16*2**20,final_report_resource_check_passed=False,files_deleted=False,retirement_authorized=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    target=BASE/'ROOT_MEMBER0_INDEPENDENT_RESTORE_BYTE_CONTROL_REPORT.json';raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<4*2**20 and own_source_bytes()+len(raw)<16*2**20,'bounded owning new Source/report metadata16MiB')
    with target.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    dfd=os.open(BASE,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(dfd)
    finally:os.close(dfd)
    final=budget(True);report['resources_after_including_summary_bytes']=final;report['final_report_resource_check_passed']=True
    previous=target.lstat();before_report_ids=ids(previous);raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<4*2**20 and own_source_bytes()-previous.st_size+len(raw)<16*2**20,'own summary rewrite within Source16MiB')
    with os.fdopen(os.open(target,os.O_WRONLY|os.O_NOFOLLOW),'wb')as f:
        need(ids(os.fstat(f.fileno()))==before_report_ids and previous.st_uid==os.getuid()and previous.st_nlink==1,'only own exact one-link report before rewrite');f.seek(0);f.truncate(0);f.write(raw);f.flush();os.fsync(f.fileno())
    need(ids(target.lstat())[:4]==before_report_ids[:4],'same own summary inode/link role');budget(True)
    s=target.lstat();reportpin=dict(path=str(target),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=ids(s))
    print(json.dumps(dict(status=report['status'],report_pin=reportpin,member0_only=True,all4_archive_complete=False,files_deleted=False)),flush=True)

if __name__=='__main__':main()
