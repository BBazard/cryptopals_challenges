# Break fixed-nonce CTR mode using substitutions

import base64

from set3.challenge18 import aes_encrypt_ctr
from set3.challenge18 import aes_decrypt_ctr
from set2.challenge12 import randKey
from set1.challenge3 import decryptSingleByteXor
from set1.challenge2 import fixed_xor

if __name__ == "__main__":
    const_key = randKey()
    fixed_nounce = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    with open("set3/19.txt") as f:
        b64_data_set = f.read()
    lines = [base64.b64decode(x) for x in b64_data_set.split("\n")[:-1]]

    encrypted_lines = []
    for line in lines:
        encrypted_lines.append(aes_encrypt_ctr(const_key, line, fixed_nounce))

    max_len = max([len(x) for x in encrypted_lines])
    keystream = bytearray()
    for i in range(max_len):
        ith_block = bytearray([x[i] for x in encrypted_lines if len(x) > i])
        score, key, decrypted = decryptSingleByteXor(ith_block)
        keystream.append(key[0])

    sorted(lines, key=len)

    for line, encrypted_line in zip(sorted(lines, key=len), sorted(encrypted_lines, key=len)):
        print("expected", line.decode())
        print("found   ", fixed_xor(encrypted_line, keystream).decode())
        print("\n")
