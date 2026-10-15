subroutine SPOBOOX64(nentry,hentry,ientry,jentry,kentry)
  ! Two fresh private XSM outputs, eight readonly current BOOT context operands,
  ! three actual fresh ASM systems, three actual binary tracking operands.
  ! The owning host independently pins actual producers/case/deck/full inputs.
  use GANLIB
  use, intrinsic::iso_fortran_env,only:int64,real32,real64
  use SPOR64_BOOT_CONTEXT64_V2,only:SPOR64_BOOT_CONTEXT64_READ
  use SPOR64_BOOTQ64_V2,only:SPOR64_BOOTQ64_BUILD,SPOR64_BOOTQ64_COMMITTED
  use SPOR64_BOOTB64,only:SPOR64_BOOTB64_INGRESS,SPOR64_BOOTB64_BOOT
  use SPOR64_BOOTC64,only:SPOR64_BOOTC64_HOST_COMMITTED
  use SPOR64_B2IX,only:SPOR64_B2IX_SEAL_BOOTSTRAP,SPOR64_B2IX_BOOTSTRAP_COMMITTED
  use SPOR64_RCONTRACT,only:SPOR64_ROUTE_CONTRACT
  use SPOR64_VERIFY,only:EMPTY_ROOT,RECORD_MATCHES
  use SPOR64_XSM_STORE64,only:EMPTY_XSM_ROOT
  use SPOR64_XSM_RB64,only:SEALED_XSM_PAIR_READBACK
  implicit none
  integer,intent(in)::nentry,ientry(nentry),jentry(nentry)
  character(len=12),intent(in)::hentry(nentry)
  type(c_ptr),intent(in)::kentry(nentry)
  integer,parameter::NP=3,NG=370,NS=40
  character(len=12),parameter::physical_names(7)= &
      ['FLUX        ','MACRO0      ','TRACK       ','TRACK_f     ', &
       'SYSTEM      ','FSOURCE     ','FLUX_OLD    ']
  character(len=12),parameter::archive_names(4)= &
      ['TRACK       ','MICROLIB2   ','SYSTEM      ','FLUX        ']
  character(len=24)::macro_file,source_file
  character(len=24),parameter::archive_file='BOOT-SOLVED-STAGE.xsm'
  character(len=12)::signature
  character(len=4)::keyword
  type(SPOR64_ROUTE_CONTRACT)::contract
  type(c_ptr)::macro_stage,source_stage,flux_stage,archive_stage
  type(c_ptr)::physical(7),projected_tracks,projected_fluxes,projected_libraries
  type(c_ptr)::track,seed,library,out_lists(4),item
  integer::i,j,p,k,indic,nitma,rank,impx,status,rankvec(NG),state(NS),macro_state(NS)
  integer::physical_kind(7),physical_access(7),npayload
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
  inquire(file=trim(archive_file),exist=exists)
  if(exists)call XABORT('SPOBOOX64: PRIVATE ARCHIVE EXISTS; NO OVERWRITE.')
  do p=1,NP
    write(macro_file,'(A,I1,A)')'BOOT-MAC-',p,'.xsm'
    write(source_file,'(A,I1,A)')'BOOT-Q-',p,'.xsm'
    inquire(file=trim(macro_file),exist=exists)
    if(exists)call XABORT('SPOBOOX64: PRIVATE MACRO EXISTS; NO OVERWRITE.')
    inquire(file=trim(source_file),exist=exists)
    if(exists)call XABORT('SPOBOOX64: PRIVATE SOURCE EXISTS; NO OVERWRITE.')
  enddo
  call LCMOP(archive_stage,archive_file,0,2,0)
  if(.not.EMPTY_ROOT(archive_stage))call XABORT('SPOBOOX64: FRESH PRIVATE ARCHIVE REQUIRED.')
  signature='L_ARCHIVE';npayload=NP
  call LCMPTC(archive_stage,'SIGNATURE',12,signature)
  call LCMPUT(archive_stage,'LISTDIM',1,1,npayload)
  call LCMPUT(archive_stage,'SPOT-ITER-K',1,4,keff64)
  do k=1,4
    out_lists(k)=LCMLID(archive_stage,archive_names(k),NP)
  enddo
  eps32=transfer(contract%eps_radial_bits,0.0_real32)
  physical_kind=[1,2,1,3,1,2,1];physical_access=[0,2,2,2,2,2,2]
  cutoff_visits=0_int64
  do p=1,NP
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
    if(status/=SPOR64_BOOTC64_HOST_COMMITTED)then
      write(6,'(A,I0,A,I0,A)') &
        '{"schema":"ACTUAL_BOOT_EXACT_FAILURE_STATUS_DIAGNOSTIC_V1","boot_plane":',p, &
        ',"actual_return_status":',status,',"required_committed_status":8}'
      flush(6)
      call XABORT('SPOBOOX64: ACTUAL STRICT SOLVE NOT COMMITTED.')
    endif
    ! Real accepted terminal fields remain unsealed until the real B2I seal.
    item=LCMDIL(out_lists(1),p);call LCMEQU(track,item)
    item=LCMDIL(out_lists(2),p);call LCMEQU(library,item)
    item=LCMDIL(out_lists(3),p);call LCMEQU(kentry(10+p),item)
    item=LCMDIL(out_lists(4),p);call LCMEQU(flux_stage,item)
    call LCMCL(flux_stage,2)
    call LCMCL(source_stage,2)
    call LCMCL(macro_stage,2)
  enddo
  call SPOR64_B2IX_SEAL_BOOTSTRAP(kentry(1),kentry(2),kentry(5),kentry(6), &
      archive_stage,kentry(10),status)
  if(status==SPOR64_B2IX_BOOTSTRAP_COMMITTED) then
    call SEALED_XSM_PAIR_READBACK(kentry(1),kentry(2),kentry(5),archive_stage,ok)
    if(.not.ok)call XABORT('SPOBOOX64: COMPLETE SEALED PAIR PAYLOAD READBACK FAILED.')
    write(*,'(A)') '{"schema":"ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1",'// &
      '"status":"PASS","all_payload_bits_equal":true,"complete_lifecycle_checked":true,'// &
      '"groups":370,"planes":3,"epoch":0,"AAA_qualified":false,"ABA_admitted":false}'
  endif
  call LCMCL(archive_stage,2)
  if(status/=SPOR64_B2IX_BOOTSTRAP_COMMITTED)call XABORT('SPOBOOX64: TRUE BOOTSTRAP SEAL FAILED.')
end subroutine SPOBOOX64
