#!/usr/bin/env python3
"""Source-only, exclusive draft generation; never invokes a compiler or Dragon."""
import base64
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import stat

REC = Path(__file__).resolve().parent
ROOT = REC.parents[2]
DRAFT = REC / 'bq64_compact_expected_composed_source_draft_v1_20261013'
OLD = REC / 'bootstrap_qfiss_source_v2/SPOR64_BOOTQ64.f90'
COMPARATOR = REC / 'new_source/SPOR64_BOOT64.f90'
BUILD70 = ROOT / 'validation/artifacts/axial-material-new-native-rank1-exact-block-cache-complete70-build-only-20261012-v2/Root_actual_build_only_summary.json'


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def read_pin(path):
    path = Path(path)
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode) and not path.is_symlink(), str(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        assert identity(os.fstat(fd)) == identity(before)
        pieces = []
        while True:
            piece = os.read(fd, 1024 * 1024)
            if not piece:
                break
            pieces.append(piece)
        data = b''.join(pieces)
        assert len(data) == before.st_size
        assert identity(os.fstat(fd)) == identity(before)
    finally:
        os.close(fd)
    assert identity(path.lstat()) == identity(before)
    return data, dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(),
                     size_bytes=len(data), identity=identity(before))


def write_once(name, data):
    path = DRAFT / name
    raw = data.encode() if isinstance(data, str) else data
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    try:
        assert os.write(fd, raw) == len(raw)
        os.fsync(fd)
    finally:
        os.close(fd)
    got, pin = read_pin(path)
    assert got == raw and pin['identity'][3] == 1
    return pin


