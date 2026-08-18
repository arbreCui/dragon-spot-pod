program check_rank2_modal_aa1_candidate
  ! Independent, read-only Ganlib audit of one materialized rank-2
  ! modal-projected Anderson proposal.  This program performs no
  ! assembly, transport solve, map evaluation, or convergence decision.
  !
  !   check_rank2_modal_aa1_candidate x0 x1 x2 x2_snap basis \
  !     proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --next x1 x2 y z z_snap basis \
  !     proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --next-x4 x3 x4 qy z z_snap basis \
  !     proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --next-x4z qy z qt u u_snap basis \
  !     proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --next-zu qt u qs v v_snap basis \
  !     proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --next-x4aa2-screened q v w x \
  !     x_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --next-aa1aa2-screened q1 g q2 h \
  !     h_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --next-aa1aa2-ij-screened q3 i q4 j \
  !     j_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --next-aa2aa1-jk-screened q4 j q5 k \
  !     k_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --next-zpcd-screened z zp c d \
  !     d_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --next-aa1aa1-screened q6 m q7 n \
  !     n_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --u y z w v v_snap basis \
  !     proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --post-aa1 x2 x3 aa1 aa1p \
  !     aa1p_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --rolling-aa1 aa1 aa1p xnext \
  !     xnextp xnextp_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --rolling-aa1-next xnext xnextp \
  !     xroll xrollp xrollp_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --rolling-aa2 x0 x0p x1 x1p \
  !     x2 x2p x2p_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --rolling-aa2-next x0 x0p x1 x1p \
  !     x2 x2p x2p_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --consecutive x1_pub x2 x3 \
  !     x3_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --consecutive-returned x2 x3 x4 \
  !     x4_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --consecutive-returned-screened \
  !     z r s s_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --consecutive-ptu-screened \
  !     p t u u_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --consecutive-current qs v w \
  !     w_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate \
  !     --consecutive-current-aa2-picard q p z z_snap basis \
  !     proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate \
  !     --consecutive-qvwx-zplus-screened y z zp zp_snap basis \
  !     proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate \
  !     --consecutive-q5kl-screened q5 k l l_snap basis \
  !     proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --current-qpzst-aa2 q p p z s t \
  !     t_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --current-stuvvw-aa2 s t u v v w \
  !     w_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --current-uvvwxy-aa2 u v v w x y \
  !     y_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --current-ptuqv-aa2 p t t u q v \
  !     v_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --current-cefg-aa2 c e e f q g \
  !     g_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --current-ghi-aa2 q1 g q2 h q3 i \
  !     i_snap basis proposal_ax proposal_snap
  !   check_rank2_modal_aa1_candidate --current-klmn-aa2 k l q6 m q7 n \
  !     n_snap basis proposal_ax proposal_snap
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  implicit none

  integer, parameter :: nstate=40
  integer, parameter :: ngrp_expected=370
  integer, parameter :: nsnap_expected=3
  integer, parameter :: nreg_expected=8
  integer, parameter :: rank_expected=2
  integer, parameter :: positive_count_expected= &
    ngrp_expected*nsnap_expected*nreg_expected
  integer, parameter :: max_xsm_path=72

  type :: canonical_state
    character(len=12) :: signature=''
    character(len=12) :: norm_id=''
    character(len=12) :: basis_type=''
    integer :: state(nstate)=0
    integer :: dims(4)=0
    integer :: fixb=-1
    integer, allocatable :: rank(:)
    integer, allocatable :: offset(:)
    integer, allocatable :: gram_offset(:)
    integer, allocatable :: basis_offset(:)
    real(real32), allocatable :: basis(:)
    real(real64), allocatable :: coordinates(:)
    real(real64), allocatable :: leakage(:)
    real(real64), allocatable :: height(:)
    real(real64), allocatable :: gram(:)
    real(real32) :: keff=0.0_real32
    real(real64) :: rho=0.0_real64
    real(real64) :: norm=0.0_real64
    real(real64) :: gram_error=0.0_real64
  end type canonical_state

  character(len=1024) :: path(10)
  character(len=1024) :: mode_argument
  type(canonical_state) :: x0,x1,x2,proposal
  real(real64), allocatable :: expected_a(:),expected_l(:)
  real(real32), allocatable :: expected_l32(:)
  real(real64) :: update0_sq,update1_sq,update_dot,denominator
  real(real64) :: beta,previous_weight,rho_affine,rho_published
  real(real64) :: modal_affine_sq,modal_affine_norm,modal_current_norm
  real(real64) :: publication_delta
  real(real64) :: leakage_sq(2),leakage_dot,leakage_affine_sq
  real(real64) :: leakage_affine_norm,leakage_current_norm
  real(real64) :: leakage_affine_d,leakage_current_d
  real(real64) :: leakage_delta01,leakage_delta12
  real(real32) :: keff_published,min_published_flux
  integer :: argument_count,i,g,s,il,min_group,min_snapshot,min_region
  logical :: next_mode,u_mode,post_aa1_mode,rolling_mode
  logical :: rolling_next_mode,x4_history_mode,rolling_aa2_next_mode
  logical :: current_aa2_mode
  logical :: current_qpzst_aa2_mode
  logical :: current_stuvvw_aa2_mode
  logical :: current_uvvwxy_aa2_mode
  logical :: current_ptuqv_aa2_mode
  logical :: current_cefg_aa2_mode
  logical :: x4z_history_mode,zu_history_mode
  logical :: x4aa2_screened_mode
  logical :: consecutive_mode
  logical :: consecutive_returned_mode
  logical :: consecutive_current_mode
  logical :: consecutive_current_aa2_picard_mode
  logical :: consecutive_qvwx_zplus_screened_mode
  logical :: consecutive_q5kl_screened_mode
  logical :: consecutive_returned_screened_mode
  logical :: consecutive_ptu_screened_mode
  character(len=24) :: report_prefix
  character(len=12) :: proposal_carrier
  character(len=2) :: previous_output,latest_output

  argument_count=command_argument_count()
  next_mode=.false.
  u_mode=.false.
  post_aa1_mode=.false.
  rolling_mode=.false.
  rolling_next_mode=.false.
  x4_history_mode=.false.
  x4z_history_mode=.false.
  zu_history_mode=.false.
  x4aa2_screened_mode=.false.
  rolling_aa2_next_mode=.false.
  current_aa2_mode=.false.
  current_qpzst_aa2_mode=.false.
  current_stuvvw_aa2_mode=.false.
  current_uvvwxy_aa2_mode=.false.
  current_ptuqv_aa2_mode=.false.
  current_cefg_aa2_mode=.false.
  consecutive_mode=.false.
  consecutive_returned_mode=.false.
  consecutive_current_mode=.false.
  consecutive_current_aa2_picard_mode=.false.
  consecutive_qvwx_zplus_screened_mode=.false.
  consecutive_q5kl_screened_mode=.false.
  consecutive_returned_screened_mode=.false.
  consecutive_ptu_screened_mode=.false.
  if (argument_count == 11) then
    call get_command_argument(1,mode_argument)
    if (trim(mode_argument) == '--rolling-aa2-next') then
      rolling_aa2_next_mode=.true.
    else if (trim(mode_argument) == '--current-aa2') then
      current_aa2_mode=.true.
    else if (trim(mode_argument) == '--current-qpzst-aa2') then
      current_qpzst_aa2_mode=.true.
    else if (trim(mode_argument) == '--current-stuvvw-aa2') then
      current_stuvvw_aa2_mode=.true.
    else if (trim(mode_argument) == '--current-uvvwxy-aa2') then
      current_uvvwxy_aa2_mode=.true.
    else if (trim(mode_argument) == '--current-ptuqv-aa2') then
      current_ptuqv_aa2_mode=.true.
    else if (trim(mode_argument) == '--current-cefg-aa2') then
      current_cefg_aa2_mode=.true.
    else if (trim(mode_argument) == '--current-ghi-aa2') then
      current_cefg_aa2_mode=.true.
    else if (trim(mode_argument) == '--current-klmn-aa2') then
      current_cefg_aa2_mode=.true.
    else if (trim(mode_argument) /= '--rolling-aa2') then
      call fail('ELEVEN ARGUMENTS REQUIRE AN AA2 MODE.')
    endif
    do i=1,10
      call get_command_argument(i+1,path(i))
      if (len_trim(path(i)) == 0) call fail('EMPTY AA2 XSM PATH ARGUMENT.')
      if (len_trim(path(i)) > max_xsm_path) &
        call fail('AA2 XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
    enddo
    call check_rolling_aa2_candidate(trim(path(1)),trim(path(2)), &
      trim(path(3)),trim(path(4)),trim(path(5)),trim(path(6)), &
      trim(path(7)),trim(path(8)),trim(path(9)),trim(path(10)), &
      rolling_aa2_next_mode,current_aa2_mode,current_qpzst_aa2_mode, &
      current_stuvvw_aa2_mode,current_uvvwxy_aa2_mode, &
      current_ptuqv_aa2_mode,current_cefg_aa2_mode)
    stop
  else if (argument_count == 9) then
    call get_command_argument(1,mode_argument)
    if (trim(mode_argument) == '--u') then
      u_mode=.true.
    else if (trim(mode_argument) == '--next-x4') then
      x4_history_mode=.true.
    else if (trim(mode_argument) == '--next-x4z') then
      x4z_history_mode=.true.
    else if (trim(mode_argument) == '--next-zu') then
      zu_history_mode=.true.
    else if (trim(mode_argument) == '--next-x4aa2-screened') then
      x4aa2_screened_mode=.true.
    else if (trim(mode_argument) == '--next-aa1aa2-screened') then
      x4aa2_screened_mode=.true.
    else if (trim(mode_argument) == '--next-aa1aa2-ij-screened') then
      x4aa2_screened_mode=.true.
    else if (trim(mode_argument) == '--next-aa2aa1-jk-screened') then
      x4aa2_screened_mode=.true.
    else if (trim(mode_argument) == '--next-zpcd-screened') then
      x4aa2_screened_mode=.true.
    else if (trim(mode_argument) == '--next-aa1aa1-screened') then
      x4aa2_screened_mode=.true.
    else if (trim(mode_argument) == '--post-aa1') then
      post_aa1_mode=.true.
    else if (trim(mode_argument) == '--rolling-aa1') then
      rolling_mode=.true.
    else if (trim(mode_argument) == '--rolling-aa1-next') then
      rolling_next_mode=.true.
    else if (trim(mode_argument) /= '--next') then
      call fail('NINE ARGUMENTS REQUIRE --NEXT, --NEXT-X4, --NEXT-X4Z, '// &
        '--NEXT-ZU, --NEXT-X4AA2-SCREENED, --NEXT-AA1AA2-SCREENED, '// &
        '--NEXT-AA1AA2-IJ-SCREENED, --NEXT-AA2AA1-JK-SCREENED, '// &
        '--NEXT-ZPCD-SCREENED, --NEXT-AA1AA1-SCREENED, '// &
        '--U, --POST-AA1 OR --ROLLING-AA1/--ROLLING-AA1-NEXT.')
    endif
    next_mode=.true.
    do i=1,8
      call get_command_argument(i+1,path(i))
      if (len_trim(path(i)) == 0) call fail('EMPTY XSM PATH ARGUMENT.')
      if (len_trim(path(i)) > max_xsm_path) &
        call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
    enddo
  else if (argument_count == 8) then
    call get_command_argument(1,mode_argument)
    if (trim(mode_argument) == '--consecutive') then
      consecutive_mode=.true.
    else if (trim(mode_argument) == '--consecutive-returned') then
      consecutive_mode=.true.
      consecutive_returned_mode=.true.
    else if (trim(mode_argument) == '--consecutive-returned-screened') then
      consecutive_mode=.true.
      consecutive_returned_mode=.true.
      consecutive_returned_screened_mode=.true.
    else if (trim(mode_argument) == '--consecutive-ptu-screened') then
      consecutive_mode=.true.
      consecutive_ptu_screened_mode=.true.
    else if (trim(mode_argument) == '--consecutive-current') then
      consecutive_mode=.true.
      consecutive_current_mode=.true.
    else if (trim(mode_argument) == &
        '--consecutive-current-aa2-picard') then
      consecutive_mode=.true.
      consecutive_current_aa2_picard_mode=.true.
    else if (trim(mode_argument) == &
        '--consecutive-qvwx-zplus-screened') then
      consecutive_mode=.true.
      consecutive_qvwx_zplus_screened_mode=.true.
    else if (trim(mode_argument) == '--consecutive-q5kl-screened') then
      consecutive_mode=.true.
      consecutive_q5kl_screened_mode=.true.
    else
      call fail('EIGHT ARGUMENTS REQUIRE A CONSECUTIVE MODE.')
    endif
    do i=1,7
      call get_command_argument(i+1,path(i))
      if (len_trim(path(i)) == 0) call fail('EMPTY XSM PATH ARGUMENT.')
      if (len_trim(path(i)) > max_xsm_path) &
        call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
    enddo
  else if (argument_count == 7) then
    do i=1,7
      call get_command_argument(i,path(i))
      if (len_trim(path(i)) == 0) call fail('EMPTY XSM PATH ARGUMENT.')
      if (len_trim(path(i)) > max_xsm_path) &
        call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
    enddo
  else
    call fail('EXPECTED DEFAULT SEVEN ARGUMENTS, A CONSECUTIVE MODE PLUS '// &
      'SEVEN, OR --NEXT/--NEXT-X4/--NEXT-X4Z/--NEXT-ZU/--U/--POST-AA1/'// &
      '--NEXT-ZPCD-SCREENED/--ROLLING-AA1/'// &
      '--ROLLING-AA1-NEXT PLUS EIGHT, OR A ROLLING-AA2 MODE PLUS TEN.')
  endif

  if (next_mode) then
    call check_next_candidate(trim(path(1)),trim(path(2)),trim(path(3)), &
      trim(path(4)),trim(path(5)),trim(path(6)),trim(path(7)),trim(path(8)), &
      u_mode,post_aa1_mode,rolling_mode,rolling_next_mode,x4_history_mode, &
      x4z_history_mode,zu_history_mode,x4aa2_screened_mode)
  else

  report_prefix='RANK2-MODAL-AA1'
  previous_output='X1'
  latest_output='X2'
  proposal_carrier='X2-RAW-FLUX'
  if (consecutive_q5kl_screened_mode) then
    report_prefix='RANK2-CURRENT-KL-AA1'
    previous_output='K'
    latest_output='L'
    proposal_carrier='AA1-RAW-FLUX'
    call load_state(trim(path(1)),2,x0,'Q5 AA1 PROPOSAL','AA1-RAW-FLUX')
  else if (consecutive_qvwx_zplus_screened_mode) then
    report_prefix='RANK2-QVWX-ZPLUS-AA1'
    previous_output='Z'
    latest_output='ZP'
    proposal_carrier='AA1-RAW-FLUX'
    call load_state(trim(path(1)),2,x0,'Y AA1 PROPOSAL','AA1-RAW-FLUX')
  else if (consecutive_current_aa2_picard_mode) then
    report_prefix='RANK2-AA2-PICARD-AA1'
    previous_output='P'
    latest_output='Z'
    proposal_carrier='Z-RAW-FLUX'
    call load_state(trim(path(1)),2,x0,'QAA2 PROPOSAL','AA2-RAW-FLUX')
  else if (consecutive_ptu_screened_mode) then
    report_prefix='RANK2-CURRENT-PTU-AA1'
    previous_output='T'
    latest_output='U'
    proposal_carrier='X4-RAW-FLUX'
    call load_state(trim(path(1)),2,x0,'P PROPOSAL','X4-RAW-FLUX')
  else if (consecutive_current_mode) then
    report_prefix='RANK2-QSVW-AA1'
    previous_output='V'
    latest_output='W'
    proposal_carrier='X4-RAW-FLUX'
    call load_state(trim(path(1)),2,x0,'QS PROPOSAL','U-RAW-FLUX')
  else if (consecutive_returned_mode) then
    if (consecutive_returned_screened_mode) then
      report_prefix='RANK2-CURRENT-ZRS-AA1'
      previous_output='R'
      latest_output='S'
    else
      report_prefix='RANK2-LATEST-AA1'
      previous_output='X3'
      latest_output='X4'
    endif
    proposal_carrier='X4-RAW-FLUX'
    call load_state(trim(path(1)),1,x0,'X2 RETURNED')
  else if (consecutive_mode) then
    report_prefix='RANK2-CONSECUTIVE-AA1'
    previous_output='X2'
    latest_output='X3'
    proposal_carrier='X3-RAW-FLUX'
    call load_state(trim(path(1)),2,x0,'X1 PROPOSAL','V-RAW-FLUX')
  else
    call load_state(trim(path(1)),0,x0,'X0')
  endif
  call load_state(trim(path(2)),1,x1,'X1')
  call load_state(trim(path(3)),1,x2,'X2')
  call load_state(trim(path(6)),2,proposal,'PROPOSAL',proposal_carrier)

  call compare_fixed_bundle(x0,x1,'X0/X1')
  call compare_fixed_bundle(x0,x2,'X0/X2')
  call compare_fixed_bundle(x0,proposal,'X0/PROPOSAL')
  call check_basis_reference(trim(path(5)),proposal)
  if (consecutive_q5kl_screened_mode) then
    call validate_input_snapshot(trim(path(4)),x1,x2,'K','L')
  else if (consecutive_qvwx_zplus_screened_mode) then
    call validate_input_snapshot(trim(path(4)),x1,x2,'Z','ZP')
  else if (consecutive_current_aa2_picard_mode) then
    call validate_input_snapshot(trim(path(4)),x1,x2,'P','Z')
  else if (consecutive_ptu_screened_mode) then
    call validate_input_snapshot(trim(path(4)),x1,x2,'T','U')
  else if (consecutive_returned_screened_mode) then
    call validate_input_snapshot(trim(path(4)),x1,x2,'R','S')
  else if (consecutive_current_mode) then
    call validate_input_snapshot(trim(path(4)),x1,x2,'V','W')
  else if (consecutive_returned_mode) then
    call validate_input_snapshot(trim(path(4)),x1,x2,'X3','X4')
  else if (consecutive_mode) then
    call validate_input_snapshot(trim(path(4)),x1,x2,'X2','X3')
  endif

  call modal_history_geometry(x0,x1,x2,update0_sq,update1_sq, &
    update_dot)
  denominator=update0_sq+update1_sq-2.0_real64*update_dot
  if ((.not.ieee_is_finite(denominator)).or. &
      (denominator <= 0.0_real64)) &
    call fail('NONPOSITIVE MODAL-AA1 DENOMINATOR.')
  beta=(update0_sq-update_dot)/denominator
  previous_weight=1.0_real64-beta
  if ((.not.ieee_is_finite(beta)).or. &
      (.not.ieee_is_finite(previous_weight))) &
    call fail('NON-FINITE MODAL-AA1 WEIGHT.')
  if (consecutive_current_aa2_picard_mode.or. &
      consecutive_q5kl_screened_mode.or. &
      consecutive_qvwx_zplus_screened_mode.or. &
      consecutive_returned_screened_mode.or. &
      consecutive_ptu_screened_mode) then
    modal_affine_sq=previous_weight**2*update0_sq+beta**2*update1_sq+ &
      2.0_real64*previous_weight*beta*update_dot
    if ((.not.ieee_is_finite(modal_affine_sq)).or. &
        (modal_affine_sq < 0.0_real64)) then
      if (consecutive_current_aa2_picard_mode) then
        call fail('INVALID AA2-PICARD MODAL ANDERSON SCREEN.')
      else
        call fail('INVALID SCREENED RETURNED MODAL ANDERSON SCREEN.')
      endif
    endif
    modal_affine_norm=sqrt(modal_affine_sq)
    modal_current_norm=sqrt(update1_sq)
  endif

  if (consecutive_current_mode.or. &
      consecutive_current_aa2_picard_mode.or. &
      consecutive_q5kl_screened_mode.or. &
      consecutive_qvwx_zplus_screened_mode.or. &
      consecutive_returned_screened_mode.or. &
      consecutive_ptu_screened_mode) then
    leakage_sq=0.0_real64
    leakage_dot=0.0_real64
    leakage_affine_d=0.0_real64
    do s=1,x0%dims(3)
      do g=1,x0%dims(2)
        il=(s-1)*x0%dims(2)+g
        leakage_delta01=x1%leakage(il)-x0%leakage(il)
        leakage_delta12=x2%leakage(il)-x1%leakage(il)
        leakage_sq(1)=leakage_sq(1)+x0%height(s)*leakage_delta01**2
        leakage_sq(2)=leakage_sq(2)+x0%height(s)*leakage_delta12**2
        leakage_dot=leakage_dot+x0%height(s)* &
          leakage_delta01*leakage_delta12
        leakage_affine_d=max(leakage_affine_d, &
          abs(previous_weight*leakage_delta01+beta*leakage_delta12))
      enddo
    enddo
    leakage_affine_sq=previous_weight**2*leakage_sq(1)+ &
      beta**2*leakage_sq(2)+ &
      2.0_real64*previous_weight*beta*leakage_dot
    leakage_current_d=maxval(abs(x2%leakage-x1%leakage))
    if (any(.not.ieee_is_finite(leakage_sq)).or. &
        any(leakage_sq <= 0.0_real64).or. &
        (.not.ieee_is_finite(leakage_dot)).or. &
        (.not.ieee_is_finite(leakage_affine_sq)).or. &
        (leakage_affine_sq < 0.0_real64).or. &
        (.not.ieee_is_finite(leakage_affine_d)).or. &
        (.not.ieee_is_finite(leakage_current_d)).or. &
        (leakage_current_d <= 0.0_real64)) &
      call fail('INVALID CURRENT LEAKAGE ANDERSON SCREEN.')
    leakage_current_norm=sqrt(leakage_sq(2))
    leakage_affine_norm=sqrt(leakage_affine_sq)
    if (consecutive_current_aa2_picard_mode.or. &
        consecutive_q5kl_screened_mode.or. &
        consecutive_qvwx_zplus_screened_mode.or. &
        consecutive_returned_screened_mode.or. &
        consecutive_ptu_screened_mode) then
      if ((modal_affine_norm >= modal_current_norm).or. &
          (leakage_affine_norm >= leakage_current_norm).or. &
          (leakage_affine_d >= leakage_current_d)) then
        if (consecutive_current_aa2_picard_mode) then
          call fail('AA2-PICARD PARAMETER-FREE DIRECTION GATE FAILED.')
        else
          call fail('SCREENED RETURNED PARAMETER-FREE DIRECTION GATE FAILED.')
        endif
      endif
    endif
  endif

  allocate(expected_a(size(x1%coordinates)))
  expected_a=previous_weight*x1%coordinates+beta*x2%coordinates
  if (any(.not.ieee_is_finite(expected_a))) &
    call fail('NON-FINITE AFFINE MODAL PROPOSAL.')
  if (any(real64_bits(expected_a) /= &
          real64_bits(proposal%coordinates))) &
    call fail('PROPOSAL SPOT-X-A DIFFERS FROM REAL64 AFFINE VALUE.')

  rho_affine=previous_weight*x1%rho+beta*x2%rho
  if ((.not.ieee_is_finite(rho_affine)).or. &
      (rho_affine <= 0.0_real64)) &
    call fail('NONPOSITIVE AFFINE INVERSE EIGENVALUE.')
  keff_published=real(1.0_real64/rho_affine,real32)
  if ((.not.ieee_is_finite(keff_published)).or. &
      (keff_published <= 0.0_real32)) &
    call fail('NONPOSITIVE PUBLISHED EIGENVALUE.')
  rho_published=1.0_real64/real(keff_published,real64)
  if (real32_bits(proposal%keff) /= real32_bits(keff_published)) &
    call fail('PROPOSAL K-EFFECTIVE DIFFERS FROM REAL32 PUBLICATION.')
  if (real64_bits(proposal%rho) /= real64_bits(rho_published)) &
    call fail('PROPOSAL SPOT-X-RHO DIFFERS FROM PUBLISHED K RECIPROCAL.')
  publication_delta=abs(rho_published-rho_affine)

  allocate(expected_l32(size(x1%leakage)))
  allocate(expected_l(size(x1%leakage)))
  expected_l32=real(previous_weight*x1%leakage+beta*x2%leakage,real32)
  expected_l=real(expected_l32,real64)
  if (any(.not.ieee_is_finite(expected_l32)).or. &
      any(.not.ieee_is_finite(expected_l))) &
    call fail('NON-FINITE PUBLISHED LEAKAGE.')
  if (any(real64_bits(proposal%leakage) /= real64_bits(expected_l))) &
    call fail('PROPOSAL SPOT-X-L DIFFERS FROM REAL32-ROUNDTRIP AFFINE VALUE.')
  if (real64_bits(proposal%norm) /= real64_bits(x2%norm)) &
    call fail('PROPOSAL SPOT-X-NORM DIFFERS FROM X2 RAW CARRIER.')

  call compare_axial_raw_flux(trim(path(3)),trim(path(6)),x2%state(2))
  if (consecutive_mode) &
    call compare_axial_carrier_payload(trim(path(3)),trim(path(6)))
  call check_snapshot_publication(trim(path(4)),trim(path(7)), &
    expected_l32,keff_published)
  call check_projected_positivity(proposal,min_published_flux,min_group, &
    min_snapshot,min_region)

  call write_real64_metric(trim(report_prefix)//' BETA WEIGHT-'// &
    latest_output,beta)
  call write_real64_metric(trim(report_prefix)//' WEIGHT-'// &
    previous_output,previous_weight)
  call write_real64_metric(trim(report_prefix)//' DENOMINATOR',denominator)
  call write_real32_metric(trim(report_prefix)//' PUBLISHED K',keff_published)
  call write_real64_metric(trim(report_prefix)//' PUBLISHED RHO',rho_published)
  call write_real64_metric(trim(report_prefix)//' RHO PUBLICATION DELTA', &
    publication_delta)
  call write_real32_metric(trim(report_prefix)//' MIN PUBLISHED B*A', &
    min_published_flux)
  if (consecutive_current_mode.or. &
      consecutive_current_aa2_picard_mode.or. &
      consecutive_q5kl_screened_mode.or. &
      consecutive_qvwx_zplus_screened_mode.or. &
      consecutive_returned_screened_mode.or. &
      consecutive_ptu_screened_mode) then
    if (consecutive_current_aa2_picard_mode.or. &
        consecutive_q5kl_screened_mode.or. &
        consecutive_qvwx_zplus_screened_mode.or. &
        consecutive_returned_screened_mode.or. &
        consecutive_ptu_screened_mode) then
      call write_real64_metric(trim(report_prefix)// &
        ' MODAL AFFINE L2/CURRENT',modal_affine_norm/modal_current_norm)
    endif
    call write_real64_metric(trim(report_prefix)// &
      ' LEAKAGE AFFINE L2/CURRENT SAME-MODAL-BETA', &
      leakage_affine_norm/leakage_current_norm)
    call write_real64_metric(trim(report_prefix)// &
      ' LEAKAGE AFFINE DL/CURRENT SAME-MODAL-BETA', &
      leakage_affine_d/leakage_current_d)
    write(6,'(A)') trim(report_prefix)// &
      ' LEAKAGE SCREEN ONLY NO LEAKAGE FIT'
    if (consecutive_current_aa2_picard_mode.or. &
        consecutive_q5kl_screened_mode.or. &
        consecutive_qvwx_zplus_screened_mode.or. &
        consecutive_returned_screened_mode.or. &
        consecutive_ptu_screened_mode) &
      write(6,'(A)') trim(report_prefix)// &
        ' PARAMETER-FREE DIRECTION GATE PASS'
  endif
  write(6,'(A,3(1X,I0))') &
    trim(report_prefix)//' MIN B*A GROUP/SNAPSHOT/REGION', &
    min_group,min_snapshot,min_region
  write(6,'(A,I0)') trim(report_prefix)// &
    ' STRICT-POSITIVE PUBLISHED POINTS ', &
    positive_count_expected
  write(6,'(A)') trim(report_prefix)// &
    ' FIXED-RANK2-BUNDLE BITWISE PASS'
  write(6,'(A)') trim(report_prefix)//' PUBLICATION-Q BITWISE PASS'
  write(6,'(A)') trim(report_prefix)// &
    ' AXIAL/PLANE RAW-FLUX CARRIER BITWISE PASS'
  write(6,'(A)') trim(report_prefix)// &
    ' SNAPSHOT LEAKAGE/K PUBLICATION PASS'
  write(6,'(A)') trim(report_prefix)//' LAGGED SYSTEM BITWISE PASS'
  write(6,'(A)') trim(report_prefix)//' NO STALE RESULT RECORD PASS'
  write(6,'(A)') trim(report_prefix)// &
    ' CLASSIFICATION MATERIALIZED_PROPOSAL_NOT_EVALUATED'
  write(6,'(A)') trim(report_prefix)//' COMPLETE'
  endif

contains

  subroutine check_rolling_aa2_candidate(in0_name,out0_name,in1_name, &
      out1_name,in2_name,out2_name,out2_snap_name,basis_name, &
      proposal_name,proposal_snap_name,rolling_next_mode,current_mode, &
      current_qpzst_mode,current_stuvvw_mode,current_uvvwxy_mode, &
      current_ptuqv_mode,current_cefg_mode)
    character(len=*), intent(in) :: in0_name,out0_name,in1_name,out1_name
    character(len=*), intent(in) :: in2_name,out2_name,out2_snap_name
    character(len=*), intent(in) :: basis_name,proposal_name
    character(len=*), intent(in) :: proposal_snap_name
    logical, intent(in) :: rolling_next_mode,current_mode
    logical, intent(in), optional :: current_qpzst_mode
    logical, intent(in), optional :: current_stuvvw_mode
    logical, intent(in), optional :: current_uvvwxy_mode
    logical, intent(in), optional :: current_ptuqv_mode
    logical, intent(in), optional :: current_cefg_mode
    type(canonical_state) :: in0,out0,in1,out1,in2,out2,proposal_state
    real(real64), allocatable :: affine_a(:),affine_l(:)
    real(real32), allocatable :: published_l(:)
    real(real64) :: f0a,f0b,f1a,f1b,f2a,f2b
    real(real64) :: d0a,d0b,d1a,d1b,metric
    real(real64) :: h00,h01,h11,c0,c1,f2_sq,determinant
    real(real64) :: gamma0,gamma1,alpha0,alpha1,alpha2,predicted_sq
    real(real64) :: modal_predicted_norm,modal_current_norm
    real(real64) :: leakage_predicted_sq,leakage_current_sq
    real(real64) :: leakage_predicted_norm,leakage_current_norm
    real(real64) :: leakage_predicted_d,leakage_current_d
    real(real64) :: leakage_f0,leakage_f1,leakage_f2,leakage_affine
    real(real64) :: rho_affine,rho_published,publication_delta
    real(real32) :: keff_published,min_published_flux
    integer :: g,s,a,b,nmode,index_a,index_b,index_g
    integer :: min_group,min_snapshot,min_region
    character(len=24) :: aa2_report_prefix
    character(len=12) :: aa2_label0,aa2_label1,aa2_label2
    character(len=12) :: aa2_latest_input,aa2_latest_output
    integer :: il
    logical :: qpzst_mode,stuvvw_mode,uvvwxy_mode,ptuqv_mode,cefg_mode
    logical :: direction_gate_mode

    qpzst_mode=.false.
    if (present(current_qpzst_mode)) qpzst_mode=current_qpzst_mode
    stuvvw_mode=.false.
    if (present(current_stuvvw_mode)) stuvvw_mode=current_stuvvw_mode
    uvvwxy_mode=.false.
    if (present(current_uvvwxy_mode)) uvvwxy_mode=current_uvvwxy_mode
    ptuqv_mode=.false.
    if (present(current_ptuqv_mode)) ptuqv_mode=current_ptuqv_mode
    cefg_mode=.false.
    if (present(current_cefg_mode)) cefg_mode=current_cefg_mode
    direction_gate_mode=qpzst_mode.or.stuvvw_mode.or.uvvwxy_mode.or. &
      ptuqv_mode.or.cefg_mode

    if (qpzst_mode.and.(trim(out0_name) /= trim(in1_name))) &
      call fail('QPZST P OUTPUT AND P INPUT MUST BE THE SAME PATH.')
    if (stuvvw_mode.and.(trim(out1_name) /= trim(in2_name))) &
      call fail('STUVVW V OUTPUT AND V INPUT MUST BE THE SAME PATH.')
    if (uvvwxy_mode.and.(trim(out0_name) /= trim(in1_name))) &
      call fail('UVVWXY V OUTPUT AND V INPUT MUST BE THE SAME PATH.')
    if (ptuqv_mode.and.(trim(out0_name) /= trim(in1_name))) &
      call fail('PTUQV T OUTPUT AND T INPUT MUST BE THE SAME PATH.')
    if (cefg_mode.and. &
        (trim(mode_argument) == '--current-cefg-aa2').and. &
        (trim(out0_name) /= trim(in1_name))) &
      call fail('CEFG E OUTPUT AND E INPUT MUST BE THE SAME PATH.')

    if ((current_mode.and.rolling_next_mode).or. &
        (qpzst_mode.and.(current_mode.or.rolling_next_mode.or. &
          stuvvw_mode.or.uvvwxy_mode)).or. &
        (stuvvw_mode.and.(current_mode.or.rolling_next_mode.or. &
          uvvwxy_mode)).or. &
        (uvvwxy_mode.and.(current_mode.or.rolling_next_mode)).or. &
        (ptuqv_mode.and.(current_mode.or.rolling_next_mode.or. &
          qpzst_mode.or.stuvvw_mode.or.uvvwxy_mode)).or. &
        (cefg_mode.and.(current_mode.or.rolling_next_mode.or. &
          qpzst_mode.or.stuvvw_mode.or.uvvwxy_mode.or.ptuqv_mode))) &
      call fail('AA2 MODES ARE MUTUALLY EXCLUSIVE.')
    if (cefg_mode) then
      if (trim(mode_argument) == '--current-klmn-aa2') then
        aa2_report_prefix='RANK2-CURRENT-KLMN-AA2'
        aa2_label0='L'
        aa2_label1='M'
        aa2_label2='N'
        aa2_latest_input='Q7'
        aa2_latest_output='N'
        call load_state(in0_name,1,in0,'KLMN K INPUT')
        call load_state(out0_name,1,out0,'KLMN L OUTPUT')
        call load_state(in1_name,2,in1,'KLMN Q6 INPUT','AA1-RAW-FLUX')
        call load_state(out1_name,1,out1,'KLMN M OUTPUT')
        call load_state(in2_name,2,in2,'KLMN Q7 INPUT','AA1-RAW-FLUX')
        call load_state(out2_name,1,out2,'KLMN N OUTPUT')
      else if (trim(mode_argument) == '--current-ghi-aa2') then
        aa2_report_prefix='RANK2-CURRENT-GHI-AA2'
        aa2_label0='G'
        aa2_label1='H'
        aa2_label2='I'
        aa2_latest_input='Q3'
        aa2_latest_output='I'
        call load_state(in0_name,2,in0,'GHI Q1 INPUT','AA1-RAW-FLUX')
        call load_state(out0_name,1,out0,'GHI G OUTPUT')
        call load_state(in1_name,2,in1,'GHI Q2 INPUT','AA2-RAW-FLUX')
        call load_state(out1_name,1,out1,'GHI H OUTPUT')
        call load_state(in2_name,2,in2,'GHI Q3 INPUT','AA1-RAW-FLUX')
        call load_state(out2_name,1,out2,'GHI I OUTPUT')
      else
        aa2_report_prefix='RANK2-CURRENT-CEFG-AA2'
        aa2_label0='E'
        aa2_label1='F'
        aa2_label2='G'
        aa2_latest_input='Q'
        aa2_latest_output='G'
        call load_state(in0_name,2,in0,'CEFG C INPUT','AA1-RAW-FLUX')
        call load_state(out0_name,1,out0,'CEFG E OUTPUT')
        call load_state(in1_name,1,in1,'CEFG E INPUT')
        call load_state(out1_name,1,out1,'CEFG F OUTPUT')
        call load_state(in2_name,2,in2,'CEFG Q INPUT','AA1-RAW-FLUX')
        call load_state(out2_name,1,out2,'CEFG G OUTPUT')
      endif
    else if (ptuqv_mode) then
      aa2_report_prefix='RANK2-CURRENT-PTUQV-AA2'
      aa2_label0='T'
      aa2_label1='U'
      aa2_label2='V'
      aa2_latest_input='Q'
      aa2_latest_output='V'
      call load_state(in0_name,2,in0,'PTUQV P INPUT','X4-RAW-FLUX')
      call load_state(out0_name,1,out0,'PTUQV T OUTPUT')
      call load_state(in1_name,1,in1,'PTUQV T INPUT')
      call load_state(out1_name,1,out1,'PTUQV U OUTPUT')
      call load_state(in2_name,2,in2,'PTUQV Q INPUT','X4-RAW-FLUX')
      call load_state(out2_name,1,out2,'PTUQV V OUTPUT')
    else if (uvvwxy_mode) then
      aa2_report_prefix='RANK2-CURRENT-UVVWXY-AA2'
      aa2_label0='V'
      aa2_label1='W'
      aa2_label2='Y'
      aa2_latest_input='X'
      aa2_latest_output='Y'
      call load_state(in0_name,2,in0,'UVVWXY U INPUT','AA2-RAW-FLUX')
      call load_state(out0_name,1,out0,'UVVWXY V OUTPUT')
      call load_state(in1_name,1,in1,'UVVWXY V INPUT')
      call load_state(out1_name,1,out1,'UVVWXY W OUTPUT')
      call load_state(in2_name,2,in2,'UVVWXY X INPUT','AA2-RAW-FLUX')
      call load_state(out2_name,1,out2,'UVVWXY Y OUTPUT')
    else if (stuvvw_mode) then
      aa2_report_prefix='RANK2-CURRENT-STUVVW-AA2'
      aa2_label0='T'
      aa2_label1='V'
      aa2_label2='W'
      aa2_latest_input='V'
      aa2_latest_output='W'
      call load_state(in0_name,2,in0,'STUVVW S INPUT','Z-RAW-FLUX')
      call load_state(out0_name,1,out0,'STUVVW T OUTPUT')
      call load_state(in1_name,2,in1,'STUVVW U INPUT','AA2-RAW-FLUX')
      call load_state(out1_name,1,out1,'STUVVW V OUTPUT')
      call load_state(in2_name,1,in2,'STUVVW V INPUT')
      call load_state(out2_name,1,out2,'STUVVW W OUTPUT')
    else if (qpzst_mode) then
      aa2_report_prefix='RANK2-CURRENT-QPZST-AA2'
      aa2_label0='P'
      aa2_label1='Z'
      aa2_label2='T'
      aa2_latest_input='S'
      aa2_latest_output='T'
      call load_state(in0_name,2,in0,'QPZST Q INPUT','AA2-RAW-FLUX')
      call load_state(out0_name,1,out0,'QPZST P OUTPUT')
      call load_state(in1_name,1,in1,'QPZST P INPUT')
      call load_state(out1_name,1,out1,'QPZST Z OUTPUT')
      call load_state(in2_name,2,in2,'QPZST S INPUT','Z-RAW-FLUX')
      call load_state(out2_name,1,out2,'QPZST T OUTPUT')
    else if (current_mode) then
      aa2_report_prefix='RANK2-CURRENT-AA2'
      aa2_label0='X'
      aa2_label1='D'
      aa2_label2='E'
      aa2_latest_input='Y'
      aa2_latest_output='E'
      call load_state(in0_name,1,in0,'CURRENT W INPUT')
      call load_state(out0_name,1,out0,'CURRENT X OUTPUT')
      call load_state(in1_name,2,in1,'CURRENT C INPUT','X4-RAW-FLUX')
      call load_state(out1_name,1,out1,'CURRENT D OUTPUT')
      call load_state(in2_name,2,in2,'CURRENT Y INPUT','Z-RAW-FLUX')
      call load_state(out2_name,1,out2,'CURRENT E OUTPUT')
    else if (rolling_next_mode) then
      aa2_report_prefix='RANK2-ROLLING-AA2-NEXT'
      aa2_label0='XROLL-PLUS'
      aa2_label1='XROLL2-PLUS'
      aa2_label2='XAA2-PLUS'
      aa2_latest_input='XAA2'
      aa2_latest_output='XAA2-PLUS'
      call load_state(in0_name,2,in0,'AA2-NEXT XROLL INPUT', &
        'XNP-RAW-FLUX')
      call load_state(out0_name,1,out0,'AA2-NEXT XROLL OUTPUT')
      call load_state(in1_name,2,in1,'AA2-NEXT XROLL2 INPUT', &
        'XRP-RAW-FLUX')
      call load_state(out1_name,1,out1,'AA2-NEXT XROLL2 OUTPUT')
      call load_state(in2_name,2,in2,'AA2-NEXT XAA2 INPUT', &
        'AA2-RAW-FLUX')
      call load_state(out2_name,1,out2,'AA2-NEXT XAA2 OUTPUT')
    else
      aa2_report_prefix='RANK2-ROLLING-AA2'
      aa2_label0='XNEXT-PLUS'
      aa2_label1='XROLL-PLUS'
      aa2_label2='XROLL2-PLUS'
      aa2_latest_input='XROLL2'
      aa2_latest_output='XROLL2-PLUS'
      call load_state(in0_name,2,in0,'AA2 XNEXT INPUT','AA1-RAW-FLUX')
      call load_state(out0_name,1,out0,'AA2 XNEXT OUTPUT')
      call load_state(in1_name,2,in1,'AA2 XROLL INPUT','XNP-RAW-FLUX')
      call load_state(out1_name,1,out1,'AA2 XROLL OUTPUT')
      call load_state(in2_name,2,in2,'AA2 XROLL2 INPUT','XRP-RAW-FLUX')
      call load_state(out2_name,1,out2,'AA2 XROLL2 OUTPUT')
    endif
    call load_state(proposal_name,2,proposal_state, &
      'AA2 MATERIALIZED PROPOSAL','AA2-RAW-FLUX')

    call compare_fixed_basis_layout(in0,out0,'AA2 IN0/OUT0')
    call compare_fixed_basis_layout(in0,in1,'AA2 IN0/IN1')
    call compare_fixed_basis_layout(in0,out1,'AA2 IN0/OUT1')
    call compare_fixed_basis_layout(in0,in2,'AA2 IN0/IN2')
    call compare_fixed_basis_layout(in0,out2,'AA2 IN0/OUT2')
    call compare_fixed_basis_layout(in0,proposal_state,'AA2 IN0/PROPOSAL')
    call compare_axial_carrier_metadata(out2,proposal_state, &
      trim(aa2_latest_output))
    call check_basis_reference(basis_name,proposal_state)
    call validate_input_snapshot(out2_snap_name,in2,out2, &
      trim(aa2_latest_input),trim(aa2_latest_output))

    h00=0.0_real64
    h01=0.0_real64
    h11=0.0_real64
    c0=0.0_real64
    c1=0.0_real64
    f2_sq=0.0_real64
    do g=1,in0%dims(2)
      nmode=in0%rank(g)
      do s=1,in0%dims(3)
        do a=1,nmode
          index_a=in0%offset(g)+(s-1)*nmode+a
          f0a=out0%coordinates(index_a)-in0%coordinates(index_a)
          f1a=out1%coordinates(index_a)-in1%coordinates(index_a)
          f2a=out2%coordinates(index_a)-in2%coordinates(index_a)
          d0a=f0a-f2a
          d1a=f1a-f2a
          do b=1,nmode
            index_b=in0%offset(g)+(s-1)*nmode+b
            index_g=in0%gram_offset(g)+(b-1)*nmode+a
            f0b=out0%coordinates(index_b)-in0%coordinates(index_b)
            f1b=out1%coordinates(index_b)-in1%coordinates(index_b)
            f2b=out2%coordinates(index_b)-in2%coordinates(index_b)
            d0b=f0b-f2b
            d1b=f1b-f2b
            metric=in0%height(s)*in0%gram(index_g)
            h00=h00+d0a*metric*d0b
            h01=h01+d0a*metric*d1b
            h11=h11+d1a*metric*d1b
            c0=c0+d0a*metric*f2b
            c1=c1+d1a*metric*f2b
            f2_sq=f2_sq+f2a*metric*f2b
          enddo
        enddo
      enddo
    enddo
    if ((.not.ieee_is_finite(h00)).or.(h00 <= 0.0_real64).or. &
        (.not.ieee_is_finite(h01)).or. &
        (.not.ieee_is_finite(h11)).or.(h11 <= 0.0_real64).or. &
        (.not.ieee_is_finite(c0)).or.(.not.ieee_is_finite(c1)).or. &
        (.not.ieee_is_finite(f2_sq)).or.(f2_sq < 0.0_real64)) &
      call fail('INVALID ROLLING AA2 MODAL GEOMETRY.')
    determinant=h00*h11-h01*h01
    if ((.not.ieee_is_finite(determinant)).or. &
        (determinant <= 0.0_real64)) &
      call fail('SINGULAR ROLLING AA2 SYSTEM.')
    gamma0=(h01*c1-h11*c0)/determinant
    gamma1=(h01*c0-h00*c1)/determinant
    alpha0=gamma0
    alpha1=gamma1
    alpha2=1.0_real64-gamma0-gamma1
    if ((.not.ieee_is_finite(alpha0)).or. &
        (.not.ieee_is_finite(alpha1)).or. &
        (.not.ieee_is_finite(alpha2))) &
      call fail('NON-FINITE ROLLING AA2 WEIGHT.')
    predicted_sq=f2_sq+2.0_real64*gamma0*c0+ &
      2.0_real64*gamma1*c1+gamma0*gamma0*h00+ &
      2.0_real64*gamma0*gamma1*h01+gamma1*gamma1*h11
    if ((.not.ieee_is_finite(predicted_sq)).or. &
        (predicted_sq < 0.0_real64)) &
      call fail('INVALID ROLLING AA2 PREDICTED RESIDUAL.')

    if (direction_gate_mode) then
      if (f2_sq <= 0.0_real64) &
        call fail('INVALID CURRENT AA2 MODAL RESIDUAL.')
      modal_predicted_norm=sqrt(predicted_sq)
      modal_current_norm=sqrt(f2_sq)
      leakage_predicted_sq=0.0_real64
      leakage_current_sq=0.0_real64
      leakage_predicted_d=0.0_real64
      leakage_current_d=0.0_real64
      do s=1,in0%dims(3)
        do g=1,in0%dims(2)
          il=(s-1)*in0%dims(2)+g
          leakage_f0=out0%leakage(il)-in0%leakage(il)
          leakage_f1=out1%leakage(il)-in1%leakage(il)
          leakage_f2=out2%leakage(il)-in2%leakage(il)
          leakage_affine=alpha0*leakage_f0+alpha1*leakage_f1+ &
            alpha2*leakage_f2
          leakage_predicted_sq=leakage_predicted_sq+ &
            in0%height(s)*leakage_affine**2
          leakage_current_sq=leakage_current_sq+ &
            in0%height(s)*leakage_f2**2
          leakage_predicted_d=max(leakage_predicted_d, &
            abs(leakage_affine))
          leakage_current_d=max(leakage_current_d,abs(leakage_f2))
        enddo
      enddo
      if ((.not.ieee_is_finite(leakage_predicted_sq)).or. &
          (leakage_predicted_sq < 0.0_real64).or. &
          (.not.ieee_is_finite(leakage_current_sq)).or. &
          (leakage_current_sq <= 0.0_real64).or. &
          (.not.ieee_is_finite(leakage_predicted_d)).or. &
          (.not.ieee_is_finite(leakage_current_d)).or. &
          (leakage_current_d <= 0.0_real64)) &
        call fail('INVALID CURRENT AA2 LEAKAGE DIRECTION SCREEN.')
      leakage_predicted_norm=sqrt(leakage_predicted_sq)
      leakage_current_norm=sqrt(leakage_current_sq)
      if ((modal_predicted_norm >= modal_current_norm).or. &
          (leakage_predicted_norm >= leakage_current_norm).or. &
          (leakage_predicted_d >= leakage_current_d)) &
        call fail('CURRENT AA2 PARAMETER-FREE DIRECTION GATE FAILED.')
    endif

    allocate(affine_a(size(out2%coordinates)))
    affine_a=alpha0*out0%coordinates+alpha1*out1%coordinates+ &
      alpha2*out2%coordinates
    if (any(.not.ieee_is_finite(affine_a))) &
      call fail('NON-FINITE ROLLING AA2 AFFINE MODAL PROPOSAL.')
    if (any(real64_bits(affine_a) /= &
            real64_bits(proposal_state%coordinates))) &
      call fail('ROLLING AA2 SPOT-X-A DIFFERS FROM REAL64 AFFINE VALUE.')

    rho_affine=alpha0*out0%rho+alpha1*out1%rho+alpha2*out2%rho
    if ((.not.ieee_is_finite(rho_affine)).or. &
        (rho_affine <= 0.0_real64)) &
      call fail('NONPOSITIVE ROLLING AA2 AFFINE INVERSE EIGENVALUE.')
    keff_published=real(1.0_real64/rho_affine,real32)
    if ((.not.ieee_is_finite(keff_published)).or. &
        (keff_published <= 0.0_real32)) &
      call fail('NONPOSITIVE ROLLING AA2 PUBLISHED EIGENVALUE.')
    rho_published=1.0_real64/real(keff_published,real64)
    if (real32_bits(proposal_state%keff) /= &
        real32_bits(keff_published)) &
      call fail('ROLLING AA2 K-EFFECTIVE DIFFERS FROM PUBLICATION.')
    if (real64_bits(proposal_state%rho) /= real64_bits(rho_published)) &
      call fail('ROLLING AA2 SPOT-X-RHO DIFFERS FROM K RECIPROCAL.')
    publication_delta=abs(rho_published-rho_affine)

    allocate(affine_l(size(out2%leakage)))
    allocate(published_l(size(out2%leakage)))
    affine_l=alpha0*out0%leakage+alpha1*out1%leakage+ &
      alpha2*out2%leakage
    published_l=real(affine_l,real32)
    if (any(.not.ieee_is_finite(affine_l)).or. &
        any(.not.ieee_is_finite(published_l))) &
      call fail('NON-FINITE ROLLING AA2 PUBLISHED LEAKAGE.')
    if (any(real64_bits(proposal_state%leakage) /= &
            real64_bits(real(published_l,real64)))) &
      call fail('ROLLING AA2 SPOT-X-L DIFFERS FROM PUBLICATION.')
    if (real64_bits(proposal_state%norm) /= real64_bits(out2%norm)) &
      call fail('ROLLING AA2 NORM DIFFERS FROM LATEST RAW CARRIER.')

    call compare_axial_carrier_payload(out2_name,proposal_name)
    call compare_axial_raw_flux(out2_name,proposal_name,out2%state(2))
    call check_snapshot_publication(out2_snap_name,proposal_snap_name, &
      published_l,keff_published)
    call check_projected_positivity(proposal_state,min_published_flux, &
      min_group,min_snapshot,min_region)

    call write_real64_metric(trim(aa2_report_prefix)//' ALPHA-'// &
      trim(aa2_label0),alpha0)
    call write_real64_metric(trim(aa2_report_prefix)//' ALPHA-'// &
      trim(aa2_label1),alpha1)
    call write_real64_metric(trim(aa2_report_prefix)//' ALPHA-'// &
      trim(aa2_label2),alpha2)
    call write_real64_metric(trim(aa2_report_prefix)//' H00',h00)
    call write_real64_metric(trim(aa2_report_prefix)//' H01',h01)
    call write_real64_metric(trim(aa2_report_prefix)//' H11',h11)
    call write_real64_metric(trim(aa2_report_prefix)//' DETERMINANT', &
      determinant)
    call write_real64_metric( &
      trim(aa2_report_prefix)//' PREDICTED-RESIDUAL-SQ',predicted_sq)
    call write_real32_metric(trim(aa2_report_prefix)//' PUBLISHED K', &
      keff_published)
    call write_real64_metric(trim(aa2_report_prefix)//' PUBLISHED RHO', &
      rho_published)
    call write_real64_metric(trim(aa2_report_prefix)// &
      ' RHO PUBLICATION DELTA',publication_delta)
    call write_real32_metric(trim(aa2_report_prefix)// &
      ' MIN PUBLISHED B*A', &
      min_published_flux)
    write(6,'(A,3(1X,I0))') &
      trim(aa2_report_prefix)//' MIN B*A GROUP/SNAPSHOT/REGION', &
      min_group,min_snapshot,min_region
    write(6,'(A,I0)') trim(aa2_report_prefix)// &
      ' STRICT-POSITIVE POINTS ', &
      positive_count_expected
    if (direction_gate_mode) then
      call write_real64_metric(trim(aa2_report_prefix)// &
        ' MODAL AFFINE L2/CURRENT', &
        modal_predicted_norm/modal_current_norm)
      call write_real64_metric(trim(aa2_report_prefix)// &
        ' LEAKAGE AFFINE L2/CURRENT SAME-MODAL-WEIGHTS', &
        leakage_predicted_norm/leakage_current_norm)
      call write_real64_metric(trim(aa2_report_prefix)// &
        ' LEAKAGE AFFINE DL/CURRENT SAME-MODAL-WEIGHTS', &
        leakage_predicted_d/leakage_current_d)
      write(6,'(A)') trim(aa2_report_prefix)// &
        ' LEAKAGE SCREEN ONLY NO LEAKAGE FIT'
      write(6,'(A)') trim(aa2_report_prefix)// &
        ' PARAMETER-FREE DIRECTION GATE PASS'
    endif
    write(6,'(A)') trim(aa2_report_prefix)// &
      ' STANDARD 2X2 SYSTEM PASS'
    write(6,'(A)') trim(aa2_report_prefix)// &
      ' FIXED-RANK2-BUNDLE BITWISE PASS'
    write(6,'(A)') trim(aa2_report_prefix)// &
      ' PUBLICATION-Q BITWISE PASS'
    write(6,'(A)') trim(aa2_report_prefix)// &
      ' LATEST AX/RAW-FLUX CARRIER BITWISE PASS'
    write(6,'(A)') trim(aa2_report_prefix)// &
      ' LATEST SNAPSHOT LIFECYCLE PASS'
    write(6,'(A)') trim(aa2_report_prefix)// &
      ' NO STALE RESULT RECORD PASS'
    write(6,'(A)') trim(aa2_report_prefix)//' CLASSIFICATION '// &
      'MATERIALIZED_PROPOSAL_NOT_EVALUATED'
    write(6,'(A)') trim(aa2_report_prefix)//' COMPLETE'
  end subroutine check_rolling_aa2_candidate

  subroutine check_next_candidate(x1_name,x2_name,y_name,z_name,z_snap_name, &
      basis_name,proposal_name,proposal_snap_name,u_mode,post_aa1_mode, &
      rolling_mode,rolling_next_mode,x4_history_mode,x4z_history_mode, &
      zu_history_mode,x4aa2_screened_mode)
    character(len=*), intent(in) :: x1_name,x2_name,y_name,z_name,z_snap_name
    character(len=*), intent(in) :: basis_name,proposal_name,proposal_snap_name
    logical, intent(in) :: u_mode,post_aa1_mode,rolling_mode
    logical, intent(in) :: rolling_next_mode,x4_history_mode
    logical, intent(in) :: x4z_history_mode,zu_history_mode
    logical, intent(in), optional :: x4aa2_screened_mode
    type(canonical_state) :: state_x1,state_x2,state_y,state_z,state_proposal
    real(real64), allocatable :: affine_a(:),affine_l(:)
    real(real32), allocatable :: published_l(:)
    real(real64) :: p_sq,q_sq,p_dot_q,denominator,beta,weight_x2
    real(real64) :: modal_affine_sq,modal_affine_norm,modal_current_norm
    real(real64) :: leakage_affine_sq,leakage_affine_norm
    real(real64) :: leakage_current_sq,leakage_current_norm
    real(real64) :: leakage_affine_d,leakage_current_d
    real(real64) :: leakage_p,leakage_q,leakage_affine
    real(real64) :: rho_affine,rho_published,publication_delta
    real(real32) :: keff_published,min_published_flux
    integer :: min_group,min_snapshot,min_region,g,s,il
    character(len=24) :: report_prefix
    character(len=12) :: input_carrier,output_carrier
    character(len=8) :: latest_input,latest_output,previous_output
    logical :: current_screened_mode

    current_screened_mode=.false.
    if (present(x4aa2_screened_mode)) &
      current_screened_mode=x4aa2_screened_mode

    if ((u_mode.and.(post_aa1_mode.or.rolling_mode.or. &
          rolling_next_mode.or.x4_history_mode.or.x4z_history_mode.or. &
          zu_history_mode.or.current_screened_mode)).or. &
        (post_aa1_mode.and.(rolling_mode.or.rolling_next_mode.or. &
          x4_history_mode.or.x4z_history_mode.or.zu_history_mode.or. &
          current_screened_mode)).or. &
        (rolling_mode.and.(rolling_next_mode.or.x4_history_mode.or. &
          x4z_history_mode.or.zu_history_mode.or.current_screened_mode)).or. &
        (rolling_next_mode.and.(x4_history_mode.or.x4z_history_mode.or. &
          zu_history_mode.or.current_screened_mode)).or. &
        (x4_history_mode.and.(x4z_history_mode.or.zu_history_mode.or. &
          current_screened_mode)).or. &
        (x4z_history_mode.and.(zu_history_mode.or.current_screened_mode)).or. &
        (zu_history_mode.and.current_screened_mode)) &
      call fail('NEXT PROPOSAL MODES ARE MUTUALLY EXCLUSIVE.')
    if (current_screened_mode) then
      if (trim(mode_argument) == '--next-aa1aa1-screened') then
        input_carrier='AA1-RAW-FLUX'
        output_carrier='AA1-RAW-FLUX'
        report_prefix='RANK2-CURRENT-MN-AA1'
        latest_input='Q7'
        latest_output='N'
        previous_output='M'
        call load_state(x1_name,2,state_x1,'PREVIOUS PROPOSAL Q6', &
          'AA1-RAW-FLUX')
      else if (trim(mode_argument) == '--next-zpcd-screened') then
        input_carrier='AA1-RAW-FLUX'
        output_carrier='AA1-RAW-FLUX'
        report_prefix='RANK2-CURRENT-ZPCD-AA1'
        latest_input='C'
        latest_output='D'
        previous_output='ZP'
        call load_state(x1_name,1,state_x1,'PREVIOUS MAP INPUT Z')
      else if (trim(mode_argument) == '--next-aa1aa2-ij-screened') then
        input_carrier='AA2-RAW-FLUX'
        output_carrier='AA1-RAW-FLUX'
        report_prefix='RANK2-CURRENT-IJ-AA1'
        latest_input='Q4'
        latest_output='J'
        previous_output='I'
        call load_state(x1_name,2,state_x1,'PREVIOUS PROPOSAL Q3', &
          'AA1-RAW-FLUX')
      else if (trim(mode_argument) == '--next-aa2aa1-jk-screened') then
        input_carrier='AA1-RAW-FLUX'
        output_carrier='AA1-RAW-FLUX'
        report_prefix='RANK2-CURRENT-JK-AA1'
        latest_input='Q5'
        latest_output='K'
        previous_output='J'
        call load_state(x1_name,2,state_x1,'PREVIOUS PROPOSAL Q4', &
          'AA2-RAW-FLUX')
      else if (trim(mode_argument) == '--next-aa1aa2-screened') then
        input_carrier='AA2-RAW-FLUX'
        output_carrier='AA1-RAW-FLUX'
        report_prefix='RANK2-CURRENT-GH-AA1'
        latest_input='Q2'
        latest_output='H'
        previous_output='G'
        call load_state(x1_name,2,state_x1,'PREVIOUS PROPOSAL Q1', &
          'AA1-RAW-FLUX')
      else
        input_carrier='AA2-RAW-FLUX'
        output_carrier='AA1-RAW-FLUX'
        report_prefix='RANK2-CURRENT-QVWX-AA1'
        latest_input='W'
        latest_output='X'
        previous_output='V'
        call load_state(x1_name,2,state_x1,'PREVIOUS PROPOSAL Q', &
          'X4-RAW-FLUX')
      endif
    else if (zu_history_mode) then
      input_carrier='U-RAW-FLUX'
      output_carrier='V2-RAW-FLUX'
      report_prefix='RANK2-LATEST-QV-AA1'
      latest_input='QS'
      latest_output='V'
      previous_output='U'
      call load_state(x1_name,2,state_x1,'PREVIOUS PROPOSAL QT', &
        'Z-RAW-FLUX')
    else if (x4z_history_mode) then
      input_carrier='Z-RAW-FLUX'
      output_carrier='U-RAW-FLUX'
      report_prefix='RANK2-LATEST2-AA1-NEXT'
      latest_input='QT'
      latest_output='U'
      previous_output='Z'
      call load_state(x1_name,2,state_x1,'PREVIOUS PROPOSAL QY', &
        'X4-RAW-FLUX')
    else if (x4_history_mode) then
      input_carrier='X4-RAW-FLUX'
      output_carrier='Z-RAW-FLUX'
      report_prefix='RANK2-LATEST-AA1-NEXT'
      latest_input='QY'
      latest_output='Z'
      previous_output='X4'
      call load_state(x1_name,1,state_x1,'PREVIOUS MAP INPUT X3')
    else if (rolling_next_mode) then
      input_carrier='XNP-RAW-FLUX'
      output_carrier='XRP-RAW-FLUX'
      report_prefix='RANK2-ROLL2-AA1'
      latest_input='XROLL'
      latest_output='XROLL-P'
      previous_output='XNEXT-P'
      call load_state(x1_name,2,state_x1,'PREVIOUS PROPOSAL XNEXT', &
        'AA1-RAW-FLUX')
    else if (rolling_mode) then
      input_carrier='AA1-RAW-FLUX'
      output_carrier='XNP-RAW-FLUX'
      report_prefix='RANK2-ROLL-AA1'
      latest_input='XNEXT'
      latest_output='XNEXT-P'
      previous_output='AA1-PLUS'
      call load_state(x1_name,2,state_x1,'PREVIOUS PROPOSAL AA1', &
        'X3-RAW-FLUX')
    else if (post_aa1_mode) then
      input_carrier='X3-RAW-FLUX'
      output_carrier='AA1-RAW-FLUX'
      report_prefix='RANK2-POST-AA1'
      latest_input='AA1'
      latest_output='AA1-PLUS'
      previous_output='X3'
      call load_state(x1_name,1,state_x1,'PREVIOUS MAP INPUT X2')
    else if (u_mode) then
      input_carrier='Z-RAW-FLUX'
      output_carrier='V-RAW-FLUX'
      report_prefix='RANK2-MODAL-AA1-U'
      latest_input='W'
      latest_output='V'
      previous_output='Z'
      call load_state(x1_name,2,state_x1,'PREVIOUS PROPOSAL Y', &
        'X2-RAW-FLUX')
    else
      input_carrier='X2-RAW-FLUX'
      output_carrier='Z-RAW-FLUX'
      report_prefix='RANK2-NEXT-MODAL-AA1'
      latest_input='Y'
      latest_output='Z'
      previous_output='X2'
      call load_state(x1_name,1,state_x1,'NEXT X1')
    endif
    call load_state(x2_name,1,state_x2,'PREVIOUS RETURNED OUTPUT')
    call load_state(y_name,2,state_y,'LATEST PROPOSAL INPUT',input_carrier)
    call load_state(z_name,1,state_z,'LATEST RETURNED OUTPUT')
    call load_state(proposal_name,2,state_proposal,'MATERIALIZED PROPOSAL', &
      output_carrier)

    call compare_fixed_basis_layout(state_x1,state_x2,'NEXT X1/X2')
    call compare_fixed_basis_layout(state_x1,state_y,'NEXT X1/Y')
    call compare_fixed_basis_layout(state_x1,state_z,'NEXT X1/Z')
    call compare_fixed_basis_layout(state_x1,state_proposal, &
      'NEXT X1/PROPOSAL')
    call compare_axial_carrier_metadata(state_z,state_proposal, &
      latest_output)
    call check_basis_reference(basis_name,state_proposal)
    call validate_input_snapshot(z_snap_name,state_y,state_z,latest_input, &
      latest_output)

    call modal_pair_geometry(state_x1,state_x2,state_y,state_z,p_sq,q_sq, &
      p_dot_q)
    denominator=p_sq+q_sq-2.0_real64*p_dot_q
    if ((.not.ieee_is_finite(denominator)).or. &
        (denominator <= 0.0_real64)) &
      call fail('NONPOSITIVE NEXT MODAL-AA1 DENOMINATOR.')
    beta=(p_sq-p_dot_q)/denominator
    weight_x2=1.0_real64-beta
    if ((.not.ieee_is_finite(beta)).or. &
        (.not.ieee_is_finite(weight_x2))) &
      call fail('NON-FINITE NEXT MODAL-AA1 WEIGHT.')

    if (current_screened_mode) then
      if (q_sq <= 0.0_real64) &
        call fail('INVALID CURRENT SCREENED MODAL RESIDUAL.')
      modal_affine_sq=weight_x2**2*p_sq+beta**2*q_sq+ &
        2.0_real64*weight_x2*beta*p_dot_q
      if ((.not.ieee_is_finite(modal_affine_sq)).or. &
          (modal_affine_sq < 0.0_real64)) &
        call fail('INVALID CURRENT SCREENED MODAL DIRECTION.')
      modal_affine_norm=sqrt(modal_affine_sq)
      modal_current_norm=sqrt(q_sq)

      leakage_affine_sq=0.0_real64
      leakage_current_sq=0.0_real64
      leakage_affine_d=0.0_real64
      leakage_current_d=0.0_real64
      do s=1,state_x1%dims(3)
        do g=1,state_x1%dims(2)
          il=(s-1)*state_x1%dims(2)+g
          leakage_p=state_x2%leakage(il)-state_x1%leakage(il)
          leakage_q=state_z%leakage(il)-state_y%leakage(il)
          leakage_affine=weight_x2*leakage_p+beta*leakage_q
          leakage_affine_sq=leakage_affine_sq+ &
            state_x1%height(s)*leakage_affine**2
          leakage_current_sq=leakage_current_sq+ &
            state_x1%height(s)*leakage_q**2
          leakage_affine_d=max(leakage_affine_d,abs(leakage_affine))
          leakage_current_d=max(leakage_current_d,abs(leakage_q))
        enddo
      enddo
      if ((.not.ieee_is_finite(leakage_affine_sq)).or. &
          (leakage_affine_sq < 0.0_real64).or. &
          (.not.ieee_is_finite(leakage_current_sq)).or. &
          (leakage_current_sq <= 0.0_real64).or. &
          (.not.ieee_is_finite(leakage_affine_d)).or. &
          (.not.ieee_is_finite(leakage_current_d)).or. &
          (leakage_current_d <= 0.0_real64)) &
        call fail('INVALID CURRENT SCREENED LEAKAGE DIRECTION.')
      leakage_affine_norm=sqrt(leakage_affine_sq)
      leakage_current_norm=sqrt(leakage_current_sq)
      if ((modal_affine_norm >= modal_current_norm).or. &
          (leakage_affine_norm >= leakage_current_norm).or. &
          (leakage_affine_d >= leakage_current_d)) &
        call fail('CURRENT AA1 PARAMETER-FREE DIRECTION GATE FAILED.')
    endif

    allocate(affine_a(size(state_x2%coordinates)))
    affine_a=weight_x2*state_x2%coordinates+beta*state_z%coordinates
    if (any(.not.ieee_is_finite(affine_a))) &
      call fail('NON-FINITE NEXT AFFINE MODAL PROPOSAL.')
    if (any(real64_bits(affine_a) /= &
            real64_bits(state_proposal%coordinates))) &
      call fail('NEXT PROPOSAL SPOT-X-A DIFFERS FROM REAL64 AFFINE VALUE.')

    rho_affine=weight_x2*state_x2%rho+beta*state_z%rho
    if ((.not.ieee_is_finite(rho_affine)).or. &
        (rho_affine <= 0.0_real64)) &
      call fail('NONPOSITIVE NEXT AFFINE INVERSE EIGENVALUE.')
    keff_published=real(1.0_real64/rho_affine,real32)
    if ((.not.ieee_is_finite(keff_published)).or. &
        (keff_published <= 0.0_real32)) &
      call fail('NONPOSITIVE NEXT PUBLISHED EIGENVALUE.')
    rho_published=1.0_real64/real(keff_published,real64)
    if (real32_bits(state_proposal%keff) /= &
        real32_bits(keff_published)) &
      call fail('NEXT PROPOSAL K-EFFECTIVE DIFFERS FROM REAL32 PUBLICATION.')
    if (real64_bits(state_proposal%rho) /= real64_bits(rho_published)) &
      call fail( &
        'NEXT PROPOSAL SPOT-X-RHO DIFFERS FROM PUBLISHED K RECIPROCAL.')
    publication_delta=abs(rho_published-rho_affine)

    allocate(affine_l(size(state_x2%leakage)))
    allocate(published_l(size(state_x2%leakage)))
    affine_l=weight_x2*state_x2%leakage+beta*state_z%leakage
    published_l=real(affine_l,real32)
    if (any(.not.ieee_is_finite(affine_l)).or. &
        any(.not.ieee_is_finite(published_l))) &
      call fail('NON-FINITE NEXT PUBLISHED LEAKAGE.')
    if (any(real64_bits(state_proposal%leakage) /= &
            real64_bits(real(published_l,real64)))) &
      call fail( &
        'NEXT PROPOSAL SPOT-X-L DIFFERS FROM REAL32-ROUNDTRIP AFFINE VALUE.')
    if (real64_bits(state_proposal%norm) /= real64_bits(state_z%norm)) &
      call fail('PROPOSAL SPOT-X-NORM DIFFERS FROM RAW CARRIER.')

    call compare_axial_carrier_payload(z_name,proposal_name)
    call compare_axial_raw_flux(z_name,proposal_name,state_z%state(2))
    call check_snapshot_publication(z_snap_name,proposal_snap_name, &
      published_l,keff_published)
    call check_projected_positivity(state_proposal,min_published_flux, &
      min_group,min_snapshot,min_region)

    call write_real64_metric(trim(report_prefix)//' BETA WEIGHT-'// &
      trim(latest_output),beta)
    call write_real64_metric(trim(report_prefix)//' WEIGHT-'// &
      trim(previous_output),weight_x2)
    call write_real64_metric(trim(report_prefix)//' DENOMINATOR',denominator)
    call write_real32_metric(trim(report_prefix)//' PUBLISHED K', &
      keff_published)
    call write_real64_metric(trim(report_prefix)//' PUBLISHED RHO', &
      rho_published)
    call write_real64_metric(trim(report_prefix)// &
      ' RHO PUBLICATION DELTA',publication_delta)
    call write_real32_metric(trim(report_prefix)//' MIN PUBLISHED B*A', &
      min_published_flux)
    write(6,'(A,3(1X,I0))') &
      trim(report_prefix)//' MIN B*A GROUP/SNAPSHOT/REGION', &
      min_group,min_snapshot,min_region
    write(6,'(A,I0)') &
      trim(report_prefix)//' STRICT-POSITIVE PUBLISHED POINTS ', &
      positive_count_expected
    if (current_screened_mode) then
      call write_real64_metric(trim(report_prefix)// &
        ' MODAL AFFINE L2/CURRENT',modal_affine_norm/modal_current_norm)
      call write_real64_metric(trim(report_prefix)// &
        ' LEAKAGE AFFINE L2/CURRENT SAME-MODAL-BETA', &
        leakage_affine_norm/leakage_current_norm)
      call write_real64_metric(trim(report_prefix)// &
        ' LEAKAGE AFFINE DL/CURRENT SAME-MODAL-BETA', &
        leakage_affine_d/leakage_current_d)
      write(6,'(A)') trim(report_prefix)// &
        ' LEAKAGE SCREEN ONLY NO LEAKAGE FIT'
      write(6,'(A)') trim(report_prefix)// &
        ' PARAMETER-FREE DIRECTION GATE PASS'
    endif
    write(6,'(A)') trim(report_prefix)// &
      ' FIXED-RANK2-BUNDLE BITWISE PASS'
    write(6,'(A)') trim(report_prefix)//' PUBLICATION-Q BITWISE PASS'
    write(6,'(A)') trim(report_prefix)//' '//trim(latest_output)// &
      ' AXIAL ROOT/RAW-FLUX CARRIER BITWISE PASS'
    write(6,'(A)') trim(report_prefix)//' '//trim(latest_output)// &
      ' AXIAL STATE/GERR CARRIER BITWISE PASS'
    write(6,'(A)') trim(report_prefix)//' '//trim(latest_output)// &
      ' INPUT SNAPSHOT '//trim(latest_input)//'-TO-'// &
      trim(latest_output)//' LIFECYCLE PASS'
    write(6,'(A)') trim(report_prefix)// &
      ' SNAPSHOT LEAKAGE/K PUBLICATION PASS'
    write(6,'(A)') trim(report_prefix)// &
      ' SNAPSHOT ROOT/PAYLOAD BITWISE PASS'
    write(6,'(A)') trim(report_prefix)//' LAGGED SYSTEM BITWISE PASS'
    write(6,'(A)') trim(report_prefix)//' NO STALE RESULT RECORD PASS'
    write(6,'(A)') trim(report_prefix)// &
      ' CLASSIFICATION MATERIALIZED_PROPOSAL_NOT_EVALUATED'
    write(6,'(A)') trim(report_prefix)//' COMPLETE'
  end subroutine check_next_candidate

  subroutine load_state(file_name,record_mode,data,owner,proposal_carrier)
    character(len=*), intent(in) :: file_name,owner
    integer, intent(in) :: record_mode
    type(canonical_state), intent(out) :: data
    character(len=*), intent(in), optional :: proposal_carrier
    type(c_ptr) :: root
    integer :: ngrp,nsnap,ncoef,total_basis,total_gram,g
    integer :: length_found,type_found
    real(real64), allocatable :: offspace(:),defect(:)
    character(len=12) :: marker,expected_carrier

    call LCMOP(root,file_name,2,2,0)
    call require_record(root,'SIGNATURE',3,3,owner)
    call LCMGTC(root,'SIGNATURE',12,data%signature)
    if (data%signature /= 'L_FLUX') &
      call fail(trim(owner)//' L_FLUX SIGNATURE EXPECTED.')
    call require_record(root,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(root,'STATE-VECTOR',data%state)

    call require_record(root,'SPOT-X-DIMS',4,1,owner)
    call LCMGET(root,'SPOT-X-DIMS',data%dims)
    ngrp=data%dims(2)
    nsnap=data%dims(3)
    ncoef=data%dims(4)
    if ((data%dims(1) /= 1).or.(ngrp /= ngrp_expected).or. &
        (nsnap /= nsnap_expected).or.(ncoef <= 0).or. &
        (data%state(1) /= ngrp).or.(data%state(2) <= 0)) &
      call fail(trim(owner)//' INVALID CANONICAL DIMENSIONS.')

    allocate(data%rank(ngrp),data%offset(ngrp+1))
    allocate(data%gram_offset(ngrp+1),data%basis_offset(ngrp+1))
    call require_record(root,'SPOT-X-RANK',ngrp,1,owner)
    call require_record(root,'SPOT-X-OFF',ngrp+1,1,owner)
    call require_record(root,'SPOT-X-GOFF',ngrp+1,1,owner)
    call require_record(root,'SPOT-X-BOFF',ngrp+1,1,owner)
    call LCMGET(root,'SPOT-X-RANK',data%rank)
    call LCMGET(root,'SPOT-X-OFF',data%offset)
    call LCMGET(root,'SPOT-X-GOFF',data%gram_offset)
    call LCMGET(root,'SPOT-X-BOFF',data%basis_offset)
    if (any(data%rank /= rank_expected).or. &
        (data%offset(1) /= 0).or.(data%gram_offset(1) /= 0).or. &
        (data%basis_offset(1) /= 0).or. &
        (data%offset(ngrp+1) /= ncoef)) &
      call fail(trim(owner)//' IS NOT THE FROZEN RANK-TWO LAYOUT.')
    do g=1,ngrp
      if (data%offset(g+1)-data%offset(g) /= &
          nsnap_expected*rank_expected) &
        call fail(trim(owner)//' INVALID COORDINATE OFFSETS.')
      if (data%gram_offset(g+1)-data%gram_offset(g) /= &
          rank_expected*rank_expected) &
        call fail(trim(owner)//' INVALID GRAM OFFSETS.')
      if (data%basis_offset(g+1)-data%basis_offset(g) /= &
          nreg_expected*rank_expected) &
        call fail(trim(owner)//' INVALID BASIS OFFSETS.')
    enddo
    total_basis=data%basis_offset(ngrp+1)
    total_gram=data%gram_offset(ngrp+1)

    allocate(data%basis(total_basis),data%coordinates(ncoef))
    allocate(data%leakage(ngrp*nsnap),data%height(nsnap))
    allocate(data%gram(total_gram))
    call require_record(root,'SPOT-X-BASIS',total_basis,2,owner)
    call require_record(root,'SPOT-X-A',ncoef,4,owner)
    call require_record(root,'SPOT-X-L',ngrp*nsnap,4,owner)
    call require_record(root,'SPOT-X-H',nsnap,4,owner)
    call require_record(root,'SPOT-X-GRAM',total_gram,4,owner)
    call require_record(root,'K-EFFECTIVE',1,2,owner)
    call require_record(root,'SPOT-X-RHO',1,4,owner)
    call require_record(root,'SPOT-X-NORM',1,4,owner)
    call require_record(root,'SPOT-X-GERR',1,4,owner)
    call require_record(root,'SPOT-X-FIXB',1,1,owner)
    call require_record(root,'SPOT-X-NID',3,3,owner)
    call require_record(root,'SPOT-X-BTYP',3,3,owner)
    call LCMGET(root,'SPOT-X-BASIS',data%basis)
    call LCMGET(root,'SPOT-X-A',data%coordinates)
    call LCMGET(root,'SPOT-X-L',data%leakage)
    call LCMGET(root,'SPOT-X-H',data%height)
    call LCMGET(root,'SPOT-X-GRAM',data%gram)
    call LCMGET(root,'K-EFFECTIVE',data%keff)
    call LCMGET(root,'SPOT-X-RHO',data%rho)
    call LCMGET(root,'SPOT-X-NORM',data%norm)
    call LCMGET(root,'SPOT-X-GERR',data%gram_error)
    call LCMGET(root,'SPOT-X-FIXB',data%fixb)
    call LCMGTC(root,'SPOT-X-NID',12,data%norm_id)
    call LCMGTC(root,'SPOT-X-BTYP',12,data%basis_type)
    if ((data%fixb /= 1).or.(data%norm_id /= 'NUFISS-UNIT').or. &
        (data%basis_type /= 'POD-FIXED')) &
      call fail(trim(owner)//' INVALID FIXED-BASIS MARKERS.')
    if (any(.not.ieee_is_finite(data%basis)).or. &
        any(.not.ieee_is_finite(data%coordinates)).or. &
        any(.not.ieee_is_finite(data%leakage)).or. &
        any(.not.ieee_is_finite(data%height)).or. &
        any(data%height <= 0.0_real64).or. &
        any(.not.ieee_is_finite(data%gram)).or. &
        (.not.ieee_is_finite(data%keff)).or. &
        (data%keff <= 0.0_real32).or. &
        (.not.ieee_is_finite(data%rho)).or.(data%rho <= 0.0_real64).or. &
        (.not.ieee_is_finite(data%norm)).or.(data%norm <= 0.0_real64).or. &
        (.not.ieee_is_finite(data%gram_error)).or. &
        (data%gram_error < 0.0_real64)) &
      call fail(trim(owner)//' NON-FINITE OR NONPHYSICAL STATE.')
    if (real64_bits(data%rho) /= &
        real64_bits(1.0_real64/real(data%keff,real64))) &
      call fail(trim(owner)//' K/RHO PUBLICATION IDENTITY FAILED.')

    if (record_mode == 2) then
      call require_absent(root,'SPOT-X-RRHO',owner)
      call require_absent(root,'SPOT-X-RLEAK',owner)
      call require_absent(root,'SPOT-X-DLEAK',owner)
      call require_absent(root,'SPOT-X-RA',owner)
      call require_absent(root,'SPOT-X-PERP',owner)
      call require_absent(root,'SPOT-X-EPOCH',owner)
      call require_absent(root,'SPOT-GBAL',owner)
      ! Ganlib record names contain at most 12 characters.  SPOGBAL's
      ! source-level label SPOT-GBAL-MAX is physically stored under this
      ! twelve-character key.
      call require_absent(root,'SPOT-GBAL-MA',owner)
      call require_record(root,'SPOT-X-STATE',3,3,owner)
      call require_record(root,'SPOT-X-CARR',3,3,owner)
      call LCMGTC(root,'SPOT-X-STATE',12,marker)
      if (marker /= 'PROPOSAL') &
        call fail('PROPOSAL SPOT-X-STATE MARKER IS INVALID.')
      call LCMGTC(root,'SPOT-X-CARR',12,marker)
      expected_carrier='X2-RAW-FLUX'
      if (present(proposal_carrier)) then
        if (len_trim(proposal_carrier) > len(expected_carrier)) &
          call fail('PROPOSAL CARRIER MARKER EXCEEDS GANLIB LIMIT.')
        expected_carrier=proposal_carrier
      endif
      if (marker /= expected_carrier) &
        call fail('PROPOSAL SPOT-X-CARR MARKER IS INVALID.')
    else
      call require_record(root,'SPOT-X-PERP',ngrp*nsnap,4,owner)
      allocate(offspace(ngrp*nsnap))
      call LCMGET(root,'SPOT-X-PERP',offspace)
      if (any(.not.ieee_is_finite(offspace)).or. &
          any(offspace < 0.0_real64)) &
        call fail(trim(owner)//' INVALID OFF-SPACE DIAGNOSTIC.')
      deallocate(offspace)
      call require_absent(root,'SPOT-X-STATE',owner)
      call require_absent(root,'SPOT-X-CARR',owner)
      if (record_mode == 0) then
        call require_absent(root,'SPOT-X-RRHO',owner)
        call require_absent(root,'SPOT-X-RLEAK',owner)
        call require_absent(root,'SPOT-X-DLEAK',owner)
        call require_absent(root,'SPOT-X-RA',owner)
      else
        allocate(defect(4))
        call require_record(root,'SPOT-X-RRHO',1,4,owner)
        call require_record(root,'SPOT-X-RLEAK',1,4,owner)
        call require_record(root,'SPOT-X-DLEAK',1,4,owner)
        call require_record(root,'SPOT-X-RA',1,4,owner)
        call LCMGET(root,'SPOT-X-RRHO',defect(1))
        call LCMGET(root,'SPOT-X-RLEAK',defect(2))
        call LCMGET(root,'SPOT-X-DLEAK',defect(3))
        call LCMGET(root,'SPOT-X-RA',defect(4))
        if (any(.not.ieee_is_finite(defect)).or. &
            any(defect < 0.0_real64)) &
          call fail(trim(owner)//' INVALID SAVED MAP DEFECT.')
        deallocate(defect)
      endif
    endif
    call LCMLEN(root,'FLUX',length_found,type_found)
    if ((length_found /= ngrp).or.(type_found /= 10)) &
      call fail(trim(owner)//' INVALID RAW AXIAL FLUX LIST.')
    call LCMCL(root,1)
  end subroutine load_state

  subroutine compare_fixed_bundle(left,right,owner)
    type(canonical_state), intent(in) :: left,right
    character(len=*), intent(in) :: owner

    if ((left%signature /= right%signature).or. &
        any(left%state /= right%state).or.any(left%dims /= right%dims).or. &
        (left%fixb /= right%fixb).or. &
        (left%norm_id /= right%norm_id).or. &
        (left%basis_type /= right%basis_type).or. &
        any(left%rank /= right%rank).or. &
        any(left%offset /= right%offset).or. &
        any(left%gram_offset /= right%gram_offset).or. &
        any(left%basis_offset /= right%basis_offset)) &
      call fail(trim(owner)//' FIXED LAYOUT DIFFERS.')
    if (any(real32_bits(left%basis) /= real32_bits(right%basis))) &
      call fail(trim(owner)//' FIXED BASIS BITS DIFFER.')
    if (any(real64_bits(left%height) /= real64_bits(right%height)).or. &
        any(real64_bits(left%gram) /= real64_bits(right%gram)).or. &
        (real64_bits(left%gram_error) /= &
         real64_bits(right%gram_error))) &
      call fail(trim(owner)//' FIXED METRIC BITS DIFFER.')
  end subroutine compare_fixed_bundle

  subroutine compare_fixed_basis_layout(left,right,owner)
    type(canonical_state), intent(in) :: left,right
    character(len=*), intent(in) :: owner

    if (any(left%dims /= right%dims).or. &
        (left%fixb /= right%fixb).or. &
        (left%norm_id /= right%norm_id).or. &
        (left%basis_type /= right%basis_type).or. &
        any(left%rank /= right%rank).or. &
        any(left%offset /= right%offset).or. &
        any(left%gram_offset /= right%gram_offset).or. &
        any(left%basis_offset /= right%basis_offset)) &
      call fail(trim(owner)//' FIXED BASIS LAYOUT DIFFERS.')
    if (any(real32_bits(left%basis) /= real32_bits(right%basis))) &
      call fail(trim(owner)//' FIXED BASIS BITS DIFFER.')
    if (any(real64_bits(left%height) /= real64_bits(right%height)).or. &
        any(real64_bits(left%gram) /= real64_bits(right%gram))) &
      call fail(trim(owner)//' FIXED BASIS METRIC BITS DIFFER.')
  end subroutine compare_fixed_basis_layout

  subroutine compare_axial_carrier_metadata(carrier,proposal_state, &
      carrier_label)
    type(canonical_state), intent(in) :: carrier,proposal_state
    character(len=*), intent(in) :: carrier_label

    if ((carrier%signature /= proposal_state%signature).or. &
        any(carrier%state /= proposal_state%state)) &
      call fail('PROPOSAL AXIAL STATE METADATA DIFFERS FROM '// &
        trim(carrier_label)//' CARRIER.')
    if (real64_bits(carrier%gram_error) /= &
        real64_bits(proposal_state%gram_error)) &
      call fail('PROPOSAL SPOT-X-GERR DIFFERS FROM '// &
        trim(carrier_label)//' CARRIER.')
  end subroutine compare_axial_carrier_metadata

  subroutine check_basis_reference(file_name,state_data)
    character(len=*), intent(in) :: file_name
    type(canonical_state), intent(in) :: state_data
    type(c_ptr) :: root,groups,group_ptr
    integer :: system_state(nstate),rank_root(ngrp_expected)
    integer :: fixb,g,nmode,nreg,nsnap,first,last
    real(real32), allocatable :: basis(:)
    character(len=12) :: signature,basis_type

    call LCMOP(root,file_name,2,2,0)
    call require_record(root,'SIGNATURE',3,3,'BASIS REFERENCE')
    call LCMGTC(root,'SIGNATURE',12,signature)
    if (signature /= 'L_PIJ') call fail('BASIS REFERENCE L_PIJ EXPECTED.')
    call require_record(root,'STATE-VECTOR',nstate,1,'BASIS REFERENCE')
    call LCMGET(root,'STATE-VECTOR',system_state)
    if (system_state(8) /= ngrp_expected) &
      call fail('BASIS REFERENCE GROUP COUNT DIFFERS.')
    call require_record(root,'SPOT-FIXB',1,1,'BASIS REFERENCE')
    call require_record(root,'SPOT-BTYPE',3,3,'BASIS REFERENCE')
    call LCMGET(root,'SPOT-FIXB',fixb)
    call LCMGTC(root,'SPOT-BTYPE',12,basis_type)
    if ((fixb /= 0).or.(basis_type /= 'POD-BUILT')) &
      call fail('BASIS REFERENCE BUILD MARKERS DIFFER.')
    call require_record(root,'POD-RANK-G',ngrp_expected,1, &
      'BASIS REFERENCE')
    call LCMGET(root,'POD-RANK-G',rank_root)
    if (any(rank_root /= rank_expected)) &
      call fail('BASIS REFERENCE IS NOT RANK TWO.')
    call require_record(root,'GROUP',ngrp_expected,10,'BASIS REFERENCE')
    groups=LCMGID(root,'GROUP')
    do g=1,ngrp_expected
      group_ptr=LCMGIL(groups,g)
      call require_record(group_ptr,'NREG2D',1,1,'BASIS GROUP')
      call require_record(group_ptr,'NSNAP',1,1,'BASIS GROUP')
      call require_record(group_ptr,'POD-NMODE',1,1,'BASIS GROUP')
      call LCMGET(group_ptr,'NREG2D',nreg)
      call LCMGET(group_ptr,'NSNAP',nsnap)
      call LCMGET(group_ptr,'POD-NMODE',nmode)
      if ((nreg /= nreg_expected).or.(nsnap /= nsnap_expected).or. &
          (nmode /= rank_expected)) &
        call fail('BASIS REFERENCE GROUP DIMENSIONS DIFFER.')
      allocate(basis(nreg*nmode))
      call require_record(group_ptr,'POD-BASIS',nreg*nmode,2, &
        'BASIS GROUP')
      call LCMGET(group_ptr,'POD-BASIS',basis)
      first=state_data%basis_offset(g)+1
      last=state_data%basis_offset(g+1)
      if (any(real32_bits(basis) /= &
              real32_bits(state_data%basis(first:last)))) &
        call fail('STATE BASIS BITS DIFFER FROM RANK-TWO REFERENCE.')
      deallocate(basis)
    enddo
    call LCMCL(root,1)
  end subroutine check_basis_reference

  subroutine modal_history_geometry(state0,state1,state2,sq0,sq1,dot01)
    type(canonical_state), intent(in) :: state0,state1,state2
    real(real64), intent(out) :: sq0,sq1,dot01
    integer :: g,s,a,b,nmode,index_a,index_b,index_g
    real(real64) :: delta0_a,delta0_b,delta1_a,delta1_b

    sq0=0.0_real64
    sq1=0.0_real64
    dot01=0.0_real64
    do g=1,state0%dims(2)
      nmode=state0%rank(g)
      do s=1,state0%dims(3)
        do a=1,nmode
          index_a=state0%offset(g)+(s-1)*nmode+a
          delta0_a=state1%coordinates(index_a)- &
            state0%coordinates(index_a)
          delta1_a=state2%coordinates(index_a)- &
            state1%coordinates(index_a)
          do b=1,nmode
            index_b=state0%offset(g)+(s-1)*nmode+b
            index_g=state0%gram_offset(g)+(b-1)*nmode+a
            delta0_b=state1%coordinates(index_b)- &
              state0%coordinates(index_b)
            delta1_b=state2%coordinates(index_b)- &
              state1%coordinates(index_b)
            sq0=sq0+state0%height(s)*delta0_a* &
              state0%gram(index_g)*delta0_b
            sq1=sq1+state0%height(s)*delta1_a* &
              state0%gram(index_g)*delta1_b
            dot01=dot01+state0%height(s)*delta0_a* &
              state0%gram(index_g)*delta1_b
          enddo
        enddo
      enddo
    enddo
    if ((.not.ieee_is_finite(sq0)).or.(sq0 <= 0.0_real64).or. &
        (.not.ieee_is_finite(sq1)).or.(sq1 <= 0.0_real64).or. &
        (.not.ieee_is_finite(dot01))) &
      call fail('INVALID MODAL HISTORY GEOMETRY.')
  end subroutine modal_history_geometry

  subroutine modal_pair_geometry(input_p,output_p,input_q,output_q,p_sq,q_sq, &
      p_dot_q)
    type(canonical_state), intent(in) :: input_p,output_p,input_q,output_q
    real(real64), intent(out) :: p_sq,q_sq,p_dot_q
    integer :: g,s,a,b,nmode,index_a,index_b,index_g
    real(real64) :: p_a,p_b,q_a,q_b

    p_sq=0.0_real64
    q_sq=0.0_real64
    p_dot_q=0.0_real64
    do g=1,input_p%dims(2)
      nmode=input_p%rank(g)
      do s=1,input_p%dims(3)
        do a=1,nmode
          index_a=input_p%offset(g)+(s-1)*nmode+a
          p_a=output_p%coordinates(index_a)-input_p%coordinates(index_a)
          q_a=output_q%coordinates(index_a)-input_q%coordinates(index_a)
          do b=1,nmode
            index_b=input_p%offset(g)+(s-1)*nmode+b
            index_g=input_p%gram_offset(g)+(b-1)*nmode+a
            p_b=output_p%coordinates(index_b)-input_p%coordinates(index_b)
            q_b=output_q%coordinates(index_b)-input_q%coordinates(index_b)
            p_sq=p_sq+input_p%height(s)*p_a*input_p%gram(index_g)*p_b
            q_sq=q_sq+input_p%height(s)*q_a*input_p%gram(index_g)*q_b
            p_dot_q=p_dot_q+input_p%height(s)*p_a* &
              input_p%gram(index_g)*q_b
          enddo
        enddo
      enddo
    enddo
    if ((.not.ieee_is_finite(p_sq)).or.(p_sq < 0.0_real64).or. &
        (.not.ieee_is_finite(q_sq)).or.(q_sq < 0.0_real64).or. &
        (.not.ieee_is_finite(p_dot_q))) &
      call fail('INVALID NEXT MODAL PAIR GEOMETRY.')
  end subroutine modal_pair_geometry

  subroutine compare_axial_carrier_payload(carrier_name,proposal_name)
    character(len=*), intent(in) :: carrier_name,proposal_name
    type(c_ptr) :: carrier,proposal_root
    character(len=12) :: name,first
    integer :: length_left,length_right,type_left,type_right,expected_count

    call LCMOP(carrier,carrier_name,2,2,0)
    call LCMOP(proposal_root,proposal_name,2,2,0)
    ! The proposal adds exactly two lifecycle markers.
    expected_count=2
    name=' '
    call LCMNXT(carrier,name)
    first=name
    do
      call LCMLEN(carrier,name,length_left,type_left)
      call LCMLEN(proposal_root,name,length_right,type_right)
      select case(name)
      case('SPOT-X-RRHO','SPOT-X-RLEAK','SPOT-X-DLEAK','SPOT-X-RA', &
           'SPOT-X-PERP','SPOT-X-EPOCH','SPOT-GBAL','SPOT-GBAL-MA')
        if (length_right /= 0) &
          call fail('PROPOSAL AXIAL ROOT RETAINS STALE RECORD: '//trim(name))
      case('SPOT-X-A','K-EFFECTIVE','SPOT-X-RHO','SPOT-X-L')
        expected_count=expected_count+1
        if ((length_left /= length_right).or. &
            (type_left /= type_right)) &
          call fail('PROPOSAL AXIAL PUBLISHED RECORD SHAPE DIFFERS: '// &
            trim(name))
      case default
        expected_count=expected_count+1
        if ((length_left /= length_right).or. &
            (type_left /= type_right)) &
          call fail('PROPOSAL AXIAL CARRIER RECORD SHAPE DIFFERS: '// &
            trim(name))
        call compare_named_record(carrier,proposal_root,name,length_left, &
          type_left,'AXIAL CARRIER ROOT')
      end select
      call LCMNXT(carrier,name)
      if (name == first) exit
    enddo
    if (count_table_records(proposal_root) /= expected_count) &
      call fail('PROPOSAL AXIAL ROOT INVENTORY DIFFERS FROM CARRIER.')
    call LCMCL(proposal_root,1)
    call LCMCL(carrier,1)
  end subroutine compare_axial_carrier_payload

  subroutine compare_axial_raw_flux(x2_name,proposal_name,nunk)
    character(len=*), intent(in) :: x2_name,proposal_name
    integer, intent(in) :: nunk
    type(c_ptr) :: x2_root,proposal_root,x2_flux,proposal_flux
    real(real32), allocatable :: left(:),right(:)
    integer :: g

    call LCMOP(x2_root,x2_name,2,2,0)
    call LCMOP(proposal_root,proposal_name,2,2,0)
    call require_record(x2_root,'FLUX',ngrp_expected,10,'X2 AXIAL')
    call require_record(proposal_root,'FLUX',ngrp_expected,10, &
      'PROPOSAL AXIAL')
    x2_flux=LCMGID(x2_root,'FLUX')
    proposal_flux=LCMGID(proposal_root,'FLUX')
    allocate(left(nunk),right(nunk))
    do g=1,ngrp_expected
      call require_list_item(x2_flux,g,nunk,2,'X2 AXIAL FLUX')
      call require_list_item(proposal_flux,g,nunk,2, &
        'PROPOSAL AXIAL FLUX')
      call LCMGDL(x2_flux,g,left)
      call LCMGDL(proposal_flux,g,right)
      if (any(real32_bits(left) /= real32_bits(right))) &
        call fail('PROPOSAL RAW AXIAL FLUX CARRIER CHANGED.')
    enddo
    deallocate(right,left)
    call LCMCL(proposal_root,1)
    call LCMCL(x2_root,1)
  end subroutine compare_axial_raw_flux

  subroutine validate_input_snapshot(file_name,parent_state,returned_state, &
      parent_label,returned_label)
    character(len=*), intent(in) :: file_name
    type(canonical_state), intent(in) :: parent_state,returned_state
    character(len=*), intent(in) :: parent_label,returned_label
    type(c_ptr) :: root,fluxes,systems,plane,system
    integer :: listdim,s,first,plane_id
    real(real32) :: fixed_source_k
    real(real32), allocatable :: plane_leakage(:),system_leakage(:)
    real(real64) :: iter_k
    character(len=64) :: owner

    call LCMOP(root,file_name,2,2,0)
    owner=trim(returned_label)//' SNAPSHOT INPUT'
    call require_archive_root(root,listdim,trim(owner))
    if (listdim /= nsnap_expected) &
      call fail(trim(owner)//' PLANE COUNT DIFFERS.')
    call require_record(root,'SPOT-ITER-K',1,4,trim(owner))
    call LCMGET(root,'SPOT-ITER-K',iter_k)
    if (real64_bits(iter_k) /= &
        real64_bits(real(returned_state%keff,real64))) &
      call fail(trim(owner)//' K IS NOT THE RETURNED '// &
        trim(returned_label)//' VALUE.')
    call require_absent(root,'SPOT-R64',trim(owner))
    fluxes=LCMGID(root,'FLUX')
    systems=LCMGID(root,'SYSTEM')
    allocate(plane_leakage(ngrp_expected),system_leakage(ngrp_expected))
    do s=1,nsnap_expected
      plane=LCMGIL(fluxes,s)
      system=LCMGIL(systems,s)
      call require_record(plane,'SPOT-LEAK1D',ngrp_expected,2, &
        trim(owner)//' PLANE FLUX')
      call require_record(plane,'SPOT-FS-K',1,2, &
        trim(owner)//' PLANE FLUX')
      call LCMGET(plane,'SPOT-LEAK1D',plane_leakage)
      call LCMGET(plane,'SPOT-FS-K',fixed_source_k)
      first=(s-1)*ngrp_expected+1
      if (any(real32_bits(plane_leakage) /= real32_bits(real( &
          returned_state%leakage(first:first+ngrp_expected-1),real32)))) &
        call fail(trim(owner)//' PLANE LEAKAGE DIFFERS FROM '// &
          trim(returned_label)//'.')
      if (real32_bits(fixed_source_k) /= real32_bits(parent_state%keff)) &
        call fail(trim(owner)//' FIXED-SOURCE K DIFFERS FROM '// &
          trim(parent_label)//'.')
      call require_record(system,'SPOT-LEAK1D',ngrp_expected,2, &
        trim(owner)//' LAGGED SYSTEM')
      call require_record(system,'SPOT-L1-SNAP',1,1, &
        trim(owner)//' LAGGED SYSTEM')
      call LCMGET(system,'SPOT-LEAK1D',system_leakage)
      call LCMGET(system,'SPOT-L1-SNAP',plane_id)
      if (any(real32_bits(system_leakage) /= real32_bits(real( &
          parent_state%leakage(first:first+ngrp_expected-1),real32)))) &
        call fail(trim(owner)//' LAGGED SYSTEM LEAKAGE DIFFERS FROM '// &
          trim(parent_label)//'.')
      if (plane_id /= s) &
        call fail(trim(owner)//' LAGGED SYSTEM SNAPSHOT INDEX DIFFERS.')
    enddo
    deallocate(system_leakage,plane_leakage)
    call LCMCL(root,1)
  end subroutine validate_input_snapshot

  subroutine check_snapshot_publication(x2_name,proposal_name,leak_pub,k_pub)
    character(len=*), intent(in) :: x2_name,proposal_name
    real(real32), intent(in) :: leak_pub(:),k_pub
    type(c_ptr) :: x2_root,proposal_root
    type(c_ptr) :: x2_fluxes,proposal_fluxes,x2_flux,proposal_flux
    integer :: listdim_x2,listdim_proposal,s
    real(real32), allocatable :: stored_leak(:)
    real(real64) :: iter_k

    call LCMOP(x2_root,x2_name,2,2,0)
    call LCMOP(proposal_root,proposal_name,2,2,0)
    call require_archive_root(x2_root,listdim_x2,'X2 SNAPSHOT')
    call require_archive_root(proposal_root,listdim_proposal, &
      'PROPOSAL SNAPSHOT')
    if ((listdim_x2 /= nsnap_expected).or. &
        (listdim_proposal /= listdim_x2)) &
      call fail('SNAPSHOT ARCHIVE PLANE COUNT DIFFERS.')
    call compare_snapshot_root_carrier(x2_root,proposal_root)
    call require_record(proposal_root,'SPOT-ITER-K',1,4, &
      'PROPOSAL SNAPSHOT')
    call LCMGET(proposal_root,'SPOT-ITER-K',iter_k)
    if ((.not.ieee_is_finite(iter_k)).or. &
        (real64_bits(iter_k) /= real64_bits(real(k_pub,real64)))) &
      call fail('PROPOSAL SNAPSHOT SPOT-ITER-K DIFFERS FROM PUBLISHED K.')
    call require_absent(proposal_root,'SPOT-L1-ERR','PROPOSAL SNAPSHOT')
    call require_absent(proposal_root,'SPOT-PJ-PERP','PROPOSAL SNAPSHOT')
    call require_absent(proposal_root,'SPOT-PROJECT','PROPOSAL SNAPSHOT')
    call require_absent(proposal_root,'SPOT-R64','PROPOSAL SNAPSHOT')

    x2_fluxes=LCMGID(x2_root,'FLUX')
    proposal_fluxes=LCMGID(proposal_root,'FLUX')
    allocate(stored_leak(ngrp_expected))
    do s=1,nsnap_expected
      x2_flux=LCMGIL(x2_fluxes,s)
      proposal_flux=LCMGIL(proposal_fluxes,s)
      ! Everything in the plane, including raw FLUX, SOUR, SPOT-QFISS and
      ! every fixed-source diagnostic, remains the z/x2 carrier.  Only the
      ! explicitly published SPOT-LEAK1D value may differ.
      call compare_table_except_leakage(x2_flux,proposal_flux, &
        'SNAPSHOT PLANE FLUX')
      call require_record(x2_flux,'SPOT-LEAK1D',ngrp_expected,2, &
        'X2 PLANE FLUX')
      call require_record(proposal_flux,'SPOT-LEAK1D',ngrp_expected,2, &
        'PROPOSAL PLANE FLUX')
      call LCMGET(proposal_flux,'SPOT-LEAK1D',stored_leak)
      if (any(real32_bits(stored_leak) /= real32_bits( &
          leak_pub((s-1)*ngrp_expected+1:s*ngrp_expected)))) &
        call fail('PROPOSAL SNAPSHOT LEAKAGE DIFFERS FROM PUBLISHED L.')
    enddo
    deallocate(stored_leak)
    call LCMCL(proposal_root,1)
    call LCMCL(x2_root,1)
  end subroutine check_snapshot_publication

  subroutine require_archive_root(root,listdim,owner)
    type(c_ptr), intent(in) :: root
    integer, intent(out) :: listdim
    character(len=*), intent(in) :: owner
    character(len=12) :: signature

    call require_record(root,'SIGNATURE',3,3,owner)
    call LCMGTC(root,'SIGNATURE',12,signature)
    if (signature /= 'L_ARCHIVE') &
      call fail(trim(owner)//' L_ARCHIVE SIGNATURE EXPECTED.')
    call require_record(root,'LISTDIM',1,1,owner)
    call LCMGET(root,'LISTDIM',listdim)
    call require_record(root,'TRACK',listdim,10,owner)
    call require_record(root,'MICROLIB2',listdim,10,owner)
    call require_record(root,'SYSTEM',listdim,10,owner)
    call require_record(root,'FLUX',listdim,10,owner)
  end subroutine require_archive_root

  subroutine compare_snapshot_root_carrier(carrier,proposal_root)
    type(c_ptr), intent(in) :: carrier,proposal_root
    character(len=72) :: file_name,my_name
    character(len=12) :: name,first
    logical :: empty,is_lcm
    integer :: root_length,length_left,length_right,type_left,type_right
    integer :: expected_count

    call LCMINF(carrier,file_name,my_name,empty,root_length,is_lcm)
    if (empty) call fail('SNAPSHOT CARRIER ROOT IS EMPTY.')
    expected_count=0
    name=' '
    call LCMNXT(carrier,name)
    first=name
    do
      call LCMLEN(carrier,name,length_left,type_left)
      call LCMLEN(proposal_root,name,length_right,type_right)
      select case(name)
      case('SPOT-L1-ERR','SPOT-PJ-PERP','SPOT-PROJECT')
        if (length_right /= 0) &
          call fail('PROPOSAL SNAPSHOT RETAINS STALE ROOT RECORD.')
      case default
        expected_count=expected_count+1
        if ((length_left /= length_right).or.(type_left /= type_right)) &
          call fail('PROPOSAL SNAPSHOT ROOT RECORD DIFFERS: '//trim(name))
        if ((name /= 'SPOT-ITER-K').and.(name /= 'FLUX')) &
          call compare_named_record(carrier,proposal_root,name,length_left, &
            type_left,'SNAPSHOT ROOT')
      end select
      call LCMNXT(carrier,name)
      if (name == first) exit
    enddo
    if (count_table_records(proposal_root) /= expected_count) &
      call fail('PROPOSAL SNAPSHOT ROOT INVENTORY DIFFERS.')
  end subroutine compare_snapshot_root_carrier

  subroutine check_projected_positivity(state_data,min_value,min_g,min_s, &
      min_r)
    type(canonical_state), intent(in) :: state_data
    real(real32), intent(out) :: min_value
    integer, intent(out) :: min_g,min_s,min_r
    integer :: g,s,r,a,index_a,index_b,count
    real(real64) :: canonical_value
    real(real32) :: published_value

    min_value=huge(0.0_real32)
    min_g=0
    min_s=0
    min_r=0
    count=0
    do g=1,ngrp_expected
      do s=1,nsnap_expected
        do r=1,nreg_expected
          canonical_value=0.0_real64
          do a=1,rank_expected
            index_a=state_data%offset(g)+(s-1)*rank_expected+a
            index_b=state_data%basis_offset(g)+ &
              (a-1)*nreg_expected+r
            canonical_value=canonical_value+ &
              real(state_data%basis(index_b),real64)* &
              state_data%coordinates(index_a)
          enddo
          published_value=real(canonical_value,real32)
          if ((.not.ieee_is_finite(canonical_value)).or. &
              (.not.ieee_is_finite(published_value)).or. &
              (published_value <= 0.0_real32)) &
            call fail('NONPOSITIVE REAL32-PUBLISHED B*A VALUE.')
          count=count+1
          if (published_value < min_value) then
            min_value=published_value
            min_g=g
            min_s=s
            min_r=r
          endif
        enddo
      enddo
    enddo
    if ((count /= positive_count_expected).or.(min_g == 0)) &
      call fail('PUBLISHED B*A POSITIVITY CENSUS IS INCOMPLETE.')
  end subroutine check_projected_positivity

  subroutine compare_table_except_leakage(left,right,owner)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: owner
    character(len=72) :: file_name,my_name
    character(len=12) :: name,first
    logical :: empty_left,empty_right,is_lcm
    integer :: length_left,length_right,type_left,type_right

    call LCMINF(left,file_name,my_name,empty_left,length_left,is_lcm)
    call LCMINF(right,file_name,my_name,empty_right,length_right,is_lcm)
    if (empty_left .neqv. empty_right) &
      call fail(trim(owner)//' TABLE EMPTINESS DIFFERS.')
    if (empty_left) return
    if (count_table_records(left) /= count_table_records(right)) &
      call fail(trim(owner)//' TABLE INVENTORY COUNT DIFFERS.')
    name=' '
    call LCMNXT(left,name)
    first=name
    do
      call LCMLEN(left,name,length_left,type_left)
      call LCMLEN(right,name,length_right,type_right)
      if ((length_left /= length_right).or.(type_left /= type_right)) &
        call fail(trim(owner)//' RECORD DIFFERS: '//trim(name))
      if (name /= 'SPOT-LEAK1D') &
        call compare_named_record(left,right,name,length_left,type_left,owner)
      call LCMNXT(left,name)
      if (name == first) exit
    enddo
  end subroutine compare_table_except_leakage

  recursive subroutine compare_table_exact(left,right,owner)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: owner
    character(len=72) :: file_name,my_name
    character(len=12) :: name,first
    logical :: empty_left,empty_right,is_lcm
    integer :: length_left,length_right,type_left,type_right
    integer :: count_left,count_right

    call LCMINF(left,file_name,my_name,empty_left,length_left,is_lcm)
    call LCMINF(right,file_name,my_name,empty_right,length_right,is_lcm)
    if (empty_left .neqv. empty_right) &
      call fail(trim(owner)//' TABLE EMPTINESS DIFFERS.')
    if (empty_left) return
    count_left=count_table_records(left)
    count_right=count_table_records(right)
    if (count_left /= count_right) &
      call fail(trim(owner)//' TABLE INVENTORY COUNT DIFFERS.')
    name=' '
    call LCMNXT(left,name)
    first=name
    do
      call LCMLEN(left,name,length_left,type_left)
      call LCMLEN(right,name,length_right,type_right)
      if ((length_left /= length_right).or.(type_left /= type_right)) &
        call fail(trim(owner)//' RECORD DIFFERS: '//trim(name))
      call compare_named_record(left,right,name,length_left,type_left,owner)
      call LCMNXT(left,name)
      if (name == first) exit
    enddo
  end subroutine compare_table_exact

  integer function count_table_records(table)
    type(c_ptr), intent(in) :: table
    character(len=72) :: file_name
    character(len=12) :: my_name,name,first
    logical :: empty,is_lcm
    integer :: length_found

    call LCMINF(table,file_name,my_name,empty,length_found,is_lcm)
    if (empty) then
      count_table_records=0
      return
    endif
    count_table_records=0
    name=' '
    call LCMNXT(table,name)
    first=name
    do
      count_table_records=count_table_records+1
      call LCMNXT(table,name)
      if (name == first) exit
    enddo
  end function count_table_records

  recursive subroutine compare_named_record(left,right,name,length_found, &
      type_found,owner)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length_found,type_found
    type(c_ptr) :: child_left,child_right

    if (type_found == 0) then
      child_left=LCMGID(left,name)
      child_right=LCMGID(right,name)
      call compare_table_exact(child_left,child_right, &
        trim(owner)//'/'//trim(name))
    else if (type_found == 10) then
      child_left=LCMGID(left,name)
      child_right=LCMGID(right,name)
      call compare_list_exact(child_left,child_right,length_found, &
        trim(owner)//'/'//trim(name))
    else
      call compare_table_primitive(left,right,name,length_found,type_found, &
        trim(owner)//'/'//trim(name))
    endif
  end subroutine compare_named_record

  recursive subroutine compare_list_exact(left,right,list_length,owner)
    type(c_ptr), intent(in) :: left,right
    integer, intent(in) :: list_length
    character(len=*), intent(in) :: owner
    integer :: item,length_left,length_right,type_left,type_right
    type(c_ptr) :: child_left,child_right
    character(len=512) :: label

    do item=1,list_length
      call LCMLEL(left,item,length_left,type_left)
      call LCMLEL(right,item,length_right,type_right)
      if ((length_left /= length_right).or.(type_left /= type_right)) &
        call fail(trim(owner)//' LIST ITEM SHAPE DIFFERS.')
      write(label,'(A,A,I0)') trim(owner),'/',item
      if (type_left == 0) then
        child_left=LCMGIL(left,item)
        child_right=LCMGIL(right,item)
        call compare_table_exact(child_left,child_right,trim(label))
      else if (type_left == 10) then
        child_left=LCMGIL(left,item)
        child_right=LCMGIL(right,item)
        call compare_list_exact(child_left,child_right,length_left,trim(label))
      else if (length_left > 0) then
        call compare_list_primitive(left,right,item,length_left,type_left, &
          trim(label))
      endif
    enddo
  end subroutine compare_list_exact

  subroutine compare_table_primitive(left,right,name,n,type_code,owner)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: n,type_code
    integer, allocatable :: integer_left(:),integer_right(:)
    real(real32), allocatable :: real_left(:),real_right(:)
    real(real64), allocatable :: double_left(:),double_right(:)
    logical, allocatable :: logical_left(:),logical_right(:)
    complex(real32), allocatable :: complex_left(:),complex_right(:)

    select case(type_code)
    case(1,3)
      allocate(integer_left(n),integer_right(n))
      call LCMGET(left,name,integer_left)
      call LCMGET(right,name,integer_right)
      if (any(integer_left /= integer_right)) &
        call fail(trim(owner)//' INTEGER/CHARACTER BITS DIFFER.')
      deallocate(integer_right,integer_left)
    case(2)
      allocate(real_left(n),real_right(n))
      call LCMGET(left,name,real_left)
      call LCMGET(right,name,real_right)
      if (any(real32_bits(real_left) /= real32_bits(real_right))) &
        call fail(trim(owner)//' REAL32 BITS DIFFER.')
      deallocate(real_right,real_left)
    case(4)
      allocate(double_left(n),double_right(n))
      call LCMGET(left,name,double_left)
      call LCMGET(right,name,double_right)
      if (any(real64_bits(double_left) /= real64_bits(double_right))) &
        call fail(trim(owner)//' REAL64 BITS DIFFER.')
      deallocate(double_right,double_left)
    case(5)
      allocate(logical_left(n),logical_right(n))
      call LCMGET(left,name,logical_left)
      call LCMGET(right,name,logical_right)
      if (any(logical_left .neqv. logical_right)) &
        call fail(trim(owner)//' LOGICAL VALUES DIFFER.')
      deallocate(logical_right,logical_left)
    case(6)
      allocate(complex_left(n),complex_right(n))
      call LCMGET(left,name,complex_left)
      call LCMGET(right,name,complex_right)
      if (any(complex32_bits(complex_left) /= &
              complex32_bits(complex_right))) &
        call fail(trim(owner)//' COMPLEX BITS DIFFER.')
      deallocate(complex_right,complex_left)
    case default
      call fail(trim(owner)//' UNSUPPORTED LCM TYPE.')
    end select
  end subroutine compare_table_primitive

  subroutine compare_list_primitive(left,right,item,n,type_code,owner)
    type(c_ptr), intent(in) :: left,right
    integer, intent(in) :: item,n,type_code
    character(len=*), intent(in) :: owner
    integer, allocatable :: integer_left(:),integer_right(:)
    real(real32), allocatable :: real_left(:),real_right(:)
    real(real64), allocatable :: double_left(:),double_right(:)
    logical, allocatable :: logical_left(:),logical_right(:)
    complex(real32), allocatable :: complex_left(:),complex_right(:)

    select case(type_code)
    case(1,3)
      allocate(integer_left(n),integer_right(n))
      call LCMGDL(left,item,integer_left)
      call LCMGDL(right,item,integer_right)
      if (any(integer_left /= integer_right)) &
        call fail(trim(owner)//' INTEGER/CHARACTER BITS DIFFER.')
      deallocate(integer_right,integer_left)
    case(2)
      allocate(real_left(n),real_right(n))
      call LCMGDL(left,item,real_left)
      call LCMGDL(right,item,real_right)
      if (any(real32_bits(real_left) /= real32_bits(real_right))) &
        call fail(trim(owner)//' REAL32 BITS DIFFER.')
      deallocate(real_right,real_left)
    case(4)
      allocate(double_left(n),double_right(n))
      call LCMGDL(left,item,double_left)
      call LCMGDL(right,item,double_right)
      if (any(real64_bits(double_left) /= real64_bits(double_right))) &
        call fail(trim(owner)//' REAL64 BITS DIFFER.')
      deallocate(double_right,double_left)
    case(5)
      allocate(logical_left(n),logical_right(n))
      call LCMGDL(left,item,logical_left)
      call LCMGDL(right,item,logical_right)
      if (any(logical_left .neqv. logical_right)) &
        call fail(trim(owner)//' LOGICAL VALUES DIFFER.')
      deallocate(logical_right,logical_left)
    case(6)
      allocate(complex_left(n),complex_right(n))
      call LCMGDL(left,item,complex_left)
      call LCMGDL(right,item,complex_right)
      if (any(complex32_bits(complex_left) /= &
              complex32_bits(complex_right))) &
        call fail(trim(owner)//' COMPLEX BITS DIFFER.')
      deallocate(complex_right,complex_left)
    case default
      call fail(trim(owner)//' UNSUPPORTED LCM LIST TYPE.')
    end select
  end subroutine compare_list_primitive

  subroutine require_record(ptr,name,length_expected,type_expected,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length_expected,type_expected
    integer :: length_found,type_found

    call LCMLEN(ptr,name,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) &
      call fail(trim(owner)//' INVALID RECORD '//trim(name)//'.')
  end subroutine require_record

  subroutine require_absent(ptr,name,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,owner
    integer :: length_found,type_found

    call LCMLEN(ptr,name,length_found,type_found)
    if (length_found /= 0) &
      call fail(trim(owner)//' STALE RECORD PRESENT: '//trim(name))
  end subroutine require_absent

  subroutine require_list_item(ptr,index,length_expected,type_expected,owner)
    type(c_ptr), intent(in) :: ptr
    integer, intent(in) :: index,length_expected,type_expected
    character(len=*), intent(in) :: owner
    integer :: length_found,type_found

    call LCMLEL(ptr,index,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) &
      call fail(trim(owner)//' INVALID LIST ITEM.')
  end subroutine require_list_item

  pure elemental integer(int32) function real32_bits(value)
    real(real32), intent(in) :: value

    real32_bits=transfer(value,0_int32)
  end function real32_bits

  pure elemental integer(int64) function real64_bits(value)
    real(real64), intent(in) :: value

    real64_bits=transfer(value,0_int64)
  end function real64_bits

  pure function complex32_bits(value) result(bits)
    complex(real32), intent(in) :: value(:)
    integer(int32) :: bits(2*size(value))

    bits=transfer(value,bits)
  end function complex32_bits

  subroutine write_real64_metric(label,value)
    character(len=*), intent(in) :: label
    real(real64), intent(in) :: value

    write(6,'(A,1X,ES24.16E3,1X,Z16.16)') trim(label),value, &
      real64_bits(value)
  end subroutine write_real64_metric

  subroutine write_real32_metric(label,value)
    character(len=*), intent(in) :: label
    real(real32), intent(in) :: value

    write(6,'(A,1X,ES16.8E3,1X,Z8.8)') trim(label),value, &
      real32_bits(value)
  end subroutine write_real32_metric

  subroutine fail(message)
    character(len=*), intent(in) :: message

    write(0,'(A)') 'RANK2-MODAL-AA1 CANDIDATE CHECK FAIL: '//trim(message)
    error stop 1
  end subroutine fail

end program check_rank2_modal_aa1_candidate
