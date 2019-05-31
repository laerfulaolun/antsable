#!/usr/bin/env bash

# install python3

set -xe
cd $(dirname $0)

if [ ! $(which apt) ]; then echo "*** apt not found. minimum requirement not met ***"; exit 1; fi

antsable="../"
playbooks="../playbooks"

# Put running playbooks here
/bin/bash $antsable/ansible.sh $antsable/playbooks/human_tools.yml
/bin/bash $antsable/ansible.sh $antsable/playbooks/python3.yml

