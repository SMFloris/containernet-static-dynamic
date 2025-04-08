# Containernet

## Topology

![Topology](./resources/topology.png)

## Requirements

1. OvS (Open vSwitch) installed

[https://docs.openvswitch.org/en/latest/intro/install/](https://docs.openvswitch.org/en/latest/intro/install/)

2. Docker installed

3. Make sure you have net.ipv4.ip_forward enabled:

```
sysctl -w net.ipv4.ip_forward=1
```

## How to run

```bash
sudo docker run --name containernet -it --rm --privileged --pid='host' -v ./scripts:/containernet/scripts -v /var/run/docker.sock:/var/run/docker.sock containernet/containernet python scripts/routing_static.py
```

![Setup](./resources/ss1.png)

![r1-ifconfig](./resources/ss2.png)
