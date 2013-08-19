#!/bin/sh

# Script to initialize a development server
# Ideally should be run only in conjunction
# with a vagrant initialization.

###############################
## INITIALIZE PYTHON PACKAGES
###############################
pip install -r /usr/local/vegphilly/requirements.txt

###############################
## PREPARE APP ENV
###############################
cp -v /usr/local/vegphilly/utils/dev_env/settings_local_TEMPLATE.py /usr/local/vegphilly/vegancity/settings_local.py
su postgres -c "python /usr/local/vegphilly/manage.py syncdb --noinput"
su postgres -c "python /usr/local/vegphilly/manage.py migrate"
su postgres -c "python /usr/local/vegphilly/manage.py loaddata /usr/local/vegphilly/vegancity/fixtures/public_data.json"

###############################
## PREPARE APP ENV
###############################
cp -v /usr/local/vegphilly/utils/dev_env/supervisor_vegphilly_runserver_TEMPLATE.conf /etc/supervisor/conf.d/vegphilly_runserver.conf
mkdir /var/log/vegphilly
touch /var/log/vegphilly/access.log
touch /var/log/vegphilly/error.log
chmod -R 777 /var/log/vegphilly
supervisorctl update
supervisorctl reload

###############################
## PREPARE WEBSERVER
###############################
cp -v /usr/local/vegphilly/utils/dev_env/nginx_vegphilly.conf /etc/nginx/conf.d/
rm /etc/nginx/sites-enabled/default
rm /etc/nginx/sites-available/default
sudo service nginx restart

