===============================
Domain controller configuration
===============================

Set the IP address for the machine that is going to run the Samba Active
Directory Domain Controller (DC). The chosen IP address must satisfy three
conditions:

* The IP address must be in the same subnet range of a green network.
* The green network must be bound to a bridged interface.
* The IP address must not be used by any other machine.

Create a bridge interface for the green network
    Automatically create a bridge on green interface for the DC machine
