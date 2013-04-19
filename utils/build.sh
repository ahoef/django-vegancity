#!/bin/sh

# Script to initialize a development server
# Ideally should be run only in conjunction
# with a vagrant initialization.

apt-get update

##########################
## INITIALIZE POSTGRES
##########################
apt-get install -y postgresql postgresql-server-dev-9.1
apt-get install -y postgis postgresql-9.1-postgis

POSTGIS_SQL_PATH=`pg_config --sharedir`/contrib/postgis-1.5
# Creating the template spatial database.
su postgres -c "dropdb template_postgis"
su postgres -c "createdb -l en_US.UTF8 -E UTF8 -T template0 template_postgis"
su postgres -c "createlang -d template_postgis plpgsql"
# Allows non-superusers the ability to create from this template
su postgres -c "psql -d postgres -c \"UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';\""
# Loading the PostGIS SQL routines
su postgres -c "psql -d template_postgis -f $POSTGIS_SQL_PATH/postgis.sql"
su postgres -c "psql -d template_postgis -f $POSTGIS_SQL_PATH/spatial_ref_sys.sql"
# Enabling users to alter spatial tables.
su postgres -c "psql -d template_postgis -c \"GRANT ALL ON geometry_columns TO PUBLIC;\""
su postgres -c "psql -d template_postgis -c \"GRANT ALL ON geography_columns TO PUBLIC;\""
su postgres -c "psql -d template_postgis -c \"GRANT ALL ON spatial_ref_sys TO PUBLIC;\""


echo "Creating db superuser 'vagrant'"
su postgres -c "createuser -s vagrant"
echo "Trying to delete a db called vegphilly"
su postgres -c "dropdb vegphilly"
echo "Creating db vegphilly with owner vagrant"
su postgres -c "createdb -O vagrant -l en_US.UTF8 -E UTF8 -T template_postgis vegphilly"



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
    su vagrant -c "python /var/projects/vegphilly/manage.py loaddata /var/projects/vegphilly/vegancity/fixtures/public_data.json"
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
supervisorctl reload


###############################
## COMING SOON
###############################
#apt-get install -y memcached
#apt-get install -y nginx
#cp -v /var/projects/vegphilly/utils/spin_up/nginx_vegphilly.conf /etc/nginx/conf.d/
#service nginx restart
