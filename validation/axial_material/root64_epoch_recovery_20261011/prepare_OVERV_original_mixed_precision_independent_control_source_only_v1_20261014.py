"""Source preparation only. No ENERGY reads, compilation, native controls or models run."""
import hashlib,json,os,ast
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
NEW=REC/'OVERV_original_mixed_precision_independent_control_source_v1_20261014'
M=REC/'current_formal_material_authority_exact_cache70_post_literal3_latest_full50_source_v9_20261014'
def pin(p):
 p=Path(p);s=p.lstat();b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns])
def write(p,v):
 b=v if isinstance(v,bytes)else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 return pin(p)
def main():
 if NEW.exists():raise RuntimeError('immutable new control Source namespace')
 original=(M/'ORIGINAL_COMPLETE_LIBDEN.f').read_text()
 constants=Path('/Users/wen/spot/Utilib/src/XDRCST.f').read_text()
 start=original.index('      EVJ=XDRCST(');stop=original.index('\n',original.index('      SQFMAS=SQRT(2.0D4*EVJ/NMASS)'))+1
 const_calls=original[start:stop]
 start=original.index('      IF((.NOT.LOVERV).AND.');stop=original.index('      DEALLOCATE(GA1)',start)
 fallback=original[start:stop]
 replacements={'      SQFMAS=SQRT(2.0D4*EVJ/NMASS)':None,'         ENEAVG=SQRT(GA1(LLL)*GA1(LLL+1))':None,'         ZNU=1.0/(SQRT(ENEAVG)*SQFMAS)':None,'         GAR(IBM,1)=REAL(ZNU)':None}
 for line in replacements:
  if original.count(line)!=1:raise RuntimeError('one exact original arithmetic statement')
 control='''      PROGRAM OVERV_MIXED_PRECISION_ORIGINAL_CONTROL
      USE ISO_FORTRAN_ENV, ONLY: INT32,INT64
      IMPLICIT NONE
      INTEGER NGROUP,NBMIX,LLL,IBM,UNIT,IOS,NARG
      INTEGER(KIND=INT64) INPUT_BYTES
      PARAMETER (NGROUP=370,NBMIX=8)
      REAL GA1(NGROUP+1),GAR(NBMIX,1),ENEAVG
      DOUBLE PRECISION SQFMAS,XDRCST,NMASS,EVJ,ZNU
      LOGICAL LOVERV
      CHARACTER(LEN=4) HPRT1
      CHARACTER(LEN=4096) INPUT_PATH
      NARG=COMMAND_ARGUMENT_COUNT()
      IF(NARG.NE.1) ERROR STOP 'ONE ACTUAL RAW371 ENERGY INPUT'
      CALL GET_COMMAND_ARGUMENT(1,INPUT_PATH)
      INQUIRE(FILE=TRIM(INPUT_PATH),SIZE=INPUT_BYTES,IOSTAT=IOS)
      IF((IOS.NE.0).OR.(INPUT_BYTES.NE.1484)) THEN
        ERROR STOP 'EXACT371 REAL32 RAW WORDS'
      ENDIF
      OPEN(NEWUNIT=UNIT,FILE=TRIM(INPUT_PATH),STATUS='OLD',
     1 FORM='UNFORMATTED',ACCESS='STREAM',ACTION='READ',IOSTAT=IOS)
      IF(IOS.NE.0) ERROR STOP 'ACTUAL BOUND INPUT OPEN'
      READ(UNIT,IOSTAT=IOS) GA1
      CLOSE(UNIT)
      IF(IOS.NE.0) ERROR STOP 'ACTUAL371 ENERGY READ'
      LOVERV=.FALSE.
      HPRT1='N'
'''+const_calls+'''      IF(GA1(NGROUP+1).EQ.0.0) GA1(NGROUP+1)=1.0E-5
      WRITE(*,'(A,Z16.16,A,Z16.16,A,Z16.16,A)')
     1 '{"EVJ64_hex":"',TRANSFER(EVJ,0_INT64),
     2 '","NMASS64_hex":"',TRANSFER(NMASS,0_INT64),
     3 '","SQFMAS64_hex":"',TRANSFER(SQFMAS,0_INT64),'"}'
      IF((.NOT.LOVERV).AND.((HPRT1.EQ.'N').OR.(HPRT1.EQ.'NEUT').OR.
     1   (HPRT1.EQ.' '))) THEN
         DO 800 LLL=1,NGROUP
         ENEAVG=SQRT(GA1(LLL)*GA1(LLL+1))
         ZNU=1.0/(SQRT(ENEAVG)*SQFMAS)
         DO 790 IBM=1,NBMIX
         GAR(IBM,1)=REAL(ZNU)
  790    CONTINUE
         WRITE(*,'(A,I0,A)',ADVANCE='NO')
     1   '{"group":',LLL,',"OVERV32_hex":['
         DO IBM=1,NBMIX
           IF(IBM.GT.1) WRITE(*,'(A)',ADVANCE='NO') ','
           WRITE(*,'(A,Z8.8,A)',ADVANCE='NO')
     1     '"',TRANSFER(GAR(IBM,1),0_INT32),'"'
         ENDDO
         WRITE(*,'(A)') ']}'
  800    CONTINUE
      ENDIF
      WRITE(*,'(A)') '{"control_scope":"ORIGINAL_OVERV_FALLBACK_ONLY","physics_qualified":false,"historical_machine_bit_replay":false}'
      END
'''
 for line in replacements:
  if control.count(line)!=1:raise RuntimeError('each complete original arithmetic statement once')
 buildpost=json.loads((REC/'independent_material75_after_v18_saved370_v9_actual_build_postverify_20261014/REVIEW.json').read_bytes())
 build=json.loads(Path(buildpost['actual_report_pin']['path']).read_bytes())
 compile_record=next(s for s in build['records']if s['label']=='build/compile_2')
 if compile_record['status']!='PASS':raise RuntimeError('actual original LIBDEN compile provenance')
 selected_source=next(p for p in buildpost['actual_five_compiled_Source_pins']if Path(p['path']).name=='LIBDEN.observe.UNREADY.f')
 object_pin=next(p for p in buildpost['actual_five_observer_object_pins']if Path(p['path']).name=='LIBDEN.observe.UNREADY.o')
 archives=[p for p in buildpost['actual_original70_link_input_pins']if p['path'].endswith('.a')]
 if len(archives)!=4:raise RuntimeError('actual original four library archive roles')
 command=compile_record['command'];flags=command[1:command.index(next(a for a in command if a.startswith('-I')))]
 NEW.mkdir();cp=write(NEW/'OVERV_original_mixed_precision_control.f',control.encode())
 proof=write(NEW/'COMPLETE_ORIGINAL_OVERV_ARITHMETIC_STATEMENT_SOURCE_BINDING.json',dict(schema='ORIGINAL_OVERV_MIXED_PRECISION_ARITHMETIC_SOURCE_BINDING_V1',original_complete_LIBDEN_Source_pin=pin(M/'ORIGINAL_COMPLETE_LIBDEN.f'),actual_compiled_observed_LIBDEN_Source_pin=selected_source,actual_compiled_observed_LIBDEN_object_pin=object_pin,original_XDRCST_Source_pin=pin('/Users/wen/spot/Utilib/src/XDRCST.f'),original_XDRCST_whole_Source=constants,original_LIBDEN_constant_call_block=const_calls,original_LIBDEN_complete_fallback_publication_block=fallback,control_Source_pin=cp,each_original_arithmetic_statement_once_in_control=True,original_material_Source_not_modified=True,original_LCMPUT_publication_replaced_only_by_control_word_observation=True,not_an_original_whole_LIBDEN_invocation=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 spec=write(NEW/'FUTURE_ACTUAL_OVERV_INDEPENDENT_CONTROL_INPUT_SPEC_NULL.json',dict(schema='FUTURE_ACTUAL_OVERV_ORIGINAL_MIXED_PRECISION_CONTROL_INPUT_SPEC_V1',source_only=True,actual_ENERGY_record_parent_pin=None,actual_ENERGY371_original_raw_word_input_pin=None,actual_retained_OVERV370x8_comparison_word_pin=None,actual_guarded_control_Host_freeze_pin=None,actual_control_Root_true_tool_pin=None,actual_compiler_report_pin=None,actual_native_control_report_pin=None,actual_independent_binary64_and_binary32_rounding_oracle_report_pin=None,actual_independent_postreview_pin=None,all_future_actual_required_before_any_control_execution=True))
 plan=write(NEW/'ORIGINAL_OVERV_INDEPENDENT_CONTROL_SOURCE_PLAN.json',dict(schema='ORIGINAL_OVERV_INDEPENDENT_CONTROL_SOURCE_ONLY_PLAN_V1',source_only=True,control_Source_pin=cp,original_statement_binding_pin=proof,input_spec_pin=spec,selected_actual_observer75_build_report_pin=buildpost['actual_report_pin'],selected_actual_observer75_build_post_pin=pin(REC/'independent_material75_after_v18_saved370_v9_actual_build_postverify_20261014/REVIEW.json'),selected_actual_observer75_build_post_tools_pin=pin(REC/'independent_material75_after_v18_saved370_v9_actual_build_postverify_20261014/TRUE_TOOL_RETURNS.json'),actual_original_four_archive_pins=archives,actual_original_compile_command=command,original_selected_compiler_path=command[0],original_selected_compile_flags=flags,guard_Host_template_Source_pin=pin(REC/'bq64_private_GANLIB_model_control_host_source_v5_20261013/run_guarded_model_controls.py'),guard_Host_template_is_BQ_model_only_not_direct_OVERV_executable=True,required_genuine_guarded_stage_order=['compile_control','link_control','run_independent_control'],original_caps=dict(stage_seconds=600,whole_seconds=1800,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0),original_cumulative_resource_roots_must_be_retained_not_reset=True,control_native_program_argv=['future_control_executable','required_actual_1484_byte_ENERGY_input'],control_native_program_argv_count=2,required_independent_oracle=['original_constants_conversion_to_binary64','binary64_multiply_then_divide_then_sqrt_with_independent_rounding_bounds','binary32_energy_pair_product_then_sqrt_then_sqrt','original_binary64_ZNU_reciprocal_then_REAL32_demotion','all370x8_words_and_zero_last_energy_fallback','explicit_true_finite_domain_and_rejection_cases_without_new_tolerance'],no_existing_dedicated_OVERV_control_oracle_or_guarded_Host_claimed=True,no_compiler_or_control_oracle_executed=True,old_SOURCE_CONTEXT_NOT_SAVED_issue_not_removed_or_retagged=True,historical_machine_bit_replay=False,physics_qualified=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 ready=write(NEW/'SOURCE_ONLY_READY.json',dict(schema='ORIGINAL_OVERV_INDEPENDENT_CONTROL_SOURCE_ONLY_READY_V1',Source_author_pin=pin(Path(__file__).absolute()),control_Source_pin=cp,statement_binding_pin=proof,plan_pin=plan,future_input_spec_pin=spec,actual_controls=None,actual_guarded_Host=None,actual_oracle=None,actual_control_bits_qualified=False,physics_qualified=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 fd=os.open(NEW,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='OVERV_ORIGINAL_SOURCE_CONTROL_CANDIDATE_ONLY_NOT_GUARDED_EXECUTABLE',Source_author_pin=pin(Path(__file__).absolute()),control_Source_pin=cp,statement_binding_pin=proof,plan_pin=plan,input_spec_pin=spec,ready_pin=ready,actual_controls=None,physics_qualified=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
