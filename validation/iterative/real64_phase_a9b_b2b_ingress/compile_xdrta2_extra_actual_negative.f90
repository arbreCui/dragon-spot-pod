subroutine COMPILE_XDRTA2_EXTRA_ACTUAL_NEGATIVE()
  implicit none
  interface
    subroutine XDRTA2()
    end subroutine XDRTA2
  end interface

  call XDRTA2(1)
end subroutine COMPILE_XDRTA2_EXTRA_ACTUAL_NEGATIVE
