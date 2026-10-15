import ast,hashlib,json,os,resource,stat,time
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'saved_full370_terminal_audit_host_source_v1'
NEW=REC/'saved_full370_terminal_audit_host_source_v2'
CAT=REC/'current_mount_identity_reattestation_20261012/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json'
START=time.monotonic()
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    path=Path(path);before=ident(path.lstat())
    if not stat.S_ISREG(before[2]):raise ValueError('regular no-symlink input: '+str(path))
    count=0;h=hashlib.sha256()
    with path.open('rb')as stream:
        if ident(os.fstat(stream.fileno()))!=before:raise ValueError('opened full7ID differs')
        while True:
            if time.monotonic()-START>=600 or resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20:raise ValueError('source-only bounded verifier cap')
            raw=stream.read(2**20)
            if not raw:break
            h.update(raw);count+=len(raw)
        if ident(os.fstat(stream.fileno()))!=before or count!=before[4]:raise ValueError('same-fd fullEOF identity/length differs')
    if ident(path.lstat())!=before:raise ValueError('after whole7ID differs')
    return dict(path=str(path),sha256=h.hexdigest(),size_bytes=count,identity=before)
def oldkey(row):return (row['path'],row['sha256'],row['size_bytes'],tuple(row['identity']))
def write(path,value):
    with path.open('x')as stream:json.dump(value,stream,indent=2,ensure_ascii=False,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
NEW.mkdir()
binding=json.loads((OLD/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json').read_text())
catpin=pin(CAT)
if catpin['sha256']!='77d7e680863e87bcff590cfab4be023a306ca6b7981eb00290440ff8e24e1ab2':raise ValueError('Root selected current catalog SHA')
catalog=json.loads(CAT.read_text())
if catalog['schema']!='CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG_V1':raise ValueError('current catalog schema')
table={oldkey(row['historical_pin']):row['current_pin']for row in catalog['rows']}
rows=[];missing=[];errors=[];fullbytes=0;sciencepaths=set(binding['science_original_input_pins'][i]['path']for i in range(1129))
for old in binding['fixed_current_pins']:
    path=Path(old['path'])
    if not path.exists():
        missing.append(dict(historical_pin=old,current_file_exists=False,current_pin=None,in_scientific_1129_inputs=str(path)in sciencepaths,original_v1_mandatory=True,new_mandatory_reclassification_authorized=False));continue
    actual=pin(path);fullbytes+=actual['size_bytes']
    same=(actual['path'],actual['sha256'],actual['size_bytes'],actual['identity'][1:])==(old['path'],old['sha256'],old['size_bytes'],old['identity'][1:])
    exact=(old['identity'][0]in(16777234,16777229)and actual['identity'][0]==16777229)
    match=table.get(oldkey(old))
    catalog_ok=match is None or match==actual
    if not(same and exact and catalog_ok):errors.append(dict(historical_pin=old,actual_pin=actual,same_SHA_and_other_six_ID=same,device_transition=exact,catalog_mapping_exact=catalog_ok))
    rows.append(dict(historical_pin=old,current_pin=actual,roles=['saved_full370_v1_fixed_input']+(['scientific_1129_input']if str(path)in sciencepaths else[]),mandatory=True,catalog_previously_covered=(match is not None),same_fd_full_EOF_SHA_and_seven_fields_proved=True,same_path_SHA_size_and_other_six_identity_fields=same,exact_declared_device_transition=exact))
science=[]
for old in binding['science_original_input_pins']:
    found=next((row for row in rows if row['historical_pin']==old),None)
    if found is None:raise ValueError('all1129 science fullpin rows mandatory')
    science.append(found['current_pin'])
mapping=dict(schema='SAVED_FULL370_EXPLICIT_CURRENT_MOUNT_REATTESTATION_SOURCE_DRAFT_V2',selected_actual_catalog_pin=catpin,rows=rows,historical_non_live_declarations=missing,all_original_v1_fixed_rows=3305,actual_live_rows_full_EOF_attested=len(rows),complete_scientific_input_count=len(science),complete_scientific_input_bytes=sum(row['size_bytes']for row in science),previous_catalog_covered=sum(row['catalog_previously_covered']for row in rows),new_individually_full_EOF_reattested=sum(not row['catalog_previously_covered']for row in rows),errors=errors,source_only=True,original_science_or_host_executed=False,compiler_or_transport_executed=False,no_input_or_math_or_threshold_change=True,original_missing_mandatory_not_silently_dropped=True,executable_host_freeze_declared=False,workflow_requires_true_three_plane_GLOBAL_and_online_BOOT_before_saved_audit=True,source_review_elapsed_seconds=time.monotonic()-START,source_review_SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
write(NEW/'PRELIMINARY_ALL_LIVE_INPUTS_FULL_EOF_CURRENT_MAPPING.json',mapping)
print(json.dumps(dict(live_rows=len(rows),science=len(science),science_bytes=mapping['complete_scientific_input_bytes'],full_EOF_bytes=fullbytes,catalog_covered=mapping['previous_catalog_covered'],newly_attested=mapping['new_individually_full_EOF_reattested'],missing=len(missing),errors=len(errors),mapping_pin=pin(NEW/'PRELIMINARY_ALL_LIVE_INPUTS_FULL_EOF_CURRENT_MAPPING.json'),science_executed=False,Source_only=True),allow_nan=False))
