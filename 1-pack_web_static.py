#!/usr/bin/python3
"""The Script does the following:
    - Generates a .tgz archive from the contents of the web_static folder,
    - Uses the function do_pack,
    - Adds all files in the folder web_static to the final archive,
    - Stores all archives in the folder 'versions'
"""
from datetime import datetime
from fabric.api import local


def do_pack():
    """Generates a tgz archive from web_static folder."""
    now = datetime.utcnow()
    timestamp = now.strftime('%Y%m%d%H%M%S')
    archive_name = f"web_static_{timestamp}.tgz"
    archive_path = f"versions/{archive_name}"

    # Create versions directory if it doesn't exist
    local("mkdir -p versions")

    # Create archive
    local(f"tar -czvf {archive_path} web_static/")
    return archive_path
