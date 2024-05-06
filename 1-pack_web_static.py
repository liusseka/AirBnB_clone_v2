#!/usr/bin/python3
"""
The Script does the following:
 - Generates a .tgz archive from the contents of the web_static folder,
 - Uses using the function do_pack,
 - Adds all files in the folder web_static to the final archive,
 - Stores all archives in the folder versions
"""

from fabric.api import local
import time

def do_pack():
    """Archives the web_static folder into a .tgz file"""
    try:
        local("mkdir -p versions")
        timestamp = time.strftime("%Y%m%d%H%M%S")
        local("tar -cvzf versions/web_static_{timestamp}.tgz web_static/")
        return ("versions/web_static_{timestamp}.tgz")
    except:
        return None
