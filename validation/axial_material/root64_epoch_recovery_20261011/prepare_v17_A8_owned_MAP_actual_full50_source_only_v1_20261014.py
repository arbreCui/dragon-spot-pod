#!/usr/bin/env python3
"""Create a v17 full50 Source candidate only after genuine owned-runtime V2 success.

This file is a Source-only preparer. It never imports a business Host, compiles,
runs a solver, releases files, or creates a runnable HF/CLI. Its initial binding
template contains explicit null actual authorities and is rejected by main.
The original v16 50-stage body, three helper files, compact Q40/four-control
admission and separate Driver37/budget-bit admission remain whole-byte equal.
"""
from pathlib import Path
import argparse,ast,hashlib,json,os,shlex,stat

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'aaa_three_plane_cache336_pipeline_source_v16_20261014'
NEW=REC/'aaa_three_plane_A8_owned_MAP_pipeline_source_v17_20261014'
NEW_OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-A8-owned-MAP-20261014-v17')
SPEC_SCHEMA='V17_A8_OWNED_MAP_FULL50_SOURCE_ONLY_BINDING_SPEC_V1'
OWNED_HF_SCHEMA='COMPLETE_GUARDED_ONE_BOOT_A8_18_OWNED_MAP_LIFETIME_HOST_SOURCE_ONLY_FREEZE_V1'
OWNED_SF_SCHEMA='COMPLETE_SPOR64_A8_18_CALLER_OWNED_MAP_LIFETIME_FORTRAN_SOURCE_ONLY_FREEZE_V1'
POST_SCHEMA='INDEPENDENT_A8_18_OWNED_MAP_LIFETIME_V2_ACTUAL_RUNTIME_POSTVERIFICATION_V1'
POST_STATUS='PASS_ACTUAL_A8_18_OWNED_MAP_LIFETIME_V2_SINGLE_BOOT0_FULL_PAIR_READBACK_POSTVERIFICATION'
ACTUAL_KEYS=('actual_owned_runtime_report_pin','actual_owned_runtime_Root_tools_pin',
 'actual_owned_runtime_Root_argv_pin','actual_owned_runtime_post_review_pin','actual_owned_runtime_post_tools_pin')
HELPERS=('actual_inputs_and_readback.py','direct_alias_entry_controls.f90','mutate_owned_control.f90')
PRESERVED_ADMISSIONS=('admit_compact_build','admit_control_host','exact_public_pin','live_public_pins',
 'null_public_fields','admit_exact_public_stale_lifetimes','admit_compact_controls',
 'require_cache336_bit_compiler_metadata','admit_cache336_driver_build','admit_cache336_budget_bit_controls')

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path):
    path=Path(path);before=identity(path.lstat())
    if path.is_symlink()or not stat.S_ISREG(before[2]):raise RuntimeError('ordinary exact Source/metadata')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd))!=before:raise RuntimeError('opened input exact7')
        with os.fdopen(fd,'rb')as stream:
            fd=None;raw=stream.read()
            if identity(os.fstat(stream.fileno()))!=before:raise RuntimeError('EOF input exact7')
    finally:
        if fd is not None:os.close(fd)
    if identity(path.lstat())!=before:raise RuntimeError('after EOF input exact7')
    return raw,dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)

def fullpin(row):
    if not isinstance(row,dict)or set(row)!={'path','sha256','size_bytes','identity'}or \
       not isinstance(row['path'],str)or not Path(row['path']).is_absolute()or \
       not isinstance(row['sha256'],str)or len(row['sha256'])!=64 or \
       any(x not in '0123456789abcdef'for x in row['sha256'])or \
       not isinstance(row['identity'],list)or len(row['identity'])!=7 or \
       any(type(x)is not int for x in row['identity'])or type(row['size_bytes'])is not int or \
       row['size_bytes']!=row['identity'][4]or not stat.S_ISREG(row['identity'][2]):
        raise RuntimeError('required canonical actual full PF; unknown None is not an authority')
    return row

def read(row):
    fullpin(row);raw,actual=pin(row['path'])
    if actual!=row:raise RuntimeError('selected current metadata fullpin changed: '+row['path'])
    return json.loads(raw)

def unique(rows):
    table={}
    for row in rows:
        fullpin(row)
        if row['path']in table and table[row['path']]!=row:raise RuntimeError('inconsistent current fullpin')
        table[row['path']]=row
    return list(table.values())

def current7(rows):
    for row in unique(rows):
        p=Path(row['path'])
        if p.is_symlink()or identity(p.lstat())!=row['identity']:raise RuntimeError('current exact7 changed: '+row['path'])

def live_rows(rows,retired):
    historical={r['path']:fullpin(r)for r in unique(retired)};out=[]
    for row in rows:
        fullpin(row)
        if row['path']in historical:
            if row!=historical[row['path']]:raise RuntimeError('retired exact path has another PF; no generic missing skip')
        else:out.append(row)
    return unique(out)

