program export_observables
  ! Read-only physical observables from authoritative FLUX64 and SPOT-KEFF64.
  ! No transport, reconstruction from a different basis, clipping, or fitting.
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr
  use, intrinsic :: iso_fortran_env, only: real32,real64,error_unit
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  type(c_ptr) :: track,axial,macro,flist,glist,gmacro
  character(len=1024) :: paths(4),filename
  integer :: ts(40),fs(40),ms(40),nr,nz,ng,nu,nm,nfis,ll4,ll5,nreg
  integer :: i,z,g,m,c,j,n,t,ios,out,base,idx,negative_flux,negative_end
  integer, allocatable :: key(:),mat(:),zone(:),negative(:)
  real(real32), allocatable :: vol(:),area(:),height(:),nufis(:)
  real(real64), allocatable :: u(:),phi(:),rate(:),current(:,:),minphi(:)
  real(real64) :: k,norm,coefficient,value,lo,hi,minall,escape,telescoping
  logical :: exists

  if(command_argument_count()/=4) call fail('USAGE: export_observables TRACK AXIAL MACRO NEW_PREFIX')
  do i=1,4
    call get_command_argument(i,paths(i),status=ios)
    if(ios/=0.or.len_trim(paths(i))==0) call fail('INVALID ARGUMENT')
    if(i<4) then
      if(len_trim(paths(i))>72) call fail('XSM INPUT PATH LONGER THAN 72; USE SHORT READ-ONLY NAMES')
      inquire(file=trim(paths(i)),exist=exists)
      if(.not.exists) call fail('MISSING INPUT')
    endif
  enddo
  call LCMOP(track,trim(paths(1)),2,2,0)
  call LCMOP(axial,trim(paths(2)),2,2,0)
  call LCMOP(macro,trim(paths(3)),2,2,0)
  call require(track,'STATE-VECTOR',40,1)
  call require(axial,'STATE-VECTOR',40,1)
  call require(macro,'STATE-VECTOR',40,1)
  call LCMGET(track,'STATE-VECTOR',ts)
  call LCMGET(axial,'STATE-VECTOR',fs)
  call LCMGET(macro,'STATE-VECTOR',ms)
  nr=ts(6); nz=ts(7); ng=fs(1); nu=ts(2); nm=ms(2); nfis=ms(4)
  ll4=ts(11); ll5=ts(12); nreg=ts(1)
  if(min(nr,nz,ng,nu,nm,nfis)<=0.or.nreg/=nr*nz.or.fs(2)/=nu.or.ms(1)/=ng) &
    call fail('INCONSISTENT DIMENSIONS')
  if(ll4<0.or.ll5/=nr*(nz+1).or.ll4+ll5>nu) call fail('INVALID CURRENT LAYOUT')
  call require(track,'KEYFLX',nreg,1)
  call require(track,'MATCOD',nreg,1)
  call require(track,'MAT1D',nz,1)
  call require(track,'VOLUME',nreg,2)
  call require(track,'AREA2D',nr,2)
  call require(track,'VOL1D',nz,2)
  call require(axial,'SPOT-KEFF64',1,4)
  call LCMGET(axial,'SPOT-KEFF64',k)
  if(.not.ieee_is_finite(k).or.k<=0) call fail('INVALID K64')
  allocate(key(nreg),mat(nreg),zone(nz),vol(nreg),area(nr),height(nz),nufis(nm*nfis))
  allocate(u(nu),phi(nreg),rate(nreg),current(nr,nz+1),minphi(nreg),negative(nreg))
  call LCMGET(track,'KEYFLX',key)
  call LCMGET(track,'MATCOD',mat)
  call LCMGET(track,'MAT1D',zone)
  call LCMGET(track,'VOLUME',vol)
  call LCMGET(track,'AREA2D',area)
  call LCMGET(track,'VOL1D',height)
  if(any(key<1).or.any(key>ll4).or.any(mat<1).or.any(mat>nm)) call fail('INVALID REGION MAP')
  if(any(vol<=0).or.any(area<=0).or.any(height<=0)) call fail('NONPOSITIVE VOLUME')
  if(.not.all(ieee_is_finite(vol)).or..not.all(ieee_is_finite(area)).or.&
     .not.all(ieee_is_finite(height))) call fail('NONFINITE GEOMETRY')
  do i=1,nreg
    if(any(key(:i-1)==key(i))) call fail('DUPLICATE SCALAR KEY')
  enddo
  call require(axial,'FLUX64',ng,10)
  call require(macro,'GROUP',ng,10)
  flist=LCMGID(axial,'FLUX64'); glist=LCMGID(macro,'GROUP')
  phi=0; rate=0; current=0; minphi=huge(1.0_real64); negative=0
  negative_end=0
  do g=1,ng
    call LCMLEL(flist,g,n,t)
    if(n/=nu.or.t/=4) call fail('FLUX64 GROUP LAYOUT')
    call LCMGDL(flist,g,u)
    if(.not.all(ieee_is_finite(u))) call fail('NONFINITE FLUX64')
    gmacro=LCMGIL(glist,g)
    call LCMLEN(gmacro,'NUSIGF',n,t)
    nufis=0
    if(n>0) then
      call require(gmacro,'NUSIGF',nm*nfis,2)
      call LCMGET(gmacro,'NUSIGF',nufis)
      if(.not.all(ieee_is_finite(nufis)).or.any(nufis<0)) call fail('INVALID NUSIGF')
    endif
    do i=1,nr
      base=ll4+(i-1)*(nz+1)
      if(u(base+1)>0) negative_end=negative_end+1
      if(u(base+nz+1)<0) negative_end=negative_end+1
      do z=1,nz+1
        current(i,z)=current(i,z)+real(area(i),real64)*u(base+z)
      enddo
      do z=1,nz
        j=(i-1)*nz+z; value=u(key(j)); m=mat(j)
        if(value<=0) negative(j)=negative(j)+1
        minphi(j)=min(minphi(j),value)
        phi(j)=phi(j)+real(vol(j),real64)*value
        coefficient=0
        do c=1,nfis
          coefficient=coefficient+real(nufis((c-1)*nm+m),real64)
        enddo
        rate(j)=rate(j)+real(vol(j),real64)*value*coefficient
      enddo
    enddo
  enddo
  norm=sum(rate)
  if(.not.ieee_is_finite(norm).or.norm<=0) call fail('NONPOSITIVE GLOBAL NU-FISSION')
  minall=minval(minphi); negative_flux=sum(negative)
  escape=sum(current(:,nz+1))-sum(current(:,1))
  telescoping=0
  do z=1,nz
    telescoping=telescoping+sum(current(:,z+1)-current(:,z))
  enddo
  call LCMCL(macro,1); call LCMCL(axial,1); call LCMCL(track,1)

  filename=trim(paths(4))//'.regions.csv'; call new_output(filename,out)
  write(out,'(A)') 'radial_region,axial_cell,physical_zone,material,volume_cm3,'// &
    'integrated_flux,integrated_nufission,flux_per_global_nufission,nufission_fraction,'// &
    'minimum_group_flux,nonpositive_group_flux_count'
  do i=1,nr
    do z=1,nz
      j=(i-1)*nz+z
      write(out,'(I0,3(A,I0),6(A,ES25.17E3),A,I0)') &
        i,',',z,',',zone(z),',',mat(j),',',real(vol(j),real64),',',phi(j),',',rate(j), &
        ',',phi(j)/norm,',',rate(j)/norm,',',minphi(j),',',negative(j)
    enddo
  enddo
  close(out)
  filename=trim(paths(4))//'.faces.csv'; call new_output(filename,out)
  write(out,'(A)') 'radial_region,face,z_cm,area_cm2,integrated_net_current_plus_z,current_per_global_nufission'
  do i=1,nr
    value=0
    do z=1,nz+1
      write(out,'(I0,A,I0,4(A,ES25.17E3))') i,',',z-1,',',value,',',real(area(i),real64), &
        ',',current(i,z),',',current(i,z)/norm
      if(z<=nz) value=value+real(height(z),real64)
    enddo
  enddo
  close(out)
  filename=trim(paths(4))//'.summary.txt'; call new_output(filename,out)
  write(out,'(A)') 'AXMAT SAVED REAL64 OBSERVABLES; NOT AN ACCURACY CERTIFICATE'
  write(out,'(A,ES25.17E3)') 'k64=',k
  write(out,'(A,I0)') 'radial_regions=',nr
  write(out,'(A,I0)') 'axial_cells=',nz
  write(out,'(A,I0)') 'groups=',ng
  write(out,'(A,ES25.17E3)') 'global_nufission=',norm
  write(out,'(A,ES25.17E3)') 'escape_per_nufission=',escape/norm
  write(out,'(A,ES25.17E3)') 'current_telescoping_difference=',(telescoping-escape)/norm
  write(out,'(A,ES25.17E3)') 'minimum_group_scalar_flux=',minall
  write(out,'(A,I0)') 'nonpositive_scalar_entries=',negative_flux
  write(out,'(A,I0)') 'negative_outward_end_region_group_currents=',negative_end
  close(out)
  write(*,'(A,ES25.17E3)') 'AXMAT-OBSERVABLES-COMPLETE k64=',k
contains
  subroutine fail(message)
    character(len=*),intent(in)::message
    write(error_unit,'(A)') trim(message)
    stop 1
  end subroutine
  subroutine require(obj,name,expected,type_expected)
    type(c_ptr),intent(in)::obj
    character(len=*),intent(in)::name
    integer,intent(in)::expected,type_expected
    integer::length,kind
    call LCMLEN(obj,name,length,kind)
    if(length/=expected.or.kind/=type_expected) call fail('INVALID RECORD '//name)
  end subroutine
  subroutine new_output(name,unit)
    character(len=*),intent(in)::name
    integer,intent(out)::unit
    integer::status
    open(newunit=unit,file=trim(name),status='new',action='write',iostat=status)
    if(status/=0) call fail('CANNOT CREATE NEW OUTPUT '//trim(name))
  end subroutine
end program
