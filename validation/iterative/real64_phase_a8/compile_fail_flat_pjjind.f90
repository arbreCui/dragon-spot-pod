subroutine COMPILE_FAIL_FLAT_PJJIND(keyflx_base1, keyflx_trk3, &
    pjjind_flat1, ok)
  use SPOR64_A8, only : SPOR64_A8_RANK_PROBE
  implicit none
  integer, intent(in) :: keyflx_base1(8)
  integer, intent(in) :: keyflx_trk3(8,1,1)
  integer, intent(in) :: pjjind_flat1(2)
  logical, intent(out) :: ok

  call SPOR64_A8_RANK_PROBE(keyflx_base1, keyflx_trk3, pjjind_flat1, ok)
end subroutine COMPILE_FAIL_FLAT_PJJIND
