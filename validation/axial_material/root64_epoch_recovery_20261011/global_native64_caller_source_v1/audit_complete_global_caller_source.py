#!/usr/bin/env python3
"""Complete EOF/whole-byte/ABI static Source audit. No Fortran execution."""
from pathlib import Path
import ast,hashlib,json,re,runpy
HERE=Path(__file__).resolve().parent
REC=HERE.parent
base=runpy.run_path(str(REC/'global_native64_dependency_source_v2/driver_source/generate_global_native64_dependency_source.py'))
read_pin=base['read_pin'];fresh_json=base['fresh_json']

def fixed_statements(raw):
    statements=[];current=''
    for line in raw.decode().splitlines():
        if not line or line[0] in '*cC!':continue
        if len(line)>5 and line[5] not in ' 0':current+=line[6:].strip()
        else:
            if current:statements.append(current)
            current=line[6:].strip()
    if current:statements.append(current)
    return statements

def free_join(raw):
    return ' '.join(x.split('!')[0].strip().replace('&','') for x in raw.decode().splitlines())

def args_from(text,prefix):
    assert text.upper().startswith(prefix.upper())
    body=text[text.index('(')+1:];depth=0;last=0;args=[]
    for i,c in enumerate(body):
        if c=='(':depth+=1
        elif c==')':
            if depth==0:
                args.append(body[last:i].strip().upper());return args
            depth-=1
        elif c==',' and depth==0:
            args.append(body[last:i].strip().upper());last=i+1
    raise AssertionError('unclosed statement')

def find_stmt(stmts,prefix):
    found=[x for x in stmts if x.upper().startswith(prefix.upper())]
    assert len(found)==1,(prefix,len(found))
    return found[0]

