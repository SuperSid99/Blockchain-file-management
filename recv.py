import socket
import sys
import errno

IP = "100.81.249.49"
PORT = 4455
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 10240000000


def main():
    soc = socket(AF_INET, SOCK_STREAM)
    soc.connect(ADDR)
    print('connected to', ADDR)


if __name__ == "__main__":
    main()