# Containernet

You can run everything using docker. Check requirements for info.

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
# to cleanup old networks
./start.sh --clean

# to start static example
./start.sh --static

# to start dynamic example
./start.sh --dynamic

# to force start any example by cleaning old networks
./start.sh --dynamic --clean
```

## Static routing

Adding routes statically, we are able to ping h2 from h1.

![Setup](./resources/ss1.png)

![r1-ifconfig](./resources/ss2.png)

## Dynamic routing

Routing dynamically using Quagga and Rip works by using RIP on the interfaces defined by containernet.

![Dynamic](./resources/ss3.png)

You can also use vtysh in order to connect to quagga from containernet cli.

```
containernet> r1 vtysh
```

![Dynamic-Vtysh](./resources/ss4.png)
