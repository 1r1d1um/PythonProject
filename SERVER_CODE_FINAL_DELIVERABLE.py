import socket
import _thread
import json
import os

# Anthony's Code
# checks through the list of connected users and sends the data to each of them (excluding the user who originally sent the data for retransmission)
def sendAllMessage(data, clientVal):
    for user in connectedUsers:
        if user != clientVal:
            try:
                user.send(data)                 # attempts to send data to user to check if they are connected
            except:
                user.close()                    # closes user connection if data could not be sent (possibly disconnected)
                removeConnection(clientVal)     # removes their name from the list that shows connected users

# Anthony's Code
def removeConnection(clientRemove):
    if clientRemove in connectedUsers:                          # checks for specified user in list to remove
        connectedUsers.remove(clientRemove)                     # removes name from list
        connectedUsersFriendly.remove(client.getpeername())     # removes name from friendly printable list

# threading allows multiple users to connect to server
def client_thread(clientThread, addressOfUser):
    # receives data from client until they disconnect or no longer need the thread
    while True:
        try:
            dataPackage = clientThread.recv(4096)                   # receives data from client
            if dataPackage:                                         # checks if data has been received and stops when no more is coming in
                dataCheck = json.loads(dataPackage.decode('utf-8')) # loads json package data to read

                # checks if the operation is 1 for chat box instructions
                if dataCheck['Operation'] == '1':
                    print(dataCheck["time"] + " - " + dataCheck["sender"] + ": " + dataCheck["message"])    # prints the data out on the server in the json/dictionary format. This can be modified later for better server logging
                    sendAllMessage(dataPackage, client)                                                     # sends messages to all connected users (except original sender)

                # Gabriel's Code Below
                # checks if the operation is 2 for file client to server upload
                elif dataCheck['Operation'] == '2':

                    #from server_filetransfer_GabrielYeager.py
                    # opens file for writing binary
                    sendAllMessage(dataPackage, client)
                    print("File Transfer from client to server occurring...")

                    # writes to new file until end of sent file
                    while True:
                        bytes_read = clientThread.recv(4096)        # reading 4096 bytes

                        # if there are no more bytes to read, break
                        if not bytes_read:
                            # file transmission is done
                            break
                        f = open(dataCheck["file_name"], "ab+")     # opens file with specified name from client
                        f.write(bytes_read)                         # writes data to file
                        f.close()                                   # closes file

                # Gabriel's Code Below
                # checks if the operation is 3 for file server to client upload
                elif dataCheck['Operation'] == '3':

                    # taken from client_filetransfer_Gabriel_Yeager.py
                    f = open(dataCheck['file_name'], "rb")
                    print("File Transfer from server to client occurring...")

                    # reads file until end of the file
                    while True:
                        bytes_read = f.read(4096)           # reading 4096 bytes

                        #if there are no more bytes to read, break
                        if not bytes_read:
                            # file transmitting is done
                            break
                        clientThread.sendall(bytes_read)    # sends data to client
                else:
                    print("ERROR, NO OPERATION SEEN. CLIENT ERROR DETECTED.")

            else:
                removeConnection(clientThread)  # if no data arrives from the connected user, the user is disconnected from the server
        except:
            continue

# Anthony's Code Below
TCP_IP = input("Input IP Address of Server: ")  # default 192.168.1.129 unless it changed
TCP_PORT = input("Input Port for Server: ")     # default 5005 and should remain constant
print("SERVER IP: " + TCP_IP)                   # displays current server ip
print("SERVER PORT: " + TCP_PORT + "\n")        # displays current server port

# Anthony's Code Below
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, int(TCP_PORT)))
server.listen(10)                                               # allows 10 users to connect, or rejects incoming connections
connectedUsers = []                                             # used to keep track of connected users
# connectedUsersFriendly = []                                   # used to print out currently connected threads (for tracking)

# Anthony's Code Below
# loops forever for new threads to occur
while True:
    client, address = server.accept()                           # accepts new incoming connection
    connectedUsers.append(client)                               # appends the ip address/identifier of the incoming client
    # connectedUsersFriendly.append(client.getpeername())       # used for server debugging
    # print("Current Threads Connected: ", end='')              # used for server debugging
    # print(connectedUsersFriendly)                             # prints currently connected threads to server window (used for server debugging)
    _thread.start_new_thread(client_thread, (client, address))  # starts a new thread for the new user

