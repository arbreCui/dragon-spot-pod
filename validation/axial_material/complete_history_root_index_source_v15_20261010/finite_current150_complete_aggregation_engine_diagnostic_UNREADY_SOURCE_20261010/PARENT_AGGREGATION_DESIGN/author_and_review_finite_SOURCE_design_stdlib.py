"""Finite Source/META author/reviewer. Does not import any reviewed Source."""
import ast
import hashlib
import json
from pathlib import Path
import shutil
import stat

P = Path(__file__).parent
R = Path('/Users/wen/spot')
OLD = Path('/private/tmp/axmat_reaction_TRANC_post_TONE_contract_SOURCE_META_20261010_9khfi2e_')
NATIVE = Path('/private/tmp/axmat_native_host_BINDER_STRICT_SCOPE_UNREADY_SOURCE_20261010_gs2tnzvo')
P1 = Path('/private/tmp/axmat_complete_native_XSM_ASCII_UNREADY_SOURCE_20261010_vs7f_ff8')
INPUTS = [
    ('LIBDEN', R/'src/LIBDEN.f'), ('LIBMIX', R/'src/LIBMIX.f'),
    ('LIBNFI', R/'src/LIBNFI.f'), ('LIBIPS', R/'src/LIBIPS.f'),
    ('TONDRV', R/'src/TONDRV.f'), ('TONE', R/'src/TONE.f'),
    ('LIBADJ', R/'src/LIBADJ.f'), ('XDRCST', R/'Utilib/src/XDRCST.f'),
    ('material_deck_author', R/'validation/axial_material/material_inputs.py'),
    ('original_material_audit_Source_only', P1/'SOURCE_PROVENANCE/03_material_audit.py'),
    ('saved_native_walker_Source_only', NATIVE/'complete_native_XSM_ASCII_checker_v4.UNREADY.py'),
    ('original_253_contract_META', OLD/'SOURCE_META_CONTRACT.json'),
    ('original_253_report', OLD/'REPORT.txt'),
    ('original_253_manifest', OLD/'MANIFEST.json'),
    ('original_149_layout_META', OLD/'FINITE_SOURCE_META_COPIES/05_REVIEW.json'),
    ('current_scientific_gaps', R/'validation/axial_material/complete_history_root_index_source_v15_20261010/CURRENT_SCIENTIFIC_GAPS.txt'),
]
CHECKS = []


def check(label, value):
    if type(value) is not bool or not value:
        raise ValueError(label)
    CHECKS.append(dict(check=label, passed=True))


def seven(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def fullpin(path):
    before = path.lstat()
    check('actual finite Source/META regular file '+str(path), stat.S_ISREG(before.st_mode) and not path.is_symlink())
    raw = path.read_bytes()
    after = path.lstat()
    check('finite full EOF stable7ID '+str(path), seven(before) == seven(after) and len(raw) == before.st_size)
    return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=seven(after)),raw


def write(name, value):
    path = P/name
    with path.open('x') as stream:
        json.dump(value,stream,ensure_ascii=False,indent=2,allow_nan=False)
        stream.write('\n')


copies = P/'FINITE_SOURCE_META_COPIES'
copies.mkdir()
provenance, source = [], {}
for number,(role,path) in enumerate(INPUTS,1):
    pin,raw = fullpin(path)
    target = copies/(str(number).zfill(2)+'_'+path.name)
    with target.open('xb') as out:
        out.write(raw)
    copied_pin,copied = fullpin(target)
    check('complete finite copy byte equality '+role,copied == raw)
    provenance.append(dict(role=role,original_fullpin=pin,complete_copy_fullpin=copied_pin))
    source[role] = raw.decode('utf-8')

expected = {
    'original_253_manifest':'35411e878ed6f149be576c16baa771e6c830073c8b03a1f413c8680c7c8e01d4',
    'original_253_report':'36b4383585e33b27b9be19563f26d9ae84f12a15a7116f7e644eec78ed93932e',
    'original_253_contract_META':'029ec4005924186777fd0250790d2d07e710c5e9c7b883295957ef3354efa02f',
    'saved_native_walker_Source_only':'5c50b197032b8875b9b800c0b3d8301f922846871f9d90d3190960b1e62eaf1e',
}
for entry in provenance:
    if entry['role'] in expected:
        check('fixed existing Source/META exact SHA '+entry['role'],
              entry['original_fullpin']['sha256'] == expected[entry['role']])

