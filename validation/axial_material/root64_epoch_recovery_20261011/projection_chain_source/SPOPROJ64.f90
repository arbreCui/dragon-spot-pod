!DECK SPOPROJ64
subroutine SPOPROJ64(nentry,hentry,ientry,jentry,kentry)
  ! Restrict the current global axial scalar flux to every archived 2D plane.
  ! The restriction is a volume average over all axial cells mapped to the
  ! snapshot. With the explicit FIXB option, reconstruct the feedback field
  ! from the canonical fixed-space coordinates previously written by
  ! SPOSTATE. This makes x=(a,1/k,L) a complete discrete map state.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  integer, parameter :: nstate=40
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)

  integer :: iflux(nstate),itrack(nstate),iflux2d(nstate),itrack2d(nstate)
  integer :: ngrp,nreg,nunk,nreg2d,nfloor,nsnap,nunk2d
  integer :: igr,ireg,i,ifloor,isnap,indic,nitma,a,nmode
  integer :: ncoef,total_basis,index_a,index_b,project_marker
  integer :: state_dims(4)
  integer, allocatable :: key3d(:),mat1d(:),key2d(:)
  integer, allocatable :: rank(:),offset(:),basis_offset(:)
  real, allocatable :: volume3d(:),area(:),basis_state(:),mirror3d(:),mirror2d(:)
  real(kind=dp), allocatable :: u3d(:),u2d(:)
  real :: flott
  real(kind=dp) :: weight,projected,floor_min,floor_max,group_max,relative
  real(kind=dp) :: dflott,norm,canonical_value,raw_value
  real(kind=dp) :: projection_num,projection_den,projection_perp
  real(kind=dp), allocatable :: coordinates(:)
  logical :: fixed_projection
  character(len=4) :: text4
  character(len=12) :: signature,track_type,norm_id
  type(c_ptr) :: jpax,jptracks,jpfluxes,kptrack,kpflux,jpplane,jpax32,jpplane32

  if (nentry /= 3) call XABORT('SPOPROJ64: THREE ENTRIES EXPECTED.')
  if (any((ientry /= 1).and.(ientry /= 2))) &
    call XABORT('SPOPROJ64: LCM ENTRIES EXPECTED.')
  if ((jentry(1) /= 1).or.any(jentry(2:3) /= 2)) &
    call XABORT('SPOPROJ64: MODIFIABLE ARCHIVE AND TWO INPUTS EXPECTED.')

  call LCMGTC(kentry(1),'SIGNATURE',12,signature)
  if (signature /= 'L_ARCHIVE') &
    call XABORT('SPOPROJ64: L_ARCHIVE EXPECTED.')
  call LCMGTC(kentry(2),'SIGNATURE',12,signature)
  if (signature /= 'L_FLUX') call XABORT('SPOPROJ64: L_FLUX EXPECTED.')
  call LCMGTC(kentry(3),'SIGNATURE',12,signature)
  if (signature /= 'L_TRACK') call XABORT('SPOPROJ64: L_TRACK EXPECTED.')
  call LCMGTC(kentry(3),'TRACK-TYPE',12,track_type)
  if (track_type /= 'SPOT') call XABORT('SPOPROJ64: SPOT TRACK EXPECTED.')

  fixed_projection=.false.
  call REDGET(indic,nitma,flott,text4,dflott)
  if ((indic == 3).and.(text4 == 'FIXB')) then
    fixed_projection=.true.
    call REDGET(indic,nitma,flott,text4,dflott)
  endif
  if ((indic /= 3).or.(text4 /= ';')) &
    call XABORT('SPOPROJ64: FIXB OR ; CHARACTER EXPECTED.')

  call LCMGET(kentry(2),'STATE-VECTOR',iflux)
  call LCMGET(kentry(3),'STATE-VECTOR',itrack)
  call LCMGET(kentry(1),'LISTDIM',nsnap)
  ngrp=iflux(1)
  nunk=iflux(2)
  nreg=itrack(1)
  nreg2d=itrack(6)
  nfloor=itrack(7)
  if ((ngrp <= 0).or.(nunk /= itrack(2)).or. &
      (nreg /= nreg2d*nfloor).or.(nsnap /= itrack(8)).or.(nsnap <= 0)) &
    call XABORT('SPOPROJ64: INCONSISTENT GLOBAL DIMENSIONS.')

  allocate(key3d(nreg),mat1d(nfloor),volume3d(nreg),area(nreg2d), &
      u3d(nunk),mirror3d(nunk))
  call LCMGET(kentry(3),'KEYFLX',key3d)
  call LCMGET(kentry(3),'MAT1D',mat1d)
  call LCMGET(kentry(3),'VOLUME',volume3d)
  call LCMGET(kentry(3),'AREA2D',area)
  if (any(.not.ieee_is_finite(area)).or.any(area <= 0.0)) &
    call XABORT('SPOPROJ64: INVALID RADIAL AREA.')

  projection_num=0.0_dp
  projection_den=0.0_dp
  if (fixed_projection) then
    call require_record(kentry(2),'SPOT-X-DIMS',4,1)
    call LCMGET(kentry(2),'SPOT-X-DIMS',state_dims)
    if ((state_dims(1) /= 1).or.(state_dims(2) /= ngrp).or. &
        (state_dims(3) /= nsnap).or.(state_dims(4) <= 0)) &
      call XABORT('SPOPROJ64: INVALID CANONICAL STATE DIMENSIONS.')
    ncoef=state_dims(4)
    allocate(rank(ngrp),offset(ngrp+1),basis_offset(ngrp+1))
    call require_record(kentry(2),'SPOT-X-RANK',ngrp,1)
    call require_record(kentry(2),'SPOT-X-OFF',ngrp+1,1)
    call require_record(kentry(2),'SPOT-X-BOFF',ngrp+1,1)
    call LCMGET(kentry(2),'SPOT-X-RANK',rank)
    call LCMGET(kentry(2),'SPOT-X-OFF',offset)
    call LCMGET(kentry(2),'SPOT-X-BOFF',basis_offset)
    if (any(rank <= 0).or.(offset(1) /= 0).or. &
        (basis_offset(1) /= 0).or.(offset(ngrp+1) /= ncoef)) &
      call XABORT('SPOPROJ64: INVALID CANONICAL STATE LAYOUT.')
    do igr=1,ngrp
      if (offset(igr+1)-offset(igr) /= nsnap*rank(igr)) &
        call XABORT('SPOPROJ64: INVALID COORDINATE OFFSETS.')
      if (basis_offset(igr+1)-basis_offset(igr) /= nreg2d*rank(igr)) &
        call XABORT('SPOPROJ64: INVALID BASIS OFFSETS.')
    enddo
    total_basis=basis_offset(ngrp+1)
    allocate(coordinates(ncoef),basis_state(total_basis))
    call require_record(kentry(2),'SPOT-X-A',ncoef,4)
    call require_record(kentry(2),'SPOT-X-BASIS',total_basis,2)
    call require_record(kentry(2),'SPOT-X-NORM',1,4)
    call require_record(kentry(2),'SPOT-X-NID',3,3)
    call LCMGET(kentry(2),'SPOT-X-A',coordinates)
    call LCMGET(kentry(2),'SPOT-X-BASIS',basis_state)
    call LCMGET(kentry(2),'SPOT-X-NORM',norm)
    call LCMGTC(kentry(2),'SPOT-X-NID',12,norm_id)
    if ((norm_id /= 'NUFISS-UNIT').or. &
        (.not.ieee_is_finite(norm)).or.(norm <= 0.0_dp).or. &
        any(.not.ieee_is_finite(coordinates)).or. &
        any(.not.ieee_is_finite(basis_state))) &
      call XABORT('SPOPROJ64: INVALID CANONICAL STATE.')
  endif

  call require_record(kentry(2),'FLUX64',ngrp,10)
  call require_record(kentry(2),'FLUX',ngrp,10)
  jpax=LCMGID(kentry(2),'FLUX64')
  jpax32=LCMGID(kentry(2),'FLUX')
  ! Validate the complete global numerical authority before any write.
  do igr=1,ngrp
    call read_native_pair(jpax,jpax32,igr,nunk,u3d,mirror3d)
  enddo
  jptracks=LCMGID(kentry(1),'TRACK')
  jpfluxes=LCMGID(kentry(1),'FLUX')

  do isnap=1,nsnap
    kptrack=LCMGIL(jptracks,isnap)
    call LCMGET(kptrack,'STATE-VECTOR',itrack2d)
    nunk2d=itrack2d(2)
    if ((itrack2d(1) /= nreg2d).or.(nunk2d <= 0)) &
      call XABORT('SPOPROJ64: INCONSISTENT RADIAL TRACKING.')
    allocate(key2d(nreg2d),u2d(nunk2d),mirror2d(nunk2d))
    call LCMGET(kptrack,'KEYFLX',key2d)
    kpflux=LCMGIL(jpfluxes,isnap)
    call LCMGET(kpflux,'STATE-VECTOR',iflux2d)
    if ((iflux2d(1) /= ngrp).or.(iflux2d(2) /= nunk2d)) &
      call XABORT('SPOPROJ64: INCONSISTENT RADIAL FLUX.')
    call require_record(kpflux,'FLUX64',ngrp,10)
    call require_record(kpflux,'FLUX',ngrp,10)
    jpplane=LCMGID(kpflux,'FLUX64')
    jpplane32=LCMGID(kpflux,'FLUX')
    ! Non-scalar native unknowns are preserved from the admitted plane.
    do igr=1,ngrp
      call read_native_pair(jpplane,jpplane32,igr,nunk2d,u2d,mirror2d)
    enddo

    do igr=1,ngrp
      call read_native_pair(jpax,jpax32,igr,nunk,u3d,mirror3d)
      call read_native_pair(jpplane,jpplane32,igr,nunk2d,u2d,mirror2d)
      group_max=0.0
      do ireg=1,nreg
        if (key3d(ireg) > 0) &
          group_max=max(group_max,abs(u3d(key3d(ireg))))
      enddo
      do i=1,nreg2d
        if (key2d(i) <= 0) cycle
        weight=0.0
        projected=0.0
        floor_min=huge(floor_min)
        floor_max=-huge(floor_max)
        do ifloor=1,nfloor
          if (mat1d(ifloor) /= isnap) cycle
          ireg=(i-1)*nfloor+ifloor
          if (key3d(ireg) <= 0) cycle
          projected=projected+volume3d(ireg)*u3d(key3d(ireg))
          weight=weight+volume3d(ireg)
          floor_min=min(floor_min,u3d(key3d(ireg)))
          floor_max=max(floor_max,u3d(key3d(ireg)))
        enddo
        if (weight <= 0.0) &
          call XABORT('SPOPROJ64: EMPTY SNAPSHOT RESTRICTION.')
        projected=projected/weight
        raw_value=real(projected,dp)
        if (fixed_projection) then
          nmode=rank(igr)
          canonical_value=0.0_dp
          do a=1,nmode
            index_a=offset(igr)+(isnap-1)*nmode+a
            index_b=basis_offset(igr)+(a-1)*nreg2d+i
            canonical_value=canonical_value+ &
              real(basis_state(index_b),dp)*coordinates(index_a)
          enddo
          projection_num=projection_num+real(area(i),dp)* &
            (raw_value/norm-canonical_value)**2
          projection_den=projection_den+real(area(i),dp)* &
            (raw_value/norm)**2
          projected=canonical_value
        endif
        if (.not.ieee_is_finite(projected).or.projected <= 0.0) then
          relative=projected/max(group_max,tiny(group_max))
          write(6,'(A,3I6,1P,4E13.5)') &
            'SPOPROJ64 INVALID G/SNAP/REG AVG/MIN/MAX/REL ', &
            igr,isnap,i,projected,floor_min,floor_max,relative
          call XABORT('SPOPROJ64: INVALID PROJECTED FLUX.')
        endif
        u2d(key2d(i))=projected
      enddo
      ! FLUX64 is the numerical output; FLUX is only its legacy mirror.
      mirror2d=real(u2d)
      if (any(.not.ieee_is_finite(mirror2d))) &
        call XABORT('SPOPROJ64: NON-FINITE LEGACY OUTPUT MIRROR.')
      call LCMPDL(jpplane,igr,nunk2d,4,u2d)
      call LCMPDL(jpplane32,igr,nunk2d,2,mirror2d)
    enddo
    write(6,'(A,I4)') 'SPOPROJ64 GLOBAL-TO-PLANE ',isnap
    deallocate(mirror2d,u2d,key2d)
  enddo

  if (fixed_projection) then
    if ((.not.ieee_is_finite(projection_num)).or. &
        (projection_num < 0.0_dp).or. &
        (.not.ieee_is_finite(projection_den)).or. &
        (projection_den <= 0.0_dp)) &
      call XABORT('SPOPROJ64: INVALID FIXED-SPACE PROJECTION DIAGNOSTIC.')
    projection_perp=sqrt(projection_num/projection_den)
    call LCMPUT(kentry(1),'SPOT-PJ-PERP',1,4,projection_perp)
    project_marker=2
    write(6,'(A,1P,E13.5)') &
      'SPOPROJ64 FIXED-SPACE RELATIVE OFFSPACE ',projection_perp
    deallocate(basis_state,coordinates,basis_offset,offset,rank)
  else
    project_marker=1
  endif
  call LCMPUT(kentry(1),'SPOT-PROJECT',1,1,project_marker)
  deallocate(mirror3d,u3d,area,volume3d,mat1d,key3d)

