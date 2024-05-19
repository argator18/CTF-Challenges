import zlib
import struct

def calculate_png_crc(chunk_type, data):
    """ Calculate the CRC for a PNG chunk. """
    return zlib.crc32(chunk_type + data) & 0xffffffff

def read_png_idat_chunks(filename):
    """ Reads IDAT chunks from a PNG file and calculates their CRCs """
    with open(filename, 'rb') as file:
        content = file.read()
        pos = 0
        # PNG file signature
        png_signature = b'\x89PNG\r\n\x1a\n'
        if content[:8] != png_signature:
            print("Not a valid PNG file")
            return
        
        pos += 8  # skip the signature

        while pos < len(content):
            chunk_length = struct.unpack('>I', content[pos:pos+4])[0]
            chunk_type = content[pos+4:pos+8]
            chunk_data = content[pos+8:pos+8+chunk_length]
            chunk_crc = content[pos+8+chunk_length:pos+12+chunk_length]
            calculated_crc = struct.pack('>I', calculate_png_crc(chunk_type, chunk_data))
            
            # Only process IDAT chunks
            if chunk_type == b'IDAT':
                print(f"IDAT chunk found at position {pos}")
                print(f"Data length: {chunk_length}")
                print(f"Actual CRC: {chunk_crc.hex()}")
                print(f"Calculated CRC: {calculated_crc.hex()}")
                if chunk_crc != calculated_crc:
                    print("CRC error found in this chunk!")
                else:
                    print("CRC is correct for this chunk.")
            
            pos += chunk_length + 12  # move to the next chunk

### Usage Example

read_png_idat_chunks('images/current.png')

