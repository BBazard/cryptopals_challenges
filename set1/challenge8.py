# Detect AES in ECB mode

from set1.challenge6 import groupByBlocks

if __name__ == "__main__":
    with open("set1/8.txt") as f:
        raw_bytes = f.read()
    raw_bytes = raw_bytes.rstrip("\n")

    answer = []
    for i, sample in enumerate(raw_bytes.split("\n")):
        sample1 = bytearray.fromhex(sample)
        chunks = [bytearray(x) for x in groupByBlocks(sample1, 16)]
        chunks = sorted(chunks)

        last = ""
        for x in chunks:
            if x == last:
                answer.append(i)
            last = x
    answer = sorted(set(answer))
    print(answer)
