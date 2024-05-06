#!/usr/bin/python3
"""Create and distributes an archive to web servers"""
import os
from datetime import datetime
from fabric.api import local, env, put, run
env.hosts = ['100.25.109.49', '54.209.222.176']


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
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract the file name from the archive path without extension
        file_name = os.path.basename(archive_path)
        base_name = file_name.split(".")[0]

        # Define the target directory path for the releases
        release_path = "/data/web_static/releases/"

        # Upload the archive to the temporary location on the server
        put(archive_path, '/tmp/')

        # Prepare the release directory
        run(f'mkdir -p {release_path}{base_name}/')

        # Extract the archive into the release directory
        run(f'tar -xzf /tmp/{file_name} -C {release_path}{base_name}/')

        # Remove the archive from the temporary location
        run(f'rm /tmp/{file_name}')

        # Move the contents from web_static subfolder to releases' base directory
        run(f'mv {release_path}{base_name}/web_static/* {release_path}{base_name}/')

        # Remove the now-empty subdirectory
        run(f'rm -rf {release_path}{base_name}/web_static')

        # Remove the current symbolic link 
        run(f'rm -rf /data/web_static/current')
        run(f'ln -s {release_path}{base_name}/ /data/web_static/current')

        # Finalizing
        print("New Version deployed")
        return True

    except FileNotFoundError:
        print(" Error: Archive Path Does Not Exist")
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    
    # Check and deployes if archive file exists
    try:
        archive_path = do_pack()
        return do_deploy(archive_path)

    # returns false otherwise
    except FileNotFoundError:
        print("No archive file found")
        return False
