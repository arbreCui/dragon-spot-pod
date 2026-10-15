#!/usr/bin/env python3
"""Prepare immutable Source only: one Driver bound literal plus exact-bit controls."""
import hashlib
import json
import os
from pathlib import Path
import stat

R = Path('/Users/wen/spot')
REC = R/'validation/axial_material/root64_epoch_recovery_20261011'
OLD = REC/'native_rank1_exact_block_cache_source_v1'
CTL = REC/'native_rank1_exact_block_cache_host_source_v1/test_generic_rank1_exact_cache_bits_with_abort.f90'
OUT = REC/'native_rank1_exact_cache336_source_v1_20261014'
ART = R/'validation/artifacts'

def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def read(path):
    path = Path(path)
    before = identity(path.lstat())
    if not stat.S_ISREG(before[2]):
        raise RuntimeError('regular exact Source required')
    fd = os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd)) != before:
            raise RuntimeError('opened Source7 changed')
        with os.fdopen(fd,'rb') as stream:
            fd = None
            data = stream.read()
            if identity(os.fstat(stream.fileno())) != before:
                raise RuntimeError('Source EOF7 changed')
    finally:
        if fd is not None:
            os.close(fd)
    if identity(path.lstat()) != before or len(data) != before[4]:
        raise RuntimeError('Source after7 changed')
    return data,dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity=before)

