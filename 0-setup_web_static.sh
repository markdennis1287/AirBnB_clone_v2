#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

apt-get -y update > /dev/null
apt-get install -y nginx apt-utils > /dev/null

# Create all necessary directories and file
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Hello World again!" > /data/web_static/releases/test/index.html

# Check if directory current exists
if [ -d "/data/web_static/current" ]
then
        sudo rm -rf /data/web_static/current
fi

# Create a symbolic link to test
ln -s /data/web_static/releases/test/ /data/web_static/current

# Change ownership to user ubuntu
chown -R ubuntu:ubuntu /data

# Configure nginx to serve content pointed to by symbolic link to hbnb_static
config_file="/etc/nginx/sites-available/default"
sed -i "38i\ \tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" $config_file

# Restart server
service nginx restart
