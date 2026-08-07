module B2S_FIXTURE_SUPPORT
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : error_unit, int32, int64, real32, real64
  use B2S_STUB_PROBES, only : B2S_QFISS_VALUE
  implicit none
  private

  integer, parameter, public :: B2S_NSNAP=3, B2S_NGRP=370
  integer, parameter, public :: B2S_NUNKNO=14, B2S_NREG=8
  integer, parameter, public :: B2S_NSTATE=40, B2S_NMAT=8
  integer, save :: object_counter=0

  public :: B2S_BUILD_HYBRID, B2S_CLONE_ROOT
  public :: B2S_REQUIRE_EMPTY_ROOT, B2S_REQUIRE_RECORD
  public :: B2S_REQUIRE_INTEGER, B2S_REQUIRE_CHARACTER

contains

  subroutine B2S_BUILD_HYBRID(seed_base,macro_base,track_base,system_base, &
      source_base,assembled,macros,sources,k64,rho64)
    type(c_ptr), intent(in) :: seed_base, macro_base, track_base
    type(c_ptr), intent(in) :: system_base, source_base
    type(c_ptr), intent(out) :: assembled
    type(c_ptr), intent(out) :: macros(B2S_NSNAP), sources(B2S_NSNAP)
    real(real64), intent(out) :: k64, rho64
    integer, parameter :: source_order(B2S_NSNAP)=[2,3,1]
    integer :: plane, slot
    character(len=12) :: name
    type(c_ptr) :: tracks, libraries, systems, fluxes
    type(c_ptr) :: item, embedded_macro, authority

    k64=nearest(1.0_real64,-1.0_real64)
    rho64=1.0_real64/k64
    if (transfer(rho64,0_int64) == &
        transfer(real(real(rho64,real32),real64),0_int64)) &
      error stop 'B2S fixture RHO lacks REAL64-only bits'

    call B2S_OPEN_FRESH('B2S-ASSEMB',assembled)
    call B2S_PUT_CHARACTER(assembled,'SIGNATURE',12,'L_ARCHIVE')
    call LCMPUT(assembled,'LISTDIM',1,1,B2S_NSNAP)
    call LCMPUT(assembled,'SPOT-ITER-K',1,4,k64)
    tracks=LCMLID(assembled,'TRACK',B2S_NSNAP)
    libraries=LCMLID(assembled,'MICROLIB2',B2S_NSNAP)
    systems=LCMLID(assembled,'SYSTEM',B2S_NSNAP)
    fluxes=LCMLID(assembled,'FLUX',B2S_NSNAP)
    if (.not. all([c_associated(tracks),c_associated(libraries), &
        c_associated(systems),c_associated(fluxes)])) &
      error stop 'B2S archive list creation failed'

    do plane=1,B2S_NSNAP
      item=LCMDIL(tracks,plane)
      call B2S_REQUIRE_ASSOCIATED(item,'TRACK item')
      call LCMEQU(track_base,item)
      call LCMPUT(item,'B2S-PLANE',1,1,plane)

      item=LCMDIL(libraries,plane)
      call B2S_REQUIRE_ASSOCIATED(item,'MICROLIB2 item')
      call B2S_PUT_CHARACTER(item,'SIGNATURE',12,'L_LIBRARY')
      call LCMPUT(item,'B2S-PLANE',1,1,plane)
      embedded_macro=LCMDID(item,'MACROLIB')
      call B2S_REQUIRE_ASSOCIATED(embedded_macro,'embedded MACROLIB')
      call LCMEQU(macro_base,embedded_macro)

      item=LCMDIL(systems,plane)
      call B2S_REQUIRE_ASSOCIATED(item,'SYSTEM item')
      call LCMEQU(system_base,item)
      call B2S_ADD_SYSTEM_AUTHORITY(item,plane,rho64)

      item=LCMDIL(fluxes,plane)
      call B2S_REQUIRE_ASSOCIATED(item,'PROJECTED item')
      call B2S_BUILD_PROJECTED_SEED(seed_base,item,plane, &
          LCMGIL(systems,plane),rho64)
    end do

    authority=LCMDID(assembled,'SPOT-R64')
    call B2S_REQUIRE_ASSOCIATED(authority,'archive authority')
    call LCMPUT(authority,'RHO',1,4,rho64)
    call LCMPUT(authority,'NPLANE',1,1,B2S_NSNAP)
    call B2S_PUT_CHARACTER(authority,'STATE',12,'ASSEMBLED')
    call LCMPUT(authority,'EPOCH',1,1,1)

    do slot=1,B2S_NSNAP
      write(name,'("B2S-M",I1,"-",I2.2)') source_order(slot),slot
      call B2S_CLONE_ROOT(macro_base,name,macros(slot))
      call LCMPUT(macros(slot),'SPOT-KEFF',1,2,real(k64,real32))
      write(name,'("B2S-Q",I1,"-",I2.2)') source_order(slot),slot
      call B2S_CLONE_ROOT(source_base,name,sources(slot))
      call LCMPUT(sources(slot),'SPOT-KEFF',1,2,real(k64,real32))
      call B2S_ADD_SOURCE_AUTHORITY(sources(slot),source_order(slot),rho64)
    end do
  end subroutine B2S_BUILD_HYBRID


  subroutine B2S_BUILD_PROJECTED_SEED(seed_base,seed,plane,system,rho64)
    type(c_ptr), intent(in) :: seed_base, seed, system
    integer, intent(in) :: plane
    real(real64), intent(in) :: rho64
    integer :: state_vector(B2S_NSTATE), imerge(B2S_NMAT)
    integer :: keyflx(B2S_NREG), group, unknown
    real(real32) :: eps(5), leakage(B2S_NGRP), vector32(B2S_NUNKNO)
    real(real64) :: vector64(B2S_NUNKNO)
    character(len=4) :: option
    character(len=12) :: signature, link_macro, link_track, link_system
    type(c_ptr) :: input_flux, root_flux, authority, authority_flux

    input_flux=LCMGID(seed_base,'FLUX')
    call B2S_REQUIRE_ASSOCIATED(input_flux,'base seed FLUX')
    root_flux=LCMLID(seed,'FLUX',B2S_NGRP)
    authority=LCMDID(seed,'SPOT-R64')
    authority_flux=LCMLID(authority,'FLUX',B2S_NGRP)
    call LCMPUT(authority,'RHO',1,4,rho64)
    do group=1,B2S_NGRP
      call LCMGDL(input_flux,group,vector32)
      call LCMPDL(root_flux,group,B2S_NUNKNO,2,vector32)
      vector64=real(vector32,real64)
      do unknown=1,B2S_NUNKNO
        if (vector64(unknown) < 0.0_real64) then
          vector64(unknown)=vector64(unknown)- &
              real(plane,real64)*spacing(vector64(unknown))
        else
          vector64(unknown)=vector64(unknown)+ &
              real(plane,real64)*spacing(vector64(unknown))
        end if
      end do
      call LCMPDL(authority_flux,group,B2S_NUNKNO,4,vector64)
    end do
    call B2S_PUT_CHARACTER(authority,'STATE',12,'PROJECTED')
    call LCMPUT(authority,'EPOCH',1,1,1)

    call LCMGTC(seed_base,'SIGNATURE',12,signature)
    call LCMGET(seed_base,'STATE-VECTOR',state_vector)
    call LCMGET(seed_base,'EPS-CONVERGE',eps)
    call LCMGET(seed_base,'IMERGE-LEAK',imerge)
    call LCMGET(seed_base,'KEYFLX',keyflx)
    call LCMGTC(seed_base,'OPTION',4,option)
    call LCMGTC(seed_base,'LINK.MACRO',12,link_macro)
    call LCMGTC(seed_base,'LINK.TRACK',12,link_track)
    call LCMGTC(seed_base,'LINK.SYSTEM',12,link_system)
    call LCMGET(system,'SPOT-LEAK1D',leakage)
    call LCMPTC(seed,'SIGNATURE',12,signature)
    call LCMPUT(seed,'STATE-VECTOR',B2S_NSTATE,1,state_vector)
    call LCMPUT(seed,'EPS-CONVERGE',5,2,eps)
    call LCMPUT(seed,'IMERGE-LEAK',B2S_NMAT,1,imerge)
    call LCMPUT(seed,'KEYFLX',B2S_NREG,1,keyflx)
    call LCMPTC(seed,'OPTION',4,option)
    call LCMPTC(seed,'LINK.MACRO',12,link_macro)
    call LCMPTC(seed,'LINK.TRACK',12,link_track)
    call LCMPTC(seed,'LINK.SYSTEM',12,link_system)
    call LCMPUT(seed,'SPOT-LEAK1D',B2S_NGRP,2,leakage)
  end subroutine B2S_BUILD_PROJECTED_SEED


  subroutine B2S_ADD_SYSTEM_AUTHORITY(system,plane,rho64)
    type(c_ptr), intent(in) :: system
    integer, intent(in) :: plane
    real(real64), intent(in) :: rho64
    type(c_ptr) :: authority

    call LCMPUT(system,'SPOT-L1-SNAP',1,1,plane)
    authority=LCMDID(system,'SPOT-R64')
    call B2S_REQUIRE_ASSOCIATED(authority,'SYSTEM authority')
    call LCMPUT(authority,'RHO',1,4,rho64)
    call B2S_PUT_CHARACTER(authority,'STATE',12,'ASSEMBLED')
    call LCMPUT(authority,'EPOCH',1,1,1)
  end subroutine B2S_ADD_SYSTEM_AUTHORITY


  subroutine B2S_ADD_SOURCE_AUTHORITY(source,plane,rho64)
    type(c_ptr), intent(in) :: source
    integer, intent(in) :: plane
    real(real64), intent(in) :: rho64
    integer :: group, unknown
    integer :: state(B2S_NSTATE)
    real(real32) :: q32(B2S_NUNKNO), qint(B2S_NGRP)
    real(real64) :: q64(B2S_NUNKNO)
    type(c_ptr) :: outer, inner, authority, qfiss

    state=0
    state(1:3)=[B2S_NGRP,B2S_NUNKNO,1]
    call LCMPUT(source,'STATE-VECTOR',B2S_NSTATE,1,state)
    call LCMPUT(source,'SPOT-FROZEN',1,1,1)
    outer=LCMGID(source,'DSOUR')
    call B2S_REQUIRE_ASSOCIATED(outer,'SOURCE DSOUR outer')
    inner=LCMGIL(outer,1)
    call B2S_REQUIRE_ASSOCIATED(inner,'SOURCE DSOUR inner')
    authority=LCMDID(source,'SPOT-R64')
    call B2S_REQUIRE_ASSOCIATED(authority,'SOURCE authority')
    call LCMPUT(authority,'RHO',1,4,rho64)
    call LCMPUT(authority,'PLANE',1,1,plane)
    call B2S_PUT_CHARACTER(authority,'STATE',12,'FROZEN-QFIS')
    qfiss=LCMLID(authority,'QFISS',B2S_NGRP)
    call B2S_REQUIRE_ASSOCIATED(qfiss,'SOURCE QFISS')
    do group=1,B2S_NGRP
      do unknown=1,B2S_NUNKNO
        q64(unknown)=B2S_QFISS_VALUE(plane,group,unknown)
      end do
      q32=real(q64,real32)
      qint(group)=sum(q32)
      call LCMPDL(inner,group,B2S_NUNKNO,2,q32)
      call LCMPDL(qfiss,group,B2S_NUNKNO,4,q64)
    end do
    call LCMPUT(source,'SPOT-QINT',B2S_NGRP,2,qint)
    call LCMPUT(authority,'EPOCH',1,1,1)
  end subroutine B2S_ADD_SOURCE_AUTHORITY


  subroutine B2S_CLONE_ROOT(input,name,output)
    type(c_ptr), intent(in) :: input
    character(len=*), intent(in) :: name
    type(c_ptr), intent(out) :: output

    call B2S_OPEN_FRESH(name,output)
    call LCMEQU(input,output)
  end subroutine B2S_CLONE_ROOT


  subroutine B2S_OPEN_FRESH(prefix,root)
    character(len=*), intent(in) :: prefix
    type(c_ptr), intent(out) :: root
    character(len=12) :: name

    object_counter=object_counter+1
    write(name,'("B2S",I5.5)') object_counter
    call LCMOP(root,name,0,1,0)
    call B2S_REQUIRE_ASSOCIATED(root,prefix)
  end subroutine B2S_OPEN_FRESH


  subroutine B2S_REQUIRE_ASSOCIATED(owner,what)
    type(c_ptr), intent(in) :: owner
    character(len=*), intent(in) :: what

    if (.not. c_associated(owner)) then
      write(error_unit,'(A)') trim(what)//' missing'
      error stop 'B2S fixture object missing'
    end if
  end subroutine B2S_REQUIRE_ASSOCIATED


  subroutine B2S_REQUIRE_RECORD(owner,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: owner
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: found_length, found_type

    call LCMLEN(owner,name,found_length,found_type)
    if (found_length /= expected_length .or. found_type /= expected_type) then
      write(error_unit,'(A)') 'B2S record schema differs: '//trim(name)
      error stop 'B2S record schema differs'
    end if
  end subroutine B2S_REQUIRE_RECORD


  subroutine B2S_REQUIRE_INTEGER(owner,name,expected)
    type(c_ptr), intent(in) :: owner
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected
    integer :: found

    call B2S_REQUIRE_RECORD(owner,name,1,1)
    call LCMGET(owner,name,found)
    if (found /= expected) then
      write(error_unit,'(A)') 'B2S integer differs: '//trim(name)
      error stop 'B2S integer differs'
    end if
  end subroutine B2S_REQUIRE_INTEGER


  subroutine B2S_REQUIRE_CHARACTER(owner,name,count,expected)
    type(c_ptr), intent(in) :: owner
    character(len=*), intent(in) :: name, expected
    integer, intent(in) :: count
    character(len=72) :: found

    call B2S_REQUIRE_RECORD(owner,name,(count+3)/4,3)
    found=' '
    call LCMGTC(owner,name,count,found)
    if (found(1:count) /= expected) then
      write(error_unit,'(A)') 'B2S character differs: '//trim(name)
      error stop 'B2S character differs'
    end if
  end subroutine B2S_REQUIRE_CHARACTER


  subroutine B2S_REQUIRE_EMPTY_ROOT(root)
    type(c_ptr), intent(in) :: root
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, is_lcm

    call LCMINF(root,object_file,object_name,empty,object_length,is_lcm)
    if (.not. is_lcm .or. .not. empty .or. object_length /= -1 .or. &
        trim(object_name) /= '/') error stop 'B2S rejected output mutated'
  end subroutine B2S_REQUIRE_EMPTY_ROOT


  subroutine B2S_PUT_CHARACTER(owner,name,count,value)
    type(c_ptr), intent(in) :: owner
    character(len=*), intent(in) :: name, value
    integer, intent(in) :: count
    character(len=72) :: padded

    padded=' '
    padded=value
    call LCMPTC(owner,name,count,padded)
  end subroutine B2S_PUT_CHARACTER

end module B2S_FIXTURE_SUPPORT
