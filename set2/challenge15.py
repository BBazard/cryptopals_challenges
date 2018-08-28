# PKCS#7 padding validation

def unpad_validation(plaintext):
    if len(plaintext)%16 != 0:
            raise ValueError("plaintext provided is not correctly padded", plaintext)
    last_byte = plaintext[-1]
    len_pad = last_byte
    if len_pad > 16 or len_pad < 1:
            raise ValueError("plaintext provided is not correctly padded", plaintext)
    if len_pad == 1:
        if last_byte == ord(b"\x01"):
            return plaintext[:-1]
        else:
            raise ValueError("plaintext provided is not correctly padded", plaintext)
    padding_candidate = plaintext[-len_pad:]
    for byte in padding_candidate:
        if byte != last_byte:
            raise ValueError("plaintext provided is not correctly padded", plaintext)
    return plaintext[:-len_pad]

def pkcs7pad(plaintext):
    len_pad = 16 - len(plaintext)%16
    plaintext = plaintext + (chr(len_pad)*len_pad).encode()
    return plaintext

if __name__ == "__main__":
    pkcs7pad(b"yellow_submarine")
    unpad_validation(b"ICE ICE BABY\x04\x04\x04\x04")
    unpad_validation(b"ICE ICE BABY\x05\x05\x05\x04")
    unpad_validation(b"ICE ICE BABY\x01\x02\x03\x04")
    unpad_validation(b"yellow_submarine\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10")
    unpad_validation(b"yellow_submarine")
