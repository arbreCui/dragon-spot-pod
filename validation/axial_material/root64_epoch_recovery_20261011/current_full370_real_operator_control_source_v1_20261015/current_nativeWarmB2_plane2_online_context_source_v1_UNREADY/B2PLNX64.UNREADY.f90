! UNREADY isolated plane2 only. Same complete16 interface; no three-plane seal.
! Outputs are unsealed accepted flux and constructed fixed-source byte copies.
! Original complete NP=3 context and all readonly systems/binary tracks required.
subroutine B2PLNX64(nentry,hentry,ientry,jentry,kentry)
  use GANLIB
  use, intrinsic::iso_fortran_env,only:int64,real32,real64
  use SPOR64_BOOT_CONTEXT64_V2,only:SPOR64_BOOT_CONTEXT64_READ
  use SPOR64_BOOTQ64_V2,only:SPOR64_BOOTQ64_BUILD,SPOR64_BOOTQ64_COMMITTED
  use SPOR64_BOOTB64,only:SPOR64_BOOTB64_INGRESS,SPOR64_BOOTB64_BOOT
  use SPOR64_BOOTC64,only:SPOR64_BOOTC64_HOST_COMMITTED
  use SPOR64_RCONTRACT,only:SPOR64_ROUTE_CONTRACT
  use SPOR64_VERIFY,only:RECORD_MATCHES
  use SPOR64_XSM_STORE64,only:EMPTY_XSM_ROOT
  use SPOR64_BOOT64,only:SPOR64_BOOT64_SAME_TREE
  implicit none
  integer,intent(in)::nentry,ientry(nentry),jentry(nentry)
  character(len=12),intent(in)::hentry(nentry)
  type(c_ptr),intent(in)::kentry(nentry)
  integer,parameter::NP=3,NG=370,NS=40
  character(len=12),parameter::physical_names(7)= &
      ['FLUX        ','MACRO0      ','TRACK       ','TRACK_f     ', &
       'SYSTEM      ','FSOURCE     ','FLUX_OLD    ']
  type(SPOR64_ROUTE_CONTRACT)::contract
  type(c_ptr)::macro_stage,source_stage,flux_stage,physical(7)
  type(c_ptr)::projected_tracks,projected_fluxes,projected_libraries,track,seed,library
  character(len=24)::macro_file,source_file
  character(len=4)::keyword
  integer::i,j,p,indic,nitma,rank,impx,status,rankvec(NG),state(NS),macro_state(NS)
  integer::physical_kind(7),physical_access(7)
  integer,allocatable::imerg(:)
  integer(int64)::cutoff_visits(NP)
  real::flott
  double precision::dflott
  real(real32)::eps32
  real(real64)::keff64
  logical::ok,exists,rank_seen

  if(nentry/=16)call XABORT('SPOBOOX64: SIXTEEN OPERANDS REQUIRED.')
  if(any(ientry(1:2)/=2).or.any(jentry(1:2)/=0)) &
      call XABORT('SPOBOOX64: FRESH PRIVATE XSM OUTPUT PAIR REQUIRED.')
  if(any((ientry(3:13)/=1).and.(ientry(3:13)/=2)).or.any(jentry(3:16)/=2)) &
      call XABORT('SPOBOOX64: READONLY COMPLETE CONTEXT/SYSTEMS REQUIRED.')
  if(any(ientry(14:16)/=3))call XABORT('SPOBOOX64: BINARY TRACKING FILES REQUIRED.')
  do i=1,16
    if(.not.c_associated(kentry(i)))call XABORT('SPOBOOX64: NULL OPERAND.')
    do j=1,min(2,i-1)
      if(c_associated(kentry(i),kentry(j)))call XABORT('SPOBOOX64: OUTPUT ALIAS.')
    enddo
  enddo
  if(.not.EMPTY_XSM_ROOT(kentry(1)).or..not.EMPTY_XSM_ROOT(kentry(2))) &
      call XABORT('SPOBOOX64: FRESH EMPTY OUTPUT PAIR REQUIRED.')
  rank=0;rank_seen=.false.;impx=1
  do
    call REDGET(indic,nitma,flott,keyword,dflott)
    if(indic/=3)call XABORT('SPOBOOX64: KEYWORD REQUIRED.')
    if(keyword==';')exit
    if(keyword=='RANK')then
      if(rank_seen)call XABORT('SPOBOOX64: DUPLICATE RANK.')
      call REDGET(indic,rank,flott,keyword,dflott)
      if(indic/=1.or.rank<=0)call XABORT('SPOBOOX64: EXPLICIT POSITIVE RANK REQUIRED.')
      rank_seen=.true.
    else if(keyword=='EDIT')then
      call REDGET(indic,impx,flott,keyword,dflott)
      if(indic/=1)call XABORT('SPOBOOX64: INTEGER EDIT REQUIRED.')
    else
      call XABORT('SPOBOOX64: ONLY RANK/EDIT KEYWORDS ARE VALID.')
    endif
  enddo
  if(.not.rank_seen)call XABORT('SPOBOOX64: RANK HAS NO DEFAULT.')
  call SPOR64_BOOT_CONTEXT64_READ(kentry(3),kentry(4),kentry(5), &
      kentry(6),kentry(7),kentry(8),kentry(9),kentry(10),contract,ok)
  if(.not.ok)call XABORT('SPOBOOX64: GENUINE FULL PROJECTED-BOOT/E0 CONTEXT REQUIRED.')
  if(.not.RECORD_MATCHES(kentry(5),'SPOT-X-RANK',NG,1)) &
      call XABORT('SPOBOOX64: COMPLETE CASE RANK REQUIRED.')
  call LCMGET(kentry(5),'SPOT-X-RANK',rankvec)
  if(any(rankvec/=rank))call XABORT('SPOBOOX64: CASE RANK MISMATCH.')
  if(.not.RECORD_MATCHES(kentry(5),'SPOT-X-KEFF',1,4)) &
      call XABORT('SPOBOOX64: ACTUAL NATIVE CANONICAL KEFF REQUIRED.')
  call LCMGET(kentry(5),'SPOT-X-KEFF',keff64)
  projected_tracks=LCMGID(kentry(3),'TRACK')
  projected_fluxes=LCMGID(kentry(3),'FLUX')
  projected_libraries=LCMGID(kentry(3),'MICROLIB2')
  do p=1,NP
    write(macro_file,'(A,I1,A)')'BOOT-MAC-',p,'.xsm'
    write(source_file,'(A,I1,A)')'BOOT-Q-',p,'.xsm'
    inquire(file=trim(macro_file),exist=exists)
    if(exists)call XABORT('SPOBOOX64: PRIVATE MACRO EXISTS; NO OVERWRITE.')
    inquire(file=trim(source_file),exist=exists)
    if(exists)call XABORT('SPOBOOX64: PRIVATE SOURCE EXISTS; NO OVERWRITE.')
  enddo
  eps32=transfer(contract%eps_radial_bits,0.0_real32)
  physical_kind=[1,2,1,3,1,2,1];physical_access=[0,2,2,2,2,2,2]
  cutoff_visits=0_int64
  p=2
    write(macro_file,'(A,I1,A)')'BOOT-MAC-',p,'.xsm'
    write(source_file,'(A,I1,A)')'BOOT-Q-',p,'.xsm'
    call LCMOP(macro_stage,macro_file,0,2,0)
    call LCMOP(source_stage,source_file,0,2,0)
    call LCMOP(flux_stage,'BOOT-FLUX-TEMP',0,1,0)
    call SPOR64_BOOTQ64_BUILD(kentry(3),kentry(4),kentry(5),kentry(6), &
        kentry(7),kentry(8),kentry(9),kentry(10),p,macro_stage,source_stage,status)
    if(status/=SPOR64_BOOTQ64_COMMITTED)call XABORT('SPOBOOX64: ACTUAL FROZEN Q BUILD FAILED.')
    track=LCMGIL(projected_tracks,p);seed=LCMGIL(projected_fluxes,p)
    library=LCMGIL(projected_libraries,p)
    call LCMGET(track,'STATE-VECTOR',state)
    call LCMGET(macro_stage,'STATE-VECTOR',macro_state)
    allocate(imerg(state(4)));imerg=1
    physical=[flux_stage,macro_stage,track,kentry(13+p),kentry(10+p),source_stage,seed]
    physical_kind(3)=ientry(3);physical_kind(5)=ientry(10+p)
    physical_kind(7)=ientry(3)
    call SPOR64_BOOTB64_INGRESS(7,physical_names,physical_kind,physical_access,physical, &
        0,contract%flu_maxout,contract%flu_maxinr,eps32,eps32,eps32,1, &
        contract%flu_acce_free,contract%flu_acce_accel,contract%flu_option, &
        0,1,1,imerg,impx,.false.,0,.true.,NG,state(1),state(4),macro_state(4), &
        1,2,1,.false.,.true.,SPOR64_BOOTB64_BOOT,contract,status,cutoff_visits(p), &
        kentry(3),kentry(4),kentry(5),kentry(6),kentry(7),kentry(8),kentry(9),kentry(10),rank,p)
    deallocate(imerg)
    if(status/=SPOR64_BOOTC64_HOST_COMMITTED)call XABORT('SPOBOOX64: ACTUAL STRICT SOLVE NOT COMMITTED.')
  ! No bootstrap seal or three-plane solved archive is produced.
  ! Preserve all private MAC/Q file bytes for independent owning readback.
  call LCMEQU(flux_stage,kentry(1))
  call LCMEQU(source_stage,kentry(2))
  if(.not.SPOR64_BOOT64_SAME_TREE(flux_stage,kentry(1)).or. &
     .not.SPOR64_BOOT64_SAME_TREE(source_stage,kentry(2))) &
      call XABORT('B2PLNX64: COMPLETE UNSEALED OUTPUT BYTE READBACK FAILED.')
  call LCMCL(flux_stage,2)
  call LCMCL(source_stage,1)
  call LCMCL(macro_stage,1)
  write(*,'(A)')'B2PLNX64-STRICT-PLANE2-UNSEALED'
end subroutine B2PLNX64
