# Byte-at-a-time ECB decryption

import base64
import random
from time import sleep
from set1.challenge7 import aes_encrypt_ecb
from set2.challenge12 import find_block_size
from set2.challenge12 import randKey
from set2.challenge11 import detectMode

def randPrefix():
    key = bytearray()
    nb = random.randint(20, 35)
    for i in range(nb):
        key.append(random.randint(0, 255))
    return key

def encryption_oracle(msg):
    #random_prefix = randPrefix()
    msg = bytearray(random_prefix+msg+dontlook)
    encrypted = aes_encrypt_ecb(const_key, msg)
    return encrypted

def find_padding(oracle_function):
    msg = bytearray()
    ref = oracle_function(msg)
    len(ref)
    newref = ref
    while len(newref) == len(ref):
        msg = msg + b"e"
        newref = encryption_oracle(msg)
    return len(msg)-1

def bruteforce_singleByte(refBlock, quasiBlock, encryption_oracle, nbOfBlock):
    for singleByte in range(0, 256):
        block = quasiBlock + chr(singleByte).encode()
        encrypted = encryption_oracle(block)
        to_match = encrypted[(nbOfBlock_before)*block_size:(nbOfBlock_before+1+nbOfBlock)*block_size]
        if to_match == refBlock:
            print(block) # more fun like that
            return singleByte

def findNbOfBlock_before(len_align, oracle_function):
    encrypted1 = oracle_function(bytearray(b"a"*(len_align)))
    encrypted2 = oracle_function(bytearray(b"a"*(len_align+1)))
    for i, (x, y) in enumerate(zip(encrypted1, encrypted2)):
        if x != y:
            break
    nbOfBlock_before = int(i/16)
    return nbOfBlock_before

if __name__ == "__main__":
    const_key = randKey()
    random_prefix = randPrefix()
    with open("set2/12.txt") as f:
        b64_data = f.read()
    dontlook = base64.b64decode(b64_data)
    block_size = find_block_size(encryption_oracle)
    detectMode(encryption_oracle, block_size)

    len_pad = find_padding(encryption_oracle)
    #    random                      len_pad           len(dontlook)%16
    #| p p p p p p p p p p p p p p u u | u u u u u u x x x x x x x x x x |
    #                              ^ ^                                   ^
    #                            len_align                        block boundary
    len_align = len_pad + block_size # in case len_pad doesn't cross any block boundary
    len_align = len_align - (block_size-len(dontlook)%block_size)
    len_align = len_align%16 # delete eventual extra block

    nbOfBlock_before = findNbOfBlock_before(len_align, encryption_oracle)

    def findNbOfBlock(length_discovered):
        return int((length_discovered-length_discovered%16)/16)+1

    discovered = bytearray()
    while len(discovered) < len(dontlook):
        sleep(1)
        nbOfBlock = findNbOfBlock(len(discovered))-1
        msg_pad = bytearray(b"A"*len_align) # align to block boundary
        padBlock = bytearray(b"A"*((nbOfBlock+1)*block_size-1-len(discovered)))
        encrypted = encryption_oracle(msg_pad+padBlock)
        refBlock = encrypted[(nbOfBlock_before)*block_size:(nbOfBlock_before+1+nbOfBlock)*block_size]
        quasiBlock = msg_pad + padBlock + discovered
        byte_guessed = bruteforce_singleByte(refBlock, quasiBlock, encryption_oracle, nbOfBlock)
        byte_guessed
        discovered.append(byte_guessed)
    print(discovered.decode())
