import base64
import struct

from set1.helpers import groupByBlocks
from set1.challenge2 import fixed_xor
from set1.challenge7 import aes_encrypt_block

def increment_counter(counter):
    for i in range(len(counter)):
        try:
            counter[i] += 1
        except ValueError:
            counter[i] = 0
        else:
            break
    return counter

def aes_encrypt_ctr(key, msg, nounce):
    assert len(key) == 16
    assert len(nounce) == 8

    # little endian stuff
    nounce = bytearray(reversed(nounce))
    counter = bytearray("".join(["\x00"]*8).encode())

    output = bytearray()
    for block in groupByBlocks(msg, 16):
        stream_key = nounce + counter
        encrypted_stream_key = aes_encrypt_block(key, stream_key)
        output.extend(fixed_xor(encrypted_stream_key, block))
        increment_counter(counter)
    return bytes(output)

def aes_decrypt_ctr(key, msg, nounce):
    return aes_encrypt_ctr(key, msg, nounce)

if __name__ == "__main__":
    b64_data = b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
    msg = base64.b64decode(b64_data)
    key = b"YELLOW SUBMARINE"
    nounce = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    decrypted = aes_decrypt_ctr(key, msg, nounce)
    print(decrypted.decode())
