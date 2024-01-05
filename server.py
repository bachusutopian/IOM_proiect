import threading
import socket
import argparse
import os


class Server(threading.Thread):

    def __init__(self, host, port):

        super().__init__()
        self.connections = []  # empty list
        self.host = host
        self.port = port

    def run(self):
        # multithreading -> allowing multiple pieces of code to run concurrently
        # socket = IP + port number (an IP address has a host, a host can be multiple IP addresses)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))  # bind method

        sock.listen(1)
        print("Listening at", sock.getsockname())

        # we create an entire new socket to alert when the a client connects

        sc, sockname = sock.accept()
        print(f"Acceptam conexiunea din partea {
              sc.getpeername()} to {sc.getsockname()}")

        # new thread
        server_socket = ServerSocket(sc, sockname, self)

        # turn on the new thread
        server_socket.start()

        # adding the thread to the connection
        self.connections.append(server_socket)
        print("Disponibil sa primesc mesaje de la ", sc.getpeername())

    def broadcast(self, message, source):
        for connection in self.connections:

            # notificam toti oamenii conectati ca se va conecta cineva nou
            if connection.sockname != source:
                connection.send(message)

    def remove_connection(self, connection):

        self.connections.remove(connection)


class ServerSocket(threading.Thread):

    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server

    def run(self):
        # primim data de la oamenii conectati si notifica pe ceilalti care sunt
        # conectati, de exemplu, cand paraseste chat-ul

        while True:
            message = self.sc.recv(1024).decode('ascii')

            if message:
                print(f"{self.sockname}says{message}")
                self.server.broadcast(message, self.sockname)

            else:
                print(f"{self.sockname} has closed the connection")
                self.sc.close()
                server.remove_connection(self)
                return

    def send(self, message):
        self.sc.sendall(message.encode('ascii'))

    def exit(server):  # inciderea serverului

        while True:
            inpt = input("")
            if inpt == "q":
                print("Deconectarea tuturor...")
                for connection in server.connections:
                    connection.sc.close()

                print("Inchiderea serverului...")
                os.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server-ul pt Chat")
    parser.add_argument('host', help='Se asculta la')
    parser.add_argument('-p', metavar='PORT', type=int,
                        default=1060, help='TCP port (default 1060)')

    args = parser.parse_args()

    # creerea si pornirea thread-ului pt server
    server = Server(args.host, args.p)
    server.start()

    exit_thread = threading.Thread(target=exit, args=(server,))
    exit_thread.start()
