"""Source-only final BIND47 generator and single owning HF/CLI writer interface.
Six actual cleanup fullpins are required. Unknown actual proofs are never filled.
This script never imports/executes a business Host, compiler, solver, or cleanup.
Final Host is byte-identical to reviewed v2 and retains the truthful34 input declaration.
The final six Source pins receive the same-round independent review before HF/CLI.
"""
import argparse,ast,hashlib,json,os,shlex,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
DRAFT=R/'boot_v16_BIND47_strict_native17_consumer_host_source_draft_v1_20261014'
FINAL=R/'boot_v16_BIND47_strict_native17_consumer_host_source_v1_20261014'
RELEASE_PKG=R/'storage_release_literal11_next_native17_BIND_duplicates_source_v2_20261014'
RELEASE_SF=RELEASE_PKG/'COMPLETE_LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES_SOURCE_FREEZE.json'
RELEASE_SF_SHA='5c30c1de8ab14c8ca95ffd9905c3e9bd30becff00cd757ce987fa35be69d8ab7'
DRAFT_HOST_SHA='d9e96b9d5d9002119b139338bd3bc1fbac33add6b64529c7adf33129ea803944'
HOST_SHA='d9e96b9d5d9002119b139338bd3bc1fbac33add6b64529c7adf33129ea803944'
PLAN_SHA='386687813ccd5e1eb6e42bf47672193c89910d3f8355716805a3ca45c2459d57'
RECEIPT_SCHEMA='ACTUAL_EXACT_LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES_OLD_PRIVATE_RELEASE_RECEIPT_V1'
SF_SCHEMA=RECEIPT_SCHEMA
RELEASE_STATUS='EXACT_LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES_OLD_PRIVATE_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED'
BIND_SF_PATH=R/'boot_v16_BIND64_strict_native17_consumer_source_v1_20261014/COMPLETE_BOOT_BIND64_STRICT_NATIVE17_CONSUMER_SOURCE_FREEZE.json'
BIND_SF_SHA='6e454f420ab956bf48c4999a17d95891f3b05f23cd79fe67175a9265c759d819'
PYTHON='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
ENV=['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1']
ROLES=('release-manifest','release-receipt','release-Root-tools','release-Root-argv','release-post-review','release-post-tools')
CORE_REVIEW_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/independent_BIND47_strict_native17_consumer_Host_core_Source_review_20261014/REVIEW.json', 'sha256': 'a29cdd6c1f1ae903912d9bb3fe0b37a2959ad881f05f5d3d2dcf86045b7c603f', 'size_bytes': 6185, 'identity': [16777229, 50109184, 33188, 1, 6185, 1791934582660871463, 1791934582660871463]}
CORE_TOOLS_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/independent_BIND47_strict_native17_consumer_Host_core_Source_review_20261014/TRUE_TOOL_RETURNS.json', 'sha256': '769316dcfb44d2eab22d4aea7856fd6d49f217ba6c9c0a3c5433e17cc7451591', 'size_bytes': 14555, 'identity': [16777229, 50109211, 33188, 1, 14555, 1791934606277769247, 1791934606277769247]}

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def norm(p):return{k:p[k]for k in('path','sha256','size_bytes','identity')}

def pin(p):
    p=Path(p);s=p.lstat()
    if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('bounded Source/metadata only; no scientific body EOF')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('metadata opened7 changed')
        b=f.read()
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('metadata FD changed')
    if identity(p.lstat())!=identity(s)or len(b)!=s.st_size:raise RuntimeError('metadata after7 changed')
    return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=identity(s))

def exact(p):
    if not isinstance(p,dict)or pin(p['path'])!=norm(p):raise RuntimeError('required exact actual fullpin, never None or substituted metadata')
    return json.loads(Path(p['path']).read_bytes())

def seven(p):
    p=norm(p);s=Path(p['path']).lstat()
    # The original compiler can have nlink2. Original current7 is preserved.
    if not stat.S_ISREG(s.st_mode)or identity(s)!=p['identity']or s.st_size!=p['size_bytes']:raise RuntimeError('unretired current7 changed '+p['path'])

