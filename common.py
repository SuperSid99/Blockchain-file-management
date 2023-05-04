import socket
from constants import WHITELISTED_CLIENT_IPS
import json
import logging
from blockchain_main import execute_node_process

MAIN_SERVER_IP = ""#server ip goes here
MAIN_SERVER_PORT = "1234"
IP = "client IP"
PORT = "CLIENT Port"
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 10240000000

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('')


def get_data_by_chunks(conn):
    i = 0
    total_data = []
    log.info("Getting Data By Chunks")
    while True:
        log.info(f'Receiving Data Chunk {i}')
        data = conn.recv(100).decode(FORMAT)
        i += 1
        if data:
            total_data.append(data)
        else:
            break
    log.info("All data Received.")
    return total_data


def chunks(lst, n):
    """Yield successive n-sized chunks from lst"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_node_hash_data(file_path):
    with open(file_path) as hashes_file:
        machine_blockchain = json.load(hashes_file)
        return machine_blockchain


def get_key_by_addr(addr, lst):
    for _ in lst:
        if _[0] == addr:
            return _[1]

    return ValueError("No Key Found")


def connect(addr):
    log.info(f"Connecting To Address ==> {addr}")
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        """ Connecting to the server. """
        conn.connect(addr)
        log.info(f"connected. >>{conn}")
        return conn
    except Exception as e:
        log.error(f"An Error Occurred While Connecting. Error >> {e}")
        return e


def save_node_blk_data(conn):
    log.info("Getting Data By chunks")
    data = get_data_by_chunks(conn)
    log.info("All Data Received")
    data = ''.join(data)
    execute_node_process(data)
    conn.close()
    # print(f"Disconnected {addr} disconnected")


def get_client_key_by_addr(addr):
    for _ in WHITELISTED_CLIENT_IPS:
        if _[0] == addr:
            print(_[2])
            return _[2]
    return ValueError("No key Found")

