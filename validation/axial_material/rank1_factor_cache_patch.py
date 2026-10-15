"""Reviewable source-only rank1-factor-cache-20261007 patch recipe.

No compiler, transport, numerical control, artifact creation, or admission is
performed by this module.  Consumers must retain the inputs and rendered sources
before executing the separately declared controls.  The ordinary rank-one cache
has its own enable flag, exact identity, accounting, and terminal observer.
"""
from __future__ import annotations

import hashlib

KERNEL_SHA = "7544212ac8419f9c73688c12339c8779358a24f4065523fbbf891cc4fe1c79e0"
SENDER_SHA = "15b0a314886ed224204a53dc77e52fe79114ef00eee81230f80d28eaed4a8316"
EXPERIMENT = "rank1-factor-cache-20261007"
CACHE_CAP = 512 * 1024 * 1024
DESCRIPTOR_BYTES_PER_GROUP = 4096
IDENTITY_ERROR = "SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED."
CAP_ERROR = "SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED."


def digest(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def replace_once(source: str, old: str, new: str, changes: list) -> str:
    if source.count(old) != 1:
        raise ValueError("patch anchor is not unique: " + repr(old[:100]))
    changes.append({"old": old, "new": new})
    return source.replace(old, new, 1)


POOL_DECL = """
  ! Separate ordinary-rank1 lifecycle; never changes the legacy enable flag.
  logical, save :: rank1_enabled=.false.
  integer(int64), parameter :: RANK1_CAP=536870912_int64
  integer(int64), parameter :: RANK1_DESCRIPTOR_PER_GROUP=4096_int64
  integer(int64), save :: rank1_bytes=0_int64,rank1_peak=0_int64
  integer(int64), save :: rank1_builds=0_int64,rank1_reuses=0_int64
  integer(int64), save :: rank1_validated_hits=0_int64
  public :: SPOT1P64_RANK1_ENABLED,SPOT1P64_RANK1_RESERVE
  public :: SPOT1P64_RANK1_RELEASE,SPOT1P64_RANK1_GUARD
  public :: SPOT1P64_RANK1_FACTORS,SPOT1P64_RANK1_STATS
  public :: SPOT1P64_RANK1_TERMINAL,SPOT1P64_RANK1_PROGRESS
"""

POOL_ROUTINES = """
  logical function SPOT1P64_RANK1_ENABLED()
    SPOT1P64_RANK1_ENABLED=rank1_enabled
  end function SPOT1P64_RANK1_ENABLED

  subroutine SPOT1P64_RANK1_RESERVE(amount)
    integer(int64), intent(in) :: amount
    if (amount < 0_int64 .or. amount > RANK1_CAP-rank1_bytes) &
      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
    rank1_bytes=rank1_bytes+amount
    rank1_peak=max(rank1_peak,rank1_bytes)
  end subroutine SPOT1P64_RANK1_RESERVE

  subroutine SPOT1P64_RANK1_RELEASE(amount)
    integer(int64), intent(in) :: amount
    if (amount < 0_int64 .or. amount > rank1_bytes) &
      call XABORT('SPOT1P64 RANK1 CACHE: INVALID ACCOUNTING RELEASE.')
    rank1_bytes=rank1_bytes-amount
  end subroutine SPOT1P64_RANK1_RELEASE

  subroutine SPOT1P64_RANK1_GUARD(igroup,key,phase,eligible,active)
    integer, intent(in) :: igroup,phase
    integer(int64), intent(in) :: key(:)
    logical, intent(in) :: eligible
    logical, intent(out) :: active
    integer(int64) :: amount
    active=.false.
    if (.not.rank1_enabled) return
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 CACHE: INVALID ENERGY GROUP.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) then
      if (.not.eligible) return
      ! All descriptors/scalars are covered by 4096 declared bytes/group.
      allocate(SPOT1P64_PLAN(igroup)%mode(1))
    endif
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (.not.eligible) &
        call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
      if (size(key,kind=int64) > RANK1_CAP/8_int64) &
        call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
      amount=size(key,kind=int64)*8_int64
      if (phase == 1) then
        if (allocated(plan%rank1_raw_bits)) then
          if (size(plan%rank1_raw_bits) /= size(key)) &
            call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
          if (any(plan%rank1_raw_bits /= key)) &
            call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
        else
          call SPOT1P64_RANK1_RESERVE(amount)
          allocate(plan%rank1_raw_bits(size(key)))
          plan%rank1_raw_bits=key
        endif
      else if (phase == 2) then
        if (.not.allocated(plan%rank1_raw_bits)) &
          call XABORT('SPOT1P64 RANK1 CACHE: MISSING RAW IDENTITY.')
        if (allocated(plan%rank1_operator_bits)) then
          if (size(plan%rank1_operator_bits) /= size(key)) &
            call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
          if (any(plan%rank1_operator_bits /= key)) &
            call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
          if (plan%ready) rank1_validated_hits=rank1_validated_hits+1_int64
        else
          call SPOT1P64_RANK1_RESERVE(amount)
          allocate(plan%rank1_operator_bits(size(key)))
          plan%rank1_operator_bits=key
        endif
      else
        call XABORT('SPOT1P64 RANK1 CACHE: INVALID IDENTITY PHASE.')
      endif
      active=.true.
    end associate
  end subroutine SPOT1P64_RANK1_GUARD

  subroutine SPOT1P64_RANK1_FACTORS(igroup,nstate,nblock)
    integer, intent(in) :: igroup,nstate,nblock
    integer(int64) :: square,amount,blocks
    if (.not.rank1_enabled) return
    if (nstate <= 0 .or. nblock <= 0) &
      call XABORT('SPOT1P64 RANK1 CACHE: INVALID FACTOR DIMENSIONS.')
    if (int(nstate,int64) > RANK1_CAP/24_int64/int(nstate,int64)) &
      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
    square=int(nstate,int64)*int(nstate,int64)
    ! factor/lower/cprime REAL64; pivot_value REAL64; pivot INTEGER32.
    amount=24_int64*square+12_int64*int(nstate,int64)
    blocks=int(nblock,int64)
    if (blocks > RANK1_CAP/amount) &
      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
    amount=amount*blocks
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (plan%rank1_factor_bytes /= 0_int64) &
        call XABORT('SPOT1P64 RANK1 CACHE: FACTORS ALREADY RESERVED.')
      call SPOT1P64_RANK1_RESERVE(amount)
      plan%rank1_factor_bytes=amount
    end associate
  end subroutine SPOT1P64_RANK1_FACTORS

  subroutine SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)
    integer(int64), intent(out) :: built,reused,hits,live,peak,cap
    built=rank1_builds
    reused=rank1_reuses
    hits=rank1_validated_hits
    live=rank1_bytes
    peak=rank1_peak
    cap=RANK1_CAP
  end subroutine SPOT1P64_RANK1_STATS

  subroutine SPOT1P64_RANK1_TERMINAL()
    if (rank1_enabled.and.rank1_builds > 0_int64) write(6,'(A,5(1X,I0))') &
      'AXMAT-RANK1-CACHE TERMINAL',rank1_builds,rank1_reuses, &
      rank1_validated_hits,rank1_peak,RANK1_CAP
  end subroutine SPOT1P64_RANK1_TERMINAL

  subroutine SPOT1P64_RANK1_PROGRESS(it,jt,igdeb,einn)
    integer, intent(in) :: it,jt,igdeb
    double precision, intent(in) :: einn
    if (.not.rank1_enabled .or. rank1_builds == 0_int64) return
    if (jt /= 1 .and. mod(jt,32) /= 0) return
    write(6,'(A,3(1X,I0),1X,ES25.16E3,4(1X,I0))') &
      'AXMAT-RANK1-CACHE PROGRESS',it,jt,igdeb,einn, &
      rank1_builds,rank1_reuses,rank1_validated_hits,rank1_peak
    flush(6)
  end subroutine SPOT1P64_RANK1_PROGRESS
"""

# The key is copied scalar by scalar: no packed array-constructor or TRANSFER
# array temporary is hidden from the explicitly reserved temporary key bytes.
# Raw identity catches changed dimensions, signed zero, and changed eligibility
# before old validation/dispatch can bypass a previously populated group.
IDENTITY_ROUTINES = """
  subroutine rank1_identity(phase,active)
    integer, intent(in) :: phase
    logical, intent(out) :: active
    integer(int64), allocatable :: key(:)
    integer(int64) :: count_key,position,temporary_bytes
    integer :: aa,bb,rr,ss,zz,ll,nn
    logical :: eligible
    active=.false.
    if (.not.SPOT1P64_RANK1_ENABLED()) return
    eligible=nmode == 1 .and. nreg2d > 1 .and. .not.any(ncode == 4)
    if (phase == 1) then
      count_key=17_int64
      call key_count_add(count_key,size(mat1d,kind=int64))
      call key_count_add(count_key,size(mat,kind=int64))
      call key_count_add(count_key,size(vol1d,kind=int64))
      call key_count_add(count_key,size(total,kind=int64))
      call key_count_add(count_key,size(sgas,kind=int64))
      call key_count_add(count_key,size(basis,kind=int64))
      call key_count_add(count_key,size(vol2d,kind=int64))
      call key_count_add(count_key,size(radial2d,kind=int64))
      call key_count_add(count_key,size(du,kind=int64))
      call key_count_add(count_key,size(w,kind=int64))
      call key_count_add(count_key,size(pl,kind=int64))
      call key_count_add(count_key,size(zcode,kind=int64))
    else
      count_key=2_int64
      call key_count_add(count_key,size(weight,kind=int64))
      call key_count_add(count_key,size(mass_m,kind=int64))
      call key_count_add(count_key,size(total_m,kind=int64))
      call key_count_add(count_key,size(radial_m,kind=int64))
      call key_count_add(count_key,size(scat_m,kind=int64))
      call key_count_add(count_key,size(mn,kind=int64))
      call key_count_add(count_key,size(dn,kind=int64))
      if (AXMAT_WHITE_ON) then
        call key_count_add(count_key,size(white_angle,kind=int64))
        call key_count_add(count_key,size(white_mode,kind=int64))
      endif
    endif
    if (count_key < 0_int64 .or. count_key > 536870912_int64/8_int64) &
      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
    temporary_bytes=8_int64*count_key
    call SPOT1P64_RANK1_RESERVE(temporary_bytes)
    allocate(key(count_key))
    position=0_int64
    if (phase == 1) then
      call key_integer(key,position,nreg2d)
      call key_integer(key,position,nfloor)
      call key_integer(key,position,ielem)
      call key_integer(key,position,nmat)
      call key_integer(key,position,nsnap)
      call key_integer(key,position,nmode)
      call key_integer(key,position,ischm)
      call key_integer(key,position,npq)
      call key_integer(key,position,nsct)
      call key_integer(key,position,merge(1,0,lfixup))
      call key_integer(key,position,merge(1,0,AXMAT_WHITE_ON))
      call key_integer(key,position,AXMAT_WHITE_ROW)
      call key_real64(key,position,AXMAT_WHITE_PERIMETER)
      call key_integer(key,position,ncode(1))
      call key_integer(key,position,ncode(2))
      ! Explicit ABI is also part of the immutable identity.
      call key_integer(key,position,storage_size(0.0))
      call key_integer(key,position,storage_size(0.0d0))
      do zz=1,nfloor
        call key_integer(key,position,mat1d(zz))
        call key_real32(key,position,vol1d(zz))
      enddo
      do rr=1,nreg2d
        do zz=1,nfloor
          call key_integer(key,position,mat(zz,rr))
        enddo
      enddo
      do rr=0,nmat
        call key_real32(key,position,total(rr))
      enddo
      do ll=1,nsct
        do rr=0,nmat
          call key_real32(key,position,sgas(rr,ll))
        enddo
      enddo
      do aa=1,nmode
        do rr=1,nreg2d
          call key_real32(key,position,basis(rr,aa))
        enddo
      enddo
      do rr=1,nreg2d
        call key_real32(key,position,vol2d(rr))
      enddo
      do ss=1,nsnap
        do rr=1,nreg2d
          call key_real64(key,position,radial2d(rr,ss))
        enddo
      enddo
      do nn=1,npq
        call key_real32(key,position,du(nn))
        call key_real32(key,position,w(nn))
        do ll=1,nsct
          call key_real32(key,position,pl(ll,nn))
        enddo
      enddo
      call key_real32(key,position,zcode(1))
      call key_real32(key,position,zcode(2))
    else
      call key_real64(key,position,albedo_left)
      call key_real64(key,position,albedo_right)
      do rr=1,nreg2d
        call key_real64(key,position,weight(rr))
      enddo
      do bb=1,nmode
        do aa=1,nmode
          call key_real64(key,position,mass_m(aa,bb))
        enddo
      enddo
      do zz=1,nfloor
        do bb=1,nmode
          do aa=1,nmode
            call key_real64(key,position,total_m(aa,bb,zz))
            call key_real64(key,position,radial_m(aa,bb,zz))
          enddo
        enddo
      enddo
      do zz=1,nfloor
        do ll=1,nsct
          do bb=1,nmode
            do aa=1,nmode
              call key_real64(key,position,scat_m(aa,bb,ll,zz))
            enddo
          enddo
        enddo
      enddo
      do ll=1,nsct
        do nn=1,npq
          call key_real64(key,position,mn(nn,ll))
          call key_real64(key,position,dn(ll,nn))
        enddo
      enddo
      if (AXMAT_WHITE_ON) then
        do nn=1,npq
          do rr=1,npq
            call key_real64(key,position,white_angle(rr,nn))
          enddo
        enddo
        do bb=1,nmode
          do aa=1,nmode
            call key_real64(key,position,white_mode(aa,bb))
          enddo
        enddo
      endif
    endif
    if (position /= count_key) &
      call XABORT('SPOT1P64 RANK1 CACHE: IDENTITY LENGTH ERROR.')
    call SPOT1P64_RANK1_GUARD(igroup,key,phase,eligible,active)
    deallocate(key)
    call SPOT1P64_RANK1_RELEASE(temporary_bytes)
  end subroutine rank1_identity

  subroutine key_count_add(total,amount)
    integer(int64), intent(inout) :: total
    integer(int64), intent(in) :: amount
    if (amount < 0_int64 .or. amount > 536870912_int64/8_int64-total) &
      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
    total=total+amount
  end subroutine key_count_add

  subroutine key_integer(key,position,value)
    integer(int64), intent(inout) :: key(:),position
    integer, intent(in) :: value
    position=position+1_int64
    key(position)=int(value,int64)
  end subroutine key_integer

  subroutine key_real32(key,position,value)
    integer(int64), intent(inout) :: key(:),position
    real, intent(in) :: value
    position=position+1_int64
    key(position)=int(transfer(value,0_int32),int64)
  end subroutine key_real32

  subroutine key_real64(key,position,value)
    integer(int64), intent(inout) :: key(:),position
    double precision, intent(in) :: value
    position=position+1_int64
    key(position)=transfer(value,0_int64)
  end subroutine key_real64
"""


def patch_sources(kernel_text: str, sender_text: str) -> dict:
    if digest(kernel_text) != KERNEL_SHA or digest(sender_text) != SENDER_SHA:
        raise ValueError("actual compiled source baseline digest mismatch")
    kchanges, schanges = [], []
    k = kernel_text
    k = replace_once(k, "module SPOT1P64_CACHE_MOD\n  implicit none", "module SPOT1P64_CACHE_MOD\n  use, intrinsic :: iso_fortran_env, only: int32,int64\n  implicit none", kchanges)
    k = replace_once(k, "    logical :: ready=.false.\n", "    logical :: ready=.false.\n    integer(int64) :: rank1_factor_bytes=0_int64\n    integer(int64), allocatable :: rank1_raw_bits(:),rank1_operator_bits(:)\n", kchanges)
    k = replace_once(k, "  integer, save :: reused_blocks=0\n", "  integer, save :: reused_blocks=0\n" + POOL_DECL, kchanges)
    old = """  subroutine SPOT1P64_CACHE_BEGIN(ngroup,enable)
    integer, intent(in) :: ngroup
    logical, intent(in) :: enable
    call SPOT1P64_CACHE_CLEAR()
    if (.not.enable) return
    if (ngroup <= 0) call XABORT('SPOT1P64 CACHE: INVALID GROUP COUNT.')
    allocate(SPOT1P64_PLAN(ngroup))
    cache_enabled=.true.
  end subroutine SPOT1P64_CACHE_BEGIN"""
    new = """  subroutine SPOT1P64_CACHE_BEGIN(ngroup,enable,enable_rank1)
    integer, intent(in) :: ngroup
    logical, intent(in) :: enable
    logical, optional, intent(in) :: enable_rank1
    call SPOT1P64_CACHE_CLEAR()
    if (present(enable_rank1)) rank1_enabled=enable_rank1.and.(.not.enable)
    if (.not.enable.and..not.rank1_enabled) return
    if (ngroup <= 0) call XABORT('SPOT1P64 CACHE: INVALID GROUP COUNT.')
    if (rank1_enabled) then
      if (storage_size(0) /= 32 .or. storage_size(0.0) /= 32 .or. &
          storage_size(0.0d0) /= 64 .or. storage_size(0_int64) /= 64) &
        call XABORT('SPOT1P64 RANK1 CACHE: UNSUPPORTED ELEMENT ABI.')
      if (ngroup > 370) &
        call XABORT('SPOT1P64 RANK1 CACHE: GROUP COUNT EXCEEDS DECLARED 370.')
      call SPOT1P64_RANK1_RESERVE(int(ngroup,int64)*RANK1_DESCRIPTOR_PER_GROUP)
    endif
    allocate(SPOT1P64_PLAN(ngroup))
    cache_enabled=enable
  end subroutine SPOT1P64_CACHE_BEGIN"""
    k = replace_once(k, old, new, kchanges)
    k = replace_once(k, "    reused_blocks=0\n", "    reused_blocks=0\n    rank1_enabled=.false.\n    rank1_bytes=0_int64\n    rank1_peak=0_int64\n    rank1_builds=0_int64\n    rank1_reuses=0_int64\n    rank1_validated_hits=0_int64\n", kchanges)
    k = replace_once(k, "    factorized_blocks=factorized_blocks+nblock\n", "    if (rank1_enabled) then\n      rank1_builds=rank1_builds+int(nblock,int64)\n    else\n    factorized_blocks=factorized_blocks+nblock\n    endif\n", kchanges)
    k = replace_once(k, "    reused_blocks=reused_blocks+nblock\n", "    if (rank1_enabled) then\n      rank1_reuses=rank1_reuses+int(nblock,int64)\n    else\n    reused_blocks=reused_blocks+nblock\n    endif\n", kchanges)
    k = replace_once(k, "end module SPOT1P64_CACHE_MOD\n", POOL_ROUTINES + "\nend module SPOT1P64_CACHE_MOD\n", kchanges)
    k = replace_once(k, "  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite\n", "  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite\n  use, intrinsic :: iso_fortran_env, only: int32,int64\n", kchanges)
    k = replace_once(k, "    SPOT1P64_FACTOR64,SPOT1P64_SOLVE64\n", "    SPOT1P64_FACTOR64,SPOT1P64_SOLVE64,SPOT1P64_RANK1_ENABLED, &\n    SPOT1P64_RANK1_RESERVE,SPOT1P64_RANK1_RELEASE, &\n    SPOT1P64_RANK1_GUARD,SPOT1P64_RANK1_FACTORS\n", kchanges)
    k = replace_once(k, "  logical :: translation,diagonal_basis,mode_separable,use_factor_cache\n", "  logical :: translation,diagonal_basis,mode_separable,use_factor_cache\n  logical :: rank1_identity_active\n", kchanges)
    k = replace_once(k, "  if (ielem /= 1 .or. ischm /= 1) &\n", "  call rank1_identity(1,rank1_identity_active)\n\n  if (ielem /= 1 .or. ischm /= 1) &\n", kchanges)
    anchor = "  if (.not.translation) then\n    ! Solve the two-point boundary-value problem directly."
    k = replace_once(k, anchor, "  if (rank1_identity_active) then\n    call rank1_identity(2,rank1_identity_active)\n    use_factor_cache=rank1_identity_active\n  endif\n\n" + anchor, kchanges)
    anchor = "          allocate(plan%factor(local_state,local_state,nfloor+1))\n"
    k = replace_once(k, anchor, "          if (rank1_identity_active) &\n            call SPOT1P64_RANK1_FACTORS(igroup,local_state,nfloor+1)\n" + anchor, kchanges)
    k = replace_once(k, "contains\n\n  subroutine boundary_solve", "contains\n" + IDENTITY_ROUTINES + "\n  subroutine boundary_solve", kchanges)
    s = sender_text
    s = replace_once(s, "     1 SPOT1P64_CACHE_CLEAR,SPOT1P64_CACHE_STATS\n", "     1 SPOT1P64_CACHE_CLEAR,SPOT1P64_CACHE_STATS,\n     2 SPOT1P64_RANK1_TERMINAL,SPOT1P64_RANK1_PROGRESS\n", schanges)
    s = replace_once(s, "      CALL SPOT1P64_CACHE_BEGIN(NGRP,IPHYS_CACHE.EQ.1)\n", "      CALL SPOT1P64_CACHE_BEGIN(NGRP,IPHYS_CACHE.EQ.1,\n     1 (CXDOOR.EQ.'SPOT').AND.(NDIM.EQ.1).AND.(INSB.GT.0)\n     2 .AND.(IPHYS_CACHE.EQ.0))\n", schanges)
    # Exactly two original closeout locations, including non-convergence.
    if s.count("      CALL SPOT1P64_CACHE_CLEAR()\n") != 2:
        raise ValueError("sender lifecycle CLEAR locations changed")
    old_clear = "      CALL SPOT1P64_CACHE_CLEAR()\n"
    new_clear = "      CALL SPOT1P64_RANK1_TERMINAL()\n" + old_clear
    schanges.append({"old": old_clear, "new": new_clear, "count": 2})
    s = s.replace(old_clear, new_clear)
    s = replace_once(s, "      ITERF=JT\n", "      CALL SPOT1P64_RANK1_PROGRESS(IT,JT,IGDEB,EINN)\n      ITERF=JT\n", schanges)
    reference = kernel_text.replace("SPOT1P64_CACHE_MOD", "AXMAT_ORIGINAL_CACHE_MOD")
    reference = reference.replace("subroutine SPOT1P64(", "subroutine SPOT1P64_ORIGINAL(")
    reference = reference.replace("end subroutine SPOT1P64\n", "end subroutine SPOT1P64_ORIGINAL\n")
    proof = dict(schema="AXMAT_RANK1_FACTOR_CACHE_SOURCE_PATCH_V1", experiment=EXPERIMENT,
                 original_kernel_sha256=KERNEL_SHA, original_sender_sha256=SENDER_SHA,
                 kernel_sha256=digest(k), sender_sha256=digest(s),
                 kernel_changes=kchanges, sender_changes=schanges,
                 reference_kernel_sha256=digest(reference), reference_unit_only=True,
                 reference_delta="Only module and main routine symbol names; inverse restores exact original bytes",
                 legacy_physical_enable_semantics_preserved=True,
                 legacy_dense_and_translation_algorithms_preserved=True,
                 ordinary_rank1_operator_identity="Exact primitive and projected IEEE bits including signed zero; excludes qext/source_m/RHS",
                 source_projection_and_all_matrix_RHS_factor_solve_arithmetic_unchanged=True,
                 cache_element_cap_bytes=CACHE_CAP,
                 cache_descriptor_bytes_per_group=DESCRIPTOR_BYTES_PER_GROUP,
                 temporary_key_element_bytes_included=True, no_LRU_or_input_change=True,
                 counter_delta="Ordinary rank1 NOTE_BUILD/NOTE_REUSE updates independent INTEGER64 counters only; legacy INTEGER CACHE_STATS ABI and original physical else-statements preserved; no LHS/RHS/iteration changes",
                 progress_observer_only="First and every 32nd completed inner iteration; original IPRT, algorithm, counters, residuals unchanged; rank1-built pool only",
                 controls_executed=False, production_transport_executed=False)
    result = dict(kernel=k, sender=s, reference_kernel=reference, proof=proof)
    verify_sources(kernel_text, sender_text, result)
    return result


def verify_sources(original_kernel: str, original_sender: str, patched: dict) -> dict:
    """Pure byte/string inverse proof; no imports of runtime/scientific code."""
    if digest(original_kernel) != KERNEL_SHA or digest(original_sender) != SENDER_SHA:
        raise ValueError("inverse baseline mismatch")
    for name, original, entries in (("kernel", original_kernel, patched["proof"]["kernel_changes"]),
                                    ("sender", original_sender, patched["proof"]["sender_changes"])):
        source = patched[name]
        for entry in reversed(entries):
            count = entry.get("count", 1)
            if source.count(entry["new"]) != count:
                raise ValueError("inverse anchor mismatch in " + name)
            source = source.replace(entry["new"], entry["old"], count)
        if source != original:
            raise ValueError("inverse bytes differ in " + name)
    reference = patched["reference_kernel"].replace("AXMAT_ORIGINAL_CACHE_MOD", "SPOT1P64_CACHE_MOD")
    reference = reference.replace("subroutine SPOT1P64_ORIGINAL(", "subroutine SPOT1P64(")
    reference = reference.replace("end subroutine SPOT1P64_ORIGINAL\n", "end subroutine SPOT1P64\n")
    if reference != original_kernel:
        raise ValueError("reference inverse differs")
    return dict(kernel_inverse_byte_exact=True, sender_inverse_byte_exact=True,
                reference_inverse_byte_exact=True, numerical_execution=False)


def control_contract() -> dict:
    negatives = ["total", "selfscat", "radial", "basis", "mesh", "du", "weights", "pl",
                 "boundary", "signed_zero", "white_on", "white_row", "white_perimeter", "dims"]
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_CONTROL_CONTRACT_V1", experiment=EXPERIMENT,
                positive_cases=["production_white_370", "signed_nonunit", "lifecycle_reset_1", "lifecycle_reset_2",
                                "legacy_physical", "legacy_dense", "legacy_translation", "pivot_split"],
                negative_cases=[dict(name=name,args=["negative",name],expected_message=IDENTITY_ERROR) for name in negatives],
                cap_negative_cases=[dict(name="cap_reserve",args=["cap-negative","cap_reserve"],expected_message=CAP_ERROR),
                    dict(name="cap_factor_dimensions",args=["cap-negative","cap_factor_dimensions"],expected_message=CAP_ERROR)],
                cap_request_stream="int64[12]:version=1,operation(1=reserve,2=factor_dimensions),ngroup=370,nstate(0 or HUGE(INTEGER32)),nblock(0 or49),requested_bytes(cap-live+1 or0),built,reused,hits,live,peak,cap; archived before actual guard call; expected dimensions reject before multiplication/array allocation",
                cache_accounting_cap_rejection_unit_control_required=True,
                OwnRSS_overlimit_rejection_test_claimed=False,
                argv_positive=["positive"], argv_negative_prefix=["negative"],
                positive_command_args=["positive"], cache_byte_cap=CACHE_CAP,
                geometry=dict(height_cm=150,axial_cells=48,radial_regions=8,total_regions=384,sn=32,scat=3,rank=1),
                all_energy_groups=list(range(1,371)), all_fields_bitwise_required=["flux","cour","xnei"],
                nonunit_Gram_required=True, signed_basis_required=True, changing_RHS_required=True,
                raw_before_numeric_gates=True,
                positive_fixtures=[dict(name="production_white_370",groups=370,nrhs=3,nreg2d=8,nfloor=48,npq=32,nsct=3,nmode=1,white=True,rank1=True),
                    dict(name="signed_nonunit",groups=2,nrhs=3,nreg2d=8,nfloor=48,npq=32,nsct=3,nmode=1,white=False,rank1=True),
                    dict(name="lifecycle_reset_1",groups=2,nrhs=3,nreg2d=8,nfloor=48,npq=32,nsct=3,nmode=1,white=False,rank1=True),
                    dict(name="lifecycle_reset_2",groups=2,nrhs=3,nreg2d=8,nfloor=48,npq=32,nsct=3,nmode=1,white=False,rank1=True),
                    dict(name="legacy_physical",groups=2,nrhs=3,nreg2d=2,nfloor=3,npq=8,nsct=3,nmode=2,white=False,rank1=False),
                    dict(name="legacy_dense",groups=2,nrhs=3,nreg2d=2,nfloor=3,npq=8,nsct=3,nmode=2,white=False,rank1=False),
                    dict(name="legacy_translation",groups=2,nrhs=3,nreg2d=8,nfloor=3,npq=8,nsct=3,nmode=1,white=False,rank1=False)],
                guard_rejection="Actual patched-kernel or cache-resource XABORT unit stub: archive exact message, STOP0 only for the command-specific expected identity/CAP error; unexpected error/normal return nonzero",
                full_production_XABORT_ABI_claimed=False, cache_cap_bytes=CACHE_CAP,
                descriptor_bytes_per_group=DESCRIPTOR_BYTES_PER_GROUP,
                key_accounting="Each scalar packed as int64: raw identity count=17+size(mat1d)+size(mat)+size(dz)+size(total)+size(selfscat)+size(basis)+size(volume)+size(radial)+size(du)+size(w)+size(pl)+size(zcode). Projected count=2+size(weight)+size(G)+size(total_m)+size(radial_m)+size(scat_m)+size(mn)+size(dn)+white_on*(size(white_angle)+size(white_mode)). Retained both keys plus the one live temporary key counted before allocate. Factor bytes/block=24*npq*npq+12*npq; descriptor allowance=4096*ngroup. No source/RHS data in key.",
                fixture_physics="Synthetic fixed operators, original ALGPT Gauss-Legendre quadrature; production 48 floors/32 directions/3 moments/384 regional cells/370 groups",
                raw_output="Exclusive stream-unformatted little-endian native ABI; int64 header[12] then contiguous REAL64 flux,cour,xnei; JSONL manifest binds per-group input_file, role/group/RHS and actual counters/bytes",
                raw_header=["version", "nreg2d", "nfloor", "npq", "nsct", "nmode", "group", "rhs", "flux_count", "cour_count", "xnei_count", "reserved_zero"],
                roles=["original", "build", "reuse"],
                input_stream="int64 header[12]=version,nreg2d,nfloor,npq,nsct,nmode,nmat,nsnap,white_row,white_on,0,0; INTEGER32 mat1d,mat; REAL32 dz,total,sgas,basis,volume; REAL64 radial; INTEGER32 ncode; REAL32 zcode,du,w,pl; REAL64 white_perimeter. Each group input retained after group total change; each role separate q REAL64 stream.",
                pivot_stream="inputs:matrix4x4/RHS4x3 REAL64; original/split:int64 info + REAL64 solution4x3; factors:int64 info + REAL64 factor4x4 + INTEGER32 pivot4 + REAL64 pivot_value4",
                all_raw_before_Python_finite_bitwise_counter_gate=True,
                no_driver_numerical_PASS_gate=True, archive_total_cap_bytes=2*1024**3,
                stream_audit_required=True, scientific_accuracy_or_speed_claimed=False)