def write(path,value):
    raw=value.encode()if isinstance(value,str)else value
    with Path(path).open('xb')as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    _,row=pin(path)
    if row['identity'][3]!=1:raise RuntimeError('new own Source single link')
    return row

def write_json(path,value):return write(path,json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

OWNED_ADMISSION_SOURCE=r'''def owned_runtime_terminal0(value):
    if not isinstance(value,dict)or type(value.get('exit_code'))is not int or value['exit_code']!=0 or value.get('session_id')is not None:
        raise RuntimeError('owned Runtime actual genuine terminal integer0 and no session')

def owned_runtime_live_rows(rows,retired):
    historical=current_pin_table(retired);out=[]
    for row in rows:
        if row['path']in historical:
            if row!=historical[row['path']]:raise RuntimeError('only exact historical PF can leave current roots')
        else:out.append(row)
    return unique(out)

def owned_runtime_readback_shape(value):
    if not isinstance(value,dict)or value.get('dimensions',[])[:3]!=[1,370,3]or value.get('rank_values')!=370 or value.get('rank1_all_groups')is not True or \
       value.get('independent_reference_physics_assessment')is not False or not isinstance(value.get('planes'),list)or len(value['planes'])!=3:
        raise RuntimeError('actual original complete full370 three-plane terminal readback')
    for p,row in enumerate(value['planes'],1):
        if row.get('plane')!=p or row.get('groups')!=370 or row.get('unknowns')!=14 or row.get('fission_components')!=32 or \
           row.get('SYSTEM_SPOT_L1_SNAP')!=p or row.get('SYSTEM_SPOT_L1_RAW')!=1 or row.get('SYSTEM_full370_SPOT_S0_PHYS_checked')is not True or \
           row.get('flux_values')!=370*14 or row.get('source_values')!=370*14:
            raise RuntimeError('every actual terminal plane/full370/native field/mirror readback')
    if not isinstance(value.get('complete_AX_tree'),str)or not isinstance(value.get('complete_ARCHIVE_tree'),str):
        raise RuntimeError('actual complete pair logical tree digests')

def admit_owned_map_runtime_values(report,pactual,own,pown,sf,psf,plan,pp,cli,pcli,rt,prt,argv,pargv,post,ppost,pt,ppt):
    root=Path(pactual['path']).parent
    if own.get('schema')!='COMPLETE_GUARDED_ONE_BOOT_A8_18_OWNED_MAP_LIFETIME_HOST_SOURCE_ONLY_FREEZE_V1'or \
       sf.get('schema')!='COMPLETE_SPOR64_A8_18_CALLER_OWNED_MAP_LIFETIME_FORTRAN_SOURCE_ONLY_FREEZE_V1'or \
       sf.get('source_only')is not True or any(sf.get(k)is not False for k in ('compiled','numerical_executed','business_executed','files_deleted'))or \
       own['selected_owned_Fortran_Source_freeze_pin']!=psf or own['diagnostic_host_plan_pin']!=pp or cli['selected_own_Host_freeze_pin']!=pown or \
       plan['selected_owned_Fortran_Source_freeze_pin']!=psf or plan['diagnostic_Source_pin']!=sf['diagnostic_source_pin']or \
       plan['planned_output_root']!=str(root)or cli['output_root']!=str(root)or plan['runtime_authorities_complete']is not True or \
       plan['only_replacement_zero_based_index']!=1 or plan['compiler_Module_ABI_whole_bytes_must_equal_old']is not True:
        raise RuntimeError('exact Source-only owned18 SF, V2 owning HF/PLAN/CLI and only1 obligation')
    flags=sf['Source_flags']
    if len(flags)!=9 or any(v is not True for v in flags.values())or any(sf.get(k)is not True for k in flags):
        raise RuntimeError('all nine exact owned lifetime Source flags')
    if own['host_source']['path']!=str(REC/'boot_v16_A8_18_owned_MAP_lifetime_host_source_v2_20261014/run_guarded_one_BOOT_A8_owned_MAP_lifetime.py')or \
       pactual['path']!=str(Path(cli['output_root'])/'Root_actual_one_BOOT_status_diagnostic_summary.json')or \
       len(cli['exact_reviewable_argv'])!=42 or argv['exact_argv']!=cli['exact_reviewable_argv']or argv['interface_pin']!=pcli or argv['Host_freeze_pin']!=pown:
        raise RuntimeError('only selected V2 genuine 42-token Root launch, never failed V1')
    owned_runtime_terminal0(rt['actual_terminal_return'])
    if rt.get('observed_closed')is not True or type(rt.get('original_integer_exit_code'))is not int or rt['original_integer_exit_code']!=0 or \
       not isinstance(rt.get('exact_executed_command'),str)or shlex.split(rt['exact_executed_command'])!=argv['exact_argv']:
        raise RuntimeError('genuine owned Runtime Root closed0 and exact shlex argv42')
    records=report['records']
    if report.get('schema')!='ACTUAL_GUARDED_ONE_BOOT_A8_18_OWNED_MAP_LIFETIME_V1'or report.get('status')!='ACTUAL_ONE_BOOT_ORIGINAL_SEAL_READBACK_CLOSED_ONLY'or \
       report.get('failure')is not None or report.get('first_failure_secondary_errors')!=[]or len(records)!=3 or \
       [r['label'].rsplit('/',1)[-1]for r in records]!=['compile_BOOT_diagnostic','link_Dragon','BOOT_diagnostic']or \
       any(r.get('status')!='PASS'for r in records)or report.get('final_report_resource_check_passed')is not True or \
       report.get('actual_host_Source_freeze_pin')!=pown or report.get('actual_diagnostic_Fortran_Source_freeze_pin')!=psf or \
       report.get('replacement_zero_based_link_index')!=1 or report.get('original_guard_class')!='OwnRSSSerialExecutor'or report.get('original_guard_MRO_unchanged')is not True or \
       any(report.get(k)is not False for k in ('full50_executed','engineering_qualified','physics_qualified'))or \
       any(report.get(k)is not True for k in ('other69_current_Driver37_BOOTQ40_math57_and_four_archives_unchanged','current_all9_core_objects_unchanged','retained_original9_latest_capture_nine_input_sources_full_EOF_and_all7_preserved')):
        raise RuntimeError('genuine three PASS owned Runtime, separate singleBOOT0 never full50/physics')
    caps=plan['original_caps']
    if report['original_caps']!=caps or caps['SELF_and_each_own_child_RSS_cap_bytes']!=512*2**20 or caps['original_stage_wall_cap_seconds']!=600 or caps['whole_wall_cap_seconds']!=1800 or \
       caps['fresh_output_cap_bytes']!=2*2**30 or caps['history_cap_bytes']!=96*2**30 or caps['original_cold_reserve_bytes']!=20971764748 or caps['filesystem_floor_bytes']!=8*2**30 or caps['retries']!=0 or \
       type(report.get('SELF_peak_bytes'))is not int or not 0<=report['SELF_peak_bytes']<512*2**20 or type(report.get('wall_seconds'))not in (int,float)or not 0<report['wall_seconds']<1800:
        raise RuntimeError('unchanged original owned Runtime caps and true resource snapshots')
    outcome=report['actual_outcome'];seal=outcome.get('actual_Fortran_complete_copy_readback')
    if outcome.get('kind')!='REAL_ORIGINAL_SINGLE_BOOT_SEAL_READBACK0_ONLY'or type(outcome.get('actual_exit_code'))is not int or outcome['actual_exit_code']!=0 or outcome.get('single_boot_completed')is not True or \
       not isinstance(seal,dict)or seal.get('schema')!='ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1'or seal.get('status')!='PASS'or \
       (seal.get('groups'),seal.get('planes'),seal.get('epoch'))!=(370,3,0)or seal.get('all_payload_bits_equal')is not True or seal.get('complete_lifecycle_checked')is not True:
        raise RuntimeError('original complete370×3 seal0, never preseal or failure observer')
    terminal=outcome['complete_terminal_readback'];owned_runtime_readback_shape(terminal)
    if post.get('schema')!='INDEPENDENT_A8_18_OWNED_MAP_LIFETIME_V2_ACTUAL_RUNTIME_POSTVERIFICATION_V1'or \
       post.get('status')!='PASS_ACTUAL_A8_18_OWNED_MAP_LIFETIME_V2_SINGLE_BOOT0_FULL_PAIR_READBACK_POSTVERIFICATION'or \
       post.get('failure')is not None or post.get('verification_failure')is not None or \
       any(post.get(k)is not False for k in ('business_executed','compiler_executed','numerical_executed','files_deleted','engineering_qualified','physics_qualified','full50_executed'))or \
       post.get('actual_owner_bit_control_results','MISSING')is not None or \
       post.get('actual_report_pin')!=pactual or post.get('actual_Host_freeze_pin')!=pown or post.get('actual_CLI_pin')!=pcli or \
       post.get('actual_Root_true_tool_return_pin')!=prt or post.get('actual_Root_exact_argv_pin')!=pargv or post.get('actual_Fortran_Source_freeze_pin')!=psf or \
       type(post.get('actual_Root_exit_code'))is not int or post['actual_Root_exit_code']!=0 or post.get('actual_Root_closed')is not True or \
       type(post.get('actual_stage_count'))is not int or post['actual_stage_count']!=3 or post.get('actual_stage_statuses')!=['PASS','PASS','PASS']or \
       any(post.get(k)is not True for k in ('actual_single_BOOT_completed','all_three_watches_closed_without_limit_failure','actual_terminal_pair_full370x3_readback_verified','only_ordered70_index1_changed','actual_other69_ordered70_inputs_full_EOF_unchanged','actual_module6092_fullSHA_matches_original'))or \
       post.get('actual_Fortran_complete_copy_readback')!=seal or post.get('actual_terminal_pair_readback')!=terminal:
        raise RuntimeError('exact independent genuine success post0 and original complete pair facts')
    if pt.get('observed_closed')is not True:raise RuntimeError('independent actual post observed closed')
    for key in ('actual_review_return','actual_postverification_return'):
        result=pt[key];owned_runtime_terminal0(result);lines=result['output'].strip().splitlines()
        if not lines or json.loads(lines[-1])['review_pin']!=ppost:raise RuntimeError('actual post tool original stdout exact review PF')
    actual=current_pin_table(report['fixed_current_pins']+report['output_pins']);old70=plan['current_ordered70_input_pins']
    obj=actual[str(root/'build/SPOR64_A8.o')];mod=actual[str(root/'build/spor64_a8.mod')];dragon=actual[str(root/'runtime/Dragon')]
    new70=list(old70);new70[1]=obj;oldmod=plan['selected_original_A8_module_pin']
    if len(old70)!=70 or len({r['path']for r in old70})!=70 or len({r['path']for r in new70})!=70 or \
       post['actual_new_object1_pin']!=obj or post['actual_ordered70_input_pins']!=new70 or post['actual_Module_ABI_pin']!=mod or post['original_Module_ABI_pin']!=oldmod or \
       mod['size_bytes']!=6092 or mod['sha256']!=oldmod['sha256']or mod['size_bytes']!=oldmod['size_bytes']or \
       report['actual_ordered70_link_inputs']!=[r['path']for r in new70]or \
       any(actual.get(r['path'])!=r for r in new70+plan['current_nine_core_object_pins'])or \
       [i for i,(a,b)in enumerate(zip(old70,new70))if a!=b]!=[1]:
        raise RuntimeError('actual only1 repair70, bootstrap9 and identical6092 module whole bytes')
    first=plan['original_compiler_pin']['path']
    expected_compile=[first,*plan['original_compile_flags'],'-I'+str(root/'build'),*plan['original_compile_include_arguments'],'-J'+str(root/'build'),'-c',sf['diagnostic_source_pin']['path'],'-o',obj['path']]
    expected_link=[first,'-O2','-ffp-contract=off',*[r['path']for r in new70],'-o',dragon['path']]
    if records[0]['command']!=expected_compile or records[1]['command']!=expected_link or records[2]['command']!=[dragon['path']]or \
       report['actual_commands']!=[expected_compile,expected_link,[dragon['path']]]or [r for r in new70 if r['path'].endswith('.a')]!=plan['original_four_archive_pins']:
        raise RuntimeError('actual compile1/link ordered70/BOOT commands and four archive order')
    for name,key in (('closed_boot_axial.xsm','actual_terminal_axial_pin'),('closed_boot_archive.xsm','actual_terminal_archive_pin')):
        if post[key]!=actual[str(root/'AAA'/name)]:raise RuntimeError('independent exact actual sealed physical pair PF')
    return dict(report=report,report_pin=pactual,object_pin=obj,Dragon_pin=dragon,current70_pins=new70,link_command=expected_link,
      source_pin=sf['diagnostic_source_pin'],source_freeze_pin=psf,build_Host_freeze_pin=pown,post_review_pin=ppost,
      terminal_axial_pin=post['actual_terminal_axial_pin'],terminal_archive_pin=post['actual_terminal_archive_pin'],
      provenance=dict(actual_runtime_report_pin=pactual,actual_Root_true_tool_return_pin=prt,actual_Root_exact_argv_pin=pargv,
        actual_post_review_pin=ppost,actual_post_tools_pin=ppt,actual_owned_Fortran_Source_freeze_pin=psf,actual_owned_Host_freeze_pin=pown,
        actual_object1_pin=obj,actual_module6092_pin=mod,actual_ordered70_input_pins=new70,single_boot_completed=True,
        full50_executed=False,engineering_qualified=False,physics_qualified=False,actual_owner_bit_control_results=None))

def admit_owned_map_runtime(args,hf,helper,cache_runtime,compact):
    report,pactual=ext(args,'owned_runtime')
    keys=('selected_actual_owned_runtime_report_pin','selected_owned_runtime_Host_freeze_pin','selected_owned_Fortran_Source_freeze_pin',
      'selected_owned_runtime_plan_pin','selected_owned_runtime_CLI_pin','selected_owned_runtime_Root_tools_pin','selected_owned_runtime_Root_argv_pin',
      'selected_owned_runtime_post_review_pin','selected_owned_runtime_post_tools_pin')
    rows={k:selected_pin(hf,k)for k in keys};values={k:c.load_json_exact(r['path'],r['sha256'],json.dumps(r['identity']))[0]for k,r in rows.items()}
    if pactual!=rows['selected_actual_owned_runtime_report_pin']:raise RuntimeError('only actual selected owned Runtime report')
    get=lambda key:values[key]
    runtime=admit_owned_map_runtime_values(report,pactual,get(keys[1]),rows[keys[1]],get(keys[2]),rows[keys[2]],get(keys[3]),rows[keys[3]],
      get(keys[4]),rows[keys[4]],get(keys[5]),rows[keys[5]],get(keys[6]),rows[keys[6]],get(keys[7]),rows[keys[7]],get(keys[8]),rows[keys[8]])
    own=get(keys[1]);plan=get(keys[3]);sf=get(keys[2]);old70=plan['current_ordered70_input_pins'];core=plan['current_nine_core_object_pins']
    if [old70[i]for i in (37,40,57)]!=[cache_runtime['current70_pins'][i]for i in (37,40,57)]or old70[40]!=compact['object_pin']or \
       [x for x in old70 if x['path'].endswith('.a')]!=[x for x in cache_runtime['current70_pins']if x['path'].endswith('.a')]:
        raise RuntimeError('owned only1 keeps genuine Q40/Driver37/math57 and original four archives')
    c.closed_report(report,helper,Path(pactual['path']).parent,3)
    c.verify_rows(own['dependencies']);c.same_pin(own['host_source']['path'],own['host_source']);c.verify_rows(sf['files'])
    c.verify_rows(runtime['current70_pins']+core+[plan['selected_original_A8_module_pin']])
    actual_pair=data.final_readback(runtime['terminal_axial_pin']['path'],runtime['terminal_archive_pin']['path'])
    if actual_pair!=get(keys[7])['actual_terminal_pair_readback']:raise RuntimeError('all original terminal fields and raw mirror bits rechecked')
    runtime['fixed']=unique(list(rows.values())+[own['host_source']]+own['dependencies']+sf['files']+report['fixed_current_pins']+report['output_pins'])
    return runtime

'''

def function_bytes(source,name):
    node=next(n for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name==name)
    return ast.get_source_segment(source,node)

def source_candidate(original):
    text=original;changes=[]
    def replace(before,after,reason):
        nonlocal text
        if text.count(before)!=1:raise RuntimeError('exact unique v17 Source splice: '+reason)
        changes.append(dict(before=before,after=after,reason=reason));text=text.replace(before,after,1)
    replace('import time\n','import time\nimport shlex\n','exact real Root argv validation')
    replace("OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-cache336-20261014-v16')","OUT=Path('"+str(NEW_OUT)+"')",'unique next full50 OUT')
    replace('def main():\n',OWNED_ADMISSION_SOURCE+'def main():\n','separate strict actual owned Runtime admission, original admission functions retained')
    replace("'cache336-build70','cache336-budget-bits']:","'cache336-build70','cache336-budget-bits','owned-runtime']:",'one new mandatory actual Runtime report triplet')
    replace("hf['schema']!='COMPLETE_ACTUAL_AAA3_CACHE336_PIPELINE_HOST_SOURCE_FREEZE_V16'","hf['schema']!='COMPLETE_ACTUAL_AAA3_A8_OWNED_MAP_PIPELINE_HOST_SOURCE_FREEZE_V17'",'new complete owning Source HF')
    replace("    runtime=admit_cache336_driver_build(args,hf,helper,compact)\n    build=runtime['report'];pbuild=runtime['report_pin']\n    current70_link=build['actual_complete70_link_inputs']",
      "    cache_runtime=admit_cache336_driver_build(args,hf,helper,compact)\n    runtime=admit_owned_map_runtime(args,hf,helper,cache_runtime,compact)\n    build=runtime['report'];pbuild=runtime['report_pin']\n    current70_link=[x['path']for x in runtime['current70_pins']]\n    owned_runtime_admission_provenance=runtime['provenance']",
      'final actual repair70 for execution and direct aliases, separate Driver37 chain kept')
    replace("    link_command=build['records'][-1]['command']\n", "    link_command=runtime['link_command']\n",'real link record1, not last BOOT record')
    replace("direct_binding['schema']!='DECLARED_ACTUAL_COMPONENT_DIRECT_ALIAS_ENTRY_BINDING_V3'","direct_binding['schema']!='DECLARED_ACTUAL_COMPONENT_DIRECT_ALIAS_ENTRY_BINDING_V4'",'owned Runtime direct-main binding')
    replace("    budget=admit_cache336_budget_bit_controls(args,hf,helper,runtime)\n    cache336_admission_provenance=dict(new_driver_build_report_pin=pbuild,new_Driver_object_pin=runtime['object_pin'],\n      new_Driver_Fortran_Source_freeze_pin=runtime['source_freeze_pin'],new_Driver_Host_freeze_pin=runtime['build_Host_freeze_pin'],",
      "    budget=admit_cache336_budget_bit_controls(args,hf,helper,cache_runtime)\n    cache336_admission_provenance=dict(new_driver_build_report_pin=cache_runtime['report_pin'],new_Driver_object_pin=cache_runtime['object_pin'],\n      new_Driver_Fortran_Source_freeze_pin=cache_runtime['source_freeze_pin'],new_Driver_Host_freeze_pin=cache_runtime['build_Host_freeze_pin'],",
      'budget controls retain original separate Driver build/SF provenance')
    replace("    fixed=unique(fixed+compact['fixed']+controls['fixed']+runtime['fixed']+budget['fixed']+[cache_build_pin]",
      "    fixed=unique(fixed+compact['fixed']+controls['fixed']+cache_runtime['fixed']+runtime['fixed']+budget['fixed']+[cache_build_pin]",'both original Driver chain and owned chain remain fixed')
    replace("                 original69['fixed_current_pins']+original69['output_pins'])\n    observation.checkpoint('admission.before_fixed_EOF')",
      "                 original69['fixed_current_pins']+original69['output_pins'])\n    fixed=owned_runtime_live_rows(fixed,hf['historical_retired_exact_private_body_pins'])\n    observation.checkpoint('admission.before_fixed_EOF')",'explicit exact retired PF whitelist, never generic absent or nested historical promotion')
    replace("    archives=tuple(x for x in build['records'][-1]['command']if x.endswith('.a'))\n", "    archives=tuple(x for x in link_command if x.endswith('.a'))\n",'four archives from genuine actual repair link')
    replace('    del compact,controls,cache_build,runtime,budget\n','    del compact,controls,cache_build,cache_runtime,runtime,budget\n','release only unused JSON containers before guarded original50')
    replace('          actual_cache336_driver_and_budget_bit_admission=cache336_admission_provenance,\n',
      '          actual_cache336_driver_and_budget_bit_admission=cache336_admission_provenance,\n          actual_A8_owned_MAP_runtime_admission=owned_runtime_admission_provenance,\n','raw separate owned Runtime provenance')
    replace("          actual_cache336_driver_and_budget_bit_admission=cache336_admission_provenance,angular_moments_status='UNKNOWN',",
      "          actual_cache336_driver_and_budget_bit_admission=cache336_admission_provenance,\n          actual_A8_owned_MAP_runtime_admission=owned_runtime_admission_provenance,angular_moments_status='UNKNOWN',",'summary separate owned Runtime provenance')
    ast.parse(text);restored=text
    for block in reversed(changes):
        if restored.count(block['after'])!=1:raise RuntimeError('unique entire Source inverse')
        restored=restored.replace(block['after'],block['before'],1)
    if restored!=original:raise RuntimeError('whole v16 Source bytes not recovered')
    protected=original[original.index('    try:\n        # Replace ONLY the main object'):original.index('        raw=dict(schema=')]
    if protected not in text:raise RuntimeError('original complete guarded50 continuous body changed')
    retained={}
    for node in ast.parse(original).body:
        if isinstance(node,(ast.FunctionDef,ast.ClassDef))and node.name!='main':
            old=function_bytes(original,node.name);new=function_bytes(text,node.name)
            if old!=new:raise RuntimeError('original full helper/class wholebytes changed: '+node.name)
            retained[node.name]=hashlib.sha256(old.encode()).hexdigest()
    return text,changes,protected,retained

def validate_spec(spec):
    if spec.get('schema')!=SPEC_SCHEMA or spec.get('source_only')is not True or any(spec.get(k)is not False for k in ('compiler_executed','numerical_executed','pipeline_executed','files_deleted')):
        raise RuntimeError('exact Source-only binding specification')
    for key in ACTUAL_KEYS:fullpin(spec[key])
    for key,row in spec['selected_existing_pins'].items():fullpin(row)
    if spec['expected_post_schema']!=POST_SCHEMA or spec['expected_post_status']!=POST_STATUS:raise RuntimeError('exact peer actual success protocol')

def main():
    parser=argparse.ArgumentParser(allow_abbrev=False)
    for suffix in ('summary','sha256','seven-id'):parser.add_argument('--binding-spec-'+suffix,required=True)
    args=parser.parse_args();raw,pspec=pin(args.binding_spec_summary)
    if pspec['sha256']!=args.binding_spec_sha256 or pspec['identity']!=json.loads(args.binding_spec_seven_id):raise RuntimeError('binding Spec exact external PF')
    spec=json.loads(raw);validate_spec(spec)
    if pin(__file__)[1]!=spec['preparer_source_pin']:raise RuntimeError('selected actual preparer Source')
    chosen=spec['selected_existing_pins'];values={k:read(v)for k,v in chosen.items()}
    actual={k:read(spec[k])for k in ACTUAL_KEYS}
    # This executes only the pure admission Source in this file. It does not
    # import the owning business Host, its Common, or any Fortran/science reader.
    namespace={'Path':Path,'REC':REC,'json':json,'shlex':shlex,'current_pin_table':lambda rows:{r['path']:r for r in unique(rows)},'unique':unique}
    exec(compile(OWNED_ADMISSION_SOURCE,'<pure-owned-runtime-admission-source>','exec'),namespace)
    runtime=namespace['admit_owned_map_runtime_values'](actual[ACTUAL_KEYS[0]],spec[ACTUAL_KEYS[0]],
      values['owned_runtime_Host_freeze'],chosen['owned_runtime_Host_freeze'],values['owned_Fortran_Source_freeze'],chosen['owned_Fortran_Source_freeze'],
      values['owned_runtime_plan'],chosen['owned_runtime_plan'],values['owned_runtime_CLI'],chosen['owned_runtime_CLI'],
      actual[ACTUAL_KEYS[1]],spec[ACTUAL_KEYS[1]],actual[ACTUAL_KEYS[2]],spec[ACTUAL_KEYS[2]],actual[ACTUAL_KEYS[3]],spec[ACTUAL_KEYS[3]],actual[ACTUAL_KEYS[4]],spec[ACTUAL_KEYS[4]])
    report=runtime['report'];root=Path(runtime['report_pin']['path']).parent
    outputs={r['path']:r for r in unique(report['output_pins'])}
    for record in report['records']:
        wp=outputs[str(root/(record['label']+'.watchdog.json'))];lp=outputs[str(root/(record['label']+'.log'))];w=read(wp)
        if w['command']!=record['command']or type(w.get('returncode'))is not int or w['returncode']!=0 or w.get('limit_failure')is not None or \
           w.get('rss_cap_mib')!=512 or w.get('own_child_only')is not True or w.get('liveness_group_cleanup')is not True or \
           type(w.get('sampled_peak_rss_mib'))not in (int,float)or not 0<=w['sampled_peak_rss_mib']<512 or \
           type(w.get('elapsed_seconds'))not in (int,float)or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 or lp['sha256']!=record['log_sha256']:
            raise RuntimeError('all actual three watch0/log identities and original caps')
        if pin(lp['path'])[1]!=lp:raise RuntimeError('actual log whole EOF unchanged')
    own=values['owned_runtime_Host_freeze'];oldhf=values['v16_Host_freeze'];retired=unique(spec['historical_retired_exact_private_body_pins'])
    if retired!=own['historical_retired_exact_private_body_pins']+spec['additional_exact_retired_body_pins']:
        # Each extra declaration is a named future migration proof; None/guess
        # is rejected. Ancestor JSON PFs are never recursively made live.
        if unique(own['historical_retired_exact_private_body_pins']+spec['additional_exact_retired_body_pins'])!=retired:raise RuntimeError('exact current Source role whitelist')
    deps=live_rows(oldhf['dependencies']+own['dependencies']+report['fixed_current_pins']+report['output_pins']+
      list(chosen.values())+[spec[k]for k in ACTUAL_KEYS]+[pspec,spec['preparer_source_pin']],retired)
    current7(deps)
    if NEW.exists()or NEW.is_symlink()or NEW_OUT.exists()or NEW_OUT.is_symlink():raise RuntimeError('one new Source namespace and future business OUT')
    original,poriginal=pin(OLD/'run_actual_three_plane_pipeline.py')
    if poriginal!=chosen['v16_Host_source']:raise RuntimeError('exact original v16 Host Source')
    text,changes,protected,retained=source_candidate(original.decode())
    direct=values['v16_direct_binding'];old_direct=dict(direct)
    if runtime['current70_pins'][12]!=direct['excluded_original_main_pin']:raise RuntimeError('actual repair70 retains main12')
    direct.update(schema='DECLARED_ACTUAL_COMPONENT_DIRECT_ALIAS_ENTRY_BINDING_V4',
      selected_actual_build70_report_pin=runtime['report_pin'],actual_original_ordered_70_link_inputs=runtime['current70_pins'],
      actual_complete70_source_freeze_pin=chosen['owned_Fortran_Source_freeze'],new_probe_source=str(NEW/'direct_alias_entry_controls.f90'),
      actual_pipeline_executed=False,selected_owned_Runtime_Host_freeze_pin=chosen['owned_runtime_Host_freeze'])
    NEW.mkdir();host=write(NEW/'run_actual_three_plane_pipeline.py',text);helpers=[]
    for name in HELPERS:
        helper_raw,previous=pin(OLD/name)
        if previous!=chosen['v16_'+name]:raise RuntimeError('original whole helper PF')
        helpers.append(dict(predecessor_pin=previous,candidate_pin=write(NEW/name,helper_raw),whole_bytes_unchanged=True))
    pdir=write_json(NEW/'DIRECT_ALIAS_ENTRY_BINDING.json',direct)
    inv=write_json(NEW/'COMPLETE_V16_TO_V17_OWNED_RUNTIME_ADMISSION_WHOLE_BYTE_INVERSE.json',dict(
      schema='COMPLETE_V16_TO_V17_OWNED_RUNTIME_ADMISSION_WHOLE_BYTE_INVERSE_V1',original_pin=poriginal,candidate_pin=host,changes=changes,
      whole_restored_bytes_equal=True,restored_sha256=poriginal['sha256'],original50_continuous_source_bytes=len(protected.encode()),
      original50_continuous_source_sha256=hashlib.sha256(protected.encode()).hexdigest(),original50_continuous_source_unchanged=True,
      original_function_and_class_whole_byte_SHA256=retained,original_compact40_fourcontrols_Driver37_budget_functions_wholebytes_unchanged=True,
      helpers=helpers,direct_binding_predecessor_pin=chosen['v16_direct_binding'],direct_binding_original_data=old_direct,direct_binding_actual_pin=pdir,
      source_only=True,compiler_executed=False,numerical_executed=False,pipeline_executed=False,files_deleted=False))
    selections={k:v for k,v in oldhf.items()if k.startswith('selected_')}
    selections.update(selected_actual_owned_runtime_report_pin=runtime['report_pin'],selected_owned_runtime_Host_freeze_pin=chosen['owned_runtime_Host_freeze'],
      selected_owned_Fortran_Source_freeze_pin=chosen['owned_Fortran_Source_freeze'],selected_owned_runtime_plan_pin=chosen['owned_runtime_plan'],
      selected_owned_runtime_CLI_pin=chosen['owned_runtime_CLI'],selected_owned_runtime_Root_tools_pin=spec[ACTUAL_KEYS[1]],
      selected_owned_runtime_Root_argv_pin=spec[ACTUAL_KEYS[2]],selected_owned_runtime_post_review_pin=spec[ACTUAL_KEYS[3]],selected_owned_runtime_post_tools_pin=spec[ACTUAL_KEYS[4]])
    deps=unique(deps+[pdir,inv]+[r['candidate_pin']for r in helpers]);current7(deps)
    plan=write_json(NEW/'ACTUAL_OWNED_RUNTIME_BOUND_V17_SOURCE_PREPARATION_PLAN.json',dict(
      schema='ACTUAL_OWNED_RUNTIME_BOUND_V17_SOURCE_PREPARATION_PLAN_V1',host_source=host,source_only=True,selected_actual_prerequisites=selections,
      predecessor_v16_Host_freeze_pin=chosen['v16_Host_freeze'],preparer_source_pin=spec['preparer_source_pin'],binding_spec_pin=pspec,
      dependencies=deps,historical_retired_exact_private_body_pins=retired,current_roots_come_from_actual_owned_runtime_only=True,
      ancestor_closed_v16_output_tables_never_promoted=True,no_generic_missing_pin_skip=True,complete_byte_inverse_pin=inv,direct_alias_binding_pin=pdir,
      helper_byte_equality=helpers,planned_output_root=str(NEW_OUT),original_pipeline_records_expected=dict(total=50,PASS=17,expected_refusal=33),
      original_caps=values['owned_runtime_plan']['original_caps'],current_owned_runtime_ordered70_pins=runtime['current70_pins'],
      separate_Q40_and_Driver37_four_controls_bit_provenance_preserved=True,expected_external_prefix_count=14,expected_total_argv_count=96,
      compiler_executed=False,numerical_executed=False,pipeline_executed=False,files_deleted=False,
      own_Host_freeze_pin=None,own_CLI_pin=None,future_actual_v17_report_pin=None,engineering_qualified=False,physics_qualified=False))
    ready=write_json(NEW/'SOURCE_REVIEW_READY.json',dict(schema='V17_ACTUAL_OWNED_RUNTIME_BOUND_SOURCE_REVIEW_READY_V1',
      status='SOURCE_ONLY_CANDIDATE_READY_FOR_INDEPENDENT_SOURCE_REVIEW',failure=None,host_source=host,plan_pin=plan,inverse_pin=inv,
      direct_binding_pin=pdir,helpers=helpers,source_only=True,compiler_executed=False,numerical_executed=False,pipeline_executed=False,files_deleted=False,
      actual_Host_freeze_pin=None,actual_CLI_pin=None,actual_v17_report_pin=None))
    print(json.dumps(dict(status='V17_GENUINE_OWNED_RUNTIME_PREREQUISITE_BOUND_SOURCE_CREATED_ONLY',host_source=host,plan_pin=plan,inverse_pin=inv,
      ready_pin=ready,dependency_count=len(deps),compiler_executed=False,numerical_executed=False,pipeline_executed=False,files_deleted=False)),flush=True)

if __name__=='__main__':main()
