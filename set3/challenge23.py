# Clone an MT19937 RNG from its output

(w, n, m, r) = (32, 624, 397, 31)
a = 0x9908B0DF
f = 1812433253
(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7,  0x9D2C5680)
(t, c) = (15, 0xEFC60000)
l = 18
lower_mask = (1 << r) - 1 # 32 bits
upper_mask = (1 << r)

from set3.challenge21 import MT_initialize
from set3.challenge21 import MT_extractu32
from set3.challenge21 import MT_temper

# Code adapted from https://github.com/misodengaku/mt_reverse/blob/master/mt_reverse/MersenneReverser.cs

TemperingMaskB = 0x9d2c5680
TemperingMaskC = 0xefc60000

def undoTemper(y):
	y = undoTemperShiftL(y)
	y = undoTemperShiftT(y)
	y = undoTemperShiftS(y)
	y = undoTemperShiftU(y)
	return y

def undoTemperShiftL(y):
	last14 = y >> 18
	final = y ^ last14
	return final

def undoTemperShiftT(y):
	first17 = y << 15
	final = y ^ (first17 & TemperingMaskC)
	return final

def undoTemperShiftS(y):
    # This one also sucked to figure out, but now I think i could write
    # a general one.  This basically waterfalls and keeps restoring original
    # bits then shifts the values down and xors again to restore more bits
    # and keeps on doing it.
	a = y << 7
	b = y ^ (a & TemperingMaskB)
	c = b << 7
	d = y ^ (c & TemperingMaskB) # now we have 14 of the original
	e = d << 7
	f = y ^ (e & TemperingMaskB) # now we have 21 of the original
	g = f << 7
	h = y ^ (g & TemperingMaskB) # now we have 28 of the original
	i = h << 7  # now we have the original xor
	final = y ^ (i & TemperingMaskB)
	return final

def undoTemperShiftU(y):
	# This was confusing to figure out.
	# We know the first 11 bits are un-altered becuase they were
	# xored with 0's.  We shift those 11 bits to the right and xor that with the
	# original which gives us the first 22 bits(b) of what it orginally was.  Now that we have the
	# first 22 bits so we can shift that to the right 11 bits which gives us
	# what the number was orginally xored with.  So then we just xor y with that and
	# our number is restored!
	a = y >> 11
	b = y ^ a
	c = b >> 11
	final = y ^ c
	return final

def MT_temper(u32):
    y = u32
    y ^= (y >> u)
    y ^= (y << s) & b
    y ^= (y << t) & c
    y ^= (y >> l)
    y = bin(y)[2:][-w:]
    y = int(y, 2)
    return y

if __name__ == "__main__":
    mt = [0]*n
    index = 0
    index, mt = MT_initialize(6234, index, mt)
    mt2 = [0]*n
    index2 = 0
    for i in range(624):
        index, mt, e = MT_extractu32(index, mt)
        mt2[i] = undoTemper(e)
	index2=index
	index2, mt2, output2 = MT_extractu32(index2, mt2)
	index, mt, output = MT_extractu32(index, mt)
	print(output, output2)
