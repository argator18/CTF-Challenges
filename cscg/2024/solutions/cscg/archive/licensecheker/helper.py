import sys
chars = [chr(i) for i in range(48, 58)] + [chr(i) for i in range(65, 91)]  # 0-9, A-Z
def _not(n, b=4):
    return 0x100 ** b -1 - n

def ror(value, rotations, width=32):
    rotations %= width  # Ensure rotations are within the width to avoid redundant rotations
    return ((value >> rotations) | (value << (width - rotations))) & ((1 << width) - 1)

def rol(value, shift, bits=32):
    shift %= bits  # Ensure shift is within the bit width
    return ((value << shift) & (2**bits - 1)) | (value >> (bits - shift))



def get_fix1(rdx):
     fix = [0x07, 0x0c,	0x11, 0x16,
            0x07, 0x0c,	0x11, 0x16,
            0x07, 0x0c,	0x11, 0x16,
            0x07, 0x0c,	0x11, 0x16,
            0x05, 0x09, 0x0e, 0x14,
            0x05, 0x09,	0x0e, 0x14,
           	0x05, 0x09,	0x0e, 0x14,
           	0x05, 0x09,	0x0e, 0x14,
           	0x04, 0x0b,	0x10, 0x17,
           	0x04, 0x0b,	0x10, 0x17,
           	0x04, 0x0b,	0x10, 0x17,
           	0x04, 0x0b,	0x10, 0x17,
           	0x06, 0x0a,	0x0f, 0x15,
           	0x06, 0x0a,	0x0f, 0x15,
           	0x06, 0x0a,	0x0f, 0x15,
           	0x06, 0x0a,	0x0f, 0x15]
     return fix[rdx]

def get_fix2(rdx):
    fix = [ 0xd76aa478,	0xe8c7b756,	0x242070db,	0xc1bdceee,
            0xf57c0faf,	0x4787c62a,	0xa8304613,	0xfd469501,
            0x698098d8,	0x8b44f7af,	0xffff5bb1,	0x895cd7be,
            0x6b901122,	0xfd987193,	0xa679438e,	0x49b40821,
            0xf61e2562,	0xc040b340,	0x265e5a51,	0xe9b6c7aa,
            0xd62f105d,	0x2441453 , 0xd8a1e681,	0xe7d3fbc8,
            0x21e1cde6,	0xc33707d6,	0xf4d50d87,	0x455a14ed,
            0xa9e3e905,	0xfcefa3f8,	0x676f02d9,	0x8d2a4c8a,
            0xfffa3942,	0x8771f681,	0x6d9d6122,	0xfde5380c,
            0xa4beea44,	0x4bdecfa9,	0xf6bb4b60,	0xbebfbc70,
            0x289b7ec6,	0xeaa127fa,	0xd4ef3085,	0x4881d05,
            0xd9d4d039,	0xe6db99e5,	0x1fa27cf8,	0xc4ac5665,
            0xf4292244,	0x432aff97,	0xab9423a7,	0xfc93a039,
            0x655b59c3,	0x8f0ccc92,	0xffeff47d,	0x85845dd1,
            0x6fa87e4f,	0xfe2ce6e0,	0xa3014314,	0x4e0811a1,
            0xf7537e82,	0xbd3af235,	0x2ad7d2bb,	0xeb86d391 ] 
    return fix[rdx ]

license = bytearray(b'X0XXX-XXXNX\x80')

def get_lic(val0):
    if val0 in [0,1,2]:
        #return None
        pass
    lic = [ 0x56303030, 0x31332d47, 0x80304e4e, 0x0,
            0x0,        0x0,        0x0,        0x0,
            0x0,        0x0,        0x0,        0x0,
            0x0,        0x0,        0x58,       0x0 ]
    #lic[0] = int.from_bytes(license[0:4],'little') 
    #lic[1] = int.from_bytes(license[4:8],'little') 
    #lic[2] = int.from_bytes(license[8:12],'little') 
    return lic[val0]


def rv(rdx, tar1, tar2, tar3, tar4):
    val = rdx >> 4
    if val == 1:
        val0 = (rdx * 5 + 1) & 0xf
        res = ((tar1 ^ tar2) & tar3) ^ tar2
    elif val == 2:
        val0 = ((rdx * 3) + 5) & 0xf
        res = tar1 ^ tar2 ^ tar3
    elif val == 0:
        res = ((tar2 ^ tar3) & tar1) ^ tar3
        val0 = rdx
    else :
        val0 = ((rdx << 3) - rdx) & 0xf
        res = (_not(tar3) | tar1 ) ^ tar2

    return val0, res

