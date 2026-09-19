module SPOR64_RCONTRACT
  ! The sealed route contract: the per-case declaration of the solver
  ! discipline that the lifecycle guards pin bitwise.  The historical
  ! pincell literals (radial 2.5E-7, axial 5E-8, MCCG 1E-5, EXTE 500,
  ! MAXINR 740, ACCE 3 3, OPTION 'B0') were route policy compiled into
  ! the guards; they are policy of ONE case, not invariants of the
  ! method, so they move into a contract object that is generated
  ! upstream from the case declaration and hash-sealed by the lane's
  ! input manifest.  The object under admission never certifies itself:
  ! the guards compare its records bitwise against the contract, and a
  ! mismatch is an ordinary fail-closed refusal.  No comparison is
  ! relaxed; only the source of the expected bits changes.
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, real32
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  use SPOR64_VERIFY, only : CHARACTER_RECORD_MATCHES, RECORD_MATCHES
  implicit none
  private

  character(len=12), parameter, public :: SPOR64_RCONTRACT_SIGNATURE = &
      'L_RCONTRACT'

  type, public :: SPOR64_ROUTE_CONTRACT
    character(len=12) :: case_name = ' '
    integer(int32) :: eps_radial_bits = 0_int32
    integer(int32) :: eps_axial_bits = 0_int32
    integer(int32) :: eps_mccg_bits = 0_int32
    integer :: flu_maxout = 0
    integer :: flu_maxinr = 0
    integer :: flu_acce_free = 0
    integer :: flu_acce_accel = 0
    character(len=4) :: flu_option = ' '
  end type SPOR64_ROUTE_CONTRACT

  public :: SPOR64_RCONTRACT_LOAD

contains

  ! Load and structurally validate one sealed route contract.  Every
  ! record is mandatory; any defect returns loaded=.false. and the
  ! caller refuses admission.  Values are captured as exact bit images.
  subroutine SPOR64_RCONTRACT_LOAD(ipcontract,contract,loaded)
    type(c_ptr), intent(in) :: ipcontract
    type(SPOR64_ROUTE_CONTRACT), intent(out) :: contract
    logical, intent(out) :: loaded

    real(real32) :: eps32(3)
    integer :: acce(2), caps(2)
    character(len=12) :: name12
    character(len=4) :: option4

    loaded = .false.
    if (.not. c_associated(ipcontract)) return
    if (.not. CHARACTER_RECORD_MATCHES(ipcontract,'SIGNATURE',3,12, &
        SPOR64_RCONTRACT_SIGNATURE)) return
    if (.not. RECORD_MATCHES(ipcontract,'CASE-NAME',3,3)) return
    call LCMGTC(ipcontract,'CASE-NAME',12,name12)
    if (len_trim(name12) == 0) return
    if (.not. RECORD_MATCHES(ipcontract,'EPS-TERMINAL',3,2)) return
    call LCMGET(ipcontract,'EPS-TERMINAL',eps32)
    if (.not. all(ieee_is_finite(eps32))) return
    if (any(eps32 <= 0.0_real32)) return
    if (.not. RECORD_MATCHES(ipcontract,'FLU-CAPS',2,1)) return
    call LCMGET(ipcontract,'FLU-CAPS',caps)
    if (caps(1) <= 0 .or. caps(2) <= 0) return
    if (.not. RECORD_MATCHES(ipcontract,'FLU-ACCE',2,1)) return
    call LCMGET(ipcontract,'FLU-ACCE',acce)
    if (acce(1) < 0 .or. acce(2) < 0) return
    if (acce(1)+acce(2) <= 0) return
    if (.not. RECORD_MATCHES(ipcontract,'FLU-OPTION',1,3)) return
    call LCMGTC(ipcontract,'FLU-OPTION',4,option4)
    if (len_trim(option4) == 0) return

    contract%case_name = name12
    contract%eps_radial_bits = transfer(eps32(1),0_int32)
    contract%eps_axial_bits = transfer(eps32(2),0_int32)
    contract%eps_mccg_bits = transfer(eps32(3),0_int32)
    contract%flu_maxout = caps(1)
    contract%flu_maxinr = caps(2)
    contract%flu_acce_free = acce(1)
    contract%flu_acce_accel = acce(2)
    contract%flu_option = option4
    loaded = .true.
  end subroutine SPOR64_RCONTRACT_LOAD

end module SPOR64_RCONTRACT
