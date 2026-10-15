#!/usr/bin/env python3
"""Write exact v4 control plans once the genuine Source-only build4 HF exists."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import stat

REC=Path(__file__).resolve().parent
BUILD=REC/'bq64_compact_expected_build_host_source_v4_20261013'
COMMON_DIR=REC/'post_curated66_current_catalog_common_source_v2_20261013'
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
 b=p.read_bytes();assert len(b)==s.st_size and ids(p.lstat())==ids(s)
 return b,dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))
def read(p):
 b,pf=pin(p);return json.loads(b),pf
def put(folder,name,value):
 b=(json.dumps(value,indent=2)+'\n').encode();p=folder/name;fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
 try:assert os.write(fd,b)==len(b);os.fsync(fd)
 finally:os.close(fd)
 return pin(p)[1]
def main():
 csf,csfpf=read(COMMON_DIR/'COMPLETE_POST_CURATED66_CURRENT_CATALOG_BINDING_COMMON_SOURCE_FREEZE.json')
 assert csfpf['sha256']=='e2b380b7acf9d0d550adf260420454f2a08f16380e41f1d66bd6b7f678aae5d9'
 assert csf['schema']=='COMPLETE_POST_CURATED66_CURRENT_CATALOG_BINDING_COMMON_SOURCE_ONLY_FREEZE_V1'
 assert csf['source_only']is True and csf['compiled']is False and csf['numerical_executed']is False
 for pf in csf['files']+csf['original_source_metadata_pins']:assert pin(pf['path'])[1]==pf
 bp,bppf=read(BUILD/'EXACT_ORIGINAL70_TO_COMPACT_BQ64_BUILD_PLAN.json')
 hf,hfpf=read(BUILD/'COMPLETE_BQ64_COMPACT_EXPECTED_BUILD_HOST_SOURCE_FREEZE.json')
 hostbytes,hostpf=pin(BUILD/'build_bq64_compact_expected_runtime.py')
 assert hf['compiler_executed']is False and hf['numerical_executed']is False
 assert hostpf['sha256']=='97c65524edcb0649f0f33c426ffd155f192794e48fe20cb4280922fb7d1bd8f0'
 # Exact build4 Source owns the selected new Common and the unchanged original flags/order/caps.
 assert bp['planned_output_root'].endswith('-20261013-v4')
 assert csf['new_Common_Source_pin']['path'].encode()in hostbytes or b"post_curated66_current_catalog_common_source_v2_20261013"in hostbytes
 assert csf['new_Common_Source_pin']['sha256'].encode()in hostbytes
 table={x['path']:x for x in hf['dependencies']}
 for pf in [csfpf,csf['new_Common_Source_pin'],csf['new_catalog_pin'],csf['new_binding_pin'],csf['actual_release_receipt_pin'],csf['actual_independent_postrelease_review_pin']]:
  assert table.get(pf['path'])==pf
 results=[]
 for kind,stem in [('model','bq64_private_GANLIB_model_control_host'),('public','public_read_compact_bq_admission_control_host')]:
  folder=REC/(stem+'_source_v4_20261013');oldfolder=REC/(stem+'_source_v3_20261013')
  oldplan,oldplanpf=read(oldfolder/'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json')
  ownbytes,ownpf=pin(folder/('run_guarded_'+kind+'_controls.py'));ast.parse(ownbytes)
  plan=copy.deepcopy(oldplan)
  oldroot=oldplan['new_build_expected_build_directory'].removesuffix('/build')
  newroot=bp['planned_output_root']
  # Change exactly the necessary own Source/build4 Source dependencies and path literals.
  def paths(value):
   if isinstance(value,str):return value.replace(oldroot,newroot)
   if isinstance(value,list):return[paths(v)for v in value]
   if isinstance(value,dict):return{k:paths(v)for k,v in value.items()}
   return value
  for key in ['new_build_expected_report_path','new_build_expected_BOOTQ_object_path','new_build_expected_Dragon_path',
              'new_build_expected_build_directory','new_build_compile_include_arguments']:
   plan[key]=paths(plan[key])
  plan['host_source_pin']=ownpf
  plan['planned_output_root']=oldplan['planned_output_root'].removesuffix('v3')+'v4'
  plan['selected_new_build_Host_freeze_pin']=hfpf
  plan['selected_new_build_Host_source_pin']=hostpf
  plan['selected_new_build_plan_pin']=bppf
  plan['selected_post_release_Common_Source_freeze_pin']=csfpf
  plan['selected_post_release_Common_Source_pin']=csf['new_Common_Source_pin']
  plan['selected_post_release_current_catalog_pin']=csf['new_catalog_pin']
  plan['selected_post_release_current_binding_pin']=csf['new_binding_pin']
  plan['actual_exact_release_receipt_pin']=csf['actual_release_receipt_pin']
  plan['actual_exact_release_true_tool_return_pin']=csf['actual_release_true_tool_return_pin']
  plan['actual_independent_postrelease_review_pin']=csf['actual_independent_postrelease_review_pin']
  plan['actual_independent_postrelease_true_tool_return_pin']=csf['actual_independent_postrelease_true_tool_return_pin']
  assert plan['original_compile_flags']==bp['original_compile_flags']
  assert plan['original_compile_include_arguments']==bp['original_compile_include_arguments']
  assert plan['original_ordered70_paths']==[x['path']for x in bp['original_ordered70_input_pins']]
  assert plan['original_caps']==bp['original_caps']
  assert all(plan[k]is None for k in ['future_actual_new_build70_report_pin','future_actual_control_object_pin',
      'future_actual_control_executable_pin','future_actual_control_report_pin','future_actual_stale_manifests'])
  planpf=put(folder,'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json',plan)
  deltas={k:oldplan.get(k)for k in set(oldplan)|set(plan)if oldplan.get(k)!=plan.get(k)}
  back=copy.deepcopy(plan)
  for key,previous in deltas.items():
   if key in oldplan:back[key]=previous
   else:back.pop(key)
  assert back==oldplan
  invpf=put(folder,'COMPLETE_V3_TO_V4_CONTROL_PLAN_WHOLE_DATA_INVERSE.json',
    dict(schema='COMPLETE_COMPACT_BQ_CONTROL_PLAN_V3_TO_V4_WHOLE_DATA_INVERSE_V1',original_plan_pin=oldplanpf,
      new_plan_pin=planpf,exact_original_changed_field_values=deltas,
      complete_canonical_data_inverse_observed=True,all_original_control_flags_caps_oracles_unchanged=True,
      future_actual_pins_none=True,Host_imported=False,compiler_executed=False,numerical_executed=False))
  literal,_=read(folder/'HOST_LITERAL_SOURCE_REVIEW_READY_PENDING_EXACT_NEWBUILD4_PLAN.json')
  ready=put(folder,'HOST_SOURCE_REVIEW_READY.json',
    dict(schema='COMPACT_BQ_CONTROL_HOST_SOURCE_REVIEW_READY_V1',kind=kind,source_only=True,
      compiler_executed=False,numerical_executed=False,Host_imported=False,host_source=ownpf,
      control_host_plan_pin=planpf,complete_plan_data_inverse_pin=invpf,
      complete_host_byte_inverse_pin=literal['complete_byte_inverse_pin'],
      selected_control_Source_freeze_pin=plan['selected_control_Source_freeze_pin'],
      selected_new_build_Host_freeze_pin=hfpf,selected_post_release_Common_Source_freeze_pin=csfpf,
      future_independent_Host_review_pin=None,future_Host_freeze_pin=None,future_actual_control_report_pin=None,
      reader_qualified=False,AAA_qualified=False,ABA_admitted=False))
  results.append(dict(kind=kind,host_source_pin=ownpf,control_host_plan_pin=planpf,source_review_ready_pin=ready,complete_plan_inverse_pin=invpf))
 print(json.dumps({'status':'TWO_V4_CONTROL_HOST_PLANS_EXACT_NEWBUILD4_HF_AND_POSTRELEASE_COMMON_SOURCE_ONLY','packages':results,
    'selected_new_build_Host_freeze_pin':hfpf,'selected_post_release_Common_Source_freeze_pin':csfpf,
    'Host_imported':False,'compiler_executed':False,'numerical_executed':False,'future_actual_build_report_pin':None}))
if __name__=='__main__':main()
