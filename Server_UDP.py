# Importing the socket module
import socket
# For realtime updation of state
import threading

# AF_INET - IPv4 Connection
# SOCK_DGRAM - UDP Connection
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# For allowing reconnecting of clients
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Socket successfully created.")

# IPv4 to be used
# The Binding port no is reserved in my laptop
IP = "127.0.0.1"  
port = 3000 

# Now we bind our host machine and port with the socket object we created
# The IPv4 address is given above
# The server is now listening for requests from other host machines also connected to the network
serverSocket.bind((IP,port))
print("Socket(Server) is currently active and listening to requests!!")

# Stores all those sockets which are connected
socketsList = [port]
# Client conected
clients = {}
# Clients IP who are connected
clients_ip = {}

# A function to recieve messages from the clients connected over the network
def recieveMessage():
    try:
        # Recieving the message from users
        sender = serverSocket.recvfrom(1024)
        sender_ip = sender[1][0]
        sender_port = sender[1][1]
        sender_message = sender[0].decode()
        if not len(sender):
            return False 
        # Returning the message and its header
        return {"Sender_IP" : sender_ip , "Sender_Port" : sender_port , "Data" : sender_message}
    except: 
        return False

# Making a thread for every user connected to the server
def clientThread():
    while True:
        try:
            sender = recieveMessage()
            if(sender["Data"][0:8] == "USERNAME"):
                print(f"Connection from {(sender['Sender_IP'],sender['Sender_Port'])} has been established!! : UserName : {sender['Data'][8:]}")        
                # The message to be sent
                msg = "Welcome to the server,Thanks for connecting!!"
                # Sending information to client socket
                serverSocket.sendto(msg.encode(),(sender['Sender_IP'],sender['Sender_Port']))
                socketsList.append(sender['Sender_Port'])
                clients[sender['Sender_Port']] = sender['Data'][8:]
                clients_ip[sender['Sender_Port']] = sender['Sender_IP']
            else:
                if sender["Sender_Port"] == "":
                    print(f"Closed Connection from {clients[sender['Sender_Port']]}")
                    socketsList.remove(sender["Sender_Port"])
                    del clients[sender["Sender_Port"]]
                    break
                # This is the exiting condition if the user types exit@me he exists the connection
                if (sender['Data'][(int(sender['Data'][0]) + 1) : ] == "exit@me"):
                    print(f"Closed Connection from {clients[sender['Sender_Port']]}")
                    socketsList.remove(sender["Sender_Port"])
                    del clients[sender["Sender_Port"]]
                    break
                user = clients[sender["Sender_Port"]]
                print(f"Recieved message from {user} : {sender['Data'][(int(sender['Data'][0]) + 1) : ] }")
                # Distributing the Data to other clients
                for client in clients_ip:
                    if client != sender["Sender_Port"]:
                       serverSocket.sendto(sender["Data"].encode(),(clients_ip[client],client))
        except:
            print(f"Closed Connection from {clients[sender['Sender_Port']]}")
            socketsList.remove(sender["Sender_Port"])
            del clients[sender["Sender_Port"]]
            break

# Function for server to sendto the message    
def writeData():
    while True:
        message = input("")           
        if message:
            message = message.encode()
        for client in clients_ip:
            if client != port:
               serverSocket.sendto("6Server".encode() + message,(clients_ip[client],client))


# Listening to requests infinitely untill interupted
while True:
        thread = threading.Thread(target = clientThread)
        thread.start()
        
        writeThread = threading.Thread(target = writeData)
        writeThread.start()

