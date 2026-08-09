program TEST_SPOR64X_ADAPTER
  use B2X_ADAPTER_PROBES
  use, intrinsic :: iso_c_binding, only : c_loc, c_ptr
  implicit none

  interface
    subroutine SPOR64V(nentry,hentry,ientry,jentry,kentry)
      use, intrinsic :: iso_c_binding, only : c_ptr
      integer, intent(in) :: nentry, ientry(nentry), jentry(nentry)
      character(len=12), intent(in) :: hentry(nentry)
      type(c_ptr), intent(in) :: kentry(nentry)
    end subroutine SPOR64V
    subroutine SPOR64X(nentry,hentry,ientry,jentry,kentry)
      use, intrinsic :: iso_c_binding, only : c_ptr
      integer, intent(in) :: nentry, ientry(nentry), jentry(nentry)
      character(len=12), intent(in) :: hentry(nentry)
      type(c_ptr), intent(in) :: kentry(nentry)
    end subroutine SPOR64X
  end interface

  character(len=12), parameter :: GOOD_HENTRY(4)=[character(len=12) :: &
      'AX_CLOSED','ARCH_CLOSED','AX_NEXT','FEEDBACK']
  integer, parameter :: GOOD_IENTRY(4)=[1,1,1,1]
  integer, parameter :: GOOD_JENTRY(4)=[0,0,2,2]
  integer, target :: backing(4)
  type(c_ptr) :: kentry(4)
  character(len=12) :: hentry(4)
  integer :: ientry(4), jentry(4), index

  do index=1,4
    backing(index)=800+index
    kentry(index)=c_loc(backing(index))
  end do

  call B2X_RESET()
  call SPOR64V(2,GOOD_HENTRY(3:4),GOOD_IENTRY(3:4), &
      GOOD_JENTRY(3:4),kentry(3:4))
  call REQUIRE_ABORT('SPOR64V: ONE ENTRY EXPECTED.',0,0,0,'V NENTRY')

  hentry=GOOD_HENTRY
  hentry(4)='RETURNED'
  call B2X_RESET()
  call SPOR64V(1,hentry(4:4),GOOD_IENTRY(4:4), &
      GOOD_JENTRY(4:4),kentry(4:4))
  call REQUIRE_ABORT('SPOR64V: FEEDBACK INPUT EXPECTED.',0,0,0,'V HENTRY')

  ientry=GOOD_IENTRY
  ientry(4)=2
  call B2X_RESET()
  call SPOR64V(1,GOOD_HENTRY(4:4),ientry(4:4), &
      GOOD_JENTRY(4:4),kentry(4:4))
  call REQUIRE_ABORT('SPOR64V: ONE LCM ENTRY EXPECTED.',0,0,0,'V IENTRY')

  jentry=GOOD_JENTRY
  jentry(4)=1
  call B2X_RESET()
  call SPOR64V(1,GOOD_HENTRY(4:4),GOOD_IENTRY(4:4), &
      jentry(4:4),kentry(4:4))
  call REQUIRE_ABORT('SPOR64V: READ-ONLY INPUT EXPECTED.',0,0,0,'V JENTRY')

  call B2X_RESET(B2X_REDGET_BAD,B2X_B2W_SUCCESS,B2X_ADMIT_SUCCESS)
  call SPOR64V(1,GOOD_HENTRY(4:4),GOOD_IENTRY(4:4), &
      GOOD_JENTRY(4:4),kentry(4:4))
  call REQUIRE_ABORT('SPOR64V: ; CHARACTER EXPECTED.',1,0,0,'V REDGET')

  call B2X_RESET(B2X_REDGET_SEMICOLON,B2X_B2W_SUCCESS, &
      B2X_ADMIT_FAILURE)
  call B2X_REGISTER(kentry)
  call SPOR64V(1,GOOD_HENTRY(4:4),GOOD_IENTRY(4:4), &
      GOOD_JENTRY(4:4),kentry(4:4))
  call REQUIRE_ABORT('SPOR64V: RETURNED ADMISSION FAILED.',1,0,1, &
      'V admission failure')
  if (identity_checks /= 1) error stop 'B2X V failure identity differs'

  call B2X_RESET(B2X_REDGET_SEMICOLON,B2X_B2W_SUCCESS, &
      B2X_ADMIT_SUCCESS)
  call B2X_REGISTER(kentry)
  call SPOR64V(1,GOOD_HENTRY(4:4),GOOD_IENTRY(4:4), &
      GOOD_JENTRY(4:4),kentry(4:4))
  if (xabort_calls /= 0 .or. redget_calls /= 1 .or. admit_calls /= 1 .or. &
      b2w_calls /= 0 .or. identity_checks /= 1) &
    error stop 'B2X V success inventory differs'

  call B2X_RESET()
  call SPOR64X(3,GOOD_HENTRY(1:3),GOOD_IENTRY(1:3), &
      GOOD_JENTRY(1:3),kentry(1:3))
  call REQUIRE_ABORT('SPOR64X: FOUR ENTRIES EXPECTED.',0,0,0,'NENTRY')

  hentry=GOOD_HENTRY
  hentry(2)='AX_CLOSED'
  call B2X_RESET()
  call SPOR64X(4,hentry,GOOD_IENTRY,GOOD_JENTRY,kentry)
  call REQUIRE_ABORT( &
      'SPOR64X: AX_CLOSED/ARCH_CLOSED OUTPUTS EXPECTED.',0,0,0,'outputs')

  hentry=GOOD_HENTRY
  hentry(4)='AX_NEXT'
  call B2X_RESET()
  call SPOR64X(4,hentry,GOOD_IENTRY,GOOD_JENTRY,kentry)
  call REQUIRE_ABORT( &
      'SPOR64X: AX_NEXT/FEEDBACK INPUTS EXPECTED.',0,0,0,'inputs')

  ientry=GOOD_IENTRY
  ientry(3)=2
  call B2X_RESET()
  call SPOR64X(4,GOOD_HENTRY,ientry,GOOD_JENTRY,kentry)
  call REQUIRE_ABORT('SPOR64X: FOUR LCM ENTRIES EXPECTED.',0,0,0,'IENTRY')

  jentry=GOOD_JENTRY
  jentry(2)=1
  call B2X_RESET()
  call SPOR64X(4,GOOD_HENTRY,GOOD_IENTRY,jentry,kentry)
  call REQUIRE_ABORT( &
      'SPOR64X: TWO NEW OUTPUTS AND TWO READ-ONLY INPUTS EXPECTED.', &
      0,0,0,'JENTRY')

  call B2X_RESET(B2X_REDGET_BAD,B2X_B2W_SUCCESS)
  call SPOR64X(4,GOOD_HENTRY,GOOD_IENTRY,GOOD_JENTRY,kentry)
  call REQUIRE_ABORT('SPOR64X: ; CHARACTER EXPECTED.',1,0,0,'REDGET')

  call B2X_RESET(B2X_REDGET_SEMICOLON,B2X_B2W_FAILURE)
  call B2X_REGISTER(kentry)
  call SPOR64X(4,GOOD_HENTRY,GOOD_IENTRY,GOOD_JENTRY,kentry)
  call REQUIRE_ABORT( &
      'SPOR64X: B2W RETURNED-CLOSE ADMISSION FAILED.',1,1,0,'B2W failure')
  if (identity_checks /= 4) error stop 'B2X failure identities differ'

  call B2X_RESET(B2X_REDGET_SEMICOLON,B2X_B2W_SUCCESS)
  call B2X_REGISTER(kentry)
  call SPOR64X(4,GOOD_HENTRY,GOOD_IENTRY,GOOD_JENTRY,kentry)
  if (xabort_calls /= 0 .or. redget_calls /= 1 .or. b2w_calls /= 1 .or. &
      identity_checks /= 4) error stop 'B2X success inventory differs'

  write(*,'(A)') 'B2X SPOR64X ADAPTER CAPTURE PASS'
  write(*,'(A)') 'B2X SPOR64V ADAPTER CAPTURE PASS'
  write(*,'(A)') &
      'B2X ABI-NEGATIVES=NENTRY,HOUTPUT,HINPUT,IENTRY,JENTRY,REDGET,B2W'
  write(*,'(A)') 'B2X SUCCESS B2W-STUB=1 ORDERED-POINTER-IDENTITIES=4'
  write(*,'(A)') 'B2X ADAPTER-CALLS=15 REAL-B2W=0 ASM=0 FLU=0 SPOSTATE=0'

contains

  subroutine REQUIRE_ABORT(expected,expected_redget,expected_b2w, &
      expected_admit,context)
    character(len=*), intent(in) :: expected, context
    integer, intent(in) :: expected_redget, expected_b2w, expected_admit

    if (xabort_calls /= 1 .or. trim(last_abort) /= trim(expected) .or. &
        redget_calls /= expected_redget .or. b2w_calls /= expected_b2w .or. &
        admit_calls /= expected_admit) then
      write(*,'(A)') 'B2X adapter abort mismatch: '//trim(context)
      error stop 'B2X adapter abort mismatch'
    end if
  end subroutine REQUIRE_ABORT

end program TEST_SPOR64X_ADAPTER
