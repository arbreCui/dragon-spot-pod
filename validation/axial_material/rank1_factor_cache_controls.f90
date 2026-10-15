! Future unit controls only. Synthetic operators; unchanged native ALGPT
! quadrature. No transport, scientific qualification, or performance claim.
! Every returned value is archived before the external Python numerical gate.
module rank1_control_abort
  implicit none
  logical, save :: expect_rejection=.false.
  character(len=*), parameter :: identity_message= &
    'SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.'
  character(len=*), parameter :: cap_message= &
    'SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.'
  character(len=160), save :: expected_message=identity_message
end module rank1_control_abort

program rank1_factor_cache_controls
  use, intrinsic :: iso_fortran_env, only: int32,int64
  use SPOT1P64_CACHE_MOD
  use AXMAT_ORIGINAL_CACHE_MOD, only: ORIGINAL_BEGIN=>SPOT1P64_CACHE_BEGIN, &
    ORIGINAL_CLEAR=>SPOT1P64_CACHE_CLEAR
  use AXMAT_WHITE_TRACE_MOD, only: AXMAT_WHITE_ON,AXMAT_WHITE_ROW,AXMAT_WHITE_PERIMETER
  use rank1_control_abort
  implicit none
  integer :: nr,nh,nq,nl,nm,nmat,nsnap,manifest,group,rhs,i,j,k,l,unit
  integer :: ncode(2),info
  integer, allocatable :: mat1d(:),mat(:,:)
  real, allocatable :: dz(:),total(:),sgas(:,:),basis(:,:),volume(:),du(:),w(:),pl(:,:)
  double precision, allocatable :: radial(:,:),q(:,:,:,:),flux(:,:,:,:),cour(:,:),xnei(:,:)
  real :: zcode(2)
  character(len=80) :: mode,mutation,label
  character(len=1024) :: record,path
  integer(int64) :: built,reused,hits,live,peak,cap,header(12)
  integer(int64) :: requested_bytes,operation_code
  integer :: legacy_built,legacy_reused
  interface
    subroutine SPOT1P64(ig,nr,nh,ie,nmat,nsnap,nm,ischm,nq,nl,fixup, &
                        mat1d,dz,mat,total,sgas,basis,volume,radial,ncode,zcode,q,du,w,pl,f,c,x)
      integer :: ig,nr,nh,ie,nmat,nsnap,nm,ischm,nq,nl,mat1d(nh),mat(nh,nr),ncode(2)
      logical :: fixup
      real :: dz(nh),total(0:nmat),sgas(0:nmat,nl),basis(nr,nm),volume(nr),zcode(2)
      real :: du(nq),w(nq),pl(nl,nq)
      double precision :: radial(nr,nsnap),q(ie,nl,nh,nr),f(ie,nl,nh,nr),c(nh+1,nr),x(nq,nr)
    end subroutine SPOT1P64
    subroutine SPOT1P64_ORIGINAL(ig,nr,nh,ie,nmat,nsnap,nm,ischm,nq,nl,fixup, &
                        mat1d,dz,mat,total,sgas,basis,volume,radial,ncode,zcode,q,du,w,pl,f,c,x)
      integer :: ig,nr,nh,ie,nmat,nsnap,nm,ischm,nq,nl,mat1d(nh),mat(nh,nr),ncode(2)
      logical :: fixup
      real :: dz(nh),total(0:nmat),sgas(0:nmat,nl),basis(nr,nm),volume(nr),zcode(2)
      real :: du(nq),w(nq),pl(nl,nq)
      double precision :: radial(nr,nsnap),q(ie,nl,nh,nr),f(ie,nl,nh,nr),c(nh+1,nr),x(nq,nr)
    end subroutine SPOT1P64_ORIGINAL
  end interface

  call get_command_argument(1,mode)
  if (storage_size(0) /= 32 .or. storage_size(0.0) /= 32 .or. storage_size(0.0d0) /= 64) stop 2
  open(newunit=manifest,file='manifest.jsonl',status='new',action='write')
  select case(trim(mode))
  case('positive')
    call fixture('production_white_370',8,48,32,3,1,370,.true.,.false.,.true.,0)
    call fixture('signed_nonunit',8,48,32,3,1,2,.false.,.false.,.true.,0)
    call fixture('lifecycle_reset_1',8,48,32,3,1,2,.false.,.false.,.true.,0)
    call fixture('lifecycle_reset_2',8,48,32,3,1,2,.false.,.false.,.true.,1)
    call fixture('legacy_physical',2,3,8,3,2,2,.false.,.true.,.false.,0)
    call fixture('legacy_dense',2,3,8,3,2,2,.false.,.false.,.false.,0)
    call fixture('legacy_translation',8,3,8,3,1,2,.false.,.false.,.false.,0,.true.)
    call pivot_control()
    call SPOT1P64_CACHE_CLEAR()
    call ORIGINAL_CLEAR()
    call SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)
    write(manifest,'(A)') '{"kind":"clear","built":'//number(built)//',"reused":'// &
      number(reused)//',"hits":'//number(hits)//',"live":'//number(live)//',"peak":'//number(peak)//'}'
    close(manifest)
    write(*,'(A)') 'RAW_CONTROLS_COMPLETE'
  case('negative')
    call get_command_argument(2,mutation)
    select case(trim(mutation))
    case('total','selfscat','radial','basis','mesh','du','weights','pl','boundary', &
         'signed_zero','white_on','white_row','white_perimeter','dims')
    case default
      stop 2
    end select
    label='negative_'//trim(mutation)
    call configure(8,48,32,3,1,.true.,.false.,.false.,0)
    call ORIGINAL_BEGIN(2,.false.)
    call SPOT1P64_CACHE_BEGIN(2,.false.,.true.)
    group=1
    rhs=1
    call source(rhs)
    call save_input(trim(label)//'_prime')
    call solve(.false.)
    call save_result(trim(label),'prime',group,rhs,trim(label)//'_prime.inputs.bin')
    select case(trim(mutation))
    case('total'); total(1)=total(1)+0.125
    case('selfscat'); sgas(1,2)=sgas(1,2)+0.0078125
    case('radial'); radial(1,1)=radial(1,1)+0.0078125d0
    case('basis'); basis(2,1)=-basis(2,1)
    case('mesh'); dz(1)=dz(1)+0.125
    case('du'); du(1)=du(1)+0.0078125
    case('weights'); w(1)=w(1)+0.0078125
    case('pl'); pl(2,1)=pl(2,1)+0.0078125
    case('boundary'); ncode(1)=2
    case('signed_zero'); total(0)=transfer(int(z'80000000',int32),0.0)
    case('white_on'); AXMAT_WHITE_ON=.false.
    case('white_row'); AXMAT_WHITE_ROW=2
    case('white_perimeter'); AXMAT_WHITE_PERIMETER=AXMAT_WHITE_PERIMETER+0.0078125d0
    case('dims')
      nm=2
      deallocate(basis)
      allocate(basis(nr,nm))
      basis(:,1)=1.25
      basis(:,2)=0.5
    end select
    call save_input(trim(label)//'_mutated')
    write(manifest,'(A)') '{"kind":"negative_expected","case":"'//trim(mutation)// &
      '","expected_XABORT":"'//identity_message//'"}'
    flush(manifest)
    close(manifest)
    expected_message=identity_message
    expect_rejection=.true.
    call solve(.false.)
    ! A normal return must never be re-labelled as successful rejection.
    open(newunit=unit,file='unexpected_return.txt',status='new',action='write')
    write(unit,'(A)') 'Actual kernel unexpectedly returned after operator mutation.'
    close(unit)
    stop 1
  case('cap-negative')
    call get_command_argument(2,mutation)
    select case(trim(mutation))
    case('cap_reserve','cap_factor_dimensions')
    case default
      stop 2
    end select
    call SPOT1P64_CACHE_BEGIN(370,.false.,.true.)
    call SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)
    requested_bytes=0_int64
    operation_code=2_int64
    header=[1_int64,operation_code,370_int64,int(huge(0),int64),49_int64, &
      requested_bytes,built,reused,hits,live,peak,cap]
    if (trim(mutation) == 'cap_reserve') then
      operation_code=1_int64
      requested_bytes=cap-live+1_int64
      header=[1_int64,operation_code,370_int64,0_int64,0_int64, &
        requested_bytes,built,reused,hits,live,peak,cap]
    endif
    open(newunit=unit,file='cap_request.bin',status='new',action='write', &
         form='unformatted',access='stream',convert='little_endian')
    write(unit) header
    close(unit)
    write(manifest,'(A)') '{"kind":"resource_negative_expected","case":"'//trim(mutation)// &
      '","file":"cap_request.bin","expected_XABORT":"'//cap_message//'","operation":'// &
      number(operation_code)//',"requested_bytes":'//number(requested_bytes)//',"live":'// &
      number(live)//',"peak":'//number(peak)//',"cap":'//number(cap)//'}'
    flush(manifest)
    close(manifest)
    expected_message=cap_message
    expect_rejection=.true.
    if (trim(mutation) == 'cap_reserve') then
      call SPOT1P64_RANK1_RESERVE(requested_bytes)
    else
      ! No factor array is allocated: the actual checked-dimension guard
      ! must reject this default-INTEGER extreme before multiplication.
      call SPOT1P64_RANK1_FACTORS(1,huge(0),49)
    endif
    open(newunit=unit,file='unexpected_return.txt',status='new',action='write')
    write(unit,'(A)') 'Actual resource guard unexpectedly returned.'
    close(unit)
    stop 1
  case default
    stop 2
  end select

contains
  function number(value) result(text)
    integer(int64), intent(in) :: value
    character(len=:), allocatable :: text
    character(len=40) :: tmp
    write(tmp,'(I0)') value
    text=trim(tmp)
  end function number

  subroutine release_fixture()
    if (allocated(mat1d)) deallocate(mat1d,mat,dz,total,sgas,basis,volume,du,w,pl,radial,q,flux,cour,xnei)
  end subroutine release_fixture

  subroutine configure(nr_in,nh_in,nq_in,nl_in,nm_in,white,physical,signed_basis,variant,cyclic)
    integer, intent(in) :: nr_in,nh_in,nq_in,nl_in,nm_in,variant
    logical, intent(in) :: white,physical,signed_basis
    logical, optional, intent(in) :: cyclic
    double precision :: area
    call release_fixture()
    nr=nr_in; nh=nh_in; nq=nq_in; nl=nl_in; nm=nm_in
    nmat=3; nsnap=3
    allocate(mat1d(nh),mat(nh,nr),dz(nh),total(0:nmat),sgas(0:nmat,nl))
    allocate(basis(nr,nm),volume(nr),du(nq),w(nq),pl(nl,nq),radial(nr,nsnap))
    allocate(q(1,nl,nh,nr),flux(1,nl,nh,nr),cour(nh+1,nr),xnei(nq,nr))
    AXMAT_WHITE_ON=white
    AXMAT_WHITE_ROW=1
    AXMAT_WHITE_PERIMETER=6.0d0*0.61776479d0
    area=sqrt(3.0d0)*AXMAT_WHITE_PERIMETER**2/24.0d0
    volume=real(area/real(nr,8))
    dz=150.0/real(nh)
    do k=1,nh
      mat1d(k)=min(3,1+(k-1)*3/nh)
      mat(k,:)=mat1d(k)
    enddo
    total(0)=0.0
    sgas=0.0
    do i=1,nmat
      total(i)=1.0+0.125*real(i)+0.0625*real(variant)
      sgas(i,1)=0.125
      sgas(i,2)=0.015625
      sgas(i,3)=0.0078125
    enddo
    basis=0.0
    do j=1,nm
      do i=1,nr
        basis(i,j)=1.0+0.0625*real(i)+0.03125*real(j)
        if (signed_basis.and.mod(i,2) == 0) basis(i,j)=-basis(i,j)
      enddo
    enddo
    if (physical) then
      basis=0.0
      do i=1,nr
        basis(i,i)=1.25+0.125*real(i)
      enddo
    else if (nm > 1) then
      basis(1,1)=1.25; basis(2,1)=0.5
      basis(1,2)=-0.375; basis(2,2)=1.5
    endif
    radial=0.03125d0
    call ALGPT(nq,-1.0,1.0,du,w)
    do i=1,nq
      pl(1,i)=1.0
      pl(2,i)=du(i)
      do l=2,nl-1
        pl(l+1,i)=((2.0*l-1.0)*du(i)*pl(l,i)-(l-1)*pl(l-1,i))/l
      enddo
    enddo
    ncode=1; zcode=0.0
    if (present(cyclic)) then
      if (cyclic) then
        ncode=4; zcode=1.0
      endif
    endif
  end subroutine configure

  subroutine source(which)
    integer, intent(in) :: which
    do i=1,nr
      do k=1,nh
        q(1,1,k,i)=0.125d0+real(which,8)/32.0d0+real(i+k,8)/1024.0d0
        q(1,2,k,i)=real(which,8)/512.0d0
        q(1,3,k,i)=-real(which,8)/1024.0d0
      enddo
    enddo
  end subroutine source

  subroutine solve(original)
    logical, intent(in) :: original
    if (original) then
      call SPOT1P64_ORIGINAL(group,nr,nh,1,nmat,nsnap,nm,1,nq,nl,.false., &
        mat1d,dz,mat,total,sgas,basis,volume,radial,ncode,zcode,q,du,w,pl,flux,cour,xnei)
    else
      call SPOT1P64(group,nr,nh,1,nmat,nsnap,nm,1,nq,nl,.false., &
        mat1d,dz,mat,total,sgas,basis,volume,radial,ncode,zcode,q,du,w,pl,flux,cour,xnei)
    endif
  end subroutine solve

  subroutine save_input(name)
    character(len=*), intent(in) :: name
    integer :: out
    integer(int64) :: input_header(12)
    input_header=[1_int64,int(nr,int64),int(nh,int64),int(nq,int64),int(nl,int64), &
      int(nm,int64),int(nmat,int64),int(nsnap,int64),int(AXMAT_WHITE_ROW,int64), &
      int(merge(1,0,AXMAT_WHITE_ON),int64),0_int64,0_int64]
    open(newunit=out,file=trim(name)//'.inputs.bin',status='new',action='write', &
         form='unformatted',access='stream',convert='little_endian')
    write(out) input_header,mat1d,mat,dz,total,sgas,basis,volume,radial,ncode,zcode,du,w,pl
    write(out) AXMAT_WHITE_PERIMETER
    close(out)
  end subroutine save_input

  subroutine save_result(name,role,ig,which,input_name)
    character(len=*), intent(in) :: name,role
    integer, intent(in) :: ig,which
    character(len=*), optional, intent(in) :: input_name
    integer :: out
    character(len=:), allocatable :: stem,input_path
    stem=trim(name)//'_g'//number(int(ig,int64))//'_r'//number(int(which,int64))//'_'//trim(role)
    input_path=trim(name)//'_g'//number(int(ig,int64))//'.inputs.bin'
    if (present(input_name)) input_path=input_name
    header=[1_int64,int(nr,int64),int(nh,int64),int(nq,int64),int(nl,int64),int(nm,int64), &
      int(ig,int64),int(which,int64),int(size(flux),int64),int(size(cour),int64), &
      int(size(xnei),int64),0_int64]
    open(newunit=out,file=stem//'.bin',status='new',action='write', &
         form='unformatted',access='stream',convert='little_endian')
    write(out) header,flux,cour,xnei
    close(out)
    open(newunit=out,file=stem//'.q.bin',status='new',action='write', &
         form='unformatted',access='stream',convert='little_endian')
    write(out) q
    close(out)
    call SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)
    call SPOT1P64_CACHE_STATS(legacy_built,legacy_reused)
    write(manifest,'(A)') '{"kind":"field","case":"'//trim(name)//'","role":"'//trim(role)// &
      '","file":"'//stem//'.bin","q_file":"'//stem//'.q.bin","input_file":"'//input_path// &
      '","group":'//number(int(ig,int64))// &
      ',"rhs":'//number(int(which,int64))//',"built":'//number(built)//',"reused":'//number(reused)// &
      ',"hits":'//number(hits)//',"live":'//number(live)//',"peak":'//number(peak)//',"cap":'//number(cap)// &
      ',"legacy_built":'//number(int(legacy_built,int64))// &
      ',"legacy_reused":'//number(int(legacy_reused,int64))//'}'
    flush(manifest)
  end subroutine save_result

  subroutine fixture(name,rr,hh,qq,ll,mm,groups,white,physical,signed_basis,variant,cyclic)
    character(len=*), intent(in) :: name
    integer, intent(in) :: rr,hh,qq,ll,mm,groups,variant
    logical, intent(in) :: white,physical,signed_basis
    logical, optional, intent(in) :: cyclic
    logical :: is_cyclic
    is_cyclic=.false.
    if (present(cyclic)) is_cyclic=cyclic
    call configure(rr,hh,qq,ll,mm,white,physical,signed_basis,variant,is_cyclic)
    call ORIGINAL_BEGIN(groups,physical)
    call SPOT1P64_CACHE_BEGIN(groups,physical,.not.physical)
    call save_input(name)
    do group=1,groups
      total(1)=1.125+0.0625*real(variant)+real(group)/8192.0
      call save_input(trim(name)//'_g'//number(int(group,int64)))
      do rhs=1,3
        call source(rhs)
        call solve(.true.)
        call save_result(name,'original',group,rhs)
        call solve(.false.)
        if (rhs == 1) then
          call save_result(name,'build',group,rhs)
        else
          call save_result(name,'reuse',group,rhs)
        endif
      enddo
    enddo
    call SPOT1P64_RANK1_TERMINAL()
    call SPOT1P64_CACHE_CLEAR()
    call ORIGINAL_CLEAR()
    call SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)
    write(manifest,'(A)') '{"kind":"clear","case":"'//trim(name)//'","built":'//number(built)// &
      ',"reused":'//number(reused)//',"hits":'//number(hits)//',"live":'//number(live)//',"peak":'//number(peak)//'}'
    flush(manifest)
  end subroutine fixture

  subroutine pivot_control()
    double precision :: matrix(4,4),augmented(4,7),factor(4,4),values(4),right(4,3)
    integer :: pivots(4),result_info,out
    matrix(1,:)=[0.0d0,2.0d0,1.0d0,0.0d0]
    matrix(2,:)=[2.0d0,1.0d0,0.0d0,1.0d0]
    matrix(3,:)=[-2.0d0,0.0d0,3.0d0,1.0d0]
    matrix(4,:)=[1.0d0,1.0d0,1.0d0,4.0d0]
    do j=1,3
      do i=1,4
        right(i,j)=real(i-j,8)/8.0d0
      enddo
    enddo
    augmented(:,:4)=matrix; augmented(:,5:)=right
    open(newunit=out,file='pivot_inputs.bin',status='new',action='write', &
         form='unformatted',access='stream',convert='little_endian')
    write(out) matrix,right
    close(out)
    call ALSBD(4,3,augmented,result_info,4)
    open(newunit=out,file='pivot_original.bin',status='new',action='write', &
         form='unformatted',access='stream',convert='little_endian')
    write(out) int(result_info,int64),augmented(:,5:)
    close(out)
    factor=matrix
    call SPOT1P64_FACTOR64(factor,pivots,values,result_info)
    open(newunit=out,file='pivot_factors.bin',status='new',action='write', &
         form='unformatted',access='stream',convert='little_endian')
    write(out) int(result_info,int64),factor,pivots,values
    close(out)
    call SPOT1P64_SOLVE64(factor,pivots,values,right,result_info)
    open(newunit=out,file='pivot_split.bin',status='new',action='write', &
         form='unformatted',access='stream',convert='little_endian')
    write(out) int(result_info,int64),right
    close(out)
    write(manifest,'(A)') '{"kind":"pivot","original":"pivot_original.bin",'// &
      '"split":"pivot_split.bin","factors":"pivot_factors.bin","rows":4,"rhs":3}'
    flush(manifest)
  end subroutine pivot_control
end program rank1_factor_cache_controls

subroutine XABORT(message)
  use rank1_control_abort
  implicit none
  character(len=*), intent(in) :: message
  integer :: out
  open(newunit=out,file='actual_XABORT.txt',status='new',action='write')
  write(out,'(A)') trim(message)
  close(out)
  write(*,'(A)') 'RAW_ACTUAL_UNIT_XABORT '//trim(message)
  if (expect_rejection.and.message == trim(expected_message)) stop 0
  stop 1
end subroutine XABORT
