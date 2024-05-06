# Update package list
exec { '/usr/bin/env apt -y update' }

# Install nginx package
package { 'nginx': ensure => installed }

# Create the data directory
file { '/data': ensure => directory }

# Create the web_static directory structure
file { [
  '/data/web_static/releases',
  '/data/web_static/releases/test',
  '/data/web_static/shared',
] : ensure => directory }

# Create an index.html file in the test release directory
file { '/data/web_static/releases/test/index.html':
    ensure  => present,
    content => "
<!DOCTYPE html>
<html>
  <head>
    <title> Nginx Server Test </title>
  </head>
  <body>
    <h2>Nginx Test</h2>
    <p>Testing My Nginx Server</p>
  </body>
</html>",
}

# Create a symbolic link named current that points to the test release directory
file { '/data/web_static/current': ensure => link, target => '/data/web_static/releases/test' }

# Set ownership of the data directory to ubuntu user
exec { 'chown -R ubuntu:ubuntu /data/': path => '/usr/bin:/usr/local/bin/:/bin/' }

# Create the var/www directory structure
file { [
  '/var/www',
  '/var/www/html',
  ] : ensure => directory}

# Create an index.html file in the var/www/html directory
file { '/var/www/html/index.html':
  ensure => present,
  content => "
<!DOCTYPE html>
<html>
  <head>
    <title> Nginx Server Test </title>
  </head>
  <body>
    <h2>Nginx Test</h2>
    <p>Testing My Nginx Server</p>
  </body>
</html>",
}

# Update the default nginx configuration
exec { 'nginx_conf':
  environment => ['data=\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n'],
  command => 'sed -i "39i $data" /etc/nginx/sites-enabled/default',
  path => '/usr/bin:/usr/sbin:/bin:/usr/local/bin',
}

# Ensure the nginx service is running
service { 'nginx': ensure => running }
