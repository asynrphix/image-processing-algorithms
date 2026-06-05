
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

def histogram_germe(header, data):
    genislik = struct.unpack('<I', header[18:22])[0]
    yukseklik = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (genislik * 3) % 4) % 4
    satir_boyutu = genislik * 3 + padding

    min_val = 255
    max_val = 0

    # 1. Aşama: min ve max gri değeri bul
    for y in range(yukseklik):
        for x in range(genislik):
            i = y * satir_boyutu + x * 3
            r, g, b = data[i+2], data[i+1], data[i]
            gri = int(0.299 * r + 0.587 * g + 0.114 * b)
            min_val = min(min_val, gri)
            max_val = max(max_val, gri)

    # 2. Aşama: piksel değerlerini yeniden ölçekle
    for y in range(yukseklik):
        for x in range(genislik):
            i = y * satir_boyutu + x * 3
            r, g, b = data[i+2], data[i+1], data[i]
            gri = int(0.299 * r + 0.587 * g + 0.114 * b)
            if max_val != min_val:
                yeni = int((gri - min_val) * 255 / (max_val - min_val))
            else:
                yeni = gri
            data[i] = data[i+1] = data[i+2] = max(0, min(255, yeni))

    return data