def unique(rows):
    out={}
    for row in rows:
        p=norm(row)
        if p['path']in out and out[p['path']]!=p:raise RuntimeError('inconsistent selected fullpin')
        out[p['path']]=p
    return sorted(out.values(),key=lambda x:x['path'])

def filter_live(rows,retired):
    allowed={p['path']:norm(p)for p in retired};out=[]
    for row in rows:
        p=norm(row)
        if p['path']in allowed:
            if p!=allowed[p['path']]:raise RuntimeError('only exact declared historical three may be removed from a live table')
        else:out.append(p)
    return unique(out)

def contains(value,p):
    if isinstance(value,dict):
        if all(k in value for k in p)and all(value[k]==p[k]for k in p):return True
        return any(contains(x,p)for x in value.values())
    if isinstance(value,list):return any(contains(x,p)for x in value)
    return False

def false_field(d,names):
    values=[d[k]for k in names if k in d]
    if not values or any(x is not False for x in values):raise RuntimeError('explicit independent false field required '+str(names))

def closed(tools,key,code):
    r=tools[key]
    if type(r['exit_code'])is not int or r['exit_code']!=code or r.get('session_id')is not None or tools['observed_closed']is not True:raise RuntimeError('genuine closed original typed integer terminal')
    return r

def write_new(p,value):
    raw=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()if isinstance(value,dict)else value
    if len(raw)>64*2**20:raise RuntimeError('Source metadata64MiB cap')
    fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())

