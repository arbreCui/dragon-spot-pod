! UNREADY Source observation extension. Never compiled/run by the author.
! Root enables only in a separately admitted fresh A/B material build under the
! original genuine caps. No old value is reconstructed from a final snapshot.
! All original numerical assignments stay byte-for-byte in derived routines.
module AXMAT_OBSERVATION_MOD_UNREADY
  use GANLIB
  implicit none
  private
  public :: AXOBS_LIBMIX_BEGIN, AXOBS_LIBDEN_OLD, AXOBS_LIBDEN_FISSION
  public :: AXOBS_LIBMIX_END, AXOBS_TRACK, AXOBS_MASK, AXOBS_SPH, AXOBS_FINAL
  integer, save :: event_number=0, libmix_number=0
contains
  logical function enabled()
    character(len=80) :: flag
    integer :: n,status
    call get_environment_variable('SPOT_AXMAT_OBSERVATION',flag,n,status)
    enabled=status==0 .and. n==20 .and. flag(:20)=='ADMITTED_SOURCE_ONLY'
  end function

  subroutine start_event(label,unit)
    character(len=*),intent(in) :: label
    integer,intent(out) :: unit
    character(len=64) :: filename
    integer(c_int32_t) :: endian
    integer(c_int8_t) :: bytes(4)
    if(storage_size(0)/=32.or.storage_size(0.0)/=32) &
      call XABORT('AXOBS: actual INTEGER/REAL width is not32; no coercion')
    endian=int(z'01020304',c_int32_t)
    bytes=transfer(endian,bytes)
    if(bytes(1)/=4.or.bytes(2)/=3.or.bytes(3)/=2.or.bytes(4)/=1) &
      call XABORT('AXOBS: actual byte order is not little endian')
    event_number=event_number+1
    write(filename,'(A,I6.6,A)') 'axobs-',event_number,'.context.bin'
    open(newunit=unit,file=trim(filename),status='new',access='stream', &
      form='unformatted',action='write')
    write(unit) 'AXOBSCTX',1_c_int32_t,int(event_number,c_int32_t), &
      int(libmix_number,c_int32_t),int(len(label),c_int32_t),label
  end subroutine

  subroutine snapshot(label,iplib,whole_library)
    character(len=*),intent(in) :: label
    type(c_ptr),intent(in) :: iplib
    logical,intent(in) :: whole_library
    character(len=64) :: filename
    integer :: length,kind
    logical :: exists
    type(c_ptr) :: target,saved
    if(whole_library)then
      target=iplib
    else
      call LCMLEN(iplib,'MACROLIB',length,kind)
      if(length/=-1.or.kind/=0)return
      target=LCMGID(iplib,'MACROLIB')
    endif
    write(filename,'(A,I6.6,A,A)') 'axobs-',event_number,'-',trim(label)//'.xsm'
    ! LCMEQU general copy copies original words to a fresh disk-backed XSM.
    ! LCMEXP binary CHARACTER uses strncpy and cannot prove arbitrary words
    ! after NUL, so it is deliberately NOT the evidence capture mechanism.
    ! The original active directory and arithmetic records are never written.
    inquire(file=trim(filename),exist=exists)
    if(exists)call XABORT('AXOBS: snapshot exists; zero retry/no overwrite')
    saved=c_null_ptr
    call LCMOP(saved,trim(filename),0,2,0)
    call LCMEQU(target,saved)
    call LCMCL(saved,1)
  end subroutine

  subroutine AXOBS_LIBMIX_BEGIN(iplib,nbmix,ngroup,nbiso,mix,den,mask,maskl,itstmp,tmpday)
    type(c_ptr),intent(in) :: iplib
    integer,intent(in) :: nbmix,ngroup,nbiso,mix(nbiso),itstmp
    real,intent(in) :: den(nbiso),tmpday(3)
    logical,intent(in) :: mask(nbmix),maskl(ngroup)
    integer :: unit,state(40),macro_length,macro_kind
    if(.not.enabled())return
    libmix_number=libmix_number+1
    call start_event('LIBMIX_BEFORE',unit)
    call LCMGET(iplib,'STATE-VECTOR',state)
    write(unit) nbmix,ngroup,nbiso,itstmp,state,mix,den,tmpday
    call LCMLEN(iplib,'MACROLIB',macro_length,macro_kind)
    write(unit) macro_length,macro_kind
    write(unit) merge(1,0,mask),merge(1,0,maskl)
    close(unit)
    call snapshot('oldmacro-pre-LIBMIX',iplib,.false.)
  end subroutine

  subroutine AXOBS_LIBDEN_OLD(iplib,nbmix,ngroup,nbiso,nl,ndel,nesp,ned,itranc, &
      maxnfi,npart,lsame,itstmp,tmpday,stern,mask,maskl,maskk,lall,ldiff,nfissi)
    type(c_ptr),intent(in) :: iplib
    integer,intent(in) :: nbmix,ngroup,nbiso,nl,ndel,nesp,ned,itranc,maxnfi,npart,itstmp,stern,nfissi
    real,intent(in) :: tmpday(3)
    logical,intent(in) :: lsame,mask(nbmix),maskl(ngroup),maskk,lall,ldiff
    integer :: unit
    if(.not.enabled())return
    call start_event('LIBDEN_OLD_CONTEXT',unit)
    write(unit) nbmix,ngroup,nbiso,nl,ndel,nesp,ned,itranc,maxnfi,npart,itstmp,stern,nfissi,tmpday
    write(unit) merge(1,0,lsame),merge(1,0,maskk),merge(1,0,lall),merge(1,0,ldiff), &
      merge(1,0,mask),merge(1,0,maskl)
    close(unit)
    call snapshot('oldmacro-LIBDEN',iplib,.false.)
  end subroutine

  subroutine AXOBS_LIBDEN_FISSION(nbmix,maxnfi,nfiss0,nfissi,indfis)
    integer,intent(in) :: nbmix,maxnfi,nfiss0,nfissi,indfis(nbmix,maxnfi)
    integer :: unit
    if(.not.enabled())return
    call start_event('LIBDEN_BEFORE_FISSION_SLOT_MUTATION',unit)
    write(unit) nbmix,maxnfi,nfiss0,nfissi
    if(nfissi>0)write(unit) indfis(:nbmix,:nfissi)
    close(unit)
  end subroutine

  subroutine AXOBS_LIBMIX_END(iplib)
    type(c_ptr),intent(in) :: iplib
    integer :: unit
    if(.not.enabled())return
    call start_event('LIBMIX_AFTER',unit)
    close(unit)
    call snapshot('postmacro-LIBMIX',iplib,.false.)
  end subroutine

  subroutine AXOBS_TRACK(nreg,nbiso,nbmix,ngro,mat,mix,den,lshi,kspH,itranz,iprob,igrmin,igrmax)
    integer,intent(in) :: nreg,nbiso,nbmix,ngro,mat(nreg),mix(nbiso),lshi(nbiso),ksph,itranz,iprob,igrmin,igrmax
    real,intent(in) :: den(nbiso)
    integer :: unit
    if(.not.enabled())return
    call start_event('TONDRV_AFTER_REAL_MAT_ELIMINATION',unit)
    write(unit) nreg,nbiso,nbmix,ngro,ksph,itranz,iprob,igrmin,igrmax,mat,mix,lshi,den
    close(unit)
  end subroutine

  subroutine AXOBS_MASK(nbiso,nbmix,ngro,mask,maskl,lshi,lshi2,ksph,itranz,iphase,nres2,itstmp,tmpday)
    integer,intent(in) :: nbiso,nbmix,ngro,lshi(nbiso),lshi2(nbiso),ksph,itranz,iphase,nres2,itstmp
    real,intent(in) :: tmpday(3)
    logical,intent(in) :: mask(nbmix),maskl(ngro)
    integer :: unit
    if(.not.enabled())return
    call start_event('TONDRV_ACTUAL_FINAL_LIBMIX_MASK',unit)
    write(unit) nbiso,nbmix,ngro,ksph,itranz,iphase,nres2,itstmp,lshi,lshi2,tmpday
    write(unit) merge(1,0,mask),merge(1,0,maskl)
    close(unit)
  end subroutine

  subroutine AXOBS_SPH(nbm,nbiso,ngro,inrs,itranc,igrmin,igrmax,maski,sph)
    integer,intent(in) :: nbm,nbiso,ngro,inrs,itranc,igrmin,igrmax
    logical,intent(in) :: maski(nbiso)
    real,intent(in) :: sph(nbm,ngro)
    integer :: unit
    if(.not.enabled())return
    call start_event('TONSPH_BEFORE_ACTUAL_TONCMI',unit)
    write(unit) nbm,nbiso,ngro,inrs,itranc,igrmin,igrmax,merge(1,0,maski),sph
    close(unit)
  end subroutine

  subroutine AXOBS_FINAL(iplib)
    type(c_ptr),intent(in) :: iplib
    integer :: unit
    if(.not.enabled())return
    call start_event('TONDRV_FINAL_AFTER_SHIBA',unit)
    close(unit)
    ! Exactly one full final micro snapshot per actual TONDRV invocation.
    ! All calls remain counted and saved; repeated actual invocations may hit
    ! the unchanged2GiB archive cap and must fail, never truncate old events.
    call snapshot('final-complete-micro',iplib,.true.)
  end subroutine
end module AXMAT_OBSERVATION_MOD_UNREADY
