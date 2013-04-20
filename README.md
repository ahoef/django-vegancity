VegPhilly / django-vegancity 
================
[![Build Status](https://travis-ci.org/vegphilly/vegphilly.com.png)](https://travis-ci.org/vegphilly/vegphilly.com)


a vegan website for every city!  

the idea is simple.  instead of building a vegan website for our city, 
we're building a vegan website that can be implemented in any city.  

In the meantime, you might be a little confused to see that there are 
lots of references to VegPhilly in the codebase. VegPhilly is the first 
(and hopefully not the last) implementation. We wrote VegPhilly in a hurry 
and haven't yet factored out the code to make django-vegancity pluggable. 
We will get there though!

quickstart
==========

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

current contributors
====================

Having trouble?  

Sometimes, but not often, switching branches can cause weird synchronization problems with  
your virtual machine. Try running ```vagrant destroy``` and ```vagrant up``` again to create  
a new virtual environment that is guaranteed to be configured for the branch you are working  
on.
