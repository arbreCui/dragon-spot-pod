import ast
import hashlib
import json
import os
from pathlib import Path

T=Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v8-root-execution-20261009')
OUT=Path('/private/tmp/axmat_trim_v8_root_recorder_config_independent_review_20261009')
ROOT=Path('/Users/wen/spot')
CANDIDATE=Path('/private/tmp/axmat-trim-v8-ready-source-admission-20261009/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v8.py')

def pin(p,expected=None):
    p=Path(p);s=p.lstat();raw=p.read_bytes();a=p.lstat()
    before=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
    after=[a.st_dev,a.st_ino,a.st_mode,a.st_size,a.st_mtime_ns,a.st_ctime_ns,a.st_nlink]
    assert before==after and not p.is_symlink(),str(p)
    h=hashlib.sha256(raw).hexdigest()
    if expected:assert h==expected,str(p)
    return raw,dict(path=str(p),sha256=h,size=len(raw),identity=before)

def main():
    new,np=pin(T/'record_root_terminal.py','0fce254f46ac85606569a0343920e6c49fa60dc9674eaeca363dacffec55de4e')
    old,op=pin(T/'record_root_terminal_parent_v7.py.txt','75a0230bca8df7b80dbc5bd61ceb494aa842e6a571623b9bd84ac17696ed36c3')
    config,cp=pin(T/'config.json','db46c96fefe30ce455b3d296cfca0c804a4010ae6abca2ad67ae2b5fb574b697')
    s=new.decode();parent=old.decode();ast.parse(s);ast.parse(parent)
    prefix='AXMAT_HISTORICAL_INPUT_OWNED_SPECS_LAST_CPRIME_TRIM_COMBINED_PHYSICAL_DEDUP_RUNTIME_LIVE_RESOURCE_SCOPES_V8'
    regions=[dict(old='/private/tmp/axmat-last-cprime-trim-combined-live-resource-v7-root-execution-20261009',new=str(T)),dict(old=prefix[:-1]+'7',new=prefix)]
    inverse=s
    for region in regions:
        assert s.count(region['new'])==1 and parent.count(region['old'])==1
        inverse=inverse.replace(region['new'],region['old'],1)
    assert inverse.encode()==old
    (OUT/'reconstructed_parent_v7.py.txt').write_bytes(inverse.encode())
    # All declarations, helper bodies and terminal logic remain exact after identity reversal.
    assert ast.dump(ast.parse(inverse),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False)
    declarations=[]
    for n in ast.parse(s).body:
        if isinstance(n,ast.FunctionDef):
            original=next(x for x in ast.parse(parent).body if isinstance(x,ast.FunctionDef) and x.name==n.name)
            body=ast.get_source_segment(s,n);previous=ast.get_source_segment(parent,original)
            assert body==previous
            declarations.append(dict(name=n.name,line=n.lineno,sha256=hashlib.sha256(body.encode()).hexdigest(),byte_exact_to_parent=True))
    c=json.loads(config)
    expected={'P':'/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','F':str(ROOT/'validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v8.py'),'factorySha':'4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4','T':str(T),'R':str(ROOT/'validation/axial_material/last_cprime_trim_combined_live_resource_v8_build_review_20261009'),'SOURCE':str(ROOT/'validation/artifacts/axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-admission-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009'),'OUT':str(ROOT/'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009'),'TERM':str(ROOT/'validation/artifacts/axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009')}
    for k,v in expected.items():assert c[k]==v,(k,c[k],v)
    future=('declarationSha','prepSha','sealSha','terminalSha','terminalPath','failed_terminal_sha')
    assert all(c[k] is None for k in future)
    assert c['source_review_status']=='PENDING_FINAL_FACTORY_AND_ROOT_RECORDER_INDEPENDENT_REVIEW'
    absences={k:dict(path=c[k],lexists=os.path.lexists(c[k])) for k in ('F','SOURCE','OUT','TERM')}
    assert all(not x['lexists'] for x in absences.values())
    assert Path(c['P']).exists() and Path(c['R']).is_dir()
    raw,fp=pin(CANDIDATE,c['factorySha']);factorytext=raw.decode();factorytree=ast.parse(factorytext)
    assignments={n.targets[0].id:n.value for n in factorytree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
    assert ast.literal_eval(assignments['PREFIX'])==prefix
    assert ast.literal_eval(assignments['FAMILY'])=='HISTORICAL_INPUT_TRIM_COMBINED_RUNTIME_LINK_V8'
    for key in ('SOURCE','OUT'):
        node=assignments[key];assert isinstance(node,ast.BinOp) and isinstance(node.op,ast.Div) and isinstance(node.left,ast.Name) and node.left.id=='ART';assert str(ROOT/'validation/artifacts'/ast.literal_eval(node.right))==c[key]
    node=assignments['FORMAL_FACTORY'];assert isinstance(node,ast.BinOp) and isinstance(node.op,ast.Div) and isinstance(node.left,ast.Name) and node.left.id=='ROOT';assert str(ROOT/ast.literal_eval(node.right))==c['F']
    for name in ('declaration_terminal_return.json','terminal_return.json','seal.json','driver_result.json'):
        assert not os.path.lexists(Path(c['TERM'])/name) and not os.path.lexists(Path(c['OUT'])/name)
    checks={
      'actual_root_tool_terminal_exit_is_builtin_integer_zero':'assert type(tool[\'exit_code\'])is int and tool[\'exit_code\']==0' in s,
      'full_SOURCE_inventory_equal_declaration':'assert inv==d[\'source_inventory\']' in s,
      'prepare_exact_stdout_and_empty_stderr':'assert json.loads(out.read_text())==dict(declaration=str(OUT/\'declaration.json\'),declaration_sha256=decl[\'sha256\']); assert err.stat().st_size==0' in s,
      'trim_INPUT_original_full_dict_forwarded':'actual_last_cprime_trim_component_INPUT=d[\'actual_last_cprime_trim_component_INPUT\']' in s,
      'original_seven_whole_body_and_historical_PREP_forwarded':'historical_PREP=d[\'historical_PREP\'],historical_whole_component_body=d[\'historical_whole_component_body\']' in s,
      'success_requires_complete_driver_return_and_no_error':'result[\'classification\']==\'COMPLETE_COMBINED_RUNTIME_LINK_IDENTITY_ONLY\'and result[\'error\']is None' in s,
      'five_planned_stages_and_no_compile_at_PREP':'planned_total_stages=5,compiled_or_numeric_stages_started=0' in s,
      'four_PREP_future_tails_None_and_four_actual_RUN_tails':'for field in (\'actual_tail_check\',\'actual_elapsed_seconds\',\'actual_archive_bytes\',\'actual_resources\'):e[field]=None' in s and 'for field in (\'actual_tail_check\',\'actual_elapsed_seconds\',\'actual_archive_bytes\',\'actual_resources\'):e[field]=body[field]' in s,
      'original_tail_wall_archive_caps':'e[\'actual_tail_check\']==\'PASS\'and e[\'actual_elapsed_seconds\']<1800 and 0<e[\'actual_archive_bytes\']<2*2**30' in s,
      'PREP_and_RUN_separately_bind_declaration_and_PREP_SHA':'assert c[\'declarationSha\']==decl[\'sha256\']' in s and 'assert prep[\'sha256\']==c[\'prepSha\']' in s,
      'fresh_exclusive_receipts':'with p.open(\'x\')' in s,
      'all_science_credit_stays_false':all((k+'=False') in s for k in ('native_transport_executed','mathematical_controls_newly_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted','scientific_qualification'))}
    assert all(checks.values()),checks
    result=dict(status='PASS_SOURCE_ONLY_V8_ROOT_SUCCESS_RECORDER_AND_CONFIG_IDENTITY',scope='Full V7 inverse of nonbusiness root success recorder plus future config identity only; no business READY/PREP/RUN credit.',source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),recorder=np,parent_recorder=op,config=cp,exact_changed_regions=regions,full_inverse_byte_exact=True,full_inverse_AST_equal=True,all_function_bodies_byte_exact=declarations,checks=checks,factory_candidate_identity_only=fp,factory_candidate_business_review_is_separate=True,configured_bindings=expected,future_receipt_fields={k:c[k] for k in future},future_formal_and_ART_roots_absent=absences,execution_credit=dict(actual_PREP=None,actual_RUN=None,actual_new_RSS=None,native_execution=False,AAA_accuracy_qualification=False,ABA_admitted=False),review_limits=['Source-only full inverse establishes unchanged original success-recorder contract. Real successful PREP/RUN receipts must be reviewed only after genuine observed terminal exit0. Failure exit1 must use the separate failure recorder.','The recorder forwards actual_resources and driver COMPLETE classification. Five real stage PASS and complete resource guards belong to upstream real business driver; no run is performed by this audit.','No isolated business import, constructor, renderer, API, PREP or RUN executed; no formal source or ART path written.'],files_deleted=0,formal_or_artifact_writes=False)
    p=OUT/'independent_recorder_config_source_review.json'
    with p.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status=result['status'],path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),new_recorder_sha256=np['sha256'],config_sha256=cp['sha256'],exact_inverse_regions=2,future_receipts_all_None=True,business_execution_started=False)))

if __name__=='__main__':main()
