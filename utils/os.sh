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
