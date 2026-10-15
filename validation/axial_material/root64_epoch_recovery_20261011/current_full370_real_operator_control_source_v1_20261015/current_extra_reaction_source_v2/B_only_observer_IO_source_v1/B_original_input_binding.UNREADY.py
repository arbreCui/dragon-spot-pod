"""Source-only B input/IO role binding; no Source-generation or native main.

The formal first-A v10 seed retains the original B input rows. This binding
uses those rows explicitly, including the original B deck, rather than turning
an A observation into B. Actual admission/publication/build remain separate.
"""
from pathlib import Path
import os
import re
import stat

CASE_SHA='fbe3362e16c19c93b87de2ebf67607c5ac0a579daa1f7af5891aae9c9faa7b16'
SEED_SHA='9bf2ba8444f0fe17989db3a31c373730da1d73bae564405c6ca71f5bc6c6579b'
NATIVE_CWD='/Users/wen/spot/validation/artifacts/axial-material-inputs-20261003/A'
IO_COMPONENT='b63'
B_SCOPE='ONE_CURRENT_ORIGINAL_B_MATERIAL_CONSTRUCTION_FULL_CONTEXT_NOT_A_RELABELLING'
PRODUCT_NAMES=('m.xsm','u.asc','a.asc','t.asc')
PRODUCT_ROLES=('material.xsm','microlib.ascii','macro.ascii','metadata.ascii')
READONLY_CWD_ROLES=('AxMatTone.c2m','geometry.dat','rnr_cc.c2m','rnr_interpol.c2m')
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,
  joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,
  threads=1,children_at_once=1,retries=0)

def require(ok,message):
    if type(ok)is not bool or not ok:raise ValueError(message)

def identity(s):
    return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def current_only(p):
    """No read/hash of SCI, old products, or geometry; this is the current7 gate."""
    path=Path(p['path'])
    require(path.is_absolute()and not any(a.is_symlink()for a in(path,*path.parents)),
      'original input has no alias')
    s=path.lstat()
    require(stat.S_ISREG(s.st_mode)and s.st_nlink==1 and identity(s)==p['identity']and
      s.st_size==p['size_bytes'],'exact original current7 '+str(path))

def validate_B_binding(binding,seed,seed_pin):
    require(seed_pin['sha256']==SEED_SHA and seed['current_case_spec_pin']['sha256']==CASE_SHA,
      'exact v10 current case and retained original B seed authority')
    original=seed['states']['B']['native_stage_inputs']
    require(binding['schema']=='CURRENT_B_ORIGINAL_INPUT_AND_FRESH_IO_BINDING_V1'and
      binding['state']=='B'and binding['state_order']==['B']and
      binding['observation_scope']==B_SCOPE and
      binding['current_case_spec_pin']==seed['current_case_spec_pin']and
      binding['original_B_native_stage_inputs']==original and
      binding['original_B_material_deck_pin']==seed['states']['B']['original_material_deck_pin'],
      'explicit original B deck/case/complete seven rows, no A observation relabel')
    require([r['destination']for r in original]==[
      'material.x2m','AxMatTone.c2m','geometry.dat','rnr_cc.c2m','rnr_interpol.c2m',
      'DLIB_ACTUAL','DLIB8R1_370'],'every original B input role')
    require(binding['actual_native_cwd']==NATIVE_CWD and binding['io_component']==IO_COMPONENT and
      binding['actual_observation_directory']==str(Path(NATIVE_CWD)/IO_COMPONENT)and
      binding['actual_output_root']==binding['actual_observation_directory']and
      re.fullmatch('[A-Za-z0-9_-]{1,12}',binding['io_component'])is not None,
      'literal original library cwd and separate fresh short output directory')
    require(binding['material_product_names']==dict(zip(PRODUCT_ROLES,PRODUCT_NAMES))and
      all(len(IO_COMPONENT+'/'+name)<=12 for name in PRODUCT_NAMES),
      'all four complete products, each literal output path within12')
    consumed=binding['actual_consumed_readonly_cwd_role_pins']
    require(set(consumed)==set(READONLY_CWD_ROLES),'complete readonly procedure/geometry roles')
    byrole={r['destination']:r['input_pin']for r in original}
    for role,p in consumed.items():
        require(p['path']==str(Path(NATIVE_CWD)/role)and
          p['sha256']==byrole[role]['sha256']and p['size_bytes']==byrole[role]['size_bytes'],
          'A cwd input bytes equivalent to actual B role without equating identities '+role)
        current_only(p)
    libraries=binding['original_library_pins']
    require(libraries=={role:byrole[role]for role in('DLIB_ACTUAL','DLIB8R1_370')},
      'original existing SCI libraries, no copies or aliases')
    for row in original:current_only(row['input_pin'])
    require(binding['original_caps']==CAPS and binding['library_copy_created']is False and
      binding['historical_B_context_claimed']is False and binding['native_executed_by_author']is False,
      'original caps and honest Source/no-history route')
    return binding

