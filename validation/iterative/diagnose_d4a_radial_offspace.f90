program diagnose_d4a_radial_offspace
  ! GANLIB-only diagnostic of saved ONLINE radial fields, never axial PERP.
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr
  use, intrinsic :: iso_fortran_env, only: real32,real64,int32,int64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  integer, parameter :: nr=132,nu=144,ng=370,np=3,nm=2
  type(c_ptr) :: basisroot,axial,radial,closed,groups,bgroup,tracks,ctracks,fluxes,cfluxes
  type(c_ptr) :: track,ctrack,flux,cflux,authority,cauthority,values,cvalues,mirrors,cmirrors
  character(len=1024) :: directory,prefix,argument
  integer :: epoch,p,g,i,j,k,unit,summary,key(nr),ckey(nr),fkey(nr),state(40),rank(ng),offset(ng+1)
  integer :: found_epoch,marker,ndim(4),dimension,ios,location(2)
  real(real32) :: volume(nr),cvolume(nr),b32(nr,nm,ng),axbasis(nr,nm,ng),v32(nr)
  real(real32) :: mirror(nu),cmirror(nu),fskeff,cfskeff
  real(real64) :: b(nr,nm,ng),w(nr,ng),gram(nm,nm,ng),computed(nm,nm),h(np),wsum
  real(real64) :: u(nu),cu(nu),norm2(ng,np),error2(ng,np),coeff(nm,ng,np),relative(ng,np)
  real(real64) :: plane_norm(np),plane_error(np),total_norm,total_error,share,ratio,maximum

  call get_command_argument(1,argument)
  if (trim(argument)=='--self-test' .or. trim(argument)=='--singular-test') then
    call synthetic(trim(argument)=='--singular-test')
    stop
  endif
  if (command_argument_count()/=3) call fail('expected SHORT_SOURCE_DIRECTORY EPOCH NEW_OUTPUT_PREFIX')
  directory=argument
  call get_command_argument(2,argument)
  read(argument,*,iostat=ios) epoch
  if (ios/=0) call fail('invalid epoch argument')
  if (epoch<=0) call fail('epoch must be a positive integer')
  call get_command_argument(3,prefix)
  if (len_trim(directory)+len('/closed_snapshots.xsm')>72) call fail('GANLIB path exceeds 72 characters')
  call LCMOP(basisroot,trim(directory)//'/basis_reference.xsm',2,2,0)
  call LCMOP(axial,trim(directory)//'/closed_axial.xsm',2,2,0)
  call LCMOP(radial,trim(directory)//'/candidate_radial.xsm',2,2,0)
  call LCMOP(closed,trim(directory)//'/closed_snapshots.xsm',2,2,0)
  call character_record(basisroot,'SIGNATURE','L_PIJ')
  call require(basisroot,'POD-RANK-G',ng,1)
  call LCMGET(basisroot,'POD-RANK-G',rank)
  if (any(rank/=2)) call fail('basis is not fixed rank two')
  call require(basisroot,'GROUP',ng,10)
  groups=LCMGID(basisroot,'GROUP')
  call character_record(axial,'SPOT-X-STATE','CLOSED')
  call require(axial,'SPOT-X-EPOCH',1,1)
  call LCMGET(axial,'SPOT-X-EPOCH',found_epoch)
  if (found_epoch/=epoch) call fail('axial epoch mismatch')
  call require(axial,'SPOT-X-DIMS',4,1)
  call LCMGET(axial,'SPOT-X-DIMS',ndim)
  if (any(ndim/=[1,ng,np,ng*np*nm])) call fail('axial POD dimensions mismatch')
  call require(axial,'SPOT-X-RANK',ng,1)
  call LCMGET(axial,'SPOT-X-RANK',rank)
  if (any(rank/=nm)) call fail('axial rank mismatch')
  call require(axial,'SPOT-X-GOFF',ng+1,1)
  call LCMGET(axial,'SPOT-X-GOFF',offset)
  if (any(offset/=[(4*i,i=0,ng)])) call fail('Gram offsets mismatch')
  call require(axial,'SPOT-X-BOFF',ng+1,1)
  call LCMGET(axial,'SPOT-X-BOFF',offset)
  if (any(offset/=[(nr*nm*i,i=0,ng)])) call fail('basis offsets mismatch')
  call require(axial,'SPOT-X-GRAM',nm*nm*ng,4)
  call require(axial,'SPOT-X-BASIS',nr*nm*ng,2)
  call require(axial,'SPOT-X-H',np,4)
  call LCMGET(axial,'SPOT-X-GRAM',gram)
  call LCMGET(axial,'SPOT-X-BASIS',axbasis)
  call LCMGET(axial,'SPOT-X-H',h)
  if (any(.not.ieee_is_finite(gram)) .or. any(.not.ieee_is_finite(h)) .or. any(h<=0)) &
    call fail('invalid stored Gram or height')
  do g=1,ng
    call directory_item(groups,g)
    bgroup=LCMGIL(groups,g)
    call require(bgroup,'NREG2D',1,1)
    call LCMGET(bgroup,'NREG2D',dimension)
    if (dimension/=nr) call fail('basis region dimension mismatch')
    call require(bgroup,'POD-NMODE',1,1)
    call LCMGET(bgroup,'POD-NMODE',dimension)
    if (dimension/=nm) call fail('group rank mismatch')
    call require(bgroup,'POD-BASIS',nr*nm,2)
    call require(bgroup,'VOL2D',nr,2)
    call LCMGET(bgroup,'POD-BASIS',b32(:,:,g))
    call LCMGET(bgroup,'VOL2D',v32)
    if (any(.not.ieee_is_finite(v32)) .or. any(v32<=0) .or. &
        any(.not.ieee_is_finite(b32(:,:,g)))) call fail('invalid basis or VOL2D')
    if (g==1) volume=v32
    if (any(transfer(v32,0_int32,nr)/=transfer(volume,0_int32,nr))) call fail('group VOL2D changed')
    if (any(transfer(b32(:,:,g),0_int32,nr*nm)/=transfer(axbasis(:,:,g),0_int32,nr*nm))) &
      call fail('closed axial basis differs from frozen reference')
    b(:,:,g)=real(b32(:,:,g),real64)
    wsum=sum(real(v32,real64))
    w(:,g)=real(v32,real64)/wsum
    ! Same order and precision as SPOSTATE; do not assume an identity Gram.
    computed=0
    do i=1,nm
      do j=1,nm
        do k=1,nr
          computed(i,j)=computed(i,j)+w(k,g)*b(k,i,g)*b(k,j,g)
        enddo
      enddo
    enddo
    if (any(transfer(computed,0_int64,nm*nm)/=transfer(gram(:,:,g),0_int64,nm*nm))) &
      call fail('stored Gram differs bitwise from frozen B^T W B')
  enddo
  call archive(radial,'RETURNED',epoch)
  call archive(closed,'CLOSED',epoch)
  tracks=LCMGID(radial,'TRACK'); ctracks=LCMGID(closed,'TRACK')
  fluxes=LCMGID(radial,'FLUX'); cfluxes=LCMGID(closed,'FLUX')
  do p=1,np
    call directory_item(tracks,p); call directory_item(ctracks,p)
    call directory_item(fluxes,p); call directory_item(cfluxes,p)
    track=LCMGIL(tracks,p); ctrack=LCMGIL(ctracks,p)
    flux=LCMGIL(fluxes,p); cflux=LCMGIL(cfluxes,p)
    call require(track,'STATE-VECTOR',40,1)
    call LCMGET(track,'STATE-VECTOR',state)
    if (any(state(1:6)/=[nr,nu,1,6,12,1])) call fail('unexpected radial tracking dimensions')
    call require(track,'KEYFLX',nr,1); call require(ctrack,'KEYFLX',nr,1)
    call require(track,'VOLUME',nr,2); call require(ctrack,'VOLUME',nr,2)
    call LCMGET(track,'KEYFLX',key); call LCMGET(ctrack,'KEYFLX',ckey)
    call LCMGET(track,'VOLUME',v32); call LCMGET(ctrack,'VOLUME',cvolume)
    if (any(key<1) .or. any(key>nu) .or. any(key/=ckey)) call fail('invalid or changed regional keys')
    do i=1,nr
      if (count(key==key(i))/=1) call fail('duplicate regional flux key')
    enddo
    if (any(transfer(v32,0_int32,nr)/=transfer(volume,0_int32,nr)) .or. &
        any(transfer(cvolume,0_int32,nr)/=transfer(volume,0_int32,nr))) call fail('TRACK/POD area mismatch')
    call child(flux,epoch,authority,values,mirrors,marker,fskeff,fkey)
    if (any(fkey/=key)) call fail('candidate child/track key mismatch')
    call child(cflux,epoch,cauthority,cvalues,cmirrors,marker,cfskeff,fkey)
    if (any(fkey/=key)) call fail('closed child/track key mismatch')
    if (transfer(fskeff,0_int32)/=transfer(cfskeff,0_int32)) call fail('radial equation receipt changed')
    do g=1,ng
      call list_record(values,g,nu,4); call list_record(cvalues,g,nu,4)
      call list_record(mirrors,g,nu,2); call list_record(cmirrors,g,nu,2)
      call LCMGDL(values,g,u); call LCMGDL(cvalues,g,cu)
      call LCMGDL(mirrors,g,mirror); call LCMGDL(cmirrors,g,cmirror)
      if (any(.not.ieee_is_finite(u)) .or. any(.not.ieee_is_finite(cu))) call fail('nonfinite radial authority')
      if (any(transfer(u,0_int64,nu)/=transfer(cu,0_int64,nu))) call fail('B2W changed radial authority FLUX')
      if (any(transfer(mirror,0_int32,nu)/=transfer(real(u,real32),0_int32,nu)) .or. &
          any(transfer(cmirror,0_int32,nu)/=transfer(real(u,real32),0_int32,nu))) &
        call fail('REAL32 flux mirror differs from REAL64 authority')
      call project(w(:,g),b(:,:,g),gram(:,:,g),u(key),coeff(:,g,p),norm2(g,p),error2(g,p))
    enddo
  enddo
  call LCMCL(basisroot,1); call LCMCL(axial,1); call LCMCL(radial,1); call LCMCL(closed,1)
  plane_norm=sum(norm2,dim=1); plane_error=sum(error2,dim=1)
  total_norm=sum(h*plane_norm); total_error=sum(h*plane_error)
  if (total_norm<=0) call fail('all online radial fields are zero')
  relative=-1
  where(norm2>0) relative=sqrt(error2/norm2)
  location=maxloc(relative); maximum=maxval(relative)
  open(newunit=unit,file=trim(prefix)//'_groups.csv',status='new',action='write')
  write(unit,'(A)') 'epoch,plane,group,weighted_norm2,offspace_norm2,relative_offspace,'// &
    'plane_norm_fraction,overall_norm_fraction,coefficient_1,coefficient_2'
  do p=1,np
    do g=1,ng
      share=0
      if (plane_norm(p)>0) share=norm2(g,p)/plane_norm(p)
      write(unit,'(I0,2(A,I0),7(A,ES25.16E3))') epoch,',',p,',',g,',',norm2(g,p),',',error2(g,p), &
        ',',relative(g,p),',',share,',',h(p)*norm2(g,p)/total_norm,',',coeff(1,g,p),',',coeff(2,g,p)
    enddo
  enddo
  close(unit)
  open(newunit=summary,file=trim(prefix)//'_summary.txt',status='new',action='write')
  write(summary,'(A)') 'DIAGNOSTIC_ONLY / REPORTED_ONLY; no accuracy or rank-adequacy acceptance threshold'
  write(summary,'(A)') 'u=candidate_radial/FLUX[plane]/SPOT-R64/FLUX[group], REAL64, regional KEYFLX'
  write(summary,'(A)') 'candidate and closed REAL64 flux: BITWISE_IDENTICAL; REAL32 mirrors: IDENTICAL'
  write(summary,'(A)') 'B=frozen REAL32 POD-BASIS promoted to REAL64; W=VOL2D/sum(VOL2D)'
  write(summary,'(A)') 'G=stored REAL64 SPOT-X-GRAM, recomputed B^T W B BITWISE_IDENTICAL'
  write(summary,'(A)') 'a=G^-1 B^T W u by existing lower-triangle Cholesky convention; u is not renormalized'
  write(summary,'(A)') 'ratio=-1 denotes zero-norm UNDEFINED, not zero error; no denominator floor'
  write(summary,'(A)') 'overall=sqrt(sum_pg H[p]*error2[p,g]/sum_pg H[p]*norm2[p,g])'
  write(summary,'(A)') 'Norm is current 370-group integrated-flux W-H norm, NOT reaction-rate or energy norm'
  write(summary,'(A)') 'No SPOT-X-PERP field was used; no axial reconstructed field was self-projected'
  do p=1,np
    ratio=-1
    if (plane_norm(p)>0) ratio=sqrt(plane_error(p)/plane_norm(p))
    write(summary,'(A,I0,A,I0,4(A,ES25.16E3))') 'epoch=',epoch,' plane=',p, &
      ' height=',h(p),' norm2=',plane_norm(p),' error2=',plane_error(p),' relative_offspace=',ratio
  enddo
  write(summary,'(A,I0,3(A,ES25.16E3))') 'epoch=',epoch,' overall_norm2=',total_norm, &
    ' overall_error2=',total_error,' overall_relative_offspace=',sqrt(total_error/total_norm)
  write(summary,'(A,I0,A,I0,2(A,ES25.16E3))') 'maximum_ratio_group=',location(1),' plane=',location(2), &
    ' ratio=',maximum,' overall_norm_fraction=',h(location(2))*norm2(location(1),location(2))/total_norm
  close(summary)
  write(*,'(A,I0)') 'D4A ONLINE RADIAL OFFSPACE DIAGNOSTIC WRITTEN: epoch=',epoch
contains
  subroutine project(weight,basis,matrix,field,a,n2,e2)
    real(real64), intent(in) :: weight(:),basis(:,:),matrix(2,2),field(:)
    real(real64), intent(out) :: a(2),n2,e2
    real(real64) :: rhs(2),lower(2,2),work(2),pivot,reconstructed
    integer :: r,c,z
    if (size(weight)/=size(field) .or. size(basis,1)/=size(field) .or. size(basis,2)/=2) &
      call fail('projection dimension mismatch')
    if (any(.not.ieee_is_finite(weight)) .or. any(weight<=0) .or. &
        any(.not.ieee_is_finite(field)) .or. any(.not.ieee_is_finite(basis))) call fail('invalid projection input')
    rhs=0; lower=0
    do r=1,2
      do z=1,size(field)
        rhs(r)=rhs(r)+weight(z)*basis(z,r)*field(z)
      enddo
      do c=1,r
        pivot=matrix(r,c)
        do z=1,c-1
          pivot=pivot-lower(r,z)*lower(c,z)
        enddo
        if (r==c) then
          if (.not.ieee_is_finite(pivot) .or. pivot<=0) call fail('singular Gram matrix')
          lower(r,c)=sqrt(pivot)
        else
          lower(r,c)=pivot/lower(c,c)
        endif
      enddo
    enddo
    do r=1,2
      work(r)=rhs(r)
      do z=1,r-1
        work(r)=work(r)-lower(r,z)*work(z)
      enddo
      work(r)=work(r)/lower(r,r)
    enddo
    do r=2,1,-1
      a(r)=work(r)
      do z=r+1,2
        a(r)=a(r)-lower(z,r)*a(z)
      enddo
      a(r)=a(r)/lower(r,r)
    enddo
    n2=0; e2=0
    do z=1,size(field)
      reconstructed=0
      do r=1,2
        reconstructed=reconstructed+basis(z,r)*a(r)
      enddo
      n2=n2+weight(z)*field(z)**2
      e2=e2+weight(z)*(field(z)-reconstructed)**2
    enddo
    if (any(.not.ieee_is_finite(a)) .or. .not.ieee_is_finite(n2) .or. &
        .not.ieee_is_finite(e2)) call fail('nonfinite projection result')
  end subroutine project
  subroutine synthetic(singular)
    logical, intent(in) :: singular
    real(real64) :: sw(3),sb(3,2),sg(2,2),su(3),sa(2),sn,se
    integer :: test
    sw=[0.25_real64,0.25_real64,0.5_real64]
    sb(:,1)=[2.0_real64,0.0_real64,0.0_real64]
    sb(:,2)=[2.0_real64,4.0_real64,0.0_real64]
    sg=reshape([1.0_real64,1.0_real64,1.0_real64,5.0_real64],[2,2])
    if (singular) sg(2,2)=1
    do test=1,4
      su=[2.0_real64,4.0_real64,3.0_real64]
      if (test==2) su(3)=0
      if (test==3) su=8*su
      if (test==4) su=0
      call project(sw,sb,sg,su,sa,sn,se)
      write(*,'(A,I0,4(1X,ES25.16E3))') 'SYNTHETIC ',test,sa,sn,se
    enddo
  end subroutine synthetic
  subroutine archive(root,lifecycle,wanted_epoch)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: lifecycle
    integer, intent(in) :: wanted_epoch
    type(c_ptr) :: auth
    integer :: value
    call character_record(root,'SIGNATURE','L_ARCHIVE')
    call require(root,'LISTDIM',1,1); call LCMGET(root,'LISTDIM',value)
    if (value/=np) call fail('not three-plane archive')
    call require(root,'SPOT-R64',-1,0)
    auth=LCMGID(root,'SPOT-R64')
    call character_record(auth,'STATE',lifecycle)
    call require(auth,'EPOCH',1,1); call LCMGET(auth,'EPOCH',value)
    if (value/=wanted_epoch) call fail('archive epoch mismatch')
    call require(root,'TRACK',np,10); call require(root,'FLUX',np,10)
  end subroutine archive
  subroutine child(root,wanted_epoch,auth,vals,mirrorlist,mark,fs,keyout)
    type(c_ptr), intent(in) :: root
    integer, intent(in) :: wanted_epoch
    type(c_ptr), intent(out) :: auth,vals,mirrorlist
    integer, intent(out) :: mark,keyout(nr)
    real(real32), intent(out) :: fs
    integer :: value
    call character_record(root,'SIGNATURE','L_FLUX')
    call require(root,'SPOT-FS-EQN',1,1); call LCMGET(root,'SPOT-FS-EQN',mark)
    if (mark/=1) call fail('not an online fixed-source radial solution')
    call require(root,'SPOT-FS-K',1,2); call LCMGET(root,'SPOT-FS-K',fs)
    if (.not.ieee_is_finite(fs) .or. fs<=0) call fail('invalid fixed-source equation receipt')
    call require(root,'KEYFLX',nr,1); call LCMGET(root,'KEYFLX',keyout)
    call require(root,'SPOT-R64',-1,0); auth=LCMGID(root,'SPOT-R64')
    call character_record(auth,'STATE','SOLVED')
    call require(auth,'EPOCH',1,1); call LCMGET(auth,'EPOCH',value)
    if (value/=wanted_epoch) call fail('solved child epoch mismatch')
    call require(auth,'FLUX',ng,10); vals=LCMGID(auth,'FLUX')
    call require(root,'FLUX',ng,10); mirrorlist=LCMGID(root,'FLUX')
  end subroutine child
  subroutine require(ptr,name,n,t)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name
    integer, intent(in) :: n,t
    integer :: actual_n,actual_t
    call LCMLEN(ptr,name,actual_n,actual_t)
    if (actual_n/=n .or. actual_t/=t) call fail('missing/wrong record: '//name)
  end subroutine require
  subroutine character_record(ptr,name,value)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,value
    character(len=12) :: actual
    call require(ptr,name,3,3); call LCMGTC(ptr,name,12,actual)
    if (actual/=value) call fail('unexpected character record: '//name)
  end subroutine character_record
  subroutine list_record(ptr,index,n,t)
    type(c_ptr), intent(in) :: ptr
    integer, intent(in) :: index,n,t
    integer :: actual_n,actual_t
    call LCMLEL(ptr,index,actual_n,actual_t)
    if (actual_n/=n .or. actual_t/=t) call fail('missing/wrong list item')
  end subroutine list_record
  subroutine directory_item(ptr,index)
    type(c_ptr), intent(in) :: ptr
    integer, intent(in) :: index
    call list_record(ptr,index,-1,0)
  end subroutine directory_item
  subroutine fail(message)
    character(len=*), intent(in) :: message
    write(*,'(A,A)') 'D4A RADIAL OFFSPACE INPUT/ALGEBRA ERROR: ',message
    error stop 1
  end subroutine fail
end program diagnose_d4a_radial_offspace
