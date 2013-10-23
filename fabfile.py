import os

from fabric.api import cd, run, require, sudo, env, local, settings, abort
from fabric import operations

from utils import db_backup

####################
# env mods
####################

env.site_path = '/usr/local/vegphilly/'
env.backup_path = '/var/vegphilly_backups/'


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
            setting_value = l[i + 1:].strip()

            # Newer versions of vagrant will wrap certain params like
            # IdentityFile in quotes, we need to strip them off
            if (setting_value[:1] + setting_value[-1]) in ('\'\'', '""'):
                setting_value = setting_value[1:-1]

            vagrant_ssh_config[setting_name] = setting_value
        except Exception:
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
    return "supervisorctl %s vegphilly_gunicorn" % cmd


def _manage(cmd):
    """ Execute 'cmd' as a python management command """
    with cd(env.site_path):
        run(_python('manage.py %s' % cmd))

####################################################################
# data management commands
####################################################################
#
# use these commands to run unit tests or linting on source


def syncdb():
    """ run syncdb and all migrations

    Set dev_data to True to load in the development data
    """
    require('site_path')
    _manage('syncdb --noinput')
    _manage('migrate --noinput')


def rebuild_fixture():
    _manage('dumpdata auth contenttypes vegancity > '
            'vegancity/fixtures/public_data.json')

####################################################################
# testing commands
####################################################################
#
# use these commands to run unit tests or linting on source


def test_all(test_filter=""):
    """ run application unit and integration tests """
    require('site_path')
    _manage('test %s' % test_filter)


def test(test_filter=""):
    """ run application unit tests """
    require('site_path')
    _manage('test --exclude-integration-tests %s' % test_filter)


def check():
    """ Run flake8 (pep8 + pyflakes) """
    require('site_path')

    with settings(warn_only=True):
        with cd(env.site_path):
            flake8 = run('flake8 --exclude=migrations,'
                         '*.md,*.txt,*.pyc,Vagrantfile,'
                         'COPYING,urls.py *')

    if flake8.failed:
        abort('Code linting failed')

####################################################################
# appserver daemon commands
####################################################################
#
# by default, the build tools will automatically start a daemon that
# runs an appserver on your host machine's port 8000. This is great
# for designers and content editors so they can just run 'vagrant up'
# and get to work. The following commands allow you to control that
# process without logging into the machine.

# see terminal/shell commands for command that give you more fine-
# grained control, like running debuggers in your current terminal


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


####################################################################
# terminal shell/debugger commands
####################################################################
#

# to run a 'debugserver' which will kill the daemon and run a server
# in your current terminal. This is useful for using pdb to debug
# python code.
#


def runserver():
    """
    run a development server in the current terminal

    kills the daemon appserver first to avoid port conflicts.
    """
    _manage("runserver 0.0.0.0:8000")


def django_shell():
    """ Opens a python shell that connects to the django application """
    operations.open_shell(command=_manage("shell"))


def dbshell():
    """ Opens a psql shell that connects to the application database """
    operations.open_shell(command=_manage("dbshell"))


def venv_shell():
    """ Opens a bash shell on the vm from the project root"""
    operations.open_shell(command="cd %s" % env.site_path)


####################################################################
# server maintenance commands
####################################################################
#
# these commands are used to maintain production servers. you will
# be responsible for providing host and credential information, but
# they make it easier to peform certain tasks.

def backup_db(copy_to_local=False):
    """
    backup the db on a remote host

    requires privilege to su to postgres user.

    should be run like: 'fab -H www.foo.com -u username backup_db'
    """
    require('backup_path')

    filename = db_backup.generate_filename()
    run(db_backup.generate_pg_dump_command(filename))
    run(db_backup.generate_mv_command(filename))

    if copy_to_local:
        operations.get(os.path.join(env.backup_path, filename),
                       os.path.join(".", filename))
