program TEST_B2S_IMMEDIATE_HOST_BRIDGE
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_loc, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use B2S_STUB_PROBES, only : xdrta2_calls, core_calls, event_count, &
      events, core_plane, captured_qfiss64, B2S_RESET_PROBES, &
      B2S_TERMINAL_FLUX, B2S_TERMINAL_SOURCE, B2S_QFISS_VALUE, &
      B2S_CUTOFF_VALUE
  use B2S_FIXTURE_SUPPORT, only : B2S_NSNAP, B2S_NGRP, B2S_NUNKNO, &
      B2S_NREG, B2S_BUILD_HYBRID, B2S_CLONE_ROOT, &
      B2S_REQUIRE_EMPTY_ROOT, B2S_REQUIRE_RECORD, B2S_REQUIRE_INTEGER, &
      B2S_REQUIRE_CHARACTER
  use SPOR64_B2S, only : SPOR64_B2S_DISABLED, SPOR64_B2S_FAILED, &
      SPOR64_B2S_RETURNED, SPOR64_B2S_HOST_BRIDGE
  implicit none

  character(len=1024) :: seed_path, macro_path, track_path
  character(len=1024) :: system_path, source_path, returned_path
  integer :: status, plane
  integer :: terminal_checks, mirror_checks, qfiss_checks
  integer(int64) :: cutoff(B2S_NSNAP)
  real(real64) :: k64, rho64
  type(c_ptr) :: seed_base, macro_base, track_base, system_base, source_base
  type(c_ptr) :: assembled, macros(B2S_NSNAP), sources(B2S_NSNAP)
  type(c_ptr) :: null_objects(B2S_NSNAP), duplicate_sources(B2S_NSNAP)
  type(c_ptr) :: duplicate_source, output, returned_xsm
  type(FIL_file), target :: fake_track
  logical :: returned_exists

  if (command_argument_count() /= 6) &
    error stop 'expected FLUX_OLD MACRO0 TRACK SYSTEM FSOURCE RETURNED paths'
  call get_command_argument(1,seed_path)
  call get_command_argument(2,macro_path)
  call get_command_argument(3,track_path)
  call get_command_argument(4,system_path)
  call get_command_argument(5,source_path)
  call get_command_argument(6,returned_path)
  inquire(file=trim(returned_path),exist=returned_exists)
  if (returned_exists) error stop 'B2S RETURNED XSM path already exists'

  call LCMOP(seed_base,trim(seed_path),2,2,0)
  call LCMOP(macro_base,trim(macro_path),2,2,0)
  call LCMOP(track_base,trim(track_path),2,2,0)
  call LCMOP(system_base,trim(system_path),2,2,0)
  call LCMOP(source_base,trim(source_path),2,2,0)
  if (.not. all([c_associated(seed_base),c_associated(macro_base), &
      c_associated(track_base),c_associated(system_base), &
      c_associated(source_base)])) error stop 'B2S read-only XSM open failed'

  call B2S_BUILD_HYBRID(seed_base,macro_base,track_base,system_base, &
      source_base,assembled,macros,sources,k64,rho64)
  fake_track%unit=77
  fake_track%kdi_file=c_null_ptr
  null_objects=c_null_ptr

  ! An omitted or false enable is a zero-access route.  Null pointers make
  ! any accidental LCM/FIL inspection fail loudly instead of passing by luck.
  call B2S_RESET_PROBES()
  cutoff=-1_int64
  call SPOR64_B2S_HOST_BRIDGE(c_null_ptr,c_null_ptr,null_objects, &
      null_objects,c_null_ptr,status,cutoff)
  if (status /= SPOR64_B2S_DISABLED .or. any(cutoff /= 0_int64)) &
    error stop 'B2S default-off result differs'
  call REQUIRE_NO_STUB_ACCESS('default off')
  cutoff=-1_int64
  call SPOR64_B2S_HOST_BRIDGE(c_null_ptr,c_null_ptr,null_objects, &
      null_objects,c_null_ptr,status,cutoff,.false.)
  if (status /= SPOR64_B2S_DISABLED .or. any(cutoff /= 0_int64)) &
    error stop 'B2S explicit-off result differs'
  call REQUIRE_NO_STUB_ACCESS('explicit off')

  ! Two distinct objects carry PLANE=2.  B2S must finish its three B2O
  ! seals and reject the duplicate label before XDRTA2 or the radial core.
  call B2S_CLONE_ROOT(sources(1),'B2S-DUP2',duplicate_source)
  duplicate_sources=[sources(1),duplicate_source,sources(3)]
  call OPEN_OUTPUT('B2S-DUP-OUT',output)
  call B2S_RESET_PROBES()
  cutoff=-1_int64
  call SPOR64_B2S_HOST_BRIDGE(output,assembled,macros,duplicate_sources, &
      c_loc(fake_track),status,cutoff,.true.)
  if (status /= SPOR64_B2S_FAILED .or. any(cutoff /= 0_int64)) &
    error stop 'B2S duplicate-plane result differs'
  call B2S_REQUIRE_EMPTY_ROOT(output)
  call REQUIRE_NO_STUB_ACCESS('duplicate plane')
  call LCMCL(output,2)
  call LCMCL(duplicate_source,2)

  ! A core failure on canonical plane 2 stops before plane 3 and before B2R;
  ! the caller-visible output stays empty.
  call OPEN_OUTPUT('B2S-FAIL-OUT',output)
  call B2S_RESET_PROBES(2)
  cutoff=-1_int64
  call SPOR64_B2S_HOST_BRIDGE(output,assembled,macros,sources, &
      c_loc(fake_track),status,cutoff,.true.)
  if (status /= SPOR64_B2S_FAILED) error stop 'B2S plane-2 failure accepted'
  call B2S_REQUIRE_EMPTY_ROOT(output)
  if (xdrta2_calls /= 2 .or. core_calls /= 2 .or. event_count /= 4) then
    write(*,'(A,3(I0,1X))') 'failure inventory XDR CORE EVENT=', &
        xdrta2_calls,core_calls,event_count
    error stop 'B2S plane-2 failure call inventory differs'
  end if
  if (any(events(1:4) /= [0,1,0,2])) &
    error stop 'B2S plane-2 failure call order differs'
  if (any(cutoff /= [B2S_CUTOFF_VALUE(1),B2S_CUTOFF_VALUE(2),0_int64])) &
    error stop 'B2S plane-2 failure cutoffs differ'
  call LCMCL(output,2)

  ! The accepted call is one immediate causal chain.  The caller supplies no
  ! SOLVED object: B2S owns the three private B2B products consumed by B2R.
  call OPEN_OUTPUT('B2S-RETURNED',output)
  call B2S_RESET_PROBES()
  cutoff=-1_int64
  call SPOR64_B2S_HOST_BRIDGE(output,assembled,macros,sources, &
      c_loc(fake_track),status,cutoff,.true.)
  if (status /= SPOR64_B2S_RETURNED) &
    error stop 'B2S canonical immediate bridge rejected'
  if (xdrta2_calls /= 3 .or. core_calls /= 3 .or. event_count /= 6) &
    error stop 'B2S canonical call inventory differs'
  if (any(events(1:6) /= [0,1,0,2,0,3])) &
    error stop 'B2S canonical call order differs'
  if (any(core_plane /= [1,2,3])) &
    error stop 'B2S canonical core plane order differs'
  do plane=1,B2S_NSNAP
    if (cutoff(plane) /= B2S_CUTOFF_VALUE(plane)) &
      error stop 'B2S canonical cutoff differs'
  end do

  terminal_checks=0
  mirror_checks=0
  qfiss_checks=0
  call VERIFY_CAPTURED_QFISS(qfiss_checks)
  call VERIFY_RETURNED(output,track_base,system_base,k64,rho64, &
      terminal_checks,mirror_checks,qfiss_checks)

  call LCMOP(returned_xsm,trim(returned_path),0,2,0)
  if (.not. c_associated(returned_xsm)) &
    error stop 'B2S RETURNED XSM creation failed'
  call LCMEQU(output,returned_xsm)
  call LCMCL(returned_xsm,1)

  call LCMCL(output,2)
  do plane=1,B2S_NSNAP
    call LCMCL(sources(plane),2)
    call LCMCL(macros(plane),2)
  end do
  call LCMCL(assembled,2)
  call LCMCL(source_base,1)
  call LCMCL(system_base,1)
  call LCMCL(track_base,1)
  call LCMCL(macro_base,1)
  call LCMCL(seed_base,1)

  write(*,'(A)') 'B2S IMMEDIATE-HOST-BRIDGE PASS'
  write(*,'(A)') 'B2S DEFAULT-OFF=0-ACCESS EXPLICIT-OFF=0-ACCESS'
  write(*,'(A)') 'B2S DUPLICATE-PLANE=PRE-CORE PLANE2-FAIL=EMPTY-OUTPUT'
  write(*,'(A,I0,A,I0,A,I0)') 'B2S XDRTA2=',xdrta2_calls, &
      ' STUB-CORE=',core_calls,' RETURNED=',1
  write(*,'(A,I0,A,I0,A,I0)') 'B2S TERMINAL64=',terminal_checks, &
      ' MIRROR32=',mirror_checks,' QFISS64=',qfiss_checks

