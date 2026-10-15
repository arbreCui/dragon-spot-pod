"""Ordinary-rank1 factor storage compaction; no import-time business I/O.

Keep FACTOR64 and SOLVE64 byte-for-byte. After all full build solves, retain
strictly off-diagonal factor entries. Decode into the existing square lower
workspace before the unchanged SOLVE64. This source patch is not an RSS or
physical-accuracy qualification.
"""
from __future__ import annotations
import hashlib
import re
import copy
import importlib
from pathlib import Path
import sys

PARENT_KERNEL_SHA256 = '343e731fa190d80f8d390831185aef11dabcab32f51a229a5761c827a4aeb1e1'
SCHEMA = 'AXMAT_RANK1_DEAD_FACTOR_DIAGONAL_STORAGE_PATCH_V1'
PARENT_HELPER = Path('/Users/wen/spot/validation/axial_material/rank1_factor_cache_last_cprime_trim_patch.py')
PARENT_HELPER_SHA256 = '7a625a87f797e59f30c61408fe50012fee8b718cd0b487d76005118ce5302836'

FACTOR_CODEC = """
  ! Ordinary-rank1 only: FACTOR64/SOLVE64 no longer read factor diagonals
  ! after build. Keep every live entry, pivot, and pivot_value unchanged.
  subroutine SPOT1P64_RANK1_FACTOR_PACK(igroup)
    integer, intent(in) :: igroup
    double precision, allocatable :: packed(:,:,:)
    integer :: n,b,i,j,k,row
    integer(int64) :: full_bytes,packed_bytes,dead_bytes
    if (.not.rank1_enabled .or. .not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    if (size(SPOT1P64_PLAN(igroup)%mode) /= 1) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      n=plan%nstate; b=plan%nblock
      if (n <= 0 .or. b <= 0 .or. plan%ready .or. .not.allocated(plan%factor)) &
        call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
      if (any(shape(plan%factor) /= (/n,n,b/))) &
        call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
      if (int(n,int64) > RANK1_CAP/24_int64/int(n,int64)) &
        call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
      full_bytes=8_int64*int(n,int64)*int(n,int64)
      if (int(b,int64) > RANK1_CAP/full_bytes) &
        call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
      full_bytes=full_bytes*int(b,int64)
      dead_bytes=8_int64*int(n,int64)*int(b,int64)
      packed_bytes=full_bytes-dead_bytes
      if (plan%rank1_factor_bytes < full_bytes) &
        call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
      ! Both arrays coexist until move_alloc. Account the complete temporary.
      call SPOT1P64_RANK1_RESERVE(packed_bytes)
      allocate(packed(n-1,n,b))
      do k=1,b
        do j=1,n
          row=0
          do i=1,n
            if (i == j) cycle
            row=row+1
            packed(row,j,k)=plan%factor(i,j,k)
          enddo
        enddo
      enddo
      call move_alloc(packed,plan%factor)
      call SPOT1P64_RANK1_RELEASE(full_bytes)
      plan%rank1_factor_bytes=plan%rank1_factor_bytes-dead_bytes
    end associate
  end subroutine SPOT1P64_RANK1_FACTOR_PACK

  subroutine SPOT1P64_RANK1_FACTOR_LOAD(igroup,block,factor)
    integer, intent(in) :: igroup,block
    double precision, intent(out) :: factor(:,:)
    integer :: n,b,i,j,row
    if (.not.rank1_enabled .or. .not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    if (size(SPOT1P64_PLAN(igroup)%mode) /= 1) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      n=plan%nstate; b=plan%nblock
      if (n <= 0 .or. b <= 0 .or. .not.plan%ready .or. .not.allocated(plan%factor)) &
        call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
      if (any(shape(plan%factor) /= (/n-1,n,b/)) .or. &
          any(shape(factor) /= (/n,n/)) .or. block < 1 .or. block > b) &
        call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
      factor=0.0d0
      do j=1,n
        row=0
        do i=1,n
          if (i == j) cycle
          row=row+1
          factor(i,j)=plan%factor(row,j,block)
        enddo
      enddo
    end associate
  end subroutine SPOT1P64_RANK1_FACTOR_LOAD

"""

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

