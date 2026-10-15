import hashlib,json,os,stat,shutil,time
from pathlib import Path
ROOT=Path("/Users/wen/spot")
ART=ROOT/"validation/artifacts"

def canonical_pieces(value):
    return json.JSONEncoder(sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).iterencode(value)

def digest(value):
    result = hashlib.sha256()
    for text in canonical_pieces(value):
        result.update(text.encode('utf-8'))
    return result.hexdigest()

def root_validation(roots, art):
    assert type(roots) is list and roots and all(type(p) is str for p in roots)
    paths = [Path(p) for p in roots]
    assert len(paths) == len(set(paths))
    for p in paths:
        assert p.is_absolute() and '..' not in p.parts and art in p.parents
        for ancestor in [p] + list(p.parents):
            if os.path.lexists(ancestor):
                s = ancestor.lstat()
                assert stat.S_ISDIR(s.st_mode) and not stat.S_ISLNK(s.st_mode), str(ancestor)
            if ancestor == art:
                break
    for i, p in enumerate(paths):
        assert not any(p in q.parents or q in p.parents for q in paths[i+1:])
    return paths

def dynamic_roots(declared, art):
    return sorted(set(declared) | {str(p) for p in art.glob('axial-material-*')})

def resource_inventory(roots, art):
    # Reproduce the inherited no-follow apparent-byte scope using only stdlib.
    # Regular hard links count per path, matching the original resource contract.
    root_validation(roots, art)
    total = 0
    regular = 0
    directories = 0
    symlinks_ignored = 0
    h = hashlib.sha256()
    def emit(kind, path, s):
        record = [kind, str(path), s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]
        h.update(json.dumps(record,separators=(',',':')).encode() + b'\n')
    def visit(path):
        nonlocal total, regular, directories, symlinks_ignored
        fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            s = os.fstat(fd)
            emit('directory',path,s)
            directories += 1
            with os.scandir(fd) as iterator:
                entries = sorted(iterator, key=lambda e:e.name)
            for entry in entries:
                p = path / entry.name
                s = entry.stat(follow_symlinks=False)
                if stat.S_ISDIR(s.st_mode):
                    visit(p)
                elif stat.S_ISREG(s.st_mode):
                    emit('regular',p,s)
                    total += s.st_size
                    regular += 1
                elif stat.S_ISLNK(s.st_mode):
                    emit('ignored_symlink',p,s)
                    symlinks_ignored += 1
                else:
                    emit('other_ignored',p,s)
        finally:
            os.close(fd)
    absent_roots = []
    for path in map(Path,roots):
        if os.path.lexists(path):
            visit(path)
        else:
            absent_roots.append(str(path))
    assert roots == dynamic_roots(roots, art)
    root_validation(roots, art)
    return dict(artifact_bytes=total,regular_files=regular,directories=directories,symlinks_ignored=symlinks_ignored,absent_declared_roots=absent_roots,
                full_path_identity_inventory_sha256=h.hexdigest(),scope='Original complete axial-family live resource roots; no symlink following; apparent bytes per regular path')

def current_graph_namespace(row,canonical):
    root=Path(row['canonical_root']); assert Path(row['root']).resolve(strict=True)==root and root.resolve(strict=True)==root
    assert row['namespace_exhaustive'] is True
    files={};dirs=[];links={}
    for base,names,leaves in os.walk(root,followlinks=False):
        base=Path(base)
        for name in names[:]:
            p=base/name;rel=str(p.relative_to(root))
            if p.is_symlink():
                target=p.resolve(strict=True); links[rel]=dict(kind='dir',target=str(target),text=os.readlink(p));names.remove(name)
            else: dirs.append(rel)
        for name in leaves:
            p=base/name;rel=str(p.relative_to(root))
            if p.is_symlink():
                target=p.resolve(strict=True);links[rel]=dict(kind='file' if target.is_file() else 'dir',target=str(target),text=os.readlink(p))
            else:
                assert str(p) in canonical and row['files'][rel]==canonical[str(p)]
                assert stat.S_ISREG(p.lstat().st_mode) and p.resolve(strict=True)==p
                files[rel]=canonical[str(p)]
    assert files==row['files'] and sorted(dirs)==row['directories'] and links==row['symlinks'],row['root']
    return dict(root=row['root'],canonical_root=str(root),files=len(files),directories=len(dirs),symlinks=len(links),expected_namespace_sha256=digest(row))

