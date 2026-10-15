program test_generic_rank1_exact_cache_bits
  use, intrinsic :: iso_fortran_env, only : int64
  use SPOT1P64_CACHE_MOD, only : SPOT1P64_CACHE_CLEAR
  use SPOT1P64_R1_GENERIC_CACHE_MOD
  implicit none
  integer,parameter :: nr=3,nz=4,nm=6,ns=3,nq=32,nl=3
  integer :: mat1d(nz),mat(nz,nr),ncode(2),case_id,assertions,calls
  integer :: nb,nruse,nmiss,nfallback,nb0,nr0,nm0,nf0
  integer(int64) :: bytes,limit
  real :: vol1d(nz),total(0:nm),sgas(0:nm,nl),basis(nr,1),vol2d(nr),zcode(2)
  real :: du(nq),w(nq),pl(nl,nq)
  double precision :: radial(nr,ns),q1(1,nl,nz,nr),q2(1,nl,nz,nr)
  double precision :: f(1,nl,nz,nr),c(nz+1,nr),x(nq,nr)
  double precision :: g1(1,nl,nz,nr),g2(1,nl,nz,nr),gm(1,nl,nz,nr)
  double precision :: c1(nz+1,nr),c2(nz+1,nr),cm(nz+1,nr)
  double precision :: x1(nq,nr),x2(nq,nr),xm(nq,nr)
  assertions=0;calls=0
  call SPOT1P64_CACHE_CLEAR()
  do case_id=1,18
    call setup()
    call SPOT1P64_R1_CACHE_CLEAR()
    call solve(q1,g1,c1,x1)
    call solve(q2,g2,c2,x2)
    call mutation(case_id)
    call solve(q2,gm,cm,xm)
    call setup()
    call SPOT1P64_R1_CACHE_BEGIN(1,368_int64*1024_int64*1024_int64)
    call solve(q1,f,c,x)
    call equal_fields(f,c,x,g1,c1,x1)
    call SPOT1P64_R1_CACHE_STATS(nb0,nr0,nm0,nf0,bytes,limit)
    call check(nb0==nz+1.and.nr0==0.and.nm0==1.and.nf0==0)
    call check(bytes<=limit.and.limit==368_int64*1024_int64*1024_int64)
    call check(SPOT1P64_R1_PLAN(1)%compressed)
    call solve(q2,f,c,x)
    call equal_fields(f,c,x,g2,c2,x2)
    call SPOT1P64_R1_CACHE_STATS(nb,nruse,nmiss,nfallback,bytes,limit)
    call check(nb==nb0.and.nruse==nz+1.and.nmiss==1.and.nfallback==0)
    call mutation(case_id)
    call solve(q2,f,c,x)
    call equal_fields(f,c,x,gm,cm,xm)
    call SPOT1P64_R1_CACHE_STATS(nb,nruse,nmiss,nfallback,bytes,limit)
    call check(nb==2*(nz+1).and.nruse==nz+1.and.nmiss==2.and.nfallback==0)
    call check(bytes<=limit)
  enddo
  call setup()
  call SPOT1P64_R1_CACHE_CLEAR()
  call solve(q1,g1,c1,x1)
  call SPOT1P64_R1_CACHE_BEGIN(1,1_int64)
  call solve(q1,f,c,x)
  call equal_fields(f,c,x,g1,c1,x1)
  call SPOT1P64_R1_CACHE_STATS(nb,nruse,nmiss,nfallback,bytes,limit)
  call check(nb==0.and.nruse==0)
  call storage_checks()
  call SPOT1P64_R1_CACHE_CLEAR()
  write(*,'(A,I0,A,I0,A)') &
    '{"status":"ACTUAL_GENERIC_RANK1_COMPONENT_BIT_CONTROLS_COMPLETED_ONLY","actual_assertions":', &
    assertions,',"actual_SPOT1P64_calls":',calls, &
    ',"formal_SN32_quadrature_equivalence":false,"genuine_solver_qualified":false,'// &
    '"physics_qualified":false,"AAA_qualified":false,"ABA_admitted":false,"goal_complete":false}'
