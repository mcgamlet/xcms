import time
import datetime
import parse_rrd
import XenAPI
import random
import pickle
import json


def init2(session,hosts):
    host_refs=session.xenapi.host.get_all()
    for host_ref in host_refs:
        free=0
        host={}
        host['host_ref']=host_ref
        host['name']=session.xenapi.host.get_name_label(host_ref)
        host['ip']='http://'+str(session.xenapi.host.get_address(host_ref))
        host['fluid']=False
        host['unic']=random.randrange(1,10000,1)
        host['cpu']=0
        vmrs=session.xenapi.host.get_resident_VMs(host_ref)
        vms=[]
        for vmr in vmrs:
            vm={}
            vm['vmr']=vmr
            vm['name']=session.xenapi.VM.get_name_label(vmr)
            vm['unic']=random.randrange(1,10000,1)
            vm['power_state']=session.xenapi.VM.get_power_state(vmr)
            vm['fluid']=False
            vm['cpu']=0
            vm['snapshot_time']=""
            vm['actions']=session.xenapi.VM.get_record(vmr)['allowed_operations']
            rec=session.xenapi.VM.get_metrics(vmr)
            if session.xenapi.VM.get_is_control_domain(vmr):
                state="power_on"
                key="allowed_operations"
                for op in session.xenapi.host.get_record(host_ref)[key]:
                    if op==state:
                        host['power_state']="Halted"
                    else: host['power_state']="Running"
            else:
                if vm['power_state']=="Running":
                    vm['mem']=int(session.xenapi.VM_metrics.get_memory_actual(rec))/1000000
                    vm['mem_max']=int(session.xenapi.VM.get_memory_dynamic_max(vmr))/1000000
                    fl=float(vm['mem'])/float(vm['mem_max'])*100
                    vm['mem_load']=int(fl)
                    vms.append(vm)
            free=free+int(session.xenapi.VM_metrics.get_memory_actual(rec))
        host['vms']=vms
        if host['power_state']=="Running":
            hrec=session.xenapi.host.get_metrics(host_ref)
            host['mem_total']=int(session.xenapi.host_metrics.get_memory_total(hrec))/1000000
            host['free_mem']=host['mem_total']-free/1000000
            host['mem']=host['mem_total']-host['free_mem']
            host['mem_load']=100*free/host['mem_total']/1000000
        hosts.append(host)

def vms2(session,vms,url,login_2,password_2):
    vmrs=session.xenapi.VM.get_all()
    for vmr in vmrs:
        if not session.xenapi.VM.get_record(vmr)["is_a_template"]:
            if not session.xenapi.VM.get_is_control_domain(vmr):
                vm={}
                vm['vmr']=vmr
                vm['name']=session.xenapi.VM.get_name_label(vmr)
                vm['unic']=random.randrange(1,10000,1)
                vm['power_state']=session.xenapi.VM.get_power_state(vmr)
                vm['fluid']=False
                vm['snapshot_time']=""
                vm['actions']=session.xenapi.VM.get_record(vmr)['allowed_operations']
                vm['mem']=0
                vm['cpu']=0
                if vm['power_state']=="Running":
                    rec=session.xenapi.VM.get_metrics(vmr)
                    vm['mem']=int(session.xenapi.VM_metrics.get_memory_actual(rec))/1000000
                    vm['mem_max']=int(session.xenapi.VM.get_memory_dynamic_max(vmr))/1000000
                    fl=float(vm['mem'])/float(vm['mem_max'])*100
                    vm['mem_load']=int(fl)
                    vm['resident_on']=session.xenapi.host.get_name_label(session.xenapi.VM.get_resident_on(vm['vmr']))
                vm['snapshots']=get_snapshots(session,vmr,url,login_2,password_2)
                vms.append(vm)





def get_snapshots(session,vmr,url,login_2,password_2):
    snapshots=[]
    snaps=session.xenapi.VM.get_snapshots(vmr)
    for snap in snaps:
        vm={}
        vm['vmr']=snap
        vm['name']=session.xenapi.VM.get_name_label(snap)
        vm['unic']=random.randrange(1,10000,1)
        vm['power_state']=session.xenapi.VM.get_power_state(snap)
        vm['fluid']=False
        vm['snapshot_time']=str(datetime.datetime.strptime(str(session.xenapi.VM.get_record(snap)['snapshot_time']),'%Y%m%dT%H:%M:%SZ'))
        vm['actions']=session.xenapi.VM.get_record(vmr)['allowed_operations']     
        vm['export']='http://'+str(login_2)+':'+str(password_2)+'@'+url+'/export?uuid='+str(session.xenapi.VM.get_uuid(snap))        
        snapshots.append(vm)
    return snapshots

def get_templates(session,templates):
    vm_refs=session.xenapi.VM.get_all()
    for vmr in vm_refs:
        if not session.xenapi.VM.get_is_control_domain(vmr):
            record=session.xenapi.VM.get_record(vmr)
            if record["is_a_template"]:
                vm={}
                vm['vmr']=vmr
                vm['name']=session.xenapi.VM.get_name_label(vmr)
                if record["last_booted_record"] and not record["snapshot_metadata"]:
                    templates.append(vm)

