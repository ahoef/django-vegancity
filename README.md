VegPhilly / django-vegancity 
================
[![Build Status](https://travis-ci.org/vegphilly/vegphilly.com.png)](https://travis-ci.org/vegphilly/vegphilly.com)
[![Coverage Status](https://coveralls.io/repos/vegphilly/vegphilly.com/badge.png)](https://coveralls.io/r/vegphilly/vegphilly.com)


description
----------
a vegan website for every city!  

the idea is simple.  instead of building a vegan website for our city, 
we're building a vegan website that can be implemented in any city.  

In the meantime, you might be a little confused to see that there are 
lots of references to VegPhilly in the codebase. VegPhilly is the first 
(and hopefully not the last) implementation. We wrote VegPhilly in a hurry 
and haven't yet factored out the code to make django-vegancity pluggable. 
We will get there though!

quickstart
----------

This project is meant to be developed from within a virtualbox environment.  
Please InstallVirtualbox and Vagrant for your OS.  

Navigate to the root of this project and run:  
```vagrant up```

This will create a virtual environment, install dependencies, provide you with  
enough data to get coding right away, and fire up a runserver. Point your browser  
to ```localhost:8000``` and start editing files.  
  
When you're finished working on the site, just run ```vagrant halt``` to power down  
the VM. The next time you start it up, it will purge any changes you made to the provided  
data.  

Of course, you can work on the project without using a virtual machine, but it's on you  
to get it to work.  

additional resources
--------------------

If you have `fabric` installed on your local machine (recommended), you can use fabric
commands to automate common development tasks. Try reading the `fabfile.py` source or running
`fab -l` from the project root to see what commands are available.

FAQ
---

Having trouble? Here's some common problems and solutions.  

### development server
###### not running after ```vagrant up```
at times, for one reason or another, the django runserver doesn't start on boot.  
To start this manually, enter from the project room:
```
vagrant ssh
sudo supervisorctl restart vegphilly-runserver
```
The password for the vagrant account is 'vagrant'.

###### viewing the log in realtime
normally a django runserver runs in your terminal for debugging. If you'd like to view
the terminal to watch for output, execute:
```
vagrant ssh
cd /var/log/vegphilly/
tail -f access.log
```
###### stopping the server to free port 8000 for other things
just run
```
vagrant ssh
sudo supervisorctl stop vegphilly-runserver
```


### database error or general weirdness
Sometimes, but not often, switching branches can cause weird synchronization problems with  
your virtual machine. Try running ```vagrant destroy``` and ```vagrant up``` again to create  
a new virtual environment that is guaranteed to be configured for the branch you are working  
on.