contains
  subroutine check(ok)
    logical,intent(in) :: ok
    if (.not.ok) call XABORT('R1 EXACT CONTROL: ACTUAL ASSERTION FAILED.')
    assertions=assertions+1
  end subroutine
  subroutine setup()
    integer :: i,j,l,n
    mat1d=[1,2,3,1];vol1d=[1.0,1.25,0.75,1.5];vol2d=[1.0,2.0,3.0]
    basis(:,1)=[0.5,-0.25,0.75];ncode=[1,1];zcode=[0.2,0.1]
    do i=1,nz
      do j=1,nr
        mat(i,j)=mod(i+j-2,nm)+1
      enddo
    enddo
    total(0)=0.0;sgas(0,:)=0.0
    do i=1,nm
      total(i)=1.0+real(i)*0.03125
      sgas(i,1)=0.2+real(i)*0.001953125
      sgas(i,2)=0.03125;sgas(i,3)=0.015625
    enddo
    do n=1,nq/2
      du(n)=real(n)/real(nq/2+1);du(n+nq/2)=-du(n)
    enddo
    w=1.0/real(nq/2)
    call legendre()
    do j=1,ns
      do i=1,nr
        radial(i,j)=0.02d0+dble(i+j)*0.001953125d0
      enddo
    enddo
    do j=1,nr
      do i=1,nz
        do l=1,nl
          q1(1,l,i,j)=0.0625d0*dble(i+j)/(dble(l)+1.0d0)
        enddo
      enddo
    enddo
    q1(1,2,:,:)=-q1(1,2,:,:);q2=q1*0.875d0
  end subroutine
  subroutine legendre()
    pl(1,:)=1.0;pl(2,:)=du;pl(3,:)=(3.0*du*du-1.0)/2.0
  end subroutine
  subroutine mutation(which)
    integer,intent(in) :: which
    select case(which)
    case(1);total(0)=0.03125
    case(2);total(1)=total(1)+0.03125
    case(3);sgas(0,1)=0.03125
    case(4);sgas(1,1)=sgas(1,1)+0.00390625
    case(5);sgas(1,2)=sgas(1,2)+0.00390625
    case(6);sgas(1,3)=sgas(1,3)+0.00390625
    case(7);basis(1,1)=basis(1,1)+0.015625
    case(8);vol1d(1)=vol1d(1)+0.125
    case(9);vol2d(1)=vol2d(1)+0.125
    case(10);radial(1,1)=radial(1,1)+0.001953125d0
    case(11);mat1d(1)=2
    case(12);mat(1,1)=6
    case(13)
      du(1)=du(1)+0.001953125;du(1+nq/2)=-du(1);call legendre()
    case(14);w(1)=w(1)+0.001953125;w(1+nq/2)=w(1)
    case(15);pl(2,1)=pl(2,1)+0.015625
    case(16);ncode(1)=7
    case(17);zcode(1)=zcode(1)+0.03125
    case(18);ncode(2)=2;zcode(2)=0.5
    case default;call XABORT('R1 EXACT CONTROL: BAD CASE.')
    end select
  end subroutine
  subroutine solve(q,ff,cc,xx)
    double precision,intent(in) :: q(1,nl,nz,nr)
    double precision,intent(out) :: ff(1,nl,nz,nr),cc(nz+1,nr),xx(nq,nr)
    call SPOT1P64(1,nr,nz,1,nm,ns,1,1,nq,nl,.false.,mat1d,vol1d,mat,total,sgas, &
      basis,vol2d,radial,ncode,zcode,q,du,w,pl,ff,cc,xx)
    calls=calls+1
  end subroutine
  subroutine equal_fields(ff,cc,xx,gg,dd,yy)
    double precision,intent(in) :: ff(1,nl,nz,nr),gg(1,nl,nz,nr),cc(nz+1,nr),dd(nz+1,nr)
    double precision,intent(in) :: xx(nq,nr),yy(nq,nr)
    call check(all(transfer(ff,[0_int64])==transfer(gg,[0_int64])))
    call check(all(transfer(cc,[0_int64])==transfer(dd,[0_int64])))
    call check(all(transfer(xx,[0_int64])==transfer(yy,[0_int64])))
  end subroutine
  subroutine storage_checks()
    double precision :: low(nq,nq,nz+1),restored(nq,nq)
    double precision :: mm(1,1),tm(1,1,nz),rm(1,1,nz),sm(1,1,nl,nz)
    double precision :: mn(nq,nl),dn(nl,nq)
    integer :: opp(nq),n,j,k,test
    logical :: candidate,hit,store
    call setup()
    mm=1.0d0;tm=1.0d0;rm=0.03125d0;sm=0.015625d0;mn=0.125d0;dn=0.25d0
    do n=1,nq/2
      opp(n)=n+nq/2;opp(n+nq/2)=n
    enddo
    do test=1,4
      call SPOT1P64_R1_CACHE_BEGIN(1,368_int64*1024_int64*1024_int64)
      if (test==4) call SPOT1P64_R1_CACHE_BEGIN(1,110000_int64)
      call SPOT1P64_R1_TRY(1,nr,nz,1,nm,ns,1,1,nq,nl,.false.,.false.,mat1d,mat, &
        ncode,opp,vol1d,total,sgas,basis,vol2d,zcode,du,w,pl,radial,mm,tm,rm,sm,mn,dn, &
        0.2d0,0.1d0,candidate,hit)
      call check(candidate.and..not.hit)
      low=0.0d0
      do k=2,nz+1
        do j=1,nq
          do n=1,nq/2
            low(n,j,k)=dble(n+j+k)*0.001953125d0
          enddo
        enddo
      enddo
      if (test==2) low(nq,1,2)=transfer(-huge(0_int64)-1_int64,0.0d0)
      if (test>=3) low(nq,1,2)=0.001953125d0
      call SPOT1P64_R1_STORE_BEGIN(1,low,du,store)
      if (test==4) then
        call check(.not.store)
        call SPOT1P64_R1_CACHE_STATS(nb,nruse,nmiss,nfallback,bytes,limit)
        call check(nfallback==1.and.bytes<=limit)
      else
        call check(store)
        call check(SPOT1P64_R1_PLAN(1)%compressed.eqv.(test==1))
        do k=1,nz+1
          call SPOT1P64_R1_LOWER(1,k,restored)
          call check(all(transfer(restored,[0_int64])==transfer(low(:,:,k),[0_int64])))
        enddo
      endif
    enddo
  end subroutine
end program

subroutine XABORT(message)
  use, intrinsic :: iso_fortran_env, only : error_unit
  implicit none
  character(len=*),intent(in) :: message
  write(error_unit,'(A)') trim(message)
  error stop 1
end subroutine XABORT
