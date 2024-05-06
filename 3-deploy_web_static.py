#!/usr/bin/python3
"""Create and distributes an archive to web servers"""
import os.path
from datetime import datetime
from fabric.api import local
from fabric.operations import env, put, run
env.hosts = ['100.25.109.49', '54.209.222.176']
env.users = 'ubuntu'


def do_pack():
    """Generates a tgz archive from web_static folder."""
    now = datetime.utcnow()
    timestamp = now.strftime('%Y%m%d%H%M%S')

    # Create versions directory if it doesn't exist
    local("mkdir -p versions")

    # Archive Files
    archive_name = f"web_static_{timestamp}.tgz"
    archive_path = os.path.join("versions", archive_name)

    # Create archive
    gzip_file = local(f"tar -czvf {archive_path} web_static/")

    if gzip_file.succeeded:
        return archived_path
    else:
        return None


def do_deploy(archive_path):
    """
        Distributes the archive to the web servers.
    """
    if os.path.exists(archive_path):
        archived_file = os.path.basename(archive_path)
        newest_version = f"/data/web_static/releases/{archived_file[:-4]}"
        archived_file = f"/tmp/{archived_file}"
        put(archive_path, "/tmp/")
        run(f"sudo mkdir -p {newest_version}")
        run(f"sudo tar -xzf {archived_file} -C {newest_version}/")
        run(f"sudo rm {archived_file}")
        run(f"sudo mv {newest_version}/web_static/* {newest_version}", pty=True)
        run(f"sudo rm -rf {newest_version}/web_static", pty=True)
        run("sudo rm -rf /data/web_static/current")
        run(f"sudo ln -s {newest_version} /data/web_static/current")

        print("New version deployed!")
        return True
    else:
        return False


def deploy():
    """Create and distributes an archive to web servers"""
    try:
        path = do_pack()
        return do_deploy(path)
    except:
        return False