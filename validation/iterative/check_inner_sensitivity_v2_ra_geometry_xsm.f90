program check_inner_sensitivity_v2_ra_geometry_xsm
  ! Independent, read-only Ganlib audit of the unresolved Stage-4v2
  ! canonical-coordinate geometry.
  !
  !   check_ra_geometry X0_AXIAL X1_2H_AXIAL X1_H_AXIAL
  !
  ! The checker performs no transport solve, changes no XSM record, and
  ! introduces no numerical acceptance threshold.  All Gram products used
  ! to close R_a retain SPOXCONV's g -> s -> a -> b accumulation order.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  implicit none

  integer, parameter :: nstate=40
  integer, parameter :: expected_rank=1
  integer, parameter :: expected_groups=370
  integer, parameter :: expected_planes=3
  integer, parameter :: expected_regions=8
  integer, parameter :: expected_coefficients=1110
  integer, parameter :: max_xsm_path=72
  character(len=*), parameter :: prefix = &
    'INNER-SENSITIVITY-V2 RA-GEOMETRY'

  type :: axial_state
    integer :: dims(4)=0
    integer, allocatable :: rank(:)
    integer, allocatable :: offset(:)
    integer, allocatable :: gram_offset(:)
    integer, allocatable :: basis_offset(:)
    real(real32), allocatable :: basis(:)
    real(real64), allocatable :: coordinates(:)
    real(real64), allocatable :: height(:)
    real(real64), allocatable :: gram(:)
    real(real64) :: saved_ra=0.0_real64
    character(len=12) :: norm_id=''
  end type axial_state

  character(len=1024) :: path(3)
  type(axial_state) :: x0,x1_2h,x1_h
  real(real64), allocatable :: u(:),e(:),v(:)
  real(real64), allocatable :: plane_nout2(:),plane_nin2(:)
  real(real64), allocatable :: plane_v2(:),plane_q2h2(:),plane_qh2(:)
  real(real64), allocatable :: plane_cross(:),plane_delta2(:)
  real(real64), allocatable :: group_nout2(:),group_nin2(:)
  real(real64), allocatable :: group_v2(:),group_q2h2(:),group_qh2(:)
  real(real64), allocatable :: group_cross(:),group_delta2(:)
  real(real64) :: nout2,nin2,vnorm2,q2h_norm2,qh_norm2,cross
  real(real64) :: nout,nin,vnorm,q2h_norm,qh_norm
  real(real64) :: cosine,beta,orth_norm2,orth_norm,orth_rel
  real(real64) :: rout_2h,rin,rout_h,delta_r,delta2_post
  real(real64) :: delta2_cell_fold,delta2_plane_fold
  real(real64) :: delta2_group_fold,delta2_cell
  real(real64) :: ua,ub,ea,eb,va,vb,a2ha,a2hb,aha,ahb
  real(real64) :: wa,wb
  integer :: arg,g,s,a,b,nmode,index_a,index_b,index_g
  integer :: negative_planes,zero_planes,positive_planes
  integer :: negative_groups,zero_groups,positive_groups,max_group

  if (command_argument_count() /= 3) call fail( &
    'THREE XSM ARGUMENTS EXPECTED: X0 X1-2H X1-H.')
  do arg=1,3
    call get_command_argument(arg,path(arg))
    if (len_trim(path(arg)) == 0) call fail('EMPTY XSM PATH ARGUMENT.')
    if (len_trim(path(arg)) > max_xsm_path) &
      call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
  enddo

  call load_state(trim(path(1)),.false.,x0,'X0')
  call load_state(trim(path(2)),.true.,x1_2h,'X1 2H')
  call load_state(trim(path(3)),.true.,x1_h,'X1 H')
  call compare_space(x0,x1_2h,'X0/X1-2H')
  call compare_space(x0,x1_h,'X0/X1-H')

  allocate(u(expected_coefficients),e(expected_coefficients))
  allocate(v(expected_coefficients))
  u=x1_2h%coordinates-x0%coordinates
  e=x1_h%coordinates-x1_2h%coordinates
  v=x1_h%coordinates-x0%coordinates
  if (any(.not.ieee_is_finite(u)).or. &
      any(.not.ieee_is_finite(e)).or. &
      any(.not.ieee_is_finite(v))) &
    call fail('NON-FINITE CANONICAL DIFFERENCE VECTOR.')

  allocate(plane_nout2(expected_planes),plane_nin2(expected_planes))
  allocate(plane_v2(expected_planes),plane_q2h2(expected_planes))
  allocate(plane_qh2(expected_planes),plane_cross(expected_planes))
  allocate(plane_delta2(expected_planes))
  allocate(group_nout2(expected_groups),group_nin2(expected_groups))
  allocate(group_v2(expected_groups),group_q2h2(expected_groups))
  allocate(group_qh2(expected_groups),group_cross(expected_groups))
  allocate(group_delta2(expected_groups))
  plane_nout2=0.0_real64
  plane_nin2=0.0_real64
  plane_v2=0.0_real64
  plane_q2h2=0.0_real64
  plane_qh2=0.0_real64
  plane_cross=0.0_real64
  group_nout2=0.0_real64
  group_nin2=0.0_real64
  group_v2=0.0_real64
  group_q2h2=0.0_real64
  group_qh2=0.0_real64
  group_cross=0.0_real64
  nout2=0.0_real64
  nin2=0.0_real64
  vnorm2=0.0_real64
  q2h_norm2=0.0_real64
  qh_norm2=0.0_real64
  cross=0.0_real64

  ! Preserve the production R_a loop and arithmetic association exactly:
  ! group, snapshot plane, row mode, column mode.
  do g=1,expected_groups
    nmode=x0%rank(g)
    do s=1,expected_planes
      do a=1,nmode
        index_a=x0%offset(g)+(s-1)*nmode+a
        ua=u(index_a)
        ea=e(index_a)
        va=v(index_a)
        a2ha=x1_2h%coordinates(index_a)
        aha=x1_h%coordinates(index_a)
        do b=1,nmode
          index_b=x0%offset(g)+(s-1)*nmode+b
          index_g=x0%gram_offset(g)+(b-1)*nmode+a
          ub=u(index_b)
          eb=e(index_b)
          vb=v(index_b)
          a2hb=x1_2h%coordinates(index_b)
          ahb=x1_h%coordinates(index_b)

          nout2=nout2+x0%height(s)*ua*x0%gram(index_g)*ub
          nin2=nin2+x0%height(s)*ea*x0%gram(index_g)*eb
          vnorm2=vnorm2+x0%height(s)*va*x0%gram(index_g)*vb
          q2h_norm2=q2h_norm2+x0%height(s)*a2ha* &
            x0%gram(index_g)*a2hb
          qh_norm2=qh_norm2+x0%height(s)*aha*x0%gram(index_g)*ahb
          cross=cross+x0%height(s)*ua*x0%gram(index_g)*eb

          plane_nout2(s)=plane_nout2(s)+ &
            x0%height(s)*ua*x0%gram(index_g)*ub
          plane_nin2(s)=plane_nin2(s)+ &
            x0%height(s)*ea*x0%gram(index_g)*eb
          plane_v2(s)=plane_v2(s)+ &
            x0%height(s)*va*x0%gram(index_g)*vb
          plane_q2h2(s)=plane_q2h2(s)+ &
            x0%height(s)*a2ha*x0%gram(index_g)*a2hb
          plane_qh2(s)=plane_qh2(s)+ &
            x0%height(s)*aha*x0%gram(index_g)*ahb
          plane_cross(s)=plane_cross(s)+ &
            x0%height(s)*ua*x0%gram(index_g)*eb

          group_nout2(g)=group_nout2(g)+ &
            x0%height(s)*ua*x0%gram(index_g)*ub
          group_nin2(g)=group_nin2(g)+ &
            x0%height(s)*ea*x0%gram(index_g)*eb
          group_v2(g)=group_v2(g)+ &
            x0%height(s)*va*x0%gram(index_g)*vb
          group_q2h2(g)=group_q2h2(g)+ &
            x0%height(s)*a2ha*x0%gram(index_g)*a2hb
          group_qh2(g)=group_qh2(g)+ &
            x0%height(s)*aha*x0%gram(index_g)*ahb
          group_cross(g)=group_cross(g)+ &
            x0%height(s)*ua*x0%gram(index_g)*eb
        enddo
      enddo
    enddo
  enddo

  if ((.not.ieee_is_finite(nout2)).or.(nout2 <= 0.0_real64).or. &
      (.not.ieee_is_finite(nin2)).or.(nin2 <= 0.0_real64).or. &
      (.not.ieee_is_finite(vnorm2)).or.(vnorm2 <= 0.0_real64).or. &
      (.not.ieee_is_finite(q2h_norm2)).or. &
      (q2h_norm2 <= 0.0_real64).or. &
      (.not.ieee_is_finite(qh_norm2)).or.(qh_norm2 <= 0.0_real64).or. &
      (.not.ieee_is_finite(cross))) &
    call fail('INVALID GLOBAL GRAM/HEIGHT GEOMETRY.')
  if (any(.not.ieee_is_finite(plane_nout2)).or. &
      any(.not.ieee_is_finite(plane_nin2)).or. &
      any(.not.ieee_is_finite(plane_v2)).or. &
      any(.not.ieee_is_finite(plane_q2h2)).or. &
      any(.not.ieee_is_finite(plane_qh2)).or. &
      any(.not.ieee_is_finite(plane_cross)).or. &
      any(plane_nout2 < 0.0_real64).or. &
      any(plane_nin2 < 0.0_real64).or. &
      any(plane_v2 < 0.0_real64).or. &
      any(plane_q2h2 < 0.0_real64).or. &
      any(plane_qh2 < 0.0_real64)) &
    call fail('INVALID PLANE GRAM/HEIGHT CONTRIBUTION.')
  if (any(.not.ieee_is_finite(group_nout2)).or. &
      any(.not.ieee_is_finite(group_nin2)).or. &
      any(.not.ieee_is_finite(group_v2)).or. &
      any(.not.ieee_is_finite(group_q2h2)).or. &
      any(.not.ieee_is_finite(group_qh2)).or. &
      any(.not.ieee_is_finite(group_cross)).or. &
      any(group_nout2 < 0.0_real64).or. &
      any(group_nin2 < 0.0_real64).or. &
      any(group_v2 < 0.0_real64).or. &
      any(group_q2h2 < 0.0_real64).or. &
      any(group_qh2 < 0.0_real64)) &
    call fail('INVALID GROUP GRAM/HEIGHT CONTRIBUTION.')

  nout=sqrt(nout2)
  nin=sqrt(nin2)
  vnorm=sqrt(vnorm2)
  q2h_norm=sqrt(q2h_norm2)
  qh_norm=sqrt(qh_norm2)
  cosine=cross/(nout*nin)
  beta=cross/nout2

  orth_norm2=0.0_real64
  do g=1,expected_groups
    nmode=x0%rank(g)
    do s=1,expected_planes
      do a=1,nmode
        index_a=x0%offset(g)+(s-1)*nmode+a
        wa=e(index_a)-beta*u(index_a)
        do b=1,nmode
          index_b=x0%offset(g)+(s-1)*nmode+b
          index_g=x0%gram_offset(g)+(b-1)*nmode+a
          wb=e(index_b)-beta*u(index_b)
          orth_norm2=orth_norm2+x0%height(s)*wa* &
            x0%gram(index_g)*wb
        enddo
      enddo
    enddo
  enddo
  if ((.not.ieee_is_finite(cosine)).or. &
      (cosine < -1.0_real64).or.(cosine > 1.0_real64).or. &
      (.not.ieee_is_finite(beta)).or. &
      (.not.ieee_is_finite(orth_norm2)).or. &
      (orth_norm2 < 0.0_real64).or.negative_zero(orth_norm2)) &
    call fail('INVALID PARALLEL/ORTHOGONAL GEOMETRY.')
  orth_norm=sqrt(orth_norm2)
  orth_rel=sqrt(orth_norm2/nout2)

  ! These expressions deliberately match SPOXCONV, rather than replacing
  ! sqrt(NORM2/Q_NORM2) with a differently rounded quotient of square roots.
  rout_2h=sqrt(nout2/q2h_norm2)
  rin=sqrt(nin2/qh_norm2)
  rout_h=sqrt(vnorm2/qh_norm2)
  if (real64_bits(rout_2h) /= real64_bits(x1_2h%saved_ra)) &
    call fail('R-OUT-2H DOES NOT CLOSE ITS SAVED SPOT-X-RA BITS.')
  if (real64_bits(rout_h) /= real64_bits(x1_h%saved_ra)) &
    call fail('R-OUT-H DOES NOT CLOSE ITS SAVED SPOT-X-RA BITS.')

  delta_r=rin-rout_2h
  delta2_post=nin2/qh_norm2-nout2/q2h_norm2

  ! Form each rank-one plane/group contribution exactly once, then feed the
  ! same value into the canonical, plane, and group folds.  These folds are
  ! deliberately reported separately from the global post-division path:
  ! binary64 addition is not associative under the strong cancellation here.
  plane_delta2=0.0_real64
  group_delta2=0.0_real64
  delta2_cell_fold=0.0_real64
  do g=1,expected_groups
    nmode=x0%rank(g)
    do s=1,expected_planes
      do a=1,nmode
        index_a=x0%offset(g)+(s-1)*nmode+a
        ua=u(index_a)
        ea=e(index_a)
        do b=1,nmode
          index_b=x0%offset(g)+(s-1)*nmode+b
          index_g=x0%gram_offset(g)+(b-1)*nmode+a
          ub=u(index_b)
          eb=e(index_b)
          delta2_cell=(x0%height(s)*ea*x0%gram(index_g)*eb)/ &
            qh_norm2-(x0%height(s)*ua*x0%gram(index_g)*ub)/ &
            q2h_norm2
          delta2_cell_fold=delta2_cell_fold+delta2_cell
          plane_delta2(s)=plane_delta2(s)+delta2_cell
          group_delta2(g)=group_delta2(g)+delta2_cell
        enddo
      enddo
    enddo
  enddo
  delta2_plane_fold=0.0_real64
  do s=1,expected_planes
    delta2_plane_fold=delta2_plane_fold+plane_delta2(s)
  enddo
  delta2_group_fold=0.0_real64
  do g=1,expected_groups
    delta2_group_fold=delta2_group_fold+group_delta2(g)
  enddo
  if ((.not.ieee_is_finite(delta_r)).or. &
      (.not.ieee_is_finite(delta2_post)).or. &
      (.not.ieee_is_finite(delta2_cell_fold)).or. &
      (.not.ieee_is_finite(delta2_plane_fold)).or. &
      (.not.ieee_is_finite(delta2_group_fold)).or. &
      any(.not.ieee_is_finite(plane_delta2)).or. &
      any(.not.ieee_is_finite(group_delta2))) &
    call fail('NON-FINITE RATIO DIFFERENCE.')

  call count_signs(plane_delta2,negative_planes,zero_planes, &
    positive_planes)
  call count_signs(group_delta2,negative_groups,zero_groups, &
    positive_groups)
  max_group=1
  do g=2,expected_groups
    if (abs(group_delta2(g)) > abs(group_delta2(max_group))) max_group=g
  enddo

  write(6,'(A)') prefix//' SPACE BITWISE IDENTICAL'
  write(6,'(A,4(1X,I0))') prefix//' DIMS',x0%dims
  call write_metric('GLOBAL','NOUT-NORM2',nout2)
  call write_metric('GLOBAL','NIN-NORM2',nin2)
  call write_metric('GLOBAL','V-NORM2',vnorm2)
  call write_metric('GLOBAL','Q2H-NORM2',q2h_norm2)
  call write_metric('GLOBAL','QH-NORM2',qh_norm2)
  call write_metric('GLOBAL','NOUT-NORM',nout)
  call write_metric('GLOBAL','NIN-NORM',nin)
  call write_metric('GLOBAL','V-NORM',vnorm)
  call write_metric('GLOBAL','Q2H-NORM',q2h_norm)
  call write_metric('GLOBAL','QH-NORM',qh_norm)
  call write_metric('GLOBAL','CROSS-U-E',cross)
  call write_metric('GLOBAL','COS-U-E',cosine)
  call write_metric('GLOBAL','PARALLEL-BETA',beta)
  call write_metric('GLOBAL','ORTH-NORM2',orth_norm2)
  call write_metric('GLOBAL','ORTH-NORM',orth_norm)
  call write_metric('GLOBAL','ORTH-REL-U',orth_rel)
  call write_metric('GLOBAL','DELTA-R',delta_r)
  call write_metric('GLOBAL','DELTA2-POST',delta2_post)
  call write_metric('GLOBAL','DELTA2-CELL-FOLD',delta2_cell_fold)
  call write_metric('GLOBAL','DELTA2-PLANE-FOLD',delta2_plane_fold)
  call write_metric('GLOBAL','DELTA2-GROUP-FOLD',delta2_group_fold)
  write(6,'(A,6(1X,A))') prefix//' RA-BITS', &
    'ROUT-2H',hex64(rout_2h),'RIN',hex64(rin), &
    'ROUT-H',hex64(rout_h)
  write(6,'(A,4(1X,A))') prefix//' SAVED-RA-BITS', &
    'ROUT-2H',hex64(x1_2h%saved_ra), &
    'ROUT-H',hex64(x1_h%saved_ra)

  do s=1,expected_planes
    call write_decomposition('PLANE',s,plane_nout2(s), &
      plane_nin2(s),plane_v2(s),plane_q2h2(s),plane_qh2(s), &
      plane_cross(s),plane_delta2(s))
  enddo
  write(6,'(A,4(1X,A,1X,I0))') prefix//' PLANE-DELTA2-SIGNS', &
    'NEG',negative_planes,'ZERO',zero_planes,'POS',positive_planes, &
    'TOTAL',negative_planes+zero_planes+positive_planes

  do g=1,expected_groups
    call write_decomposition('GROUP',g,group_nout2(g), &
      group_nin2(g),group_v2(g),group_q2h2(g),group_qh2(g), &
      group_cross(g),group_delta2(g))
  enddo
  write(6,'(A,4(1X,A,1X,I0))') prefix//' GROUP-DELTA2-SIGNS', &
    'NEG',negative_groups,'ZERO',zero_groups,'POS',positive_groups, &
    'TOTAL',negative_groups+zero_groups+positive_groups
  write(6,'(A,1X,A,1X,I0,1X,A,1X,A,1X,A,1X,ES25.17E3)') &
    prefix//' GROUP-DELTA2-MAXABS','GROUP',max_group, &
    'BITS',hex64(group_delta2(max_group)), &
    'VALUE',group_delta2(max_group)
  write(6,'(A)') prefix//' COMPLETE'

