# Create the MT19937 stream cipher and break it

from set1.challenge2 import fixed_xor
from set1.helpers import groupByBlocks
from set3.challenge21 import MT_initialize
from set3.challenge21 import MT_extractu32

def mt_encrypt(seed, msg):
    msg = groupByBlocks(msg, 8)
    new_msg = bytearray()
    mt = [0]*624
    index = 0
    index, mt = MT_initialize(seed, index, mt)
    for x, block in enumerate(msg):
        block = bytearray(block)
        index, mt, output = MT_extractu32(index, mt)
        index, mt, output2 = MT_extractu32(index, mt)
        output = bytearray.fromhex(hex(output)[2:].zfill(8))
        output2 = bytearray.fromhex(hex(output2)[2:].zfill(8))
        keystream = output + output2
        new_msg.extend(fixed_xor(block, keystream))
    return new_msg

if __name__ == "__main__":
    seed = 34
    mt_encrypt(seed, mt_encrypt(seed, b"faaaaaaaaaaaaaaf"))
