import os
import socket
import sys
import threading
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()


def create_socket():
    try:
        global host
        global port
        global s
        host = ''
        port = 2222
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error" + str(msg))

def socket_bind():
    try:
        global host
        global port
        print("Binding socket to port" + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error " + str(msg) + "\n" + "Retrying...")
        socket_bind()

def socket_accept():
    global conn
    conn, address = s.accept()
    print("Connection has been established")

def send_messages(conn):
    while True:
        sent_msg = input()
        if sent_msg != "quit":
            conn.send(str.encode(sent_msg, 'utf-8'))
        else:
            conn.close()
            s.close()

def send_file():
    file_content = ""
    with open("bro.txt") as f:
        for line in f:
            file_content += line
        conn.send(str.encode("file\n" + file_content, 'utf-8'))
        f.close()


def listening_for_msgs(conn):
    while True:
        rcv_msg = conn.recv(1024)
        rcv_msg_str = str(rcv_msg[:].decode("utf-8"))
        if rcv_msg_str != " " and rcv_msg_str != "send file":
            print(rcv_msg_str)
        elif rcv_msg_str == "send file":
            send_file()


def create_worker():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        x = queue.get()
        if x == 1:
           send_messages(conn)
        if x == 2:
           listening_for_msgs(conn)
        queue.task_done()


# Each list item is a new job

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


def main():
    create_socket()
    socket_bind()
    socket_accept()
    create_worker()
    create_jobs()


main()






