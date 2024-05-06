#!/usr/bin/bash
# The script configures web servers for deployment with

# Update packages and install Nginx, if it does not exist
sudo apt update -y
sudo apt install -y nginx

# create web_static folder inside data folder
mkdir -p /data/web_static/

# Create folders /releases and /shared inside /web_static
mkdir -p /data/web_static/releases/ /data/web_static/shared/

# Create the folder /test inside /releases
mkdir -p /data/web_static/releases/test/

# Create a fake html file inside test
touch /data/web_static/releases/test/index.html

echo "
<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    <h2>Nginx Test</h2>
    <p>Testing My Nginx Server</p>
  </body>
</html>
" | tee /data/web_static/releases/test/index.html

# removing (if it exists) and creating a symbolic link
if [ -f "/data/web_static/current" ];
then
	rm "/data/web_static/current"
fi

ln -sf /data/web_static/releases/test/ /data/web_static/current

# Changing ownwership to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/
sudo chmod g+s /data/

# Updating the Nginx configuration file
sudo sed -i '39 i\ \tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n' /etc/nginx/sites-enabled/default

# restarting the Nginx service
sudo service nginx restart
