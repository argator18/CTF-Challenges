import zlib
import struct

def calculate_png_crc(chunk_type, data):
    """ Calculate the CRC for a PNG chunk. """
    return zlib.crc32(chunk_type + data) & 0xffffffff

def correct_png_crc(filename):
    """ Reads and automatically corrects CRC errors in IDAT chunks of a PNG file. """
    with open(filename, 'rb') as file:
        content = file.read()
    
    pos = 0
    new_content = bytearray()
    png_signature = b'\x89PNG\r\n\x1a\n'
    if content[:8] != png_signature:
        print("Not a valid PNG file")
        return

    pos += 8  # skip the signature
    new_content.extend(content[:pos])

    while pos < len(content):
        chunk_length = struct.unpack('>I', content[pos:pos+4])[0]
        chunk_type = content[pos+4:pos+8]
        chunk_data = content[pos+8:pos+8+chunk_length]
        chunk_crc = content[pos+8+chunk_length:pos+12+chunk_length]
        calculated_crc = struct.pack('>I', calculate_png_crc(chunk_type, chunk_data))
        
        # Append chunk length, type, and data to new content
        new_content.extend(content[pos:pos+8+chunk_length])
        
        if chunk_type == b'IDAT' and chunk_crc != calculated_crc:
            print(f"CRC error found in IDAT at pos {pos}, correcting...")
            new_content.extend(calculated_crc)
        else:
            new_content.extend(chunk_crc)
        
        pos += chunk_length + 12  # move to the next chunk

    # Overwrite the old file with the corrected data
    with open(filename, 'wb') as file:
        file.write(new_content)
    print("File has been corrected and saved.")

### Usage Example

correct_png_crc('current.png')

