from blocks import create_new_block
from image import give_encyripted_image
from image import get_key
from write_to_json import write_json
import json
import logging
import time

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('')


def execute_process(en_image,file_name,file_type):
    hash = open('hashes.json', 'r+')

    x = hash.read()
    y = json.loads(x)
    z = y["hash_data"]

    key = get_key()

    hash_value = list(z[-1].values())[-1]

    '''Here  a New Block is created with data as previous_hash + en_image '''
    log.info("Creating New Block")
    new_block = create_new_block(hash_value, en_image)
    new_hash = new_block.block_hash

    log.info("Successfully Created New Block")
    hash_data = {
        f"hashcode{len(z)}": new_hash
    }
    block_data = {
        f"block{len(z)}_file_name":file_name,
        f"block{len(z)}_file_type":file_type,
        f"block{len(z)}_hash": new_hash,
        f"block{len(z) - 1}_hash": hash_value
    }
    image_data = {
        f"hashcode{len(z)}": new_hash,
        f"image{len(z)}": en_image
    }

    log.info("Saving Block Data")
    write_json(hash_data, 'hashes.json', "hash_data")
    write_json(block_data, 'block_data.json', "blockchain_data")
    write_json(image_data, 'images.json', "image_data")

    print(new_hash)

    return {
        "previous_hash": hash_value,
        "new_hash": new_hash,
        "en_image": en_image
    }


def execute_node_process(data):
    hash = open('hashes.json', 'r+')
    data = json.loads(data)
    x = hash.read()
    y = json.loads(x)
    z = y["hash_data"]

    previous_hash = data['previous_hash']
    new_hash = data['new_hash']
    en_image = data['en_image']

    log.info("Saving Block Data in Node")

    hash_data = {
        f"hashcode{len(z)}": new_hash
    }
    block_data = {
        f"block{len(z)}_hash": new_hash,
        f"block{len(z) - 1}_hash": previous_hash
    }
    image_data = {
        f"hashcode{len(z)}": new_hash,
        f"image{len(z)}": en_image
    }

    write_json(hash_data, 'hashes.json', "hash_data")
    write_json(block_data, 'block_data.json', "blockchain_data")
    write_json(image_data, 'images.json', "image_data")

    log.info("New Block Added To Node")
    log.info(new_hash)


def execute_camera_module_process(im_path, key):
    en_camera_image = give_encyripted_image(im_path, key)
    return en_camera_image

