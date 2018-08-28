# Implement PKCS#7 padding

input = b"YELLOW SUBMARINE"
expected = b"YELLOW SUBMARINE\x04\x04\x04\x04"

def pkcs7padding(msg, length):
    excess = length - len(msg)
    if excess <= 0:
        return msg
    pad = bytearray()
    pad.extend([excess]*excess)
    return msg+pad

if __name__ == "__main__":
    print(pkcs7padding(input, 20) == expected)
