import argparse,hashlib,json,os,stat
from pathlib import Path
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
A=Path('/Users/wen/spot/validation/artifacts')
D=B/'actual_complete_native_AB_persisted_XSM_ASCII_v23_sources'
E=B/'actual_complete_native_AB_persisted_XSM_ASCII_v23_receipts'
H=A/'axial-material-complete-native-AB-persisted-XSM-ASCII-host-v23-20261010'
O=A/'axial-material-complete-native-AB-persisted-XSM-ASCII-output-v23-20261010'
C=A/'axial-material-complete-native-AB-persisted-XSM-ASCII-controls-v23-20261010'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);i=identity(p);assert p.is_absolute() and p.resolve()==p and stat.S_ISREG(i[2]) and i[3]==1
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    assert identity(p)==i
    return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def snapshot(root):
    if not os.path.lexists(root):return dict(root=str(root),present=False,files={},directories={},symlinks={})
    assert root.is_dir() and not root.is_symlink();files={};dirs={'.':identity(root)}
    for p in sorted(root.rglob('*')):
        assert not p.is_symlink();k=str(p.relative_to(root));i=identity(p)
        if stat.S_ISREG(i[2]):files[k]=pin(p)
        else:assert stat.S_ISDIR(i[2]);dirs[k]=i
    for k,q in files.items():assert pin(root/k)==q
    for k,q in dirs.items():assert identity(root/k)==q
    return dict(root=str(root),present=True,files=files,directories=dirs,symlinks={})
def read(p,sha=None):
    q=pin(p)
    if sha is not None:assert q['sha256']==sha
    d=json.loads(p.read_text());assert pin(p)==q;return d,q
def write(p,d):
    with p.open('x') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n')
