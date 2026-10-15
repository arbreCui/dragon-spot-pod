module SPOR64_A9
  ! The REAL64 outer solver: FLU2DR64_CORE, its rebalance and
  ! its outer acceleration.
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use SPOR64_A8, only : DOORFV64
  use SPOR64_RCONTRACT, only : SPOR64_ROUTE_CONTRACT
  implicit none
  private

  integer, parameter :: NGRP = 370
  integer, parameter :: NSLICE = 8
  integer, parameter :: NALBEDO = 6
  integer, parameter :: IINR_STRICT = 1
  integer, parameter :: IINR_NEAR = 2
  integer, parameter :: IINR_CAP = 3

  integer, parameter :: kind_guard = 1 / merge(1, 0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)

  public :: FLU2DR64_CORE, FLUBAL64, FLU2AC64
  public :: SPOR64_A9_TERMINAL64
  public :: SPOR64_A9_STATE_PROBE, SPOR64_A9_OPERATOR_PROBE
  public :: SPOR64_A9_COUNTER_PROBE

  interface
    subroutine ALSBD(n,is,b,ier,maxn)
      import :: real64
      integer :: n, is, ier, maxn
      real(real64) :: b(maxn,*)
    end subroutine ALSBD
  end interface

contains

  subroutine FLU2DR64_CORE(jpsys_group,iptrk,iftrak,impx,title, &
      keyflx_base1,matcod,vol32,xstrc32,xsdia0_32,keycur, &
      matalb_surface,albedo32,surfac32,njj_off,ijj_off,ipos_off, &
      nscat_off,scat_off32,fixed_source64,initial_flux64, &
      leak1d64,epsinr64,epsunk64,epsout64,contract,terminal_flux64, &
      terminal_source64,cutoff_visit64,accepted,ok)
    type(c_ptr), intent(in) :: jpsys_group, iptrk
    type(SPOR64_ROUTE_CONTRACT), intent(in) :: contract
    integer, intent(in) :: iftrak, impx
    character(len=72), intent(in) :: title
    integer, intent(in) :: keyflx_base1(:), matcod(:)
    integer, intent(in) :: keycur(:), matalb_surface(:)
    integer, intent(in) :: njj_off(:,:), ijj_off(:,:)
    integer, intent(in) :: ipos_off(:,:), nscat_off(:)
    real(real32), intent(in) :: vol32(:)
    real(real32), intent(in) :: xstrc32(0:,:), xsdia0_32(0:,:)
    real(real32), intent(in) :: albedo32(:), surfac32(:)
    real(real32), intent(in) :: scat_off32(:,:)
    real(real64), intent(in) :: fixed_source64(:,:), initial_flux64(:,:)
    real(real64), intent(in) :: leak1d64(:)
    real(real64), intent(in) :: epsinr64, epsunk64, epsout64
    real(real64), intent(out) :: terminal_flux64(:,:), terminal_source64(:,:)
    integer(int64), intent(out) :: cutoff_visit64
    logical, intent(out) :: accepted, ok

    integer :: akeep_index, allocation_status, ig, igdeb, igdeb_entry
    integer(int64) :: expected_tol64_bits
    integer :: iinr_state
    integer :: ir, it, jt, jg, jnd, ibm, ind, p
    integer :: acceleration_cycle, acceleration_free
    integer :: nreg, nmat, nunkno, nsout
    integer :: npsys(NGRP)
    integer(int64) :: cutoff_delta64
    logical :: accel_ok, balance_ok, child_ok, inner_finished
    logical :: norm_ok, operator_ok
    logical, allocatable :: seen_unknown(:)
    real(real64) :: akeep64(NSLICE), einr64, einr_last64
    real(real64) :: eext64, eunk64, group_error64, zmu64
    real(real64), allocatable :: flux64(:,:,:)
    real(real64) :: xcsou64(NGRP)

    terminal_flux64 = +0.0_real64
    terminal_source64 = +0.0_real64
    cutoff_visit64 = 0_int64
    accepted = .false.
    ok = .false.

    nreg = size(keyflx_base1)
    nmat = size(njj_off,1)
    nunkno = size(fixed_source64,1)
    nsout = size(keycur)
    if (nreg <= 0 .or. nmat <= 0 .or. nunkno <= 0 .or. nsout <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0088",'// &
        '"original_return_source_line":88,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nreg + nsout /= nunkno) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0089",'// &
        '"original_return_source_line":89,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(fixed_source64,2) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0090",'// &
        '"original_return_source_line":90,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(initial_flux64,1) /= nunkno .or. &
        size(initial_flux64,2) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0092",'// &
        '"original_return_source_line":92,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(terminal_flux64,1) /= nunkno .or. &
        size(terminal_flux64,2) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0094",'// &
        '"original_return_source_line":94,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(terminal_source64,1) /= nunkno .or. &
        size(terminal_source64,2) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0096",'// &
        '"original_return_source_line":96,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(matcod) /= nreg .or. size(vol32) /= nreg) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0097",'// &
        '"original_return_source_line":97,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(keycur) /= nsout .or. size(matalb_surface) /= nsout) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0098",'// &
        '"original_return_source_line":98,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(albedo32) /= NALBEDO .or. size(surfac32) /= nsout) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0099",'// &
        '"original_return_source_line":99,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(njj_off,2) /= NGRP .or. &
        any(shape(ijj_off) /= [nmat,NGRP]) .or. &
        any(shape(ipos_off) /= [nmat,NGRP])) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0102",'// &
        '"original_return_source_line":102,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(nscat_off) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0103",'// &
        '"original_return_source_line":103,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (lbound(xstrc32,1) /= 0 .or. ubound(xstrc32,1) /= nmat .or. &
        size(xstrc32,2) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0105",'// &
        '"original_return_source_line":105,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (lbound(xsdia0_32,1) /= 0 .or. ubound(xsdia0_32,1) /= nmat .or. &
        size(xsdia0_32,2) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0107",'// &
        '"original_return_source_line":107,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(scat_off32,1) /= nmat*NGRP .or. &
        size(scat_off32,2) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0109",'// &
        '"original_return_source_line":109,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(leak1d64) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0110",'// &
        '"original_return_source_line":110,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(seen_unknown(nunkno),stat=allocation_status)
    if (allocation_status /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0112",'// &
        '"original_return_source_line":112,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    if (.not. c_associated(jpsys_group) .or. &
        .not. c_associated(iptrk)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0115",'// &
        '"original_return_source_line":115,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (iftrak <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0116",'// &
        '"original_return_source_line":116,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (contract%flu_maxout <= 0 .or. contract%flu_maxinr <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0117",'// &
        '"original_return_source_line":117,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    acceleration_free = contract%flu_acce_free
    acceleration_cycle = acceleration_free + contract%flu_acce_accel
    if (acceleration_cycle <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0120",'// &
        '"original_return_source_line":120,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    expected_tol64_bits = transfer(real(transfer( &
        contract%eps_radial_bits,0.0_real32),real64),0_int64)
    if (transfer(epsinr64,0_int64) /= expected_tol64_bits) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0123",'// &
        '"original_return_source_line":123,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (transfer(epsunk64,0_int64) /= expected_tol64_bits) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0124",'// &
        '"original_return_source_line":124,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (transfer(epsout64,0_int64) /= expected_tol64_bits) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0125",'// &
        '"original_return_source_line":125,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(leak1d64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0126",'// &
        '"original_return_source_line":126,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(initial_flux64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0127",'// &
        '"original_return_source_line":127,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(fixed_source64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0128",'// &
        '"original_return_source_line":128,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (any(fixed_source64 < 0.0_real64)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0129",'// &
        '"original_return_source_line":129,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(vol32)) .or. &
        any(vol32 <= 0.0_real32)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0131",'// &
        '"original_return_source_line":131,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(xstrc32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0132",'// &
        '"original_return_source_line":132,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(xsdia0_32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0133",'// &
        '"original_return_source_line":133,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(albedo32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0134",'// &
        '"original_return_source_line":134,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(surfac32)) .or. &
        any(surfac32 <= 0.0_real32)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0136",'// &
        '"original_return_source_line":136,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    seen_unknown = .false.
    do ir = 1, nreg
      if (keyflx_base1(ir) < 1 .or. keyflx_base1(ir) > nunkno) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"FLU2DR64_CORE",'// &
          '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0140",'// &
          '"original_return_source_line":140,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      if (seen_unknown(keyflx_base1(ir))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"FLU2DR64_CORE",'// &
          '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0141",'// &
          '"original_return_source_line":141,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      seen_unknown(keyflx_base1(ir)) = .true.
      if (matcod(ir) < 1 .or. matcod(ir) > nmat) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"FLU2DR64_CORE",'// &
          '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0143",'// &
          '"original_return_source_line":143,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    end do
    do ir = 1, nsout
      if (keycur(ir) < 1 .or. keycur(ir) > nunkno) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"FLU2DR64_CORE",'// &
          '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0146",'// &
          '"original_return_source_line":146,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      if (seen_unknown(keycur(ir))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"FLU2DR64_CORE",'// &
          '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0147",'// &
          '"original_return_source_line":147,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      seen_unknown(keycur(ir)) = .true.
      if (matalb_surface(ir) > -1 .or. &
          matalb_surface(ir) < -NALBEDO) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"FLU2DR64_CORE",'// &
          '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0150",'// &
          '"original_return_source_line":150,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    end do
    if (.not. all(seen_unknown)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0152",'// &
        '"original_return_source_line":152,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    call VALIDATE_OFFGROUP32(njj_off,ijj_off,ipos_off,nscat_off, &
        scat_off32,operator_ok)
    if (.not. operator_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0156",'// &
        '"original_return_source_line":156,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    ! The owner storage is defined first.  Only the present outer flux is an
    ! ingress value; every other live slice is populated by the legacy copy
    ! order before it is used.
    allocate(flux64(nunkno,NGRP,NSLICE),stat=allocation_status)
    if (allocation_status /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2DR64_CORE",'// &
        '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0162",'// &
        '"original_return_source_line":162,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    flux64 = +0.0_real64
    flux64(:,:,2) = initial_flux64
    akeep64 = +0.0_real64
    do akeep_index = 5, 7
      akeep64(akeep_index) = 1.0_real64
    end do

    do it = 1, contract%flu_maxout
      flux64(:,:,4) = fixed_source64
      xcsou64 = +0.0_real64
      do ig = 1, NGRP
        do ir = 1, nreg
          ind = keyflx_base1(ir)
          xcsou64(ig) = xcsou64(ig) + flux64(ind,ig,4) * &
              real(vol32(ir),real64)
        end do
      end do
      if (.not. all(ieee_is_finite(xcsou64))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"FLU2DR64_CORE",'// &
          '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0180",'// &
          '"original_return_source_line":180,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if

      ! NBS is absent on the frozen route.  Preserve the legacy scan even
      ! though the admitted first-group integral proves IGDEB=1.
      igdeb = NGRP + 1
      do ig = 1, NGRP
        if (xcsou64(ig) > 0.0_real64) then
          igdeb = ig
          exit
        end if
      end do
      if (igdeb /= 1 .or. xcsou64(1) <= 0.0_real64) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"FLU2DR64_CORE",'// &
          '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0191",'// &
          '"original_return_source_line":191,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if

      flux64(:,:,6) = flux64(:,:,2)
      iinr_state = 0
      einr_last64 = +0.0_real64
      inner_finished = .false.

      do jt = 1, contract%flu_maxinr
        flux64(:,igdeb:NGRP,7) = flux64(:,igdeb:NGRP,6)
        flux64(:,igdeb:NGRP,8) = flux64(:,igdeb:NGRP,4)

        ! Frozen isotropic ITPIJ=1 source construction.  Destination groups
        ! and regions ascend; the packed source group descends exactly as in
        ! FLU2DR.  Self scattering is already represented inside MCCG.
        do ig = igdeb, NGRP
          do ir = 1, nreg
            ibm = matcod(ir)
            ind = keyflx_base1(ir)
            jg = ijj_off(ibm,ig)
            do jnd = 1, njj_off(ibm,ig)
              p = ipos_off(ibm,ig) + ijj_off(ibm,ig) - jg
              if (jg /= ig) then
                flux64(ind,ig,8) = flux64(ind,ig,8) + &
                    real(scat_off32(p,ig),real64) * flux64(ind,jg,7)
              end if
              jg = jg - 1
            end do
          end do
        end do
        if (.not. all(ieee_is_finite(flux64(:,igdeb:NGRP,8)))) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"FLU2DR64_CORE",'// &
            '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0220",'// &
            '"original_return_source_line":220,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if

        npsys = 0
        do ig = igdeb, NGRP
          npsys(ig) = ig
        end do
        cutoff_delta64 = 0_int64
        call DOORFV64(jpsys_group,npsys,iptrk,iftrak,impx,NGRP,nunkno, &
            keyflx_base1,title,leak1d64,flux64(:,:,8),flux64(:,:,7), &
            contract,cutoff_delta64,child_ok)
        if (cutoff_delta64 < 0_int64) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"FLU2DR64_CORE",'// &
            '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0230",'// &
            '"original_return_source_line":230,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        if (cutoff_visit64 > huge(cutoff_visit64)-cutoff_delta64) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"FLU2DR64_CORE",'// &
            '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0231",'// &
            '"original_return_source_line":231,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        cutoff_visit64 = cutoff_visit64 + cutoff_delta64
        if (.not. child_ok) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"FLU2DR64_CORE",'// &
            '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0233",'// &
            '"original_return_source_line":233,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        if (.not. all(ieee_is_finite(flux64(:,igdeb:NGRP,7)))) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"FLU2DR64_CORE",'// &
            '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0234",'// &
            '"original_return_source_line":234,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if

        call FLUBAL64(matcod,vol32,keyflx_base1,xstrc32,xsdia0_32, &
            leak1d64,xcsou64,igdeb,keycur,matalb_surface,albedo32, &
            surfac32,njj_off,ijj_off,ipos_off,nscat_off,scat_off32, &
            flux64(:,:,7),balance_ok)
        if (.not. balance_ok) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"FLU2DR64_CORE",'// &
            '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0240",'// &
            '"original_return_source_line":240,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if

        if (mod(jt-1,acceleration_cycle) >= acceleration_free) then
          call FLU2AC64(NGRP,nunkno,igdeb,flux64(:,:,5:7), &
              akeep64(5:7),zmu64,accel_ok)
          if (.not. accel_ok) then
            write(6,'(A,I0,A)') &
              '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
              '"scope":"FLU2DR64_CORE",'// &
              '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0245",'// &
              '"original_return_source_line":245,'// &
              '"actual_boolean_status_integer":',merge(1,0,ok),'}'
            flush(6)
            return
          end if
        else
          zmu64 = 1.0_real64
        end if

        einr64 = +0.0_real64
        igdeb_entry = igdeb
        do ig = igdeb_entry, NGRP
          call SCALAR_GROUP_NORM64(flux64(:,ig,6),flux64(:,ig,7), &
              keyflx_base1,group_error64,norm_ok)
          if (.not. norm_ok) then
            write(6,'(A,I0,A)') &
              '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
              '"scope":"FLU2DR64_CORE",'// &
              '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0255",'// &
              '"original_return_source_line":255,'// &
              '"actual_boolean_status_integer":',merge(1,0,ok),'}'
            flush(6)
            return
          end if
          flux64(:,ig,5) = flux64(:,ig,6)
          flux64(:,ig,6) = flux64(:,ig,7)
          if (group_error64 < epsinr64 .and. igdeb == ig) then
            igdeb = igdeb + 1
          end if
          einr64 = max(einr64,group_error64)
        end do
        einr_last64 = einr64

        if (einr64 < epsinr64) then
          iinr_state = IINR_STRICT
          inner_finished = .true.
          exit
        end if
        ! This inherited near condition only schedules the next outer visit;
        ! SPOR64_A9_TERMINAL64 never treats it as acceptance.
        if (igdeb > 1 .and. einr64 < 10.0_real64*epsinr64) then
          iinr_state = IINR_NEAR
          inner_finished = .true.
          exit
        end if
      end do
      if (.not. inner_finished) iinr_state = IINR_CAP

      flux64(:,:,3) = flux64(:,:,7)
      flux64(:,:,4) = flux64(:,:,8)
      eext64 = +0.0_real64
      akeep64(3) = 1.0_real64

      eunk64 = +0.0_real64
      do ig = 1, NGRP
        call SCALAR_GROUP_NORM64(flux64(:,ig,2),flux64(:,ig,3), &
            keyflx_base1,group_error64,norm_ok)
        if (.not. norm_ok) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"FLU2DR64_CORE",'// &
            '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0289",'// &
            '"original_return_source_line":289,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        eunk64 = max(eunk64,group_error64)
      end do

      ! Accept only the unmodified fixed-point image.  An extrapolated
      ! state has not passed through the outer map and cannot be terminal.
      call SPOR64_A9_TERMINAL64(eext64,eunk64,einr_last64, &
          epsout64,epsunk64,epsinr64,iinr_state,it,accepted)
      if (accepted) then
        if (.not. all(ieee_is_finite(flux64(:,:,3)))) then
          accepted = .false.
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"FLU2DR64_CORE",'// &
            '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0300",'// &
            '"original_return_source_line":300,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        if (.not. all(ieee_is_finite(flux64(:,:,4)))) then
          accepted = .false.
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"FLU2DR64_CORE",'// &
            '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0304",'// &
            '"original_return_source_line":304,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        terminal_flux64 = flux64(:,:,3)
        terminal_source64 = flux64(:,:,4)
        ok = .true.
        return
      end if

      if (mod(it-1,acceleration_cycle) >= acceleration_free) then
        call FLU2AC64(NGRP,nunkno,1,flux64(:,:,1:3), &
            akeep64(1:3),zmu64,accel_ok)
        if (.not. accel_ok) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"FLU2DR64_CORE",'// &
            '"predicate_id":"A9_FLU2DR64_CORE_RETURN_L0315",'// &
            '"original_return_source_line":315,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
      else
        zmu64 = 1.0_real64
      end if
      flux64(:,:,1) = flux64(:,:,2)
      flux64(:,:,2) = flux64(:,:,3)
      akeep64(1) = akeep64(2)
      akeep64(2) = akeep64(3)
    end do

    ! Exhausting MAXOUT is a normal mathematical return.  It is not an
    ! accepted state and A9a has no publication capability.
    accepted = .false.
    ok = .true.
  end subroutine FLU2DR64_CORE

  subroutine FLUBAL64(matcod,vol32,keyflx_base1,xstrc32,xsdia0_32, &
      leak1d64,xcsou64,igdeb,keycur,matalb_surface,albedo32,surfac32, &
      njj_off,ijj_off,ipos_off,nscat_off,scat_off32,flux64,ok)
    integer, intent(in) :: matcod(:), keyflx_base1(:), igdeb
    integer, intent(in) :: keycur(:), matalb_surface(:)
    integer, intent(in) :: njj_off(:,:), ijj_off(:,:)
    integer, intent(in) :: ipos_off(:,:), nscat_off(:)
    real(real32), intent(in) :: vol32(:)
    real(real32), intent(in) :: xstrc32(0:,:), xsdia0_32(0:,:)
    real(real64), intent(in) :: leak1d64(:)
    real(real32), intent(in) :: albedo32(:), surfac32(:)
    real(real32), intent(in) :: scat_off32(:,:)
    real(real64), intent(in) :: xcsou64(:)
    real(real64), contiguous, intent(inout) :: flux64(:,:)
    logical, intent(out) :: ok

    integer :: ier, ifscat, igr, ioff, ir, isur, jgr, ngreb
    integer :: ibm, ind, p, nreg, nmat, nunkno, nsout
    real(real64), allocatable :: rebal64(:,:)

    ok = .false.
    nreg = size(matcod)
    nmat = size(njj_off,1)
    nunkno = size(flux64,1)
    nsout = size(keycur)
    if (nreg <= 0 .or. nmat <= 0 .or. nunkno <= 0 .or. nsout <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0356",'// &
        '"original_return_source_line":356,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nreg + nsout /= nunkno) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0357",'// &
        '"original_return_source_line":357,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (igdeb < 1 .or. igdeb > NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0358",'// &
        '"original_return_source_line":358,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(flux64,2) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0359",'// &
        '"original_return_source_line":359,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(keyflx_base1) /= nreg .or. size(vol32) /= nreg) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0360",'// &
        '"original_return_source_line":360,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(matalb_surface) /= nsout .or. &
        size(albedo32) /= NALBEDO .or. size(surfac32) /= nsout) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0362",'// &
        '"original_return_source_line":362,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(njj_off,2) /= NGRP .or. &
        any(shape(ijj_off) /= [nmat,NGRP]) .or. &
        any(shape(ipos_off) /= [nmat,NGRP])) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0365",'// &
        '"original_return_source_line":365,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(nscat_off) /= NGRP .or. size(leak1d64) /= NGRP .or. &
        size(xcsou64) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0367",'// &
        '"original_return_source_line":367,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (lbound(xstrc32,1) /= 0 .or. ubound(xstrc32,1) /= nmat .or. &
        size(xstrc32,2) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0369",'// &
        '"original_return_source_line":369,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (lbound(xsdia0_32,1) /= 0 .or. ubound(xsdia0_32,1) /= nmat .or. &
        size(xsdia0_32,2) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0371",'// &
        '"original_return_source_line":371,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(scat_off32,1) /= nmat*NGRP .or. &
        size(scat_off32,2) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0373",'// &
        '"original_return_source_line":373,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(xcsou64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0374",'// &
        '"original_return_source_line":374,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(flux64(:,igdeb:NGRP)))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0375",'// &
        '"original_return_source_line":375,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(vol32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0376",'// &
        '"original_return_source_line":376,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(xstrc32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0377",'// &
        '"original_return_source_line":377,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(xsdia0_32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0378",'// &
        '"original_return_source_line":378,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(albedo32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0379",'// &
        '"original_return_source_line":379,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(surfac32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0380",'// &
        '"original_return_source_line":380,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    ngreb = NGRP - igdeb + 1
    allocate(rebal64(NGRP,NGRP+1))
    rebal64 = +0.0_real64

    do igr = igdeb, NGRP
      ioff = igr - igdeb + 1
      rebal64(ioff,ngreb+1) = xcsou64(igr)

      do isur = 1, nsout
        if (-matalb_surface(isur) < 1 .or. &
            -matalb_surface(isur) > NALBEDO) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"FLUBAL64",'// &
            '"predicate_id":"A9_FLUBAL64_RETURN_L0392",'// &
            '"original_return_source_line":392,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        if (keycur(isur) < 1 .or. keycur(isur) > nunkno) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"FLUBAL64",'// &
            '"predicate_id":"A9_FLUBAL64_RETURN_L0393",'// &
            '"original_return_source_line":393,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        rebal64(ioff,ioff) = rebal64(ioff,ioff) + &
            (1.0_real64-real(albedo32(-matalb_surface(isur)),real64)) * &
            flux64(keycur(isur),igr) * real(surfac32(isur),real64)
      end do

      do ir = 1, nreg
        ibm = matcod(ir)
        if (ibm < 1 .or. ibm > nmat) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"FLUBAL64",'// &
            '"predicate_id":"A9_FLUBAL64_RETURN_L0401",'// &
            '"original_return_source_line":401,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        ind = keyflx_base1(ir)
        if (ind < 1 .or. ind > nunkno) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"FLUBAL64",'// &
            '"predicate_id":"A9_FLUBAL64_RETURN_L0403",'// &
            '"original_return_source_line":403,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        ifscat = ijj_off(ibm,igr) - njj_off(ibm,igr) + 1

        ! Already-converged groups contribute to the right-hand side.
        do jgr = ifscat, min(igdeb-1,ijj_off(ibm,igr))
          p = ipos_off(ibm,igr) + ijj_off(ibm,igr) - jgr
          if (p < 1 .or. p > nscat_off(igr)) then
            write(6,'(A,I0,A)') &
              '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
              '"scope":"FLUBAL64",'// &
              '"predicate_id":"A9_FLUBAL64_RETURN_L0409",'// &
              '"original_return_source_line":409,'// &
              '"actual_boolean_status_integer":',merge(1,0,ok),'}'
            flush(6)
            return
          end if
          rebal64(ioff,ngreb+1) = rebal64(ioff,ngreb+1) + &
              flux64(ind,jgr) * real(scat_off32(p,igr),real64) * &
              real(vol32(ir),real64)
        end do

        ! Non-converged groups form the active matrix in ascending group
        ! order, which is the legacy FLUBAL accumulation order.
        do jgr = max(ifscat,igdeb), ijj_off(ibm,igr)
          p = ipos_off(ibm,igr) + ijj_off(ibm,igr) - jgr
          if (p < 1 .or. p > nscat_off(igr)) then
            write(6,'(A,I0,A)') &
              '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
              '"scope":"FLUBAL64",'// &
              '"predicate_id":"A9_FLUBAL64_RETURN_L0419",'// &
              '"original_return_source_line":419,'// &
              '"actual_boolean_status_integer":',merge(1,0,ok),'}'
            flush(6)
            return
          end if
          if (jgr == igr) then
            rebal64(ioff,ioff) = rebal64(ioff,ioff) + &
                flux64(ind,igr) * &
                (real(xstrc32(ibm,igr),real64) - &
                 real(xsdia0_32(ibm,igr),real64) + &
                 leak1d64(igr)) * &
                real(vol32(ir),real64)
          else
            rebal64(ioff,jgr-igdeb+1) = &
                rebal64(ioff,jgr-igdeb+1) - flux64(ind,jgr) * &
                real(scat_off32(p,igr),real64) * &
                real(vol32(ir),real64)
          end if
        end do
      end do
    end do

    if (.not. all(ieee_is_finite(rebal64(:ngreb,:ngreb+1)))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0437",'// &
        '"original_return_source_line":437,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    call ALSBD(ngreb,1,rebal64,ier,NGRP)
    if (ier /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0439",'// &
        '"original_return_source_line":439,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(rebal64(:ngreb,ngreb+1)))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0440",'// &
        '"original_return_source_line":440,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    do igr = igdeb, NGRP
      ioff = igr - igdeb + 1
      do ind = 1, nunkno
        flux64(ind,igr) = flux64(ind,igr) * &
            rebal64(ioff,ngreb+1)
      end do
    end do
    if (.not. all(ieee_is_finite(flux64(:,igdeb:NGRP)))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLUBAL64",'// &
        '"predicate_id":"A9_FLUBAL64_RETURN_L0449",'// &
        '"original_return_source_line":449,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    ok = .true.
  end subroutine FLUBAL64

  subroutine FLU2AC64(ng,nun,ig0,flux64,akeep64,zmu64,ok)
    integer, intent(in) :: ng, nun, ig0
    real(real64), contiguous, intent(inout) :: flux64(:,:,:)
    real(real64), contiguous, intent(inout) :: akeep64(:)
    real(real64), intent(out) :: zmu64
    logical, intent(out) :: ok

    integer :: ig, ir
    real(real64) :: denom64, dmu64, nom64, r1_64, r2_64

    zmu64 = 1.0_real64
    ok = .false.
    if (ng < 1 .or. nun < 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2AC64",'// &
        '"predicate_id":"A9_FLU2AC64_RETURN_L0465",'// &
        '"original_return_source_line":465,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (ig0 < 1 .or. ig0 > ng) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2AC64",'// &
        '"predicate_id":"A9_FLU2AC64_RETURN_L0466",'// &
        '"original_return_source_line":466,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(flux64,1) /= nun .or. size(flux64,2) /= ng .or. &
        size(flux64,3) /= 3) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2AC64",'// &
        '"predicate_id":"A9_FLU2AC64_RETURN_L0468",'// &
        '"original_return_source_line":468,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(akeep64) /= 3) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2AC64",'// &
        '"predicate_id":"A9_FLU2AC64_RETURN_L0469",'// &
        '"original_return_source_line":469,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(flux64(:,ig0:ng,:)))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2AC64",'// &
        '"predicate_id":"A9_FLU2AC64_RETURN_L0470",'// &
        '"original_return_source_line":470,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(akeep64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2AC64",'// &
        '"predicate_id":"A9_FLU2AC64_RETURN_L0471",'// &
        '"original_return_source_line":471,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    nom64 = +0.0_real64
    denom64 = +0.0_real64
    do ig = ig0, ng
      do ir = 1, nun
        r1_64 = flux64(ir,ig,2) - flux64(ir,ig,1)
        r2_64 = flux64(ir,ig,3) - flux64(ir,ig,2)
        nom64 = nom64 + r1_64*(r2_64-r1_64)
        denom64 = denom64 + (r2_64-r1_64)*(r2_64-r1_64)
      end do
    end do
    if (.not. ieee_is_finite(nom64)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2AC64",'// &
        '"predicate_id":"A9_FLU2AC64_RETURN_L0483",'// &
        '"original_return_source_line":483,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. ieee_is_finite(denom64)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2AC64",'// &
        '"predicate_id":"A9_FLU2AC64_RETURN_L0484",'// &
        '"original_return_source_line":484,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    ! Exact zero is not a fitted cutoff.  It avoids an undefined division
    ! and retains the legacy no-acceleration state with ZMU=1.
    if (denom64 <= 0.0_real64) then
      ok = .true.
      return
    end if
    dmu64 = -nom64/denom64
    if (.not. ieee_is_finite(dmu64)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2AC64",'// &
        '"predicate_id":"A9_FLU2AC64_RETURN_L0493",'// &
        '"original_return_source_line":493,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (dmu64 > 0.0_real64) then
      zmu64 = dmu64
      do ig = ig0, ng
        do ir = 1, nun
          flux64(ir,ig,3) = flux64(ir,ig,2) + dmu64 * &
              (flux64(ir,ig,3)-flux64(ir,ig,2))
          flux64(ir,ig,2) = flux64(ir,ig,1) + dmu64 * &
              (flux64(ir,ig,2)-flux64(ir,ig,1))
        end do
      end do
      akeep64(3) = akeep64(2) + dmu64*(akeep64(3)-akeep64(2))
      akeep64(2) = akeep64(1) + dmu64*(akeep64(2)-akeep64(1))
    end if
    if (.not. all(ieee_is_finite(flux64(:,ig0:ng,:)))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2AC64",'// &
        '"predicate_id":"A9_FLU2AC64_RETURN_L0507",'// &
        '"original_return_source_line":507,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(akeep64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"FLU2AC64",'// &
        '"predicate_id":"A9_FLU2AC64_RETURN_L0508",'// &
        '"original_return_source_line":508,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    ok = .true.
  end subroutine FLU2AC64

  pure subroutine SPOR64_A9_TERMINAL64(eext64,eunk64,einr_last64, &
      epsout64,epsunk64,epsinr64,iinr_state,outer_iteration,accepted)
    real(real64), intent(in) :: eext64, eunk64, einr_last64
    real(real64), intent(in) :: epsout64, epsunk64, epsinr64
    integer, intent(in) :: iinr_state, outer_iteration
    logical, intent(out) :: accepted

    accepted = eext64 < epsout64 .and. eunk64 < epsunk64 .and. &
        einr_last64 < epsinr64 .and. iinr_state == IINR_STRICT .and. &
        outer_iteration >= 2
  end subroutine SPOR64_A9_TERMINAL64

  subroutine SPOR64_A9_STATE_PROBE(state64,ok)
    real(real64), contiguous, intent(in) :: state64(:,:,:)
    logical, intent(out) :: ok

    ok = size(state64,1) > 0 .and. size(state64,2) == NGRP .and. &
        size(state64,3) == NSLICE
    if (ok) ok = all(ieee_is_finite(state64))
  end subroutine SPOR64_A9_STATE_PROBE

  subroutine SPOR64_A9_OPERATOR_PROBE(operator32,ok)
    real(real32), contiguous, intent(in) :: operator32(:,:)
    logical, intent(out) :: ok

    ok = size(operator32) > 0
    if (ok) ok = all(ieee_is_finite(operator32))
  end subroutine SPOR64_A9_OPERATOR_PROBE

  subroutine SPOR64_A9_COUNTER_PROBE(counter64,ok)
    integer(int64), intent(in) :: counter64
    logical, intent(out) :: ok

    ok = counter64 >= 0_int64
  end subroutine SPOR64_A9_COUNTER_PROBE

  subroutine SCALAR_GROUP_NORM64(present64,new64,keyflx_base1, &
      group_error64,ok)
    real(real64), intent(in) :: present64(:), new64(:)
    integer, intent(in) :: keyflx_base1(:)
    real(real64), intent(out) :: group_error64
    logical, intent(out) :: ok

    integer :: ind, ir, nreg, nunkno
    real(real64) :: difference64, denominator64

    group_error64 = +0.0_real64
    denominator64 = +0.0_real64
    ok = .false.
    nreg = size(keyflx_base1)
    nunkno = size(present64)
    if (nreg <= 0 .or. nunkno <= 0 .or. size(new64) /= nunkno) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SCALAR_GROUP_NORM64",'// &
        '"predicate_id":"A9_SCALAR_GROUP_NORM64_RETURN_L0563",'// &
        '"original_return_source_line":563,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    do ir = 1, nreg
      ind = keyflx_base1(ir)
      if (ind < 1 .or. ind > nunkno) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"SCALAR_GROUP_NORM64",'// &
          '"predicate_id":"A9_SCALAR_GROUP_NORM64_RETURN_L0566",'// &
          '"original_return_source_line":566,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      difference64 = abs(present64(ind)-new64(ind))
      group_error64 = max(group_error64,difference64)
      denominator64 = max(denominator64,abs(new64(ind)))
    end do
    if (.not. ieee_is_finite(group_error64)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SCALAR_GROUP_NORM64",'// &
        '"predicate_id":"A9_SCALAR_GROUP_NORM64_RETURN_L0571",'// &
        '"original_return_source_line":571,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. ieee_is_finite(denominator64)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SCALAR_GROUP_NORM64",'// &
        '"predicate_id":"A9_SCALAR_GROUP_NORM64_RETURN_L0572",'// &
        '"original_return_source_line":572,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (denominator64 <= 0.0_real64) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SCALAR_GROUP_NORM64",'// &
        '"predicate_id":"A9_SCALAR_GROUP_NORM64_RETURN_L0573",'// &
        '"original_return_source_line":573,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    group_error64 = group_error64/denominator64
    if (.not. ieee_is_finite(group_error64)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"SCALAR_GROUP_NORM64",'// &
        '"predicate_id":"A9_SCALAR_GROUP_NORM64_RETURN_L0575",'// &
        '"original_return_source_line":575,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    ok = .true.
  end subroutine SCALAR_GROUP_NORM64

  subroutine VALIDATE_OFFGROUP32(njj_off,ijj_off,ipos_off,nscat_off, &
      scat_off32,ok)
    integer, intent(in) :: njj_off(:,:), ijj_off(:,:)
    integer, intent(in) :: ipos_off(:,:), nscat_off(:)
    real(real32), intent(in) :: scat_off32(:,:)
    logical, intent(out) :: ok

    integer :: ibm, ifscat, ig, last_position, nmat

    ok = .false.
    nmat = size(njj_off,1)
    if (nmat <= 0 .or. size(njj_off,2) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"VALIDATE_OFFGROUP32",'// &
        '"predicate_id":"A9_VALIDATE_OFFGROUP32_RETURN_L0590",'// &
        '"original_return_source_line":590,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (any(shape(ijj_off) /= [nmat,NGRP]) .or. &
        any(shape(ipos_off) /= [nmat,NGRP])) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"VALIDATE_OFFGROUP32",'// &
        '"predicate_id":"A9_VALIDATE_OFFGROUP32_RETURN_L0592",'// &
        '"original_return_source_line":592,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(nscat_off) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"VALIDATE_OFFGROUP32",'// &
        '"predicate_id":"A9_VALIDATE_OFFGROUP32_RETURN_L0593",'// &
        '"original_return_source_line":593,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(scat_off32,1) /= nmat*NGRP .or. &
        size(scat_off32,2) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"VALIDATE_OFFGROUP32",'// &
        '"predicate_id":"A9_VALIDATE_OFFGROUP32_RETURN_L0595",'// &
        '"original_return_source_line":595,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    do ig = 1, NGRP
      if (nscat_off(ig) < 0 .or. nscat_off(ig) > nmat*NGRP) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"VALIDATE_OFFGROUP32",'// &
          '"predicate_id":"A9_VALIDATE_OFFGROUP32_RETURN_L0597",'// &
          '"original_return_source_line":597,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      if (nscat_off(ig) > 0) then
        if (.not. all(ieee_is_finite( &
            scat_off32(1:nscat_off(ig),ig)))) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"VALIDATE_OFFGROUP32",'// &
            '"predicate_id":"A9_VALIDATE_OFFGROUP32_RETURN_L0600",'// &
            '"original_return_source_line":600,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
      end if
      do ibm = 1, nmat
        if (njj_off(ibm,ig) < 0) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"VALIDATE_OFFGROUP32",'// &
            '"predicate_id":"A9_VALIDATE_OFFGROUP32_RETURN_L0603",'// &
            '"original_return_source_line":603,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        if (njj_off(ibm,ig) == 0) cycle
        if (ipos_off(ibm,ig) < 1) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"VALIDATE_OFFGROUP32",'// &
            '"predicate_id":"A9_VALIDATE_OFFGROUP32_RETURN_L0605",'// &
            '"original_return_source_line":605,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        last_position = ipos_off(ibm,ig) + njj_off(ibm,ig) - 1
        if (last_position > nscat_off(ig)) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"VALIDATE_OFFGROUP32",'// &
            '"predicate_id":"A9_VALIDATE_OFFGROUP32_RETURN_L0607",'// &
            '"original_return_source_line":607,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        if (ijj_off(ibm,ig) < 1 .or. ijj_off(ibm,ig) > NGRP) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"VALIDATE_OFFGROUP32",'// &
            '"predicate_id":"A9_VALIDATE_OFFGROUP32_RETURN_L0608",'// &
            '"original_return_source_line":608,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        ifscat = ijj_off(ibm,ig) - njj_off(ibm,ig) + 1
        if (ifscat < 1) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"VALIDATE_OFFGROUP32",'// &
            '"predicate_id":"A9_VALIDATE_OFFGROUP32_RETURN_L0610",'// &
            '"original_return_source_line":610,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
      end do
    end do
    ok = .true.
  end subroutine VALIDATE_OFFGROUP32

end module SPOR64_A9
