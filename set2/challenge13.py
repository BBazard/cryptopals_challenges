# EDB cut-and-paste

from set1.challenge7 import aes_encrypt_ecb
from set1.challenge7 import aes_decrypt_ecb
from set2.challenge11 import randKey

const_key = randKey()

def kvParser(to_parse):
    args = to_parse.split("&")
    ansDict = {}
    for arg in args:
        k, v = arg.split("=")
        ansDict[k] = v
    return ansDict

def kvEncoder(dict_to_encode):
    ansString = []
    for k, v in dict_to_encode.items():
        ansString.append(str(k+"="+v+"&"))
    return "".join(ansString).rstrip("&")

def profile_for(mailStringUnsafe):
    mailStringSafe = mailStringUnsafe.split("&")[0]
    ansDict = {}
    ansDict["email"] = mailStringSafe
    ansDict["uid"] = str(10)
    ansDict["role"] = "user"
    return kvEncoder(ansDict)

def encrypt_profile(encoded_profile):
    return aes_encrypt_ecb(const_key, encoded_profile)

def decryptParse(encrypted_profile):
    ansDict = kvParser(aes_decrypt_ecb(const_key, encrypted_profile).decode())
    ansDict["role"] = ansDict["role"].rstrip("\x00")
    return ansDict

def fiddleWith(a):
    return a

def regroup(to_regroup):
    ans = bytearray()
    for group in to_regroup:
        ans.extend(group)
    return ans

def ask_a_block(plaintext_block, padding_until_block):
    assert len(plaintext_block == 16)
    assert len(padding_until_block < 16)
    inputString = padding_until_block + plaintext_block
    profile = profile_for(inputString).encode()
    encrypted_profile = encrypt_profile(profile)
    block_asked = encrypted_profile[16:32]
    return block_asked

if __name__ == "__main__":
    padding_until_block = "aaaaaaaaaa" # align to blocksize
    block_to_ask = "admin" + "\x00"*(16-len("admin")) # is exactly the second block
    inputString = padding_until_block + block_to_ask
    profile = profile_for(inputString).encode()
    encrypted_profile = encrypt_profile(profile)
    block_asked = encrypted_profile[16:32]

    padding_after_equal = "aaaaaaaaaaaaa" # put the equal just before the last block
    padding_after_equal = "example+thissiforme@gmail.com" # for fun something believable
    assert len(padding_after_equal)%16 == 13
    inputString = padding_after_equal
    profile = profile_for(inputString).encode()
    encrypted_profile = encrypt_profile(profile)

    # replace last block "user" by "admin"
    encrypted_profile = encrypted_profile[:-16] + block_asked

    decrypted = decryptParse(encrypted_profile)
    print(kvEncoder(decrypted))
    decrypted["role"]
