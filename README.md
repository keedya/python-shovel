# Shovel Server

## Overview
Shovel is an application that provides a service with a set of APIs that wraps around RackHD/Ironic’s existing APIs.  It allows users to find Baremetal the compute nodes that were dynamically discovered by RackHD. In addition, it enables the user to register/unregister the nodes with Ironic (OpenStack Bare Metal Provisioning Program).Shovel also provides poller service that monitors compute nodes and logs the errors from SEL into the Ironic Database.
A Shovel Horizon plugin is also provided to interface with the Shovel service. The plugin adds a new Panel to the admin Dashboard called rackhd that displays a table of all the Baremetal systems discovered by RackHD. It also allows the user to see the node catalog in a nice table View, Register/Unregister node in Ironic, display node SEL and enable/register a failover node.

## Demo
<a href="http://www.youtube.com/watch?feature=player_embedded&v=LluHht5ixTI" target="_blank"><img src="http://img.youtube.com/vi/LluHht5ixTI/0.jpg"
alt="Shovel" width="240" height="180" border="10" /></a>

## setup

- git clone https://github.com/keedya/python-shovel
- cd python-shovel
- pip install -r requirement.txt
- python main.py

## configuration
- Config file can be found in python-shovel/config/config.yml

## ui

- Shovel swagger is reachable via (shovel-host':'shovel port')/#
- Shovel swagger json file can be found at  ('shovel-host':'shovel port')/swagger.json

## Run in docker

- docker build -t rackhd/shovel .
- docker run -p 9005:9005

If you want to mount a different config yml you can run:
- docker run -p 9005:9005 -v ~/python-shovel/config/config.yml:/usr/src/app/config/config.yml