def validate_manifest_B(manifest,binding,binding_pin):
    require(manifest['current_B_case_input_binding_pin']==binding_pin and
      manifest['state_order']==['B']and set(manifest['states'])=={'B'}and
      manifest['current_case_spec_pin']==binding['current_case_spec_pin']and
      manifest['observation_scope']==B_SCOPE,'same actual B input binding in complete observation')
    s=manifest['states']['B']
    require(s['current_B_case_input_binding_pin']==binding_pin and
      s['actual_native_cwd']==binding['actual_native_cwd']and
      s['actual_observation_directory']==binding['actual_observation_directory']and
      s['actual_material_deck_pin']==binding['derived_B_material_deck_pin']and
      s['original_B_material_deck_pin']==binding['original_B_material_deck_pin'],
      'actual B deck consumed in original library cwd, observer files in own directory')
    require(len(s['complete_context_pins'])==55 and len(s['complete_state_snapshot_inputs'])==8,
      'complete current B scope requires actual55events/8trees, never Source prediction')
    return s

def snapshot_old_cwd_current7():
    cwd=Path(NATIVE_CWD)
    require(not any(p.is_symlink()for p in(cwd,*cwd.parents)),'literal original input directory')
    result={}
    for path in cwd.iterdir():
        if path.name==IO_COMPONENT:continue
        s=path.lstat();require(not stat.S_ISLNK(s.st_mode),'no old cwd alias')
        result[path.name]=identity(s)
    return result

def recheck_old_cwd_current7(before):
    require(snapshot_old_cwd_current7()==before,
      'all old cwd objects unchanged/no new old-cwd cache or scratch write')

def require_output_reserve(prefix_roots,new_output_root,existing_joint_bytes,
                           context_tree_extraction_reserve_bytes,build_reserve_bytes=0):
    """Called before any business by Root's unchanged bounded Resource guard.

    423456221 is the observed old four-product stat total, not a maximum for
    new B. The separately admitted new-output bound must cover all products,
    contexts, eight full XSM trees and complete extraction/aggregation spools.
    """
    require(type(prefix_roots)is list and len(prefix_roots)>=62 and
      len(prefix_roots)==len(set(prefix_roots)),'complete latest prefix, no reset')
    roots=[Path(p)for p in prefix_roots];out=Path(new_output_root)
    require(out==Path(NATIVE_CWD)/IO_COMPONENT and out not in roots and
      not any(out.is_relative_to(p)or p.is_relative_to(out)for p in roots),
      'one explicit next B root, no overlap or hiding original SCI input directory')
    require(type(existing_joint_bytes)is int and existing_joint_bytes>=0 and
      type(context_tree_extraction_reserve_bytes)is int and context_tree_extraction_reserve_bytes>=584802416 and
      type(build_reserve_bytes)is int and build_reserve_bytes>=0,'strict prospective byte bounds')
    reserve=423456221+context_tree_extraction_reserve_bytes+build_reserve_bytes
    require(existing_joint_bytes+reserve<2*2**30,
      'pre-business refusal: complete four-product/context/tree/extraction/build reserve does not fit2GiB')
    return dict(prefix_roots=prefix_roots,joint_archive_roots=prefix_roots+[str(out)],
      B_output_root_index=len(prefix_roots)+1,minimum_complete_new_bytes=reserve,
      original_four_product_stat_bytes=423456221,
      original_A55context_8tree_stat_bytes=145938890,
      original_A_full_extraction_stat_bytes=438863526,
      independently_admitted_new_total_upper_bound_required=True)
