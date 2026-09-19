subroutine SPOR64V(nentry,hentry,ientry,jentry,kentry)
  ! Read-only admission of a returned object immediately
  ! before ASM.
  use, intrinsic :: iso_c_binding, only : c_ptr
  use GANLIB
  use SPOR64_B2W, only : SPOR64_B2W_RETURNED_ADMITTED, &
      SPOR64_B2W_ADMIT_RETURNED
  implicit none

  integer, intent(in) :: nentry, ientry(nentry), jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)

  integer :: indic, nitma, status
  real :: flott
  double precision :: dflott
  character(len=4) :: text4

  ! Read-only returned-object admission immediately before ASM.  This binds
  ! the child leakage actually consumed by ASM to the same-index SYSTEM L0.
  ! The sealed route contract is a mandatory second read-only operand.
  if (nentry /= 2) then
    call XABORT('SPOR64V: TWO ENTRIES EXPECTED.')
    return
  end if
  if (hentry(1) /= 'FEEDBACK') then
    call XABORT('SPOR64V: FEEDBACK INPUT EXPECTED.')
    return
  end if
  if (hentry(2) /= 'RCONTRACT') then
    call XABORT('SPOR64V: RCONTRACT INPUT EXPECTED.')
    return
  end if
  if (any(ientry /= 1)) then
    call XABORT('SPOR64V: TWO LCM ENTRIES EXPECTED.')
    return
  end if
  if (any(jentry /= 2)) then
    call XABORT('SPOR64V: READ-ONLY INPUTS EXPECTED.')
    return
  end if

  call REDGET(indic,nitma,flott,text4,dflott)
  if (indic /= 3 .or. text4 /= ';') then
    call XABORT('SPOR64V: ; CHARACTER EXPECTED.')
    return
  end if

  call SPOR64_B2W_ADMIT_RETURNED(kentry(1),kentry(2),status)
  if (status /= SPOR64_B2W_RETURNED_ADMITTED) then
    call XABORT('SPOR64V: RETURNED ADMISSION FAILED.')
    return
  end if
end subroutine SPOR64V


subroutine SPOR64X(nentry,hentry,ientry,jentry,kentry)
  use, intrinsic :: iso_c_binding, only : c_ptr
  use GANLIB
  use SPOR64_B2W, only : SPOR64_B2W_CLOSED, SPOR64_B2W_CLOSE
  implicit none

  integer, intent(in) :: nentry, ientry(nentry), jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)

  integer :: indic, nitma, status
  real :: flott
  double precision :: dflott
  character(len=4) :: text4

  ! SPOR64X is the thin terminal adapter of the deployment-default-off
  ! SpotCloseR64 procedure.  The procedure owns AX_NEXT and FEEDBACK from
  ! their creation through this call; the public B2W gate remains responsible
  ! for exact content admission and the final CLOSED/e commit.
  if (nentry /= 5) then
    call XABORT('SPOR64X: FIVE ENTRIES EXPECTED.')
    return
  end if
  if (hentry(1) /= 'AX_CLOSED' .or. hentry(2) /= 'ARCH_CLOSED') then
    call XABORT('SPOR64X: AX_CLOSED/ARCH_CLOSED OUTPUTS EXPECTED.')
    return
  end if
  if (hentry(3) /= 'AX_NEXT' .or. hentry(4) /= 'FEEDBACK') then
    call XABORT('SPOR64X: AX_NEXT/FEEDBACK INPUTS EXPECTED.')
    return
  end if
  if (hentry(5) /= 'RCONTRACT') then
    call XABORT('SPOR64X: RCONTRACT INPUT EXPECTED.')
    return
  end if
  if (any(ientry /= 1)) then
    call XABORT('SPOR64X: FIVE LCM ENTRIES EXPECTED.')
    return
  end if
  if (any(jentry(1:2) /= 0) .or. any(jentry(3:5) /= 2)) then
    call XABORT('SPOR64X: TWO NEW OUTPUTS AND THREE READ-ONLY INPUTS '// &
      'EXPECTED.')
    return
  end if

  ! Consume the exact empty option list before B2W can publish anything.
  call REDGET(indic,nitma,flott,text4,dflott)
  if (indic /= 3 .or. text4 /= ';') then
    call XABORT('SPOR64X: ; CHARACTER EXPECTED.')
    return
  end if

  call SPOR64_B2W_CLOSE(kentry(1),kentry(2),kentry(3),kentry(4), &
    kentry(5),status)
  if (status /= SPOR64_B2W_CLOSED) then
    call XABORT('SPOR64X: B2W RETURNED-CLOSE ADMISSION FAILED.')
    return
  end if
end subroutine SPOR64X