facts = []
FACT_NEEDLES = {
    'TONE': ["CALL LCMGET(IPLIB,'ISOTOPESSHI',LSHI)", 'IGRMIN=IPAR(9)+1',
             'IGRMAX=IPAR(10)', "CALL LCMSIX(IPLIB,'SHIBA',1)"],
    'TONDRV':['MASKL(:NGRO)=.FALSE.', 'MASKL(LLL)=.TRUE.',
              'MASK(IBM)=(MIX(ISO).EQ.IBM).AND.(LSHI(ISO).GT.0)',
              'ITSTMP=0','IPAR(1)=IGRMIN','IPAR(2)=IGRMAX',
              "CALL LCMPUT(IPLIB,'STATE-VECTOR',NSTATE,1,IPAR)",
              'IF(MAT(IREG).EQ.IBM) GO TO 85', 'IF(MIX(ISO).EQ.IBM) LSHI(ISO)=0'],
    'LIBDEN':['PARAMETER (NBLK=50,NSTATE=40,IOUT=6,MAXESP=4)',
              "DATA NORD/'    ',' LIN',' QUA'/", "CALL LCMLEN(IPLIB,'TIMESPER',ILONG,ITYLCM)",
              "CALL XABORT('LIBDEN: XS PERTURBATION FORBIDDEN.')", 'MASKK=(ILONG.EQ.-1)',
              'LALL=NBMIX.GT.NBM0', 'GAR(IBM,IBLK)=GAR(IBM,IBLK)+GA1(LLL)*DEN(ISOT)',
              'GAF(IBM,IG1,IBLK)=GAF(IBM,IG1,IBLK)+GA2(IOF)*DEN(ISOT)*FACT',
              'IOF0=IOF0+NJJ(LLL)', 'FACT=FACT*TIMFCT',
              'LOGL=LOGL.OR.(MASKL(IG1).AND.(GAF(IBM,IG1,IBLK).NE.0.0))',
              'IGMIN=LLL', 'IGMAX=LLL', 'CHECK(IBM,IG1,M)=CHECK(IBM,IG1,M)+SCAT(IPOSDE)',
              "CALL LCMPUT(KPLIB,'SIGW'//CM,NBMIX,2,GAR(1,1))",
              "IF(CV(:2).EQ.'NW') GO TO 770", "IF(CV.EQ.'TRANC') GO TO 770",
              "IF((CV(:3).EQ.'BST').OR.(CV(:3).EQ.'CST')) GO TO 770",
              "IF(CV(:8).EQ.'H-FACTOR') GO TO 770", 'IF(ILONG.EQ.0) GO TO 720',
              'IF(KFIS.GT.NFISS0*NESP) THEN', 'IOF=(KFIS-1)*NBMIX*NESP+(ISP-1)*NBMIX+IBM',
              'IF((NDEL.GT.0).AND.(ISP.EQ.1)) THEN',
              "WRITE(TEXT12,'(6HNUSIGF,I2.2,A4)') NDEL,NORD(IXSPER)",
              "CALL LCMPUT(IPLIB,'LAMBDA-D',NDEL*NFISSI,2,GA3)",
              'IF(IBM.GT.0) VOLMIX(IBM)=VOLI(ISOT)',
              'FLUX(IBM,IGR,1)=NWTMIX(IGR)*VOLMIX(IBM)',
              'FLUX(IBM,IGR,2)=NWTMIX(IGR)*VOLMIX(IBM)',
              'ENEAVG=SQRT(GA1(LLL)*GA1(LLL+1))', 'GAR(IBM,1)=REAL(ZNU)'],
    'LIBIPS': ['IF(ISONAM(1,ISOT).NE.ISONAM(1,JSOT)) CYCLE',
               'IF(ISONAM(2,ISOT).NE.ISONAM(2,JSOT)) CYCLE',
               'IF(ISONAM(3,ISOT).NE.ISONAM(3,JSOT)) CYCLE',
               'IPISO(ISOT)=IPISO(JSOT) ! set JSOT-th isotope'],
    'LIBMIX':['NED=ISTATE(13)','NBESP=ISTATE(16)','NDEL=ISTATE(19)',
              'NPART=ISTATE(26)','STERN=ISTATE(27)'],
    'LIBADJ':["IF(NBESP.NE.0) CALL XABORT('LIBADJ: MULTIPLE FISSION SPECTRA NOT'"],
    'XDRCST':['PARAMETER       (EVJOULE=1.60217653D-19,AMUKG=1.66053886D-27,',
              'XDRCST=1.67492728D-27'],
    'saved_native_walker_Source_only':['self.db.execute(\'PRAGMA cache_size=-8192\')',
              'self.db.execute(\'PRAGMA mmap_size=0\')', 'self.db.execute(\'PRAGMA temp_store=FILE\')',
              "(folder/'complete_native_original_value_bytes.bin').open('xb')",
              "records = DiskRecords(folder/'complete_native_original_path_index.sqlite')"],
    'original_material_audit_Source_only': ['replay[:, 24:281] = core.density_mix(returned, densities, mixtures, 8)[:, 24:281]',
              'for order in (0, 1):'],
}
for role, needles in FACT_NEEDLES.items():
    lines = source[role].splitlines()
    for needle in needles:
        matching = [dict(line=i+1,text=line) for i,line in enumerate(lines) if needle in line]
        check('exact finite Source fact '+role+'/'+needle, bool(matching))
        facts.append(dict(role=role,source_fullpin=next(p['original_fullpin'] for p in provenance if p['role']==role),
                          needle=needle,complete_matching_lines=matching))

