#!/usr/bin/env python
from jinja2 import Template, Environment, FileSystemLoader
from subprocess import Popen
from os import listdir, remove, environ
import time

# Kernel configuration.
#
# $ sysctl -a | grep fs.inotify
# fs.inotify.max_queued_events = 16384
# fs.inotify.max_user_instances = 128
# fs.inotify.max_user_watches = 8192
#
# Put this in a privileged container and run it on host_type='app':
#
# echo fs.inotify.max_user_instances=512 | sudo tee -a /etc/sysctl.conf
# echo fs.inotify.max_user_watches=524298 | sudo tee -a /etc/sysctl.conf
# sudo sysctl -p

# configuration parameters
start = 74
stop = 125
maxprocs = 3

# Rancher API credentials
environ['RANCHER_URL'] = 'http://130.211.199.188:8080/v1/projects/1a5'
environ['RANCHER_ACCESS_KEY'] = 'C2F34238E877F768AFBC'
environ['RANCHER_SECRET_KEY'] = 'KC6A2ymkRogigqRvAADN69nE1x9TNCT7ZABckDKB'

# Template environment
env = Environment(
  loader=FileSystemLoader('templates'),
  trim_blocks=True)

# scheduling frequency step function
def delay(id):
  if   id < 50:  return 20
  elif id < 100: return 25
  elif id < 200: return 30
  else:          return 35

for id in range(start, stop + 1):
  procs = []
  for filename in listdir('templates'):
    if filename.endswith('.j2'):
      with open(filename[:-3], 'w') as f:
        template = env.get_template(filename)
        f.write(template.render(host_port=80+id))
  procs.append(Popen(['rancher-compose', '--project-name', 'reaction-{0}'.format(id), 'up']))
  if len(procs) > maxprocs:
    procs.pop().kill()
  time.sleep(delay(id))
  remove('docker-compose.yml')
  remove('rancher-compose.yml')
