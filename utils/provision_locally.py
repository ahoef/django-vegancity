#!/usr/bin/env python

import os
import sys

REQUIRED_PACKAGES = ["python-software-properties", "ansible"]


def install_dependencies():
    for package in REQUIRED_PACKAGES:
        command_template = "dpkg -l | grep 'ii  %s '"
        return_code = os.system(command_template % package)

        if return_code != 0:
            os.system("apt-get update")
            os.system("apt-get install -y python-software-properties")
            os.system("apt-add-repository -y ppa:rquillo/ansible")
            # TODO: this shouldn't really go here, it should
            # go in the ansible config
            os.system("apt-add-repository -y ppa:ubuntugis/ppa")
            os.system("apt-get update")
            os.system("apt-get install -y ansible")
            break


def run_ansible(user, path, project_dir, app_user):
    os.system("echo [dev_servers] > /etc/ansible/hosts")
    os.system("echo localhost >> /etc/ansible/hosts")

    os.system('ansible-playbook %s '
              '--connection=local --user=%s --sudo '
              '--extra-vars "project_dir=%s '
              'app_user=%s db_user=%s db_password=%s"'
              % (path, user, project_dir, app_user, app_user, app_user))

if __name__ == '__main__':
    install_dependencies()
    run_ansible(*sys.argv[1:])