adapter_pin, adapter_raw = fullpin(P/'saved_native_data_access_adapter.UNREADY.py')
tree = ast.parse(adapter_raw,filename=adapter_pin['path'])
walker = ast.parse(source['saved_native_walker_Source_only'])
allowed_imports={'hashlib','json','os','pathlib','sqlite3','stat','struct'}
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        check('adapter stdlib-only imports line '+str(node.lineno), all(a.name in allowed_imports for a in node.names))
    if isinstance(node, ast.ImportFrom):
        check('adapter stdlib-only from line '+str(node.lineno), node.module in allowed_imports and node.level==0)
    if isinstance(node, ast.Call) and isinstance(node.func,ast.Name):
        check('adapter no dynamic import/exec/compile line '+str(node.lineno),
              node.func.id not in {'exec','eval','compile','__import__'})
top = {n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign)
       and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
for name in ('ROOT_ACTUAL_NATIVE_CLOSED_RECEIPT_PIN','ROOT_ACTUAL_NATIVE_INDEPENDENT_REVIEW_PIN',
             'ROOT_BOUND_GENUINE_AGGREGATION_HOST_PIN','ROOT_BOUND_COMPLETE_AGGREGATION_ENGINE_PIN'):
    check('future actual pin None '+name, isinstance(top[name],ast.Constant) and top[name].value is None)
adapter_caps=top['ORIGINAL_CAPS']
walker_caps=next(n.value for n in walker.body if isinstance(n,ast.Assign)
    and any(isinstance(t,ast.Name) and t.id=='CAPS' for t in n.targets))
check('all original cap AST exact equality', ast.dump(adapter_caps)==ast.dump(walker_caps))
entry=tree.body[-1]
check('direct CLI refuses before payloads',isinstance(entry,ast.If) and len(entry.body)==1
    and isinstance(entry.body[0],ast.Raise) and isinstance(entry.body[0].exc,ast.Call)
    and isinstance(entry.body[0].exc.func,ast.Name) and entry.body[0].exc.func.id=='SystemExit')
check('entry adapter-only status honest', 'NO_AGGREGATION_OR_QUALIFICATION' in source.get('adapter','')
      or 'NO_AGGREGATION_OR_QUALIFICATION' in adapter_raw.decode())

scope=dict(states_in_actual_execution_order=['A','B'],isotope_slots=62,groups=370,mixtures=8,
    moments=3,declared_extra_edits=18,fission_spectra=4,fission_isotope_slots=8,
    macro_fission_components=32,original_FISSIONINDEX_integer_elements=64,
    delayed_precursor_groups=6,full_original_macro_records_per_state=19619,
    full_original_macro_physical_headers_per_state=19990,
    full_original_macro_numeric_values_per_state=2264113,
    full_scattering_mathematical_domain_per_state=3*370*370*8,
    all_original_presence_order_types_padding_empty_nodes_and_bytes_retained=True)
columns=('key','ordinal','api_key','row','micro_ordinal','macro_ordinal')
sql_contract=dict(complete_saved_sql_columns=list(columns),numeric_values_in_SQL=False,
    source_byte_pool='complete_native_original_value_bytes.bin',byte_pool_has_MAGIC=False,
    pool_spans_not_XSM_offset=True,all_full_native_records_streamed=True,
    SQLite_cache_KiB=8192,mmap_size=0,temp_store='FILE',read_only_URI=True,
    bounded_pread_bytes=2**20,whole_material_ASCII_or_XSM_decode=False,
    no_business_API_or_helper_import=True)
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,
    history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
false=dict(aggregate_engine_complete=False,aggregation_executed=False,
    original_native_RAM_bits_verified=False,Source_binary_link_proved=False,
    historical_masked_arithmetic_replay_qualified=False,MF6_multiplicity_qualified=False,
    physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,
    ABA_admitted=False,scientific_accuracy_qualified=False,new_runtime_Q_created=False)
