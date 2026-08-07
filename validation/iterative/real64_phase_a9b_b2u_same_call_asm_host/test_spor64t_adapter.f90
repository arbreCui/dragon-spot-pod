program TEST_SPOR64T_ADAPTER
  use B2U_ADAPTER_PROBES
  use, intrinsic :: iso_c_binding, only : c_loc, c_ptr
  implicit none

  interface
    subroutine SPOR64T(nentry,hentry,ientry,jentry,kentry)
      use, intrinsic :: iso_c_binding, only : c_ptr
      integer, intent(in) :: nentry, ientry(nentry), jentry(nentry)
      character(len=12), intent(in) :: hentry(nentry)
      type(c_ptr), intent(in) :: kentry(nentry)
    end subroutine SPOR64T
  end interface

  character(len=12), parameter :: GOOD_HENTRY(6) = &
      [character(len=12) :: 'RETURNED','PROJECTED','SYSTEM1','SYSTEM2', &
       'SYSTEM3','TRACK_f']
  integer, parameter :: GOOD_IENTRY(6) = [1,1,1,1,1,3]
  integer, parameter :: GOOD_JENTRY(6) = [0,2,2,2,2,2]
  integer, target :: media(6)
  type(c_ptr) :: kentry(6), systems(3)
  character(len=12) :: hentry(6)
  integer :: ientry(6), jentry(6), index

  do index = 1, 6
    media(index) = 100+index
    kentry(index) = c_loc(media(index))
  end do
  systems = kentry(3:5)

  call B2U_RESET()
  call SPOR64T(5,GOOD_HENTRY(1:5),GOOD_IENTRY(1:5), &
      GOOD_JENTRY(1:5),kentry(1:5))
  call REQUIRE_ABORT('SPOR64T: SIX ENTRIES EXPECTED.',0,0,'NENTRY')

  hentry = GOOD_HENTRY
  hentry(4) = 'SYSTEM1'
  call B2U_RESET()
  call SPOR64T(6,hentry,GOOD_IENTRY,GOOD_JENTRY,kentry)
  call REQUIRE_ABORT('SPOR64T: SYSTEM1/2/3 INPUTS EXPECTED.',0,0, &
      'HENTRY')

  ientry = GOOD_IENTRY
  ientry(6) = 1
  call B2U_RESET()
  call SPOR64T(6,GOOD_HENTRY,ientry,GOOD_JENTRY,kentry)
  call REQUIRE_ABORT( &
      'SPOR64T: FIVE LCM ENTRIES AND ONE BINARY FILE EXPECTED.',0,0, &
      'IENTRY')

  jentry = GOOD_JENTRY
  jentry(3) = 1
  call B2U_RESET()
  call SPOR64T(6,GOOD_HENTRY,GOOD_IENTRY,jentry,kentry)
  call REQUIRE_ABORT( &
      'SPOR64T: NEW OUTPUT AND READ-ONLY INPUTS EXPECTED.',0,0,'JENTRY')

  call B2U_RESET(B2U_REDGET_BAD,B2U_B2T_SUCCESS)
  call SPOR64T(6,GOOD_HENTRY,GOOD_IENTRY,GOOD_JENTRY,kentry)
  call REQUIRE_ABORT('SPOR64T: ; CHARACTER EXPECTED.',1,0,'REDGET')

  call B2U_RESET(B2U_REDGET_SEMICOLON,B2U_B2T_FAILURE)
  call B2U_REGISTER_MEDIA(kentry(1),kentry(2),systems,kentry(6))
  call SPOR64T(6,GOOD_HENTRY,GOOD_IENTRY,GOOD_JENTRY,kentry)
  call REQUIRE_ABORT('SPOR64T: B2T OWNED HOST STEP FAILED.',1,1, &
      'B2T failure')
  call REQUIRE_IDENTITIES('B2T failure')

  call B2U_RESET(B2U_REDGET_SEMICOLON,B2U_B2T_SUCCESS)
  call B2U_REGISTER_MEDIA(kentry(1),kentry(2),systems,kentry(6))
  call SPOR64T(6,GOOD_HENTRY,GOOD_IENTRY,GOOD_JENTRY,kentry)
  if (xabort_calls /= 0 .or. redget_calls /= 1 .or. b2t_calls /= 1) &
    error stop 'B2U adapter success inventory differs'
  call REQUIRE_IDENTITIES('B2T success')

  write(*,'(A)') 'B2U SPOR64T ADAPTER STUB PASS'
  write(*,'(A)') &
      'B2U NEGATIVES=NENTRY,HENTRY,IENTRY,JENTRY,REDGET,B2T-FAIL'
  write(*,'(A)') &
      'B2U SUCCESS B2T-STUB=1 SYSTEM-BINDINGS=3 TRACK-HANDLE=CURRENT-CALL'
  write(*,'(A)') 'B2U CUTOFF=INT64-PER-PLANE-DIAGNOSTIC-ONLY'
  write(*,'(A)') &
      'B2U REAL-ASM=0 REAL-B2T=0 FLU=0 TRANSPORT=0 PICARD=0'

contains

  subroutine REQUIRE_ABORT(expected,expected_redget,expected_b2t,context)
    character(len=*), intent(in) :: expected, context
    integer, intent(in) :: expected_redget, expected_b2t

    if (xabort_calls /= 1 .or. trim(last_abort) /= trim(expected) .or. &
        redget_calls /= expected_redget .or. b2t_calls /= expected_b2t) then
      write(*,'(A)') 'B2U adapter abort mismatch: '//trim(context)
      error stop 'B2U adapter abort mismatch'
    end if
  end subroutine REQUIRE_ABORT


  subroutine REQUIRE_IDENTITIES(context)
    character(len=*), intent(in) :: context

    if (system_identity_checks /= 3 .or. track_identity_checks /= 1) then
      write(*,'(A)') 'B2U adapter identity-count mismatch: '//trim(context)
      error stop 'B2U adapter identity-count mismatch'
    end if
  end subroutine REQUIRE_IDENTITIES

end program TEST_SPOR64T_ADAPTER
