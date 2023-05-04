import socket
import sys
import errno

#ip address of the main server
IP = "100.81.249.49"
PORT = 4455
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 10240000000
import time
from image import give_encyripted_image, get_key


def chunks(lst, n):
    "Yield successive n-sized chunks from lst"
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():
    """ Staring a TCP socket. """
    f = []
    import os
    from os import listdir

    # get the path or directory
    folder_dir = ""
    for images in os.listdir(folder_dir):

        # check if the image end swith png or jpg or jpeg
        if (images.endswith(".png") or images.endswith(".jpg")
                or images.endswith(".jpeg")):
            # display
            f.append(images)
            print(images)
    print("Available Files Are::")
    print(f)

    for image in f:
        print(f"Sending Image {image}")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        """ Connecting to the server. """
        client.connect(ADDR)
        key = get_key()

        # client.send(image.encode(FORMAT))

        en_image = give_encyripted_image(f"path to folder/{image}", key)
        i = 0
        print("Sending data in Chunks")
        for chunk in chunks(en_image, 100):
            print(f"Sending chunk {i}")
            client.send(chunk.encode(FORMAT))
            i += 1

        print("All Data sent")

        client.close()

        time.sleep(2)


if __name__ == "__main__":
    main()
