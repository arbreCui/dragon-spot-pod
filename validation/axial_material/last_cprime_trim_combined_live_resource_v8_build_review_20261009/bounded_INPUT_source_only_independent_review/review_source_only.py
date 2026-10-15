import ast
import difflib
import hashlib
import json
import os
import stat
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('/private/tmp/spot_v8_bounded_input_source_independent_review_20261009')
D = Path('/private/tmp/axmat-trim-v8-bounded-runtime-input-intake-source-draft-20261009')
M = Path('/private/tmp/axmat-trim-v7-bounded-runtime-input-intake-source-draft-20261009')
A = Path('/Users/wen/spot/validation/axial_material')
START = time.monotonic()
PINS = {}

def identity(p):
    s = Path(p).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def read(p, expected=None):
    p = Path(p); a = identity(p)
    assert stat.S_ISREG(a[2]), str(p)
    b = p.read_bytes()
    assert a == identity(p)
    rec = dict(path=str(p),identity=a,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
    if isinstance(expected,str):
        assert rec['sha256']==expected, str(p)
    elif expected:
        for k in ['identity','sha256','bytes']:
            if k in expected:
                assert rec[k]==expected[k], (str(p),k)
    if str(p) in PINS:
        assert rec==PINS[str(p)]
    PINS[str(p)] = rec
    return b

def doc(p,expected=None):
    return json.loads(read(p,expected))

def assignments(tree):
    return {t.id:n.value for n in tree.body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}

def segment(s,n):
    lines=s.splitlines(keepends=True)
    start=sum(len(x) for x in lines[:n.lineno-1])+n.col_offset
    end=sum(len(x) for x in lines[:n.end_lineno-1])+n.end_col_offset
    return start,end,s[start:end]

def inverse(mother,candidate,expected_assignments,expected_if_index,nonversion_map):
    ms=mother.decode();cs=candidate.decode();mt=ast.parse(ms);ct=ast.parse(cs)
    assert len(mt.body)==len(ct.body)
    changed=[]; patches=[]
    for i,(mn,cn) in enumerate(zip(mt.body,ct.body)):
        _,_,old=segment(ms,mn);start,end,new=segment(cs,cn)
        if old==new:
            assert ast.dump(mn,include_attributes=False)==ast.dump(cn,include_attributes=False)
            continue
        assert type(mn)==type(cn)
        names=[x.id for x in cn.targets if isinstance(x,ast.Name)] if isinstance(cn,ast.Assign) else []
        if names:
            assert len(names)==1 and names[0] in expected_assignments, ('unapproved changed assignment',names)
            name=names[0]
        else:
            assert isinstance(cn,ast.If) and i==expected_if_index, ('unapproved changed statement',i)
            name='version_schema_guard'
        predicted=old.replace('v7','v8').replace('V7','V8')
        for oldpin,newpin in nonversion_map.items():
            predicted=predicted.replace(oldpin,newpin)
        assert predicted==new, ('nonidentity source change',i,name)
        changed.append(dict(index=i,node_type=type(cn).__name__,assignment_names=names,original_source=old,candidate_source=new))
        patches.append((start,end,old))
    assert {x['assignment_names'][0] for x in changed if x['assignment_names']}==set(expected_assignments)
    assert len(changed)==len(expected_assignments)+1
    restored=cs
    for start,end,old in sorted(patches,reverse=True):
        restored=restored[:start]+old+restored[end:]
    assert restored.encode()==mother
    compile(cs,'source-only-compile-never-executed','exec',dont_inherit=True)
    return dict(changed_top_level_nodes=changed,patch_regions=len(patches),all_other_source_including_whitespace_byteexact=True,full_inverse_byteexact=True,full_inverse_SHA256=hashlib.sha256(restored.encode()).hexdigest(),top_level_nodes=len(ct.body),compile_only_no_exec=True),ct,cs

def function_source(s,t,name):
    return ast.get_source_segment(s,next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name==name))

