#!/usr/bin/env python3
"""Full current KDRDRV plus exactly two real legal CLE branches. Source only."""
from pathlib import Path
import runpy,json,re,ast
ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
OUT=REC/'online_boot_dispatcher_source_v1'
base=runpy.run_path(str(REC/'global_native64_dependency_source_v2/driver_source/generate_global_native64_dependency_source.py'))
read_pin=base['read_pin'];fresh=base['fresh'];fresh_json=base['fresh_json'];Transform=base['Transform']
def main():
    assert not(OUT/'KDRDRV.F').exists()
    old=REC/'bootstrap_cle_entry_source_v1/KDRDRV.F'
    raw,pin=read_pin(old)
    original_branches=re.findall(rb"HMODUL.EQ.'([^']*)'",raw)
    t=Transform(raw)
    anchor="      ELSE IF(HMODUL.EQ.'FLU:') THEN\n"
    added=("      ELSE IF(HMODUL.EQ.'SPOOPG64:') THEN\n"
           "         CALL SPOOPG64(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)\n"
           "      ELSE IF(HMODUL.EQ.'SPOBOOT64:') THEN\n"
           "         CALL SPOBOOTRUN64(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)\n")
    t.splice('two true legal CLE entries preserving complete original body',anchor,added+anchor)
    proof=t.verify()
    branches=re.findall(rb"HMODUL.EQ.'([^']*)'",t.raw)
    assert [v for v in branches if v not in [b'SPOOPG64:',b'SPOBOOT64:']]==original_branches
    assert branches.count(b'SPOOPG64:')==branches.count(b'SPOBOOT64:')==1
    assert b'SPOBOOTRUN64:' not in t.raw
    assert len('SPOOPG64:')<=12 and len('SPOBOOT64:')<=12
    callees=[REC/'online_boot_native64_source_v1/operator_source_v2/SPOOPG64.f90',
             REC/'online_boot_native64_source_v1/SPOBOOTRUN64.f90']
    callee_pins=[]
    for p in callees:
        body,cp=read_pin(p);callee_pins.append(cp)
        match=re.search(rb'^subroutine\s+\w+\(([^)]*)\)',body,re.M|re.I)
        assert match and match.group(1).decode().lower()=='nentry,hentry,ientry,jentry,kentry'
        for decl in [b'integer,intent(in)::nentry,ientry(nentry),jentry(nentry)',
                     b'character(len=12),intent(in)::hentry(nentry)',
                     b'type(c_ptr),intent(in)::kentry(nentry)']:
            assert decl in body
    frozen=REC/'online_boot_native64_source_v1/COMPLETE_TRUE_ONLINE_BOOT_AND_OPERATOR_SOURCE_FREEZE.json'
    package=json.loads(read_pin(frozen)[0])
    for p in package['fixed_files']:assert read_pin(Path(p['path']))[1]==p
    length_sources=[ROOT/'src/dramod.f90',ROOT/'Ganlib/src/clelog.c',ROOT/'Ganlib/src/cle2000_c.c']
    length_pins=[read_pin(p)[1] for p in length_sources]
    assert b'character :: hmodul*12' in read_pin(length_sources[0])[0]
    assert b'if (ifinwd[iwords-1] - idebwd[iwords-1] > 11) goto L5012;' in read_pin(length_sources[1])[0]
    fresh(OUT/'KDRDRV.F',t.raw);fresh(OUT/'ORIGINAL_COMPLETE_BOOTSTRAP_KDRDRV.F',raw)
    fresh_json(OUT/'COMPLETE_DISPATCHER_WHOLE_BYTE_INVERSE_PROOF.json',proof)
    fresh_json(OUT/'CURRENT_TRUE_ONLINE_BOOT_DISPATCHER_SOURCE_BINDING.json',{
        'scope':'Complete Source-only original dispatcher including every prior entry and HDF5 branch, with exactly two new true five-tuple calls. No actual compile/link/transport/qualification.',
        'new_source_pin':read_pin(OUT/'KDRDRV.F')[1],
        'original_current_source_pin':pin,'original_current_source_after':read_pin(old)[1],
        'new_entry_mapping':{'SPOOPG64:':'SPOOPG64','SPOBOOT64:':'SPOBOOTRUN64'},
        'inaccessible_long_name_not_retained':'SPOBOOTRUN64: is13 characters and cannot pass real CLE12-character token/DRAMOD boundary; legal alias directly invokes unchanged full Fortran callee.',
        'actual_standard_ABI':{'argument_order':['NENTRY','HENTRY','IENTRY','JENTRY','KENTRY'],
          'NENTRY':'INTEGER scalar','HENTRY':'CHARACTER(LEN=12) array(NENTRY)',
          'IENTRY':'INTEGER array(NENTRY)','JENTRY':'INTEGER array(NENTRY)',
          'KENTRY':'TYPE(C_PTR) array(NENTRY)'},
        'callee_complete_current_pins':callee_pins,'seven_source_package_freeze_pin':read_pin(frozen)[1],
        'all_original_branches_exact_order_preserved':True,'all_original_branch_names':[b.decode() for b in original_branches],
        'new_branches_only':2,'actual_full_transform_steps':proof['actual_transform_steps'],
        'all_original_HDF5_and_fallback_cpu_memory_XDR_logic_complete_bytes_preserved':True,
        'actual_CLE_length_source_pins':length_pins,
        'owning_guard_must_preserve':{'stage_seconds':600,'whole_seconds':1800,
          'memory_bytes':512*1024*1024,'threads':1,'retries':0},
        'qualified':False,'compiled':False,'numeric_executed':False})
    assert read_pin(old)[1]==pin
    for p,pin0 in zip(callees,callee_pins):assert read_pin(p)[1]==pin0
    for p,pin0 in zip(length_sources,length_pins):assert read_pin(p)[1]==pin0
    ast.parse(read_pin(Path(__file__))[0])
    print(json.dumps({'status':'COMPLETE_TRUE_LEGAL_ONLINE_BOOT_DISPATCHER_SOURCE_WRITTEN',
        'source_pin':read_pin(OUT/'KDRDRV.F')[1],'actual_whole_inverse_steps':proof['actual_transform_steps'],
        'old_branches_preserved':len(original_branches),'new_real_branches':2,
        'legal_CLE_to_frozen_Fortran':{'SPOOPG64:':'SPOOPG64','SPOBOOT64:':'SPOBOOTRUN64'},
        'protected_original_and_callee_pins_stable':True,'Fortran_or_numeric_executed':False}))
if __name__=='__main__':main()
