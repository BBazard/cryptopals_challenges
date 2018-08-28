# An ECB/CBC detection oracle

import random
import numpy as np

from set1.helpers import groupByBlocks
from set1.challenge6 import hamming_distance
from set1.challenge7 import aes_encrypt_ecb
from set2.challenge10 import aes_encrypt_cbc

def randKey():
    key = bytearray()
    for i in range(16):
        key.append(random.randint(0, 255))
    return key

def encryption_oracle(msg):
    key = randKey()
    iv = randKey()
    pad_before = bytearray([0]*random.randint(5, 10))
    pad_after = bytearray([0]*random.randint(5, 10))
    msg = bytearray(pad_before + msg + pad_after)
    choice = random.randint(0, 1)
    if choice == 1:
        print("ecb choosen")
        encrypted = aes_encrypt_ecb(key, msg)
    else:
        print("cbc choosen")
        encrypted = aes_encrypt_cbc(key, msg, iv)
    return encrypted

def avgDst(raw_bytes, block_size):
    chunks = groupByBlocks(raw_bytes, block_size)
    indexes = range(len(chunks))
    combinations = np.array(np.meshgrid(indexes, indexes)).T.reshape(-1, 2)
    np.random.shuffle(combinations) # inplace
    combinations = combinations[:100]
    dist_list = []
    for x1, x2 in combinations:
        if x1 != x2:
            dist = hamming_distance(chunks[x1], chunks[x2])
            normalized_dist = dist/block_size
            dist_list.append(normalized_dist)
    average_dist = np.average(dist_list)
    return average_dist

def detectMode(oracle_function, block_size):
    m = bytearray([0]*1000)
    msg = oracle_function(m)
    avg = avgDst(msg, block_size)
    if avg > 3:
        print("cbc predicted")
    else:
        print("ecb predicted")
    print("\n")

if __name__ == "__main__":
    for i in range(10):
        detectMode(encryption_oracle, 16)
