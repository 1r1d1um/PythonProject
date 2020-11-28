
import socket
import _thread

# threading allows multiple users to connect to server *THIS WILL BE MODIFIED LATER*
def client_thread(client, address):
    while True:
        data = client.recv(1024) # receives data from client
        print(data) # prints it out for us to see
        if not data: break # if no data is being recieved (blank lines), breaks out
        reply = "no u" # "prepares a reply to send back to client on acknowledgements, may be modified."
        reply = bytes(reply, encoding='utf8') # Makes reply into bytes. This must be done between our program to communicate correctly
        client.send(reply) # sents a reply back
    client.close() # closes connection

# starts up the server *THIS WILL MOST LIKELY REMAIN THE SAME EXCEPT ALLOWING MODIFICATION OF TCP_IP AND PORT (or automatic finding).
def serverReceive():
    TCP_IP = '192.168.1.129'
    TCP_PORT = 5005
    print(TCP_IP)
    print(TCP_PORT)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(10)    # allows 10 users to connect, or rejects incoming connections

    # loops forever for new threads to occur
    while True:
        c, address = s.accept()
        _thread.start_new_thread(client_thread, (c, address))

#Code below used to send message to server to test connectivity
#def serverSend():
#    TCP_IP = '192.168.1.129'
#    TCP_PORT = 5005
#    MESSAGE = 'THIS SENT SUCCESSFULLY'
#    MESSAGE = bytes(MESSAGE, encoding='utf8')
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.connect((TCP_IP, TCP_PORT))
#    s.send(MESSAGE)
#    data = s.recv(1024)
#    s.close()


serverReceive()     # starts server up and will continue to run and recieve messages, then send a response back
