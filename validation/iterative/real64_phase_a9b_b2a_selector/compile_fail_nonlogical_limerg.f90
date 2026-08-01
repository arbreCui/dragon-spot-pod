module COMPILE_FAIL_NONLOGICAL_LIMERG
  use B2A_SELECTOR_ABI, only : FLUGPI_SELECTOR_TAIL
  implicit none

contains

  subroutine FAIL_NONLOGICAL_LIMERG()
    integer :: limerg
    logical :: lr64
    call FLUGPI_SELECTOR_TAIL(limerg, lr64)
  end subroutine FAIL_NONLOGICAL_LIMERG

end module COMPILE_FAIL_NONLOGICAL_LIMERG
