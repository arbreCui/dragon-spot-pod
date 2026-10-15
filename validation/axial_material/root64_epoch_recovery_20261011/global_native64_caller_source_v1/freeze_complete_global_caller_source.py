#!/usr/bin/env python3
"""Pin and freeze the complete new caller Source package; no compiler/solver."""
from pathlib import Path
import ast,json,runpy
HERE=Path(__file__).resolve().parent
REC=HERE.parent
base=runpy.run_path(str(REC/'global_native64_dependency_source_v2/driver_source/generate_global_native64_dependency_source.py'))
read_pin=base['read_pin'];fresh=base['fresh'];fresh_json=base['fresh_json']

def main():
    outputs=['FINAL_CURRENT_GLOBAL_CALLER_EXTERNAL_SOURCE_DEPENDENCY_BINDING.json','COMPLETE_GLOBAL_CALLER_SOURCE_HANDOFF.txt','COMPLETE_GLOBAL_NATIVE64_CALLER_SOURCE_FREEZE.json']
    assert all(not(HERE/x).exists() for x in outputs)
    audit=json.loads(read_pin(HERE/'ACTUAL_COMPLETE_GLOBAL_CALLER_SOURCE_STATIC_AUDIT.json')[0])
    assert audit['status']=='ACTUAL_STDLIB_COMPLETE_EOF_FORWARD_REVERSE_AND_ABI_STATIC_AUDIT_CLOSED'
    sources=[read_pin(p['path'])[1] for p in audit['candidate_Source_pins'].values()]
    assert sources==list(audit['candidate_Source_pins'].values())
    original=json.loads(read_pin(HERE/'CURRENT_GLOBAL_CALLER_SOURCE_BINDING_AND_RUNTIME_SCOPE.json')[0])
    protected=[read_pin(p['path'])[1] for p in original['original_and_v2_frozen_Source_before']]
    assert protected==original['original_and_v2_frozen_Source_before']
    bootstrap=REC/'bootstrap_qfiss_source_v2'
    bp=json.loads(read_pin(bootstrap/'SOURCE_PINS_DEPENDENCIES_AND_REMAINING_SCOPE.json')[0])
    newdeps=[]
    for p in bp['source_pins']:
        raw,pin=read_pin(p['path'])
        assert pin['size_bytes']==p['bytes'] and pin['sha256']==p['sha256'] and pin['identity']==p['seven_id']
        newdeps.append(pin)
    canonical=read_pin(bootstrap/'SPOR64_BOOT_CANONICAL64.f90')
    assert canonical[1]['sha256']=='5d161094b3f5c671eb77d139042e396474225c138ae545de0384febfa7241bc2'
    assert b'module SPOR64_BOOT_CANONICAL64_V2\n' in canonical[0]
    publisher=read_pin(REC/'bootstrap_global_projection_publish_source_v1/SPOR64_BOOT_PUBLISH64.f90')
    assert b'use SPOR64_BOOT_CANONICAL64_V2' in publisher[0]
    assert b'use SPOR64_BOOT_CONTEXT64_V2' in publisher[0]
    assert b'SPOR64_BOOT_GLOBAL_PUBLISHED=2' in publisher[0]
    assert b'any(terminal_counters>caps)' in publisher[0] and b'any(terminal_counters>=caps)' not in publisher[0]
    foundation=[read_pin(REC.parent.parent.parent/'src'/n)[1] for n in ['SPOR64_VERIFY.f90','SPOR64_RCONTRACT.f90']]
    binding={'schema':'CURRENT_COMPLETE_GLOBAL_CALLER_EXTERNAL_SOURCE_BINDING_FINAL_V1',
        'status':'COMPLETE_NEW_CALLER_SOURCE_FROZEN_DEPENDENT_SOURCE_CURRENT_AT_THIS_READ_ONLY',
        'caller_five_complete_Source_pins':sources,'bootstrap_v2_complete_Source_pins':newdeps,
        'bootstrap_v2_binding_pin':read_pin(bootstrap/'SOURCE_PINS_DEPENDENCIES_AND_REMAINING_SCOPE.json')[1],
        'publisher_current_complete_Source_pin':publisher[1],'foundation_complete_Source_pins':foundation,
        'original_and_frozen_global_v2_Source_pins':protected,
        'correct_actual_canonical_path':str(bootstrap/'SPOR64_BOOT_CANONICAL64.f90'),
        'correct_actual_canonical_module':'SPOR64_BOOT_CANONICAL64_V2',
        'historical_candidate_manifest_path_note':'The initial writer manifest named a proposed SPOR64_BOOT_CANONICAL64_V2.f90 path while that dependency was still pending. The actual frozen filename is SPOR64_BOOT_CANONICAL64.f90, and this current fullEOF binding supersedes that proposed dependency path. The actual caller USE module was already V2.',
        'original_state_and_math':'Original TYPE K B1 SIGS becomes TYPE3, ILEAK3, OPTION B1; REBA OFF stays original. Radial RCON B0 remains a different operator contract. No physical setting changed for a validator.',
        'cold_native_rule':'Original scalar KEYFLX>0 = 1.0D0, all other unknowns zero directly in the native seed. No REAL32 mirror promotion.',
        'CONT_native_rule':'Modification/REC requires INIT ON, full native TYPE4 FLUX64/SOUR64/keff/B2, dimensions/keys/state/finite and exact compatibility mirror checks before actual native driver invocation.',
        'typed_dynamic_path':'Full SPOT parser/53arg wrapper -> frozen global SPOT native60 driver with native B1 dependencies -> actual native terminal flux/source/k/resid/counters/valid -> complete original headers and postchecks -> true canonical WRITE -> true independent GLOBAL publisher.',
        'no_legacy_MCCG_driver_reused':True,'no_reconstructed_header_masquerades_as_actual_producer':True,
        'dependent_publisher_not_owned_or_frozen_by_this_package':True,
        'required_before_actual_bounded_compile':['Root independent complete Source review','Root final current publisher/bootstrap/driver/tool/compiler/module/object/library pin validation under original guard/caps/resources','Compile new helpers/API/parser/wrapper/owner in dependency order with actual complete canonical/publisher modules'],
        'required_after_compile':['Real dispatcher FLUGLOBAL64 and seven operands production/deck implementation','Full actual original global solve and strict typed terminal publication with external pins','Actual projection/QFISS/BOOT/17/new-epoch/whole-input controls and online qualification'],
        'Fortran_or_transport_executed':False,'global_producer_qualified':False,'online_BOOT_qualified':False,'seventeen_controls_qualified':False,'whole_input_admitted':False,'AAA_qualified':False,'ABA_admitted':False,'goal_complete':False}
    fresh_json(HERE/outputs[0],binding)
    text='''Complete new SPOT global typed caller Source package. Source-only, no solve or qualification.

Five full Sources: SPOT_GLOBAL_CALLER_CARRIERS.f90, SPOT_GLOBAL_CALLER_API.f90,
FLUGPG64.f, FLUDRVG64.f, FLUGLOBAL64.f. The latter uses the standard five-tuple
CLE ABI with exactly seven operands: AX_CURRENT, fresh independent GLOBAL_NEW,
readonly MACROLIB3, TRACK_AX, SYSTEM_NEXT, ARCH_BOOT, RCONTRACT.

The lower wrapper returns actual typed terminal values to the full owning FLU.
All original headers and complete FLU postchecks execute before canonical WRITE,
then the real publisher receives actual terminal arrays and checks full context.
No stored header re-read substitutes for producing a solve result.

Cold: original scalar=1/all-other=0 math directly in REAL64.
CONT: complete native TYPE4 flux/source/keff/B2 and exact legacy mirror checks;
the native values are authoritative, not promoted compatibility values.
Parser B2/BSDIR are REAL64; static MACRO type2 B2 is read into independent
REAL32 buffers then exactly promoted. All original formula/parser/caps/eps/
ACCE/REBA/TYPE K B1 SIGS physical settings and FORMAT bytes are preserved.

Actual Source writer EXIT0; static audit EXIT0: complete forward/inverse
16 FLU /12 wrapper /10 parser /5 API transforms; all 46 protected original and
frozen v2 files unchanged. Exact current argument orders: 53 wrapper,60 native
driver,15 real publisher. This audit is not a Fortran parser or numerical test.

Actual canonical filename: bootstrap_qfiss_source_v2/SPOR64_BOOT_CANONICAL64.f90
with module SPOR64_BOOT_CANONICAL64_V2. Publisher module SPOR64_BOOT_PUBLISH64
is Root-owned and still needs its Root freeze/current-pin verification.
Build helper/API/parser/wrapper/owner using frozen v2 global driver, complete V2
canonical/context and complete publisher dependencies. Required actual guards,
compiler/objects/lib/tool/input pin validation remain Root's bounded host work.

Dispatcher/deck/production route, actual global solve, independent global-output
binding, projection/QFISS/BOOT/17/whole-input/AAA/ABA qualification remain open.
This Source freeze never declares whole-chain online or physical qualification.
'''
    fresh(HERE/outputs[1],text.encode())
    expected={
        'SPOT_GLOBAL_CALLER_CARRIERS.f90','SPOT_GLOBAL_CALLER_API.f90','FLUGLOBAL64.f','FLUDRVG64.f','FLUGPG64.f',
        'ORIGINAL_COMPLETE_FLU.f','ORIGINAL_COMPLETE_FLUDRV.f','ORIGINAL_COMPLETE_FLUGPI.f','ORIGINAL_COMPLETE_REVIEWED_CALLER_API.f90',
        'generate_complete_global_caller_source.py','COMPLETE_GLOBAL_CALLER_EXACT_BYTE_INVERSE_PROOFS.json','CURRENT_GLOBAL_CALLER_SOURCE_BINDING_AND_RUNTIME_SCOPE.json',
        'ACTUAL_COMPLETE_GLOBAL_CALLER_SOURCE_WRITER_TOOL_RETURNS.json','audit_complete_global_caller_source.py','ACTUAL_COMPLETE_GLOBAL_CALLER_SOURCE_STATIC_AUDIT.json',
        'ACTUAL_COMPLETE_GLOBAL_CALLER_SOURCE_STATIC_AUDIT_TOOL_RETURN.json','freeze_complete_global_caller_source.py',outputs[0],outputs[1]}
    paths=sorted(p for p in HERE.iterdir() if p.is_file())
    assert {p.name for p in paths}==expected
    pins=[read_pin(p)[1] for p in paths]
    for p in paths:
        if p.suffix=='.py':ast.parse(read_pin(p)[0])
    freeze={'schema':'COMPLETE_GLOBAL_NATIVE64_CALLER_SOURCE_FINAL_FREEZE_V1','status':'FROZEN_COMPLETE_SOURCE_ONLY_REAL_GLOBAL_COLD_CONT_CALLER_REAL_NATIVE_RETURN_AND_REAL_PUBLISHER',
        'fixed_regular_files':pins,'five_complete_Source_pins':sources,
        'actual_static_audit_pin':read_pin(HERE/'ACTUAL_COMPLETE_GLOBAL_CALLER_SOURCE_STATIC_AUDIT.json')[1],
        'actual_writer_tool_return_pin':read_pin(HERE/'ACTUAL_COMPLETE_GLOBAL_CALLER_SOURCE_WRITER_TOOL_RETURNS.json')[1],
        'actual_static_audit_tool_return_pin':read_pin(HERE/'ACTUAL_COMPLETE_GLOBAL_CALLER_SOURCE_STATIC_AUDIT_TOOL_RETURN.json')[1],
        'external_Source_dependency_binding_pin':read_pin(HERE/outputs[0])[1],
        'all_original_and_frozen_v2_Source_unchanged':True,'entire_current_package_pins_self_excluded':True,
        'Fortran_compile_or_transport_executed':False,'physical_global_or_online_or_whole_input_qualification':False,'goal_complete':False}
    fresh_json(HERE/outputs[2],freeze)
    assert [read_pin(p['path'])[1] for p in pins]==pins
    assert [read_pin(p['path'])[1] for p in protected]==protected
    print(json.dumps({'status':freeze['status'],'fixed_regular_file_count':len(pins),'complete_package_file_count_including_freeze':len(pins)+1,'freeze_pin':read_pin(HERE/outputs[2])[1],'five_complete_Source_pins':sources,'all_original_and_v2_unchanged':True,'Fortran_or_numeric_executed':False}))

if __name__=='__main__':main()
