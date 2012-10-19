## XCMs: management console for XCP or XenServer


### Description

XCMs is a web based app for manage your XCP/XenServer pool.

It's alpha version, and distributed as is.

### Features

* Supports all modern browsers including mobile (iOS, Android)
* No need to modify pool.
* Can open multiple VNC console in same window(java applet now)
* Twitter bootstrap & jQueryUI on client side
* Python & Django on server side
* Ajax-based monitoring
* Role-based control
* Available in source and .xva appliance (see INSTALL paragraph)
* Licensed under the [MPL 2.0](http://www.mozilla.org/MPL/2.0/)

### Screenshots

<img src="https://dl.dropbox.com/u/14074890/monitoring.PNG" width=400>&nbsp;<img src="https://dl.dropbox.com/u/14074890/user_management.PNG" width=400>&nbsp;
<img src="https://dl.dropbox.com/u/14074890/vnc.PNG" width=400>

### Client Requirements

May not properly work in IE & Opera

JavaScript and coockes must be enabled

To use VNC [java jre](http://www.oracle.com/technetwork/java/javase/downloads/index.html) must be installed

### Server Requirements

python 2.* and django 1.3.1 must be installed(described in the INSTALL paragraph)


###How to install

XCMs installed like any other Django apps. Here is a example of installation on Ubuntu 10.04:

* Install Apache and mod_wsgi

	`sudo apt-get install apache2 libapache2-mod-wsgi`

* Install setup tools and pip

	`sudo apt-get install python-setuptools`&nbsp;	
	`sudo apt-get install python-pip`
	
* Install Django 1.3.1

	`sudo pip install http://pypi.python.org/packages/source/D/Django/Django-1.3.1.tar.gz#md5=62d8642fd06b9a0bf8544178f8500767`
	
* Edit ../xcms/apache/django.wsgi file: edit both path lines by path, where xcms located

* Edit settings.py file:
	**Enter name of you future db &nbsp;
	**Change TIME_ZONE,MEDIA_ROOT,TEMPLATE_DIRS accordingly with you path
	
* In xcms folder run:

	`python manage.py syncdb`
	
	Don't create user now!
	
* Now run:

	`python manage.py shell`
	
	`from xcms.customuser.models import CustomUser`
	
	`new_user = CustomUser.objects.create_user(username='yourname', email='', password='yourpassword')`
	
	`new_user.is_superuser=True`
	
	`new_user.save()`
	
	`exit()`
	
* Create the apache site:

	`sudo nano /etc/apache2/sites-available/xcms`
	
And paste this configuration:

	`
	<VirtualHost *:80>
    ServerName server.com
    ServerAlias www.server.com
    DocumentRoot /path/to/xcms/
    Alias /media/ /path/to/templates/media/
    Alias /static/admin/ /usr/local/lib/python2.6/dist-packages/django/contrib/admin/media/


    <Directory /path/to/xcms>
        Order allow,deny
        Allow from all
    </Directory>
   
    WSGIDaemonProcess server.com processes=2 threads=15 display-name=%{GROUP}
    WSGIProcessGroup server.com
    WSGIScriptAlias / /path/to/xcms/apache/django.wsgi

	</VirtualHost>
	`

And activate the site

	`sudo a2ensite xcms`
	
	`sudo /etc/init.d/apache2 reload`
	
* Modify path.json file: enter existing ip, url, login and pass of your pool master and right path to the hosts and vms dump files

* In file views.py modify a full path to the path.json file

* make run.py runnable

* get apache right to read path.json file

* In xcms folder run

	`python run.py`
	
* restart apache

Now you able to open youserver.com in browser and enter login/pass of user you created

Enjoy:)
