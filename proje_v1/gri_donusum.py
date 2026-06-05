
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

def gri_donusum(header, data):
    genislik = struct.unpack('<I', header[18:22])[0]
    yukseklik = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (genislik * 3) % 4) % 4
    satir_boyutu = genislik * 3 + padding

    for y in range(yukseklik):
        for x in range(genislik):
            i = y * satir_boyutu + x * 3
            r, g, b = data[i+2], data[i+1], data[i]
            gri = int(0.299 * r + 0.587 * g + 0.114 * b)
            gri = max(0, min(255, gri))
            data[i] = data[i+1] = data[i+2] = gri
    return data