def aliases_and_absences(graph,canonical):
    observed=[]
    for row in graph['aliases']:
        p=Path(row['path']);assert p.is_symlink() and os.readlink(p)==row['text']
        resolved=p.resolve(strict=True);assert str(resolved)==row['target']
        assert row['kind']=='file' and resolved.is_file() and row['sha256']==canonical[str(resolved)]
        observed.append(dict(path=str(p),identity=identity(p),text=os.readlink(p),target=str(resolved)))
    absent=[]
    for p,expected in graph['absence_observations'].items():
        assert p in graph['absence_inputs'] and not os.path.lexists(p)
        assert expected['missing_errno']==2 and expected['observation']=='EXACT_DECLARED_ENOENT_ONLY' and expected['regular_input_bytes']==0
        for ancestor in expected['existing_ancestors']:
            literal=Path(ancestor['literal_component']);actual=literal.resolve(strict=True)
            assert str(actual)==ancestor['canonical_path']
            s=actual.lstat();wanted=ancestor['identity']
            assert dict(device=s.st_dev,inode=s.st_ino,mode=s.st_mode,rdev=s.st_rdev,major=os.major(s.st_rdev),minor=os.minor(s.st_rdev))==wanted
        assert not os.path.lexists(expected['first_missing_component'])
        absent.append(expected)
    assert len(observed)==186 and len(absent)==445
    return dict(alias_identity_digest=digest(observed),absence_observations_digest=digest(absent),aliases=186,absence_inputs=445)

def identity(path):
    s=Path(path).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def pin(path, expected=None):
    p=Path(path);before=identity(p)
    assert stat.S_ISREG(before[2]) and p.resolve(strict=True)==p,str(p)
    h=hashlib.sha256()
    with p.open('rb') as f:
        while block:=f.read(4*1024**2):h.update(block)
    assert identity(p)==before,str(p)
    if expected is not None:assert h.hexdigest()==expected,str(p)
    return dict(path=str(p),sha256=h.hexdigest(),bytes=before[3],identity=before)

def read(path, expected=None):
    result=pin(path,expected)
    def pairs(rows):
        value={}
        for k,v in rows:
            assert k not in value
            value[k]=v
        return value
    body=json.loads(Path(path).read_bytes(),object_pairs_hook=pairs)
    assert identity(path)==result['identity']
    return body,result

