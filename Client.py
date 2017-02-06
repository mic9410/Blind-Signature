# -*- coding: utf-8 -*-

#Michał Foryt
import getopt
import socket
import sys
from Crypto.PublicKey import RSA


from Utils import complete_message, delete_noise, generate_coprime_random


class Client(object): # pylint: disable=too-few-public-methods
    def __init__(self, server_public_key, message):
        self.server_public_key = server_public_key
        self.server = None
        self.message = message

    def run(self):
        try:

            key = RSA.importKey(open(self.server_public_key).read())
            public_key = key.publickey().exportKey()
            self.server = socket.socket()
            self.server.connect((SERVER_HOST, SERVER_PORT))
            random_number = generate_coprime_random(self.message)
            blinded_message = complete_message(str(public_key.blind(self.message, random_number)))
            self.server.send(blinded_message)
            server_request = str(delete_noise(self.server.recv(4096)))
            unblinded_number = str(public_key.unblind(server_request, random_number))
            print str(unblinded_number)

        except(RuntimeError, TypeError, NameError):
            print 'ERROR'
            sys.exit(2)

if __name__ == '__main__':

    SERVER_HOST = None
    SERVER_PORT = None
    SERVER_PUBLIC_KEY = None
    MESSAGE = None

    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:], "o:p:K:M:")

        for opt, arg in OPTS:
            if opt == '-o':
                SERVER_HOST = arg
            if opt == '-p':
                SERVER_PORT = int(arg)
            if opt == '-K':
                SERVER_PUBLIC_KEY = arg
            if opt == '-M':
                MESSAGE = long(arg)

        CLIENT = Client(server_public_key=SERVER_PUBLIC_KEY, message=MESSAGE)
        CLIENT.run()

    except (RuntimeError, TypeError, NameError):
        print 'ERROR'
        sys.exit(2)