def jwrite(name, data):
    return write_once(name, json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def region(text, start, end):
    assert text.count(start) == 1 and text.count(end) == 1
    begin = text.index(start)
    finish = text.index(end, begin) + len(end)
    return text[begin:finish]


PRIVATE_CONSTANTS = '''  ! Private composed comparison retains the original BOOT64 limits.
  integer, parameter :: MAX_DEPTH = 64, MAX_NODES = 2000000
  integer, parameter :: MAX_RECORD_WORDS = 16777216
  integer, parameter :: composed_integer_kind_guard = &
      1 / merge(1,0,kind(1) == int32)
  integer, parameter :: VIEW_NONE = -1, VIEW_ROOT = 0, VIEW_AUTH = 1
  integer, parameter :: VIEW_GLOBAL = 2, VIEW_SEED = 3
  integer(int64), parameter :: COMPACT_FIXED_BYTES = 844632_int64
  integer(int64), parameter :: COMPACT_BYTES_PER_UNKNOWN = 7400_int64
  integer(int64), parameter :: COMPACT_STORAGE_CAP = 32_int64*1024_int64*1024_int64

'''

BUDGET = '''  logical function COMPACT_EXPECTED_STORAGE_FITS(nunkno)
    integer, intent(in) :: nunkno
    integer(int64) :: required_bytes
    COMPACT_EXPECTED_STORAGE_FITS = .false.
    if (nunkno <= 0) return
    required_bytes = COMPACT_FIXED_BYTES + &
        COMPACT_BYTES_PER_UNKNOWN*int(nunkno,int64)
    COMPACT_EXPECTED_STORAGE_FITS = required_bytes <= COMPACT_STORAGE_CAP
  end function COMPACT_EXPECTED_STORAGE_FITS

'''

COMPOSED_FRONT = '''  ! Exactly two empty expected placeholders are resolved to immutable inputs.
  ! Every resolved subtree then uses the original full raw tree comparison.
  logical function BQ64_SAME_COMPOSED_SOURCE(left,right,ipglobal,ipseed)
    type(c_ptr), intent(in) :: left,right,ipglobal,ipseed
    integer :: nodes, visited(2)
    logical :: equal
    nodes = 0
    visited = 0
    BQ64_SAME_COMPOSED_SOURCE = .false.
    if (.not.c_associated(left).or..not.c_associated(right)) return
    if (.not.c_associated(ipglobal).or..not.c_associated(ipseed)) return
    equal = BQ64_COMPOSED_NODE(left,right,0,nodes,VIEW_ROOT, &
        ipglobal,ipseed,visited)
    BQ64_SAME_COMPOSED_SOURCE = equal.and.all(visited == 1)
  end function BQ64_SAME_COMPOSED_SOURCE

  recursive logical function BQ64_COMPOSED_NODE(left,right,depth,nodes, &
      view,ipglobal,ipseed,visited) result(equal)
    type(c_ptr), intent(in) :: left,right,ipglobal,ipseed
    integer, intent(in) :: depth,view
    integer, intent(inout) :: nodes,visited(2)
    type(c_ptr) :: resolved_left
    character(len=72) :: file_name
    character(len=12) :: object_name
    integer :: slot,extent,next_view
    logical :: empty,medium
    equal = .false.
    if (depth > MAX_DEPTH) return
    if (.not.c_associated(left).or..not.c_associated(right)) return
    resolved_left = left
    next_view = view
    if (view == VIEW_GLOBAL.or.view == VIEW_SEED) then
      if (depth /= 2) return
      slot = view-1
      if (visited(slot) /= 0) return
      ! The parent has already compared both directory type/length metadata.
      call LCMINF(left,file_name,object_name,empty,extent,medium)
      if (.not.empty.or.extent /= -1) return
      if (view == VIEW_GLOBAL) then
        resolved_left = ipglobal
      else
        resolved_left = ipseed
      endif
      if (.not.c_associated(resolved_left)) return
      visited(slot) = 1
      next_view = VIEW_NONE
    else if (view == VIEW_ROOT) then
      if (depth /= 0) return
    else if (view == VIEW_AUTH) then
      if (depth /= 1) return
    else if (view /= VIEW_NONE) then
      return
    endif
    ! This call compares empty flags, inventories, extents and all raw words
    ! after resolution, with the original cumulative depth and shared nodes.
    equal = BQ64_SAME_DIRECTORY(resolved_left,right,depth,nodes,next_view, &
        ipglobal,ipseed,visited)
  end function BQ64_COMPOSED_NODE

'''


def matcher_clone(old_comparator):
    directory = region(old_comparator,
        '  recursive logical function SAME_DIRECTORY(',
        '  end function SAME_DIRECTORY\n')
    lists = region(old_comparator,
        '  recursive logical function SAME_LIST(',
        '  end function SAME_LIST\n')
    record = region(old_comparator,
        '  logical function SAME_RECORD(',
        '  end function SAME_RECORD\n')
    for name in ('SAME_DIRECTORY', 'SAME_LIST', 'SAME_RECORD'):
        directory = directory.replace(name, 'BQ64_' + name)
        lists = lists.replace(name, 'BQ64_' + name)
        record = record.replace(name, 'BQ64_' + name)
    directory = directory.replace(
        'BQ64_SAME_DIRECTORY(left,right,depth,nodes) result(equal)',
        'BQ64_SAME_DIRECTORY(left,right,depth,nodes, &\n'
        '      view,ipglobal,ipseed,visited) result(equal)', 1)
    directory = directory.replace('    type(c_ptr), intent(in) :: left, right\n',
        '    type(c_ptr), intent(in) :: left,right,ipglobal,ipseed\n', 1)
    directory = directory.replace('    integer, intent(in) :: depth\n',
        '    integer, intent(in) :: depth,view\n', 1)
    directory = directory.replace('    integer, intent(inout) :: nodes\n',
        '    integer, intent(inout) :: nodes,visited(2)\n'
        '    integer :: child_view\n', 1)
    directory = directory.replace(
        '        if (.not. BQ64_SAME_DIRECTORY(child_left,child_right,depth+1,nodes)) return',
        '''        child_view = VIEW_NONE
        if (view == VIEW_ROOT.and.depth == 0.and.item_name == 'SPOT-R64') then
          child_view = VIEW_AUTH
        else if (view == VIEW_AUTH.and.depth == 1) then
          if (item_name == 'GLOBAL64') child_view = VIEW_GLOBAL
          if (item_name == 'SEED') child_view = VIEW_SEED
        endif
        if (.not. BQ64_COMPOSED_NODE(child_left,child_right,depth+1,nodes, &
            child_view,ipglobal,ipseed,visited)) return''', 1)
    directory = directory.replace(
        '        if (.not. BQ64_SAME_LIST(child_left,child_right,length_left,depth+1,nodes)) return',
        '        if (.not. BQ64_SAME_LIST(child_left,child_right,length_left,depth+1,nodes, &\n'
        '            ipglobal,ipseed,visited)) return', 1)
    lists = lists.replace(
        'BQ64_SAME_LIST(left,right,extent,depth,nodes) result(equal)',
        'BQ64_SAME_LIST(left,right,extent,depth,nodes, &\n'
        '      ipglobal,ipseed,visited) result(equal)', 1)
    lists = lists.replace('    type(c_ptr), intent(in) :: left, right\n',
        '    type(c_ptr), intent(in) :: left,right,ipglobal,ipseed\n', 1)
    lists = lists.replace('    integer, intent(inout) :: nodes\n',
        '    integer, intent(inout) :: nodes,visited(2)\n', 1)
    lists = lists.replace(
        '        if (.not. BQ64_SAME_DIRECTORY(child_left,child_right,depth+1,nodes)) return',
        '        if (.not. BQ64_COMPOSED_NODE(child_left,child_right,depth+1,nodes, &\n'
        '            VIEW_NONE,ipglobal,ipseed,visited)) return', 1)
    lists = lists.replace(
        '        if (.not. BQ64_SAME_LIST(child_left,child_right,length_left,depth+1,nodes)) return',
        '        if (.not. BQ64_SAME_LIST(child_left,child_right,length_left,depth+1,nodes, &\n'
        '            ipglobal,ipseed,visited)) return', 1)
    assert 'SAME_DIRECTORY(child_left,child_right,depth+1,nodes))' not in directory + lists
    assert record.replace('BQ64_SAME_RECORD', 'SAME_RECORD') == region(
        old_comparator, '  logical function SAME_RECORD(', '  end function SAME_RECORD\n')
    return directory + '\n' + lists + '\n' + record


CONTROL_PROGRAM = '''program test_BQ64_compact_composed_tree
  use, intrinsic :: iso_c_binding, only : c_ptr,c_null_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  use GANLIB
  use BQ64_COMPACT_CONTROL_ACCESS
  implicit none
  type(c_ptr) :: expected,actual,global,seed,auth,branch,child,groups
  integer :: assertions,case_id,words(8),g,nodes,total_nodes,visited(2),deep
  integer(int64) :: file_size
  logical :: ok,exists
  assertions = 0
  call check(.not.COMPACT_EXPECTED_STORAGE_FITS(0))
  call check(COMPACT_EXPECTED_STORAGE_FITS(1))
  call check(COMPACT_EXPECTED_STORAGE_FITS(14))
  call check(COMPACT_EXPECTED_STORAGE_FITS(4420))
  call check(.not.COMPACT_EXPECTED_STORAGE_FITS(4421))
  call check(.not.COMPACT_EXPECTED_STORAGE_FITS(huge(1)))
  ! Model trees contain no physical solve or production inputs.
  do case_id=0,12
    call setup(1)
    auth=LCMGID(actual,'SPOT-R64')
    select case(case_id)
    case(1)
      branch=LCMGID(auth,'GLOBAL64');words=0;words(1)=99
      call LCMPUT(branch,'RAW-1',2,1,words)
    case(2)
      branch=LCMGID(auth,'SEED');words=0;words(1)=99
      call LCMPUT(branch,'RAW-1',2,1,words)
    case(3)
      branch=LCMGID(auth,'GLOBAL64');words=0;words(2)=int(z'80000000',int32)
      call LCMPUT(branch,'RAW-4',2,4,transfer(words(1:4),[0.0_real64,0.0_real64]))
    case(4)
      branch=LCMGID(auth,'GLOBAL64');call LCMPUT(branch,'EXTRA',1,1,1)
    case(5)
      auth=LCMGID(expected,'SPOT-R64');branch=LCMGID(auth,'GLOBAL64')
      call LCMPUT(branch,'DIRTY',1,1,1)
    case(6)
      auth=LCMGID(expected,'SPOT-R64');branch=LCMGID(auth,'SEED')
      call LCMPUT(branch,'DIRTY',1,1,1)
    case(7)
      call LCMPUT(actual,'STATE-VECTOR',1,1,1)
    case(8)
      branch=LCMGID(auth,'GLOBAL64');call LCMPUT(branch,'RAW-1',2,2,[0.0,0.0])
    case(9)
      call LCMPUT(actual,'EXTRA-ROOT',1,1,1)
    case(10)
      call LCMPUT(auth,'EXTRA-AUTH',1,1,1)
    case(11)
      branch=LCMGID(auth,'GLOBAL64');child=LCMGID(branch,'SEED')
      call LCMPUT(child,'MARKER',1,1,99)
    case(12)
      groups=LCMGID(actual,'ROOT-QFISS64');words=0;words(2)=int(z'80000000',int32)
      call LCMPDL(groups,370,1,4,[transfer(words(1:2),0.0_real64)])
    end select
    ok=BQ64_SAME_COMPOSED_SOURCE(expected,actual,global,seed)
    call check(ok.eqv.(case_id == 0))
    if (case_id == 0) then
      call check(.not.BQ64_SAME_COMPOSED_SOURCE(expected,actual,c_null_ptr,seed))
      call check(.not.BQ64_SAME_COMPOSED_SOURCE(expected,actual,global,c_null_ptr))
      call check(.not.BQ64_SAME_COMPOSED_SOURCE(c_null_ptr,actual,global,seed))
      nodes=0;visited=0
      ok=BQ64_COMPOSED_NODE(expected,actual,0,nodes,VIEW_ROOT,global,seed,visited)
      call check(ok.and.all(visited == 1));total_nodes=nodes
      nodes=MAX_NODES-total_nodes;visited=0
      ok=BQ64_COMPOSED_NODE(expected,actual,0,nodes,VIEW_ROOT,global,seed,visited)
      call check(ok.and.nodes == MAX_NODES.and.all(visited == 1))
      nodes=MAX_NODES-total_nodes+1;visited=0
      ok=BQ64_COMPOSED_NODE(expected,actual,0,nodes,VIEW_ROOT,global,seed,visited)
      call check(.not.ok)
      nodes=0;visited=1
      ok=BQ64_COMPOSED_NODE(expected,actual,0,nodes,VIEW_ROOT,global,seed,visited)
      call check(.not.ok)
      call check(.not.BQ64_SAME_RECORD(global,global,'RAW-1',0,MAX_RECORD_WORDS+1,1))
      call check(.not.BQ64_SAME_RECORD(global,global,'RAW-4',0,MAX_RECORD_WORDS/2+1,4))
      call check(.not.BQ64_SAME_RECORD(global,global,'RAW-1',0,1,7))
    endif
    call close_all()
  enddo
  do deep=62,63
    call setup(1)
    branch=global
    do g=1,deep
      child=LCMDID(branch,'DEEP');branch=child
    enddo
    call LCMPUT(branch,'END',1,1,1)
    auth=LCMGID(actual,'SPOT-R64');branch=LCMGID(auth,'GLOBAL64')
    call LCMEQU(global,branch)
    call check(BQ64_SAME_COMPOSED_SOURCE(expected,actual,global,seed).eqv.(deep == 62))
    call close_all()
  enddo
  ! The physical-bound model uses the exact small writer layout and NUNKNO14.
  inquire(file='C64-EXP',exist=exists);call check(.not.exists)
  inquire(file='C64-ACT',exist=exists);call check(.not.exists)
  call setup(14,2)
  call check(BQ64_SAME_COMPOSED_SOURCE(expected,actual,global,seed))
  call LCMCL(expected,1)
  inquire(file='C64-EXP',size=file_size)
  call check(file_size == 844632_int64+7400_int64*14_int64)
  call check(file_size <= 32_int64*1024_int64*1024_int64)
  ! Future Host retains these two model files; no production artifact is touched.
  call LCMCL(actual,1);call LCMCL(global,2);call LCMCL(seed,2)
  write(*,'(A,I0,A)') '{"status":"ACTUAL_COMPACT_GANLIB_MODEL_CONTROLS_ONLY","assertions":', &
      assertions,',"physics_qualified":false,"reader_qualified":false,"AAA_qualified":false}'
contains
  subroutine check(condition)
    logical,intent(in) :: condition
    if (.not.condition) call XABORT('BQ64 COMPACT CONTROL ASSERTION FAILED.')
    assertions=assertions+1
  end subroutine check
  subroutine setup(nunkno,medium)
    integer,intent(in) :: nunkno
    integer,optional,intent(in) :: medium
    integer :: kind_file,t
    kind_file=1;if(present(medium))kind_file=medium
    call LCMOP(global,'C64-GLOBAL',0,1,0);call LCMOP(seed,'C64-SEED',0,1,0)
    words=0
    do t=1,6
      call put_raw(global,t);call put_raw(seed,t)
    enddo
    child=LCMDID(global,'SEED');call LCMPUT(child,'MARKER',1,1,7)
    child=LCMDID(seed,'GLOBAL64');call LCMPUT(child,'MARKER',1,1,8)
    groups=LCMLID(global,'LIST',3)
    child=LCMDIL(groups,1);call LCMPUT(child,'ONE',1,1,1)
    call LCMPDL(groups,2,2,1,[1,2])
    child=LCMDIL(groups,3);child=LCMDID(child,'GLOBAL64')
    call LCMPUT(child,'MARKER',1,1,9)
    call LCMOP(expected,'C64-EXP',0,kind_file,0)
    call LCMOP(actual,'C64-ACT',0,kind_file,0)
    call populate(expected,nunkno,.true.);call populate(actual,nunkno,.false.)
  end subroutine setup
  subroutine put_raw(root,type_code)
    type(c_ptr),intent(in) :: root
    integer,intent(in) :: type_code
    character(len=5) :: name
    write(name,'(A,I1)') 'RAW-',type_code
    select case(type_code)
    case(1,3)
      call LCMPUT(root,name,2,type_code,words(1:2))
    case(2)
      call LCMPUT(root,name,2,2,transfer(words(1:2),[0.0_real32,0.0_real32]))
    case(4)
      call LCMPUT(root,name,2,4,transfer(words(1:4),[0.0_real64,0.0_real64]))
    case(5)
      call LCMPUT(root,name,2,5,[.false.,.false.])
    case(6)
      call LCMPUT(root,name,2,6,[cmplx(0.0,0.0),cmplx(0.0,0.0)])
    end select
  end subroutine put_raw
  subroutine populate(root,nunkno,compact)
    type(c_ptr),intent(in) :: root
    integer,intent(in) :: nunkno
    logical,intent(in) :: compact
    type(c_ptr) :: a,outer,inner,qlist,rlist,c
    integer :: state(40),i
    real(real32),allocatable :: q32(:)
    real(real64),allocatable :: q64(:)
    allocate(q32(nunkno),q64(nunkno));q32=0.0_real32;q64=0.0_real64
    call LCMPTC(root,'SIGNATURE',12,'L_SOURCE    ')
    state=0;state(1:3)=[370,nunkno,1]
    call LCMPUT(root,'STATE-VECTOR',40,1,state)
    call LCMPUT(root,'SPOT-FROZEN',1,1,1)
    call LCMPUT(root,'SPOT-KEFF',1,2,1.0_real32)
    call LCMPUT(root,'SPOT-QINT',370,2,[(0.0_real32,i=1,370)])
    outer=LCMLID(root,'DSOUR',1);inner=LCMLIL(outer,1,370)
    do i=1,370
      call LCMPDL(inner,i,nunkno,2,q32)
    enddo
    a=LCMDID(root,'SPOT-R64')
    call LCMPUT(a,'RHO',1,4,1.0_real64);call LCMPUT(a,'PLANE',1,1,1)
    call LCMPTC(a,'STATE',12,'FROZEN-QFIS ')
    call LCMPUT(a,'NORM',1,4,1.0_real64)
    c=LCMDID(a,'GLOBAL64');if(.not.compact)call LCMEQU(global,c)
    c=LCMDID(a,'SEED');if(.not.compact)call LCMEQU(seed,c)
    qlist=LCMLID(a,'QFISS',370)
    do i=1,370
      call LCMPDL(qlist,i,nunkno,4,q64)
    enddo
    rlist=LCMLID(root,'ROOT-QFISS64',370)
    do i=1,370
      call LCMPDL(rlist,i,nunkno,4,q64)
    enddo
    call LCMPUT(a,'EPOCH',1,1,0)
  end subroutine populate
  subroutine close_all()
    call LCMCL(expected,2);call LCMCL(actual,2)
    call LCMCL(global,2);call LCMCL(seed,2)
  end subroutine close_all
end program test_BQ64_compact_composed_tree
'''


def main():
    old_bytes, old_pin = read_pin(OLD)
    comparator_bytes, comparator_pin = read_pin(COMPARATOR)
    assert old_pin['sha256'] == '7172121d57c3411c62845a81cc41886ee9759d4c168423b13541fc3a91afecd8'
    assert comparator_pin['sha256'] == 'cd19000790003d84645ea323ffa95766ba1478230c9c703d32b05b555f1425a7'
    original = old_bytes.decode()
    comparator = comparator_bytes.decode()
    public_build = region(original, '  subroutine SPOR64_BOOTQ64_BUILD(',
                          '  end subroutine SPOR64_BOOTQ64_BUILD\n')
    clone = public_build.replace('SPOR64_BOOTQ64_BUILD', 'BQ64_BUILD_COMPACT_EXPECTED')
    marker = '    ! MACRO0 is a recursive copy of the selected macrolib.'
    assert clone.count(marker) == 1
    clone = clone.replace(marker,
        '    ! Only a fresh compact expected tree receives this storage-bound gate.\n'
        '    if (.not.COMPACT_EXPECTED_STORAGE_FITS(nunkno)) return\n\n' + marker, 1)
    assert clone.count('    call LCMEQU(ipglobal,child)\n') == 1
    assert clone.count('    call LCMEQU(input_flux,child)\n') == 1
    clone = clone.replace('    call LCMEQU(ipglobal,child)\n', '', 1)
    clone = clone.replace('    call LCMEQU(input_flux,child)\n', '', 1)
    inverse_clone = clone.replace('BQ64_BUILD_COMPACT_EXPECTED', 'SPOR64_BOOTQ64_BUILD')
    inverse_clone = inverse_clone.replace(
        '    ! Only a fresh compact expected tree receives this storage-bound gate.\n'
        '    if (.not.COMPACT_EXPECTED_STORAGE_FITS(nunkno)) return\n\n', '', 1)
    inverse_clone = inverse_clone.replace("    child=LCMDID(source_authority,'GLOBAL64')\n",
        "    child=LCMDID(source_authority,'GLOBAL64')\n    call LCMEQU(ipglobal,child)\n", 1)
    inverse_clone = inverse_clone.replace("    child=LCMDID(source_authority,'SEED')\n",
        "    child=LCMDID(source_authority,'SEED')\n    call LCMEQU(input_flux,child)\n", 1)
    assert inverse_clone == public_build
    helpers = COMPOSED_FRONT + matcher_clone(comparator)
    old_read = region(original, '  subroutine SPOR64_BOOTQ64_READ(',
                      '  end subroutine SPOR64_BOOTQ64_READ\n')
    new_read = old_read.replace(
        '    type(c_ptr) :: staged_macro,staged_source,source_auth,typed_source\n',
        '    type(c_ptr) :: staged_macro,staged_source,source_auth,typed_source\n'
        '    type(c_ptr) :: original_fluxes,original_seed\n', 1)
    new_read = new_read.replace(
        '    ! Private disk-backed full trees avoid duplicating the archive in memory.\n',
        '    ! Private disk-backed expected records use two immutable context views.\n', 1)
    new_read = new_read.replace('    call SPOR64_BOOTQ64_BUILD(',
                                '    call BQ64_BUILD_COMPACT_EXPECTED(', 1)
    new_read = new_read.replace(
        '      same_source=SPOR64_BOOT64_SAME_TREE(staged_source,ipsource)\n',
        "      original_fluxes=LCMGID(ipprojected,'FLUX')\n"
        '      original_seed=LCMGIL(original_fluxes,plane_index)\n'
        '      same_source=BQ64_SAME_COMPOSED_SOURCE(staged_source,ipsource, &\n'
        '          ipglobal,original_seed)\n', 1)
    candidate = original.replace('contains\n', PRIVATE_CONSTANTS + 'contains\n', 1)
    candidate = candidate.replace(old_read, new_read, 1)
    candidate = candidate.replace('end module SPOR64_BOOTQ64_V2\n',
        '\n' + clone + '\n' + BUDGET + helpers + '\nend module SPOR64_BOOTQ64_V2\n', 1)
    assert region(candidate, '  subroutine SPOR64_BOOTQ64_BUILD(',
                  '  end subroutine SPOR64_BOOTQ64_BUILD\n') == public_build
    assert re.findall(r'^.*\bpublic\b.*$', candidate, re.M | re.I) == \
        re.findall(r'^.*\bpublic\b.*$', original, re.M | re.I)
    assert max(map(len, candidate.splitlines())) <= 132
    control = '''! Source-only fixture. This module is never linked into Dragon.
module BQ64_COMPACT_CONTROL_ACCESS
  use, intrinsic :: iso_c_binding, only : c_associated,c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64
  use GANLIB
  implicit none
  private
''' + PRIVATE_CONSTANTS + '''  public :: COMPACT_EXPECTED_STORAGE_FITS,BQ64_SAME_COMPOSED_SOURCE
  public :: BQ64_COMPOSED_NODE,BQ64_SAME_RECORD,VIEW_ROOT,MAX_NODES,MAX_RECORD_WORDS
contains
''' + BUDGET + helpers + 'end module BQ64_COMPACT_CONTROL_ACCESS\n\n' + CONTROL_PROGRAM
    assert max(map(len, control.splitlines())) <= 132
    original_pins = [old_pin, comparator_pin]
    closure_paths = [
        ROOT/'src/SPOR64_VERIFY.f90', ROOT/'src/SPOR64_RCONTRACT.f90',
        ROOT/'src/SPOR64_SCHEMA.f90', ROOT/'Ganlib/src/ganlib.f90',
        ROOT/'Ganlib/src/LCMAUX.f90', ROOT/'Ganlib/src/LCMMOD.f90',
        ROOT/'Ganlib/src/xsm_c.c', ROOT/'Ganlib/src/xsm.h',
        ROOT/'Ganlib/src/kdi_c.c', ROOT/'Ganlib/src/lcm_c.c',
        REC/'bootstrap_context_expected_planes_source_v3/SPOR64_BOOT_CONTEXT64.f90',
        REC/'online_boot_native64_source_v1/SPOR64_BOOT_BIND64.f90',
        REC/'online_boot_native64_source_v1/SPOR64_BOOTB64.f90',
        REC/'aaa_three_plane_streaming_source_v2/SPOBOOX64.f90',
    ]
    for path in closure_paths:
        _, pin = read_pin(path)
        original_pins.append(pin)
    build_bytes, build_pin = read_pin(BUILD70)
    build = json.loads(build_bytes)
    ordered = build['actual_complete70_link_inputs']
    assert len(ordered) == 70 and sum(p.endswith('.a') for p in ordered) == 4
    assert Path(ordered[40]).name == 'SPOR64_BOOTQ64.o'
    assert len([p for p in ordered if p.endswith('.o')]) == 66
    old_pin_again = read_pin(OLD)[1]
    assert old_pin_again == old_pin and read_pin(COMPARATOR)[1] == comparator_pin
    DRAFT.mkdir(exist_ok=False)
    candidate_pin = write_once('SPOR64_BOOTQ64.f90', candidate)
    control_pin = write_once('test_BQ64_compact_composed_tree.f90', control)
    delta = ''.join(difflib.unified_diff(original.splitlines(True),
        candidate.splitlines(True), fromfile=str(OLD), tofile=str(DRAFT/'SPOR64_BOOTQ64.f90')))
    diff_pin = write_once('SPOR64_BOOTQ64.original_v2_to_candidate.diff', delta)
    old_lines, new_lines = old_bytes.splitlines(True), candidate.encode().splitlines(True)
    old_offsets, new_offsets = [0], [0]
    for line in old_lines: old_offsets.append(old_offsets[-1]+len(line))
    for line in new_lines: new_offsets.append(new_offsets[-1]+len(line))
    blocks = []
    for op,a,b,c,d in difflib.SequenceMatcher(None,old_lines,new_lines,autojunk=False).get_opcodes():
        if op == 'equal': continue
        original_piece = old_bytes[old_offsets[a]:old_offsets[b]]
        new_piece = candidate.encode()[new_offsets[c]:new_offsets[d]]
        blocks.append(dict(original_offset=old_offsets[a],original_end=old_offsets[b],
            candidate_offset=new_offsets[c],candidate_end=new_offsets[d],
            original_bytes_base64=base64.b64encode(original_piece).decode(),
            original_piece_sha256=hashlib.sha256(original_piece).hexdigest(),
            candidate_piece_sha256=hashlib.sha256(new_piece).hexdigest()))
    cursor=0;restored=[]
    for block in blocks:
        restored.append(candidate.encode()[cursor:block['candidate_offset']])
        restored.append(base64.b64decode(block['original_bytes_base64']))
        cursor=block['candidate_end']
    restored.append(candidate.encode()[cursor:])
    assert b''.join(restored) == old_bytes
    inverse_pin = jwrite('COMPLETE_BO​​OTQ64_WHOLE_FILE_BYTE_INVERSE.json'.replace('\u200b',''), {
        'schema':'COMPLETE_BQ64_SINGLE_FORTRAN_WHOLE_BYTE_INVERSE_V1',
        'original_source_pin':old_pin,'candidate_source_pin':candidate_pin,
        'blocks':blocks,'whole_inverse_observed':True,
        'restored_size_bytes':len(old_bytes),'restored_sha256':old_pin['sha256'],
        'public_BUILD_whole_bytes_sha256':hashlib.sha256(public_build.encode()).hexdigest(),
        'public_BUILD_whole_bytes_identical':True,
        'private_builder_inverse_to_entire_public_BUILD_observed':True,
        'private_builder_inverse_operations':['rename procedure','remove storage gate',
            'restore exactly LCMEQU(ipglobal,child)','restore exactly LCMEQU(input_flux,child)'],
        'old_BOOT64_whole_source_unchanged_pin':comparator_pin,
        'raw_record_clone_only_procedure_renamed':True,
        'raw_record_original_sha256':hashlib.sha256(region(comparator,
            '  logical function SAME_RECORD(', '  end function SAME_RECORD\n').encode()).hexdigest(),
        'control_exact_production_blocks':{
            'private_constants_sha256':hashlib.sha256(PRIVATE_CONSTANTS.encode()).hexdigest(),
            'storage_function_sha256':hashlib.sha256(BUDGET.encode()).hexdigest(),
            'entire_matcher_block_sha256':hashlib.sha256(helpers.encode()).hexdigest(),
            'all_three_blocks_whole_bytes_identical_in_control_and_candidate':True},
        'compiled':False,'numerical_executed':False})
    cases = [
        'valid entire compact/full tree model, all raw types 1..6, nested dirs/lists',
        'GLOBAL64 single raw word mismatch','SEED single raw word mismatch',
        'GLOBAL64 REAL64 signed-zero raw bit mismatch','extra GLOBAL64 record',
        'dirty expected GLOBAL64 placeholder','dirty expected SEED placeholder',
        'root extent mismatch','GLOBAL64 type mismatch','extra root key',
        'extra authority key','nested SEED does not graft','ROOT-QFISS64 final index raw bit mismatch',
        'null external GLOBAL64','null external SEED','null expected root',
        'both fixed graft slots visited exactly once',
        'shared MAX_NODES exact boundary and next node rejection',
        'previsited duplicate graft rejection','MAX_RECORD_WORDS 1-word over-limit',
        'MAX_RECORD_WORDS double-word over-limit','unsupported raw type rejection',
        'original cumulative depth 64 pass,65 reject through global prefix depth2',
        'compact typed 8+8 field layout with NUNKNO14 exact physical948232 bytes',
        'storage guard NUNKNO0/1/14/4420/4421/huge integer',
    ]
    plan_pin = jwrite('COMPOSED_MATCHER_CONTROL_PLAN.json', {
        'schema':'BQ64_COMPACT_EXPECTED_COMPOSED_SOURCE_CONTROL_PLAN_V1',
        'source_only':True,'compiled':False,'numerical_executed':False,
        'control_source_pin':control_pin,'candidate_source_pin':candidate_pin,
        'implemented_future_cases':cases,
        'additional_required_genuine_reader_controls':[
            'missing root key,missing authority key,missing each exact graft key',
            'actual graft directory empty while original input nonempty',
            'wrong graft item type or directory extent',
            'typed list extent,index,type,empty-item metadata mismatch',
            'stale BQ64-SRC-ST and stale BQ64-MAC-ST each refuse without deleting preexisting file',
            'all original direct entry read/view/copy/alias refusal controls retained',
            'original connected17 before/after full actual new runtime requalification',
            'original full50 exact17positive/33negative,completed BOOT full pair readback and sealed inputs'],
        'control_module_isolated_from_Dragon':True,
        'control_matcher_and_budget_are_exact_whole_block_copies_of_candidate':True,
        'fixture_does_not_recompute_physics_or_qualify_reader':True,
        'model_files_future_fresh_owned_cwd_only':['C64-EXP','C64-ACT'],
        'guards_unchanged':{'SELF_MiB':512,'child_MiB':512,'stage_s':600,'whole_s':1800,
            'fresh_GiB':2,'free_GiB':8,'history_GiB':96,'aux_MiB':128},
        'future_control_object_pin':None,'future_control_executable_pin':None,
        'future_control_actual_report_pin':None,'future_reader_qualification_pin':None})
    closure_pin = jwrite('ACTUAL_MODULE_AND_ORDERED70_SOURCE_CLOSURE.json', {
        'schema':'BQ64_SINGLE_PRIVATE_MODULE_ACTUAL_SOURCE_CLOSURE_V1',
        'candidate_module':'SPOR64_BOOTQ64_V2','new_private_symbols_only':True,
        'public_declarations_whole_lines_identical':True,
        'direct_uses':['GANLIB','SPOR64_RCONTRACT','SPOR64_BOOT_CONTEXT64_V2',
            'SPOR64_BOOT64','SPOR64_VERIFY','SPOR64_SCHEMA'],
        'original_source_pins':original_pins,'actual_complete70_report_pin':build_pin,
        'original_complete70_ordered_paths':ordered,'complete70_count':70,
        'original_object_count':66,'original_archive_count':4,
        'replacement_zero_based_complete70_index':40,
        'replacement_one_based_complete70_slot':41,
        'replacement_one_based_original_nine_core_slot':6,
        'old_object_path':ordered[40],'new_object_path':None,
        'new_object_pin':None,'new_Dragon_executable_pin':None,
        'new_runtime_build_report_pin':None,'remaining69_ordered_paths_retained':
            [p for index,p in enumerate(ordered) if index != 40],
        'new_compile_required_for_single_production_object':True,
        'whole70_Dragon_relink_required':True,
        'old_executable_does_not_qualify_new_reader':True})
    report_pin = jwrite('SOURCE_REVIEW_READY.json', {
        'schema':'BQ64_COMPACT_EXPECTED_COMPOSED_DRAFT_SOURCE_REVIEW_READY_V1',
        'source_only':True,'compiled':False,'numerical_executed':False,
        'files':[candidate_pin,control_pin,diff_pin,inverse_pin,plan_pin,closure_pin],
        'original_source_pins':original_pins,'complete_byte_inverse_pin':inverse_pin,
        'control_plan_pin':plan_pin,'module_and_ordered70_closure_pin':closure_pin,
        'conditional_forecast_MiB':{'solve_with_compact_readback':2032,'seal':1888},
        'compact_formula':'844632 + 7400*NUNKNO bytes','actual_fixed_nunkno_evidence':14,
        'compact_NUNKNO14_bytes':948232,'planned_compact_cap_MiB':32,
        'forecast_is_not_actual_resource_or_physics_qualification':True,
        'private_expected_builder_math_prefix_and_all_small_writers_preserved':True,
        'expected_MAC_full_tree_and_original_macro_comparator_preserved':True,
        'READ_stale_names_and_original_close_order_retained':True,
        'future_peer_source_review_pin':None,'future_object_pin':None,
        'future_executable_pin':None,'future_build_report_pin':None,
        'future_connected17_report_pin':None,'future_full50_report_pin':None,
        'AAA_qualified':False,'ABA_admitted':False,'goal_complete':False})
    # Re-observe the immutable inputs after all output publication.
    for pin in original_pins+[build_pin]:
        assert read_pin(pin['path'])[1] == pin
    print(json.dumps({'status':'SOURCE_ONLY_DRAFT_WRITTEN_UNCOMPILED_UNQUALIFIED',
        'source_review_ready_pin':report_pin,'candidate_source_pin':candidate_pin,
        'control_source_pin':control_pin,'complete_byte_inverse_pin':inverse_pin,
        'control_plan_pin':plan_pin,'module_and_ordered70_closure_pin':closure_pin,
        'inverse_block_count':len(blocks),'compiled':False,'numerical_executed':False},
        ensure_ascii=False))


if __name__ == '__main__':
    main()
