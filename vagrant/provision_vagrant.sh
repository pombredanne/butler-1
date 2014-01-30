#!/bin/bash
if [ `whoami` != "root" ]
then
    echo >&2 "This script must be run as root"
    exit 1
fi

set -e

/puppet/bin/apply.sh

sed -i '/nameserver/d' /etc/resolv.conf
echo 'nameserver 192.168.50.101' >> /etc/resolv.conf

rm -f /var/akvo/butler/code
sudo -u butler ln -s /vagrant/butler/checkout /var/akvo/butler/code

if [ ! -e /var/akvo/butler/venv ]
then
    sudo -u butler virtualenv --quiet /var/akvo/butler/venv
fi

sudo -u butler /var/akvo/butler/venv/bin/pip install -e /var/akvo/butler/code/

manage='sudo -u butler /var/akvo/butler/venv/bin/python /var/akvo/butler/code/akvo/manage.py'

$manage syncdb --noinput
$manage migrate

supervisorctl restart butler
