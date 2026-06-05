
import struct

def bmp_oku(dosya_yolu):
    with open(dosya_yolu, 'rb') as f:
        header = f.read(54)
        data = bytearray(f.read())
    return header, data

def bmp_kaydet(dosya_yolu, header, data):
    with open(dosya_yolu, 'wb') as f:
        f.write(header)
        f.write(data)

def binary_donusum(header, data, threshold=128):
    # Extract width and height from DIB header (immediately after 14 bytes)
    dib_header = header[14:14+40]
    width = struct.unpack('<I', dib_header[4:8])[0]
    height_signed = struct.unpack('<i', dib_header[8:12])[0]
    height = abs(height_signed)
    bottom_up = height_signed > 0
    # Bits per pixel (to determine bytes per pixel)
    bpp = struct.unpack('<H', dib_header[14:16])[0]
    bytes_per_pixel = bpp // 8
    padding = (4 - (width * bytes_per_pixel) % 4) % 4
    row_size = width * bytes_per_pixel + padding

    for y in range(height):
        row_idx = (height - 1 - y) if bottom_up else y
        for x in range(width):
            i = row_idx * row_size + x * bytes_per_pixel
            if i + bytes_per_pixel > len(data):
                continue
            # Unpack based on pixel format
            if bytes_per_pixel >= 3:
                b, g, r = data[i], data[i+1], data[i+2]
            else:
                # For 8-bit or less, treat the byte as grayscale directly
                gray = data[i]
                r = g = b = gray
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            new_val = 255 if gray >= threshold else 0
            for p in range(bytes_per_pixel):
                data[i+p] = new_val
    return data
