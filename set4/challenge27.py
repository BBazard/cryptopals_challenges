# Recover the key from CBC with IV=key

from set2.challenge10 import aes_encrypt_cbc
from set2.challenge10 import aes_decrypt_cbc
from set2.challenge12 import randKey
from set2.challenge15 import unpad_validation
from set2.challenge15 import pkcs7pad
from set1.challenge2 import fixed_xor

const_key = randKey()
iv = const_key

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
    to_append = b";comment2=pound"
    string = percent_encode(unsafeString)
    string = to_prepend + string + to_append
    string = pkcs7pad(string)
    encrypted = aes_encrypt_cbc(const_key, string, iv)
    return encrypted

def isAdmin(encrypted):
    ascii_comply = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~%,;:!?=+)([]{})"
    string = aes_decrypt_cbc(const_key, encrypted, iv)
    safeString = bytearray()
    string = unpad_validation(string)
    for c in string:
        if c not in ascii_comply:
            print("ERROR, plaintext: ", string)
            return False
    return (b";admin=true;" in string)

if __name__ == "__main__":
    plaintext_toscramble = b"yy8888888888888888888888888"
    encrypted = bytearray(encryption_oracle(plaintext_toscramble))

    string = aes_decrypt_cbc(const_key, encrypted, iv) #
    string = unpad_validation(string) #

    encrypted[16*1:16*2] = bytearray(b"\x00")*16

    encrypted[16*2:16*3] = encrypted[16*0:16*1]

    isAdmin(encrypted) # print Error

    gotFromError = bytearray(b'comment1=cookingj\r:\x81\xfd\xe4\xdf\xb2\x8f\x93w\xba\x95\\b\x83\xd1\xc9J\xc9I\xbc_ka\xb3e\xfb\xdc\x0ea[\xa3\xfd\x1fgTeQ\xbe\x02\xa7wF"*\xe1\xa9ent2=pound')
    supposedly_key = fixed_xor(gotFromError[0:16], gotFromError[32:48])

    print(supposedly_key == iv)
    print(supposedly_key == const_key)

    # Proof p1^p3 = key ?
    #
    # From CBC we know that
    # A(p1^iv)=C1
    # A(p3^C2)=C3
    # A(C1)^iv = p1
    # p3 = A(C3)^C2
    #
    # Then we deduce
    # p1^p3 = A(C3)^C2^A(C1)^iv
    #
    # Or we made it so that C3=C1 and C2=0 and we know that iv = key
    # p1^p3 = A(C1)^0^A(C1)^key
    #
    # 0^x = x and x^x = 0 so finally we have
    ###############
    # p1^p3 = key #
    ###############
