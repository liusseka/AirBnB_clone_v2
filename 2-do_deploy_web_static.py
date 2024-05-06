#!/usr/bin/env python3
"""A Script that:
 - a Fabric script that distributes an archive to web servers
 - The archive based on the file 1-pack_web_static.py)
"""

import os
from datetime import datetime
from fabric.api import *

env.user = "ubuntu"
env.hosts = ["100.25.109.49", "54.209.222.176"]

def do_deploy(archive_path):
    """
        Distributes the archive to the web servers.
    """
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run(f"sudo mkdir -p {newest_version}")
        run(f"sudo tar -xzf {archived_file} -C {newest_version}/")
        run(f"sudo rm {archived_file}")
        run(f"sudo mv {newest_version}/web_static/* {newest_version}")
        run(f"sudo rm -rf {newest_version}/web_static")
        run("sudo rm -rf /data/web_static/current")
        run(f"sudo ln -s {newest_version} /data/web_static/current")

        print("New version deployed!")
        return True

    return False