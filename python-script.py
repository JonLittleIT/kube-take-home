#!/usr/bin/env python

import yaml
import logging
import subprocess

# set the logger object
logger = logging.getLogger('my_logger')
logger.setLevel(logging.ERROR)

# load the .yaml file
with open('myappresource.yaml', 'r') as f:
    data = yaml.safe_load(f)

# call Helm command
try:
    subprocess.call(['helm', 'install', '--name', 'whatever', 'myappresource', '--set', 'spec.ui.color=#34577c', 'spec.ui.message=some string', 'spec.redis.enabled=true'])
except subprocess.CalledProcessError as e:
    # log an error message if the script fails
    logger.error('Failed to run Helm command: %s', e.output)

# reconcile any updates in the .yaml file
if data['spec']['redis']['enabled'] == False:
    try:
        subprocess.call(['helm', 'upgrade', '--name', 'whatever', 'myappresource', '--set', 'spec.redis.enabled=true'])
    except subprocess.CalledProcessError as e:
        # log an error message if the script fails
        logger.error('Failed to run Helm command: %s', e.output)