## To run:

$ python receiver.py  #on one terminal instance
$ python sender.py <loss_injection> <fec_process> #on another terminal instance

loss_injection : 0% to 100%, 0% by default
fec_process: xor or triple, xor by default

### Details

==========
sender.py
==========

This file consists of four functions:
* packetmaker: divides the entire message into 100 byte sized chunks
* calcLoss: calculates how many packets should not be sent, based on the value entered by user
* fec_xor: returns the XOR of two 100 byte sized chunks
* main: includes the processing and socket operations

The program starts with reading the data from a file named 'text.txt' included in the zip file. The read bytes are then stored into a list called 'initial_packet', after being divided into 100 byte chunks and adding the header (sequence number) and trailer (timestamp).

While running the sender program, the user enters a desired percentage of packet loss and the required FEC method. To inject loss in the transmission, the first n packets are dropped, where n is the number of packets based on the percentage entered by the user. In each FEC method, the remaining packets are sent to the receiver.

============
receiver.py
============

This program receives packets from the sender and breaks the packet into three parts namely, sequence number, actual message and timestamp. It checks for duplicate sequence numbers and rejects retranmitted packets. It also detects the xor packets and decrypts the message using the 'fec_xor' function.


Q. How does	increasing loss rate affect	the	success rate of decoding?
On a general level, higher loss in packets results in a lower the success rate of decoding. The 	
