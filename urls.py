from django.conf.urls.defaults import patterns, include, url
from xcms.views import monitoring
from xcms.views import monitoring_ajax
from django.conf import settings
from django.contrib import admin
from xcms.views import login
from xcms.views import logout
from xcms.views import reboot_vm
from xcms.views import play_pause
from xcms.views import shutdown_vm
from xcms.views import try_host
from xcms.views import try_migrate
from xcms.views import host_action
from xcms.views import vms
from xcms.views import vms_ajax
from xcms.views import start
from xcms.views import properties
from xcms.views import migrate
from xcms.views import backup
from xcms.views import new_vm
from xcms.views import get_consoles
from xcms.views import users
from xcms.views import user_detail
from xcms.views import user_add
from xcms.views import user_change
from xcms.views import host_vnc
from xcms.views import del_vm
from xcms.views import revert
from xcms.views import from_snapshot
from xcms.views import export


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ('^$', login),
    ('^logout/$', logout),
    (r'^reboot_vm/(?P<vmr>((\w+:)+(\w+-)+\w+))/$', reboot_vm),
    (r'^play_pause/(?P<vmr>((\w+:)+(\w+-)+\w+))/$', play_pause),
    (r'^del_vm/(?P<vmr>((\w+:)+(\w+-)+\w+))/$', del_vm),
    (r'^revert/(?P<vmr>((\w+:)+(\w+-)+\w+))/$', revert),
    (r'^get_consoles/(?P<vmr>((\w+:)+(\w+-)+\w+))/$', get_consoles),
    (r'^export/(?P<vmr>((\w+:)+(\w+-)+\w+))/$', export),
    (r'^host_vnc/(?P<host_ref>((\w+:)+(\w+-)+\w+))/$', host_vnc),
    (r'^shutdown_vm/(?P<vmr>((\w+:)+(\w+-)+\w+))/$', shutdown_vm),
    (r'^start/(?P<vmr>((\w+:)+(\w+-)+\w+))/$', start),
    (r'^try_migrate/(?P<vmr>((\w+:)+(\w+-)+\w+))/$', try_migrate),
    (r'^properties/(?P<type>\w+)/(?P<ref>((\w+:)+(\w+-)+\w+))/$', properties),
    (r'^try_host/(?P<host_ref>((\w+:)+(\w+-)+\w+))/$', try_host),
    (r'^host_action/(?P<host_ref>((\w+:)+(\w+-)+\w+))/(?P<action>\w+)/$', host_action),
    ('^monitoring/$', monitoring),
    ('^monitoring_ajax/$', monitoring_ajax),
    ('^migrate/$', migrate),
    ('^from_snapshot/$', from_snapshot),
    ('^backup/$', backup),
    ('^users/$', users),
    ('^user_detail/$', user_detail),
    ('^user_add/$', user_add),
    ('^user_change/$', user_change),
    ('^new_vm/$', new_vm),
    ('^vms/$', vms),
    ('^vms_ajax/$', vms_ajax),



    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Examples:
    # url(r'^$', 'xcms.views.home', name='home'),
     #url(r'^xcms/', include('xcms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
