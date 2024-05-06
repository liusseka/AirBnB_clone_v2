#!/usr/bin/python3
""" Function that cleans unnessecaru archives """
from fabric.api import *

env.hosts = ['44.210.150.159', '35.173.47.15']
env.user = "ubuntu"

def do_clean(number=0):
    """ cleans a certain number of archives """

    # define number
    number = int(number)
    if number == 0:
        number = 2
    else:
        number += 1

    # Local clean up
    local(f'cd versions ; ls -t | tail -n +{number} | xargs rm -rf')

    # Remote clean up
    path = f'/data/web_static/releases'
    run(f'cd {path} ; ls -t | tail -n +{number} | xargs rm -rf')