contains

  subroutine OPEN_OUTPUT(name,root)
    character(len=*), intent(in) :: name
    type(c_ptr), intent(out) :: root

    call LCMOP(root,name,0,1,0)
    if (.not. c_associated(root)) error stop 'B2S output creation failed'
  end subroutine OPEN_OUTPUT


  subroutine REQUIRE_NO_STUB_ACCESS(context)
    character(len=*), intent(in) :: context

    if (xdrta2_calls /= 0 .or. core_calls /= 0 .or. event_count /= 0) then
      write(*,'(A)') 'unexpected access context='//trim(context)
      error stop 'B2S unexpected stub access'
    end if
  end subroutine REQUIRE_NO_STUB_ACCESS


  subroutine VERIFY_CAPTURED_QFISS(checks)
    integer, intent(inout) :: checks
    integer :: group, unknown, p
    integer(int64) :: found_bits, expected_bits

    do p=1,B2S_NSNAP
      do group=1,B2S_NGRP
        do unknown=1,B2S_NUNKNO
          found_bits=transfer(captured_qfiss64(unknown,group,p),0_int64)
          expected_bits=transfer(B2S_QFISS_VALUE(p,group,unknown),0_int64)
          if (found_bits /= expected_bits) &
            error stop 'B2S core QFISS capture differs'
          checks=checks+1
        end do
      end do
    end do
  end subroutine VERIFY_CAPTURED_QFISS


  subroutine VERIFY_RETURNED(root,raw_track,raw_system,k_value,rho_value, &
      terminal_count,mirror_count,qfiss_count)
    type(c_ptr), intent(in) :: root, raw_track, raw_system
    real(real64), intent(in) :: k_value, rho_value
    integer, intent(inout) :: terminal_count, mirror_count, qfiss_count
    integer :: p, group, unknown
    integer :: raw_key(B2S_NREG), found_key(B2S_NREG)
    integer(int32) :: found32_bits, expected32_bits
    integer(int64) :: found64_bits, expected64_bits
    real(real32) :: raw_leak(B2S_NGRP), found_leak(B2S_NGRP)
    real(real32) :: vector32(B2S_NUNKNO)
    real(real64) :: vector64(B2S_NUNKNO), found_rho
    type(c_ptr) :: authority, tracks, libraries, systems, fluxes
    type(c_ptr) :: item, embedded, auth_flux, auth_source, auth_qfiss
    type(c_ptr) :: root_flux, root_source, legacy_outer, legacy_inner

    call B2S_REQUIRE_CHARACTER(root,'SIGNATURE',12,'L_ARCHIVE')
    call B2S_REQUIRE_INTEGER(root,'LISTDIM',B2S_NSNAP)
    call REQUIRE_ABSENT(root,'SPOT-ITER-K')
    call REQUIRE_ABSENT(root,'AX-NEXT')
    call REQUIRE_ABSENT(root,'CLOSED')
    authority=LCMGID(root,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'B2S root authority missing'
    call B2S_REQUIRE_CHARACTER(authority,'STATE',12,'RETURNED')
    call B2S_REQUIRE_INTEGER(authority,'NPLANE',B2S_NSNAP)
    call B2S_REQUIRE_INTEGER(authority,'EPOCH',1)
    call REQUIRE_ABSENT(authority,'RHO')

    tracks=LCMGID(root,'TRACK')
    libraries=LCMGID(root,'MICROLIB2')
    systems=LCMGID(root,'SYSTEM')
    fluxes=LCMGID(root,'FLUX')
    if (.not. all([c_associated(tracks),c_associated(libraries), &
        c_associated(systems),c_associated(fluxes)])) &
      error stop 'B2S returned lists missing'
    call LCMGET(raw_track,'KEYFLX',raw_key)
    call LCMGET(raw_system,'SPOT-LEAK1D',raw_leak)

    do p=1,B2S_NSNAP
      item=LCMGIL(tracks,p)
      call B2S_REQUIRE_INTEGER(item,'B2S-PLANE',p)
      call LCMGET(item,'KEYFLX',found_key)
      if (any(found_key /= raw_key)) error stop 'B2S returned TRACK differs'

      item=LCMGIL(libraries,p)
      call B2S_REQUIRE_CHARACTER(item,'SIGNATURE',12,'L_LIBRARY')
      call B2S_REQUIRE_INTEGER(item,'B2S-PLANE',p)
      embedded=LCMGID(item,'MACROLIB')
      if (.not. c_associated(embedded)) &
        error stop 'B2S returned embedded MACROLIB missing'
      call B2S_REQUIRE_CHARACTER(embedded,'SIGNATURE',12,'L_MACROLIB')

      item=LCMGIL(systems,p)
      call B2S_REQUIRE_INTEGER(item,'SPOT-L1-SNAP',p)
      call LCMGET(item,'SPOT-LEAK1D',found_leak)
      if (any(transfer(found_leak,0_int32,B2S_NGRP) /= &
          transfer(raw_leak,0_int32,B2S_NGRP))) &
        error stop 'B2S returned SYSTEM leakage differs'
      authority=LCMGID(item,'SPOT-R64')
      call LCMGET(authority,'RHO',found_rho)
      if (transfer(found_rho,0_int64) /= transfer(rho_value,0_int64)) &
        error stop 'B2S returned SYSTEM RHO differs'

      item=LCMGIL(fluxes,p)
      authority=LCMGID(item,'SPOT-R64')
      call B2S_REQUIRE_CHARACTER(authority,'STATE',12,'SOLVED')
      call B2S_REQUIRE_INTEGER(authority,'EPOCH',1)
      call REQUIRE_ABSENT(authority,'PLANE')
      call LCMGET(authority,'RHO',found_rho)
      if (transfer(found_rho,0_int64) /= transfer(rho_value,0_int64)) &
        error stop 'B2S returned SOLVED RHO differs'
      call B2S_REQUIRE_RECORD(item,'SPOT-FS-EQN',1,1)
      call B2S_REQUIRE_RECORD(item,'SPOT-FS-K',1,2)
      call VERIFY_RETURNED_K(item,k_value)

      auth_flux=LCMGID(authority,'FLUX')
      auth_source=LCMGID(authority,'SOUR')
      auth_qfiss=LCMGID(authority,'QFISS')
      root_flux=LCMGID(item,'FLUX')
      root_source=LCMGID(item,'SOUR')
      legacy_outer=LCMGID(item,'SPOT-QFISS')
      legacy_inner=LCMGIL(legacy_outer,1)
      if (.not. all([c_associated(auth_flux),c_associated(auth_source), &
          c_associated(auth_qfiss),c_associated(root_flux), &
          c_associated(root_source),c_associated(legacy_inner)])) &
        error stop 'B2S returned payload missing'

      do group=1,B2S_NGRP
        call LCMGDL(auth_flux,group,vector64)
        call LCMGDL(root_flux,group,vector32)
        do unknown=1,B2S_NUNKNO
          found64_bits=transfer(vector64(unknown),0_int64)
          expected64_bits=transfer( &
              B2S_TERMINAL_FLUX(p,group,unknown),0_int64)
          if (found64_bits /= expected64_bits) &
            error stop 'B2S returned FLUX64 differs'
          found32_bits=transfer(vector32(unknown),0_int32)
          expected32_bits=transfer(real(B2S_TERMINAL_FLUX( &
              p,group,unknown),real32),0_int32)
          if (found32_bits /= expected32_bits) &
            error stop 'B2S returned FLUX32 mirror differs'
          terminal_count=terminal_count+1
          mirror_count=mirror_count+1
        end do

        call LCMGDL(auth_source,group,vector64)
        call LCMGDL(root_source,group,vector32)
        do unknown=1,B2S_NUNKNO
          found64_bits=transfer(vector64(unknown),0_int64)
          expected64_bits=transfer( &
              B2S_TERMINAL_SOURCE(p,group,unknown),0_int64)
          if (found64_bits /= expected64_bits) &
            error stop 'B2S returned SOUR64 differs'
          found32_bits=transfer(vector32(unknown),0_int32)
          expected32_bits=transfer(real(B2S_TERMINAL_SOURCE( &
              p,group,unknown),real32),0_int32)
          if (found32_bits /= expected32_bits) &
            error stop 'B2S returned SOUR32 mirror differs'
          terminal_count=terminal_count+1
          mirror_count=mirror_count+1
        end do

        call LCMGDL(auth_qfiss,group,vector64)
        call LCMGDL(legacy_inner,group,vector32)
        do unknown=1,B2S_NUNKNO
          found64_bits=transfer(vector64(unknown),0_int64)
          expected64_bits=transfer(B2S_QFISS_VALUE( &
              p,group,unknown),0_int64)
          if (found64_bits /= expected64_bits) &
            error stop 'B2S returned QFISS64 differs'
          found32_bits=transfer(vector32(unknown),0_int32)
          expected32_bits=transfer(real(B2S_QFISS_VALUE( &
              p,group,unknown),real32),0_int32)
          if (found32_bits /= expected32_bits) &
            error stop 'B2S returned QFISS32 mirror differs'
          qfiss_count=qfiss_count+1
        end do
      end do
    end do
  end subroutine VERIFY_RETURNED


  subroutine VERIFY_RETURNED_K(item,k_value)
    type(c_ptr), intent(in) :: item
    real(real64), intent(in) :: k_value
    real(real32) :: found

    call LCMGET(item,'SPOT-FS-K',found)
    if (transfer(found,0_int32) /= transfer(real(k_value,real32),0_int32)) &
      error stop 'B2S returned SPOT-FS-K differs'
  end subroutine VERIFY_RETURNED_K


  subroutine REQUIRE_ABSENT(owner,name)
    type(c_ptr), intent(in) :: owner
    character(len=*), intent(in) :: name

    call B2S_REQUIRE_RECORD(owner,name,0,99)
  end subroutine REQUIRE_ABSENT

end program TEST_B2S_IMMEDIATE_HOST_BRIDGE
