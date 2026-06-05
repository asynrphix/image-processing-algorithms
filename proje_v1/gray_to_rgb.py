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

def jet_colormap_256():
    cmap = []
    for i in range(256):
        r = int(255 * max(min(1.5 - abs((i / 255.0 * 4) - 3), 1), 0))
        g = int(255 * max(min(1.5 - abs((i / 255.0 * 4) - 2), 1), 0))
        b = int(255 * max(min(1.5 - abs((i / 255.0 * 4) - 1), 1), 0))
        cmap.append((r, g, b))
    return cmap

def gray_to_rgb(header, data):
    width = struct.unpack('<I', header[18:22])[0]
    height = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (width * 3) % 4) % 4
    row_size = width * 3 + padding

    expected_size = row_size * height
    if len(data) < expected_size:
        raise ValueError(f"Yetersiz piksel verisi: beklenen {expected_size}, elde edilen {len(data)}")

    new_data = bytearray(len(data))
    colormap = jet_colormap_256()

    for y in range(height):
        for x in range(width):
            i = y * row_size + x * 3
            if i + 2 >= len(data):
                continue
            b, g, r = data[i], data[i+1], data[i+2]
            gri = int(0.299 * r + 0.587 * g + 0.114 * b)
            gri = max(0, min(gri, 255))
            rr, gg, bb = colormap[gri]
            new_data[i] = bb
            new_data[i+1] = gg
            new_data[i+2] = rr

        for p in range(padding):
            new_data[y * row_size + width * 3 + p] = 0

    return header, new_data