contract=dict(schema='FINAL_COMPLETE_MICROLIB_MACROLIB_AGGREGATION_SOURCE_DESIGN_V1',
    status='SOURCE_DESIGN_ONLY_UNREADY_DATA_ACCESS_ADAPTER_NOT_COMPLETE_ENGINE',
    source_only=True,actual_material_payload_read=False,native_API_executed=False,
    source_scope=scope,original_caps=caps,complete_saved_native_schema=sql_contract,
    existing_253_contract_pin=next(e['original_fullpin'] for e in provenance if e['role']=='original_253_contract_META'),
    new_exact_SOURCE_facts=facts,adapter_pin=adapter_pin,
    implemented_Source_scope=['typed fullpin/fullEOF future Root-only verifier','bounded complete record data-access stream',
        'read-only saved SQLite/paired native pool accessor','fixed small complete62 input context capture'],
    NOT_implemented_Source_scope=['full scalar/18extra/three-moment aggregation','prompt+six delayed fission aggregation',
        'exact independent binary32 arithmetic/control suite','complete original19619 coverage classification and verdict',
        'genuine aggregation host/binder and Root actual input receipts'],
    exact_algorithm_document='COMPLETE_AGGREGATION_EXECUTION_DESIGN.md',
    current_saved_contract_vs_historical_call_context_separate=True,
    actual_historical_inputs_not_automatically_in_saved_SQL=['track MAT mixture presence',
        'pre-call old MACROLIB and old FISSIONINDEX','old TIMESTAMP/ITSTMP for any non-TONE route',
        'SPH transient factors and Source/compiler/binary linkage'],
    immediately_readable_future_actual_context=['SHIBA/STATE-VECTOR','ISOTOPESSHI','TIMESPER presence',
        'all62 alias/mix/density/temp','actual18 ADDXSNAME','all64 FISSIONINDEX','CHI-LIMITS','STATE19 NDEL6'],
    next_actual_step='After Root actual native CLOSED plus finite independent saved review, read pinned SQLite/pool small context; implement full rulebook under same genuine caps; no direct adapter execution.',
    remaining_actual_pins=None,**false)
request=dict(schema='UNREADY_ROOT_FINAL_COMPLETE_MICRO_MACRO_REQUEST_TEMPLATE_V1',
    source_status='UNREADY_NO_ACTUAL_REQUEST_OR_RUNTIME_QUALIFICATION',
    Root_actual_native_closed_receipt_pin=None,Root_actual_native_saved_review_pin=None,
    actual_native_manifest_pin=None,complete_129_original_input_pins=None,
    states={state:dict(saved_SQL_pin=None,paired_native_pool_pin=None,
        original_native_complete_state_META_pin=None,track_MAT_provenance_META_pin=None,
        historical_pre_call_MACROLIB_pin=None,actual_shiba_context_output_pin=None) for state in ('A','B')},
    bound_genuine_host_pin=None,bound_complete_engine_pin=None,source_admission_pin=None,
    independent_complete_Source_review_pin=None,H=None,O=None,C=None,D=None,E=None,
    original_caps=caps,required_complete_scope=scope,**false)
write('FULL_FINITE_SOURCE_META_PROVENANCE.json',dict(source_only=True,inputs=provenance))
write('EXACT_NEW_SOURCE_FACTS.json',dict(source_only=True,facts=facts))
write('COMPLETE_AGGREGATION_CONTRACT.json',contract)
write('ROOT_REQUEST_TEMPLATE.UNREADY.json',request)
for entry in provenance:
    pin,_=fullpin(Path(entry['original_fullpin']['path']))
    check('all finite original Source/META unchanged '+entry['role'],pin==entry['original_fullpin'])
design_pin,_=fullpin(P/'COMPLETE_AGGREGATION_EXECUTION_DESIGN.md')
write('SOURCE_DESIGN_STATIC_REVIEW.json',dict(schema='FINITE_COMPLETE_AGGREGATION_SOURCE_DESIGN_STATIC_REVIEW_V1',
    status='SOURCE_DESIGN_REVIEWED_NOT_COMPLETE_AGGREGATION',source_only=True,
    adapter_AST_parsed_not_imported_or_executed=True,all_checks_passed=True,check_count=len(CHECKS),
    checks=CHECKS,design_pin=design_pin,adapter_pin=adapter_pin,**false))
print(json.dumps(dict(status='FINITE_SOURCE_DESIGN_AUTHORED_AND_AST_REVIEWED_ONLY',source_only=True,
    finite_Source_META_count=len(INPUTS),checks=len(CHECKS),source_facts=len(facts),
    design_pin=design_pin,adapter_pin=adapter_pin,**false),ensure_ascii=False,allow_nan=False))
