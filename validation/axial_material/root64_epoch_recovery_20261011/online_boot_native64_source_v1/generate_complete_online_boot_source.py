#!/usr/bin/env python3
"""Generate complete native BOOT Source, inverse proof; never compile/run it."""
from pathlib import Path
import re,json,ast,runpy,hashlib
ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
OUT=REC/'online_boot_native64_source_v1'
base=runpy.run_path(str(REC/'global_native64_dependency_source_v2/driver_source/generate_global_native64_dependency_source.py'))
Transform=base['Transform'];read_pin=base['read_pin'];fresh=base['fresh'];fresh_json=base['fresh_json']

BIND_HEAD='''module SPOR64_BOOT_BIND64
  ! Full current PROJECTED-BOOT/e0 context and physical frozen-Q binding.
  ! Stored labels/tree consistency do not replace the owning host's actual
  ! complete external file SHA/7ID and actual tool terminal pins.
  use GANLIB
  use, intrinsic :: iso_fortran_env, only:int32,int64,real32,real64
  use, intrinsic :: ieee_arithmetic, only:ieee_is_finite
  use SPOR64_BOOT_CONTEXT64_V2,only:SPOR64_BOOT_CONTEXT64_READ
  use SPOR64_BOOTQ64_V2,only:SPOR64_BOOTQ64_READ,SPOR64_BOOTQ64_LOADED
  use SPOR64_BOOT64,only:SPOR64_BOOT64_SAME_TREE
  use SPOR64_RCONTRACT,only:SPOR64_ROUTE_CONTRACT
  use SPOR64_VERIFY,only:ABSENT_RECORD,CHARACTER_RECORD_MATCHES, &
      EXACT_INVENTORY,LIST_ITEM_IS_DIRECTORY,RECORD_MATCHES,SAME_REAL32_BITS
  use SPOR64_SCHEMA,only:SCHEMA_RESPONSE_GROUP,SCHEMA_RESPONSE_GROUP_P3, &
      SCHEMA_RESPONSE_GROUP_PHYS,SCHEMA_RESPONSE_GROUP_PHYS_P3, &
      SCHEMA_CANDIDATE_SYSTEM_ROOT,SCHEMA_CANDIDATE_SYSTEM_ROOT_L1RAW
  implicit none
  private
  integer,parameter::NSTATE=40,NGRP=370,NSNAP=3
  public::SPOR64_BOOT_BIND64_READ
contains
  subroutine SPOR64_BOOT_BIND64_READ(ipprojected,ipglobal,ipax, &
      ipaxtrack,ipaxsystem,ipaxmacro,iparchive,ipcontract,requested_rank, &
      plane_index,ipseed,iptrack,ipsystem,ipmacro,ipsource, &
      initial_flux64,fixed_source64,leak1d64,ok)
    type(c_ptr),intent(in)::ipprojected,ipglobal,ipax,ipaxtrack,ipaxsystem
    type(c_ptr),intent(in)::ipaxmacro,iparchive,ipcontract
    type(c_ptr),intent(in)::ipseed,iptrack,ipsystem,ipmacro,ipsource
    integer,intent(in)::requested_rank,plane_index
    real(real64),intent(out)::initial_flux64(:,:),fixed_source64(:,:),leak1d64(:)
    logical,intent(out)::ok
    type(SPOR64_ROUTE_CONTRACT)::contract
    type(c_ptr)::tracks,fluxes,expected_seed,expected_track,roots,native,groups
    integer::rank(NGRP),state(NSTATE),mccg(NSTATE),pflag,g,n,t,nreg,nunk,nmat
    integer::status
    real(real64)::rho
    real(real64),allocatable::q64(:,:),phi(:)
    real(real32)::leak32(NGRP)
    logical::valid
    ok=.false.;initial_flux64=0.0_real64;fixed_source64=0.0_real64;leak1d64=0.0_real64
    if(requested_rank<=0.or.plane_index<1.or.plane_index>NSNAP)return
    call SPOR64_BOOT_CONTEXT64_READ(ipprojected,ipglobal,ipax,ipaxtrack, &
        ipaxsystem,ipaxmacro,iparchive,ipcontract,contract,valid)
    if(.not.valid)return
    if(.not.RECORD_MATCHES(ipax,'SPOT-X-RANK',NGRP,1))return
    call LCMGET(ipax,'SPOT-X-RANK',rank)
    if(any(rank/=requested_rank))return
    tracks=LCMGID(ipprojected,'TRACK');fluxes=LCMGID(ipprojected,'FLUX')
    expected_track=LCMGIL(tracks,plane_index);expected_seed=LCMGIL(fluxes,plane_index)
    if(.not.SPOR64_BOOT64_SAME_TREE(iptrack,expected_track))return
    if(.not.SPOR64_BOOT64_SAME_TREE(ipseed,expected_seed))return
    call LCMGET(iptrack,'STATE-VECTOR',state)
    nreg=state(1);nunk=state(2);nmat=state(4)
    if(nreg<=0.or.nunk<=nreg.or.nmat<=0)return
    if(any(shape(initial_flux64)/=[nunk,NGRP]))return
    if(any(shape(fixed_source64)/=[nunk,NGRP]).or.size(leak1d64)/=NGRP)return
    call SPOR64_BOOTQ64_READ(ipprojected,ipglobal,ipax,ipaxtrack, &
        ipaxsystem,ipaxmacro,iparchive,ipcontract,plane_index, &
        ipmacro,ipsource,q64,rho,status)
    if(status/=SPOR64_BOOTQ64_LOADED)return
    if(.not.allocated(q64))return
    if(any(shape(q64)/=[nunk,NGRP]))return
    if(any(.not.ieee_is_finite(q64)).or.any(q64<0.0_real64))return
    fixed_source64=q64
    if(.not.RECORD_MATCHES(ipseed,'ROOT-FLUX64',NGRP,10))return
    roots=LCMGID(ipseed,'ROOT-FLUX64')
    native=LCMGID(LCMGID(ipseed,'SPOT-R64'),'FLUX')
    allocate(phi(nunk))
    do g=1,NGRP
      call LCMLEL(roots,g,n,t)
      if(n/=nunk.or.t/=4)return
      call LCMGDL(roots,g,initial_flux64(:,g))
      call LCMLEL(native,g,n,t)
      if(n/=nunk.or.t/=4)return
      call LCMGDL(native,g,phi)
      if(any(.not.ieee_is_finite(initial_flux64(:,g))))return
      if(any(transfer(phi,[0_int64],nunk)/= &
          transfer(initial_flux64(:,g),[0_int64],nunk)))return
    enddo
    if(.not.RECORD_MATCHES(ipseed,'LEAK1D64',NGRP,4))return
    call LCMGET(ipseed,'LEAK1D64',leak1d64)
    if(any(.not.ieee_is_finite(leak1d64)))return
    call LCMGET(ipseed,'SPOT-LEAK1D',leak32)
    if(any(transfer(leak32,[0_int32],NGRP)/= &
        transfer(real(leak1d64,real32),[0_int32],NGRP)))return
    ! Real fresh ASM result only; no forged ASSEMBLED/e0 lifecycle wrapper.
    if(.not.CANDIDATE_SYSTEM_ROOT_IS_EXACT(ipsystem))return
    if(.not.RECORD_MATCHES(ipsystem,'SPOT-L1-RAW',1,1))return
    call LCMGET(ipsystem,'SPOT-L1-RAW',pflag)
    if(pflag/=1)return
    if(.not.ABSENT_RECORD(ipsystem,'SPOT-R64'))return
    if(.not.ABSENT_RECORD(ipsystem,'B2I-SENT').or. &
        .not.ABSENT_RECORD(ipsystem,'B2I-DEEP'))return
    if(.not.RECORD_MATCHES(iptrack,'MCCG-STATE',NSTATE,1))return
    call LCMGET(iptrack,'MCCG-STATE',mccg)
    if(.not.SYSTEM_PAYLOAD_IS_VALID(ipsystem,ipmacro,leak32,plane_index, &
        .true.,nreg,nmat,nunk,state(5),mccg(6),mccg(10),mccg(17)))return
    ok=.true.
  end subroutine SPOR64_BOOT_BIND64_READ
'''

