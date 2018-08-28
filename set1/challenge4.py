# Detect single-character XOR

import operator
import codecs
import numpy as np

from set1.challenge3 import decryptSingleByteXor

if __name__ == "__main__":
    with open("set1/4.txt") as f:
        data = f.read()
    answer = []
    for line in data.split("\n"):
        msg = bytearray.fromhex(line)
        decrypted = decryptSingleByteXor(msg)
        answer.append(decrypted[0])
    score, key, decrypted = zip(*sorted(answer, reverse=True))
    print(decrypted[0].decode())
