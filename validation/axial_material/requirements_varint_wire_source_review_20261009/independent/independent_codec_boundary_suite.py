from pathlib import Path
import ast,hashlib,json,time
P=Path('/private/tmp/axmat-requirements-varint-wire-compact-phase-source-draft-20261009/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py')
OUT=Path('/private/tmp/axmat_requirements_varint_wire_final_independent_review_20261009')
b=P.read_bytes();assert hashlib.sha256(b).hexdigest()=='1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643'
tree=ast.parse(b);permitted=(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.ClassDef,ast.Assign);space={'__name__':'independent_isolated_codec_boundaries'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,permitted)],type_ignores=[]),str(P),'exec'),space)
encode=space['_encode_requirement_rows'];decode=space['_decoded_requirement_rows'];E=space['InputGraphError'];results=[]
def positive(name,rows,limits):
 codec=encode(rows,len(rows));actual=[list(r)for r in decode(codec,limits)];assert actual==rows;results.append({'case':name,'PASS':True,'kind':'positive','rows':len(rows)})
def reject(name,codec,limits):
 try:list(decode(codec,limits))
 except E as exc:results.append({'case':name,'PASS':True,'kind':'negative','error_type':'InputGraphError','message':str(exc)});return
 raise AssertionError('accepted '+name)
# Independently exercise five actual symbol-column bounds rather than role-only bound.
limits=(129,257,17,9,4)
positive('all-five-column-highest-valid-index-exact-inverse',[[128,256,16,8,3],[128,256,16,8,3]],limits)
for column in range(5):
 row=[0]*5;row[column]=limits[column];reject('out-of-range-column-'+str(column),encode([row],1),limits)
# Symbol-table length boundaries where one- and multi-byte shortest forms meet.
for size in (1,127,128,129,255,256,257,16384,16385,65536):
 positive('valid-final-symbol-at-table-length-'+str(size),[[size-1,size-1,size-1,8,3]],(size,size,size,9,4))
zero=encode([[0]*5],1)
reject('positive-row-with-empty-literal-path-table',zero,(0,1,1,9,4))
reject('positive-row-with-empty-canonical-path-table',zero,(1,0,1,9,4))
reject('positive-row-with-empty-owner-table',zero,(1,1,0,9,4))
for bad in (1.0,'1',None):
 codec=dict(zero,row_count=bad);reject('non-builtin-int-rowcount-'+type(bad).__name__,codec,limits)
codec=dict(zero,data=zero['data'].encode());reject('bytes-base64-payload-not-str',codec,limits)
# No large graph/table is constructed: only one tiny row and one large integer count.
codec=dict(zero,row_count=10**1000);start=time.monotonic();reject('thousand-digit-rowcount-one-row-payload-refused-before-loop',codec,limits);elapsed=time.monotonic()-start
report={'schema':'AXMAT_REQUIREMENTS_WIRE_FINAL_INDEPENDENT_CODEC_BOUNDARY_TINY_V1','status':'PASS_ISOLATED_CODEC_BOUNDARIES_ONLY','candidate_sha256':hashlib.sha256(b).hexdigest(),'case_count':len(results),'positive_cases':sum(r['kind']=='positive'for r in results),'negative_cases':sum(r['kind']=='negative'for r in results),'results':results,'huge_declared_count_does_not_allocate_rows':'Actual 1001-decimal-digit count with 5-byte raw row rejected; source count*5<=len(raw) gate is before for range(count).','huge_count_refusal_elapsed_seconds':elapsed,'private_limits_boundary':'These tests supply exact five builtin nonnegative lengths, as all existing production caller sites do. No arbitrary limits arity/type extension is approved.','no_production_graph_business_API_constructor_PREP_RUN_ART_or_formal_source_write':True,'actual_RSS_native_AAA_ABA_credit':False}
p=OUT/'independent_codec_boundary_report.json';assert not p.exists();p.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps({'report':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'case_count':len(results),'positive_cases':report['positive_cases'],'negative_cases':report['negative_cases'],'status':report['status'],'huge_count_refusal_elapsed_seconds':elapsed},sort_keys=True))
