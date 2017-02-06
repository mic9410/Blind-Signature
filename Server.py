# -*- coding: utf-8 -*-
# Michał Foryt
import getopt
import socket
import sys

from Crypto.PublicKey import RSA

from Utils import complete_message, delete_noise


class Server(object):
    def __init__(self, server_private_key):
        self.server_private_key = server_private_key
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        self.server.bind((SERVER_HOST, SERVER_PORT))
        self.server.listen(5)

    def run(self):
        private_key_string = open(str(self.server_private_key), "r").read()
        private_key = RSA.importKey(private_key_string)
        while True:
            try:
                client = self.server.accept()[0]
                client_request = long(delete_noise(str(client.recv(4096))))
                signed_message = complete_message(
                    str(
                        private_key.sign(client_request, "")[0]
                    )
                )
                client.send(signed_message)
            finally:
                client.close()


if __name__ == '__main__':
    SERVER_HOST = 'localhost'
    SERVER_PORT = None
    CLIENT_PUBLIC_KEY = None
    SERVER_PRIVATE_KEY = None

    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:], "p:S:")

        for opt, arg in OPTS:
            if opt == '-p':
                SERVER_PORT = int(arg)
            if opt == '-S':
                SERVER_PRIVATE_KEY = arg

        SERVER = Server(server_private_key=SERVER_PRIVATE_KEY)
        SERVER.bind()
        SERVER.run()

    except (RuntimeError, TypeError, NameError):
        print "ERROR"
        sys.exit(2)
