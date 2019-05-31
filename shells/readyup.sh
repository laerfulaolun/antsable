#!/usr/bin/env bash

# ssh jumphost

set -xe
cd $(dirname $0)

if [ ! "$(which apt)" ]; then echo "*** apt not found. minimum requirement not met ***"; exit 1; fi

antsable="../"
playbooks="../playbooks"

# Put running playbooks here
/bin/bash $antsable/ansible.sh $playbooks/ssh.yml
/bin/bash $antsable/ansible.sh $playbooks/sshfs.yml
/bin/bash $antsable/ansible.sh $playbooks/ping.yml
/bin/bash $antsable/ansible.sh $playbooks/ubuntu-readyup-18.x.yml

