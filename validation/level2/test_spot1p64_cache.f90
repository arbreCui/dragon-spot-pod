program test_spot1p64_cache
  use, intrinsic :: iso_fortran_env, only : error_unit,int64,real64
  use SPOT1P64_CACHE_MOD, only : SPOT1P64_CACHE_BEGIN, &
    SPOT1P64_CACHE_CLEAR,SPOT1P64_CACHE_STATS, &
    SPOT1P64_FACTOR64,SPOT1P64_SOLVE64
  implicit none
  integer, parameter :: dp=real64
  integer, parameter :: nr=2,nz=2,nm=2,nq=4,nl=1
  integer :: failures,nfactor,nreuse,info_legacy,info_split
  integer :: pivot3(3),pivot1(1),pivot_singular(2)
  integer :: mat(nz,nr),mat1d(nz),ncode(2)
  real :: dz(nz),total(0:nm),scatter(0:nm,nl),vol(nr)
  real :: basis(nr,nr),basis_dense(nr,nr),zcode(2)
  real :: mu(nq),sn_weight(nq),pl(nl,nq)
  real(dp) :: a3(3,3),factor3(3,3),rhs3(3,2),split3(3,2)
  real(dp) :: legacy3(3,5),pivot_value3(3)
  real(dp) :: a1(1,1),factor1(1,1),rhs1(1,2),split1(1,2)
  real(dp) :: legacy1(1,3),pivot_value1(1)
  real(dp) :: singular(2,2),pivot_value_singular(2)
  real(dp) :: radial(nr,1),source_a(1,nl,nz,nr)
  real(dp) :: source_b(1,nl,nz,nr)
  real(dp) :: flux_ref_a(1,nl,nz,nr),flux_ref_b(1,nl,nz,nr)
  real(dp) :: flux_cache_a(1,nl,nz,nr),flux_cache_b(1,nl,nz,nr)
  real(dp) :: cour_ref_a(nz+1,nr),cour_ref_b(nz+1,nr)
  real(dp) :: cour_cache_a(nz+1,nr),cour_cache_b(nz+1,nr)
  real(dp) :: xnei_ref_a(nq,nr),xnei_ref_b(nq,nr)
  real(dp) :: xnei_cache_a(nq,nr),xnei_cache_b(nq,nr)

  failures=0

  ! The split factor/solve must reproduce ALSBD for finite nonsingular
  ! systems, including a first-column pivot swap and multiple right sides.
  a3(1,:)=[0.5_dp,2.0_dp,-1.0_dp]
  a3(2,:)=[4.0_dp,-1.0_dp,0.25_dp]
  a3(3,:)=[-2.0_dp,3.0_dp,5.0_dp]
  rhs3(1,:)=[1.0_dp,-2.0_dp]
  rhs3(2,:)=[3.0_dp,0.5_dp]
  rhs3(3,:)=[-1.0_dp,4.0_dp]
  legacy3(:,:3)=a3
  legacy3(:,4:5)=rhs3
  call ALSBD(3,2,legacy3,info_legacy,3)
  factor3=a3
  split3=rhs3
  call SPOT1P64_FACTOR64(factor3,pivot3,pivot_value3,info_split)
  call assert_true('split factor status matches ALSBD', &
                   info_split == info_legacy,failures)
  call SPOT1P64_SOLVE64(factor3,pivot3,pivot_value3,split3,info_split)
  call assert_true('split solve status matches ALSBD', &
                   info_split == info_legacy,failures)
  call assert_true('split coefficient factor is bitwise ALSBD', &
                   all(same_bits(factor3,legacy3(:,:3))),failures)
  call assert_true('split multiple RHS is bitwise ALSBD', &
                   all(same_bits(split3,legacy3(:,4:5))),failures)

  a1(1,1)=2.5_dp
  rhs1(1,:)=[-1.0_dp,3.0_dp]
  legacy1(:,1)=a1(:,1)
  legacy1(:,2:3)=rhs1
  call ALSBD(1,2,legacy1,info_legacy,1)
  factor1=a1
  split1=rhs1
  call SPOT1P64_FACTOR64(factor1,pivot1,pivot_value1,info_split)
  call SPOT1P64_SOLVE64(factor1,pivot1,pivot_value1,split1,info_split)
  call assert_true('split order-one RHS is bitwise ALSBD', &
                   info_split == info_legacy .and. &
                   all(same_bits(split1,legacy1(:,2:3))),failures)

  singular=reshape([1.0_dp,2.0_dp,2.0_dp,4.0_dp],[2,2])
  call SPOT1P64_FACTOR64(singular,pivot_singular, &
                         pivot_value_singular,info_split)
  call assert_true('split factor rejects an exactly singular matrix', &
                   info_split == 1,failures)

  dz=[1.2,0.8]
  total=[0.0,1.10,0.82]
  scatter=0.0
  scatter(1,1)=0.23
  scatter(2,1)=0.11
  mat(:,1)=1
  mat(:,2)=2
  mat1d=1
  mu=[0.86113631,0.33998104,-0.33998104,-0.86113631]
  sn_weight=[0.34785485,0.65214515,0.65214515,0.34785485]
  pl=1.0
  vol=[1.0,3.0]
  radial(:,1)=[0.08_dp,-0.03_dp]
  basis=0.0
  basis(1,1)=1.0/sqrt(vol(1)/sum(vol))
  basis(2,2)=1.0/sqrt(vol(2)/sum(vol))
  basis_dense(1,:)=[basis(1,1)/sqrt(2.0),basis(1,1)/sqrt(2.0)]
  basis_dense(2,:)=[basis(2,2)/sqrt(2.0),-basis(2,2)/sqrt(2.0)]
  ncode=[1,1]
  zcode=0.0
  source_a=0.0_dp
  source_a(1,1,1,1)=1.0_dp
  source_a(1,1,2,1)=0.7_dp
  source_a(1,1,1,2)=0.4_dp
  source_a(1,1,2,2)=1.3_dp
  source_b=1.25_dp*source_a
  source_b(1,1,1,2)=source_b(1,1,1,2)+0.125_dp
  call assert_true('changed RHS fixture differs bitwise', &
                   any(.not.same_bits(source_a,source_b)),failures)

  ! Default-off calls are the unmodified ALSBD reference.
  call SPOT1P64_CACHE_CLEAR()
  call solve_spot(source_a,basis,flux_ref_a,cour_ref_a,xnei_ref_a)
  call solve_spot(source_b,basis,flux_ref_b,cour_ref_b,xnei_ref_b)
  call assert_true('changed RHS changes the reference solution', &
    any(.not.same_bits(flux_ref_a,flux_ref_b)) .or. &
    any(.not.same_bits(cour_ref_a,cour_ref_b)) .or. &
    any(.not.same_bits(xnei_ref_a,xnei_ref_b)),failures)

  ! The first physical call builds exact factors; the changed second RHS
  ! must reuse them while still producing the corresponding new solution.
  call SPOT1P64_CACHE_BEGIN(1,.true.)
  call solve_spot(source_a,basis,flux_cache_a,cour_cache_a,xnei_cache_a)
  call SPOT1P64_CACHE_STATS(nfactor,nreuse)
  call assert_true('first physical solve only builds fixed LHS blocks', &
                   nfactor == nr*(nz+1) .and. nreuse == 0,failures)
  call solve_spot(source_b,basis,flux_cache_b,cour_cache_b,xnei_cache_b)
  call SPOT1P64_CACHE_STATS(nfactor,nreuse)
  call assert_true('physical cache builds each axial block exactly once', &
                   nfactor == nr*(nz+1),failures)
  call assert_true('physical cache reuses each block for changed RHS', &
                   nreuse == nr*(nz+1),failures)
  call assert_true('first cached physical solve is bitwise reference', &
    all(same_bits(flux_cache_a,flux_ref_a)) .and. &
    all(same_bits(cour_cache_a,cour_ref_a)) .and. &
    all(same_bits(xnei_cache_a,xnei_ref_a)),failures)
  call assert_true('reused-factor physical solve is bitwise reference', &
    all(same_bits(flux_cache_b,flux_ref_b)) .and. &
    all(same_bits(cour_cache_b,cour_ref_b)) .and. &
    all(same_bits(xnei_cache_b,xnei_ref_b)),failures)

  ! Even inside an enabled lifecycle, an ordinary dense POD basis stays on
  ! the original ALSBD path and does not populate the physical cache.
  call SPOT1P64_CACHE_CLEAR()
  call solve_spot(source_a,basis_dense,flux_ref_a,cour_ref_a,xnei_ref_a)
  call SPOT1P64_CACHE_BEGIN(1,.true.)
  call solve_spot(source_a,basis_dense,flux_cache_a,cour_cache_a,xnei_cache_a)
  call SPOT1P64_CACHE_STATS(nfactor,nreuse)
  call assert_true('ordinary POD basis bypasses physical factor cache', &
                   nfactor == 0 .and. nreuse == 0,failures)
  call assert_true('ordinary POD solve is bitwise unchanged', &
    all(same_bits(flux_cache_a,flux_ref_a)) .and. &
    all(same_bits(cour_cache_a,cour_ref_a)) .and. &
    all(same_bits(xnei_cache_a,xnei_ref_a)),failures)
  call SPOT1P64_CACHE_CLEAR()
  call SPOT1P64_CACHE_STATS(nfactor,nreuse)
  call assert_true('cache clear resets its FLU-local lifecycle', &
                   nfactor == 0 .and. nreuse == 0,failures)

  if (failures /= 0) then
    write(error_unit,'(a,i0)') 'SPOT1P64 CACHE FAILURES: ',failures
    error stop 1
  endif
  write(*,'(a)') 'LEVEL2 PASS: exact SPOT1P64 physical factor reuse'

