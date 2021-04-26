import socket
import sys
import sqlite3
from sqlite3 import Error

def tcp_connect(ip,port):
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((socket.gethostname(),port))
    print("Server is listening")
    sock.listen(5)
    return sock

def tcp_send(msg,conn):
    print("Sending message")
    conn.send(bytes(msg,"utf-8"))

def tcp_receive(conn):
    print("Message Receiving started")
    full_msg = ''
    while True:
        print("Receiving Message")
        msg = conn.recv(8)
        if len(msg) <=0:
            break
        full_msg = full_msg + msg.decode("utf-8")
    return full_msg

def tcp_close(conn):
    print("Closing connection")
    conn.close()

def conn_db():
    try:
        conn=sqlite3.connect("users.db")
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)

def db_table(conn):
    sql_create_table = """ CREATE TABLE IF NOT EXISTS user(
                                        id integer primary key AUTOINCREMENT,
                                        name nvarchar(40) not null,
                                        password nvarchar(32) not null
                                    ); """
    
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
        
    except Error as e:
        print(e)
    
def db_insert(conn,username,password):
    try:
        c = conn.cursor()
        c.execute('insert into user (name, password) values (?, ?)', (username, password,))
        conn.commit()
    except Error as e:
        print(e)    

print("Connecting to db")
db_conn=conn_db() #Connect to db
print("Checking table")
db_table(db_conn) #Create user table if it doesn't exist

sock=tcp_connect('localhost',8001) #Setting up server
while True:
    print("Waiting for connection\n")
    conn, address = sock.accept()
    print("Connection has been established with: ",address,"\n")

    recvMsg = tcp_receive(conn)
    print(recvMsg)
    if(recvMsg=="1\n"):
        tcp_send("Registerting",conn) #Letting client know 
        username=tcp_receive(conn) #Listen for username
        password=tcp_receive(conn) #Listen for password
        username=username.strip('\n') #Removing backslash
        password=password.strip('\n')
        db_insert(db_conn,username,password)
        tcp_send("Registered",conn)

    elif(recvMsg=="2\n"): #Debugging Connection  
        tcp_send("Hello this is server",conn)
        tcp_close(conn)
    else:
        tcp_send("Exception message: Some Error in message",conn)
        tcp_close(conn)

