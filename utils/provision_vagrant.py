#!/usr/bin/env python

import os

def provision_vagrant():
    for package in ["python-software-properties", "ansible"]:
        command_template = "dpkg -l | grep 'ii  %s '"
        return_code = os.system(command_template % package)

        if return_code != 0:
            # if any of the packages aren't installed,
            # install them all and break the loop
            os.system("apt-get update")
            os.system("apt-get install -y python-software-properties")
            os.system("apt-add-repository -y ppa:rquillo/ansible")
            os.system("apt-get update")
            os.system("apt-get install -y ansible")
            os.system("echo localhost > /etc/ansible/hosts")
            break

            os.system("ansible-playbook --connection=local --user=vagrant "
                      "--sudo --extra-vars is_dev_server=True "
                      "/usr/local/vegphilly/ansible/appservers.yml")

if __name__ == '__main__':
    provision_vagrant()
