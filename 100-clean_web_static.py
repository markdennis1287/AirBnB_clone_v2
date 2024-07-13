#!/usr/bin/python3
"""Clean up old archives based on the specified number"""

from fabric.api import run, local, env

# Define the remote hosts
env.hosts = ['52.201.219.250', '100.26.138.113']

def do_clean(number=0):
    """Clean up old archives"""
    number = int(number)
    if number == 0:
        number = 2
    else:
        number += 1

    # Clean local archives
    local('cd versions && ls -t | tail -n +{} | xargs rm -rf'.format(number))

    # Clean remote archives
    path = '/data/web_static/releases'
    run('cd {} && ls -t | tail -n +{} | xargs rm -rf'.format(path, number))