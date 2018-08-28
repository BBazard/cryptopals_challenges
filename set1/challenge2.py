# Fixed XOR

import codecs
import operator

def fixed_xor(input1, input2):
    xored = [operator.xor(x1, x2) for x1, x2 in zip(input1, input2)]
    return bytearray(xored)

def fixed_xor_fast1(input1, input2):
    return bytearray([x1^x2 for x1, x2 in zip(input1, input2)])

def fixed_xor_fast2(input1, input2):
    mylist = []
    for x1, x2 in zip(input1, input2):
        mylist.append(x1^x2)
    return bytearray(mylist)

if __name__ == "__main__":
    input1 = bytearray.fromhex("1c0111001f010100061a024b53535009181c")
    input2 = bytearray.fromhex("686974207468652062756c6c277320657965")
    output = bytearray.fromhex("746865206b696420646f6e277420706c6179")
    print(output == fixed_xor(input1, input2))
    print(output == fixed_xor_fast1(input1, input2))
    print(output == fixed_xor_fast2(input1, input2))
