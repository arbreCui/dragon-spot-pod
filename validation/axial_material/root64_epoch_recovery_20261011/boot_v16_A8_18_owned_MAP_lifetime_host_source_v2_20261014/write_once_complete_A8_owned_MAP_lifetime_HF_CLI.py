"""One owning Source-only namespace-v2 HF/CLI write. No business/compiler/delete."""
import argparse,ast,hashlib,json,os,stat
from pathlib import Path
HERE=Path(__file__).absolute().parent
HF=HERE/'COMPLETE_GUARDED_ONE_BOOT_A8_18_OWNED_MAP_LIFETIME_HOST_SOURCE_FREEZE.json'
CLI=HERE/'DECLARED_EXECUTION_INTERFACE.json'

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

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    for role in('peer-review','peer-tools'):
        for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
    a=ap.parse_args()
    if os.path.lexists(HF)or os.path.lexists(CLI):raise RuntimeError('once O_EXCL owning Source HF/CLI only')
    def external(role):
        n=role.replace('-','_');p=pin(getattr(a,n+'_summary'))
        if p['sha256']!=getattr(a,n+'_sha256')or p['identity']!=json.loads(getattr(a,n+'_seven_id')):raise RuntimeError('exact peer Source0 PF')
        return p
    rp=external('peer-review');tp=external('peer-tools');review=exact(rp);tools=exact(tp);r=closed(tools,'actual_review_return',0)
    if review['failure']is not None or not review['status'].startswith('PASS')or norm(json.loads(r['output'].strip().splitlines()[-1])['review_pin'])!=rp:raise RuntimeError('genuine closed same-round Source0')
    for names in(('business_executed','independent_business_executed'),('compiler_executed','independent_compiler_executed'),('numerical_executed','numeric','independent_numerical_executed'),('files_deleted','deletion_executed','independent_deletion_executed')):false_field(review,names)
    hp=pin(HERE/'run_guarded_one_BOOT_A8_owned_MAP_lifetime.py');pp=pin(HERE/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json');ip=pin(HERE/'COMPLETE_OWNED_RUNTIME_HOST_V1_TO_V2_NAMESPACE_SOURCE_PLAN_INVERSE.json');rd=pin(HERE/'SOURCE_ONLY_READY.json');wp=pin(__file__);plan=exact(pp);sf=plan['selected_owned_Fortran_Source_freeze_pin']
    for p in(hp,pp,ip,rd,wp,sf):
        if not contains(review,p):raise RuntimeError('peer report must bind six actual Source/plan/inverse/ready/writer/FortranSF PFs')
    parentpin=plan['namespace_predecessor_Host_freeze_pin'];parent=exact(parentpin);parentcli=exact(plan['namespace_predecessor_CLI_pin']);inv=exact(ip);oldsource=exact_source(inv['original_Host_pin']);current=Path(hp['path']).read_text()
    if len(parent['dependencies'])!=3892 or inv['whole_Host_namespace_inverse_equal']is not True or current.replace(inv['Source_literal_change']['after'],inv['Source_literal_change']['before'],1)!=oldsource:raise RuntimeError('one exact namespace literal inverse/all original methods byte-identical')
    if sf!=parent['selected_owned_Fortran_Source_freeze_pin']or plan['original_caps']!=parentcli['original_caps']:raise RuntimeError('Fortran source and all resource caps unchanged')
    hist=plan['failed_namespace_v1_nine_input_bodies_historical_only'];paths={x['historical_pin']['path']for x in hist}
    if len(hist)!=9 or sum(x['historical_pin']['size_bytes']for x in hist)!=802234184 or any(x['current_pin']is not None or x['current_read_required']is not False for x in hist):raise RuntimeError('only exact v1 copied9 historical declarations, no live body reads')
    own=[pin(p)for p in sorted(HERE.iterdir())if p.is_file()]
    metadata=own+[rp,tp,parentpin,plan['namespace_predecessor_CLI_pin'],plan['failed_namespace_v1_summary_pin'],plan['failed_namespace_v1_Root_tools_pin'],plan['failed_namespace_v1_Root_argv_pin'],inv['original_Host_pin'],inv['original_plan_pin']]
    rows=unique(parent['dependencies']+metadata)
    if any(p['path']in paths for p in rows):raise RuntimeError('v1 bodyPFs must never be promoted from nested historical metadata')
    for p in rows:seven(p)
    for p in unique(metadata):
        if pin(p['path'])!=p:raise RuntimeError('all own/metadata exact EOF7')
    for p in rows:seven(p)
    h=dict(parent);h.update(host_source=hp,diagnostic_host_plan_pin=pp,dependencies=rows,peer_Source_review_pin=rp,peer_Source_true_tools_pin=tp,once_HF_CLI_writer_Source_pin=wp,namespace_predecessor_Host_freeze_pin=parentpin,namespace_predecessor_CLI_pin=plan['namespace_predecessor_CLI_pin'],failed_namespace_v1_summary_pin=plan['failed_namespace_v1_summary_pin'],failed_namespace_v1_Root_tools_pin=plan['failed_namespace_v1_Root_tools_pin'],failed_namespace_v1_Root_argv_pin=plan['failed_namespace_v1_Root_argv_pin'],failed_namespace_v1_nine_input_bodies_historical_only=hist,all_original3892_dependencies_exact_current7_retained=True,v1_sealed_output_tables_not_promoted_into_current_dependencies=True,own_source_namespace_only_change=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,future_actual_object_pin=None,future_actual_mod_pin=None,future_actual_Dragon_pin=None,future_actual_owned9_input_copy_pins=None,future_actual_BOOT_report_pin=None)
    c=dict(parentcli);bindings=dict(parentcli['mandatory_external_fullpin_bindings']);argv=list(parentcli['exact_reviewable_argv'])
    if len(argv)!=42 or len(bindings)!=5 or argv[11]!=parent['host_source']['path']:raise RuntimeError('exact original five-role42 execution interface')
    write_new(HF,h);hfp=pin(HF);bindings['host-freeze']=hfp;argv[11]=hp['path']
    for suffix,value in(('summary',hfp['path']),('sha256',hfp['sha256']),('seven-id',json.dumps(hfp['identity'],separators=(',',':')))):
        flag='--host-freeze-'+suffix
        if argv.count(flag)!=1:raise RuntimeError('one exact ownHF argument')
        argv[argv.index(flag)+1]=value
    c.update(selected_own_Host_freeze_pin=hfp,output_root=plan['planned_output_root'],mandatory_external_fullpin_bindings=bindings,exact_reviewable_argv=argv,namespace_predecessor_CLI_pin=plan['namespace_predecessor_CLI_pin'],only_namespace_v1_to_v2_changed=True)
    write_new(CLI,c);fd=os.open(HERE,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)
    for p in rows:seven(p)
    print(json.dumps(dict(status='ONCE_OWNED_RUNTIME_V2_SOURCE_HF_CLI_READY_NO_BUSINESS',Host_freeze_pin=hfp,CLI_pin=pin(CLI),dependency_count=len(rows),exact_argv_count=42,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False)))
def exact_source(p):
    if pin(p['path'])!=norm(p):raise RuntimeError('exact original Host EOF7')
    return Path(p['path']).read_text()
if __name__=='__main__':main()
