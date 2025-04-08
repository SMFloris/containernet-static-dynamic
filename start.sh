#!/usr/bin/env bash

docker ps | grep mn. | cut -d' ' -f1 | xargs -I{} docker kill {}
docker ps -a | grep mn. | cut -d' ' -f1 | xargs -I{} docker rm {}
sudo docker run --name containernet -it --rm --privileged --pid='host' -v ./scripts:/containernet/scripts -v /var/run/docker.sock:/var/run/docker.sock containernet/containernet python scripts/routing_static.py