CALLER='''subroutine SPOBOOTRUN64(nentry,hentry,ientry,jentry,kentry)
  ! Two fresh memory outputs, eight readonly current BOOT context operands,
  ! three actual fresh ASM systems, three actual binary tracking operands.
  ! The owning host independently pins actual producers/case/deck/full inputs.
  use GANLIB
  use, intrinsic::iso_fortran_env,only:int64,real32,real64
  use SPOR64_BOOT_CONTEXT64_V2,only:SPOR64_BOOT_CONTEXT64_READ
  use SPOR64_BOOTQ64_V2,only:SPOR64_BOOTQ64_BUILD,SPOR64_BOOTQ64_COMMITTED
  use SPOR64_BOOTB64,only:SPOR64_BOOTB64_INGRESS,SPOR64_BOOTB64_BOOT
  use SPOR64_BOOTC64,only:SPOR64_BOOTC64_HOST_COMMITTED
  use SPOR64_B2I,only:SPOR64_B2I_SEAL_BOOTSTRAP,SPOR64_B2I_BOOTSTRAP_COMMITTED
  use SPOR64_RCONTRACT,only:SPOR64_ROUTE_CONTRACT
  use SPOR64_VERIFY,only:EMPTY_MEMORY_ROOT,EMPTY_ROOT,RECORD_MATCHES
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

  if(nentry/=16)call XABORT('SPOBOOTRUN64: SIXTEEN OPERANDS REQUIRED.')
  if(any(ientry(1:2)/=1).or.any(jentry(1:2)/=0)) &
      call XABORT('SPOBOOTRUN64: FRESH MEMORY OUTPUT PAIR REQUIRED.')
  if(any((ientry(3:13)/=1).and.(ientry(3:13)/=2)).or.any(jentry(3:16)/=2)) &
      call XABORT('SPOBOOTRUN64: READONLY COMPLETE CONTEXT/SYSTEMS REQUIRED.')
  if(any(ientry(14:16)/=3))call XABORT('SPOBOOTRUN64: BINARY TRACKING FILES REQUIRED.')
  do i=1,16
    if(.not.c_associated(kentry(i)))call XABORT('SPOBOOTRUN64: NULL OPERAND.')
    do j=1,min(2,i-1)
      if(c_associated(kentry(i),kentry(j)))call XABORT('SPOBOOTRUN64: OUTPUT ALIAS.')
    enddo
  enddo
  if(.not.EMPTY_MEMORY_ROOT(kentry(1)).or..not.EMPTY_MEMORY_ROOT(kentry(2))) &
      call XABORT('SPOBOOTRUN64: FRESH EMPTY OUTPUT PAIR REQUIRED.')
  rank=0;rank_seen=.false.;impx=1
  do
    call REDGET(indic,nitma,flott,keyword,dflott)
    if(indic/=3)call XABORT('SPOBOOTRUN64: KEYWORD REQUIRED.')
    if(keyword==';')exit
    if(keyword=='RANK')then
      if(rank_seen)call XABORT('SPOBOOTRUN64: DUPLICATE RANK.')
      call REDGET(indic,rank,flott,keyword,dflott)
      if(indic/=1.or.rank<=0)call XABORT('SPOBOOTRUN64: EXPLICIT POSITIVE RANK REQUIRED.')
      rank_seen=.true.
    else if(keyword=='EDIT')then
      call REDGET(indic,impx,flott,keyword,dflott)
      if(indic/=1)call XABORT('SPOBOOTRUN64: INTEGER EDIT REQUIRED.')
    else
      call XABORT('SPOBOOTRUN64: ONLY RANK/EDIT KEYWORDS ARE VALID.')
    endif
  enddo
  if(.not.rank_seen)call XABORT('SPOBOOTRUN64: RANK HAS NO DEFAULT.')
  call SPOR64_BOOT_CONTEXT64_READ(kentry(3),kentry(4),kentry(5), &
      kentry(6),kentry(7),kentry(8),kentry(9),kentry(10),contract,ok)
  if(.not.ok)call XABORT('SPOBOOTRUN64: GENUINE FULL PROJECTED-BOOT/E0 CONTEXT REQUIRED.')
  if(.not.RECORD_MATCHES(kentry(5),'SPOT-X-RANK',NG,1)) &
      call XABORT('SPOBOOTRUN64: COMPLETE CASE RANK REQUIRED.')
  call LCMGET(kentry(5),'SPOT-X-RANK',rankvec)
  if(any(rankvec/=rank))call XABORT('SPOBOOTRUN64: CASE RANK MISMATCH.')
  if(.not.RECORD_MATCHES(kentry(5),'SPOT-X-KEFF',1,4)) &
      call XABORT('SPOBOOTRUN64: ACTUAL NATIVE CANONICAL KEFF REQUIRED.')
  call LCMGET(kentry(5),'SPOT-X-KEFF',keff64)
  projected_tracks=LCMGID(kentry(3),'TRACK')
  projected_fluxes=LCMGID(kentry(3),'FLUX')
  projected_libraries=LCMGID(kentry(3),'MICROLIB2')
  inquire(file=trim(archive_file),exist=exists)
  if(exists)call XABORT('SPOBOOTRUN64: PRIVATE ARCHIVE EXISTS; NO OVERWRITE.')
  do p=1,NP
    write(macro_file,'(A,I1,A)')'BOOT-MAC-',p,'.xsm'
    write(source_file,'(A,I1,A)')'BOOT-Q-',p,'.xsm'
    inquire(file=trim(macro_file),exist=exists)
    if(exists)call XABORT('SPOBOOTRUN64: PRIVATE MACRO EXISTS; NO OVERWRITE.')
    inquire(file=trim(source_file),exist=exists)
    if(exists)call XABORT('SPOBOOTRUN64: PRIVATE SOURCE EXISTS; NO OVERWRITE.')
  enddo
  call LCMOP(archive_stage,archive_file,0,2,0)
  if(.not.EMPTY_ROOT(archive_stage))call XABORT('SPOBOOTRUN64: FRESH PRIVATE ARCHIVE REQUIRED.')
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
    if(status/=SPOR64_BOOTQ64_COMMITTED)call XABORT('SPOBOOTRUN64: ACTUAL FROZEN Q BUILD FAILED.')
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
    if(status/=SPOR64_BOOTC64_HOST_COMMITTED)call XABORT('SPOBOOTRUN64: ACTUAL STRICT SOLVE NOT COMMITTED.')
    ! Real accepted terminal fields remain unsealed until the real B2I seal.
    item=LCMDIL(out_lists(1),p);call LCMEQU(track,item)
    item=LCMDIL(out_lists(2),p);call LCMEQU(library,item)
    item=LCMDIL(out_lists(3),p);call LCMEQU(kentry(10+p),item)
    item=LCMDIL(out_lists(4),p);call LCMEQU(flux_stage,item)
    call LCMCL(flux_stage,2)
    call LCMCL(source_stage,2)
    call LCMCL(macro_stage,2)
  enddo
  call SPOR64_B2I_SEAL_BOOTSTRAP(kentry(1),kentry(2),kentry(5),kentry(6), &
      archive_stage,kentry(10),status)
  call LCMCL(archive_stage,2)
  if(status/=SPOR64_B2I_BOOTSTRAP_COMMITTED)call XABORT('SPOBOOTRUN64: TRUE BOOTSTRAP SEAL FAILED.')
end subroutine SPOBOOTRUN64
'''

