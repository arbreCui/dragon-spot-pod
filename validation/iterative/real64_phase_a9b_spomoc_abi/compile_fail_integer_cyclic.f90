subroutine COMPILE_FAIL_INTEGER_CYCLIC(ngrp, ngeff, ngind, nun, cyclic)
  use SPOMOC_AUDIT, only: SPOMOC_MCCGF_BEGIN
  implicit none
  integer, intent(in) :: ngrp, ngeff, nun, ngind(ngeff), cyclic

  call SPOMOC_MCCGF_BEGIN(ngrp, ngeff, ngind, nun, 2, cyclic, 14, 8, &
      6, 1, 1, 1, 10, 1, 80, 0, 0, 4, 0)
end subroutine COMPILE_FAIL_INTEGER_CYCLIC
