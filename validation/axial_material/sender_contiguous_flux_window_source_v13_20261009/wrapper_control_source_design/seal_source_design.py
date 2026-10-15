"""STDlib source reads, reference-name-only extraction and control contract.
Does not import business, compile Fortran, execute a control, or write project.
"""
from pathlib import Path
import hashlib,json,re

D=Path('/private/tmp/axmat_v13_flusp64_window_wrapper_control_source_draft_20261009')
SRC=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-rank1-factor-cache-build-admission-20261007/FLU2DR64.f')
DRIVER=D/'flusp64_window_observer_controls.UNREADY.f90'
SPOF=Path('/Users/wen/spot/validation/artifacts/axial-material-AAA-white-trace-cold-control-paths-20261004/build/SPOF64.f')
ROOT=Path('/Users/wen/spot')

def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    a=p.stat();b=p.read_bytes();z=p.stat()
    fields=['st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns']
    assert [getattr(a,x) for x in fields]==[getattr(z,x) for x in fields]
    return {'path':str(p),'sha256':sha(b),'size_bytes':len(b),'identity':{x:getattr(z,x) for x in fields}}
def save(name,data):
    p=D/name
    with p.open('x') as f: json.dump(data,f,indent=2,allow_nan=False);f.write('\n')
    return pin(p)

body=SRC.read_bytes();mark=b'      SUBROUTINE FLUSP64('
assert body.count(mark)==1
start=body.index(mark);original=body[start:]
assert original.rstrip().endswith(b'      END')
reference=original.replace(b'SUBROUTINE FLUSP64(',b'SUBROUTINE FLUSP64_REFERENCE(',1)
assert reference.replace(b'SUBROUTINE FLUSP64_REFERENCE(',b'SUBROUTINE FLUSP64(',1)==original
with (D/'FLUSP64_REFERENCE.f').open('xb') as f:f.write(reference)
text=DRIVER.read_text()
assert max(map(len,text.splitlines()))<=132
observer_body=re.search(r'  subroutine observe\((.*?)  end subroutine',text,re.S).group(1)
assert 'transfer(fun' not in observer_body.lower()
assert 'observed_source=source' in observer_body
assert 'fun(i,j)=transfer(bits,0.0d0)' in observer_body

# Planned mode observations only; no test has run.
cases=[
 ('all',1,370,0,[370,370],['production NUN1800/NGRP370 all groups; ILEAK=0; system IDs reverse energy-group indices']),
 ('suffix',2,8,3,[6,6],['groups 3..8; nonzero B1; skip KEY/MAT/IMERG; duplicate KEY accumulation']),
 ('interior',3,8,0,[4,4],['groups 2..5; unchanged columns before AND after window']),
 ('scalar_first',4,8,3,[1,1],['group 1; B2(4) raw negative zero; correction skipped']),
 ('scalar_last',5,8,3,[1,1],['group 8; negative nonzero B2; one-column direct sequence association']),
 ('scalar_one',6,1,0,[1,1],['NGRP=1 boundary']),
 ('sparse',7,8,3,[3,3],['groups 1,3,8; nonzero B1; original F2 fallback']),
 ('empty_ileak0',8,8,0,[0,0],['zero active; no observer; full caller unchanged']),
 ('empty_ileak3',9,8,3,[0,0],['zero active; nonzero B2; return before correction/observer']),
 ('transition',10,8,3,[6,1,3,0],['same live arrays: suffix -> scalar -> sparse -> empty; no reset between steps'])]
negative=[('unsupported_reference_active',11,8,2,8,'reference'),
 ('unsupported_candidate_active',12,8,2,8,'candidate'),
 ('unsupported_reference_empty',13,8,2,0,'reference'),
 ('unsupported_candidate_empty',14,8,2,0,'candidate')]
allcases=[];rawtotal=0
for name,cid,ng,ileak,act,coverage in cases:
    files=[];steps=[]
    nun=1800 if name=='all' else 12
    for step,nact in enumerate(act,1):
        route=0 if nact==0 else (2 if name=='sparse' or name=='transition' and step==3 else 1)
        size=8*(56+(4+8*nun)*ng+(2+nun)*nact)
        for who in ['input','reference','candidate']:
            files.append({'name':f'{name}.s{step}.{who}.bin','size_bytes':size,'who':who})
            rawtotal+=size
        steps.append({'step':step,'active_groups':nact,'expected_route':route,'each_raw_size_bytes':size,
                      'reference_observer_calls':int(nact>0),'candidate_observer_calls':int(nact>0)})
    allcases.append({'name':name,'args':[name],'case_id':cid,'expected_returncode':0,
      'ngrp':ng,'nun':nun,'nreg':7,'nmat':4,'nmerg':3,'ileak':ileak,'steps':steps,'coverage':coverage,
      'raw_files':files,'manifest_lines':len(act),'negative':False,
      'strict_case_namespace':['execute.log','execute.watchdog.json','wrapper_manifest.jsonl']+[x['name'] for x in files]})