def rename_prefix(t,old,new):
    names=sorted(set(re.findall(rb'\b'+old.encode()+rb'[A-Z0-9_]*\b',t.raw)))
    for n in names:
        s=n.decode();t.rename(s,new+s[len(old):],len(re.findall(rb'\b'+n+rb'\b',t.raw)))

def body(raw,name):
    p=rb'  logical function '+name.encode()+rb'\b[\s\S]*?  end function '+name.encode()+rb'\n'
    hits=re.findall(p,raw,re.I);assert len(hits)==1
    return hits[0]

def main():
    assert not(OUT/'SPOR64_BOOTB64.f90').exists()
    dependencies=[ROOT/'src'/n for n in ['SPOR64_B2B.f90','SPOR64_B2C.f90','SPOR64_B2I.f90','SPOR64_B2K.f90',
        'SPOR64_A9.f90','SPOR64_A8.f90','SPOR64_RCONTRACT.f90','SPOR64_VERIFY.f90','SPOR64_SCHEMA.f90']]
    dependencies += [REC/'bootstrap_qfiss_source_v2'/n for n in [
        'SPOR64_BOOT_CONTEXT64.f90','SPOR64_BOOTQ64.f90','SPOR64_BOOT_CANONICAL64.f90']]
    dependencies += [REC/'new_source/SPOR64_BOOT64.f90']
    before=[read_pin(p)[1] for p in dependencies]
    br,bp=read_pin(dependencies[0]);b=Transform(br)
    rename_prefix(b,'SPOR64_B2B','SPOR64_BOOTB64')
    rename_prefix(b,'SPOR64_B2C','SPOR64_BOOTC64')
    b.splice('real full projected-BOOT binding import','  use SPOR64_A9, only : FLU2DR64_CORE\n',
        '  use SPOR64_A9, only : FLU2DR64_CORE\n  use SPOR64_BOOT_BIND64, only : SPOR64_BOOT_BIND64_READ\n')
    b.splice('complete explicit current BOOT proof and external-case ABI','      cutoff_visit64)\n',
        '      cutoff_visit64,ipprojected,ipglobal,ipax,ipaxtrack,ipaxsystem, &\n'
        '      ipaxmacro,iparchive,ipcontract,requested_rank,boot_plane)\n')
    b.splice('complete current context operand declarations','    type(c_ptr), intent(in) :: kentry(:)\n',
        '    type(c_ptr), intent(in) :: kentry(:)\n'
        '    type(c_ptr), intent(in) :: ipprojected,ipglobal,ipax,ipaxtrack,ipaxsystem\n'
        '    type(c_ptr), intent(in) :: ipaxmacro,iparchive,ipcontract\n'
        '    integer, intent(in) :: requested_rank,boot_plane\n'
        '    logical :: boot_bound\n')
    b.splice('independent BOOT-only; old CONT contracts are never relaxed',
        '    if (r64_mode /= SPOR64_BOOTB64_BOOT .and. &\n        r64_mode /= SPOR64_BOOTB64_CONT) return\n',
        '    if (r64_mode /= SPOR64_BOOTB64_BOOT) return\n'
        '    if (requested_rank <= 0 .or. boot_plane < 1 .or. boot_plane > 3) return\n')
    b.splice('BOOT native committed authority mandatory, no legacy fallback',
        "      if (.not. ABSENT_RECORD(ipseed,'SPOT-R64')) return\n"
        "      if (.not. ABSENT_RECORD(ipsou,'SPOT-R64')) return\n",
        "      if (.not. RECORD_MATCHES(ipseed,'SPOT-R64',-1,0)) return\n"
        "      if (.not. RECORD_MATCHES(ipsou,'SPOT-R64',-1,0)) return\n")
    b.splice('all BOOT leakage must be typed actual projection',
        '    if (r64_mode == SPOR64_BOOTB64_CONT .and. .not. have_leak1d64) return\n',
        '    if (.not. have_leak1d64) return\n')
    b.splice('true projected BOOT seed is TYPE S0, not solved TYPE K header',
        '      if (flux_state(6) /= 0 .and. flux_state(6) /= 2) return\n',
        '      if (flux_state(6) /= 0) return\n')
    start=b.raw.index(b'    initial_flux64 = +0.0_real64\n')
    end=b.raw.index(b'    xcsou1 = +0.0_real64\n',start)
    b.splice('replace complete sole legacy ingress with genuine full native BOOT reader',b.raw[start:end],
        '    call SPOR64_BOOT_BIND64_READ(ipprojected,ipglobal,ipax,ipaxtrack, &\n'
        '        ipaxsystem,ipaxmacro,iparchive,ipcontract,requested_rank,boot_plane, &\n'
        '        ipseed,iptrk,ipsys,ipmacr,ipsou,initial_flux64,fixed_source64,leak1d64,boot_bound)\n'
        '    if (.not. boot_bound) return\n\n')
    b.splice('publish true native BOOT leakage with strict actual terminal fields',
        '            leak1d_input32,epsout32,epsunk32,epsinr32,coptio, &\n',
        '            leak1d_input32,leak1d64,epsout32,epsunk32,epsinr32,coptio, &\n')
    cr,cp=read_pin(dependencies[1]);c=Transform(cr)
    rename_prefix(c,'SPOR64_B2C','SPOR64_BOOTC64')
    # New plain BOOT publication has typed leak but remains deliberately
    # unsealed: original real B2I alone publishes SOLVED/CLOSED/e0.
    c.splice('plain BOOT native leakage argument',
        '      leak1d_input32,epsout32, &\n','      leak1d_input32,leak1d_input64,epsout32, &\n')
    anchor='    real(real32), intent(in) :: leak1d_input32(:)\n'
    at=c.raw.index(anchor.encode());following=c.raw[at:at+len(anchor)]
    c.splice('plain BOOT typed leakage declaration',following,
        anchor+'    real(real64), intent(in) :: leak1d_input64(:)\n',3)
    # Restore the two existing CONT/IMPL declarations that already follow it.
    duplicate='    real(real64), intent(in) :: leak1d_input64(:)\n'
    c.splice('retain full original CONT declaration without duplicate',duplicate+duplicate,duplicate)
    c.splice('retain full original optional impl declaration',
        anchor+duplicate+'    real(real32), intent(in) :: epsout32, epsunk32, epsinr32\n'
        '    character(len=4), intent(in) :: coptio\n'
        '    character(len=12), intent(in) :: macro_name, track_name, system_name\n'
        '    integer, intent(out) :: status\n'
        '    type(c_ptr), intent(in), optional :: ipseed_lifecycle\n',
        anchor+'    real(real32), intent(in) :: epsout32, epsunk32, epsinr32\n'
        '    character(len=4), intent(in) :: coptio\n'
        '    character(len=12), intent(in) :: macro_name, track_name, system_name\n'
        '    integer, intent(out) :: status\n'
        '    type(c_ptr), intent(in), optional :: ipseed_lifecycle\n')
    c.splice('true BOOT passed directly to real original publication body',
        '        track_name,system_name,contract,status)\n',
        '        track_name,system_name,contract,status,leak1d_input64=leak1d_input64)\n')
    c.splice('complete native leakage preflight ahead of writes',
        '    if (.not. all(ieee_is_finite(leak1d_input32))) return\n',
        '    if (.not. all(ieee_is_finite(leak1d_input32))) return\n'
        '    if (.not. present(leak1d_input64)) return\n'
        '    if (size(leak1d_input64) /= NGRP) return\n'
        '    if (.not. all(ieee_is_finite(leak1d_input64))) return\n'
        '    do ig=1,NGRP\n'
        '      if(transfer(leak1d_input32(ig),0_int32)/= &\n'
        '          transfer(real(leak1d_input64(ig),real32),0_int32)) return\n'
        '    enddo\n')
    c.splice('native leak publication before actual host commit without fake BOOT lifecycle',
        "    if (publish_solved) then\n      call LCMPUT(ipflux,'LEAK1D64',NGRP,4,leak1d_input64)\n",
        "    call LCMPUT(ipflux,'LEAK1D64',NGRP,4,leak1d_input64)\n    if (publish_solved) then\n")
    kr,kp=read_pin(dependencies[3]);helper_names=['SYSTEM_PAYLOAD_IS_VALID',
        'RESPONSE_GROUP_IS_EXACT','FINITE_REAL32_RECORD','CANDIDATE_SYSTEM_ROOT_IS_EXACT']
    extracted=[body(kr,n) for n in helper_names]
    bind=BIND_HEAD.encode()+b'\n\n'.join(extracted)+b'end module SPOR64_BOOT_BIND64\n'
    proofs={'kernel':b.verify(),'publisher':c.verify(),
        'system_full_functions':[{'name':n,'sha256':hashlib.sha256(v).hexdigest(),
          'bytes':len(v),'exact_complete_original_body':True} for n,v in zip(helper_names,extracted)]}
    for raw in [bind,CALLER.encode()]:assert max(map(len,raw.splitlines()))<=132
    for name,raw in [('SPOR64_BOOTB64.f90',b.raw),('SPOR64_BOOTC64.f90',c.raw),
        ('SPOR64_BOOT_BIND64.f90',bind),('SPOBOOTRUN64.f90',CALLER.encode())]:fresh(OUT/name,raw)
    for p in dependencies[:5]:fresh(OUT/('ORIGINAL_COMPLETE_'+p.name),read_pin(p)[0])
    fresh_json(OUT/'COMPLETE_ONLINE_BOOT_WHOLE_BYTE_INVERSE_PROOFS.json',proofs)
    after=[read_pin(p)[1] for p in dependencies];assert before==after
    pins=[read_pin(OUT/n)[1] for n in ['SPOR64_BOOTB64.f90','SPOR64_BOOTC64.f90',
        'SPOR64_BOOT_BIND64.f90','SPOBOOTRUN64.f90']]
    ast.parse(read_pin(Path(__file__))[0])
    fresh_json(OUT/'CURRENT_COMPLETE_ONLINE_BOOT_SOURCE_BINDING.json',{
        'scope':'SOURCE ONLY; real V2 GLOBAL/projected/e0 full physical-Q/typed-flux/typed-leak -> actual original CORE -> real B2C then real B2I. No actual execution/qualification.',
        'source_pins':pins,'complete_dependencies_before':before,'complete_dependencies_after':after,
        'CLE_16_operand_order':['AX_OUT fresh memory','ARCH_OUT fresh memory','PROJECTED_BOOT',
          'GLOBAL64','AX','AX_TRACK','AX_SYSTEM','AX_MACRO','ARCH_ORIGINAL','RCON',
          'SYSTEM_FRESH_1','SYSTEM_FRESH_2','SYSTEM_FRESH_3','TRACK_f_1','TRACK_f_2','TRACK_f_3'],
        'case_rank':'Mandatory unique RANK >0, all 370 ranks exact same; owning host must independently verify frozen case_spec.basis.requested_rank == prepared.production_config.rank and pin full case/prepared/deck.',
        'physical_semantics':'Original TYPE S0 INIT ON REBA ON ACCE, 370 groups/32 fission slots/all scalar and higher unknowns, original radial eps/caps/strict-terminal/real CORE math kept. Old CONT e>0 functions preserved and never reached or relaxed.',
        'complete_native_ingress':'Context V2 full reader verifies actual global terminal/producer provenance plus full bound trees and ROOT-FLUX64; Q reader recomputes actual whole physical Q from same projected/global context and all 370x32. Fresh real ASM raw full response/control/math checks precede CORE. No legacy iterative promotion.',
        'real_seal':'New B2C first publishes actual accepted all-unknown flux/source and native leakage with no SOLVED/EPOCH/RHO labels. Actual original B2I_SEAL_BOOTSTRAP alone seals fresh final pair after all three real solves. No fake e1 or pre-solved e0.',
        'operator':'operator_source complete SPOASMG64 native eigen/online producer is required before actual GLOBAL. Never promote legacy RADIAL-OP to native.',
        'remaining':['Independent complete Source/interface review; actual Fortran compile is not performed',
          'True dispatcher/actual producer/global/projected/Q/ASM/BOOT owning deck route and current external fullfile SHA/7ID actual tool pins',
          'All 17 actual hostile controls (including coherent tamper via external pins) before actual transport',
          'Actual guarded compile/link/business solves and original physics/strict terminal/whole-input qualification'],
        'compiled':False,'numeric_executed':False,'physical_qualified':False})
    print(json.dumps({'status':'COMPLETE_ONLINE_BOOT_SOURCE_WRITTEN','source_pins':pins,
        'inverse_step_counts':{n:proofs[n]['actual_transform_steps'] for n in ['kernel','publisher']},
        'system_complete_functions':len(extracted),'protected_current_dependencies_unchanged':True,
        'Fortran_or_numeric_executed':False}))

if __name__=='__main__':main()
