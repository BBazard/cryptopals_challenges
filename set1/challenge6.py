# Break repeating-key XOR

import codecs
import base64
import numpy as np

from set1.helpers import groupByBlocks
from set1.challenge3 import decryptSingleByteXor
from set1.challenge5 import repeatedKeyXor

def hamming_distance(input1, input2):
    sum = 0
    for x, y in zip(input1, input2):
        a = bin(x)[2:].zfill(8)
        b = bin(y)[2:].zfill(8)
        for i, j in zip(a, b):
            if i != j:
                sum = sum + 1
    return sum

def guess_keysize(raw_bytes):
    keysize_list_with_dist = []
    for keysize in range(2, 41):

        chunks = groupByBlocks(raw_bytes, keysize)

        if len(chunks) > 100:
            indexes = np.random.choice(range(len(chunks)), 100, replace=False)
        else:
            indexes = range(len(chunks))

        combinations = np.array(np.meshgrid(indexes, indexes)).T.reshape(-1, 2)
        np.random.shuffle(combinations) # inplace
        combinations = combinations[:20]

        dist_list = []
        for x1, x2 in combinations:
            if x1 != x2:
                dist = hamming_distance(chunks[x1], chunks[x2])
                normalized_dist = dist/keysize
                dist_list.append(normalized_dist)
        average_dist = np.average(dist_list)
        keysize_list_with_dist.append(tuple([average_dist, keysize]))
    keysize_list_with_dist = list(sorted(keysize_list_with_dist))
    keysize_list = [x[1] for x in keysize_list_with_dist]
    top_keysize = keysize_list[0]
    return top_keysize

def guess_subkeys(to_xor_list):
    key_set = []
    for msg in to_xor_list:
        score, key, decrypted = decryptSingleByteXor(msg)
        top_key = key[0]
        key_set.append(top_key)
    return key_set

if __name__ == "__main__":
    assert hamming_distance(b"this is a test", b"wokka wokka!!!") == 37

    with open("set1/6.txt") as f:
        b64_data = f.read()
    raw_bytes = bytearray(base64.b64decode(b64_data))

    keysize = guess_keysize(raw_bytes)
    # From the keysize n create n block that can be xor decrypted
    result = groupByBlocks(raw_bytes, keysize)
    # the last block is not necessarily of size keysize so is discarded
    result = result[:-1]
    to_xor_list = list(zip(*result))
    assert len(to_xor_list) == keysize

    # For each block
    # try to guess the key that leads to the best character distribution
    key_set = guess_subkeys(to_xor_list)
    assert len(key_set) == keysize

    # The key of repeated xor is assembled for the keys of single byte xor
    key = bytearray(key_set)
    print("Found key")
    print(key.decode())

    decrypted = repeatedKeyXor(raw_bytes, key)
    print(decrypted.decode())
