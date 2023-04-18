# Product Description

DIONA is a deep learning-based system for detecting and responding to
network intrusions on IoT devices. It analyzes device behavior and
network traffic in real-time to identify and respond to potential
threats, improving the overall security of IoT networks. The system has
been rigorously tested for performance and accuracy.

## Problem

IoT networks are vulnerable to attacks due to limited security features
and widespread deployment. Effective solutions for securing these
networks in real-time are lacking.

## Solution

DIONA uses deep learning to analyze device behavior and network traffic
in real-time, identifying and responding to potential threats, thereby
improving the overall security of IoT networks.[1]

# High Level System View

The Figure <a href="#fig:fig-1" data-reference-type="ref"
data-reference="fig:fig-1">1</a> represents the context flow diagram of
DIONA, which defines the boundaries and interactions between the DIONA
and External elements.

<figure id="fig:fig-1">
<img src="Documentation/DIONA-context_diagram_2_.png" style="width:70.0%" />
<figcaption>The Context Flow Diagram</figcaption>
</figure>

  
DIONA has four external elements that are crucial for its functionality:
IoT Network Interface, Shared Distributed Database, IoT Device Manager,
and Security Analyst/System Administrator.

1.  The IoT Network Interface is responsible for allowing the system to
    analyze network traffic from the IoT devices.

2.  The Shared Distributed Database stores logs and actions generated by
    DIONA and the IoT devices.

3.  The IoT Device Manager controls the IoT devices, asserts actions
    generated by DIONA and receives commands from DIONA as network
    response. It also pushes its activity to the system.

4.  The Security Analyst/System Administrator monitors the system
    activity and confirms correct actions taken by DIONA in case of
    intrusions or alerts.

Note that the System Administrator is not a requirement for DIONA as the
system is fully autonomous. However, it is included for the purpose of
monitoring and reinforcement learning.

# System Design

The Figure <a href="#fig:fig-2" data-reference-type="ref"
data-reference="fig:fig-2">2</a> represents the Deployment UML diagram
of DIONA, which defines the nodes,components, artifacts and protocols
used by the System.

<figure id="fig:fig-2">
<img src="images/Untitled Diagram.png" style="width:90.0%" />
<figcaption>The Context Flow Diagram</figcaption>
</figure>

## Nodes

1.  GPU capable DL engine server: A server that is equipped with a GPU
    and is used to run the deep learning models of the DIONA system

2.  IDS server: A server that runs the intrusion detection system (IDS)
    to detect and prevent network attacks

3.  Distributed database server: A server that runs a distributed
    database system to store logs and actions generated by the DIONA
    system and the IoT devices

4.  Network flow management server: A server that manages the network
    flow of the IoT devices and the DIONA system

5.  UI server: A server that runs the user interface of the DIONA system

6.  IoT Hub: A server that acts as a hub for IoT devices to connect to
    the DIONA system

## Components

1.  DL Engines Django API service: A service that provides an API for
    the deep learning models of the DIONA system

2.  Grafana UI service: A service that provides a web-based user
    interface for monitoring and alerting

3.  InfluxDB service: A service that runs the InfluxDB time-series
    database

4.  Node-red service: A service that manages the flow of messages
    between the IoT devices and the DIONA system

5.  Suricata service: A service that runs the Suricata network security
    monitoring tool

6.  Telegraf service: A service that collects and reports metrics

7.  Docker engine: A service that runs the Docker containerization
    technology

8.  MQTT-broker service: A service that runs the MQTT message broker

## Artifacts

Each service within the DIONA system has its own set of configuration
files, installation scripts, and runtime scripts. These artifacts are
essential for the proper functioning of the system.

## Dependencies

The DIONA system relies on a single external dependency, which is a
company-provided IoT hub service. However, in the event that this
service is not available, the DIONA system has a built-in IoT hub
service as a fallback.

## Interfaces

1.  IoT devices Network Interface: The interface through which IoT
    devices connect to the DIONA system

2.  Local network Network Interface: The interface through which the
    DIONA system connects to the local network

## Deployment specifications

Total of 5 servers:

1.  3 servers with the following specifications: (2GB Memory, 2 CPUs,
    16GB Disk) for network flow management , grafana and IDS

2.  1 \* (2GB Memory, 2 CPUs, 64 GB Disk) for database server

3.  1 \* (4GB Memory, 2 CPUs, 16GB Disk, 16 GPU cores ) for DL engines

# Alternative Design Options

When addressing the concern of IoT Network Security, the DIONA system
utilizes a design approach that employs a DL/ML engine to analyze IoT
devices and combine the insights with rules established for network
traffic, resulting in a final decision. The system is designed to
provide an IoT Network Security solution and is ready to be deployed on
a Kubernetes cluster in the cloud. The use of Kubernetes allows for
efficient scaling and management of the system’s resources, making it a
suitable option for large-scale deployment. Additionally, it is
important to note that the effectiveness of the solution is highly
dependent on the accuracy of the deep learning models used and the
quality of the data used to train those models. [2]

[1] It is worth mentioning that the effectiveness of the solution is
highly dependent on the accuracy of the deep learning models used and
the quality of the data used to train those models.

[2] All the related configuration files are ready and are on the gitlab
repo and the cluster is already up and running.
