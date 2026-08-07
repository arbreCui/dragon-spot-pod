program TEST_B2T_OWNED_SOURCE_ORCHESTRATION
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_loc, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int64
  use B2T_STUB_PROBES
  use SPOR64_B2T, only : SPOR64_B2T_DISABLED, SPOR64_B2T_FAILED, &
      SPOR64_B2T_RETURNED, SPOR64_B2T_HOST_STEP
  implicit none

  integer :: status, plane
  integer(int64) :: cutoff(B2T_NSNAP)
  integer, parameter :: SUCCESS_EVENTS(5) = &
      [B2T_EVENT_K,B2T_EVENT_N_BASE+1,B2T_EVENT_N_BASE+2, &
       B2T_EVENT_N_BASE+3,B2T_EVENT_S]
  type(c_ptr) :: projected, systems(B2T_NSNAP)
  type(c_ptr) :: duplicate_systems(B2T_NSNAP)
  type(c_ptr) :: null_systems(B2T_NSNAP)
  type(c_ptr) :: replay_asmb, replay_macro(B2T_NSNAP)
  type(c_ptr) :: replay_source(B2T_NSNAP), output
  type(FIL_file), target :: track_file

  null_systems = c_null_ptr
  track_file%unit = 77
  track_file%kdi_file = c_null_ptr

  ! Disabled routing must return before even null caller objects are tested.
  call B2T_RESET_PROBES()
  cutoff = -1_int64
  call SPOR64_B2T_HOST_STEP(c_null_ptr,c_null_ptr,null_systems, &
      c_null_ptr,status,cutoff)
  call REQUIRE_RESULT(status,SPOR64_B2T_DISABLED,cutoff, &
      [0_int64,0_int64,0_int64],'omitted OFF')
  call REQUIRE_NO_SUBCALLS('omitted OFF')

  cutoff = -1_int64
  call SPOR64_B2T_HOST_STEP(c_null_ptr,c_null_ptr,null_systems, &
      c_null_ptr,status,cutoff,.false.)
  call REQUIRE_RESULT(status,SPOR64_B2T_DISABLED,cutoff, &
      [0_int64,0_int64,0_int64],'explicit OFF')
  call REQUIRE_NO_SUBCALLS('explicit OFF')

  call OPEN_ROOT(projected)
  call B2T_PUT_MARKER(projected,500)
  do plane = 1, B2T_NSNAP
    call OPEN_ROOT(systems(plane))
    call B2T_PUT_MARKER(systems(plane),500+plane)
  end do
  call OPEN_ROOT(replay_asmb)
  call B2T_PUT_MARKER(replay_asmb,100)
  do plane = 1, B2T_NSNAP
    call OPEN_ROOT(replay_macro(plane))
    call B2T_PUT_MARKER(replay_macro(plane),100+plane)
    call OPEN_ROOT(replay_source(plane))
    call B2T_PUT_MARKER(replay_source(plane),200+plane)
  end do

  ! Three public preflight failures must stop before B2K and leave every
  ! fresh output empty.  The first case aliases output and PROJECTED; the
  ! second repeats a SYSTEM handle; the third supplies a nonfresh output.
  call B2T_RESET_PROBES()
  cutoff = -1_int64
  call SPOR64_B2T_HOST_STEP(projected,projected,systems, &
      c_loc(track_file),status,cutoff,.true.)
  call REQUIRE_RESULT(status,SPOR64_B2T_FAILED,cutoff, &
      [0_int64,0_int64,0_int64],'output/PROJECTED alias')
  call REQUIRE_NO_SUBCALLS('output/PROJECTED alias')
  call B2T_REQUIRE_MARKER(projected,500,'immutable PROJECTED alias case')

  duplicate_systems = systems
  duplicate_systems(2) = systems(1)
  call OPEN_ROOT(output)
  call B2T_RESET_PROBES()
  cutoff = -1_int64
  call SPOR64_B2T_HOST_STEP(output,projected,duplicate_systems, &
      c_loc(track_file),status,cutoff,.true.)
  call REQUIRE_RESULT(status,SPOR64_B2T_FAILED,cutoff, &
      [0_int64,0_int64,0_int64],'duplicate SYSTEM')
  call REQUIRE_NO_SUBCALLS('duplicate SYSTEM')
  call B2T_REQUIRE_FRESH(output,'duplicate SYSTEM caller output')
  call LCMCL(output,2)

  call OPEN_ROOT(output)
  call B2T_PUT_MARKER(output,777)
  call B2T_RESET_PROBES()
  cutoff = -1_int64
  call SPOR64_B2T_HOST_STEP(output,projected,systems, &
      c_loc(track_file),status,cutoff,.true.)
  call REQUIRE_RESULT(status,SPOR64_B2T_FAILED,cutoff, &
      [0_int64,0_int64,0_int64],'nonfresh output')
  call REQUIRE_NO_SUBCALLS('nonfresh output')
  call B2T_REQUIRE_MARKER(output,777,'nonfresh output preservation')
  call LCMCL(output,2)

  ! A failed B2K is the only event.  None of the private work may escape to
  ! the still-fresh caller output.
  call OPEN_ROOT(output)
  call PREPARE_ACTIVE_CASE(output,B2T_FAIL_K)
  cutoff = -1_int64
  call SPOR64_B2T_HOST_STEP(output,projected,systems, &
      c_loc(track_file),status,cutoff,.true.)
  call REQUIRE_RESULT(status,SPOR64_B2T_FAILED,cutoff, &
      [0_int64,0_int64,0_int64],'B2K failure')
  call REQUIRE_CALLS(1,0,0,'B2K failure')
  call REQUIRE_EVENTS([B2T_EVENT_K],'B2K failure')
  call B2T_REQUIRE_FRESH(output,'B2K failure caller output')
  call LCMCL(output,2)

  ! Plane 2 fails after one committed private pair.  Plane 3 and B2S must
  ! not run, and the caller output remains fresh.
  call OPEN_ROOT(output)
  call PREPARE_ACTIVE_CASE(output,B2T_FAIL_N2)
  cutoff = -1_int64
  call SPOR64_B2T_HOST_STEP(output,projected,systems, &
      c_loc(track_file),status,cutoff,.true.)
  call REQUIRE_RESULT(status,SPOR64_B2T_FAILED,cutoff, &
      [0_int64,0_int64,0_int64],'B2N plane-2 failure')
  call REQUIRE_CALLS(1,2,0,'B2N plane-2 failure')
  call REQUIRE_EVENTS([B2T_EVENT_K,B2T_EVENT_N_BASE+1, &
      B2T_EVENT_N_BASE+2],'B2N plane-2 failure')
  call B2T_REQUIRE_FRESH(output,'B2N plane-2 failure caller output')
  call LCMCL(output,2)

  ! The B2S failure stub validates all seven private handle identities and
  ! the exact TRACK_f handle, but deliberately performs no output write.
  call OPEN_ROOT(output)
  call PREPARE_ACTIVE_CASE(output,B2T_FAIL_S)
  cutoff = -1_int64
  call SPOR64_B2T_HOST_STEP(output,projected,systems, &
      c_loc(track_file),status,cutoff,.true.)
  call REQUIRE_RESULT(status,SPOR64_B2T_FAILED,cutoff, &
      [B2T_FAIL_CUTOFF,0_int64,0_int64],'B2S failure')
  call REQUIRE_CALLS(1,3,1,'B2S failure')
  call REQUIRE_EVENTS(SUCCESS_EVENTS,'B2S failure')
  call REQUIRE_IDENTITY_COUNTS('B2S failure')
  call B2T_REQUIRE_FRESH(output,'B2S failure caller output')
  call LCMCL(output,2)

  ! The accepted route uses the identical private pointers produced during
  ! this call.  The seven content-identical replay objects are not API inputs
  ! and cannot replace any of those private products.
  call OPEN_ROOT(output)
  call PREPARE_ACTIVE_CASE(output,B2T_FAIL_NONE)
  cutoff = -1_int64
  call SPOR64_B2T_HOST_STEP(output,projected,systems, &
      c_loc(track_file),status,cutoff,.true.)
  call REQUIRE_RESULT(status,SPOR64_B2T_RETURNED,cutoff, &
      B2T_SUCCESS_CUTOFF,'successful owned-source route')
  call REQUIRE_CALLS(1,3,1,'successful owned-source route')
  call REQUIRE_EVENTS(SUCCESS_EVENTS,'successful owned-source route')
  call REQUIRE_IDENTITY_COUNTS('successful owned-source route')
  call B2T_REQUIRE_MARKER(output,9001,'successful caller output')
  call LCMCL(output,2)

  call B2T_REQUIRE_MARKER(projected,500,'final PROJECTED immutability')
  do plane = 1, B2T_NSNAP
    call B2T_REQUIRE_MARKER(systems(plane),500+plane, &
        'final SYSTEM immutability')
    call B2T_REQUIRE_MARKER(replay_macro(plane),100+plane, &
        'final MACRO0 replay immutability')
    call B2T_REQUIRE_MARKER(replay_source(plane),200+plane, &
        'final FSOURCE replay immutability')
  end do
  call B2T_REQUIRE_MARKER(replay_asmb,100, &
      'final ASSEMBLED replay immutability')

  do plane = 1, B2T_NSNAP
    call LCMCL(replay_source(plane),2)
    call LCMCL(replay_macro(plane),2)
  end do
  call LCMCL(replay_asmb,2)
  do plane = 1, B2T_NSNAP
    call LCMCL(systems(plane),2)
  end do
  call LCMCL(projected,2)

  write(*,'(A)') 'B2T OWNED-SOURCE ORCHESTRATION PASS'
  write(*,'(A)') 'B2T OFF OMITTED=0-SUBCALLS FALSE=0-SUBCALLS'
  write(*,'(A)') &
      'B2T PREFLIGHT ALIAS=REJECTED DUPLICATE=REJECTED NONFRESH=REJECTED'
  write(*,'(A)') 'B2T B2K-FAIL EVENTS=K OUTPUT=EMPTY'
  write(*,'(A)') 'B2T B2N2-FAIL EVENTS=K,N1,N2 OUTPUT=EMPTY'
  write(*,'(A)') 'B2T B2S-FAIL EVENTS=K,N1,N2,N3,S OUTPUT=EMPTY'
  write(*,'(A)') 'B2T SUCCESS EVENTS=K,N1,N2,N3,S RETURNED=1'
  write(*,'(A)') &
      'B2T PRIVATE-HANDLE-BINDINGS=7 REPLAY-SUBSTITUTIONS=0 TRACK-HANDLE=IDENTICAL'
  write(*,'(A)') &
      'B2T CUTOFF64=4294967301,4294967302,4294967303'
  write(*,'(A)') 'B2T DRAGON=0 ASM=0 FLU=0 TRANSPORT=0'