for name,cid,ng,ileak,nact,target in negative:
    size=8*(56+100*ng+14*nact);rawtotal+=size
    f={'name':f'{name}.s1.input.bin','size_bytes':size,'who':'input'}
    allcases.append({'name':name,'args':[name],'case_id':cid,'expected_returncode':1,
      'expected_message':'FLUSP64: UNSUPPORTED LEAKAGE MODEL.','message_stream':'actual stdout/stderr retained; require exact message in combined text',
      'ngrp':ng,'nun':12,'nreg':7,'nmat':4,'nmerg':3,'ileak':ileak,'negative':True,'target':target,
      'target_wrapper_calls':1,'observer_calls':0,'raw_files':[f],'manifest_lines':0,'manifest_size_bytes':0,
      'strict_case_namespace':['execute.log','execute.watchdog.json','wrapper_manifest.jsonl',f['name']]})
assert len(allcases)==14
counts={'positive_cases':10,'negative_cases':4,'positive_steps':22,
 'positive_reference_wrapper_calls':22,'positive_candidate_wrapper_calls':22,
 'negative_reference_wrapper_calls':2,'negative_candidate_wrapper_calls':2,
 'positive_reference_observer_calls':17,'positive_candidate_observer_calls':17,'negative_observer_calls':0,
 'wrapper_calls_total':48,'observer_calls_total':34,'positive_raw_files':66,'negative_raw_files':4,
 'raw_files_total':70,'raw_bytes_total':rawtotal,'manifest_files':14}
contract={
 'schema':'AXMAT_FLUSP64_WINDOW_WRAPPER_CONTROL_CONTRACT_V1','status':'SOURCE_ONLY_UNREADY',
 'runtime_auditor_interface':'audit_sender_controls(controls_root, contract) -> dict',
 'source_driver':pin(DRIVER),'reference_unit':pin(D/'FLUSP64_REFERENCE.f'),
 'candidate_unit':'link actual fullsender object; do not add or replace candidate wrapper source',
 'compiler_or_control_execution_performed':False,'actual_outputs':None,
 'original_68_controls_must_remain_unmodified':True,'all_four_negative_modes_required':True,
 'cases':allcases,'planned_counts_not_actual':counts,
 'raw_schema':{
   'schema':'AXMAT_FLUSP64_WINDOW_OBSERVER_RAW_V1','byte_order':'little','word_type':'signed int64',
   'magic_hex':'41584657494E3133','version':1,'exact_eof_required':True,
   'header_words':['magic','version','case_id','who:0input/1reference/2candidate','step','NUN','NGRP','NREG','NMAT','NMERG','NGEFF',
     'observer_calls','ILEAK','expected_route:0empty/1direct/2fallback','caller_FUN_first_LOC','observer_FUNKNO_first_LOC','expected_direct','observed_direct'],
   'body_in_order':[
     {'field':'NPSYS','words':'NGRP','kind':'int32 value sign-extended to int64'},
     {'field':'MAT','words':'NREG','kind':'int32 value sign-extended to int64'},
     {'field':'KEYFLX','words':'NREG','kind':'int32 value sign-extended to int64'},
     {'field':'IMERG','words':'NMAT','kind':'int32 value sign-extended to int64'},
     {'field':'VOL','words':'NREG','kind':'raw float32 bits as signed int32 sign-extended to int64'},
     {'field':'B2','words':4,'kind':'raw float32 bits as signed int32 sign-extended to int64'},
     {'field':'DIFHET','words':'NMERG*NGRP','kind':'raw float32 bits as signed int32 sign-extended to int64; column major'},
     {'field':'TITR','bytes':72,'kind':'exact blank-padded ASCII'},
     {'field':'all_caller_FLUX','words':'8*NUN*NGRP','kind':'raw float64 int64 bits; Fortran column major; planes 2/8/7 are old/source/output'},
     {'field':'energy_group_map','words':'NGEFF','kind':'int64'},
     {'field':'LCM_read_system_IDs','words':'NGEFF','kind':'int64'},
     {'field':'S2_observed_source','words':'NUN*NGEFF','kind':'raw float64 int64 bits; column major'}],
   'generic_bytes_formula':'8*(18+NGRP+2*NREG+NMAT+NREG+4+NMERG*NGRP+8*NUN*NGRP+2*NGEFF+NUN*NGEFF)+72',
   'small_fixture_formula':'8*(56+100*NGRP+14*NGEFF)',
   'all_production_shape_formula':'8*(56+14404*370+1802*370)=47970208 bytes per raw file; 6 files',
   'input_address_fields':[0,0,0,0],
   'reference_address_rule':'active => both addresses positive and unequal, expected_direct=observed_direct=0; empty => all 0',
   'candidate_address_rule':'contiguous active => both addresses positive and equal, flags1; sparse => positive unequal flags0; empty => all0',
   'comparisons':'all body fields reference==candidate exact bytes; inputs unchanged except active plane7 output; S2 independently computed original B1 expression/order; output finite bit transform from source; no tolerance',
   'no_hidden_copy_credit':'LOC proves actual observer pointer relation only; F2 non-allocation requires fullsender source inverse, not measured RSS'},
 'fixture_model':{
   'MAT':[1,2,0,3,4,2,1],'KEYFLX':'[1,0,4,5,1,NUN,NUN-1]','IMERG':[1,0,2,3],
   'VOL':'float32 i/8, i=1..7','DIFHET':'float32 (-1)^(i+g)*(i/4+g/128), i=1..3',
   'FLUX':'float64 (-1)^(i+g+p)*(p+g/32+i/1024); raw -0 when mod(i+g+p,17)=0; 1<=p<=8',
   'NPSYS':'active IG receives NGRP+1-IG; inactive0',
   'B2':'all +0 except suffix/sparse/empty3/transition B2(4)=1.25; scalar_last=-0.75; scalar_first raw float32 -0',
   'S2':'ascending groups; copy SUN plane8, then original IR-ordered DBLE(DIFHET)*DBLE(B2)*FLUOLD plane2 subtraction; skip KEY0/MAT0/IMERG0',
   'output':'SPOF observer never reads initial FUN; mantissa/sign bitxor of S2 with (IG<<20)+row, exponent0x3ff; raw -0 when mod(row+column,11)=0',
   'readonly':'all other FLUX planes plus inactive plane7, NPSYS/MAT/KEY/IMERG/VOL/B2/DIFHET/TITR and GANLIB marker data unchanged'},
 'scope_limits':['Only observer-wrapper routing/alias/dataflow eligibility; no real SPOF/SPOT numerical result',
   'No runtime/compiler/fixture has run; planned counts and raw bytes are not measurements',
   'Original public ABI and production real GANLIB+real SPOF linkage remain unchanged',
   'Direct write can leave partial FUN on fatal SPOF failure; no resumed/reused failed state allowed',
   'Current production four callers have disjoint FLUX2/8/7; external aliased callers are not newly admitted',
   'Original512MiB/4200/43200/thread/cap/zero-retry unchanged; no RSS benefit or native/AAA/ABA credit']}
