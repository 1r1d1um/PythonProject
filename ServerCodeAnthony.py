
import socket
import _thread
import json
import os

# checks through the list of connected users and sends the data to each of them (excluding the user who originally sent the data for retransmission)
def sendAllMessage(data, clientVal):
    for user in connectedUsers:
        if user != clientVal:
            try:
                user.send(data)
            except:
                user.close()                    # closes user connection if data could not be sent (possibly disconnected)
                removeConnection(clientVal)     # removes their name from the list that shows connected users

def removeConnection(clientRemove):
    if clientRemove in connectedUsers:          # checks for specified user in list to remove
        connectedUsers.remove(clientRemove)     # removes name from list
        connectedUsersFriendly.remove(client.getpeername())

# threading allows multiple users to connect to server *THIS WILL BE MODIFIED LATER*
def client_thread(clientThread, addressOfUser):
    connectionString = "Connected to chatroom"
    clientThread.send(bytes(connectionString, encoding='utf-8'))

    while True:
        try:
            dataPackage = clientThread.recv(4096)           # receives data from client
            if dataPackage:                                 # checks if data has been received and stops when no more is coming in
                dataCheck = json.loads(dataPackage.decode('utf-8'))

                if dataCheck['Operation'] == '1':
                    print(dataCheck["time"] + " - " + dataCheck["sender"] + ": " + dataCheck["message"])  # prints the data out on the server in the json/dictionary format. This can be modified later for better server logging
                    sendAllMessage(dataPackage, client)            # sends messages to all connected users (except original sender)


                elif dataCheck['Operation'] == '2':
                    #from server_filetransfer_GabrielYeager.py

                    # opens file for writing binary
                    sendAllMessage(dataPackage, client)

                    # writes to new file until end of sent file
                    byte_read = True
                    while byte_read:
                        bytes_read = clientThread.recv(4096)
                        if not bytes_read:
                            # file transmission is done
                            break
                        f = open(dataCheck["file_name"], "ab+")
                        f.write(bytes_read)
                        f.close()


                elif dataCheck['Operation'] == '3':
                    # taken from client_filetransfer_Gabriel_Yeager.py
                    f = open(dataCheck['file_name'], "rb")
                    # reads file until end of the file
                    byte_read = True
                    while byte_read:
                        bytes_read = f.read(4096)
                        if not bytes_read:
                            # file transmitting is done
                            break
                        clientThread.sendall(bytes_read)
                    # SEND FILE HERE
                #elif dataCheck['Operation'] == '4':
                #    serverFiles = os.listdir()
                #    serverFiles = str(serverFiles)
                #    clientThread.send(bytes(serverFiles, encoding='utf8'))
                else:
                    print("ERROR, NO OPERATION SEEN. CLIENT ERROR DETECTED.")

            else:
                removeConnection(clientThread)  # if no data arrives from the connected user, the user is disconnected from the server
        except:
            continue

TCP_IP = input("Input IP Address of Server: ")  # default 192.168.1.129 unless it changed
TCP_PORT = input("Input Port for Server: ")     # default 5005 and should remain constant
print("SERVER IP: " + TCP_IP)
print("SERVER PORT: " + TCP_PORT + "\n")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, int(TCP_PORT)))
server.listen(10)                                               # allows 10 users to connect, or rejects incoming connections
connectedUsers = []                                             # used to keep track of connected users
connectedUsersFriendly = []

# loops forever for new threads to occur
while True:
    client, address = server.accept()                           # accepts new incoming connection
    connectedUsers.append(client)                               # appends the ip address/identifier of the incoming client
    connectedUsersFriendly.append(client.getpeername())
    print("Current Users Connected: ", end='')
    print(connectedUsersFriendly)
    _thread.start_new_thread(client_thread, (client, address))  # starts a new thread for the new user


