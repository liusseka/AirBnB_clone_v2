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
    """Creates a .tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None
