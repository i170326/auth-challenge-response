import socket
import sys
import hashlib


def tcp_connect(ip,port):
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((socket.gethostname(),port))
    return sock

def tcp_receive(sock):
    full_msg = ''
    while True:
        msg = sock.recv(8)
        if len(msg) <=0:
            break
        full_msg = full_msg + msg.decode("utf-8")
    return full_msg

def tcp_send(msg,conn):
    print("Sending message")
    conn.send(bytes(msg,"utf-8"))

def tcp_close(conn):
    print("Closing connection")
    conn.close()

def hashed_password():
    u_password=(input("Enter password: "))
    f_password=hashlib.sha512() #assignment requirement for hash algo
    f_password.update(u_password.encode("utf-8"))
    return f_password.hexdigest() #to return as string


while True:
    print("Connecting to server")
    sock=tcp_connect('locahost',8001)
    print("Connected\n")

    #Menu - add UI later
    option = (input("Choose from the following\n1. Press 1 for Registeration.\n2.Press 2 for Server's Message"))
    print(option)
    if (option=='1'): #Registeration
        tcp_send("1",sock)
        print("Message sent") #Letting server know the option
        recvMsg = tcp_receive(sock)
        if(recvMsg=="Registerting\n"): #Server has started registering
            username=input("Enter username: ")
            tcp_send(username,sock) #Send username
            tcp_send(hashed_password(),sock) #Send hashed password
            recvMsg = tcp_receive(sock)
            if(len(recvMsg)>0):
                print(recvMsg)
                tcp_close(sock)
                break


    elif option=='2': #Debugging connection
        tcp_send("2",sock)
        recvMsg = tcp_receive(sock)
        if(len(recvMsg)>0):
            print(recvMsg)
            tcp_close(sock)
            break