def compact_kernel(source):
    if sha(source) != PARENT_KERNEL_SHA256:
        raise ValueError('complete immutable last-cprime-trim kernel required')
    kernel=source
    edits=[]
    def change(old,new,region):
        nonlocal kernel
        if kernel.count(old)!=1:
            raise ValueError('source anchor must occur exactly once: '+region)
        kernel=kernel.replace(old,new,1)
        edits.append(dict(region=region,old=old,new=new))
    change('  public :: SPOT1P64_RANK1_LOWER_LOAD\n',
           '  public :: SPOT1P64_RANK1_LOWER_LOAD\n'
           '  public :: SPOT1P64_RANK1_FACTOR_PACK,SPOT1P64_RANK1_FACTOR_LOAD\n','public_codec')
    change('    SPOT1P64_RANK1_LOWER_LOAD\n',
           '    SPOT1P64_RANK1_LOWER_LOAD, &\n'
           '    SPOT1P64_RANK1_FACTOR_PACK,SPOT1P64_RANK1_FACTOR_LOAD\n','import_codec')
    change('  subroutine SPOT1P64_RANK1_LOWER_STORE(igroup,lower,du)\n',
           FACTOR_CODEC+'  subroutine SPOT1P64_RANK1_LOWER_STORE(igroup,lower,du)\n','factor_codec')
    change('      expected_bytes=expected_bytes-8_int64*square\n'
           '      if (expected_bytes /= plan%rank1_factor_bytes) &\n',
           '      expected_bytes=expected_bytes-8_int64*square\n'
           '      if (plan%ready .and. allocated(plan%factor)) then\n'
           '        if (any(shape(plan%factor) /= (/nstate-1,nstate,nblock/))) &\n'
           "          call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')\n"
           '        expected_bytes=expected_bytes-8_int64*int(nstate,int64)*int(nblock,int64)\n'
           '      endif\n'
           '      if (expected_bytes /= plan%rank1_factor_bytes) &\n','retained_accounting')
    change('            if (any(shape(plan%factor) /= (/local_state,local_state,nfloor+1/))) &\n',
           '            if (any(shape(plan%factor) /= (/local_state-1,local_state,nfloor+1/))) &\n','hit_physical_shape')
    old=('            call SPOT1P64_SOLVE64(plan%factor(:,:,block), &\n'
         '              plan%pivot(:,block),plan%pivot_value(:,block), &\n'
         '              rhs_one,info)\n')
    change(old,
           '            if (rank1_identity_active) then\n'
           '              call SPOT1P64_RANK1_FACTOR_LOAD(igroup,block,rank1_lower_work)\n'
           '              call SPOT1P64_SOLVE64(rank1_lower_work, &\n'
           '                plan%pivot(:,block),plan%pivot_value(:,block), &\n'
           '                rhs_one,info)\n'
           '            else\n'+old+'            endif\n','hit_decode_existing_workspace')
    change('          plan%ready=.true.\n'
           '          call SPOT1P64_CACHE_NOTE_BUILD(nfloor+1)\n',
           '          if (rank1_identity_active) call SPOT1P64_RANK1_FACTOR_PACK(igroup)\n'
           '          plan%ready=.true.\n'
           '          call SPOT1P64_CACHE_NOTE_BUILD(nfloor+1)\n','pack_after_all_original_build_solves')
    inverse=kernel
    for edit in reversed(edits):
        if inverse.count(edit['new'])!=1:
            raise ValueError('source inverse anchor ambiguous: '+edit['region'])
        inverse=inverse.replace(edit['new'],edit['old'],1)
    if inverse!=source or any(len(line)>132 for line in kernel.splitlines()):
        raise ValueError('complete source inverse or Fortran width failed')
    unchanged={}
    for name in ('SPOT1P64_FACTOR64','SPOT1P64_SOLVE64'):
        pattern=rf'  subroutine {name}\(.*?  end subroutine {name}'
        a=re.findall(pattern,source,re.S);b=re.findall(pattern,kernel,re.S)
        if len(a)!=1 or a!=b:raise ValueError('original mathematical routine changed: '+name)
        unchanged[name]=sha(a[0])
    return dict(kernel=kernel,proof=dict(schema=SCHEMA,parent_kernel_sha256=sha(source),
        candidate_kernel_sha256=sha(kernel),complete_inverse_byteexact=True,
        retained_mathematical_routine_byte_sha256=unchanged,edits=edits,
        physical_ready_factor_shape='[nstate-1,nstate,nblock]',
        square_solve_workspace='existing rank1_lower_work, reused after lower RHS matmul',
        full_build_factor_and_solve_operations_retained=True,
        transient_pack_reservation_bytes='8*(nstate-1)*nstate*nblock',
        exact_persistent_reduction_bytes='8*nstate*nblock',
        ordinary_rank1_only=True,legacy_dense_and_uncached_paths_unchanged=True,
        factor_type_descriptor_unchanged=True,actual_controls_executed=False,
        actual_native_RSS_passed=False,AAA_accuracy_qualified=False,ABA_admitted=False))