def put(path,data):
    if isinstance(data,dict):
        data = (json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    fd = os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    result = read(path)[1]
    if result['identity'][3] != 1:
        raise RuntimeError('own Source must have one link')
    return result

EXTRA = '''  ! This finite test proves an enabled cache's STORE budget rejection uses
  ! the genuine original solver, and mixed groups retain every solution bit.
  ! All original 301 assertions and 110 calls finish before this routine.
  subroutine enabled_budget_and_mixed_groups()
    type(SPOT1P64_R1_GENERIC_PLAN) :: empty
    integer(int64) :: table_one,table_two,key_bytes,store_bytes,charge,small_limit
    double precision :: h1(1,nl,nz,nr),h2(1,nl,nz,nr)
    double precision :: hc1(nz+1,nr),hc2(nz+1,nr),hx1(nq,nr),hx2(nq,nr)
    call setup()
    call SPOT1P64_R1_CACHE_CLEAR()
    call solve_group(1,q1,g1,c1,x1)
    call solve_group(1,q2,g2,c2,x2)
    call SPOT1P64_R1_CACHE_BEGIN(1,336_int64*1024_int64*1024_int64)
    call solve_group(1,q1,f,c,x)
    call equal_fields(f,c,x,g1,c1,x1)
    call check(SPOT1P64_R1_PLAN(1)%ready.and.SPOT1P64_R1_PLAN(1)%compressed)
    call SPOT1P64_R1_CACHE_STATS(nb,nruse,nmiss,nfallback,bytes,limit)
    call check(nb==nz+1.and.nruse==0.and.nmiss==1.and.nfallback==0.and.bytes<=limit)
    table_one=int(storage_size(empty)/8,int64)
    table_two=2_int64*table_one
    key_bytes=int(size(SPOT1P64_R1_PLAN(1)%key_i),int64)*4_int64+ &
      int(size(SPOT1P64_R1_PLAN(1)%key_r32),int64)*4_int64+ &
      int(size(SPOT1P64_R1_PLAN(1)%key_r64),int64)*8_int64
    charge=SPOT1P64_R1_PLAN(1)%charged_bytes
    store_bytes=charge-key_bytes
    call check(key_bytes>0_int64.and.store_bytes>0_int64.and.bytes==table_one+charge)
    small_limit=table_one+key_bytes+store_bytes-1_int64
    call SPOT1P64_R1_CACHE_BEGIN(1,small_limit)
    call solve_group(1,q1,f,c,x)
    call equal_fields(f,c,x,g1,c1,x1)
    call SPOT1P64_R1_CACHE_STATS(nb,nruse,nmiss,nfallback,bytes,limit)
    call check(nb==0.and.nruse==0.and.nmiss==1.and.nfallback==1)
    call check(bytes==table_one.and.limit==small_limit)
    call check(.not.SPOT1P64_R1_PLAN(1)%ready.and..not.allocated(SPOT1P64_R1_PLAN(1)%key_i))
    call solve_group(1,q2,f,c,x)
    call equal_fields(f,c,x,g2,c2,x2)
    call SPOT1P64_R1_CACHE_STATS(nb,nruse,nmiss,nfallback,bytes,limit)
    call check(nb==0.and.nruse==0.and.nmiss==2.and.nfallback==2)
    call check(bytes==table_one.and.bytes<=limit)
    call SPOT1P64_R1_CACHE_CLEAR()
    call solve_group(2,q1,h1,hc1,hx1)
    call solve_group(2,q2,h2,hc2,hx2)
    small_limit=table_two+2_int64*charge-1_int64
    call SPOT1P64_R1_CACHE_BEGIN(2,small_limit)
    call solve_group(1,q1,f,c,x)
    call equal_fields(f,c,x,g1,c1,x1)
    call SPOT1P64_R1_CACHE_STATS(nb,nruse,nmiss,nfallback,bytes,limit)
    call check(nb==nz+1.and.nruse==0.and.nmiss==1.and.nfallback==0.and.bytes<=limit)
    call check(SPOT1P64_R1_PLAN(1)%ready.and..not.SPOT1P64_R1_PLAN(2)%ready)
    call solve_group(2,q1,f,c,x)
    call equal_fields(f,c,x,h1,hc1,hx1)
    call SPOT1P64_R1_CACHE_STATS(nb,nruse,nmiss,nfallback,bytes,limit)
    call check(nb==nz+1.and.nruse==0.and.nmiss==2.and.nfallback==1.and.bytes<=limit)
    call check(SPOT1P64_R1_PLAN(1)%ready.and..not.SPOT1P64_R1_PLAN(2)%ready)
    call solve_group(1,q2,f,c,x)
    call equal_fields(f,c,x,g2,c2,x2)
    call SPOT1P64_R1_CACHE_STATS(nb,nruse,nmiss,nfallback,bytes,limit)
    call check(nb==nz+1.and.nruse==nz+1.and.nmiss==2.and.nfallback==1)
    call check(bytes==table_two+charge.and.limit==small_limit)
    call solve_group(2,q2,f,c,x)
    call equal_fields(f,c,x,h2,hc2,hx2)
    call SPOT1P64_R1_CACHE_STATS(nb,nruse,nmiss,nfallback,bytes,limit)
    call check(nb==nz+1.and.nruse==nz+1.and.nmiss==3.and.nfallback==2)
    call check(SPOT1P64_R1_PLAN(1)%ready.and.bytes==table_two+charge.and.bytes<=limit)
  end subroutine enabled_budget_and_mixed_groups
  subroutine solve_group(igroup,q,ff,cc,xx)
    integer,intent(in) :: igroup
    double precision,intent(in) :: q(1,nl,nz,nr)
    double precision,intent(out) :: ff(1,nl,nz,nr),cc(nz+1,nr),xx(nq,nr)
    call SPOT1P64(igroup,nr,nz,1,nm,ns,1,1,nq,nl,.false.,mat1d,vol1d,mat,total,sgas, &
      basis,vol2d,radial,ncode,zcode,q,du,w,pl,ff,cc,xx)
    calls=calls+1
  end subroutine solve_group
'''

def main():
    if OUT.exists():
        raise RuntimeError('unique candidate namespace already exists; never overwrite')
    driver,old_driver = read(OLD/'SPOT_GLOBAL_NATIVE_DRIVER64.f')
    math,old_math = read(OLD/'SPOT1P64.f90')
    control,old_control = read(CTL)
    old_literal = b'CALL SPOT1P64_R1_CACHE_BEGIN(NGRP,368_INT64*1024_INT64*'
    new_literal = b'CALL SPOT1P64_R1_CACHE_BEGIN(NGRP,336_INT64*1024_INT64*'
    if driver.count(old_literal) != 1 or driver.count(new_literal) != 0:
        raise RuntimeError('single exact original Driver cache-bound literal')
    new_driver = driver.replace(old_literal,new_literal)
    blocks = [
      dict(old='  call storage_checks()\n  call SPOT1P64_R1_CACHE_CLEAR()',
           new='  call storage_checks()\n  call enabled_budget_and_mixed_groups()\n  call SPOT1P64_R1_CACHE_CLEAR()'),
      dict(old='ACTUAL_GENERIC_RANK1_COMPONENT_BIT_CONTROLS_COMPLETED_ONLY',
           new='ACTUAL_GENERIC_RANK1_CACHE336_BUDGET_COMPONENT_BIT_CONTROLS_COMPLETED_ONLY'),
      dict(old='end program\n',new=EXTRA+'end program\n')]
    derived = control
    for row in blocks:
        a=row['old'].encode();b=row['new'].encode()
        if derived.count(a) != 1:
            raise RuntimeError('exact control Source splice once')
        derived=derived.replace(a,b)
    recovered=derived
    for row in reversed(blocks):
        a=row['old'].encode();b=row['new'].encode()
        if recovered.count(b) != 1:
            raise RuntimeError('control inverse splice once')
        recovered=recovered.replace(b,a)
    if recovered != control or new_driver.replace(new_literal,old_literal) != driver:
        raise RuntimeError('whole-file inverse must recover both original Sources')
    if EXTRA.count('call equal_fields(') != 7 or EXTRA.count('call check(') != 16 or EXTRA.count('call solve_group(') != 11:
        raise RuntimeError('finite new assertion/call Source accounting')
    paths=[OLD/'COMPLETE_NATIVE_RANK1_EXACT_BLOCK_CACHE_SOURCE_FREEZE.json',
      OLD/'CURRENT_GENERIC_RANK1_LOGICAL_MEMORY_AND_EXACT_KEY_CONTRACT.json',
      R/'Utilib/src/ALSBD.f',REC/'global_native64_caller_source_v1/FLUDRVG64.f',
      REC/'global_native64_caller_source_v1/FLUGLOBAL64.f',
      REC/'global_native64_dependency_source_v2/driver_source/SPOT_SPOF_NATIVE64.f',
      ART/'axial-material-new-BQ64-compact-expected-composed-complete70-build-only-20261013-v4/Root_actual_build_only_summary.json',
      ART/'axial-material-new-generic-rank1-exact-cache-bit-controls-20261012-v1/Root_actual_component_bit_summary.json',
      ART/'axial-material-new-generic-rank1-exact-cache-bit-controls-20261012-v1/controls/run_component.log',
      ART/'axial-material-new-generic-rank1-exact-cache-bit-controls-20261012-v1/controls/run_component.watchdog.json',
      REC/'independent_v15_GLOBAL_own_child512_failure_postverify_20261014/REVIEW.json',
      REC/'independent_v15_GLOBAL_own_child512_failure_postverify_20261014/TRUE_TOOL_RETURNS.json']
    rows=[]
    for path in paths:
        rows.append(read(path)[1])
    OUT.mkdir()
    pd=put(OUT/'SPOT_GLOBAL_NATIVE_DRIVER64.f',new_driver)
    pc=put(OUT/'test_generic_rank1_cache336_budget_bits_with_abort.f90',derived)
    inverse=put(OUT/'COMPLETE_DRIVER336_AND_CONTROL_WHOLE_BYTE_INVERSE.json',dict(
      schema='COMPLETE_NATIVE_RANK1_DRIVER336_CONTROL_BYTE_INVERSE_V1',source_only=True,
      original_driver_pin=old_driver,candidate_driver_pin=pd,driver_blocks=[dict(old=old_literal.decode(),new=new_literal.decode())],
      original_control_pin=old_control,candidate_control_pin=pc,control_blocks=blocks,
      both_whole_files_reverse_to_original_bytes=True,original_math_whole_file_pin=old_math,
      original_math_modified=False,Fortran_compiled=False,numerical_executed=False))
    plan=put(OUT/'CACHE336_EXACT_BIT_CONTROL_AND_RUNTIME_PLAN.json',dict(
      schema='NATIVE_RANK1_DRIVER336_EXACT_WORKSET_SOURCE_ONLY_PLAN_V1',source_only=True,
      compiler_executed=False,numerical_executed=False,source_freeze_future_pin=None,
      original_source_pins=[old_driver,old_math,old_control],candidate_source_pins=[pd,pc],
      complete_byte_inverse_pin=inverse,exact_source_evidence_pins=rows,
      old_cache_working_set_limit_bytes=368*2**20,new_cache_working_set_limit_bytes=336*2**20,
      reduction_bytes=32*2**20,resource_acceptance_unchanged=True,
      original_assertions_preserved=301,original_SPOT1P64_calls_preserved=110,
      finite_added_assertions=37,finite_added_actual_calls=11,expected_actual_assertions=338,
      expected_actual_SPOT1P64_calls=121,
      expected_actual_control_status='ACTUAL_GENERIC_RANK1_CACHE336_BUDGET_COMPONENT_BIT_CONTROLS_COMPLETED_ONLY',
      control_qualification='component bit controls only; never production reader or physics qualification',
      added_case_contracts=['enabled STORE rejection after exact keys fit, two full solves bit-equal to disabled-cache baselines',
        'two group cache: group1 stored then reused, group2 STORE rejected on both solves, every flux/cour/xnei INT64 bit equal'],
      required_stats='compiled descriptor plus measured exact key/store charges; genuine build/reuse/miss/fallback counters, bytes<=limit',
      fixed_compile_and_floating_order='original -O2 -march=native -ffp-contract=off -fcheck=all flags; original SPOT1P64 and ALSBD unchanged',
      actual_new_driver_object_pin=None,actual_new_Dragon_pin=None,actual_build_report_pin=None,
      actual_bit_control_report_pin=None,actual_full50_report_pin=None,
      complete70_replacement_zero_based_index=37,original70_other_input_count=69,
      retained_new_BOOTQ_index=40,retained_SPOT1P64_index=57,retained_archives=4,
      unchanged_caps=dict(SELF_and_child_RSS_bytes=512*2**20,stage_seconds=600,whole_seconds=1800,
        fresh_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,
        cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,retries=0,children=1,threads=1),
      actual_RSS_and_stage_cost_not_predicted=True))
    causal=put(OUT/'GLOBAL512_CACHE_WORKSET_SOURCE_CAUSAL_REVIEW.json',dict(
      schema='GLOBAL512_R1_CACHE_WORKSET_READONLY_SOURCE_CAUSAL_REVIEW_V1',status='PASS_SOURCE_ONLY_CANDIDATE_PREPARED',
      failure=None,source_only=True,compiled=False,numerical_executed=False,deletion_executed=False,
      exact_source_evidence_pins=rows,original_source_pins=[old_driver,old_math,old_control],
      new_source_pins=[pd,pc],inverse_pin=inverse,control_plan_pin=plan,
      old_GLOBAL_peak_MiB=507.09375,new_GLOBAL_peak_MiB=512.203125,difference_MiB=5.109375,
      old_GLOBAL_returncode=0,new_GLOBAL_returncode=-15,new_failure='own-child 512 MiB RSS cap reached',
      scope_evidence='both actual watchdogs own_child_only=true; parent SELF and filesystem auxiliary128 excluded',
      exact_allocation_cause_not_established=True,
      new_BOOTQ_not_called_by_GLOBAL=True,
      cache_lifecycle=dict(begin_line=710,strict_success_go_to_410_line=1495,
        nonconvergence_clear_lines=[1531,1532],successful_clear_lines=[1726,1727],
        conclusion='successful strict branch skips nonconvergence clear, retains cache through normalization and 370-group output publication'),
      R1_raw_key_comparison_lines=[284,301],R1_key_budget_reject_line=305,R1_store_budget_reject_line=344,
      original_fallback_ALSBD_lines=[963,977],all_group_and_RHS_loops_unchanged=True,
      bit_order_argument='complete INT32/INT64 LHS keys; RHS is rebuilt each call; FACTOR/SOLVE split retains ALSBD pivot rule and each RHS column arithmetic order; dense full-shape MATMUL and reverse block substitution unchanged',
      existing_real_component_evidence=dict(assertions=301,SPOT1P64_calls=110,elapsed_seconds=0.6969719160042587,
        cached_and_uncached_bitwise_mutation_cases=18,one_byte_disabled_bitwise_case=True,
        store_reject_existing_case_only_checked_store_false_and_stats=True),
      next_minimal_change='Driver one literal 368 to336 MiB internal exact-cache upper bound; unchanged solver fallbacks',
      excluded_changes=['no acceptance cap increase','no group/solver/pivot/eigen/float-sum-order change','no random retry','no physics or reader qualification'],
      optional_lifetime_change_not_selected='R1-only clear just after label410 is math-independent after final door call, but buffered logs do not prove peak timing; leave current Source lifecycle unchanged for this minimal candidate',
      future_compile_control_RSS_runtime_results=None,all_file_descriptors_closed=True))
    ready=put(OUT/'SOURCE_ONLY_READY.json',dict(status='READY_FOR_INDEPENDENT_SOURCE_REVIEW',failure=None,
      source_only=True,compiled=False,numerical_executed=False,candidate_driver_pin=pd,candidate_control_pin=pc,
      complete_byte_inverse_pin=inverse,control_plan_pin=plan,causal_review_pin=causal,
      preparer_pin=read(__file__)[1],final_Source_freeze_pin=None))
    print(json.dumps(dict(status='SOURCE_ONLY_PREPARATION_CLOSED0',ready_pin=ready,driver_pin=pd,
      control_pin=pc,inverse_pin=inverse,control_plan_pin=plan,causal_review_pin=causal),ensure_ascii=False),flush=True)

if __name__=='__main__':
    main()
