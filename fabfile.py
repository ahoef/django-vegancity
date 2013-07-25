from fabric.api import cd, run, require, sudo, env, local

import os

####################
# env mods
####################

env.site_path = '/var/projects/vegphilly'

def vagrant():
    """ Configure fabric to use vagrant as a host.

    Use the current vagrant directory to gather ssh-config settings
    for the vagrant VM. Write these settings to the fabric env.

    This should prefix any commands to be run in this context.

    EX:
    fab vagrant <command_name>
    """
    vagrant_ssh_config = {}
    for l in local('vagrant ssh-config', capture=True).split('\n'):
        try:
            l = l.strip()
            i = l.index(' ')

            setting_name = l[:i].strip()
            setting_value = l[i+1:].strip()

            # Newer versions of vagrant will wrap certain params like
            # IdentityFile in quotes, we need to strip them off
            if (setting_value[:1] + setting_value[-1]) in ('\'\'', '""'):
                setting_value = setting_value[1:-1]

            vagrant_ssh_config[setting_name] = setting_value
        except Exception, e:
            pass

    env.key_filename = vagrant_ssh_config['IdentityFile']
    env.user = vagrant_ssh_config['User']
    env.hosts = ['localhost:%s' % vagrant_ssh_config['Port']]

####################
# utility commands
####################

def _python(cmd):
    """ build a command string for python """
    return 'python %s' % cmd

def _supervisor_runserver(cmd):
    return "supervisorctl %s vegphilly-runserver" % cmd

def _manage(cmd):
    """ Execute 'cmd' as a python management command """
    with cd(env.site_path):
        run(_python('manage.py %s' % cmd))

####################
# runnable commands
####################

def syncdb():
    """ run syncdb and all migrations

    Set dev_data to True to load in the development data
    """
    require('site_path')
    _manage('syncdb --noinput')
    _manage('migrate --noinput')

def schemamigration(app_name, flag=' --auto'):
    """ create a south schemamigration """
    require('site_path')

    _manage('schemamigration %s %s' % (app_name, flag))

def test(test_filter="vegancity"):
    """ run application tests """
    require('site_path')

    _manage('test %s' % test_filter)


def restart_app():
    """ restart the development webserver """
    sudo(_supervisor_runserver("restart"))

def start_app():
    """ start the development webserver """
    sudo(_supervisor_runserver("start"))

def stop_app():
    """ stop the development webserver """
    sudo(_supervisor_runserver("stop"))

def app_status():
    """ view the status of the webserver process """
    sudo(_supervisor_runserver("status"))

def watch_log():
    """ view the development webserver console in realtime """
    sudo("tail -f /var/log/vegphilly/log.log")
