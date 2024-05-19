import pwn
# Constants
multiplier = 0xb6db6db7
target = 0x24924924


def check(hex1, hex2, n):
    # Convert the numbers to hexadecimal strings without the '0x' prefix
    hex_str1 = format(hex1, 'x')
    hex_str2 = format(hex2, 'x')

    # Compare the last n characters of the hexadecimal strings
    return hex_str1[-n:] == hex_str2[-n:]

eax = 0
for n in range(8):
    for d in range(0x10):
        cur_val = ((eax + (0x10 ** n) *d ) * multiplier) & 0xFFFFFFFF
        print(f"cur_val: {hex(cur_val)}")
        input()
        if check(cur_val , target , n+1):
            eax = eax + 0x10 ** n * d
            print(f"eax: {hex(eax)}")
            break

exit()
def find_eax():
    for eax in range(2**28):  # Iterate over all 32-bit unsigned integers
        eax = eax * 2**4 + 0xc
        print(f'\rtry: {hex(eax)}',end='')
        result = (eax * multiplier) & 0xFFFFFFFF  # Perform 32-bit multiplication
        if result == target:
            return eax
    return None

# Find the eax value
eax_value = find_eax()

if eax_value is not None:
    print(f"Found eax: {eax_value}")
else:
    print("No solution found.")

