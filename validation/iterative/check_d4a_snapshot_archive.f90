program check_d4a_snapshot_archive
  ! Independent GANLIB-only audit of the three physical D4-A snapshots.
  ! No SVD, assembly, transport, axial solve or convergence routine is linked.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,real32
  implicit none

  integer, parameter :: nstate=40,expected_snap=3,expected_group=370
  integer, parameter :: expected_reg=132,expected_unk=144
  integer, parameter :: expected_mat=6,expected_surf=12,ncode=6
  integer, parameter :: max_path=72
  integer(int32), parameter :: mccg_epsi_bits=int(z'3727c5ac',int32)

  type(c_ptr) :: root,tracks,libraries,systems,fluxes
  type(c_ptr) :: track,library,macro,system,flux
  type(c_ptr) :: macro_groups,system_groups,flux_groups,source_groups
  character(len=1024) :: path
  character(len=96) :: owner
  integer :: listdim,isnap,igroup,ireg,i,length_found,type_found
  integer :: nreg,nunk,nmat,nsurf
  integer :: track_state(nstate),mccg_state(nstate),library_state(nstate)
  integer :: macro_state(nstate),system_state(nstate),flux_state(nstate)
  integer, allocatable :: matcod(:),keyflx(:),keyflx_anis(:)
  integer, allocatable :: keycur(:),nzon(:),icode(:),bc(:),seen_count(:)
  integer, allocatable :: flux_key(:)
  integer, allocatable :: matcod_ref(:),keyflx_ref(:),keycur_ref(:)
  integer, allocatable :: nzon_ref(:),icode_ref(:),bc_ref(:)
  real(real32), allocatable :: volume(:),v_mccg(:),albedo(:)
  real(real32), allocatable :: volume_ref(:),v_mccg_ref(:),albedo_ref(:)
  real(real32), allocatable :: unknown_flux(:),unknown_source(:)
  real(real32), allocatable :: regional_flux(:,:,:),keff(:)
  real(real32) :: real_param(4),minimum_flux,maximum_flux

  if (command_argument_count() /= 1) &
    call fail('EXPECTED ONE SNAPSHOT XSM PATH.')
  call get_command_argument(1,path)
  if ((len_trim(path) == 0).or.(len_trim(path) > max_path)) &
    call fail('XSM PATH IS EMPTY OR EXCEEDS THE GANLIB LIMIT.')

  call LCMOP(root,trim(path),2,2,0)
  call require_character(root,'SIGNATURE','L_ARCHIVE','ROOT')
  call require_record(root,'LISTDIM',1,1,'ROOT')
  call LCMGET(root,'LISTDIM',listdim)
  if (listdim /= expected_snap) call fail('DIRECT THREE-ITEM ARCHIVE EXPECTED.')
  call require_record(root,'TRACK',expected_snap,10,'ROOT')
  call require_record(root,'MICROLIB2',expected_snap,10,'ROOT')
  call require_record(root,'SYSTEM',expected_snap,10,'ROOT')
  call require_record(root,'FLUX',expected_snap,10,'ROOT')
  tracks=LCMGID(root,'TRACK')
  libraries=LCMGID(root,'MICROLIB2')
  systems=LCMGID(root,'SYSTEM')
  fluxes=LCMGID(root,'FLUX')

  allocate(regional_flux(expected_reg,expected_group,expected_snap))
  allocate(keff(expected_snap))
  regional_flux=0.0_real32
  keff=0.0_real32
  minimum_flux=huge(1.0_real32)
  maximum_flux=0.0_real32

  do isnap=1,expected_snap
    write(owner,'(A,I0)') 'SNAPSHOT ',isnap
    call require_directory_item(tracks,isnap,trim(owner)//' TRACK')
    call require_directory_item(libraries,isnap,trim(owner)//' LIBRARY')
    call require_directory_item(systems,isnap,trim(owner)//' SYSTEM')
    call require_directory_item(fluxes,isnap,trim(owner)//' FLUX')
    track=LCMGIL(tracks,isnap)
    library=LCMGIL(libraries,isnap)
    system=LCMGIL(systems,isnap)
    flux=LCMGIL(fluxes,isnap)

    call require_character(track,'SIGNATURE','L_TRACK',owner)
    call require_character(track,'TRACK-TYPE','MCCG',owner)
    call require_record(track,'STATE-VECTOR',nstate,1,owner)
    call require_record(track,'MCCG-STATE',nstate,1,owner)
    call require_record(track,'REAL-PARAM',4,2,owner)
    call LCMGET(track,'STATE-VECTOR',track_state)
    call LCMGET(track,'MCCG-STATE',mccg_state)
    call LCMGET(track,'REAL-PARAM',real_param)
    nreg=track_state(1)
    nunk=track_state(2)
    nmat=track_state(4)
    nsurf=track_state(5)
    if (any(track_state(1:6) /= &
        [expected_reg,expected_unk,1,expected_mat,expected_surf,1])) &
      call fail(trim(owner)//' INVALID D4-A TRACK TUPLE.')
    if (nunk /= nreg+nsurf) call fail(trim(owner)//' NUNK IS NOT NREG+NSURF.')
    if ((mccg_state(19) /= 1).or.(mccg_state(20) /= 1)) &
      call fail(trim(owner)//' NON-ISOTROPIC MCCG UNKNOWN LAYOUT.')
    if (any(.not.ieee_is_finite(real_param))) &
      call fail(trim(owner)//' NON-FINITE MCCG REAL-PARAM.')
    if ((transfer(real_param(1),0_int32) /= mccg_epsi_bits).or. &
        any(transfer(real_param(2:4),0_int32,3) /= 0_int32)) &
      call fail(trim(owner)//' MCCG REAL-PARAM CHANGED.')

    allocate(matcod(nreg),keyflx(nreg),keyflx_anis(nreg))
    allocate(keycur(nsurf),nzon(nunk),icode(ncode),bc(nsurf))
    allocate(volume(nreg),v_mccg(nunk),albedo(ncode),seen_count(nunk))
    call require_record(track,'MATCOD',nreg,1,owner)
    call require_record(track,'KEYFLX',nreg,1,owner)
    call require_record(track,'KEYFLX$ANIS',nreg,1,owner)
    call require_record(track,'KEYCUR$MCCG',nsurf,1,owner)
    call require_record(track,'NZON$MCCG',nunk,1,owner)
    call require_record(track,'ICODE',ncode,1,owner)
    call require_record(track,'BC-REFL+TRAN',nsurf,1,owner)
    call require_record(track,'VOLUME',nreg,2,owner)
    call require_record(track,'V$MCCG',nunk,2,owner)
    call require_record(track,'ALBEDO',ncode,2,owner)
    call LCMGET(track,'MATCOD',matcod)
    call LCMGET(track,'KEYFLX',keyflx)
    call LCMGET(track,'KEYFLX$ANIS',keyflx_anis)
    call LCMGET(track,'KEYCUR$MCCG',keycur)
    call LCMGET(track,'NZON$MCCG',nzon)
    call LCMGET(track,'ICODE',icode)
    call LCMGET(track,'BC-REFL+TRAN',bc)
    call LCMGET(track,'VOLUME',volume)
    call LCMGET(track,'V$MCCG',v_mccg)
    call LCMGET(track,'ALBEDO',albedo)
    if (any(matcod < 1).or.any(matcod > nmat)) &
      call fail(trim(owner)//' MATCOD OUT OF RANGE.')
    if (any(nzon(:nreg) /= matcod)) &
      call fail(trim(owner)//' REGION NZON/MATCOD MISMATCH.')
    if (any(nzon(nreg+1:) >= 0).or.any(abs(nzon(nreg+1:)) > ncode)) &
      call fail(trim(owner)//' INVALID SURFACE BOUNDARY CODES.')
    if (any(.not.ieee_is_finite(volume)).or.any(volume <= 0.0_real32)) &
      call fail(trim(owner)//' INVALID REGIONAL VOLUME.')
    if (any(.not.ieee_is_finite(v_mccg)).or.any(v_mccg <= 0.0_real32)) &
      call fail(trim(owner)//' INVALID MCCG MEASURE.')
    if (any(.not.ieee_is_finite(albedo))) &
      call fail(trim(owner)//' NON-FINITE ALBEDO.')
    if (any(bc < 1).or.any(bc > nsurf)) &
      call fail(trim(owner)//' INVALID REFLECTION/TRANSMISSION MAP.')
    seen_count=0
    do ireg=1,nreg
      if ((keyflx(ireg) < 1).or.(keyflx(ireg) > nunk)) &
        call fail(trim(owner)//' KEYFLX OUT OF RANGE.')
      if (keyflx_anis(ireg) /= keyflx(ireg)) &
        call fail(trim(owner)//' ISOTROPIC KEYFLX RECORDS DIFFER.')
      seen_count(keyflx(ireg))=seen_count(keyflx(ireg))+1
    enddo
    do i=1,nsurf
      if ((keycur(i) < 1).or.(keycur(i) > nunk)) &
        call fail(trim(owner)//' KEYCUR OUT OF RANGE.')
      seen_count(keycur(i))=seen_count(keycur(i))+1
    enddo
    if (any(seen_count /= 1)) &
      call fail(trim(owner)//' REGION/SURFACE KEYS DO NOT COVER NUNK ONCE.')

    if (isnap == 1) then
      allocate(matcod_ref(nreg),keyflx_ref(nreg),keycur_ref(nsurf))
      allocate(nzon_ref(nunk),icode_ref(ncode),bc_ref(nsurf))
      allocate(volume_ref(nreg),v_mccg_ref(nunk),albedo_ref(ncode))
      matcod_ref=matcod
      keyflx_ref=keyflx
      keycur_ref=keycur
      nzon_ref=nzon
      icode_ref=icode
      bc_ref=bc
      volume_ref=volume
      v_mccg_ref=v_mccg
      albedo_ref=albedo
    else
      if (any(matcod /= matcod_ref).or.any(keyflx /= keyflx_ref).or. &
          any(keycur /= keycur_ref).or.any(nzon /= nzon_ref).or. &
          any(icode /= icode_ref).or.any(bc /= bc_ref).or. &
          any(real32_bits(volume) /= real32_bits(volume_ref)).or. &
          any(real32_bits(v_mccg) /= real32_bits(v_mccg_ref)).or. &
          any(real32_bits(albedo) /= real32_bits(albedo_ref))) &
        call fail(trim(owner)//' GEOMETRY/TRACK MAP DIFFERS.')
    endif

    call require_character(library,'SIGNATURE','L_LIBRARY',owner)
    call require_record(library,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(library,'STATE-VECTOR',library_state)
    if ((library_state(1) /= nmat).or.(library_state(2) <= 0).or. &
        (library_state(3) /= expected_group).or.(library_state(4) /= 3)) &
      call fail(trim(owner)//' INVALID LIBRARY DIMENSIONS.')
    call require_record(library,'MACROLIB',-1,0,owner)
    macro=LCMGID(library,'MACROLIB')
    call require_character(macro,'SIGNATURE','L_MACROLIB',owner)
    call require_record(macro,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(macro,'STATE-VECTOR',macro_state)
    if ((macro_state(1) /= expected_group).or.(macro_state(2) /= nmat).or. &
        (macro_state(3) /= 3).or.(macro_state(4) <= 0)) &
      call fail(trim(owner)//' INVALID MACROLIB DIMENSIONS.')
    call require_record(macro,'GROUP',expected_group,10,owner)
    macro_groups=LCMGID(macro,'GROUP')

    call require_character(system,'SIGNATURE','L_PIJ',owner)
    call require_record(system,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(system,'STATE-VECTOR',system_state)
    if ((system_state(8) /= expected_group).or. &
        (system_state(9) /= nunk).or.(system_state(10) /= nmat)) &
      call fail(trim(owner)//' INVALID SYSTEM DIMENSIONS.')
    call require_record(system,'GROUP',expected_group,10,owner)
    system_groups=LCMGID(system,'GROUP')
    do igroup=1,expected_group
      call require_directory_item(macro_groups,igroup, &
        trim(owner)//' MACROLIB GROUP')
      call require_directory_item(system_groups,igroup, &
        trim(owner)//' SYSTEM GROUP')
    enddo

    call require_character(flux,'SIGNATURE','L_FLUX',owner)
    call require_record(flux,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(flux,'STATE-VECTOR',flux_state)
    if ((flux_state(1) /= expected_group).or.(flux_state(2) /= nunk)) &
      call fail(trim(owner)//' INVALID FLUX DIMENSIONS.')
    allocate(flux_key(nreg))
    call require_record(flux,'KEYFLX',nreg,1,owner)
    call LCMGET(flux,'KEYFLX',flux_key)
    if (any(flux_key /= keyflx_anis)) &
      call fail(trim(owner)//' FLUX/TRACK KEYFLX MISMATCH.')
    call require_record(flux,'K-EFFECTIVE',1,2,owner)
    call LCMGET(flux,'K-EFFECTIVE',keff(isnap))
    if ((.not.ieee_is_finite(keff(isnap))).or.(keff(isnap) <= 0.0_real32)) &
      call fail(trim(owner)//' INVALID K-EFFECTIVE.')
    call LCMLEN(flux,'SPOT-FS-EQN',length_found,type_found)
    if (length_found /= 0) &
      call fail(trim(owner)//' OFFLINE SNAPSHOT IS MARKED FIXED-SOURCE.')
    call require_record(flux,'FLUX',expected_group,10,owner)
    call require_record(flux,'SOUR',expected_group,10,owner)
    flux_groups=LCMGID(flux,'FLUX')
    source_groups=LCMGID(flux,'SOUR')
    allocate(unknown_flux(nunk),unknown_source(nunk))
    do igroup=1,expected_group
      call require_list_item(flux_groups,igroup,nunk,2,owner,'FLUX')
      call require_list_item(source_groups,igroup,nunk,2,owner,'SOUR')
      call LCMGDL(flux_groups,igroup,unknown_flux)
      call LCMGDL(source_groups,igroup,unknown_source)
      if (any(.not.ieee_is_finite(unknown_flux)).or. &
          any(.not.ieee_is_finite(unknown_source))) &
        call fail(trim(owner)//' NON-FINITE FLUX OR SOURCE.')
      do ireg=1,nreg
        regional_flux(ireg,igroup,isnap)=unknown_flux(keyflx(ireg))
        if (regional_flux(ireg,igroup,isnap) <= 0.0_real32) &
          call fail(trim(owner)//' NONPOSITIVE ACTIVE REGIONAL FLUX.')
        minimum_flux=min(minimum_flux,regional_flux(ireg,igroup,isnap))
        maximum_flux=max(maximum_flux,regional_flux(ireg,igroup,isnap))
      enddo
    enddo

    deallocate(unknown_source,unknown_flux,flux_key)
    deallocate(seen_count,albedo,v_mccg,volume,bc,icode,nzon,keycur)
    deallocate(keyflx_anis,keyflx,matcod)
  enddo

  if (all(real32_bits(regional_flux(:,:,1)) == &
          real32_bits(regional_flux(:,:,2))).or. &
      all(real32_bits(regional_flux(:,:,1)) == &
          real32_bits(regional_flux(:,:,3))).or. &
      all(real32_bits(regional_flux(:,:,2)) == &
          real32_bits(regional_flux(:,:,3)))) &
    call fail('TWO PHYSICAL SNAPSHOTS ARE BITWISE IDENTICAL.')
  call LCMCL(root,1)

  write(*,'(A,3(1X,ES24.16E3))') 'D4A-SNAPSHOT K-EFFECTIVE', &
    real(keff(1)),real(keff(2)),real(keff(3))
  write(*,'(A,2(1X,ES24.16E3))') 'D4A-SNAPSHOT ACTIVE-FLUX MIN/MAX', &
    real(minimum_flux),real(maximum_flux)
  write(*,'(A)') &
    'D4A-SNAPSHOT TUPLE NSNAP=3 NGRP=370 NREG=132 NMAT=6 NSURF=12 NUNK=144'
  write(*,'(A)') 'D4A-SNAPSHOT ARCHIVE GANLIB-ONLY PASS'

contains

  subroutine require_record(ptr,name,length_expected,type_expected,label)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,label
    integer, intent(in) :: length_expected,type_expected
    integer :: length_actual,type_actual
    call LCMLEN(ptr,name,length_actual,type_actual)
    if ((length_actual /= length_expected).or. &
        (type_actual /= type_expected)) &
      call fail(trim(label)//' INVALID RECORD '//trim(name)//'.')
  end subroutine require_record

  subroutine require_character(ptr,name,expected,label)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,expected,label
    character(len=12) :: actual
    call require_record(ptr,name,3,3,label)
    call LCMGTC(ptr,name,12,actual)
    if (actual /= expected) &
      call fail(trim(label)//' INVALID CHARACTER RECORD '//trim(name)//'.')
  end subroutine require_character

  subroutine require_directory_item(list_ptr,index0,label)
    type(c_ptr), intent(in) :: list_ptr
    integer, intent(in) :: index0
    character(len=*), intent(in) :: label
    integer :: length_actual,type_actual
    call LCMLEL(list_ptr,index0,length_actual,type_actual)
    if ((length_actual /= -1).or.(type_actual /= 0)) &
      call fail(trim(label)//' IS NOT A DIRECTORY.')
  end subroutine require_directory_item

  subroutine require_list_item(list_ptr,index0,length_expected, &
                               type_expected,label,item_name)
    type(c_ptr), intent(in) :: list_ptr
    integer, intent(in) :: index0,length_expected,type_expected
    character(len=*), intent(in) :: label,item_name
    integer :: length_actual,type_actual
    call LCMLEL(list_ptr,index0,length_actual,type_actual)
    if ((length_actual /= length_expected).or. &
        (type_actual /= type_expected)) &
      call fail(trim(label)//' INVALID '//trim(item_name)//' LIST ITEM.')
  end subroutine require_list_item

  pure elemental integer(int32) function real32_bits(value)
    real(real32), intent(in) :: value
    real32_bits=transfer(value,0_int32)
  end function real32_bits

  subroutine fail(message)
    character(len=*), intent(in) :: message
    write(*,'(A,A)') 'D4A-SNAPSHOT ARCHIVE FAIL: ',trim(message)
    error stop 1
  end subroutine fail

end program check_d4a_snapshot_archive
