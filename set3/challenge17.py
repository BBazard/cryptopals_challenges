import random
import base64

from set2.challenge10 import aes_encrypt_cbc
from set2.challenge10 import aes_decrypt_cbc
from set2.challenge12 import randKey
from set2.challenge15 import unpad_validation
from set2.challenge15 import pkcs7pad

const_key = randKey()
with open("set3/17.txt") as f:
    b64_data_set = f.read()

def encryption_oracle(iv):
    raw_bytes = base64.b64decode(b64_data_set.split("\n")[random.randint(0, 9)])
    padded = pkcs7pad(raw_bytes)
    encrypted = aes_encrypt_cbc(const_key, padded, iv)
    return encrypted

def isPaddingGood(encrypted, iv):
    plaintext = aes_decrypt_cbc(const_key, encrypted, iv)
    try:
        unpad_validation(plaintext)
    except ValueError:
        return False
    return True

if __name__ == "__main__":
    iv = randKey()

    encrypted = bytearray(encryption_oracle(iv))
    nbOfBlocks = int(len(encrypted)/16)

    discovered_total = []
    nb = len(encrypted)-len(iv) # len(encrypted) will change inside the loop
    while len(discovered_total) < nb:
        discovered = []
        while len(discovered)<16:
            mask_len = len(discovered)+1 # number of byte we will modify in the ciphertext
            for x in range(0, 256):
                new_encrypted = encrypted.copy()
                for i in range(mask_len-1):
                    new_encrypted[-i-1-16] = encrypted[-i-1-16]^discovered[i]^mask_len
                new_encrypted[-mask_len-16] = encrypted[-mask_len-16]^x
                if isPaddingGood(new_encrypted, iv) and not (x == 0 and len(discovered) == 0):
                    discovered.append(x^mask_len)
        discovered_total.extend(discovered)
        encrypted = encrypted[:-16]

    # only the first block is remaining to be decrypted
    # need to do the same thing with the iv instead of the preceding ciphertext
    discovered = []
    while len(discovered)<16:
        mask_len = len(discovered)+1 # number of byte we will modify in the ciphertext
        for x in range(0, 256):
            new_iv = iv.copy()
            for i in range(mask_len-1):
                new_iv[-i-1] = iv[-i-1]^discovered[i]^mask_len
            new_iv[-mask_len] = iv[-mask_len]^x
            if isPaddingGood(encrypted, new_iv) and not (x == 0 and len(discovered) == 0):
                discovered.append(x^mask_len)
    discovered_total.extend(discovered)

    decrypted_plaintext = bytearray(reversed(discovered_total))
    print(decrypted_plaintext.decode())
