#!/bin/sh

# Script to initialize a development server
# Ideally should be run only in conjunction
# with a vagrant initialization.

###############################
## INITIALIZE PYTHON PACKAGES
###############################
pip install -r /var/projects/vegphilly/requirements.txt

###############################
## PREPARE APP ENV
###############################
cp -v /var/projects/vegphilly/utils/dev_env/settings_local_TEMPLATE.py /var/projects/vegphilly/vegancity/settings_local.py
su vagrant -c "python /var/projects/vegphilly/manage.py syncdb --noinput"
su vagrant -c "python /var/projects/vegphilly/manage.py migrate"
su vagrant -c "python /var/projects/vegphilly/manage.py loaddata /var/projects/vegphilly/vegancity/fixtures/public_data.json"

###############################
## PREPARE APP ENV
###############################
cp -v /var/projects/vegphilly/utils/dev_env/supervisor_vegphilly_runserver_TEMPLATE.conf /etc/supervisor/conf.d/vegphilly_runserver.conf
mkdir /var/log/vegphilly
touch /var/log/vegphilly/log.log
chmod -R 777 /var/log/vegphilly
supervisorctl update
supervisorctl reload
