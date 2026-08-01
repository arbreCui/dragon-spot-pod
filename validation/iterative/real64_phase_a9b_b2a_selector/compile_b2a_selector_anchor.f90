module COMPILE_B2A_SELECTOR_ANCHOR
  use B2A_SELECTOR_ABI, only : FLUGPI_SELECTOR_TAIL, FLUDRV_SELECTOR_TAIL
  implicit none

contains

  subroutine COMPILE_SELECTOR_ANCHOR()
    logical :: limerg, lr64
    call FLUGPI_SELECTOR_TAIL(limerg, lr64)
    call FLUDRV_SELECTOR_TAIL(lr64)
  end subroutine COMPILE_SELECTOR_ANCHOR

end module COMPILE_B2A_SELECTOR_ANCHOR
