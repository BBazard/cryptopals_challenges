# Break "random access read/write" AES CTR

import base64

from set3.challenge18 import aes_encrypt_ctr
from set3.challenge18 import aes_decrypt_ctr
from set3.challenge18 import increment_counter
from set2.challenge12 import randKey
from set1.challenge7 import aes_decrypt_ecb
from set1.challenge7 import aes_encrypt_block
from set1.challenge2 import fixed_xor

def edit(ciphertext, key, offset, newtext):
    fixed_nounce = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    nounce = bytearray(reversed(fixed_nounce))
    counter = bytearray("".join(["\x00"]*8).encode())
    output = bytearray()

    nbBlock, remaining = int((offset%16)/16), offset%16

    for i in range(nbBlock):
        stream_key = nounce + counter
        increment_counter(counter)
    if remaining != 0 or nbBlock == 0:
        stream_key = nounce + counter
        increment_counter(counter)

    encrypted_stream_key = aes_encrypt_block(key, stream_key)[remaining:]
    print(len(encrypted_stream_key)) # 16
    while len(newtext) > len(encrypted_stream_key):
        stream_key = nounce + counter
        increment_counter(counter)
        encrypted_stream_key.extend(aes_encrypt_block(key, stream_key))
    # Read part
    # with "to_read" the number of bytes to read
    #original_plaintext = fixed_xor(encrypted_stream_key[:len(to_read)], ciphertext[offset:])
    #return original_plaintext
    ciphertext = bytearray(ciphertext)
    ciphertext[offset:offset+len(newtext)] = fixed_xor(encrypted_stream_key, newtext)
    return ciphertext

if __name__ == "__main__":
    with open("set4/25.txt") as f:
        b64_data = f.read()
    msg = base64.b64decode(b64_data)
    key = b"YELLOW SUBMARINE"
    decrypted = aes_decrypt_ecb(key, msg)
    const_key = randKey()
    fixed_nounce = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    encrypted = aes_encrypt_ctr(const_key, decrypted, fixed_nounce)
    len(encrypted)
    attacker_encrypted = edit(encrypted, const_key, 0, b"\x00"*len(encrypted))
    guessed_stream_key = attacker_encrypted
    decrypted = fixed_xor(encrypted, guessed_stream_key)
    print(decrypted.decode())