def rev(ret, rdx, tar1, tar2, tar3, tar4 = None):
    rdx = rdx - 1
    tmp_res = ror(ret - tar1 , get_fix1(rdx))
    
    val0, res = rv(rdx, tar1, tar2, tar3, tar4)
    
    fix2 = get_fix2(rdx)

    if get_lic(val0) != None:
        lic = get_lic(val0)
        tar4 = tmp_res - res - fix2 - lic
        tar4 &= 0xffffffff
    elif tar4 != None:
        lic = tmp_res - res - fix2 - tar4
    else: 
        print("with both unkown not implemented yet")    
        return None

    ret = tar1
    tar1 = tar2
    tar2 = tar3
    tar3 = tar4
    tar4 = None

    return {'ret': ret,
            'rdx': rdx,
            'tar1': tar1,
            'tar2': tar2,
            'tar3': tar3,
            'tar4': tar4,
            } 
def fwd(rdx, tar1, tar2, tar3, tar4):
    
    val0, res = rv(rdx, tar1, tar2, tar3, tar4)
    
    fix2 = get_fix2(rdx)
    if get_lic(val0) != None:
        lic = get_lic(val0)
        tmp_res = (tar4 + res + fix2 + lic) & 0xffffffff
    else: 
        print("not implemented yet")
        return None

    ret = (rol(tmp_res,get_fix1(rdx)) + tar1) & 0xffffffff

    tar4 = tar3
    tar3 = tar2
    tar2 = tar1
    tar1 = ret
    rdx = rdx + 1
    return {
            'rdx': rdx,
            'tar1': tar1,
            'tar2': tar2,
            'tar3': tar3,
            'tar4': tar4,
            } 
def print_(d):
    if d == None:
        print(d)
        return
    for key, value in d.items():
        if isinstance(value, int):  # Check if the value is an integer
            print(f"{key}: {hex(value)}")  # Print the key and value in hex
        else:
            print(f"{key}: {value}")  # Print the key and value as is




def backwards():
    for i in range(0x40):
        val0, _ = rv(i,0,0,0,0)
        RED = '\033[91m'
        RESET = '\033[0m'
        if val0 in [0,1,2]:
            text = RED + hex(val0) + RESET
        else:
            text = hex(val0)
        print(text, end = ", ")
        if i % 0x10 ==0xf:
            print()
    args = {'ret': 0x7b41bf6b,
            'rdx': 0x40,
            'tar1': 0x3b3f6fc6,
            'tar2': 0xbe8e4519,
            'tar3': 0xd22413c4
            } 

    exit()
    while args != None :
        res = rev(**args)
        print_(res)
        args = res

def forwards():
    args = {'rdx': 0x0,
            'tar1': 0xefcdab89,
            'tar2': 0x98badcfe,
            'tar3': 0x10325476,
            'tar4': 0x67452301 }
    for i in range(0x40):
        args = fwd(**args)
        #print(hex(args["tar1"]))
        if args["tar1"] in [0x3b3f6fc6, 0x7b41bf6b, 0xbe8e4519, 0xd22413c4]:
            print(f"found in round {i} with license: {license} {args['tar1']}")
    print_(args)
    if args["tar1"] == 0x7b41bf6b:
        return True
    else:
        return False

def main():
    global license
    #license[int(sys.argv[1])]=ord(sys.argv[2])
    forwards()
    exit()
    i = 0

    for a in chars:
        license[0] = ord(a)
        for b in chars:
            license[2] = ord(b)
            for c in chars:
                license[3] = ord(c)
                for d in chars:
                    license[4] = ord(d)
                    for e in chars:
                        license[6] = ord(e)
                        for f in chars:
                            license[7] = ord(f)
                            for g in chars:
                                license[8] = ord(g)
                                for h in chars:
                                    license[10] = ord(h)
                                    if i % 0x1000==0:
                                        print(f'\rtry {hex(i)}: {license}',end='')
                                    i +=1
                                    forwards()
                                    

    
    exit()
    for c in ['0','1']:
        license[0] = ord(c)
        print()
        print(license)
        
        forwards()
        
    print("finish")

if __name__ == "__main__":
    main()