def main():
    handoff=doc(D/'STOPPED_handoff.json','ee153dfd1e0e2c00246719f534265e62b7328017f4c4beb188cd579314e2aa58')
    author=doc(D/'source_audit.json','ddaaab9c113235365c8395da90ea9a3916c439e39893623b0fac62a119c3b4f2')
    manifest=doc(D/'evidence_manifest.json','294ec723cd84af5f1ea9d76de2a839ea04606695410a280d5a9965698a86a062')
    findings=read(D/'SOURCE_FINDINGS.txt','9fd9bca2e218840ef973e3140d254c2a87d2b4e663523e61cc29419eb5162dcd').decode()
    wire=doc(D/'wire_compatibility_source_review.json','2e12e945426a3e400dbd05ce90acd63e602fcc597402383ad909ee599573de96')
    author_tools=doc(D/'actual_source_generation_and_static_tool_receipts.json','85dc687d073135ff304bcbdfda881a2c857b0d89b3b4a8cffda7c161dddfdd26')
    for rec in manifest['files']:
        read(rec['path'],rec)
    assert manifest['status']==handoff['status']=='STOPPED_SOURCE_ONLY_UNREADY'
    assert manifest['actual_new_host_API_or_Root_return_sha256'] is None
    assert len(handoff['actual_bindings'])==11 and all(x is None for x in handoff['actual_bindings'].values())
    assert handoff['independent_external_source_review'] is None
    hostpath=D/'axmat_trim_v8_standalone_bounded_runtime_api_intake_host_20261009.py'
    recorderpath=D/'axmat_trim_v8_standalone_bounded_runtime_api_intake_postterminal_recorder_20261009.py'
    oldhost=M/'axmat_trim_v7_standalone_bounded_runtime_api_intake_host_20261009.py'
    oldrec=M/'axmat_trim_v7_standalone_bounded_runtime_api_intake_postterminal_recorder_20261009.py'
    hb=read(hostpath,handoff['host']);rb=read(recorderpath,handoff['recorder'])
    mh=read(oldhost,author['mother_host']);mr=read(oldrec,author['mother_recorder'])
    assert PINS[str(hostpath)]['sha256']=='2c531b47705b3e617733b6d0d1bc37650b648cea8003a0dd9ec0c03b553b6481'
    assert PINS[str(recorderpath)]['sha256']=='301bb1f3683e7d5c3b4b336bdc19e59ef4520f6dcaa8d1911f0c2cc26dacfa2c'
    hp,ht,hs=inverse(mh,hb,['DRAFT_STATUS','FACTORY','FACTORY_SHA','OUT','TERM','BASE'],4,{'45783d9920a53ca517f28abbff9071e81cd29b0ef87336f45216aa86d8e4bc5a':'4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4'})
    rp,rt,rs=inverse(mr,rb,['BASE','OUT','HOST','HOST_SHA','COMPONENT_TERM','CMD','stdout'],41,{'c2c32ef178de27699fb8a50a1a08ff396b1f985f56ec18d290423073d5e1a0cd':'2c531b47705b3e617733b6d0d1bc37650b648cea8003a0dd9ec0c03b553b6481'})
    assert hp['patch_regions']==7 and rp['patch_regions']==8
    for name,proof in [('host',hp),('recorder',rp)]:
        old=doc(D/(name+'_v7_to_v8_source_inverse.json'))
        assert old['changed_top_level_nodes']==proof['changed_top_level_nodes']
        assert old['patch_regions_count']==proof['patch_regions'] and old['full_inverse_byteexact'] is True
    ha=assignments(ht);ra=assignments(rt)
    hostfuture={k:ast.literal_eval(ha[k]) for k in ['DECL_SHA','SEAL_SHA','RUN_SHA','PREP_SHA']}
    recfuture={k:ast.literal_eval(ra[k]) for k in ['DECL_SHA','SEAL_SHA','RUN_SHA','PREP_SHA','API_RETURN_SHA']}
    assert all(x is None for x in hostfuture.values()) and all(x is None for x in recfuture.values())
    assert ast.literal_eval(ha['DRAFT_STATUS'])=='UNREADY_ACTUAL_TRIM_V8_COMPONENT_AND_ROOT_BINDINGS_PENDING'
    assert ast.literal_eval(ra['DRAFT_STATUS'])=='UNREADY_ACTUAL_HOST_COMPONENT_AND_ROOT_BINDINGS_PENDING'
    assert isinstance(ht.body[4],ast.If) and isinstance(rt.body[4],ast.If)
    assert 'raise ValueError' in ast.get_source_segment(hs,ht.body[4]) and 'raise ValueError' in ast.get_source_segment(rs,rt.body[4])
    for text in [hs,rs]:
        for needle in ["loader.exec_module",".mkdir("]:
            assert text.index('if DRAFT_STATUS')<text.index(needle)
        assert 'consumer_scope' not in text and "['requirements']" not in text and "['rows']" not in text
    hostcommand=ha['command'];reccommand=ra['CMD']
    assert isinstance(hostcommand,ast.List) and isinstance(reccommand,ast.List) and len(hostcommand.elts)==len(reccommand.elts)==9
    assert [ast.literal_eval(hostcommand.elts[i]) for i in [2,3,5,7]]==['admit','--sha256','--terminal-evidence','--terminal-evidence-sha256']
    assert [ast.literal_eval(reccommand.elts[i]) for i in [2,3,5,7]]==['admit','--sha256','--terminal-evidence','--terminal-evidence-sha256']
    assert "runner.execute(BASE/'intake','admit',command,600)" in hs
    assert 'len(runner.records)!=1' in hs and 'resources=f.resources_for(d[\'resource_roots\'],c.ResourceFailure)' in hs
    assert 'full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,)' in hs
    assert 'runner=full.OwnRSSSerialExecutor(BASE,1800-(time.monotonic()-STARTED),FAMILY,resources)' in hs
    assert 'type(runner)is not full.OwnRSSSerialExecutor' in hs
    assert "f.require(OUT/'seal.json',SEAL_SHA)" in hs and "f.require(TERM/'terminal_return.json',RUN_SHA)" in hs
    assert "f.require(TERM/'declaration_terminal_return.json',PREP_SHA)" in hs
    assert 'if a.actual_exit_code!=0:raise ValueError' in rs
    assert 'stderr.stat().st_size!=0' in rs and 'r.strict(stdout)!=x' in rs
    payload=ra['payload'];assert isinstance(payload,ast.Dict)
    payloadnames=[ast.literal_eval(x) for x in payload.keys]
    assert payloadnames==author['nine_payload_names'] and len(set(payloadnames))==9
    assert "r.write(OUT/'Root_terminal_return.json',receipt)" in rs
    assert 'record_written_after_actual_tool_return=True' in rs
    assert "any(x[k]is not False for k in FALSE)" in rs
    assert author['source_mode_business_import_API_constructor_PREP_RUN_or_ART'] is False
    assert author_tools['actual_business_API_PREP_RUN_constructor_or_child_execution'] is False
    factory_path=A/'prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v8.py'
    fb=read(factory_path,handoff['producer']);assert PINS[str(factory_path)]['sha256']=='4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4'
    fs=fb.decode();ft=ast.parse(fs)
    admission=function_source(fs,ft,'production_admission')
    fn=next(n for n in ft.body if isinstance(n,ast.FunctionDef) and n.name=='production_admission')
    assert [x.arg for x in fn.args.args]==['seal_sha','terminal_evidence','terminal_evidence_sha256']
    assert not fn.args.vararg and not fn.args.kwarg and not fn.args.kwonlyargs and not fn.args.defaults
    assert hashlib.sha256(admission.encode()).hexdigest()==wire['formal_F8_production_admission_source_sha256']
    binding=function_source(fs,ft,'graph_input_bindings')
    assert binding==wire['F8_graph_input_bindings_source']
    assert hashlib.sha256(binding.encode()).hexdigest()==wire['F8_graph_input_bindings_source_sha256']
    assert 'for row in g.iter_graph_requirement_rows(graph):' in binding
    assert "files!=actual" in binding and "len(aliases)!=len(graph['aliases'])" in binding
    assert "table['rows']" not in binding
    for text in ["len(stages)!=5", "any(s['status']!='PASS' for s in stages)", "watches[:-1]!=audit['previous_stage_watchdogs']", "set(actual['files'])!=set(seal['files'])|{'seal.json'}", 'bodies,_=actual_components()', 'actual_components=bodies', 'historical_whole_component_body=BODY_BINDING']:
        assert text in admission, text
    actualcomponents=function_source(fs,ft,'actual_components')
    assert 'if bodies!=expected:raise ValueError' in actualcomponents and 'no field filtering' in actualcomponents
    for text in ['TOTAL_WALL, STAGE_WALL, RSS = 1800, 600, 512','RESERVE, HISTORY_CAP, FREE_FLOOR = 2*2**30, 96*2**30, 8*2**30',"TAIL_FIELDS = ('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')"]:
        assert text in fs
    config=doc(handoff['Root_config_observed_pin']['path'],handoff['Root_config_observed_pin'])
    assert '4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4' in json.dumps(config)
    helper_path=Path('/private/tmp/axmat_root_historical_owned_specs_combined_runtime_actual_bound_recorder_20261007.py')
    read(helper_path,'0b8a9a0a3b71bdea15269a14e54011d142e00c92979fbedef8ade3bcac7ec047')
    read(A/'combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py','1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643')
    read(A/'combined_runtime_current_predicates_private_declaration_lifetimes_20261009.py','2d9bf60b5a27d8cc32de5cc231e20b6caf65fa85f8c66d770124e0a0f1809b8f')
    specs=doc(A/'combined_runtime_complete_historical_input_specs_20261007.json','2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa')
    seven=specs['metadata']['historical_actual_components']
    assert set(seven)=={'capture','capture_scope_is_original_operator_only','combined_runtime_RSS_not_proved','dedup','mathematical_controls_inherited_not_newly_executed','original92','physical'}
    seven_sha=hashlib.sha256(json.dumps(seven,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()).hexdigest()
    assert seven_sha=='a0b0445e79f91f5d3767ee57719937a5188608f6a22f77d62b17c5036950e130'
    genuine=[(A/'qualify_refined_AAA_layered_full.py','70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'),(Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py'),'38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'),(Path('/Users/wen/spot/validation/artifacts/axial-material-rank1-factor-cache-build-20261007/runtime/run_bounded_dragon.py'),'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09')]
    for p,sha in genuine:
        read(p,sha)
    absentpaths=author['all_planned_intake_execution_and_durable_paths_absent']
    assert len(absentpaths)==4 and all(not os.path.lexists(x) for x in absentpaths)
    assert handoff['intake_WORK']==absentpaths[0] and handoff['durable_evidence_family']==absentpaths[1]
    for rec in PINS.values():
        assert identity(rec['path'])==rec['identity'],rec['path']
    pinsfile=OUT/'all_fresh_source_and_metadata_pins.json';pinsfile.write_text(json.dumps(sorted(PINS.values(),key=lambda x:x['path']),indent=2)+'\n')
    proofs=OUT/'complete_independent_inverse_proofs.json';proofs.write_text(json.dumps(dict(host=hp,recorder=rp),indent=2)+'\n')
    report=dict(schema='AXMAT_TRIM_V8_BOUNDED_INTAKE_INDEPENDENT_COMPLETE_SOURCE_REVIEW_V1',status='PASS',scope='Independent source-only identity retarget review; candidate remains STOPPED UNREADY',completed_utc=datetime.now(timezone.utc).isoformat(),host=PINS[str(hostpath)],recorder=PINS[str(recorderpath)],mother_host=PINS[str(oldhost)],mother_recorder=PINS[str(oldrec)],formal_factory=PINS[str(factory_path)],host_complete_inverse_regions=7,recorder_complete_inverse_regions=8,complete_whole_source_inverse_to_frozen_V7=True,only_approved_identity_fields_changed=True,all_numeric_bool_constants_and_nonidentity_AST_and_whitespace_preserved=True,host_four_future_actual_bindings=hostfuture,recorder_five_future_actual_bindings=recfuture,handoff_eleven_future_actual_bindings=handoff['actual_bindings'],candidate_draft_status=ast.literal_eval(ha['DRAFT_STATUS']),postterminal_draft_status=ast.literal_eval(ra['DRAFT_STATUS']),UNREADY_guards_precede_business_reads_imports_constructor_and_output=True,standard_API_signature_three_original_arguments=True,ordinary_canonical_CLI_tokens=9,no_consumer_scope_argument_no_partial_union_no_Mapping_no_alternate_entry=True,genuine_supervisor_module_parent_MRO_constructor_checks_unchanged=True,original_resource_roots_fresh_complete_checks_unchanged=True,caps=dict(total_wall_seconds=1800,stage_wall_seconds=600,RSS_mib=512,archive_bytes=2147483648,history_bytes=103079215104,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0),complete_seal_inventory_five_stage_four_tail_and_actual_Root_PREP_RUN_checks_preserved=True,whole_seven_key_INPUT=PINS[str(A/'combined_runtime_complete_historical_input_specs_20261007.json')],seven_body_keys=sorted(seven),seven_body_semantic_SHA256=seven_sha,host_recorder_no_legacy_graph_row_assumptions=True,formal_factory_strict_wire_accessor_and_full_canonical_and_alias_union_comparison_preserved=True,nine_payload_names=payloadnames,independent_tenth_Root_namespace='Root_terminal_return.json',Root_record_success_only_after_observed_true_exit0=True,merged_child_stdout_stderr_complete_no_separate_child_stderr_claim=True,whole_host_JSON_stderr_empty_stage_watch_metadata_and_source_repin_checks_preserved=True,four_planned_execution_durable_stdout_stderr_paths_absent=absentpaths,author_source_generation_tool_receipts_only=author_tools,source_pins_count=len(PINS),source_and_metadata_fresh_SHA_bytes=sum(x['bytes'] for x in PINS.values()),fresh_pins_file_sha256=hashlib.sha256(pinsfile.read_bytes()).hexdigest(),complete_inverse_file_sha256=hashlib.sha256(proofs.read_bytes()).hexdigest(),source_only_release_contract_PASS=True,actual_READY_source_not_authorized_by_this_review=True,actual_RUN_or_seal_or_API_or_Root_return_witness_created=False,actual_science_native_RSS_AAA_ABA_credit=False,project_or_ART_or_formal_writes=False,business_import_API_constructor_PREP_RUN_or_child_execution=False,files_deleted=0,compile_only_no_exec=True,limitations=['Identity-only source review accepts a stopped draft, not a bound READY host or business completion. Four host andfive recorder actual pins plus11 handoff future bindings remainNone.', 'Final successful V8 five-stage RUN, true Root receipts andseal must exist before new bound host source review and one actual standard intake. Recorder needs exact reviewed final host SHA andreal API stream only after true observed return0.', 'Formal wire helper andfactory are fresh source pins and AST-only contracts here; no graph business verification, constructor, API, stage execution or memory claim was performed.', 'Original postterminal recorder handles successful0 only. Failed business host terminal facts must be retained honestly by Root; this draft does not turn failure into a successful intake receipt.'],audit_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),elapsed_seconds=time.monotonic()-START)
    rpout=OUT/'REPORT.json';rpout.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',draft_status='STOPPED_SOURCE_ONLY_UNREADY',report=str(rpout),sha256=hashlib.sha256(rpout.read_bytes()).hexdigest(),host_inverse_regions=7,recorder_inverse_regions=8,all_future_None=True,source_pins=len(PINS),business_executed=False,elapsed_seconds=report['elapsed_seconds'])),flush=True)

try:
    main()
except Exception:
    (OUT/'failure_observation.json').write_text(json.dumps(dict(status='BLOCKED',error=traceback.format_exc(),formal_or_ART_writes=False,business_executed=False),indent=2)+'\n')
    raise
