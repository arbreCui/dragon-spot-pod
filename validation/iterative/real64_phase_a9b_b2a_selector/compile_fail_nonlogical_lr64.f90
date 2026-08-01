module COMPILE_FAIL_NONLOGICAL_LR64
  use B2A_SELECTOR_ABI, only : FLUGPI_SELECTOR_TAIL
  implicit none

contains

  subroutine FAIL_NONLOGICAL_LR64()
    logical :: limerg
    integer :: lr64
    call FLUGPI_SELECTOR_TAIL(limerg, lr64)
  end subroutine FAIL_NONLOGICAL_LR64

end module COMPILE_FAIL_NONLOGICAL_LR64
