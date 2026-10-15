"""Future real private OS fixture. Only a Source-bound genuine control runner.
Never a compiler, material deck, native transport, or scientific qualification.
"""
import json
import os
from pathlib import Path
import sys
import time

def wait_file(path,deadline):
    while not path.exists():
        if time.monotonic()>=deadline:raise RuntimeError('private control original stage600 deadline')
        time.sleep(.01)

def write_new(path,value):
    with path.open('x') as stream:
        json.dump(value,stream,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())

def main():
    case,root,deadline_text=sys.argv[1:];root=Path(root);deadline=float(deadline_text)
    if not root.is_absolute() or not root.is_dir():raise ValueError('actual private control directory')
    if case=='early_exit':return
    if case=='byte_producer':
        # A declared private byte producer only. Its output is never labelled
        # canonical lsof output or evidence of a canonical tool oversize.
        sys.stdout.buffer.write(b'x'*(8*2**20));sys.stdout.buffer.flush()
        write_new(root/'leader_ready.json',dict(pid=os.getpid(),ppid=os.getppid(),pgid=os.getpgrp(),descendant_pid=None))
        wait_file(root/'leader_release',deadline);return
    if case=='clock_producer':
        wait_file(root/'clock_release',deadline);return
    fd=None;descendant=None
    if case in ('live_descendant','closed_leader_group','late_descendant_exit'):
        descendant=os.fork()
        if descendant==0:
            target=root/'actual_deleted_control_file'
            fd=os.open(target,os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600)
            os.write(fd,b'actual private control bytes\n');os.fsync(fd);os.unlink(target)
            write_new(root/'descendant_ready.json',dict(pid=os.getpid(),ppid=os.getppid(),pgid=os.getpgrp(),actual_unlinked_fd=fd))
            wait_file(root/'descendant_release',deadline)
            os.close(fd);os._exit(0)
    write_new(root/'leader_ready.json',dict(pid=os.getpid(),ppid=os.getppid(),pgid=os.getpgrp(),descendant_pid=descendant))
    if case=='late_descendant_exit':
        wait_file(root/'descendant_release',deadline)
        pid,status=os.waitpid(descendant,0)
        write_new(root/'descendant_real_wait.json',dict(pid=pid,status=status,exited=os.WIFEXITED(status),exitcode=os.waitstatus_to_exitcode(status)))
    wait_file(root/'leader_release',deadline)
    if case=='nonzero':raise SystemExit(7)
    if case=='closed_leader_group':return
    if descendant is not None and case!='late_descendant_exit':
        (root/'descendant_release').touch(exist_ok=False)
        os.waitpid(descendant,0)

if __name__=='__main__':main()
