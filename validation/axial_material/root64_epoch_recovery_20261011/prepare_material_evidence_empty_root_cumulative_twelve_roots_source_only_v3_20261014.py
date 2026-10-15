"""Source only: retain typed-root fix and join previous eight transaction roots."""
import ast,base64,copy,hashlib,json,os
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'current_material_evidence_explicit_empty_MACROLIB_root_source_v2_20261014'
NEW=REC/'current_material_evidence_empty_root_cumulative_twelve_roots_source_v3_20261014'
def pin(p):
 p=Path(p);s=p.stat();ids=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 if s.st_size>64*2**20 or any(x.is_symlink()for x in(p,*p.parents)):raise RuntimeError('bounded ordinary Source metadata')
 b=p.read_bytes()
 if ids(p.stat())!=ids(s):raise RuntimeError('Source current7')
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))
def write(p,v):
 b=v if isinstance(v,bytes)else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 return pin(p)
def read(p):return json.loads(Path(p).read_bytes())
def splice(text,old,new):
 if text.count(old)!=1:raise RuntimeError('unique Source block '+old[:70])
 return text.replace(old,new)
def main():
 if NEW.exists():raise RuntimeError('new Source namespace immutable')
 oldplan=read(OLD/'EXPLICIT_EMPTY_MACROLIB_ROOT_INVENTORY_SOURCE_PLAN.json')
 arg=read(REC/'ROOT_EXACT_EIGHT_ROOT_FIRST_A_COMPLETE_AGGREGATE_ACTUAL_ARGV_20261014.json')
 requestpin=arg['request_pin'];request=read(requestpin['path'])
 if pin(requestpin['path'])!=requestpin or len(request['joint_archive_roots'])!=8:raise RuntimeError('actual prior eight-root request exactPF')
 priorroot=Path(request['owning_host_output_directory']);priorhostpin=pin(priorroot/'Root_actual_current_material_evidence_summary.json');priorhost=read(priorhostpin['path']);priorchildpin=priorhost['actual_complete_child_receipt']['report']
 if priorhost['operation']!='aggregate' or priorhost['failure']is not None or priorhost['after_check_error']is not None or priorhost['actual_intentional_exit2_normal_closure']is not True or requestpin not in priorhost['fixed_current_pins']:raise RuntimeError('real previous closed aggregate request binding; no mathematical qualification')
 builder=(OLD/'prepare_current_material_evidence_requests.py').read_text()
 original="    target=root/'CURRENT_ACTUAL_MATERIAL_EVIDENCE_REQUEST.json';write(target,request)\n"
 added='''    if args.operation == 'aggregate':
        prior_request_pin = sf['retained_actual_prior_aggregation_request_pin']
        prior_host_pin = sf['retained_actual_prior_aggregation_report_pin']
        prior_request = read(prior_request_pin, lambda:None)
        prior_host, prior_child, prior_child_pin = admit_evidence_host(prior_host_pin)
        require(prior_host['operation'] == 'aggregate' and prior_request['operation'] == 'aggregate' and
          prior_request['schema'] == 'CURRENT_FORMAL_MATERIAL_LINEAGE_EVIDENCE_REQUEST_V1' and
          prior_request_pin in prior_host['fixed_current_pins'] and
          prior_request['actual_observation_manifest_pin'] == mpin and
          prior_child['actual_observation_manifest_pin'] == mpin and
          prior_request['owning_host_output_directory'] == str(Path(prior_host_pin['path']).parent) and
          prior_request['output_directory'] == str(Path(prior_child_pin['path']).parent) and
          prior_request['joint_archive_roots'] == sf['retained_prior_joint_archive_roots'] and
          len(prior_request['joint_archive_roots']) == 8,
          'exact previous closed aggregate and original complete eight resource roots')
        request['original_current_eight_role_roots'] = list(request['joint_archive_roots'])
        for retained in prior_request['joint_archive_roots']:
            if retained not in request['joint_archive_roots']:
                request['joint_archive_roots'].append(retained)
        require(len(request['joint_archive_roots']) == 12 and
          len(set(request['joint_archive_roots'])) == 12 and
          not any(Path(a).is_relative_to(Path(b)) for a in request['joint_archive_roots']
                  for b in request['joint_archive_roots'] if a != b),
          'original eight plus previous aggregate pair and previous Source/request share unchanged2GiB')
        request['retained_actual_prior_aggregation_report_pin'] = prior_host_pin
        request['retained_actual_prior_aggregation_request_pin'] = prior_request_pin
        request['retained_prior_joint_archive_roots'] = prior_request['joint_archive_roots']
        request['prior_aggregation_mathematical_qualification_claimed'] = False
        request['complete_input_pins'] = unique(request['complete_input_pins'] +
          [prior_host_pin, prior_child_pin, prior_request_pin] +
          prior_host['fixed_current_pins'] + prior_host['complete_output_pins'])
'''+original
 newbuilder=splice(builder,original,added);ast.parse(newbuilder)
 writer=(OLD/'write_once_explicit_empty_MACROLIB_root_evidence_SF_HF_dynamic.py').read_text()
 old="proof+phase['fixed_current_pins']+phase['output_pins']:"
 new="proof+phase['fixed_current_pins']+phase['output_pins']+[plan['retained_actual_prior_aggregation_report_pin'],plan['retained_actual_prior_aggregation_request_pin'],plan['retained_actual_prior_aggregation_child_report_pin']]+read(plan['retained_actual_prior_aggregation_report_pin'])['fixed_current_pins']+read(plan['retained_actual_prior_aggregation_report_pin'])['complete_output_pins']:"
 newwriter=splice(writer,old,new)
 oldmeta="scientific_body_EOF_not_repeated_by_writer=True,empty_typed_MACROLIB_root_and_all19619_descendants_retained=True,only_DiskEvidence_inventory_record_contract_changed=True,physics_qualified=False)"
 newmeta="scientific_body_EOF_not_repeated_by_writer=True,empty_typed_MACROLIB_root_and_all19619_descendants_retained=True,only_DiskEvidence_inventory_and_request_cumulative_resource_metadata_changed=True,retained_actual_prior_aggregation_report_pin=plan['retained_actual_prior_aggregation_report_pin'],retained_actual_prior_aggregation_request_pin=plan['retained_actual_prior_aggregation_request_pin'],retained_prior_joint_archive_roots=plan['retained_prior_joint_archive_roots'],prior_aggregation_mathematical_qualification_claimed=False,physics_qualified=False)"
 newwriter=splice(newwriter,oldmeta,newmeta)
 newwriter=splice(newwriter,"status='EXPLICIT_EMPTY_MACROLIB_ROOT_EVIDENCE_SF_HF_DYNAMIC24_SOURCE_ONLY_PUBLISHED'","status='EMPTY_ROOT_CUMULATIVE_TWELVE_ROOTS_EVIDENCE_SF_HF_DYNAMIC24_SOURCE_ONLY_PUBLISHED'")
 ast.parse(newwriter)
 NEW.mkdir();copies=[];sources=[]
 for selected in oldplan['complete_source_file_pins_candidate']:
  p=Path(selected['path'])
  if p.parent==OLD:
   if pin(p)!=selected:raise RuntimeError('predecessor current SourcePF')
   before=p.read_bytes();after=newbuilder.encode()if p.name=='prepare_current_material_evidence_requests.py'else before
   cp=write(NEW/p.name,after);copies.append(dict(predecessor_pin=selected,candidate_pin=cp,whole_bytes_unchanged=before==after));sources.append(cp)
  else:sources.append(selected)
 binder=OLD/'bind_actual_completion_to_six_root_extract21_metadata_only.py'
 if not(NEW/binder.name).exists():
  cp=write(NEW/binder.name,binder.read_bytes());copies.append(dict(predecessor_pin=pin(binder),candidate_pin=cp,whole_bytes_unchanged=True))
 wp=write(NEW/'write_once_empty_root_cumulative_twelve_roots_evidence_SF_HF_dynamic.py',newwriter.encode())
 inverse=write(NEW/'COMPLETE_V2_TO_V3_PRIOR_AGGREGATE_CUMULATIVE_RESOURCE_SOURCE_BYTE_INVERSE.json',dict(schema='COMPLETE_PRIOR_AGGREGATE_CUMULATIVE_TWELVE_ROOTS_SOURCE_BYTE_INVERSE_V1',source_only=True,predecessor_empty_root_whole_engine_inverse_pin=oldplan['complete_byte_inverse_pin'],original_builder_Source_pin=pin(OLD/'prepare_current_material_evidence_requests.py'),candidate_builder_Source_pin=pin(NEW/'prepare_current_material_evidence_requests.py'),original_builder_whole_bytes_base64=base64.b64encode(builder.encode()).decode(),candidate_builder_whole_bytes_base64=base64.b64encode(newbuilder.encode()).decode(),original_request_write_block=original,candidate_cumulative_request_write_block=added,whole_builder_inverse_byte_equal=splice(newbuilder,added,original)==builder,original_writer_whole_bytes_base64=base64.b64encode(writer.encode()).decode(),candidate_writer_whole_bytes_base64=base64.b64encode(newwriter.encode()).decode(),writer_exact_original_candidate_blocks=[dict(original=old,candidate=new),dict(original=oldmeta,candidate=newmeta)],source_copies=copies,aggregation_engine_typed_root_fix_and_all_other_scientific_sources_whole_bytes_unchanged=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 plan=copy.deepcopy(oldplan)
 plan.update(schema='CURRENT_EVIDENCE_EMPTY_ROOT_CUMULATIVE_TWELVE_ROOTS_SOURCE_ONLY_PLAN_V3',source_copies=copies,complete_source_file_pins_candidate=sources,complete_byte_inverse_pin=inverse,predecessor_v2_Source_plan_pin=pin(OLD/'EXPLICIT_EMPTY_MACROLIB_ROOT_INVENTORY_SOURCE_PLAN.json'),retained_actual_prior_aggregation_report_pin=priorhostpin,retained_actual_prior_aggregation_request_pin=requestpin,retained_actual_prior_aggregation_child_report_pin=priorchildpin,retained_prior_joint_archive_roots=request['joint_archive_roots'],planned_cumulative_aggregate_root_count=12,prior_aggregation_mathematical_qualification_claimed=False,actual_request_pin=None,actual_aggregate_report_pin=None,actual_aggregate_post_pin=None,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_dynamic_interface_pin=None)
 pp=write(NEW/'EMPTY_ROOT_CUMULATIVE_TWELVE_ROOTS_SOURCE_PLAN.json',plan)
 ready=write(NEW/'SOURCE_REVIEW_READY.json',dict(schema='EMPTY_ROOT_CUMULATIVE_TWELVE_ROOTS_AGGREGATION_SOURCE_ONLY_READY_V3',source_only=True,host_source_pin=pin(NEW/'run_current_material_lineage_evidence.py'),builder_source_pin=pin(NEW/'prepare_current_material_evidence_requests.py'),scientific_child_source_pin=pin(NEW/'current_material_lineage_evidence.py'),split_binder_source_pin=pin(NEW/binder.name),aggregation_engine_source_pin=pin(NEW/'complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'),Source_author_pin=pin(Path(__file__).absolute()),plan_pin=pp,inverse_pin=inverse,writer_source_pin=wp,actual_request_pin=None,actual_aggregation_report_pin=None,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_dynamic_interface_pin=None,physics_qualified=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 fd=os.open(NEW,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='EMPTY_ROOT_CUMULATIVE_TWELVE_ROOTS_SOURCE_ONLY_READY_NO_PUBLICATION',Source_author_pin=pin(Path(__file__).absolute()),builder_source_pin=pin(NEW/'prepare_current_material_evidence_requests.py'),engine_source_pin=pin(NEW/'complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'),plan_pin=pp,inverse_pin=inverse,ready_pin=ready,writer_source_pin=wp,actual_aggregate_report_pin=None,planned_cumulative_root_count=12,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
