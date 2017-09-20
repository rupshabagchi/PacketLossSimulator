import socket, datetime, sys

#command-line argument for user defined packet loss injection
def getarg():
        arg = sys.argv[1] if len(sys.argv) > 1 else '.'
        if arg == "0":
            print "Injecting 0 percent loss in the transmission."
        elif arg > "0":
            print "Injecting {} percent loss in the transmission".format(arg)
def calcLoss():
        
def main():

    host="localhost"
    port=12345
    received_packet = 0
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind((host,port))
        print "Client started at {} port: {}.".format(host,port)
    except socket.error, e:
        print "Error binding socket {}".format(e)
        s.close()

    while True:
        try:
            # Set timeout of one minute for socket operations
            # s.settimeout(60)
            packet,address = s.recvfrom(800)
            message_decoded = packet.split(',')
            time_sent = datetime.datetime.strptime(message_decoded[1],"%Y-%m-%d %H:%M:%S.%f")
            print "packet {}, sent at Time: {}".format(message_decoded[0],time_sent)
            received_packet+=1
            #Time delay in receiving packet transmission
            delay = datetime.datetime.now()-time_sent
            print "reception delay in seconds= {}".format(delay.total_seconds())

        #safe exit
        except KeyboardInterrupt:
            print '\n\n\n Closing the socket'
            s.close()


if __name__ == "__main__":
    main()
