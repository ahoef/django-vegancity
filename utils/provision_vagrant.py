#!/usr/bin/env python

import os

REQUIRED_PACKAGES = ["python-software-properties", "ansible"]


def install_dependencies():
    for package in REQUIRED_PACKAGES:
        command_template = "dpkg -l | grep 'ii  %s '"
        return_code = os.system(command_template % package)

        if return_code != 0:
            os.system("apt-get update")
            os.system("apt-get install -y python-software-properties")
            os.system("apt-add-repository -y ppa:rquillo/ansible")
            os.system("apt-get update")
            os.system("apt-get install -y ansible")
            break


def run_ansible():
    os.system("echo [dev_servers] > /etc/ansible/hosts")
    os.system("echo localhost >> /etc/ansible/hosts")

    os.system("ansible-playbook --connection=local --user=vagrant --sudo "
              "/usr/local/vegphilly/ansible/site.yml")

if __name__ == '__main__':
    install_dependencies()
    run_ansible()
