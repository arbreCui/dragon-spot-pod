subroutine SPOTCOLTRACE(track,it,ng,nun,nreg,nmat,nfis,mat,key,vol,nuf,flux,akeep,eext,einr)
  ! Passive diagnostic of an unconverged physical-coordinate eigen-iteration.
  ! No solver array or LCM object is changed; the snapshot is not a terminal.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  type(c_ptr),intent(in) :: track
  integer,intent(in) :: it,ng,nun,nreg,nmat,nfis,mat(nreg),key(nreg)
  real,intent(in) :: vol(nreg),nuf(0:nmat,nfis,ng)
  real(dp),intent(in) :: flux(nun,ng,3),akeep(3),eext,einr
  integer :: st(40),nf,nr,r,g,z,reg,k,j,unit,valid
  real(dp),allocatable :: f(:,:),fraction(:,:),shape(:),growth(:)
  real(dp) :: ft(2),xs,x,y,w,num,den,local_num,local_den,eunk,gn,gf,df
  real(dp) :: nom,denom,dmu,r1,r2,global_shape
  character(32) :: label
  call LCMGET(track,'STATE-VECTOR',st)
  nf=st(7);nr=st(6)
  if(min(nf,nr,ng,nun,nmat,nfis)<=0.or.nr*nf/=nreg.or.st(2)/=nun) error stop 'column trace dimensions'
  if(any(key<1).or.any(key>nun).or.any(mat<1).or.any(mat>nmat)) error stop 'column trace mapping'
  if(any(.not.ieee_is_finite(flux)).or.any(.not.ieee_is_finite(akeep))) error stop 'column trace finite'
  allocate(f(nr,2),fraction(nr,2),shape(nr),growth(nr))
  f=0;shape=0;growth=0
  do g=1,ng
    do r=1,nr
      do z=1,nf
        reg=(r-1)*nf+z;k=key(reg);xs=0
        do j=1,nfis
          xs=xs+real(nuf(mat(reg),j,g),dp)
        enddo
        do j=1,2
          f(r,j)=f(r,j)+real(vol(reg),dp)*xs*flux(k,g,j+1)
        enddo
      enddo
    enddo
  enddo
  ft=sum(f,dim=1)
  if(any(ft<=0)) error stop 'column trace global fission norm'
  fraction(:,1)=f(:,1)/ft(1);fraction(:,2)=f(:,2)/ft(2)
  num=0;den=0;eunk=0
  do g=1,ng
    gn=0;gf=0
    do reg=1,nreg
      k=key(reg);w=real(vol(reg),dp)
      x=flux(k,g,2)/ft(1);y=flux(k,g,3)/ft(2)
      num=num+w*(y-x)**2;den=den+w*y*y
      gn=max(gn,abs(flux(k,g,3)-flux(k,g,2)));gf=max(gf,abs(flux(k,g,3)))
    enddo
    if(gf<=0) error stop 'column trace zero group scalar flux'
    eunk=max(eunk,gn/gf)
  enddo
  global_shape=sqrt(num/den)
  do r=1,nr
    if(any(f(r,:)<=0)) cycle
    growth(r)=fraction(r,2)/fraction(r,1)
    local_num=0;local_den=0
    do g=1,ng
      do z=1,nf
        reg=(r-1)*nf+z;k=key(reg);w=real(vol(reg),dp)
        x=flux(k,g,2)/f(r,1);y=flux(k,g,3)/f(r,2)
        local_num=local_num+w*(y-x)**2;local_den=local_den+w*y*y
      enddo
    enddo
    shape(r)=sqrt(local_num/local_den)
  enddo
  ! Exactly the REAL64 acceleration routine's candidate-factor arithmetic.
  nom=0;denom=0
  do g=1,ng
    do k=1,nun
      r1=flux(k,g,2)-flux(k,g,1);r2=flux(k,g,3)-flux(k,g,2)
      nom=nom+r1*(r2-r1);denom=denom+(r2-r1)*(r2-r1)
    enddo
  enddo
  dmu=1
  if(denom>0) dmu=-nom/denom
  df=sum(abs(fraction(:,2)-fraction(:,1)))
  write(*,'(a,1x,i0,11(1x,es25.17e3))') 'COLUMN-ITER',it,akeep(2),akeep(3),eext,einr, &
       eunk,global_shape,df,dmu,nom,denom,maxval(shape)
  do r=1,nr
    valid=merge(1,0,all(f(r,:)>0))
    write(*,'(a,3(1x,i0),6(1x,es25.17e3))') 'COLUMN-FISSION',it,r,valid, &
         f(r,:),fraction(r,:),growth(r),shape(r)
  enddo
  if(it==10) then
    ! Diagnostic checkpoint of old/input/raw fields only; never an L_FLUX result.
    label='UNACCEPTED_COLUMN_TRACE_V1'
    open(newunit=unit,file='unaccepted_outer10.bin',status='new',access='stream',form='unformatted')
    write(unit) label,ng,nun,nreg,nr,nf,nmat,nfis
    write(unit) akeep,eext,einr,mat,key,vol,nuf,flux
    close(unit)
    write(*,'(a)') 'COLUMN-CHECKPOINT UNACCEPTED ITER=10; NO TERMINAL OR CONVERGENCE CLAIM'
  endif
end subroutine SPOTCOLTRACE
