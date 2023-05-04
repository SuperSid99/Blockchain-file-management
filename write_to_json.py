import json


def write_json(new_data, filename, key_name=None):
    with open(filename, "r+") as file:
        file_data = json.load(file)
        file_data[key_name].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

def get_image_data(hashcode):

    image = open('images.json', 'r+')

    x = image.read()
    y = json.loads(x)
    z = y["image_data"]
    
    count=0


# this function is to send the blockchain to the server

# print(z.values())

    for _ in z:
        if _[f'hashcode{count}'] == hashcode :
            return(_[f'image{count}'])
        count+=1
    
    return("no results found")

def get_file_type(hashcode):
    file=open("block_data.json","r+")
    x=file.read()
    y=json.loads(x)
    z=y["blockchain_data"]

    count=0

    for _ in z:
        if _[f"block{count}_hash"] == hashcode:
            return(_[f'block{count}_file_name'],_[f'block{count}_file_type'])
        count+=1
    
    return("no results found")


def get_blockchain():
    pass
