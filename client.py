from image import decyript_image
import socket
import time
from common import get_data_by_chunks
import numpy
import cv2 as cv
import json
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('')

MAIN_SERVER_IP = ""#server IP goes here
MAIN_SERVER_PORT = 1234
MACHINE_KEY = 111111
IP = ""#client ip goes here
PORT = 1234
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 10240000000



def connect_to_main_server():
    try:
        main_server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        """ Connecting to the server. """
        main_server_connection.connect((MAIN_SERVER_IP, MAIN_SERVER_PORT))
        return main_server_connection
    except Exception as e:
        log.error(f"An Error Occurred While Connecting To Main Server. Error ==> {e}")
        raise e


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
            hash_value = input()
            get_data(flag, hash_value)
        elif x == 4:
            print("\nReturning")
        elif x == 5:
            print("\nThanks Exiting!!")
            # connection.close()
            break
        else:
            print("\nInvalid choice. Please Enter A valid Choice")


def authenticate():
    connection = connect_to_main_server()
    connection.send("authenticate".encode(FORMAT))
    var = connection.recv(512).decode(FORMAT)
    if var == "OK":
        # connection.send(IP.encode(FORMAT))
        log.info("Please wait while we are authenticating You.")
        authentication_flag = connection.recv(512).decode(FORMAT)
        print(authentication_flag)
        if not authentication_flag:
            log.info("Invalid Client. Please Try Again")
        else:
            log.info("You Are Authenticated.")
        connection.close()
    else:
        log.error("Connection Not Acknowledged.")
    return authentication_flag


def get_hashes(authentication_flag):
    if authentication_flag:
        log.info("Please Wait While We are Fetching Info of Hashes From Main Server")
        get_hashes_data(authentication_flag)
    else:
        log.error("\nYou Are Not Authenticated. Please Authenticate Yourself First.")


def get_hashes_data(authentication_flag):
    connection = connect_to_main_server()
    if authentication_flag:
        connection.send("get_hash_data".encode(FORMAT))
        time.sleep(1)
        var = connection.recv(512).decode(FORMAT)
        if var == "OK":
            data = get_data_by_chunks(connection)
            data = "".join(data)
            data = json.loads(data)
            log.info("The Available Hashes are-->>>")
            print(data)
        else:
            log.error("Connection Not Acknowledged.")
    else:
        log.error("\nYou Are Not Authenticated. Please Authenticate Yourself First.")
    connection.close()


def get_data(authentication_flag, hash_value):
    connection = connect_to_main_server()
    if authentication_flag:
        connection.send("get_en_data".encode(FORMAT))
        time.sleep(1)
        var = connection.recv(512).decode(FORMAT)
        if var == "OK":
            connection.send(hash_value.encode(FORMAT))
            file_type=connection.recv(512).decode(FORMAT)
            time.sleep(1)
            file_name=connection.recv(512).decode(FORMAT)
            time.sleep(1)
            data = get_data_by_chunks(connection)
            data = ''.join(data)
            
            if file_type in ["jpg", "jpeg","png"]:
                decrypted_data = decyript_image(data, MACHINE_KEY)
                img = (numpy.array(decrypted_data, dtype=numpy.uint8))
                cv.imshow(f"{file_name}", img)
                cv.waitKey(0)
                cv.destroyAllWindows()
                cv.waitKey(1)
            elif file_type=="txt":
                txt_file=open(f"{file_name}","w+")
                txt_file.write(data)
        else:
            log.error("Connection Not Acknowledged.")
        return 1

    else:
        log.error("\nYou Are Not Authenticated. Please Authenticate Yourself First.")
    connection.close()


if __name__ == "__main__":
    # print("reaching")
    # t1 = threading.Thread(target=initiate_socket_listener)
    # t1.daemon = True
    # t1.start()
    cli()

    log.info("Connection Closed")
