program build_rank2_modal_aa1_candidate
  ! Materialize one rank-two modal-projected Anderson proposal without
  ! assembly, transport, or a nonlinear-map evaluation.
  !
  !   --consecutive-current qs v w w_snap out_ax out_snap
  !   --consecutive-current-aa2-picard q p z z_snap out_ax out_snap
  !   --consecutive-qvwx-zplus-screened y z zp zp_snap out_ax out_snap
  !   --consecutive-returned-screened z r s s_snap out_ax out_snap
  !   --consecutive-ptu-screened p t u u_snap out_ax out_snap
  !   --current-qpzst-aa2 q p p z s t t_snap out_ax out_snap
  !   --current-stuvvw-aa2 s t u v v w w_snap out_ax out_snap
  !   --current-uvvwxy-aa2 u v v w x y y_snap out_ax out_snap
  !   --current-ptuqv-aa2 p t t u q v v_snap out_ax out_snap
  !   --current-cefg-aa2 c e e f q g g_snap out_ax out_snap
  !   --current-ghi-aa2 q1 g q2 h q3 i i_snap out_ax out_snap
  !   --next-x4aa2-screened q v w x x_snap out_ax out_snap
  !   --next-aa1aa2-screened q1 g q2 h h_snap out_ax out_snap
  !   --next-zpcd-screened z zp c d d_snap out_ax out_snap
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  implicit none

  integer, parameter :: nstate=40,max_path=72

  type :: canonical_state
    type(c_ptr) :: root
    integer :: state(nstate)=0
    integer :: dims(4)=0
    integer :: fixb=-1
    integer, allocatable :: rank(:),offset(:),gram_offset(:),basis_offset(:)
    real(real32), allocatable :: basis(:)
    real(real64), allocatable :: coordinates(:),leakage(:),height(:),gram(:)
    real(real64), allocatable :: offspace(:)
    real(real32) :: keff=0.0_real32
    real(real64) :: rho=0.0_real64,norm=0.0_real64,gram_error=0.0_real64
    character(len=12) :: norm_id='',basis_type=''
  end type canonical_state

  character(len=1024) :: path(6)
  character(len=24) :: report_prefix
  character(len=40) :: mode
  character(len=12) :: marker,carrier_marker
  character(len=2) :: previous_output,latest_output
  type(canonical_state) :: x0,x1,x2
  type(c_ptr) :: snap2,staged_ax,staged_snap,out_ax,out_snap,fluxes,plane
  integer :: i,igr,isnap,a,b,nmode,nreg2d,argument_offset
  integer :: index_a,index_b,index_g,index_l
  real(real64) :: update_sq(2),update_dot,denominator,beta,weight1
  real(real64) :: modal_affine_sq,modal_affine_norm,modal_current_norm
  real(real64) :: leakage_sq(2),leakage_dot,leakage_affine_sq
  real(real64) :: leakage_affine_norm,leakage_current_norm
  real(real64) :: leakage_affine_d,leakage_current_d
  real(real64) :: leakage_delta01,leakage_delta12
  real(real64) :: delta01_a,delta01_b,delta12_a,delta12_b
  real(real64) :: rho_star,rho_public,l_roundtrip,reconstructed
  real(real64) :: min_reconstructed,iter_keff
  real(real32) :: keff_public,projected
  real(real64), allocatable :: candidate_a(:),candidate_l(:)
  real(real32), allocatable :: published_l(:)
  logical :: consecutive_mode,consecutive_returned_mode
  logical :: consecutive_current_mode
  logical :: consecutive_current_aa2_picard_mode
  logical :: consecutive_qvwx_zplus_screened_mode
  logical :: consecutive_returned_screened_mode
  logical :: consecutive_ptu_screened_mode

  consecutive_mode=.false.
  consecutive_returned_mode=.false.
  consecutive_current_mode=.false.
  consecutive_current_aa2_picard_mode=.false.
  consecutive_qvwx_zplus_screened_mode=.false.
  consecutive_returned_screened_mode=.false.
  consecutive_ptu_screened_mode=.false.
  argument_offset=0
  if (command_argument_count() == 10) then
    call get_command_argument(1,mode)
    if (trim(mode) == '--rolling-aa2') then
      call build_rolling_aa2_candidate(.false.,.false.)
    else if (trim(mode) == '--rolling-aa2-next') then
      call build_rolling_aa2_candidate(.true.,.false.)
    else if (trim(mode) == '--current-aa2') then
      call build_rolling_aa2_candidate(.false.,.true.)
    else if (trim(mode) == '--current-qpzst-aa2') then
      call build_rolling_aa2_candidate(.false.,.false.,.true.)
    else if (trim(mode) == '--current-stuvvw-aa2') then
      call build_rolling_aa2_candidate(.false.,.false.,.false.,.true.)
    else if (trim(mode) == '--current-uvvwxy-aa2') then
      call build_rolling_aa2_candidate(.false.,.false.,.false.,.false., &
        .true.)
    else if (trim(mode) == '--current-ptuqv-aa2') then
      call build_rolling_aa2_candidate(.false.,.false.,.false.,.false., &
        .false.,.true.)
    else if (trim(mode) == '--current-cefg-aa2') then
      call build_rolling_aa2_candidate(.false.,.false.,.false.,.false., &
        .false.,.false.,.true.)
    else if (trim(mode) == '--current-ghi-aa2') then
      call build_rolling_aa2_candidate(.false.,.false.,.false.,.false., &
        .false.,.false.,.true.)
    else
      error stop 'ten-argument mode requires an AA2 mode'
    endif
    stop
  else if (command_argument_count() == 8) then
    call get_command_argument(1,mode)
    if (trim(mode) == '--next') then
      call build_next_candidate(.false.,.false.,.false.,.false.,.false.,.false.,.false.)
    else if (trim(mode) == '--next-x4') then
      call build_next_candidate(.false.,.false.,.false.,.false.,.true.,.false.,.false.)
    else if (trim(mode) == '--next-x4z') then
      call build_next_candidate(.false.,.false.,.false.,.false.,.false.,.true.,.false.)
    else if (trim(mode) == '--next-zu') then
      call build_next_candidate(.false.,.false.,.false.,.false.,.false.,.false.,.true.)
    else if (trim(mode) == '--next-x4aa2-screened') then
      call build_next_candidate(.false.,.false.,.false.,.false.,.false., &
        .false.,.false.,.true.)
    else if (trim(mode) == '--next-aa1aa2-screened') then
      call build_next_candidate(.false.,.false.,.false.,.false.,.false., &
        .false.,.false.,.true.)
    else if (trim(mode) == '--next-zpcd-screened') then
      call build_next_candidate(.false.,.false.,.false.,.false.,.false., &
        .false.,.false.,.true.)
    else if (trim(mode) == '--u') then
      call build_next_candidate(.true.,.false.,.false.,.false.,.false.,.false.,.false.)
    else if (trim(mode) == '--post-aa1') then
      call build_next_candidate(.false.,.true.,.false.,.false.,.false.,.false.,.false.)
    else if (trim(mode) == '--rolling-aa1') then
      call build_next_candidate(.false.,.false.,.true.,.false.,.false.,.false.,.false.)
    else if (trim(mode) == '--rolling-aa1-next') then
      call build_next_candidate(.false.,.false.,.false.,.true.,.false.,.false.,.false.)
    else
      error stop 'eight-argument mode requires --next, --next-x4, '// &
        '--next-x4z, --next-zu, --next-x4aa2-screened, '// &
        '--next-aa1aa2-screened, '// &
        '--next-zpcd-screened, --u, '// &
        '--post-aa1, --rolling-aa1 or --rolling-aa1-next'
    endif
    stop
  else if (command_argument_count() == 7) then
    call get_command_argument(1,mode)
    if (trim(mode) == '--consecutive') then
      consecutive_mode=.true.
    else if (trim(mode) == '--consecutive-returned') then
      consecutive_mode=.true.
      consecutive_returned_mode=.true.
    else if (trim(mode) == '--consecutive-returned-screened') then
      consecutive_mode=.true.
      consecutive_returned_mode=.true.
      consecutive_returned_screened_mode=.true.
    else if (trim(mode) == '--consecutive-ptu-screened') then
      consecutive_mode=.true.
      consecutive_ptu_screened_mode=.true.
    else if (trim(mode) == '--consecutive-current') then
      consecutive_mode=.true.
      consecutive_current_mode=.true.
    else if (trim(mode) == '--consecutive-current-aa2-picard') then
      consecutive_mode=.true.
      consecutive_current_aa2_picard_mode=.true.
    else if (trim(mode) == '--consecutive-qvwx-zplus-screened') then
      consecutive_mode=.true.
      consecutive_qvwx_zplus_screened_mode=.true.
    else
      error stop 'seven-argument mode requires a consecutive mode'
    endif
    argument_offset=1
  else if (command_argument_count() /= 6) then
    error stop 'expected x0 x1 x2 x2_snap out_ax out_snap or '// &
      '--next x1 x2 y z z_snap out_ax out_snap or '// &
      '--next-x4 x3 x4 qy z z_snap out_ax out_snap or '// &
      '--next-x4z qy z qt u u_snap out_ax out_snap or '// &
      '--next-zu qt u qs v v_snap out_ax out_snap or '// &
      '--next-x4aa2-screened q v w x x_snap out_ax out_snap or '// &
      '--next-aa1aa2-screened q1 g q2 h h_snap out_ax out_snap or '// &
      '--next-zpcd-screened z zp c d d_snap out_ax out_snap or '// &
      '--u y z w v v_snap out_ax out_snap or '// &
      '--post-aa1 x2 x3 aa1 aa1p aa1p_snap out_ax out_snap or '// &
      '--rolling-aa1 aa1 aa1p xnext xnextp xnextp_snap '// &
      'out_ax out_snap or '// &
      '--rolling-aa1-next xnext xnextp xroll xrollp xrollp_snap '// &
      'out_ax out_snap or '// &
      '--rolling-aa2 x0 x0p x1 x1p x2 x2p x2p_snap '// &
      'out_ax out_snap or '// &
      '--rolling-aa2-next x0 x0p x1 x1p x2 x2p x2p_snap '// &
      'out_ax out_snap or '// &
      '--current-aa2 w x c d y e e_snap '// &
      'out_ax out_snap or '// &
      '--current-qpzst-aa2 q p p z s t t_snap '// &
      'out_ax out_snap or '// &
      '--current-stuvvw-aa2 s t u v v w w_snap '// &
      'out_ax out_snap or '// &
      '--current-uvvwxy-aa2 u v v w x y y_snap '// &
      'out_ax out_snap or '// &
      '--current-cefg-aa2 c e e f q g g_snap '// &
      'out_ax out_snap or '// &
      '--current-ghi-aa2 q1 g q2 h q3 i i_snap '// &
      'out_ax out_snap or '// &
      '--consecutive x1_pub x2 x3 x3_snap out_ax out_snap or '// &
      '--consecutive-returned x2 x3 x4 x4_snap out_ax out_snap or '// &
      '--consecutive-current qs v w w_snap out_ax out_snap or '// &
      '--consecutive-current-aa2-picard q p z z_snap out_ax out_snap or '// &
      '--consecutive-qvwx-zplus-screened y z zp zp_snap out_ax out_snap'
  endif
  do i=1,6
    call get_command_argument(i+argument_offset,path(i))
    if ((len_trim(path(i)) == 0).or.(len_trim(path(i)) > max_path)) &
      error stop 'XSM path is empty or exceeds GANLIB limit'
  enddo
  if (trim(path(5)) == trim(path(6))) &
    error stop 'candidate AX and snapshot paths must differ'
  call require_fresh_path(path(5))
  call require_fresh_path(path(6))

  report_prefix='RANK2-MODAL-AA1'
  previous_output='X1'
  latest_output='X2'
  carrier_marker='X2-RAW-FLUX'
  if (consecutive_qvwx_zplus_screened_mode) then
    report_prefix='RANK2-QVWX-ZPLUS-AA1'
    previous_output='Z'
    latest_output='ZP'
    carrier_marker='AA1-RAW-FLUX'
    call load_state(trim(path(1)),x0,'y AA1 proposal',.true., &
      'AA1-RAW-FLUX')
  else if (consecutive_current_aa2_picard_mode) then
    report_prefix='RANK2-AA2-PICARD-AA1'
    previous_output='P'
    latest_output='Z'
    carrier_marker='Z-RAW-FLUX'
    call load_state(trim(path(1)),x0,'qAA2 proposal',.true., &
      'AA2-RAW-FLUX')
  else if (consecutive_ptu_screened_mode) then
    report_prefix='RANK2-CURRENT-PTU-AA1'
    previous_output='T'
    latest_output='U'
    carrier_marker='X4-RAW-FLUX'
    call load_state(trim(path(1)),x0,'p proposal',.true.,'X4-RAW-FLUX')
  else if (consecutive_current_mode) then
    report_prefix='RANK2-QSVW-AA1'
    previous_output='V'
    latest_output='W'
    carrier_marker='X4-RAW-FLUX'
    call load_state(trim(path(1)),x0,'qs proposal',.true.,'U-RAW-FLUX')
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
    carrier_marker='X4-RAW-FLUX'
    call load_state(trim(path(1)),x0,'x2 returned')
  else if (consecutive_mode) then
    report_prefix='RANK2-CONSECUTIVE-AA1'
    previous_output='X2'
    latest_output='X3'
    carrier_marker='X3-RAW-FLUX'
    call load_state(trim(path(1)),x0,'x1 proposal',.true.,'V-RAW-FLUX')
  else
    call load_state(trim(path(1)),x0,'x0')
  endif
  call load_state(trim(path(2)),x1,'x1')
  call load_state(trim(path(3)),x2,'x2')
  call compare_fixed_space(x0,x1,'x0/x1')
  call compare_fixed_space(x1,x2,'x1/x2')
  call validate_snapshot(trim(path(4)),x1,x2,snap2)

  ! Reproduce the full Gram-height arithmetic of the frozen direction audit.
  update_sq=0.0_real64
  update_dot=0.0_real64
  do igr=1,x0%dims(2)
    nmode=x0%rank(igr)
    do isnap=1,x0%dims(3)
      do a=1,nmode
        index_a=x0%offset(igr)+(isnap-1)*nmode+a
        delta01_a=x1%coordinates(index_a)-x0%coordinates(index_a)
        delta12_a=x2%coordinates(index_a)-x1%coordinates(index_a)
        do b=1,nmode
          index_b=x0%offset(igr)+(isnap-1)*nmode+b
          index_g=x0%gram_offset(igr)+(b-1)*nmode+a
          delta01_b=x1%coordinates(index_b)-x0%coordinates(index_b)
          delta12_b=x2%coordinates(index_b)-x1%coordinates(index_b)
          update_sq(1)=update_sq(1)+x0%height(isnap)*delta01_a* &
            x0%gram(index_g)*delta01_b
          update_sq(2)=update_sq(2)+x0%height(isnap)*delta12_a* &
            x0%gram(index_g)*delta12_b
          update_dot=update_dot+x0%height(isnap)*delta01_a* &
            x0%gram(index_g)*delta12_b
        enddo
      enddo
    enddo
  enddo
  if (any(.not.ieee_is_finite(update_sq)).or. &
      any(update_sq <= 0.0_real64).or. &
      (.not.ieee_is_finite(update_dot))) &
    error stop 'invalid modal update geometry'
  denominator=update_sq(1)+update_sq(2)-2.0_real64*update_dot
  if ((.not.ieee_is_finite(denominator)).or. &
      (denominator <= 0.0_real64)) &
    error stop 'singular modal Anderson scalar system'
  beta=(update_sq(1)-update_dot)/denominator
  weight1=1.0_real64-beta
  if ((.not.ieee_is_finite(beta)).or.(.not.ieee_is_finite(weight1))) &
    error stop 'nonfinite modal Anderson weight'
  if (consecutive_current_aa2_picard_mode.or. &
      consecutive_qvwx_zplus_screened_mode.or. &
      consecutive_returned_screened_mode.or. &
      consecutive_ptu_screened_mode) then
    modal_affine_sq=weight1**2*update_sq(1)+beta**2*update_sq(2)+ &
      2.0_real64*weight1*beta*update_dot
    if ((.not.ieee_is_finite(modal_affine_sq)).or. &
        (modal_affine_sq < 0.0_real64)) then
      if (consecutive_current_aa2_picard_mode) then
        error stop 'invalid AA2-Picard modal Anderson screen'
      else
        error stop 'invalid screened returned modal Anderson screen'
      endif
    endif
    modal_affine_norm=sqrt(modal_affine_sq)
    modal_current_norm=sqrt(update_sq(2))
  endif

  if (consecutive_current_mode.or. &
      consecutive_current_aa2_picard_mode.or. &
      consecutive_qvwx_zplus_screened_mode.or. &
      consecutive_returned_screened_mode.or. &
      consecutive_ptu_screened_mode) then
    leakage_sq=0.0_real64
    leakage_dot=0.0_real64
    leakage_affine_d=0.0_real64
    do isnap=1,x0%dims(3)
      do igr=1,x0%dims(2)
        index_l=(isnap-1)*x0%dims(2)+igr
        leakage_delta01=x1%leakage(index_l)-x0%leakage(index_l)
        leakage_delta12=x2%leakage(index_l)-x1%leakage(index_l)
        leakage_sq(1)=leakage_sq(1)+x0%height(isnap)* &
          leakage_delta01**2
        leakage_sq(2)=leakage_sq(2)+x0%height(isnap)* &
          leakage_delta12**2
        leakage_dot=leakage_dot+x0%height(isnap)* &
          leakage_delta01*leakage_delta12
        leakage_affine_d=max(leakage_affine_d, &
          abs(weight1*leakage_delta01+beta*leakage_delta12))
      enddo
    enddo
    leakage_affine_sq=weight1**2*leakage_sq(1)+ &
      beta**2*leakage_sq(2)+2.0_real64*weight1*beta*leakage_dot
    leakage_current_d=maxval(abs(x2%leakage-x1%leakage))
    if (any(.not.ieee_is_finite(leakage_sq)).or. &
        any(leakage_sq <= 0.0_real64).or. &
        (.not.ieee_is_finite(leakage_dot)).or. &
        (.not.ieee_is_finite(leakage_affine_sq)).or. &
        (leakage_affine_sq < 0.0_real64).or. &
        (.not.ieee_is_finite(leakage_affine_d)).or. &
        (.not.ieee_is_finite(leakage_current_d)).or. &
        (leakage_current_d <= 0.0_real64)) &
      error stop 'invalid current leakage Anderson screen'
    leakage_current_norm=sqrt(leakage_sq(2))
    leakage_affine_norm=sqrt(leakage_affine_sq)
    if (consecutive_current_aa2_picard_mode.or. &
        consecutive_qvwx_zplus_screened_mode.or. &
        consecutive_returned_screened_mode.or. &
        consecutive_ptu_screened_mode) then
      if ((modal_affine_norm >= modal_current_norm).or. &
          (leakage_affine_norm >= leakage_current_norm).or. &
          (leakage_affine_d >= leakage_current_d)) then
        if (consecutive_current_aa2_picard_mode) then
          error stop 'AA2-Picard parameter-free direction gate failed'
        else
          error stop 'screened returned parameter-free direction gate failed'
        endif
      endif
    endif
  endif

  allocate(candidate_a(size(x1%coordinates)))
  allocate(candidate_l(size(x1%leakage)),published_l(size(x1%leakage)))
  candidate_a=weight1*x1%coordinates+beta*x2%coordinates
  candidate_l=weight1*x1%leakage+beta*x2%leakage
  published_l=real(candidate_l,real32)
  rho_star=weight1*x1%rho+beta*x2%rho
  if ((.not.ieee_is_finite(rho_star)).or.(rho_star <= 0.0_real64)) &
    error stop 'invalid affine inverse eigenvalue'
  keff_public=real(1.0_real64/rho_star,real32)
  if ((.not.ieee_is_finite(keff_public)).or. &
      (keff_public <= 0.0_real32)) &
    error stop 'invalid published effective eigenvalue'
  rho_public=1.0_real64/real(keff_public,real64)
  if (any(.not.ieee_is_finite(candidate_a)).or. &
      any(.not.ieee_is_finite(candidate_l)).or. &
      any(.not.ieee_is_finite(published_l)).or. &
      (.not.ieee_is_finite(rho_public)).or.(rho_public <= 0.0_real64)) &
    error stop 'nonfinite published proposal'
  l_roundtrip=maxval(abs(real(published_l,real64)-candidate_l))

  ! Reproduce SPOPROJ FIXB's B*a accumulation and final binary32 cast.
  min_reconstructed=huge(min_reconstructed)
  do igr=1,x2%dims(2)
    nmode=x2%rank(igr)
    nreg2d=(x2%basis_offset(igr+1)-x2%basis_offset(igr))/nmode
    do isnap=1,x2%dims(3)
      do i=1,nreg2d
        reconstructed=0.0_real64
        do a=1,nmode
          index_a=x2%offset(igr)+(isnap-1)*nmode+a
          index_b=x2%basis_offset(igr)+(a-1)*nreg2d+i
          reconstructed=reconstructed+ &
            real(x2%basis(index_b),real64)*candidate_a(index_a)
        enddo
        projected=real(reconstructed,real32)
        if ((.not.ieee_is_finite(projected)).or. &
            (projected <= 0.0_real32)) &
          error stop 'published reconstructed flux is not strictly positive'
        min_reconstructed=min(min_reconstructed,real(projected,real64))
      enddo
    enddo
  enddo

  ! AX is an explicitly labelled latest-returned raw-flux carrier.  Only the
  ! outer state (A,rho,L) and its binary32 effective eigenvalue are replaced.
  call LCMOP(staged_ax,' ',0,1,0)
  call LCMEQU(x2%root,staged_ax)
  call LCMPUT(staged_ax,'SPOT-X-A',size(candidate_a),4,candidate_a)
  call LCMPUT(staged_ax,'K-EFFECTIVE',1,2,keff_public)
  call LCMPUT(staged_ax,'SPOT-X-RHO',1,4,rho_public)
  call LCMPUT(staged_ax,'SPOT-X-L',size(published_l),4, &
    real(published_l,real64))
  call delete_if_present(staged_ax,'SPOT-X-RRHO')
  call delete_if_present(staged_ax,'SPOT-X-RLEAK')
  call delete_if_present(staged_ax,'SPOT-X-DLEAK')
  call delete_if_present(staged_ax,'SPOT-X-RA')
  call delete_if_present(staged_ax,'SPOT-X-PERP')
  call delete_if_present(staged_ax,'SPOT-X-EPOCH')
  call delete_if_present(staged_ax,'SPOT-GBAL')
  ! The physical GANLIB key is the 12-character truncation of the logical
  ! diagnostic name SPOT-GBAL-MAX.
  call delete_if_present(staged_ax,'SPOT-GBAL-MA')
  marker='PROPOSAL'
  call LCMPTC(staged_ax,'SPOT-X-STATE',12,marker)
  marker=carrier_marker
  call LCMPTC(staged_ax,'SPOT-X-CARR',12,marker)
  call LCMOP(out_ax,trim(path(5)),0,2,0)
  call LCMEQU(staged_ax,out_ax)
  call LCMCL(out_ax,1)
  call LCMCL(staged_ax,2)

  ! The latest returned archive remains a carrier.  Publish only the root k
  ! identity and FLUX leakage; preserve the actual lagged SYSTEM history.
  call LCMOP(staged_snap,' ',0,1,0)
  call LCMEQU(snap2,staged_snap)
  iter_keff=real(keff_public,real64)
  call LCMPUT(staged_snap,'SPOT-ITER-K',1,4,iter_keff)
  call delete_if_present(staged_snap,'SPOT-L1-ERR')
  call delete_if_present(staged_snap,'SPOT-PJ-PERP')
  call delete_if_present(staged_snap,'SPOT-PROJECT')
  fluxes=LCMGID(staged_snap,'FLUX')
  do isnap=1,x2%dims(3)
    plane=LCMGIL(fluxes,isnap)
    index_l=(isnap-1)*x2%dims(2)+1
    call LCMPUT(plane,'SPOT-LEAK1D',x2%dims(2),2, &
      published_l(index_l:index_l+x2%dims(2)-1))
  enddo

  call LCMOP(out_snap,trim(path(6)),0,2,0)
  call LCMEQU(staged_snap,out_snap)
  call LCMCL(out_snap,1)
  call LCMCL(staged_snap,2)
  call LCMCL(snap2,1)
  call LCMCL(x2%root,1)
  call LCMCL(x1%root,1)
  call LCMCL(x0%root,1)

  write(*,'(A,ES24.16)') trim(report_prefix)//' BETA-WEIGHT-'// &
    latest_output//' ',beta
  write(*,'(A,ES24.16)') trim(report_prefix)//' WEIGHT-'// &
    previous_output//' ',weight1
  write(*,'(A,ES24.16)') trim(report_prefix)//' DENOMINATOR ',denominator
  write(*,'(A,ES24.16)') trim(report_prefix)//' RHO-AFFINE ',rho_star
  write(*,'(A,ES24.16)') trim(report_prefix)//' K-PUBLISHED ', &
    real(keff_public,real64)
  write(*,'(A,ES24.16)') trim(report_prefix)//' RHO-PUBLISHED ',rho_public
  write(*,'(A,ES24.16)') trim(report_prefix)//' RHO-Q-DELTA ', &
    rho_public-rho_star
  write(*,'(A,ES24.16)') trim(report_prefix)//' L-ROUNDTRIP-MAX ', &
    l_roundtrip
  write(*,'(A,ES24.16)') trim(report_prefix)//' MIN-PUBLISHED-BA ', &
    min_reconstructed
  if (consecutive_current_mode.or. &
      consecutive_current_aa2_picard_mode.or. &
      consecutive_qvwx_zplus_screened_mode.or. &
      consecutive_returned_screened_mode.or. &
      consecutive_ptu_screened_mode) then
    if (consecutive_current_aa2_picard_mode.or. &
        consecutive_qvwx_zplus_screened_mode.or. &
        consecutive_returned_screened_mode.or. &
        consecutive_ptu_screened_mode) then
      write(*,'(A,ES24.16)') trim(report_prefix)// &
        ' MODAL-AFFINE-L2/CURRENT ', &
        modal_affine_norm/modal_current_norm
    endif
    write(*,'(A,ES24.16)') trim(report_prefix)// &
      ' LEAKAGE-AFFINE-L2/CURRENT SAME-MODAL-BETA ', &
      leakage_affine_norm/leakage_current_norm
    write(*,'(A,ES24.16)') trim(report_prefix)// &
      ' LEAKAGE-AFFINE-DL/CURRENT SAME-MODAL-BETA ', &
      leakage_affine_d/leakage_current_d
    write(*,'(A)') trim(report_prefix)// &
      ' LEAKAGE SCREEN ONLY NO LEAKAGE FIT'
    if (consecutive_current_aa2_picard_mode.or. &
        consecutive_qvwx_zplus_screened_mode.or. &
        consecutive_returned_screened_mode.or. &
        consecutive_ptu_screened_mode) &
      write(*,'(A)') trim(report_prefix)// &
        ' PARAMETER-FREE DIRECTION GATE PASS'
  endif
  write(*,'(A)') trim(report_prefix)//' CARRIER '//trim(carrier_marker)
  write(*,'(A)') trim(report_prefix)// &
    ' PROPOSAL COMPLETE NOT-EVALUATED NO-DRAGON NO-MAP'

