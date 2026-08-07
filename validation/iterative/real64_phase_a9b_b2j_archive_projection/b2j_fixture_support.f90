module B2J_FIXTURE_SUPPORT
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use SPOR64_B2C, only : SPOR64_B2C_HOST_COMMITTED, SPOR64_B2C_PUBLISH
  use SPOR64_B2I, only : SPOR64_B2I_BOOTSTRAP_COMMITTED, &
      SPOR64_B2I_SEAL_BOOTSTRAP
  implicit none
  private

  integer, parameter, public :: B2J_NSTATE=40
  integer, parameter, public :: B2J_NGRP=370
  integer, parameter, public :: B2J_NREG=8
  integer, parameter, public :: B2J_NSNAP=3
  integer, parameter, public :: B2J_NUNKNO=14
  integer, parameter, public :: B2J_NMAT=8
  integer(int32), parameter :: B2C_TOL_BITS=int(z'348637bd',int32)

  public :: B2J_BUILD_CLOSED_PAIR
  public :: B2J_BITS32, B2J_BITS64
  public :: B2J_CLONE_OBJECT
  public :: B2J_COMPARE_CHARACTER_RECORD
  public :: B2J_COMPARE_INTEGER_RECORD
  public :: B2J_COMPARE_REAL32_RECORD
  public :: B2J_COMPARE_REAL64_RECORD
  public :: B2J_REQUIRE_ABSENT
  public :: B2J_REQUIRE_ASSOCIATED
  public :: B2J_REQUIRE_CHARACTER
  public :: B2J_REQUIRE_DIRECTORY_ITEM
  public :: B2J_REQUIRE_DISTINCT
  public :: B2J_REQUIRE_EMPTY_ROOT
  public :: B2J_REQUIRE_EXACT_INVENTORY
  public :: B2J_REQUIRE_ONLY_SENTINEL
  public :: B2J_REQUIRE_RECORD
  public :: B2J_VERIFY_DEEP_SENTINEL

