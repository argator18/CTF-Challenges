import zlib
import struct

def calculate_png_crc(chunk_type, data):
    """Calculate the CRC for a PNG chunk."""
    return zlib.crc32(chunk_type + data) & 0xffffffff

def correct_compression_header(data):
    """Correct the zlib compression header to use DEFLATE with a 32K window."""
    if len(data) < 2:
        return data  # Not enough data to correct
    
    cmf = data[0]
    method = cmf & 0x0F  # Compression method
    cinfo = cmf >> 4     # Compression info
    
    if method != 8 or cinfo != 7:
        # Set method to 8 (DEFLATE) and cinfo to 7 (32KB window size)
        cmf = (7 << 4) | 8
        data = bytearray(data)
        data[0] = cmf
        data = bytes(data)
        print("Corrected compression header to standard DEFLATE with a 32K window.")
    
    return data

def read_png_idat_chunks(filename):
    """Reads IDAT chunks from a PNG file, corrects their CRCs and compression headers, and writes back corrected data."""
    with open(filename, 'rb') as file:
        content = file.read()
    
    pos = 0
    new_content = bytearray()
    png_signature = b'\x89PNG\r\n\x1a\n'
    if content[:8] != png_signature:
        print("Not a valid PNG file")
        return
    
    pos += 8  # Skip the signature
    new_content.extend(content[:pos])

    while pos < len(content):
        chunk_length = struct.unpack('>I', content[pos:pos+4])[0]
        chunk_type = content[pos+4:pos+8]
        chunk_data = content[pos+8:pos+8+chunk_length]
        chunk_crc = content[pos+8+chunk_length:pos+12+chunk_length]

        if chunk_type == b'IDAT':
            # Correct the compression method and info if needed
            corrected_data = correct_compression_header(chunk_data)
            # Recalculate CRC for potentially corrected data
            calculated_crc = struct.pack('>I', calculate_png_crc(chunk_type, corrected_data))
            new_content.extend(struct.pack('>I', chunk_length))
            new_content.extend(chunk_type)
            new_content.extend(corrected_data)
            new_content.extend(calculated_crc)
        else:
            new_content.extend(content[pos:pos+12+chunk_length])

        pos += 12 + chunk_length  # Move to the next chunk
    
    # Overwrite the original file with corrected content
    with open(filename, 'wb') as file:
        file.write(new_content)
    print("File corrected and saved.")

### Usage Example

read_png_idat_chunks('images/current.png')

