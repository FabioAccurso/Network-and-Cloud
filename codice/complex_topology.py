#!/usr/bin/python
from mininet.log import setLogLevel, info
from mininet.net import Mininet, CLI
from mininet.node import RemoteController
from mininet.link import TCLink

class Environment(object):
    def __init__(self): 
        self.net = Mininet(link=TCLink, controller=RemoteController)
        try: 
            info("*** Starting controller\n")
            self.net.addController('C1', controller=RemoteController, port=6633)
            
            info("*** Adding hosts\n")
            # Host legittimi
            self.h1 = self.net.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1')
            self.h2 = self.net.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.0.2')
            self.h3 = self.net.addHost('h3', mac='00:00:00:00:00:03', ip='10.0.0.3') # Server
            self.h4 = self.net.addHost('h4', mac='00:00:00:00:00:04', ip='10.0.0.4')
            self.h5 = self.net.addHost('h5', mac='00:00:00:00:00:05', ip='10.0.0.5')
            self.h6 = self.net.addHost('h6', mac='00:00:00:00:00:06', ip='10.0.0.6')
            
            # Host attaccanti distribuiti
            self.attacker1 = self.net.addHost('attacker1', mac='00:00:00:00:00:11', ip='10.0.0.11')
            self.attacker2 = self.net.addHost('attacker2', mac='00:00:00:00:00:12', ip='10.0.0.12')
            self.attacker3 = self.net.addHost('attacker3', mac='00:00:00:00:00:13', ip='10.0.0.13')
            
            info("*** Adding switches\n")
            self.s1 = self.net.addSwitch('s1')
            self.s2 = self.net.addSwitch('s2')
            self.s3 = self.net.addSwitch('s3')
            self.s4 = self.net.addSwitch('s4')
            self.s5 = self.net.addSwitch('s5')
            self.s6 = self.net.addSwitch('s6')
            self.s7 = self.net.addSwitch('s7')
            self.s8 = self.net.addSwitch('s8')
            self.s9 = self.net.addSwitch('s9')
            self.s10 = self.net.addSwitch('s10')
            
            info("*** Adding links\n")
            
            # Collegamenti host - switch (Access link a 100 Mbps)
            # Ramo inferiore
            self.net.addLink(self.attacker1, self.s2, bw=100, delay='2ms')
            self.net.addLink(self.h1, self.s5, bw=100, delay='2ms')
            self.net.addLink(self.h2, self.s8, bw=100, delay='2ms')
            
            # Ramo centrale
            self.net.addLink(self.h4, self.s3, bw=100, delay='2ms')
            self.net.addLink(self.attacker2, self.s6, bw=100, delay='2ms')
            self.net.addLink(self.h3, self.s9, bw=100, delay='2ms') # Server
            
            # Ramo superiore
            self.net.addLink(self.h5, self.s4, bw=100, delay='2ms')
            self.net.addLink(self.attacker3, self.s7, bw=100, delay='2ms')
            self.net.addLink(self.h6, self.s10, bw=100, delay='2ms')

            # Collegamenti tra switch (Core link a 150 Mbps)
            # Root -> Livello 1
            self.net.addLink(self.s1, self.s2, bw=150, delay='25ms')
            self.net.addLink(self.s1, self.s3, bw=150, delay='25ms')
            self.net.addLink(self.s1, self.s4, bw=150, delay='25ms')

            # Livello 1 -> Livello 2
            self.net.addLink(self.s2, self.s5, bw=150, delay='25ms')
            self.net.addLink(self.s3, self.s6, bw=150, delay='25ms')
            self.net.addLink(self.s4, self.s7, bw=150, delay='25ms')

            # Livello 2 -> Livello 3
            self.net.addLink(self.s5, self.s8, bw=150, delay='25ms')
            self.net.addLink(self.s6, self.s9, bw=150, delay='25ms')
            self.net.addLink(self.s7, self.s10, bw=150, delay='25ms')
            
            info("*** Starting network\n")
            self.net.build()
            self.net.start()
            self.net.pingAll()
            
            # Avvio del server iperf su h3 (vittima)
            self.h3.cmd('iperf -s -u &')
            
            info("*** Network topology summary:\n")
            info("*** Legitimate hosts: h1, h2, h3(server), h4, h5, h6\n")
            info("*** Attackers: attacker1(s2), attacker2(s6), attacker3(s7)\n")
            
        except Exception as e:
            info(f"!!! Errore durante l'inizializzazione della rete: {e}\n")
            self.net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    info('*** Avvio dell\'ambiente complesso\n')
    env = Environment()
    info("*** Avvio CLI\n")
    CLI(env.net)
    env.net.stop()
