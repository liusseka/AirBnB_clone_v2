#!/usr/bin/python3
"""Create and distributes an archive to web servers"""
import os.path
from datetime import datetime
from fabric.api import local, env, put, run
from os.path import exists, isdir
env.hosts = ['100.25.109.49', '54.209.222.176']
env.users = 'ubuntu'


# def do_pack():
#     """Generates a tgz archive from web_static folder."""
#     now = datetime.utcnow()
#     timestamp = now.strftime('%Y%m%d%H%M%S')

#     # Create versions directory if it doesn't exist
#     local("mkdir -p versions")

#     # Archive Files
#     archive_name = f"web_static_{timestamp}.tgz"
#     archive_path = os.path.join("versions", archive_name)

#     # Create archive
#     gzip_file = local(f"tar -czvf {archive_path} web_static/")

#     if gzip_file.succeeded:
#         return archived_path
#     else:
#         return None

def do_pack():
    """generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None

def do_deploy(archive_path):
    """distributes an archive to the web servers"""
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

# def do_deploy(archive_path):
#     """
#         Uploads the archive to the web servers.
#     """
#     if os.path.exists(archive_path):
#         archived_file = os.path.basename(archive_path)
#         newest_version = f"/data/web_static/releases/{archived_file[:-4]}"
#         archived_file = f"/tmp/{archived_file}"
#         put(archive_path, "/tmp/")
#         run(f"sudo mkdir -p {newest_version}")
#         run(f"sudo tar -xzf {archived_file} -C {newest_version}/")
#         run(f"sudo rm {archived_file}")
#         run(f"sudo mv {newest_version}/web_static/* {newest_version}")
#         run(f"sudo rm -rf {newest_version}/web_static")
#         run("sudo rm -rf /data/web_static/current")
#         run(f"sudo ln -s {newest_version} /data/web_static/current")

#         print("New version deployed!")
#         return True
#     else:
#         return False


# def deploy():
#     """Create and distributes an archive to web servers"""
#     try:
#         path = do_pack()
#         return do_deploy(path)
#     except:
#         return False
def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)