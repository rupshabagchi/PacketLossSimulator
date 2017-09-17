import SocketServer, threading, time

class Server(SocketServer.ThreadingMixIn, SocketServer.UDPServer):pass
class RequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        threadcount = threading.current_thread()
        print("{}: client: {}, sent: {}".format(threadcount.name, self.client_address, data))
        socket.sendto(data, self.client_address)


if __name__ == "__main__":
    HOST, PORT = "localhost", 12345

    server = Server((HOST, PORT), RequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print("Server started at {} port {}".format(HOST, PORT))
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        exit()
