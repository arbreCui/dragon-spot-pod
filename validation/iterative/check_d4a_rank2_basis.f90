program check_d4a_rank2_basis
  ! GANLIB-only audit of the D4-A POD basis built by production ASM/SPOPOD.
  ! No SVD, assembly, transport, feedback or convergence routine is linked.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  implicit none

  integer, parameter :: nstate=40,expected_group=370
  integer, parameter :: expected_reg=132,expected_snap=3,expected_rank=2
  integer, parameter :: expected_floor=3,expected_mix=18
  integer, parameter :: expected_axial_reg=396,expected_axial_unk=2772
  integer, parameter :: max_path=72

  type :: snapshot_data
    integer, allocatable :: matcod(:,:)
    real(real32), allocatable :: volume(:)
    real(real32), allocatable :: phi(:,:,:)
  end type snapshot_data

  type :: pod_group
    real(real32), allocatable :: volume(:)
    real(real32), allocatable :: basis(:)
    real(real32), allocatable :: coeff(:)
    real(real64) :: sigma(expected_snap)=0.0_real64
    real(real64) :: rec_err=0.0_real64
    real(real64) :: ortho_err=0.0_real64
  end type pod_group

  type :: pod_data
    integer :: state(nstate)=0
    integer :: rank(expected_group)=0
    real(real64) :: sigma(expected_snap,expected_group)=0.0_real64
    type(pod_group), allocatable :: group(:)
  end type pod_data

  character(len=1024) :: path(3)
  type(snapshot_data) :: snapshots
  type(pod_data) :: pod
  integer :: track_state(nstate),i,worst_gram,worst_projection
  integer :: axial_matcod(expected_axial_reg),ireg,isnap
  integer :: worst_tail_delta,worst_stored
  real(real32) :: track_area(expected_reg)
  real(real64) :: gram(expected_group),projection(expected_group)
  real(real64) :: tail(expected_group),tail_delta(expected_group)
  real(real64) :: stored(expected_group)

  if (command_argument_count() /= 3) &
    call fail('EXPECTED SNAPSHOT, AXIAL-TRACK AND BASIS XSM PATHS.')
  do i=1,3
    call get_command_argument(i,path(i))
    if ((len_trim(path(i)) == 0).or.(len_trim(path(i)) > max_path)) &
      call fail('AN XSM PATH IS EMPTY OR EXCEEDS THE GANLIB LIMIT.')
  enddo

  call load_snapshots(trim(path(1)),snapshots)
  call load_axial_track(trim(path(2)),track_state,track_area,axial_matcod)
  if (any(real32_bits(track_area) /= real32_bits(snapshots%volume))) &
    call fail('AXIAL TRACK AREA2D DIFFERS FROM SNAPSHOT VOLUME.')
  do ireg=1,expected_reg
    do isnap=1,expected_snap
      i=(ireg-1)*expected_floor+isnap
      if (axial_matcod(i) /= &
          snapshots%matcod(ireg,isnap)+(isnap-1)*6) &
        call fail('AXIAL MATERIAL BLOCK MAP DIFFERS FROM SNAPSHOTS.')
    enddo
  enddo
  call load_basis(trim(path(3)),track_state(2),pod)
  call verify_pod(snapshots,pod,gram,projection,tail,tail_delta,stored)

  worst_gram=maxloc(gram,dim=1)
  worst_projection=maxloc(projection,dim=1)
  worst_tail_delta=maxloc(tail_delta,dim=1)
  worst_stored=maxloc(stored,dim=1)
  call write_metric_group('D4A-RANK2 GRAM MAX DEFECT', &
    gram(worst_gram),worst_gram)
  call write_metric_group('D4A-RANK2 PROJECTION RELATIVE DEFECT', &
    projection(worst_projection),worst_projection)
  call write_metric('D4A-RANK2 SPECTRAL TAIL MIN',minval(tail))
  call write_metric('D4A-RANK2 SPECTRAL TAIL MAX',maxval(tail))
  call write_metric('D4A-RANK2 STORED ERROR MIN',minval(stored))
  call write_metric_group('D4A-RANK2 STORED ERROR MAX', &
    stored(worst_stored),worst_stored)
  call write_metric_group('D4A-RANK2 STORED/SPECTRAL MAX ABS DELTA', &
    tail_delta(worst_tail_delta),worst_tail_delta)
  write(*,'(A)') 'D4A-RANK2 DIMENSIONS NGRP=370 NREG2D=132 NSNAP=3 NMODE=2'
  write(*,'(A)') 'D4A-RANK2 STORED-DIAGNOSTICS BITWISE PASS'
  write(*,'(A)') &
    'D4A-RANK2 CLASSIFICATION OFFLINE_AXIAL_GEOMETRY_AND_FIXED_BASIS_BUILT'
  write(*,'(A)') 'D4A-RANK2 GANLIB-ONLY PASS'

