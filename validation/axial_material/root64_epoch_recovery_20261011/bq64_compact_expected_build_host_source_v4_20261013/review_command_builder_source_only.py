#!/usr/bin/env python3
"""Exercise the extracted pure command function only; no Host/module import."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace

HERE=Path(__file__).resolve().parent
REPORT=HERE/'ROOT_EXTRACTED_COMMAND_BUILDER_SOURCE_ONLY_REVIEW.json'

def main():
    if REPORT.exists():raise RuntimeError('fresh Source-only review output')
    host=HERE/'build_bq64_compact_expected_runtime.py'
    raw=host.read_bytes();tree=ast.parse(raw)
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='commands')
    literals={}
    for name in ('SOURCE','OUT'):
        node=next(n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==name for t in n.targets))
        if name=='SOURCE':
            literals[name]=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')/ast.literal_eval(node.value.right)
        else:
            literals[name]=Path('/Users/wen/spot')/ast.literal_eval(node.value.right)
    namespace={'Path':Path,**literals}
    exec(compile(ast.Module(body=[fn],type_ignores=[]),str(host),'exec'),namespace)
    plan=json.loads((HERE/'EXACT_ORIGINAL70_TO_COMPACT_BQ64_BUILD_PLAN.json').read_text())
    assert plan['planned_output_root']==str(literals['OUT'])
    base=json.loads(Path(plan['original_actual_complete70_report_pin']['path']).read_text())
    function=namespace['commands'];common=SimpleNamespace(FLAGS=plan['original_compile_flags'])
    cmds=function(common,base,plan)
    old=plan['original_complete70_link_command'][3:-2];new=cmds[1][3:-2]
    assert len(cmds)==2 and len(new)==70
    assert [i for i,(a,b)in enumerate(zip(old,new))if a!=b]==[40]
    assert [p for p in old if p.endswith('.a')]==[p for p in new if p.endswith('.a')]
    assert cmds[0][1:10]==common.FLAGS
    cases=[]
    mutations=[
      ('link_missing_input',lambda b,p:b['records'][-1]['command'].pop(4)),
      ('link_reordered_inputs',lambda b,p:b['records'][-1]['command'].__setitem__(slice(3,5),list(reversed(b['records'][-1]['command'][3:5])))),
      ('link_changed_archive',lambda b,p:b['records'][-1]['command'].__setitem__(64,'/private/tmp/different.a')),
      ('wrong_compile_flag',lambda b,p:b['records'][0]['command'].__setitem__(1,'-O3')),
      ('wrong_compiler',lambda b,p:b['records'][0]['command'].__setitem__(0,'/private/tmp/other-compiler')),
      ('different_include_order',lambda b,p:b['records'][0]['command'].__setitem__(slice(10,12),list(reversed(b['records'][0]['command'][10:12])))),
      ('wrong_bootq_identity_path',lambda b,p:p['original_BOOTQ_object_pin'].__setitem__('path','/private/tmp/other.o')),
      ('wrong_ordered_pin_path',lambda b,p:p['original_ordered70_input_pins'][0].__setitem__('path','/private/tmp/different.o')),
    ]
    for name,mutate in mutations:
        changed_base=copy.deepcopy(base);changed_plan=copy.deepcopy(plan);mutate(changed_base,changed_plan)
        try:function(common,changed_base,changed_plan)
        except RuntimeError as error:cases.append(dict(case=name,exact_refusal=str(error)))
        else:raise RuntimeError('command mutation not refused: '+name)
    report=dict(schema='EXTRACTED_COMPACT_BQ_COMMAND_BUILDER_SOURCE_ONLY_REVIEW_V1',
      host_source_sha256=hashlib.sha256(raw).hexdigest(),positive_cases=1,exact_negative_cases=cases,
      original_ordered_input_count=len(old),new_ordered_input_count=len(new),only_replacement_index=40,
      compiler_executed=False,numerical_executed=False,new_Host_imported=False,
      only_pure_function_extracted=True,whole_source_freeze_or_runtime_qualification=False)
    with REPORT.open('x',encoding='utf-8')as f:
        json.dump(report,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    print(json.dumps({'status':'EXTRACTED_COMMAND_SOURCE_ONLY_POSITIVE_AND8_EXACT_REFUSALS_PASS',
                      'report_path':str(REPORT),'compiler_executed':False,'numerical_executed':False}))

if __name__=='__main__':main()
