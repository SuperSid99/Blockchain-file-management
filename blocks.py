import hashlib

class Block:
    def __init__(self, prvious_block_hash, encrypted_images):
        self.prvious_block_hash = prvious_block_hash
        self.encrypted_images = encrypted_images

        self.block_data = "-".join(encrypted_images) + "-" + prvious_block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()


def create_new_block(prvious_block_hash, encrypted_images):
    new_block = Block(prvious_block_hash, [encrypted_images])
    return new_block
