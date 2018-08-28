# Byte-at-a-time ECB decryption (Simple)

import base64
import random
from time import sleep
from set2.challenge11 import randKey
from set2.challenge11 import detectMode
from set1.challenge7 import aes_encrypt_ecb

def encryption_oracle(msg):
    msg = bytearray(msg+dontlook)
    encrypted = aes_encrypt_ecb(const_key, msg)
    return encrypted

def find_block_size(oracle_function):
    ref = len(oracle_function(bytearray()))
    for i in range(1, 256):
        pad = bytearray(b"A"*i)
        to_check = len(oracle_function(pad))
        if to_check != ref:
            block_size = to_check - ref
            return block_size

def bruteforce_singleByte(refBlock, quasiBlock, encryption_oracle):
    for singleByte in range(256):
        block = quasiBlock + chr(singleByte).encode()
        to_match = encryption_oracle(block)[:len(block)]
        if to_match == refBlock:
            print(block) # more fun like that
            return singleByte

if __name__ == "__main__":
    const_key = randKey()
    with open("set2/12.txt") as f:
        b64_data = f.read()
    dontlook = base64.b64decode(b64_data)

    # step 1 : find block_size
    block_size = find_block_size(encryption_oracle)

    # step 2
    detectMode(encryption_oracle, block_size)
    # the remaining steps

    def findNbOfBlock(length_discovered):
        return int((length_discovered-length_discovered%16)/16)+1

    discovered = bytearray()
    while len(discovered) < len(dontlook):
        sleep(1) # poor cpu
        nbOfBlock = findNbOfBlock(len(discovered))
        padBlock = bytearray(b"A"*(nbOfBlock*block_size-1-len(discovered)))
        refBlock = encryption_oracle(padBlock)[:nbOfBlock*block_size]
        quasiBlock = padBlock + discovered
        byte_guessed = bruteforce_singleByte(refBlock, quasiBlock, encryption_oracle)
        discovered.append(byte_guessed)
    print(discovered.decode())
