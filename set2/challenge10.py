# Implement CBC mode

import base64

from set1.helpers import groupByBlocks
from set1.challenge2 import fixed_xor
from set1.challenge7 import aes_encrypt_block
from set1.challenge7 import aes_decrypt_block

from set2.challenge9 import pkcs7padding

def aes_encrypt_cbc(key, hex_data, iv):
    output = bytearray()
    if len(hex_data)%16 != 0:
        len_pad = 16 - len(hex_data)%16
        hex_data = pkcs7padding(hex_data, len(hex_data)+len_pad)
    chunks = groupByBlocks(hex_data, 16)
    decrypted_chunk = iv
    for chunk in chunks:
        xored = fixed_xor(chunk, decrypted_chunk)
        decrypted_chunk = aes_encrypt_block(key, xored)
        output.extend(decrypted_chunk)
    return bytes(output)

def aes_decrypt_cbc(key, hex_data, iv):
    output = bytearray()
    if len(hex_data)%16 != 0:
        len_pad = 16 - len(hex_data)%16
        hex_data = pkcs7padding(hex_data, len(hex_data)+len_pad)
    chunks = groupByBlocks(hex_data, 16)
    last_chunk = iv
    for chunk in chunks:
        decrypted_chunk = aes_decrypt_block(key, chunk)
        xored = fixed_xor(decrypted_chunk, last_chunk)
        last_chunk = chunk
        output.extend(xored)
    return output

if __name__ == "__main__":
    with open("set2/10.txt") as f:
        raw_data = f.read()
    hex_data = base64.b64decode("".join(raw_data))
    key = b"YELLOW SUBMARINE"
    iv = bytearray([0]*16)
    decrypted = aes_decrypt_cbc(key, aes_encrypt_cbc(key, aes_decrypt_cbc(key, hex_data, iv), iv), iv)
    print(decrypted.decode())
