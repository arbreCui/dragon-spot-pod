"""Recover only exact retained bytes for the original 21 N9 author owners.

The old binding remains historical and unchanged. New copies get real current
identities. No source owner is reconstructed from invented values and no old
execution, identity, resource, Native or science qualification is inherited.
"""
import gzip
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import sys
import tarfile
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE=HERE.parent/'complete_history_root_index_source_v15_20261010'
BINDING=BASE/'actual_complete_native_observation_BUILD5_AB_v9_link_count_monitor_controls_sources/Root_actual_N8_monitor_controls_Source_binding.json'
START=time.monotonic()
FIELDS=('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')

def require(value,message):
    if type(value)is not bool or not value:raise ValueError(message)

def budget():
    require(time.monotonic()-START<600,'metadata recovery600 cap')
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':peak*=1024
    require(peak<512*2**20,'metadata recovery self512MiB cap')

def identity(s):return [getattr(s,k)for k in FIELDS]

def pin(path):
    path=Path(path);before=identity(path.lstat())
    require(path.is_absolute()and all(not p.is_symlink()for p in(path,*path.parents))and stat.S_ISREG(before[2]),'ordinary real full file')
    digest=hashlib.sha256();size=0
    with path.open('rb')as stream:
        require(identity(os.fstat(stream.fileno()))==before,'source opened unchanged')
        while True:
            budget();raw=stream.read(2**20)
            if not raw:break
            digest.update(raw);size+=len(raw)
        require(identity(os.fstat(stream.fileno()))==before,'source EOF unchanged')
    require(identity(path.lstat())==before and size==before[4],'source current full EOF unchanged')
    return dict(path=str(path),size_bytes=size,sha256=digest.hexdigest(),identity=before)

def strict(raw):
    def pairs(items):
        out={}
        for k,v in items:require(k not in out,'source META duplicate key');out[k]=v
        return out
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in()).throw(ValueError(s)))

def write(path,value):
    budget()
    with Path(path).open('x',encoding='utf-8')as stream:
        json.dump(value,stream,ensure_ascii=False,allow_nan=False,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())

