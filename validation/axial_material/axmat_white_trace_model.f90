! Conditional angular trace model for the declared rank-one AAA diagnostic.
! This file is separate from the shared solver. No coefficient is CE fitted.
module AXMAT_WHITE_TRACE_MOD
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  private
  logical, save, public :: AXMAT_WHITE_ON=.false.
  integer, save, public :: AXMAT_WHITE_ROW=0
  double precision, save, public :: AXMAT_WHITE_PERIMETER=0.0d0
  logical, save :: reported(370)=.false.
  public :: AXMAT_WHITE_CONFIGURE,AXMAT_WHITE_KERNEL,AXMAT_WHITE_NOTE
contains
  subroutine AXMAT_WHITE_NOTE(group,trace_factor)
    integer, intent(in) :: group
    double precision, intent(in) :: trace_factor
    if (group < 1 .or. group > 370) call XABORT('AXMAT WHITE: INVALID GROUP.')
    if (.not.ieee_is_finite(trace_factor) .or. trace_factor <= 0.0d0) &
      call XABORT('AXMAT WHITE: INVALID DECLARED BOUNDARY TRACE.')
    if (.not.reported(group)) then
      write(*,'(A,I0,A,ES25.16E3)') 'AXMAT-WHITE-APPLY GROUP=',group, &
                                  ' TRACE-FACTOR=',trace_factor
      reported(group)=.true.
    endif
  end subroutine AXMAT_WHITE_NOTE

  subroutine AXMAT_WHITE_CONFIGURE(enable,marker,perimeter,nreg,nfloor, &
                                   nsnap,nlf,iscat,ielem,info)
    logical, intent(in) :: enable
    integer, intent(in) :: marker(4),nreg,nfloor,nsnap,nlf,iscat,ielem
    double precision, intent(in) :: perimeter
    integer, intent(out) :: info
    info=0
    if (.not.enable) then
      if (any(marker /= 0) .or. perimeter /= 0.0d0) then
        info=1
        return
      endif
      AXMAT_WHITE_ON=.false.
      AXMAT_WHITE_ROW=0
      AXMAT_WHITE_PERIMETER=0.0d0
      return
    endif
    if (any(marker /= [1,1,8,3])) then
      info=2
      return
    endif
    if (nreg /= 8 .or. nfloor /= 12 .or. nsnap /= 3 .or. &
        nlf /= 8 .or. iscat /= 3 .or. ielem /= 1) then
      info=3
      return
    endif
    if (.not.ieee_is_finite(perimeter)) then
      info=4
      return
    endif
    ! Fixed physical hexagon; there is no free gap-correction multiplier.
    if (perimeter /= 6.0d0*0.61776479d0) then
      info=5
      return
    endif
    AXMAT_WHITE_ON=.true.
    AXMAT_WHITE_ROW=marker(2)
    AXMAT_WHITE_PERIMETER=perimeter
  end subroutine AXMAT_WHITE_CONFIGURE

  subroutine AXMAT_WHITE_KERNEL(mu,weights,perimeter,area,matrix,info)
    double precision, intent(in) :: mu(:),weights(:),perimeter,area
    double precision, intent(out) :: matrix(:,:)
    integer, intent(out) :: info
    double precision :: s(size(mu)),normalization,prefactor
    integer :: i,j,n
    info=0
    matrix=0.0d0
    n=size(mu)
    if (n < 2 .or. size(weights) /= n .or. size(matrix,1) /= n .or. &
        size(matrix,2) /= n) then
      info=10
      return
    endif
    if (any(.not.ieee_is_finite(mu)) .or. &
        any(.not.ieee_is_finite(weights)) .or. any(abs(mu) >= 1.0d0) .or. &
        any(weights <= 0.0d0)) then
      info=11
      return
    endif
    if (abs(sum(weights)-2.0d0) > 8.0d0*real(epsilon(1.0),8)) then
      info=12
      return
    endif
    if (.not.ieee_is_finite(perimeter) .or. .not.ieee_is_finite(area)) then
      info=13
      return
    endif
    if (perimeter <= 0.0d0 .or. area <= 0.0d0) then
      info=14
      return
    endif
    s=sqrt(1.0d0-mu*mu)
    normalization=dot_product(weights,s)
    prefactor=perimeter/(acos(-1.0d0)*area)
    do j=1,n
      do i=1,n
        matrix(i,j)=-prefactor*s(i)*weights(j)*s(j)/normalization
      enddo
      matrix(j,j)=matrix(j,j)+prefactor*s(j)
    enddo
    if (any(.not.ieee_is_finite(matrix))) info=15
  end subroutine AXMAT_WHITE_KERNEL
end module AXMAT_WHITE_TRACE_MOD
