"""Ordinary rank1 dead terminal cprime storage trim, source preparation only.

Import performs no I/O or production imports. All original last-block solve
columns and arithmetic remain. New actual controls and native RSS are required.
"""
from __future__ import annotations

import copy
import hashlib
import importlib
from pathlib import Path
import sys

SCHEMA = 'AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_SOURCE_PATCH_V1'
TRIM_SCHEMA = 'AXMAT_RANK1_UNUSED_TERMINAL_CPRIME_STORAGE_SOURCE_PATCH_V1'
PARENT_HELPER = Path('/Users/wen/spot/validation/axial_material/rank1_factor_cache_memory_dedup_patch.py')
PARENT_HELPER_SHA256 = '6596aa9a11b8f86e837a23add01b24970a87ba4aabf6007fc3ada1925884ccf2'
PARENT_KERNEL_SHA256 = 'c0fddcd2ddc4dba6969440024a9205fbb297727a6a045886acba626323ab5718'
DENSE_PARENT_KERNEL_SHA256 = 'c017167b5c48bc922efb7353db8c11a91758add1c2c5a02c42bd2baaeba210a2'
PARENT_DEDUP_KERNEL_SHA256 = '50071dfc713cd1a7f319e392706686c73ef250ea03049a91ef29d5dec341adb6'
CAP_BYTES = 536870912


def _sha(source):
    return hashlib.sha256(source.encode()).hexdigest()


def _parent():
    p=PARENT_HELPER
    if p.is_symlink() or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=PARENT_HELPER_SHA256:
        raise ValueError('entire immutable ordinary memory-dedup helper required')
    name=p.stem
    existing=sys.modules.get(name)
    if existing is not None and (getattr(existing,'__file__',None)!=str(p) or existing.__spec__ is None
                                or existing.__spec__.origin!=str(p)):
        raise ValueError('existing ordinary parent helper source differs')
    sys.path.insert(0,str(p.parent))
    module=importlib.import_module(name)
    if module.__file__!=str(p) or module.__spec__ is None or module.__spec__.origin!=str(p):
        raise ValueError('actual parent helper must use its real file and module stem')
    if hashlib.sha256(p.read_bytes()).hexdigest()!=PARENT_HELPER_SHA256:
        raise ValueError('parent helper changed during normal import')
    return module


