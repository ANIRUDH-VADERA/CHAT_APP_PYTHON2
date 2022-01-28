# Importing the socket module
import socket
# When no message recieved or any other communication error
import errno
import sys
# For realtime updation of state
import threading

# AF_INET - IPv4 Connection
# SOCK_DGRAM - UDP Connection
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# IPv4 to be used
# The port to which the client wants to connect and send data to
IP = "127.0.0.1"
port = 3000 

# The client userName
my_userName = input("UserName : ")

# Connect to the server on this machine or locally
# No blocking the incoming messages
clientSocket.setblocking(False)

# sendtoing the username to the server
my_userName = "USERNAME" + my_userName
userName = my_userName.encode()
clientSocket.sendto(userName, (IP,port) )

my_userName = my_userName[8:]

# recieving chunks of data from the server
def recieveData():
    flag = 0
    # Recieving things infinitely
    while True:
        try:
            if(flag == 0):# For the initial informative message
                sender = clientSocket.recvfrom(1024)
                sender_message = sender[0].decode()
                print(f"Server > {sender_message}")
                flag = 1
            else:# For the subsequent messages
                sender = clientSocket.recvfrom(1024)
                if not (sender):
                    print("Connection closed by the Server")
                    sys.exit()
                sender_message = sender[0].decode()
                sender_userName_length = int(sender[0].decode()[0])
                sender_Name = sender[0].decode()[1:(sender_userName_length+1)]
                sender_message = sender[0].decode()[(sender_userName_length+1) : ]
                print(f"{sender_Name} > {sender_message}")
        except IOError as e:
            # This is normal on non blocking connections - when there are no incoming data, error is going to be raised
            # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
            # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
            # If we got different error code - something happened
            if(e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK):
                print("Reading Error",str(e))
                sys.exit()
            continue
        except Exception as e:
            print("General error",str(e))
            sys.exit()

# Writing the data and sendtoing it         
def writeData():
    while True:
        message = input("")
        
        if message:
            message = message.encode()
            clientSocket.sendto((str(len(my_userName)) + my_userName).encode() + message, (IP,port) )

recieveThread = threading.Thread(target = recieveData)
recieveThread.start()
            
writeThread = threading.Thread(target = writeData)
writeThread.start()
