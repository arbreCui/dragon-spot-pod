#!/usr/bin/env python3
"""Finite static Source byte/AST audit only; never imports a candidate.

Only the literal Source files below are read. Old SCI, XSM, SQL, pool, ASCII
products and extraction documents are stat/current7-only. This writes draft
Source evidence, not an AUTHOR freeze, GEN/READY/publication or run admission.
"""
import ast
import difflib
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT=Path('/Users/wen/spot')
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
BASE=Path(__file__).absolute().parent
OBS=REC/'current_formal_material_authority_exact_cache70_post_literal3_latest_full50_source_v9_20261014'
EVID=REC/'current_material_evidence_compare_three_after_GENDF_cumulative_resources_source_v7_20261014'
PROD=REC/'current_formal_first_A_short_FIL_producer_source_v10_20261014'
SCI_CWD=ROOT/'validation/artifacts/axial-material-inputs-20261003/A'

def identity(s):
    return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def source_bytes(path):
    path=Path(path)
    assert path.suffix in('.py','.f','.F','.f90','.c','.h','.c2m','.x2m')
    assert not any(p.is_symlink()for p in(path,*path.parents))
    before=path.lstat();assert stat.S_ISREG(before.st_mode)and before.st_nlink==1 and before.st_size<2**20
    with path.open('rb')as f:
        assert identity(os.fstat(f.fileno()))==identity(before)
        raw=f.read();assert identity(os.fstat(f.fileno()))==identity(before)
    assert identity(path.lstat())==identity(before)and len(raw)==before.st_size
    return raw,dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),
      size_bytes=len(raw),identity=identity(before))

def inverse(original,candidate):
    old=original.splitlines(keepends=True);new=candidate.splitlines(keepends=True)
    edits=[]
    for tag,a,b,c,d in difflib.SequenceMatcher(a=old,b=new,autojunk=False).get_opcodes():
        if tag=='equal':continue
        edits.append(dict(candidate_line_start_zero_based=c,candidate_line_end_zero_based=d,
          original_bytes_hex=b''.join(old[a:b]).hex(),candidate_bytes_hex=b''.join(new[c:d]).hex()))
    restored=list(new)
    for item in reversed(edits):
        a=item['candidate_line_start_zero_based'];b=item['candidate_line_end_zero_based']
        assert b''.join(restored[a:b]).hex()==item['candidate_bytes_hex']
        restored[a:b]=bytes.fromhex(item['original_bytes_hex']).splitlines(keepends=True)
    assert b''.join(restored)==original
    return edits

def current_only(expected):
    p=Path(expected['path']);s=p.lstat()
    assert not any(q.is_symlink()for q in(p,*p.parents))
    assert identity(s)==expected['identity']and s.st_size==expected['size_bytes']
    return dict(path=str(p),size_bytes=s.st_size,identity=identity(s),
      declared_frozen_sha256_not_read_or_recomputed=expected['sha256'])

def stat_files(directory,pattern='*'):
    return[dict(path=str(p),size_bytes=p.lstat().st_size,identity=identity(p.lstat()))
      for p in sorted(directory.glob(pattern))if p.is_file()]

def write(name,value):
    with(BASE/name).open('x')as f:
        json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

