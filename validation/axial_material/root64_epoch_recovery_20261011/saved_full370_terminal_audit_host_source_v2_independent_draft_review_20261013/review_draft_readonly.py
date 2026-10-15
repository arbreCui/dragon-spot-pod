"""Independent static review and full EOF pin verification; never load a candidate."""
from pathlib import Path
import ast, hashlib, json, os, resource, stat, time

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
V1=REC/'saved_full370_terminal_audit_host_source_v1'
V2=REC/'saved_full370_terminal_audit_host_source_v2'
OUT=Path(__file__).resolve().parent
started=time.monotonic()
checks=[]
def require(ok, label):
    checks.append(dict(check=label, PASS=bool(ok)))
    if not ok: raise RuntimeError(label)
def seven(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def fullpin(path):
    path=Path(path); before=seven(path.lstat())
    require(stat.S_ISREG(before[2]), 'regular non-symlink leaf '+str(path))
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb') as f:
        require(seven(os.fstat(f.fileno()))==before, 'opened exact7ID '+str(path))
        sha=hashlib.file_digest(f,'sha256').hexdigest()
        require(seven(os.fstat(f.fileno()))==before, 'same-fd whole EOF exact7ID '+str(path))
    require(seven(path.lstat())==before, 'after exact path7ID '+str(path))
    return dict(path=str(path),sha256=sha,size_bytes=before[4],identity=before)
def dump(path, value):
    with Path(path).open('x') as f:
        json.dump(value,f,indent=2,allow_nan=False); f.write('\n');f.flush();os.fsync(f.fileno())
def func(text,name):
    tree=ast.parse(text)
    node=next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
    return ast.get_source_segment(text,node)
def matches_current(historical, actual):
    return historical['path']==actual['path'] and historical['sha256']==actual['sha256'] and historical['size_bytes']==actual['size_bytes'] and historical['identity'][1:]==actual['identity'][1:] and historical['identity'][0] in (16777234,16777229) and actual['identity'][0]==16777229

source_names=['audit_saved_terminal_source_all370.py','run_actual_saved_full370_terminal_source_original_guard.py','ACTUAL_INPUT_PIN_PLAN_UNRUN.json']
source_pins=[fullpin(d/n) for d in (V1,V2) for n in source_names]
inverse_path=V2/'COMPLETE_SAVED_FULL370_SOURCE_AND_HOST_BYTE_INVERSE_DRAFT.json'
mapping_path=V2/'PRELIMINARY_ALL_LIVE_INPUTS_FULL_EOF_CURRENT_MAPPING.json'
evidence_pins=[fullpin(inverse_path),fullpin(mapping_path),fullpin(V1/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json'),fullpin(V1/'COMPLETE_SAVED_FULL370_SOURCE_AND_HOST_DERIVATION.json')]
inverse=json.loads(inverse_path.read_text()); mapping=json.loads(mapping_path.read_text())
binding=json.loads((V1/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json').read_text())
original_derivation=json.loads((V1/'COMPLETE_SAVED_FULL370_SOURCE_AND_HOST_DERIVATION.json').read_text())
science1=(V1/source_names[0]).read_bytes();science2=(V2/source_names[0]).read_bytes()
require(science1==science2 and len(science2)==29339 and hashlib.sha256(science2).hexdigest()=='2027ec61895902575165869d753926808e882e5233e89c26a3ca9c973408024f','science whole29339 bytes identical actual SHA')
old_host=(V1/source_names[1]).read_text();new_host=(V2/source_names[1]).read_text(); restored=new_host
require(len(inverse['complete_host_literal_changes'])==6,'six host changes plus one manifest change accounting')
for change in reversed(inverse['complete_host_literal_changes']):
    require(restored.count(change['new_literal'])==change['literal_count']==1,'complete unique host change '+change['label'])
    restored=restored.replace(change['new_literal'],change['old_literal'])
require(restored==old_host,'all host bytes restored exactly by full inverse')
old_manifest=(V1/source_names[2]).read_text();new_manifest=(V2/source_names[2]).read_text()
change=inverse['manifest_only_literal_rebind']
require(new_manifest.count(change['new_literal'])==1 and new_manifest.replace(change['new_literal'],change['old_literal'])==old_manifest,'whole manifest inverse only one selected Source path')
manifest1=json.loads(old_manifest);manifest2=json.loads(new_manifest)
require(manifest1['inputs']==manifest2['inputs'] and len(manifest2['inputs'])==1129,'all1129 original input paths and SHA pairs unchanged')
require(manifest1['roles']==manifest2['roles'],'all scientific roles unchanged')
require(manifest2['source']==dict(path=str(V2/source_names[0]),sha256=hashlib.sha256(science2).hexdigest()),'manifest selects actual v2 source SHA/path')
require(mapping['errors']==[] and len(mapping['rows'])==3301 and len(mapping['historical_non_live_declarations'])==4,'complete3305 accounting split3301live plus4 historical')
current_rows={}; historical_rows=[]; attested_bytes=0
for item in mapping['rows']:
    declared=item['current_pin']; old=item['historical_pin']; actual=fullpin(declared['path'])
    require(actual==declared,'actual full EOF matches current declaration '+declared['path'])
    require(matches_current(old,actual),'actual only declared device transition '+declared['path'])
    require(item['mandatory'] is True,'all live declarations mandatory '+declared['path'])
    require(declared['path'] not in current_rows,'all live paths unique '+declared['path'])
    current_rows[declared['path']]=declared; historical_rows.append(old);attested_bytes+=declared['size_bytes']
missing=mapping['historical_non_live_declarations']
for row in missing:
    old=row['historical_pin'];path=Path(old['path'])
    require(not os.path.lexists(path),'missing historical path actually absent '+str(path))
    require(row['current_pin'] is None and row['in_scientific_1129_inputs'] is False and row['original_v1_mandatory'] is True,'missing Source provenance honest historical classification '+str(path))
    require(str(path) not in manifest2['inputs'],'missing provenance outside complete scientific inputs '+str(path))
    historical_rows.append(old)
require(sorted(historical_rows,key=lambda p:p['path'])==sorted(binding['fixed_current_pins'],key=lambda p:p['path']),'exact original3305 multiset fully accounted')
require(len({p['path'] for p in historical_rows})==3305,'original3305 paths unique')
science_bytes=0
for path,sha in manifest2['inputs'].items():
    require(path in current_rows and current_rows[path]['sha256']==sha,'every scientific input covered by actual current EOF '+path)
    science_bytes+=current_rows[path]['size_bytes']
require(len(binding['science_original_input_pins'])==1129,'original scientific pinlist1129')
require({p['path']:p['sha256'] for p in binding['science_original_input_pins']}==manifest2['inputs'],'science input pins exact manifest coverage')
require(all(matches_current(p,current_rows[p['path']]) for p in binding['science_original_input_pins']),'all scientific current pins only device change')
for name in ('identity','pin','verify','write','tmp_inventory'):
    require(func(old_host,name)==func(new_host,name),'original whole function unchanged '+name)
require('class Resources:' in old_host and old_host[old_host.index(' class Resources:'):old_host.index(' resources=Resources();before=resources.check()')]==new_host[new_host.index(' class Resources:'):new_host.index(' resources=Resources();before=resources.check()')],'whole original Resources class unchanged including both TMP counts and all caps')
reattest=func(new_host,'verify_current_mount_derivation')
for fragment in ("len(mapping['rows'])!=3301","len(mapping['historical_non_live_declarations'])!=4","len(original_binding['fixed_current_pins'])!=3305","historical_non_live_Source_origins_explicitly_reclassified",'sorted(historical',"any(p not in binding['fixed_current_pins']for p in current)","len(binding['science_original_input_pins'])!=1129",'verify(current)'):
    require(fragment in reattest,'full current derivation Source covers '+fragment)
late=func(new_host,'replace_just_created_owned_report')
for fragment in ("p!=OUT/'Root_actual_saved_full370_diagnostic_summary.json'","wanted['identity'][3]!=1",'pin(p)!=wanted','os.O_RDWR|os.O_NOFOLLOW',"opened!=wanted['identity']",'stat.S_ISREG(s.st_mode)','s.st_nlink!=1',"hashlib.file_digest(f,'sha256').hexdigest()!=wanted['sha256']",'after!=opened or identity(p)!=opened','f.seek(0);f.write(raw);f.truncate();f.flush();os.fsync(f.fileno())','closed[:4]!=opened[:4]','identity(p)!=closed',"actual['sha256']!=hashlib.sha256(raw).hexdigest()"):
    require(fragment in late,'owned late summary Source covers '+fragment)
require('summary=OUT/' in new_host and new_host.index('write(summary,report);summary_pin=pin(summary)')<new_host.index('  verify(fixed);verify(outputs);resources.check()'),'forced final resource check after final report bytes')
require("report['status']='FAILED_SAVED_FULL370_DIAGNOSTIC_NO_RETRY'" in new_host and 'replace_just_created_owned_report(summary,summary_pin,report)' in new_host and 'return 0 if failure is None else 1' in new_host,'late failure honest report and true exit1 required')
require(not (V2/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json').exists() and not (V2/'COMPLETE_SAVED_FULL370_GUARD_HOST_SOURCE_FREEZE.json').exists(),'draft has no executable frozen input binding or host freeze')
require(mapping['schema']!='SAVED_FULL370_EXPLICIT_CURRENT_MOUNT_REATTESTATION_SOURCE_V2','preliminary mapping cannot pass intended final executable schema')
require(all(not row['new_mandatory_reclassification_authorized'] for row in missing),'draft correctly leaves historical reclassification unresolved')
science_text=science2.decode()
require('source_predecessor_UNRUN' not in science_text and 'PARSER_SOURCE_PROOF' not in science_text and 'SCIENTIFIC_REVIEW_AND_SOURCE_ONLY_HANDOFF' not in science_text,'science never reads old predecessor/proof/handoff metadata')
require(all(row['historical_pin']['path'] not in new_host for row in missing),'new host direct executable code never dereferences absent provenance paths')
old_plan=old_manifest.replace(original_derivation['new_literal'],original_derivation['old_literal'])
require(old_manifest.count(original_derivation['new_literal'])==1 and hashlib.sha256(old_plan.encode()).hexdigest()==original_derivation['original_plan']['sha256'],'available v1 manifest reconstructs exact original historical plan whole SHA')
old_science=next(row['historical_pin']for row in missing if row['historical_pin']['path'].endswith('/audit_saved_terminal_source_all370.py'))
require(hashlib.sha256(science1).hexdigest()==old_science['sha256'] and len(science1)==old_science['size_bytes'],'available v1 science equals disappeared historical Source whole SHA/size')
catalog=mapping['selected_actual_catalog_pin']; require(fullpin(catalog['path'])==catalog,'selected actual catalog full EOF pin')
for p in source_pins+evidence_pins:
    require(fullpin(p['path'])==p,'all reviewed Source/evidence unchanged after input review '+p['path'])
report=dict(schema='INDEPENDENT_SAVED_FULL370_CURRENT_MOUNT_V2_DRAFT_SOURCE_REVIEW_V1',status='SOURCE_DRAFT_REVIEW_PASS_EXECUTABLE_RELEASE_UNPROVEN',Source_blockers=[],release_prerequisites=[dict(item='Explicit historical classification and final current manifest',state='PENDING',details='Retain all original3305 historical declarations; keep3301 live declarations mandatory and fullEOF current; classify exactly4 absent Source-only origins as historical, no current PF, no current-content re-verification claim. This is a new current dataset and changes4 old mandatory classifications, not a claim of unchanged original-v1 executable proof.'),dict(item='Final BIND/MappingSchema/HF/current exact CLI',state='PENDING',details='Bind only genuine extant Source/manifest/runtime dependencies plus complete current mapping and unchanged original binding. No fabricated future outputs; completed independent Source freeze review and actual true closed0 remain required.'),dict(item='Upstream order gate',state='PENDING_NOT_REVIEWED',details='This draft review does not prove real three-plane GLOBAL or online BOOT. Owning Root must inspect true successful current evidence before executing diagnostic.')],reclassification_admissible_in_new_package=True,reclassification_reason='Actual science reads selected manifest.inputs/roles and its own selected Source, not disappeared predecessor metadata/proof/handoff. Science and all1129 input path/SHA pairs unchanged;3305 lineage fully accounted. Disappeared519B proof and9467B handoff content was not re-observed and must remain explicitly historical.',source_pins=source_pins,evidence_pins=evidence_pins,selected_actual_catalog_pin=catalog,full_EOF_live_declarations=3301,full_EOF_live_bytes=attested_bytes,scientific_inputs=1129,scientific_bytes=science_bytes,historical_nonlive_declarations=missing,host_changes=6,manifest_changes=1,complete_host_inverse=True,science_wholebytes_identical=True,original_resources_MRO_math_and_thresholds_unchanged=True,forced_postwrite_final_resources_check=True,owned_failure_summary_exact_samefd_fullEOF_and_nlink1=True,final_summary_bytes_and_both_TMP_ART_copies_counted=True,candidate_imported=False,candidate_compiled=False,candidate_executed=False,science_numerical_results_produced=False,upstream_BOOT_qualified=False,full_eigen_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,review_checks_passed=len(checks),elapsed_seconds=time.monotonic()-started,review_SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
require(report['review_SELF_peak_bytes']<512*2**20 and report['elapsed_seconds']<1800,'independent Source review itself bounded')
report['review_checks_passed']=len(checks)
dump(OUT/'INDEPENDENT_DRAFT_SOURCE_REVIEW.json',report)
print(json.dumps(dict(status=report['status'],report_pin=fullpin(OUT/'INDEPENDENT_DRAFT_SOURCE_REVIEW.json'),checks=len(checks),live_declarations=3301,full_EOF_bytes=attested_bytes,science_inputs=1129,source_blockers=[],release_prerequisites=len(report['release_prerequisites']),elapsed_seconds=report['elapsed_seconds'],SELF_peak_bytes=report['review_SELF_peak_bytes'])))
