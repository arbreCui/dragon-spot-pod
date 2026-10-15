"""Source-only explicit2383 consumption projection; no reports or scientific bodies changed."""
import ast,base64,copy,hashlib,json,os
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'current_material_evidence_empty_root_cumulative_twelve_roots_source_v4_20261014'
NEW=R/'current_material_evidence_compare_three_exact_current_projection_source_v5_20261014'
A=R/'independent_compare_three_formal_producer_input_plan_current_metadata_audit_20261014'
def pin(p):
 p=Path(p);s=p.lstat();b=p.read_bytes();ids=lambda x:[x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
 if s.st_size>64*2**20 or any(x.is_symlink()for x in(p,*p.parents))or ids(p.lstat())!=ids(s):raise RuntimeError('bounded ordinary current Source/metadata')
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))
def read(p):return json.loads(Path(p).read_bytes())
def write(p,v):
 b=v if isinstance(v,bytes)else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 return pin(p)
def splice(text,a,b):
 if text.count(a)!=1:raise RuntimeError('one exact consumer metadata block '+a[:70])
 return text.replace(a,b)
def main():
 if NEW.exists():raise RuntimeError('immutable new Source namespace')
 audit=read(A/'REVIEW.json');supp=read(A/'OUTPUT_PIN_SUPPLEMENT_REVIEW.json')
 for d,schema,status in [(audit,'INDEPENDENT_COMPARE_THREE_FORMAL_PRODUCER_INPUT_CURRENT_METADATA_AUDIT_V1','PASS_COMPARE_THREE_FORMAL_PRODUCER_INPUT_EXACT_CURRENT_METADATA_AUDIT'),(supp,'INDEPENDENT_COMPARE_THREE_PRODUCER_OUTPUT_PIN_CURRENT_METADATA_SUPPLEMENT_V1','PASS_COMPARE_THREE_PRODUCER_OUTPUT_PIN_CURRENT_METADATA_SUPPLEMENT')]:
  if d['schema']!=schema or d['status']!=status or d['failure']is not None or d['source_only']is not True or any(d[k]is not False for k in ['business_executed','compiler_executed','numerical_executed','files_deleted']):raise RuntimeError('real exact complete metadata audit')
 rows=audit['exact_rebinding_enumeration']+supp['exact_rebinding_enumeration']
 if len(rows)!=2383 or len(audit['exact_rebinding_enumeration'])!=2345 or len(supp['exact_rebinding_enumeration'])!=38 or supp['original_metadata_audit_pin']!=pin(A/'REVIEW.json'):raise RuntimeError('complete actual2345+38 enumeration')
 table={}
 for row in rows:
  old=row['historical_pin'];new=row['canonical_current_full_EOF_pin']
  if old['path']in table or old['path']!=new['path']or old['sha256']!=new['sha256']or old['size_bytes']!=new['size_bytes']or row['changed_identity_indices']!=[0]or old['identity'][0]!=16777234 or new['identity'][0]!=16777229 or old['identity'][1:]!=new['identity'][1:]or row['exact_source_catalog_match']is not True or row['exact_latest_MF9914_match']is not True:raise RuntimeError('exact explicit historical/current pair, no generic device rule')
  s=Path(new['path']).lstat()
  if [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]!=new['identity']:raise RuntimeError('explicit current7')
  table[old['path']]=(old,new)
 def project(p):
  if p['path']not in table or table[p['path']][0]!=p:raise RuntimeError('every consumed declaration has one exact enumerated original pin')
  return copy.deepcopy(table[p['path']][1])
 original_plan=read(audit['actual_original_plan_pin']['path']);formal=copy.deepcopy(original_plan)
 formal['formal_inputs']=[project(p)for p in original_plan['formal_inputs']]
 by_report={};all_projected=[]
 for n,row in enumerate(original_plan['producers'],1):
  updated=formal['producers'][n-1]
  for key in ['report','archive','radial_binary_track']:updated[key]=project(row[key])
  if updated['native_readback']!=row['native_readback']:raise RuntimeError('original numerical readback retained')
  rp=updated['report']
  if rp!=audit['actual_producer_report_current_fullpins'][n-1]or pin(rp['path'])!=rp:raise RuntimeError('exact original sealed producer report')
  report=read(rp['path']);fixed=[project(p)for p in report['fixed_current_pins']];outputs=[project(p)for p in report['output_pins']]
  if len(outputs)!=21 or len(fixed)!=audit['producer_fixed_pin_declaration_counts'][n-1]or report['output_pins']!=supp['actual_output_pin_declarations_by_plane'][str(n)]:raise RuntimeError('exact complete fixed and21 output declarations')
  by_report[rp['path']]=dict(plane=n,actual_original_report_pin=rp,projected_fixed_current_pins=fixed,projected_output_pins=outputs,original_report_not_modified=True)
  all_projected+=fixed+outputs
 current_arg=read(R/'ROOT_EXACT_EMPTY_ROOT_CUMULATIVE12_FIRST_A_COMPLETE_AGGREGATE_ACTUAL_ARGV_20261014.json');prior_request_pin=current_arg['request_pin'];prior_request=read(prior_request_pin['path']);prior_host_pin=pin(Path(prior_request['owning_host_output_directory'])/'Root_actual_current_material_evidence_summary.json');prior_host=read(prior_host_pin['path']);prior_child_pin=prior_host['actual_complete_child_receipt']['report']
 if len(prior_request['joint_archive_roots'])!=12 or prior_host['operation']!='aggregate'or prior_host['failure']is not None or prior_host['actual_intentional_exit2_normal_closure']is not True:raise RuntimeError('actual corrected aggregate complete12 resource roots')
 sf=read(OLD/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json');builder=(OLD/'prepare_current_material_evidence_requests.py').read_text()
 a="            producers=[]\n            for plane,row in enumerate(formal['producers'],1):\n"
 b="""            projection_pin=sf['current_producer_consumption_projection_pin']
            projection=read(projection_pin,lambda:None)
            require(projection['schema']=='EXPLICIT_CURRENT_PRODUCER_REPORT_CONSUMPTION_PROJECTION_V1'and
              projection['current_formal_plan_pin']==fpin and projection['original_reports_not_modified']is True,
              'exact separately bound current consumption projection, never replacement producer report')
            request['complete_input_pins']=unique(request['complete_input_pins']+[projection_pin])
            producers=[]
            for plane,row in enumerate(formal['producers'],1):
                projected=projection['by_original_report_path'][row['report']['path']]
                require(projected['actual_original_report_pin']==row['report']and projected['plane']==plane,
                  'same original sealed producer and exact projected consumption arrays')
"""
 c="report['fixed_current_pins']+report['output_pins'])"
 d="projected['projected_fixed_current_pins']+projected['projected_output_pins'])"
 e="    target=root/'CURRENT_ACTUAL_MATERIAL_EVIDENCE_REQUEST.json';write(target,request)\n"
 f="""    if args.operation=='compare-three':
        retained_request_pin=sf['retained_current_corrected_aggregation_request_pin']
        retained_host_pin=sf['retained_current_corrected_aggregation_report_pin']
        retained_request=read(retained_request_pin,lambda:None)
        retained_host,retained_child,retained_child_pin=admit_evidence_host(retained_host_pin)
        require(retained_host['operation']=='aggregate'and retained_request['operation']=='aggregate'and
          retained_request_pin in retained_host['fixed_current_pins']and
          retained_request['actual_observation_manifest_pin']==mpin and
          retained_request['joint_archive_roots']==sf['retained_corrected_aggregation_joint_archive_roots']and
          len(retained_request['joint_archive_roots'])==12,
          'retain exact corrected aggregation12 roots, original child2 is factual not mathematical qualification')
        request['current_compare_eight_role_roots']=list(request['joint_archive_roots'])
        for retained in retained_request['joint_archive_roots']:
            if retained not in request['joint_archive_roots']:request['joint_archive_roots'].append(retained)
        require(len(set(request['joint_archive_roots']))==len(request['joint_archive_roots'])==16 and
          not any(Path(a).is_relative_to(Path(b))for a in request['joint_archive_roots']for b in request['joint_archive_roots']if a!=b),
          'new compare8 plus actual retained aggregation12 union16, original joint2GiB not reset')
        request['retained_current_corrected_aggregation_request_pin']=retained_request_pin
        request['retained_current_corrected_aggregation_report_pin']=retained_host_pin
        request['complete_input_pins']=unique(request['complete_input_pins']+[retained_request_pin,retained_host_pin,retained_child_pin]+
          retained_host['fixed_current_pins']+retained_host['complete_output_pins'])
"""+e
 edits=[(a,b),(c,d),(e,f)];candidate=builder
 for x,y in edits:candidate=splice(candidate,x,y)
 ast.parse(candidate);restored=candidate
 for x,y in reversed(edits):restored=splice(restored,y,x)
 if restored!=builder:raise RuntimeError('complete builder inverse')
 NEW.mkdir();fp=write(NEW/'CURRENT_FORMAL_AND_PRODUCER_INPUTS_EXACT_CURRENT_PROJECTION.json',formal)
 projection=write(NEW/'ACTUAL_PRODUCER_CURRENT_CONSUMPTION_PROJECTION.json',dict(schema='EXPLICIT_CURRENT_PRODUCER_REPORT_CONSUMPTION_PROJECTION_V1',source_only=True,current_formal_plan_pin=fp,original_formal_plan_pin=audit['actual_original_plan_pin'],original_metadata_audit_pin=pin(A/'REVIEW.json'),original_metadata_audit_tools_pin=pin(A/'TRUE_TOOL_RETURNS.json'),output_supplement_review_pin=pin(A/'OUTPUT_PIN_SUPPLEMENT_REVIEW.json'),output_supplement_tools_pin=pin(A/'OUTPUT_PIN_SUPPLEMENT_TRUE_TOOL_RETURNS.json'),explicit2383_rebinding_enumeration=rows,by_original_report_path=by_report,original_reports_not_modified=True,no_generic_device_rule_or_missing_skip=True,scientific_payload_or_native_tree_EOF_not_repeated=True,physics_qualified=False))
 copies=[];sources=[]
 for p in sf['complete_source_file_pins']:
  path=Path(p['path'])
  if path.parent==OLD:
   before=path.read_bytes();after=candidate.encode()if path.name=='prepare_current_material_evidence_requests.py'else before
   cp=write(NEW/path.name,after);copies.append(dict(predecessor_pin=p,candidate_pin=cp,whole_bytes_unchanged=before==after));sources.append(cp)
  else:sources.append(p)
 binder=OLD/'bind_actual_completion_to_six_root_extract21_metadata_only.py';bp=write(NEW/binder.name,binder.read_bytes());copies.append(dict(predecessor_pin=pin(binder),candidate_pin=bp,whole_bytes_unchanged=True))
 oldwriter=(OLD/'write_once_empty_root_cumulative_twelve_roots_evidence_SF_HF_dynamic_v2.py').read_text();writer=oldwriter
 x="['host_source_pin','builder_source_pin','scientific_child_source_pin','split_binder_source_pin','aggregation_engine_source_pin','plan_pin','inverse_pin']"
 y="['host_source_pin','builder_source_pin','scientific_child_source_pin','split_binder_source_pin','aggregation_engine_source_pin','current_formal_plan_pin','current_producer_projection_pin','plan_pin','inverse_pin']"
 writer_edits=[("SOURCE_REVIEW_READY_v2.json","SOURCE_REVIEW_READY.json"),(x,y),("'same-round nine exact Source PFs'","'same-round eleven exact Source PFs'"),("proof+phase['fixed_current_pins']+phase['output_pins']+[plan['retained_actual_prior_aggregation_report_pin']","proof+phase['fixed_current_pins']+phase['output_pins']+plan['projection_current_live_pins']+plan['projection_metadata_authority_pins']+[plan['retained_actual_prior_aggregation_report_pin']"),("newsf.update(provenance,complete_source_file_pins=source,candidate_executed=False,compiler_executed=False,material_job_executed=False)","newsf.update(provenance,complete_source_file_pins=source,current_producer_consumption_projection_pin=ready['current_producer_projection_pin'],current_formal_producer_plan_pin=ready['current_formal_plan_pin'],retained_current_corrected_aggregation_request_pin=plan['retained_current_corrected_aggregation_request_pin'],retained_current_corrected_aggregation_report_pin=plan['retained_current_corrected_aggregation_report_pin'],retained_corrected_aggregation_joint_archive_roots=plan['retained_corrected_aggregation_joint_archive_roots'],candidate_executed=False,compiler_executed=False,material_job_executed=False)"),("status='EMPTY_ROOT_CUMULATIVE_TWELVE_ROOTS_EVIDENCE_SF_HF_DYNAMIC24_SOURCE_ONLY_PUBLISHED'","status='COMPARE_THREE_EXACT_CURRENT_PROJECTION_SF_HF_DYNAMIC24_SOURCE_ONLY_PUBLISHED'")]
 for x,y in writer_edits:
  count=writer.count(x)
  if count not in (1,2):raise RuntimeError('exact writer metadata splice')
  writer=writer.replace(x,y)
 ast.parse(writer);wp=write(NEW/'write_once_compare_three_current_projection_SF_HF_dynamic.py',writer.encode())
 iv=write(NEW/'COMPLETE_COMPARE_CURRENT_PROJECTION_CONSUMER_SOURCE_BYTE_INVERSE.json',dict(schema='COMPLETE_COMPARE_CURRENT_PROJECTION_SOURCE_BYTE_INVERSE_V1',source_only=True,original_builder_whole_bytes_base64=base64.b64encode(builder.encode()).decode(),candidate_builder_whole_bytes_base64=base64.b64encode(candidate.encode()).decode(),builder_unique_splices=[dict(original=x,candidate=y)for x,y in edits],whole_builder_inverse_byte_equal=True,original_writer_whole_bytes_base64=base64.b64encode(oldwriter.encode()).decode(),candidate_writer_whole_bytes_base64=base64.b64encode(writer.encode()).decode(),writer_splices=[dict(original=x,candidate=y)for x,y in writer_edits],source_copies=copies,original_scientific_child_and_aggregation_engine_and_owning_stage_math_fullbytes_unchanged=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 oldcontrol=read(OLD/'EMPTY_ROOT_CUMULATIVE_TWELVE_ROOTS_SOURCE_PLAN_v2.json')
 metadata=[pin(A/n)for n in ['REVIEW.json','TRUE_TOOL_RETURNS.json','OUTPUT_PIN_SUPPLEMENT_REVIEW.json','OUTPUT_PIN_SUPPLEMENT_TRUE_TOOL_RETURNS.json']]+[fp,projection,prior_request_pin,prior_host_pin,prior_child_pin]
 plan=copy.deepcopy(oldcontrol);plan.update(schema='COMPARE_THREE_EXACT_CURRENT_PROJECTION_SOURCE_ONLY_PLAN_V1',complete_source_file_pins_candidate=sources,source_copies=copies,complete_byte_inverse_pin=iv,projection_current_live_pins=all_projected,projection_metadata_authority_pins=metadata,retained_current_corrected_aggregation_request_pin=prior_request_pin,retained_current_corrected_aggregation_report_pin=prior_host_pin,retained_corrected_aggregation_joint_archive_roots=prior_request['joint_archive_roots'],current_formal_plan_pin=fp,current_producer_projection_pin=projection,planned_cumulative_compare_three_root_count=16,actual_compare_three_report_pin=None,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_dynamic_interface_pin=None)
 pp=write(NEW/'COMPARE_THREE_EXACT_CURRENT_PROJECTION_SOURCE_PLAN.json',plan)
 ready=write(NEW/'SOURCE_REVIEW_READY.json',dict(schema='COMPARE_THREE_EXACT_CURRENT_PROJECTION_SOURCE_ONLY_READY_V1',source_only=True,host_source_pin=pin(NEW/'run_current_material_lineage_evidence.py'),builder_source_pin=pin(NEW/'prepare_current_material_evidence_requests.py'),scientific_child_source_pin=pin(NEW/'current_material_lineage_evidence.py'),split_binder_source_pin=bp,aggregation_engine_source_pin=pin(NEW/'complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'),current_formal_plan_pin=fp,current_producer_projection_pin=projection,Source_author_pin=pin(Path(__file__).absolute()),plan_pin=pp,inverse_pin=iv,writer_source_pin=wp,actual_compare_three_report_pin=None,actual_request_pin=None,physics_qualified=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 fd=os.open(NEW,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='COMPARE_THREE_EXACT_CURRENT_PROJECTION_SOURCE_ONLY_READY_NO_PUBLICATION',Source_author_pin=pin(Path(__file__).absolute()),formal_plan_pin=fp,projection_pin=projection,builder_source_pin=pin(NEW/'prepare_current_material_evidence_requests.py'),plan_pin=pp,inverse_pin=iv,ready_pin=ready,writer_source_pin=wp,explicit_rebinding_count=2383,projected_output_count=63,cumulative_root_count=16,actual_compare_three_report_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