def main():
    derived=[]
    for name in('cle2000_c','clemod_c','kdrdpr'):
        derived.append((ROOT/'Ganlib/src'/(name+'.c'),BASE/(name+'.B_IO.UNREADY.c')))
    derived +=[(OBS/'AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90',BASE/'AXMAT_CONTEXT_OBSERVATION_MOD.B_IO.UNREADY.f90'),
      (ROOT/'validation/artifacts/axial-material-inputs-20261003/B/material.x2m',BASE/'material_B.b63.UNREADY.x2m'),
      (EVID/'current_material_lineage_evidence.py',BASE/'current_B_material_lineage_evidence.UNREADY.py')]
    proofs=[]
    for original,candidate in derived:
        old,op=source_bytes(original);new,np=source_bytes(candidate)
        proofs.append(dict(original_Source_pin=op,candidate_Source_pin=np,
          complete_original_bytes_restored=True,inverse_line_edits=inverse(old,new)))
    unchanged=[]
    for parent,names in[(OBS,['LIBMIX.observe.UNREADY.f','LIBDEN.observe.UNREADY.f',
      'TONDRV.context_observe.UNREADY.f','TONSPH.observe.UNREADY.f']),
      (EVID,['complete_observed_old_post_final_XSM_extractor.UNREADY.py',
      'extract_actual_complete_context_with_SPH_decisions.UNREADY.py',
      'saved_native_data_access_adapter.UNREADY.py',
      'complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'])]:
        for name in names:
            old,op=source_bytes(parent/name);new,np=source_bytes(BASE/name);assert old==new
            unchanged.append(dict(original_Source_pin=op,candidate_Source_pin=np,whole_Source_bytes_equal=True))
    old,op=source_bytes(PROD/'produce_current_formal_material_observations.py')
    new,np=source_bytes(BASE/'capture_current_original_B.UNREADY.py')
    def collector(raw):
        code=raw.decode();n=next(n for n in ast.parse(code).body if isinstance(n,ast.FunctionDef)and n.name=='collect_state')
        return ast.get_source_segment(code,n).encode()
    original_function=collector(old);candidate_function=collector(new)
    collector_proof=dict(original_whole_Source_pin=op,candidate_whole_Source_pin=np,
      original_function='collect_state',candidate_function='collect_state',
      original_function_bytes_sha256=hashlib.sha256(original_function).hexdigest(),
      candidate_function_bytes_sha256=hashlib.sha256(candidate_function).hexdigest(),
      complete_original_function_bytes_restored=True,
      allowed_change='only four product output basenames via B_PRODUCT_NAMES; header/traversal arithmetic untouched',
      inverse_line_edits=inverse(original_function,candidate_function))
    inventories=[];candidate_pins=[]
    for p in sorted(BASE.iterdir()):
        if p.suffix not in('.py','.f','.F','.f90','.c','.h','.x2m'):continue
        raw,pin=source_bytes(p);candidate_pins.append(pin)
        row=dict(Source_pin=pin,Python_AST_parsed=False)
        if p.suffix=='.py':
            code=raw.decode();tree=ast.parse(code);row['Python_AST_parsed']=True
            row['top_level_definition_pins']=[dict(name=n.name,kind=type(n).__name__,line=n.lineno,
              end_line=n.end_lineno,Source_segment_sha256=hashlib.sha256(ast.get_source_segment(code,n).encode()).hexdigest())
              for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef))]
        inventories.append(row)
    seed_path=PROD/'CURRENT_FORMAL_COMPLETE_AB_ORIGINAL_MATERIAL_SEED_PLAN_SOURCE_ONLY.json'
    seed_raw=seed_path.read_bytes();assert len(seed_raw)==10710 and hashlib.sha256(seed_raw).hexdigest()=='9bf2ba8444f0fe17989db3a31c373730da1d73bae564405c6ca71f5bc6c6579b'
    seed=json.loads(seed_raw)
    original_B_current7=[current_only(row['input_pin'])for row in seed['states']['B']['native_stage_inputs']]
    Aroles={r['destination']:r['input_pin']for r in seed['states']['A']['native_stage_inputs']}
    consumed=[current_only(Aroles[name])for name in('AxMatTone.c2m','geometry.dat','rnr_cc.c2m','rnr_interpol.c2m')]
    prior_observed=ROOT/'validation/artifacts/axial-material-new-current-formal-material-observations-short-FIL-after-v18-saved370-20261014-v10/A'
    observations=stat_files(prior_observed,'axobs-*')
    assert len(observations)==63
    prior_evidence=ROOT/'validation/artifacts/axial-material-current-first-A-fullfield-extract-six-roots-20261014-v1-evidence'
    evidence=[dict(path=str(p),size_bytes=p.lstat().st_size,identity=identity(p.lstat()))
      for p in sorted(prior_evidence.rglob('*'))if p.is_file()]
    contexts=sum(p['size_bytes']for p in observations if p['path'].endswith('.context.bin'))
    trees=sum(p['size_bytes']for p in observations if p['path'].endswith('.xsm'))
    extraction=sum(p['size_bytes']for p in evidence)
    assert (contexts,trees,extraction)==(125254,145813636,438863526)
    output=SCI_CWD/'b63';assert not os.path.lexists(output)
    scratch=['_DUMMY','_main001','_FIL000','_AxMatTone002','_rnr_cc003','_rnr_interpol003','TRACK_T_f']
    caches=[name+suffix for name in('AxMatTone','rnr_cc','rnr_interpol')for suffix in('.o2m','.l2m')]
    products=['m.xsm','u.asc','a.asc','t.asc']
    output_names=scratch+caches+products+[Path(p['path']).name for p in observations]
    assert len(output_names)==len(set(output_names))
    assert all(not os.path.lexists(output/name)for name in output_names)
    evidence_doc=dict(schema='B_ONLY_UNFROZEN_STATIC_SOURCE_BYTE_INVERSE_EVIDENCE_V1',
      status='STATIC_SOURCE_BYTES_AND_AST_CHECKS_ONLY_NO_BUILD_ADMISSION',
      derived_whole_Source_inverse_proofs=proofs,unchanged_whole_scientific_Source_proofs=unchanged,
      original_collector_function_IO_only_inverse_proof=collector_proof,
      candidate_Source_inventory=inventories,complete_candidate_Source_pins=candidate_pins,
      old_science_or_science_valued_document_body_reads=0,old_science_body_hashes=0,
      original_B_seven_inputs_current7_only=original_B_current7,
      actual_readonly_original_A_CWD_roles_current7_only=consumed,
      original_A55context_8tree_current7_only=observations,
      original_A_full_extraction_all_files_current7_only=evidence,
      original_scope_budget_reference=dict(four_products=423456221,context_bytes=contexts,
        eight_tree_bytes=trees,extraction_bytes=extraction,total_without_new_build_or_aggregation=423456221+contexts+trees+extraction,
        actual_new_B_size_predicted=False,independent_new_B_upper_bound_still_required=True),
      fresh_output_name_current_absence=dict(native_cwd=str(SCI_CWD),fresh_io_component='b63',
        output_root=str(output),output_root_currently_absent=True,all_known_native_output_names=output_names,
        all_output_paths_absent=True,Root_must_recheck_after_exclusive_claim=True),
      source_generation_performed=False,publication_performed=False,compiler_run=False,native_run=False,
      new_IO_compiled_equivalence_qualified=False,physical_accuracy_qualified=False,
      AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    write('SOURCE_BYTE_INVERSE_EVIDENCE.json',evidence_doc)
    write('AST_INVENTORY.json',dict(schema='B_ONLY_UNFROZEN_AST_INVENTORY_V1',Source_inventory=inventories,
      imports_executed=False,compiler_run=False,native_run=False,budget_prefix_frozen=False))
    print(json.dumps(dict(status=evidence_doc['status'],candidate_Source_count=len(candidate_pins),
      Python_AST_count=sum(r['Python_AST_parsed']for r in inventories),whole_derived_inverse_count=len(proofs),
      whole_unchanged_scientific_Source_count=len(unchanged),collector_IO_only_inverse_equal=True,
      original_science_body_reads=0,original_science_body_hashes=0,original_stat_reference_bytes=1008258637),separators=(',',':')),flush=True)

if __name__=='__main__':main()
