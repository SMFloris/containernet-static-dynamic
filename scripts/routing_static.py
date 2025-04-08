#!/usr/bin/python
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import info, setLogLevel
setLogLevel('info')

# use this if you want auto broadcast address
def setIpWithAutoBroadcast(node, ip, intf):
    return node.cmd('ip', 'address', 'add', ip, 'brd', '+', 'dev', intf)

net = Containernet(controller=Controller, waitConnected=True)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')
# set ip of the first intf and default route
# if you don't set these, they will get flushed by containernet when starting
h1 = net.addDocker('h1', ip="192.168.1.1/24", defaultRoute="via 192.168.1.254", dimage="ubuntu:trusty", waitConnected=True)
h2 = net.addDocker('h2', ip="192.168.2.1/24", defaultRoute="via 192.168.2.254", dimage="ubuntu:trusty", waitConnected=True)
r1 = net.addDocker('r1', ip="192.168.1.254/24", defaultRoute="via 192.168.1.1", dimage="ubuntu:trusty", waitConnected=True)
r2 = net.addDocker('r2', ip="192.168.2.254/24", defaultRoute="via 192.168.2.1", dimage="ubuntu:trusty", waitConnected=True)
r3 = net.addDocker('r3', ip="13.1.1.3/24", defaultRoute="via 13.1.1.1", dimage="ubuntu:trusty", waitConnected=True)
info('*** Creating links\n')
net.addLink(h1, r1, intfName1="h1-eth0", intfName2="r1-eth0")
net.addLink(h2, r2, intfName1="h2-eth0", intfName2="r2-eth0")
net.addLink(r1, r2, intfName1="r1-eth1", intfName2="r2-eth1")
net.addLink(r1, r3, intfName1="r1-eth2", intfName2="r3-eth0")
net.addLink(r2, r3, intfName1="r2-eth2", intfName2="r3-eth1")
info('*** Setting interface ips\n')
# alternatively, if you want auto broadcast address use:
# setIpWithAutoBroadcast(h1, "ip/prefixLen", "intfname")
h1.setIP("192.168.1.1", 24, intf="h1-eth0")
h2.setIP("192.168.2.1", 24, intf="h2-eth0")
r1.setIP("192.168.1.254", 24, intf="r1-eth0")
r1.setIP("12.1.1.1", 24, intf="r1-eth1")
r1.setIP("13.1.1.1", 24, intf="r1-eth2")
r2.setIP("192.168.2.254", 24, intf="r2-eth0")
r2.setIP("12.1.1.2", 24, intf="r2-eth1")
r2.setIP("23.1.1.2", 24, intf="r2-eth2")
r3.setIP("13.1.1.3", 24, intf="r3-eth0")
r3.setIP("23.1.1.3", 24, intf="r3-eth1")
# usually, with docker this is already enabled on host so it is not needed
# uncomment if not enabled on host
# info('*** Enabling ipv4 forward\n')
# r1.cmd("sysctl -w net.ipv4.ip_forward=1")
# r2.cmd("sysctl -w net.ipv4.ip_forward=1")
# r3.cmd("sysctl -w net.ipv4.ip_forward=1")
info('*** Adding routes\n')
r1.cmd("ip route add 192.168.2.0/24 via 12.1.1.2")
r1.cmd("ip route add 23.1.1.0/24 via 13.1.1.3")
r2.cmd("ip route add 192.168.1.0/24 via 12.1.1.1")
r2.cmd("ip route add 13.1.1.0/24 via 23.1.1.3")
r3.cmd("ip route add 192.168.1.0/24 via 13.1.1.1")
r3.cmd("ip route add 192.168.2.0/24 via 23.1.1.2")
r3.cmd("ip route add 12.1.1.0/24 via 13.1.1.1")
info('*** Starting network\n')
net.start()
info('*** Testing connectivity\n')
net.ping([h1, h2])
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()

