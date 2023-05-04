import socket
client_ips=[] #format[(,0),(,1)]
client_ports=[] 
FORMAT = "utf-8"
SIZE = 10240000000
from ..image import give_encyripted_image , get_key
from ..write_to_json import get_blockchain

def request_chain_from_client():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    for _ in client_ips:
        addr=(_[0],client_ports[_[1]])
        client.connect(addr)
# code to trigger sending of block chain to server from cliennt to go here
# 
# 
# 
#         


def send_chain_to_server():
    
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Connecting to the server. """
    client.connect(ADDR)

    chain = get_blockchain
# send the blockchain in chunks
# 
# 

def verify_chain(client_chain,server_chain):
    if client_chain==server_chain:
        return (True)



if __name__=="__main__":
    pass