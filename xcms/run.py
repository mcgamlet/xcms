
import os               # Miscellaneous OS interfaces.
import sys              # System-specific parameters and functions.
from XenAPI import Session
from Balancer import init2
from Balancer import vms2
from Balancer import rebalance
from Balancer import get_cpu
import time
import json

with open('./path.json','r') as f:
    path=json.load(f)

# Default daemon parameters.
# File mode creation mask of the daemon.
UMASK = 0

# Default working directory for the daemon.
WORKDIR = "/"

# Default maximum for the number of available file descriptors.
MAXFD = 1024

# The standard I/O file descriptors are redirected to /dev/null by default.
if (hasattr(os, "devnull")):
    REDIRECT_TO = os.devnull
else:
    REDIRECT_TO = "/dev/null"

def createDaemon(session):
    """Detach a process from the controlling terminal and run it in the
    background as a daemon.
    """

    try:
        pid = os.fork()
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror, e.errno)

    if (pid == 0):	# The first child.
        os.setsid()
        try:
            pid = os.fork()	# Fork a second child.
        except OSError, e:
            raise Exception, "%s [%d]" % (e.strerror, e.errno)
        if (pid == 0):	# The second child.
            os.chdir(WORKDIR)
            os.umask(UMASK)
        else:
            os._exit(0)	# Exit parent (the first child) of the second child.
    else:
        os._exit(0)	# Exit parent of the first child.

    import resource		# Resource usage information.
    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if (maxfd == resource.RLIM_INFINITY):
        maxfd = MAXFD
  
    # Iterate through and close all file descriptors.
    for fd in range(0, maxfd):
        try:
            os.close(fd)
        except OSError:	# ERROR, fd wasn't open to begin with (ignored)
            pass

    os.open(REDIRECT_TO, os.O_RDWR)	# standard input (0)

    # Duplicate standard input to standard output and standard error.
    os.dup2(0, 1)			# standard output (1)
    os.dup2(0, 2)			# standard error (2)


    return(0)

if __name__ == "__main__":
    ses = Session(path['url'])
    ses.xenapi.login_with_password(path['login'], path['password'])
    retCode = createDaemon(ses)

    procParams = """
    return code = %s
    process ID = %s
    parent process ID = %s
    process group ID = %s
    session ID = %s
    user ID = %s
    effective user ID = %s
    real group ID = %s
    effective group ID = %s
    """ % (retCode, os.getpid(), os.getppid(), os.getpgrp(), os.getsid(0),
    os.getuid(), os.geteuid(), os.getgid(), os.getegid())

    #open("createDaemon.log", "w").write(procParams + "\n")
    while 1:
        try:
            hosts = []
            vms=[]
            init2(ses,hosts)
            try:
                get_cpu(ses,hosts)
            except Exception: pass
            vms2(ses,vms,path['ip'],path['login'],path['password'])
        except Exception: pass
        for i in range(len(vms)):
            vms[i]['snapshots'].sort(key=lambda vm: vm['snapshot_time'], reverse=True)
            for host in hosts:
                for vm in host['vms']:
                    if vms[i]['vmr']==vm['vmr']:
                        vms[i]['cpu']=vm['cpu']
        with open(path['hosts'],'w') as f:
            json.dump(hosts,f)
        with open(path['vms'],'w') as f:
            json.dump(vms,f)
    time.sleep(5)

   #sys.exit(retCode)
