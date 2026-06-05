
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

def blurring(header, data):
    genislik = struct.unpack('<I', header[18:22])[0]
    yukseklik = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (genislik * 3) % 4) % 4
    satir_boyutu = genislik * 3 + padding
    sonuc = bytearray(data)

    for y in range(1, yukseklik - 1):
        for x in range(1, genislik - 1):
            toplam = [0, 0, 0]
            for j in range(-1, 2):
                for i in range(-1, 2):
                    idx = (y + j) * satir_boyutu + (x + i) * 3
                    for c in range(3):
                        toplam[c] += data[idx + c]
            idx_merkez = y * satir_boyutu + x * 3
            for c in range(3):
                sonuc[idx_merkez + c] = toplam[c] // 9
    return sonuc
