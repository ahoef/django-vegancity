#!/bin/sh

# Script to initialize a development server
# Ideally should be run only in conjunction
# with a vagrant initialization.

###############################
## PREPARE OS FOR APP
###############################

mkdir /var/log/vegphilly
touch /var/log/vegphilly/gunicorn-general.log
touch /var/log/vegphilly/gunicorn-access.log
touch /var/log/vegphilly/gunicorn-error.log
touch /var/log/vegphilly/django-general.log
touch /var/log/vegphilly/django-request.log
touch /var/log/vegphilly/django-sql.log
touch /var/log/vegphilly/vegancity-general.log
touch /var/log/vegphilly/vegancity-search.log
chmod -R 777 /var/log/vegphilly/
chown -R vegphilly:nogroup /var/log/vegphilly/
mkdir /var/vegphilly_backups/

###############################
## PREPARE WEBSERVER
###############################
cp -v /usr/local/vegphilly/utils/dev_env/nginx_vegphilly.conf /etc/nginx/conf.d/
rm /etc/nginx/sites-enabled/default
rm /etc/nginx/sites-available/default
sudo service nginx restart

###############################
## CREATE BACKUP CRONJOB
###############################

echo '0 2 * * * /usr/local/vegphilly/utils/db_backup.py' | crontab -

###############################
## INITIALIZE PYTHON PACKAGES
###############################
pip install -r /usr/local/vegphilly/requirements.txt

###############################
## PREPARE APP ENV
###############################
cp -v /usr/local/vegphilly/utils/dev_env/settings_local_TEMPLATE.py /usr/local/vegphilly/vegancity/settings_local.py
python /usr/local/vegphilly/manage.py syncdb --noinput
python /usr/local/vegphilly/manage.py migrate
python /usr/local/vegphilly/manage.py loaddata /usr/local/vegphilly/vegancity/fixtures/public_data.json

###############################
## REASSIGN LOG PERMISSIONS
###############################
#
# for some reason syncdb or migrate will change the owner
# of the django db backend log. supervisor will crash
# if it can't get permission to that log file.
#
chmod -R 777 /var/log/vegphilly/
chown -R vegphilly:nogroup /var/log/vegphilly/

###############################
## PREPARE GUNICORN
###############################

cp -v /usr/local/vegphilly/utils/dev_env/supervisor_vegphilly_runserver_TEMPLATE.conf /etc/supervisor/conf.d/vegphilly_runserver.conf
supervisorctl update
supervisorctl reload


