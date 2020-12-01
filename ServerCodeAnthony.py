
import socket
import _thread
import json

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

# threading allows multiple users to connect to server *THIS WILL BE MODIFIED LATER*
def client_thread(clientThread, addressOfUser):
    connectionString = "Connected to chatroom"
    clientThread.send(bytes(connectionString, encoding='utf8'))

    while True:
        data = clientThread.recv(1024)      # receives data from client
        if data:                            # checks if data has been received and stops when no more is coming in
            print(data)                     # prints the data out on the server in the json/dictionary format. This can be modified later for better server logging
            sendAllMessage(data, client)    # sends messages to all connected users (except original sender)
            # client.send(data) <-- used to test if original user can also recieve messages
        else:
            removeConnection(clientThread)  # if no data arrives from the connected user, the user is disconnected from the server

TCP_IP = input("Input IP Address of Server: ")  # default 192.168.1.129 unless it changed
TCP_PORT = input("Input Port for Server: ")     # default 5005 and should remain constant
print(TCP_IP)
print(TCP_PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, int(TCP_PORT)))
server.listen(10)                                               # allows 10 users to connect, or rejects incoming connections
connectedUsers = []                                             # used to keep track of connected users

# loops forever for new threads to occur
while True:
    client, address = server.accept()                           # accepts new incoming connection
    connectedUsers.append(client)                               # appends the ip address/identifier of the incoming client
    _thread.start_new_thread(client_thread, (client, address))  # starts a new thread for the new user
