#!/bin/bash

cd /etc/postgresql/9.1/main/
cp -v /usr/local/vegphilly/utils/dev_env/pg_hba_TEMPLATE.conf ./pg_hba.conf
chown postgres:postgres pg_hba.conf
chmod 640 pg_hba.conf
sudo service postgresql restart
