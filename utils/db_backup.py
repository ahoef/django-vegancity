#!/usr/bin/env python
"""
tool for running postgres backups with timestamps

can be used as a script on the server for things like cron,
or a libary for building remote commands, from tools like
fabric.
"""
import datetime
import sys
import os

BACKUP_FOLDER = '/var/vegphilly_backups/'


def generate_filename():
    formatted_datestring = datetime.datetime.now()\
                                            .strftime("%Y%m%d_%I%M%p")
    return "%s.sql" % formatted_datestring


def generate_pg_dump_command(filename):
    return 'su postgres -c "pg_dump vegphilly > /tmp/%s"' % filename


def generate_mv_command(filename):
    return 'mv /tmp/%s %s' % (filename, BACKUP_FOLDER)

if __name__ == '__main__':

    if not os.path.exists(BACKUP_FOLDER):
        print "backup folder %s does not exist. EXITING." % BACKUP_FOLDER
        sys.exit(1)
    else:
        filename = generate_filename()
        os.system(generate_pg_dump_command(filename))
        os.system(generate_mv_command(filename))