contains

  subroutine load_state(filename,expect_saved_ra,data,owner)
    character(len=*), intent(in) :: filename,owner
    logical, intent(in) :: expect_saved_ra
    type(axial_state), intent(out) :: data
    type(c_ptr) :: root
    character(len=12) :: signature
    integer :: g,total_basis,total_gram,state(nstate)

    call LCMOP(root,filename,2,2,0)
    call require_record(root,'SIGNATURE',3,3,owner)
    call LCMGTC(root,'SIGNATURE',12,signature)
    if (signature /= 'L_FLUX') &
      call fail(trim(owner)//' L_FLUX SIGNATURE EXPECTED.')
    call require_record(root,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(root,'STATE-VECTOR',state)
    if (state(1) /= expected_groups) &
      call fail(trim(owner)//' STATE-VECTOR GROUP COUNT CHANGED.')
    call require_record(root,'SPOT-X-DIMS',4,1,owner)
    call LCMGET(root,'SPOT-X-DIMS',data%dims)
    if (any(data%dims /= (/expected_rank,expected_groups, &
        expected_planes,expected_coefficients/))) &
      call fail(trim(owner)//' CANONICAL DIMENSIONS CHANGED.')

    allocate(data%rank(expected_groups))
    allocate(data%offset(expected_groups+1))
    allocate(data%gram_offset(expected_groups+1))
    allocate(data%basis_offset(expected_groups+1))
    call require_record(root,'SPOT-X-RANK',expected_groups,1,owner)
    call require_record(root,'SPOT-X-OFF',expected_groups+1,1,owner)
    call require_record(root,'SPOT-X-GOFF',expected_groups+1,1,owner)
    call require_record(root,'SPOT-X-BOFF',expected_groups+1,1,owner)
    call LCMGET(root,'SPOT-X-RANK',data%rank)
    call LCMGET(root,'SPOT-X-OFF',data%offset)
    call LCMGET(root,'SPOT-X-GOFF',data%gram_offset)
    call LCMGET(root,'SPOT-X-BOFF',data%basis_offset)
    if (any(data%rank /= expected_rank).or. &
        (data%offset(1) /= 0).or. &
        (data%gram_offset(1) /= 0).or. &
        (data%basis_offset(1) /= 0)) &
      call fail(trim(owner)//' INVALID RANK-ONE LAYOUT OR ORIGIN.')
    do g=1,expected_groups
      if (data%offset(g+1)-data%offset(g) /= expected_planes) &
        call fail(trim(owner)//' INVALID COORDINATE OFFSETS.')
      if (data%gram_offset(g+1)-data%gram_offset(g) /= 1) &
        call fail(trim(owner)//' INVALID GRAM OFFSETS.')
      if (data%basis_offset(g+1)-data%basis_offset(g) /= &
          expected_regions) &
        call fail(trim(owner)//' INVALID BASIS OFFSETS.')
    enddo
    if (data%offset(expected_groups+1) /= expected_coefficients) &
      call fail(trim(owner)//' INVALID COORDINATE EXTENT.')
    total_basis=data%basis_offset(expected_groups+1)
    total_gram=data%gram_offset(expected_groups+1)
    if ((total_basis /= expected_groups*expected_regions).or. &
        (total_gram /= expected_groups)) &
      call fail(trim(owner)//' INVALID FIXED-SPACE EXTENT.')

    allocate(data%basis(total_basis))
    allocate(data%coordinates(expected_coefficients))
    allocate(data%height(expected_planes))
    allocate(data%gram(total_gram))
    call require_record(root,'SPOT-X-BASIS',total_basis,2,owner)
    call require_record(root,'SPOT-X-A',expected_coefficients,4,owner)
    call require_record(root,'SPOT-X-H',expected_planes,4,owner)
    call require_record(root,'SPOT-X-GRAM',total_gram,4,owner)
    call require_record(root,'SPOT-X-NID',3,3,owner)
    call LCMGET(root,'SPOT-X-BASIS',data%basis)
    call LCMGET(root,'SPOT-X-A',data%coordinates)
    call LCMGET(root,'SPOT-X-H',data%height)
    call LCMGET(root,'SPOT-X-GRAM',data%gram)
    call LCMGTC(root,'SPOT-X-NID',12,data%norm_id)
    if (data%norm_id /= 'NUFISS-UNIT') &
      call fail(trim(owner)//' INVALID NORMALIZATION ID.')
    if (any(.not.ieee_is_finite(data%basis)).or. &
        any(.not.ieee_is_finite(data%coordinates)).or. &
        any(.not.ieee_is_finite(data%height)).or. &
        any(data%height <= 0.0_real64).or. &
        any(.not.ieee_is_finite(data%gram)).or. &
        any(data%gram <= 0.0_real64)) &
      call fail(trim(owner)//' INVALID CANONICAL GEOMETRY FIELD.')

    if (expect_saved_ra) then
      call require_record(root,'SPOT-X-RA',1,4,owner)
      call LCMGET(root,'SPOT-X-RA',data%saved_ra)
      if ((.not.ieee_is_finite(data%saved_ra)).or. &
          (data%saved_ra < 0.0_real64)) &
        call fail(trim(owner)//' INVALID SAVED SPOT-X-RA.')
    endif
    call LCMCL(root,1)
  end subroutine load_state


  subroutine compare_space(reference,candidate,owner)
    type(axial_state), intent(in) :: reference,candidate
    character(len=*), intent(in) :: owner

    if ((reference%norm_id /= candidate%norm_id).or. &
        any(reference%dims /= candidate%dims).or. &
        any(reference%rank /= candidate%rank).or. &
        any(reference%offset /= candidate%offset).or. &
        any(reference%gram_offset /= candidate%gram_offset).or. &
        any(reference%basis_offset /= candidate%basis_offset)) &
      call fail(trim(owner)//' FIXED-SPACE METADATA DIFFERS BITWISE.')
    if (any(real32_bits(reference%basis) /= &
            real32_bits(candidate%basis)).or. &
        any(real64_bits(reference%height) /= &
            real64_bits(candidate%height)).or. &
        any(real64_bits(reference%gram) /= &
            real64_bits(candidate%gram))) &
      call fail(trim(owner)//' BASIS, HEIGHT, OR GRAM DIFFERS BITWISE.')
  end subroutine compare_space


  subroutine count_signs(values,negative,zero,positive)
    real(real64), intent(in) :: values(:)
    integer, intent(out) :: negative,zero,positive
    integer :: i

    negative=0
    zero=0
    positive=0
    do i=1,size(values)
      if (values(i) < 0.0_real64) then
        negative=negative+1
      else if (values(i) > 0.0_real64) then
        positive=positive+1
      else
        zero=zero+1
      endif
    enddo
  end subroutine count_signs


  subroutine write_metric(scope,name,value)
    character(len=*), intent(in) :: scope,name
    real(real64), intent(in) :: value

    write(6,'(A,3(1X,A),1X,ES25.17E3)') &
      prefix,trim(scope),trim(name),hex64(value),value
  end subroutine write_metric


  subroutine write_decomposition(kind,index,nout_value,nin_value, &
      v_value,q2h_value,qh_value,cross_value,delta_value)
    character(len=*), intent(in) :: kind
    integer, intent(in) :: index
    real(real64), intent(in) :: nout_value,nin_value,v_value
    real(real64), intent(in) :: q2h_value,qh_value,cross_value,delta_value

    write(6,'(A,1X,A,1X,I0,7(1X,A,1X,A,1X,ES25.17E3))') &
      prefix,trim(kind),index, &
      'NOUT-NORM2',hex64(nout_value),nout_value, &
      'NIN-NORM2',hex64(nin_value),nin_value, &
      'V-NORM2',hex64(v_value),v_value, &
      'Q2H-NORM2',hex64(q2h_value),q2h_value, &
      'QH-NORM2',hex64(qh_value),qh_value, &
      'CROSS-U-E',hex64(cross_value),cross_value, &
      'DELTA2',hex64(delta_value),delta_value
  end subroutine write_decomposition


  subroutine require_record(ptr,name,length_expected,type_expected,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length_expected,type_expected
    integer :: length_found,type_found

    call LCMLEN(ptr,name,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) then
      write(0,'(A,1X,A,4(1X,I0))') trim(owner)//' INVALID RECORD', &
        trim(name),length_found,type_found,length_expected,type_expected
      call fail('RECORD CONTRACT FAILURE.')
    endif
  end subroutine require_record


  pure function hex64(value) result(field)
    real(real64), intent(in) :: value
    character(len=18) :: field
    character(len=16) :: digits

    write(digits,'(Z16.16)') real64_bits(value)
    field='0x'//digits
  end function hex64


  pure elemental integer(int32) function real32_bits(value)
    real(real32), intent(in) :: value

    real32_bits=transfer(value,0_int32)
  end function real32_bits


  pure elemental integer(int64) function real64_bits(value)
    real(real64), intent(in) :: value

    real64_bits=transfer(value,0_int64)
  end function real64_bits


  pure elemental logical function negative_zero(value)
    real(real64), intent(in) :: value

    negative_zero=(value == 0.0_real64).and. &
      btest(real64_bits(value),bit_size(0_int64)-1)
  end function negative_zero


  subroutine fail(message)
    character(len=*), intent(in) :: message

    write(0,'(A)') prefix//' ERROR: '//trim(message)
    error stop 2
  end subroutine fail

end program check_inner_sensitivity_v2_ra_geometry_xsm
