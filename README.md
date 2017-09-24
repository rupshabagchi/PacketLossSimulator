## To run:

```
$ python receiver.py
$ python sender.py <loss_injection> <fec_process>

loss_injection : 0% to 100%, 0% by default
fec_process: xor or triple, xor by default

```

#### Example usage:
```
$ python receiver.py                #on one terminal instance
$ python sender.py 20 triple        #on another terminal instance
```

## Details

#### sender.py

This file consists of four functions:
* packetmaker: divides the entire message into 100 byte sized chunks
* calcLoss: calculates how many packets should not be sent, based on the value entered by user
* fec_xor: returns the XOR of two 100 byte sized chunks
* main: includes the processing and socket operations

The program starts with reading the data from a file named 'text.txt' included in the zip file. The read bytes are stored into a list called 'initial_packet', after adding the header (sequence number) and trailer (timestamp), and then being divided into 100 byte chunks.

While running the sender program, the user enters a desired percentage of packet loss and the required FEC method. To inject loss in the transmission, the first n packets are dropped, where n is the number of packets based on the percentage entered by the user. The 'calcLoss' function considers the ceiling value of the decimal obtained while calculating the number of packets from the percentage.  
In each FEC method, the remaining packets are sent to the receiver.

#### receiver.py

This program receives packets from the sender and breaks the received packet into three parts namely, sequence number, actual message and timestamp. It checks for duplicate sequence numbers and rejects re-transmitted packets. It also detects the Xor packets and decrypts the message using the 'fec_xor' function.


### Testing:

The program was tested in the following manner.

* From the sender's end, consecutive packets were dropped and checked if they could be recovered at the receiver's end.
* Random packets were dropped to see if they could be recovered from at the receiver's end. The randomization was done manually.


### Answers to asked questions:

Q. How does	increasing loss rate affect	the	success rate of decoding?

On a general level, higher loss in packets results in a lower the success rate of decoding. The way the transmission loss happens also seems to play a role in the rate of decoding. If a few consecutive packets are lost, then neither of the forward error correction methods prove useful in decoding the lost packets.

Q. What was the overhead, i.e., how many additional bytes you needed to send	to get a certain number of bytes	successfully decoded?

At the moment, I am sending 67 bytes of overhead in a 100 byte packet. The first 40 bytes are the header consisting of the sequence number, and identification bytes marking the end of header. The trailer consists of identification bytes marking the end of message, and timestamp. The overhead size was determined in the following method:

```
import sys, datetime
sys.getsizeof(str(seq)+"->"+"#"+str(datetime.datetime.now()))
```

The timestamp was added to calculate the delay in receiving the packet from the sender. However, in this case it may not be necessary to have the timestamp, since the sequence number alone can be used to decode the message. So only 40 bytes should be enough to successfully decode the actual message on the receiver's side in this case.
