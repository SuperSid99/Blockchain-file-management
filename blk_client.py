from blocks import create_new_block
from write_to_json import write_json
import json
import time


def execute_process(en_image):
    hash = open('hashes.json', 'r+')

    x = hash.read()
    y = json.loads(x)
    z = y["hash_data"]

    hash_value = list(z[-1].values())[-1]

    '''commenting the code as we are now operating this in main server'''
    '''To be uncommented for main server and commented for remaining ones'''

    # sttime=time.time()
    # print(f"encryption started at {sttime}\n")
    #
    # en_image = give_encyripted_image(image_path,key)
    #
    # endtime=time.time()
    # print(f"encryption ended at {endtime}\n")
    # print(f"total time taken to encrypt = {endtime-sttime}\n")

    new_block = create_new_block(hash_value, en_image)
    new_hash = new_block.block_hash

    hash_data = {
        f"hashcode{len(z)}": new_hash
    }
    block_data = {
        f"block{len(z)}_hash": new_hash,
        f"block{len(z) - 1}_hash": hash_value
    }
    image_data = {
        f"hashcode{len(z)}": new_hash,
        f"image{len(z)}": en_image
    }

    write_json(hash_data, 'hashes.json', "hash_data")
    write_json(block_data, 'block_data.json', "blockchain_data")
    write_json(image_data, 'images.json', "image_data")

    print("\nNEW BLOCK ADDED!!!!")
    print(new_hash)
