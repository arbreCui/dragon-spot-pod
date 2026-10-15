#!/usr/bin/env python3
"""Bind a real completed new build, then freeze the reviewed fresh17 Host."""
import argparse,ast,hashlib,json,os,stat
from pathlib import Path

R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
HERE=Path(__file__).resolve().parent
HF=HERE/'COMPLETE_FRESH17_NEW_BOOTQ_HOST_SOURCE_FREEZE.json'
CLI=HERE/'ROOT_REVIEWABLE_EXACT_FRESH17_ARGV.json'

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(path,wanted=None,body=False):
    path=Path(path);before=identity(path.lstat());assert stat.S_ISREG(before[2])
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        assert identity(os.fstat(fd))==before
        h=hashlib.sha256();parts=[]if body else None
        while True:
            chunk=os.read(fd,2**20)
            if not chunk:break
            h.update(chunk)
            if body:parts.append(chunk)
        assert identity(os.fstat(fd))==before
    finally:os.close(fd)
    assert identity(path.lstat())==before
    row=dict(path=str(path),sha256=h.hexdigest(),size_bytes=before[4],identity=before)
    if wanted is not None:assert row==wanted,str(path)
    return row,b''.join(parts)if body else None
def load(p,wanted=None):
    pin,raw=read(p,wanted,True);return json.loads(raw),pin
