#!/bin/sh

# Script to initialize a development server
# Ideally should be run only in conjunction
# with a vagrant initialization.

apt-get update
# TODO: don't require emacs.
apt-get install -y emacs
apt-get install -y postgresql
#apt-get install -y memcached

#sudo apt-get install -y nginx
#sudo cp -v /var/projects/vegphilly/utils/nginx_vegphilly.conf /etc/nginx/conf.d/
#sudo service nginx restart

apt-get install python-pip

pip install Django
pip install south

apt-get install -y python-psycopg2