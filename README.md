# Description

An SDN-based technique to find the optimal path for in a network with least delay and path loss. Uses mininet for simulation and OpenDayLight as SDN Controller.

# Intro

## Tested Physical Env.
- OS: Ubuntu 22.04 LTS

## Requirements
- OSCP (OpenDaylight SDN Controller Platform)
- Mininet

## OSCP
The web UI can be used to manage and visualize the network.

![oscp-screenshot](https://github.com/Abhinavxox/SMOTE-based-SDN-Simulation/assets/72064600/495c34a3-f1f2-4a44-b2a6-a24db188317e)

## Mininet
Running a custom topology connected to the OpenDayLight controller.

![image](https://github.com/Abhinavxox/SMOTE-based-SDN-Simulation/assets/72064600/01b400ac-b734-4d70-bb29-92c47f3aa32a)

### Run OSCP

Go to the bin folder.

```
./karaf-<version>/bin
```

Run the karaf file to open run OpenDayLight.

```
./karaf
```

![image](https://github.com/Abhinavxox/SMOTE-based-SDN-Simulation/assets/72064600/c1ef68f3-76a9-4a35-9006-fa394f682512)

### Run Mininet

Run this command to run the custom topology:

```
sudo mn --custom ./topo/topology.py --topo=mytopo --controller=remote,ip=127.0.0.1,port=6633 --link=tc
```

### Check connection to controller

```
sudo ovs-vsctl show
```

![Alt text](/images/odlConnection.png)


# References

 - Research Paper: https://www.tandfonline.com/doi/full/10.1080/03772063.2021.1894248
 - ODL Docs: https://docs.opendaylight.org/en/stable-potassium/
