# CBC bitflipping attacks

from set2.challenge10 import aes_encrypt_cbc
from set2.challenge10 import aes_decrypt_cbc
from set2.challenge12 import randKey
from set2.challenge15 import unpad_validation
from set2.challenge15 import pkcs7pad
from set1.challenge2 import fixed_xor

const_key = randKey()
iv = randKey()

def kvParser_url(to_parse):
    args = to_parse.split(";")
    ansDict = {}
    for arg in args:
        k, v = arg.split("=")
        ansDict[k] = v
    return ansDict

def percent_encode(string):
    """
    doesn't handle non-ascii characters correctly
    """
    unreserved_set = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~"
    len(unreserved_set)

    safeString = bytearray()
    for c in string:
        if c in unreserved_set:
            safeString.append(c)
        else:
            hexString = hex(c)[2:].zfill(2)
            encoded = bytearray(b"%"+hexString.encode())
            safeString.extend(encoded)
    return safeString

def encryption_oracle(unsafeString):
    to_prepend = b"comment1=cooking%20MCs;userdata="
    to_append = b";comment2=%20like%20a%20pound%20of%20bacon"
    string = percent_encode(unsafeString)
    string = to_prepend + string + to_append
    string = pkcs7pad(string)
    encrypted = aes_encrypt_cbc(const_key, string, iv)
    return encrypted

def isAdmin(encrypted):
    string = aes_decrypt_cbc(const_key, encrypted, iv)
    string = unpad_validation(string)
    return (b";admin=true;" in string)

if __name__ == "__main__":
    plaintext_toscramble = b"yellow_submarineyellow_submarineyellow_submarine"
    encrypted = bytearray(encryption_oracle(plaintext_toscramble))
    a = fixed_xor(b"yellow_submarine", b"nawao;admin=true")
    encrypted[16*3:16*4] = fixed_xor(encrypted[16*3:16*4], a)
    print(isAdmin(encrypted))
