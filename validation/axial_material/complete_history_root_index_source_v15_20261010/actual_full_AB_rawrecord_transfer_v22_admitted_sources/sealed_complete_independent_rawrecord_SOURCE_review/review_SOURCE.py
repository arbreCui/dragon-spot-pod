"""Independent stdlib SOURCE/AST review only; never executes reviewed sources."""
import ast
import hashlib
import json
from pathlib import Path
import stat
import sys

HERE=Path(__file__).absolute().parent
BASE=Path('/private/tmp/axmat_full_rawrecord_ready_binding_genuine_host_SOURCE_20261010_angular_k6m8')
BASE_MANIFEST_SHA='bce9c6a4e7af2cfb9a96f8c4b513fc8f67f18f9a41821bf13e428b7085a853e7'
DERIVATIVE=Path('/private/tmp/axmat_rawrecord_fixed_historical_auditor_retention_SOURCE_20261010_tl856qp8')
DERIVATIVE_MANIFEST_SHA='641682743ba9f411dd5d09eae4c2df8c3dcce8178f325cc42da71dd1f84f9b4d'
CHECKS=[]

def check(name,value,evidence=None):
    if type(value) is not bool:
        raise TypeError(name+' requires exact bool')
    CHECKS.append(dict(name=name,pass_=value,evidence=evidence))
    CHECKS[-1]['pass']=CHECKS[-1].pop('pass_')
    if not value:raise AssertionError(name)

def identity(path):
    s=path.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path):
    before=identity(path)
    if not stat.S_ISREG(before[2]) or before[3]!=1:raise ValueError('not single-link regular SOURCE '+str(path))
    raw=path.read_bytes()
    after=identity(path)
    if before!=after or len(raw)!=before[4]:raise ValueError('changed fullEOF SOURCE '+str(path))
    return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)

def strict_json(raw):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d:raise ValueError('duplicate metadata key')
            d[k]=v
        return d
    def bad(v):raise ValueError('nonfinite metadata '+v)
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)

def tree(root):
    files=[];directories=[]
    for p in sorted(root.rglob('*')):
        s=p.lstat()
        if stat.S_ISDIR(s.st_mode):directories.append(dict(path=str(p),identity=identity(p)))
        elif stat.S_ISREG(s.st_mode) and s.st_nlink==1:files.append(pin(p))
        else:raise ValueError('unexpected namespace member '+str(p))
    return dict(root=str(root),root_identity=identity(root),directories=directories,files=files)

def function_map(source):
    parsed=ast.parse(source)
    return {n.name:ast.dump(n,include_attributes=False) for n in parsed.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}

def top_values(source):
    return {n.targets[0].id:n.value for n in ast.parse(source).body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}

def arithmetic(node):
    if isinstance(node,ast.Constant) and type(node.value) in (str,int,bool,type(None)):return node.value
    if isinstance(node,ast.BinOp) and isinstance(node.op,(ast.Mult,ast.Pow)):
        a,b=arithmetic(node.left),arithmetic(node.right)
        return a*b if isinstance(node.op,ast.Mult) else a**b
    if isinstance(node,ast.Dict):return {arithmetic(k):arithmetic(v) for k,v in zip(node.keys,node.values)}
    if isinstance(node,(ast.Tuple,ast.List)):return [arithmetic(x) for x in node.elts]
    raise ValueError('unsupported nonexecuting constant expression '+ast.dump(node))

def require_text(source,name,chunk):
    check(name,chunk in source,chunk)

def read_inventory_source(root,inventory):
    result={}
    for row in inventory['files']:
        p=Path(row['path'])
        raw=p.read_bytes()
        if p.suffix=='.py':
            parsed=ast.parse(raw,filename=str(p))
            result[str(p.relative_to(root))]=dict(sha256=hashlib.sha256(raw).hexdigest(),top_definitions=[n.name for n in parsed.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))],all_definitions_count=sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))for n in ast.walk(parsed)),call_count=sum(isinstance(n,ast.Call)for n in ast.walk(parsed)))
        elif p.suffix=='.json':strict_json(raw)
        else:raw.decode('utf8')
    return result

