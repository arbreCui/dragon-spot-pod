"""Author Source writer only: bytes/AST/META. Never imports/executes a candidate."""
import ast
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat

P=Path('/private/tmp/axmat_N8_exact_owner_complete_UNREADY_Source_mjczixe4')
MOTHER=Path('/private/tmp/axmat_complete_native_observation_N7_failure_only_monitor_UNREADY_Source_piquf6v6')
MOTHER_SHA='178b885f37bf7c65cdd3375f9be29bd53c7b7e408aa61011894d25bb23cee928'
ROLES=['complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py']

def pin(p):
    p=Path(p);s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    assert p.is_absolute() and stat.S_ISREG(s.st_mode) and s.st_nlink==1 and not any(q.is_symlink() for q in (p,*p.parents))
    with p.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    t=p.lstat();assert [t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==before
    return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=before)

def write(p,obj):
    with p.open('x') as f:json.dump(obj,f,indent=2,allow_nan=False);f.write('\n')

def replace_once(raw,old,new):
    assert raw.count(old)==1,(old[:100],raw.count(old))
    return raw.replace(old,new,1)

def insert_def(raw,name,source):
    nodes=[n for n in ast.parse(raw).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name]
    assert len(nodes)==1
    n=nodes[0];lines=raw.splitlines(keepends=True)
    return ''.join(lines[:n.lineno-1])+source+'\n'+''.join(lines[n.lineno-1:])

