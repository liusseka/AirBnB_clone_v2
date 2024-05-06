#!/usr/bin/python3
"""
The Script does the following:
 - Generates a .tgz archive from the contents of the web_static folder,
 - Uses using the function do_pack,
 - Adds all files in the folder web_static to the final archive,
 - Stores all archives in the folder versions
"""

from datetime import datetime
from fabric.api import env, local, mkdir, run

def do_pack():
  """Generates a .tgz archive of web_static contents and returns its path."""

  now = datetime.utcnow()
  timestamp = now.strftime('%Y%m%d%H%M%S')

  archive_name = f"web_static_{timestamp}.tgz"
  archive_path = f"versions/{archive_name}"

  try:
    run("mkdir -p versions")
  except Exception as e:
    print(f"Error creating versions directory: {e}")
    return None

  with local():
    try:
      local(f"tar -czvf {archive_path} web_static/*")
      return archive_path
    except Exception as e:
      print(f"Error creating archive: {e}")
      return None
