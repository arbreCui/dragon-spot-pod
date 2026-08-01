subroutine COMPILE_FAIL_FLAT_KEYFLX(keyflx_base1,keyflx_flat1, &
    pjjind_trk2,ok)
  use SPOR64_A8, only : SPOR64_A8_RANK_PROBE
  implicit none

  integer, intent(in) :: keyflx_base1(8), keyflx_flat1(8)
  integer, intent(in) :: pjjind_trk2(1,2)
  logical, intent(out) :: ok

  call SPOR64_A8_RANK_PROBE(keyflx_base1,keyflx_flat1,pjjind_trk2,ok)
end subroutine COMPILE_FAIL_FLAT_KEYFLX
