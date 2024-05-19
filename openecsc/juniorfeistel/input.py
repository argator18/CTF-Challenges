inputs = [0b0000, 0b0001, 0b0010, 0b0100,0b0111, 0b1000]
outputs = set()
for i in inputs:
    for j in inputs:
        outputs.add(i ^ j)
for out in outputs:
    print(bin(out)[2:].rjust(4,'0'))
