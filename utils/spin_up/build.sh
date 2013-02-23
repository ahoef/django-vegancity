#!/bin/sh

# Script to initialize a development server
# Ideally should be run only in conjunction
# with a vagrant initialization.

sudo apt-get update
# sorry for hogging bandwidth
# but the vegphilly team needs
# emacs to do everything.
# TODO: don't require emacs.
sudo apt-get install emacs
sudo apt-get install -y postgresql
sudo apt-get install -y memcached

sudo apt-get install -y nginx
sudo cp -v /var/projects/vegphilly/utils/nginx_vegphilly.conf /etc/nginx/conf.d/
sudo service nginx restart

sudo apt-get install -y python-pip

sudo pip install django
sudo pip install south
sudo pip install gunicorn

