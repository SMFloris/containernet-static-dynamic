#!/usr/bin/env bash

while [[ $# -gt 0 ]]; do
  case "$1" in
    --clean) SHOULDCLEAN="yes" ;;
    --static) ACTION="static" ;;
    --dynamic) ACTION="dynamic" ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
  shift
done

if [[ "$SHOULDCLEAN" == "yes" ]]; then
  docker ps | grep mn. | cut -d' ' -f1 | xargs -I{} docker kill {}
  docker ps -a | grep mn. | cut -d' ' -f1 | xargs -I{} docker rm {}
fi

if [[ -z "$ACTION" ]]; then
  echo "Usage: $0 --static|--dynamic [--clean]"
  exit 1
fi

if [[ "$ACTION" == "dynamic" ]]; then
  SCRIPT="scripts/routing_dynamic.py"
fi

if [[ "$ACTION" == "static" ]]; then
  SCRIPT="scripts/routing_static.py"
fi

if [[ -z "$SCRIPT" ]]; then
  echo "Script variable is not set."
  exit 1
fi

sudo docker run --name containernet -it --rm --privileged --pid='host' \
  -v ./scripts/:/containernet/scripts \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containernet/containernet python "$SCRIPT"