def main():
    assert pin(MOTHER/'MANIFEST.json')['sha256']==MOTHER_SHA
    mf=json.loads((MOTHER/'MANIFEST.json').read_bytes());assert len(mf['members'])==181
    saved=P/'PREVIOUS_SEALED_N7_SOURCE_PROVENANCE';saved.mkdir()
    shutil.copy2(MOTHER/'MANIFEST.json',saved/'MANIFEST.json')
    original_members=[]
    for row in mf['members']:
        rel=Path(row['relative_path']);assert pin(MOTHER/rel)==row['fullpin']
        dst=P/rel;dst.parent.mkdir(parents=True,exist_ok=True);assert not dst.exists();shutil.copy2(MOTHER/rel,dst)
        original_members.append(dict(relative_path=str(rel),mother_fullpin=row['fullpin'],new_original_copy_fullpin=pin(dst)))
    gate=(P/'N8_actual_controls_qualification_gate.Source_META_only.py').read_text()
    gate=gate[gate.index('CASE_IDS='):]
    for name in ('require','strict_json','fullpin','recheck_pinned','read_pinned','actual_closed_zero'):
        import re
        gate=re.sub(r'\b'+name+r'\b','n8_'+name,gate)
    gate=gate.replace('CASE_IDS','N8_CASE_IDS')
    new_roles={'owner_scope_helper':'N8_exact_owner_scope_observer.UNREADY.py','monitor_controls_gate':'N8_actual_controls_qualification_gate.Source_META_only.py','monitor_controls_protocol':'N8_TWELVE_GENUINE_CONTROL_PROTOCOL.UNREADY.json','monitor_control_driver':'N8_genuine_integrated_controls_driver.UNREADY.py','monitor_control_child_Source':'N8_private_control_child.UNREADY.py','monitor_control_Source_binder':'N8_bind_monitor_controls_SOURCE_META_only.UNREADY.py','monitor_controls_postclose_qualifier':'N8_Root_controls_postclose_META.UNREADY.py'}
    inverse=[]
    for name in ROLES:
        old=(MOTHER/name).read_text();shutil.copy2(MOTHER/name,saved/name)
        raw=old.replace('REQUIRED_N7_FRESH_NAMESPACES','REQUIRED_N8_FRESH_NAMESPACES').replace('BUILD5-AB-v7-','BUILD5-AB-v8-').replace('BUILD5_AB_v7_','BUILD5_AB_v8_').replace('fixed v7','fixed v8').replace('ACTUAL_N7_FAILURE_ONLY_MONITOR','ACTUAL_N8_FAILURE_ONLY_MONITOR')
        if name in ROLES[:3]:
            if name!=ROLES[0]:
                node=next(n for n in ast.parse(raw).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ROLES' for t in n.targets))
                original_roles=ast.literal_eval(node.value);original_roles.update(new_roles)
                lines=raw.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['ROLES='+repr(original_roles)+'\n'];raw=''.join(lines)
            raw=insert_def(raw,'main' if name!=ROLES[0] else 'actual_scope',gate)
        if name==ROLES[1]:
            raw=replace_once(raw,"'request-output'):ap.add_argument", "'request-output','monitor-controls-qualification','monitor-controls-qualification-terminal'):ap.add_argument")
            anchor="    require(all(getattr(a,k)==v for k,v in CANONICAL_OS_TOOL_PATHS.items()),'all six original canonical OS tool CLI paths unchanged')"
            raw=replace_once(raw,anchor,"    monitor_q=pin(a.monitor_controls_qualification,deadline);monitor_q_terminal=pin(a.monitor_controls_qualification_terminal,deadline)\n    monitor_scope=validate_actual_N8_monitor_controls(monitor_q,monitor_q_terminal,author)\n"+anchor)
            raw=replace_once(raw,'[review,admission,terminal,*tools.values(),*libraries.values()]','[review,admission,terminal,monitor_q,monitor_q_terminal,*tools.values(),*libraries.values()]')
            raw=replace_once(raw,'actual_author_Source_contract=author,independent_observation_Source_review_pin=review','actual_author_Source_contract=author,actual_monitor_controls_qualification_pin=monitor_q,actual_monitor_controls_qualification_terminal_pin=monitor_q_terminal,actual_required_monitor_controls_scope=monitor_scope,independent_observation_Source_review_pin=review')
        elif name==ROLES[2]:
            anchor="    seed_contract=strict_json((P/'ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json').read_bytes())"
            raw=replace_once(raw,anchor,"    monitor_scope=validate_actual_N8_monitor_controls(b['actual_monitor_controls_qualification_pin'],b['actual_monitor_controls_qualification_terminal_pin'],author)\n    require(b['actual_required_monitor_controls_scope']==monitor_scope,'actual required monitor Q coupling before Source binding')\n"+anchor)
            anchor="    allpins={p['path']:p for p in rows+extra}"
            raw=replace_once(raw,anchor,anchor+"\n    for p in (b['actual_monitor_controls_qualification_pin'],b['actual_monitor_controls_qualification_terminal_pin']):require(allpins.get(p['path'])==p,'actual monitor Q evidence protected in whole input list')")
        elif name==ROLES[0]:
            raw=replace_once(raw,"    expected=request['actual_author_Source_contract']","    expected=request['actual_author_Source_contract']\n    monitor_scope=validate_actual_N8_monitor_controls(request['actual_monitor_controls_qualification_pin'],request['actual_monitor_controls_qualification_terminal_pin'],author)\n    require(request['actual_required_monitor_controls_scope']==monitor_scope,'actual monitor controls complete Source coupling before native action')")
            raw=replace_once(raw,"def joint_bytes(roots,lsof_tool,ps_tool,monitor=None):","def joint_bytes(roots,lsof_tool,ps_tool,monitor=None,owner_observer=None,control_barrier=None):")
            raw=replace_once(raw,"        ps_argv=[ps_tool,'-axo','pid=,ppid=']","        require(control_barrier is None or (owner_observer is not None and owner_observer.control_mode is True),'no controls barrier in production scope')\n        if owner_observer is not None:owner_observer.poll_for_snapshot()\n        ps_started_monotonic=time.monotonic()\n        ps_argv=[ps_tool,'-axo','pid=,ppid=,pgid=,stat=']")
            raw=replace_once(raw,"        parents={int(a):int(b)for a,b in(line.split()for line in ps_stdout.splitlines())}","        require(len(ps_stdout)<8*2**20 and len(ps_stderr)<8*2**20,'complete bounded fullPS raw streams, never truncated')\n        ps_rows={}\n        for line in ps_stdout.splitlines():\n            words=line.split();require(len(words)==4 and all(w.isdigit()for w in words[:3])and bool(words[3]),'full actual PS pid/ppid/pgid/state rows')\n            pid,ppid,pgid=map(int,words[:3]);require(pid>0 and pid not in ps_rows,'unique positive fullPS PID');ps_rows[pid]=dict(pid=pid,ppid=ppid,pgid=pgid,state=words[3])\n        parents={pid:r['ppid']for pid,r in ps_rows.items()}")
            raw=replace_once(raw,"        selected.discard(ps_diagnostic_pid)\n        observed=subprocess.run", "        selected.discard(ps_diagnostic_pid)\n        if control_barrier is not None:control_barrier(ps_rows,selected)\n        if owner_observer is not None:\n            owner_observer.poll_for_snapshot()\n            selected=owner_observer.expand_selection(ps_rows,selected,ps_diagnostic_pid,ps_started_monotonic)\n        observed=subprocess.run")
            raw=replace_once(raw,"        require(len(observed.stdout)<8*2**20,'finite complete lsof output; never truncated')","        require(len(observed.stdout)<8*2**20 and len(observed.stderr)<8*2**20,'finite complete lsof streams; never truncated')\n        returned_pids=[]\n        for line in observed.stdout.splitlines():\n            if line.startswith('p'):require(line[1:].isdigit(),'actual lsof PID field');returned_pids.append(int(line[1:]))\n        require(set(returned_pids)==selected and len(returned_pids)==len(set(returned_pids)),'single strict lsof0 complete selected PID coverage; no absent-PID acceptance')")
            raw=replace_once(raw,"            original_PS_lsof_argv_timeout_and_PID_parent_chain_unchanged=True,\n            only_two_bounded_callable_objects_wrapped_for_failure_evidence=True,","            original_lsof_argv_and_single_strict_zero_timeout_unchanged=True,\n            full_PS_pid_ppid_pgid_state_and_captured_union_explicitly_new=True,\n            original_parent_chain_never_reduced_except_individually_proven_closed_owned_PIDs=True,\n            three_bounded_callable_objects_and_two_private_methods_per_actual_owned_Popen_declared=True,\n            actual_owner_scope_state=None if getattr(self.resources,'_exact_owner_observer',None)is None else self.resources._exact_owner_observer.summary(),")
            raw=replace_once(raw,"            new_instrumented_runtime_controls_actual=None,new_native_runtime_qualification=None,","            actual_required_new_monitor_controls_scope=getattr(self.resources,'_required_monitor_controls_scope',None),new_native_runtime_qualification=None,")
            start=raw.index('    monitor=None\n    class JointHistoryResources',raw.index('def run('))
            end=raw.index("    def budget():",start)
            original_factory=raw[start:end]
            factory='''def build_exact_owner_resources(support,roots5,tools,started,dfreeze,efreeze,history,genuine_modules):
    resource,full,production=genuine_modules
    require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'same actual original classes/MRO for production and controls')
    archive,receipts=map(Path,roots5[3:]);monitor=None
    class JointHistoryResources(resource.DynamicHistoryResources):
        def check(self):
            value=super().check()
            joint=joint_bytes(roots5,tools['lsof']['path'],tools['ps']['path'],monitor,getattr(self,'_exact_owner_observer',None),getattr(self,'_actual_control_barrier',None));require(joint['complete_joint_HOCDE_bytes']<2*2**30,'live full jointHOCDE including open-unlinked2GiB')
            require(tree(archive)==dfreeze and tree(receipts)==efreeze,'complete D/E and all directory/fullSource identities frozen while live')
            require(value['artifact_bytes']+sum(p['size_bytes']for p in dfreeze['files']+efreeze['files'])+joint['open_unlinked_bytes']<=96*2**30,'complete history plus external D/E')
            if monitor is not None:monitor.latest_joint=dict(joint)
            sink=getattr(self,'_actual_control_scan_sink',None)
            if sink is not None:
                require(self._exact_owner_observer is not None and self._exact_owner_observer.control_mode is True,'full raw sink only in actual controls mode')
                sink(joint,monitor.latest_original_scan,self._exact_owner_observer.summary())
            value.update(joint);return value
    resources=JointHistoryResources(support.ART,history,8*2**30,96*2**30,production.ResourceFailure)
    resources._genuine_full=full;resources._exact_owner_observer=None;resources._actual_control_barrier=None;resources._actual_control_scan_sink=None
    monitor=FailureOnlyMonitorEvidence(roots5,tools,started,resources,resource.DynamicHistoryResources.check,dfreeze,efreeze)
    resources._failure_only_monitor=monitor
    return resources,monitor

def attach_exact_owner_observer(runner,resources,monitor,stdlib_pin,started,deadline_getter,helper_source_pin,support,control_mode=False):
    recheck(helper_source_pin)
    module,actual=support.load(Path(helper_source_pin['path']),helper_source_pin['sha256'],'axmat_N8_exact_owner_scope_Source')
    require(actual=={k:helper_source_pin[k]for k in actual},'complete actual owner helper Source pin')
    observer=module.ExactOwnerScopeObserver(runner,resources,monitor,resources._genuine_full,stdlib_pin,started,deadline_getter,control_mode)
    observer.install_original_start_capture();resources._exact_owner_observer=observer
    return observer

'''
            raw=raw[:start]+"    resources,monitor=build_exact_owner_resources(support,roots5,b['tool_pins'],started,dfreeze,efreeze,history,(resource,full,production));runner=None;owner_observer=None\n    resources._required_monitor_controls_scope=b['actual_required_monitor_controls_scope']\n"+raw[end:]
            raw=insert_def(raw,'run',factory)
            raw=replace_once(raw,"        monitor.install_bounded_wrappers(runner)","        monitor.install_bounded_wrappers(runner)\n        owner_observer=attach_exact_owner_observer(runner,resources,monitor,b['actual_required_monitor_controls_scope']['actual_stdlib_subprocess_Source_pin'],started,lambda:monitor.stage_deadline,author['owner_scope_helper'],support,control_mode=False)")
            raw=replace_once(raw,"    finally:\n        monitor.restore_bounded_objects()","    finally:\n        try:\n            if owner_observer is not None:owner_observer.restore_original_objects()\n        finally:monitor.restore_bounded_objects()")
        elif name==ROLES[3]:
            raw=replace_once(raw,"    diagnostic=h['actual_failure_only_monitor_evidence']","    diagnostic=h['actual_failure_only_monitor_evidence']\n    require(diagnostic['actual_required_new_monitor_controls_scope']==b['actual_required_monitor_controls_scope'] and diagnostic['actual_owner_scope_state']['unknown']==[],'actual required monitor Q and no unknown ownership in successful host result')")
        ast.parse(raw)
        (P/name).write_text(raw)
        oldlines=old.splitlines(keepends=True);newlines=raw.splitlines(keepends=True);hunks=[]
        for tag,a,b,c,d in difflib.SequenceMatcher(a=oldlines,b=newlines,autojunk=False).get_opcodes():
            if tag!='equal':hunks.append(dict(old_start_line0=a,old_end_line0=b,new_start_line0=c,new_end_line0=d,old_text=''.join(oldlines[a:b]),new_text=''.join(newlines[c:d])))
        restored=newlines[:]
        for h in reversed(hunks):
            assert ''.join(restored[h['new_start_line0']:h['new_end_line0']])==h['new_text']
            restored[h['new_start_line0']:h['new_end_line0']]=h['old_text'].splitlines(keepends=True)
        assert ''.join(restored)==old
        inverse.append(dict(role_basename=name,parent_original_fullpin=pin(MOTHER/name),new_complete_Source_pin=pin(P/name),hunks=hunks,full_byte_inverse=True,full_AST_inverse=True))
    contract=json.loads((P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json').read_bytes())
    shutil.copy2(MOTHER/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json',saved/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json')
    contract['required_author_Source_roles'].update(new_roles)
    contract['N8_actual_monitor_controls_qualification_required_before_business_request']=True
    contract['N8_all_actual_controls_and_Q_future']=None
    (P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json').write_text(json.dumps(contract,indent=2)+'\n')
    write(P/'COMPLETE_N8_FOUR_ROLE_BYTE_AST_INVERSE.json',dict(schema='COMPLETE_N8_FOUR_ROLE_BYTE_AST_INVERSE_V1',source_only=True,mother_manifest_pin=pin(MOTHER/'MANIFEST.json'),roles=inverse,all_other_original_N7_Source_members_retained=True,actual_candidate_or_API_execution=False))
    write(P/'COMPLETE_ORIGINAL_N7_MEMBER_RETENTION.Source_META.json',dict(schema='COMPLETE_N8_ORIGINAL_N7_MEMBER_RETENTION_V1',source_only=True,mother_manifest_pin=pin(MOTHER/'MANIFEST.json'),members=original_members,changed_relative_paths=ROLES+['EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json'],unchanged_native_physics_material_guard_Source_bytes=True,actual_execution=False))
    print(json.dumps(dict(status='AUTHOR_SOURCE_DRAFT_WRITTEN_NOT_CHECKED_OR_READY',source_only=True,path=str(P),actual_candidate_execution=False),allow_nan=False))

if __name__=='__main__':main()
