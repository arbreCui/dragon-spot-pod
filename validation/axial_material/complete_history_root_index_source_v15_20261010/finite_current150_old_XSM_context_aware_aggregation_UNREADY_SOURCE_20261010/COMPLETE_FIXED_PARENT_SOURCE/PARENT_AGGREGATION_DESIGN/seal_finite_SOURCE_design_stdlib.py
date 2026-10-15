"""Seal only this fresh finite Source/META design package; no candidate imports."""
import hashlib
import json
from pathlib import Path
import stat

P=Path(__file__).parent


def require(value,message):
    if type(value) is not bool or not value:
        raise ValueError(message)


def seven(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pin(path):
    before=path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_nlink==1 and not path.is_symlink(), 'regular singleton Source/META member')
    raw=path.read_bytes()
    after=path.lstat()
    require(seven(before)==seven(after) and len(raw)==before.st_size,'finite Source/META fullEOF7ID stable')
    return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=seven(after))


def write_new(path,value):
    with path.open('x') as stream:
        json.dump(value,stream,ensure_ascii=False,indent=2,allow_nan=False)
        stream.write('\n')


review=json.loads((P/'SOURCE_DESIGN_STATIC_REVIEW.json').read_bytes())
require(review['source_only'] is True and review['all_checks_passed'] is True
    and type(review['check_count']) is int and review['check_count']==len(review['checks'])
    and all(type(c) is dict and type(c['check']) is str and c['passed'] is True for c in review['checks']),
    'real complete Source static checks')
for key in ('aggregate_engine_complete','aggregation_executed','original_native_RAM_bits_verified',
    'Source_binary_link_proved','historical_masked_arithmetic_replay_qualified','MF6_multiplicity_qualified',
    'physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted','scientific_accuracy_qualified','new_runtime_Q_created'):
    require(review[key] is False,'all unperformed aggregate/science flags false')
require(review['adapter_pin']==pin(P/'saved_native_data_access_adapter.UNREADY.py'),'adapter body unchanged since AST-only actual author')
require(review['design_pin']==pin(P/'COMPLETE_AGGREGATION_EXECUTION_DESIGN.md'),'complete algorithm document unchanged')
receipt=json.loads((P/'actual_SOURCE_design_author_tool_terminal_return.json').read_bytes())
terminal=receipt['terminal_tool_return']
require(receipt['closed'] is True and receipt['observed_terminal'] is True
    and receipt['session_repolled_after_close'] is False
    and type(terminal['exit_code']) is int and terminal['exit_code']==0
    and 'session_id' not in terminal and receipt['actual_terminal_chunk']==terminal['chunk_id'],
    'genuine actual Source author typed0closed observation')
for entry in json.loads((P/'FULL_FINITE_SOURCE_META_PROVENANCE.json').read_bytes())['inputs']:
    require(entry['original_fullpin']==pin(Path(entry['original_fullpin']['path'])),'finite original Source/META unmodified')
    require(entry['complete_copy_fullpin']==pin(Path(entry['complete_copy_fullpin']['path'])),'complete finite Source/META copy unmodified')
    require(entry['original_fullpin']['sha256']==entry['complete_copy_fullpin']['sha256'],'wholeSource copy exactSHA')
members,dirs=[],[]
for path in sorted(P.rglob('*')):
    s=path.lstat()
    require(not stat.S_ISLNK(s.st_mode),'no Source package aliases')
    if stat.S_ISDIR(s.st_mode):
        dirs.append(dict(relative_path=str(path.relative_to(P)),identity=seven(s)))
    else:
        members.append(dict(relative_path=str(path.relative_to(P)),**pin(path)))
manifest=dict(schema='FINAL_COMPLETE_MICRO_MACRO_SOURCE_DESIGN_PACKAGE_MANIFEST_V1',
    status='SEALED_SOURCE_DESIGN_UNREADY_NOT_AGGREGATION_ENGINE',source_only=True,
    root=str(P),members=members,member_count=len(members),
    total_member_bytes=sum(m['size_bytes'] for m in members),directories=dirs,
    material_payload_read=False,candidate_adapter_executed=False,aggregation_executed=False,new_Q_created=False)
write_new(P/'MANIFEST.json',manifest)
manifest_pin=pin(P/'MANIFEST.json')
for row in members:
    require(pin(Path(row['path']))=={key:row[key] for key in ('path','sha256','size_bytes','identity')},'all complete sealed Source members stable')
require(len(list(P.rglob('*')))==len(members)+len(dirs)+1,'no omitted Source namespace members')
sibling=Path(str(P)+'_seal_receipt')
sibling.mkdir()
seal=dict(schema='ACTUAL_FINAL_COMPLETE_MICRO_MACRO_SOURCE_DESIGN_SEAL_V1',
    status='ACTUAL_SOURCE_ONLY_FIXED_DESIGN_NO_AGGREGATION',source_only=True,
    manifest_pin=manifest_pin,member_count=len(members),fullEOF_SHA7ID_all_members_verified=True,
    root_directory_identity_after_manifest=seven(P.lstat()),
    original_finite_Source_META_inputs_unmodified=True,
    design_pin=pin(P/'COMPLETE_AGGREGATION_EXECUTION_DESIGN.md'),
    adapter_pin=pin(P/'saved_native_data_access_adapter.UNREADY.py'),
    contract_pin=pin(P/'COMPLETE_AGGREGATION_CONTRACT.json'),
    review_pin=pin(P/'SOURCE_DESIGN_STATIC_REVIEW.json'),
    candidate_executed=False,native_or_API_executed=False,material_payload_read=False,
    aggregation_executed=False,science_qualified=False,new_Q_created=False)
write_new(sibling/'SOURCE_DESIGN_SEAL.json',seal)
print(json.dumps(dict(status='ACTUAL_FINITE_SOURCE_DESIGN_SEALED_ONLY',source_only=True,
    manifest_pin=manifest_pin,member_count=len(members),total_member_bytes=manifest['total_member_bytes'],
    design_pin=seal['design_pin'],adapter_pin=seal['adapter_pin'],
    contract_pin=seal['contract_pin'],review_pin=seal['review_pin'],seal_pin=pin(sibling/'SOURCE_DESIGN_SEAL.json'),
    aggregation_executed=False,new_Q_created=False),ensure_ascii=False,allow_nan=False))
