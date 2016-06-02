#!/usr/bin/env python
from jinja2 import Template, Environment, FileSystemLoader
from subprocess import call
from os import listdir, remove, environ
from time import time, sleep
import urllib
import psutil

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
stop = 5

# Rancher API credentials
environ['RANCHER_URL'] = 'http://52.53.239.197:8080/v1/projects/1a5'
environ['RANCHER_ACCESS_KEY'] = '20B8F8646AF81E867021'
environ['RANCHER_SECRET_KEY'] = 'oroS2frKbbomFoK3WCg9XMfUcPwhHrvjB9mBDhyA'

app_host = '127.0.0.1'
result_file = 'result.csv'

# Template environment
env = Environment(
  loader=FileSystemLoader('templates'),
  trim_blocks=True)

samples=[]
for id in range(start, stop + 1):
  app_port = 80 + id - 1

  for filename in listdir('templates'):
    if filename.endswith('.j2'):
      with open(filename[:-3], 'w') as f:
        template = env.get_template(filename)
        f.write(template.render(host_port=app_port))

  # sample start time
  start=time()
  
  # Wait for containers to become active
  call(['rancher-compose', '--project-name', 'reaction-{0}'.format(id), 'up', '-d'])
  active_time = time() - start

  print 'Waiting for app to accept HTTP requests'
  while True:
    try:
      urllib.urlopen('http://{0}:{1}'.format(app_host, app_port))
      break
    except:
      sleep(.5)
  up_time = time() - start

  print 'Sampling host cpu/memory'
  cpu_percent = psutil.cpu_percent(interval=1)
  vmem_percent = psutil.virtual_memory().percent
  smem_percent = psutil.swap_memory().percent

  with open(result_file, 'a') as f:
    samples.append((id, active_time, up_time, cpu_percent, vmem_percent, smem_percent))
    f.write('{0},{1},{2},{3},{4},{5}\n'.format(id, active_time, up_time, cpu_percent, vmem_percent, smem_percent))

for sample in samples:
  print sample
