import socket
import sys
import hashlib
from Crypto.Cipher import AES


def tcp_connect(ip,port):
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((socket.gethostname(),port))
    return sock

def tcp_receive(sock):
    """full_msg = ''
    while True:
        msg = sock.recv(2048)
        if len(msg) <=0:
            break
        full_msg = full_msg + msg.decode("utf-8")
    return full_msg"""
    #time.sleep(10)
    msg = sock.recv(2048).decode("utf-8")
    return msg

def tcp_send(msg,conn):
    #print("Sending message")
    conn.sendall(bytes(msg,"utf-8"))

def tcp_send_cipher(msg,conn):
    #print("Sending message")
    conn.sendall(msg)

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
    option = (input("Choose from the following\n1. Press 1 for Registeration.\n2.Press 2 for Login\n"))
    print(option)
    if (option=='1'): #Registeration
        tcp_send("1",sock)
        #print("Message sent") #Letting server know the option
        recvMsg = tcp_receive(sock)
        if(recvMsg=="Registerting"): #Server has started registering
            username=input("Enter username: ")
            tcp_send(username,sock) #Send username
            tcp_send(hashed_password(),sock) #Send hashed password
            recvMsg = tcp_receive(sock)
            if(len(recvMsg)>0):
                print(recvMsg)
                tcp_close(sock)
                break

    elif(option=='2'):
        tcp_send("2",sock)
        recvMsg = tcp_receive(sock)
        
        if(recvMsg=="Logging In"):
            username=input("Enter username: ")
            tcp_send(username,sock) #Send username
            password=hashed_password()
            tcp_send(password,sock) #Send hashed password
            recvMsg = tcp_receive(sock)
            if(len(recvMsg)>0):
                if(recvMsg=="User does not exist"):
                    print(recvMsg,"\n")
                    tcp_close(sock)
                
                else:
                    token=tcp_receive(sock)
                    print("Token received")
                    obj = AES.new(token.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
                    ciphertext = obj.encrypt(password.encode("utf8"))
                    tcp_send_cipher(ciphertext,sock)
                    recvMsg=tcp_receive(sock)
                    if(recvMsg=="Logged In"):
                        print(recvMsg)
                        tcp_close(sock)
                        break
                    else:
                        print(recvMsg,"\n")
                        tcp_close(sock)