contains

  subroutine solve_spot(source,basis_in,flux,cour,xnei)
    real(dp), intent(in) :: source(1,nl,nz,nr)
    real, intent(in) :: basis_in(nr,nr)
    real(dp), intent(out) :: flux(1,nl,nz,nr),cour(nz+1,nr),xnei(nq,nr)
    call SPOT1P64(1,nr,nz,1,nm,1,nr,1,nq,nl,.false., &
      mat1d,dz,mat,total,scatter,basis_in,vol,radial,ncode,zcode, &
      source,mu,sn_weight,pl,flux,cour,xnei)
  end subroutine solve_spot

  pure elemental logical function same_bits(a,b)
    real(dp), intent(in) :: a,b
    same_bits=transfer(a,0_int64) == transfer(b,0_int64)
  end function same_bits

  subroutine assert_true(label,condition,count)
    character(*), intent(in) :: label
    logical, intent(in) :: condition
    integer, intent(inout) :: count
    if (condition) then
      write(*,'(a)') 'PASS: '//label
    else
      write(error_unit,'(a)') 'FAIL: '//label
      count=count+1
    endif
  end subroutine assert_true
end program test_spot1p64_cache

subroutine XABORT(message)
  character(*), intent(in) :: message
  write(*,'(a)') 'XABORT: '//message
  error stop 2
end subroutine XABORT
