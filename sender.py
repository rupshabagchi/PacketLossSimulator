import socket
import sys
import math
import datetime, time

#dividing a packet into 'size' sized bytes
def packetmaker(str, size):
    return (str[position:position + (size-67)] for position in range(0, len(str), (size-67)))

#calculating number of packets to drop
def calcLoss(percent,total_packets ):
        return math.ceil((percent/100.0)*total_packets)

def main():
    host="localhost"
    port=12345
    packet = [] #packet number
    new_packet = [] #list after dropping some packets
    seq = 0 #sequence number
    try:
        with open("text.txt", "rt") as f:
            bytes = f.read()

        for pkt in packetmaker(bytes, 100):
            pkt = (str(seq)+"->"+pkt+","+str(datetime.datetime.now()))
            packet.append(pkt)
            #print sys.getsizeof(pkt)
            seq+=1

        #user enters % loss in packet transmission
        percent = sys.argv[1] if len(sys.argv) > 1 else '0'
        if percent == "0":
            print "Injecting 0 percent loss in the transmission."
        elif percent > "0":
            print "Injecting {} percent loss in the transmission".format(percent)
        packets_tolose = calcLoss(int(percent),(seq+1))
        print "Number of packets to lose {}".format(packets_tolose)
        new_packet = list(packet)
        for i in range(int(packets_tolose)):
            del new_packet[i]

        try:
            #socket connections and operations
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect((host, port))
            print "Server started at {}, port {}.".format(host,port)

            for pkt in new_packet:
                s.sendto(pkt,(host,port))
                print "sent: Packet:{}" .format(pkt)
                time.sleep(2)

        except socket.error, e:
            print "Error creating socket {}".format(e)

    #safe exit
    except KeyboardInterrupt:
        print '\n\n Closing the sender socket\n'
        print '-------------------------------------------'

    s.close()

if __name__ == "__main__":
    main()
