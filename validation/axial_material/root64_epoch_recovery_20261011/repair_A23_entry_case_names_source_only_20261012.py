#!/usr/bin/env python3
"""Pure Source repair writer; never imports a host or starts a business child."""
from pathlib import Path
import importlib.util
import json

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD_B=REC/'native_warm_A2_A3_runtime_build_source_v1'
OLD_W=REC/'native_warm_A2_A3_bounded_host_source_v1'
NEW_W=REC/'native_warm_A2_A3_bounded_host_source_v2'

def main():
    spec=importlib.util.spec_from_file_location('pure_original_A23_Source_writer',REC/'prepare_A2_A3_complete_bounded_hosts_20261012.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    assert not NEW_W.exists()
    NEW_W.mkdir()
    old_binding=json.loads((OLD_W/'CURRENT_A23_COMPLETE_HOST_SOURCE_BINDING.json').read_text())
    fixed={}
    def add(row):
        row=m.normalized(row);assert m.pin(row['path'])==row
        if row['path']in fixed:assert fixed[row['path']]==row
        fixed[row['path']]=row
    for row in old_binding['fixed_current_pins']:add(row)
    for p in [Path(__file__).resolve(),REC/'prepare_A2_A3_complete_bounded_hosts_20261012.py',OLD_B/'CURRENT_A23_COMPLETE61_BUILD_BINDING.json',OLD_B/'COMPLETE_A23_RUNTIME_BUILD_SOURCE_FREEZE.json',OLD_W/'CURRENT_A23_COMPLETE_HOST_SOURCE_BINDING.json',OLD_W/'COMPLETE_A23_HOST_SOURCE_BYTE_INVERSE.json']:add(m.pin(p))
    proofs=[]
    host='build_complete_native_A23_handlers_operator_dispatcher61_only.py'
    for case in ('A2','A3'):
        name=f'guarded_warm_{case}_common.py';t=m.Change(OLD_W/name)
        t.replace(str(OLD_W.relative_to(REC))+'/CURRENT_A23_COMPLETE_HOST_SOURCE_BINDING.json',str(NEW_W.relative_to(REC))+'/CURRENT_A23_COMPLETE_HOST_SOURCE_BINDING.json')
        proofs.append(t.save(NEW_W/name));add(m.pin(NEW_W/name))
        name=f'run_current_warm_{case}_entry_controls.py';t=m.Change(OLD_W/name)
        t.replace(f"'R64WARM-{case}-V1 '",f"'R64-{case}-WARM1 '")
        proofs.append(t.save(NEW_W/name));add(m.pin(NEW_W/name))
        name=f'run_current_native_warm_{case}.py';t=m.Change(OLD_W/name)
        proofs.append(t.save(NEW_W/name));add(m.pin(NEW_W/name))
    plan_path=OLD_B/'CURRENT_A23_COMPLETE61_BUILD_BINDING.json'
    binding=dict(old_binding)
    binding.update(planned_A23_61_build_binding_pin=m.pin(plan_path),planned_A23_61_build_host_pin=m.pin(OLD_B/host),planned_A23_61_build_freeze_pin=m.pin(OLD_B/'COMPLETE_A23_RUNTIME_BUILD_SOURCE_FREEZE.json'),Source_repair_only=True,prior_unexecuted_A23_host_binding_pin=m.pin(OLD_W/'CURRENT_A23_COMPLETE_HOST_SOURCE_BINDING.json'),requires_host_process_metadata_access=True)
    binding['fixed_current_pins']=[fixed[p]for p in sorted(fixed)]
    bind_path=NEW_W/'CURRENT_A23_COMPLETE_HOST_SOURCE_BINDING.json';m.write(bind_path,binding)
    proof=dict(schema='COMPLETE_A23_UNEXECUTED_ENTRY_CASE_NAME_REPAIR_SOURCE_ONLY_V2',sources=proofs,prior_complete_original_B_Source_byte_inverse_pin=m.pin(OLD_W/'COMPLETE_A23_HOST_SOURCE_BYTE_INVERSE.json'),planned_build_binding_pin=m.pin(plan_path),planned_case_binding_pin=m.pin(bind_path),exact_changes=['one common BIND namespace per case','one actual case_name assertion per entry'],main_hosts_exact_wholebytes_unchanged=True,actual_warm_output_namespaces_unchanged_and_absent=True,build_host_binding_and_compile_output_namespace_unchanged=True,all_original_resources_guards_flags_caps_physics_preserved=True,compiler_or_solver_or_probe_child_executed=False,old_unexecuted_warm_candidate_not_qualified=True)
    proof_path=NEW_W/'COMPLETE_A23_HOST_SOURCE_BYTE_INVERSE.json';m.write(proof_path,proof)
    print(json.dumps(dict(status='SOURCE_ONLY_A23_CASE_NAMES_REPAIRED_NO_CHILD',build_host=m.pin(OLD_B/host),build_binding=m.pin(plan_path),warm_binding=m.pin(bind_path),proof=m.pin(proof_path),fixed_current_count=len(fixed))))

if __name__=='__main__':main()
