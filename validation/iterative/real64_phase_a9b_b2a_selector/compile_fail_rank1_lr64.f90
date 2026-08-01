module COMPILE_FAIL_RANK1_LR64
  use B2A_SELECTOR_ABI, only : FLUDRV_SELECTOR_TAIL
  implicit none

contains

  subroutine FAIL_RANK1_LR64()
    logical :: lr64(1)
    call FLUDRV_SELECTOR_TAIL(lr64)
  end subroutine FAIL_RANK1_LR64

end module COMPILE_FAIL_RANK1_LR64
