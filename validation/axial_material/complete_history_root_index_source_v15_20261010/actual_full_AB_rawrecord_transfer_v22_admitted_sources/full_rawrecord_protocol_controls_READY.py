"""UNREADY SOURCE protocol controls. No reviewed API action at import.

Future Root alone runs this as one serial child under the unchanged genuine
512 MiB supervisor. Fixtures are small software records, never actual material
or transport truth. This driver reads no actual macro/XSM numeric payload.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import struct
import sys
import time

SOURCE_STATUS='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'
ACTUAL_PROTOCOL_QUALIFICATION_SHA256=None
CAPS={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_archive_bytes':2*2**30,'history_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children_at_once':1,'retries':0}
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
FALSE={'actual_material_payload_parsed':False,'scientific_accuracy_qualified':False,'physical_neutron_balance_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'original_XSM_memory_bits_verified':False,'reaction_multiplicity_verified':False,'coupled_370group_reference_qualified':False,'native_transport_executed':False,'whole_combined_build_or_INPUT_qualified':False}

def require(value,message):
    if type(value)is not bool or not value:raise ValueError(message)

def pin(path):
    path=Path(path);s=path.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    require(path.is_file()and not path.is_symlink()and s.st_nlink==1,'ordinary protocol SOURCE/META required')
    with path.open('rb')as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    t=path.lstat();after=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
    require(before==after,'protocol SOURCE fullEOF identity changed')
    return {'path':str(path),'sha256':sha,'size_bytes':s.st_size,'identity':before}

def load_wrapper(path,sha):
    before=pin(path);require(before['sha256']==sha,'future fixed READY wrapper required')
    spec=importlib.util.spec_from_file_location('axmat_rawrecord_protocol_fixed_wrapper',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    require(pin(path)==before,'protocol wrapper SOURCE changed')
    return module,before

def tiny_fixture():
    # All original LCM record kinds and nested key types, signed zeros,
    # ordinary finite REAL32 rounding, REAL64, characters with raw padding,
    # three raw Legendre sparse moments, two independent toy fissile columns.
    # Toy dimensions intentionally do not claim the actual370/8/32 contract.
    chunks=[]
    def named(level,name,kind,count,payload=''):
        chunks.append(f'-> {level} 12 {kind} {count} <-\n{name}\n'+payload)
    def indexed(level,index,kind,count,payload=''):
        chunks.append(f'-> {level} 0 {kind} {count} <- {index:08d}\n'+payload)
    named(1,'SIGNATURE',3,3,'4 4 4\nL_MACROLIB   \n')
    state=[2,2,3,2]+[0]*36
    named(1,'STATE-VECTOR',1,40,' '.join(map(str,state))+'\n')
    named(1,'ENERGY',2,3,'1.0E+7 1.0E+3 0.0\n')
    named(1,'FISSIONINDEX',1,4,'1 0 0 2\n')
    named(1,'ROUND32',2,6,'-0.0 0.0 1.00000001 -1.00000001 1e-300 -1e-300\n')
    named(1,'ROUND64',4,4,'-0.0 0.0 1.0000000000000002 -1.0000000000000002\n')
    named(1,'EXACTINT',1,4,'-9223372036854775808 9007199254740993 0 9223372036854775807\n')
    named(1,'RAWCHAR',3,2,'4 4\nAB      \n')
    named(1,'EMPTY99',99,0)
    named(1,'GROUP',10,2)
    for g in (1,2):
        indexed(2,g,0,-1)
        named(3,'NTOT0',2,2,'1.0 2.0\n')
        named(3,'NUSIGF',2,4,'-0.0 0.0 0.1 0.2\n')
        named(3,'CHI',2,4,'0.2 0.3 0.4 0.1\n')
        named(3,'EXTRA_RXN',2,2,'0.01 0.02\n')
        for moment in (0,1,2):
            s=f'{moment:02d}'
            named(3,'NJJS'+s,1,2,'0 1\n')
            named(3,'IJJS'+s,1,2,'0 2\n')
            named(3,'IPOS'+s,1,2,'0 2\n')
            named(3,'SCAT'+s,2,3,'-0.0 -0.25 77.0\n')
        chunks.append('-> -2 0 0 0 <-\n')
    chunks.append('-> -1 0 0 0 <-\n')
    return ''.join(chunks).encode('ascii')

def all_reader_values_equal(first,second):
    require(type(first)is dict and type(second)is dict,'both complete toy record dictionaries required')
    require(list(first)==list(second),'all original toy key insertion order required')
    for key,(kind,value)in first.items():
        kind2,value2=second[key]
        require(type(key)is tuple and [type(x)for x in key]==[type(x)for x in next(k for k in second if k==key)],'all toy nested key types')
        require(type(kind)is type(kind2)is int and kind==kind2 and type(value)is type(value2),'all toy record kinds and value types')
        if kind in (2,4):
            require(len(value)==len(value2),'complete toy real count')
            for a,b in zip(value,value2):
                require(type(a)is type(b)is float and math.isfinite(a)and math.isfinite(b),'all toy float types and finite')
                require(struct.pack('<d',a)==struct.pack('<d',b),'all parser64 bits including signed zeros')
                if kind==2:require(struct.pack('<f',a)==struct.pack('<f',b),'all raw-kind REAL32 bits including signed zeros')
        else:require(value==value2,'all toy integer/string/directory/list values')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ready-wrapper',required=True);parser.add_argument('--ready-wrapper-sha256',required=True)
    parser.add_argument('--binding',required=True);parser.add_argument('--binding-sha256',required=True)
    parser.add_argument('--output-dir',required=True);parser.add_argument('--expected-parent-pid',type=int,required=True)
    args=parser.parse_args();started=time.monotonic()
    require(SOURCE_STATUS=='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'and ACTUAL_PROTOCOL_QUALIFICATION_SHA256 is None,'UNREADY controls cannot run; actual control success remains unknown')
    require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in THREAD_KEYS),'original one-thread unprofiled protocol environment')
    require(type(args.expected_parent_pid)is int and os.getppid()==args.expected_parent_pid,'actual genuine parent PID required')
    w,wrapper_pin=load_wrapper(Path(args.ready_wrapper),args.ready_wrapper_sha256)
    binding_pin=pin(Path(args.binding));require(binding_pin['sha256']==args.binding_sha256==w.ACTUAL_ROOT_BINDING_RECEIPT_SHA256,'actual immutable Root binding required')
    b=w.strict_json(Path(args.binding).read_bytes());require(b['schema']=='ROOT_ACTUAL_CURRENT150_AB_FULL_RAWRECORD_TRANSFER_SOURCE_BINDING_V1'and b['source_only']is True and b['scientific_qualification_created']is False and b['original_caps']==CAPS,'protocol actual SOURCE binding/original caps required')
    require(w.SOURCE_STATUS=='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'and w.SOURCE_QUALIFICATION_SHA256==b['source_qualification_sha256']and all(value is None for value in(w.ACTUAL_TRANSFER_QUALIFICATION_SHA256,w.REACTION_MULTIPLICITY_QUALIFICATION_SHA256,w.ACTUAL_SCIENTIFIC_REFERENCE_SHA256)),'original wrapper SOURCE only; no fabricated future success pins')
    w.exact_pin(b['python']);require(Path(sys.executable).resolve()==Path(b['python']['path']).resolve(),'original Python for default reader protocol')
    nr=w.load_reader('native_records',b['readers']['native_records']);sr=w.load_reader('stream_records',b['readers']['stream_records'])
    out=Path(args.output_dir);require(out.is_absolute()and out.is_relative_to(w.ART)and out!=w.ART and not os.path.lexists(out),'one-use strict ART protocol output required')
    w.ordinary(out.parent,directory=True);out.mkdir()
    controls=[]
    def accepted(name,value):
        require(value,name);controls.append({'name':name,'actual_control_passed':True})
    raw=tiny_fixture();raw_path=out/'complete_tiny_protocol_fixture.ascii'
    with raw_path.open('xb')as f:f.write(raw)
    inv=out/'complete_tiny_raw_header_spans.jsonl';counts=w.raw_inventory(raw_path,inv)
    first=nr.decode(raw);second,stats=sr.decode_stream(io.BytesIO(raw))
    all_reader_values_equal(first,second)
    accepted('both original default readers retain every toy record and all key/type/value/bits/order',stats['all_records_validated']==stats['retained_records']==len(first)==len(second)==counts['records'])
    index=out/'complete_tiny_typed_index.jsonl';payload=out/'complete_tiny_typed_payload.bin'
    w.spool_first_reader(first,inv,index,payload)
    result=w.compare_second_reader(second,stats,index,payload,counts['records'])
    accepted('full typed/raw-span payload exact comparison',result['all_paths_types_order_values_floatbits_equal']is True)
    round_value=first[('ROUND32',)][1][2]
    accepted('finite nonexact REAL32 rounding and underflow are accepted with exact parser64 bits; full signed wide integers retained',struct.pack('<f',round_value)==struct.pack('<f',1.0)and struct.pack('<d',round_value)!=struct.pack('<d',1.0)and struct.pack('<f',first[('ROUND32',)][1][4])==struct.pack('<f',0.0)and first[('ROUND32',)][1][4]!=0.0 and first[('EXACTINT',)][1]==(-9223372036854775808,9007199254740993,0,9223372036854775807))
    summary=w.contract_inventory(first,out/'complete_tiny_required_field_gap_inventory.jsonl',out/'complete_tiny_sparse_spans.jsonl')
    accepted('actual missing fields/dimensions remain full scientific gaps without zero replacement',summary['gap_counts'].get('missing_real_record_no_substitution',0)>0 and summary['gap_counts'].get('actual_STATE_VECTOR_dims_not_370_8_3_32')==1 and summary['future_solver_scientific_input_admitted']is False)
    accepted('original unknown extra reaction and all3 toy raw moments retained',all(('GROUP',g,'EXTRA_RXN')in first and all(('GROUP',g,'SCAT'+f'{m:02d}')in first for m in (0,1,2))for g in (1,2)))
    # All actual error observations are retained individually. No filtering or
    # expected rejection can substitute for the complete positive full payload.
    rejects=[]
    def both_reject(name,malformed):
        details=[]
        for label,call in (('native_default',lambda:nr.decode(malformed)),('stream_default',lambda:sr.decode_stream(io.BytesIO(malformed)))):
            try:call()
            except (ValueError,OverflowError)as error:details.append({'reader':label,'error_type':type(error).__name__,'error':str(error)})
            else:raise ValueError('malformed fixture unexpectedly accepted: '+name+' '+label)
        rejects.append({'name':name,'both_full_readers_rejected':True,'actual_observed_errors':details})
    both_reject('duplicate full record key',raw.replace(b'-> -1 0 0 0 <-\n',b'-> 1 12 1 1 <-\nSTATE-VECTOR\n1\n-> -1 0 0 0 <-\n'))
    both_reject('truncated final numeric payload',raw.replace(b'1.00000001 -1.00000001',b'1.00000001'))
    both_reject('nonfinite real payload',raw.replace(b'1.00000001',b'INF',1))
    both_reject('missing terminal root close',raw[:-len(b'-> -1 0 0 0 <-\n')])
    both_reject('wrong raw character width',raw.replace(b'RAWCHAR\n4 4\n',b'RAWCHAR\n4 3\n'))
    both_reject('truncated raw character payload',raw.replace(b'RAWCHAR\n4 4\nAB      \n',b'RAWCHAR\n4 4\nAB\n'))
    both_reject('truncated malformed full header',raw.replace(b'-> 1 12 4 4 <-\nROUND64',b'-> 1 12 4\nROUND64'))
    overflow=nr.decode(raw.replace(b'1.00000001',b'1e40',1))
    try:list(w.payload_chunks(2,overflow[('ROUND32',)][1]))
    except (ValueError,OverflowError)as error:rejects.append({'name':'REAL32 overflow or nonfinite resulting cast rejected, finite ordinary rounding allowed','observed_rejection':True,'error_type':type(error).__name__,'error':str(error)})
    else:raise ValueError('REAL32 overflow unexpectedly accepted')
    permuted=dict(reversed(list(second.items())))
    try:w.compare_second_reader(permuted,stats,index,payload,counts['records'])
    except ValueError as error:rejects.append({'name':'key order mutation rejected','observed_rejection':True,'error':str(error)})
    else:raise ValueError('key order mutation unexpectedly accepted')
    flipped=dict(second);kind,values=flipped[('ROUND64',)];flipped[('ROUND64',)]=(kind,(0.0,)+values[1:])
    try:w.compare_second_reader(flipped,stats,index,payload,counts['records'])
    except ValueError as error:rejects.append({'name':'signed zero parser/REAL64 bit mutation rejected','observed_rejection':True,'error':str(error)})
    else:raise ValueError('signed zero mutation unexpectedly accepted')
    require(len(controls)==5 and len(rejects)==10,'complete5 positive and10 negative controls required')
    del first,second,overflow,permuted,flipped,nr,sr
    require(pin(args.ready_wrapper)==wrapper_pin and pin(args.binding)==binding_pin,'protocol full source/binding EOF changed')
    elapsed=time.monotonic()-started;require(math.isfinite(elapsed)and 0<=elapsed<CAPS['stage_seconds'],'original600 stage cap')
    report={'schema':'CURRENT150_AB_ACTUAL_COMPLETE_RAWRECORD_PROTOCOL_CONTROLS_V1','status':'ACTUAL_FULL_SMALL_PROTOCOL_CONTROLS_ONLY_EXTERNAL_GENUINE_ROOT_CLOSURE_REQUIRED','actual_child_PID':os.getpid(),'actual_parent_PID':os.getppid(),'child_seconds':elapsed,'wrapper':wrapper_pin,'binding':binding_pin,'complete_positive_controls':controls,'complete_negative_controls':rejects,'positive_count':len(controls),'negative_count':len(rejects),'full_tiny_raw_inventory':counts,'full_raw_and_typed_control_files':{p.name:pin(p)for p in out.iterdir()if p.is_file()},'genuine_supervisor_watch_verified_here':False,'root_true_exit0_closed_required':True,'original_caps':CAPS,**FALSE}
    w.write_meta(out/'ACTUAL_PROTOCOL_REPORT.json',report)
    print(json.dumps({'status':report['status'],'report':pin(out/'ACTUAL_PROTOCOL_REPORT.json'),'positive_count':5,'negative_count':10,**FALSE},allow_nan=False),flush=True)

if __name__=='__main__':main()
