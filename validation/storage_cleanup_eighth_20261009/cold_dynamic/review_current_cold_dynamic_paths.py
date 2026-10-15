import ast
import hashlib
import json
from pathlib import Path
import stat

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
OUT=Path('/private/tmp/spot_eighth_storage_independent_source_review_20261009')
COLD=Path('/private/tmp/axmat-last-cprime-trim-cold-v7-input-v5-draft-20261009/prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py')
CONSUMER=COLD.with_name('cold_component_input_consumer_last_cprime_trim_own_pid_peak.py')
BASE=ART/'axial-material-production-qualified-AB-rank1-factor-cache-20261007'
OLD=ART/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005'

def pin(p,wanted=None):
    p=Path(p);s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
    assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
    raw=p.read_bytes();a=p.lstat();after=[a.st_dev,a.st_ino,a.st_mode,a.st_size,a.st_mtime_ns,a.st_ctime_ns,a.st_nlink]
    assert before==after
    h=hashlib.sha256(raw).hexdigest()
    if wanted:assert h==wanted,str(p)
    return dict(path=str(p),sha256=h,size=len(raw),identity=before),raw

def main():
    candidates=json.loads((OUT/'independent_material_seed_exact_candidates.json').read_text())
    paths={r['path'] for r in candidates['selected']}
    sources=[];metadata=[];protected={};intersections=[]
    def add(path,wanted,reason):
        path=str(path)
        assert path.startswith('/'),path
        if path not in protected:protected[path]=dict(path=path,sha256=wanted,roles=[])
        assert protected[path]['sha256']==wanted,(path,wanted,protected[path]['sha256'])
        protected[path]['roles'].append(reason)
    def read(p,wanted=None):
        item,raw=pin(p,wanted);metadata.append(item);return json.loads(raw)
    def source(p,wanted,names):
        item,raw=pin(p,wanted);s=raw.decode();tree=ast.parse(s);defs=[]
        for n in tree.body:
            if isinstance(n,ast.FunctionDef) and n.name in names:
                seg=ast.get_source_segment(s,n)
                defs.append(dict(name=n.name,line=n.lineno,end_line=n.end_lineno,source_sha256=hashlib.sha256(seg.encode()).hexdigest(),source=seg))
        sources.append(dict(**item,definitions=defs));return s
    coldtext=source(COLD,'ceaf7f8e0c876fd3ecee5e171a706db5b0af794526c7f74232f3c5b650b3dd0f',['prepare','normal_runtime_preload','render_controller','write_controller','base_component_prepared'])
    source(CONSUMER,'39e114aa2304b08e504a9803f7d12dda7bcb335fcc1341cd0c3814a80c53c3f8',[])
    source(BASE/'runtime/production_runner.py','844fe18738a2232d2947a8c65dc13afebcfbfd2e2afc9f0743c1c94c06fd0f7d',['prepare','preflight'])
    source(BASE/'runtime/qualified_snapshot_ingestion.py',None,['verify_offline_state','admit_snapshots'])
    source(OLD/'runtime/production_runner.py','38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128',['prepare','preflight'])
    source(OLD/'runtime/qualified_snapshot_ingestion.py','4ea482a6f3536bdb61e0de2c0693a8f128893fd7e0ecdaa72b7bd424645f8658',['verify_offline_state','admit_snapshots'])
    per_parent=[]
    for label,base,want in [('BASE',BASE,'7d2154e9c722eab23f4411c9a8588ed8250da658ae880298c24dfb53308656b5'),('OLD',OLD,'024ffb9263e3d3b6cf10301d6fe2bac5a87a9b368008440e01038982291a6d53')]:
        prepared=read(base/'prepared.json',want)
        for field,item in prepared['inputs'].items():add(item['path'],item['sha256'],label+'/prepared.inputs/'+field)
        item=prepared['inputs']['material_results'];receipt=read(item['path'],item['sha256'])
        add(receipt['producer_runtime']['path'],receipt['producer_runtime']['sha256'],label+'/producer_runtime')
        add(receipt['receiver_source']['path'],receipt['receiver_source']['sha256'],label+'/receiver_source')
        per_state=[]
        for letter,state in receipt['states'].items():
            for field,item in state.items():
                if isinstance(item,dict) and set(item)>=set(['path','sha256']):add(item['path'],item['sha256'],label+'/'+letter+'/state/'+field)
            item=state['execution'];execution=read(item['path'],item['sha256'])
            for p,w in execution['files'].items():add(p,w,label+'/'+letter+'/verify_offline_state.execution.files')
            ehits=sorted(paths&set(execution['files']))
            item=state['snapshot_run_status'];run=read(item['path'],item['sha256']);directory=Path(state['archive']['path']).parent
            for name,w in run['outputs'].items():add(directory/name,w,label+'/'+letter+'/verify_offline_state.run.outputs')
            item=state['audit_status'];audit=read(item['path'],item['sha256']);auditdir=Path(item['path']).parent
            add(auditdir/'protocol.json',audit['protocol_sha256'],label+'/'+letter+'/audit.protocol')
            protocol=read(auditdir/'protocol.json',audit['protocol_sha256'])
            for p,w in protocol['files'].items():add(p,w,label+'/'+letter+'/verify_offline_state.audit.protocol.files')
            for name,w in audit['outputs'].items():add(auditdir/name,w,label+'/'+letter+'/verify_offline_state.audit.outputs')
            phits=sorted(paths&set(protocol['files']))
            per_state.append(dict(state=letter,execution_path=state['execution']['path'],execution_sha256=state['execution']['sha256'],execution_file_count=len(execution['files']),execution_candidate_intersection=ehits,audit_protocol_sha256=audit['protocol_sha256'],audit_protocol_candidate_intersection=phits))
        # Factory preserves the original receipt states while changing only receiver metadata.
        variant=read(base/'runtime/conditional_white_receiver_variant.json')
        for p,w in variant['files'].items():add(p,w,label+'/controller.runtime_sources.variant.files')
        per_parent.append(dict(parent=label,prepared_path=str(base/'prepared.json'),prepared_sha256=want,receipt_path=item['path'] if False else prepared['inputs']['material_results']['path'],receipt_sha256=prepared['inputs']['material_results']['sha256'],state_intersections=per_state))
    hitpaths=paths&set(protected)
    # Fresh complete reads independently confirm only prospective 42 material/seed intersections.
    for p in sorted(hitpaths):
        item,raw=pin(p,protected[p]['sha256']);protected[p]['candidate_fresh_file_pin']=item
    material_manifest=read(Path(json.loads((OLD/'prepared.json').read_text())['inputs']['material_manifest']['path']))
    # All absolute scientific descriptors in the current original material manifest are conservative path protection.
    def descriptor_walk(d,label):
        if isinstance(d,dict):
            if isinstance(d.get('path'),str) and d['path'].startswith('/') and isinstance(d.get('sha256'),str):add(d['path'],d['sha256'],label)
            for k,v in d.items():descriptor_walk(v,label+'/'+k)
        elif isinstance(d,list):
            for i,v in enumerate(d):descriptor_walk(v,label+'/'+str(i))
    descriptor_walk(material_manifest,'OLD/current_original_material_manifest')
    # Documentary source evidence only; no rendering/patching/importing current controller.
    call_chain=[dict(source=str(COLD),caller='prepare',callee='normal_runtime_preload + c.prepare',detail='Cold prepare child normally preloads the generated production_runner and explicitly invokes c.prepare(declaration, expected, OUTPUT).'),dict(source=str(BASE/'runtime/production_runner.py'),caller='prepare',callee='preflight',line=559),dict(source=str(BASE/'runtime/production_runner.py'),caller='preflight',callee='qualified_snapshot_ingestion.admit_snapshots',line=422),dict(source=str(BASE/'runtime/qualified_snapshot_ingestion.py'),caller='admit_snapshots',callee='verify_offline_state',line=157),dict(source=str(BASE/'runtime/qualified_snapshot_ingestion.py'),caller='verify_offline_state',callee='digest every execution.files path',lines=[92,93,94])]
    result=dict(status='HOLD_ALL_42_MATERIAL_SEED_CANDIDATES_CURRENT_COLD_DYNAMIC_DEPENDENCY',source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),prior_exact_report_sha256=hashlib.sha256((OUT/'independent_material_seed_exact_candidates.json').read_bytes()).hexdigest(),candidate_count=42,explicit_dynamic_candidate_intersection_count=len(hitpaths),explicit_dynamic_candidate_intersection=sorted(hitpaths),remaining_11_material_candidate_paths=sorted(paths-hitpaths),approved_deletion_paths=[],source_pins_and_actual_function_definitions=sources,actual_pinned_metadata=metadata,actual_parent_receipt_intersections=per_parent,current_cold_dynamic_protected_files=sorted(protected.values(),key=lambda r:r['path']),current_cold_dynamic_protected_count=len(protected),call_chain=call_chain,why_hold='31 exact copies are still read by current next cold PREP through unchanged original offline producer admission. The other 11 were not proven free from every relevant dynamic consumer in this bounded review. Parent requested HOLD when any live cold path intersects; no deletion approval is given for the 42.',scope_limits=['Future cold/intake is STOPPED with successful terminal fields unknown; this is static intended-next-source dependency evidence, not execution credit.','Protected map records expected historical bytes from real prepared/receipt/execution/protocol metadata. Only the 31 candidate files were fresh-read as large data in this supplement; no claim that every protected path currently exists/passes all scientific gates.','Renderer source and original callback bodies are included for independent review; no business renderer/import/prepare/API ran.','Original documents, result records, code, manifests, all main inputs and final scientific results remain unchanged.'],files_deleted=0,solver_or_API_executed=False,formal_or_artifact_writes=False)
    target=OUT/'current_cold_dynamic_protected_files.json'
    with target.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status=result['status'],path=str(target),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),protected_count=len(protected),candidate_intersection=len(hitpaths),candidate_paths_approved_for_deletion=0)))

if __name__=='__main__':main()
