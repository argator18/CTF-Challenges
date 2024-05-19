import zlib
import struct

def read_png_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return data

def find_idat_chunks(data):
    position = 0
    idat_data = b''
    while True:
        pos = data.find(b'IDAT', position)
        if pos == -1:
            break
        length = struct.unpack('!I', data[pos-4:pos])[0]
        idat_data += data[pos+8:pos+8+length]  # Skip the 4-byte CRC at the end of each chunk
        position = pos + 12 + length  # Move past the chunk header+data+CRC
    return idat_data

def correct_zlib_header(data):
    corrected_data = bytearray(data)
    # The first byte of the zlib data should be 0x78 for default compression,
    # followed by one of several possible values for the flags byte.
    # We'll try changing the second byte to common values (0x9C, 0xDA, 0x20).
    common_flags = [0x9C, 0xDA, 0x20]
    for flags in common_flags:
        corrected_data[0] = 0x78
        corrected_data[1] = flags
        try:
            result = zlib.decompress(corrected_data)
            print(f"Success with zlib flags byte: {hex(flags)}")
            return result
        except zlib.error as e:
            print(f"Failed with zlib flags byte: {hex(flags)}, error: {e}")
    return None

filename = 'images/current.png'
data = read_png_file(filename)
idat_data = find_idat_chunks(data)
result = correct_zlib_header(idat_data)

if result:
    print("Decompression successful, data can now be saved or further processed.")
else:
    print("All attempts failed, further manual inspection needed.")