def bytes_in(views):return sum(q['size_bytes'] for v in views for q in v['files'].values())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--tool-receipt',required=True);ap.add_argument('--tool-receipt-sha256',required=True);ap.add_argument('--prelaunch',required=True);ap.add_argument('--prelaunch-sha256',required=True);ap.add_argument('--writer-sha256',required=True)
    a=ap.parse_args();writer=pin(Path(__file__).absolute());assert writer['sha256']==a.writer_sha256
    receipt,rpin=read(Path(a.tool_receipt),a.tool_receipt_sha256);tr=receipt['terminal_tool_return']
    assert receipt['schema']=='ROOT_V23_ACTUAL_COMPLETE_NATIVE_TOOL_TERMINAL_RETURN_V1' and receipt['closed'] is True and receipt['observed_terminal'] is True and receipt['session_repolled_after_close'] is False
    assert type(tr['exit_code']) is int and 'session_id' not in tr and receipt['actual_terminal_chunk']==tr['chunk_id']
    pre,ppin=read(Path(a.prelaunch),a.prelaunch_sha256);assert pre['schema']=='ROOT_V23_NATIVE_COMPLETE_SOURCE_PRELAUNCH_AND_FROZEN_E_V1' and pre['native_executed'] is False
    assert snapshot(D)==pre['complete_D_frozen']
    current_E=snapshot(E)
    for k,q in pre['complete_E_frozen_before_actual_launch']['files'].items():assert current_E['files'][k]==q
    host=None;report=None;watch=None;success=False
    if (H/'result.json').exists():host,_=read(H/'result.json')
    if (O/'ACTUAL_COMPLETE_NATIVE_XSM_ASCII_EVIDENCE_REPORT.json').exists():report,report_pin=read(O/'ACTUAL_COMPLETE_NATIVE_XSM_ASCII_EVIDENCE_REPORT.json')
    if (H/'native_run/native_xsm_ascii.watchdog.json').exists():watch,_=read(H/'native_run/native_xsm_ascii.watchdog.json')
    if tr['exit_code']==0:
        assert host is not None and report is not None and watch is not None and not (H/'failed_host_result.json').exists()
        assert host['schema']=='CURRENT150_AB_GENUINE_COMPLETE_NATIVE_PERSISTED_XSM_ASCII_HOST_V1'
        assert host['status']=='ACTUAL_SAVED_COMPLETE_NATIVE_PERSISTED_BYTE_EVIDENCE_ONLY_EXTERNAL_ROOT_CLOSURE_REVIEW_REQUIRED'
        assert {k:report_pin[k] for k in ('path','sha256','identity')}==host['actual_native']['report']
        assert host['original_caps']==CAPS and report['original_caps']==CAPS
        assert report['schema']=='ACTUAL_COMPLETE_NATIVE_PERSISTED_XSM_ASCII_BIT_EVIDENCE_ONLY_V1'
        assert host['native_persisted_XSM_value_bits_verified'] is True and report['native_persisted_XSM_value_bits_verified'] is True and report['all_complete_state_scope_retained'] is True
        assert [r['state'] for r in report['states']]==['A','B']
        for row in report['states']:
            assert row['native_persisted_XSM_value_bits_verified'] is True
            m=row['complete_MACROLIB'];assert (m['records'],m['physical_headers_including_all_closes'],m['numeric_components'])==(19619,19990,2264113)
            for name in ('complete_MACROLIB','complete_MICROLIB'):
                assert all(row[name][k] is True for k in ('all_persisted_native_value_bits_equal_ASCII','native_physical_preorder_equal_original_ASCII','all_complete_orders_preserved_on_disk'))
        assert type(watch['returncode']) is int and watch['returncode']==0 and watch['limit_failure'] is None and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
        assert 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and watch['rss_cap_mib']==512
        assert host['actual_native']['watchdog']==watch and host['whole_seconds']<1800 and len(host['stage_records'])==1 and host['stage_records'][0]['status']=='PASS'
        for obj in (host,report):
            for k in ('scientific_accuracy_qualified','AAA_accuracy_qualified','ABA_admitted'):assert obj[k] is False
        success=True
    views=[snapshot(p) for p in (H,O,C,D,E)];assert bytes_in(views)<2*2**30
    ns=dict(schema='ROOT_V23_ACTUAL_NATIVE_COMPLETE_POSTCLOSE_NAMESPACES_V1',namespaces=views,actual_tool_receipt=rpin,prelaunch=ppin,writer=writer,all_current_files_full_EOF_SHA7ID=True,complete_D_unchanged=True,all_original_E_files_unchanged=True,E_directory_identity_after_postclose_appends_claimed_unchanged=False,namespace_snapshot_before_this_manifest_and_summary_append=True,no_new_numeric_or_guard_API_executed=True)
    f=E/'Root_actual_complete_native_postclose_namespace_manifest.json';write(f,ns)
    summary=dict(schema='ROOT_V23_ACTUAL_COMPLETE_NATIVE_PERSISTED_BYTE_POSTCLOSE_SUMMARY_V1',status='ACTUAL_COMPLETE_NATIVE_PERSISTED_BYTE_EXIT0_ONLY_PENDING_INDEPENDENT_SAVED_REVIEW' if success else 'ACTUAL_NATIVE_NONZERO_NO_RETRY_NO_QUALIFICATION',actual_tool_receipt=rpin,actual_exit_code=tr['exit_code'],closed=True,actual_prelaunch=ppin,namespace_manifest=pin(f),original_caps=CAPS,native_persisted_XSM_value_bits_verified=success,all_complete_A_B_scopes_retained_and_verified=success,actual_native_byte_qualification_sha256=None,original_XSM_memory_bits_verified=False,original_native_build_binary_Source_linkage_qualified=False,new_native_walker_controls_actual_run=None,physical_neutron_balance_qualified=False,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False,outer_tool_output_scope='ACTUAL_EXEC_COMMAND_MERGED_EXTERNAL_HOST_STDOUT_STDERR',separate_external_host_stderr_saved=False,independent_external_host_stderr_empty_verified=False,actual_outer_watchdog=watch,actual_child_report=pin(O/'ACTUAL_COMPLETE_NATIVE_XSM_ASCII_EVIDENCE_REPORT.json') if report is not None else None,actual_host_result=pin(H/'result.json') if host is not None else None,actual_failed_host_result=pin(H/'failed_host_result.json') if (H/'failed_host_result.json').exists() else None,complete_D_unchanged=True,all_original_E_files_unchanged=True,new_numeric_execution_by_writer=False,cleanup_performed=False)
    f=E/'Root_actual_complete_native_postclose_summary.json';write(f,summary)
    final=[snapshot(p) for p in (H,O,C,D,E)];assert bytes_in(final)<2*2**30
    print(json.dumps(dict(status=summary['status'],summary=pin(f),joint_bytes_after_metadata_capture=bytes_in(final),native_actual_exit_code=tr['exit_code'],scientific_accuracy_qualified=False)))
if __name__=='__main__':main()