contains

  subroutine load_snapshots(file_name,data)
    character(len=*), intent(in) :: file_name
    type(snapshot_data), intent(out) :: data
    type(c_ptr) :: root,tracks,fluxes,track,flux,group_flux
    integer :: listdim,isnap,igroup,ireg,length_found,type_found
    integer :: state(nstate),nreg,nunk
    integer, allocatable :: key(:)
    real(real32), allocatable :: volume(:),unknown_flux(:)
    character(len=96) :: owner

    call LCMOP(root,file_name,2,2,0)
    call require_character(root,'SIGNATURE','L_ARCHIVE','SNAPSHOT ROOT')
    call require_record(root,'LISTDIM',1,1,'SNAPSHOT ROOT')
    call LCMGET(root,'LISTDIM',listdim)
    if (listdim /= expected_snap) call fail('THREE SNAPSHOTS EXPECTED.')
    call require_record(root,'TRACK',expected_snap,10,'SNAPSHOT ROOT')
    call require_record(root,'FLUX',expected_snap,10,'SNAPSHOT ROOT')
    tracks=LCMGID(root,'TRACK')
    fluxes=LCMGID(root,'FLUX')
    allocate(data%volume(expected_reg))
    allocate(data%matcod(expected_reg,expected_snap))
    allocate(data%phi(expected_reg,expected_snap,expected_group))
    data%phi=0.0_real32

    do isnap=1,expected_snap
      write(owner,'(A,I0)') 'SNAPSHOT ',isnap
      call require_directory_item(tracks,isnap,trim(owner)//' TRACK')
      call require_directory_item(fluxes,isnap,trim(owner)//' FLUX')
      track=LCMGIL(tracks,isnap)
      flux=LCMGIL(fluxes,isnap)
      call require_record(track,'STATE-VECTOR',nstate,1,owner)
      call LCMGET(track,'STATE-VECTOR',state)
      nreg=state(1)
      nunk=state(2)
      if ((nreg /= expected_reg).or.(nunk /= 144)) &
        call fail(trim(owner)//' INVALID D4-A RADIAL DIMENSIONS.')
      allocate(key(nreg),volume(nreg),unknown_flux(nunk))
      call require_record(track,'MATCOD',nreg,1,owner)
      call require_record(track,'KEYFLX',nreg,1,owner)
      call require_record(track,'VOLUME',nreg,2,owner)
      call LCMGET(track,'MATCOD',data%matcod(:,isnap))
      call LCMGET(track,'KEYFLX',key)
      call LCMGET(track,'VOLUME',volume)
      if (any(key < 1).or.any(key > nunk)) &
        call fail(trim(owner)//' INVALID REGIONAL FLUX KEYS.')
      if (any(.not.ieee_is_finite(volume)).or. &
          any(volume <= 0.0_real32)) &
        call fail(trim(owner)//' INVALID RADIAL VOLUME.')
      if (isnap == 1) then
        data%volume=volume
      else if (any(real32_bits(volume) /= real32_bits(data%volume))) then
        call fail(trim(owner)//' RADIAL VOLUME BITS DIFFER.')
      endif

      call require_record(flux,'FLUX',expected_group,10,owner)
      group_flux=LCMGID(flux,'FLUX')
      do igroup=1,expected_group
        call LCMLEL(group_flux,igroup,length_found,type_found)
        if ((length_found /= nunk).or.(type_found /= 2)) &
          call fail(trim(owner)//' INVALID GROUP FLUX ITEM.')
        call LCMGDL(group_flux,igroup,unknown_flux)
        if (any(.not.ieee_is_finite(unknown_flux))) &
          call fail(trim(owner)//' NON-FINITE GROUP FLUX.')
        do ireg=1,nreg
          data%phi(ireg,isnap,igroup)=unknown_flux(key(ireg))
          if (data%phi(ireg,isnap,igroup) <= 0.0_real32) &
            call fail(trim(owner)//' NONPOSITIVE REGIONAL FLUX.')
        enddo
      enddo
      deallocate(unknown_flux,volume,key)
    enddo
    call LCMCL(root,1)
  end subroutine load_snapshots

  subroutine load_axial_track(file_name,state,area,matcod)
    character(len=*), intent(in) :: file_name
    integer, intent(out) :: state(nstate)
    real(real32), intent(out) :: area(expected_reg)
    integer, intent(out) :: matcod(expected_axial_reg)
    type(c_ptr) :: root
    integer :: mat1d(expected_floor),ncode(2),icode(2)
    real(real32) :: vol1d(expected_floor),zcode(2)

    call LCMOP(root,file_name,2,2,0)
    call require_character(root,'SIGNATURE','L_TRACK','AXIAL TRACK')
    call require_character(root,'TRACK-TYPE','SPOT','AXIAL TRACK')
    call require_record(root,'STATE-VECTOR',nstate,1,'AXIAL TRACK')
    call LCMGET(root,'STATE-VECTOR',state)
    if ((state(1) /= expected_axial_reg).or. &
        (state(2) /= expected_axial_unk).or.(state(3) /= 0).or. &
        (state(4) /= expected_mix).or.(state(5) /= 0).or. &
        (state(6) /= expected_reg).or. &
        (state(7) /= expected_floor).or.(state(8) /= expected_snap).or. &
        (state(9) /= 1).or.(state(10) /= 1).or. &
        (state(11) /= 1188).or.(state(12) /= 528).or. &
        (state(15) /= 8).or.(state(16) /= 3).or. &
        (state(27) /= 1)) &
      call fail('INVALID COARSE D4-A AXIAL TRACK DIMENSIONS.')
    call require_record(root,'AREA2D',expected_reg,2,'AXIAL TRACK')
    call require_record(root,'MATCOD',expected_axial_reg,1,'AXIAL TRACK')
    call require_record(root,'MAT1D',expected_floor,1,'AXIAL TRACK')
    call require_record(root,'VOL1D',expected_floor,2,'AXIAL TRACK')
    call require_record(root,'NCODE',2,1,'AXIAL TRACK')
    call require_record(root,'ICODE',2,1,'AXIAL TRACK')
    call require_record(root,'ZCODE',2,2,'AXIAL TRACK')
    call LCMGET(root,'AREA2D',area)
    call LCMGET(root,'MATCOD',matcod)
    call LCMGET(root,'MAT1D',mat1d)
    call LCMGET(root,'VOL1D',vol1d)
    call LCMGET(root,'NCODE',ncode)
    call LCMGET(root,'ICODE',icode)
    call LCMGET(root,'ZCODE',zcode)
    if (any(mat1d /= [1,2,3])) &
      call fail('AXIAL SNAPSHOT SCHEDULE IS NOT 1/2/3.')
    if (any(real32_bits(vol1d) /= &
            real32_bits([50.0_real32,50.0_real32,50.0_real32]))) &
      call fail('AXIAL LAYER HEIGHTS ARE NOT 50/50/50 CM.')
    if (any(ncode /= [1,1]).or.any(icode /= [0,0]).or. &
        any(real32_bits(zcode) /= 0_int32)) &
      call fail('AXIAL END BOUNDARIES ARE NOT VOID/VOID.')
    call LCMCL(root,1)
  end subroutine load_axial_track

  subroutine load_basis(file_name,track_nunk,data)
    character(len=*), intent(in) :: file_name
    integer, intent(in) :: track_nunk
    type(pod_data), intent(out) :: data
    type(c_ptr) :: root,groups,group_ptr
    integer :: igroup,nreg,nsnap,nmode
    integer :: fixb
    real(real64) :: rank_tolerance
    character(len=96) :: owner

    call LCMOP(root,file_name,2,2,0)
    call require_character(root,'SIGNATURE','L_PIJ','BASIS ROOT')
    call require_record(root,'STATE-VECTOR',nstate,1,'BASIS ROOT')
    call LCMGET(root,'STATE-VECTOR',data%state)
    if ((data%state(8) /= expected_group).or. &
        (data%state(9) /= track_nunk).or. &
        (data%state(10) /= expected_mix).or.(data%state(14) /= 1)) &
      call fail('INVALID SPOD BASIS STATE-VECTOR.')
    call require_record(root,'SPOT-FIXB',1,1,'BASIS ROOT')
    call LCMGET(root,'SPOT-FIXB',fixb)
    if (fixb /= 0) call fail('POD-BUILT BASIS EXPECTED.')
    call require_character(root,'SPOT-BTYPE','POD-BUILT','BASIS ROOT')
    call require_record(root,'POD-RANK-G',expected_group,1,'BASIS ROOT')
    call require_record(root,'POD-SIGMA-G', &
      expected_snap*expected_group,4,'BASIS ROOT')
    call LCMGET(root,'POD-RANK-G',data%rank)
    call LCMGET(root,'POD-SIGMA-G',data%sigma)
    if (any(data%rank /= expected_rank)) &
      call fail('RANK TWO WAS NOT REALIZED IN ALL GROUPS.')
    if (any(.not.ieee_is_finite(data%sigma)).or. &
        any(data%sigma < 0.0_real64)) &
      call fail('INVALID ROOT POD SPECTRA.')
    call require_record(root,'GROUP',expected_group,10,'BASIS ROOT')
    groups=LCMGID(root,'GROUP')
    allocate(data%group(expected_group))

    do igroup=1,expected_group
      write(owner,'(A,I0)') 'BASIS GROUP ',igroup
      call require_directory_item(groups,igroup,owner)
      group_ptr=LCMGIL(groups,igroup)
      call require_record(group_ptr,'NREG2D',1,1,owner)
      call require_record(group_ptr,'NSNAP',1,1,owner)
      call require_record(group_ptr,'POD-NMODE',1,1,owner)
      call LCMGET(group_ptr,'NREG2D',nreg)
      call LCMGET(group_ptr,'NSNAP',nsnap)
      call LCMGET(group_ptr,'POD-NMODE',nmode)
      if ((nreg /= expected_reg).or.(nsnap /= expected_snap).or. &
          (nmode /= expected_rank)) &
        call fail(trim(owner)//' INVALID POD DIMENSIONS.')
      allocate(data%group(igroup)%volume(nreg))
      allocate(data%group(igroup)%basis(nreg*nmode))
      allocate(data%group(igroup)%coeff(nmode*nsnap))
      call require_record(group_ptr,'VOL2D',nreg,2,owner)
      call require_record(group_ptr,'POD-BASIS',nreg*nmode,2,owner)
      call require_record(group_ptr,'POD-COEFF',nmode*nsnap,2,owner)
      call require_record(group_ptr,'POD-SIGMA',nsnap,4,owner)
      call require_record(group_ptr,'POD-REC-ERR',1,4,owner)
      call require_record(group_ptr,'POD-ORTHO',1,4,owner)
      call LCMGET(group_ptr,'VOL2D',data%group(igroup)%volume)
      call LCMGET(group_ptr,'POD-BASIS',data%group(igroup)%basis)
      call LCMGET(group_ptr,'POD-COEFF',data%group(igroup)%coeff)
      call LCMGET(group_ptr,'POD-SIGMA',data%group(igroup)%sigma)
      call LCMGET(group_ptr,'POD-REC-ERR',data%group(igroup)%rec_err)
      call LCMGET(group_ptr,'POD-ORTHO',data%group(igroup)%ortho_err)
      if (any(.not.ieee_is_finite(data%group(igroup)%volume)).or. &
          any(data%group(igroup)%volume <= 0.0_real32).or. &
          any(.not.ieee_is_finite(data%group(igroup)%basis)).or. &
          any(.not.ieee_is_finite(data%group(igroup)%coeff)).or. &
          any(.not.ieee_is_finite(data%group(igroup)%sigma)).or. &
          (.not.ieee_is_finite(data%group(igroup)%rec_err)).or. &
          (.not.ieee_is_finite(data%group(igroup)%ortho_err)).or. &
          (data%group(igroup)%rec_err < 0.0_real64).or. &
          (data%group(igroup)%ortho_err < 0.0_real64)) &
        call fail(trim(owner)//' INVALID STORED POD FIELD.')
      if ((data%group(igroup)%sigma(1) <= 0.0_real64).or. &
          any(data%group(igroup)%sigma(2:) > &
              data%group(igroup)%sigma(:expected_snap-1))) &
        call fail(trim(owner)//' INVALID SINGULAR-VALUE ORDER.')
      if (any(real64_bits(data%group(igroup)%sigma) /= &
              real64_bits(data%sigma(:,igroup)))) &
        call fail(trim(owner)//' ROOT/GROUP SPECTRA DIFFER BITWISE.')
      rank_tolerance=real(max(nreg,nsnap),real64)* &
        epsilon(1.0_real64)*data%group(igroup)%sigma(1)
      if (data%group(igroup)%sigma(2) <= rank_tolerance) &
        call fail(trim(owner)//' SECOND MODE FAILS PRODUCTION RANK RULE.')
    enddo
    call LCMCL(root,1)
  end subroutine load_basis

  subroutine verify_pod(snapshot,pod0,gram_out,projection_out,tail_out, &
                        tail_delta_out,stored_out)
    type(snapshot_data), intent(in) :: snapshot
    type(pod_data), intent(in) :: pod0
    real(real64), intent(out) :: gram_out(expected_group)
    real(real64), intent(out) :: projection_out(expected_group)
    real(real64), intent(out) :: tail_out(expected_group)
    real(real64), intent(out) :: tail_delta_out(expected_group)
    real(real64), intent(out) :: stored_out(expected_group)
    real(real64) :: weight(expected_reg)
    real(real64) :: shape(expected_reg,expected_snap)
    real(real64) :: recon(expected_reg,expected_snap)
    real(real64) :: rec_err,ortho_err,norm_full,norm_diff
    real(real64) :: inner,projection_value,projection_num,projection_den
    real(real64) :: total
    integer :: igroup,ireg,isnap,imode,jmode,index_b,index_c
    character(len=96) :: owner

    weight=real(snapshot%volume,real64)/ &
      sum(real(snapshot%volume,real64))
    do igroup=1,expected_group
      write(owner,'(A,I0)') 'POD ALGEBRA GROUP ',igroup
      if (any(real32_bits(pod0%group(igroup)%volume) /= &
              real32_bits(snapshot%volume))) &
        call fail(trim(owner)//' VOLUME DIFFERS FROM RAW SNAPSHOTS.')
      do isnap=1,expected_snap
        inner=sum(weight*real(snapshot%phi(:,isnap,igroup),real64))
        if ((.not.ieee_is_finite(inner)).or.(inner <= 0.0_real64)) &
          call fail(trim(owner)//' INVALID SNAPSHOT NORMALIZATION.')
        shape(:,isnap)=real(snapshot%phi(:,isnap,igroup),real64)/inner
      enddo

      recon=0.0_real64
      do isnap=1,expected_snap
        do imode=1,expected_rank
          index_c=(isnap-1)*expected_rank+imode
          index_b=(imode-1)*expected_reg+1
          recon(:,isnap)=recon(:,isnap)+real(pod0%group(igroup)%basis( &
            index_b:index_b+expected_reg-1),real64)* &
            real(pod0%group(igroup)%coeff(index_c),real64)
        enddo
      enddo
      norm_full=sqrt(sum(spread(weight,2,expected_snap)*shape*shape))
      norm_diff=sqrt(sum(spread(weight,2,expected_snap)* &
        (recon-shape)*(recon-shape)))
      if (norm_full <= 0.0_real64) &
        call fail(trim(owner)//' ZERO SNAPSHOT NORM.')
      rec_err=norm_diff/norm_full

      ortho_err=0.0_real64
      do imode=1,expected_rank
        do jmode=1,expected_rank
          inner=sum(weight*real(pod0%group(igroup)%basis( &
            (imode-1)*expected_reg+1:imode*expected_reg),real64)* &
            real(pod0%group(igroup)%basis( &
            (jmode-1)*expected_reg+1:jmode*expected_reg),real64))
          if (imode == jmode) inner=inner-1.0_real64
          ortho_err=max(ortho_err,abs(inner))
        enddo
      enddo
      if ((.not.ieee_is_finite(rec_err)).or. &
          (.not.ieee_is_finite(ortho_err))) &
        call fail(trim(owner)//' NON-FINITE RECOMPUTED DIAGNOSTIC.')
      if (real64_bits(rec_err) /= &
          real64_bits(pod0%group(igroup)%rec_err)) &
        call fail(trim(owner)//' RECONSTRUCTION ERROR DIFFERS BITWISE.')
      if (real64_bits(ortho_err) /= &
          real64_bits(pod0%group(igroup)%ortho_err)) &
        call fail(trim(owner)//' ORTHOGONALITY ERROR DIFFERS BITWISE.')

      projection_num=0.0_real64
      projection_den=0.0_real64
      do isnap=1,expected_snap
        do imode=1,expected_rank
          projection_value=0.0_real64
          do ireg=1,expected_reg
            projection_value=projection_value+weight(ireg)* &
              real(pod0%group(igroup)%basis( &
              (imode-1)*expected_reg+ireg),real64)*shape(ireg,isnap)
          enddo
          inner=real(pod0%group(igroup)%coeff( &
            (isnap-1)*expected_rank+imode),real64)
          projection_num=projection_num+(inner-projection_value)**2
          projection_den=projection_den+projection_value**2
        enddo
      enddo
      if (projection_den <= 0.0_real64) &
        call fail(trim(owner)//' ZERO PROJECTION NORM.')
      gram_out(igroup)=ortho_err
      projection_out(igroup)=sqrt(projection_num/projection_den)
      total=sum(pod0%group(igroup)%sigma**2)
      if ((.not.ieee_is_finite(total)).or.(total <= 0.0_real64)) &
        call fail(trim(owner)//' INVALID SPECTRAL NORM.')
      tail_out(igroup)=pod0%group(igroup)%sigma(3)/sqrt(total)
      tail_delta_out(igroup)=abs(rec_err-tail_out(igroup))
      stored_out(igroup)=pod0%group(igroup)%rec_err
    enddo
  end subroutine verify_pod

  subroutine require_record(ptr,name,length_expected,type_expected,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length_expected,type_expected
    integer :: length_found,type_found
    call LCMLEN(ptr,name,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) &
      call fail(trim(owner)//' INVALID RECORD '//trim(name)//'.')
  end subroutine require_record

  subroutine require_character(ptr,name,expected,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,expected,owner
    character(len=12) :: actual
    call require_record(ptr,name,3,3,owner)
    call LCMGTC(ptr,name,12,actual)
    if (actual /= expected) &
      call fail(trim(owner)//' INVALID CHARACTER RECORD '//trim(name)//'.')
  end subroutine require_character

  subroutine require_directory_item(list_ptr,index0,owner)
    type(c_ptr), intent(in) :: list_ptr
    integer, intent(in) :: index0
    character(len=*), intent(in) :: owner
    integer :: length_found,type_found
    call LCMLEL(list_ptr,index0,length_found,type_found)
    if ((length_found /= -1).or.(type_found /= 0)) &
      call fail(trim(owner)//' IS NOT A DIRECTORY.')
  end subroutine require_directory_item

  pure elemental integer(int32) function real32_bits(value)
    real(real32), intent(in) :: value
    real32_bits=transfer(value,0_int32)
  end function real32_bits

  pure elemental integer(int64) function real64_bits(value)
    real(real64), intent(in) :: value
    real64_bits=transfer(value,0_int64)
  end function real64_bits

  subroutine write_metric(label,value)
    character(len=*), intent(in) :: label
    real(real64), intent(in) :: value
    write(*,'(A,1X,ES25.17E3)') trim(label),value
  end subroutine write_metric

  subroutine write_metric_group(label,value,group_index)
    character(len=*), intent(in) :: label
    real(real64), intent(in) :: value
    integer, intent(in) :: group_index
    write(*,'(A,1X,ES25.17E3,1X,A,I0)') &
      trim(label),value,'GROUP=',group_index
  end subroutine write_metric_group

  subroutine fail(message)
    character(len=*), intent(in) :: message
    write(*,'(A,A)') 'D4A-RANK2 FAIL: ',trim(message)
    error stop 1
  end subroutine fail

end program check_d4a_rank2_basis
