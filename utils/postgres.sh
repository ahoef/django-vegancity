#!/bin/sh

##########################
## INITIALIZE POSTGRES
##########################

POSTGIS_SQL_PATH=`pg_config --sharedir`/contrib/postgis-1.5
# Creating the template spatial database.
su postgres -c "psql -d postgres -c \"UPDATE pg_database SET datistemplate='false' WHERE datname='template_postgis';\""
su postgres -c "dropdb template_postgis"
su postgres -c "createdb -l en_US.UTF8 -E UTF8 -T template0 template_postgis"
su postgres -c "psql -d postgres -c \"UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';\""
# Loading the PostGIS SQL routines
su postgres -c "psql -d template_postgis -f $POSTGIS_SQL_PATH/postgis.sql"
su postgres -c "psql -d template_postgis -f $POSTGIS_SQL_PATH/spatial_ref_sys.sql"
su postgres -c "psql -d template_postgis -c \"GRANT ALL ON geometry_columns TO PUBLIC;\""
su postgres -c "psql -d template_postgis -c \"GRANT ALL ON geography_columns TO PUBLIC;\""
su postgres -c "psql -d template_postgis -c \"GRANT ALL ON spatial_ref_sys TO PUBLIC;\""


echo "Creating db superuser 'vagrant'"
su postgres -c "createuser -s vagrant"
echo "Trying to delete a db called vegphilly"
su postgres -c "dropdb vegphilly"
echo "Creating db vegphilly with owner vagrant"
su postgres -c "createdb -O vagrant -l en_US.UTF8 -E UTF8 -T template_postgis vegphilly"

