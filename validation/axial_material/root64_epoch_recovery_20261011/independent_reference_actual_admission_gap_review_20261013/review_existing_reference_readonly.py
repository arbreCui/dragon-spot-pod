"""Full current PF/Source read and static admission analysis; no reference import."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import struct
import time

ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';PKG=REC/'full370_unreduced_eigen_reference_source_v2';OUT=Path(__file__).absolute().parent
H=REC/'storage_release_closed_v7_v8_project_pair_20261013/independent_postverify_20261013/verify_exact_two_postrelease_v2.py'
spec=importlib.util.spec_from_file_location('own_readonly_full_EOF',H);s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
START=time.monotonic();TRANSITIONS=[]

def current(old):
    actual=s.pin(old['path']);s.check(actual['path']==old['path'] and actual['sha256']==old['sha256'] and actual['size_bytes']==old['size_bytes'] and actual['identity'][1:]==old['identity'][1:] and old['identity'][0] in (16777234,16777229) and actual['identity'][0]==16777229,'strict fullEOF unchanged except declared current mount device')
    if old!=actual:TRANSITIONS.append(dict(historical_pin=old,current_measured_full_EOF_pin=actual,only_device_changed=True))
    s.same(actual);return actual

def read_current(old):return s.exact_json(current(old))

def nested(value):
    if isinstance(value,dict):
        if 'path' in value and 'sha256' in value and 'size_bytes' in value and 'identity' in value:yield value;return
        for v in value.values():yield from nested(v)
    elif isinstance(value,list):
        for v in value:yield from nested(v)

def main():
    ownfiles=sorted(PKG.iterdir());s.check(len(ownfiles)==18 and all(p.is_file() for p in ownfiles),'17 original package files plus separate V2 inverse proof')
    all_source_pins=[s.pin(p) for p in ownfiles]
    contents={p.name:p.read_bytes() for p in ownfiles}
    for row in all_source_pins:s.same(row)
    python_AST_count=0
    for name,raw in contents.items():
        if name.endswith('.py'):ast.parse(raw);python_AST_count+=1
    s.check(python_AST_count==9,'all nine complete Python Sources read and parsed only')
    proof=json.loads(contents['COMPLETE_EFFECTIVE_ANGLE_AND_FULL_MODEL_OPERATOR_BINDING_SOURCE_INVERSE.json']);s.check(len(proof['files'])==17 and len(proof['changed_source_files'])==4,'exact finite original17 Source inverse scope')
    inverses=[]
    for entry in proof['files']:
        a=current(entry['original_source_pin']);b=current(entry['new_source_pin']);old=Path(a['path']).read_bytes();new=Path(b['path']).read_bytes();result=[];oldpos=0;newpos=0
        for chunk in entry['complete_byte_changes']:
            ob,oe,nb,ne=[chunk[k] for k in ['old_begin','old_end','new_begin','new_end']];ov=bytes.fromhex(chunk['old_hex']);nv=bytes.fromhex(chunk['new_hex'])
            s.check(ob>=oldpos and nb>=newpos and old[ob:oe]==ov and new[nb:ne]==nv and old[oldpos:ob]==new[newpos:nb],'exact all Source hunks and unchanged intervening bytes')
            result.extend([old[oldpos:ob],nv]);oldpos=oe;newpos=ne
        result.append(old[oldpos:]);s.check(b''.join(result)==new and old[oldpos:]==new[newpos:],'all17 complete forward/inverse Source bytes verified')
        inverses.append(dict(old_current_pin=a,new_current_pin=b,changed_hunks=len(entry['complete_byte_changes'])))
    copy=json.loads(contents['COMPLETE_MATHEMATICAL_DEPENDENCY_SOURCE_COPY_PROOF.json'])
    for entry in copy['files']:
        a=current(entry['original']);b=current(entry['copy']);s.check(Path(a['path']).read_bytes()==Path(b['path']).read_bytes(),'all11 mathematical origin copies full bytes')
    priorpin=s.pin(REC/'independent_reference_v2_finite_source_review_20261012/INDEPENDENT_SOURCE_REVIEW.json');prior=s.exact_json(priorpin)
    s.check(len(prior['checks'])==153 and all(row['passed'] is True for row in prior['checks']) and prior['full_reference_qualified'] is False and prior['numerical_job_executed'] is False,'full historical153 review read; Source-only scope retained')
    for row in prior['source_pins']:current(row)
    plan=json.loads(contents['CURRENT_FORMAL_FULL370_INPUT_PLAN_SOURCE_ONLY.json'])
    for row in nested(plan):current(row)
    formal=read_current(plan['protected_formal_and_producer_plan_pin'])
    for row in nested(formal):current(row)
    producer_proofs=[];controls=[]
    for row in formal['producers']:
        reportpin=current(row['report']);report=s.exact_json(reportpin)
        s.check(len(report['records'])==4 and all(x['status']=='PASS' for x in report['records']) and report['failure'] is None and report['actual_native_terminal']==row['native_readback'],'current producer summaries each contain four production PASS, not21')
        output_table={p['path']:p for p in report['output_pins']}
        for record in report['records']:
            wp=Path(reportpin['path']).parent/(record['label']+'.watchdog.json');lp=Path(reportpin['path']).parent/(record['label']+'.log')
            w=read_current(output_table[str(wp)]);current(output_table[str(lp)])
            s.check(w['returncode']==0 and w['limit_failure'] is None and w['command']==record['command'] and w['own_child_only'] is True and w['liveness_group_cleanup'] is True and w['rss_cap_mib']==512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and 0<=w['sampled_peak_rss_mib']<512,'all12 producer actual success watchdogs under original caps')
        producer_proofs.append(dict(plane=row['plane'],current_report_pin=reportpin,production_record_count=4,all_actual_production_stages_PASS=True,actual_native_terminal_equals_plan=True))
        exact_entry=[p for p in report['fixed_current_pins'] if p['path'].endswith('/Root_actual_entry_controls_summary.json') and ('current-warm-A'+str(row['plane'])+'-CLE-entry-controls-' in p['path'] if row['plane']>1 else 'current-warm-A-CLE-entry-controls-' in p['path'])]
        if not exact_entry:continue
        ep=current(exact_entry[0]);entry=s.exact_json(ep)
        s.check(len(entry['records'])==17 and sum(r['status']=='PASS' for r in entry['records'])==5 and sum(r['status']=='FAILED' for r in entry['records'])==12 and len(entry['actual_refusal_cases'])==12,'separate17 control receipt retains5PASS12 genuine refusals')
        oracle={r['case']:r['expected_abort'] for r in entry['declared_control_oracles']}
        for case in entry['actual_refusal_cases']:
            wp=current(case['actual_watchdog_pin']);lp=current(case['actual_log_pin']);w=s.exact_json(wp);log=Path(lp['path']).read_text()
            s.check(w['returncode']==1 and w['limit_failure'] is None and w['own_child_only'] is True and w['liveness_group_cleanup'] is True and w['rss_cap_mib']==512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and 0<=w['sampled_peak_rss_mib']<512 and log.count(oracle[case['case']])==1,'all separate strict refusals actual exit1/oracle/caps, never converted toPASS')
        controls.append(dict(plane=row['plane'],entry_report_current_pin=ep,records=17,positive_count=5,strict_refusal_count=12,all12_actual_exit1_oracles_and_watchdogs_verified=True))
    # Existing current GENDF provenance/data remains Source-only; no extraction.
    gendir=REC/'reaction_genDF_current_mount_stream_source_v2';gendf_files=[]
    for p in sorted(gendir.iterdir()):
        if not p.is_file():continue
        pin=s.pin(p);s.same(pin);gendf_files.append(pin)
        if p.suffix=='.json':
            for row in nested(json.loads(p.read_bytes())):current(row)
    gdhost=REC/'current_eleven_saved_gendf_current_mount_host_source_v4'
    for p in sorted(gdhost.iterdir()):
        if p.is_file():s.same(s.pin(p))
    mat=REC/'current_formal_material_authority_exact_cache70_source_v6';material_pins=[]
    for p in sorted(mat.rglob('*')):
        if p.is_file():row=s.pin(p);s.same(row);material_pins.append(row)
    functions={}
    for name in ['current_formal_input_authority.py','current_formal_full370_ray_operator.py','full370_unreduced_eigen.py']:
        functions[name]={node.name:node.lineno for node in ast.walk(ast.parse(contents[name])) if isinstance(node,(ast.FunctionDef,ast.ClassDef))}
    cpp=contents['current_full370_white_accumulate.cpp'].decode();s.check('std::vector<double> local_transfer(nz*nz*k,0.);' in cpp and 'std::vector<double> local_leakage(2*8*nz*k,0.);' in cpp and 'for(int i=0;i<nz;++i)for(int c=0;c<k;++c)' in cpp,'actual full dense peraction white accumulation cost Source')
    action=11364*4*2*2;local_values=(48*48+2*8*48)*370
    cost=dict(actual_declared_original_tracks=11364,angular_states=1536,actions_per_full_group_sweep=action,no_extra_times96=True,white_local_transfer_leakage_values_per_action=local_values,white_local_zero_bytes_per_action=local_values*8,white_preparation_local_zero_bytes_minimum=action*local_values*8,white_dense_aggregate_value_visits=action*local_values,white_T_bytes=288*288*370*8,white_L_bytes=2*8*288*370*8,phi9_full370_bytes=8*48*370*9*8,raw_P0_P1_P2_scatter64_bytes=8*3*370*370*8,one_ray_fields_upper_bytes=15*48*9*370*8,source_cache16_max_bytes=16*8*48*370*8,geometric_piece_count_static_upper=((16*49)-1)*32*(15+48),geometry_piece_and_length_raw_bytes_static_upper=((16*49)-1)*32*(15+48)*48,one_apply_full_transport_actions=2*action,each_apply_white_LU_systems=370,each_white_system_dimension=288,current_group_chunk_affects_LU_only_not_full370_volume_sweeps=True,walltime_or_peak_RSS_not_measured=True,original_child600_SELF512_and_host1800_not_admitted_by_static_formula=True)
    s.check(plan['required_actual_material_lineage_pin'] is None and plan['required_actual_kernel_control_pin'] is None and plan['required_actual_kernel_origin_pin'] is None,'all actual missing prerequisite PFs remain absent, not fabricated')
    for row in s.VERIFIED.values():s.check(s.seven(Path(row['path']).lstat())==row['identity'],'all current actual PFs stable at audit completion')
    result=dict(schema='READONLY_FULL_REFERENCE_V2_CURRENT_PF_SOURCE_ACTUAL_ADMISSION_GAP_REVIEW_V1',status='READONLY_REVIEW_COMPLETE_REFERENCE_STILL_UNADMITTED',current_package_file_pins=all_source_pins,original_source_package_count=17,current_inverse_proof_extra_count=1,all17_complete_Source_forward_inverse_verified=inverses,complete_python_AST_count=9,old153_review_current_pin=priorpin,old153_checks_allPASS_but_Source_only=True,old153_review_scope_limitations=prior['scope_limitations'],current_only_device_reattestations=TRANSITIONS,current_original_plan_still_stale_device34_internals=True,no_current_reference_Source_rebind_created=True,current_actual_production_reports=producer_proofs,separate_entry_controls_actual_proofs=controls,withdrawn_initial_false_report_assumption='A2/A3 17+4 meant two separate receipts; actual producer summaries each contain4 PASS, so current actual_success_report/len4 is not a blocker',all_actual_missing_required_reference_pins_still_null=True,functions_and_class_line_numbers=functions,static_full_scope_resource_inventory=cost,current_material_v6_all_files_pins=material_pins,current_GENDF_stream_v2_Source_and_provenance_pins=gendf_files,current_code_and_data_gaps_documented_in_REPORT=True,compiler_or_reference_business_or_reference_module_import_executed=False,old_Source_or_report_modified=False,nine_moments_not_inferred_from_three_observed=True,formal_SN32_angular_equivalence_not_proven=True,complete_AAA_material_authority_pending=True,B_ABA_material_authority_pending=True,physical_reaction_semantics_pending=True,full_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,full_EOF_unique_verified_files=len(s.VERIFIED),full_EOF_unique_verified_bytes=sum(r['size_bytes'] for r in s.VERIFIED.values()),checks=s.CHECKS,elapsed_seconds=time.monotonic()-START,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,reviewer_Source_pin=s.pin(Path(__file__).absolute()))
    path=OUT/'FULL_CURRENT_PF_SOURCE_AND_ACTUAL_ADMISSION_GAP_REVIEW.json';raw=(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode();fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status=result['status'],review_pin=s.pin(path),full_EOF_files=result['full_EOF_unique_verified_files'],full_EOF_bytes=result['full_EOF_unique_verified_bytes'],checks=result['checks'],original17_source_inverse_verified=True,old153_review_read=True,production_reports_records_each=[r['production_record_count'] for r in producer_proofs],white_dense_visits=cost['white_dense_aggregate_value_visits'],reference_business_executed=False)))

if __name__=='__main__':main()
