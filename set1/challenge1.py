# Convert hex to base64

import base64
import codecs
from set1.helpers import groupByBlocks

dec2b64 = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

def toBase64(raw_bytes):
    raw_bytes = bytearray(raw_bytes)
    pad_len = 0
    while (len(raw_bytes) + pad_len)%3 != 0:
        pad_len = pad_len + 1
    raw_bytes.extend([0]*pad_len)
    triplets = groupByBlocks(raw_bytes, 3)
    new = []
    for triplet in triplets:
        hex1, hex2, hex3 = triplet

        b1 = (hex1 & 0b11111100) >> 2
        b2 = (hex1 & 0b00000011)
        b3 = (hex2 & 0b11110000) >> 4
        b4 = (hex2 & 0b00001111)
        b5 = (hex3 & 0b11000000) >> 6
        b6 = (hex3 & 0b00111111)

        c1 = b1
        c2 = (b2 << 4) ^ b3
        c3 = (b4 << 2) ^ b5
        c4 = b6

        d1 = dec2b64[c1]
        d2 = dec2b64[c2]
        d3 = dec2b64[c3]
        d4 = dec2b64[c4]

        new.extend([d1, d2, d3, d4])
    # padding
    if pad_len != 0:
        new[-pad_len:] = ["="]*pad_len
    return bytearray(new)

if __name__ == "__main__":
    output = bytearray(b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t")
    input1 = bytearray.fromhex("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d")

    # Version 1
    print(output == codecs.encode(input1, "base64")[:-1])
    # Version 2
    print(output == toBase64(input1))