def validate_release(pins,retired):
    if set(pins)!=set(ROLES)or any(not isinstance(pins[k],dict)for k in ROLES):raise RuntimeError('all six genuine actual cleanup PFs required, no future None')
    data={k:exact(pins[k])for k in ROLES};mf=data['release-manifest'];receipt=data['release-receipt'];root=data['release-Root-tools'];argv=data['release-Root-argv'];post=data['release-post-review'];tools=data['release-post-tools']
    sfp=pin(RELEASE_SF)
    if sfp['sha256']!=RELEASE_SF_SHA:raise RuntimeError('exact selected literal3 release Source v1')
    sf=exact(sfp)
    if mf['schema']!='ROOT_EXACT_LITERAL_LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES_OLD_PRIVATE_RELEASE_MANIFEST_V1'or mf['draft_only']is not False or mf['action_executed']is not False or mf['selected_Source_freeze_pin']!=sfp or mf['target_count']!=11 or mf['target_logical_bytes']!=1330716816 or mf['target_full_EOF_pins']!=retired or sf['literal11_fullpins']!=retired:raise RuntimeError('actual manifest exact ordered prior-probe Q/MAC and oldDiag4 PROJECT three')
    if pins['release-manifest']['path']!=str(RELEASE_PKG/'EXACT_LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES_MANIFEST.json'):raise RuntimeError('exact literal3 Source-v1 manifest namespace')
    terminal_keys=[k for k in('actual_execute_return','actual_terminal_return')if k in root]
    if not terminal_keys or any(root[k]!=root[terminal_keys[0]]for k in terminal_keys):raise RuntimeError('one genuine original Root terminal, named copies agree')
    terminal=closed(root,terminal_keys[0],0)
    if pins['release-Root-argv']['path']!=str(R/'ROOT_EXACT_LITERAL11_NEXT_NATIVE17_BIND_V2_READONLY_AND_EXECUTE_ARGV_20261014.json')or argv['manifest_pin']!=pins['release-manifest']or type(root['original_integer_exit_code'])is not int or root['original_integer_exit_code']!=0 or shlex.split(root['exact_executed_command'])!=argv['execute_argv']:raise RuntimeError('genuine Root0 exact approved cleanup execute_argv')
    cmd=argv['execute_argv'];exe=str(RELEASE_PKG/'verify_or_execute_literal11.py')
    if cmd.count(exe)!=1 or cmd.count('--execute')!=1:raise RuntimeError('only selected frozen execute Source and one literal --execute')
    i=cmd.index(exe)
    if cmd[:i]!=['env',*ENV[1:],PYTHON,'-B']:raise RuntimeError('exact approved literal env/Python cleanup launch prefix')
    parser=argparse.ArgumentParser(allow_abbrev=False);parser.add_argument('--manifest-sha256',required=True);parser.add_argument('--manifest-seven-id',required=True);parser.add_argument('--execute',action='store_true');args=parser.parse_args(cmd[i+1:])
    if args.execute is not True or args.manifest_sha256!=pins['release-manifest']['sha256']or json.loads(args.manifest_seven_id)!=pins['release-manifest']['identity']:raise RuntimeError('Root command exact full MF SHA/all7 arguments')
    record=receipt['deletion_records'];expected_budget=dict(original_cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,initial_fresh_reserve_bytes=2*2**30,artifact_budget_bytes=96*2**30,min_free_bytes=8*2**30)
    if receipt['schema']!=SF_SCHEMA or receipt['status']!=RELEASE_STATUS or receipt['manifest_pin']!=pins['release-manifest']or receipt['execute_requested']is not True or receipt['deleted_files']!=11 or receipt['logical_bytes_released']!=1330716816 or len(record)!=11 or [r['original_fullpin']for r in record]!=retired or receipt['next_target_intent']is not None or any(r['actual_unlink_returned']is not True or r['target_directory_fsync_attempted']is not True or r['target_directory_fsync_returned']is not True or r['confirmed_absent']is not True for r in record):raise RuntimeError('actual three unlink/fsync/absence truthful complete receipt')
    b=receipt['original_budget_after']
    if any(b[k]!=v for k,v in expected_budget.items())or b['original_initial_reserve_admitted']is not True or type(b['remaining_after_original_initial_reserves_bytes'])is not int or b['remaining_after_original_initial_reserves_bytes']<=0:raise RuntimeError('original actual fullfresh2 budget admission, no prediction')
    last=json.loads(terminal['output'].strip().splitlines()[-1])
    if norm(last['receipt_pin'])!=pins['release-receipt']or last['deleted_files']!=11 or last['logical_bytes_released']!=1330716816 or last['original_initial_reserve_admitted']is not True:raise RuntimeError('Root real last stdout exact receipt/count/budget')
    ret=closed(tools,'actual_review_return',0)
    if norm(json.loads(ret['output'].strip().splitlines()[-1])['review_pin'])!=pins['release-post-review']or post['schema']!='INDEPENDENT_LITERAL11_NEXT_NATIVE17_BIND_ACTUAL_EXACT_RELEASE_POSTVERIFICATION_V1'or post['status']!='PASS_ACTUAL_LITERAL11_NEXT_NATIVE17_BIND_EXACT_RELEASE_POSTVERIFICATION'or post['failure']is not None or post['actual_release_receipt_pin']!=pins['release-receipt']or post['actual_Root_true_tool_pin']!=pins['release-Root-tools']or post['actual_manifest_pin']!=pins['release-manifest']:raise RuntimeError('exact genuine independent release post0 closure')
    for key in('business_executed','compiler_executed','numerical_executed','deletion_executed_by_reviewer'):
        if post[key]is not False:raise RuntimeError('exact independent literal11 reviewer false field '+key)
    for p in retired:
        if os.path.lexists(p['path']):raise RuntimeError('only three named retired bodies must actually remain absent')
    return data,sfp,sf

