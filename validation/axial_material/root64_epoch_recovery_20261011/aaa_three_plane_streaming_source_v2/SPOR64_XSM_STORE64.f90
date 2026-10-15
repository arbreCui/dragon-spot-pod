module SPOR64_XSM_STORE64
  use GANLIB
  use SPOR64_VERIFY, only: EMPTY_ROOT
  implicit none
  private
  public :: EMPTY_XSM_ROOT
contains
  logical function EMPTY_XSM_ROOT(p)
    type(c_ptr), intent(in) :: p
    character(len=72) :: f
    character(len=12) :: d
    integer :: n
    logical :: empty,memory
    EMPTY_XSM_ROOT=.false.
    if(.not.c_associated(p)) return
    call LCMINF(p,f,d,empty,n,memory)
    if(memory.or.n/=-1.or.trim(d)/='/'.or..not.empty) return
    EMPTY_XSM_ROOT=EMPTY_ROOT(p)
  end function EMPTY_XSM_ROOT
end module SPOR64_XSM_STORE64