def review_base():
    before=tree(BASE)
    mp=pin(BASE/'sealed_SOURCE_manifest.json')
    check('base fixed manifest exact SHA',mp['sha256']==BASE_MANIFEST_SHA,mp)
    manifest=strict_json((BASE/'sealed_SOURCE_manifest.json').read_bytes())
    check('base 50 complete listed members',len(manifest['files'])==50)
    check('base full namespace 50 members plus manifest',len(before['files'])==51)
    declared={r['relative_path']:r for r in manifest['files']}
    actual={str(Path(r['path']).relative_to(BASE)):r for r in before['files'] if Path(r['path']).name!='sealed_SOURCE_manifest.json' or Path(r['path']).parent!=BASE}
    check('all base names exact no filtered members',set(declared)==set(actual))
    for name,row in declared.items():
        now=actual[name]
        check('full EOF SHA7ID base member '+name,all(now[k]==row[k]for k in ('sha256','size_bytes','identity')),now)
    source_stats=read_inventory_source(BASE,before)
    check('full base SOURCE/JSON UTF8 parsed without importing',bool(source_stats),source_stats)
    text={k:(BASE/k).read_text()for k in ('generate_ROOT_actual_rawrecord_binding.py','full_AB_rawrecord_genuine_host_UNREADY.py','full_rawrecord_protocol_controls_UNREADY.py','ORIGINAL_UNREADY_PACKAGE/transfer_full_AB_rawrecord_UNREADY.py','ORIGINAL_UNREADY_PACKAGE/original_native_records_full.SOURCE.py','ORIGINAL_UNREADY_PACKAGE/original_stream_records_full.SOURCE.py')}
    binder=text['generate_ROOT_actual_rawrecord_binding.py'];host=text['full_AB_rawrecord_genuine_host_UNREADY.py'];protocol=text['full_rawrecord_protocol_controls_UNREADY.py'];wrapper=text['ORIGINAL_UNREADY_PACKAGE/transfer_full_AB_rawrecord_UNREADY.py'];native=text['ORIGINAL_UNREADY_PACKAGE/original_native_records_full.SOURCE.py'];stream=text['ORIGINAL_UNREADY_PACKAGE/original_stream_records_full.SOURCE.py']
    proof=strict_json((BASE/'full_genuine_host_adaptation_complete_inverse.json').read_bytes())
    original=(BASE/'ORIGINAL_GENUINE_AND_MATERIAL_SOURCE/original_normal_PREP_host_776b.SOURCE.py').read_text()
    lines=host.splitlines(keepends=True)
    check('host 12 declared finite adaptations',len(proof['all_full_hunks'])==12)
    for i,hunk in reversed(list(enumerate(proof['all_full_hunks']))):
        a,b=hunk['candidate_line_interval'];oa,ob=hunk['original_line_interval']
        check('host full candidate hunk '+str(i),''.join(lines[a:b])==hunk['candidate_bytes_utf8'])
        check('host full parent hunk '+str(i),''.join(original.splitlines(keepends=True)[oa:ob])==hunk['original_bytes_utf8'])
        lines[a:b]=hunk['original_bytes_utf8'].splitlines(keepends=True)
    restored=''.join(lines)
    check('host whole byte inverse equals full 776b parent',restored==original)
    check('host whole AST inverse equals full 776b parent',ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False))
    check('host parent SHA exact',hashlib.sha256(restored.encode()).hexdigest()=='776bf8300f5c5a55c9e9f4929760b0db10b5f6d2392ea0971483364d19365405')
    for i,chunk in enumerate(proof['genuine_original_guard_byte_chunks_preserved']):check('genuine guard full byte chunk '+str(i),chunk in original and chunk in host,chunk)
    readerproof=strict_json((BASE/'ORIGINAL_UNREADY_PACKAGE/full_reader_SOURCE_pin_inverse.json').read_bytes())
    restored=wrapper
    for i,h in reversed(list(enumerate(readerproof['hunks']))):
        check('wrapper reader hunk unique '+str(i),restored.count(h['new'])==1)
        restored=restored.replace(h['new'],h['old'],1)
    rawparent=(BASE/'ORIGINAL_UNREADY_PACKAGE/wrapper_before_reader_pin_SOURCE.txt').read_text()
    check('wrapper whole 2-hunk original byte inverse',restored==rawparent)
    check('wrapper whole AST original inverse',ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(rawparent),include_attributes=False))
    check('wrapper entire preserved original 098b',hashlib.sha256(wrapper.encode()).hexdigest()=='098b2a463877767254441ad49dd61076c0adb3320adf2d6c521e7abebac44116')
    caps={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_archive_bytes':2*2**30,'history_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children_at_once':1,'retries':0}
    for name,src in [('binder',binder),('host',host),('protocol',protocol),('wrapper',wrapper)]:
        check(name+' original full caps exact integers',arithmetic(top_values(src)['CAPS'])==caps)
        require_text(src,name+' main guarded only',"if __name__=='__main__'" if name!='wrapper' else "if __name__=='__main__'")
    check('host all 13 READY globals initially None',all(isinstance(top_values(host)[k],ast.Constant)and top_values(host)[k].value is None for k in ('SOURCE_STATUS','SOURCE_ARCHIVE','RECEIPTS','HOST','OUT','CONTROL','TARGET','TARGET_SHA','PROTOCOL','PROTOCOL_SHA','BINDING','BINDING_SHA','SOURCE_ADMISSION_SHA')))
    for name,src in [('binder',binder),('host',host),('protocol',protocol),('wrapper',wrapper)]:
        for k,v in top_values(src).items():
            if ('QUALIFICATION_SHA' in k or 'SCIENTIFIC_REFERENCE_SHA' in k)and isinstance(v,ast.Constant):check(name+' future '+k+' remains None',v.value is None)
    chunks=[('wrapper original default native decode','records = first_reader.decode(raw)'),('wrapper original default stream decode','second_records, second_stats = second_reader.decode_stream(binary_lines)'),('first all records raw inventory ziplongest','itertools.zip_longest(records.items(), raw_record_rows(inventory_path))'),('second all records exact ordered comparison','itertools.zip_longest(records.items(), index)'),('first full raw count','require(len(records) == counts[\'records\']'),('second full validated retained count',"stats['all_records_validated'] == stats['retained_records'] == len(records) == expected_records"),('all unknown extras retained','all_actual_GROUP_field_names_including_extra_reactions'),('full 370 8 3 32 dimensions','EXPECTED_DIMENSIONS = (370, 8, 3, 32)'),('all three moments','for moment in range(3):'),('all 370 destination groups','for destination in range(1,371):'),('all 32 fissile components','8*32'),('no trailing typed bytes',"require(payload.read(1) == b''"),('full raw EOF terminal close',"require(last_closed and src.tell() == raw_path.stat().st_size"),('original header flags retained',"'flags': flags"),('complete original raw spans retained','raw_span_sha256=digest.hexdigest()'),('REAL32 plus parser64 exact bits',"struct.pack('<fd', x, x)"),('REAL64 exact bits',"struct.pack('<d', x)"),('wide integers no float coercion',"str(x).encode('ascii') + b'\\n'"),('raw char padding retained',"'ASCII_decoded_character_with_original_padding_in_raw_span'"),('preserves A then B',"for state in ('A','B'):"),('all payload files retained','complete_typed_payload.bin'),('honest XSM not qualified','original_LCM_memory_bit_identity_directly_verified'),('honest future scientific input false',"'future_solver_scientific_input_admitted':False")]
    for name,chunk in chunks:require_text(wrapper,name,chunk)
    for name,chunk in [('native defaults no selection','def decode(raw):'),('native all records assignment','records[path] = (kind, value)'),('stream defaults full','def decode_stream(source, select=lambda path, kind, count: True):'),('stream all duplicate keys','require(path not in seen'),('stream all numeric finite','require(math.isfinite(value)'),('native full terminal close',"require(ended, 'native export has no terminal closing header')"),('stream full terminal close',"require(last_closing, 'native export has no terminal closing header')")]:require_text(native if name.startswith('native')else stream,name,chunk)
    for name,chunk in [('new source admission exact independent schema','INDEPENDENT_CURRENT150_AB_FULL_RAWRECORD_BINDING_HOST_SOURCE_REVIEW_V1'),('new source review typedchecks',"r.get('pass')is True"),('full retained SOURCE package copy',"for row in manifest['files']:"),('full actual Source int0 no session',"type(tr.get('exit_code'))is int and tr['exit_code']==0 and 'session_id'not in tr"),('normal protected complete union',"len(declared)==len(protected)and{r['path']for r in declared}==set(protected)"),('inputs general original Source checks retained',"for row in inputs['source_files'].values():provenance.append(pin(row['path'],row['sha256']))"),('generated input general checks retained',"provenance.append(pin(MATERIAL/relative,wanted))"),('base protected current-path original SHA strict check',"for row in declared:actual_pin(row);require(row['sha256']==protected[row['path']]")]:require_text(binder,name,chunk)
    for name,chunk in [('original strict5 ART roots',"roots=resource.history_roots([str(host),str(out),str(control),str(support.OUT),str(support.TERMINAL)],support.ART)"),('D E separate complete joint archive',"joint_paths=(host,out,control,archive,receipts)"),('D E all Source members beforeafter',"complete_source_inputs(support,archive)==source_inputs and complete_source_inputs(support,receipts)==receipt_inputs"),('exact genuine MRO',"full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)"),('own bound runtime actualpath',"Path(runner.bounded.__file__).resolve()!=host/'runtime/run_bounded_dragon.py'"),('protocol actual five positive ten reject',"protocol_report['positive_count']==len(protocol_report['complete_positive_controls'])==5"),('actual ten reject count',"protocol_report['negative_count']==len(protocol_report['complete_negative_controls'])==10"),('whole two actual stages',"len(runner.records)==2"),('actual typed own child int0',"type(watch['returncode'])is int and watch['returncode']==0"),('actual no limit failure',"watch['limit_failure']is None"),('actual ownchild cleanup',"watch['liveness_group_cleanup']is True"),('honest merged stdout stderr',"'child_separate_stderr_saved':False"),('external Root int0 required','external_actual_Root_typed_EXIT0_CLOSED_required=True')]:require_text(host,name,chunk)
    for name,chunk in [('protocol parser64 exact compare',"struct.pack('<d',a)==struct.pack('<d',b)"),('protocol REAL32 exact compare',"struct.pack('<f',a)==struct.pack('<f',b)"),('protocol complete full positive negative counts',"require(len(controls)==5 and len(rejects)==10"),('protocol signedzero reject',"signed zero"),('protocol complete wide ints','9007199254740993'),('protocol order negative','key order mutation rejected'),('protocol unknown extras','EXTRA_RXN')]:require_text(protocol,name,chunk)
    after=tree(BASE)
    check('base full files directories root SHA7ID beforeafter unchanged',before==after)
    report=dict(schema='INDEPENDENT_RAWRECORD_BASE_COMPLETE_SOURCE_PRELIMINARY_REVIEW_V1',status='SOURCE_BASE_BLOCKED_PENDING_UNIQUE_HISTORICAL_RETENTION_DERIVATIVE',source_only=True,all_nonmaterial_source_checks_passed=True,qualified_for_execution=False,source_manifest_pin=mp,checks=CHECKS,source_definition_scope=source_stats,complete_source_namespace_before=before,complete_source_namespace_after=after,blockers=[dict(code='ONE_PROTECTED_HISTORICAL_MATERIAL_AUDIT_SOURCE_CURRENT_PATH_SHA_MISMATCH',source_location='generate_ROOT_actual_rawrecord_binding.py material_admission complete protected source union',scope='54 producer-declared protected logical sources: only material_audit.py per Root actual fullhash META observation',general_input_rules='inputs.source_files8 and generated12 original SHA rules retained; Root reports actual PASS',required_fix='only explicit original906/currentcb/retained906/retentionJSON mapping for fixed material_audit.py; preserve all original logical sources and all other exact current path SHA checks',peak_or_numeric_payload_read=False)],actual_protocol_controls_executed=False,actual_full_rawrecord_transfer_executed=False,any_reviewed_SOURCE_imported_or_executed=False,guard_API_called=False,material_numeric_payload_read=False,actual_transfer_qualification_sha256=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    (HERE/'BASE_PRELIMINARY_SOURCE_REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    return report

def review_derivative(base_report):
    before=tree(DERIVATIVE)
    mp=pin(DERIVATIVE/'sealed_SOURCE_manifest.json')
    check('fixed derivative exact final sealed manifest SHA',mp['sha256']==DERIVATIVE_MANIFEST_SHA,mp)
    manifest=strict_json((DERIVATIVE/'sealed_SOURCE_manifest.json').read_bytes())
    check('fixed derivative full 118 members plus manifest',manifest['file_count']==len(manifest['files'])==118 and len(before['files'])==119)
    declared={r['relative_path']:r for r in manifest['files']}
    actual={str(Path(r['path']).relative_to(DERIVATIVE)):r for r in before['files'] if Path(r['path'])!=DERIVATIVE/'sealed_SOURCE_manifest.json'}
    check('fixed derivative exact all names no omitted member',len(declared)==118 and set(declared)==set(actual))
    for name,row in declared.items():
        now=actual[name]
        check('fixed derivative complete EOF SHA7ID '+name,all(now[k]==row[k]for k in ('sha256','size_bytes','identity')),now)
    stats=read_inventory_source(DERIVATIVE,before)
    check('fixed derivative all 44 Python SOURCE ASTs parsed no execution',len(stats)==44,stats)
    base_files=base_report['complete_source_namespace_before']['files']
    preserved={str(Path(r['path']).relative_to(DERIVATIVE/'ORIGINAL_BINDING_PACKAGE')):r for r in before['files'] if Path(r['path']).is_relative_to(DERIVATIVE/'ORIGINAL_BINDING_PACKAGE')}
    check('fixed derivative exact complete original51 names',set(preserved)=={str(Path(r['path']).relative_to(BASE))for r in base_files})
    for row in base_files:
        name=str(Path(row['path']).relative_to(BASE))
        check('fixed derivative original base wholebytes preserved '+name,all(preserved[name][k]==row[k]for k in ('sha256','size_bytes')))
    for name,wanted in [('full_AB_rawrecord_genuine_host_UNREADY.py','450497eec591778eaeecff0e42f5af5ab9bec493ec07bc55ef86ebe4c5bcccec'),('full_rawrecord_protocol_controls_UNREADY.py','45de90e675192a78cf2f80de4c3fee94cace03516a58dd2fb15364ed1d67838b'),('ORIGINAL_UNREADY_PACKAGE/transfer_full_AB_rawrecord_UNREADY.py','098b2a463877767254441ad49dd61076c0adb3320adf2d6c521e7abebac44116')]:
        check('fixed derivative full unchanged exact Source '+name,actual[name]['sha256']==wanted and (DERIVATIVE/name).read_bytes()==(BASE/name).read_bytes())
    binder=(DERIVATIVE/'generate_ROOT_actual_rawrecord_binding.py').read_text();parent=(BASE/'generate_ROOT_actual_rawrecord_binding.py').read_text()
    check('fixed new binder exact52b Source',hashlib.sha256(binder.encode()).hexdigest()=='52b8665a6505c0965f3af5c9f42fa440a9dd6df2dcbca1d1f00e3146472fe58f')
    inverse=strict_json((DERIVATIVE/'FIXED_HISTORICAL_RETENTION_BINDER_COMPLETE_INVERSE.json').read_bytes())
    check('fixed binder exactly7 SOURCE hunks',inverse['hunk_count']==len(inverse['hunks'])==7)
    restored=binder
    for i,h in reversed(list(enumerate(inverse['hunks']))):
        check('fixed binder unique whole Source hunk '+str(i),restored.count(h['new'])==1 and parent.count(h['old'])==1)
        restored=restored.replace(h['new'],h['old'],1)
    check('fixed binder full7 inverse wholebytes6da',restored==parent)
    check('fixed binder full7 inverse wholeAST6da',ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False))
    oldfunc=function_map(parent);newfunc=function_map(binder)
    check('fixed binder full original13 plus one14 definitions',len(oldfunc)==13 and len(newfunc)==14 and set(newfunc)-set(oldfunc)=={'historical_material_auditor_retention'})
    for name in oldfunc:
        if name not in ('material_admission','main'):
            oldnode=next(n for n in ast.parse(parent).body if isinstance(n,ast.FunctionDef)and n.name==name)
            newnode=next(n for n in ast.parse(binder).body if isinstance(n,ast.FunctionDef)and n.name==name)
            check('fixed binder full unchanged original definition '+name,oldfunc[name]==newfunc[name] and '\n'.join(parent.splitlines()[oldnode.lineno-1:oldnode.end_lineno])=='\n'.join(binder.splitlines()[newnode.lineno-1:newnode.end_lineno]))
    require_text(binder,'fixed general input8 strict Source rule unchanged',"for row in inputs['source_files'].values():provenance.append(pin(row['path'],row['sha256']))")
    require_text(binder,'fixed generated12 strict rule unchanged',"provenance.append(pin(MATERIAL/relative,wanted))")
    require_text(binder,'fixed complete original54 expected map',"type(expected)is dict and len(expected)==len(protected)==54 and expected==protected")
    require_text(binder,'fixed all54 logical current pin paths preserved',"len(declared)==len(protected)and{r['path']for r in declared}==set(protected)")
    require_text(binder,'fixed only one precise logical exception',"if row['path']==str(MATERIAL_AUDITOR_ORIGINAL):require(row==history['current_original_source']and row['sha256']==MATERIAL_AUDITOR_CURRENT_SHA and protected[row['path']]==MATERIAL_AUDITOR_OLD_SHA")
    require_text(binder,'fixed other53 strict producerSHA unchanged',"else:require(row['sha256']==protected[row['path']]")
    require_text(binder,'fixed every current path actual fullpin check','        actual_pin(row)')
    require_text(binder,'fixed complete expected map stored binding',"'protected_material_source_expected_sha256':material['protected_material_source_expected_sha256']")
    require_text(binder,'fixed explicit resolution stored binding',"'historical_material_source_resolution':material['historical_material_source_retention']")
    require_text(binder,'fixed all4 retention pins final host input scope','*provenance,*history_pins')
    require_text(binder,'fixed complete retention evidence copied fresh Source',"('complete_material_auditor_one_hunk_SOURCE_inverse.json',history['full_source_inverse_proof'])")
    parsed=ast.parse(binder);helper=next(n for n in parsed.body if isinstance(n,ast.FunctionDef)and n.name=='historical_material_auditor_retention')
    calls=[n for n in ast.walk(helper)if isinstance(n,ast.Call)]
    forbidden={'exec','eval','compile','__import__','import_module','exec_module','decode_stream','analyze','terminal','run','execute','Popen'}
    callnames={n.func.id if isinstance(n.func,ast.Name)else n.func.attr if isinstance(n.func,ast.Attribute)else '<other>'for n in calls}
    check('fixed retention helper SOURCE/metadata only no dynamic import/parser/API execution',not bool(callnames&forbidden),sorted(callnames))
    decodecalls=[n for n in calls if isinstance(n.func,ast.Attribute)and n.func.attr=='decode']
    check('fixed retention decode only UTF8 source text no material decoder',len(decodecalls)==2 and all(isinstance(n.func.value,ast.Name)and n.func.value.id in ('current_raw','retained_raw')and len(n.args)==1 and isinstance(n.args[0],ast.Constant)and n.args[0].value=='utf-8'for n in decodecalls))
    exactkeys={'schema','resolution_kind','original_path','original_expected_sha256','current_original_source','retained_source','retention_record','full_source_inverse_proof'}
    sets=[set(x.value for x in n.elts)for n in ast.walk(helper)if isinstance(n,ast.Set)and all(isinstance(x,ast.Constant)and type(x.value)is str for x in n.elts)]
    check('fixed retention private object exact eight keys',exactkeys in sets)
    values=top_values(binder)
    for key,wanted in [('MATERIAL_AUDITOR_OLD_SHA','90659465a03f6b9464df5a7780aabbce06aeb8c0bbfb746c3dc40eda1b6afed5'),('MATERIAL_AUDITOR_CURRENT_SHA','cb461b94ae61917da63e813e3dae2261d8f48a20834b15b42d0cad9fe0b8ddc9'),('MATERIAL_AUDITOR_RETENTION_RECORD_SHA','1e5cc9cc2edba850080c61dbad8a71e7e76551dc920c8a0fb844017a3b8c5697'),('MATERIAL_AUDITOR_FULL_SOURCE_PROOF_SHA','e1755e33f677ad3ded8e5722d76f1abe4dd0d5db8610d015348ca25074b20ba8')]:check('fixed exact immutable source binding '+key,arithmetic(values[key])==wanted)
    proof_path=DERIVATIVE/'MATERIAL_AUDITOR_FULL_SOURCE_INVERSE.json';proofpin=pin(proof_path);proof=strict_json(proof_path.read_bytes())
    check('fixed full auditor inverse actuale175 Source metadata',proofpin['sha256']==arithmetic(values['MATERIAL_AUDITOR_FULL_SOURCE_PROOF_SHA']))
    old=(DERIVATIVE/'FINITE_RETENTION_SOURCE_FACTS/historical_material_audit.py').read_text();new=(DERIVATIVE/'FINITE_RETENTION_SOURCE_FACTS/current_material_audit.py').read_text();recordraw=(DERIVATIVE/'FINITE_RETENTION_SOURCE_FACTS/original_retention_record.json').read_bytes();record=strict_json(recordraw)
    check('fixed complete retained old906 Source bytes',hashlib.sha256(old.encode()).hexdigest()==arithmetic(values['MATERIAL_AUDITOR_OLD_SHA'])and len(old.encode())==18947)
    check('fixed complete actual currentcb Source bytes',hashlib.sha256(new.encode()).hexdigest()==arithmetic(values['MATERIAL_AUDITOR_CURRENT_SHA'])and len(new.encode())==18948)
    check('fixed original whole retention mapping1e5cc bytes',hashlib.sha256(recordraw).hexdigest()==arithmetic(values['MATERIAL_AUDITOR_RETENTION_RECORD_SHA'])and len(recordraw)==1222)
    h=proof['full_hunk'];check('auditor one complete original/current Source hunk only',old.count(h['old'])==new.count(h['new'])==1 and new.replace(h['new'],h['old'],1)==old)
    check('auditor full inverse AST equals full old SOURCE',ast.dump(ast.parse(new.replace(h['new'],h['old'],1)),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
    od={n.name:n for n in ast.parse(old).body if isinstance(n,ast.FunctionDef)};nd={n.name:n for n in ast.parse(new).body if isinstance(n,ast.FunctionDef)}
    check('auditor full8 definition names order unchanged',list(od)==list(nd)==['sha','fuel_densities','names','resolve_isotope_rows','metadata_check','terminal','analyze','main'])
    for name in od:
        if name!='terminal':check('auditor full other7 definitions exact '+name,ast.dump(od[name],include_attributes=False)==ast.dump(nd[name],include_attributes=False)and '\n'.join(old.splitlines()[od[name].lineno-1:od[name].end_lineno])=='\n'.join(new.splitlines()[nd[name].lineno-1:nd[name].end_lineno]))
    check('auditor full nondefinition AST unchanged',[ast.dump(n,include_attributes=False)for n in ast.parse(old).body if not isinstance(n,ast.FunctionDef)]==[ast.dump(n,include_attributes=False)for n in ast.parse(new).body if not isinstance(n,ast.FunctionDef)])
    terminal=od['terminal'];branches=[n for n in terminal.body if isinstance(n,ast.If)and ast.dump(n.test,include_attributes=False)==ast.dump(ast.parse("stage == 'MATERIAL'",mode='eval').body,include_attributes=False)]
    check('auditor default MATERIAL stage unchanged',terminal.args.defaults[-1].value=='MATERIAL')
    check('auditor MATERIAL branch returns before changed snapshot check',len(branches)==1 and isinstance(branches[0].body[-1],ast.Return)and branches[0].end_lineno<next(n for n in ast.walk(terminal)if isinstance(n,ast.Call)and any(isinstance(a,ast.Constant)and a.value=='snapshot native module count'for a in n.args)).lineno)
    terminalcalls=[n for n in ast.walk(od['analyze'])if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='terminal']
    check('auditor analyze uses unchanged MATERIAL default two positional args',len(terminalcalls)==1 and len(terminalcalls[0].args)==2 and not terminalcalls[0].keywords)
    expectedmapping=[dict(original_path='/Users/wen/spot/validation/axial_material/material_audit.py',original_sha256=arithmetic(values['MATERIAL_AUDITOR_OLD_SHA']),retained_path='/Users/wen/spot/validation/artifacts/axial-material-tools-20261003/material_audit_used_for_ab.py',retained_sha256=arithmetic(values['MATERIAL_AUDITOR_OLD_SHA']))]
    check('retention original one exact old906 Source mapping',record['mapping']==expectedmapping and type(record['schema_version'])is int and record['schema_version']==1 and record['status']=='EXACT_MATERIAL_AUDITOR_RETAINED')
    check('retention current Source disclosure no audit modification',record['current_reader_path']==expectedmapping[0]['original_path']and record['current_reader_sha256']==arithmetic(values['MATERIAL_AUDITOR_CURRENT_SHA'])and record['audit_json_modified']is False)
    check('retention unchanged A/B actual audit SHA metadata only',record['audit_receipts']=={proof['pins']['A_audit']['path']:proof['pins']['A_audit']['sha256'],proof['pins']['B_audit']['path']:proof['pins']['B_audit']['sha256']})
    for name in('current_original_source','retained_source','retention_record','A_audit','B_audit'):
        p=proof['pins'][name]
        check('retention Source proof exact7 integer pin '+name,set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])and p['identity'][4]==p['size_bytes'])
    contract=strict_json((DERIVATIVE/'ROOT_MATERIAL_PROVENANCE_ADMISSION_CONTRACT.UNREADY.json').read_bytes())
    check('root retention contract two new fields only additions to original',set(contract['future_required_top_level_fields'])-set(strict_json((BASE/'ROOT_MATERIAL_PROVENANCE_ADMISSION_CONTRACT.UNREADY.json').read_bytes())['future_required_top_level_fields'])=={'protected_material_source_expected_sha256','historical_material_source_retention'})
    for key in('actual_transfer_qualification_sha256','actual_scientific_reference_sha256'):check('fixed future actual runtime/scientific '+key+' None',manifest[key]is None)
    for key in('original_XSM_memory_bits_verified','reaction_multiplicity_verified','scientific_accuracy_qualified','physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted'):check('fixed manifest honest scope '+key+' false',manifest[key]is False)
    after=tree(DERIVATIVE);check('fixed complete119 files dirs root fullEOF SHA7ID beforeafter unchanged',before==after)
    check('base complete51 files dirs root unchanged during derivative review',tree(BASE)==base_report['complete_source_namespace_before'])
    report=dict(schema='INDEPENDENT_CURRENT150_AB_FULL_RAWRECORD_BINDING_HOST_SOURCE_REVIEW_V1',status='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE',source_only=True,all_checks_passed=all(r['pass']is True for r in CHECKS),blockers=[],qualified_source_manifest_sha256=DERIVATIVE_MANIFEST_SHA,qualified_generator_sha256=actual['generate_ROOT_actual_rawrecord_binding.py']['sha256'],qualified_original_wrapper_sha256='098b2a463877767254441ad49dd61076c0adb3320adf2d6c521e7abebac44116',qualified_host_template_sha256='450497eec591778eaeecff0e42f5af5ab9bec493ec07bc55ef86ebe4c5bcccec',qualified_protocol_source_sha256='45de90e675192a78cf2f80de4c3fee94cace03516a58dd2fb15364ed1d67838b',checks=CHECKS,base_preliminary_review_pin=pin(HERE/'BASE_PRELIMINARY_SOURCE_REVIEW.json'),complete_derivative_source_namespace_before=before,complete_derivative_source_namespace_after=after,complete_source_definition_scope=stats,source_only_retention_scope='one fixed material_audit.py original906→currentcb disclosure with exact old906 retained SOURCE and fixed1e5cc mapping; original54logical expected map kept; other53 producerSHA strict; input8/generated12 general originalSHA unchanged',original_genuine_caps=arithmetic(values['CAPS']),new_source_ready_not_actual_execution_qualification=True,actual_protocol_controls_executed=False,actual_full_rawrecord_transfer_executed=False,any_reviewed_SOURCE_imported_or_executed=False,reader_helper_guard_or_business_API_called=False,material_numeric_payload_read=False,ART_enumerated=False,canonical_D_E_or_sealed_sources_modified=False,actual_transfer_qualification_sha256=None,actual_scientific_reference_sha256=None,original_XSM_memory_bits_verified=False,reaction_multiplicity_verified=False,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    (HERE/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    return report

if __name__=='__main__':
    report=review_base()
    if sys.argv[1:]==['--fixed-derivative']:
        report=review_derivative(report);filename='REVIEW.json'
    elif not sys.argv[1:]:filename='BASE_PRELIMINARY_SOURCE_REVIEW.json'
    else:raise ValueError('fixed SOURCE-only review args')
    print(json.dumps(dict(source_only=True,status=report['status'],review_file=str(HERE/filename),review_sha256=pin(HERE/filename)['sha256'],check_count=len(CHECKS),reviewed_API_or_business_executed=False),allow_nan=False))
