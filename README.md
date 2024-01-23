# Project

```
sudo mn --custom ./topo/topology.py --topo=mytopo --controller=remote,ip=127.0.0.1,port=8101
```

sudo mn --topo linear,3 --mac --controller=remote,ip=10.113.2.51,port=6633 --switch ovs,protocols=OpenFlow13
sudo mn --custom ./topo/topology.py --topo=mytopo --controller=remote,ip=127.0.0.1,port=6633 --link=tc
![Alt text](/images/initialState.png)

![Alt text](/images/odlConnection.png)
