subroutine COMPILE_FAIL_KEYFLX_RANK(keyflx_base2, keyflx_trk3, &
    pjjind_trk2, ok)
  use SPOR64_A8, only : SPOR64_A8_RANK_PROBE
  implicit none
  integer, intent(in) :: keyflx_base2(8,1)
  integer, intent(in) :: keyflx_trk3(8,1,1)
  integer, intent(in) :: pjjind_trk2(1,2)
  logical, intent(out) :: ok

  call SPOR64_A8_RANK_PROBE(keyflx_base2, keyflx_trk3, pjjind_trk2, ok)
end subroutine COMPILE_FAIL_KEYFLX_RANK
