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

#FEC XOR encoding
def fec_xor(packet1,packet2):
    return "".join(chr(ord(a)^ord(b)) for a,b in zip(packet1,packet2))

def main():
    host = "localhost"
    port = 12345
    initial_packet = [] # initial packet
    injected_packet = [] #list after dropping some packets
    xor_fec_packet = [] #list after adding xor of packets
    seq = 0 #sequence number

    try:
        with open("text.txt", "rt") as f:
            bytes = f.read()

        #dividing the whole byte variable into smaller packets
        for pkt in packetmaker(bytes, 100):
            pkt = (str(seq)+"->"+pkt+"#"+str(datetime.datetime.now()))
            initial_packet.append(pkt)
            #print sys.getsizeof(pkt)
            seq += 1

        #user enters % loss in packet transmission
        percent = sys.argv[1] if len(sys.argv) > 1 else '0'
        if percent == "0":
            print "Injecting 0 percent loss in the transmission."
        elif percent > "0":
            print "Injecting {} percent loss in the transmission".format(percent)
        packets_tolose = calcLoss(int(percent),(seq+1))
        print "Number of packets to lose {}".format(packets_tolose)

        #dropping packets to inject loss
        injected_packet = list(initial_packet)
        for i in range(int(packets_tolose)):
            del injected_packet[i]

        try:
            #socket connections and operations
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect((host, port))
            print "Server started at {}, port {}.".format(host,port)
            print '-------------------------------------------'

            #FEC selector: can be 'triple' or 'xor'. Default is xor
            selection = sys.argv[2] if len(sys.argv) == 3 else 'xor'

            #triple redundancy FEC
            if selection == "triple":
                print "Proceeding with triple redundancy FEC"
                print '-------------------------------------------'
                for pkt in injected_packet:
                     for i in range (3):
                         s.sendto(pkt,(host,port))
                         print "sent: Packet:{}" .format(pkt)
                     time.sleep(2)
                print "All packets sent."

            #XOR FEC
            if selection == "xor":
                print "Proceeding with XOR FEC"
                print '-------------------------------------------'

                #Calculating and preparing xor fec packet
                xor_list = []
                xor_fec_packet = list (initial_packet)
                ind = 3
                n = 0
                for i in range(0, len(initial_packet), 2):
                    xor_list.append(fec_xor(initial_packet[i],initial_packet[i+1]))

                while ind < len(xor_fec_packet):
                    xor_fec_packet.insert(ind, xor_list[n])
                    ind += 4
                    n += 1

                print "\n\n xor fec packet"
                print xor_fec_packet





        except socket.error, e:
            print "Error creating socket {}".format(e)

    #safe exit
    except KeyboardInterrupt:
        print '\n\n Closing the sender socket\n'
        print '-------------------------------------------'

    s.close()

if __name__ == "__main__":
    main()
