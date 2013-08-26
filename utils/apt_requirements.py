#!/usr/bin/env python

import os

packages = [
    "postgresql",
    "python-dev",
    "postgresql-server-dev-9.1",
    "postgis",
    "postgresql-9.1-postgis",
    "python-pip",
    "supervisor",
    "nginx",
]

not_installed = []

for package in packages:
    command_template = "dpkg -l | grep 'ii  %s '"
    return_code = os.system(command_template % package)

    if return_code != 0:
        # if any of the packages aren't installed,
        # install them all and break the loop
        install_template = "apt-get install -y %s"
        install_string = install_template % " ".join(packages)

        os.system("apt-get update")
        os.system(install_string)
        break
