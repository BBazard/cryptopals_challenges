# CTR bitflipping

from set3.challenge18 import aes_encrypt_ctr
from set3.challenge18 import aes_decrypt_ctr
from set2.challenge12 import randKey
from set2.challenge15 import unpad_validation
from set2.challenge15 import pkcs7pad
from set1.challenge2 import fixed_xor
from set2.challenge16 import percent_encode

const_key = randKey()
nounce = b"\x00\x00\x00\x00\x00\x00\x00\x00"

def encryption_oracle(unsafeString):
    to_prepend = b"comment1=cooking%20MCs;userdata="
    to_append = b";comment2=%20like%20a%20pound%20of%20bacon"
    string = percent_encode(unsafeString)
    string = to_prepend + string + to_append
    string = pkcs7pad(string)
    encrypted = aes_encrypt_ctr(const_key, string, nounce)
    return encrypted

def isAdmin(encrypted):
    string = aes_decrypt_ctr(const_key, encrypted, nounce)
    string = unpad_validation(string)
    return (b";admin=true;" in string)

if __name__ == "__main__":
    plaintext_toscramble = b"I liketrainsaryellow_submarine"
    encrypted = bytearray(encryption_oracle(plaintext_toscramble))
    a = fixed_xor(b"yellow_submarine", b"egood;admin=true")
    encrypted[16*3:16*4] = fixed_xor(encrypted[16*3:16*4], a)
    print(isAdmin(encrypted))
