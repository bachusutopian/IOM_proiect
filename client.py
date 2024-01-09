import threading
import socket
import argparse
import os
import tkinter as tk
import sys


class Send(threading.Thread):

    # waits for the user input

    # connects the sock object
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):

        # listens to the user input and sends it to the server

        while True:
            print('{}'.format(self.name), end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]
            # if we type quit, then we leave the chat
            if message == 'QUIT':
                self.sock.sendall('Server:{} a iesit de pe chat.'.format(
                    self.name).encode('ascii'))
                break
            else:
                self.sock.sendall('{}:{}'.format(
                    self.name, message).encode('ascii'))
        print('\n Quitting the server...')
        self.sock.close()
        os.exit(0)


class IncomingMessageHandler(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None

    # functionalities that our gui will have

    def run(self):
        while True:
            message = self.sock.recv(1024).decode('ascii')

            if message:
                if self.messages:
                    self.messages.insert(tk.END, message)
                    print("Salut!")
                    print('\r{}\n{}:'.format(message.self.name), end='')
                else:
                    print('\r{}\n{}:'.format(message.self.name), end='')
            else:
                print('\n Conexiunea cu server-ul a fost blocata')
                print('Quiting!')
                self.sock.close()
                os.exit(0)


class Client:

    # Client-server interface ( connection + integration )

    def __init__(self, host, port):
        self.host = host
        self.port = port,
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None

    # notifies the other clients when a user connects

    def connection(self):
        print('Incearca sa se conecteze la {}:{}...'.format(self.host, self.port))

        self.sock.connect((self.host, self.port))

        print('Conectare cu succes la {}:{}'.format(self.host, self.port))

        print()

        self.name = input('Numele tau:')

        print()

        print('Bine ai venit, {}! Poti trimite si primi mesaje'.format(self.name))

        # creation and reception of threads

        send = Send(self.host, self.port)
        receive = IncomingMessageHandler(self.sock, self.name)

        # start

        send.start()
        receive.start()

        self.sock.sendall(
            'Server: {} s-a alaturat in discutie'.format(self.name).encode('ascii'))
        print('\rPregatit de a trimite mesaje! Poti parasi discutia tastand "QUIT"')
        print('{}'.format(self.name).encode(''))

        return receive
    
    def exit(self, textIn):
        