def main():
    r=ROOT/'validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009'
    sd=Path('/private/tmp/spot_v9_actual_controls_full_source_independent_review_20261009')
    gd=Path('/private/tmp/axmat_v9_actual_controls_graph_resource_scope_20261009')
    cd=Path('/private/tmp/axmat_v9_cold_actual_controls_postterminal_reader_20261009')
    s,sp=read(sd/'REPORT.json','9ffb0efce0a65dc8dd452c3e77e8a0475e254e5c1718a307e6a43ffd04a764be')
    sr,srp=read(sd/'actual_readonly_tool_return.json','0320a01e31efc180219c6c3d86b0891f947c2eb8057870edd66c01560785eca9')
    g,gp=read(gd/'REPORT.json','891ba5161ae1759187bd5f840419e2b1cc8125aba8865ffed4476121e30af0ba')
    gr,grp=read(gd/'actual_readonly_tool_return.json','6c05fc3dad643cd48ef5c5f4b3f5bd64366dbd2dcf8ad445811074de6d828147')
    j,jp=read(gd/'joint_scope_binding.json','c63a05ecefb484663216a73930f6e44747daba374a8ea3fbb90f22f3984822a8')
    jr,jrp=read(gd/'actual_joint_tool_return.json','94a7d2ed88f0d73a8172f35eca49844e5f21c83b45756796ca33c9509c9cafcc')
    c,cp=read(cd/'actual_readonly_REPORT.json','58b1d0061948b9d76b9d609114b9c8967b88d1b024f797eb78a2ebb8b12b458a')
    cr,crp=read(cd/'actual_readonly_postterminal_tool_receipt.json','415514b5ca5c6ff179c708e2f3055ef74bde31fc4fca4b0d0e976d574d6458ab')
    assert s['status']==g['status']==j['status']=='PASS' and c['status']=='PASS_ACTUAL_NEW_CANONICAL_THREE_CONTROLS_ONLY'
    for rec in (sr,gr,jr,cr):
        tool=rec['actual_tool_result'];assert type(tool['exit_code']) is int and tool['exit_code']==0 and tool.get('closed',rec.get('closed')) is True
    assert sr['actual_tool_result']['initial_chunk_id']=='e8ba44'
    assert gr['actual_tool_result']==dict(initial_chunk_id='bacc75',session_id=54568,terminal_chunk_id='3ba86f',exit_code=0,closed=True)
    assert jr['actual_tool_result']['initial_chunk_id']==jr['actual_tool_result']['terminal_chunk_id']=='43f4a9'
    assert cr['actual_tool_result']==dict(initial_chunk_id='444136',session_id=87440,terminal_chunk_id='2d03c2',exit_code=0)
    for rec,key in ((sr,'source'),(gr,'whole_executed_readonly_source'),(jr,'whole_source')):pin(rec[key]['path'],rec[key]['sha256'])
    pin(cd/'audit_actual_controls_readonly.py',cr['reader_source_sha256'])
    pin(cd/'actual_controls_config_ROOT_OBSERVED.json',cr['actual_configuration_sha256'])
    for key in ('SOURCE31_fullSHA_namespace','environment1860_complete_expected_fullSHA','moduleowners391_complete_current_fullSHA','runtime31_and7preloads_unchanged','prepared43_fullSHA','original18_source_functions_and6fullsources_exact','original_fullSerialExecutor_andresource_monitor_qualifyABA_source_exact','independent_CT3_exact','all_three_exact_watch_stage_log_intent_checks','sorted_result_watch_original_write_once_boundary_typed_floatbit_equal','Root_purewriter_exact_control_bind_only_inverse','source_only_future_None_plan_preserved','controls_only_qualification'):
        assert s[key] is True,key
    assert len(s['actual_mro_source_compile11_sha256'])==11 and len(s['actual_bounded_helper4_sha256'])==4
    for key in ('controls_complete_seal9_plus_self_fullSHA','controls_result_stages3_and_complete_raw_logs_watch_fields','short_genuine_wait4_kernel_at_least16MiB','oversize_actual_kernel_fields_retained_None_not_fabricated','normal_completion_missing_kernel_fields_never_defaulted_to0','all_graph_schema_typed_owners_dtype_layout_trace_content_retained','descriptor_union35675_unchanged','full_expected_ownerunion37395_independent_proof_inherited_and_whole_source_map_current_equal','module391_all_independent_expected_and_current_source_identities_preserved','whole65_original7_trim73_new7_complete_type_order_floatbits_equal','new_control_endpoints_separate_seal_not_backfilled_into_binding_map','binding_self_file_entry_absent','SOURCE31_OUTPUT45_base_TERM9_whole_original_byte_identity_unchanged','only_control_tree10_and_CT3_added','original_runtime31_flat_and_declared_sources_unchanged','archive_host_controls_binding_exact_source_rule','all4_actual_tail_fields_complete_and_original_caps_pass','original231_roots_retained','strong_future_AAA_reserve_gate_passed','future_prepared_cold_native_AAA_ABA_outputs_absent'):
        assert g[key] is True,key
    for key in ('history96GiB_free8GiB_future_reserve20971764748_preserved','control_archive_bytes61047970_of67108864','resource_roots236_retaining231','controls_only_qualification'):assert j[key] is True,key
    assert s['actual_controls_tool']==g['actual_Root_controls_tool']==j['actual_controls_tool']==dict(initial_chunk_id='085698',session_id=92301,terminal_chunk_id='5c78de',exit_code=0,closed=True)
    assert j['source_reader_actual_tool']==sr['actual_tool_result'] and j['graph_resource_reader_actual_tool']==gr['actual_tool_result']
    for body in (s,g,j,c):
        for key in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','scientific_qualification'):
            if key in body:assert body[key] is False,key
    obs,op=read(r/'Root_actual_V9_cold_controls_tool_return.json','f37d6f364d520c3f789dd71791d81f1f1e3e414dbfa3b6f88efa9c44439adfa1')
    assert obs['actual_tool_result']==s['actual_controls_tool']
    assert obs['actual_success_recorder_tool']==dict(chunk_id='0b84d1',exit_code=0,closed=True)
    terminal,tp=read(obs['control_terminal']['path'],'04f61e9377d468730ffd06cd3b511240d48ee881c5177b548c3b86e754c1747e')
    seal,sealp=read(obs['control_seal']['path'],'339f8385c45e4a196dba39cc4c6bf0753acbdc13953179456630bc6735a9f746')
    assert terminal['actual_tool_result']==dict(initial_chunk_id='085698',session_id=92301,terminal_chunk_id='5c78de',exit_code=0)
    assert set(terminal['actual_tool_result'])=={'initial_chunk_id','session_id','terminal_chunk_id','exit_code'}
    assert type(terminal['returncode']) is int and terminal['returncode']==0 and terminal['transport_started'] is False
    admission,ap=read(r/'Root_actual_full_V9_cold_binding_independent_admission.json','ae1577974abf75e738a3e74cc682ac3449ff3239ae617e1494dbeabeef33b726')
    assert admission['status']=='QUALIFIED_COMPLETE_ACTUAL_CANONICAL_BINDING_INPUT_ONLY_READY_FOR_UNIQUE_ORIGINAL_CONTROLS'
    pins={}
    for rows in (s['all_fresh_pins'],list(g['full_read_pins'].values()),list(j['all_reports_and_raw_source_receipts_fresh_sha256'].values())):
        for row in rows:
            if row['path'] in pins:assert pins[row['path']]['sha256']==row['sha256'] and pins[row['path']]['identity']==row['identity']
            pins[row['path']]=row
    for p,row in pins.items():
        assert identity(p)==row['identity'],p
        assert pin(p,row['sha256'])['identity']==row['identity'],p
    for row in c['read_pins']:pin(row['path'],row['sha256'])
    b,bp=read(obs['binding']['path'],'4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930')
    work=Path(b['work_root']);control=work/'binding_controls'
    stdout,stdoutpin=read(obs['full_stdout']['path'],obs['full_stdout']['sha256'])
    result,rp=read(control/'result.json',obs['actual_result_file']['sha256'])
    assert stdout['result']==result and set(stdout)=={'result','actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources'}
    for k in ('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources'):assert stdout[k]==terminal[k]
    assert stdout['actual_tail_check']=='PASS' and stdout['actual_elapsed_seconds']==91.97639445803361 and 0<stdout['actual_elapsed_seconds']<120
    assert stdout['actual_archive_bytes']==g['exact_archive_bytes']==61047970<64*2**20
    assert b['caps']==admission['original_all_caps'] and all(type(v) is int for v in b['caps'].values())
    assert result['caps']==b['caps'] and result['classification']=='PASS_NEW_CANONICAL_OWN_RSS_BINDING_CONTROLS_ONLY'
    assert [row['mode'] for row in result['observations']]==['positive','oversize','short']
    for row in result['observations']:
        watch=row['watch'];assert row['actual_group_no_longer_live'] is True and watch['own_child_only'] is True
        assert watch['rss_cap_mib']==512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=60
        if row['mode']=='oversize':
            assert watch['returncode'] in (-15,-9) and watch['sampled_peak_rss_mib']>=512 and watch['own_pid_wait4_observed'] is False
            assert all(watch[key] is None for key in ['own_pid_wait4_pid','own_pid_wait4_status','own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib'])
        else:
            assert watch['returncode']==0 and watch['own_pid_wait4_observed'] is True and watch['own_pid_wait4_pid']==watch['pid']
            assert watch['own_pid_wait4_peak_rss_mib']==watch['own_pid_wait4_ru_maxrss_bytes']/2**20
            assert watch['observed_peak_rss_mib']==max(watch['sampled_peak_rss_mib'],watch['own_pid_wait4_peak_rss_mib'])<512
            assert watch['own_pid_wait4_peak_rss_mib']>=16
    names=sorted(str(p.relative_to(control)) for p in control.rglob('*') if p.is_file())
    assert len(names)==10 and set(names)==set(seal['files'])|{'seal.json'}
    assert len(seal['namespace_directories'])==3
    for name,h in seal['files'].items():pin(control/name,h)
    bg,bgp=read(g['inherited_complete_binding_graph_report']['path'],g['inherited_complete_binding_graph_report']['sha256'])
    mpath=next(p for p in bg['additional_expected_files'] if p.endswith('/rank1_factor_cache_admission.json') and '/runtime/' not in p)
    m,mp=read(mpath,bg['additional_expected_files'][mpath]);expected=dict(m['files']);expected.update(bg['additional_expected_files'])
    assert list(expected.items())==list(b['files'].items()) and len(expected)==37395 and digest(expected)==g['expected_map_sha256']
    wire,wp=read(g['graph_whole_pin']['path'],g['graph_whole_pin']['sha256'])
    canonical={row['path']:row['sha256'] for row in wire['canonical_files']};canonical_ids={p:identity(p) for p in canonical};metadata_ids={p:identity(p) for p in m['files']}
    assert len(canonical)==35647 and digest(canonical_ids)==g['canonical_full_seven_field_beforeafter_digest']
    assert digest(metadata_ids)==g['metadata37339_beforeafter_identity_digest']
    assert [current_graph_namespace(row,canonical) for row in wire['namespaces']]==g['namespaces86_beforeafter']
    assert aliases_and_absences(wire,canonical)==g['aliases186_absences445_beforeafter']
    roots=dynamic_roots(b['resource_info']['resource_roots'],ART);assert len(roots)==236 and roots==m['component_resource_roots']
    resources=resource_inventory(roots,ART);assert resources==g['resource_after']
    assert resources['artifact_bytes']==c['fresh_independent_metadata_resources']['artifact_bytes']==72602503997
    free=shutil.disk_usage(ART).free;assert resources['artifact_bytes']+20971764748<96*2**30 and free-20971764748>=8*2**30
    assert not (work/'prepared_cold.json').exists() and not (work/'AAA').exists()
    assert canonical_ids=={p:identity(p) for p in canonical} and metadata_ids=={p:identity(p) for p in m['files']}
    for p,row in pins.items():assert identity(p)==row['identity'],p
    dest=r/'cold_v9_actual_full_controls_independent_review';assert not dest.exists();dest.mkdir();copies=[]
    for directory,name in ((sd,'source_environment_MRO'),(gd,'graph_resources_joint'),(cd,'complete_three_controls')):
        for p in sorted(directory.rglob('*')):
            if p.is_dir():continue
            assert p.is_file() and not p.is_symlink();rec=pin(p);q=dest/name/p.relative_to(directory);q.parent.mkdir(parents=True,exist_ok=True)
            with q.open('xb') as f:f.write(p.read_bytes())
            assert pin(q)['sha256']==rec['sha256'];copies.append(dict(source=rec,destination=str(q)))
    mine=pin(__file__);q=dest/'Root_admission_source.py';q.write_bytes(Path(__file__).read_bytes());assert pin(q)['sha256']==mine['sha256'];copies.append(dict(source=mine,destination=str(q)))
    report=dict(schema='AXMAT_ROOT_V9_ACTUAL_ORIGINAL_THREE_CONTROLS_FULL_COMPLEMENTARY_ADMISSION_V1',status='QUALIFIED_COMPLETE_ACTUAL_ORIGINAL_THREE_CONTROLS_ONLY_READY_FOR_UNIQUE_FINALIZATION',observed_unix=time.time(),actual_controls_tool=obs['actual_tool_result'],actual_control_terminal=tp,actual_control_seal=sealp,qualified_complete_binding_admission=ap,source_report=sp,graph_report=gp,joint_report=jp,complete_controls_report=cp,actual_source_review_tool=sr['actual_tool_result'],actual_graph_review_tool=gr['actual_tool_result'],actual_joint_tool=jr['actual_tool_result'],actual_complete_controls_review_tool=cr['actual_tool_result'],fresh_whole_source_and_metadata_pins=len(pins),complete_expected_files=37395,inherited_canonical_bytes=35803098221,canonical_files=35647,new_35GB_scientific_payload_read=False,original_caps=b['caps'],actual_elapsed_seconds=stdout['actual_elapsed_seconds'],actual_archive_bytes=stdout['actual_archive_bytes'],complete_resource_epochs=g['resource_epochs'],current_complete_resources=resources,current_disk_free_bytes=free,whole_control_namespace_files=names,actual_control_observations=result['observations'],reference_policy_boundary=s['reference_policy_boundary'],evidence_copies=copies,actual_finalization_tool=None,prepared_cold_sha256=None,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False)
    target=r/'Root_actual_full_V9_cold_controls_independent_admission.json';assert not target.exists()
    with target.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status=report['status'],admission=pin(target),fresh_pins=len(pins),evidence_copies=len(copies),native_RSS_verified=False)),flush=True)

if __name__=='__main__':main()
