function action(hostname,host_act,name){
    $.getJSON("/try_host/"+hostname,function(data){
        upd=$("#mod");upd.empty();
        $("#mdf").empty();

        jQuery.each(data,function(){


            upd.append('<p> Action: '+this.status.toUpperCase()+'</p>');

            var arr=this.vms;
            jQuery.each(arr,function(){
                upd.append('<p>Vm '+this.vm+' migrates to '+this.host+'</p>');

            });
            if(this.status=="possible"){
               var onc="action_submit('"+hostname+"','"+host_act+"','"+name+"')";

                upd.append('<a href="#" class="btn btn-primary" id="action" onclick="'+onc+'">'+host_act+'</a>');
            }

        });


    });
    $('#myModal').modal();

}

function action_submit(hostname,host_act,name){
  //  "/host_action/'+hostname+'/'+host_act+'"
    $('#myModal').modal('hide');
    $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
        +'<strong>'+host_act+' '+name+'!</strong></div>');
    $.getJSON("/host_action/"+hostname+'/'+host_act,function(data){

    });
}

function migrate(vmr){
    //upd=$("#mod");upd.empty();
    //upd.append('<p>Loading...</p>');

    $.getJSON("/try_migrate/"+vmr,function(data){
        upd=$("#mod");upd.empty();
        $("#mdf").empty();
        upd.append('<div   id="migrate_form">'
            +'<label class="control-label" for="host">Select host</label> '
            +'<input type="hidden" id="vmr" name="vmr" value="'+vmr+'">'
            +'<div class="span3"> <select id="host" name="host">'
            +'</select> </div>'
            +'<div class="span1"><button class="btn btn-primary" onclick="migrate_submit()" ">Migrate</button> </div>'
            +'</div>'

        );
        jQuery.each(data,function(){
            $("#host").append('<option value="'+this.host_ref+'">'+this.hostname+'</option>');
        });



    });
    $('#myModal').modal('show');



}

function migrate_submit(){
   $('#myModal').modal('hide');

   // $("#message_up").append('<button class="close" data-dismiss="alert">×</button>'
   //     +'<strong>VM is migrating...</strong>');
   // $("#message_up").show("slow");
    var options={
        type: "POST",
        //dataType: "json",
        url: "/migrate/",
        data: {host:$("#host").val(),vmr:$("#vmr").val()},
        beforeSend: function(){
            $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
                +'<strong>VM is migrating...</strong></div>');
           // $("#message_up").show("slow");
        },
        complete: function(data){
           // $("#message_up").empty();
            $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
            +'<strong>Migration Complete!</strong></div>');
            //if($("#message_up").css('display')=='none'){
               // $("#message_up").show('slow');
            //}
        }

    }
    $("#mdf").empty();
        $.ajax(options);
        //return false;



}

function backup(vmr,state){
    upd=$("#mod");upd.empty();
    if(state=="Running")
    {
        upd.append(
            '<div id="backup_form">'
                +'<div class="control-group">'
                +'<label class="control-label" for="type">Select type</label> '
                +'<input type="hidden" id="vmr" name="vmr" value="'+vmr+'">'
                +'<label class="radio">'
                +'<input type="radio" name="type" id="r1" value="disk" checked="true"/> '
                +'Disk'
                +'</label>'
                +'<label class="radio">'
                +'<input type="radio" name="type" id="r2" value="disk_mem"/> '
                +'Disk + mem'
                +'</label>'
                +'</div>'
                +'<div class="control-group">'

                +'<input class="span3" type="text" name="name" id="name" placeholder="Enter name">'
                +'</div>'
                +'<div class="control-group">'

                +'<button class="btn btn-success left" onclick="backup_submit()">Backup</button> '
                +'</div> '



                +'</div'
        );
    }
    else{
        upd.append(
            '<div id="backup_form"">'
                +'<div class="control-group">'
                +'<input type="hidden" id="vmr" name="vmr" value="'+vmr+'">'
                +'<input type="hidden" id="type" name="type" value="disk">'
                +'</div>'
                +'<div class="control-group">'
                +'<input class="input-medium" type="text" name="name" id="name" placeholder="Enter name"/>'
                +'</div>'
                +'<button class="btn btn-success left" onclick="backup_submit()">Backup</button> '
                +'</form>'
        );
    }
    $('#myModal').modal();
}


function backup_submit(){
    $('#myModal').modal('hide');
    var back_t;

    var d=document.getElementById("type");
        var t=document.getElementsByName("type");
    try{
        if(d.value=="disk"){
            back_t=d.value;
        }
    } catch(e){
        var r=document.getElementById("r1");
        if(r.checked){
            back_t=r.value;
        }
        else{
            r=document.getElementById("r2");
            back_t=r.value;
        }
    }



if(back_t=="disk"){
   var type_b="Snapshot";
}
    else{
    var type_b="Checkpoint";
}



    var options={
        type: "POST",
        url: "/backup/",
        data: {type:back_t,vmr:$("#vmr").val(),name:$("#name").val()},
        beforeSend: function(){
            $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
                +'<strong>'+type_b+' is creating...</strong></div>');
            // $("#message_up").show("slow");
        },
        complete: function(data){
            $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
                +'<strong>Creation Complete!</strong></div>');

        }

    }
    $("#mdf").empty();
    $.ajax(options);

}

function from_snapshot(vmr){
    upd=$("#mod");upd.empty();

        upd.append(
            '<div id="from_snapshot">'
                +'<div class="control-group">'
                +'<input type="hidden" id="vmr" name="vmr" value="'+vmr+'">'
                +'</div>'
                +'<div class="control-group">'
                +'<input class="input-medium" type="text" id="name" name="name" placeholder="Enter name"/>'
                +'</div>'
                +'<button class="btn btn-success left" onclick="from_snap_submit()">Create</button> '
                +'</div>'
        );
    $('#myModal').modal();
}