contains

  subroutine build_rolling_aa2_candidate(rolling_next_mode,current_mode, &
      current_qpzst_mode,current_stuvvw_mode,current_uvvwxy_mode, &
      current_ptuqv_mode,current_cefg_mode)
    logical, intent(in) :: rolling_next_mode,current_mode
    logical, intent(in), optional :: current_qpzst_mode
    logical, intent(in), optional :: current_stuvvw_mode
    logical, intent(in), optional :: current_uvvwxy_mode
    logical, intent(in), optional :: current_ptuqv_mode
    logical, intent(in), optional :: current_cefg_mode
    character(len=1024) :: aa2_path(9)
    type(canonical_state) :: in0,out0,in1,out1,in2,out2
    type(c_ptr) :: out2_snap,aa2_staged_ax,aa2_staged_snap
    type(c_ptr) :: aa2_out_ax,aa2_out_snap,aa2_fluxes,aa2_plane
    character(len=24) :: aa2_report_prefix
    character(len=12) :: aa2_marker,aa2_label0,aa2_label1,aa2_label2
    integer :: j,g,s,r,ia,ib,ig,il,nm,nr,positive_count
    real(real64) :: f0a,f0b,f1a,f1b,f2a,f2b
    real(real64) :: d0a,d0b,d1a,d1b,metric
    real(real64) :: h00,h01,h11,c0,c1,f2_sq,determinant
    real(real64) :: gamma0,gamma1,alpha0,alpha1,alpha2,predicted_sq
    real(real64) :: modal_predicted_norm,modal_current_norm
    real(real64) :: leakage_predicted_sq,leakage_current_sq
    real(real64) :: leakage_predicted_norm,leakage_current_norm
    real(real64) :: leakage_predicted_d,leakage_current_d
    real(real64) :: leakage_f0,leakage_f1,leakage_f2,leakage_affine
    real(real64) :: rho_affine,rho_public,l_roundtrip
    real(real64) :: reconstructed,min_reconstructed,iter_k
    real(real32) :: k_public,projected
    real(real64), allocatable :: candidate_a(:),candidate_l(:)
    real(real32), allocatable :: published_l(:)
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

    do j=1,9
      call get_command_argument(j+1,aa2_path(j))
      if ((len_trim(aa2_path(j)) == 0).or. &
          (len_trim(aa2_path(j)) > max_path)) &
        error stop 'AA2 XSM path is empty or exceeds GANLIB limit'
    enddo
    if (trim(aa2_path(8)) == trim(aa2_path(9))) &
      error stop 'AA2 candidate AX and snapshot paths must differ'
    if (qpzst_mode.and. &
        (trim(aa2_path(2)) /= trim(aa2_path(3)))) &
      error stop 'QPZST p output and p input must be the same path'
    if (stuvvw_mode.and. &
        (trim(aa2_path(4)) /= trim(aa2_path(5)))) &
      error stop 'STUVVW v output and v input must be the same path'
    if (uvvwxy_mode.and. &
        (trim(aa2_path(2)) /= trim(aa2_path(3)))) &
      error stop 'UVVWXY v output and v input must be the same path'
    if (ptuqv_mode.and. &
        (trim(aa2_path(2)) /= trim(aa2_path(3)))) &
      error stop 'PTUQV t output and t input must be the same path'
    if (cefg_mode.and.(trim(mode) == '--current-cefg-aa2').and. &
        (trim(aa2_path(2)) /= trim(aa2_path(3)))) &
      error stop 'CEFG e output and e input must be the same path'
    call require_fresh_path(aa2_path(8))
    call require_fresh_path(aa2_path(9))

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
      error stop 'AA2 modes are mutually exclusive'
    if (cefg_mode) then
      if (trim(mode) == '--current-ghi-aa2') then
        aa2_report_prefix='RANK2-CURRENT-GHI-AA2'
        aa2_label0='G'
        aa2_label1='H'
        aa2_label2='I'
        call load_state(trim(aa2_path(1)),in0,'GHI q1 input', &
          .true.,'AA1-RAW-FLUX')
        call load_state(trim(aa2_path(2)),out0,'GHI g output')
        call load_state(trim(aa2_path(3)),in1,'GHI q2 input', &
          .true.,'AA2-RAW-FLUX')
        call load_state(trim(aa2_path(4)),out1,'GHI h output')
        call load_state(trim(aa2_path(5)),in2,'GHI q3 input', &
          .true.,'AA1-RAW-FLUX')
        call load_state(trim(aa2_path(6)),out2,'GHI i output')
      else
        aa2_report_prefix='RANK2-CURRENT-CEFG-AA2'
        aa2_label0='E'
        aa2_label1='F'
        aa2_label2='G'
        call load_state(trim(aa2_path(1)),in0,'CEFG c input', &
          .true.,'AA1-RAW-FLUX')
        call load_state(trim(aa2_path(2)),out0,'CEFG e output')
        call load_state(trim(aa2_path(3)),in1,'CEFG e input')
        call load_state(trim(aa2_path(4)),out1,'CEFG f output')
        call load_state(trim(aa2_path(5)),in2,'CEFG q input', &
          .true.,'AA1-RAW-FLUX')
        call load_state(trim(aa2_path(6)),out2,'CEFG g output')
      endif
    else if (ptuqv_mode) then
      aa2_report_prefix='RANK2-CURRENT-PTUQV-AA2'
      aa2_label0='T'
      aa2_label1='U'
      aa2_label2='V'
      call load_state(trim(aa2_path(1)),in0,'PTUQV p input', &
        .true.,'X4-RAW-FLUX')
      call load_state(trim(aa2_path(2)),out0,'PTUQV t output')
      call load_state(trim(aa2_path(3)),in1,'PTUQV t input')
      call load_state(trim(aa2_path(4)),out1,'PTUQV u output')
      call load_state(trim(aa2_path(5)),in2,'PTUQV q input', &
        .true.,'X4-RAW-FLUX')
      call load_state(trim(aa2_path(6)),out2,'PTUQV v output')
    else if (uvvwxy_mode) then
      aa2_report_prefix='RANK2-CURRENT-UVVWXY-AA2'
      aa2_label0='V'
      aa2_label1='W'
      aa2_label2='Y'
      call load_state(trim(aa2_path(1)),in0,'UVVWXY u input', &
        .true.,'AA2-RAW-FLUX')
      call load_state(trim(aa2_path(2)),out0,'UVVWXY v output')
      call load_state(trim(aa2_path(3)),in1,'UVVWXY v input')
      call load_state(trim(aa2_path(4)),out1,'UVVWXY w output')
      call load_state(trim(aa2_path(5)),in2,'UVVWXY x input', &
        .true.,'AA2-RAW-FLUX')
      call load_state(trim(aa2_path(6)),out2,'UVVWXY y output')
    else if (stuvvw_mode) then
      aa2_report_prefix='RANK2-CURRENT-STUVVW-AA2'
      aa2_label0='T'
      aa2_label1='V'
      aa2_label2='W'
      call load_state(trim(aa2_path(1)),in0,'STUVVW s input', &
        .true.,'Z-RAW-FLUX')
      call load_state(trim(aa2_path(2)),out0,'STUVVW t output')
      call load_state(trim(aa2_path(3)),in1,'STUVVW u input', &
        .true.,'AA2-RAW-FLUX')
      call load_state(trim(aa2_path(4)),out1,'STUVVW v output')
      call load_state(trim(aa2_path(5)),in2,'STUVVW v input')
      call load_state(trim(aa2_path(6)),out2,'STUVVW w output')
    else if (qpzst_mode) then
      aa2_report_prefix='RANK2-CURRENT-QPZST-AA2'
      aa2_label0='P'
      aa2_label1='Z'
      aa2_label2='T'
      call load_state(trim(aa2_path(1)),in0,'QPZST q input', &
        .true.,'AA2-RAW-FLUX')
      call load_state(trim(aa2_path(2)),out0,'QPZST p output')
      call load_state(trim(aa2_path(3)),in1,'QPZST p input')
      call load_state(trim(aa2_path(4)),out1,'QPZST z output')
      call load_state(trim(aa2_path(5)),in2,'QPZST s input', &
        .true.,'Z-RAW-FLUX')
      call load_state(trim(aa2_path(6)),out2,'QPZST t output')
    else if (current_mode) then
      aa2_report_prefix='RANK2-CURRENT-AA2'
      aa2_label0='X'
      aa2_label1='D'
      aa2_label2='E'
      call load_state(trim(aa2_path(1)),in0,'current w input')
      call load_state(trim(aa2_path(2)),out0,'current x output')
      call load_state(trim(aa2_path(3)),in1,'current c input', &
        .true.,'X4-RAW-FLUX')
      call load_state(trim(aa2_path(4)),out1,'current d output')
      call load_state(trim(aa2_path(5)),in2,'current y input', &
        .true.,'Z-RAW-FLUX')
      call load_state(trim(aa2_path(6)),out2,'current e output')
    else if (rolling_next_mode) then
      aa2_report_prefix='RANK2-ROLLING-AA2-NEXT'
      aa2_label0='XROLL-PLUS'
      aa2_label1='XROLL2-PLUS'
      aa2_label2='XAA2-PLUS'
      call load_state(trim(aa2_path(1)),in0,'AA2-next xroll input', &
        .true.,'XNP-RAW-FLUX')
      call load_state(trim(aa2_path(2)),out0,'AA2-next xroll output')
      call load_state(trim(aa2_path(3)),in1,'AA2-next xroll2 input', &
        .true.,'XRP-RAW-FLUX')
      call load_state(trim(aa2_path(4)),out1,'AA2-next xroll2 output')
      call load_state(trim(aa2_path(5)),in2,'AA2-next xAA2 input', &
        .true.,'AA2-RAW-FLUX')
      call load_state(trim(aa2_path(6)),out2,'AA2-next xAA2 output')
    else
      aa2_report_prefix='RANK2-ROLLING-AA2'
      aa2_label0='XNEXT-PLUS'
      aa2_label1='XROLL-PLUS'
      aa2_label2='XROLL2-PLUS'
      call load_state(trim(aa2_path(1)),in0,'AA2 xnext input', &
        .true.,'AA1-RAW-FLUX')
      call load_state(trim(aa2_path(2)),out0,'AA2 xnext output')
      call load_state(trim(aa2_path(3)),in1,'AA2 xroll input', &
        .true.,'XNP-RAW-FLUX')
      call load_state(trim(aa2_path(4)),out1,'AA2 xroll output')
      call load_state(trim(aa2_path(5)),in2,'AA2 xroll2 input', &
        .true.,'XRP-RAW-FLUX')
      call load_state(trim(aa2_path(6)),out2,'AA2 xroll2 output')
    endif
    call compare_next_fixed_space(in0,out0,'AA2 in0/out0')
    call compare_next_fixed_space(in0,in1,'AA2 in0/in1')
    call compare_next_fixed_space(in0,out1,'AA2 in0/out1')
    call compare_next_fixed_space(in0,in2,'AA2 in0/in2')
    call compare_next_fixed_space(in0,out2,'AA2 in0/out2')
    call validate_snapshot(trim(aa2_path(7)),in2,out2,out2_snap)

    ! Standard constrained AA(2) in the unchanged Gram-height metric.
    ! d0=f0-f2 and d1=f1-f2; solve H*gamma=-c exactly as a 2x2
    ! system.  No condition threshold or fallback is used.
    h00=0.0_real64
    h01=0.0_real64
    h11=0.0_real64
    c0=0.0_real64
    c1=0.0_real64
    f2_sq=0.0_real64
    do g=1,in0%dims(2)
      nm=in0%rank(g)
      do s=1,in0%dims(3)
        do ia=1,nm
          il=in0%offset(g)+(s-1)*nm+ia
          f0a=out0%coordinates(il)-in0%coordinates(il)
          f1a=out1%coordinates(il)-in1%coordinates(il)
          f2a=out2%coordinates(il)-in2%coordinates(il)
          d0a=f0a-f2a
          d1a=f1a-f2a
          do ib=1,nm
            r=in0%offset(g)+(s-1)*nm+ib
            ig=in0%gram_offset(g)+(ib-1)*nm+ia
            f0b=out0%coordinates(r)-in0%coordinates(r)
            f1b=out1%coordinates(r)-in1%coordinates(r)
            f2b=out2%coordinates(r)-in2%coordinates(r)
            d0b=f0b-f2b
            d1b=f1b-f2b
            metric=in0%height(s)*in0%gram(ig)
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
      error stop 'invalid rolling AA2 modal geometry'
    determinant=h00*h11-h01*h01
    if ((.not.ieee_is_finite(determinant)).or. &
        (determinant <= 0.0_real64)) &
      error stop 'singular rolling AA2 system'
    gamma0=(h01*c1-h11*c0)/determinant
    gamma1=(h01*c0-h00*c1)/determinant
    alpha0=gamma0
    alpha1=gamma1
    alpha2=1.0_real64-gamma0-gamma1
    if ((.not.ieee_is_finite(alpha0)).or. &
        (.not.ieee_is_finite(alpha1)).or. &
        (.not.ieee_is_finite(alpha2))) &
      error stop 'nonfinite rolling AA2 weight'
    predicted_sq=f2_sq+2.0_real64*gamma0*c0+ &
      2.0_real64*gamma1*c1+gamma0*gamma0*h00+ &
      2.0_real64*gamma0*gamma1*h01+gamma1*gamma1*h11
    if ((.not.ieee_is_finite(predicted_sq)).or. &
        (predicted_sq < 0.0_real64)) &
      error stop 'invalid rolling AA2 predicted residual'

    if (direction_gate_mode) then
      if (f2_sq <= 0.0_real64) &
        error stop 'invalid current AA2 modal residual'
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
        error stop 'invalid current AA2 leakage direction screen'
      leakage_predicted_norm=sqrt(leakage_predicted_sq)
      leakage_current_norm=sqrt(leakage_current_sq)
      if ((modal_predicted_norm >= modal_current_norm).or. &
          (leakage_predicted_norm >= leakage_current_norm).or. &
          (leakage_predicted_d >= leakage_current_d)) &
        error stop 'current AA2 parameter-free direction gate failed'
    endif

    allocate(candidate_a(size(out2%coordinates)))
    allocate(candidate_l(size(out2%leakage)))
    allocate(published_l(size(out2%leakage)))
    candidate_a=alpha0*out0%coordinates+alpha1*out1%coordinates+ &
      alpha2*out2%coordinates
    candidate_l=alpha0*out0%leakage+alpha1*out1%leakage+ &
      alpha2*out2%leakage
    published_l=real(candidate_l,real32)
    rho_affine=alpha0*out0%rho+alpha1*out1%rho+alpha2*out2%rho
    if ((.not.ieee_is_finite(rho_affine)).or. &
        (rho_affine <= 0.0_real64)) &
      error stop 'invalid rolling AA2 affine inverse eigenvalue'
    k_public=real(1.0_real64/rho_affine,real32)
    if ((.not.ieee_is_finite(k_public)).or. &
        (k_public <= 0.0_real32)) &
      error stop 'invalid rolling AA2 published eigenvalue'
    rho_public=1.0_real64/real(k_public,real64)
    if (any(.not.ieee_is_finite(candidate_a)).or. &
        any(.not.ieee_is_finite(candidate_l)).or. &
        any(.not.ieee_is_finite(published_l)).or. &
        (.not.ieee_is_finite(rho_public)).or. &
        (rho_public <= 0.0_real64)) &
      error stop 'nonfinite rolling AA2 proposal'
    l_roundtrip=maxval(abs(real(published_l,real64)-candidate_l))

    min_reconstructed=huge(min_reconstructed)
    positive_count=0
    do g=1,out2%dims(2)
      nm=out2%rank(g)
      nr=(out2%basis_offset(g+1)-out2%basis_offset(g))/nm
      do s=1,out2%dims(3)
        do r=1,nr
          reconstructed=0.0_real64
          do ia=1,nm
            il=out2%offset(g)+(s-1)*nm+ia
            ib=out2%basis_offset(g)+(ia-1)*nr+r
            reconstructed=reconstructed+ &
              real(out2%basis(ib),real64)*candidate_a(il)
          enddo
          projected=real(reconstructed,real32)
          if ((.not.ieee_is_finite(reconstructed)).or. &
              (.not.ieee_is_finite(projected)).or. &
              (projected <= 0.0_real32)) &
            error stop 'rolling AA2 reconstructed flux is not positive'
          positive_count=positive_count+1
          min_reconstructed=min(min_reconstructed,real(projected,real64))
        enddo
      enddo
    enddo
    if (positive_count /= out2%dims(2)*out2%dims(3)*8) &
      error stop 'rolling AA2 reconstructed-flux census is incomplete'

    ! Carry the latest returned raw AX/snapshot payload without mixing it.
    call LCMOP(aa2_staged_ax,' ',0,1,0)
    call LCMEQU(out2%root,aa2_staged_ax)
    call LCMPUT(aa2_staged_ax,'SPOT-X-A',size(candidate_a),4,candidate_a)
    call LCMPUT(aa2_staged_ax,'K-EFFECTIVE',1,2,k_public)
    call LCMPUT(aa2_staged_ax,'SPOT-X-RHO',1,4,rho_public)
    call LCMPUT(aa2_staged_ax,'SPOT-X-L',size(published_l),4, &
      real(published_l,real64))
    call delete_if_present(aa2_staged_ax,'SPOT-X-RRHO')
    call delete_if_present(aa2_staged_ax,'SPOT-X-RLEAK')
    call delete_if_present(aa2_staged_ax,'SPOT-X-DLEAK')
    call delete_if_present(aa2_staged_ax,'SPOT-X-RA')
    call delete_if_present(aa2_staged_ax,'SPOT-X-PERP')
    call delete_if_present(aa2_staged_ax,'SPOT-X-EPOCH')
    call delete_if_present(aa2_staged_ax,'SPOT-GBAL')
    call delete_if_present(aa2_staged_ax,'SPOT-GBAL-MA')
    aa2_marker='PROPOSAL'
    call LCMPTC(aa2_staged_ax,'SPOT-X-STATE',12,aa2_marker)
    aa2_marker='AA2-RAW-FLUX'
    call LCMPTC(aa2_staged_ax,'SPOT-X-CARR',12,aa2_marker)
    call LCMOP(aa2_out_ax,trim(aa2_path(8)),0,2,0)
    call LCMEQU(aa2_staged_ax,aa2_out_ax)
    call LCMCL(aa2_out_ax,1)
    call LCMCL(aa2_staged_ax,2)

    call LCMOP(aa2_staged_snap,' ',0,1,0)
    call LCMEQU(out2_snap,aa2_staged_snap)
    iter_k=real(k_public,real64)
    call LCMPUT(aa2_staged_snap,'SPOT-ITER-K',1,4,iter_k)
    call delete_if_present(aa2_staged_snap,'SPOT-L1-ERR')
    call delete_if_present(aa2_staged_snap,'SPOT-PJ-PERP')
    call delete_if_present(aa2_staged_snap,'SPOT-PROJECT')
    aa2_fluxes=LCMGID(aa2_staged_snap,'FLUX')
    do s=1,out2%dims(3)
      aa2_plane=LCMGIL(aa2_fluxes,s)
      il=(s-1)*out2%dims(2)+1
      call LCMPUT(aa2_plane,'SPOT-LEAK1D',out2%dims(2),2, &
        published_l(il:il+out2%dims(2)-1))
    enddo
    call LCMOP(aa2_out_snap,trim(aa2_path(9)),0,2,0)
    call LCMEQU(aa2_staged_snap,aa2_out_snap)
    call LCMCL(aa2_out_snap,1)
    call LCMCL(aa2_staged_snap,2)

    call LCMCL(out2_snap,1)
    call LCMCL(out2%root,1)
    call LCMCL(in2%root,1)
    call LCMCL(out1%root,1)
    call LCMCL(in1%root,1)
    call LCMCL(out0%root,1)
    call LCMCL(in0%root,1)

    write(*,'(A,ES24.16)') trim(aa2_report_prefix)//' ALPHA-'// &
      trim(aa2_label0)//' ',alpha0
    write(*,'(A,ES24.16)') trim(aa2_report_prefix)//' ALPHA-'// &
      trim(aa2_label1)//' ',alpha1
    write(*,'(A,ES24.16)') trim(aa2_report_prefix)//' ALPHA-'// &
      trim(aa2_label2)//' ',alpha2
    write(*,'(A,ES24.16)') trim(aa2_report_prefix)//' H00 ',h00
    write(*,'(A,ES24.16)') trim(aa2_report_prefix)//' H01 ',h01
    write(*,'(A,ES24.16)') trim(aa2_report_prefix)//' H11 ',h11
    write(*,'(A,ES24.16)') trim(aa2_report_prefix)//' DETERMINANT ', &
      determinant
    write(*,'(A,ES24.16)') trim(aa2_report_prefix)// &
      ' PREDICTED-RESIDUAL-SQ ',predicted_sq
    write(*,'(A,ES24.16)') trim(aa2_report_prefix)//' RHO-AFFINE ', &
      rho_affine
    write(*,'(A,ES24.16)') trim(aa2_report_prefix)//' K-PUBLISHED ', &
      real(k_public,real64)
    write(*,'(A,ES24.16)') trim(aa2_report_prefix)//' RHO-PUBLISHED ', &
      rho_public
    write(*,'(A,ES24.16)') trim(aa2_report_prefix)//' RHO-Q-DELTA ', &
      rho_public-rho_affine
    write(*,'(A,ES24.16)') trim(aa2_report_prefix)// &
      ' L-ROUNDTRIP-MAX ', &
      l_roundtrip
    write(*,'(A,ES24.16)') trim(aa2_report_prefix)// &
      ' MIN-PUBLISHED-BA ', &
      min_reconstructed
    write(*,'(A,I0)') trim(aa2_report_prefix)//' POSITIVE-BA-POINTS ', &
      positive_count
    if (direction_gate_mode) then
      write(*,'(A,ES24.16)') trim(aa2_report_prefix)// &
        ' MODAL-AFFINE-L2/CURRENT ', &
        modal_predicted_norm/modal_current_norm
      write(*,'(A,ES24.16)') trim(aa2_report_prefix)// &
        ' LEAKAGE-AFFINE-L2/CURRENT SAME-MODAL-WEIGHTS ', &
        leakage_predicted_norm/leakage_current_norm
      write(*,'(A,ES24.16)') trim(aa2_report_prefix)// &
        ' LEAKAGE-AFFINE-DL/CURRENT SAME-MODAL-WEIGHTS ', &
        leakage_predicted_d/leakage_current_d
      write(*,'(A)') trim(aa2_report_prefix)// &
        ' LEAKAGE SCREEN ONLY NO LEAKAGE FIT'
      write(*,'(A)') trim(aa2_report_prefix)// &
        ' PARAMETER-FREE DIRECTION GATE PASS'
    endif
    write(*,'(A)') trim(aa2_report_prefix)//' CARRIER AA2-RAW-FLUX'
    write(*,'(A)') trim(aa2_report_prefix)//' CLASSIFICATION '// &
      'MATERIALIZED_PROPOSAL_NOT_EVALUATED NO-DRAGON NO-MAP'
  end subroutine build_rolling_aa2_candidate

  subroutine build_next_candidate(u_mode,post_aa1_mode,rolling_mode, &
      rolling_next_mode,x4_history_mode,x4z_history_mode,zu_history_mode, &
      x4aa2_screened_mode)
    logical, intent(in) :: u_mode,post_aa1_mode,rolling_mode
    logical, intent(in) :: rolling_next_mode,x4_history_mode
    logical, intent(in) :: x4z_history_mode,zu_history_mode
    logical, intent(in), optional :: x4aa2_screened_mode
    character(len=1024) :: next_path(7)
    character(len=24) :: report_prefix
    character(len=12) :: next_marker,input_carrier,output_carrier
    character(len=8) :: latest_output,previous_output
    type(canonical_state) :: next_x1,next_x2,next_y,next_z
    type(c_ptr) :: next_z_snap,next_staged_ax,next_staged_snap
    type(c_ptr) :: next_out_ax,next_out_snap,next_fluxes,next_plane
    integer :: j,g,s,r,ia,ib,ig,il,mode_count,region_count
    integer :: positive_count
    real(real64) :: p_sq,q_sq,p_dot,p_a,p_b,q_a,q_b
    real(real64) :: next_denominator,next_beta,next_weight_x2
    real(real64) :: next_modal_affine_sq,next_modal_affine_norm
    real(real64) :: next_modal_current_norm
    real(real64) :: next_leakage_affine_sq,next_leakage_affine_norm
    real(real64) :: next_leakage_current_sq,next_leakage_current_norm
    real(real64) :: next_leakage_affine_d,next_leakage_current_d
    real(real64) :: next_leakage_p,next_leakage_q,next_leakage_affine
    real(real64) :: next_rho_star,next_rho_public,next_l_roundtrip
    real(real64) :: next_reconstructed,next_min_reconstructed,next_iter_k
    real(real32) :: next_k_public,next_projected
    real(real64), allocatable :: next_candidate_a(:),next_candidate_l(:)
    real(real32), allocatable :: next_published_l(:)
    logical :: current_screened_mode

    current_screened_mode=.false.
    if (present(x4aa2_screened_mode)) &
      current_screened_mode=x4aa2_screened_mode

    do j=1,7
      call get_command_argument(j+1,next_path(j))
      if ((len_trim(next_path(j)) == 0).or. &
          (len_trim(next_path(j)) > max_path)) &
        error stop 'XSM path is empty or exceeds GANLIB limit'
    enddo
    if (trim(next_path(6)) == trim(next_path(7))) &
      error stop 'candidate AX and snapshot paths must differ'
    call require_fresh_path(next_path(6))
    call require_fresh_path(next_path(7))

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
      error stop 'next proposal modes are mutually exclusive'
    if (current_screened_mode) then
      if (trim(mode) == '--next-zpcd-screened') then
        input_carrier='AA1-RAW-FLUX'
        output_carrier='AA1-RAW-FLUX'
        report_prefix='RANK2-CURRENT-ZPCD-AA1'
        latest_output='D'
        previous_output='ZP'
      else if (trim(mode) == '--next-aa1aa2-screened') then
        input_carrier='AA2-RAW-FLUX'
        output_carrier='AA1-RAW-FLUX'
        report_prefix='RANK2-CURRENT-GH-AA1'
        latest_output='H'
        previous_output='G'
      else
        input_carrier='AA2-RAW-FLUX'
        output_carrier='AA1-RAW-FLUX'
        report_prefix='RANK2-CURRENT-QVWX-AA1'
        latest_output='X'
        previous_output='V'
      endif
    else if (zu_history_mode) then
      input_carrier='U-RAW-FLUX'
      output_carrier='V2-RAW-FLUX'
      report_prefix='RANK2-LATEST-QV-AA1'
      latest_output='V'
      previous_output='U'
    else if (x4z_history_mode) then
      input_carrier='Z-RAW-FLUX'
      output_carrier='U-RAW-FLUX'
      report_prefix='RANK2-LATEST2-AA1-NEXT'
      latest_output='U'
      previous_output='Z'
    else if (x4_history_mode) then
      input_carrier='X4-RAW-FLUX'
      output_carrier='Z-RAW-FLUX'
      report_prefix='RANK2-LATEST-AA1-NEXT'
      latest_output='Z'
      previous_output='X4'
    else if (rolling_next_mode) then
      input_carrier='XNP-RAW-FLUX'
      output_carrier='XRP-RAW-FLUX'
      report_prefix='RANK2-ROLL2-AA1'
      latest_output='XROLL-P'
      previous_output='XNEXT-P'
    else if (rolling_mode) then
      input_carrier='AA1-RAW-FLUX'
      output_carrier='XNP-RAW-FLUX'
      report_prefix='RANK2-ROLL-AA1'
      latest_output='XNEXT-P'
      previous_output='AA1-PLUS'
    else if (post_aa1_mode) then
      input_carrier='X3-RAW-FLUX'
      output_carrier='AA1-RAW-FLUX'
      report_prefix='RANK2-POST-AA1'
      latest_output='AA1-PLUS'
      previous_output='X3'
    else if (u_mode) then
      input_carrier='Z-RAW-FLUX'
      output_carrier='V-RAW-FLUX'
      report_prefix='RANK2-MODAL-AA1-U'
      latest_output='V'
      previous_output='Z'
    else
      input_carrier='X2-RAW-FLUX'
      output_carrier='Z-RAW-FLUX'
      report_prefix='RANK2-MODAL-AA1-NEXT'
      latest_output='Z'
      previous_output='X2'
    endif

    if (current_screened_mode) then
      if (trim(mode) == '--next-zpcd-screened') then
        call load_state(trim(next_path(1)),next_x1,'previous map input')
      else if (trim(mode) == '--next-aa1aa2-screened') then
        call load_state(trim(next_path(1)),next_x1, &
          'previous proposal input',.true.,'AA1-RAW-FLUX')
      else
        call load_state(trim(next_path(1)),next_x1, &
          'previous proposal input',.true.,'X4-RAW-FLUX')
      endif
    else if (zu_history_mode) then
      call load_state(trim(next_path(1)),next_x1, &
        'previous proposal input',.true.,'Z-RAW-FLUX')
    else if (x4z_history_mode) then
      call load_state(trim(next_path(1)),next_x1, &
        'previous proposal input',.true.,'X4-RAW-FLUX')
    else if (rolling_next_mode) then
      call load_state(trim(next_path(1)),next_x1,'previous proposal input', &
        .true.,'AA1-RAW-FLUX')
    else if (rolling_mode) then
      call load_state(trim(next_path(1)),next_x1,'previous proposal input', &
        .true.,'X3-RAW-FLUX')
    else if (u_mode) then
      call load_state(trim(next_path(1)),next_x1,'previous proposal input', &
        .true.,'X2-RAW-FLUX')
    else
      call load_state(trim(next_path(1)),next_x1,'previous map input')
    endif
    call load_state(trim(next_path(2)),next_x2,'previous map output')
    call load_state(trim(next_path(3)),next_y,'latest proposal input', &
      .true.,input_carrier)
    call load_state(trim(next_path(4)),next_z,'latest returned output')
    call compare_next_fixed_space(next_x1,next_x2,'x1/x2')
    call compare_next_fixed_space(next_x1,next_y,'x1/y')
    call compare_next_fixed_space(next_x1,next_z,'x1/z')
    call validate_snapshot(trim(next_path(5)),next_y,next_z,next_z_snap)

    ! The two evaluated map residuals are output-input for each pair.
    p_sq=0.0_real64
    q_sq=0.0_real64
    p_dot=0.0_real64
    do g=1,next_x1%dims(2)
      mode_count=next_x1%rank(g)
      do s=1,next_x1%dims(3)
        do ia=1,mode_count
          il=next_x1%offset(g)+(s-1)*mode_count+ia
          p_a=next_x2%coordinates(il)-next_x1%coordinates(il)
          q_a=next_z%coordinates(il)-next_y%coordinates(il)
          do ib=1,mode_count
            r=next_x1%offset(g)+(s-1)*mode_count+ib
            ig=next_x1%gram_offset(g)+(ib-1)*mode_count+ia
            p_b=next_x2%coordinates(r)-next_x1%coordinates(r)
            q_b=next_z%coordinates(r)-next_y%coordinates(r)
            p_sq=p_sq+next_x1%height(s)*p_a*next_x1%gram(ig)*p_b
            q_sq=q_sq+next_x1%height(s)*q_a*next_x1%gram(ig)*q_b
            p_dot=p_dot+next_x1%height(s)*p_a*next_x1%gram(ig)*q_b
          enddo
        enddo
      enddo
    enddo
    if ((.not.ieee_is_finite(p_sq)).or.(p_sq < 0.0_real64).or. &
        (.not.ieee_is_finite(q_sq)).or.(q_sq < 0.0_real64).or. &
        (.not.ieee_is_finite(p_dot))) &
      error stop 'invalid next modal residual geometry'
    next_denominator=p_sq+q_sq-2.0_real64*p_dot
    if ((.not.ieee_is_finite(next_denominator)).or. &
        (next_denominator <= 0.0_real64)) &
      error stop 'singular next modal Anderson scalar system'
    next_beta=(p_sq-p_dot)/next_denominator
    next_weight_x2=1.0_real64-next_beta
    if ((.not.ieee_is_finite(next_beta)).or. &
        (.not.ieee_is_finite(next_weight_x2))) &
      error stop 'nonfinite next modal Anderson weight'

    if (current_screened_mode) then
      if (q_sq <= 0.0_real64) &
        error stop 'invalid current screened modal residual'
      next_modal_affine_sq=next_weight_x2**2*p_sq+next_beta**2*q_sq+ &
        2.0_real64*next_weight_x2*next_beta*p_dot
      if ((.not.ieee_is_finite(next_modal_affine_sq)).or. &
          (next_modal_affine_sq < 0.0_real64)) &
        error stop 'invalid current screened modal direction'
      next_modal_affine_norm=sqrt(next_modal_affine_sq)
      next_modal_current_norm=sqrt(q_sq)

      next_leakage_affine_sq=0.0_real64
      next_leakage_current_sq=0.0_real64
      next_leakage_affine_d=0.0_real64
      next_leakage_current_d=0.0_real64
      do s=1,next_x1%dims(3)
        do g=1,next_x1%dims(2)
          il=(s-1)*next_x1%dims(2)+g
          next_leakage_p=next_x2%leakage(il)-next_x1%leakage(il)
          next_leakage_q=next_z%leakage(il)-next_y%leakage(il)
          next_leakage_affine=next_weight_x2*next_leakage_p+ &
            next_beta*next_leakage_q
          next_leakage_affine_sq=next_leakage_affine_sq+ &
            next_x1%height(s)*next_leakage_affine**2
          next_leakage_current_sq=next_leakage_current_sq+ &
            next_x1%height(s)*next_leakage_q**2
          next_leakage_affine_d=max(next_leakage_affine_d, &
            abs(next_leakage_affine))
          next_leakage_current_d=max(next_leakage_current_d, &
            abs(next_leakage_q))
        enddo
      enddo
      if ((.not.ieee_is_finite(next_leakage_affine_sq)).or. &
          (next_leakage_affine_sq < 0.0_real64).or. &
          (.not.ieee_is_finite(next_leakage_current_sq)).or. &
          (next_leakage_current_sq <= 0.0_real64).or. &
          (.not.ieee_is_finite(next_leakage_affine_d)).or. &
          (.not.ieee_is_finite(next_leakage_current_d)).or. &
          (next_leakage_current_d <= 0.0_real64)) &
        error stop 'invalid current screened leakage direction'
      next_leakage_affine_norm=sqrt(next_leakage_affine_sq)
      next_leakage_current_norm=sqrt(next_leakage_current_sq)
      if ((next_modal_affine_norm >= next_modal_current_norm).or. &
          (next_leakage_affine_norm >= next_leakage_current_norm).or. &
          (next_leakage_affine_d >= next_leakage_current_d)) &
        error stop 'current AA1 parameter-free direction gate failed'
    endif

    allocate(next_candidate_a(size(next_x2%coordinates)))
    allocate(next_candidate_l(size(next_x2%leakage)))
    allocate(next_published_l(size(next_x2%leakage)))
    next_candidate_a=next_weight_x2*next_x2%coordinates+ &
      next_beta*next_z%coordinates
    next_candidate_l=next_weight_x2*next_x2%leakage+ &
      next_beta*next_z%leakage
    next_published_l=real(next_candidate_l,real32)
    next_rho_star=next_weight_x2*next_x2%rho+next_beta*next_z%rho
    if ((.not.ieee_is_finite(next_rho_star)).or. &
        (next_rho_star <= 0.0_real64)) &
      error stop 'invalid next affine inverse eigenvalue'
    next_k_public=real(1.0_real64/next_rho_star,real32)
    if ((.not.ieee_is_finite(next_k_public)).or. &
        (next_k_public <= 0.0_real32)) &
      error stop 'invalid next published effective eigenvalue'
    next_rho_public=1.0_real64/real(next_k_public,real64)
    if (any(.not.ieee_is_finite(next_candidate_a)).or. &
        any(.not.ieee_is_finite(next_candidate_l)).or. &
        any(.not.ieee_is_finite(next_published_l)).or. &
        (.not.ieee_is_finite(next_rho_public)).or. &
        (next_rho_public <= 0.0_real64)) &
      error stop 'nonfinite next published proposal'
    next_l_roundtrip=maxval(abs( &
      real(next_published_l,real64)-next_candidate_l))

    next_min_reconstructed=huge(next_min_reconstructed)
    positive_count=0
    do g=1,next_z%dims(2)
      mode_count=next_z%rank(g)
      region_count=(next_z%basis_offset(g+1)- &
        next_z%basis_offset(g))/mode_count
      do s=1,next_z%dims(3)
        do r=1,region_count
          next_reconstructed=0.0_real64
          do ia=1,mode_count
            il=next_z%offset(g)+(s-1)*mode_count+ia
            ib=next_z%basis_offset(g)+(ia-1)*region_count+r
            next_reconstructed=next_reconstructed+ &
              real(next_z%basis(ib),real64)*next_candidate_a(il)
          enddo
          next_projected=real(next_reconstructed,real32)
          if ((.not.ieee_is_finite(next_reconstructed)).or. &
              (.not.ieee_is_finite(next_projected)).or. &
              (next_projected <= 0.0_real32)) &
            error stop 'next published reconstructed flux is not positive'
          positive_count=positive_count+1
          next_min_reconstructed=min(next_min_reconstructed, &
            real(next_projected,real64))
        enddo
      enddo
    enddo
    if (positive_count /= next_z%dims(2)*next_z%dims(3)*8) &
      error stop 'next reconstructed-flux census is incomplete'

    ! The latest returned state supplies the AX and raw-flux carrier.
    call LCMOP(next_staged_ax,' ',0,1,0)
    call LCMEQU(next_z%root,next_staged_ax)
    call LCMPUT(next_staged_ax,'SPOT-X-A',size(next_candidate_a),4, &
      next_candidate_a)
    call LCMPUT(next_staged_ax,'K-EFFECTIVE',1,2,next_k_public)
    call LCMPUT(next_staged_ax,'SPOT-X-RHO',1,4,next_rho_public)
    call LCMPUT(next_staged_ax,'SPOT-X-L',size(next_published_l),4, &
      real(next_published_l,real64))
    call delete_if_present(next_staged_ax,'SPOT-X-RRHO')
    call delete_if_present(next_staged_ax,'SPOT-X-RLEAK')
    call delete_if_present(next_staged_ax,'SPOT-X-DLEAK')
    call delete_if_present(next_staged_ax,'SPOT-X-RA')
    call delete_if_present(next_staged_ax,'SPOT-X-PERP')
    call delete_if_present(next_staged_ax,'SPOT-X-EPOCH')
    call delete_if_present(next_staged_ax,'SPOT-GBAL')
    call delete_if_present(next_staged_ax,'SPOT-GBAL-MA')
    next_marker='PROPOSAL'
    call LCMPTC(next_staged_ax,'SPOT-X-STATE',12,next_marker)
    next_marker=output_carrier
    call LCMPTC(next_staged_ax,'SPOT-X-CARR',12,next_marker)
    call LCMOP(next_out_ax,trim(next_path(6)),0,2,0)
    call LCMEQU(next_staged_ax,next_out_ax)
    call LCMCL(next_out_ax,1)
    call LCMCL(next_staged_ax,2)

    ! Preserve the carrier's lagged SYSTEM and publish only k and FLUX L.
    call LCMOP(next_staged_snap,' ',0,1,0)
    call LCMEQU(next_z_snap,next_staged_snap)
    next_iter_k=real(next_k_public,real64)
    call LCMPUT(next_staged_snap,'SPOT-ITER-K',1,4,next_iter_k)
    call delete_if_present(next_staged_snap,'SPOT-L1-ERR')
    call delete_if_present(next_staged_snap,'SPOT-PJ-PERP')
    call delete_if_present(next_staged_snap,'SPOT-PROJECT')
    next_fluxes=LCMGID(next_staged_snap,'FLUX')
    do s=1,next_z%dims(3)
      next_plane=LCMGIL(next_fluxes,s)
      il=(s-1)*next_z%dims(2)+1
      call LCMPUT(next_plane,'SPOT-LEAK1D',next_z%dims(2),2, &
        next_published_l(il:il+next_z%dims(2)-1))
    enddo
    call LCMOP(next_out_snap,trim(next_path(7)),0,2,0)
    call LCMEQU(next_staged_snap,next_out_snap)
    call LCMCL(next_out_snap,1)
    call LCMCL(next_staged_snap,2)

    call LCMCL(next_z_snap,1)
    call LCMCL(next_z%root,1)
    call LCMCL(next_y%root,1)
    call LCMCL(next_x2%root,1)
    call LCMCL(next_x1%root,1)

    write(*,'(A,ES24.16)') trim(report_prefix)//' BETA-WEIGHT-'// &
      trim(latest_output)//' ',next_beta
    write(*,'(A,ES24.16)') trim(report_prefix)//' WEIGHT-'// &
      trim(previous_output)//' ',next_weight_x2
    write(*,'(A,ES24.16)') trim(report_prefix)//' DENOMINATOR ', &
      next_denominator
    write(*,'(A,ES24.16)') trim(report_prefix)//' RHO-AFFINE ', &
      next_rho_star
    write(*,'(A,ES24.16)') trim(report_prefix)//' K-PUBLISHED ', &
      real(next_k_public,real64)
    write(*,'(A,ES24.16)') trim(report_prefix)//' RHO-PUBLISHED ', &
      next_rho_public
    write(*,'(A,ES24.16)') trim(report_prefix)//' RHO-Q-DELTA ', &
      next_rho_public-next_rho_star
    write(*,'(A,ES24.16)') trim(report_prefix)//' L-ROUNDTRIP-MAX ', &
      next_l_roundtrip
    write(*,'(A,ES24.16)') trim(report_prefix)//' MIN-PUBLISHED-BA ', &
      next_min_reconstructed
    write(*,'(A,I0)') trim(report_prefix)//' POSITIVE-BA-POINTS ', &
      positive_count
    if (current_screened_mode) then
      write(*,'(A,ES24.16)') trim(report_prefix)// &
        ' MODAL-AFFINE-L2/CURRENT ', &
        next_modal_affine_norm/next_modal_current_norm
      write(*,'(A,ES24.16)') trim(report_prefix)// &
        ' LEAKAGE-AFFINE-L2/CURRENT SAME-MODAL-BETA ', &
        next_leakage_affine_norm/next_leakage_current_norm
      write(*,'(A,ES24.16)') trim(report_prefix)// &
        ' LEAKAGE-AFFINE-DL/CURRENT SAME-MODAL-BETA ', &
        next_leakage_affine_d/next_leakage_current_d
      write(*,'(A)') trim(report_prefix)// &
        ' LEAKAGE SCREEN ONLY NO LEAKAGE FIT'
      write(*,'(A)') trim(report_prefix)// &
        ' PARAMETER-FREE DIRECTION GATE PASS'
    endif
    write(*,'(A)') trim(report_prefix)//' CARRIER '//trim(output_carrier)
    write(*,'(A)') trim(report_prefix)//' CLASSIFICATION '// &
      'MATERIALIZED_PROPOSAL_NOT_EVALUATED NO-DRAGON NO-MAP'
  end subroutine build_next_candidate

  subroutine load_state(file_name,data,owner,proposal_schema, &
      proposal_carrier)
    character(len=*), intent(in) :: file_name,owner
    type(canonical_state), intent(out) :: data
    logical, intent(in), optional :: proposal_schema
    character(len=*), intent(in), optional :: proposal_carrier
    integer :: ngrp,nsnap,ncoef,total_basis,total_gram,g,nreg
    logical :: is_proposal
    character(len=12) :: expected_carrier

    is_proposal=.false.
    if (present(proposal_schema)) is_proposal=proposal_schema
    expected_carrier='X2-RAW-FLUX'
    if (present(proposal_carrier)) expected_carrier=proposal_carrier
    call LCMOP(data%root,file_name,2,2,0)
    call require_character(data%root,'SIGNATURE','L_FLUX',owner)
    call require_record(data%root,'STATE-VECTOR',nstate,1,owner)
    call require_record(data%root,'SPOT-X-DIMS',4,1,owner)
    call LCMGET(data%root,'STATE-VECTOR',data%state)
    call LCMGET(data%root,'SPOT-X-DIMS',data%dims)
    ngrp=data%dims(2)
    nsnap=data%dims(3)
    ncoef=data%dims(4)
    if ((data%dims(1) /= 1).or.(ngrp /= 370).or.(nsnap /= 3).or. &
        (ncoef /= 2220).or.(data%state(1) /= ngrp)) &
      error stop 'invalid frozen rank-two dimensions'

    allocate(data%rank(ngrp),data%offset(ngrp+1))
    allocate(data%gram_offset(ngrp+1),data%basis_offset(ngrp+1))
    call require_record(data%root,'SPOT-X-RANK',ngrp,1,owner)
    call require_record(data%root,'SPOT-X-OFF',ngrp+1,1,owner)
    call require_record(data%root,'SPOT-X-GOFF',ngrp+1,1,owner)
    call require_record(data%root,'SPOT-X-BOFF',ngrp+1,1,owner)
    call LCMGET(data%root,'SPOT-X-RANK',data%rank)
    call LCMGET(data%root,'SPOT-X-OFF',data%offset)
    call LCMGET(data%root,'SPOT-X-GOFF',data%gram_offset)
    call LCMGET(data%root,'SPOT-X-BOFF',data%basis_offset)
    if (any(data%rank /= 2).or.(data%offset(1) /= 0).or. &
        (data%gram_offset(1) /= 0).or.(data%basis_offset(1) /= 0).or. &
        (data%offset(ngrp+1) /= ncoef)) &
      error stop 'invalid frozen rank-two layout'
    do g=1,ngrp
      if (data%offset(g+1)-data%offset(g) /= nsnap*data%rank(g)) &
        error stop 'invalid rank-two coordinate offsets'
      if (data%gram_offset(g+1)-data%gram_offset(g) /= &
          data%rank(g)*data%rank(g)) &
        error stop 'invalid rank-two Gram offsets'
      nreg=(data%basis_offset(g+1)-data%basis_offset(g))/data%rank(g)
      if ((nreg /= 8).or. &
          (data%basis_offset(g+1)-data%basis_offset(g) /= &
           nreg*data%rank(g))) &
        error stop 'invalid rank-two basis offsets'
    enddo
    total_basis=data%basis_offset(ngrp+1)
    total_gram=data%gram_offset(ngrp+1)
    allocate(data%basis(total_basis),data%coordinates(ncoef))
    allocate(data%leakage(ngrp*nsnap),data%height(nsnap))
    allocate(data%gram(total_gram))
    if (.not.is_proposal) allocate(data%offspace(ngrp*nsnap))
    call require_record(data%root,'SPOT-X-BASIS',total_basis,2,owner)
    call require_record(data%root,'SPOT-X-A',ncoef,4,owner)
    call require_record(data%root,'SPOT-X-L',ngrp*nsnap,4,owner)
    call require_record(data%root,'SPOT-X-H',nsnap,4,owner)
    call require_record(data%root,'SPOT-X-GRAM',total_gram,4,owner)
    if (is_proposal) then
      call require_absent(data%root,'SPOT-X-PERP',owner)
    else
      call require_record(data%root,'SPOT-X-PERP',ngrp*nsnap,4,owner)
    endif
    call require_record(data%root,'K-EFFECTIVE',1,2,owner)
    call require_record(data%root,'SPOT-X-RHO',1,4,owner)
    call require_record(data%root,'SPOT-X-NORM',1,4,owner)
    call require_record(data%root,'SPOT-X-GERR',1,4,owner)
    call require_record(data%root,'SPOT-X-FIXB',1,1,owner)
    call require_record(data%root,'SPOT-X-NID',3,3,owner)
    call require_record(data%root,'SPOT-X-BTYP',3,3,owner)
    call LCMGET(data%root,'SPOT-X-BASIS',data%basis)
    call LCMGET(data%root,'SPOT-X-A',data%coordinates)
    call LCMGET(data%root,'SPOT-X-L',data%leakage)
    call LCMGET(data%root,'SPOT-X-H',data%height)
    call LCMGET(data%root,'SPOT-X-GRAM',data%gram)
    if (.not.is_proposal) &
      call LCMGET(data%root,'SPOT-X-PERP',data%offspace)
    call LCMGET(data%root,'K-EFFECTIVE',data%keff)
    call LCMGET(data%root,'SPOT-X-RHO',data%rho)
    call LCMGET(data%root,'SPOT-X-NORM',data%norm)
    call LCMGET(data%root,'SPOT-X-GERR',data%gram_error)
    call LCMGET(data%root,'SPOT-X-FIXB',data%fixb)
    call LCMGTC(data%root,'SPOT-X-NID',12,data%norm_id)
    call LCMGTC(data%root,'SPOT-X-BTYP',12,data%basis_type)
    if ((data%fixb /= 1).or.(data%norm_id /= 'NUFISS-UNIT').or. &
        (data%basis_type /= 'POD-FIXED')) &
      error stop 'invalid fixed-basis state markers'
    if (any(.not.ieee_is_finite(data%basis)).or. &
        any(.not.ieee_is_finite(data%coordinates)).or. &
        any(.not.ieee_is_finite(data%leakage)).or. &
        any(.not.ieee_is_finite(data%height)).or. &
        any(data%height <= 0.0_real64).or. &
        any(.not.ieee_is_finite(data%gram)).or. &
        (.not.ieee_is_finite(data%keff)).or.(data%keff <= 0.0_real32).or. &
        (.not.ieee_is_finite(data%rho)).or.(data%rho <= 0.0_real64).or. &
        (.not.ieee_is_finite(data%norm)).or.(data%norm <= 0.0_real64).or. &
        (.not.ieee_is_finite(data%gram_error)).or. &
        (data%gram_error < 0.0_real64)) &
      error stop 'nonfinite canonical rank-two state'
    if (.not.is_proposal) then
      if (any(.not.ieee_is_finite(data%offspace)).or. &
          any(data%offspace < 0.0_real64)) &
        error stop 'invalid canonical off-space diagnostic'
    else
      call require_absent(data%root,'SPOT-X-RRHO',owner)
      call require_absent(data%root,'SPOT-X-RLEAK',owner)
      call require_absent(data%root,'SPOT-X-DLEAK',owner)
      call require_absent(data%root,'SPOT-X-RA',owner)
      call require_absent(data%root,'SPOT-X-EPOCH',owner)
      call require_absent(data%root,'SPOT-GBAL',owner)
      call require_absent(data%root,'SPOT-GBAL-MA',owner)
      call require_character(data%root,'SPOT-X-STATE','PROPOSAL',owner)
      call require_character(data%root,'SPOT-X-CARR',expected_carrier,owner)
    endif
    if (any(bits64(data%leakage) /= &
            bits64(real(real(data%leakage,real32),real64)))) &
      error stop 'canonical leakage is not promoted binary32'
    if (bits64(data%rho) /= &
        bits64(1.0_real64/real(data%keff,real64))) &
      error stop 'inverse-eigenvalue identity differs'
  end subroutine load_state

  subroutine compare_fixed_space(left,right,owner)
    type(canonical_state), intent(in) :: left,right
    character(len=*), intent(in) :: owner
    if (any(left%state /= right%state).or.any(left%dims /= right%dims).or. &
        any(left%rank /= right%rank).or.any(left%offset /= right%offset).or. &
        any(left%gram_offset /= right%gram_offset).or. &
        any(left%basis_offset /= right%basis_offset).or. &
        any(bits32(left%basis) /= bits32(right%basis)).or. &
        any(bits64(left%height) /= bits64(right%height)).or. &
        any(bits64(left%gram) /= bits64(right%gram)).or. &
        (bits64(left%gram_error) /= bits64(right%gram_error)).or. &
        (left%fixb /= right%fixb).or.(left%norm_id /= right%norm_id).or. &
        (left%basis_type /= right%basis_type)) then
      write(*,'(A,1X,A)') 'fixed-space mismatch',trim(owner)
      error stop 'fixed rank-two package changed'
    endif
  end subroutine compare_fixed_space

  subroutine compare_next_fixed_space(left,right,owner)
    type(canonical_state), intent(in) :: left,right
    character(len=*), intent(in) :: owner
    if (any(left%dims /= right%dims).or. &
        any(left%rank /= right%rank).or.any(left%offset /= right%offset).or. &
        any(left%gram_offset /= right%gram_offset).or. &
        any(left%basis_offset /= right%basis_offset).or. &
        any(bits32(left%basis) /= bits32(right%basis)).or. &
        any(bits64(left%height) /= bits64(right%height)).or. &
        any(bits64(left%gram) /= bits64(right%gram)).or. &
        (left%fixb /= right%fixb).or.(left%norm_id /= right%norm_id).or. &
        (left%basis_type /= right%basis_type)) then
      write(*,'(A,1X,A)') 'next fixed-space mismatch',trim(owner)
      error stop 'next fixed rank-two package changed'
    endif
  end subroutine compare_next_fixed_space

  subroutine validate_snapshot(file_name,previous,current,root)
    character(len=*), intent(in) :: file_name
    type(canonical_state), intent(in) :: previous,current
    type(c_ptr), intent(out) :: root
    type(c_ptr) :: local_fluxes,local_systems,local_plane,local_system
    integer :: s,first,plane_id
    integer :: local_listdim
    real(real64) :: local_iter
    real(real32), allocatable :: local_l(:),local_system_l(:)

    call LCMOP(root,file_name,2,2,0)
    call require_character(root,'SIGNATURE','L_ARCHIVE','x2 snapshots')
    call require_record(root,'LISTDIM',1,1,'x2 snapshots')
    call LCMGET(root,'LISTDIM',local_listdim)
    if (local_listdim /= current%dims(3)) &
      error stop 'x2 snapshot count differs'
    call require_record(root,'SPOT-ITER-K',1,4,'x2 snapshots')
    call LCMGET(root,'SPOT-ITER-K',local_iter)
    if (bits64(local_iter) /= bits64(real(current%keff,real64))) &
      error stop 'x2 snapshot effective eigenvalue differs'
    call require_absent(root,'SPOT-R64','x2 snapshots')
    call require_record(root,'FLUX',local_listdim,10,'x2 snapshots')
    call require_record(root,'SYSTEM',local_listdim,10,'x2 snapshots')
    local_fluxes=LCMGID(root,'FLUX')
    local_systems=LCMGID(root,'SYSTEM')
    allocate(local_l(current%dims(2)),local_system_l(current%dims(2)))
    do s=1,local_listdim
      local_plane=LCMGIL(local_fluxes,s)
      local_system=LCMGIL(local_systems,s)
      call require_record(local_plane,'SPOT-LEAK1D',current%dims(2),2, &
        'x2 snapshot FLUX')
      call require_record(local_system,'SPOT-LEAK1D',current%dims(2),2, &
        'x2 snapshot SYSTEM')
      call require_record(local_system,'SPOT-L1-SNAP',1,1, &
        'x2 snapshot SYSTEM')
      call LCMGET(local_plane,'SPOT-LEAK1D',local_l)
      call LCMGET(local_system,'SPOT-LEAK1D',local_system_l)
      call LCMGET(local_system,'SPOT-L1-SNAP',plane_id)
      first=(s-1)*current%dims(2)+1
      if (any(bits32(local_l) /= bits32(real( &
          current%leakage(first:first+current%dims(2)-1),real32)))) &
        error stop 'x2 snapshot FLUX leakage differs from x2 state'
      if (any(bits32(local_system_l) /= bits32(real( &
          previous%leakage(first:first+current%dims(2)-1),real32)))) &
        error stop 'x2 lagged SYSTEM leakage differs from x1 state'
      if (plane_id /= s) error stop 'x2 lagged SYSTEM snapshot id differs'
    enddo
    deallocate(local_system_l,local_l)
  end subroutine validate_snapshot

  subroutine require_fresh_path(file_name)
    character(len=*), intent(in) :: file_name
    logical :: exists
    inquire(file=trim(file_name),exist=exists)
    if (exists) error stop 'output XSM path already exists'
  end subroutine require_fresh_path

  subroutine require_record(object,name,length_expected,type_expected,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length_expected,type_expected
    integer :: length_found,type_found
    call LCMLEN(object,name,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) then
      write(*,'(A,1X,A)') trim(owner),trim(name)
      error stop 'required GANLIB record differs'
    endif
  end subroutine require_record

  subroutine require_character(object,name,expected,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,expected,owner
    character(len=12) :: found
    call require_record(object,name,3,3,owner)
    call LCMGTC(object,name,12,found)
    if (found /= expected) error stop 'required character record differs'
  end subroutine require_character

  subroutine require_absent(object,name,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    integer :: length_found,type_found
    call LCMLEN(object,name,length_found,type_found)
    if (length_found /= 0) then
      write(*,'(A,1X,A)') trim(owner),trim(name)
      error stop 'GANLIB record must be absent'
    endif
  end subroutine require_absent

  subroutine delete_if_present(object,name)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name
    integer :: length_found,type_found
    call LCMLEN(object,name,length_found,type_found)
    if (length_found /= 0) call LCMDEL(object,name)
  end subroutine delete_if_present

  pure elemental integer(int32) function bits32(value)
    real(real32), intent(in) :: value
    bits32=transfer(value,0_int32)
  end function bits32

  pure elemental integer(int64) function bits64(value)
    real(real64), intent(in) :: value
    bits64=transfer(value,0_int64)
  end function bits64

end program build_rank2_modal_aa1_candidate
