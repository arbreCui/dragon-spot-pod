import hashlib, json, os, stat, shutil, time
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
    sd=Path('/private/tmp/spot_v9_cold_actual_binding_full_source_independent_review_20261009')
    gd=Path('/private/tmp/axmat_v9_actual_cold_binding_graph_resource_independent_review_20261009')
    source,sp=read(sd/'REPORT.json','bfaf98e2a9038c0b1634f2a49be90fdacb025aed8c2bcf1e6adc3534cfb772f7')
    sr,srp=read(sd/'actual_readonly_tool_return.json','74b9172fc5e3e111e2314004f353d71bf4744cd73f99f0ef9120bd7ea391a03b')
    graph,gp=read(gd/'REPORT.json','03ebde650f63e045ae7a35f1018e02f787aac47fef28812a9a7a7fd719760e3c')
    gr,grp=read(gd/'actual_readonly_tool_return.json','34075c6b3c6f0e4197ab6e5ea93bd16b615ca25a3b38f6b57af87b6d8edaa1dd')
    joint,jp=read(gd/'joint_scope_binding.json','f6d7fe1efff715350daa344d74ce40f1416089270d09347f0f1dca54e151fe91')
    jr,jrp=read(gd/'actual_joint_readonly_tool_return.json','38bfc4346fd806b05124998ec01ff5aea1832dbdff7374d0128e74a11b0db5f5')
    assert source['status']==graph['status']==joint['status']=='PASS'
    for receipt in (sr,gr,jr):
        actual=receipt['actual_tool_result']
        assert type(actual['exit_code']) is int and actual['exit_code']==0 and actual['closed'] is True
    assert sr['actual_tool_result']['initial_chunk_id']=='1fb2f1'
    assert gr['actual_tool_result']==dict(initial_chunk_id='9a9803',session_id=71255,terminal_chunk_id='c050ac',exit_code=0,closed=True)
    assert jr['actual_tool_result']==dict(chunk_id='208936',exit_code=0,closed=True)
    assert joint['source_report']['sha256']==sp['sha256'] and joint['graph_report']['sha256']==gp['sha256']
    assert joint['source_actual_reader_tool']==sr['actual_tool_result'] and joint['graph_actual_reader_tool']==gr['actual_tool_result']
    for item in (sr['reader_source'],gr['reader_source'],jr['reader_source']):pin(item['path'],item['sha256'])
    for key in ('whole_scope_complementary_reports_pass','all24binding_fields_original_order_and_original_caps_pass','whole65_original7_and_trim73_plus_new7_complete_source_order_types_floatbits_pass','SOURCE31_environment1860_OUTPUT45_runtime31_preload7_guard6_complete','all391_module_owners_independently_expected','all11_compiled_originalPython314_callable_hashes_independently_source_equal','all235528rows_86namespaces_186aliases_445absences_complete','complete_mfiles37339_API_descriptor35675_retained','binding_no_self_file_pin'):
        assert joint[key] is True,key
    for key in ('binding_all24_AST_top_fields_original_order','original_SOURCE31_fullSHA_namespace','full1860_expected_environment_pins_and_whole_environment_body_preserved','original_PREP43_fullSHA_and_new_binding_only_added_to_output','runtime31_exact_flat_namespace_and7_preloads','all6_prior_guard_files_exact_original_order_fullSHA','entire_original_SerialExecutor_class_and_qualifyABA_resource_monitor_bytes_equal','whole_metadata_math_dtype_layout_original_source_contract_unchanged','all_pins_identity_before_after_stable'):
        assert source[key] is True,key
    assert source['producer_compile_python']=='3.14.4' and len(source['all11_compiled_callable_hashes_independently_source_compiled_under_original_Python'])==11
    for key in ('expected_files_complete_insertion_order_equal','all_module_owners_expected_independent','no_arbitrary_current_module_fresh_SHA_used_as_expected','whole65_complete_type_order_values_floatbits_equal','original_API_raw65_order_unchanged','strict_sorted_consumer_materialization_boundary_exact','new_actual_component_returns7_complete_type_order_floatbits_equal','full_dtype_layout_owner_trace_graph_content_unchanged','source31_full_SHA_and_identity_unchanged','new_OUTPUT43_local_files_prepared_and_binding45_full_SHA','runtime_namespace31_and_7preload_exact','terminal_exact9_fullSHA','strict_reservation_gate_passed','future_controls_prepared_cold_and_native_outputs_absent'):
        assert graph[key] is True,key
    for body in (source,joint):
        for key in ('new_binding_fixtures_executed','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','scientific_qualification'):assert body[key] is False,key
    assert graph['new_binding_fixtures_executed'] is False and graph['native_RSS_credit'] is False and graph['scientific_qualification'] is False
    obs,op=read(r/'Root_actual_V9_cold_binding_tool_return.json','c24ff19a49b77d904057faeb694faaeeaaa181c621850f62353f7a43c839ad98')
    real=dict(initial_chunk_id='ce453a',session_id=31625,terminal_chunk_id='13d167',exit_code=0,closed=True)
    assert obs['actual_tool_result']==joint['actual_Root_binding_tool']==source['actual_binding_tool']==graph['actual_binding_Root_tool']==real
    assert obs['actual_success_recorder_tool']==dict(chunk_id='2169ff',exit_code=0,closed=True)
    b,bp=read(obs['actual_binding']['path'],'4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930')
    terminal,tp=read(obs['binding_terminal']['path'],'d26300e92fc469bc1674f5c788b8806656791da817019d99d12daf6f912af1b1')
    assert type(terminal['returncode']) is int and terminal['returncode']==0 and terminal['transport_started'] is False
    assert bp['bytes']==60598579 and obs['actual_stdout_result']['classification']=='PREPARED_NEW_CANONICAL_BINDING_INPUT_ONLY_NO_FIXTURE_CREDIT'
    prep_admission,pp=read(r/'Root_actual_full_V9_cold_PREP_independent_admission.json','8fd5bd7965cb61030ce5423b642d5356267818694dc90935ba62f09c0f9e33c3')
    assert prep_admission['status']=='QUALIFIED_COMPLETE_ACTUAL_PREP_INPUT_ONLY_READY_FOR_UNIQUE_CANONICAL_BINDING'
    pins={}
    for rows in (source['all_fresh_pins'],list(graph['full_read_pins'].values()),list(joint['full_small_pins'].values())):
        for row in rows:
            prior=pins.get(row['path'])
            if prior is not None:assert prior['sha256']==row['sha256'] and prior['identity']==row['identity']
            pins[row['path']]=row
    for p,row in pins.items():
        assert identity(p)==row['identity'],p
        fresh=pin(p,row['sha256']);assert fresh['identity']==row['identity'],p
    work=Path(b['work_root']);term=Path(obs['binding_terminal']['path']).parent
    source_root=Path(obs['launch_command'][1]).parent
    admission_path=next(p for p in graph['additional_expected_files'] if p.endswith('/rank1_factor_cache_admission.json') and '/runtime/' not in p)
    m,mp=read(admission_path,graph['additional_expected_files'][admission_path])
    expected=dict(m['files']);expected.update(graph['additional_expected_files'])
    assert len(m['files'])==37339 and len(expected)==37395 and list(expected.items())==list(b['files'].items())
    assert digest(expected)==graph['expected_files_whole_sha256'] and len(b['module_owners'])==391
    for row in b['module_owners'].values():assert expected[row['path']]==row['sha256']
    assert len(joint['source_peer15_pending_owner_expectations_closed'])==15
    for row in joint['source_peer15_pending_owner_expectations_closed']:assert expected[row['path']]==row['sha256']
    original_caps=dict(rss_cap_mib=512,control_stage_seconds=60,control_total_seconds=120,control_archive_reserve_bytes=64*2**20,cold_total_seconds=43200,min_free_bytes=8*2**30,history_cap_bytes=96*2**30,threads=1,children_at_once=1,retries=0)
    assert b['caps']==source['original_CAPS_complete_typed_unchanged']==original_caps
    assert len(b['tested_guard_files'])==6 and len(b['runtime_namespace']['files'])==31 and len(b['runtime_module_owners'])==7
    policy=source['reference_policy_boundary'];assert policy==prep_admission['reference_policy_boundary']
    assert policy['unchanged_legacy_case_spec_active_batches']==250 and policy['separate_frozen_recipe_fixed_history_active_batches']==2000
    assert policy['first_active_statepoint']==101 and policy['last_active_statepoint']==2100 and len(policy['original_all8_checks_required'])==8 and policy['recipe_admitted_new_science_or_reference_result'] is False
    wire,wp=read(graph['graph_full_json_pin']['path'],graph['graph_full_json_pin']['sha256'])
    canonical={row['path']:row['sha256'] for row in wire['canonical_files']}
    assert len(canonical)==35647 and sum(row['size_bytes'] for row in wire['canonical_files'])==35803098221
    canonical_ids={p:identity(p) for p in canonical};metadata_ids={p:identity(p) for p in m['files']}
    assert digest(canonical_ids)==graph['complete_canonical_before_after_seven_field_identity_digest']
    assert digest(metadata_ids)==graph['metadata_before_after_identity_digest']
    assert [current_graph_namespace(row,canonical) for row in wire['namespaces']]==graph['namespaces_before_after86']
    assert aliases_and_absences(wire,canonical)==graph['aliases_absences_before_after']
    roots=dynamic_roots(b['resource_info']['resource_roots'],ART)
    assert roots==m['component_resource_roots']==b['resource_info']['resource_roots'] and len(roots)==236
    resources=resource_inventory(roots,ART);assert resources==graph['current_resources_after']
    free=shutil.disk_usage(ART).free;reserve=20971764748
    assert resources['artifact_bytes']+reserve<96*2**30 and free-reserve>=8*2**30
    assert not (work/'binding_controls').exists() and not Path(b['control_terminal_root']).exists() and not (work/'prepared_cold.json').exists()
    assert canonical_ids=={p:identity(p) for p in canonical} and metadata_ids=={p:identity(p) for p in m['files']}
    for p,row in pins.items():assert identity(p)==row['identity'],p
    dest=r/'cold_v9_actual_full_binding_independent_review';assert not dest.exists()
    dest.mkdir();copies=[]
    for directory,name in ((sd,'source_environment_MRO'),(gd,'graph_resources_joint')):
        for path in sorted(directory.rglob('*')):
            if path.is_dir():continue
            assert path.is_file() and not path.is_symlink()
            rec=pin(path);target=dest/name/path.relative_to(directory);target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as stream:stream.write(path.read_bytes())
            assert pin(target)['sha256']==rec['sha256'];copies.append(dict(source=rec,destination=str(target)))
    my_source=pin(__file__);target=dest/'Root_admission_source.py';target.write_bytes(Path(__file__).read_bytes());assert pin(target)['sha256']==my_source['sha256']
    copies.append(dict(source=my_source,destination=str(target)))
    result=dict(schema='AXMAT_ROOT_V9_ACTUAL_COLD_BINDING_FULL_COMPLEMENTARY_ADMISSION_V1',status='QUALIFIED_COMPLETE_ACTUAL_CANONICAL_BINDING_INPUT_ONLY_READY_FOR_UNIQUE_ORIGINAL_CONTROLS',observed_unix=time.time(),actual_binding_tool=real,actual_binding=bp,actual_binding_terminal=tp,actual_PREP_admission=pp,source_report=sp,graph_report=gp,joint_scope=jp,source_actual_tool=sr['actual_tool_result'],graph_actual_tool=gr['actual_tool_result'],joint_actual_tool=jr['actual_tool_result'],fresh_whole_source_and_metadata_pins=len(pins),fresh_fullSHA_scope_total_distinct_bytes=sum(row['identity'][3] for row in pins.values()),complete_expected_files=37395,module_owners=391,all11_compiled_code_Python314_source_proof_retained=True,inherited_full_canonical_inputs=dict(files=35647,bytes=35803098221,current_seven_field_identity_digest=digest(canonical_ids),new_full35GB_read=False),complete_graph_scope=dict(rows=235528,namespaces=86,aliases=186,absence_inputs=445,metadata_files=37339,descriptor_union=35675),current_complete_resources=resources,current_disk_free_bytes=free,original_all_caps=original_caps,reference_policy_boundary=policy,evidence_copies=copies,previous_goal_turn_classification='progress',previous_goal_progress_evidence='Actual complete binding source and graph postreviews and small complementary joint completed; latest storage preservation verified original goal inputs remain.',actual_controls_tool=None,new_binding_controls_executed=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False,source_derived_handoff_not_syscall_trace=True)
    target=r/'Root_actual_full_V9_cold_binding_independent_admission.json';assert not target.exists()
    with target.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status=result['status'],admission=pin(target),fresh_pins=len(pins),evidence_copies=len(copies),actual_controls_tool=None,scientific_qualification=False)),flush=True)

if __name__=='__main__':main()