contains

  subroutine B2J_BUILD_CLOSED_PAIR(axial_base,archive_base, &
      axial_track_base,axial_closed,archive_closed,b2c_calls,b2i_calls)
    type(c_ptr), intent(in) :: axial_base, archive_base, axial_track_base
    type(c_ptr), intent(out) :: axial_closed, archive_closed
    integer, intent(out) :: b2c_calls, b2i_calls
    integer :: status
    type(c_ptr) :: candidate

    b2c_calls=0
    b2i_calls=0
    call BUILD_LIGHTWEIGHT_CANDIDATE(archive_base,candidate,b2c_calls)
    call LCMOP(axial_closed,'B2J-AX0',0,1,0)
    call LCMOP(archive_closed,'B2J-AR0',0,1,0)
    call B2J_REQUIRE_ASSOCIATED(axial_closed,'closed AX output')
    call B2J_REQUIRE_ASSOCIATED(archive_closed,'closed archive output')
    call B2J_REQUIRE_EMPTY_ROOT(axial_closed)
    call B2J_REQUIRE_EMPTY_ROOT(archive_closed)

    b2i_calls=b2i_calls+1
    call SPOR64_B2I_SEAL_BOOTSTRAP(axial_closed,archive_closed, &
        axial_base,axial_track_base,candidate,status)
    if (status /= SPOR64_B2I_BOOTSTRAP_COMMITTED) &
      error stop 'production B2I rejected the real-derived candidate'
    if (b2c_calls /= B2J_NSNAP .or. b2i_calls /= 1) &
      error stop 'fixture producer-call inventory differs'

    call B2J_REQUIRE_CHARACTER(axial_closed,'SPOT-X-STATE',12,'CLOSED')
    call REQUIRE_INTEGER_VALUE(axial_closed,'SPOT-X-EPOCH',0)
    call B2J_REQUIRE_EXACT_INVENTORY(archive_closed, &
        [character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
         'TRACK','MICROLIB2','SYSTEM','FLUX','SPOT-R64'])
    call B2J_REQUIRE_CHARACTER(LCMGID(archive_closed,'SPOT-R64'), &
        'STATE',12,'CLOSED')
    call REQUIRE_INTEGER_VALUE(LCMGID(archive_closed,'SPOT-R64'), &
        'EPOCH',0)
    call LCMCL(candidate,2)
  end subroutine B2J_BUILD_CLOSED_PAIR


  subroutine BUILD_LIGHTWEIGHT_CANDIDATE(archive_base,candidate,b2c_calls)
    type(c_ptr), intent(in) :: archive_base
    type(c_ptr), intent(out) :: candidate
    integer, intent(inout) :: b2c_calls
    character(len=12) :: signature
    integer :: listdim, ip
    real(real64) :: iter_keff
    type(c_ptr) :: real_tracks, real_libraries, real_systems, real_fluxes
    type(c_ptr) :: out_tracks, out_libraries, out_systems, out_fluxes
    type(c_ptr) :: source_item, output_item

    call B2J_REQUIRE_CHARACTER(archive_base,'SIGNATURE',12,'L_ARCHIVE')
    call B2J_REQUIRE_RECORD(archive_base,'LISTDIM',1,1)
    call B2J_REQUIRE_RECORD(archive_base,'SPOT-ITER-K',1,4)
    call LCMGET(archive_base,'LISTDIM',listdim)
    call LCMGET(archive_base,'SPOT-ITER-K',iter_keff)
    if (listdim /= B2J_NSNAP) error stop 'real archive plane count differs'
    if (.not. ieee_is_finite(iter_keff) .or. iter_keff <= 0.0_real64) &
      error stop 'real archive K is invalid'

    real_tracks=LCMGID(archive_base,'TRACK')
    real_libraries=LCMGID(archive_base,'MICROLIB2')
    real_systems=LCMGID(archive_base,'SYSTEM')
    real_fluxes=LCMGID(archive_base,'FLUX')
    call B2J_REQUIRE_ASSOCIATED(real_tracks,'real TRACK list')
    call B2J_REQUIRE_ASSOCIATED(real_libraries,'real MICROLIB2 list')
    call B2J_REQUIRE_ASSOCIATED(real_systems,'real SYSTEM list')
    call B2J_REQUIRE_ASSOCIATED(real_fluxes,'real FLUX list')

    call LCMOP(candidate,'B2J-RAW',0,1,0)
    call B2J_REQUIRE_ASSOCIATED(candidate,'unsealed archive candidate')
    call B2J_REQUIRE_EMPTY_ROOT(candidate)
    signature='L_ARCHIVE'
    call LCMPTC(candidate,'SIGNATURE',12,signature)
    call LCMPUT(candidate,'LISTDIM',1,1,listdim)
    call LCMPUT(candidate,'SPOT-ITER-K',1,4,iter_keff)
    out_tracks=LCMLID(candidate,'TRACK',B2J_NSNAP)
    out_libraries=LCMLID(candidate,'MICROLIB2',B2J_NSNAP)
    out_systems=LCMLID(candidate,'SYSTEM',B2J_NSNAP)
    out_fluxes=LCMLID(candidate,'FLUX',B2J_NSNAP)
    call B2J_REQUIRE_ASSOCIATED(out_tracks,'candidate TRACK list')
    call B2J_REQUIRE_ASSOCIATED(out_libraries,'candidate MICROLIB2 list')
    call B2J_REQUIRE_ASSOCIATED(out_systems,'candidate SYSTEM list')
    call B2J_REQUIRE_ASSOCIATED(out_fluxes,'candidate FLUX list')

    do ip=1,B2J_NSNAP
      call B2J_REQUIRE_DIRECTORY_ITEM(real_tracks,ip)
      call B2J_REQUIRE_DIRECTORY_ITEM(real_libraries,ip)
      call B2J_REQUIRE_DIRECTORY_ITEM(real_systems,ip)
      call B2J_REQUIRE_DIRECTORY_ITEM(real_fluxes,ip)

      source_item=LCMGIL(real_tracks,ip)
      output_item=LCMDIL(out_tracks,ip)
      call B2J_REQUIRE_ASSOCIATED(output_item,'candidate TRACK item')
      call LCMEQU(source_item,output_item)
      call ADD_DEEP_SENTINEL(output_item,1000+ip)

      source_item=LCMGIL(real_libraries,ip)
      output_item=LCMDIL(out_libraries,ip)
      call B2J_REQUIRE_ASSOCIATED(output_item,'candidate MICROLIB2 item')
      call BUILD_MINIMAL_LIBRARY(source_item,output_item,2000+ip)

      source_item=LCMGIL(real_systems,ip)
      output_item=LCMDIL(out_systems,ip)
      call B2J_REQUIRE_ASSOCIATED(output_item,'candidate SYSTEM item')
      call BUILD_MINIMAL_SYSTEM(source_item,output_item,3000+ip)

      source_item=LCMGIL(real_fluxes,ip)
      output_item=LCMDIL(out_fluxes,ip)
      call B2J_REQUIRE_ASSOCIATED(output_item,'candidate FLUX item')
      call PUBLISH_B2C_CANDIDATE(source_item,output_item,b2c_calls)
      call ADD_DEEP_SENTINEL(output_item,4000+ip)
    end do
  end subroutine BUILD_LIGHTWEIGHT_CANDIDATE


  subroutine BUILD_MINIMAL_LIBRARY(source,target,sentinel)
    type(c_ptr), intent(in) :: source, target
    integer, intent(in) :: sentinel
    character(len=12) :: signature
    integer :: state(B2J_NSTATE), macro_state(B2J_NSTATE), ig
    type(c_ptr) :: source_macro, target_macro, target_groups, group_item

    call B2J_REQUIRE_CHARACTER(source,'SIGNATURE',12,'L_LIBRARY')
    call B2J_REQUIRE_RECORD(source,'STATE-VECTOR',B2J_NSTATE,1)
    call LCMGTC(source,'SIGNATURE',12,signature)
    call LCMGET(source,'STATE-VECTOR',state)
    source_macro=LCMGID(source,'MACROLIB')
    call B2J_REQUIRE_ASSOCIATED(source_macro,'real MACROLIB')
    call B2J_REQUIRE_CHARACTER(source_macro,'SIGNATURE',12,'L_MACROLIB')
    call B2J_REQUIRE_RECORD(source_macro,'STATE-VECTOR',B2J_NSTATE,1)
    call LCMGET(source_macro,'STATE-VECTOR',macro_state)

    call LCMPTC(target,'SIGNATURE',12,signature)
    call LCMPUT(target,'STATE-VECTOR',B2J_NSTATE,1,state)
    target_macro=LCMDID(target,'MACROLIB')
    call B2J_REQUIRE_ASSOCIATED(target_macro,'minimal MACROLIB')
    signature='L_MACROLIB'
    call LCMPTC(target_macro,'SIGNATURE',12,signature)
    call LCMPUT(target_macro,'STATE-VECTOR',B2J_NSTATE,1,macro_state)
    target_groups=LCMLID(target_macro,'GROUP',B2J_NGRP)
    call B2J_REQUIRE_ASSOCIATED(target_groups,'minimal MACROLIB GROUP')
    do ig=1,B2J_NGRP
      group_item=LCMDIL(target_groups,ig)
      call B2J_REQUIRE_ASSOCIATED(group_item,'minimal MACROLIB group')
    end do
    call ADD_DEEP_SENTINEL(target,sentinel)
  end subroutine BUILD_MINIMAL_LIBRARY


  subroutine BUILD_MINIMAL_SYSTEM(source,target,sentinel)
    type(c_ptr), intent(in) :: source, target
    integer, intent(in) :: sentinel
    character(len=12) :: signature, link_macro, link_track
    integer :: state(B2J_NSTATE), ig, snapshot
    real(real32) :: leakage(B2J_NGRP)
    type(c_ptr) :: target_groups, group_item

    call B2J_REQUIRE_CHARACTER(source,'SIGNATURE',12,'L_PIJ')
    call B2J_REQUIRE_RECORD(source,'STATE-VECTOR',B2J_NSTATE,1)
    call B2J_REQUIRE_CHARACTER(source,'LINK.MACRO',12,'MACRO0')
    call B2J_REQUIRE_CHARACTER(source,'LINK.TRACK',12,'TRACK')
    call B2J_REQUIRE_RECORD(source,'SPOT-LEAK1D',B2J_NGRP,2)
    call B2J_REQUIRE_RECORD(source,'SPOT-L1-SNAP',1,1)
    call LCMGTC(source,'SIGNATURE',12,signature)
    call LCMGTC(source,'LINK.MACRO',12,link_macro)
    call LCMGTC(source,'LINK.TRACK',12,link_track)
    call LCMGET(source,'STATE-VECTOR',state)
    call LCMGET(source,'SPOT-LEAK1D',leakage)
    call LCMGET(source,'SPOT-L1-SNAP',snapshot)
    if (snapshot /= sentinel-3000) &
      error stop 'real SYSTEM plane identity differs'
    if (.not. all(ieee_is_finite(leakage))) &
      error stop 'real SYSTEM leakage is nonfinite'

    call LCMPTC(target,'SIGNATURE',12,signature)
    call LCMPUT(target,'STATE-VECTOR',B2J_NSTATE,1,state)
    call LCMPTC(target,'LINK.MACRO',12,link_macro)
    call LCMPTC(target,'LINK.TRACK',12,link_track)
    call LCMPUT(target,'SPOT-LEAK1D',B2J_NGRP,2,leakage)
    call LCMPUT(target,'SPOT-L1-SNAP',1,1,snapshot)
    target_groups=LCMLID(target,'GROUP',B2J_NGRP)
    call B2J_REQUIRE_ASSOCIATED(target_groups,'minimal SYSTEM GROUP')
    do ig=1,B2J_NGRP
      group_item=LCMDIL(target_groups,ig)
      call B2J_REQUIRE_ASSOCIATED(group_item,'minimal SYSTEM group')
    end do
    call ADD_DEEP_SENTINEL(target,sentinel)
  end subroutine BUILD_MINIMAL_SYSTEM


  subroutine PUBLISH_B2C_CANDIDATE(history,target,b2c_calls)
    type(c_ptr), intent(in) :: history, target
    integer, intent(inout) :: b2c_calls
    character(len=4), parameter :: option='B0  '
    character(len=12), parameter :: macro_name='MACRO0'
    character(len=12), parameter :: track_name='TRACK'
    character(len=12), parameter :: system_name='SYSTEM'
    character(len=12) :: published_name
    integer :: ig, iu, length, record_type, status
    integer :: keyflx(B2J_NREG), imerge(B2J_NMAT)
    integer(int32) :: original_bits, mirror_bits
    real(real32) :: flux32(B2J_NUNKNO), source32(B2J_NUNKNO)
    real(real32) :: leakage32(B2J_NGRP), eps32
    real(real64) :: flux64(B2J_NUNKNO,B2J_NGRP)
    real(real64) :: source64(B2J_NUNKNO,B2J_NGRP)
    type(c_ptr) :: history_flux, history_source, authority, published

    call B2J_REQUIRE_RECORD(history,'FLUX',B2J_NGRP,10)
    call B2J_REQUIRE_RECORD(history,'SOUR',B2J_NGRP,10)
    call B2J_REQUIRE_RECORD(history,'KEYFLX',B2J_NREG,1)
    call B2J_REQUIRE_RECORD(history,'IMERGE-LEAK',B2J_NMAT,1)
    call B2J_REQUIRE_RECORD(history,'SPOT-LEAK1D',B2J_NGRP,2)
    history_flux=LCMGID(history,'FLUX')
    history_source=LCMGID(history,'SOUR')
    call B2J_REQUIRE_ASSOCIATED(history_flux,'historical root FLUX')
    call B2J_REQUIRE_ASSOCIATED(history_source,'historical root SOUR')
    call LCMGET(history,'KEYFLX',keyflx)
    call LCMGET(history,'IMERGE-LEAK',imerge)
    call LCMGET(history,'SPOT-LEAK1D',leakage32)
    if (any(imerge /= 1)) error stop 'historical merge map differs'
    if (.not. all(ieee_is_finite(leakage32))) &
      error stop 'historical leakage is nonfinite'

    do ig=1,B2J_NGRP
      call LCMLEL(history_flux,ig,length,record_type)
      if (length /= B2J_NUNKNO .or. record_type /= 2) &
        error stop 'historical FLUX list schema differs'
      call LCMLEL(history_source,ig,length,record_type)
      if (length /= B2J_NUNKNO .or. record_type /= 2) &
        error stop 'historical SOUR list schema differs'
      call LCMGDL(history_flux,ig,flux32)
      call LCMGDL(history_source,ig,source32)
      if (.not. all(ieee_is_finite(flux32)) .or. &
          .not. all(ieee_is_finite(source32))) &
        error stop 'historical terminal payload is nonfinite'
      flux64(:,ig)=real(flux32,real64)
      source64(:,ig)=real(source32,real64)
      do iu=1,B2J_NUNKNO
        if (flux64(iu,ig) < 0.0_real64) then
          flux64(iu,ig)=flux64(iu,ig)-spacing(flux64(iu,ig))
        else
          flux64(iu,ig)=flux64(iu,ig)+spacing(flux64(iu,ig))
        end if
        if (source64(iu,ig) < 0.0_real64) then
          source64(iu,ig)=source64(iu,ig)-spacing(source64(iu,ig))
        else
          source64(iu,ig)=source64(iu,ig)+spacing(source64(iu,ig))
        end if
        original_bits=transfer(flux32(iu),0_int32)
        mirror_bits=transfer(real(flux64(iu,ig),real32),0_int32)
        if (mirror_bits /= original_bits) &
          error stop 'FLUX witness changes its REAL32 mirror'
        original_bits=transfer(source32(iu),0_int32)
        mirror_bits=transfer(real(source64(iu,ig),real32),0_int32)
        if (mirror_bits /= original_bits) &
          error stop 'SOUR witness changes its REAL32 mirror'
      end do
    end do

    eps32=transfer(B2C_TOL_BITS,0.0_real32)
    write(published_name,'("B2J-B2C",I2.2)') b2c_calls+1
    call LCMOP(published,published_name,0,1,0)
    call B2J_REQUIRE_ASSOCIATED(published,'B2C publication stage')
    call B2J_REQUIRE_EMPTY_ROOT(published)
    b2c_calls=b2c_calls+1
    call SPOR64_B2C_PUBLISH(published,4,flux64,source64,keyflx,1,imerge, &
        leakage32,eps32,eps32,eps32,option,macro_name,track_name, &
        system_name,status)
    if (status /= SPOR64_B2C_HOST_COMMITTED) &
      error stop 'production B2C rejected real payload'
    call LCMEQU(published,target)
    call LCMCL(published,2)
    authority=LCMGID(target,'SPOT-R64')
    call B2J_REQUIRE_ASSOCIATED(authority,'published candidate authority')
    call B2J_REQUIRE_EXACT_INVENTORY(authority, &
        [character(len=12) :: 'FLUX','SOUR'])
  end subroutine PUBLISH_B2C_CANDIDATE


  subroutine ADD_DEEP_SENTINEL(root,sentinel)
    type(c_ptr), intent(in) :: root
    integer, intent(in) :: sentinel
    type(c_ptr) :: deep

    call LCMPUT(root,'B2I-SENT',1,1,sentinel)
    deep=LCMDID(root,'B2I-DEEP')
    call B2J_REQUIRE_ASSOCIATED(deep,'deep-copy sentinel directory')
    call LCMPUT(deep,'VALUE',1,1,sentinel)
  end subroutine ADD_DEEP_SENTINEL


  subroutine B2J_VERIFY_DEEP_SENTINEL(input,output,expected)
    type(c_ptr), intent(in) :: input, output
    integer, intent(in) :: expected
    integer :: input_root, output_root, input_deep, output_deep
    type(c_ptr) :: input_directory, output_directory

    call B2J_REQUIRE_RECORD(input,'B2I-SENT',1,1)
    call B2J_REQUIRE_RECORD(output,'B2I-SENT',1,1)
    call LCMGET(input,'B2I-SENT',input_root)
    call LCMGET(output,'B2I-SENT',output_root)
    if (input_root /= expected .or. output_root /= expected) &
      error stop 'deep-copy root sentinel differs'
    input_directory=LCMGID(input,'B2I-DEEP')
    output_directory=LCMGID(output,'B2I-DEEP')
    call B2J_REQUIRE_DISTINCT(input_directory,output_directory, &
        'deep-copy sentinel directory')
    call B2J_REQUIRE_RECORD(input_directory,'VALUE',1,1)
    call B2J_REQUIRE_RECORD(output_directory,'VALUE',1,1)
    call LCMGET(input_directory,'VALUE',input_deep)
    call LCMGET(output_directory,'VALUE',output_deep)
    if (input_deep /= expected .or. output_deep /= expected) &
      error stop 'deep-copy nested sentinel differs'
  end subroutine B2J_VERIFY_DEEP_SENTINEL


  subroutine B2J_COMPARE_CHARACTER_RECORD(input,output,name,count)
    type(c_ptr), intent(in) :: input, output
    character(len=*), intent(in) :: name
    integer, intent(in) :: count
    character(len=:), allocatable :: left, right
    integer :: words

    words=(count+3)/4
    call B2J_REQUIRE_RECORD(input,name,words,3)
    call B2J_REQUIRE_RECORD(output,name,words,3)
    allocate(character(len=count) :: left,right)
    left(:)=' '
    right(:)=' '
    call LCMGTC(input,name,count,left)
    call LCMGTC(output,name,count,right)
    if (left /= right) error stop 'copied character record differs'
  end subroutine B2J_COMPARE_CHARACTER_RECORD


  subroutine B2J_COMPARE_INTEGER_RECORD(input,output,name)
    type(c_ptr), intent(in) :: input, output
    character(len=*), intent(in) :: name
    integer :: nleft, tleft, nright, tright
    integer, allocatable :: left(:), right(:)

    call LCMLEN(input,name,nleft,tleft)
    call LCMLEN(output,name,nright,tright)
    if (nleft < 1 .or. tleft /= 1 .or. nright /= nleft .or. &
        tright /= tleft) error stop 'copied integer schema differs'
    allocate(left(nleft),right(nleft))
    call LCMGET(input,name,left)
    call LCMGET(output,name,right)
    if (any(left /= right)) error stop 'copied integer record differs'
  end subroutine B2J_COMPARE_INTEGER_RECORD


  subroutine B2J_COMPARE_REAL32_RECORD(input,output,name)
    type(c_ptr), intent(in) :: input, output
    character(len=*), intent(in) :: name
    integer :: nleft, tleft, nright, tright
    real(real32), allocatable :: left(:), right(:)

    call LCMLEN(input,name,nleft,tleft)
    call LCMLEN(output,name,nright,tright)
    if (nleft < 1 .or. tleft /= 2 .or. nright /= nleft .or. &
        tright /= tleft) error stop 'copied REAL32 schema differs'
    allocate(left(nleft),right(nleft))
    call LCMGET(input,name,left)
    call LCMGET(output,name,right)
    if (any(B2J_BITS32(left) /= B2J_BITS32(right))) &
      error stop 'copied REAL32 bits differ'
  end subroutine B2J_COMPARE_REAL32_RECORD


  subroutine B2J_COMPARE_REAL64_RECORD(input,output,name)
    type(c_ptr), intent(in) :: input, output
    character(len=*), intent(in) :: name
    integer :: nleft, tleft, nright, tright
    real(real64), allocatable :: left(:), right(:)

    call LCMLEN(input,name,nleft,tleft)
    call LCMLEN(output,name,nright,tright)
    if (nleft < 1 .or. tleft /= 4 .or. nright /= nleft .or. &
        tright /= tleft) error stop 'copied REAL64 schema differs'
    allocate(left(nleft),right(nleft))
    call LCMGET(input,name,left)
    call LCMGET(output,name,right)
    if (any(B2J_BITS64(left) /= B2J_BITS64(right))) &
      error stop 'copied REAL64 bits differ'
  end subroutine B2J_COMPARE_REAL64_RECORD


  subroutine B2J_REQUIRE_EXACT_INVENTORY(root,expected)
    type(c_ptr), intent(in) :: root
    character(len=12), intent(in) :: expected(:)
    character(len=12) :: first_name, item_name
    logical, allocatable :: found(:)
    integer :: count, i

    call B2J_REQUIRE_ASSOCIATED(root,'inventory root')
    allocate(found(size(expected)))
    found=.false.
    item_name=' '
    call LCMNXT(root,item_name)
    if (item_name == ' ') error stop 'inventory root is empty'
    first_name=item_name
    count=0
    do
      count=count+1
      if (count > size(expected)) error stop 'inventory has extra record'
      do i=1,size(expected)
        if (item_name == expected(i)) exit
      end do
      if (i > size(expected)) error stop 'inventory has unknown record'
      if (found(i)) error stop 'inventory has duplicate record'
      found(i)=.true.
      call LCMNXT(root,item_name)
      if (item_name == first_name) exit
    end do
    if (count /= size(expected) .or. .not. all(found)) &
      error stop 'exact inventory differs'
  end subroutine B2J_REQUIRE_EXACT_INVENTORY


  subroutine B2J_REQUIRE_CHARACTER(root,name,count,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    integer, intent(in) :: count
    character(len=:), allocatable :: found
    integer :: words

    words=(count+3)/4
    call B2J_REQUIRE_RECORD(root,name,words,3)
    allocate(character(len=count) :: found)
    found(:)=' '
    call LCMGTC(root,name,count,found)
    if (found /= expected) then
      write(*,'(A,1X,A,1X,A,1X,A)') 'CHARACTER-MISMATCH',trim(name), &
          trim(found),trim(expected)
      error stop 'character record differs'
    end if
  end subroutine B2J_REQUIRE_CHARACTER


  subroutine B2J_REQUIRE_RECORD(root,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: length, record_type

    call B2J_REQUIRE_ASSOCIATED(root,'record owner')
    call LCMLEN(root,name,length,record_type)
    if (length /= expected_length .or. record_type /= expected_type) &
      error stop 'record schema differs'
  end subroutine B2J_REQUIRE_RECORD


  subroutine B2J_REQUIRE_ABSENT(root,name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer :: length, record_type

    call B2J_REQUIRE_ASSOCIATED(root,'absence owner')
    call LCMLEN(root,name,length,record_type)
    if (length /= 0 .or. record_type /= 99) &
      error stop 'unexpected record is present'
  end subroutine B2J_REQUIRE_ABSENT


  subroutine B2J_REQUIRE_DIRECTORY_ITEM(list,index)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index
    integer :: length, record_type

    call B2J_REQUIRE_ASSOCIATED(list,'directory list')
    call LCMLEL(list,index,length,record_type)
    if (length /= -1 .or. record_type /= 0) &
      error stop 'list item is not a directory'
  end subroutine B2J_REQUIRE_DIRECTORY_ITEM


  subroutine B2J_REQUIRE_ASSOCIATED(pointer,owner)
    type(c_ptr), intent(in) :: pointer
    character(len=*), intent(in) :: owner

    if (.not. c_associated(pointer)) then
      write(*,'(A,1X,A)') 'UNASSOCIATED',trim(owner)
      error stop 'required GANLIB pointer is unassociated'
    end if
  end subroutine B2J_REQUIRE_ASSOCIATED


  subroutine B2J_REQUIRE_DISTINCT(left,right,owner)
    type(c_ptr), intent(in) :: left, right
    character(len=*), intent(in) :: owner

    call B2J_REQUIRE_ASSOCIATED(left,trim(owner)//' input')
    call B2J_REQUIRE_ASSOCIATED(right,trim(owner)//' output')
    if (c_associated(left,right)) error stop 'deep-copy pointer aliases input'
  end subroutine B2J_REQUIRE_DISTINCT


  subroutine B2J_REQUIRE_EMPTY_ROOT(root)
    type(c_ptr), intent(in) :: root
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, is_lcm

    call B2J_REQUIRE_ASSOCIATED(root,'empty-root candidate')
    call LCMINF(root,object_file,object_name,empty,object_length,is_lcm)
    if (.not. is_lcm .or. .not. empty .or. object_length /= -1 .or. &
        trim(object_name) /= '/') error stop 'rejected output was mutated'
  end subroutine B2J_REQUIRE_EMPTY_ROOT


  subroutine B2J_REQUIRE_ONLY_SENTINEL(root,expected)
    type(c_ptr), intent(in) :: root
    integer, intent(in) :: expected
    character(len=12) :: first_name, item_name
    integer :: found, count

    call B2J_REQUIRE_RECORD(root,'SENTINEL',1,1)
    call LCMGET(root,'SENTINEL',found)
    if (found /= expected) error stop 'collision sentinel changed'
    item_name=' '
    call LCMNXT(root,item_name)
    if (item_name /= 'SENTINEL') &
      error stop 'collision output gained an unexpected record'
    first_name=item_name
    count=0
    do
      count=count+1
      call LCMNXT(root,item_name)
      if (item_name == first_name) exit
    end do
    if (count /= 1) error stop 'collision output gained a new record'
  end subroutine B2J_REQUIRE_ONLY_SENTINEL


  subroutine B2J_CLONE_OBJECT(source,name,target)
    type(c_ptr), intent(in) :: source
    character(len=*), intent(in) :: name
    type(c_ptr), intent(out) :: target

    call LCMOP(target,name,0,1,0)
    call B2J_REQUIRE_ASSOCIATED(target,'clone target')
    call B2J_REQUIRE_EMPTY_ROOT(target)
    call LCMEQU(source,target)
  end subroutine B2J_CLONE_OBJECT


  subroutine REQUIRE_INTEGER_VALUE(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected
    integer :: found

    call B2J_REQUIRE_RECORD(root,name,1,1)
    call LCMGET(root,name,found)
    if (found /= expected) error stop 'integer record value differs'
  end subroutine REQUIRE_INTEGER_VALUE


  elemental integer(int32) function B2J_BITS32(value)
    real(real32), intent(in) :: value

    B2J_BITS32=transfer(value,0_int32)
  end function B2J_BITS32


  elemental integer(int64) function B2J_BITS64(value)
    real(real64), intent(in) :: value

    B2J_BITS64=transfer(value,0_int64)
  end function B2J_BITS64

end module B2J_FIXTURE_SUPPORT