contains

  subroutine read_native_pair(native,mirror,group,nunknown,values,mirror_values)
    type(c_ptr), intent(in) :: native,mirror
    integer, intent(in) :: group,nunknown
    real(kind=dp), intent(out) :: values(nunknown)
    real, intent(out) :: mirror_values(nunknown)
    integer :: length,type_code,index
    call LCMLEL(native,group,length,type_code)
    if (length /= nunknown .or. type_code /= 4) &
      call XABORT('SPOPROJ64: EXACT TYPE4 NATIVE ITEM REQUIRED.')
    call LCMLEL(mirror,group,length,type_code)
    if (length /= nunknown .or. type_code /= 2) &
      call XABORT('SPOPROJ64: EXACT TYPE2 MIRROR ITEM REQUIRED.')
    call LCMGDL(native,group,values)
    call LCMGDL(mirror,group,mirror_values)
    if (any(.not.ieee_is_finite(values)) .or. &
        any(.not.ieee_is_finite(mirror_values))) &
      call XABORT('SPOPROJ64: NON-FINITE NATIVE/MIRROR ITEM.')
    do index=1,nunknown
      if (transfer(real(values(index)),0) /= transfer(mirror_values(index),0)) &
        call XABORT('SPOPROJ64: LEGACY MIRROR MISMATCH.')
    enddo
  end subroutine read_native_pair

  subroutine require_record(object,name,length,type_code)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name
    integer, intent(in) :: length,type_code
    integer :: actual_length,actual_type

    call LCMLEN(object,name,actual_length,actual_type)
    if ((actual_length /= length).or.(actual_type /= type_code)) &
      call XABORT('SPOPROJ64: INVALID '//trim(name)//' RECORD.')
  end subroutine require_record

end subroutine SPOPROJ64
