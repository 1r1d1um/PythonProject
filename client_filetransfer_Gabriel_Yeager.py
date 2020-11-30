'''
Gabriel Yeager
11/29/2020
Python Final Project: File transfer client
'''

import socket
import os

SEPARATOR = "<SEPARATOR>"
# for sending 4096 bytes each iteration
BUFFER_SIZE = 4096

# ip address of server
host = "10.0.0.203"
# the port
port = 2001
# the name of file to be sent
filename = "testData.txt"
# gets the file size
filesize = os.path.getsize(filename)

# creates the client socket
s = socket.socket()

print("Connecting...")
s.connect((host, port))
print("Connection established")


def send_file(fname, fsize):
    # opens file for reading binary
    f = open(filename, "rb")

    # sends the file name and file size
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # reads file until end of the file
    byte_read = True
    while byte_read:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        s.sendall(bytes_read)


send_file(filename, filesize)
