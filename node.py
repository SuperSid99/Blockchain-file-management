import socket
import time
import logging
from common import save_node_blk_data, get_node_hash_data, chunks
import json
NODE_IP = "" #node ip goes here
NODE_PORT = 1234
SIZE = 10240000000
FORMAT = "utf-8"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('')

# This function will open up a port of listener(with given IP) for the client to recieve the data files


def initiate_socket_listener():
    global conn
    global addr
    global server
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        'Bind the IP and PORT to the server'
        server.bind((NODE_IP, NODE_PORT))
        'Server is Listening, i.e, server is now waiting for the client to get connected.'
        server.listen()
        '''Accepting Connection from Client. '''

        log.info(f"Server is Listening on {NODE_IP, NODE_PORT}")
        while True:
            conn, addr = server.accept()
            log.info(f"[New Connection] {addr} connected.")
            log.info("New Connection Started seeding.")
            func = conn.recv(512).decode(FORMAT)

            if func == 'save_node_blk_data':
                log.info("Request Received for Saving a New Block")
                conn.send("OK".encode(FORMAT))
                time.sleep(3)
                save_node_blk_data(conn)
                log.info(f"Block Data saved!!")
            elif func == 'get_node_hash_data':
                log.info("Request Received for ")
                conn.send("OK".encode(FORMAT))
                log.info("SENT OK")
                time.sleep(5)
                hash_data = get_node_hash_data("path to/hashes.json")
                i = 0
                log.info("Sending Data in Chunks")
                for chunk in chunks(json.dumps(hash_data), 100):
                    conn.send(chunk.encode(FORMAT))
                    i += 1
                # connection.send("  END".encode(FORMAT))
                conn.close()
                log.info("All Data sent")

            elif KeyboardInterrupt:
                server.close()
                break
                # conn.close()


def main():
    initiate_socket_listener()


if __name__ == '__main__':
    main()

