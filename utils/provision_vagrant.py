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
            break

    os.system("echo [dev_servers] > /etc/ansible/hosts")
    os.system("echo localhost >> /etc/ansible/hosts")

    os.system("ansible-playbook --connection=local --user=vagrant --sudo "
              "/usr/local/vegphilly/ansible/site.yml")

if __name__ == '__main__':
    provision_vagrant()
