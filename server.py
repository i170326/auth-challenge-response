import socket
import sys
import sqlite3
import string
import random
from sqlite3 import Error
from Crypto.Cipher import AES

def tcp_connect(ip,port):
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((socket.gethostname(),port))
    print("Server is listening")
    sock.listen(5)
    return sock

def tcp_send(msg,conn):
    #print("Sending message")
    conn.send(bytes(msg,"utf-8"))

def tcp_receive(sock):
    #time.sleep(10)
    msg = sock.recv(2048).decode("utf-8")
    """while True:
        msg = sock.recv(8)
        if len(msg) <=0:
            break
        full_msg = full_msg + msg.decode("utf-8")
    return full_msg"""
    return msg

def tcp_receive_cipher(sock):
    msg = sock.recv(2048)
    return msg

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

def db_fetch(conn,username):
    try:
        c = conn.cursor()
        c.execute('select password from user where name = ?', (username,))
        rows = c.fetchall()
        return rows
    except Error as e:
        print(e)

def random_token_generator(size=16, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

print("Connecting to db")
db_conn=conn_db() #Connect to db
#print("Checking table")
db_table(db_conn) #Create user table if it doesn't exist

sock=tcp_connect('localhost',8001) #Setting up server
while True:
    print("Waiting for connection\n")
    conn, address = sock.accept()
    print("Connection has been established with: ",address,"\n")

    recvMsg = tcp_receive(conn)
    #print(recvMsg)
    if(recvMsg=="1"):
        tcp_send("Registerting",conn) #Letting client know 
        username=tcp_receive(conn) #Listen for username
        password=tcp_receive(conn) #Listen for password
        username=username.strip('\n') #Removing backslash
        password=password.strip('\n')
        db_insert(db_conn,username,password)
        tcp_send("Registered",conn)
    
    elif(recvMsg=="2"):
        tcp_send("Logging In",conn) #Letting client know
        username=tcp_receive(conn) #Listen for username
        password=tcp_receive(conn) #Listen for password
        username=username.strip('\n') #Removing backslash
        password=password.strip('\n')
        pass_db=db_fetch(db_conn,username)
        if(not pass_db):
            print("No username found")
            tcp_send("User does not exist",conn)
        else:
            tcp_send("User found",conn)
            pass_db=pass_db[0]
            pass_db=pass_db[0]
            token=random_token_generator()
            tcp_send(token,conn)
            obj = AES.new(token.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
            ciphertext = obj.encrypt(pass_db.encode("utf8"))
            chal_pass=tcp_receive_cipher(conn)
            if(chal_pass==ciphertext):
                print("Logged In")
                tcp_send("Logged In",conn)

            else:
                print("Unsuccessful")
                tcp_send("Password Mismatch",conn)
    
    else:
        tcp_send("Exception message: Some Error in Option",conn)
        tcp_close(conn)

