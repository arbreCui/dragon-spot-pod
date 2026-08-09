module B2W_FIXTURE_SUPPORT
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none
  private

  integer, parameter, public :: NGRP=370, NSNAP=3, NUNK=14
  integer, parameter, public :: NREG=8, NSTATE=40, NMAT=8
  integer(int32), parameter, public :: K0_BITS=int(z'3f900001',int32)
  integer(int32), parameter, public :: K1_BITS=int(z'3fa00001',int32)
  integer(int32), parameter :: EPS_BITS=int(z'348637bd',int32)
  integer, save :: object_counter=0

  public :: BUILD_AX, BUILD_AX_TRACK, BUILD_FEEDBACK_BEFORE_SPOLEAK
  public :: VERIFY_AX_INPUT, VERIFY_FEEDBACK_INPUT
  public :: OPEN_FRESH, CLONE_ROOT, EMPTY_ROOT
  public :: REQUIRE_ASSOCIATED, REQUIRE_RECORD, REQUIRE_ABSENT
  public :: REQUIRE_INTEGER, REQUIRE_CHARACTER, REQUIRE_REAL32_BITS
  public :: REQUIRE_REAL64_BITS, REQUIRE_EXACT_INVENTORY
  public :: PUT_CHARACTER, EXPECTED_VECTOR64, EXPECTED_LEAK32
  public :: K0_VALUE, K1_VALUE, RHO0_VALUE, RHO1_VALUE
  public :: BITS32, BITS64

