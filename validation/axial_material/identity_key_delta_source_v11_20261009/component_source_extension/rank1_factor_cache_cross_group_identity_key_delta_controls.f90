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

program rank1_factor_cache_last_cprime_trim_controls
  use, intrinsic :: iso_fortran_env, only: int32,int64
  use SPOT1P64_CACHE_MOD
  use AXMAT_ORIGINAL_CACHE_MOD, only: ORIGINAL_BEGIN=>SPOT1P64_CACHE_BEGIN, &
    ORIGINAL_CLEAR=>SPOT1P64_CACHE_CLEAR
  use AXMAT_DENSE_CACHE_MOD, only: DENSE_BEGIN=>SPOT1P64_CACHE_BEGIN, &
    DENSE_CLEAR=>SPOT1P64_CACHE_CLEAR,DENSE_PLAN=>SPOT1P64_PLAN, &
    DENSE_STATS=>SPOT1P64_RANK1_STATS
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
  integer :: legacy_built,legacy_reused,memory_manifest
  logical :: active
  real :: tiny_du(4)
  double precision :: tiny_lower(4,4,3)
  integer(int64) :: tiny_key(2)
  real, allocatable :: dedup_du(:)
  double precision, allocatable :: dedup_lower(:,:,:)
  double precision :: dedup_decoded(4,4)
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
    subroutine SPOT1P64_DENSE(ig,nr,nh,ie,nmat,nsnap,nm,ischm,nq,nl,fixup, &
                        mat1d,dz,mat,total,sgas,basis,volume,radial,ncode,zcode,q,du,w,pl,f,c,x)
      integer :: ig,nr,nh,ie,nmat,nsnap,nm,ischm,nq,nl,mat1d(nh),mat(nh,nr),ncode(2)
      logical :: fixup
      real :: dz(nh),total(0:nmat),sgas(0:nmat,nl),basis(nr,nm),volume(nr),zcode(2)
      real :: du(nq),w(nq),pl(nl,nq)
      double precision :: radial(nr,nsnap),q(ie,nl,nh,nr),f(ie,nl,nh,nr),c(nh+1,nr),x(nq,nr)
    end subroutine SPOT1P64_DENSE
  end interface

  call get_command_argument(1,mode)
  if (storage_size(0) /= 32 .or. storage_size(0.0) /= 32 .or. storage_size(0.0d0) /= 64) stop 2
  open(newunit=manifest,file='manifest.jsonl',status='new',action='write')
  open(newunit=memory_manifest,file='memory_manifest.jsonl',status='new',action='write')
  select case(trim(mode))
  case('factor-positive')
    call factor_fixture('factor_nstate1',1,.false.)
    call factor_fixture('factor_pivot4',4,.false.)
    call factor_fixture('factor_signed_zero4',4,.true.)
    close(manifest)
    close(memory_manifest)
    write(*,'(A)') 'RAW_FACTOR_CONTROLS_COMPLETE'
  case('factor-negative')
    call get_command_argument(2,mutation)
    call factor_negative(trim(mutation))
  case('positive')
    call fixture('production_white_370',8,48,32,3,1,370,.true.,.false.,.true.,0)
    call fixture('signed_nonunit',8,48,32,3,1,2,.false.,.false.,.true.,0)
    call fixture('lifecycle_reset_1',8,48,32,3,1,2,.false.,.false.,.true.,0)
    call fixture('lifecycle_reset_2',8,48,32,3,1,2,.false.,.false.,.true.,1)
    call fixture('legacy_physical',2,3,8,3,2,2,.false.,.true.,.false.,0)
    call fixture('legacy_dense',2,3,8,3,2,2,.false.,.false.,.false.,0)
    call fixture('legacy_translation',8,3,8,3,1,2,.false.,.false.,.false.,0,.true.)
    call fixture('permuted_angles',8,48,32,3,1,2,.true.,.false.,.true.,0)
    call pivot_control()
    call SPOT1P64_CACHE_CLEAR()
    call ORIGINAL_CLEAR()
    call SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)
    write(manifest,'(A)') '{"kind":"clear","built":'//number(built)//',"reused":'// &
      number(reused)//',"hits":'//number(hits)//',"live":'//number(live)//',"peak":'//number(peak)//'}'
    close(manifest)
    close(memory_manifest)
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
    ! Retain the actual first-miss dictionary and full decode before mutation,
    ! so the external auditor never has to trust a claimed unique count.
    call archive_packed(trim(label),group,du)
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
  case('memory-positive')
    call primitive_setup()
    call save_primitive('primitive_before_store')
    call SPOT1P64_RANK1_LOWER_STORE(1,tiny_lower,tiny_du)
    call save_primitive('primitive_stored')
    call archive_packed('primitive',1,tiny_du)
    call SPOT1P64_CACHE_CLEAR()
    call save_memory_clear('primitive')
    close(manifest)
    close(memory_manifest)
    write(*,'(A)') 'RAW_MEMORY_CONTROLS_COMPLETE'
  case('memory-negative')
    call get_command_argument(2,mutation)
    call primitive_setup()
    call save_primitive('primitive_before_store')
    select case(trim(mutation))
    case('omitted_nonzero')
      tiny_lower(2,1,2)=0.125d0
      expected_message='SPOT1P64 RANK1 LOWER: NONZERO OR SIGNED ZERO OMITTED ROW.'
    case('omitted_negative_zero')
      tiny_lower(2,1,2)=transfer(int(z'8000000000000000',int64),0.0d0)
      expected_message='SPOT1P64 RANK1 LOWER: NONZERO OR SIGNED ZERO OMITTED ROW.'
    case('row_count','row_out_of_range','row_duplicate_or_reordered','packed_dimensions')
      call SPOT1P64_RANK1_LOWER_STORE(1,tiny_lower,tiny_du)
      select case(trim(mutation))
      case('row_count')
        SPOT1P64_PLAN(1)%mode(1)%rank1_lower_rows_count=1
        expected_message='SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.'
      case('row_out_of_range')
        SPOT1P64_PLAN(1)%mode(1)%rank1_lower_rows(1)=0
        expected_message='SPOT1P64 RANK1 LOWER: INVALID ROW MAP.'
      case('row_duplicate_or_reordered')
        SPOT1P64_PLAN(1)%mode(1)%rank1_lower_rows=[3,1]
        expected_message='SPOT1P64 RANK1 LOWER: INVALID ROW MAP.'
      case('packed_dimensions')
        deallocate(SPOT1P64_PLAN(1)%mode(1)%rank1_lower)
        allocate(SPOT1P64_PLAN(1)%mode(1)%rank1_lower(2,4,2))
        SPOT1P64_PLAN(1)%mode(1)%rank1_lower=tiny_lower([1,3],:,1:2)
        expected_message='SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.'
      end select
    case default
      stop 2
    end select
    call save_primitive('primitive_mutated')
    write(memory_manifest,'(A)') '{"kind":"memory_negative_expected","case":"'//trim(mutation)// &
      '","expected_XABORT":"'//trim(expected_message)//'"}'
    flush(memory_manifest)
    close(memory_manifest)
    close(manifest)
    expect_rejection=.true.
    if (trim(mutation) == 'omitted_nonzero'.or.trim(mutation) == 'omitted_negative_zero') then
      call SPOT1P64_RANK1_LOWER_STORE(1,tiny_lower,tiny_du)
    else
      call SPOT1P64_RANK1_LOWER_VALIDATE(1,4,3,tiny_du)
    endif
    open(newunit=unit,file='unexpected_return.txt',status='new',action='write')
    write(unit,'(A)') 'Actual packed-lower guard unexpectedly returned.'
    close(unit)
    stop 1
  case('dedup-positive')
    call dedup_setup('exact_repeated_blocks')
    call save_dedup('exact_repeated_blocks_before_store')
    call SPOT1P64_RANK1_LOWER_STORE(1,dedup_lower,dedup_du)
    call save_dedup('exact_repeated_blocks_stored')
    call archive_packed('exact_repeated_blocks',1,dedup_du)
    call SPOT1P64_CACHE_CLEAR()
    call save_memory_clear('exact_repeated_blocks')
    call dedup_setup('permuted_rows_repeated_blocks')
    call save_dedup('permuted_rows_repeated_blocks_before_store')
    call SPOT1P64_RANK1_LOWER_STORE(1,dedup_lower,dedup_du)
    call save_dedup('permuted_rows_repeated_blocks_stored')
    call archive_packed('permuted_rows_repeated_blocks',1,dedup_du)
    call SPOT1P64_CACHE_CLEAR()
    call save_memory_clear('permuted_rows_repeated_blocks')
    call dedup_setup('all_unique_fallback')
    call save_dedup('all_unique_fallback_before_store')
    call SPOT1P64_RANK1_LOWER_STORE(1,dedup_lower,dedup_du)
    call save_dedup('all_unique_fallback_stored')
    call archive_packed('all_unique_fallback',1,dedup_du)
    call SPOT1P64_CACHE_CLEAR()
    call save_memory_clear('all_unique_fallback')
    close(manifest)
    close(memory_manifest)
    write(*,'(A)') 'RAW_DEDUP_CONTROLS_COMPLETE'
  case('dedup-negative')
    call get_command_argument(2,mutation)
    call dedup_setup('exact_repeated_blocks')
    call save_dedup('dedup_before_store')
    call SPOT1P64_RANK1_LOWER_STORE(1,dedup_lower,dedup_du)
    call save_dedup('dedup_stored')
    expected_message='SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.'
    associate(plan=>SPOT1P64_PLAN(1)%mode(1))
      select case(trim(mutation))
      case('block_index_out_of_range')
        plan%rank1_lower_blocks(2)=plan%rank1_lower_unique_count+1
        expected_message='SPOT1P64 RANK1 LOWER: INVALID CANONICAL BLOCK MAP.'
      case('block_map_dimensions')
        deallocate(plan%rank1_lower_blocks)
        allocate(plan%rank1_lower_blocks(5))
        plan%rank1_lower_blocks=[1,2,2,3,3]
      case('missing_unique_block')
        plan%rank1_lower_unique_count=plan%rank1_lower_unique_count+1
      case('noncanonical_first_occurrence')
        do i=1,size(plan%rank1_lower_blocks)
          if (plan%rank1_lower_blocks(i)==1) then
            plan%rank1_lower_blocks(i)=2
          else if (plan%rank1_lower_blocks(i)==2) then
            plan%rank1_lower_blocks(i)=1
          endif
        enddo
        do j=1,size(plan%rank1_lower,2)
          do i=1,size(plan%rank1_lower,1)
            header(1)=transfer(plan%rank1_lower(i,j,1),0_int64)
            plan%rank1_lower(i,j,1)=plan%rank1_lower(i,j,2)
            plan%rank1_lower(i,j,2)=transfer(header(1),0.0d0)
          enddo
        enddo
        expected_message='SPOT1P64 RANK1 LOWER: INVALID CANONICAL BLOCK MAP.'
      case('duplicate_dictionary_value')
        plan%rank1_lower(:,:,3)=plan%rank1_lower(:,:,2)
        expected_message='SPOT1P64 RANK1 LOWER: DUPLICATE DICTIONARY BLOCK.'
      case('dictionary_dimensions')
        deallocate(plan%rank1_lower)
        allocate(plan%rank1_lower(2,4,2))
        plan%rank1_lower=dedup_lower([1,3],:,1:2)
      case('accounting_bytes')
        plan%rank1_factor_bytes=plan%rank1_factor_bytes-1_int64
      case('release_exceeds_live')
        expected_message='SPOT1P64 RANK1 CACHE: INVALID ACCOUNTING RELEASE.'
      case default
        stop 2
      end select
    end associate
    if (trim(mutation)/='release_exceeds_live') call SPOT1P64_RANK1_RESERVE(128_int64)
    call save_dedup('dedup_mutated')
    write(memory_manifest,'(A)') '{"kind":"dedup_negative_expected","case":"'//trim(mutation)// &
      '","expected_XABORT":"'//trim(expected_message)//'"}'
    flush(memory_manifest)
    close(memory_manifest)
    close(manifest)
    expect_rejection=.true.
    if (trim(mutation)=='release_exceeds_live') then
      call SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)
      open(newunit=unit,file='dedup_release_request.bin',status='new',action='write', &
        form='unformatted',access='stream',convert='little_endian')
      write(unit) live+1_int64,live,peak,cap
      close(unit)
      call SPOT1P64_RANK1_RELEASE(live+1_int64)
    else
      ! Default/direct LOAD must perform complete deep dictionary validation.
      call SPOT1P64_RANK1_LOWER_LOAD(1,1,dedup_decoded,dedup_du)
      call SPOT1P64_RANK1_RELEASE(128_int64)
    endif
    open(newunit=unit,file='unexpected_return.txt',status='new',action='write')
    write(unit,'(A)') 'Actual dictionary guard unexpectedly returned.'
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
    integer :: order(qq),angle
    real :: permuted_du(qq),permuted_w(qq),permuted_pl(ll,qq)
    is_cyclic=.false.
    if (present(cyclic)) is_cyclic=cyclic
    call configure(rr,hh,qq,ll,mm,white,physical,signed_basis,variant,is_cyclic)
    if (name == 'permuted_angles') then
      do angle=1,qq/2
        order(2*angle-1)=qq/2+angle
        order(2*angle)=angle
      enddo
      permuted_du=du(order); permuted_w=w(order); permuted_pl=pl(:,order)
      du=permuted_du; w=permuted_w; pl=permuted_pl
    endif
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
        if (rhs == 1.and.mm == 1.and..not.physical.and..not.is_cyclic) then
          ! The dense c017 reference has only one live group, independent of
          ! the candidate's 370 retained groups. Group is a cache address.
          call DENSE_BEGIN(1,.false.,.true.)
          call SPOT1P64_DENSE(1,nr,nh,1,nmat,nsnap,nm,1,nq,nl,.false., &
            mat1d,dz,mat,total,sgas,basis,volume,radial,ncode,zcode,q,du,w,pl,flux,cour,xnei)
          call archive_dense(name,group)
          call DENSE_CLEAR()
          call DENSE_STATS(built,reused,hits,live,peak,cap)
          write(memory_manifest,'(A)') '{"kind":"dense_clear","case":"'//trim(name)// &
            '","group":'//number(int(group,int64))//',"built":'//number(built)//',"reused":'// &
            number(reused)//',"hits":'//number(hits)//',"live":'//number(live)//',"peak":'//number(peak)//'}'
        endif
        call solve(.false.)
        if (rhs == 1) then
          call save_result(name,'build',group,rhs)
        else
          call save_result(name,'reuse',group,rhs)
        endif
      enddo
      if (mm == 1.and..not.physical.and..not.is_cyclic) call archive_packed(name,group,du)
    enddo
    call SPOT1P64_RANK1_TERMINAL()
    call SPOT1P64_CACHE_CLEAR()
    call ORIGINAL_CLEAR()
    call SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)
    write(manifest,'(A)') '{"kind":"clear","case":"'//trim(name)//'","built":'//number(built)// &
      ',"reused":'//number(reused)//',"hits":'//number(hits)//',"live":'//number(live)//',"peak":'//number(peak)//'}'
    flush(manifest)
  end subroutine fixture

  subroutine archive_dense(name,logical_group)
    character(len=*), intent(in) :: name
    integer, intent(in) :: logical_group
    integer :: out
    character(len=:), allocatable :: stem
    integer(int64) :: dense_header(12)
    stem=trim(name)//'_g'//number(int(logical_group,int64))//'_dense'
    dense_header=[1_int64,int(nq,int64),int(nh+1,int64),int(logical_group,int64),1_int64, &
      int(size(flux),int64),int(size(cour),int64),int(size(xnei),int64),0_int64,0_int64,0_int64,0_int64]
    open(newunit=out,file=stem//'.bin',status='new',action='write', &
      form='unformatted',access='stream',convert='little_endian')
    write(out) dense_header,DENSE_PLAN(1)%mode(1)%lower,flux,cour,xnei
    close(out)
    call DENSE_STATS(built,reused,hits,live,peak,cap)
    write(memory_manifest,'(A)') '{"kind":"dense","case":"'//trim(name)// &
      '","group":'//number(int(logical_group,int64))//',"file":"'//stem//'.bin","runtime_group":1,'// &
      '"built":'//number(built)//',"reused":'//number(reused)//',"hits":'//number(hits)// &
      ',"live":'//number(live)//',"peak":'//number(peak)//',"cap":'//number(cap)//'}'
    flush(memory_manifest)
    call archive_dense_identity_keys(name,logical_group)
  end subroutine archive_dense

  subroutine archive_packed(name,logical_group,directions)
    character(len=*), intent(in) :: name
    integer, intent(in) :: logical_group
    real, intent(in) :: directions(:)
    integer :: out,block,nstate,nblock,nrow,factor_dims(3),cprime_dims(3)
    integer(int64) :: memory_header(12),workspace_bytes,before_live,after_live
    double precision, allocatable :: decoded(:,:)
    character(len=:), allocatable :: stem
    associate(plan=>SPOT1P64_PLAN(logical_group)%mode(1))
      nstate=plan%nstate; nblock=plan%nblock; nrow=size(plan%rank1_lower_rows)
      ! Pure observations: lower-only primitives never allocate factor/cprime.
      factor_dims=0; cprime_dims=0
      if (allocated(plan%factor)) factor_dims=shape(plan%factor)
      if (allocated(plan%cprime)) cprime_dims=shape(plan%cprime)
      stem=trim(name)//'_g'//number(int(logical_group,int64))//'_packed'
      call SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)
      memory_header=[2_int64,int(nstate,int64),int(nblock,int64),int(nrow,int64), &
        int(logical_group,int64),plan%rank1_factor_bytes,live,peak,cap,built,reused,hits]
      open(newunit=out,file=stem//'.bin',status='new',action='write', &
        form='unformatted',access='stream',convert='little_endian')
      write(out) memory_header,plan%rank1_lower_rows,plan%rank1_lower_blocks
      write(out) int(plan%rank1_lower_unique_count,int32),plan%rank1_lower
      close(out)
      before_live=live
      workspace_bytes=8_int64*int(nstate,int64)*int(nstate,int64)
      call SPOT1P64_RANK1_RESERVE(workspace_bytes)
      allocate(decoded(nstate,nstate))
      call SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)
      stem=trim(name)//'_g'//number(int(logical_group,int64))//'_decoded'
      memory_header=[1_int64,int(nstate,int64),int(nblock,int64),int(nrow,int64), &
        int(logical_group,int64),workspace_bytes,before_live,live,peak,cap,0_int64,0_int64]
      open(newunit=out,file=stem//'.bin',status='new',action='write', &
        form='unformatted',access='stream',convert='little_endian')
      write(out) memory_header
      do block=1,nblock
        call SPOT1P64_RANK1_LOWER_LOAD(logical_group,block,decoded,directions)
        write(out) decoded
      enddo
      close(out)
      deallocate(decoded)
      call SPOT1P64_RANK1_RELEASE(workspace_bytes)
      call SPOT1P64_RANK1_STATS(built,reused,hits,after_live,peak,cap)
      write(memory_manifest,'(A)') '{"kind":"packed","case":"'//trim(name)// &
        '","group":'//number(int(logical_group,int64))//',"file":"'//trim(name)// &
        '_g'//number(int(logical_group,int64))//'_packed.bin","decoded_file":"'//stem// &
        '.bin","before_live":'//number(before_live)//',"after_live":'//number(after_live)// &
        ',"workspace_bytes":'//number(workspace_bytes)//',"peak":'//number(peak)// &
        ',"unique_count":'//number(int(plan%rank1_lower_unique_count,int64))// &
        ',"dictionary_bytes":'//number(8_int64*int(size(plan%rank1_lower),int64))// &
        ',"block_map_bytes":'//number(4_int64*int(size(plan%rank1_lower_blocks),int64))// &
        ',"factor_bytes":'//number(plan%rank1_factor_bytes)// &
        ',"factor_shape":['//number(int(factor_dims(1),int64))//','// &
        number(int(factor_dims(2),int64))//','//number(int(factor_dims(3),int64))//']'// &
        ',"cprime_shape":['//number(int(cprime_dims(1),int64))//','// &
        number(int(cprime_dims(2),int64))//','//number(int(cprime_dims(3),int64))//']}'
      flush(memory_manifest)
      if (plan%ready) call archive_candidate_identity_keys(name,logical_group)
    end associate
  end subroutine archive_packed

  ! Observation-only identity archives. Original numerical files are intact.
  subroutine archive_dense_identity_keys(name,logical_group)
    character(len=*), intent(in) :: name
    integer, intent(in) :: logical_group
    integer :: out
    integer(int64) :: h(12),bb,rr,hh,ll,pp,cc,nraw,noperator
    character(len=:), allocatable :: stem
    ! archive_dense is reached only for a genuine completed rank1 c017 run.
    if (nm /= 1 .or. nr <= 1 .or. any(ncode == 4)) return
    associate(plan=>DENSE_PLAN(1)%mode(1))
      nraw=size(plan%rank1_raw_bits,kind=int64)
      noperator=size(plan%rank1_operator_bits,kind=int64)
      call DENSE_STATS(bb,rr,hh,ll,pp,cc)
      h=[1_int64,int(logical_group,int64),1_int64,nraw,noperator,bb,rr,hh,ll,pp,cc,0_int64]
      stem=trim(name)//'_g'//number(int(logical_group,int64))//'_dense_keys'
      open(newunit=out,file=stem//'.bin',status='new',action='write', &
        form='unformatted',access='stream',convert='little_endian')
      write(out) h,plan%rank1_raw_bits,plan%rank1_operator_bits
      close(out)
      write(memory_manifest,'(A)') '{"kind":"dense_identity_keys","case":"'//trim(name)// &
        '","group":'//number(int(logical_group,int64))//',"runtime_group":1,"file":"'// &
        stem//'.bin","raw_key_words":'//number(nraw)//',"operator_key_words":'//number(noperator)//'}'
      flush(memory_manifest)
    end associate
  end subroutine archive_dense_identity_keys

  subroutine archive_candidate_identity_keys(name,logical_group)
    character(len=*), intent(in) :: name
    integer, intent(in) :: logical_group
    integer :: out,phase,owner
    integer(int64) :: h(16),bb,rr,hh,ll,pp,cc,nkey,words,positions,base_words
    integer(int64), allocatable :: decoded_key(:)
    logical :: compressed
    character(len=:), allocatable :: stem
    if (.not.SPOT1P64_RANK1_ENABLED()) return
    if (nm /= 1 .or. nr <= 1 .or. any(ncode == 4)) return
    associate(plan=>SPOT1P64_PLAN(logical_group)%mode(1))
      if (.not.plan%ready) return
      stem=trim(name)//'_g'//number(int(logical_group,int64))//'_identity_keys'
      open(newunit=out,file=stem//'.bin',status='new',action='write', &
        form='unformatted',access='stream',convert='little_endian')
      do phase=1,2
        call SPOT1P64_RANK1_KEY_STATS(logical_group,phase,owner,nkey,compressed,words,positions)
        allocate(decoded_key(nkey))
        call SPOT1P64_RANK1_KEY_LOAD(logical_group,phase,decoded_key)
        call SPOT1P64_RANK1_STATS(bb,rr,hh,ll,pp,cc)
        associate(base=>SPOT1P64_PLAN(owner)%mode(1))
          if (phase == 1) then
            base_words=size(base%rank1_raw_bits,kind=int64)
          else
            base_words=size(base%rank1_operator_bits,kind=int64)
          endif
          h=[1_int64,int(logical_group,int64),int(phase,int64),int(owner,int64),nkey, &
            merge(1_int64,0_int64,compressed),words,positions,base_words,bb,rr,hh,ll,pp,cc,0_int64]
          write(out) h
          if (phase == 1) then
            write(out) plan%rank1_raw_bits
            if (allocated(plan%rank1_raw_positions)) write(out) plan%rank1_raw_positions
            write(out) base%rank1_raw_bits,decoded_key
          else
            write(out) plan%rank1_operator_bits
            if (allocated(plan%rank1_operator_positions)) write(out) plan%rank1_operator_positions
            write(out) base%rank1_operator_bits,decoded_key
          endif
        end associate
        deallocate(decoded_key)
      enddo
      close(out)
      write(memory_manifest,'(A)') '{"kind":"candidate_identity_keys","case":"'//trim(name)// &
        '","group":'//number(int(logical_group,int64))//',"file":"'//stem//'.bin","phases":[1,2]}'
      flush(memory_manifest)
    end associate
  end subroutine archive_candidate_identity_keys

  subroutine primitive_setup()
    call SPOT1P64_CACHE_BEGIN(1,.false.,.true.)
    tiny_key=[1_int64,2_int64]
    call SPOT1P64_RANK1_GUARD(1,tiny_key,1,.true.,active)
    call SPOT1P64_RANK1_GUARD(1,tiny_key,2,.true.,active)
    SPOT1P64_PLAN(1)%mode(1)%nstate=4
    SPOT1P64_PLAN(1)%mode(1)%nblock=3
    tiny_du=[0.25,-0.5,0.75,-1.0]
    tiny_lower=0.0d0
    do k=1,3
      do j=1,4
        tiny_lower(1,j,k)=real(1+2*j+3*k,8)/8.0d0
        tiny_lower(3,j,k)=-real(3+2*j+3*k,8)/8.0d0
      enddo
    enddo
    tiny_lower(3,2,2)=transfer(int(z'8000000000000000',int64),0.0d0)
    call SPOT1P64_RANK1_FACTORS(1,4,3,2)
  end subroutine primitive_setup

  subroutine save_primitive(name)
    character(len=*), intent(in) :: name
    integer :: out,nrow,p1,p2,p3
    integer(int64) :: primitive_header(12)
    nrow=0; p1=0; p2=0; p3=0
    associate(plan=>SPOT1P64_PLAN(1)%mode(1))
      if (allocated(plan%rank1_lower_rows)) nrow=size(plan%rank1_lower_rows)
      if (allocated(plan%rank1_lower)) then
        p1=size(plan%rank1_lower,1); p2=size(plan%rank1_lower,2); p3=size(plan%rank1_lower,3)
      endif
      call SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)
      primitive_header=[2_int64,4_int64,3_int64,int(plan%rank1_lower_rows_count,int64), &
        int(nrow,int64),int(p1,int64),int(p2,int64),int(p3,int64),plan%rank1_factor_bytes,live,peak,cap]
      open(newunit=out,file=trim(name)//'.bin',status='new',action='write', &
        form='unformatted',access='stream',convert='little_endian')
      write(out) primitive_header,tiny_du,tiny_lower
      if (nrow > 0) write(out) plan%rank1_lower_rows
      if (allocated(plan%rank1_lower_blocks)) then
        write(out) int(size(plan%rank1_lower_blocks),int32),int(plan%rank1_lower_unique_count,int32)
        write(out) plan%rank1_lower_blocks
      else
        write(out) 0_int32,0_int32
      endif
      if (p1 > 0) write(out) plan%rank1_lower
      close(out)
      write(memory_manifest,'(A)') '{"kind":"primitive","file":"'//trim(name)//'.bin"}'
      flush(memory_manifest)
    end associate
  end subroutine save_primitive

  subroutine dedup_setup(kind)
    character(len=*), intent(in) :: kind
    integer :: blocks,positive_rows(2),b,r,col
    if (allocated(dedup_du)) deallocate(dedup_du,dedup_lower)
    blocks=6
    if (kind=='all_unique_fallback') blocks=49
    allocate(dedup_du(4),dedup_lower(4,4,blocks))
    dedup_du=[0.25,-0.5,0.75,-1.0]
    positive_rows=[1,3]
    if (kind=='permuted_rows_repeated_blocks') then
      dedup_du=[-0.5,0.25,-1.0,0.75]
      positive_rows=[2,4]
    endif
    dedup_lower=0.0d0
    if (kind=='all_unique_fallback') then
      do b=1,blocks
        do col=1,4
          do r=1,2
            dedup_lower(positive_rows(r),col,b)=real(b+2*col+3*r,8)/16.0d0
          enddo
        enddo
      enddo
    else
      do col=1,4
        do r=1,2
          dedup_lower(positive_rows(r),col,2)=real(2*col+3*r,8)/16.0d0
        enddo
      enddo
      dedup_lower(positive_rows(2),2,2)=0.0d0
      dedup_lower(:,:,3)=dedup_lower(:,:,2)
      dedup_lower(:,:,4)=dedup_lower(:,:,2)
      dedup_lower(positive_rows(2),2,4)=transfer(int(z'8000000000000000',int64),0.0d0)
      dedup_lower(:,:,5)=dedup_lower(:,:,4)
      dedup_lower(:,:,6)=dedup_lower(:,:,2)
    endif
    call SPOT1P64_CACHE_BEGIN(1,.false.,.true.)
    tiny_key=[1_int64,2_int64]
    call SPOT1P64_RANK1_GUARD(1,tiny_key,1,.true.,active)
    call SPOT1P64_RANK1_GUARD(1,tiny_key,2,.true.,active)
    SPOT1P64_PLAN(1)%mode(1)%nstate=4
    SPOT1P64_PLAN(1)%mode(1)%nblock=blocks
    call SPOT1P64_RANK1_FACTORS(1,4,blocks,2)
  end subroutine dedup_setup

  subroutine save_dedup(name)
    character(len=*), intent(in) :: name
    integer :: out,nrow,nmap,p1,p2,p3
    integer(int64) :: dedup_header(12)
    nrow=0; nmap=0; p1=0; p2=0; p3=0
    associate(plan=>SPOT1P64_PLAN(1)%mode(1))
      if (allocated(plan%rank1_lower_rows)) nrow=size(plan%rank1_lower_rows)
      if (allocated(plan%rank1_lower_blocks)) nmap=size(plan%rank1_lower_blocks)
      if (allocated(plan%rank1_lower)) then
        p1=size(plan%rank1_lower,1); p2=size(plan%rank1_lower,2); p3=size(plan%rank1_lower,3)
      endif
      call SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)
      dedup_header=[2_int64,4_int64,int(size(dedup_lower,3),int64), &
        int(plan%rank1_lower_rows_count,int64),int(nrow,int64),int(p1,int64),int(p2,int64), &
        int(p3,int64),plan%rank1_factor_bytes,live,peak,cap]
      open(newunit=out,file=trim(name)//'.bin',status='new',action='write', &
        form='unformatted',access='stream',convert='little_endian')
      write(out) dedup_header,dedup_du,dedup_lower
      if (nrow>0) write(out) plan%rank1_lower_rows
      write(out) int(nmap,int32),int(plan%rank1_lower_unique_count,int32)
      if (nmap>0) write(out) plan%rank1_lower_blocks
      if (p1>0) write(out) plan%rank1_lower
      close(out)
      write(memory_manifest,'(A)') '{"kind":"dedup_primitive","file":"'//trim(name)//'.bin"}'
      flush(memory_manifest)
    end associate
  end subroutine save_dedup

  subroutine save_memory_clear(name)
    character(len=*), intent(in) :: name
    call SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)
    write(memory_manifest,'(A)') '{"kind":"memory_clear","case":"'//trim(name)// &
      '","built":'//number(built)//',"reused":'//number(reused)//',"hits":'//number(hits)// &
      ',"live":'//number(live)//',"peak":'//number(peak)//'}'
    flush(memory_manifest)
  end subroutine save_memory_clear

  ! Codec-only controls. All raw bytes precede external numerical/bit gates.
  ! No native physics/accuracy/RSS qualification follows from these fixtures.
  subroutine factor_setup(n,b)
    integer, intent(in) :: n,b
    integer :: row,col,block
    integer(int64) :: key(2)
    logical :: enabled
    real :: directions(n)
    double precision :: full_lower(n,n,b)
    key=[11_int64,29_int64]
    call SPOT1P64_CACHE_BEGIN(1,.false.,.true.)
    call SPOT1P64_RANK1_GUARD(1,key,1,.true.,enabled)
    call SPOT1P64_RANK1_GUARD(1,key,2,.true.,enabled)
    associate(plan => SPOT1P64_PLAN(1)%mode(1))
      plan%nstate=n; plan%nblock=b
      call SPOT1P64_RANK1_FACTORS(1,n,b,n)
      allocate(plan%factor(n,n,b),plan%pivot(n,b),plan%pivot_value(n,b))
      allocate(plan%cprime(n,n,b-1))
      plan%factor=0.0d0; plan%pivot=0; plan%pivot_value=0.0d0
      plan%cprime=0.0d0
    end associate
    directions=1.0
    do block=1,b
      do col=1,n
        do row=1,n
          full_lower(row,col,block)=real(row+2*col+3*block,8)/16.0d0
        enddo
      enddo
    enddo
    call SPOT1P64_RANK1_LOWER_STORE(1,full_lower,directions)
    call SPOT1P64_RANK1_LOWER_VALIDATE(1,n,b,directions)
  end subroutine factor_setup

  subroutine factor_snapshot(name)
    character(len=*), intent(in) :: name
    integer :: out,n,b,dims(3)
    integer(int64) :: h(16),bb,rr,hh,ll,pp,cc
    call SPOT1P64_RANK1_STATS(bb,rr,hh,ll,pp,cc)
    associate(plan => SPOT1P64_PLAN(1)%mode(1))
      n=plan%nstate; b=plan%nblock; dims=shape(plan%factor)
      h=[1_int64,int(n,int64),int(b,int64),merge(1_int64,0_int64,plan%ready), &
        int(dims(1),int64),int(dims(2),int64),int(dims(3),int64),plan%rank1_factor_bytes, &
        ll,pp,cc,int(size(plan%rank1_raw_bits),int64),int(size(plan%rank1_operator_bits),int64), &
        int(size(plan%rank1_lower_rows),int64),int(plan%rank1_lower_unique_count,int64), &
        int(size(plan%cprime,3),int64)]
      open(newunit=out,file=trim(name)//'.bin',status='new',action='write', &
        form='unformatted',access='stream',convert='little_endian')
      write(out) h,plan%factor,plan%pivot,plan%pivot_value,plan%cprime
      write(out) plan%rank1_raw_bits,plan%rank1_operator_bits
      write(out) plan%rank1_lower_rows,plan%rank1_lower_blocks,plan%rank1_lower
      close(out)
    end associate
  end subroutine factor_snapshot

  subroutine factor_fixture(name,n,signed_pattern)
    character(len=*), intent(in) :: name
    integer, intent(in) :: n
    logical, intent(in) :: signed_pattern
    integer, parameter :: b=2,nrhs=3
    integer :: row,col,block,out,fi(b),oi(b),di(b)
    double precision :: matrix(n,n,b),full(n,n,b),decoded(n,n,b),values(n,b)
    double precision :: input_rhs(n,nrhs,b),original(n,nrhs,b),reloaded(n,nrhs,b)
    integer :: pivots(n,b)
    integer(int64) :: h(4),clear_h(6),bb,rr,hh,ll,pp,cc
    real :: directions(n)
    call factor_setup(n,b)
    do block=1,b
      if (n == 1) then
        matrix(1,1,block)=2.0d0**block
      else
        matrix(1,:,block)=[0.0d0,2.0d0,1.0d0,0.0d0]
        matrix(2,:,block)=[2.0d0,1.0d0,0.0d0,1.0d0]
        matrix(3,:,block)=[-2.0d0,0.0d0,3.0d0,1.0d0]
        matrix(4,:,block)=[1.0d0,1.0d0,1.0d0,4.0d0+real(block-1,8)/8.0d0]
      endif
      do col=1,nrhs
        do row=1,n
          input_rhs(row,col,block)=real(row-col+block,8)/8.0d0
        enddo
      enddo
      full(:,:,block)=matrix(:,:,block)
      call SPOT1P64_FACTOR64(full(:,:,block),pivots(:,block),values(:,block),fi(block))
      if (signed_pattern) then
        ! A second, explicitly synthetic valid-SOLVE factor representation.
        ! Different off-diagonal words and both signed zeros expose codec loss.
        do col=1,n
          pivots(col,block)=col
          values(col,block)=2.0d0**col
          do row=1,n
            full(row,col,block)=real(2*row-3*col+5*block,8)/64.0d0
          enddo
          full(col,col,block)=-real(100*block+col,8)
        enddo
      endif
    enddo
    if (signed_pattern) then
      full(2,3,1)=0.0d0
      full(3,2,2)=transfer(int(z'8000000000000000',int64),0.0d0)
    endif
    input_rhs(1,3,1)=transfer(int(z'8000000000000000',int64),0.0d0)
    h=[1_int64,int(n,int64),int(b,int64),int(nrhs,int64)]
    open(newunit=out,file=trim(name)//'_inputs.bin',status='new',action='write', &
      form='unformatted',access='stream',convert='little_endian')
    write(out) h,matrix,input_rhs
    close(out)
    associate(plan => SPOT1P64_PLAN(1)%mode(1))
      plan%factor=full; plan%pivot=pivots; plan%pivot_value=values
    end associate
    original=input_rhs
    do block=1,b
      call SPOT1P64_SOLVE64(full(:,:,block),pivots(:,block),values(:,block), &
        original(:,:,block),oi(block))
    enddo
    call factor_snapshot(trim(name)//'_before')
    call SPOT1P64_RANK1_FACTOR_PACK(1)
    SPOT1P64_PLAN(1)%mode(1)%ready=.true.
    directions=1.0
    call SPOT1P64_RANK1_LOWER_VALIDATE(1,n,b,directions)
    call factor_snapshot(trim(name)//'_after')
    reloaded=input_rhs
    do block=1,b
      call SPOT1P64_RANK1_FACTOR_LOAD(1,block,decoded(:,:,block))
      call SPOT1P64_SOLVE64(decoded(:,:,block),pivots(:,block),values(:,block), &
        reloaded(:,:,block),di(block))
    enddo
    open(newunit=out,file=trim(name)//'_outputs.bin',status='new',action='write', &
      form='unformatted',access='stream',convert='little_endian')
    write(out) h,decoded,original,reloaded,fi,oi,di
    close(out)
    write(manifest,'(A)') '{"kind":"factor_fixture","case":"'//trim(name)// &
      '","nstate":'//number(int(n,int64))//',"nblock":2,"nrhs":3,"signed_pattern":'// &
      merge('true ','false',signed_pattern)//'}'
    flush(manifest)
    call SPOT1P64_CACHE_CLEAR()
    call SPOT1P64_RANK1_STATS(bb,rr,hh,ll,pp,cc)
    clear_h=[bb,rr,hh,ll,pp,cc]
    open(newunit=out,file=trim(name)//'_clear.bin',status='new',action='write', &
      form='unformatted',access='stream',convert='little_endian')
    write(out) clear_h
    close(out)
  end subroutine factor_fixture

  subroutine factor_negative(which)
    character(len=*), intent(in) :: which
    integer :: op,block,out
    integer(int64) :: filler,pbytes,request(8),bb,rr,hh,ll,pp,cc
    double precision :: decoded(4,4)
    call factor_setup(4,2)
    call factor_snapshot('factor_negative_before')
    filler=0_int64; pbytes=8_int64*3_int64*4_int64*2_int64
    block=1
    expected_message='SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.'
    select case(which)
    case('pack_already_ready')
      op=1
      call SPOT1P64_RANK1_FACTOR_PACK(1)
      SPOT1P64_PLAN(1)%mode(1)%ready=.true.
    case('load_full_square')
      op=2
      SPOT1P64_PLAN(1)%mode(1)%ready=.true.
    case('load_block_zero')
      op=3; block=0
      call SPOT1P64_RANK1_FACTOR_PACK(1)
      SPOT1P64_PLAN(1)%mode(1)%ready=.true.
    case('pack_temporary_cap')
      op=4
      call SPOT1P64_RANK1_STATS(bb,rr,hh,ll,pp,cc)
      ! Account-only filler: no fictitious 512 MiB allocation/RSS claim.
      filler=cc-ll-pbytes+1_int64
      call SPOT1P64_RANK1_RESERVE(filler)
      expected_message=cap_message
    case default
      stop 2
    end select
    call factor_snapshot('factor_negative_after')
    call SPOT1P64_RANK1_STATS(bb,rr,hh,ll,pp,cc)
    request=[1_int64,int(op,int64),1_int64,int(block,int64),filler,pbytes,ll,cc]
    open(newunit=out,file='factor_negative_request.bin',status='new',action='write', &
      form='unformatted',access='stream',convert='little_endian')
    write(out) request
    close(out)
    write(memory_manifest,'(A)') '{"kind":"factor_negative_expected","case":"'//trim(which)// &
      '","expected_XABORT":"'//trim(expected_message)//'"}'
    flush(memory_manifest)
    close(memory_manifest)
    close(manifest)
    expect_rejection=.true.
    if (op == 1.or.op == 4) then
      call SPOT1P64_RANK1_FACTOR_PACK(1)
    else
      call SPOT1P64_RANK1_FACTOR_LOAD(1,block,decoded)
    endif
    open(newunit=out,file='unexpected_return.txt',status='new',action='write')
    write(out,'(A)') 'Actual factor guard unexpectedly returned.'
    close(out)
    stop 1
  end subroutine factor_negative

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
end program rank1_factor_cache_last_cprime_trim_controls

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
