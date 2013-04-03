django-vegancity
================

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

The code is provided with a sample dataset that should be enough to get started. 
If you have python and django installed, you should be able to get a development server
going quickly with the following commands, from the project root directory:  
  
python manage.py syncdb  
...  
follow steps / create superuser  
...  
python manage.py loaddata vegancity/fixtures/public_data.json  
python manage.py runserver  
  
then direct your browser to localhost:8000 and start hacking!

current contributors
====================

Having trouble?

Sometimes commits can fall out of sync with your database. That's why your development
database is meant to be thrown out. Just delete your development db (vegancity/db) and
run the quickstart commands above.
