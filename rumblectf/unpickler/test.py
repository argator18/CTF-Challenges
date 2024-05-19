import pickle
import pickletools
from pickle import dumps

# Create a sample object

pickled = b''
# Use genops to process the pickled data
def parse_line(op, arg):
    global pickled

    #print(f"Opcode: {op.code}, Arg: {arg}, Position: {pos}")
    len_arg = 0
    if type(arg) == int:
        len_arg = 1
    elif type(arg) == str:
        len_arg = len(arg)+1
        
    #pickled += (pos +1 - len(pickled) - len_arg - len(op)) * b'\x00' + op
    pickled += op
    if type(arg) == int:
        pickled += int.to_bytes(arg)
    if type(arg) == bytes:
        #pickled += int.to_bytes(len(arg))
        pickled += arg
    #print("p: ",pickled)

# File path
file_path = 'pickle.txt'

# Open and read the file
with open(file_path, 'r') as file:
    for line in file:
        # Strip newlines and split the line by comma
        parts = line.strip().split(',')
        
        # Extract and strip extra spaces
        op = parts[0].strip()
        arg = parts[1].strip()
        
        op = op.encode()

        if arg == "None":
            arg = None
        else:
            arg = bytes.fromhex(arg)

        parse_line(op,arg)

print(pickled.hex())
pickletools.dis(pickled)
