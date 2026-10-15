#!/usr/bin/env python3
"""Review extracted command mapping; synthetic future paths are not real pins."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace

HERE=Path(__file__).resolve().parent
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
REPORT=HERE/'ROOT_EXTRACTED_FRESH17_COMMANDS_SOURCE_ONLY_REVIEW.json'

def main():
    if REPORT.exists():raise RuntimeError('fresh Source-only review namespace')
    path=HERE/'run_fresh_connected17.py';raw=path.read_bytes();tree=ast.parse(raw)
    compile(tree,str(path),'exec')
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='make_commands')
    out_node=next(n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='OUT'for t in n.targets))
    out=Path('/Users/wen/spot')/ast.literal_eval(out_node.value.right)
    namespace={'Path':Path,'OUT':out}
    exec(compile(ast.Module(body=[function],type_ignores=[]),str(path),'exec'),namespace)
    oracle=json.loads((REC/'root64_full17_expected_planes_rebind_v4/CURRENT_FULL_CONNECTED17_EXPECTED_PLANES_COMMAND_ORACLE_BINDING.json').read_text())
    original=json.loads(Path('/Users/wen/spot/validation/artifacts/axial-material-new-native-rank1-exact-block-cache-complete70-build-only-20261012-v2/Root_actual_build_only_summary.json').read_text())
    original_inputs=original['actual_complete70_link_inputs']
    future_object_path=str(Path('/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-compact-expected-composed-complete70-build-only-20261013-v3/build/SPOR64_BOOTQ64.o'))
    synthetic_inputs=list(original_inputs);synthetic_inputs[40]=future_object_path
    build={'actual_complete70_link_inputs':synthetic_inputs};obj={'path':future_object_path}
    c=SimpleNamespace(FLAGS=oracle['planned_compile_command'][1:10])
    commands=namespace['make_commands'](c,oracle,build,obj)
    assert len(commands)==20 and commands[0][-3]==oracle['source_pin']['path']
    assert commands[1][3:-2][3]==future_object_path
    assert commands[0][10]=='-I'+str(Path(future_object_path).parent)
    assert commands[0][-1]==commands[1][3]
    assert commands[1][-1]==commands[2][0]
    assert [cmd[1:]for cmd in commands[2:]]==[cmd[1:]for cmd in oracle['planned_run_commands']]
    refusals=[]
    changes=[
      ('changed_compile_flags',lambda o,b:o['planned_compile_command'].__setitem__(1,'-O3')),
      ('wrong_Source_path',lambda o,b:o['source_pin'].__setitem__('path','/private/tmp/other.f90')),
      ('wrong_original_control_main',lambda o,b:o['planned_link_command'].__setitem__(3,'/private/tmp/main.o')),
      ('missing_original_core_object',lambda o,b:o['planned_link_command'].pop(4)),
      ('production_core_mismatch',lambda o,b:b['actual_complete70_link_inputs'].remove(synthetic_inputs[22])),
      ('wrong_case_order',lambda o,b:o['original_case_names'].__setitem__(0,'other')),
      ('missing_run_phase',lambda o,b:o['planned_run_commands'].pop()),
      ('wrong_coherent_phase',lambda o,b:o['planned_run_commands'][-1].__setitem__(2,'prepare')),
    ]
    for name,mutate in changes:
        o=copy.deepcopy(oracle);b=copy.deepcopy(build);mutate(o,b)
        try:namespace['make_commands'](c,o,b,obj)
        except RuntimeError as error:refusals.append(dict(case=name,exact_refusal=str(error)))
        else:raise RuntimeError('missing exact refusal '+name)
    result=dict(schema='EXTRACTED_FRESH17_COMMANDS_SOURCE_ONLY_REVIEW_V1',host_source_sha256=hashlib.sha256(raw).hexdigest(),
      positive_cases=1,exact_refusals=refusals,original17_oracles_and_full_Source_path_unchanged=True,
      original20_stages_retained=True,synthetic_future_paths_are_not_actual_PF=True,
      Host_imported=False,compiler_executed=False,controls_executed=False,reader_qualified=False)
    with REPORT.open('x',encoding='utf-8')as f:
        json.dump(result,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status='SOURCE_ONLY_FRESH17_COMMAND_MAPPING_1POSITIVE_8REFUSALS_PASS',
      report_path=str(REPORT),Host_imported=False,compiler_executed=False,controls_executed=False)))

if __name__=='__main__':main()
