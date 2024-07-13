#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers"""

from fabric.api import *
import os

env.hosts = ['52.201.219.250', '100.26.138.113']


def do_deploy(archive_path):
    """Archive distributor"""
    if not os.path.exists(archive_path):
        print('Archive file does not exist')
        return False

    try:
        arc_tgz = archive_path.split("/")[-1]
        arc_name = arc_tgz.split('.')[0]

        # Upload archive to the server
        put(archive_path, '/tmp/')

        # Create /data/web_static/releases/ if it doesn't exist
        run('mkdir -p /data/web_static/releases/')

        # Save folder paths in variables
        uncomp_fold = '/data/web_static/releases/{}'.format(arc_name)
        tmp_location = '/tmp/{}'.format(arc_tgz)

        # Run remote commands on the server
        run('mkdir -p {}'.format(uncomp_fold))
        run('tar -xvzf {} -C {}'.format(tmp_location, uncomp_fold))
        run('rm {}'.format(tmp_location))
        run('mv {}/web_static/* {}'.format(uncomp_fold, uncomp_fold))
        run('rm -rf {}/web_static'.format(uncomp_fold))
        run('rm -rf /data/web_static/current')
        run('ln -sf {} /data/web_static/current'.format(uncomp_fold))
        sudo('service nginx restart')
        print('New version deployed!')
        return True
    except Exception as e:
        print('Deployment failed:', str(e))
        return False
