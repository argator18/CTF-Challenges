import zlib
import struct

def read_png_file(filename):
    """Reads a PNG file and returns its content."""
    with open(filename, 'rb') as file:
        content = file.read()
    return content

def parse_chunks(png_data):
    """Parse the PNG file and yield chunks as (type, data) tuples."""
    pos = 8  # Skip the initial PNG file signature
    while pos < len(png_data):
        length = struct.unpack('>I', png_data[pos:pos+4])[0]
        type_code = png_data[pos+4:pos+8].decode('ascii')
        data = png_data[pos+8:pos+8+length]
        pos += 12 + length
        yield type_code, data

def decompress_idat_chunks(idat_chunks):
    """Decompress concatenated IDAT chunks using zlib and check block types."""
    decompressed = bytearray()
    decompressor = zlib.decompressobj()
    for chunk in idat_chunks:
        try:
            decompressed += decompressor.decompress(chunk)
        except zlib.error as e:
            print(f"Decompression error: {e}, continuing...")
        decompressed += decompressor.unused_data  # Append any undecompressed data
    try:
        decompressed += decompressor.flush()
    except zlib.error as e:
        print(f"Flush error: {e}, some data might be missing.")
    return decompressed

def validate_deflate_blocks(data):
    """Validate DEFLATE block types in decompressed data."""
    pos = 0
    while pos < len(data) and pos + 1 < len(data):
        bfinal = data[pos] & 1
        btype = (data[pos] >> 1) & 3
        if btype > 2:
            print(f"Invalid block type {btype} found at position {pos}")
        else:
            print(f"Valid block type {btype} found at position {pos}")
        pos += 1  # Naive next block position; not accurate for actual streams
        if bfinal:
            print("Last block reached.")
            break

def main():
    filename = 'images/current.png'
    png_data = read_png_file(filename)
    idat_data = []

    for type_code, data in parse_chunks(png_data):
        if type_code == 'IDAT':
            idat_data.append(data)
    
    if idat_data:
        decompressed_data = decompress_idat_chunks(idat_data)
        validate_deflate_blocks(decompressed_data)
    else:
        print("No IDAT chunks found in the PNG file.")

if __name__ == "__main__":
    main()

