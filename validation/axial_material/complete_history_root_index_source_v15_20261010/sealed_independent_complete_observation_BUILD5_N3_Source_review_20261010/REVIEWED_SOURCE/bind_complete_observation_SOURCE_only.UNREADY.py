"""Finite Source-only observer host binder. Reads Source and real small META only.
Never opens numeric libraries/decks/context/XSM/SQL payload, imports a candidate,
compiles, launches a child, or creates an actual observation/runtime qualification.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat

P=Path(__file__).resolve().parent
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FUTURE=dict(actual_runtime_qualification_sha256=None,actual_observer_native_controls_run=None,actual_native_Source_binary_linkage_qualification_sha256=None,actual_scientific_qualification_sha256=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_transport_executed=False,complete_context_aggregation_qualified=False)
ROLES={'qualified_source_manifest':'MANIFEST.json','host_template':'complete_observation_genuine_host.UNREADY.py','runtime_template':'complete_observation_BUILD5_AB_runtime.UNREADY.py','binder':'bind_complete_observation_SOURCE_only.UNREADY.py','postclose_writer':'Root_observation_postclose_META_writer.UNREADY.py','native_Source_archive':'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','native_Source_index':'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json','observer_module':'OBSERVATION_SOURCE/AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90','context_extractor':'OBSERVATION_SOURCE/extract_actual_complete_context_with_SPH_decisions.UNREADY.py','original_complete_native_walker':'PARENT_SOURCE/Root_bound_complete_native_checker.py','original_material_seed_contract':'ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json','material_blueprint_Source':'GUARD_SOURCE/material_inputs.py','request_preparer':'Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','legacy_context_old_XSM_extractor':'COMPLETE_LEGACY_CONTEXT_HANDOFF_SOURCE/complete_observed_old_post_final_XSM_extractor.UNREADY.py'}

def require(v,m):
    if type(v)is not bool or not v:raise ValueError(m)

def strict_json(raw):
    def pairs(items):
        d={}
        for k,v in items:require(k not in d,'duplicate Source-only request key');d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))

def pin(path):
    p=Path(path);s=p.lstat();ident=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];require(p.is_absolute()and all(not x.is_symlink()for x in(p,*p.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1,'regular single-link nonalias Source/META')
    with p.open('rb')as stream:d=hashlib.file_digest(stream,'sha256').hexdigest()
    t=p.lstat();require([t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==ident,'full Source/META EOF unchanged')
    return dict(path=str(p),sha256=d,size_bytes=s.st_size,identity=ident)

def shape(p):
    require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['path'])is str and Path(p['path']).is_absolute()and '..'not in Path(p['path']).parts and type(p['sha256'])is str and re.fullmatch('[0-9a-f]{64}',p['sha256'])is not None,'exact complete input pin shape')
    require(type(p['size_bytes'])is int and p['size_bytes']>=0 and type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int and v>=0 for v in p['identity'])and p['identity'][3]==1 and p['identity'][4]==p['size_bytes'],'strict integer7ID/size; no bool/equalfloat')

def metadata(p):shape(p);require(pin(p['path'])==p,'actual small META pin');return strict_json(Path(p['path']).read_bytes())

def write_new(path,value):
    with Path(path).open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

def replace_assignments(raw,changes):
    text=raw.decode();lines=text.splitlines(keepends=True);found={};hunks=[]
    for node in ast.parse(text).body:
        if isinstance(node,ast.Assign)and len(node.targets)==1 and isinstance(node.targets[0],ast.Name)and node.targets[0].id in changes:
            key=node.targets[0].id;require(key not in found,'one exact bound global');found[key]=node;old=''.join(lines[node.lineno-1:node.end_lineno]);new=key+' = '+repr(changes[key])+'\n';hunks.append(dict(key=key,line=node.lineno,old=old,new=new))
    require(set(found)==set(changes),'every exact global present')
    for h in sorted(hunks,key=lambda x:x['line'],reverse=True):node=found[h['key']];lines[node.lineno-1:node.end_lineno]=[h['new']]
    result=''.join(lines).encode();ast.parse(result)
    inverse=result
    for h in hunks:require(inverse.count(h['new'].encode())==1,'unique full hunk inverse');inverse=inverse.replace(h['new'].encode(),h['old'].encode(),1)
    require(inverse==raw,'whole Source inverse exact original bytes')
    return result,hunks

def main():
    cli=argparse.ArgumentParser();cli.add_argument('--source-manifest-sha256',required=True);cli.add_argument('--request',required=True);cli.add_argument('--request-sha256',required=True);cli.add_argument('--output-source-dir',required=True);a=cli.parse_args()
    actual=pin(P/'MANIFEST.json');require(actual['sha256']==a.source_manifest_sha256,'complete author manifest actual SHA')
    mf=strict_json((P/'MANIFEST.json').read_bytes());require(mf['schema']=='COMPLETE_NATIVE_OBSERVATION_BUILD5_AB_UNREADY_SOURCE_MANIFEST_V1'and mf['source_only']is True and mf['status']=='UNREADY_SOURCE_ONLY_REQUIRES_INDEPENDENT_REVIEW','whole author Source manifest scope')
    members=mf['members'];require(type(members)is list and len(members)>0 and len({x['relative_path']for x in members})==len(members),'whole manifest file coverage')
    known=set()
    for row in members:
        rel=Path(row['relative_path']);require(not rel.is_absolute()and '..'not in rel.parts,'strict Source relative member');require(pin(P/rel)==row['fullpin'],'whole complete Source body/member EOF');known.add(str(rel))
    require({str(p.relative_to(P))for p in P.rglob('*')if p.is_file()}==known|{'MANIFEST.json'},'no omitted Source members')
    author={k:pin(P/v)for k,v in ROLES.items()};request_path=Path(a.request);rp=pin(request_path);require(rp['sha256']==a.request_sha256,'exact actual Root request Source SHA');b=strict_json(request_path.read_bytes())
    require(b['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_BUILD_BINDING_REQUEST_V1'and b['source_only']is True and b['Root_only_actual_execution']is True and b['scientific_qualification_created']is False,'actual Root request scope')
    require(b['actual_author_Source_contract']==author and b['original_caps']==CAPS and all(type(v)is int for v in b['original_caps'].values())and b['state_order']==['A','B']and b['build_stage_order']==['Ganlib','Utilib','Trivac','Dragon','Dragon_link']and b['SPOT_AXMAT_OBSERVATION']=='ADMITTED_SOURCE_ONLY','full Source/caps/order/env exact')
    for k,v in FUTURE.items():require(b[k]is v,'future actual facts unknown/false')
    seed_contract=strict_json((P/'ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json').read_bytes());require(b['original129_input_pins']==seed_contract['original129_input_pins'],'original129 fullpins cannot be silently refreshed/replaced');rows=b['original129_input_pins'];extra=b['additional_actual_evidence_input_pins'];require(type(rows)is list and len(rows)==129 and type(extra)is list and bool(extra)and len({p['path']for p in rows+extra})==len(rows+extra),'all original129 plus unique nonempty actual extra inputs')
    for p in rows+extra:shape(p)
    allpins={p['path']:p for p in rows+extra}
    peer=metadata(b['independent_observation_Source_review_pin']);ad=metadata(b['independent_observation_Source_admission_pin']);truth=metadata(b['actual_Root_observation_Source_admission_tool_return_pin'])
    require(peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_BINDER_SOURCE_REVIEW_V1'and peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and peer['source_only']is True and peer['all_checks_passed']is True and peer['blockers']==[] and peer['actual_author_Source_contract']==author,'actual independent observer Source pass exact scope')
    checks=peer['checks'];require(type(checks)is list and type(peer['check_count'])is int and peer['check_count']==len(checks)>0 and all(type(c)is dict and set(c)=={'check','passed'}and type(c['check'])is str and bool(c['check'])and c['passed']is True for c in checks)and len({c['check']for c in checks})==len(checks),'actual aggregate checks true/count/unique')
    require(ad['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_V1'and ad['status']=='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE'and ad['source_only']is True and ad['scientific_qualification_created']is False and ad['actual_author_Source_contract']==author and ad['independent_Source_review_pin']==b['independent_observation_Source_review_pin'],'actual Root Source admission exact whole source/peer')
    for k,v in FUTURE.items():require(ad[k]is v,'admission future flags unknown/false')
    terminal=truth['terminal_tool_return'];require(truth['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1'and truth['closed']is True and truth['observed_terminal']is True and truth['session_repolled_after_close']is False and type(terminal['exit_code'])is int and terminal['exit_code']==0 and 'session_id'not in terminal and type(terminal['chunk_id'])is str and bool(terminal['chunk_id'])and truth['actual_terminal_chunk']==terminal['chunk_id'],'actual Root typed0 CLOSED Source admission')
    stdout=strict_json(terminal['output']);require(stdout['source_only']is True and stdout['status']=='ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE'and stdout['source_admission_pin']==b['independent_observation_Source_admission_pin'],'actual Root admission output fullpin coupling')
    for k in('independent_observation_Source_review_pin','independent_observation_Source_admission_pin','actual_Root_observation_Source_admission_tool_return_pin'):require(allpins.get(b[k]['path'])==b[k],'all actual Source evidence protected')
    require(type(b['tool_pins'])is dict and set(b['tool_pins'])=={'fortran','c','cpp','ar','lsof','ps'},'all actual tool Source request pins')
    for p in b['tool_pins'].values():shape(p);require(allpins.get(p['path'])==p,'all actual toolpins protected')
    needed={'material.x2m','AxMatTone.c2m','geometry.dat','rnr_cc.c2m','rnr_interpol.c2m','DLIB_ACTUAL','DLIB8R1_370'};require(type(b['states'])is dict and list(b['states'])==['A','B'],'ordered full A/B native input shape')
    for state in('A','B'):
        stage=b['states'][state]['native_stage_inputs'];require(type(stage)is list and len(stage)==7 and {r['destination']for r in stage}==needed,'complete original material seed mapping')
        for r in stage:require(type(r)is dict and set(r)=={'destination','input_pin'},'exact seed row');shape(r['input_pin']);require(allpins.get(r['input_pin']['path'])==r['input_pin'],'all seedpins protected without payload reads')
        require(b['states'][state]['original_material_deck_pin']==next(r['input_pin']for r in stage if r['destination']=='material.x2m'),'exact original immutable deck source')
        for row in stage:
            destination=row['destination'];expected=seed_contract['states'][state].get(destination)
            if expected is not None:require(row['input_pin']==expected,'same original full physical input pin: '+destination)
            else:require(row['input_pin']['path']==seed_contract['libraries'][destination]['path']and row['input_pin']['sha256']==seed_contract['libraries'][destination]['generation_sha256'],'same original material library generation SHA/path')
    ns=b['namespaces'];require(type(ns)is dict and set(ns)=={'host','output','control','source','receipts'},'exact H/O/C/D/E');roots=[Path(ns[k])for k in('host','output','control','source','receipts')];art=Path('/Users/wen/spot/validation/artifacts');base=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
    require(len(set(roots))==5 and not any(p.is_relative_to(q)for p in roots for q in roots if p!=q),'disjoint roots');require(all(p.is_absolute()and '..'not in p.parts and all(not q.is_symlink()for q in(p,*p.parents))for p in roots),'no aliases');require(all(p!=art and p.is_relative_to(art)for p in roots[:3])and all(p!=base and p.is_relative_to(base)for p in roots[3:]),'original Root namespaces');require(not any(os.path.lexists(p)for p in roots[:4])and roots[4].is_dir(),'H/O/C/D fresh and E actualpreexistingSource receipts')
    out=Path(a.output_source_dir);require(out==roots[3]and out!=P and not out.is_relative_to(P)and not P.is_relative_to(out),'bound full D Source matchesrequest')
    before={str(p.relative_to(P)):pin(p)for p in P.rglob('*')if p.is_file()};out.mkdir()
    for p in P.rglob('*'):
        rel=p.relative_to(P);target=out/rel
        if p.is_dir():target.mkdir()
        else:shutil.copy2(p,target)
    runtime,hunks=replace_assignments((P/ROLES['runtime_template']).read_bytes(),{'SOURCE_STATUS':'READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'});runtime_path=out/'Root_bound_complete_observation_runtime.py';runtime_path.write_bytes(runtime);runtime_pin=pin(runtime_path)
    binding=dict(b);binding['schema']='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_BUILD_BINDING_V1';binding['actual_original_Root_request_pin']=rp;binding['bound_runtime_pin']=runtime_pin;binding['actual_observer_native_execution']=None;binding_path=out/'Root_actual_observation_SOURCE_binding.json';write_new(binding_path,binding);binding_pin=pin(binding_path)
    replacements={'SOURCE_STATUS':'READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED','SOURCE_ARCHIVE':str(out),'RECEIPTS':ns['receipts'],'HOST':ns['host'],'OUT':ns['output'],'CONTROL':ns['control'],'TARGET':str(runtime_path),'TARGET_SHA':runtime_pin['sha256'],'BINDING':str(binding_path),'BINDING_SHA':binding_pin['sha256'],'SOURCE_ADMISSION_SHA':b['independent_observation_Source_admission_pin']['sha256']}
    raw=(P/ROLES['host_template']).read_bytes();host,hunks_host=replace_assignments(raw,replacements);host_path=out/'Root_bound_complete_observation_genuine_host.py';host_path.write_bytes(host)
    write_new(out/'Root_actual_observation_bound_Source_full_inverse.json',dict(schema='ROOT_ACTUAL_OBSERVATION_BOUND_SOURCE_FULL_INVERSE_V1',source_only=True,host_original_Source_pin=author['host_template'],runtime_original_Source_pin=author['runtime_template'],bound_host_pin=pin(host_path),bound_runtime_pin=runtime_pin,host_complete_inverse_hunks=hunks_host,runtime_complete_inverse_hunks=hunks,all_other_Source_bytes_unchanged=True,actual_observer_native_execution=None,**FUTURE))
    require(before=={str(p.relative_to(P)):pin(p)for p in P.rglob('*')if p.is_file()},'all original Source immutable after Source-only binding')
    print(json.dumps(dict(status='BOUND_COMPLETE_OBSERVATION_SOURCE_ONLY_NOT_EXECUTED',source_only=True,bound_host_pin=pin(host_path),bound_runtime_pin=runtime_pin,binding_pin=binding_pin,wholeSourcefullinverse_pin=pin(out/'Root_actual_observation_bound_Source_full_inverse.json'),actual_observation_manifest=None,actual_Root_execution_required=True,**FUTURE),allow_nan=False),flush=True)
if __name__=='__main__':main()
