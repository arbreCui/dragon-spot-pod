"""Prepare the original NJOY formatter component; no compile/native/SCI reads."""
import ast,hashlib,json,os,shlex,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent;REC=BASE.parent;OLD=REC/'saved_MT5_NX_raw32_yield_source_v2_20261014';ART=REC.parents[1]/'artifacts'
OUT=ART/'axial-material-original-a11-NX-formatter-component-20261014-v1'
PRODUCER=ART/'d4a-mt51-mf6-control-prepared-20261001/candidate'
FALSE=dict(business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def require(ok,msg):
 if type(ok)is not bool or not ok:raise RuntimeError(msg)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,compiler=False):
 p=Path(p);s=p.lstat();require(p.is_absolute()and not any(a.is_symlink()for a in(p,*p.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==(2 if compiler else 1),'exact role-specific regular file')
 with p.open('rb')as f:
  require(identity(os.fstat(f.fileno()))==identity(s),'opened7');h=hashlib.file_digest(f,'sha256').hexdigest();require(identity(os.fstat(f.fileno()))==identity(s),'EOF7')
 require(identity(p.lstat())==identity(s),'path7');return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=identity(s))
def read(p):
 p=pin(p);require(p['size_bytes']<8*2**20,'bounded metadata');d=json.loads(Path(p['path']).read_bytes());require(pin(p['path'])==p,'same metadata');return d,p
def write(p,v):
 with Path(p).open('x')as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def unique(rows):
 d={}
 for p in rows:
  if p['path']in d:require(d[p['path']]==p,'unique fullPF per path')
  d[p['path']]=p
 return list(d.values())
def main():
 require(not os.path.lexists(OUT)and not os.path.lexists(BASE/'PLAN.json')and not os.path.lexists(BASE/'SOURCE_REVIEW_READY.json'),'fresh component Source namespace')
 old,pold=read(OLD/'PLAN.json');prior,pprior=read(ART/'axial-material-saved-MT5-NX-raw32-producer-yield-diagnostic-20261014-v2/diagnostic/ACTUAL_SAVED_MT5_NX_RAW32_AND_YIELD_DIAGNOSTIC.json')
 require(len(old['complete_joint_roots'])==36 and prior['status']=='ORIGINAL_NX_PRODUCER_RAW32_MISMATCH'and len(prior['temperature_diagnostics'])==79,'real failed all79 binary-bypass comparison preserved')
 require(sum(r['original_NX_words']for r in prior['temperature_diagnostics'])==9294,'actual complete stored NX word domain')
 endf=PRODUCER/'source/src/endf.f90';locale=PRODUCER/'source/src/locale.f90';dragr=PRODUCER/'source/src/dragr.f90';flags=PRODUCER/'build/source/CMakeFiles/njoy.dir/flags.make'
 pe,pL,pD,pF=pin(endf),pin(locale),pin(dragr),pin(flags)
 require(pe['sha256']=='4095daab3c32330324897fb1fc6b350784f717a757795412a7505a188e109a30'and pL['sha256']=='a763f2618fe52ee2190adba1448506334f3475e4be090047a625a3ca85d530c5'and pD['sha256']=='047ed05e54c54aad2681ce1796bec72f47a0118a2d80295d0d9929e4e42381ac','actual producer exact original Source bytes')
 raw=endf.read_bytes();start=raw.index(b'   subroutine a11(');stop=raw.index(b'   end subroutine a11',start)+len(b'   end subroutine a11\n');a11=raw[start:stop]
 lraw=locale.read_bytes();require(b'kr=selected_real_kind(12,300)'in lraw,'exact original binary64 kind declaration')
 wrapper=Path(__file__).read_text().split('# NATIVE_WRAPPER\n',1)[1].split('# END_NATIVE_WRAPPER',1)[0];wrapper=wrapper[wrapper.index("WRAPPER = r'''")+len("WRAPPER = r'''"):wrapper.rindex("'''")]
 native=lraw+b'\n'+wrapper.encode()+a11+b'\nend program original_a11_component\n'
 with (BASE/'original_a11_component.f90').open('xb')as f:f.write(native)
 require((BASE/'original_a11_component.f90').read_bytes().count(a11)==1 and native.startswith(lraw),'whole original a11 and locale exactly included')
 flagtext=flags.read_text();fl=[line.split('=',1)[1].strip()for line in flagtext.splitlines()if line.startswith('Fortran_FLAGS =')];require(len(fl)==1,'one actual producer flag declaration')
 original_flags=shlex.split(fl[0]);require(original_flags[0]=='-J../fortran_modules'and not any('default-real'in s or 'fast-math'in s for s in original_flags),'actual original flags, no kind or arithmetic override')
 compiler=Path('/opt/homebrew/bin/gfortran').resolve();pc=pin(compiler,True)
 require(pc['path']=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'and pc['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492','one exact original compiler role, two links only here')
 library_inputs,pli=read(ART/'d4a-actual-temperature-library-run-20261003/inputs.json');library_prep,plp=read(ART/'d4a-actual-temperature-material-prepared-20261003/preparation.json');actual_sources={r['nuclide']:r for r in library_prep['sources']}
 evidence,pevidence=read(old['actual_GENDF_evidence_pin']['path']);require(pevidence==old['actual_GENDF_evidence_pin'],'actual saved GF11 proof')
 historical=[];meta=[pli,plp]
 for r in evidence['actual_extractions']:
  source=actual_sources[r['nuclide']];require(library_inputs[source['path']]==source['sha256'],'exact actual library producer component provenance');d=Path(source['path']).parent;folder=d.parent;tape=d/'tape24';require(str(folder/'groupr/tape27')==r['input_pin']['path'],'saved binary file belongs to exact library-selected producer stage')
  ih=d/'input_hashes.json';gr=folder/'groupr/receipt.json';dr=d/'receipt.json'
  if not ih.exists():ih=folder/'staged_inputs.json';gr=folder/'groupr_receipt.json';dr=folder/'dragr_receipt.json'
  hashes,pih=read(ih);g,pg=read(gr);dreceipt,pdr=read(dr);deckpin=pin(d/'input.in');deck=(d/'input.in').read_text()
  require(dreceipt['output_sha256']==source['sha256'],'actual DRAGR output receipt equals exact library input SHA');oldsha=hashes[str(tape)];require(not os.path.lexists(tape)and oldsha==g['output_sha256']and type(g['returncode'])is int and g['returncode']==0 and type(dreceipt['returncode'])is int and dreceipt['returncode']==0,'historical absent tape24 hash bound to actual GROUPR/DRAGR receipts')
  require('24 -25'in deck and '-25 0 0'in deck,'actual original ASCII moder then DRAGR input path')
  historical.append(dict(nuclide=r['nuclide'],actual_library_producer_component_path=source['path'],actual_library_producer_component_sha256=source['sha256'],historical_only_missing_ASCII_path=str(tape),historical_ASCII_sha256=oldsha,current_file_present=False,current_PF_not_invented=True,actual_input_hash_metadata_pin=pih,actual_GROUPR_receipt_pin=pg,actual_DRAGR_receipt_pin=pdr,actual_DRAGR_deck_pin=deckpin,current_binary_GENDF_pin=r['input_pin']))
  meta +=[pih,pg,pdr,deckpin]
 proof=dict(schema='ORIGINAL_NJOY_A11_FORMATTER_COMPONENT_SOURCE_BYTES_V1',source_only=True,original_endf_Source_pin=pe,original_locale_Source_pin=pL,original_dragr_Source_pin=pD,original_flags_Source_pin=pF,original_a11_begin_byte=start,original_a11_end_byte=stop,original_a11_statement_sha256=hashlib.sha256(a11).hexdigest(),original_a11_statement_bytes_hex=a11.hex(),original_locale_exact_bytes_included=True,original_a11_exact_bytes_included=True,original_ASCII_io_format='(6e11.0,i4,i2,i3,i5); per component read(field,(e11.0))',historical_ASCII_inputs=historical,historical_whole_ASCII_files_reconstructed=False,whole_original_NJOY_build_reproduced=False,**FALSE)
 write(BASE/'ORIGINAL_SOURCE_AND_HISTORICAL_INPUT_PROOF.json',proof)
 roots=old['complete_joint_roots']+[str(BASE),str(OUT)];require(len(roots)==38 and len(set(roots))==38,'old36 plus formatter Source/output, no reset')
 plan=dict(old);plan.update(schema='ORIGINAL_A11_NX_FORMATTER_COMPONENT_SOURCE_ONLY_PLAN_V1',planned_actual_output_root=str(OUT),complete_joint_roots=roots,selected_prior_NX36_plan_pin=pold,actual_prior_binary_bypass79_report_pin=pprior,original_NX_core_byte_reader_pin=pin(OLD/'check_saved_MT5_NX_raw32_and_yield.py'),compiler_pin=pc,compiler_role_two_links_exact=True,original_Fortran_FLAGS=original_flags,compile_flags_except_private_J_directory=original_flags[1:],original_flags_Source_pin=pF,native_formatter_Source_pin=pin(BASE/'original_a11_component.f90'),original_formatter_statement_proof_pin=pin(BASE/'ORIGINAL_SOURCE_AND_HISTORICAL_INPUT_PROOF.json'),private_input_future_full_pin=None,private_output_future_full_pin=None,standalone_formatter_component_only=True,historical_whole_ASCII_file_reconstruction_qualified=False,whole_original_NJOY_build_reproduced=False,scope='original a11 + native E11.0 parse + default REAL32 cast component for all79 original saved sigma5 vectors, compare all9294 current SCI NX words; no whole ASCII or reaction authority')
 write(BASE/'PLAN.json',plan);pplan=pin(BASE/'PLAN.json')
 host=BASE/'run_guarded_original_a11_component.py';publisher=BASE/'write_once_Root_original_a11_SF_HF_CLI.py'
 for p in(host,publisher,Path(__file__).absolute()):ast.parse(p.read_text(),filename=str(p))
 sources=[pin(p)for p in(host,publisher,Path(__file__).absolute(),BASE/'original_a11_component.f90',BASE/'ORIGINAL_SOURCE_AND_HISTORICAL_INPUT_PROOF.json')]+[pe,pL,pD,pF,plan['original_NX_core_byte_reader_pin']]
 hf,_=read(OLD/'FINAL_HOST_FREEZE.json');cli,_=read(OLD/'FINAL_ROOT_REVIEWABLE_CLI.json')
 failureproof=[pin(OLD/'actual_failure_postverify_20261014'/n)for n in ('REVIEW.json','TRUE_TOOL_RETURNS.json')]
 deps=unique(hf['dependencies']+sources+meta+failureproof+[pold,pprior,pplan,pc,pin(REC/'ROOT_NX_ELEVEN_ORIGINAL_ASCII_PRODUCER_INPUT_LINEAGE_20261014.json')])
 ready=dict(schema='ORIGINAL_A11_NX_FORMATTER_COMPONENT_SOURCE_REVIEW_READY_V1',source_only=True,control_plan_pin=pplan,host_source_pin=pin(host),final_publisher_Source_pin=pin(publisher),complete_source_file_pins=unique(sources),dependencies=deps,selected_Source_pins=unique(deps+sources),original_caps=plan['original_caps'],original_complete_ENV_Python_B_prefix=cli['argv'][:11],actual_business_started=False,Root_final_publication_executed=False,**FALSE)
 write(BASE/'SOURCE_REVIEW_READY.json',ready);print(json.dumps(dict(status='ORIGINAL_A11_COMPONENT_SOURCE_PREPARATION_ONLY',ready_pin=pin(BASE/'SOURCE_REVIEW_READY.json'),**FALSE)))
if __name__=='__main__':main()

# NATIVE_WRAPPER
WRAPPER = r'''program original_a11_component
 use locale
 use iso_fortran_env, only: int32,int64,error_unit
 use, intrinsic :: ieee_arithmetic
 implicit none
 integer(int32) :: ng,nr,ri,ni,nstored,ig,ix,ios,before,after,expected(370)
 real(kr) :: temperature,sigma(370),parsed,x
 character(8) :: magic
 character(11) :: field
 character(4096) :: input_path,output_path
 character :: extra
 if(storage_size(0.0)/=32.or.storage_size(0.0_kr)/=64) error stop 'original REAL32/binary64 kind required'
 if(command_argument_count()/=2) error stop 'exact private input/output args'
 call get_command_argument(1,input_path)
 call get_command_argument(2,output_path)
 open(20,file=trim(input_path),access='stream',form='unformatted',status='old',action='read')
 read(20,iostat=ios) magic,ng,nr
 if(ios/=0.or.magic/='NXA11I01'.or.ng/=370.or.nr/=79) error stop 'complete79/370 private scope'
 open(30,file=trim(output_path),access='stream',form='unformatted',status='new',action='write')
 write(30) 'NXA11O01',ng,nr
 do ri=1,nr
  read(20,iostat=ios) ni,nstored,temperature,sigma,expected
  if(ios/=0.or.ni<1.or.ni>11.or.nstored<1.or.nstored>370) error stop 'complete actual record'
  if(.not.all(ieee_is_finite(sigma)).or.any(sigma<0.0_kr)) error stop 'original finite sigma domain'
  write(30) ni,nstored,temperature
  do ig=1,ng
   x=sigma(ig)
   call a11(x,field)
   read(field,'(e11.0)',iostat=ios) parsed
   if(ios/=0.or..not.ieee_is_finite(parsed)) error stop 'native original E11.0 parse'
   before=transfer(real(x),before)
   after=transfer(real(parsed),after)
   write(30) ig,x,field,parsed,before,after,expected(ig)
  enddo
 enddo
 read(20,iostat=ios) extra
 if(ios>=0) error stop 'complete private input EOF'
 close(20)
 close(30)
 write(*,'(a)') 'ORIGINAL_A11_COMPONENT_NATIVE79_COMPLETE'
contains
'''
# END_NATIVE_WRAPPER