function from_snap_submit(){
    $('#myModal').modal('hide');
    var options={
        type: "POST",
        url: "/from_snapshot/",
        data: {vmr:$("#vmr").val(),name:$("#name").val()},
        beforeSend: function(){
            $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
                +'<strong>VM is creating...</strong></div>');
            // $("#message_up").show("slow");
        },
        complete: function(data){
            $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
                +'<strong>Creation Complete!</strong></div>');

        }

    }
    $("#mdf").empty();
    $.ajax(options);
}

function show_vm(vmr){

if(localStorage[vmr]){
    localStorage.removeItem(vmr);
}
    else{
    localStorage[vmr]=vmr;
}


       // $("#"+unic).collapse("show")

}

function update(upd){
    if(upd=="hosts"){
        $.getJSON("/monitoring_ajax/",function(data){
            var hosts=data;
            if(localStorage['param'])
            {
                var param=localStorage['param'];
                var param2=localStorage['param'].value;
                hosts=sort_json(param,hosts);
            }
            var i=0;
            jQuery.each(data,function(){
                this.fluid=false;
                var scr=$(document).width();
                span="";
                if(scr>1200){
                    span="span4";
                    if(i%3==0 & i>=3){
                        this.fluid=true;
                    }
                }
                else {
                    span="span6";
                    if(i%2==0 & i>=2){
                        this.fluid=true;
                    }
                }

                i++;
            });
            $("#main").setTemplateElement("template");
            $("#main").setParam('span',span);
            $("#main").processTemplate(hosts);
            jQuery.each(data,function(){
                var vms=this.vms;
                jQuery.each(vms,function(){
                    if(localStorage[this.vmr]==this.vmr){
                        $("#"+this.unic).addClass("in");
                    }
                });
            });
        });
    }
    else{
        $.getJSON("/vms_ajax/",function(data){
            var vms=data;
           if(localStorage['param'])
           {
               var param=localStorage['param'];
               var param2=localStorage['param'].value;
               vms=sort_json(param,vms);
           }
            var i=0;
            jQuery.each(data,function(){
                this.fluid=false;
                if(i%3==0 & i>=3){
                    this.fluid=true;
                }
                i++;
            });
            $("#main").setTemplateElement("template");
            $("#main").processTemplate(vms);
            jQuery.each(data,function(){
                var snapshots=this.snapshots;
                jQuery.each(snapshots,function(){
                    if(localStorage[this.vmr]==this.vmr){
                        $("#"+this.unic).addClass("in");
                    }
                });
            });
        });
    }

}
function new_vm_message(){
    $("#message").show("slow");
}

function reboot_vm(vmr,name){
    $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
        +'<strong>VM '+name+' is rebooting now...</strong></div>');
    $.getJSON("/reboot_vm/"+vmr,function(data){
        $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
            +'<strong>'+data.message+'</strong></div>');
    });
}

function play_pause(vmr,name){

    $.getJSON("/play_pause/"+vmr,function(data){
        $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
            +'<strong>'+data.message+'</strong></div>');

        //$("#"+vmr+name).empty();
    });
}

function shutdown_vm(vmr,name){
    $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
        +'<strong>VM '+name+' halting now...</strong></div>');
    $.getJSON("/shutdown_vm/"+vmr,function(data){
        $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
            +'<strong>'+data.message+'</strong></div>');
    });
}

function get_consoles(vmr,name,unic){
   // $("#console").empty();

    $.getJSON("/get_consoles/"+vmr,function(data){
        var param=data;

        $("#console").append('<div id="console'+unic+'" title=" VNC '+name+'"></div>');
        $("#console"+unic).setTemplateElement("vnc");
        $("#console"+unic).processTemplate(param);
        $("#console"+unic).dialog({ height: 470,width: 650 });
    });


}
function host_vnc(vmr,name,unic){
    // $("#console").empty();
    $.getJSON("/host_vnc/"+vmr,function(data){
        var param=data;

        $("#console").append('<div id="console'+unic+'" title=" VNC '+name+'"></div>');
        $("#console"+unic).setTemplateElement("vnc");
        $("#console"+unic).processTemplate(param);
        $("#console"+unic).dialog({ height: 470,width: 650 });
    });


}
function start_vm(vmr,name){
    $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
        +'<strong>VM '+name+' starting...</strong></div>');
    $.getJSON("/start/"+vmr,function(data){
        $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
            +'<strong>'+data.message+'</strong></div>');
    });
}

function del_vm(vmr,name){
    $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
        +'<strong>Removing '+name+' start...</strong></div>');
    $.getJSON("/del_vm/"+vmr,function(data){
        $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
            +'<strong>'+data.message+'</strong></div>');
    });
}

function revert(vmr,name,vm_name){
    $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
        +'<strong>Reverting '+vm_name+' from snapshot '+name+'</strong></div>');
    $.getJSON("/revert/"+vmr,function(data){
        $("#message").append('<div class="alert"> <button class="close" data-dismiss="alert">×</button>'
            +'<strong>'+data.message+'</strong></div>');
    });
}

function sort_json(prop,arr){
arr=arr.sort(function(a,b){
    if(prop=='name'){
        return (a[prop]>b[prop]);
    }
    return (a[prop]<b[prop]);
});
    return arr;
}

function sort_click(param,upd){
    localStorage['param']=param;
    update(upd);
}