# general function

def binFromHex(s):
    """
    binFromHex("1f") # '00011111'
    binFromHex("333") # '0000001100110011'
    """
    not_padded = bin(int(s, 16))[2:]
    len_pad = 8 - len(not_padded)%8
    padded = "0"*len_pad + not_padded
    return padded


def binary2hex(input, padding = True):
    """
    binary2hex("011101") # "1d"
    binary2hex("000000000100011101") # "011d"
    """
    not_padded = hex(int(input, 2))[2:].zfill(2)
    if len(not_padded) %2 == 1: # padding
        padded = "0"+not_padded
    else:
        padded = not_padded
    if padding:
        return padded
    else:
        return not_padded


def groupByBlocks(to_group, group_size):
    """
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    groupByBlocks(a, 4)
    [(1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15)]
    """
    result = []
    subresult = []
    for i, elt in enumerate(to_group):
        if i%group_size == 0 and i != 0:
            result.append(tuple(subresult))
            subresult = []
        subresult.append(elt)
    lastTuple = tuple(subresult)
    result.append(lastTuple)
    return result
