#!/bin/bash

# Install Ansible
# for Ubuntu 18.04


echo -n "Installing ansible"
apt update >/dev/null 2>&1 && echo -n "." && \
apt-get install -y apt-transport-https sudo >/dev/null 2>&1 && echo -n "." && \
apt-add-repository -y 'ppa:ansible/ansible' >/dev/null 2>&1 && echo -n "." && \
apt update >/dev/null 2>&1 && echo -n "." && \
apt install -y ansible >/dev/null 2>&1 && echo -n "." && \
echo "done"

if [ ! -z "$1" ]; then
     ansible-playbook -i localhost, -c local "$1"
fi

