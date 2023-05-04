from fileinput import filename
import socket
import sys
import json
import errno
from config import CLIENT_IPS, CLIENT_PORTS

# "IP Address of the main server"
IP = "100.81.249.49"
PORT = 5589
ADDR = (IP, PORT)
SIZE = 10240000000
FORMAT = "utf-8"
from blockchain_main import execute_process
import time


def main():
    print("*[STARTING] The server is Starting")
    '''Starting the socket'''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    'Bind the IP and PORT to the server'
    server.bind(ADDR)
    'Server is Listening, i.e, server is now waiting for the client to get connected.'
    server.listen()
    print(f'Listening to port {PORT}')
    while True:
        '''Accepting Connection from Client. '''
        conn, addr = server.accept()
        print(f"[New Connection] {addr} connected.")
        print("New Connection Started seeding file")
        # dat = conn.recv(512).decode(FORMAT)
        # print(dat)
        i = 0
        total_data = []
        while True:
            print(f'Receiving Data Chunk {i}')
            data = conn.recv(512).decode(FORMAT)
            i += 1
            if data:
                total_data.append(data)
            else:
                break
        print("All Data Received")
        data = ''.join(total_data)
        '''Here for the main server  addition of data as well as image data will be done, and for all other only 
        addition data will be done '''
        execute_process(data)
        send_blk_data_to_machines(data)
        conn.close()
        print(f"Disconnected {addr} disconnected")


def connect(addr):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Connecting to the server. """
    conn.connect(addr)
    return conn


def chunks(lst, n):
    """Yield successive n-sized chunks from lst"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def send_blk_data_to_machines(data):
    for ip, port in CLIENT_IPS, CLIENT_PORTS:
        connection = connect((ip, port))
        connection.send("save_blk_data".encode(FORMAT))
        time.sleep(2)
        i = 0
        print("Sending data in Chunks")
        for chunk in chunks(data, 100):
            print(f"Sending chunk {i}")
            connection.send(chunk.encode(FORMAT))
            i += 1

        print("All Data sent")

        connection.close()


def verify_chain():
    flag = 0
    for ip, port in CLIENT_IPS, CLIENT_PORTS:
        connection = connect((ip, port))
        connection.send("verify_chain".encode(FORMAT))
        time.sleep(2)
        with open('/home/vishwajeet/Travclan/BLK/the_blockchain/hashes.json') as hashes_file:
            main_server_hash_dict = json.load(hashes_file)
            connection.send(main_server_hash_dict.encode(FORMAT))

        current_flag = int(connection.recv(SIZE).decode(FORMAT))

        flag = flag & current_flag
        connection.close()

    if flag:
        print("********Block Chain Verified****************")

    print("Block chain is corrupted please check the Data")


if __name__ == "__main__":
    main()