def write(p,data):
    with p.open('x',encoding='utf-8')as f:
        json.dump(data,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def unique(rows):
    table={}
    for row in rows:
        if row['path']in table:assert table[row['path']]==row
        table[row['path']]=row
    return list(table.values())

def main():
    p=argparse.ArgumentParser(allow_abbrev=False)
    for s in ('summary','sha256','seven-id'):p.add_argument('--new-build70-'+s,required=True)
    a=p.parse_args()
    assert not HF.exists()and not CLI.exists()
    pbuild,raw=read(a.new_build70_summary,body=True)
    assert pbuild['sha256']==a.new_build70_sha256 and pbuild['identity']==json.loads(a.new_build70_seven_id)
    build=json.loads(raw)
    assert build['schema']=='ACTUAL_BQ64_COMPACT_EXPECTED_COMPLETE70_BUILD_ONLY_V1'
    assert build['status']=='ACTUAL_ONE_BOOTQ_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'
    assert build['failure']is None and build['after_check_error']is None and build['Dragon_linked']is True
    assert build['final_report_resource_check_passed']is True and len(build['records'])==2
    assert build['replacement_zero_based_complete70_input_index']==40
    parent,parent_pin=load(REC/'aaa_three_plane_streaming_pipeline_source_v14/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')
    old_cli,_=load(REC/'ROOT_EXACT_ACTUAL_PIPELINE_V14_ARGV_20261013.json')
    old17,pold17=load(old_cli['mandatory_external_bindings']['seventeen']['path'],old_cli['mandatory_external_bindings']['seventeen'])
    host,raw=read(HERE/'run_fresh_connected17.py',body=True)
    assert host['sha256']=='c68980d2079817b72cf578ded142841d0bedf8389e4773bc2ae8bf920e75ba69'
    tree=ast.parse(raw);compile(tree,host['path'],'exec')
    node=next(n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='OUT'for t in n.targets))
    out=R/ast.literal_eval(node.value.right);assert not out.exists()and not out.is_symlink()
    review_dir=REC/'independent_bq64_build_v4_fresh17_v2_post_curated66_Source_review_20261013'
    review,review_pin=load(review_dir/'FRESH17_REVIEW.json');tools,tools_pin=load(review_dir/'TRUE_TOOL_RETURNS.json')
    assert review['status']=='PASS_FRESH17_V2_POST_CURATED66_COMMON_OUTPUT_ONLY_SOURCE_REVIEW' and review['failure'] is None
    assert review['current_host_pin']==host
    post,post_pin=load(REC/'post_curated66_current_catalog_common_source_v2_20261013/COMPLETE_POST_CURATED66_CURRENT_CATALOG_BINDING_COMMON_SOURCE_FREEZE.json')
    assert post['schema']=='COMPLETE_POST_CURATED66_CURRENT_CATALOG_BINDING_COMMON_SOURCE_ONLY_FREEZE_V1'
    assert post['source_only'] is True and post['compiler_executed'] is False and post['numerical_executed'] is False
    actualtools,actualtools_pin=load(REC/'ROOT_ACTUAL_COMPACT_BQ_BUILD_V4_TRUE_TOOL_RETURNS_20261013.json')
    terminal=actualtools['actual_terminal_return']
    assert type(terminal['exit_code']) is int and terminal['exit_code']==0 and terminal.get('session_id') is None
    post_review_dir=REC/'independent_bq64_compact_build_v4_actual_postverify_20261013'
    actualpost,actualpost_pin=load(post_review_dir/'REVIEW.json')
    actualposttools,actualposttools_pin=load(post_review_dir/'TRUE_TOOL_RETURNS.json')
    assert actualpost.get('failure') is None and actualpost['status'].startswith('PASS')
    closed=actualposttools['actual_postverification_return']
    assert type(closed['exit_code']) is int and closed['exit_code']==0 and closed.get('session_id') is None
    buildhf=build['actual_host_Source_freeze_pin'];newsf=build['actual_new_Source_freeze_pin']
    rows=unique(parent['dependencies']+[parent_pin,parent['host_source'],host,pbuild,pold17,buildhf,newsf,review_pin,tools_pin]+
      build['fixed_current_pins']+build['output_pins']+[post_pin,actualtools_pin,actualpost_pin,actualposttools_pin]+post['files']+post['original_source_metadata_pins']+[read(p)[0]for p in sorted(HERE.iterdir())if p.is_file()])
    for row in rows:read(row['path'],row)
    freeze=dict(schema='COMPLETE_BQ64_COMPACT_EXPECTED_CONNECTED17_HOST_SOURCE_ONLY_FREEZE_V1',
      compiler_executed=False,controls_executed=False,Host_imported_or_executed=False,
      host_source=host,dependencies=rows,selected_original17_report_pin=pold17,
      selected_actual_new_build70_report_pin=pbuild,selected_new_build_Host_freeze_pin=buildhf,
      selected_new_Fortran_Source_freeze_pin=newsf,independent_Host_Source_review_pin=review_pin,
      selected_postrelease_catalog_binding_Source_freeze_pin=post_pin,
      actual_new_build_true_tool_return_pin=actualtools_pin,independent_actual_build_postverification_pin=actualpost_pin,independent_actual_build_postverification_true_tool_pin=actualposttools_pin,
      independent_Host_Source_true_tool_returns_pin=tools_pin,planned_output_root=str(out),
      original_17_names_oracles_and_current_factory_Source_unchanged=True,
      future_actual_control_object_pin=None,future_actual_control_executable_pin=None,
      future_actual_control_report_pin=None,production_reader_admitted=False,AAA_qualified=False,ABA_admitted=False)
    write(HF,freeze);phf=read(HF)[0]
    argv=['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1',
      'OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1',
      '/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',host['path']]
    for name,pin in [('build70',pbuild),('original17',pold17),('host-freeze',phf)]:
        argv+=['--'+name+'-summary',pin['path'],'--'+name+'-sha256',pin['sha256'],
               '--'+name+'-seven-id',json.dumps(pin['identity'],separators=(',',':'))]
    write(CLI,dict(schema='ROOT_REVIEWABLE_EXACT_FRESH17_NEW_BOOTQ_ARGV_V1',argv=argv,
      mandatory_external_bindings=dict(build70=pbuild,original17=pold17,host_freeze=phf),
      compiler_executed=False,controls_executed=False,requires_host_process_metadata_access=True))
    print(json.dumps(dict(status='FRESH17_SOURCE_ONLY_HF_AND_ARGV_BOUND_TO_REAL_NEW_BUILD_WRITTEN',
      host_freeze_pin=phf,argv_pin=read(CLI)[0],dependencies=len(rows),compiler_executed=False,controls_executed=False)))

if __name__=='__main__':main()
