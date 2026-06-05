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

def rgb_to_gray(r, g, b):
    return int(0.299 * r + 0.587 * g + 0.114 * b)

def rgb_to_gray_donusum(header, data):
    width = struct.unpack('<I', header[18:22])[0]
    height = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (width * 3) % 4) % 4
    row_size = width * 3 + padding

    new_data = bytearray(len(data))

    for y in range(height):
        for x in range(width):
            i = y * row_size + x * 3
            b, g, r = data[i], data[i+1], data[i+2]
            gri = rgb_to_gray(r, g, b)
            new_data[i] = new_data[i+1] = new_data[i+2] = gri

        for p in range(padding):
            new_data[y * row_size + width * 3 + p] = 0

    return header, new_data
