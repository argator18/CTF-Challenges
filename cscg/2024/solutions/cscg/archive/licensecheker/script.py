import itertools
import subprocess

# License template
lic_template = "A1KXB-XXXLX-BY82X-00GHK-L1MNS"

# Positions of 'X's in the license string (0-indexed)
x_positions = [0x3 ]

# Characters to try at each 'X' position
chars = [chr(i) for i in range(48, 58)] + [chr(i) for i in range(65, 91)]  # 0-9, A-Z


vals1 = []
for a in chars:
    for b in chars:
        if b == a:
            continue
        if chr(0x31 ^ ord(a) ^ ord(b)) in chars:
            vals1.append((a,b))

print(f"found all a and b ({len(vals1)})")
vals2 = {}
num2 = 0
for a in chars:
    tmp = []
    if ord(a) ==0x40:
        continue
    for b in chars:
        if chr(0x40 ^ ord(a) ^ ord(b))  in chars and chr((0x40 ^ ord(a) ^ ord(b)) + 5) in chars:
            tmp.append((b))
            num2+=1
    vals2[a] = tmp

print(f"found all c ({num2})")

vals3=[]
for a in chars:
    if chr(0x3 ^ ord(a)) in chars and ord(a) != 0x42:
           vals3.append(a)
print(f"found all d ({len(vals3)})")

vals4=[]
for a in chars:
    if chr(0x7e ^ ord(a)) in chars and ord(a) != 0x38:
           vals4.append(a)
print(f"found all e ({len(vals4)})")

# Helper function to apply constraints
def valid_lic(license_str,n):
    # Convert characters to their ASCII values for calculation
    lic = [ord(c) for c in license_str]


    # Constraint checks
    if not (lic[0x6] != 0x42 and
            lic[0x7] != lic[0xd] and
            lic[0x8] != 0x38 and
            lic[0xa] != lic[0x10] and
            lic[3] != 0x32):
        return False
    print(f"\rtry: {hex(n)} | lic = {license_str}",end = "")
    command = f"licensecheck {license_str}"

    # Execute the command and capture the output
    try:
        output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output

    # Check if the output contains 'license is valid'
    return "License is valid" in output

# Function to attempt to fill in 'X's and find valid license
def find_valid_license():
    n = 0
    lic = list(lic_template)
    lic[0x10] = lic[0x19]
    lic[0xa] = chr(0x31 ^ ord(lic[0x1c]) ^ ord(lic[0x10]) )

    lic[0xd] = chr(ord(lic[0x14]) - 5 )
    lic[0x7] = chr(0x40 ^ ord(lic[0xd]) ^ ord(lic[0x19]))
    
    

    lic[0x6] = chr(0x3 ^ ord(lic[0x18]))
    lic[0x8] = chr(0x7e ^ ord(lic[0x1a]))
    for combo in itertools.product(chars, repeat=len(x_positions)):
        for pos, char in zip(x_positions, combo):
            lic[pos] = char
            n +=1

            lic_str = ''.join(lic)
            if valid_lic(lic_str,n):
                return lic_str
            
    return "No valid license found."

# Find and print a valid license
print(find_valid_license())