def trim_dedup_kernel(source):
    if not isinstance(source,str) or _sha(source)!=PARENT_DEDUP_KERNEL_SHA256:
        raise ValueError('entire immutable50071 dedup kernel required')
    kernel=source
    edits=[]

    def change(old,new,region):
        nonlocal kernel
        if kernel.count(old)!=1:
            raise ValueError('one whole original trim source anchor required: '+region)
        offset=kernel.index(old)
        kernel=kernel.replace(old,new,1)
        edits.append(dict(old=old,new=new,region=region,original_offset=offset,
                          old_sha256=_sha(old),new_sha256=_sha(new)))

    change('    amount=amount+map_bytes\n',
           '    amount=amount+map_bytes\n'
           '    ! Last cprime is never read; keep every full original solve.\n'
           '    amount=amount-8_int64*square\n',
           'FACTORS_exact_one_dead_cprime_block_reservation_reduction')
    change('        4_int64*int(nrow,int64)+4_int64*int(nblock,int64)\n'
           '      if (expected_bytes /= plan%rank1_factor_bytes) &\n',
           '        4_int64*int(nrow,int64)+4_int64*int(nblock,int64)\n'
           '      expected_bytes=expected_bytes-8_int64*square\n'
           '      if (expected_bytes /= plan%rank1_factor_bytes) &\n',
           'LOWER_VALIDATE_exact_retained_accounting_reduction')
    change('          allocate(plan%cprime(local_state,local_state,nfloor+1))\n',
           '          if (rank1_identity_active) then\n'
           '            allocate(plan%cprime(local_state,local_state,nfloor))\n'
           '          else\n'
           '            allocate(plan%cprime(local_state,local_state,nfloor+1))\n'
           '          endif\n',
           'ordinary_rank1_only_terminal_cprime_allocation_trim')
    change('            plan%cprime(:,:,block)=solve_pack(:,:local_state)\n',
           '            if (.not.rank1_identity_active .or. block <= nfloor) &\n'
           '              plan%cprime(:,:,block)=solve_pack(:,:local_state)\n',
           'ordinary_rank1_only_dead_terminal_store_guard')
    change('        if (cache_hit) then\n'
           '          do block=1,nfloor+1\n',
           '        if (cache_hit) then\n'
           '          if (rank1_identity_active) then\n'
           '            if (.not.allocated(plan%factor) .or. .not.allocated(plan%cprime)) &\n'
           "              call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')\n"
           '            if (any(shape(plan%factor) /= (/local_state,local_state,nfloor+1/))) &\n'
           "              call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')\n"
           '            if (any(shape(plan%cprime) /= (/local_state,local_state,nfloor/))) &\n'
           "              call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')\n"
           '          endif\n'
           '          do block=1,nfloor+1\n',
           'actual_cached_boundary_hit_ordinary_shapes_not_primitive_GATE')
    restored=kernel
    for edit in reversed(edits):
        if restored.count(edit['new'])!=1:
            raise ValueError('whole trim inverse ambiguous')
        restored=restored.replace(edit['new'],edit['old'],1)
    if restored!=source or any(len(line)>132 for line in kernel.splitlines()):
        raise ValueError('whole original dedup source inverse/Fortran width failed')
    return dict(kernel=kernel,proof=dict(schema=TRIM_SCHEMA,parent_dedup_kernel_sha256=_sha(source),
        candidate_kernel_sha256=_sha(kernel),complete_inverse_to_dedup_byteexact=True,
        inverse_kernel_sha256=_sha(restored),edits=edits,ordinary_rank1_only=True,
        full_33_rhs_solve_unchanged=True,persistent_cprime_blocks='nblock-1',
        bytes_saved_per_group='8*nstate^2',actual_controls_executed=False,
        actual_native_RSS_passed=False,AAA_accuracy_qualified=False,ABA_admitted=False))


def patch_kernel(source):
    base=_parent().patch_kernel(source)
    trim=trim_dedup_kernel(base['kernel'])
    proof=copy.deepcopy(base['proof'])
    proof['edits']+=trim['proof']['edits']
    proof['candidate_kernel_sha256']=_sha(trim['kernel'])
    proof['last_cprime_trim']=trim['proof']
    proof['delegated_parent_helper']=dict(path=str(PARENT_HELPER),sha256=PARENT_HELPER_SHA256)
    proof['scope']='ORDINARY_RANK1_LOWER_RAW_BIT_DICTIONARY_AND_UNUSED_TERMINAL_CPRIME_STORAGE_ONLY'
    proof['persistent_accounting']='(16*nstate^2+12*nstate)*nblock+8*nrow*nstate*nunique+4*nrow+4*nblock-8*nstate^2'
    proof['preallocation_accounting']='unchanged checked positive original worst bound minus exactly8*nstate^2 before RESERVE'
    restored=trim['kernel']
    for edit in reversed(proof['edits']):
        if restored.count(edit['new'])!=1:
            raise ValueError('full c0 inverse anchor differs')
        restored=restored.replace(edit['new'],edit['old'],1)
    if restored!=source or _sha(restored)!=PARENT_KERNEL_SHA256:
        raise ValueError('whole source must inversely restore immutable c0')
    proof['complete_inverse_byteexact']=True
    proof['inverse_kernel_sha256']=_sha(restored)
    return dict(kernel=trim['kernel'],proof=proof)


def control_contract():
    contract=copy.deepcopy(_parent().control_contract())
    contract['last_cprime_trim']=dict(schema=TRIM_SCHEMA,ordinary_rank1_only=True,
        persistent_cprime_blocks='nblock-1',bytes_saved_per_group='8*nstate^2',
        actual_boundary_cprime_extent_required=True,all_original_40_stages_required=True,
        last_block_full_33_rhs_solve_retained=True,actual_controls_executed=False,
        actual_native_RSS_passed=False)
    return contract


def dense_reference_kernel(source):
    return _parent().dense_reference_kernel(source)