WRITER_MAIN="def main():\n    ap=argparse.ArgumentParser(allow_abbrev=False)\n    for role in('peer-review','peer-tools'):\n        for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)\n    a=ap.parse_args()\n    if os.path.lexists(HF)or os.path.lexists(CLI):raise RuntimeError('one owning HF/CLI write only, no overwrite or retry')\n    def external(role):\n        n=role.replace('-','_');p=pin(getattr(a,n+'_summary'))\n        if p['sha256']!=getattr(a,n+'_sha256')or p['identity']!=json.loads(getattr(a,n+'_seven_id')):raise RuntimeError('exact independent Source review external PF')\n        return p\n    rp=external('peer-review');tp=external('peer-tools');review=exact(rp);tools=exact(tp);ret=closed(tools,'actual_review_return',0)\n    if review['failure']is not None or not review['status'].startswith('PASS')or norm(json.loads(ret['output'].strip().splitlines()[-1])['review_pin'])!=rp:raise RuntimeError('genuine same-round independent Source0')\n    for names in(('business_executed','independent_business_executed'),('compiler_executed','independent_compiler_executed'),('numerical_executed','numeric','independent_numerical_executed'),('files_deleted','deletion_executed','independent_deletion_executed')):false_field(review,names)\n    hp=pin(HERE/'run_guarded_one_BOOT_strict_native17_consumer.py');pp=pin(HERE/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json');ready=pin(HERE/'SOURCE_ONLY_READY.json');inverse=pin(HERE/'COMPLETE_DRAFT_TO_ACTUAL_BOUND_FINAL_SOURCE_PLAN_INVERSE.json');writer=pin(Path(__file__).absolute());plan=exact(pp);sf=plan['selected_bind_Fortran_Source_freeze_pin'];sfd=exact(sf)\n    for p in(hp,pp,ready,inverse,sf,writer):\n        if not contains(review,p):raise RuntimeError('peer Source review must contain all six exact final Source/PLAN/READY/inverse/FortranSF/writer PFs')\n    if hp['sha256']!=HOST_SHA or plan['runtime_authorities_complete']is not True or plan['draft_only']is not False:raise RuntimeError('reviewed final Host and bound real authorities')\n    retired=plan['exact_historical_retired_private_body_pins'];actual,release_sfp,release_sf=validate_release(plan['actual_retirement_external_pins'],retired)\n    selected={k:plan[k]for k in('selected_prior_probe_Host_freeze_pin','selected_bind_Fortran_Source_freeze_pin','selected_prior_probe_Root_tool_pin','selected_prior_probe_actual_post_review_pin','selected_prior_probe_actual_post_tools_pin','selected_closed_v16_Host_freeze_pin','selected_closed_v16_Root_tool_pin','selected_closed_v16_actual_post_review_pin','selected_closed_v16_actual_post_tools_pin','selected_exact11_actual_release_pin','selected_exact11_actual_Root_tool_pin','selected_exact11_actual_post_review_pin','selected_exact11_actual_post_tools_pin','selected_exact11_actual_manifest_pin')}\n    prior=exact(selected['selected_prior_probe_Host_freeze_pin']);v16=exact(selected['selected_closed_v16_Host_freeze_pin'])\n    if len(prior['dependencies'])!=3639 or len(v16['dependencies'])!=2920:raise RuntimeError('original complete3639/2920 dependency lineages retained except exact three historical bodies')\n    base=exact(plan['actual_prior_probe_report_pin'])\n    own=[pin(p)for p in sorted(HERE.iterdir())if p.is_file()]\n    metadata=own+[rp,tp,sf,release_sfp]+list(selected.values())+list(plan['actual_retirement_external_pins'].values())+[plan['actual_prior_probe_report_pin'],plan['actual_closed_v16_report_pin'],plan['Source_generator_pin']]+plan['reviewed_core_draft_complete_metadata_pins']+[plan['actual_Fortran_Source_freeze_creation_true_tool_pin']]\n    metadata+=plan['original_BOOT_status_definition_and_assignment_Source_pins']+[plan['selected_original_BOOTB216_Source_freeze_pin']]\n    metadata+=sfd['files']+[sfd['diagnostic_source_pin'],sfd['consumer_Source_pin'],sfd['original_source_pin'],sfd['complete_byte_inverse_pin'],sfd['control_plan_pin']]+release_sf['Source_pins']\n    metadata+=[pin(Path(selected[k]['path']).parent/'DECLARED_EXECUTION_INTERFACE.json')for k in('selected_prior_probe_Host_freeze_pin','selected_closed_v16_Host_freeze_pin')]\n    current34=plan['retained_original_v16_nine_input_pins']+plan['retained_old_diag4_remaining_eight_copy_pins']+plan['retained_prior_probe_eight_input_copy_pins']+plan['retained_latest_probe_nine_input_copy_pins']\n    if len(current34)!=34 or len({p['path']for p in current34})!=34 or any(p['path']in {r['path']for r in retired}for p in current34):raise RuntimeError('exact truthful34 current inputs; retired priorPROJECT has no current role')\n    if len(base['fixed_current_pins'])!=3640 or len(base['output_pins'])!=27:raise RuntimeError('exact latest reported3640 fixed and27 outputs direct live-root authority')\n    rows=filter_live(metadata+base['fixed_current_pins']+base['output_pins']+base['owned_runtime_pins']+plan['current_ordered70_input_pins']+plan['current_nine_core_object_pins']+current34+[plan['selected_original_BIND_module_pin'],plan['original_BOOT_deck_pin'],plan['readonly_pair_helper_pin']],retired)\n    current={p['path']:p for p in rows}\n    for p in filter_live(prior['dependencies']+v16['dependencies'],retired):\n        if current.get(p['path'])!=p:raise RuntimeError('all unretired3639/2920 Source dependencies already in direct latest root; never promote sealed historical body tables')\n    for p in rows:seven(p)\n    for p in unique(metadata):\n        if pin(p['path'])!=p:raise RuntimeError('all Source/metadata whole EOF exact')\n    for p in rows:seven(p)\n    bindings={'prior-probe-failure':plan['actual_prior_probe_report_pin'],'bind-source-freeze':sf,'host-freeze':None,'exact11-release':plan['selected_exact11_actual_release_pin'],'exact11-Root-tools':plan['selected_exact11_actual_Root_tool_pin']}\n    if list(bindings)!=['prior-probe-failure','bind-source-freeze','host-freeze','exact11-release','exact11-Root-tools']or len(ENV+[PYTHON,'-B',hp['path']])+6*len(bindings)!=42:raise RuntimeError('original12 environment plus five exact fullpin triplets')\n    ast.parse(Path(hp['path']).read_text())\n    h=dict(schema='COMPLETE_GUARDED_ONE_BOOT_BIND47_STRICT_NATIVE17_CONSUMER_HOST_SOURCE_ONLY_FREEZE_V1',host_source=hp,dependencies=rows,diagnostic_host_plan_pin=pp,**selected,selected_exact11_release_Source_freeze_pin=release_sfp,selected_exact11_actual_Root_argv_pin=plan['actual_retirement_external_pins']['release-Root-argv'],peer_Source_review_pin=rp,peer_Source_true_tools_pin=tp,once_HF_CLI_writer_Source_pin=writer,Source_generator_pin=plan['Source_generator_pin'],historical_retired_exact_private_body_pins=retired,complete_original_prior_probeHF3639_and_v16HF2920_unretired_dependencies_preserved=True,original_dependencies_current7_only_scientific_EOF_not_repeated=True,metadata_and_Source_full_EOF_exact=True,current_root_authority_exact_latest_fixed3640_output27=True,ancestor_sealed_output_tables_never_promoted=True,retained_current34_original9_old_diag4eight_prior8_latest9_input_pins=current34,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,future_actual_object_pin=None,future_actual_mod_pin=None,future_actual_Dragon_pin=None,future_actual_owned9_input_copy_pins=None,future_actual_BOOT_report_pin=None,full50_executed=False,engineering_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False)\n    write_new(HF,h);hfp=pin(HF);bindings['host-freeze']=hfp;argv=ENV+[PYTHON,'-B',hp['path']]\n    for k,p in bindings.items():argv+=['--'+k+'-summary',p['path'],'--'+k+'-sha256',p['sha256'],'--'+k+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]\n    interface=dict(schema='DECLARED_GUARDED_ONE_BOOT_BIND47_STRICT_NATIVE17_CONSUMER_EXECUTION_INTERFACE_V1',selected_own_Host_freeze_pin=hfp,output_root=plan['planned_output_root'],mandatory_external_prefixes=list(bindings),mandatory_external_fullpin_bindings=bindings,exact_reviewable_argv=argv,planned_stage_count=3,only_zero_based47_replaced=True,other69_including_actualBOOTB49_BOXX68_Driver37_BOOTQ40_math57_current9_archives_unchanged=True,exact9_ordinary_owned_input_copies=True,original_BOOT_deck_whole_bytes_unchanged=True,original_caps=plan['original_caps'],compiler_executed=False,numerical_executed=False,business_executed=False,future_actual_object_pin=None,future_actual_mod_pin=None,future_actual_Dragon_pin=None,future_actual_BOOT_report_pin=None,engineering_qualified=False,physics_qualified=False)\n    write_new(CLI,interface);fd=os.open(HERE,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)\n    try:os.fsync(fd)\n    finally:os.close(fd)\n    for p in rows:seven(p)\n    print(json.dumps(dict(status='ACTUAL_ONCE_BIND47_HF_CLI_SOURCE_PUBLICATION_NO_EXECUTION',Host_freeze_pin=hfp,CLI_pin=pin(CLI),dependency_count=len(rows),exact_argv_count=42,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False)))\nif __name__=='__main__':main()\n"

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    for role in ROLES:
        for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
    a=ap.parse_args();pins={}
    for role in ROLES:
        n=role.replace('-','_');p=pin(getattr(a,n+'_summary'))
        if p['sha256']!=getattr(a,n+'_sha256')or p['identity']!=json.loads(getattr(a,n+'_seven_id')):raise RuntimeError('required exact external actual cleanup PF')
        pins[role]=p
    hp=pin(DRAFT/'run_guarded_one_BOOT_strict_native17_consumer.py');pp=pin(DRAFT/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json');plan=exact(pp)
    if hp['sha256']!=DRAFT_HOST_SHA or pp['sha256']!=PLAN_SHA or plan['runtime_authorities_complete']is not False:raise RuntimeError('immutable concrete draft v2 authority')
    retired=plan['exact_historical_retired_private_body_pins'];data,release_sfp,release_sf=validate_release(pins,retired)
    bind_sfp=pin(BIND_SF_PATH);bind_sf=exact(bind_sfp)
    if bind_sfp['sha256']!=BIND_SF_SHA or plan['selected_bind_Fortran_Source_freeze_pin']!=bind_sfp or bind_sf['schema']!='COMPLETE_BOOT_BIND64_STRICT_NATIVE17_CONSUMER_FORTRAN_SOURCE_ONLY_FREEZE_V1'or len(bind_sf['original_explicit_return_mapping'])!=82 or bind_sf['original_explicit_return_mapping']!=plan['exact_BIND_original_return_mapping']or bind_sf['diagnostic_source_pin']!=plan['diagnostic_Source_pin']or bind_sf['original_module_pin']!=plan['selected_original_BIND_module_pin']:raise RuntimeError('actual exact BIND SF,82map,Source,module authorities')
    if any(bind_sf[k]is not True for k in plan['required_BIND_Source_freeze_true_flags']):raise RuntimeError('actual original ABI/math/condition/statement Source obligations')
    control=exact(bind_sf['control_plan_pin'])
    if bind_sf['control_plan_pin']!=plan['strict_native17_consumer_Source_plan_pin']or control['schema']!='SOURCE_ONLY_PRIVATE_BIND64_STRICT_NATIVE17_CONSUMER_PLAN_V1'or control['native17_fixed_scope']!=plan['native17_fixed_scope']or control['native17_complete_names']!=plan['native17_complete_names']or control['native17_rejection_predicate_ids']!=[p['predicate_id']for p in plan['exact_native17_rejection_Source_mapping']]or bind_sf['consumer_Source_pin']!=plan['diagnostic_Source_pin']or bind_sf['all_82_original_eligibility_conditions_unchanged']is not False or control['original15_and_P3_exact_forms_and_original_all_subsequent_checks_preserved']is not True:raise RuntimeError('exact native17 only236 extension and legacy15/P3/native7 Source contract')
    if os.path.lexists(FINAL)or os.path.lexists(plan['planned_output_root']):raise RuntimeError('unique fresh final Source package and future own runtime output only')
    draft_files=sorted(DRAFT.iterdir())
    if len(draft_files)!=5 or any(not p.is_file()for p in draft_files):raise RuntimeError('all original five draft files, including genuine Source raw proof, remain current')
    core_review=exact(CORE_REVIEW_PIN);core_tools=exact(CORE_TOOLS_PIN);core_return=closed(core_tools,'actual_review_return',0)
    if core_review['schema']!='INDEPENDENT_BIND47_STRICT_NATIVE17_CONSUMER_HOST_CORE_SOURCE_REVIEW_V1'or core_review['status']!='PASS_BIND47_STRICT_NATIVE17_CONSUMER_HOST_CORE_SOURCE_ONLY_READY_FOR_ACTUAL_PROOF_BINDING'or core_review['failure']is not None or core_review['source_only']is not True or core_review['host_source_pin']!=hp or core_review['plan_pin']!=pp or norm(json.loads(core_return['output'].strip().splitlines()[-1])['review_pin'])!=CORE_REVIEW_PIN:raise RuntimeError('exact current core Source0 and genuine integer0 original stdout review closure')
    for key in('business_executed','compiler_executed','numerical_executed','deletion_executed'):
        if core_review[key]is not False:raise RuntimeError('current independent core review explicit false execution fields')
    draft_pins=[pin(p)for p in draft_files]+[CORE_REVIEW_PIN,CORE_TOOLS_PIN]
    original_plan=Path(pp['path']).read_bytes();newplan=dict(plan)
    newplan.update(draft_only=False,runtime_authorities_complete=True,selected_exact11_actual_release_pin=pins['release-receipt'],selected_exact11_actual_Root_tool_pin=pins['release-Root-tools'],selected_exact11_actual_post_review_pin=pins['release-post-review'],selected_exact11_actual_post_tools_pin=pins['release-post-tools'],selected_exact11_actual_manifest_pin=pins['release-manifest'],selected_exact11_release_schema=SF_SCHEMA,selected_exact11_release_status=RELEASE_STATUS,actual_retirement_external_pins=pins,selected_exact11_release_Source_freeze_pin=release_sfp,Source_generator_pin=pin(Path(__file__).absolute()),reviewed_core_draft_complete_metadata_pins=draft_pins,selected_exact11_post_schema='INDEPENDENT_LITERAL11_NEXT_NATIVE17_BIND_ACTUAL_EXACT_RELEASE_POSTVERIFICATION_V1',selected_exact11_post_status='PASS_ACTUAL_LITERAL11_NEXT_NATIVE17_BIND_EXACT_RELEASE_POSTVERIFICATION',actual_Fortran_Source_freeze_creation_true_tool_pin=pin(R/'ACTUAL_STRICT_NATIVE17_BIND_CONSUMER_SOURCE_FREEZE_TRUE_TOOL_RETURN_20261014.json'))
    original_host=Path(hp['path']).read_bytes();host_bytes=original_host
    if hashlib.sha256(host_bytes).hexdigest()!=HOST_SHA:raise RuntimeError('exact byte-identical final truthful34 current Host')
    ast.parse(host_bytes.decode())
    selftext=Path(__file__).read_text();tree=ast.parse(selftext);utility_names={'identity','norm','pin','exact','seven','unique','filter_live','contains','false_field','closed','write_new','validate_release'}
    utilities='\n\n'.join(ast.get_source_segment(selftext,n)for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in utility_names)
    header='"""One owning BIND47 HF/CLI write after same-round peer Source0; no business."""\nimport argparse,ast,hashlib,json,os,shlex,stat\nfrom pathlib import Path\n'
    constants='\n'.join(ast.get_source_segment(selftext,n)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id in {'R','RELEASE_PKG','RELEASE_SF','RELEASE_SF_SHA','HOST_SHA','SF_SCHEMA','RELEASE_STATUS','PYTHON','ENV','ROLES','RECEIPT_SCHEMA'}for x in n.targets))
    writer_source=header+constants+"\nHERE=Path(__file__).absolute().parent\nHF=HERE/'COMPLETE_GUARDED_ONE_BOOT_BIND47_FAILED_PHYS_INVENTORY_HOST_SOURCE_FREEZE.json'\nCLI=HERE/'DECLARED_EXECUTION_INTERFACE.json'\n\n"+utilities+'\n\n'+WRITER_MAIN;ast.parse(writer_source)
    prior=exact(plan['selected_prior_probe_Host_freeze_pin']);v16=exact(plan['selected_closed_v16_Host_freeze_pin']);base=exact(plan['actual_prior_probe_report_pin'])
    current34=plan['retained_original_v16_nine_input_pins']+plan['retained_old_diag4_remaining_eight_copy_pins']+plan['retained_prior_probe_eight_input_copy_pins']+plan['retained_latest_probe_nine_input_copy_pins']
    if len(current34)!=34 or len({p['path']for p in current34})!=34 or any(p['path']in {x['path']for x in retired}for p in current34):raise RuntimeError('exact disjoint retained34 inputs')
    # Do not promote ancestor v16 outputs: their earlier retired5 remain historical.
    if len(prior['dependencies'])!=3639 or len(v16['dependencies'])!=2920 or len(base['fixed_current_pins'])!=3640 or len(base['output_pins'])!=27:raise RuntimeError('exact latest3639HF/3640fixed/27outputs and2920Source authority')
    rows=filter_live(base['fixed_current_pins']+base['output_pins']+base['owned_runtime_pins']+plan['current_ordered70_input_pins']+current34,retired)
    live={p['path']:p for p in rows}
    for p in filter_live(prior['dependencies']+v16['dependencies'],retired):
        if live.get(p['path'])!=p:raise RuntimeError('unretired Source dependencies already present in direct latest current root; no ancestor body promotion')
    for p in rows:seven(p)
    for p in rows:seven(p)
    FINAL.mkdir();host=FINAL/'run_guarded_one_BOOT_strict_native17_consumer.py';pl=FINAL/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json';writer=FINAL/'write_once_complete_BIND47_strict_native17_consumer_HF_CLI.py'
    write_new(host,host_bytes);write_new(pl,newplan);write_new(writer,writer_source.encode());iv=FINAL/'COMPLETE_DRAFT_TO_ACTUAL_BOUND_FINAL_SOURCE_PLAN_INVERSE.json'
    changes={k:dict(before=plan.get(k),before_key_present=k in plan,after_key_present=k in newplan,after=newplan.get(k))for k in set(plan)|set(newplan)if plan.get(k)!=newplan.get(k)or(k in plan)!=(k in newplan)}
    write_new(iv,dict(schema='STRICT_NATIVE17_CONSUMER_DRAFT_V1_TO_ACTUAL_CLEANUP_BOUND_FINAL_SOURCE_PLAN_INVERSE_V1',original_Host_pin=hp,final_Host_pin=pin(host),Host_changes=[],whole_Host_bytes_identical=True,whole_Host_inverse_exact=True,original_plan_pin=pp,original_plan_complete_UTF8=original_plan.decode(),final_plan_pin=pin(pl),changed_or_added_fields=changes,original_core8_methods_parser_FirstFatal_math_caps_whole_bytes_identical=True))
    ready=FINAL/'SOURCE_ONLY_READY.json';write_new(ready,dict(status='ACTUAL_EXACT3_RELEASE0_POST0_BOUND_FINAL_BIND47_SOURCE_READY_FOR_SAME_ROUND_PEER_AND_ONCE_HF_CLI',failure=None,host_source_pin=pin(host),plan_pin=pin(pl),inverse_pin=pin(iv),writer_Source_pin=pin(writer),Source_generator_pin=pin(Path(__file__).absolute()),selected_bind_Fortran_Source_freeze_pin=bind_sfp,selected_release_Source_freeze_pin=release_sfp,actual_retirement_external_pins=pins,all_unretired_original_current7_checked_twice=True,exact_three_missing_bodies_individually_historical_only=True,truthful_retained34_input_sources=True,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,own_Host_freeze_pin=None,actual_object_pin=None,actual_mod_pin=None,actual_Dragon_pin=None,actual_BOOT_report_pin=None))
    fd=os.open(FINAL,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)
    for p in rows:seven(p)
    print(json.dumps(dict(status='ACTUAL_REAL_EXACT3_PROOF_BOUND_BIND47_FINAL_SOURCE_ONLY_NO_EXECUTION',host_source_pin=pin(host),plan_pin=pin(pl),inverse_pin=pin(iv),writer_Source_pin=pin(writer),ready_pin=pin(ready),unretired_current_rows=len(rows),own_Host_freeze_pin=None,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False)))
if __name__=='__main__':main()