def _last_cprime_parent():
    if PARENT_HELPER.is_symlink() or hashlib.sha256(PARENT_HELPER.read_bytes()).hexdigest()!=PARENT_HELPER_SHA256:
        raise ValueError('immutable last-cprime-trim helper required')
    sys.path.insert(0,str(PARENT_HELPER.parent))
    parent=importlib.import_module(PARENT_HELPER.stem)
    if parent.__file__!=str(PARENT_HELPER) or parent.__spec__.origin!=str(PARENT_HELPER):
        raise ValueError('actual canonical last-cprime-trim helper required')
    if hashlib.sha256(PARENT_HELPER.read_bytes()).hexdigest()!=PARENT_HELPER_SHA256:
        raise ValueError('last-cprime-trim helper changed while importing')
    return parent

def patch_kernel(source):
    """Preserve the complete original c0-to-trim lineage and append this patch."""
    base=_last_cprime_parent().patch_kernel(source)
    compact=compact_kernel(base['kernel'])
    proof=copy.deepcopy(base['proof'])
    proof['edits']+=compact['proof']['edits']
    proof['factor_diagonal_trim']=compact['proof']
    proof['candidate_kernel_sha256']=sha(compact['kernel'])
    proof['delegated_last_cprime_helper']=dict(path=str(PARENT_HELPER),sha256=PARENT_HELPER_SHA256)
    proof['scope']='ORDINARY_RANK1_LOWER_DICTIONARY_TERMINAL_CPRIME_AND_DEAD_FACTOR_DIAGONAL_STORAGE_ONLY'
    proof['persistent_accounting']='parent post-dedup/last-cprime retained bytes minus exactly 8*nstate*nblock after FACTOR_PACK'
    proof['preallocation_accounting']='parent worst reservation unchanged; packed coexistence fully RESERVED until move_alloc releases dense factor'
    inverse=compact['kernel']
    for edit in reversed(proof['edits']):
        if inverse.count(edit['new'])!=1:
            raise ValueError('complete c0 source inverse ambiguous')
        inverse=inverse.replace(edit['new'],edit['old'],1)
    if inverse!=source:
        raise ValueError('complete c0 source inverse differs')
    proof['complete_inverse_byteexact']=True
    proof['inverse_kernel_sha256']=sha(inverse)
    return dict(kernel=compact['kernel'],proof=proof)

def control_contract():
    contract=copy.deepcopy(_last_cprime_parent().control_contract())
    contract['factor_diagonal_trim']=dict(schema=SCHEMA,ordinary_rank1_only=True,
        ready_factor_physical_shape='[nstate-1,nstate,nblock]',public_solve_shape='[nstate,nstate]',
        retained_build_all_original_factor_and_full_RHS_solves=True,
        all_original_40_stages_required=True,persistent_release_bytes='8*nstate*nblock',
        transient_pack_reservation_bytes='8*(nstate-1)*nstate*nblock',
        reused_square_workspace='rank1_lower_work',actual_native_RSS_passed=False)
    return contract

def dense_reference_kernel(source):
    return _last_cprime_parent().dense_reference_kernel(source)
