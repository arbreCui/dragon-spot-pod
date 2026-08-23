program check_convergence_gate
  ! Independent evaluation of the outer convergence gate.
  !
  ! Every record shape, lineage tie and bit of a map is recomputed by a
  ! checker before it is believed.  The acceptance criterion itself was
  ! the exception: the GATE and CLASSIFICATION lines of a receipt were
  ! typed by hand from the printed defect.  This program removes that
  ! exception.  It reads the four double-precision stopping defects of a
  ! closed axial state, compares the three gated ones against the
  ! threshold pinned below, and emits the receipt lines verbatim.
  !
  ! It also reports the fixed-space out-of-span diagnostic.  That quantity
  ! and the outer stopping defects use different norms, so they are not
  ! divided or ordered here; neither one proves rank adequacy.
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  ! The unchanged outer AND gate.  Pinned here so that relaxing it is a
  ! visible source change rather than a typed assertion.
  real(real64), parameter :: GATE = 5.0e-7_real64
  integer, parameter :: MAX_PATH = 72

  character(len=1024) :: path
  type(c_ptr) :: ax
  integer :: dims(4), ngrp, nsnap, ncoef, ilong, itylcm
  integer :: ig, is, a, b, nmode, ia, ib, ig_worst, is_worst
  integer, allocatable :: rank(:), off(:), goff(:)
  real(real64) :: rrho, rleak, dleak, ra
  real(real64) :: nrm2, rel, rel_max
  real(real64), allocatable :: coeff(:), gram(:), perp(:)
  logical :: have_perp, pass_rho, pass_leak, pass_a

  if (command_argument_count() /= 1) &
    error stop 'usage: check_convergence_gate <closed-axial.xsm>'
  call get_command_argument(1,path)
  if (len_trim(path) == 0 .or. len_trim(path) > MAX_PATH) &
    error stop 'XSM path is empty or exceeds the GANLIB limit'

  call LCMOP(ax,trim(path),2,2,0)

  call require(ax,'SPOT-X-DIMS',4,1)
  call LCMGET(ax,'SPOT-X-DIMS',dims)
  ngrp = dims(2); nsnap = dims(3); ncoef = dims(4)
  if (ngrp <= 0 .or. nsnap <= 0 .or. ncoef <= 0) &
    error stop 'invalid state dimensions'

  call require(ax,'SPOT-X-RRHO',1,4)
  call require(ax,'SPOT-X-RLEAK',1,4)
  call require(ax,'SPOT-X-DLEAK',1,4)
  call require(ax,'SPOT-X-RA',1,4)
  call LCMGET(ax,'SPOT-X-RRHO',rrho)
  call LCMGET(ax,'SPOT-X-RLEAK',rleak)
  call LCMGET(ax,'SPOT-X-DLEAK',dleak)
  call LCMGET(ax,'SPOT-X-RA',ra)
  if (.not.ieee_is_finite(rrho) .or. .not.ieee_is_finite(rleak) .or. &
      .not.ieee_is_finite(dleak) .or. .not.ieee_is_finite(ra)) &
    error stop 'non-finite stopping defect'
  if (rrho < 0.0_real64 .or. rleak < 0.0_real64 .or. &
      dleak < 0.0_real64 .or. ra < 0.0_real64) &
    error stop 'negative stopping defect'

  allocate(rank(ngrp),off(ngrp+1),goff(ngrp+1))
  call require(ax,'SPOT-X-RANK',ngrp,1)
  call require(ax,'SPOT-X-OFF',ngrp+1,1)
  call require(ax,'SPOT-X-GOFF',ngrp+1,1)
  call LCMGET(ax,'SPOT-X-RANK',rank)
  call LCMGET(ax,'SPOT-X-OFF',off)
  call LCMGET(ax,'SPOT-X-GOFF',goff)
  if (off(1) /= 0 .or. goff(1) /= 0) error stop 'invalid offsets'
  if (off(ngrp+1) /= ncoef) error stop 'coordinate extent mismatch'
  do ig = 1, ngrp
    if (rank(ig) < 1 .or. rank(ig) > nsnap) error stop 'invalid rank'
    if (off(ig+1)-off(ig) /= nsnap*rank(ig)) error stop 'invalid stride'
    if (goff(ig+1)-goff(ig) /= rank(ig)*rank(ig)) &
      error stop 'invalid gram stride'
  end do

  allocate(coeff(ncoef),gram(goff(ngrp+1)))
  call require(ax,'SPOT-X-A',ncoef,4)
  call require(ax,'SPOT-X-GRAM',goff(ngrp+1),4)
  call LCMGET(ax,'SPOT-X-A',coeff)
  call LCMGET(ax,'SPOT-X-GRAM',gram)
  if (.not.all(ieee_is_finite(coeff))) error stop 'non-finite coordinates'
  if (.not.all(ieee_is_finite(gram))) error stop 'non-finite gram'

  ! SPOT-X-PERP is the volume-weighted RMS of the part of the radial flux
  ! the basis cannot represent, in the same norm the gram defines, so the
  ! resulting ratio is a relative representation diagnostic in that norm.
  call LCMLEN(ax,'SPOT-X-PERP',ilong,itylcm)
  have_perp = (ilong == ngrp*nsnap .and. itylcm == 4)
  if (ilong /= 0 .and. .not.have_perp) error stop 'invalid SPOT-X-PERP'
  rel_max = 0.0_real64; ig_worst = 0; is_worst = 0
  if (have_perp) then
    allocate(perp(ngrp*nsnap))
    call LCMGET(ax,'SPOT-X-PERP',perp)
    if (.not.all(ieee_is_finite(perp))) error stop 'non-finite SPOT-X-PERP'
    if (any(perp < 0.0_real64)) error stop 'negative SPOT-X-PERP'
    do ig = 1, ngrp
      nmode = rank(ig)
      do is = 1, nsnap
        nrm2 = 0.0_real64
        do a = 1, nmode
          ia = off(ig)+(is-1)*nmode+a
          do b = 1, nmode
            ib = off(ig)+(is-1)*nmode+b
            nrm2 = nrm2 + coeff(ia)*gram(goff(ig)+(b-1)*nmode+a)*coeff(ib)
          end do
        end do
        if (nrm2 <= 0.0_real64) error stop 'non-positive modal norm'
        rel = perp((ig-1)*nsnap+is)/sqrt(nrm2)
        if (rel > rel_max) then
          rel_max = rel; ig_worst = ig; is_worst = is
        end if
      end do
    end do
  end if
  call LCMCL(ax,1)

  pass_rho  = rrho  <= GATE
  pass_leak = rleak <= GATE
  pass_a    = ra    <= GATE
  write(*,'(A,ES24.16)') 'SPOT-GATE THRESHOLD      ', GATE
  write(*,'(A,ES24.16,1X,A)') 'SPOT-GATE RRHO           ', rrho, verdict(pass_rho)
  write(*,'(A,ES24.16,1X,A)') 'SPOT-GATE RLEAK          ', rleak, verdict(pass_leak)
  write(*,'(A,ES24.16,1X,A)') 'SPOT-GATE RA             ', ra, verdict(pass_a)
  write(*,'(A,ES24.16,1X,A)') 'SPOT-GATE DLEAK          ', dleak, 'NOT-GATED'
  if (have_perp) then
    write(*,'(A,ES24.16,A,I0,A,I0)') 'SPOT-GATE REPRESENTATION ', &
      rel_max, ' max relative out-of-span at group ', ig_worst, &
      ' plane ', is_worst
    write(*,'(A)') 'SPOT-GATE REPRESENTATION DIAGNOSTIC-NOT-GATED; '// &
      'NOT COMPARABLE TO OUTER DEFECTS WITHOUT A COMMON NORM'
  else
    write(*,'(A)') 'SPOT-GATE REPRESENTATION UNAVAILABLE (no SPOT-X-PERP)'
  end if
  if (pass_rho .and. pass_leak .and. pass_a) then
    write(*,'(A)') 'GATE=(Rrho,RL,Ra) ALL <= 5.0e-7 : PASS'
    write(*,'(A)') 'CLASSIFICATION=VALID_MET'
  else
    write(*,'(A)') 'GATE=(Rrho,RL,Ra) ALL <= 5.0e-7 : NOT MET'
    write(*,'(A)') 'CLASSIFICATION=VALID_NOT_MET'
  end if
  write(*,'(A)') 'SPOT-GATE COMPLETE'

contains

  function verdict(ok) result(text)
    logical, intent(in) :: ok
    character(len=8) :: text
    if (ok) then
      text = 'PASS'
    else
      text = 'NOT MET'
    end if
  end function verdict

  subroutine require(ip,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: ip
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: found_length, found_type
    call LCMLEN(ip,name,found_length,found_type)
    if (found_length /= expected_length .or. found_type /= expected_type) then
      write(*,'(A,A,2(1X,I0),A,2(1X,I0))') 'SPOT-GATE MALFORMED RECORD ', &
        name, found_length, found_type, ' expected', expected_length, &
        expected_type
      error stop 'missing or malformed record'
    end if
  end subroutine require

end program check_convergence_gate
