subroutine COMPILE_SPOR64_A9B_PROMOTION_ANCHOR(a8_values64, &
    keyflx_base1, keyflx_trk3, pjjind_trk2, sc32, sigal32, im, cf32, &
    a9_state64, a9_operator32, counter64, cutoff_delta64, ok)
  use, intrinsic :: iso_fortran_env, only : int64, real32, real64
  use SPOR64_A8, only : SPOR64_A8_MUTABLE_PROBE, &
      SPOR64_A8_OPERATOR_PROBE, SPOR64_A8_RANK_PROBE
  use SPOR64_A8_ACA, only : SPOR64_A8_ACA_SHAPE_PROBE
  use SPOR64_A9, only : SPOR64_A9_COUNTER_PROBE, &
      SPOR64_A9_OPERATOR_PROBE, SPOR64_A9_STATE_PROBE
  implicit none

  real(real64), contiguous, intent(inout) :: a8_values64(:,:)
  integer, contiguous, intent(in) :: keyflx_base1(:)
  integer, contiguous, intent(in) :: keyflx_trk3(:,:,:)
  integer, contiguous, intent(in) :: pjjind_trk2(:,:)
  real(real32), intent(in) :: sc32(0:8,1), sigal32(-6:8)
  integer, intent(in) :: im(15)
  real(real32), intent(in) :: cf32(32)
  real(real64), contiguous, intent(in) :: a9_state64(:,:,:)
  real(real32), contiguous, intent(in) :: a9_operator32(:,:)
  integer(int64), intent(in) :: counter64
  integer(int64), intent(out) :: cutoff_delta64
  logical, intent(out) :: ok

  logical :: a8_mutable_ok, a8_operator_ok, a8_rank_ok, aca_ok
  logical :: a9_counter_ok, a9_operator_ok, a9_state_ok

  call SPOR64_A8_MUTABLE_PROBE(a8_values64,a8_mutable_ok)
  call SPOR64_A8_RANK_PROBE(keyflx_base1,keyflx_trk3,pjjind_trk2, &
      a8_rank_ok)
  call SPOR64_A8_OPERATOR_PROBE(sc32,sigal32,a8_operator_ok)
  call SPOR64_A8_ACA_SHAPE_PROBE(14,32,im,cf32,cutoff_delta64,aca_ok)
  call SPOR64_A9_STATE_PROBE(a9_state64,a9_state_ok)
  call SPOR64_A9_OPERATOR_PROBE(a9_operator32,a9_operator_ok)
  call SPOR64_A9_COUNTER_PROBE(counter64,a9_counter_ok)

  ok = a8_mutable_ok .and. a8_rank_ok .and. a8_operator_ok .and. &
      aca_ok .and. a9_state_ok .and. a9_operator_ok .and. a9_counter_ok
end subroutine COMPILE_SPOR64_A9B_PROMOTION_ANCHOR
