#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

TOPOS = {'mytopo' : (lambda : MyTopo())}

class MyTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        h1 = self.addHost('h1', cpu=.5/4)
        h2 = self.addHost('h2', cpu=.5/4)
        h3 = self.addHost('h3', cpu=.5/4)
        h4 = self.addHost('h4', cpu=.5/4)

        # Add links with bandwidth, delay, and loss characteristics
        self.addLink(s1, s2, bw=10, delay='5ms', loss=2)
        self.addLink(s1, s3, bw=5, delay='10ms', loss=5)
        self.addLink(s2, s4, bw=8, delay='8ms', loss=1)
        self.addLink(s3, s4, bw=12, delay='3ms', loss=0)

        self.addLink(h1, s1, bw=2, delay='20ms', loss=1)
        self.addLink(h2, s2, bw=3, delay='15ms', loss=0)
        self.addLink(h3, s3, bw=4, delay='12ms', loss=2)
        self.addLink(h4, s4, bw=6, delay='7ms', loss=3)

def runMyTopo():
    topo = MyTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    
    # Test connectivity
    net.pingAll()

    # Start the CLI
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    runMyTopo()
