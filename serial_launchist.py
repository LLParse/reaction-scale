#!/usr/bin/env python
from jinja2 import Template, Environment, FileSystemLoader
from subprocess import Popen
from os import listdir, remove, environ
import time

scale = 25
sleep = 20

env = Environment(
  loader=FileSystemLoader('templates'),
  trim_blocks=True)

# set API credentials
environ['RANCHER_URL'] = 'http://130.211.205.37:8080/v1/projects/1a42'
environ['RANCHER_ACCESS_KEY'] = '6FC9190F002500B49CD5'
environ['RANCHER_SECRET_KEY'] = 'dn7xjK31nAyXk3Ecdh3h8p8rTSpf3zJfoCtXqRTJ'

for id in range(0, scale):
  # Render templates
  for filename in listdir('templates'):
    if filename.endswith('.j2'):
      with open(filename[:-3], 'w') as f:
        template = env.get_template(filename)
        f.write(template.render(
          host_port=80+id))
  p = Popen(['rancher-compose', '--project-name', 'reaction-{0}'.format(id), 'up'])
  # sleep for N seconds
  time.sleep(sleep)
  p.kill()
  # TODO detect when this app is stabilized
  remove('docker-compose.yml')
  remove('rancher-compose.yml')
