"""Finite independent v10 Source read/AST review. No candidate imports/compilation."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import resource
import time

ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';ART=ROOT/'validation/artifacts';OUT=Path(__file__).absolute().parent
H=REC/'storage_release_closed_v7_v8_project_pair_20261013/independent_postverify_20261013/verify_exact_two_postrelease_v2.py'
spec=importlib.util.spec_from_file_location('own_readonly_streaming_helpers',H);s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
V9=REC/'aaa_three_plane_streaming_pipeline_source_v9';V10=REC/'aaa_three_plane_streaming_pipeline_source_v10';START=time.monotonic()

def static(n,env):
    if isinstance(n,ast.Constant):return n.value
    if isinstance(n,ast.Name):return env[n.id]
    if isinstance(n,(ast.Tuple,ast.List)):return [static(v,env) for v in n.elts]
    if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Add):return static(n.left,env)+static(n.right,env)
    if isinstance(n,ast.Subscript):return static(n.value,env)[ast.literal_eval(n.slice)]
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('replace','rsplit'):
        value=static(n.func.value,env);s.check(isinstance(value,str) and not n.keywords,'restricted AST string method only')
        return getattr(value,n.func.attr)(*[static(a,env) for a in n.args])
    raise RuntimeError('unsupported static string AST '+type(n).__name__)

def decks(text):
    tree=ast.parse(text);main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    prefix=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='BOOT_PREFIX' for t in n.targets))
    env={'BOOT_PREFIX':ast.literal_eval(prefix)}
    for name in ('precheck','viewops'):
        assignment=next(n for n in ast.walk(main) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets));env[name]=static(assignment.value,env)
    result={};direct=[]
    for loop in ast.walk(main):
        if not isinstance(loop,ast.For) or not isinstance(loop.iter,ast.List) or not loop.iter.elts:continue
        item=loop.iter.elts[0]
        if not isinstance(item,ast.Tuple) or not isinstance(item.elts[0],ast.Constant) or item.elts[0].value not in ('view_missing_operand','pair_missing_rank'):continue
        rows=static(loop.iter,env)
        call=next(n for n in ast.walk(loop) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='storage_refuse')
        names=[n.id for n in loop.target.elts]
        for row in rows:
            scope=dict(env);scope.update(zip(names,row));label=scope['label']
            if label=='view_system_alias':direct.append(dict(case=label,expected_abort=scope['message'],CLE_deck_generated=False));continue
            result[label]=dict(deck=static(call.args[1],scope),expected_abort=static(call.args[2],scope))
    for call in ast.walk(main):
        if isinstance(call,ast.Call) and isinstance(call.func,ast.Name) and call.func.id=='refuse' and call.args and isinstance(call.args[0],ast.Constant) and str(call.args[0].value).startswith('lifecycle_'):
            result[call.args[0].value]=dict(deck=static(call.args[1],env),expected_abort=static(call.args[2],env))
    node=next(n for n in ast.walk(main) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='bootdeck' for t in n.targets))
    result['BOOT_positive']=dict(deck=static(node.value,env),expected_abort=None)
    return result,direct,env

def main():
    hfpin=dict(path=str(V10/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'),sha256='aa75076e2ff7819eb164cecfd927b9485559b2282b0f7ac5ea9c8a5d9ead6861',size_bytes=146046,identity=[16777229,50013648,33188,1,146046,1791870345211171880,1791870345211171880])
    cp=dict(path=str(REC/'ROOT_EXACT_ACTUAL_PIPELINE_V10_ARGV_20261013.json'),sha256='6114a646a30e3ec0599e96f631e8262a146ef360289ca78f24f927f878219c36',size_bytes=11660,identity=[16777229,50013649,33188,1,11660,1791870345212109800,1791870345212109800])
    hf=s.exact_json(hfpin);cli=s.exact_json(cp)
    s.check(hf['schema']=='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V10' and len(hf['dependencies'])==278 and hf['prepared_only'] is True and hf['actual_pipeline_executed'] is False and hf['old_frozen_Fortran_source_changed'] is False,'exact current Source-only278 HF')
    for row in [hf['host_source']]+hf['dependencies']:s.same(row)
    oldhf=s.exact_json(s.pin(V9/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'));newtable={r['path']:r for r in hf['dependencies']}
    s.check(len(oldhf['dependencies'])==257 and all(newtable.get(r['path'])==r for r in oldhf['dependencies']),'all original257 current dependency rows byte/identity preserved')
    oldpin=oldhf['host_source'];s.same(oldpin);old=Path(oldpin['path']).read_text();new=Path(hf['host_source']['path']).read_text()
    changes=[("-20261012-v9'","-20261012-v10'"),('COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V9','COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V10'),("viewops='PROJECT AX AXTRACK AXSYSTEM AXMACRO GRCON SYS1 SYS2 SYS3 TRACK_f1 TRACK_f2 TRACK_f3'","viewops='PROJECT AX AXTRACK AXSYSTEM AXMACRO GRCON\\n  SYS1 SYS2 SYS3 TRACK_f1 TRACK_f2 TRACK_f3'")]
    inverse=new
    for before,after in changes:s.check(old.count(before)==1 and inverse.count(after)==1,'exact one approved literal change');inverse=inverse.replace(after,before)
    s.check(inverse==old,'whole host byte inverse equal only three declared literals')
    helpers=[]
    for name in ('actual_inputs_and_readback.py','mutate_owned_control.f90','direct_alias_entry_controls.f90'):
        a=s.pin(V9/name);b=s.pin(V10/name);s.same(a);s.same(b);s.check(Path(a['path']).read_bytes()==Path(b['path']).read_bytes(),'complete helper bytes unchanged');helpers.append(dict(name=name,old_pin=a,new_pin=b))
    argv=cli['argv'];s.check(argv[:11]==['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1','/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B'] and argv[11]==hf['host_source']['path'],'original env/python/single-thread exact owning host')
    for role,row in cli['mandatory_external_bindings'].items():
        s.same(row)
        s.check(argv[argv.index('--'+role+'-summary')+1]==row['path'] and argv[argv.index('--'+role+'-sha256')+1]==row['sha256'] and json.loads(argv[argv.index('--'+role+'-seven-id')+1])==row['identity'],'every external CLI binding full PF Python integers')
    s.check(cli['mandatory_external_bindings']['host-freeze']==hfpin and len(cli['mandatory_external_bindings'])==7 and cli['actual_pipeline_executed'] is False and cli['physics_qualification'] is False,'all seven external roles current and no runtime qualification')
    oldcards,olddirect,oldenv=decks(old);newcards,newdirect,newenv=decks(new);s.check(set(oldcards)==set(newcards) and len(newcards)==8 and olddirect==newdirect and len(newdirect)==1,'all8 CLE cards and unchanged direct alias family')
    s.check(oldenv['BOOT_PREFIX']==newenv['BOOT_PREFIX'] and newenv['BOOT_PREFIX'].count('MICROLIB2 := DELETE: MICROLIB2 ;')==3 and newenv['BOOT_PREFIX'].count('MACRO0 TRACK := DELETE: MACRO0 TRACK ;')==3,'all six writable owned copy DELETE lifecycle statements exact')
    tokens=lambda text:re.findall(r"'[^']*'|\"[^\"]*\"|[^\s]+",text)
    cards=[];author=s.exact_json(hf['all_generated_view_deck_token_and_CLE_card_source_review_pin']);authortable={r['case']:r for r in author['cards']}
    for label in sorted(newcards):
        a=oldcards[label];b=newcards[label];mx=max(map(len,b['deck'].splitlines()))
        s.check(tokens(a['deck'])==tokens(b['deck']) and a['expected_abort']==b['expected_abort'] and mx<=120,'all full CLE deck tokens/oracles same; every card<=120')
        s.check(authortable[label]['new_complete_CLE_deck']==b['deck'] and authortable[label]['expected_abort']==b['expected_abort'],'independent reconstruction matches exact published full deck')
        cards.append(dict(case=label,old_max_columns=max(map(len,a['deck'].splitlines())),new_max_columns=mx,full_deck_sha256=hashlib.sha256(b['deck'].encode()).hexdigest(),all_tokens_equal=True,expected_abort=b['expected_abort']))
    s.check(oldcards['BOOT_positive']==newcards['BOOT_positive'] and len(newenv['viewops'].split())==12 and len(newenv['viewops'].rsplit(' ',1)[0].split())==11,'positive BOOT literal unchanged; with two LHS outputs exact14 or13 operands')
    for literal in ["len(runner.records)!=50","sum(x['status']=='PASS'for x in runner.records)!=17","sum(x['status']=='FAILED'for x in runner.records)!=33","len(cases)!=33","len(new_storage_cases)!=17","5.00000000E-08","20971764748","64*MI","2*2**30","512","600"]:s.check(literal in new,'original stages/oracles/numeric/resource constraints retained '+literal)
    # Complete current catalog and Common binding protect all physical/Fortran
    # prerequisites; preserve duplicate rows, verify every original fullpin row.
    catalog=s.exact_json(hf['current_mount_full_identity_catalog_pin']);binding=s.exact_json(hf['current_Common_binding_pin'])
    s.check(len(catalog['rows'])==3040 and len(binding['fixed_current_pins'])==2012,'all catalog and Common row counts')
    for row in [r['current_pin'] for r in catalog['rows']]+binding['fixed_current_pins']:s.same(row)
    compiler=[r for r in hf['dependencies'] if r['path']=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15']
    s.check(len(compiler)==1 and compiler[0]['identity'][3]==2,'actual fixed immutable compiler nlink2 preserved')
    out=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v10';s.check(not os.path.lexists(out),'v10 fresh output namespace not yet business executed')
    for row in s.VERIFIED.values():s.check(s.seven(Path(row['path']).lstat())==row['identity'],'all verified current pins remained exact at end')
    result=dict(schema='INDEPENDENT_FINITE_V10_CLE_CARD_WHITESPACE_CURRENT_SOURCE_REVIEW_V1',status='SOURCE_ONLY_FULL_EOF_WHOLE_BYTE_INVERSE_ALL8_CLE_CARDS_ORACLES_PASS',host_freeze_pin=hfpin,external_CLI_pin=cp,host_pin=hf['host_source'],dependencies_count=278,all_original257_dependencies_exactly_retained=True,whole_byte_inverse_only_three_literals=True,three_helpers_full_byte_equality=helpers,eight_independently_AST_reconstructed_CLE_decks=cards,direct_alias_family_unchanged=newdirect,all_six_DELETE_lifecycle_statements_unchanged=True,all3040_current_catalog_rows_and2012_Common_rows_fullEOF_verified=True,original_math_Fortran_native70_compiler_inputs_caps_and50_17_33_oracles_unchanged=True,output_namespace_currently_absent=True,candidate_imported=False,compiler_CLE_or_numerical_business_executed=False,online_BOOT_or_AAA_or_ABA_qualified=False,goal_complete=False,full_EOF_unique_verified_files=len(s.VERIFIED),full_EOF_unique_verified_bytes=sum(r['size_bytes'] for r in s.VERIFIED.values()),checks=s.CHECKS,elapsed_seconds=time.monotonic()-START,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,reviewer_Source_pin=s.pin(Path(__file__).absolute()))
    path=OUT/'INDEPENDENT_FINITE_SOURCE_REVIEW.json';raw=(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode();fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status=result['status'],review_pin=s.pin(path),full_EOF_files=result['full_EOF_unique_verified_files'],full_EOF_bytes=result['full_EOF_unique_verified_bytes'],checks=result['checks'],CLE_cards=8,candidate_imported=False,compiler_or_numerical_business_executed=False)))

if __name__=='__main__':main()
