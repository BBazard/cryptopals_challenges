# Break a SHA-1 keyed MAC using length extension

from set1.helpers import groupByBlocks
from set4.challenge28 import sha1
from set4.challenge28 import sha1_mac
from set4.challenge28 import sha1_pad_message

if __name__ == "__main__":
    original_plaintext = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    key = b"yellow_submarine"
    original_mac = sha1_mac(key, original_plaintext)

    for guessed_len_key in range(1, 40):
        sha1registers = [int(bytearray(x), 16) for x in groupByBlocks(original_mac, 8)]
        sha1padded_plaintext = sha1_pad_message(b"A"*guessed_len_key+original_plaintext)
        offset = len(sha1padded_plaintext)

        forged_message = sha1padded_plaintext+b";admin=true"
        forged_digest = sha1(forged_message, registers=sha1registers, offset=offset)

        forged_message_withoutkey = forged_message[guessed_len_key:]

        forged_mac = sha1_mac(key, forged_message_withoutkey)

        if forged_digest == forged_mac:
            print("len_key", guessed_len_key, "\nforged_message", forged_message_withoutkey, "\nforged_digest:", forged_digest, "\nforged_mac",  forged_mac)
            break
