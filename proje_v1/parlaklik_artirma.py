
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

def parlaklik_artir(header, data, miktar=40):
    genislik = struct.unpack('<I', header[18:22])[0]
    yukseklik = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (genislik * 3) % 4) % 4
    satir_boyutu = genislik * 3 + padding

    for y in range(yukseklik):
        for x in range(genislik):
            i = y * satir_boyutu + x * 3
            for c in range(3):
                yeni_deger = data[i + c] + miktar
                data[i + c] = max(0, min(255, yeni_deger))

    return data
