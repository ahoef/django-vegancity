#!/bin/sh

# Script to initialize a development server
# Ideally should be run only in conjunction
# with a vagrant initialization.

apt-get update

##########################
## INITIALIZE POSTGRES
##########################
apt-get install -y postgresql
echo "Creating db superuser 'vagrant'"
su postgres -c "createuser -s vagrant"
echo "Trying to delete a db called vegphilly"
su postgres -c "dropdb vegphilly"
echo "Creating db vegphilly with owner vagrant"
su postgres -c "createdb -O vagrant -l en_US.UTF8 -E UTF8 -T template0 vegphilly"

###############################
## INITIALIZE PYTHON PACKAGES
###############################
apt-get install -y python-psycopg2
apt-get install -y python-pip
pip install -r /var/projects/vegphilly/requirements.txt

###############################
## PREPARE APP ENV
###############################
cp -v /var/projects/vegphilly/utils/dev_env/settings_local_TEMPLATE.py /var/projects/vegphilly/vegancity/settings_local.py
if [ -f /var/projects/vegphilly/utils/dev_env/private_data.sql ]
then
    su vagrant -c "python /var/projects/vegphilly/manage.py dbshell < /var/projects/vegphilly/utils/dev_env/private_data.sql"
    su vagrant -c "python /var/projects/vegphilly/manage.py syncdb --noinput"
    su vagrant -c "python /var/projects/vegphilly/manage.py migrate"
else
    su vagrant -c "python /var/projects/vegphilly/manage.py syncdb --noinput"
    su vagrant -c "python /var/projects/vegphilly/manage.py migrate"
    su vagrant -c "python /var/projects/vegphilly/manage.py loaddata /var/projects/vegphilly/utils/lite_env/public_data.json"
    # TODO: switch to south, when installed
fi

###############################
## PREPARE APP ENV
###############################
apt-get install -y supervisor
cp -v /var/projects/vegphilly/utils/dev_env/supervisor_vegphilly_runserver_TEMPLATE.conf /etc/supervisor/conf.d/vegphilly_runserver.conf
mkdir /var/log/vegphilly
touch /var/log/vegphilly/log.log
chmod -R 777 /var/log/vegphilly
supervisorctl update


###############################
## COMING SOON
###############################
#apt-get install -y memcached
#apt-get install -y nginx
#cp -v /var/projects/vegphilly/utils/spin_up/nginx_vegphilly.conf /etc/nginx/conf.d/
#service nginx restart
