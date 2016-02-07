import socket
import sys
import threading
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()


def socket_create():
    global host
    global port
    global s
    host = '192.168.1.41'
    port = 2222
    s = socket.socket()
    s.connect((host, port))

def create_and_store_file(data_str):
    file = open("bro2.txt", "a+")
    file.write(data_str)

def listen_for_msg():
    while True:
        data = s.recv(1024)
        data_str = str(data[:].decode("utf-8"))
        data_list = data_str.split("\n")
        if data_list[0] != " " and data_list[0] != "file":
            print(data_str)
        elif data_list[0] == "file":
            del data_list[0]
            data_str = "\n".join(data_list)
            create_and_store_file(data_str)


def send_msg():
    while True:
        sent_msg = input()
        if sent_msg != " ":
            s.send(str.encode(sent_msg, "utf-8"))
        elif sent_msg == "quit":
            s.close()

def create_worker():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        x = queue.get()
        if x == 1:
           listen_for_msg()
        if x == 2:
           send_msg()
        queue.task_done()


# Each list item is a new job

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

socket_create()
create_worker()
create_jobs()
