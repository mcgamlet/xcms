from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from XenAPI import Session
from xcms.forms import LoginForm
from xcms.customuser.forms import Change
from django.contrib import auth
from django.utils import simplejson
from xmlrpclib import *
from xcms.customuser.models import CustomUser
from xcms.VM.models import VM
from django.contrib.auth.forms import UserCreationForm
import time
import json
import httplib
import base64
import urllib
import datetime

#open config file
with open('/home/user/xcms/path.json','r') as f:
    path=json.load(f)
#open session
ses=Session(path['url'])
ses.xenapi.login_with_password(path['login'],path['password'])

def monitoring(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            #read dump
            with open(path['hosts'],'r') as f:
                hosts=json.load(f)

            #server-side sort array
            if 'sort' in request.GET:
                sort=request.GET['sort']
                if sort=='name':
                    hosts.sort(key=lambda host: host['name'])
                elif sort=='state':
                    hosts.sort(key=lambda host: host['power_state'],reverse=True)
                else:
                    hosts.sort(key=lambda host: host['mem'],reverse=True)
            else: hosts.sort(key=lambda host: host['name'])
            
            #need stuff for template
            for i in range(len(hosts)):
                hosts[i]['fluid']=False
                if i%3==0 and i>=3:
                    hosts[i]['fluid']=True

            return render_to_response('monitoring.html',locals())
            #not superuser can't access to hosts, only vms
        else: return HttpResponseRedirect('/vms/')
    else: return HttpResponseRedirect('/')

#for ajax updates, no need refresh page
def monitoring_ajax(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:

            with open(path['hosts'],'r') as f:
                hosts=json.load(f)

            if 'sort' in request.GET:
                sort=request.GET['sort']
                if sort=='name':
                    hosts.sort(key=lambda host: host['name'])
                elif sort=='state':
                    hosts.sort(key=lambda host: host['power_state'],reverse=True)
                else:
                    hosts.sort(key=lambda host: host['mem'],reverse=True)
            else: hosts.sort(key=lambda host: host['name'])

            for i in range(len(hosts)):
                hosts[i]['fluid']=False
                if i%3==0 and i>=3:
                    hosts[i]['fluid']=True
            data=simplejson.dumps(hosts)

            return HttpResponse(data,'text/javascript')
        else: return HttpResponseRedirect('/vms/')
    else: return HttpResponseRedirect('/')

def vms(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            with open(path['vms'],'r') as f:
                vms=json.load(f)


            if 'sort' in request.GET:
                sort=request.GET['sort']
                if sort=='name':
                    vms.sort(key=lambda vm: vm['name'])
                elif sort=='state':
                    vms.sort(key=lambda vm: vm['power_state'],reverse=True)
                else:
                    vms.sort(key=lambda vm: vm['mem'],reverse=True)
            else: vms.sort(key=lambda vm: vm['name'])


            for i in range(len(vms)):
                vms[i]['fluid']=False
                if i%3==0 and i>=3:
                    vms[i]['fluid']=True

            return render_to_response('vms.html',locals())
        else:
            #get vms, available for user
            vms_tab=request.user.vms.all()

            with open(path['vms'],'r') as f:
                vms=json.load(f)

            if 'sort' in request.GET:
                sort=request.GET['sort']
                if sort=='name':
                    vms.sort(key=lambda vm: vm['name'])
                elif sort=='state':
                    vms.sort(key=lambda vm: vm['power_state'],reverse=True)
                else:
                    vms.sort(key=lambda vm: vm['mem'],reverse=True)
            else: vms.sort(key=lambda vm: vm['name'])

            vms2=vms
            vms=[]
            for vm in vms2:
                for vm_t in vms_tab:
                    if vm['vmr']==vm_t.vmr:
                        vms.append(vm)

            for i in range(len(vms)):
                vms[i]['fluid']=False
                if i%3==0 and i>=3:
                    vms[i]['fluid']=True

            return render_to_response('vms.html',locals())
    else: return HttpResponseRedirect('/')

#for ajax updates, no need refresh page
def vms_ajax(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            with open(path['vms'],'r') as f:
                vms=json.load(f)
            if 'sort' in request.GET:
                sort=request.GET['sort']
                if sort=='name':
                    vms.sort(key=lambda vm: vm['name'])
                elif sort=='state':
                    vms.sort(key=lambda vm: vm['power_state'],reverse=True)
                else:
                    vms.sort(key=lambda vm: vm['mem'],reverse=True)
            else: vms.sort(key=lambda vm: vm['name'])
            for i in range(len(vms)):
                vms[i]['fluid']=False
                if i%3==0 and i>=3:
                    vms[i]['fluid']=True
            data=simplejson.dumps(vms)

            return HttpResponse(data,'text/javascript')
        else:
            vms_tab=request.user.vms.all()

            with open(path['vms'],'r') as f:
                vms=json.load(f)

            if 'sort' in request.GET:
                sort=request.GET['sort']
                if sort=='name':
                    vms.sort(key=lambda vm: vm['name'])
                elif sort=='state':
                    vms.sort(key=lambda vm: vm['power_state'],reverse=True)
                else:
                    vms.sort(key=lambda vm: vm['mem'],reverse=True)
            else: vms.sort(key=lambda vm: vm['name'])

            vms2=vms
            vms=[]
            for vm in vms2:
                for vm_t in vms_tab:
                    if vm['vmr']==vm_t.vmr:
                        vms.append(vm)

            for i in range(len(vms)):
                vms[i]['fluid']=False
                if i%3==0 and i>=3:
                    vms[i]['fluid']=True

            data=simplejson.dumps(vms)

            return HttpResponse(data,'text/javascript')
    else: return HttpResponseRedirect('/')


def login(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=request.POST.get('username','')
            password=request.POST.get('password','')
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('monitoring')
            else:
                err='Invalid username or password'
                form3=LoginForm()
                return render_to_response('login.html',locals())
        else:
            err='Unable to connect'
            form2=LoginForm()
            return render_to_response('login.html',locals())
    else:
        visible='hidden'
        if request.user.is_authenticated():
            if request.user.is_superuser:
                return HttpResponseRedirect('monitoring')
            else: return HttpResponseRedirect('/vms/')
        else:
            form=LoginForm()
            return render_to_response('login.html',{'form': form})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')



def reboot_vm(request,vmr):
    if request.user.is_authenticated():
            task=ses.xenapi.Async.VM.hard_reboot(vmr)
            finished=False
            while not finished:
                finished=True
                record=ses.xenapi.task.get_record(task)
                if record["status"]!="success":
                    finished=False
                time.sleep(1)
            message={"message":"Reboot success!"}
            data=simplejson.dumps(message)
            return HttpResponse(data,'text/javascript')
    else: return HttpResponseRedirect('/')

def play_pause(request,vmr):
    if request.user.is_authenticated():
        vm=ses.xenapi.VM.get_record(vmr)
        if vm['power_state']=='Running':
            task=ses.xenapi.Async.VM.pause(vmr)
            finished=False
            while not finished:
                finished=True
                record=ses.xenapi.task.get_record(task)
                if record["status"]!="success":
                    finished=False
                time.sleep(1)
            message={"message":"VM paused!"}
            data=simplejson.dumps(message)
            return HttpResponse(data,'text/javascript')
        else:
            task=ses.xenapi.Async.VM.unpause(vmr)
            finished=False
            while not finished:
                finished=True
                record=ses.xenapi.task.get_record(task)
                if record["status"]!="success":
                    finished=False
                time.sleep(1)
            message={"message":"VM unpaused!"}
            data=simplejson.dumps(message)
            return HttpResponse(data,'text/javascript')
        return HttpResponseRedirect('/monitoring/')
    else: return HttpResponseRedirect('/')

def shutdown_vm(request,vmr):
    if request.user.is_authenticated():
        task=ses.xenapi.Async.VM.hard_shutdown(vmr)
        finished=False
        while not finished:
            finished=True
            record=ses.xenapi.task.get_record(task)
            if record["status"]!="success":
                finished=False
            time.sleep(1)
        message={"message":"VM halted!"}
        data=simplejson.dumps(message)
        return HttpResponse(data,'text/javascript')
    else: return HttpResponseRedirect('/')

def start(request,vmr):
    if request.user.is_authenticated():
        try:
            task=ses.xenapi.Async.VM.start(vmr,False,True)
            finished=False
            while not finished:
                finished=True
                record=ses.xenapi.task.get_record(task)
                if record["status"]=="pending":
                    finished=False
                time.sleep(1)
            if record["status"]=="success":
                message={"message":"VM started!"}
            else:
                message={"message":"Error:VM not started"}
            data=simplejson.dumps(message)
            return HttpResponse(data,'text/javascript')
        except Exception:
            message={"message":"Error:VM not started"}
            data=simplejson.dumps(message)
            return HttpResponse(data,'text/javascript')
        return HttpResponseRedirect('/vms/')
    else: return HttpResponseRedirect('/')

def try_host(request,host_ref):
    dict=[]
    vms=[]
    vms_new=[]
    vm_count=0
    with open(path['hosts'],'r') as f:
        hosts=json.load(f)

    for host in hosts:
        if host['host_ref']!=host_ref:
            host['vms']=[]
            dict.append(host)
        else:
            for vm in host['vms']:
                vms.append(vm)
            vm_count=len(host['vms'])
    for vm in vms:
        for host in dict:
            if vm['mem']<host['free_mem']:
                host['vms'].append(vm)
                host['free_mem']=host['free_mem']-vm['mem']
                vm_count=vm_count-1
                break
    dict2=[]
    dict0=[]
    if not vm_count:
        for host in dict:
            for vm in host['vms']:
                rect2={"vm":vm['name'],"host":host['name']}
                dict2.append(rect2)
        rect={'status':'possible',"vms":dict2}
        dict0.append(rect)

    else:
        dict0=[]
        rect={"status":"impossible"}
        dict0.append(rect)
    json_1=simplejson.dumps(dict0)
    return HttpResponse(json_1,'text/javascript')

def host_action(request,host_ref,action):
    if request.user.is_authenticated():
        dict=[]
        vms=[]
        vms_new=[]
        vm_count=0
        with open(path['hosts'],'r') as f:
            hosts=json.load(f)
        for host in hosts:
            if host['host_ref']!=host_ref:
                host['vms']=[]
                dict.append(host)
            else:
                for vm in host['vms']:
                    vms.append(vm)
                vm_count=len(host['vms'])
        for vm in vms:
            for host in dict:
                if vm['mem']<host['free_mem']:
                    host['vms'].append(vm)
                    host['free_mem']=host['free_mem']-vm['mem']
                    vm_count=vm_count-1
                    break
        for host in dict:
            for vm in host['vms']:
                rec={"live":"true"}
                task=ses.xenapi.VM.pool_migrate(vm['vmr'],host['host_ref'],rec)
        for host in hosts:
            if host['host_ref']==host_ref:
                if action=="Reboot":
                    ses.xenapi.host.disable(host['host_ref'])
                    task=ses.xenapi.Async.host.reboot(host['host_ref'])
                elif action=="Shutdown":
                    ses.xenapi.host.disable(host['host_ref'])
                    ses.xenapi.host.shutdown(host['host_ref'])
        data={"message":"success"}
        data=simplejson.dumps(data)
        return HttpResponse(data,'text/javascript')
    else: return HttpResponseRedirect('/')

def properties(request,type,ref):
    if request.user.is_authenticated():
        options={}
        if type=="host":
            options=ses.xenapi.host.get_record(ref)
        elif type=="vm":
            options=ses.xenapi.VM.get_record(ref)
        options2=options.iteritems()
        options3=options.itervalues()
        options4=options.iterkeys()
        return render_to_response("properties.html",locals())
    else: return HttpResponseRedirect('/')

def try_migrate(request,vmr):
    if request.user.is_authenticated():
        hoho=[]
        set=ses.xenapi.VM.get_possible_hosts(vmr)
        resid=ses.xenapi.VM.get_resident_on(vmr)
        with open(path['hosts'],'r') as f:
            hosts=json.load(f)
        for host in hosts:
            for hrec in set:
                if host['host_ref']==hrec and hrec!=resid:
                    rec={"hostname":host['name'],"host_ref":host['host_ref']}
                    hoho.append(rec)
        json_1=simplejson.dumps(hoho)
        return HttpResponse(json_1,'text/javascript')
    else: return HttpResponseRedirect('/')

def migrate(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            host=request.POST.get('host','')
            vmr=request.POST.get('vmr','')
            rec={"live":"true"}
            task=ses.xenapi.Async.VM.pool_migrate(vmr,host,rec)
            finished=False
            while not finished:
                finished=True
                record=ses.xenapi.task.get_record(task)
                if record["status"]!="success":
                    finished=False
                time.sleep(1)
            message={"message":"Migrate done!"}
            data=simplejson.dumps(message)
            return HttpResponse(data,'text/javascript')
        else: return HttpResponseRedirect('/')
    else: return HttpResponseRedirect('/')

def backup(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            type=request.POST.get('type','')
            vmr=request.POST.get('vmr','')
            name=request.POST.get('name','')
            if type=="disk":
                task=ses.xenapi.Async.VM.snapshot(vmr,name)
                finished=False
                while not finished:
                    finished=True
                    record=ses.xenapi.task.get_record(task)
                    if record["status"]!="success":
                        finished=False
                    time.sleep(1)
                message={"message":"Creating snapshot"}
                data=simplejson.dumps(message)
                return HttpResponse(data,'text/javascript')
            elif type=="disk_mem":
                task=ses.xenapi.Async.VM.checkpoint(vmr,name)
                finished=False
                while not finished:
                    finished=True
                    record=ses.xenapi.task.get_record(task)
                    if record["status"]!="success":
                        finished=False
                    time.sleep(1)
                message={"message":"Creating snapshot"}
                data=simplejson.dumps(message)
                return HttpResponse(data,'text/javascript')
        else: return HttpResponseRedirect('/monitoring/')
    else: return HttpResponseRedirect('/')

def new_vm(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            err=[]
            if request.POST.get('name',''):
                name=request.POST.get('name','')
            else: err.append("Enter name")
            if request.POST.get('vCPUs',''):
                try:
                    vCPUs=int(request.POST.get('vCPUs',''))
                except Exception:
                    vCPUs=-1
                if vCPUs<1 or vCPUs>request.user.core_num:
                    err.append("Wrong vCPUs num")
            if request.POST.get('mem',''):
                try:
                    mem=int(request.POST.get('mem',''))
                except Exception:
                    mem=-1
                if mem<256 or mem>request.user.mem_limit:
                    err.append("Wrong mem value")
            template=request.POST.get('template','')


            if request.POST.get('host_ref',''):
                host_ref=request.POST.get('host_ref','')
            if err:
                templates=[]
                get_templates(ses,templates)
                return render_to_response('new_vm.html',locals())
            else:
                vm=ses.xenapi.VM.clone(template,name)
                ses.xenapi.VM.set_PV_args(vm, "noninteractive")
                pool = ses.xenapi.pool.get_all()[0]
                ses.xenapi.Async.VM.provision(vm)
                try:
                    if vCPUs:
                        ses.xenapi.VM.set_VCPUs_max(vm,str(vCPUs))
                        ses.xenapi.VM.set_VCPUs_at_startup(vm,str(vCPUs))
                except Exception : pass
                #try:
                if mem:
                    try:
                        ses.xenapi.VM.set_memory_static_min(vm,str(256*1024*1024))
                        ses.xenapi.VM.set_memory_dynamic_min(vm,str(256*1024*1024))
                        ses.xenapi.VM.set_memory_static_max(vm,str(mem*1024*1024))
                        ses.xenapi.VM.set_memory_dynamic_max(vm,str(mem*1024*1024))
                    except Exception : pass



                #except Exception : pass
                if request.POST.get('run',''):
                    try:
                            ses.xenapi.VM.start_on(vm,host_ref,False,True)
                            return HttpResponseRedirect('/monitoring/')
                    except Exception : pass
                    try:
                        ses.xenapi.VM.start(vm,False,True)
                        return HttpResponseRedirect('/monitoring/')
                    except Exception: return HttpResponseRedirect('/monitoring/')

                return HttpResponseRedirect('/monitoring/')

            return HttpResponseRedirect('/')
        else:
            if 'host_ref' in request.GET:
                host_ref=request.GET['host_ref']
            templates=[]
            get_templates(ses,templates)
            templates.sort(key=lambda vm: vm['name'])
            return render_to_response('new_vm.html',locals())
    else: return HttpResponseRedirect('/')


def del_vm(request,vmr):
    if request.user.is_authenticated():
        task=ses.xenapi.Async.VM.destroy(vmr)
        finished=False
        while not finished:
            finished=True
            record=ses.xenapi.task.get_record(task)
            if record["status"]!="success":
                finished=False
            time.sleep(1)
        message={"message":"VM deleted!"}
        data=simplejson.dumps(message)
        return HttpResponse(data,'text/javascript')
    else: return HttpResponseRedirect('/')

def revert(request,vmr):
    if request.user.is_authenticated():
        task=ses.xenapi.Async.VM.revert(vmr)
        finished=False
        while not finished:
            finished=True
            record=ses.xenapi.task.get_record(task)
            if record["status"]!="success":
                finished=False
            time.sleep(1)
        message={"message":"VM reverted from snapshot!"}
        data=simplejson.dumps(message)
        return HttpResponse(data,'text/javascript')
    else: return HttpResponseRedirect('/')

def from_snapshot(request):
    if request.user.is_authenticated():
        if request.method=='POST':
            if request.POST.get('name','') and request.POST.get('vmr',''):
                vmr=request.POST.get('vmr','')
                name=request.POST.get('name','')
            vm=ses.xenapi.VM.clone(vmr,name)
            ses.xenapi.VM.set_PV_args(vm, "noninteractive")
            ses.xenapi.VM.provision(vm)
            message={"message":"VM from snapshot created!"}
            data=simplejson.dumps(message)
            return HttpResponse(data,'text/javascript')
        else: return HttpResponseRedirect('vms')
    else: return HttpResponseRedirect('/')

def host_vnc(request,host_ref):
    if request.user.is_authenticated():
        host_refs=ses.xenapi.host.get_all()
        for i in range(len(host_refs)):
            vmrs=ses.xenapi.host.get_resident_VMs(host_refs[i])
            for vmr in vmrs:
                if ses.xenapi.VM.get_is_control_domain(vmr):
                    if host_ref==host_refs[i]:
                        cons=ses.xenapi.VM.get_consoles(vmr)
                        for con in cons:
                            loc=ses.xenapi.console.get_location(con)
                        sesid=ses._session
                        data={"sesid":sesid,"loc":loc}
                        data=simplejson.dumps(data)
                        return HttpResponse(data,'text/javascript')
    else: return HttpResponseRedirect('/')

def get_consoles(request,vmr):
    if request.user.is_authenticated():
        cons=ses.xenapi.VM.get_consoles(vmr)
        for con in cons:
            loc=ses.xenapi.console.get_location(con)
        sesid=ses._session
        data={"sesid":sesid,"loc":loc}
        data=simplejson.dumps(data)
        return HttpResponse(data,'text/javascript')
    else: return HttpResponseRedirect('/')

def users(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        users=CustomUser.objects.all()
        return render_to_response('users.html',locals())
    else: return HttpResponseRedirect('/')

def user_detail(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        if 'username' in request.GET:
            user=CustomUser.objects.get(username=request.GET['username'])
            vms=user.vms.all()
            return render_to_response('user_det.html',locals())
        else: return HttpResponseRedirect('/users/')
    else: return HttpResponseRedirect('/')

def user_add(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        form = Change()
        if request.method == 'POST':
            vm_list=request.POST.getlist('vmSelect')
            form = Change(request.POST)
            data = request.POST.copy()
            if form.is_valid():
                username=request.POST.get('username','')
                password=request.POST.get('password','')
                try:
                    user=CustomUser.objects.get(username=username)
                except Exception: user=None
                if not user:
                    new_user = CustomUser.objects.create_user(username=username,email='',password=password)
                    if request.POST.get('core_num'):
                        new_user.core_num=int(request.POST.get('core_num'))
                    if request.POST.get('mem_limit'):
                        new_user.mem_limit=int(request.POST.get('mem_limit'))
                    new_user.save()
                    vms=VM.objects.all()
                    if request.POST.get('is_superuser',''):
                        for vm in vms:
                            new_user.vms.add(vm)
                        new_user.is_superuser=True
                    else:
                        new_user.is_superuser=False
                        if vm_list:
                            for vmr in vm_list:
                                for vm in vms:
                                    if vm.vmr==vmr:
                                        new_user.vms.add(vm)
                    if request.POST.get('email',''):
                        new_user.email=request.POST.get('email','')
                    new_user.save()
                else:
                    error="User already exist"
                    action='/user_add/'
                    vms=VM.objects.all()

                    return render_to_response('change.html',locals())
                message="User created"
                users=CustomUser.objects.all()


                return render_to_response('users.html',locals())
            else:
                with open(path['vms'],'r') as f:
                    vms=json.load(f)
                for vm in vms:
                    try: vm2=VM.objects.get(vmr=vm['vmr'])
                    except Exception: vm2=None
                    if not vm2:
                        new_vm=VM.objects.create(name=vm['name'],vmr=vm['vmr'])
                        new_vm.save()
                action='/user_add/'
                vms=VM.objects.all()
                error = "form invalid"
                return render_to_response('change.html',locals())

        else:
            with open(path['vms'],'r') as f:
                vms=json.load(f)
            for vm in vms:
                try: vm2=VM.objects.get(vmr=vm['vmr'])
                except Exception: vm2=None
                if not vm2:
                    new_vm=VM.objects.create(name=vm['name'],vmr=vm['vmr'])
                    new_vm.save()
            action='/user_add/'
            vms=VM.objects.all()
            #new user

            return render_to_response('change.html',locals())

    else: return HttpResponseRedirect('/')

def user_change(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        if request.method=='POST':
            vm_list=request.POST.getlist('vmSelect')
            user=request.POST.get('user')
            user=CustomUser.objects.get(username=user)
            form = Change(request.POST)
            if form.is_valid():
                user.delete()
                user=CustomUser.objects.create_user(username=request.POST.get('username'),email='',password=request.POST.get('password'))
                if request.POST.get('core_num'):
                    user.core_num=int(request.POST.get('core_num'))
                if request.POST.get('mem_limit'):
                    user.mem_limit=int(request.POST.get('mem_limit'))
                vms=VM.objects.all()
                if request.POST.get('is_superuser',''):
                    for vm in vms:
                        user.vms.add(vm)
                    user.is_superuser=True
                else :
                    user.vms.clear()
                    if vm_list:
                        for vmr in vm_list:
                            for vm in vms:
                                if vm.vmr==vmr:
                                    user.vms.add(vm)
                    user.is_superuser=False
                if request.POST.get('email',''):
                    user.email=request.POST.get('email','')
                user.save()
                users=CustomUser.objects.all()
                message="User changed"
                return render_to_response('users.html',locals())
            else:
                form=Change({'username':user.username,'email':user.email, 'core_num':user.core_num,'mem_limit':user.mem_limit})
                with open(path['vms'],'r') as f:
                    vms=json.load(f)
                for vm in vms:
                    try: vm2=VM.objects.get(vmr=vm['vmr'])
                    except Exception: vm2=None
                    if not vm2:
                        new_vm=VM.objects.create(name=vm['name'],vmr=vm['vmr'])
                        new_vm.save()
                action='/user_change/'
                vms=VM.objects.all()
                errors = form.errors
                form.user=user.username
                return render_to_response('change.html',locals())

        if 'username' in request.GET:
            user=CustomUser.objects.get(username=request.GET['username'])
            #del user
            if 'del' in request.GET:
                user.delete()
                message="User deleted"
                users=CustomUser.objects.all()
                return render_to_response('users.html',locals())
            form=Change({'username':user.username,'email':user.email, 'core_num':user.core_num,'mem_limit':user.mem_limit})
            form.username=user.username
            form.core_num=user.core_num
            form.mem_limit=user.mem_limit
            form.user=user.username
            action='/user_change/'
            with open(path['vms'],'r') as f:
                vms=json.load(f)
            for vm in vms:
                try: vm2=VM.objects.get(vmr=vm['vmr'])
                except Exception: vm2=None
                if not vm2:
                    new_vm=VM.objects.create(name=vm['name'],vmr=vm['vmr'])
                    new_vm.save()
            action='/user_change/'
            vms=VM.objects.all()
            return render_to_response('change.html',locals())

        else: return HttpResponseRedirect('/user_add/')
    else: return HttpResponseRedirect('/')

def export(request,vmr):
	with open(path['vms'],'r') as f:
		vms=json.load(f)
	name="vm_export"
	url=""
	for vm in vms:
		for snapshot in vm['snapshots']:
			if snapshot['vmr']==vmr:
				name=str(vm['name'])+'_snapshot'
				url=snapshot['export']
	f=urllib.urlopen(url)
	response=HttpResponse(file2G(f),content_type='application/x-download')
	response['Content-Disposition']="attachment; filename=\"%s\"" % (name + ".xva")
	return response

def file2G(f):
    while True:
        data = f.read(1024 * 8)
        if not data:
            break
        yield data


