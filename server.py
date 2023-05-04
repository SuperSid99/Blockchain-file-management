import socket
import json

from blockchain_main import execute_process, execute_node_process
import time
from image import decyript_image, get_key, give_encyripted_image_for_main_server
from common import (
    chunks,
    get_data_by_chunks,
    get_key_by_addr,
    connect,
    get_node_hash_data,
    get_client_key_by_addr,
)
from constants import NODES, CAMERA_MODULES_IPS, WHITELISTED_CLIENT_IPS
from write_to_json import get_image_data, get_file_type
import logging

# "IP Address of the main server"
IP = ""  # public ip
PORT = 5589
ADDR = (IP, PORT)
SIZE = 10240000000
FORMAT = "utf-8"
MAIN_SERVER_KEY = "0000"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("")


def save_node_blk_data(conn):
    data = get_data_by_chunks(conn)
    execute_node_process(data)
    conn.close()


def get_decrypted_data_of_camera_module(addr, data):
    key = get_key_by_addr(addr, CAMERA_MODULES_IPS)
    decrypted_image_data = decyript_image(data, key)
    return decrypted_image_data


def main():
    log.info("*[STARTING] The server is Starting")
    """Starting the socket"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    "Bind the IP and PORT to the server"
    server.bind(ADDR)
    "Server is Listening, i.e, server is now waiting for the client to get connected."
    server.listen()
    log.info(f"Listening to port {PORT}")
    try:
        while True:
            """Accepting Connection from Client."""
            # print("while started")
            conn, addr = server.accept()
            log.info(f"[New Connection] {addr} connected.")
            log.info("New Connection Started seeding file")

            # data = conn.recv(512).decode(FORMAT)
            # print(data)

            func = conn.recv(51).decode(FORMAT)
            log.info(func)

            if func == "camera":

                log.info("Request Received By Camera Module")
                conn.send("OK".encode(FORMAT))
                log.info("Request Acknowledged")
                log.info("Receiving Camera Encrypted Data from Camera Module")
                file_type=conn.recv(51).decode(FORMAT)
                time.sleep(1)
                file_name=conn.recv(51).decode(FORMAT)
                time.sleep(1)
                total_data = get_data_by_chunks(conn)
                data = "".join(total_data)
                # print(len(total_data))
                if file_type in ["jpg","png","jpeg"]:
                    """Now Decrypt image from Camera Module"""
                    log.info("Blockchain Creation Process Started.")
                    log.info("[STEP 1] Decrypting image from Camera Module")
                    decrypted_data_from_camera_module = get_decrypted_data_of_camera_module(
                        addr[0], data
                    )

                    # print(len(decrypted_data_from_camera_module))
                    # print(len(decrypted_data_from_camera_module[0]))

                    # imggg= (numpy.array(decrypted_data_from_camera_module, dtype=numpy.uint8))
                    # print(imggg.shape)
                    # cv.imshow("im_numpy", imggg)
                    # cv.waitKey(0)
                    log.info(
                        "[STEP 2] Verifying The Existing Block chain Before Creating New Block"
                    )
                    if verify_chain():
                        log.info("BlockChain Is Verified")
                        key = get_key()
                        log.info("[STEP 3] Encrypting Data For Blockchain")
                        final_encrypted_data = give_encyripted_image_for_main_server(
                            decrypted_data_from_camera_module, key
                        )
                        log.info("[STEP 4] Finally Process the Block.")
                        processed_block = execute_process(final_encrypted_data,file_name,file_type)
                        log.info("Final Processed Block Data >>")
                        log.info(processed_block)
                        send_blk_data_to_machines(processed_block)
                        log.info("Process Finished")
                    else:
                        log.info("Block Chain is Corrupted")
                    print(f"Disconnected {addr} disconnected")
                elif file_type=="txt":
                    log.info("Blockchain Creation Process Started.")
                    log.info(
                        "[STEP 2] Verifying The Existing Block chain Before Creating New Block"
                    )
                    if verify_chain():
                        log.info("BlockChain Is Verified")
                        log.info("[STEP 3] Encrypting Data For Blockchain")
                        log.info("[STEP 4] Finally Process the Block.")
                        processed_block = execute_process(data,file_name,file_type)
                        log.info("Final Processed Block Data >>")
                        log.info(processed_block)
                        send_blk_data_to_machines(processed_block)
                        log.info("Process Finished")
                    else:
                        log.info("Block Chain is Corrupted")
                    print(f"Disconnected {addr} disconnected")

            elif func == "authenticate":
                log.info("Request Received By Client For Authentication ")
                conn.send("OK".encode(FORMAT))
                log.info("Request Acknowledged")
                time.sleep(2)
                flag = str(authenticate(addr[0]))
                conn.send(flag.encode(FORMAT))
                log.info("Authentication Process Complete")
                conn.close()
            elif func == "get_hash_data":
                log.info("Request Received By Client For Hashes Data ")
                conn.send("OK".encode(FORMAT))
                log.info("Request Acknowledged")
                time.sleep(2)
                hashes_data = get_node_hash_data(
                    "/Users/siddharthsharma/Desktop/Blockchain_file_management/hashes.json"
                )
                log.info("Sending data in Chunks")
                i = 0
                for chunk in chunks(json.dumps(hashes_data), 100):
                    # print(f"Sending chunk {i}")
                    conn.send(chunk.encode(FORMAT))
                    i += 1
                log.info("All Data Sent")
                conn.close()
            elif func == "get_en_data":
                log.info("Request Received By Client For Hash Data")
                conn.send("OK".encode(FORMAT))
                log.info("Request Acknowledged")
                time.sleep(2)
                hash_value = conn.recv(512).decode(FORMAT)
                log.info(f"Received Hash =>> {hash_value}")
                send_en_data_by_hash_value(hash_value, conn, addr)
                # print("All Data Sent")
                conn.close()

            else:
                log.info("Invalid connection. Please Try Again")
                conn.close()
    except Exception as e:
        log.error(f"An Error Occurred. Error ==>  {e}")
        import traceback

        traceback.print_exc()


def authenticate(addr):
    for _ in WHITELISTED_CLIENT_IPS:
        if _[0] == addr:
            return 1
    return 0


def send_blk_data_to_machines(data):
    for _ in NODES:
        connection = connect((_[0], _[1]))
        connection.send("save_node_blk_data".encode(FORMAT))
        time.sleep(2)
        i = 0
        var = connection.recv(512).decode(FORMAT)
        if var == "OK":
            log.info("Sending data in Chunks")
            for chunk in chunks(json.dumps(data), 100):
                # print(f"Sending chunk {i}")
                connection.send(chunk.encode(FORMAT))
                i += 1

            log.info("All Data sent")

        connection.close()


def send_en_data_by_hash_value(hash_value, conn, addr):
    file_info=get_file_type(hash_value)
    en_data = get_image_data(hash_value)
    if file_info[1] in ["jpg","jpeg","png"]:
        decrypted_data_of_main_server = decyript_image(en_data, MAIN_SERVER_KEY)
        client_key = get_client_key_by_addr(addr[0])
        file_data = give_encyripted_image_for_main_server(
            decrypted_data_of_main_server, client_key
        )
    elif file_info[1]=="txt":
        file_data=en_data
    conn.send(file_info[1].encode(FORMAT))
    time.sleep(1)
    conn.send(file_info[0].encode(FORMAT))
    time.sleep(1)
    log.info("Sending data in Chunks")
    i = 0
    for chunk in chunks(json.dumps(file_data), 100):
        # print(f"Sending chunk {i}")
        conn.send(chunk.encode(FORMAT))
        i += 1
    log.info("All Data Sent")


def verify_chain():
    print("reaching Here")
    flag = True
    for _ in NODES:
        connection = connect((_[0], _[1]))
        print("CONNECTED")
        time.sleep(2)
        connection.send("get_node_hash_data".encode(FORMAT))
        var = connection.recv(512).decode(FORMAT)
        if var == "OK":
            node_hash_dict = get_data_by_chunks(connection)
            node_hash_dict = "".join(node_hash_dict)
            node_hash_dict = json.loads(node_hash_dict)
            with open(
                "/Users/siddharthsharma/Desktop/Blockchain_file_management/hashes.json"
            ) as hashes_file:
                main_server_hash_dict = json.load(hashes_file)

            print(main_server_hash_dict == node_hash_dict)

            current_flag = main_server_hash_dict == node_hash_dict
            log.info(current_flag)
            if not current_flag:
                log.error(
                    f"Block Chain Not Verified At Node {_[0]}, {_[1]}. Please check the Machine."
                )
            flag = flag & current_flag
            connection.close()
        else:
            log.info("Connection Not Acknowledged")
            return flag

    if flag:
        log.info("******** Block Chain Verified ****************")

    return flag


if __name__ == "__main__":
    main()
