# Implement the MT19937 Mersenne Twister RNG

(w, n, m, r) = (32, 624, 397, 31)
a = 0x9908B0DF
f = 1812433253
(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7,  0x9D2C5680)
(t, c) = (15, 0xEFC60000)
l = 18
lower_mask = (1 << r) - 1 # 32 bits
upper_mask = (1 << r)

def MT_initialize(seed, index, mt):
    mt[0] = seed

    for i in range(1, n):
        mt[i] = (f * (mt[i-1] ^ (mt[i-1] >> 30)) + i)
        mt[i] = bin(mt[i])[2:][-w:]
        mt[i] = int(mt[i], 2)
    index = n
    return index, mt

def MT_twist(index, mt):
    for i in range(n):
        x = (mt[i] & upper_mask) + (mt[(i+1)%n] & lower_mask)
        xA = x >> 1
        if (x & 0x1):
            xA = xA^a
        mt[i] = mt[(i+m)%n] ^ xA
    index = 0
    return index, mt

# function used in challenge 23
def MT_temper(u32):
    y = u32
    y ^= (y >> u)
    y ^= (y << s) & b
    y ^= (y << t) & c
    y ^= (y >> l)
    y = bin(y)[2:][-w:]
    y = int(y, 2)
    return y

def MT_extractu32(index, mt):
    i = index
    if index >= n:
        index, mt = MT_twist(index, mt)
        i = index
    index = i+1
    return index, mt, MT_temper(mt[i])

if __name__ == "__main__":
    mt = [0]*n
    index = 0
    index, mt = MT_initialize(5489, index, mt)
    print(hex(MT_extractu32(index, mt)[-1]))