contains

  real(real32) function K0_VALUE()
    K0_VALUE=transfer(K0_BITS,0.0_real32)
  end function K0_VALUE


  real(real32) function K1_VALUE()
    K1_VALUE=transfer(K1_BITS,0.0_real32)
  end function K1_VALUE


  real(real64) function RHO0_VALUE()
    RHO0_VALUE=1.0_real64/real(K0_VALUE(),real64)
  end function RHO0_VALUE


  real(real64) function RHO1_VALUE()
    RHO1_VALUE=1.0_real64/real(K1_VALUE(),real64)
  end function RHO1_VALUE


  elemental integer(int32) function BITS32(value)
    real(real32), intent(in) :: value
    BITS32=transfer(value,0_int32)
  end function BITS32


  elemental integer(int64) function BITS64(value)
    real(real64), intent(in) :: value
    BITS64=transfer(value,0_int64)
  end function BITS64


  subroutine BUILD_AX(root)
    type(c_ptr), intent(out) :: root
    integer, parameter :: NCOEF=NGRP*NSNAP
    integer, parameter :: NBASIS=NGRP*NREG, NGRAM=NGRP
    integer :: state(NSTATE), dims(4), rank(NGRP)
    integer :: offset(NGRP+1), gram_offset(NGRP+1)
    integer :: basis_offset(NGRP+1), ig, ip, index
    real(real32) :: basis(NBASIS), keff, unknown(NUNK)
    real(real64) :: coordinates(NCOEF), gram(NGRAM)
    real(real64) :: leakage(NCOEF), height(NSNAP)
    real(real64) :: offspace(NCOEF), rho, norm, gram_error
    type(c_ptr) :: flux

    call OPEN_FRESH('AX',root)
    state=0
    state(1)=NGRP
    state(2)=NUNK
    dims=[1,NGRP,NSNAP,NCOEF]
    rank=1
    do ig=1,NGRP+1
      offset(ig)=(ig-1)*NSNAP
      gram_offset(ig)=ig-1
      basis_offset(ig)=(ig-1)*NREG
    end do
    basis=1.0_real32
    coordinates=0.0_real64
    gram=1.0_real64
    offspace=0.0_real64
    height=1.0_real64
    norm=1.0_real64
    gram_error=0.0_real64
    keff=K1_VALUE()
    rho=RHO1_VALUE()
    do ip=1,NSNAP
      do ig=1,NGRP
        index=(ip-1)*NGRP+ig
        leakage(index)=real(EXPECTED_LEAK32(ip),real64)
        coordinates(index)=nearest(real(ip*100000+ig,real64), &
            +1.0_real64)
      end do
    end do

    call PUT_CHARACTER(root,'SIGNATURE',12,'L_FLUX')
    call LCMPUT(root,'STATE-VECTOR',NSTATE,1,state)
    call LCMPUT(root,'SPOT-X-DIMS',4,1,dims)
    call LCMPUT(root,'SPOT-X-FIXB',1,1,1)
    call PUT_CHARACTER(root,'SPOT-X-NID',12,'NUFISS-UNIT')
    call PUT_CHARACTER(root,'SPOT-X-BTYP',12,'POD-FIXED')
    call LCMPUT(root,'SPOT-X-RANK',NGRP,1,rank)
    call LCMPUT(root,'SPOT-X-OFF',NGRP+1,1,offset)
    call LCMPUT(root,'SPOT-X-GOFF',NGRP+1,1,gram_offset)
    call LCMPUT(root,'SPOT-X-BOFF',NGRP+1,1,basis_offset)
    call LCMPUT(root,'SPOT-X-BASIS',NBASIS,2,basis)
    call LCMPUT(root,'K-EFFECTIVE',1,2,keff)
    call LCMPUT(root,'SPOT-X-A',NCOEF,4,coordinates)
    call LCMPUT(root,'SPOT-X-GRAM',NGRAM,4,gram)
    call LCMPUT(root,'SPOT-X-RHO',1,4,rho)
    call LCMPUT(root,'SPOT-X-L',NCOEF,4,leakage)
    call LCMPUT(root,'SPOT-X-H',NSNAP,4,height)
    call LCMPUT(root,'SPOT-X-NORM',1,4,norm)
    call LCMPUT(root,'SPOT-X-PERP',NCOEF,4,offspace)
    call LCMPUT(root,'SPOT-X-GERR',1,4,gram_error)

    ! This ordinary FLUX list is consumed by the real SPOLEAK call.  It is
    ! deliberately outside the SPOSTATE-owned SPOT-X-* canonical bundle.
    flux=LCMLID(root,'FLUX',NGRP)
    call REQUIRE_ASSOCIATED(flux,'AX FLUX list')
    do ig=1,NGRP
      unknown=0.0_real32
      unknown(1:3)=1.0_real32
      unknown(4)=0.0_real32
      unknown(5)=0.125_real32
      unknown(6)=0.375_real32
      unknown(7)=0.875_real32
      call LCMPDL(flux,ig,NUNK,2,unknown)
    end do
  end subroutine BUILD_AX


  subroutine BUILD_AX_TRACK(root)
    type(c_ptr), intent(out) :: root
    integer :: state(NSTATE), key(3), mat1d(3)
    real(real32) :: area(1), dz(3), volume(3)

    call OPEN_FRESH('AX-TRACK',root)
    state=0
    state(1)=3
    state(2)=NUNK
    state(6)=1
    state(7)=3
    state(8)=NSNAP
    state(11)=3
    state(12)=4
    key=[1,2,3]
    mat1d=[1,2,3]
    area=1.0_real32
    dz=1.0_real32
    volume=1.0_real32
    call PUT_CHARACTER(root,'SIGNATURE',12,'L_TRACK')
    call PUT_CHARACTER(root,'TRACK-TYPE',12,'SPOT')
    call LCMPUT(root,'STATE-VECTOR',NSTATE,1,state)
    call LCMPUT(root,'AREA2D',1,2,area)
    call LCMPUT(root,'KEYFLX',3,1,key)
    call LCMPUT(root,'MAT1D',3,1,mat1d)
    call LCMPUT(root,'VOL1D',3,2,dz)
    call LCMPUT(root,'VOLUME',3,2,volume)
  end subroutine BUILD_AX_TRACK


  subroutine BUILD_FEEDBACK_BEFORE_SPOLEAK(root)
    type(c_ptr), intent(out) :: root
    integer :: ip, ig, state(NSTATE), key(NREG), marker
    real(real32) :: leakage0(NGRP), flux32(NUNK), sour32(NUNK)
    real(real32) :: qfiss32(NUNK), eps(5), system_leak(NGRP)
    real(real64) :: flux64(NUNK), sour64(NUNK), qfiss64(NUNK)
    type(c_ptr) :: tracks, libraries, systems, fluxes
    type(c_ptr) :: item, groups, group, authority
    type(c_ptr) :: mirror_flux, mirror_sour, auth_flux, auth_sour
    type(c_ptr) :: auth_qfiss, qouter, qinner, deep

    call OPEN_FRESH('FEEDBACK',root)
    call PUT_CHARACTER(root,'SIGNATURE',12,'L_ARCHIVE')
    call LCMPUT(root,'LISTDIM',1,1,NSNAP)
    tracks=LCMLID(root,'TRACK',NSNAP)
    libraries=LCMLID(root,'MICROLIB2',NSNAP)
    systems=LCMLID(root,'SYSTEM',NSNAP)
    fluxes=LCMLID(root,'FLUX',NSNAP)
    call REQUIRE_ASSOCIATED(tracks,'feedback TRACK list')
    call REQUIRE_ASSOCIATED(libraries,'feedback MICROLIB2 list')
    call REQUIRE_ASSOCIATED(systems,'feedback SYSTEM list')
    call REQUIRE_ASSOCIATED(fluxes,'feedback FLUX list')

    key=[1,2,3,4,5,6,7,8]
    eps=[transfer(EPS_BITS,0.0_real32), &
         transfer(EPS_BITS,0.0_real32), &
         transfer(EPS_BITS,0.0_real32),0.0_real32,0.0_real32]
    leakage0=0.0_real32

    do ip=1,NSNAP
      item=LCMDIL(tracks,ip)
      call REQUIRE_ASSOCIATED(item,'feedback TRACK child')
      call PUT_CHARACTER(item,'SIGNATURE',12,'L_TRACK')
      call LCMPUT(item,'KEYFLX',NREG,1,key)
      call LCMPUT(item,'KEYFLX$ANIS',NREG,1,key)
      marker=1000+ip
      call LCMPUT(item,'B2W-ID',1,1,marker)
      deep=LCMDID(item,'B2W-DEEP')
      call LCMPUT(deep,'VALUE',1,1,marker)

      item=LCMDIL(libraries,ip)
      call REQUIRE_ASSOCIATED(item,'feedback MICROLIB2 child')
      call PUT_CHARACTER(item,'SIGNATURE',12,'L_LIBRARY')
      marker=2000+ip
      call LCMPUT(item,'B2W-ID',1,1,marker)
      deep=LCMDID(item,'B2W-DEEP')
      call LCMPUT(deep,'VALUE',1,1,marker)

      item=LCMDIL(systems,ip)
      call REQUIRE_ASSOCIATED(item,'feedback SYSTEM child')
      call PUT_CHARACTER(item,'SIGNATURE',12,'L_PIJ')
      call PUT_CHARACTER(item,'LINK.MACRO',12,'MACRO0')
      call PUT_CHARACTER(item,'LINK.TRACK',12,'TRACK')
      state=0
      state(1:14)=[1,1,1,0,1,1,4,NGRP,NUNK,NMAT,1,0,0,0]
      call LCMPUT(item,'STATE-VECTOR',NSTATE,1,state)
      ! This is the lagged L0 admitted by B2R and is equal to the child's
      ! pre-SPOLEAK value.  SPOLEAK updates only the child to L1 below.
      system_leak=0.0_real32
      call LCMPUT(item,'SPOT-LEAK1D',NGRP,2,system_leak)
      call LCMPUT(item,'SPOT-L1-SNAP',1,1,ip)
      groups=LCMLID(item,'GROUP',NGRP)
      do ig=1,NGRP
        group=LCMDIL(groups,ig)
        marker=ip*100000+ig
        call LCMPUT(group,'B2W-WITNESS',1,1,marker)
      end do
      authority=LCMDID(item,'SPOT-R64')
      call LCMPUT(authority,'RHO',1,4,RHO0_VALUE())
      call PUT_CHARACTER(authority,'STATE',12,'ASSEMBLED')
      call LCMPUT(authority,'EPOCH',1,1,1)

      item=LCMDIL(fluxes,ip)
      call REQUIRE_ASSOCIATED(item,'feedback FLUX child')
      state=0
      state(1:18)=[NGRP,NUNK,1,0,0,0,0,3,3,1,740,500, &
          0,0,0,0,NMAT,1]
      call PUT_CHARACTER(item,'SIGNATURE',12,'L_FLUX')
      call LCMPUT(item,'STATE-VECTOR',NSTATE,1,state)
      call LCMPUT(item,'EPS-CONVERGE',5,2,eps)
      call LCMPUT(item,'IMERGE-LEAK',NMAT,1,[1,1,1,1,1,1,1,1])
      call LCMPUT(item,'KEYFLX',NREG,1,key)
      call PUT_CHARACTER(item,'OPTION',4,'B0  ')
      call PUT_CHARACTER(item,'LINK.MACRO',12,'MACRO0')
      call PUT_CHARACTER(item,'LINK.TRACK',12,'TRACK')
      call PUT_CHARACTER(item,'LINK.SYSTEM',12,'SYSTEM')
      call LCMPUT(item,'SPOT-LEAK1D',NGRP,2,leakage0)
      call LCMPUT(item,'SPOT-FS-EQN',1,1,1)
      call LCMPUT(item,'SPOT-FS-K',1,2,K0_VALUE())
      mirror_flux=LCMLID(item,'FLUX',NGRP)
      mirror_sour=LCMLID(item,'SOUR',NGRP)
      qouter=LCMLID(item,'SPOT-QFISS',1)
      qinner=LCMLIL(qouter,1,NGRP)
      authority=LCMDID(item,'SPOT-R64')
      call LCMPUT(authority,'RHO',1,4,RHO0_VALUE())
      auth_flux=LCMLID(authority,'FLUX',NGRP)
      auth_sour=LCMLID(authority,'SOUR',NGRP)
      auth_qfiss=LCMLID(authority,'QFISS',NGRP)
      do ig=1,NGRP
        call EXPECTED_VECTOR64(1,ip,ig,flux64)
        call EXPECTED_VECTOR64(2,ip,ig,sour64)
        call EXPECTED_VECTOR64(3,ip,ig,qfiss64)
        flux32=real(flux64,real32)
        sour32=real(sour64,real32)
        qfiss32=real(qfiss64,real32)
        call LCMPDL(mirror_flux,ig,NUNK,2,flux32)
        call LCMPDL(mirror_sour,ig,NUNK,2,sour32)
        call LCMPDL(qinner,ig,NUNK,2,qfiss32)
        call LCMPDL(auth_flux,ig,NUNK,4,flux64)
        call LCMPDL(auth_sour,ig,NUNK,4,sour64)
        call LCMPDL(auth_qfiss,ig,NUNK,4,qfiss64)
      end do
      call PUT_CHARACTER(authority,'STATE',12,'SOLVED')
      call LCMPUT(authority,'EPOCH',1,1,1)
    end do

    authority=LCMDID(root,'SPOT-R64')
    call LCMPUT(authority,'NPLANE',1,1,NSNAP)
    call PUT_CHARACTER(authority,'STATE',12,'RETURNED')
    call LCMPUT(authority,'EPOCH',1,1,1)
  end subroutine BUILD_FEEDBACK_BEFORE_SPOLEAK


  subroutine VERIFY_AX_INPUT(root)
    type(c_ptr), intent(in) :: root
    integer, parameter :: NCOEF=NGRP*NSNAP
    integer :: state(NSTATE), dims(4), rank(NGRP)
    integer :: offset(NGRP+1), goff(NGRP+1), boff(NGRP+1)
    integer :: ig, ip, index
    real(real32) :: keff
    real(real64) :: leakage(NCOEF), rho

    call REQUIRE_CHARACTER(root,'SIGNATURE',12,'L_FLUX')
    call REQUIRE_RECORD(root,'STATE-VECTOR',NSTATE,1)
    call LCMGET(root,'STATE-VECTOR',state)
    if (state(1) /= NGRP .or. state(2) /= NUNK) &
      call FAIL('AX STATE-VECTOR differs')
    call REQUIRE_ABSENT(root,'SPOT-X-STATE')
    call REQUIRE_ABSENT(root,'SPOT-X-EPOCH')
    call REQUIRE_RECORD(root,'SPOT-X-DIMS',4,1)
    call LCMGET(root,'SPOT-X-DIMS',dims)
    if (any(dims /= [1,NGRP,NSNAP,NCOEF])) &
      call FAIL('AX dimensions differ')
    call REQUIRE_INTEGER(root,'SPOT-X-FIXB',1)
    call REQUIRE_CHARACTER(root,'SPOT-X-NID',12,'NUFISS-UNIT')
    call REQUIRE_CHARACTER(root,'SPOT-X-BTYP',12,'POD-FIXED')
    call REQUIRE_RECORD(root,'SPOT-X-RANK',NGRP,1)
    call REQUIRE_RECORD(root,'SPOT-X-OFF',NGRP+1,1)
    call REQUIRE_RECORD(root,'SPOT-X-GOFF',NGRP+1,1)
    call REQUIRE_RECORD(root,'SPOT-X-BOFF',NGRP+1,1)
    call LCMGET(root,'SPOT-X-RANK',rank)
    call LCMGET(root,'SPOT-X-OFF',offset)
    call LCMGET(root,'SPOT-X-GOFF',goff)
    call LCMGET(root,'SPOT-X-BOFF',boff)
    if (any(rank /= 1)) call FAIL('AX rank differs')
    do ig=1,NGRP+1
      if (offset(ig) /= (ig-1)*NSNAP .or. goff(ig) /= ig-1 .or. &
          boff(ig) /= (ig-1)*NREG) call FAIL('AX offsets differ')
    end do
    call REQUIRE_RECORD(root,'SPOT-X-BASIS',NGRP*NREG,2)
    call REQUIRE_RECORD(root,'SPOT-X-A',NCOEF,4)
    call REQUIRE_RECORD(root,'SPOT-X-GRAM',NGRP,4)
    call REQUIRE_RECORD(root,'SPOT-X-RHO',1,4)
    call REQUIRE_RECORD(root,'SPOT-X-L',NCOEF,4)
    call REQUIRE_RECORD(root,'SPOT-X-H',NSNAP,4)
    call REQUIRE_RECORD(root,'SPOT-X-NORM',1,4)
    call REQUIRE_RECORD(root,'SPOT-X-PERP',NCOEF,4)
    call REQUIRE_RECORD(root,'SPOT-X-GERR',1,4)
    call REQUIRE_RECORD(root,'FLUX',NGRP,10)
    call REQUIRE_REAL32_BITS(root,'K-EFFECTIVE',K1_VALUE())
    call LCMGET(root,'SPOT-X-RHO',rho)
    if (.not. ieee_is_finite(rho) .or. BITS64(rho) /= &
        BITS64(RHO1_VALUE())) call FAIL('AX RHO differs')
    call LCMGET(root,'K-EFFECTIVE',keff)
    if (BITS64(rho) /= BITS64(1.0_real64/real(keff,real64))) &
      call FAIL('AX reciprocal identity differs')
    call LCMGET(root,'SPOT-X-L',leakage)
    do ip=1,NSNAP
      do ig=1,NGRP
        index=(ip-1)*NGRP+ig
        if (BITS64(leakage(index)) /= &
            BITS64(real(EXPECTED_LEAK32(ip),real64))) &
          call FAIL('AX leakage differs')
      end do
    end do
  end subroutine VERIFY_AX_INPUT


  subroutine VERIFY_FEEDBACK_INPUT(root)
    type(c_ptr), intent(in) :: root
    character(len=12), parameter :: root_names(9)=[ &
        character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
        'SPOT-L1-ERR','TRACK','MICROLIB2','SYSTEM','FLUX','SPOT-R64']
    character(len=12), parameter :: root_auth_names(3)=[ &
        character(len=12) :: 'NPLANE','STATE','EPOCH']
    character(len=12), parameter :: child_auth_names(6)=[ &
        character(len=12) :: 'RHO','FLUX','SOUR','QFISS','STATE','EPOCH']
    integer :: ip, ig
    real(real32) :: l1err, k0, leakage(NGRP), system_leak(NGRP)
    real(real32) :: found32(NUNK), expected32(NUNK)
    real(real64) :: found64(NUNK), expected64(NUNK), rho
    type(c_ptr) :: tracks, libraries, systems, fluxes, item, authority
    type(c_ptr) :: mirror, payload, outer, inner

    call REQUIRE_EXACT_INVENTORY(root,root_names,'feedback root')
    call REQUIRE_CHARACTER(root,'SIGNATURE',12,'L_ARCHIVE')
    call REQUIRE_INTEGER(root,'LISTDIM',NSNAP)
    call REQUIRE_REAL64_BITS(root,'SPOT-ITER-K',real(K1_VALUE(),real64))
    call REQUIRE_RECORD(root,'SPOT-L1-ERR',1,2)
    call LCMGET(root,'SPOT-L1-ERR',l1err)
    if (.not. ieee_is_finite(l1err) .or. &
        BITS32(l1err) /= BITS32(0.5_real32)) &
      call FAIL('feedback L1 error differs')
    authority=LCMGID(root,'SPOT-R64')
    call REQUIRE_EXACT_INVENTORY(authority,root_auth_names, &
        'feedback root authority')
    call REQUIRE_INTEGER(authority,'NPLANE',NSNAP)
    call REQUIRE_CHARACTER(authority,'STATE',12,'RETURNED')
    call REQUIRE_INTEGER(authority,'EPOCH',1)

    tracks=LCMGID(root,'TRACK')
    libraries=LCMGID(root,'MICROLIB2')
    systems=LCMGID(root,'SYSTEM')
    fluxes=LCMGID(root,'FLUX')
    do ip=1,NSNAP
      item=LCMGIL(tracks,ip)
      call REQUIRE_CHARACTER(item,'SIGNATURE',12,'L_TRACK')
      call REQUIRE_INTEGER(item,'B2W-ID',1000+ip)
      item=LCMGIL(libraries,ip)
      call REQUIRE_CHARACTER(item,'SIGNATURE',12,'L_LIBRARY')
      call REQUIRE_INTEGER(item,'B2W-ID',2000+ip)

      item=LCMGIL(systems,ip)
      call REQUIRE_CHARACTER(item,'SIGNATURE',12,'L_PIJ')
      call REQUIRE_RECORD(item,'SPOT-LEAK1D',NGRP,2)
      call LCMGET(item,'SPOT-LEAK1D',system_leak)
      if (.not. all(ieee_is_finite(system_leak))) &
        call FAIL('SYSTEM leakage is nonfinite')

      item=LCMGIL(fluxes,ip)
      call REQUIRE_CHARACTER(item,'SIGNATURE',12,'L_FLUX')
      call REQUIRE_RECORD(item,'SPOT-LEAK1D',NGRP,2)
      call LCMGET(item,'SPOT-LEAK1D',leakage)
      if (any(BITS32(leakage) /= BITS32(EXPECTED_LEAK32(ip)))) &
        call FAIL('feedback direct leakage differs')
      if (all(BITS32(leakage) == BITS32(system_leak))) &
        call FAIL('fixture does not distinguish SYSTEM L0 from returned L1')
      call REQUIRE_INTEGER(item,'SPOT-FS-EQN',1)
      call REQUIRE_REAL32_BITS(item,'SPOT-FS-K',K0_VALUE())
      call LCMGET(item,'SPOT-FS-K',k0)
      authority=LCMGID(item,'SPOT-R64')
      call REQUIRE_EXACT_INVENTORY(authority,child_auth_names, &
          'feedback child authority')
      call REQUIRE_ABSENT(authority,'PLANE')
      call REQUIRE_CHARACTER(authority,'STATE',12,'SOLVED')
      call REQUIRE_INTEGER(authority,'EPOCH',1)
      call LCMGET(authority,'RHO',rho)
      if (BITS64(rho) /= BITS64(RHO0_VALUE()) .or. &
          BITS64(rho) /= BITS64(1.0_real64/real(k0,real64))) &
        call FAIL('feedback child RHO identity differs')
      if (BITS64(rho) == BITS64(RHO1_VALUE())) &
        call FAIL('fixture does not distinguish rho0 from rho1')

      mirror=LCMGID(item,'FLUX')
      payload=LCMGID(authority,'FLUX')
      do ig=1,NGRP
        call EXPECTED_VECTOR64(1,ip,ig,expected64)
        call LCMGDL(payload,ig,found64)
        if (any(BITS64(found64) /= BITS64(expected64))) &
          call FAIL('feedback authority FLUX differs')
        expected32=real(expected64,real32)
        call LCMGDL(mirror,ig,found32)
        if (any(BITS32(found32) /= BITS32(expected32))) &
          call FAIL('feedback FLUX mirror differs')
      end do
      mirror=LCMGID(item,'SOUR')
      payload=LCMGID(authority,'SOUR')
      do ig=1,NGRP
        call EXPECTED_VECTOR64(2,ip,ig,expected64)
        call LCMGDL(payload,ig,found64)
        if (any(BITS64(found64) /= BITS64(expected64))) &
          call FAIL('feedback authority SOUR differs')
        expected32=real(expected64,real32)
        call LCMGDL(mirror,ig,found32)
        if (any(BITS32(found32) /= BITS32(expected32))) &
          call FAIL('feedback SOUR mirror differs')
      end do
      outer=LCMGID(item,'SPOT-QFISS')
      inner=LCMGIL(outer,1)
      payload=LCMGID(authority,'QFISS')
      do ig=1,NGRP
        call EXPECTED_VECTOR64(3,ip,ig,expected64)
        call LCMGDL(payload,ig,found64)
        if (any(BITS64(found64) /= BITS64(expected64))) &
          call FAIL('feedback authority QFISS differs')
        expected32=real(expected64,real32)
        call LCMGDL(inner,ig,found32)
        if (any(BITS32(found32) /= BITS32(expected32))) &
          call FAIL('feedback QFISS mirror differs')
      end do
    end do
  end subroutine VERIFY_FEEDBACK_INPUT


  elemental real(real32) function EXPECTED_LEAK32(plane)
    integer, intent(in) :: plane
    select case(plane)
    case(1)
      EXPECTED_LEAK32=0.125_real32
    case(2)
      EXPECTED_LEAK32=0.25_real32
    case(3)
      EXPECTED_LEAK32=0.5_real32
    case default
      EXPECTED_LEAK32=-1.0_real32
    end select
  end function EXPECTED_LEAK32


  subroutine EXPECTED_VECTOR64(field,plane,group,values)
    integer, intent(in) :: field, plane, group
    real(real64), intent(out) :: values(NUNK)
    integer :: iu, base

    do iu=1,NUNK
      select case(field)
      case(1)
        base=1000000+plane*100000+group*100+iu
      case(2)
        base=4000000+plane*100000+group*100+iu
      case(3)
        base=7000000+plane*100000+group*100+iu
      case default
        call FAIL('unknown expected vector field')
      end select
      values(iu)=nearest(real(base,real64),+1.0_real64)
    end do
  end subroutine EXPECTED_VECTOR64


  subroutine OPEN_FRESH(prefix,root)
    character(len=*), intent(in) :: prefix
    type(c_ptr), intent(out) :: root
    character(len=12) :: name

    object_counter=object_counter+1
    write(name,'("B2W",I6.6)') object_counter
    call LCMOP(root,name,0,1,0)
    call REQUIRE_ASSOCIATED(root,trim(prefix)//' memory root')
    if (.not. EMPTY_ROOT(root)) call FAIL(trim(prefix)//' root is not fresh')
  end subroutine OPEN_FRESH


  subroutine CLONE_ROOT(source,label,copy)
    type(c_ptr), intent(in) :: source
    character(len=*), intent(in) :: label
    type(c_ptr), intent(out) :: copy

    call OPEN_FRESH(label,copy)
    call LCMEQU(source,copy)
  end subroutine CLONE_ROOT


  logical function EMPTY_ROOT(root)
    type(c_ptr), intent(in) :: root
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, memory_backed

    EMPTY_ROOT=.false.
    if (.not. c_associated(root)) return
    call LCMINF(root,object_file,object_name,empty,object_length, &
        memory_backed)
    EMPTY_ROOT=memory_backed .and. empty .and. object_length == -1 .and. &
        trim(object_name) == '/'
  end function EMPTY_ROOT


  subroutine REQUIRE_ASSOCIATED(ptr,label)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: label
    if (.not. c_associated(ptr)) call FAIL(trim(label)//' is missing')
  end subroutine REQUIRE_ASSOCIATED


  subroutine REQUIRE_RECORD(root,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: actual_length, actual_type

    call LCMLEN(root,name,actual_length,actual_type)
    if (actual_length /= expected_length .or. actual_type /= expected_type) &
      call FAIL(trim(name)//' schema differs')
  end subroutine REQUIRE_RECORD


  subroutine REQUIRE_ABSENT(root,name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer :: actual_length, actual_type

    call LCMLEN(root,name,actual_length,actual_type)
    if (actual_length /= 0 .or. actual_type /= 99) &
      call FAIL(trim(name)//' is unexpectedly present')
  end subroutine REQUIRE_ABSENT


  subroutine REQUIRE_INTEGER(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected
    integer :: found

    call REQUIRE_RECORD(root,name,1,1)
    call LCMGET(root,name,found)
    if (found /= expected) call FAIL(trim(name)//' value differs')
  end subroutine REQUIRE_INTEGER


  subroutine REQUIRE_REAL32_BITS(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    real(real32), intent(in) :: expected
    real(real32) :: found

    call REQUIRE_RECORD(root,name,1,2)
    call LCMGET(root,name,found)
    if (BITS32(found) /= BITS32(expected)) &
      call FAIL(trim(name)//' REAL32 bits differ')
  end subroutine REQUIRE_REAL32_BITS


  subroutine REQUIRE_REAL64_BITS(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    real(real64), intent(in) :: expected
    real(real64) :: found

    call REQUIRE_RECORD(root,name,1,4)
    call LCMGET(root,name,found)
    if (BITS64(found) /= BITS64(expected)) &
      call FAIL(trim(name)//' REAL64 bits differ')
  end subroutine REQUIRE_REAL64_BITS


  subroutine REQUIRE_CHARACTER(root,name,count,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    integer, intent(in) :: count
    character(len=72) :: found

    call REQUIRE_RECORD(root,name,(count+3)/4,3)
    found=' '
    call LCMGTC(root,name,count,found)
    if (found(1:count) /= expected) &
      call FAIL(trim(name)//' character value differs')
  end subroutine REQUIRE_CHARACTER


  subroutine PUT_CHARACTER(root,name,count,value)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, value
    integer, intent(in) :: count
    character(len=72) :: padded
    integer :: copy_length

    padded=' '
    copy_length=min(count,len_trim(value))
    if (copy_length > 0) padded(1:copy_length)=value(1:copy_length)
    call LCMPTC(root,name,count,padded)
  end subroutine PUT_CHARACTER


  subroutine REQUIRE_EXACT_INVENTORY(root,names,label)
    type(c_ptr), intent(in) :: root
    character(len=12), intent(in) :: names(:)
    character(len=*), intent(in) :: label
    character(len=12) :: first_name, item_name
    character(len=72) :: object_file
    logical, allocatable :: seen(:)
    logical :: empty, memory_backed
    integer :: count, i, object_length

    call REQUIRE_ASSOCIATED(root,label)
    call LCMINF(root,object_file,item_name,empty,object_length,memory_backed)
    if (empty .or. object_length /= -1) &
      call FAIL(trim(label)//' is empty or is a list')
    allocate(seen(size(names)))
    seen=.false.
    item_name=' '
    call LCMNXT(root,item_name)
    if (item_name == ' ') call FAIL(trim(label)//' is empty')
    first_name=item_name
    count=0
    do
      count=count+1
      do i=1,size(names)
        if (item_name == names(i)) exit
      end do
      if (i > size(names)) call FAIL(trim(label)//' has extra record')
      if (seen(i)) call FAIL(trim(label)//' has duplicate record')
      seen(i)=.true.
      call LCMNXT(root,item_name)
      if (item_name == first_name) exit
      if (count > size(names)) call FAIL(trim(label)//' traversal overflow')
    end do
    if (count /= size(names) .or. .not. all(seen)) &
      call FAIL(trim(label)//' inventory differs')
    deallocate(seen)
  end subroutine REQUIRE_EXACT_INVENTORY


  subroutine FAIL(message)
    character(len=*), intent(in) :: message
    write(*,'(A)') 'B2W FIXTURE FAILURE: '//trim(message)
    error stop 'B2W synthetic fixture failed'
  end subroutine FAIL

end module B2W_FIXTURE_SUPPORT
