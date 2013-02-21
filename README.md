django-vegancity
================

a vegan website for every city!  

the idea is simple.  instead of building a vegan website for our city, 
we're building a vegan website that can be implemented in any city.  

quickstart
==========

The code is provided with a sample dataset that should be enough to get started. 
If you have python and django installed, you should be able to get a development server
going quickly with the following commands, from the project root directory:

python manage.py syncdb
...
follow steps / create superuser
...
python manage.py loaddata utils/data.json
python manage.py runserver

then direct your browser to localhost:8000 and start hacking!
