subroutine SPOR64T(nentry,hentry,ientry,jentry,kentry)
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int64
  use GANLIB
  use SPOR64_B2T, only : SPOR64_B2T_RETURNED, SPOR64_B2T_HOST_STEP
  implicit none

  integer, intent(in) :: nentry, ientry(nentry), jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)

  integer :: indic, nitma, status
  integer(int64) :: cutoff_by_plane(3)
  real :: flott
  double precision :: dflott
  character(len=4) :: text4
  type(c_ptr) :: systems(3)

  ! SPOR64T is deliberately a thin CLE-2000 adapter.  Selection of the
  ! enclosing SpotStepR64 procedure is the opt-in boundary before ASM.
  if (nentry /= 6) then
    call XABORT('SPOR64T: SIX ENTRIES EXPECTED.')
    return
  end if
  if (hentry(1) /= 'RETURNED' .or. hentry(2) /= 'PROJECTED') then
    call XABORT('SPOR64T: RETURNED/PROJECTED ENTRIES EXPECTED.')
    return
  end if
  if (hentry(3) /= 'SYSTEM1' .or. hentry(4) /= 'SYSTEM2' .or. &
      hentry(5) /= 'SYSTEM3') then
    call XABORT('SPOR64T: SYSTEM1/2/3 INPUTS EXPECTED.')
    return
  end if
  if (hentry(6) /= 'TRACK_f') then
    call XABORT('SPOR64T: TRACK_f INPUT EXPECTED.')
    return
  end if
  if (any(ientry(1:5) /= 1) .or. ientry(6) /= 3) then
    call XABORT('SPOR64T: FIVE LCM ENTRIES AND ONE BINARY FILE EXPECTED.')
    return
  end if
  if (jentry(1) /= 0 .or. any(jentry(2:6) /= 2)) then
    call XABORT('SPOR64T: NEW OUTPUT AND READ-ONLY INPUTS EXPECTED.')
    return
  end if

  ! Consume the exact empty option list before B2T can publish anything.
  call REDGET(indic,nitma,flott,text4,dflott)
  if (indic /= 3 .or. text4 /= ';') then
    call XABORT('SPOR64T: ; CHARACTER EXPECTED.')
    return
  end if

  systems = kentry(3:5)
  call SPOR64_B2T_HOST_STEP(kentry(1),kentry(2),systems,kentry(6), &
      status,cutoff_by_plane,.true.)

  ! B2V_OBSERVER_BEGIN
  ! This unconditional write is the observer's sole semantic difference
  ! from production SPOR64_B2U.  The values remain ordered, unaggregated,
  ! and absent from every physical LCM/XSM object and acceptance branch.
  write(6,'(A,I0,A,I0,A,I0,A,I0)') 'B2V-OBSERVER STATUS=',status, &
      ' CUTOFF-P1=',cutoff_by_plane(1), &
      ' CUTOFF-P2=',cutoff_by_plane(2), &
      ' CUTOFF-P3=',cutoff_by_plane(3)
  ! B2V_OBSERVER_END

  if (status /= SPOR64_B2T_RETURNED) then
    call XABORT('SPOR64T: B2T OWNED HOST STEP FAILED.')
    return
  end if

  ! cutoff_by_plane is an INT64 observability value owned by B2T/B2S.  This
  ! adapter neither aggregates it nor uses it for acceptance or physics.
end subroutine SPOR64T
