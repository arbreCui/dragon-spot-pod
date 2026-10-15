import hashlib,importlib.util,json,os,sys
from pathlib import Path
SOURCE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_AB_persisted_XSM_ASCII_v23_sources/Root_native_postclose_META_writer.py')
WRITER_SHA='abd8ff37de4128f0bbcfc68cdf6a5f500276dd64aaf99246f208294927c6c139'
def main():
    assert len(sys.argv)==1 and not sys.flags.optimize and sys.getprofile() is None
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==WRITER_SHA
    sp=importlib.util.spec_from_file_location('Root_native_prelaunch_metadata_functions',SOURCE);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
    assert not any(os.path.lexists(p) for p in (m.H,m.O,m.C))
    freeze,freeze_pin=m.read(m.E/'Root_complete_native_D_source_freeze.json');assert freeze['schema']=='ROOT_V23_COMPLETE_NATIVE_D_SOURCE_FREEZE_V1'
    d=m.snapshot(m.D);assert d==freeze['complete_D']
    binding,bpin=m.read(m.D/'Root_actual_native_SOURCE_binding.json','765fb053ae13a10aa71cd9d20ced1aff4a8f275d7b2a2a3ac9a838a403927d87')
    assert binding['original_caps']==m.CAPS and len(binding['complete_input_pins'])==129
    assert binding['namespaces']==dict(host=str(m.H),output=str(m.O),control=str(m.C),source=str(m.D),receipts=str(m.E))
    assert m.pin(m.D/'Root_bound_complete_native_genuine_host.py')['sha256']=='90d4cf339eaa2aceb01e9736f65443351c64948ff96496b8d6a416dcf022f76f'
    assert m.pin(m.D/'Root_bound_complete_native_checker.py')['sha256']=='9d8494234a3a6d58ef4cf8f151ff0505f35c750929ad444dfee8ca8a667dedb0'
    p=m.B/'actual_prepare_sources/prepare_cli_host_v15.py';assert m.pin(p)['sha256']=='3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
    spec=importlib.util.spec_from_file_location('Root_native_prelaunch_original_support',p);support=importlib.util.module_from_spec(spec);sys.modules[spec.name]=support;spec.loader.exec_module(support)
    assert Path(sys.executable).resolve()==support.PYTHON and all(os.environ.get(k)=='1' for k in support.THREAD_KEYS)
    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'Root_native_prelaunch_original619')
    resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'Root_native_prelaunch_original_ebbb')
    full,production=helper.modules();helper.guard_admission(full)
    assert full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,) and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT
    roots=resource.history_roots([str(p) for p in (m.H,m.O,m.C,support.OUT,support.TERMINAL)],support.ART)
    resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure);actual=resources.check()
    assert actual['artifact_bytes']+2*2**30<96*2**30 and actual['disk_free_bytes']-2*2**30>=8*2**30
    e=m.snapshot(m.E);assert m.bytes_in([d,e])<2*2**30
    before=m.snapshot(m.E);assert before==e and m.snapshot(m.D)==d
    record=dict(schema='ROOT_V23_NATIVE_COMPLETE_SOURCE_PRELAUNCH_AND_FROZEN_E_V1',complete_D_frozen=d,complete_E_frozen_before_actual_launch=e,actual_D_source_freeze=freeze_pin,actual_binding=bpin,genuine_guard_MRO_verified=True,original_helper=hpin,resource_factory=rpin,genuine_resources=actual,original_caps=m.CAPS,native_executed=False,preflight_source=m.pin(Path(__file__).absolute()),full129_material_payloads_not_rehashed_by_this_preflight=True,complete129_payloads_will_be_fresh_EOF_verified_by_genuine_host_before_and_after=True,outer_tool_capture_scope='EXEC_COMMAND_MERGED_STDOUT_STDERR',no_runtime_E_append=True)
    dest=Path('/private/tmp/spot_v23_native_complete_prelaunch_frozen_D_E_ROOT_20261010_f73f14.json');m.write(dest,record)
    assert m.snapshot(m.E)==e and m.snapshot(m.D)==d
    print(json.dumps(dict(status='SOURCE_PRELAUNCH_PASS_NO_NATIVE_EXECUTION',prelaunch=m.pin(dest),D_files=len(d['files']),E_files=len(e['files']),history_bytes=actual['artifact_bytes'],free_bytes=actual['disk_free_bytes'],joint_D_E_bytes=m.bytes_in([d,e]))))
if __name__=='__main__':main()
