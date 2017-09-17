import socket
import sys
import datetime, time

#dividing a packet into 'size' sized bytes
def packetmaker(str, size):
    return (str[position:position + (size-67)] for position in range(0, len(str), (size-67)))


def main():
    #command-line argument for user defined packet loss injection
    arg = sys.argv[1] if len(sys.argv) > 1 else '.'
    if arg == "0":
        print "Injecting 0 loss in the transmission."
    elif arg > "0":
        print "Injecting {} loss in the transmission".format(arg)

    host="localhost"
    port=12345
    packet = [] #packet number
    seq = 0 #sequence number
    bytes = "random shit i am sending just to test if i can send it more and more and more text just to see how much i can send kanye west here i come here i am this is me theres no one else on earth than rather me here i am its me and you tonight we make our dreams come true its a new world its a new start its a life with the beating of young heart"
    for pkt in packetmaker(bytes, 100):
        pkt = (str(seq)+"->"+pkt+","+str(datetime.datetime.now()))
        packet.append(pkt)
        #print sys.getsizeof(pkt)
        seq+=1
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        # Set timeout of one minute for socket operations
        s.settimeout(60)
        s.connect((host, port))
        print "Server started at {}, port {}.".format(host,port)
        for pkt in packet:
            s.sendto(pkt,(host,port))
            print "sent: Packet:{}" .format(pkt)
            time.sleep(2)
    except socket.error, e:
            print "Error creating socket {}".format(e)
            s.close()

if __name__ == "__main__":
    main()
