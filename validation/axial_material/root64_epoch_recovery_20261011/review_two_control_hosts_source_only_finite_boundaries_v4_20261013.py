#!/usr/bin/env python3
"""Extract pure Host functions with AST; no Host import, compiler, or child."""
import ast
import base64
import difflib
import hashlib
import json
import os
from pathlib import Path
import stat
from types import SimpleNamespace

REC=Path(__file__).resolve().parent


def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pin(p):
    p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        assert ids(os.fstat(fd))==ids(s);parts=[]
        while True:
            b=os.read(fd,1048576)
            if not b:break
            parts.append(b)
        b=b''.join(parts);assert len(b)==s.st_size and ids(os.fstat(fd))==ids(s)
    finally:os.close(fd)
    assert ids(p.lstat())==ids(s)
    return b,dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))


def put(p,data):
    raw=(json.dumps(data,indent=2)+'\n').encode();fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    try:assert os.write(fd,raw)==len(raw);os.fsync(fd)
    finally:os.close(fd)
    return pin(p)[1]


def main():
    results=[]
    for kind,stem in [('model','bq64_private_GANLIB_model_control_host'),('public','public_read_compact_bq_admission_control_host')]:
        folder=REC/(stem+'_source_v4_20261013');source=folder/('run_guarded_'+kind+'_controls.py')
        data,pf=pin(source);text=data.decode();tree=ast.parse(text)
        functions=['safe_repr','FirstFailure','make_commands','model_oracle','public_oracle']
        selected=[node for node in tree.body if isinstance(node,(ast.FunctionDef,ast.ClassDef))and node.name in functions]
        assert {node.name for node in selected}==set(functions)
        ns={'Path':Path,'stat':stat,'KIND':kind,'OUT':Path('/SOURCE_ONLY_FAKE_OUTPUT_NOT_CREATED')}
        exec(compile(ast.Module(body=selected,type_ignores=[]),'<finite-source-functions-only>','exec'),ns)
        checks=[]
        def check(value,label):assert value,label;checks.append(label)
        def refuses(call,label):
            try:call()
            except RuntimeError:checks.append(label);return
            raise AssertionError('expected finite RuntimeError: '+label)
        first=ns['FirstFailure']();primary=RuntimeError('SOURCE ONLY FIRST MARKER');secondary=OSError('SOURCE ONLY SECONDARY')
        try:raise primary
        except RuntimeError as error:tb=error.__traceback__;first.capture(error,'initial')
        first.capture(secondary,'late')
        check(first.error is primary and first.traceback is tb and len(first.secondary)==1,'first object and original traceback retained')
        try:first.reraise()
        except RuntimeError as error:
            chain=[];node=error.__traceback__
            while node is not None:chain.append(node);node=node.tb_next
            check(error is primary and tb in chain,'reraise same original object includes original traceback')
        late=ns['FirstFailure']()
        try:raise secondary
        except OSError as error:late.capture(error,'first publication error')
        check(late.error is secondary,'first publication-only error is original object')
        plan_fixture_path=REC/(stem+'_source_v3_20261013')/'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json'
        plan_bytes,plan_fixture_pin=pin(plan_fixture_path);plan=json.loads(plan_bytes)
        compiler=plan['original_compiler_pin']['path'];new=list(plan['original_ordered70_paths']);new[40]=plan['new_build_expected_BOOTQ_object_path']
        compile_cmd=[compiler,*plan['original_compile_flags'],*plan['new_build_compile_include_arguments'],
          '-J'+plan['new_build_expected_build_directory'],'-c',plan['production_Source_pin']['path'],'-o',plan['new_build_expected_BOOTQ_object_path']]
        link_cmd=[compiler,'-O2','-ffp-contract=off',*new,'-o',plan['new_build_expected_Dragon_path']]
        base={'records':[{'command':compile_cmd},{'command':link_cmd}],'actual_complete70_link_inputs':new}
        common=SimpleNamespace(FLAGS=plan['original_compile_flags'])
        compiled,linked,exe,core=ns['make_commands'](common,base,plan,plan['control_Source_pin'])
        check(linked[-6:-2]==plan['original_four_archive_paths'],'four archives order exact')
        check((len(core)==0)if kind=='model'else(len(core)==9 and core[5]==new[40]),'private no core;public new core6 only')
        bad=json.loads(json.dumps(base));bad['records'][0]['command'][-3]='/FAKE_WRONG_PRODUCTION_SOURCE'
        refuses(lambda:ns['make_commands'](common,bad,plan,plan['control_Source_pin']),'wrong genuine production compile Source rejects')
        bad=json.loads(json.dumps(base));bad['actual_complete70_link_inputs'][40]=plan['original_nine_core_paths'][5]
        refuses(lambda:ns['make_commands'](common,bad,plan,plan['control_Source_pin']),'old BOOTQ input40 rejects')
        # All following observations are labelled in-memory fixture data. They
        # are not files, watchdogs, real control outputs, or qualification pins.
        fixture={'rows':[]}
        ns['log_rows']=lambda*c:(fixture['rows'],{'fixture_only':True})
        cp={'identity':[0,0,stat.S_IFREG|0o644,1,948232,0,0],'size_bytes':948232,'sha256':'0'*64}
        ap={'identity':[0,0,stat.S_IFREG|0o644,1,949232,0,0],'size_bytes':949232,'sha256':'1'*64}
        dummy=SimpleNamespace(pin=lambda p:cp if p.name=='C64-EXP'else ap)
        fixture['rows']=[dict(status='ACTUAL_COMPACT_GANLIB_MODEL_CONTROLS_ONLY',assertions=36,
          physics_qualified=False,reader_qualified=False,AAA_qualified=False)]
        observed=ns['model_oracle'](dummy,None,None,Path('/FAKE_FIXTURE_NOT_CREATED'))
        check(observed['actual_model_assertions']==36,'private36 finite oracle accepts')
        for bad_value in (True,35,37,None):
            fixture['rows'][0]['assertions']=bad_value
            refuses(lambda:ns['model_oracle'](dummy,None,None,Path('/FAKE_FIXTURE_NOT_CREATED')),'private assertion boundary '+str(bad_value))
        fixture['rows'][0]['assertions']=36;cp['size_bytes']=948231
        refuses(lambda:ns['model_oracle'](dummy,None,None,Path('/FAKE_FIXTURE_NOT_CREATED')),'wrong physical expected byte count rejects')
        if kind=='public':
            for declared in plan['planned_run_phases']:
                row=dict(case=declared['case'],phase=declared['phase'],schema='GENUINE_PUBLIC_READ_COMPACT_BQ_ADMISSION_CONTROL_V1',
                  all_actual_assertions_completed=True,synthetic_fixture=True,private_matcher_used_as_assertion_oracle=False,
                  physics_qualified=False,reader_qualified=False,AAA_qualified=False,ABA_admitted=False)
                for key,value in declared.items():
                    if key.startswith('expected_'):row[key[9:]]=value
                fixture['rows']=[row];ns['public_oracle'](dummy,None,None,declared);checks.append('public exact '+declared['case']+'/'+declared['phase'])
                for key in ('actual_public_read_status','actual_control_public_read_calls','actual_baseline_public_read_calls'):
                    original=row[key];row[key]=True
                    refuses(lambda:ns['public_oracle'](dummy,None,None,declared),'public non-integer '+key);row[key]=original
        # Whole v1-to-v3 inverse reconstructs the earlier retained Source bytes.
        oldbytes,oldpf=pin(REC/(stem+'_source_v3_20261013')/source.name)
        a,b=oldbytes.splitlines(True),data.splitlines(True);ao,bo=[0],[0]
        for line in a:ao.append(ao[-1]+len(line))
        for line in b:bo.append(bo[-1]+len(line))
        blocks=[]
        for op,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
            if op=='equal':continue
            blocks.append(dict(candidate_offset=bo[k],candidate_end=bo[l],original_bytes_base64=base64.b64encode(oldbytes[ao[i]:ao[j]]).decode(),candidate_piece_sha256=hashlib.sha256(data[bo[k]:bo[l]]).hexdigest()))
        cursor=0;restored=[]
        for block in blocks:restored.extend([data[cursor:block['candidate_offset']],base64.b64decode(block['original_bytes_base64'])]);cursor=block['candidate_end']
        restored.append(data[cursor:]);check(b''.join(restored)==oldbytes,'whole inverse returns retained v3 Source')
        inversepf=put(folder/'AUTHOR_EXTRACTED_COMPLETE_CONTROL_HOST_V3_TO_V4_WHOLE_BYTE_INVERSE.json',dict(schema='CONTROL_HOST_V3_TO_V4_COMPLETE_WHOLE_BYTE_INVERSE_V1',original_source_pin=oldpf,new_source_pin=pf,blocks=blocks,whole_byte_inverse_observed=True,restored_sha256=oldpf['sha256'],Host_imported=False,compiler_executed=False,numerical_executed=False))
        reportpf=put(folder/'AUTHOR_EXTRACTED_FUNCTIONS_FINITE_SOURCE_BOUNDARY_REVIEW.json',dict(schema='COMPACT_BQ_CONTROL_HOST_SOURCE_ONLY_FINITE_FUNCTION_REVIEW_V1',status='PASS_SOURCE_ONLY_FINITE_BOUNDARIES_UNIMPORTED_UNQUALIFIED',source_pin=pf,passed_case_count=len(checks),checks=checks,whole_byte_inverse_pin=inversepf,historical_v3_in_memory_fixture_plan_pin=plan_fixture_pin,current_v4_build_plan_not_selected_by_this_finite_fixture=True,in_memory_fake_observations_not_actual_controls=True,Host_imported=False,Host_main_executed=False,compiler_executed=False,numerical_executed=False,future_actual_control_report_pin=None))
        assert pin(source)[1]==pf
        results.append(dict(kind=kind,source_pin=pf,finite_review_pin=reportpf,whole_byte_inverse_pin=inversepf,passed_case_count=len(checks)))
    print(json.dumps({'status':'PASS_TWO_HOST_SOURCE_ONLY_FINITE_FUNCTION_BOUNDARIES','packages':results,'Host_imported':False,'Host_main_executed':False,'compiler_executed':False,'numerical_executed':False}))


if __name__=='__main__':main()