def inform(session, hosts):
    for host in hosts:
        #hrec=session.xenapi.host.get_metrics(hosts[i].HostRef)
        #hmem=int(session.xenapi.host_metrics.get_memory_total(hrec))
        print "*********************"
        print "Host : " , host.name
        print "*********************"
        print "Free mem = ", host.free_mem/1000000, "Mb, ", host.mem_load," %"
        print "IP: ", host.ip
        print "AV_CPU: ", host.cpu
        for vm in host.vms:
            print "------------------------"
            print "VM :", vm.name
            print "VM mem : ", vm.mem/1000000, "Mb, ",100*vm.mem/host.mem_total, " %"
            print "VM mem max : ", vm.mem_max/1000000, "Mb"
            print "VM mem load :  ", vm.mem_load
            print "VM av_cpu:", vm.cpu


            

    
    
def get_cpu(session,hosts):# get cpu load from rrd
    keys=[] #params
    datas=[] #value of params
    rrd_updates = parse_rrd.RRDUpdates()
    params = {}
    params["cf"] = "AVERAGE"
    params["start"] = int(time.time()) - 10
    params["interval"] = 5
    params["host"] = 'true'
    #with open('dump.json','w') as f:
        #json.dump(hosts,f)
    # Get load of hosts

    for n in range(len(hosts)):
        if hosts[n]['power_state']=="Running":
            url=hosts[n]['ip']
            rrd_updates.refresh(session.handle, params, url)
            #host_uuid = rrd_updates.get_host_uuid()
            for param in rrd_updates.get_host_param_list():
                if param != "":
                    max_time=0
                    data=0
                    for row in range(rrd_updates.get_nrows()):
                        epoch = rrd_updates.get_row_time(row)
                        try:
                            dv = float(rrd_updates.get_host_data(param,row))
                        except Exception: dv=0
                        if epoch > max_time:
                            max_time = epoch
                            data = dv
                    #nt = time.strftime("%H:%M:%S", time.localtime(max_time))
                    keys.append(param)
                    datas.append(data)
            l=0
            sum=0
            for i in range (len(keys)):
                for j in range(16):
                    if keys[i]=='cpu'+str(j):
                        sum=sum+datas[i] #average cpu load
                        l=l+1
            sum=sum*100/l # in percent
            #if sum:
            hosts[n]['cpu']=round(sum,2)
            #hosts[n].cpu=int(hosts[n].cpu)
            keys=[]
            datas=[]
            l=0
            sum=0
            # Get vms average cpu load
            for a in range(len(hosts[n]['vms'])):
                if hosts[n]['vms'][a]['power_state']=="Running":
                    uuid=session.xenapi.VM.get_uuid(hosts[n]['vms'][a]['vmr'])
                    l=0
                    sum=0
                    for param in rrd_updates.get_vm_param_list(uuid):
                        if param != "":
                            max_time=0
                            data=0
                            for row in range(rrd_updates.get_nrows()):
                                epoch = rrd_updates.get_row_time(row)
                                try:
                                    dv = float(rrd_updates.get_vm_data(uuid,param,row))
                                except Exception: dv=0
                                if epoch > max_time:
                                    max_time = epoch
                                    data = dv
                            nt = time.strftime("%H:%M:%S", time.localtime(max_time))
                            keys.append(param)
                            datas.append(data)
                    for i in range (len(keys)):
                        for j in range(100):
                            if keys[i]=='cpu'+str(j):
                                sum=sum+datas[i]
                                l=l+1
                    sum=sum*100/l
                    #hosts[n].VMs_CPUs.append(sum)
                    #if sum:
                    hosts[n]['vms'][a]['cpu']=round(sum,2)
                    #for g in range(len(hosts[n].vms)):
                        #hosts[n].vms[g].cpu=sum
                    keys=[]
                    datas=[]
                    l=0
                    sum=0



def main(session):

    while(1):
        hosts = []
        vms=[]
        init2(session,hosts)
        #try:
        get_cpu(session,hosts)
        #except Exception: None
        vms2(session,vms,path['ip'],path['login'],path['password'])
        for i in range(len(vms)):
            vms[i]['snapshots'].sort(key=lambda vm: vm['snapshot_time'], reverse=True)
            for host in hosts:
                for vm in host['vms']:
                    if vms[i]['vmr']==vm['vmr']:
                        #print vm['cpu']
                        vms[i]['cpu']=vm['cpu']
        with open(path['hosts'],'w') as f:
            json.dump(hosts,f)
        with open(path['vms'],'w') as f:
            json.dump(vms,f)
        time.sleep(10)



if __name__ == "__main__":

    with open('./path.json','r') as f:
        path=json.load(f)
    ses = XenAPI.Session(path['url'])
    ses.xenapi.login_with_password(path['login'], path['password'])
    try:
        main(ses)
    finally:
        ses.xenapi.session.logout()
