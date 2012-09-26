django-vegancity
================

a vegan website for every city!  

the idea is simple.  instead of building a vegan website for our city, we're building a vegan website that can be implemented in any city.  

project notes
=============
for the moment, all development notes and bugs will exist in this file.

the database is not distributed with this project.  In order to use this code,
one must run:

~ django-vegancity/$ python manage.py syncdb

to create the following file:

django-vegancity/vegancity/db                  - this is the sqlite database file used, until we outgrow it.  

todo:
====
-Get some dummy data for Philadelphia into vegacity/script.py  
-work on search page (extensively)  
-set up user account models  
-set up user review system  
-Pretty much everything...  