def main():
    require(os.environ.get('PYTHONDONTWRITEBYTECODE')=='1'and all(os.environ.get(k)=='1'for k in THREADS),'metadata recovery one thread')
    before=pin(BINDING);b=strict(BINDING.read_bytes());author=b['actual_author_Source_contract']
    require(b['schema']=='ROOT_ACTUAL_N8_MONITOR_CONTROLS_SOURCE_BINDING_V1'and b['source_only']is True and len(author)==21,'original exact 21-role Source contract')
    sizes={p['size_bytes']for p in author.values()};by_pair={}
    for role,p in author.items():by_pair.setdefault((p['size_bytes'],p['sha256']),[]).append(role)
    found={role:[]for role in author};archives=[];jsons=[];walk_count=0;candidate_count=0;hashed_bytes=0;unreadable=[]
    excluded={'.git','.aws','.codex','.agents'}
    for folder,dirs,names in os.walk(ROOT,followlinks=False):
        budget();dirs[:]=[d for d in dirs if d not in excluded and not(Path(folder)/d).is_symlink()]
        for name in names:
            budget();path=Path(folder)/name
            try:s=path.lstat()
            except OSError as error:unreadable.append(dict(path=str(path),error=repr(error)));continue
            if not stat.S_ISREG(s.st_mode):continue
            walk_count+=1
            if path.suffix=='.json'and s.st_size<=16*2**20:jsons.append(path)
            if name.endswith(('.tar','.tar.gz','.tgz','.gz'))and s.st_size<=128*2**20:archives.append(path)
            if s.st_size not in sizes:continue
            p=pin(path);candidate_count+=1;hashed_bytes+=p['size_bytes']
            for role in by_pair.get((p['size_bytes'],p['sha256']),[]):found[role].append(dict(kind='ordinary_file',source_pin=p))
    # Recover archive members only if direct retained ordinary copies do not
    # cover a role. Archives themselves are pinned before/after the real read.
    archive_checks=[]
    for path in archives:
        if all(found.values()):break
        budget();archive_pin=pin(path);members=0;matched=[];error=None
        try:
            with tarfile.open(path,'r|*')as archive:
                for member in archive:
                    budget();members+=1
                    if not member.isfile()or member.size not in sizes:continue
                    reader=archive.extractfile(member)
                    require(reader is not None,'actual regular archive member')
                    with reader:raw=reader.read(member.size+1)
                    require(len(raw)==member.size,'complete actual archive member bytes')
                    digest=hashlib.sha256(raw).hexdigest()
                    for role in by_pair.get((len(raw),digest),[]):
                        found[role].append(dict(kind='exact_archive_member',container_pin=archive_pin,member=member.name,member_size_bytes=len(raw),member_sha256=digest))
                        matched.append(role)
        except(tarfile.TarError,EOFError,OSError)as failure:error=repr(failure)
        require(pin(path)==archive_pin,'archive entire current pin unchanged')
        archive_checks.append(dict(archive_pin=archive_pin,members_examined=members,matched_roles=matched,actual_read_error=error))
    # An embedded complete text field counts only if its actual UTF8 bytes
    # exactly match both historical size and SHA. No JSON respelling/synthesis.
    embedded_checks=0
    if not all(found.values()):
        for path in jsons:
            budget()
            raw=path.read_bytes()
            if b'N9'in raw or b'owner_scope_helper'in raw or b'complete_observation'in raw:
                source_pin=pin(path)
                try:value=strict(raw)
                except(ValueError,UnicodeError,json.JSONDecodeError):continue
                stack=[([],value)];embedded_checks+=1
                while stack:
                    budget();trail,node=stack.pop()
                    if type(node)is dict:
                        stack.extend((trail+[k],v)for k,v in node.items())
                    elif type(node)is list:
                        stack.extend((trail+[i],v)for i,v in enumerate(node))
                    elif type(node)is str:
                        content=node.encode('utf-8')
                        if len(content)not in sizes:continue
                        digest=hashlib.sha256(content).hexdigest()
                        for role in by_pair.get((len(content),digest),[]):
                            found[role].append(dict(kind='exact_embedded_UTF8_text',container_pin=source_pin,JSON_field_path=trail,size_bytes=len(content),sha256=digest))
                require(pin(path)==source_pin,'embedded text container unchanged')
            if all(found.values()):break
    recovered=HERE/'recovered_source'
    require(not os.path.lexists(recovered),'fresh durable recovered Source namespace')
    recovered.mkdir()
    rows=[];copied_bytes=0
    for role,old in author.items():
        budget();sources=found[role]
        row=dict(role=role,historical_original_pin=old,current_original_path_exists=Path(old['path']).is_file(),exact_retained_sources=sources,status='MISSING_EXACT_BYTES',recovered_current_pin=None)
        if sources:
            # Prefer an ordinary copy with the exact original basename, then
            # the shortest current project path. Every chosen byte was hashed.
            sources.sort(key=lambda q:(q['kind']!='ordinary_file',Path(q.get('source_pin',{}).get('path','')).name!=Path(old['path']).name,len(q.get('source_pin',{}).get('path',''))))
            chosen=sources[0]
            if chosen['kind']=='ordinary_file':
                require(pin(chosen['source_pin']['path'])==chosen['source_pin'],'chosen exact Source still current')
                raw=Path(chosen['source_pin']['path']).read_bytes()
            elif chosen['kind']=='exact_archive_member':
                require(pin(chosen['container_pin']['path'])==chosen['container_pin'],'chosen exact archive current')
                with tarfile.open(chosen['container_pin']['path'],'r:*')as archive:
                    with archive.extractfile(chosen['member'])as stream:raw=stream.read(old['size_bytes']+1)
            else:
                require(pin(chosen['container_pin']['path'])==chosen['container_pin'],'chosen exact embedded current')
                value=strict(Path(chosen['container_pin']['path']).read_bytes())
                for key in chosen['JSON_field_path']:value=value[key]
                raw=value.encode('utf-8')
            require(len(raw)==old['size_bytes']and hashlib.sha256(raw).hexdigest()==old['sha256'],'actual recovered complete bytes match historical content')
            destdir=recovered/role;destdir.mkdir();dest=destdir/Path(old['path']).name
            with dest.open('xb')as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
            current=pin(dest);require(current['size_bytes']==old['size_bytes']and current['sha256']==old['sha256']and current['identity'][3]==1,'new durable singlelink Source exact content/current identity')
            row.update(status='EXACT_BYTES_RECOVERED_CURRENT_IDENTITY',recovered_current_pin=current,chosen_retained_source=chosen)
            copied_bytes+=len(raw)
        rows.append(row)
    require(pin(BINDING)==before,'old Source binding untouched current pin')
    missing=[r['role']for r in rows if r['recovered_current_pin']is None]
    result=dict(schema='ACTUAL_N9_21_AUTHOR_SOURCE_EXACT_BYTES_RECOVERY_V1',source_only=True,
        status='ALL_EXACT_SOURCE_BYTES_RECOVERED_NO_OLD_IDENTITY_OR_Q_INHERITANCE'if not missing else'PARTIAL_EXACT_SOURCE_RECOVERY_MISSING_ROLES',
        recovery_Source_pin=pin(Path(__file__).resolve()),historical_binding_current_pin=before,
        original_schema=b['schema'],original_author_role_count=21,project_walk_includes_ignored_ART=True,
        excluded_unrelated_metadata_directory_names=sorted(excluded),regular_project_files_examined=walk_count,
        size_matched_files_full_EOF_hashed=candidate_count,size_matched_actual_bytes_hashed=hashed_bytes,
        archive_checks=archive_checks,embedded_JSON_containers_examined=embedded_checks,walk_read_errors=unreadable,
        recovered_source_bytes=copied_bytes,recovered_roles=21-len(missing),missing_exact_roles=missing,roles=rows,
        old_binding_or_owner_identity_modified=False,current_Source_binding_created=False,
        exact_current_binding_blockers=['Original author Source paths and old 7-field identities remain historical; main controls metadata()/pin()==pin checks require a genuinely new current Source-only binding.',
            'Independent new prelaunch review must bind the final new current binding and exact adapter/control pins; old review qualification cannot be inherited.']+(['Original controls main() for author.values() requires all 21 owners present/current; missing exact roles must be resolved.']if missing else[]),
        PS_lsof_child_native_or_numerical_work_executed=False,actual_control_qualification=False,
        actual_native_build_qualification=False,scientific_qualification=False,actual_goal_achieved=False,
        actual_elapsed_seconds=time.monotonic()-START)
    out=HERE/'ACTUAL_N9_21_AUTHOR_SOURCE_RECOVERY.json';write(out,result)
    print(json.dumps(dict(status=result['status'],recovery_mapping_pin=pin(out),recovered_roles=21-len(missing),missing_exact_roles=missing,
        copied_bytes=copied_bytes,owner_scope_helper_current_pin=next(r['recovered_current_pin']for r in rows if r['role']=='owner_scope_helper'),
        actual_control_qualification=False),allow_nan=False),flush=True)

if __name__=='__main__':main()
