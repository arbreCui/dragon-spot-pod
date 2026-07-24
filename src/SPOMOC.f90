module SPOMOC_AUDIT
  use, intrinsic :: iso_c_binding, only: c_ptr, c_null_ptr, c_associated
  use, intrinsic :: iso_fortran_env, only: int32, real32, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use GANLIB
  implicit none
  private

  integer, parameter :: schema_version = 1
  integer, parameter :: required_groups = 370
  integer, parameter :: required_unknowns = 14
  integer, parameter :: required_regions = 8
  integer(int32), parameter :: required_epsilon_bits = &
       int(z'348637BD', int32)

  type(c_ptr), save :: audit_root = c_null_ptr
  type(c_ptr), save :: audit_groups = c_null_ptr
  logical, save :: armed = .false.
  logical, save :: complete = .false.
  logical, save :: path_checked = .false.
  logical, save :: door_seen = .false.
  logical, save :: mccgf_seen = .false.
  logical, save :: tuple_written = .false.
  integer, save :: state_vector(24) = 0
  integer, save :: current_role = 0
  integer, save :: current_iteration = 0

  public :: SPOMOC_ACTIVE
  public :: SPOMOC_BEGIN
  public :: SPOMOC_FLU_PATH
  public :: SPOMOC_FLU_CONTEXT
  public :: SPOMOC_DOOR_BEGIN
  public :: SPOMOC_MCCGF_BEGIN
  public :: SPOMOC_SET_ROLE
  public :: SPOMOC_CAPTURE
  public :: SPOMOC_PUBLISH
  public :: SPOMOC_FINISH

