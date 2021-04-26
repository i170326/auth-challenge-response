import socket
import sys

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

while True:
    print("Connecting to server\n")
    sock=tcp_connect('locahost',1234)
    print("Receiving Message\n")
    recvMsg = tcp_receive(sock)
    if(len(recvMsg)>0):
        print(recvMsg)
        break
