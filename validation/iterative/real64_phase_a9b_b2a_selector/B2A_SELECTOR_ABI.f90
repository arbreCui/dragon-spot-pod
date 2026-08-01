module B2A_SELECTOR_ABI
  implicit none
  private
  public :: FLUGPI_SELECTOR_TAIL, FLUDRV_SELECTOR_TAIL

contains

  subroutine FLUGPI_SELECTOR_TAIL(limerg, lr64)
    logical, intent(out) :: limerg, lr64
    limerg = .false.
    lr64 = .false.
  end subroutine FLUGPI_SELECTOR_TAIL

  subroutine FLUDRV_SELECTOR_TAIL(lr64)
    logical, intent(in) :: lr64
    if (lr64) return
  end subroutine FLUDRV_SELECTOR_TAIL

end module B2A_SELECTOR_ABI
