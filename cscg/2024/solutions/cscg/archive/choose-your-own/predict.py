vals = [1804289383,
846930886,
1681692777,
1714636915,
1957747793,
424238335,
719885386,
1649760492,
596516649,
1189641421,
1025202362,
1350490027,
783368690,
1102520059,
2044897763,
1967513926,
1365180540,
1540383426,
304089172,
1303455736,
35005211,
521595368,
294702567,
1726956429,
336465782,
861021530,
278722862,
233665123,
2145174067,
468703135,
1101513929,
1801979802,
1315634022,
635723058,
1369133069,
1125898167,
1059961393
]
def getnext(i):
    #int(input())
    print(vals[i])
    return vals[i]






length = int((0xa0 - 0x24) /4 -1 )
offset = int((0x30 - 0x24) /4)
state = [0] * (length+1)

for i in range(length+1):
    print(i, length)
    state[(i+offset)%(length+1)] = getnext(i)
    input()

for i in range(length+1):
    print(hex(state[i]<<1))
cur = 0

def predict():
    global cur
    print(hex(state[cur]<<1),hex(state[cur+offset]<<1))
    pred = ((state[cur]<<1) + (state[cur+offset]<<1)) % 0x100000000
    state[(cur + offset)%(length + 1)] = pred>>1
    cur += 1
    print(pred>>1)

while True:
    input()
    predict()