contains

  subroutine PREPARE_ACTIVE_CASE(ipout,requested_failure)
    type(c_ptr), intent(in) :: ipout
    integer, intent(in) :: requested_failure

    call B2T_RESET_PROBES(requested_failure)
    call B2T_REGISTER_CALL(ipout,projected,systems,c_loc(track_file))
    call B2T_REGISTER_REPLAYS(replay_asmb,replay_macro,replay_source)
  end subroutine PREPARE_ACTIVE_CASE


  subroutine OPEN_ROOT(root)
    type(c_ptr), intent(out) :: root
    integer, save :: counter = 0
    character(len=12) :: name

    counter = counter + 1
    write(name,'("B2TH",I5.5)') counter
    call LCMOP(root,name,0,1,0)
    call B2T_REQUIRE_FRESH(root,'new harness root')
  end subroutine OPEN_ROOT


  subroutine REQUIRE_RESULT(found_status,expected_status,found_cutoff, &
      expected_cutoff,context)
    integer, intent(in) :: found_status, expected_status
    integer(int64), intent(in) :: found_cutoff(B2T_NSNAP)
    integer(int64), intent(in) :: expected_cutoff(B2T_NSNAP)
    character(len=*), intent(in) :: context

    if (found_status /= expected_status .or. &
        any(found_cutoff /= expected_cutoff)) then
      write(*,'(A)') 'B2T result mismatch: '//trim(context)
      error stop 'B2T result mismatch'
    end if
  end subroutine REQUIRE_RESULT


  subroutine REQUIRE_NO_SUBCALLS(context)
    character(len=*), intent(in) :: context

    if (b2k_calls /= 0 .or. b2n_calls /= 0 .or. b2s_calls /= 0 .or. &
        event_count /= 0) then
      write(*,'(A)') 'B2T unexpected subcall: '//trim(context)
      error stop 'B2T unexpected subcall'
    end if
  end subroutine REQUIRE_NO_SUBCALLS


  subroutine REQUIRE_CALLS(expected_k,expected_n,expected_s,context)
    integer, intent(in) :: expected_k, expected_n, expected_s
    character(len=*), intent(in) :: context

    if (b2k_calls /= expected_k .or. b2n_calls /= expected_n .or. &
        b2s_calls /= expected_s) then
      write(*,'(A)') 'B2T subcall inventory mismatch: '//trim(context)
      error stop 'B2T subcall inventory mismatch'
    end if
  end subroutine REQUIRE_CALLS


  subroutine REQUIRE_EVENTS(expected,context)
    integer, intent(in) :: expected(:)
    character(len=*), intent(in) :: context

    if (event_count /= size(expected)) then
      write(*,'(A)') 'B2T event count mismatch: '//trim(context)
      error stop 'B2T event count mismatch'
    end if
    if (any(events(1:event_count) /= expected)) then
      write(*,'(A)') 'B2T event order mismatch: '//trim(context)
      error stop 'B2T event order mismatch'
    end if
  end subroutine REQUIRE_EVENTS


  subroutine REQUIRE_IDENTITY_COUNTS(context)
    character(len=*), intent(in) :: context

    if (private_identity_checks /= 7 .or. replay_identity_checks /= 7 .or. &
        track_identity_checks /= 1) then
      write(*,'(A)') 'B2T private identity mismatch: '//trim(context)
      error stop 'B2T private identity mismatch'
    end if
  end subroutine REQUIRE_IDENTITY_COUNTS

end program TEST_B2T_OWNED_SOURCE_ORCHESTRATION
