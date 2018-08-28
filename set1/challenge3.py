# Single-byte XOR cipher

import operator
import codecs
import numpy as np

from set1.challenge2 import fixed_xor

def singleByteXor(msg, key):
    key_repeated = bytearray([key]*len(msg))
    message_candidate = fixed_xor(key_repeated, msg)
    return bytearray(message_candidate)

def score(raw_bytes):
    score = 0
    for byte in raw_bytes:
        if byte in bytearray(b"etaoin shrdlu ETAOIN SHRDLU"):
            score = score + 1
        if byte not in bytearray(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',:;\"."):
            score = score - 1
    return score

def decryptSingleByteXor(encrypted_msg):
    encrypted_msg = bytearray(encrypted_msg)
    singleByteKey_list = bytearray(list(range(256)))
    answer = []
    for key_tried in singleByteKey_list:
        decrypted = singleByteXor(encrypted_msg, key_tried)
        myscore = score(decrypted)
        answer.append(tuple([myscore, key_tried, decrypted]))
    zipped = list(sorted(answer, reverse=True))
    return zip(*zipped) # score, key, decrypted


if __name__ == "__main__":
    input = bytearray.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
    score, key, decrypted = decryptSingleByteXor(input)
    print(decrypted[0].decode())