def main():
    manifest=json.loads(read_pin(HERE/'CURRENT_GLOBAL_CALLER_SOURCE_BINDING_AND_RUNTIME_SCOPE.json')[0])
    proofs=json.loads(read_pin(HERE/'COMPLETE_GLOBAL_CALLER_EXACT_BYTE_INVERSE_PROOFS.json')[0])
    names={'FLU':'FLUGLOBAL64.f','DRV':'FLUDRVG64.f','GPI':'FLUGPG64.f','API':'SPOT_GLOBAL_CALLER_API.f90','carriers':'SPOT_GLOBAL_CALLER_CARRIERS.f90'}
    sources={k:read_pin(HERE/n) for k,n in names.items()}
    assert {k:v[1] for k,v in sources.items()}==manifest['source_pins']
    bases={'FLU':'ORIGINAL_COMPLETE_FLU.f','DRV':'ORIGINAL_COMPLETE_FLUDRV.f','GPI':'ORIGINAL_COMPLETE_FLUGPI.f','API':'ORIGINAL_COMPLETE_REVIEWED_CALLER_API.f90'}
    inverse=[]
    for k,n in bases.items():
        p=proofs['proofs'][k];original=read_pin(HERE/n)[0];candidate=sources[k][0]
        assert hashlib.sha256(original).hexdigest()==p['basis_sha256']
        assert hashlib.sha256(candidate).hexdigest()==p['candidate_sha256']
        current=original
        for s in p['steps']:
            assert hashlib.sha256(current).hexdigest()==s['before_sha256']
            old=s['old'].encode();new=s['new'].encode()
            if s['mode']=='whole_identifier_rename':
                pattern=rb'\b'+re.escape(old)+rb'\b'
                assert len(re.findall(pattern,current))==s['count']
                current=re.sub(pattern,new,current)
            else:
                offset=s['byte_offset'];assert current[offset:offset+len(old)]==old
                current=current[:offset]+new+current[offset+len(old):]
            assert hashlib.sha256(current).hexdigest()==s['after_sha256']
        assert current==candidate
        for s in reversed(p['steps']):
            old=s['old'].encode();new=s['new'].encode()
            if s['mode']=='whole_identifier_rename':
                pattern=rb'\b'+re.escape(new)+rb'\b'
                assert len(re.findall(pattern,current))==s['count']
                current=re.sub(pattern,old,current)
            else:
                offset=s['byte_offset'];assert current[offset:offset+len(new)]==new
                current=current[:offset]+old+current[offset+len(new):]
        assert current==original
        if k!='API':
            a=fixed_statements(original);b=fixed_statements(candidate)
            assert [x for x in a if 'FORMAT(' in x]==[x for x in b if 'FORMAT(' in x]
        inverse.append({'source':k,'actual_exact_steps':len(p['steps']),'forward_equals_current_complete_Source':True,'reverse_equals_complete_original_Source':True,'original_FORMAT_statements_exact':k!='API'})
    protected=[read_pin(p['path'])[1] for p in manifest['original_and_v2_frozen_Source_before']]
    assert protected==manifest['original_and_v2_frozen_Source_before']==manifest['original_and_v2_frozen_Source_after']
    v2=REC/'global_native64_dependency_source_v2'
    v2freeze=json.loads(read_pin(v2/'COMPLETE_GLOBAL_NATIVE64_DEPENDENCY_SOURCE_FREEZE.json')[0])
    assert [read_pin(p['path'])[1] for p in v2freeze['fixed_regular_files']]==v2freeze['fixed_regular_files']
    flu=fixed_statements(sources['FLU'][0]);drv=fixed_statements(sources['DRV'][0]);gpi=fixed_statements(sources['GPI'][0])
    api=free_join(sources['API'][0]);v2api=free_join(read_pin(v2/'driver_source/SPOT_GLOBAL_NATIVE_DRIVER_API.f90')[0])
    def free_args(text,name):
        match=re.search(r'\bsubroutine\s+'+name+r'\s*\(',text,re.I);assert match
        return args_from(text[match.start():],'subroutine '+name)
    drv_decl=args_from(find_stmt(drv,'SUBROUTINE FLUDRVG64('),'SUBROUTINE FLUDRVG64(')
    assert drv_decl==free_args(api,'FLUDRVG64')
    actual_drv=args_from(find_stmt(flu,'CALL FLUDRVG64('),'CALL FLUDRVG64(')
    replacements={'IPRT':'IPRINT','OPTION':'COPTIO','LGCONT':'REC'}
    assert actual_drv==[replacements.get(x,x) for x in drv_decl]
    actual60=args_from(find_stmt(drv,'CALL SPOT_GLOBAL_NATIVE_DRIVER64('),'CALL SPOT_GLOBAL_NATIVE_DRIVER64(')
    expected60=free_args(v2api,'SPOT_GLOBAL_NATIVE_DRIVER64')
    changes={'NUNKNO':'NUN','NCPTL':'IFRITR','NCPTA':'IACITR','TERMINAL_VALID':'KERNEL_VALID','INITIAL_BUCKLING64':'INITIAL_B2_64','TERMINAL_BUCKLING64':'TB2_64','TERMINAL_DIFHET64':'TDIF64','TERMINAL_DHOM64':'TDHOM64','TERMINAL_GAMMA64':'TGAMMA64'}
    assert len(actual60)==len(expected60)==60
    assert actual60==[changes.get(x,x) for x in expected60]
    pubargs=args_from(find_stmt(flu,'CALL SPOR64_BOOT_GLOBAL_PUBLISH('),'CALL SPOR64_BOOT_GLOBAL_PUBLISH(')
    assert pubargs==['IPGLOBAL','IPFLUX','IPTRK','IPSYS','IPMACR','IPARCH_BOOT','IPRCON','TERMINAL_FLUX64','TERMINAL_SOURCE64','TERMINAL_KEFF64','TERMINAL_RESID64','TERMINAL_COUNTERS','TERMINAL_INNER_STATE','TERMINAL_VALID','IGLOBAL_STAT']
    text=sources['FLU'][0].decode();dt=sources['DRV'][0].decode();gt=sources['GPI'][0].decode();ht=sources['carriers'][0].decode()
    assert text.index('CALL FLUDRVG64')<text.index('*  VERIFY THE MODAL SPOD SYSTEM TAG.')<text.index('CALL SPOR64_BOOT_CANONICAL64_WRITE')<text.index('CALL SPOR64_BOOT_GLOBAL_PUBLISH')<text.index('DEALLOCATE(TERMINAL_FLUX64')
    assert 'USE SPOR64_BOOT_CANONICAL64_V2' in text
    assert dt.index("CALL LCMPUT(IPFLUX,'STATE-VECTOR'")<dt.index('TERMINAL_VALID=KERNEL_VALID')
    assert dt.count('TERMINAL_VALID=')==2 and 'TERMINAL_VALID=.TRUE.' not in dt
    assert 'INITIAL_B2_64=B2' in dt and 'KERNEL_VALID,INITIAL_B2_64,TB2_64' in dt
    assert 'IF(.NOT.LGCONT) INITIAL_FLUX64(IND,IGR)=1.0D0' in dt
    assert 'KEYFLX(:,1,1),INITIAL_FLUX64,SEED_KEFF64,WARM_OK)' in dt
    assert 'IF(LGCONT.AND.INITFL.NE.1)' in dt
    assert not any('LCMGET' in x and 'IPFLUX' in x and 'B2 ' in x for x in gpi)
    assert "CALL LCMGET(IPMACR,'B2  HETE',MACRO_B232)" in gt
    assert "CALL LCMGET(IPMACR,'B2  B1HOM',MACRO_B2S32)" in gt
    assert 'BSDIR(:3)=DBLE(MACRO_B232)' in gt and 'BSDIR(5)=DBLE(MACRO_B2S32)' in gt
    assert 'DOUBLE PRECISION B2(4)' in gt and 'DOUBLE PRECISION BSDIR(NSDIR)' in gt
    assert 'GLOBAL_EMPTY,IGLOBAL_LEN,GLOBAL_LCM)' in text
    assert 'LOGICAL TERMINAL_VALID,CANONICAL_OK,GLOBAL_EMPTY,GLOBAL_LCM' in text
    assert 'DO 10 I1=3,NENTRY' in text and 'IF(NENTRY.NE.7)' in text
    assert 'JENTRY(2).NE.0' in text and 'TRIM(GLOBAL_DIRECTORY).NE."/"' in text
    for i,k in enumerate(['IPMACR','IPTRK','IPSYS','IPARCH_BOOT','IPRCON'],3):assert f'C_ASSOCIATED({k},KENTRY({i}))' in text
    assert "call LCMGDL(native,ig,initial_flux64(:,ig))" in ht
    for x in ['FLUX64','FLUX','SOUR64','SOUR','SPOT-KEFF64','K-EFFECTIVE','KEYFLX','STATE-VECTOR','SPOT-B2H64','B2  B1HOM']:assert "'"+x+"'" in ht
    assert 'transfer(real(initial_flux64(i,ig),real32),0_int32)' in ht
    assert 'transfer(real(source(i),real32),0_int32)' in ht
    assert 'real(mirror' not in ht and 'dble(mirror' not in ht
    for p in [Path(__file__),HERE/'generate_complete_global_caller_source.py']:ast.parse(read_pin(p)[0])
    results={'schema':'COMPLETE_GLOBAL_CALLER_SOURCE_STATIC_AUDIT_V1','status':'ACTUAL_STDLIB_COMPLETE_EOF_FORWARD_REVERSE_AND_ABI_STATIC_AUDIT_CLOSED',
        'candidate_Source_pins':{k:v[1] for k,v in sources.items()},'inverse_audits':inverse,
        'original_and_frozen_v2_complete_Source_pins_unchanged_count':len(protected),
        'actual_lower_driver_argument_count':len(drv_decl),'actual_native_driver_argument_count':60,'actual_publisher_argument_count':15,
        'three_actual_argument_orders_equal_exact_API':True,'type4_native_flux_B2_ingress_and_type2_mirrors_static_checked':True,
        'cold_original_scalar1_other0_math':True,'initial_terminal_B2_actual_arrays_disjoint':True,
        'full_original_postchecks_before_real_canonical_before_real_publisher':True,
        'new_helpers_complete_full_group_length_type_finite_and_exact_mirror_checks':True,
        'Fortran_parse_compile_or_numerical_execution':False,
        'limitations':['This is Source static auditing, not Fortran parsing or execution.','Root must independently review all complete Sources and pin complete V2 canonical/publisher/context before actual bounded compile.','Dispatcher/production deck route still needs actual implementation and current binding.','Source coherence/typed return/publisher flags grant no whole-input/BOOT/17/physical/AAA/ABA qualification.'],
        'audit_Source_pin':read_pin(Path(__file__))[1]}
    fresh_json(HERE/'ACTUAL_COMPLETE_GLOBAL_CALLER_SOURCE_STATIC_AUDIT.json',results)
    print(json.dumps({'status':results['status'],'Source_pins':results['candidate_Source_pins'],'inverse_steps':[x['actual_exact_steps'] for x in inverse],'actual_lower_driver_argument_count':len(drv_decl),'native_driver_argument_count':60,'publisher_argument_count':15,'protected_count':len(protected),'report_pin':read_pin(HERE/'ACTUAL_COMPLETE_GLOBAL_CALLER_SOURCE_STATIC_AUDIT.json')[1],'Fortran_or_numeric_executed':False}))

if __name__=='__main__':main()
