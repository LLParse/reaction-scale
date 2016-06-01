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
#echo fs.inotify.max_user_instances=512 | sudo tee -a /etc/sysctl.conf
#echo fs.inotify.max_user_watches=524298 | sudo tee -a /etc/sysctl.conf
#sudo sysctl -p

# configuration parameters
start = 1
stop = 1000

# Rancher API credentials
environ['RANCHER_URL'] = 'http://104.197.228.222:8080/v1/projects/1a5'
environ['RANCHER_ACCESS_KEY'] = '3A190E9E34C6B3DBA112'
environ['RANCHER_SECRET_KEY'] = 'xiBwfMf9QAsdET6ZCftdLJzLABTxbqmo4S89dcZw'

# Template environment
env = Environment(
  loader=FileSystemLoader('templates'),
  trim_blocks=True)

# scheduling step function
def delay(id):
  if   id <= 100: return 7
  elif id <= 200: return 8
  elif id <= 300: return 9
  elif id <= 400: return 10
  elif id <= 500: return 11
  elif id <= 600: return 12
  elif id <= 700: return 13
  elif id <= 800: return 14
  elif id <= 900: return 15
  else:           return 16

for id in range(start, stop + 1):
  procs = []
  for filename in listdir('templates'):
    if filename.endswith('.j2'):
      with open(filename[:-3], 'w') as f:
        template = env.get_template(filename)
        f.write(template.render(host_port=80+id-1))
  procs.append(Popen(['rancher-compose', '--project-name', 'reaction-{0}'.format(id), 'up', '-d']))
  time.sleep(delay(id))
  remove('docker-compose.yml')
  remove('rancher-compose.yml')