contains

  logical function SPOMOC_ACTIVE()
    SPOMOC_ACTIVE = armed .and. (.not. complete)
  end function SPOMOC_ACTIVE


  subroutine SPOMOC_BEGIN(ipflux, arm, cxdoor, itypec, ngrp, nun, nreg, &
       maxout, maxinr, epsout, epsunk, epsinr, lforw, ileak, lrebal, &
       initfl, ncptl, ncpta)
    type(c_ptr), intent(in) :: ipflux
    integer, intent(in) :: arm, itypec, ngrp, nun, nreg
    integer, intent(in) :: maxout, maxinr, ileak, initfl, ncptl, ncpta
    real(real32), intent(in) :: epsout, epsunk, epsinr
    logical, intent(in) :: lforw, lrebal
    character(len=*), intent(in) :: cxdoor
    integer :: ilong, itype

    if (armed) call fail('nested or repeated BEGIN')
    if (arm == 0) return
    if ((arm < 1) .or. (arm > 2)) call fail('arm must be 1 or 2')
    if (.not. c_associated(ipflux)) call fail('missing L_FLUX owner')
    if (trim(cxdoor) /= 'MCCG') call fail('MCCG door required')
    if (itypec /= 0) call fail('TYPE S required')
    if (ngrp /= required_groups) call fail('370 groups required')
    if (nun /= required_unknowns) call fail('14 unknowns required')
    if (nreg /= required_regions) call fail('8 regions required')
    if (maxout /= 1) call fail('MAXOUT=1 required')
    if (maxinr /= 740) call fail('MAXINR=740 required')
    if (transfer(epsout, 0_int32) /= required_epsilon_bits) &
         call fail('EPSOUT bits differ')
    if (transfer(epsunk, 0_int32) /= required_epsilon_bits) &
         call fail('EPSUNK bits differ')
    if (transfer(epsinr, 0_int32) /= required_epsilon_bits) &
         call fail('EPSINR bits differ')
    if (.not. lforw) call fail('direct solve required')
    if (ileak /= 0) call fail('ILEAK=0 required')
    if (.not. lrebal) call fail('rebalancing must be active')
    if (initfl /= 1) call fail('INIT ON required')
    if ((ncptl /= 1) .or. (ncpta /= 0)) &
         call fail('ACCE 1 0 required')

    call LCMLEN(ipflux, 'SPOT-MOC-AUD', ilong, itype)
    if (ilong /= 0) call fail('audit directory already exists')

    audit_root = LCMDID(ipflux, 'SPOT-MOC-AUD')
    if (.not. c_associated(audit_root)) call fail('cannot create sink')
    armed = .true.
    complete = .false.
    path_checked = .false.
    door_seen = .false.
    mccgf_seen = .false.
    tuple_written = .false.
    audit_groups = c_null_ptr
    current_role = 0
    current_iteration = 0
    state_vector = 0
    state_vector(1) = schema_version
    state_vector(2) = 0
    state_vector(3) = arm
    state_vector(4) = 1
    state_vector(5) = 1
    state_vector(21) = ngrp
    state_vector(22) = nun
    state_vector(23) = nreg
    call put_state()
  end subroutine SPOMOC_BEGIN


  subroutine SPOMOC_FLU_PATH(lscal)
    logical, intent(in) :: lscal

    if (.not. SPOMOC_ACTIVE()) return
    if (path_checked) call fail('FLU path checked twice')
    if (lscal) call fail('direct vector DOORFV path required')
    path_checked = .true.
  end subroutine SPOMOC_FLU_PATH


  subroutine SPOMOC_FLU_CONTEXT(it, jt)
    integer, intent(in) :: it, jt

    if (.not. SPOMOC_ACTIVE()) return
    if (.not. path_checked) call fail('FLU path not checked')
    if (door_seen) call fail('more than one audit DOORFV call')
    if ((it /= 1) .or. (jt /= 1)) call fail('first FLU step required')
    state_vector(6) = it
    state_vector(7) = jt
    call put_state()
  end subroutine SPOMOC_FLU_CONTEXT


  subroutine SPOMOC_DOOR_BEGIN()
    if (.not. SPOMOC_ACTIVE()) return
    if (.not. path_checked) call fail('FLU path not checked')
    if (door_seen) call fail('more than one audit DOORFV call')
    if ((state_vector(6) /= 1) .or. (state_vector(7) /= 1)) &
         call fail('FLU context missing')
    door_seen = .true.
    state_vector(8) = 1
    call put_state()
  end subroutine SPOMOC_DOOR_BEGIN


  subroutine SPOMOC_MCCGF_BEGIN(ngrp, ngeff, ngind, nun, ndim, cyclic, &
       nlong, nreg, nsou, nani, nlin, nfunl, kryl, stis, iaac, iscr, &
       idifc, paca, idir)
    integer, intent(in) :: ngrp, ngeff, ngind(ngeff), nun, ndim
    integer, intent(in) :: nlong, nreg, nsou, nani, nlin, nfunl
    integer, intent(in) :: kryl, stis, iaac, iscr, idifc, paca, idir
    logical, intent(in) :: cyclic
    integer :: i, ilong, itype

    if (.not. SPOMOC_ACTIVE()) return
    if (.not. door_seen) call fail('DOORFV context missing')
    if (mccgf_seen) call fail('more than one audit MCCGF call')
    if (ngrp /= required_groups) call fail('MCCGF group count differs')
    if (ngeff /= required_groups) call fail('all groups must be active')
    if (nun /= required_unknowns) call fail('MCCGF NUN differs')
    if (ndim /= 2) call fail('2D MOC tracking required')
    if (cyclic) call fail('non-cyclic MOC tracking required')
    if (nlong /= required_unknowns) call fail('MCCGF NLONG differs')
    if (nreg /= required_regions) call fail('MCCGF NREG differs')
    if (nsou /= 6) call fail('six surface currents required')
    if (nani /= 1) call fail('NANI=1 required')
    if ((nlin /= 1) .or. (nfunl /= 1)) &
         call fail('NLIN=NFUNL=1 required')
    if (kryl /= 10) call fail('KRYL=10 required')
    if (stis /= 1) call fail('STIS=1 required')
    if (iaac /= 80) call fail('IAAC=80 required')
    if (iscr /= 0) call fail('ISCR=0 required')
    if (idifc /= 0) call fail('IDIFC=0 required')
    if (paca /= 4) call fail('PACA=4 required')
    if (idir /= 0) call fail('IDIR=0 required')
    do i = 1, required_groups
      if (ngind(i) /= i) call fail('NGIND must equal 1..370')
    end do

    call LCMLEN(audit_root, 'NGIND', ilong, itype)
    if (ilong /= 0) call fail('NGIND already exists')
    call LCMLEN(audit_root, 'GROUP', ilong, itype)
    if (ilong /= 0) call fail('GROUP already exists')
    call LCMPUT(audit_root, 'NGIND', required_groups, 1, ngind)
    audit_groups = LCMLID(audit_root, 'GROUP', required_groups)
    if (.not. c_associated(audit_groups)) &
         call fail('cannot create GROUP list')

    mccgf_seen = .true.
    state_vector(9) = 1
    state_vector(13) = kryl
    state_vector(14) = stis
    state_vector(15) = iaac
    state_vector(16) = iscr
    state_vector(17) = idifc
    state_vector(18) = paca
    state_vector(19) = idir
    state_vector(20) = ngeff
    state_vector(21) = ngrp
    state_vector(22) = nun
    state_vector(23) = nreg
    call put_state()
  end subroutine SPOMOC_MCCGF_BEGIN


  subroutine SPOMOC_SET_ROLE(role, iteration)
    integer, intent(in) :: role, iteration

    if (.not. SPOMOC_ACTIVE()) return
    if (.not. mccgf_seen) call fail('MCCGF context missing')
    if ((role < 1) .or. (role > 3)) call fail('invalid MCGFL1 role')
    if (iteration < 1) call fail('invalid MCGMRE iteration')
    current_role = role
    current_iteration = iteration
  end subroutine SPOMOC_SET_ROLE


  subroutine SPOMOC_CAPTURE(ngeff, ngind, nun, qfr, eval, source, raw, &
       nconv)
    integer, intent(in) :: ngeff, ngind(ngeff), nun
    real(real32), intent(in) :: qfr(nun, ngeff), eval(nun, ngeff)
    real(real64), intent(in) :: source(nun, ngeff), raw(nun, ngeff)
    logical, intent(in) :: nconv(ngeff)
    type(c_ptr) :: group_dir
    real(real64) :: qfr64(required_unknowns)
    real(real64) :: eval64(required_unknowns)
    integer :: i, ig, marker(1)

    if (.not. SPOMOC_ACTIVE()) return
    if (.not. mccgf_seen) call fail('MCCGF context missing')
    if (current_role /= 1) return
    if (tuple_written) call fail('primary tuple overwrite attempted')
    if (current_iteration /= 1) call fail('first primary step required')
    if (ngeff /= required_groups) call fail('capture NGEFF differs')
    if (nun /= required_unknowns) call fail('capture NUN differs')
    if (.not. all(nconv)) call fail('all groups must remain active')
    if (.not. c_associated(audit_groups)) call fail('GROUP list missing')

    do i = 1, required_groups
      ig = ngind(i)
      if (ig /= i) call fail('capture NGIND differs')
      if (.not. all(ieee_is_finite(qfr(:, i)))) &
           call fail('nonfinite QFR')
      if (.not. all(ieee_is_finite(eval(:, i)))) &
           call fail('nonfinite EVAL')
      if (.not. all(ieee_is_finite(source(:, i)))) &
           call fail('nonfinite SRC')
      if (.not. all(ieee_is_finite(raw(:, i)))) &
           call fail('nonfinite RAW')
      qfr64 = real(qfr(:, i), real64)
      eval64 = real(eval(:, i), real64)
      group_dir = LCMDIL(audit_groups, i)
      if (.not. c_associated(group_dir)) call fail('group create failed')
      call LCMPUT(group_dir, 'SPOT-M-QFR', required_unknowns, 4, qfr64)
      call LCMPUT(group_dir, 'SPOT-M-EVAL', required_unknowns, 4, eval64)
      call LCMPUT(group_dir, 'SPOT-M-SRC', required_unknowns, 4, &
           source(:, i))
      call LCMPUT(group_dir, 'SPOT-M-RAW', required_unknowns, 4, &
           raw(:, i))
      marker(1) = current_iteration
      call LCMPUT(group_dir, 'SPOT-M-STEP', 1, 1, marker)
      marker(1) = current_role
      call LCMPUT(group_dir, 'SPOT-M-ROLE', 1, 1, marker)
      marker(1) = ig
      call LCMPUT(group_dir, 'SPOT-M-GROUP', 1, 1, marker)
    end do

    tuple_written = .true.
    state_vector(10) = current_iteration
    state_vector(11) = current_role
    state_vector(12) = 1
    state_vector(24) = required_groups
    call put_state()
  end subroutine SPOMOC_CAPTURE


  subroutine SPOMOC_PUBLISH()
    type(c_ptr) :: group_dir
    integer :: i, ilong, itype

    if (.not. SPOMOC_ACTIVE()) return
    if (.not. tuple_written) call fail('primary tuple is incomplete')
    if ((current_role /= 1) .or. (current_iteration /= 1)) &
         call fail('primary publication identity differs')
    if (state_vector(24) /= required_groups) &
         call fail('active group count differs')

    do i = 1, required_groups
      call LCMLEL(audit_groups, i, ilong, itype)
      if ((ilong /= -1) .or. (itype /= 0)) &
           call fail('group item is not a directory')
      group_dir = LCMGIL(audit_groups, i)
      call require_record(group_dir, 'SPOT-M-QFR', required_unknowns, 4)
      call require_record(group_dir, 'SPOT-M-EVAL', required_unknowns, 4)
      call require_record(group_dir, 'SPOT-M-SRC', required_unknowns, 4)
      call require_record(group_dir, 'SPOT-M-RAW', required_unknowns, 4)
      call require_record(group_dir, 'SPOT-M-STEP', 1, 1)
      call require_record(group_dir, 'SPOT-M-ROLE', 1, 1)
      call require_record(group_dir, 'SPOT-M-GROUP', 1, 1)
    end do

    state_vector(2) = 1
    call put_state()
    complete = .true.
  end subroutine SPOMOC_PUBLISH


  subroutine SPOMOC_FINISH()
    if (.not. armed) return
    if (.not. complete) call fail('audit was not published COMPLETE')
    call reset_state()
  end subroutine SPOMOC_FINISH


  subroutine require_record(directory, name, required_length, &
       required_type)
    type(c_ptr), intent(in) :: directory
    character(len=*), intent(in) :: name
    integer, intent(in) :: required_length, required_type
    integer :: ilong, itype

    call LCMLEN(directory, name, ilong, itype)
    if ((ilong /= required_length) .or. (itype /= required_type)) &
         call fail('published tuple census differs')
  end subroutine require_record


  subroutine put_state()
    if (.not. c_associated(audit_root)) call fail('audit sink missing')
    call LCMPUT(audit_root, 'STATE-VECTOR', 24, 1, state_vector)
  end subroutine put_state


  subroutine reset_state()
    audit_root = c_null_ptr
    audit_groups = c_null_ptr
    armed = .false.
    complete = .false.
    path_checked = .false.
    door_seen = .false.
    mccgf_seen = .false.
    tuple_written = .false.
    state_vector = 0
    current_role = 0
    current_iteration = 0
  end subroutine reset_state


  subroutine fail(message)
    character(len=*), intent(in) :: message
    call XABORT('SPOMOC: '//trim(message))
  end subroutine fail

end module SPOMOC_AUDIT