contract_pin=save('CONTROL_CONTRACT.json',contract)
evidence=[pin(p) for p in [SRC,SPOF,ROOT/'Ganlib/src/ganlib.f90',ROOT/'Ganlib/src/LCMAUX.f90',ROOT/'Ganlib/src/lcmmod.f90',ROOT/'Ganlib/src/xabort_c.c']]
assert 'exit(1)' in (ROOT/'Ganlib/src/xabort_c.c').read_text()
proof=save('SOURCE_ONLY_INVERSE_AND_EVIDENCE.json',{'schema':'AXMAT_FLUSP64_REFERENCE_SOURCE_NAME_ONLY_INVERSE_V1',
 'status':'PASS_SOURCE_ONLY','original_fullsender':evidence[0],'original_wrapper_sha256':sha(original),
 'original_wrapper_line_range':[1611,1666],'reference_sha256':sha(reference),'changes':[{'old':'SUBROUTINE FLUSP64(','new':'SUBROUTINE FLUSP64_REFERENCE('}],
 'whole_reference_inverse_byteexact':True,'source_evidence':evidence,'candidate_fullsender_sha256':None,'compiler_control_or_business_execution':False})
report=save('REPORT.json',{'schema':'AXMAT_V13_SENDER_WINDOW_CONTROL_SOURCE_DESIGN_REVIEW_V1','status':'PASS_SOURCE_DESIGN_ONLY_UNREADY',
 'contract':contract_pin,'inverse_proof':proof,'planned_counts_not_actual':counts,'driver':pin(DRIVER),
 'actual_compiler_or_control_exit':None,'actual_RSS':None,'business_run':False,'project_written':False,
 'numerical_science_credit':False,'native_AAA_ABA_credit':False,'safety_conditions':contract['scope_limits']})
with (D/'REPORT.txt').open('x') as f:
 f.write('V13 sender窗口控制源码草稿已封存；未编译、未运行。\n')
 f.write('固定10正例+4真GANLIB不支持泄漏负例；44正例wrapper调用、4负例调用、34 observer调用。\n')
 f.write(f'计划70 raw文件、{rawtotal}字节；每个完整8-plane输入/输出及S2/群映射均逐位审。\n')
 f.write('observer用LOC核对真实输出地址：原reference非direct，新连续窗口direct，稀疏非direct；空群不调用。\n')
 f.write('真实GANLIB对象；仅SPOF64观察器替代，不读取初始FUN，不赋予真实数学/512MiB/RSS/native资格。\n')
 f.write('reference仅routine名字更改，完整逆向回原sender；candidate应直接链接Root真实fullsender对象。\n')
 f.write('未来真正SPOF失败可留下direct窗口部分输出，禁止复用失败状态；原68控制全部保留。\n')
print(json.dumps({'status':report['sha256'],'contract_sha256':contract_pin['sha256'],'driver_sha256':pin(DRIVER)['sha256'],'counts':counts},ensure_ascii=False))
