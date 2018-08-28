# implement repeating-key XOR

import operator
import codecs
import numpy as np

from set1.challenge2 import fixed_xor

def repeatKey(key, length):
    key_pad = bytearray()
    index = 0;
    while len(key_pad) < length:
        key_pad = key_pad + key
    excess = len(key_pad) - length
    if excess > 0:
        key_pad = key_pad[:-excess]
    return key_pad

def repeatedKeyXor(msg_hexString, key_hexString):
    repeatedKey = repeatKey(key_hexString, len(msg_hexString))
    return fixed_xor(msg_hexString, repeatedKey)

if __name__ == "__main__":
    msg = bytearray(b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal")
    key = bytearray(b"ICE")
    expected = bytearray.fromhex('0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f')
    print(repeatedKeyXor(msg, key) == expected)
