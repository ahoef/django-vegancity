#!/bin/bash
###############################
## CREATE APP/DB USER
###############################

if id -u vegphilly >/dev/null 2>&1; then
    echo "'vegphilly' user exists...SKIPPING"
else
    echo "creating 'vegphilly' user"
    adduser --quiet --system --no-create-home --disabled-login --disabled-password vegphilly
fi
