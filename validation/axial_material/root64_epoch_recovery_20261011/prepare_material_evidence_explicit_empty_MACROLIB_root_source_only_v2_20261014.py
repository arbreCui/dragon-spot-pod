"""Source preparation only: preserve the empty root and all19619 descendants."""
import ast,base64,hashlib,json,os
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'current_material_evidence_six_root_validation_scope_source_v1_20261014'
NEW=REC/'current_material_evidence_explicit_empty_MACROLIB_root_source_v2_20261014'
ENGINE='complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'
def pin(path):
 p=Path(path);s=p.lstat();ids=lambda t:[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
 if s.st_size>64*2**20 or any(a.is_symlink()for a in(p,*p.parents)):raise RuntimeError('bounded ordinary Source/metadata')
 with p.open('rb')as f:raw=f.read()
 if ids(p.lstat())!=ids(s):raise RuntimeError('current Source7')
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ids(s))
def read(path):return json.loads(Path(path).read_bytes())
def write(path,value):
 raw=value if isinstance(value,bytes)else(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
 with Path(path).open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(path)
def splice(text,old,new):
 if text.count(old)!=1:raise RuntimeError('exact unique metadata Source block '+old[:80])
 return text.replace(old,new)
def main():
 if NEW.exists():raise RuntimeError('new immutable Source namespace already exists')
 sf=read(OLD/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json')
 old_engine=(OLD/ENGINE).read_text()
 original='''    def inventory(self):
        """Full original micro+macro EOF payload hashes and all order evidence."""
        for original in self.saved.iter_all():
            row = original['record']
            for raw in self.saved.iter_raw(row):
                del raw
            self.records += 1
            self.macro_records += int(row['path'][:1] == ['MACROLIB'])
            self.line(self.coverage, original)
        require(self.macro_records == 19619, 'all original 19619 macro records retained')
        self.event('COMPLETE_ORIGINAL_COVERAGE', all_records=self.records,
                   macro_records=self.macro_records, raw_type_order_span_hash_preserved=True)
'''
 candidate='''    def inventory(self):
        """Full original micro+macro EOF payload hashes and all order evidence."""
        macro_root_records = macro_descendant_records = 0
        for original in self.saved.iter_all():
            row = original['record']
            for raw in self.saved.iter_raw(row):
                del raw
            self.records += 1
            self.macro_records += int(row['path'][:1] == ['MACROLIB'])
            if row['path'] == ['MACROLIB']:
                macro_root_records += 1
            elif row['path'][:1] == ['MACROLIB']:
                macro_descendant_records += 1
            self.line(self.coverage, original)
        macro_root = self.saved.row(('MACROLIB',))
        require(macro_root is not None and macro_root['path'] == ['MACROLIB'] and
                type(macro_root['kind']) is int and macro_root['kind'] == 0 and
                type(macro_root['declared_count']) is int and macro_root['declared_count'] == -1 and
                type(macro_root['original_word_count']) is int and macro_root['original_word_count'] == -1 and
                type(macro_root['native_payload_begin_byte']) is int and
                type(macro_root['native_payload_end_byte']) is int and
                macro_root['native_payload_begin_byte'] >= 0 and
                macro_root['native_payload_begin_byte'] == macro_root['native_payload_end_byte'] and
                macro_root['native_payload_sha256'] == 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
                'one original typed empty MACROLIB root retained')
        require(macro_root_records == 1 and macro_descendant_records == 19619 and
                self.macro_records == 19620,
                'all original19619 MACROLIB descendants plus one empty typed root retained')
        self.event('COMPLETE_ORIGINAL_COVERAGE', all_records=self.records,
                   macro_records=self.macro_records, macro_root_records=macro_root_records,
                   macro_descendant_records=macro_descendant_records,
                   raw_type_order_span_hash_preserved=True)
'''
 new_engine=splice(old_engine,original,candidate);ast.parse(new_engine)
 if splice(new_engine,candidate,original)!=old_engine:raise RuntimeError('whole engine inverse')
 old_writer=(OLD/'write_once_six_root_evidence_SF_HF_dynamic_v2.py').read_text()
 writer=old_writer
 writer=splice(writer,"ready=read(pin(BASE/'SOURCE_REVIEW_READY_v2.json'))","ready=read(pin(BASE/'SOURCE_REVIEW_READY.json'))")
 writer=splice(writer,"['host_source_pin','builder_source_pin','scientific_child_source_pin','split_binder_source_pin','plan_pin','inverse_pin']","['host_source_pin','builder_source_pin','scientific_child_source_pin','split_binder_source_pin','aggregation_engine_source_pin','plan_pin','inverse_pin']")
 writer=splice(writer,"pin(BASE/'SOURCE_REVIEW_READY_v2.json')","pin(BASE/'SOURCE_REVIEW_READY.json')")
 writer=splice(writer,"'same-round eight exact Source PFs'","'same-round nine exact Source PFs'") if "'same-round eight exact Source PFs'" in writer else splice(writer,"'same-round eight exact Source PFs'".replace('exact Source PFs','exact Source PFs'),"'same-round nine exact Source PFs'")
 writer=splice(writer,"scientific_body_EOF_not_repeated_by_writer=True,physics_qualified=False)","scientific_body_EOF_not_repeated_by_writer=True,empty_typed_MACROLIB_root_and_all19619_descendants_retained=True,only_DiskEvidence_inventory_record_contract_changed=True,physics_qualified=False)")
 writer=splice(writer,"status='SIX_ROOT_EVIDENCE_SF_HF_DYNAMIC24_SOURCE_ONLY_PUBLISHED'","status='EXPLICIT_EMPTY_MACROLIB_ROOT_EVIDENCE_SF_HF_DYNAMIC24_SOURCE_ONLY_PUBLISHED'")
 ast.parse(writer)
 NEW.mkdir();copies=[];sources=[]
 for selected in sf['complete_source_file_pins']:
  p=Path(selected['path'])
  if p.parent==OLD:
   if pin(p)!=selected:raise RuntimeError('predecessor whole Source PF')
   before=p.read_bytes();after=new_engine.encode()if p.name==ENGINE else before
   cp=write(NEW/p.name,after);copies.append(dict(predecessor_pin=selected,candidate_pin=cp,whole_bytes_unchanged=before==after));sources.append(cp)
  else:sources.append(selected)
 binder=OLD/'bind_actual_completion_to_six_root_extract21_metadata_only.py'
 if not(NEW/binder.name).exists():
  cp=write(NEW/binder.name,binder.read_bytes());copies.append(dict(predecessor_pin=pin(binder),candidate_pin=cp,whole_bytes_unchanged=True))
 wp=write(NEW/'write_once_explicit_empty_MACROLIB_root_evidence_SF_HF_dynamic.py',writer.encode())
 inverse=write(NEW/'COMPLETE_EMPTY_MACROLIB_ROOT_INVENTORY_AND_WRITER_SOURCE_WHOLE_BYTE_INVERSE.json',dict(schema='COMPLETE_EMPTY_TYPED_MACROLIB_ROOT_INVENTORY_SOURCE_BYTE_INVERSE_V1',source_only=True,original_engine_Source_pin=pin(OLD/ENGINE),candidate_engine_Source_pin=pin(NEW/ENGINE),original_engine_whole_bytes_base64=base64.b64encode(old_engine.encode()).decode(),candidate_engine_whole_bytes_base64=base64.b64encode(new_engine.encode()).decode(),original_inventory_complete_block=original,candidate_inventory_complete_block=candidate,whole_engine_inverse_byte_equal=True,all_other_engine_functions_classes_arithmetic_thresholds_and_payload_order_whole_bytes_unchanged=True,original_writer_Source_pin=pin(OLD/'write_once_six_root_evidence_SF_HF_dynamic_v2.py'),candidate_writer_Source_pin=wp,original_writer_whole_bytes_base64=base64.b64encode(old_writer.encode()).decode(),candidate_writer_whole_bytes_base64=base64.b64encode(writer.encode()).decode(),source_copies=copies,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 plan=write(NEW/'EXPLICIT_EMPTY_MACROLIB_ROOT_INVENTORY_SOURCE_PLAN.json',dict(schema='CURRENT_EVIDENCE_EXPLICIT_EMPTY_MACROLIB_ROOT_SOURCE_ONLY_PLAN_V2',source_only=True,predecessor_Source_freeze_pin=pin(OLD/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json'),predecessor_Host_freeze_pin=pin(OLD/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json'),predecessor_dynamic_pin=pin(OLD/'ROOT_REVIEWABLE_MATERIAL_EVIDENCE_DYNAMIC_INTERFACE_SOURCE_ONLY.json'),complete_source_file_pins_candidate=sources,source_copies=copies,complete_byte_inverse_pin=inverse,macro_total_record_count=19620,macro_descendant_record_count=19619,macro_empty_typed_root_count=1,root_payload_is_empty_not_removed=True,all_original_inventory_ordinals_original_records_payload_hashes_and_coverage_order_preserved=True,all_other_scientific_code_and_Fortran_whole_bytes_unchanged=True,original_resource_roots_and_joint2GiB_free8_history96_SELF512_child600_whole1800_unchanged=True,actual_request_pin=None,actual_aggregate_report_pin=None,actual_aggregate_post_pin=None,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_dynamic_interface_pin=None,physics_qualified=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 ready=write(NEW/'SOURCE_REVIEW_READY.json',dict(schema='EXPLICIT_EMPTY_MACROLIB_ROOT_AGGREGATION_SOURCE_ONLY_READY_V2',source_only=True,host_source_pin=pin(NEW/'run_current_material_lineage_evidence.py'),builder_source_pin=pin(NEW/'prepare_current_material_evidence_requests.py'),scientific_child_source_pin=pin(NEW/'current_material_lineage_evidence.py'),split_binder_source_pin=pin(NEW/binder.name),aggregation_engine_source_pin=pin(NEW/ENGINE),Source_author_pin=pin(Path(__file__).absolute()),plan_pin=plan,inverse_pin=inverse,writer_source_pin=wp,actual_request_pin=None,actual_aggregation_report_pin=None,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_dynamic_interface_pin=None,physics_qualified=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 fd=os.open(NEW,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='EXPLICIT_EMPTY_MACROLIB_ROOT_AGGREGATE_SOURCE_ONLY_READY_NO_PUBLICATION',Source_author_pin=pin(Path(__file__).absolute()),aggregation_engine_source_pin=pin(NEW/ENGINE),plan_pin=plan,inverse_pin=inverse,ready_pin=ready,writer_source_pin=wp,complete_Source_count=len(sources),local_copy_count=len(copies),actual_aggregate_report_pin=None,physics_qualified=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
