#!/usr/bin/evn python 
# -*- coding: utf-8 -*- 
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

import atexit


#import sys
def get_vms(content):
    print("get all vms")
    vm_view = content.viewManager.CreateContainerView(content.rootFolder,
            [vim.VirtualMachine],True)
    vms = [vm for vm in vm_view.view ]
    vm_view.Destroy()
    return vms

def wait_for_task(task):
    """ wait for a vCenter task to finish """
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            print "there was an error"
            task_done = True
if len(sys.argv) > 1:
    delete_by_name = sys.argv[1]
else:
    delete_by_name = ""

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
# get_all_vm
#vm = si.content.searchIndex.FindByIp(None, "10.0.33.145", True)
content = si.RetrieveContent()
all_vm = get_vms(content)
#all_vm = GetVMs(content)

delete_vm_list = []

print("vm will be delete:")
for vm in all_vm:
    if vm is None:
        raise SystemExit("Unable to locate VirtualMachine.")
    if re.match(delete_by_name,vm.name):
        delete_vm_list.append(vm)
        print("vm name:{}".format(vm.name))

while True:
    choice = raw_input("是否删除(y/n):")
    if choice == "y":
        for vm in delete_vm_list:
            print("deleting vm {} ...".format(vm.name))
            task = vm.Destroy_Task()
            wait_for_task(task)
        sys.exit(0)
    else:
        sys.exit(0)


