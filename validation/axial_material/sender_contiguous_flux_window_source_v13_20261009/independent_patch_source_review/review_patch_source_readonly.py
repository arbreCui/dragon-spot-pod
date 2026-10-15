"""Independent AST literals/text/SHA/inverse review. No helper import/call."""
import ast,difflib,hashlib,json,re
from pathlib import Path
D=Path('/private/tmp/axmat_v13_sender_contiguous_flux_window_patch_readonly_review_20261009')
ROOT=Path('/Users/wen/spot');R=ROOT/'validation/axial_material'
SD=R/'sender_contiguous_flux_window_source_v13_20261009'
H=R/'sender_contiguous_flux_window_patch_v13.py'
O=ROOT/'validation/artifacts/axial-material-qualified-AB-rank1-factor-cache-build-admission-20261007/FLU2DR64.f'
N=SD/'FLU2DR64.f';P=SD/'source_patch_proof.json'
inventory={}
def sha(data):return hashlib.sha256(data).hexdigest()
def pin(p,wanted=None):
 p=Path(p);assert p.is_file() and not p.is_symlink()
 actual=sha(p.read_bytes())
 if wanted is not None:assert actual==wanted
 inventory[str(p)]={'sha256':actual,'size_bytes':p.stat().st_size}
 return dict(path=str(p),sha256=actual)
def read(p,wanted=None):pin(p,wanted);return json.loads(p.read_text())
pin(H,'77c037a14a3852f628344d9a7cdee3b09e757b00420bf78eddcc1f3a17a6f163')
pin(O,'bb901bfed9a4199a5b4c98c58c93bf3b3dda597fd2047bfed6d267c8dcadac81')
pin(N,'cd8e419c19f3a473beb6ded27705c513a07363a1a37e003c64266c5ef9cf5fb1')
proof=read(P,'f5b6bc7fdab49e97dd1178937437365ac11c347cc0b1137b02c02830c0fbfa40')
input_admission=read(SD/'source_admission_INPUT.json','6f64546cad4c055b87a00e74392a254f90e0439f692506ed6d6826ba8f54cdf7')
tree=ast.parse(H.read_text());imports=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom))]
assert len(imports)==1 and isinstance(imports[0],ast.Import) and [x.name for x in imports[0].names]==['hashlib']
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
assert [n.name for n in functions]==['digest_text','patch_sender']
assert not any(isinstance(n,ast.Call) for n in tree.body)
patch=functions[1];assignments=[n for n in patch.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='edits'for t in n.targets)]
assert len(assignments)==1;edits=ast.literal_eval(assignments[0].value)
assert len(edits)==5 and edits==proof['edits']
old=O.read_text();new=N.read_text();constructed=old;locations=[]
for e in edits:
 assert set(e)=={'name','old','new'} and constructed.count(e['old'])==1
 locations.append({'name':e['name'],'original_match_count':1,'original_line':old[:old.index(e['old'])].count('\n')+1})
 constructed=constructed.replace(e['old'],e['new'],1)
assert constructed==new
inverse=new
for e in reversed(edits):assert inverse.count(e['new'])==1;inverse=inverse.replace(e['new'],e['old'],1)
assert inverse.encode()==O.read_bytes()
start='      SUBROUTINE FLUSP64('
assert old.count(start)==new.count(start)==1
op,ow=old.split(start);np,nw=new.split(start);assert op==np
ow=start+ow;nw=start+nw
assert ow.splitlines()[0:2]==nw.splitlines()[0:2]
ref=ow.replace(start,'      SUBROUTINE FLUSP64_REFERENCE(',1)
assert (SD/'FLUSP64.original_reference_unit.f').read_text()==ref
assert (SD/'FLUSP64.candidate_unit.f').read_text()==nw
for text,key in ((old,'original_sender_sha256'),(new,'candidate_sender_sha256'),(ow,'original_wrapper_sha256'),(nw,'candidate_wrapper_sha256'),(ref,'reference_wrapper_sha256')):
 assert sha(text.encode())==proof[key]
for p in (SD/'FLUSP64.original_reference_unit.f',SD/'FLUSP64.candidate_unit.f'):pin(p)
expected_diff=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=str(O),tofile=str(N)))
assert (SD/'sender.patch').read_text()==expected_diff;pin(SD/'sender.patch')
assert len(list(SD.iterdir()))==6 and not any(p.is_dir() or p.is_symlink()for p in SD.iterdir())
for key in ('helper','original_sender','candidate_sender','proof','original_receiver'):
 d=input_admission[key];assert set(d)=={'path','bytes','sha256'};pin(Path(d['path']),d['sha256']);assert Path(d['path']).stat().st_size==d['bytes']
assert input_admission['source_only'] is True
for k in ('compiled','controls_executed','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'):assert input_admission[k] is False
assert proof['observed_native_RSS_saving'] is None
assert proof['conditional_payload_saving_bytes']==dict(formula='8 * NUN * NGEFF',NUN=1800,NGEFF=370,bytes=5328000)
for k in ('complete_inverse_byteexact','sender_outside_wrapper_byteexact','source_copy_and_leakage_arithmetic_retained',
 'sparse_gather_scatter_retained','empty_active_set_returns_before_allocation','no_pointer_or_target_or_assumed_shape_added',
 'partial_output_on_failed_direct_call_must_not_be_reused','successful_receiver_does_not_read_incoming_output_required','caller_old_source_output_nonalias_required'):
 assert proof[k] is True
