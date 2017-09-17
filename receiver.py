import socket, datetime

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
        packet,address = s.recvfrom(800)
        message_decoded = packet.split(',')
        time_sent = datetime.datetime.strptime(message_decoded[1],"%Y-%m-%d %H:%M:%S.%f")
        print "packet {}, sent at Time: {}".format(message_decoded[0],time_sent)
        received_packet+=1
        #Time delay in receiving packet transmission
        delay = datetime.datetime.now()-time_sent
        print "reception delay in seconds= {}".format(delay.total_seconds())


if __name__ == "__main__":
    main()
