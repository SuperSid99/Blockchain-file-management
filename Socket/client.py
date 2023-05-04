from ..blockchain_main import execute_process
from ..image import decyript_image
import threading
import socket
import json

MAIN_SERVER_IP = ""
MAIN_SERVER_PORT = ""
IP = "client IP"
PORT = "CLIENT Port"
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 10240000000


# This function will open up a port of listener(with given IP) for the client to recieve the data files
def initiate_socket_listener():
    global conn
    global addr
    global server
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        'Bind the IP and PORT to the server'
        server.bind(ADDR)
        'Server is Listening, i.e, server is now waiting for the client to get connected.'
        server.listen()
        '''Accepting Connection from Client. '''

        print(f"Server is Listening in The thread on {ADDR}")

        conn, addr = server.accept()
        server.setblocking(True)
        print(f"[New Connection] {addr} connected.")
        print("New Connection Started seeding file")
        func = conn.recv(512).decode(FORMAT)

        if func == 'save_blk_data':
            save_blk_data()
            print(f"Block Data saved!!")


def save_blk_data():
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
    execute_process(data)
    conn.close()
    print(f"Disconnected {addr} disconnected")


def verify_data_with_machine_blockchain(main_server_hash_dict):
    with open('/home/vishwajeet/Travclan/BLK/the_blockchain/hashes.json') as hashes_file:
        machine_blockchain = json.load(hashes_file)
        return 1 if main_server_hash_dict == machine_blockchain else 0


def verify_chain():
    main_server_hash_dict = conn.recv(SIZE).decode(FORMAT)
    flag = verify_data_with_machine_blockchain(main_server_hash_dict)
    conn.send(flag.encode(FORMAT))


def connect_to_main_server():
    main_server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Connecting to the server. """
    main_server_connection.connect((MAIN_SERVER_IP, MAIN_SERVER_PORT))
    return conn


flag = False


def cli():
    global flag
    while True:
        print("\n********Client Interface*********")
        print("1.) Authenticate With Main Server")
        print("2.) Get All Hashes")
        print("3.) Get Hash Data")
        print("4.) Return To Main Interface")
        print("5.) Exit")
        print("*********************************")
        print("\n>>Enter Your Choice:")
        x = int(input())
        if x == 1:
            flag = authenticate()
        elif x == 2:
            get_hashes(flag)
        elif x == 3:
            print("Give the hash Value")
            hash_value = int(input())
            get_data(flag, hash_value)
        elif x == 4:
            print("\nReturning")
        elif x == 5:
            print("\nThanks Exiting!!")
            break
        else:
            print("\nInvalid choice. Please Enter A valid Choice")


def authenticate():
    global connection
    connection = connect_to_main_server()
    connection.send("Authenticate".encode(FORMAT))
    connection.send(IP.encode(FORMAT))
    authentication_flag = connection.recv(SIZE).decode(FORMAT)
    if not authentication_flag:
        print("Invalid Client")
    return authentication_flag


def get_hashes(authentication_flag):
    if authentication_flag:
        connection.send("get_hashes")
        hashes_dict = connection.recv(SIZE).decode(FORMAT)
        print("These Are the Hashes")
        print(hashes_dict)
    else:
        print("\nYou Are Not Authenticated. Please Authenticate Yourself First.")


def get_data(authentication_flag, hash_value):
    if authentication_flag:
        connection.send("get_hash_value".encode(FORMAT))
        key = connection.recv(SIZE).decode(FORMAT)
        decyript_image(hash_value, key)

    else:
        print("\nYou Are Not Authenticated. Please Authenticate Yourself First.")


if __name__ == "__main__":
    print("reaching")
    # t1 = threading.Thread(target=initiate_socket_listener)
    # t1.daemon = True
    # t1.start()
    cli()

    print("T1 thread Started for Receiving Data from Main server")
