You can use these scripts to get some dummy data into an sqlite db.

The process should go something like this. From root dir:

python manage.py syncdb
python manage.py dbshell < 01_import_vendors.sql
python manage.py dbshell < 02_static_data.sql