for k in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'):assert proof[k] is False
assert new.count('CALL FLUSP64(')==4 and old.count('CALL FLUSP64(')==4
calls=re.findall(r'CALL FLUSP64\([^\n]+\n(?:[^\n]*\n){1,2}',op)
assert len(calls)==4 and all('FLUX(1,1,2),FLUX(1,1,8),FLUX(1,1,7)'in c for c in calls)
leak=ow[ow.index('          IF((ILEAK.EQ.3)'):ow.index('      CALL SPOF64(')]
assert leak in nw
assert 'IF(NGEFF.EQ.0) RETURN' in nw and nw.index('IF(NGEFF.EQ.0) RETURN')<nw.index('ALLOCATE(KPSYS')
assert 'DIRECT_OUTPUT_WINDOW=(IGLAST-IGFIRST+1.EQ.NGEFF)'in nw
assert 'IF(.NOT.DIRECT_OUTPUT_WINDOW) ALLOCATE(F2(NUN,NGEFF))'in nw
assert 'KEYFLX,FUN(1,NGIND(1)),S2,TITR)'in nw
assert 'IF(ALLOCATED(F2)) DEALLOCATE(F2)'in nw
assert 'POINTER'not in ''.join(e['new'].upper()for e in edits) and 'TARGET'not in ''.join(e['new'].upper()for e in edits)
receiver=Path(input_admission['original_receiver']['path']);rt=receiver.read_text()
def normalize_header(text):
 m=re.search(r'SUBROUTINE SPOF64\((.*?)\)',text,re.S);assert m
 lines=m.group(1).splitlines()
 return re.sub(r'\s','',lines[0]+''.join(line[6:]for line in lines[1:]))
assert normalize_header(nw)==normalize_header(rt)=='KPSYS,IPTRK,IMPX,NGEFF,NGIND,NREG,NMAT,NUN,MAT,KEYFLX,FUNKNO,SUNKNO,TITR'
interface=nw[nw.index('      INTERFACE'):nw.index('      END INTERFACE')]
for text in ('USE GANLIB','TYPE(C_PTR) KPSYS(NGEFF),IPTRK','DOUBLE PRECISION FUNKNO(NUN,NGEFF),SUNKNO(NUN,NGEFF)',
 'CHARACTER TITR*72','INTEGER NGEFF,NGIND(NGEFF),IMPX,NREG,NMAT,NUN,MAT(NREG),','KEYFLX(NREG)'):
 assert text in interface
report={'status':'PASS_SOURCE_ONLY_HELPER_TEXT_AST_AND_COMPLETE_INVERSE',
 'helper':pin(H),'candidate_sender':pin(N),'original_sender':pin(O),'proof':pin(P),
 'source_only_INPUT':pin(SD/'source_admission_INPUT.json'),'source_inventory':inventory,
 'helper_imported_or_called':False,'business_or_compiler_executed':False,'project_written':False,'Root_job_polled':False,
 'AST_literal_five_edits_independently_applied_without_helper_execution':True,'edits':locations,
 'complete_inverse_to_bb901_byte_exact':True,'outside_FLUSP64_full_sender_byte_exact':True,
 'public_FLUSP64_header_ABI_byte_exact':True,'explicit_SPOF64_interface_13_arguments_and_types_match_frozen_actual_receiver':True,
 'exact_candidate_wrapper_and_unit_only_renamed_reference_bytes':True,
 'sparse_copy_solve_scatter_AND_source_leak_expression_order_retained':True,
 'zero_group_early_return_before_allocation':True,
 'contiguous_window_reasoning':'IG visits active positions once in ascending order; nonempty last-first+1==count iff no inactive gaps. The explicit-shape FUN starts a contiguous NUN by NGEFF sequence at element(1,NGIND(1)).',
 'all_four_production_callers_full_prefix_byte_exact_planes':[2,8,7],
 'successful_OUTPUT_semantics_requires_actual_receiver_no_incoming_FUN_and_no_alias':'Peer review of complete pinned receiver/current kernel and callers is separately supplied.',
 'failure_output_semantics_deliberately_not_claimed_equal':'A failing direct receiver may partially write original FUN where the old temporary had deferred scatter; no retry/reuse of failed state is required.',
 'conditional_payload_saving_bytes':5328000,'conditional_payload_saving_MiB':5328000/(1024*1024),
 'actual_temporary_absence_or_RSS_saving_not_source_qualified':True,
 'required_next_real_tests':['fresh old/reference and new wrapper raw complete output bitwise controls','empty/single/contiguous/sparse/all-active and repeated calls','leakage branches/input nonmutation/residual output preservation','actual linked new sender binary provenance','full original68 component controls plus new sender stages','fresh complete coupled AAA and original independent eight accuracy gates'],
 'compiled':False,'controls_executed_by_this_review':False,'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False}
q=D/'REPORT_HELPER_AND_INVERSE.json';q.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':report['status'],'report':str(q),'report_sha256':sha(q.read_bytes()),'edits':5,'complete_inverse_byteexact':True},sort_keys=True))
