import ast, base64, copy, hashlib, json, os, stat
from pathlib import Path
from types import SimpleNamespace

REC = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P = REC / 'current_material_evidence_empty_root_cumulative_twelve_roots_source_v4_20261014'
DEST = REC / 'independent_empty_MACROLIB_root_cumulative12_candidate_writer_Source_review_20261014'

def require(ok, text):
    if not ok: raise RuntimeError(text)

def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path):
    q=Path(path);s=q.lstat();require(stat.S_ISREG(s.st_mode),'regular Source/meta')
    with os.fdopen(os.open(q,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
        require(identity(os.fstat(f.fileno()))==identity(s),'Source open7');sha=hashlib.file_digest(f,'sha256').hexdigest();require(identity(os.fstat(f.fileno()))==identity(s),'Source EOF7')
    require(identity(q.lstat())==identity(s),'Source path7')
    return dict(path=str(q),sha256=sha,size_bytes=s.st_size,identity=identity(s))

def read(q): return json.loads(Path(q).read_bytes())
ready=read(P/'SOURCE_REVIEW_READY_v2.json');plan=read(ready['plan_pin']['path']);iv=read(ready['inverse_pin']['path'])
own=[ready[k]for k in ['host_source_pin','builder_source_pin','scientific_child_source_pin','split_binder_source_pin','aggregation_engine_source_pin','plan_pin','inverse_pin']]+[pin(P/'SOURCE_REVIEW_READY_v2.json'),ready['writer_source_pin']]
for q in own+[ready['Source_author_pin']]:require(pin(q['path'])==q,'exact actual selected Source pin')
require(ready['source_only']is True and plan['source_only']is True and ready['physics_qualified']is False and plan['prior_aggregation_mathematical_qualification_claimed']is False,'Source only no invented scientific qualification')
for key in ['business_executed','compiler_executed','numerical_executed','files_deleted']:
    require(ready[key]is False and plan[key]is False,'no business in candidate')
for key in ['actual_request_pin','actual_aggregation_report_pin','future_Source_freeze_pin','future_Host_freeze_pin','future_dynamic_interface_pin']:require(ready[key]is None,'unknown future remains None')
ei=read(iv['predecessor_empty_root_whole_engine_inverse_pin']['path']);require(pin(iv['predecessor_empty_root_whole_engine_inverse_pin']['path'])==iv['predecessor_empty_root_whole_engine_inverse_pin'],'exact predecessor engine proof')
engine=Path(ready['aggregation_engine_source_pin']['path']).read_bytes();oldengine=base64.b64decode(ei['original_engine_whole_bytes_base64']);require(engine==base64.b64decode(ei['candidate_engine_whole_bytes_base64']),'actual complete engine')
a=ei['candidate_inventory_complete_block'];b=ei['original_inventory_complete_block'];require(engine.decode().count(a)==1 and engine.decode().replace(a,b,1).encode()==oldengine,'whole engine inverse only inventory')
builder=Path(ready['builder_source_pin']['path']).read_bytes();require(builder==base64.b64decode(iv['candidate_builder_whole_bytes_base64']),'actual complete builder')
require(builder.decode().count(iv['candidate_cumulative_request_write_block'])==1 and builder.decode().replace(iv['candidate_cumulative_request_write_block'],iv['original_request_write_block'],1).encode()==base64.b64decode(iv['original_builder_whole_bytes_base64']),'whole builder inverse only cumulative metadata')
writer=Path(ready['writer_source_pin']['path']).read_bytes();require(writer==base64.b64decode(iv['candidate_writer_whole_bytes_base64']),'actual complete writer')
back=writer.decode()
for row in reversed(iv['writer_exact_original_candidate_blocks']):
    require(back.count(row['candidate'])==1,'unique writer inverse splice');back=back.replace(row['candidate'],row['original'],1)
require(back.encode()==base64.b64decode(iv['original_writer_whole_bytes_base64']) and len(iv['writer_exact_original_candidate_blocks'])==5,'whole writer inverse five exact metadata splices')
copies=ei['source_copies']+iv['source_copies']
for row in copies:
    require(pin(row['predecessor_pin']['path'])==row['predecessor_pin'] and pin(row['candidate_pin']['path'])==row['candidate_pin'],'actual copy pins')
    require(Path(row['predecessor_pin']['path']).read_bytes()==Path(row['candidate_pin']['path']).read_bytes(),'whole unchanged Source copy')
require(len(plan['complete_source_file_pins_candidate'])==13,'all original13 Source rows')
for q in plan['complete_source_file_pins_candidate']:require(pin(q['path'])==q,'all13 current Source bytes')
require(plan['macro_total_record_count']==19620 and plan['macro_descendant_record_count']==19619 and plan['macro_empty_typed_root_count']==1 and plan['root_payload_is_empty_not_removed']is True,'exact split root contract')
oldrequest=read(plan['retained_actual_prior_aggregation_request_pin']['path']);oldhost=read(plan['retained_actual_prior_aggregation_report_pin']['path'])
for k in ['retained_actual_prior_aggregation_request_pin','retained_actual_prior_aggregation_report_pin','retained_actual_prior_aggregation_child_report_pin']:require(pin(plan[k]['path'])==plan[k],'actual prior aggregate metadata PF')
require(oldrequest['joint_archive_roots']==plan['retained_prior_joint_archive_roots'] and len(oldrequest['joint_archive_roots'])==8 and oldhost['operation']=='aggregate' and oldhost['failure']is None and oldhost['after_check_error']is None and oldhost['actual_intentional_exit2_normal_closure']is True,'prior actual evidence closure only')
newbase=['/Users/wen/spot/validation/artifacts/axial-material-current-first-A-empty-root-cumulative12-aggregate-20261014-v2','/Users/wen/spot/validation/artifacts/axial-material-current-first-A-empty-root-cumulative12-aggregate-20261014-v2-evidence',oldrequest['exact_retained_original_observed_root'],str(P),str(REC/'first_A_empty_root_cumulative12_aggregate_request_20261014_v2'),oldrequest['exact_retained_completion_metadata_root'],oldrequest['joint_archive_roots'][6],oldrequest['joint_archive_roots'][7]]
roots=newbase+[q for q in oldrequest['joint_archive_roots']if q not in newbase]
require(len(set(roots))==12 and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'complete union12 disjoint same original cap')
require('current_request[\'joint_archive_roots\']' not in builder.decode(),'no invented alternate request variable')
tree=ast.parse(engine);cls=next(n for n in tree.body if isinstance(n,ast.ClassDef)and n.name=='DiskEvidence');method=next(n for n in cls.body if isinstance(n,ast.FunctionDef)and n.name=='inventory')
namespace=dict(require=require);exec(compile(ast.Module(body=[method],type_ignores=[]),'<actual inventory guard only>','exec'),namespace)
root=dict(path=['MACROLIB'],kind=0,declared_count=-1,original_word_count=-1,native_payload_begin_byte=65443676,native_payload_end_byte=65443676,native_payload_sha256='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
def fixture(rootrow, descendants=19619, rootcopies=1):
    def rows():
        for _ in range(rootcopies):yield dict(record=rootrow)
        for number in range(descendants):yield dict(record=dict(path=['MACROLIB','GROUP',number]))
    saved=SimpleNamespace(iter_all=rows,iter_raw=lambda row:iter(()),row=lambda path:rootrow)
    obj=SimpleNamespace(saved=saved,records=0,macro_records=0,coverage=None,line=lambda *x:None,event=lambda *a,**k:None)
    namespace['inventory'](obj)
    return obj.records,obj.macro_records
require(fixture(root)==(19620,19620),'full descendants plus typed root accepted')
rejections=[]
for key,value in [('kind',False),('kind',1),('declared_count',0),('original_word_count',0),('native_payload_end_byte',65443680),('native_payload_sha256','0'*64)]:
    q=dict(root);q[key]=value
    try:fixture(q)
    except RuntimeError:rejections.append(key)
    else:raise RuntimeError('bad root fixture accepted')
for count,copiesn in [(19618,1),(19619,0),(19619,2)]:
    try:fixture(root,count,copiesn)
    except RuntimeError:rejections.append('coverage_count')
    else:raise RuntimeError('incomplete or duplicate root accepted')
require(len(rejections)==9,'meaningful inventory guard rejection boundary')
for q in own:require(pin(q['path'])==q,'final selected Source pin')
DEST.mkdir()
report=dict(schema='INDEPENDENT_EMPTY_MACROLIB_ROOT_CUMULATIVE12_CANDIDATE_WRITER_SOURCE_REVIEW_V1',status='PASS_EMPTY_MACROLIB_ROOT_CUMULATIVE12_CANDIDATE_WRITER_SOURCE_ONLY',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,complete_reviewed_Source_pins=own,host_source_pin=ready['host_source_pin'],builder_source_pin=ready['builder_source_pin'],scientific_child_source_pin=ready['scientific_child_source_pin'],split_binder_source_pin=ready['split_binder_source_pin'],aggregation_engine_source_pin=ready['aggregation_engine_source_pin'],plan_pin=ready['plan_pin'],inverse_pin=ready['inverse_pin'],writer_source_pin=ready['writer_source_pin'],Ready_pin=pin(P/'SOURCE_REVIEW_READY_v2.json'),reviewer_source_pin=pin(__file__),all_three_whole_byte_inverses_verified=True,actual_unchanged_source_copy_count=len(copies),complete_source_count=13,inventory_actual_AST_fixture_acceptance_count=1,inventory_actual_AST_fixture_rejection_count=len(rejections),all_original_19619_descendants_and_empty_typed_root_retained=True,complete_cumulative_joint_roots=roots,complete_joint_root_count=12,original_joint2GiB_caps_and_math_unchanged=True,no_scientific_payload_SQL_or_native_tree_read=True,actual_new_aggregate_report_pin=None,actual_GENDF_report_pin=None,physics_qualified=False,goal_complete=False)
q=DEST/'REVIEW.json'
with q.open('xb')as f:f.write((json.dumps(report,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
d=os.open(DEST,os.O_RDONLY|os.O_DIRECTORY);os.fsync(d);os.close(d)
print(json.dumps(dict(status=report['status'],review_pin=pin(q))))
