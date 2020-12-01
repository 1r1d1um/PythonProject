'''
Gabriel Yeager
11/29/2020
Python Final Project: File transfer server
'''

import socket
import os


# all IPv4 addresses on the local machine
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 2001
# for receiving 4096 bytes each iteration
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# creates the server socket
# TCP socket
s = socket.socket()

# binding the socket to the local address
s.bind((SERVER_HOST, SERVER_PORT))


# refuses new connections after 20 unaccepted connections
s.listen(20)
print("Listening")

# accepts connection
client_socket, address = s.accept()
print("Client is connected")


def receive_file():
    # receive using client socket
    received = client_socket.recv(BUFFER_SIZE).decode()
    # receiving file name and size from client
    filename, filesize = received.split(SEPARATOR)
    # removes absolute path
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)

    # opens file for writing binary
    f = open(filename, "wb")

    # writes to new file until end of sent file
    byte_read = True
    while byte_read:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # file transmission is done
            break
        f.write(bytes_read)


receive_file()
