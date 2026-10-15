#!/usr/bin/env python3
"""Current complete byte/actual argument inventory; no Fortran execution."""
from pathlib import Path
import runpy,re,json,ast,hashlib
ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
OUT=REC/'online_boot_native64_source_v1'
base=runpy.run_path(str(REC/'global_native64_dependency_source_v2/driver_source/generate_global_native64_dependency_source.py'))
read_pin=base['read_pin'];fresh_json=base['fresh_json']
def args(s,name,call=False):
    # Exact text argument inventory, not a Fortran parser or compilation.
    hits=list(re.finditer(r'\b'+('call' if call else 'subroutine')+r'\s+'+re.escape(name)+r'\s*\(',s,re.I))
    out=[]
    for h in hits:
        start=h.end();depth=1;end=start
        while depth:
            ch=s[end];depth+=(ch=='(')-(ch==')');end+=1
        v=s[start:end-1].replace('&','').replace('\n',' ')
        parts=[];d=0;begin=0
        for i,c in enumerate(v):
            d+=(c=='(')-(c==')')
            if c==',' and d==0:parts.append(v[begin:i].strip());begin=i+1
        parts.append(v[begin:].strip());out.append(parts)
    return out
def inverse(current,proof,original):
    v=current
    for s in reversed(proof['steps']):
        assert hashlib.sha256(v).hexdigest()==s['after_sha256']
        a=s['old'].encode();b=s['new'].encode()
        if s['mode']=='whole_identifier_rename':
            pattern=rb'\b'+re.escape(b)+rb'\b';assert len(re.findall(pattern,v))==s['count']
            v=re.sub(pattern,a,v)
        else:
            n=s['byte_offset'];assert v[n:n+len(b)]==b
            v=v[:n]+a+v[n+len(b):]
        assert hashlib.sha256(v).hexdigest()==s['before_sha256']
    assert v==original
def main():
    binding=json.loads(read_pin(OUT/'CURRENT_COMPLETE_ONLINE_BOOT_SOURCE_BINDING.json')[0])
    for p in binding['source_pins']+binding['complete_dependencies_after']:
        assert read_pin(Path(p['path']))[1]==p
    b=read_pin(OUT/'SPOR64_BOOTB64.f90')[0];c=read_pin(OUT/'SPOR64_BOOTC64.f90')[0]
    f=read_pin(OUT/'SPOBOOTRUN64.f90')[0];h=read_pin(OUT/'SPOR64_BOOT_BIND64.f90')[0]
    proof=json.loads(read_pin(OUT/'COMPLETE_ONLINE_BOOT_WHOLE_BYTE_INVERSE_PROOFS.json')[0])
    inverse(b,proof['kernel'],read_pin(ROOT/'src/SPOR64_B2B.f90')[0])
    inverse(c,proof['publisher'],read_pin(ROOT/'src/SPOR64_B2C.f90')[0])
    records=[]
    for name,declaration,caller,callee_name,count in [
        ('SPOR64_BOOTB64_INGRESS',b,f,'SPOR64_BOOTB64_INGRESS',46),
        ('SPOR64_BOOTC64_PUBLISH',c,b,'SPOR64_BOOTC64_PUBLISH',18),
        ('SPOR64_BOOT_BIND64_READ',h,b,'SPOR64_BOOT_BIND64_READ',19),
        ('FLU2DR64_CORE',read_pin(ROOT/'src/SPOR64_A9.f90')[0],b,'FLU2DR64_CORE',31),
        ('SPOR64_B2I_SEAL_BOOTSTRAP',read_pin(ROOT/'src/SPOR64_B2I.f90')[0],f,'SPOR64_B2I_SEAL_BOOTSTRAP',7)]:
        d=args(declaration.decode(),name);a=args(caller.decode(),callee_name,True)
        assert len(d)==1 and len(a)==1,(name,len(d),len(a))
        assert len(d[0])==len(a[0])==count,(name,len(d[0]),len(a[0]),count)
        records.append({'procedure':name,'argument_count':count,'full_definition_arguments':d[0],
          'full_actual_call_arguments':a[0],'actual_definition_and_call_count_equal':True})
    extra=[ROOT/'src'/n for n in ['SPOR64_A8_ACA.f90','SPOMOC.f90',
        'ASM.f','ASMDRV.f','MCGASM.f','SPOPOD.f90','SPOT_LEAKAGE.f90']]
    pins=[read_pin(p)[1] for p in extra]
    for p in pins:assert read_pin(Path(p['path']))[1]==p
    ast.parse(read_pin(Path(__file__))[0])
    fresh_json(OUT/'ACTUAL_COMPLETE_BYTE_AND_ABI_AUDIT.json',{
        'source_pins_actual_current_stable':True,'whole_kernel_publisher_inverse_actual_verified':True,
        'actual_argument_records':records,'additional_complete_current_source_dependencies':pins,
        'scope':'Actual Python current EOF/7ID/SHA and exact textual argument/inverse audit. No Fortran parser/compile/numerical or physical qualification.',
        'external_current_fullfile_and_tool_pin_admission_required':True,
        'compiler_run':False,'numeric_run':False})
    print(json.dumps({'status':'ACTUAL_FULL_BYTE_AND_ABI_AUDIT_EXIT0','actual_argument_counts':
        {r['procedure']:r['argument_count'] for r in records},'additional_whole_current_dependencies':len(pins),
        'Fortran_executed':False,'numeric_executed':False}))
if __name__=='__main__':main()
