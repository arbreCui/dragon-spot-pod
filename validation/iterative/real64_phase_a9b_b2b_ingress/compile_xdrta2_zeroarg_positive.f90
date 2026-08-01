subroutine COMPILE_XDRTA2_ZEROARG_POSITIVE()
  implicit none
  interface
    subroutine XDRTA2()
    end subroutine XDRTA2
  end interface

  call XDRTA2()
end subroutine COMPILE_XDRTA2_ZEROARG_POSITIVE
