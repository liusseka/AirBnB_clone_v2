#!/usr/bin/python3
"""Create and distributes an archive to web servers"""
import os.path
from datetime import datetime
from fabric.api import local, env, put, run
from os.path import exists, isdir
env.hosts = ['100.25.109.49', '54.209.222.176']
env.users = 'ubuntu'


def do_pack():
    """Generates a tgz archive from web_static folder."""

    try:
        # define time
        now = datetime.utcnow()
        timestamp = now.strftime('%Y%m%d%H%M%S')

        # defile file name and path
        archive_name = f"web_static_{timestamp}.tgz"
        archive_path = f"versions/{archive_name}"

        # Create versions directory if it doesn't exist
        local("mkdir -p versions")

        # Create archive
        local(f"tar -cvzf {archive_path} web_static/")
        return archive_path

    except FileNotFoundError:
        print("Error: The file does not exist.")
        return None

def do_deploy(archive_path):
    """Uploads the archive to web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)