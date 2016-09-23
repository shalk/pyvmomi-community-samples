#!/usr/bin/evn python 
# -*- encoding: UTF-8 -*- 
from pyVim.connect import SmartConnect, Disconnect

import atexit

from tools.vm import print_vm_info
#import sys

def wait_for_task(task):
    """ wait for a vCenter task to finish """
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            print "there was an error"
            task_done = True

host = "10.0.33.244"
port = "443"
user = "administrator@cloudcenter.local"
pwd = "Sugon!123"
try:
    si = SmartConnect(host=host,
                      user=user,
                      pwd=pwd,
                      port=int(port))
    atexit.register(Disconnect,si)
except IOError:
    pass

if not si:
    raise SystemExit("can not connect to host !!!")


#vm = si.content.searchIndex.FindByUuid(None, "", True, instance_search)
vm = si.content.searchIndex.FindByIp(None, "10.0.33.145", True)

if vm is None:
    raise SystemExit("Unable to locate VirtualMachine.")
else:
    print(vm)
    print(type(vm))
    print_vm_info(vm)

print("revert to current snapshot")
task = vm.RevertToCurrentSnapshot_Task()
wait_for_task(task)


