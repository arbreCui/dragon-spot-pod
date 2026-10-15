#!/usr/bin/env python3
"""Current read-only module/link Source dependency inventory. No compiler runs."""
from pathlib import Path
import runpy,json,re,ast
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts';REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
OUT=REC/'online_boot_dispatcher_source_v1';PKG=REC/'online_boot_native64_source_v1'
base=runpy.run_path(str(REC/'global_native64_dependency_source_v2/driver_source/generate_global_native64_dependency_source.py'))
read=base['read_pin'];js=base['fresh_json']
SEVEN=ART/'axial-material-new-true-online-BOOT-operator-seven-compile-only-20261012'
LINK=ART/'axial-material-new-bootstrap-CLE-global-complete-route-build-only-20261012'
def legacy_pin_same(path,pin):
    p=read(path)[1]
    assert all(p[k]==pin[k] for k in ['path','sha256','size_bytes','identity'])
    return p
def main():
    binding_path=SEVEN/'Root_current_compile_only_binding.json'
    summary_path=SEVEN/'Root_actual_compile_only_summary.json'
    binding=json.loads(read(binding_path)[0]);summary=json.loads(read(summary_path)[0])
    assert summary['status']=='SEVEN_TRUE_ONLINE_BOOT_OPERATOR_COMPILE_STEPS_CLOSED0_ONLY'
    assert summary['failure'] is None and summary['after_check_error'] is None
    assert len(summary['records'])==7 and all(r['status']=='PASS' for r in summary['records'])
    assert summary['transport_executed'] is False
    fixed_current=[legacy_pin_same(Path(p['path']),p) for p in binding['fixed_current_pins']]
    commands=binding['actual_commands'];search=[Path(a[2:]) for a in commands[0] if a.startswith('-I')]
    assert all([a for a in c if a.startswith('-I')]==[a for a in commands[0] if a.startswith('-I')] for c in commands)
    frozen=json.loads(read(PKG/'COMPLETE_TRUE_ONLINE_BOOT_AND_OPERATOR_SOURCE_FREEZE.json')[0])
    source_pins=frozen['current_sources']+frozen['current_operator_sources']
    source_by_name={Path(p['path']).name:Path(p['path']) for p in source_pins}
    origin={
      'ganlib':ROOT/'Ganlib/src/ganlib.f90','spomoc_audit':ROOT/'src/SPOMOC.f90',
      'spot_leakage':ROOT/'src/SPOT_LEAKAGE.f90','spor64_b2i':ROOT/'src/SPOR64_B2I.f90',
      'spor64_schema':ROOT/'src/SPOR64_SCHEMA.f90','spor64_verify':ROOT/'src/SPOR64_VERIFY.f90',
      'spor64_rcontract':ROOT/'src/SPOR64_RCONTRACT.f90','spor64_a9':ROOT/'src/SPOR64_A9.f90',
      'spor64_boot64':REC/'new_source/SPOR64_BOOT64.f90',
      'spor64_boot_context64_v2':REC/'bootstrap_qfiss_source_v2/SPOR64_BOOT_CONTEXT64.f90',
      'spor64_bootq64_v2':REC/'bootstrap_qfiss_source_v2/SPOR64_BOOTQ64.f90',
      'spor64_boot_bind64':source_by_name['SPOR64_BOOT_BIND64.f90'],
      'spor64_bootc64':source_by_name['SPOR64_BOOTC64.f90'],
      'spor64_bootb64':source_by_name['SPOR64_BOOTB64.f90'],
      'spot_radial_native_math64':source_by_name['SPOT_RADIAL_NATIVE_MATH64.f90']}
    intrinsic={'iso_c_binding','iso_fortran_env','ieee_arithmetic'}
    source_rows=[];all_uses=set()
    for p in source_pins:
        path=Path(p['path']);assert read(path)[1]==p
        raw=read(path)[0];s=raw.decode()
        uses=[]
        for line in s.splitlines():
            m=re.match(r'^\s*use\s*(?:,\s*intrinsic\s*::\s*|::\s*)?(\w+)',line,re.I)
            if m:uses.append(m.group(1).lower())
        includes=re.findall(r'^\s*include\s*[^\n]*',s,re.M|re.I);assert not includes
        calls=sorted(set(n.lower() for n in re.findall(r'\bcall\s+(\w+)',s,re.I)))
        all_uses.update(set(uses)-intrinsic)
        source_rows.append({'source_pin':p,'all_USE_module_names':uses,'all_INCLUDE_statements':includes,
          'all_literal_CALL_procedure_inventory':calls,
          'intrinsic_modules_from_compiler':[n for n in uses if n in intrinsic]})
    assert all_uses==set(origin)
    module_rows=[]
    for name in sorted(all_uses):
        candidates=[p/(name+'.mod') for p in search];present=[p for p in candidates if p.is_file()]
        assert present,name
        source_raw,source_pin=read(origin[name])
        assert re.search(rb'^\s*module\s+'+name.encode()+rb'\b',source_raw,re.M|re.I)
        module_rows.append({'module':name,'actual_first_module_search_match_pin':read(present[0])[1],
            'complete_current_Source_declaring_module_pin':source_pin,
            'later_same_name_paths_not_selected':[str(p) for p in present[1:]]})
    object_rows=[]
    for c in commands:
        srcs=[Path(a) for a in c if a.endswith(('.f','.f90','.F'))];assert len(srcs)==1
        obj=Path(c[c.index('-o')+1]);assert obj.is_file()
        object_rows.append({'actual_compiled_source_pin':read(srcs[0])[1],'actual_object_pin':read(obj)[1]})
    old_binding=json.loads(read(LINK/'Root_current_compile_only_binding.json')[0])
    old_link=old_binding['actual_commands'][-1]
    archives=[Path(a) for a in old_link if a.endswith('.a')]
    assert len(archives)==4
    archive_rows=[read(p)[1] for p in archives]
    # Locate explicit imported-module implementation objects in the actual
    # already completed upstream link, retaining its original source order.
    names={'SPOR64_A9.o','SPOR64_BOOT64.o','SPOR64_VERIFY.o','SPOR64_RCONTRACT.o',
      'SPOR64_BOOT_CONTEXT64.o','SPOR64_BOOTQ64.o'}
    explicit=[Path(a) for a in old_link if Path(a).name in names]
    assert len(explicit)==6
    explicit_rows=[read(p)[1] for p in explicit]
    compiler_pin=read(Path(commands[0][0]))[1]
    ast.parse(read(Path(__file__))[0])
    js(OUT/'ALL_SEVEN_SOURCE_USES_INCLUDES_AND_ACTUAL_COMPILED_DEPENDENCY_PINS.json',{
      'scope':'Actual current full EOF SHA/7ID Source/use/include/call/module/object/archive dependency inventory. Root actually compiled seven callees; this agent only reads results. No solve/qualification inherited.',
      'actual_seven_compile_summary_pin':read(summary_path)[1],
      'actual_seven_compile_binding_pin':read(binding_path)[1],
      'all_265_original_compile_fixed_current_fullpins':fixed_current,
      'actual_seven_compile_status':summary['status'],'actual_compile_wall_seconds':summary['wall_seconds'],
      'actual_module_search_order':[str(p) for p in search],'seven_complete_source_rows':source_rows,
      'all_15_nonintrinsic_used_module_rows':module_rows,'all_seven_actual_object_rows':object_rows,
      'six_explicit_actual_existing_implementation_object_pins':explicit_rows,
      'original_four_staticarchives_exact_link_order_pins':archive_rows,
      'staticarchive_member_origin_mapping':{'SPOR64_B2I':'libDragon.a/SPOR64_B2I.o; src/SPOR64_B2I.f90',
        'SPOT_LEAKAGE':'libDragon.a/SPOT_LEAKAGE.o; src/SPOT_LEAKAGE.f90',
        'SPOMOC_AUDIT':'libDragon.a/SPOMOC.o; src/SPOMOC.f90 (module name differs from member filename)',
        'SPOPOD_and_SPOPOD64':'libDragon.a/SPOPOD.o; src/SPOPOD.f90',
        'GANLIB_REDGET_LCM_and_support':'libGanlib.a; full current archive pinned'},
      'independent_module_review':'Reviewer373b43 EXIT0 verified11 upstreammod+6object+2archive rows against actualRoot48binding, readonly ar c0b03a confirmed B2I/LEAKAGE/SPOMOC member names.',
      'actual_root48_link_binding_pin':read(LINK/'Root_current_compile_only_binding.json')[1],
      'compiler_current_pin':compiler_pin,
      'guard_preserved':{'stage_seconds':600,'whole_seconds':1800,'memory_bytes':536870912,'threads':1,'retries':0},
      'dispatcher_compiled_by_this_agent':False,'transport_executed':False,'qualified':False})
    for p in source_pins:assert read(Path(p['path']))[1]==p
    for p in archive_rows+explicit_rows:assert read(Path(p['path']))[1]==p
    print(json.dumps({'status':'ACTUAL_ALL_MODULE_AND_SOURCE_DEPENDENCY_BINDING_EXIT0',
      'current_source_count':7,'nonintrinsic_modules':len(module_rows),'original_fixed_fullpins':len(fixed_current),
      'actual_new_objects':len(object_rows),'existing_explicit_objects':len(explicit_rows),'original_archives':len(archives),
      'actual_seven_callee_compile_status':summary['status'],'agent_compiler_or_numeric_run':False}))
if __name__=='__main__':main()
