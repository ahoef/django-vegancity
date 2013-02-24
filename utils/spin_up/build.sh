#!/bin/sh

# Script to initialize a development server
# Ideally should be run only in conjunction
# with a vagrant initialization.

#echo 'LC_ALL="en_US.UTF-8"' > /etc/default/locale
#echo 'LANG=en_US.UTF-8' >> /etc/default/locale
#update-locale LC_CTYPE="en_US.UTF-8" LC_ALL="en_US.UTF-8" LANG="en_US.UTF-8"

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
pip install Django
pip install south
pip install Gunicorn

###############################
## PREPARE APP ENV
###############################
cp -v /var/projects/vegphilly/utils/spin_up/settings_local_TEMPLATE.py /var/projects/vegphilly/vegancity/settings_local.py
if [ -f /var/projects/vegphilly/utils/spin_up/data.sql ]
then
    su vagrant -c "python /var/projects/vegphilly/manage.py dbshell < /var/projects/vegphilly/utils/spin_up/data.sql"
else
    su vagrant -c "python /var/projects/vegphilly/manage.py syncdb --noinput"
    # This was needed at some point while messing with south, and may be needed again
    # su vagrant -c "python /var/projects/vegphilly/manage.py schemamigration vegancity --initial"
    # su vagrant -c "python /var/projects/vegphilly/manage.py migrate vegancity"
    su vagrant -c "python /var/projects/vegphilly/manage.py loaddata /var/projects/vegphilly/utils/data.json"
fi

###############################
## COMING SOON
###############################
#apt-get install -y memcached
#apt-get install -y nginx
#cp -v /var/projects/vegphilly/utils/spin_up/nginx_vegphilly.conf /etc/nginx/conf.d/
#service nginx restart
