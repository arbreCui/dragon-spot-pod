"""Only AST/full Source hashes/finite META; no candidate/API/material execution."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

P=Path(__file__).resolve().parent
checks=[]
def check(label,value):
    assert type(value)is bool and value,label
    label=str(len(checks)+1).zfill(5)+' '+label
    assert label not in {r['check']for r in checks},label
    checks.append(dict(check=label,passed=value))
def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    path=Path(path);s=path.lstat()
    check('pin real regular '+str(path),path.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1)
    with path.open('rb')as stream:
        before=identity(os.fstat(stream.fileno()));raw=stream.read();after=identity(os.fstat(stream.fileno()))
    check('pin complete EOF '+str(path),before==after==identity(s)==identity(path.lstat())and len(raw)==s.st_size)
    return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def projection(row):
    return {k:row[k]for k in('path','sha256','size_bytes','identity')}
def read(path):return json.loads(Path(path).read_bytes())

originals=read(P/'COMPLETE_PARENT_SOURCE_PROVENANCE.json')
for family in originals:
    manifest_path=Path(family['original_manifest_path']);mp=pin(manifest_path)
    check('parent manifestSHA '+str(manifest_path),mp['sha256']==family['original_manifest_sha256'])
    manifest=read(manifest_path)
    check('parent member count '+str(manifest_path),len(family['complete_members'])==manifest['member_count'])
    actual=[str(p.relative_to(manifest_path.parent))for p in sorted(manifest_path.parent.rglob('*'))if p.is_file()and p!=manifest_path]
    check('parent complete inventory '+str(manifest_path),actual==[m['relative_path']for m in family['complete_members']])
    copy_root=Path(family['copy_root'])
    for row in family['complete_members']:
        op=pin(row['path']);cp=pin(copy_root/row['relative_path'])
        check('parent original fullpin '+row['path'],op==projection(row))
        check('complete parent copy bytes '+row['path'],cp['sha256']==op['sha256']and cp['size_bytes']==op['size_bytes'])
    check('complete manifest copy bytes '+str(manifest_path),(copy_root/'MANIFEST.json').read_bytes()==manifest_path.read_bytes())

allfiles=[f for f in sorted(P.rglob('*'))if f.is_file()and f.name not in ('AUTHOR_COMPLETE_AGGREGATION_SOURCE_STATIC_REVIEW.json','MANIFEST.json')]
inventory=[];py_trees={}
for f in allfiles:
    check('no package alias '+str(f),not f.is_symlink())
    inventory.append(pin(f))
    if f.suffix=='.py':
        tree=ast.parse(f.read_bytes());py_trees[str(f)]=tree
        check('complete Python AST '+str(f),isinstance(tree,ast.Module))
    if f.suffix=='.json':
        value=read(f);check('complete JSON EOF '+str(f),type(value)in(dict,list))

for row in read(P/'ACTUAL_FINITE_V23_NATIVE_LAYOUT_SOURCE_META.json')['complete_original_copies']:
    op=pin(row['original']['path'])
    check('actual finite Source META pin '+op['path'],op==row['original'])
    check('finite Source META copySHA '+op['path'],hashlib.sha256(Path(row['copy']['path']).read_bytes()).hexdigest()==op['sha256'])
    check('finite Source META <=100000 '+op['path'],op['size_bytes']<100000)

host=P/'complete_final_MICROLIB_MACROLIB_aggregation_genuine_host.UNREADY.py'
binder=P/'bind_complete_aggregation_SOURCE_only.UNREADY.py'
engine=P/'complete_final_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'
adapter=P/'saved_native_data_access_adapter.UNREADY.py'
sources={k:p.read_bytes()for k,p in dict(host=host,binder=binder,engine=engine,adapter=adapter).items()}
proof=read(P/'COMPLETE_HOST_BINDER_FULL_SOURCE_INVERSE.json')
for row in proof:
    old=(P/'PARENT_GENUINE_NATIVE_HOST'/('complete_native_XSM_ASCII_genuine_host.UNREADY.py'if row['label']=='host'else'bind_complete_native_SOURCE_only.UNREADY.py')).read_bytes()
    raw=sources[row['label']];restored=raw.decode().splitlines(keepends=True)
    check('whole candidate SHA '+row['label'],hashlib.sha256(raw).hexdigest()==row['candidate_sha256'])
    for i,h in enumerate(reversed(row['all_hunks_full_inverse'])):
        check('full inverse current span '+row['label']+' '+str(i),restored[h['new_start0']:h['new_end0']]==h['new_full_lines'])
        restored[h['new_start0']:h['new_end0']]=h['old_full_lines']
    check('complete original bytes restored '+row['label'],''.join(restored).encode()==old)
    check('complete original SHA '+row['label'],hashlib.sha256(old).hexdigest()==row['parent_sha256'])
    old_tree=ast.parse(old);new_tree=ast.parse(raw)
    old_lines=old.decode().splitlines(keepends=True);new_lines=raw.decode().splitlines(keepends=True)
    defs=lambda t:{n.name:n for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef))}
    od,nd=defs(old_tree),defs(new_tree)
    check('all original defs remain '+row['label'],set(od)==set(nd))
    for name in sorted(set(od)-{'main','source_scope_contract'}):
        a,b=od[name],nd[name]
        check('unchanged def fullbytesAST '+row['label']+' '+name,
            ''.join(old_lines[a.lineno-1:a.end_lineno])==''.join(new_lines[b.lineno-1:b.end_lineno])and
            ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False))

check('unchanged complete adapter',sources['adapter']==(P/'PARENT_AGGREGATION_DESIGN/saved_native_data_access_adapter.UNREADY.py').read_bytes())
obs=read(P/'COMPLETE_OBSERVATION_FORTRAN_SOURCE_INVERSE.json')
for row in obs['original_Source_pins']:
    check('observer original actual fullpin '+row['path'],pin(row['path'])==row)
    check('observer entire Source copy '+row['path'],(P/'DIRECT_OBSERVATION_API_SOURCE'/Path(row['path']).name).read_bytes()==Path(row['path']).read_bytes())
for d in obs['complete_derivatives']:
    raw=Path(d['candidate']).read_bytes();lines=raw.decode().splitlines(keepends=True)
    for i,h in enumerate(reversed(d['complete_zero_based_hunks'])):
        check('Fortran insertion only '+d['candidate']+' '+str(i),h['tag']=='insert'and h['old_full_lines']==[])
        check('Fortran full inverse span '+d['candidate']+' '+str(i),lines[h['new_start0']:h['new_end0']]==h['new_full_lines'])
        lines[h['new_start0']:h['new_end0']]=h['old_full_lines']
        check('Fortran new fixed lines <=72 '+d['candidate']+' '+str(i),all(len(x.rstrip('\n'))<=72 for x in h['new_full_lines']))
    check('Fortran entire old statements restored '+d['candidate'],''.join(lines).encode()==Path(d['original']['path']).read_bytes())
    check('Fortran candidate SHA '+d['candidate'],hashlib.sha256(raw).hexdigest()==d['candidate_sha256'])
module=(P/'AXMAT_OBSERVATION_MOD.UNREADY.f90').read_text()
check('observer freeform lines <=132',all(len(x)<=132 for x in module.splitlines()))
for name in('AXOBS_LIBMIX_BEGIN','AXOBS_LIBDEN_OLD','AXOBS_LIBDEN_FISSION','AXOBS_LIBMIX_END','AXOBS_TRACK','AXOBS_MASK','AXOBS_SPH','AXOBS_FINAL'):
    check('observer complete call definition '+name,'subroutine '+name+'('in module)
for text in("call LCMEQU(target,saved)","call LCMOP(saved,trim(filename),0,2,0)","call LCMCL(saved,1)",
    "status='new'","storage_size(0)/=32","macro_length,macro_kind","indfis(:nbmix,:nfissi)",
    "maskk,lall,ldiff","write(unit) nreg,nbiso,nbmix,ngro","write(unit) nbm,nbiso,ngro,inrs","sph",'merge(1,0,mask)'):
    check('observer required actual Source operation '+text,text in module)
check('no binary LCMEXP observation call','call LCMEXP'not in module and 'call LCMEXP'not in module.upper())
check('observer no original numerical writes',all(token not in module.upper()for token in('CALL LCMPUT','CALL LCMPTC','CALL LCMSIX','CALL TONCMI','CALL LIBDEN','CALL LIBMIX')))

def assignments(path):
    return {n.targets[0].id:n.value for n in py_trees[str(path)].body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
for path,names in((engine,['SOURCE_BINDING_SHA256','BOUND_ADAPTER_PIN']),
    (host,['SOURCE_ARCHIVE','RECEIPTS','HOST','OUT','CONTROL','TARGET','TARGET_SHA','BINDING','BINDING_SHA','SOURCE_ADMISSION_SHA','PROTOCOL','PROTOCOL_SHA',
        'ACTUAL_PROTOCOL_QUALIFICATION_SHA256','ACTUAL_TRANSFER_QUALIFICATION_SHA256','REACTION_MULTIPLICITY_QUALIFICATION_SHA256','ACTUAL_SCIENTIFIC_REFERENCE_SHA256']),
    (P/'extract_actual_observation_context.UNREADY.py',['ROOT_BOUND_OBSERVATION_REQUEST_SHA256','ROOT_BOUND_GENUINE_HOST_PIN'])):
    values=assignments(path)
    for name in names:check('future actual Source None '+str(path)+' '+name,ast.literal_eval(values[name])is None)
for kind in('engine','host','adapter'):
    for text in("rss_mib",'512','1800','600','96','8','retries','threads'):
        check('original caps Source '+kind+' '+text,text in sources[kind].decode())
for text in('OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)',
    "full,production=helper.modules();helper.guard_admission(full)",
    "type(runner)is not full.OwnRSSSerialExecutor",'runner.resources is not resources',
    "runner.execute(host/'native_run','final_micro_macro_aggregation'",'complete_directory_identity(archive)==source_directories',
    'failure_post_inputs','full_postclose_input_and_D_E_check_errors','complete_joint_HOCDE_archive_bytes_after_failure',
    'actual_complete_construction_report_pin_if_saved',"ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json",'new_aggregation_qualification_sha256=None'):
    check('original genuine/failed complete host Source '+text,text in sources['host'].decode())
for text in('SOURCE_BINDING_SHA256 = None','BOUND_ADAPTER_PIN = None',"complete_final_construction_qualified=False",
    'raise SystemExit(2 if error is None else 1)','iter_all()',"array('I'","expected_count",'all_numeric_mismatches.jsonl',
    'UNQUALIFIED_NOT_DROPPED','known_component_mask_hex','SOURCE_CONTEXT_NOT_SAVED','pre_call_LDIFF_unknown',
    "GROUPS*GROUPS*MIXES*MOMENTS",'KFIS.GT.NFISS0*NESP',"for delayed in range(DELAYED+1)",'DELAYED*SLOTS',
    'LIBDEN_LAMBDA48_SLOT_LAST_MIX_WRITE','LIBDEN_CHECK_DESTINATION_ORDER_SOURCE_SUM','SOURCE_INTEGRATED_FLUX_ILONG_NOT_NGROUP_SKIP',
    'SOURCE_INTERMEDIATE_EXTRA_OVERV_OVERWRITTEN_BY_FALLBACK','self.overv_fallback_expected = None',
    'saved.close()','unlinked[(s.st_dev,s.st_ino)]','Root_only_actual_execution',
    "('scattering','scalar','fission','extras','overv_fallback','metadata')"):
    check('full conservative engine Source '+text,text in sources['engine'].decode())
for text in("'source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin'",
    "'qualified_source_manifest','host_template','engine_template','adapter','binder'",'SOURCE_BINDING_SHA256=binding_sha',
    "original129_input_pins",'additional_actual_evidence_input_pins',"original+additional",'no_numeric_material_payload_read=True',
    "same_actual_native_report_and_independent_review_bound",'strict shape paired native pins without Source-only payload read'):
    check('complete Source-only binder scope '+text,text in sources['binder'].decode()or text in sources['host'].decode())
request=read(P/'ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json')
for key in('source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin',
    'prior_actual_V22_build_tool_return_pin','actual_native_terminal_pin','actual_native_saved_coverage_contract_pin',
    'original129_input_pins','additional_actual_evidence_input_pins','new_complete_aggregation_controls_actual_run',
    'new_aggregation_qualification_sha256','actual_scientific_qualification_sha256'):
    check('request unknown None '+key,request[key]is None)
contract=read(P/'COMPLETE_ENGINE_SCOPE_AND_UNVERIFIED_COMPONENTS.json')
check('all8 original scope families',len(contract['families'])==8)
check('no fake complete success exit',contract['normal_completed_diagnostic_exit']==2 and contract['success_qualification_exit_available']is False)
check('full original Source事实319253359引用',contract['Source_fact_parents']==[319,253,359])
extension=read(P/'EXACT_READONLY_OBSERVATION_PRODUCTION_EXTENSION_CONTRACT.json')
check('honest still incomplete extraction/oldstate replay',len(extension['missing_implementation'])==3 and 'yet unimplemented here'in extension['full_XSM_extraction_extension_required'])
check('all observation events retained',len(extension['events'])==8)
check('no Source science or binary claim',extension['scientific_qualification_created']is False and extension['Source_binary_linkage_qualified']is False)

report=dict(schema='COMPLETE_AGGREGATION_ENGINE_OBSERVER_AUTHOR_SOURCE_STATIC_REVIEW_V1',
    status='SOURCE_ONLY_STATIC_CHECKS_COMPLETE_UNREADY_NO_RUNTIME_OR_QUALIFICATION',source_only=True,
    all_checks_typed_true=True,check_count=len(checks),unique_check_label_count=len({c['check']for c in checks}),checks=checks,
    full_host_binder_inverse_hunks=[len(row['all_hunks_full_inverse'])for row in proof],
    full_Fortran_insert_only_hunks=[len(d['complete_zero_based_hunks'])for d in obs['complete_derivatives']],
    complete_parent_members=[len(f['complete_members'])for f in originals],
    complete_Source_inventory_before_report=inventory,Python_AST_count=len(py_trees),
    source_candidate_pins={key:pin(path)for key,path in dict(engine=engine,host=host,binder=binder,adapter=adapter,
        observation_module=P/'AXMAT_OBSERVATION_MOD.UNREADY.f90',context_extractor=P/'extract_actual_observation_context.UNREADY.py').items()},
    independent_Source_review_completed=False,candidate_or_API_imported_or_executed=False,
    numeric_or_large_material_payload_read=False,compiled=False,original_caps_qualified_here=False,
    full_original_scope_diagnostic_only=True,complete_aggregation_executable_qualification_ready=False,
    concrete_remaining_Source_work=extension['missing_implementation'],
    actual_Source_installation=None,actual_genuine_host_run=None,new_aggregation_qualification=None,scientific_qualification=None)
# Last candidate pins append real typed checks, so record the final complete list.
report.update(check_count=len(checks),unique_check_label_count=len({c['check']for c in checks}))
assert report['check_count']==report['unique_check_label_count']and all(c['passed']is True for c in checks)
out=P/'AUTHOR_COMPLETE_AGGREGATION_SOURCE_STATIC_REVIEW.json'
out.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
rs=out.lstat();rr=out.read_bytes()
assert identity(out.lstat())==identity(rs)and len(rr)==rs.st_size
result=dict(path=str(out),sha256=hashlib.sha256(rr).hexdigest(),size_bytes=len(rr),identity=identity(rs))
print(json.dumps(dict(source_only=True,status=report['status'],report=result,
    actual_check_count=report['check_count'],all_checks_typed_true=True,candidate_executed=False)))
