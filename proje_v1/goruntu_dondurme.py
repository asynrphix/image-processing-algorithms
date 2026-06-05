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

def goruntu_dondurme(header, data):
    genislik = struct.unpack('<I', header[18:22])[0]
    yukseklik = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (genislik * 3) % 4) % 4
    satir_boyutu = genislik * 3 + padding

    yeni_data = bytearray(len(data))
    yeni_data[:] = [255] * len(data)  # Yeni veri için beyaz pikseller

    # 180 derece döndürme işlemi: x ve y koordinatlarını ters çevir
    for y in range(yukseklik):
        for x in range(genislik):
            # Eski pikselin verilerini al
            i = y * satir_boyutu + x * 3
            # Yeni pikselin yerini hesapla (180 derece döndürme)
            j = (yukseklik - 1 - y) * satir_boyutu + (genislik - 1 - x) * 3

            # Yeni veriye eski pikseli yerleştir
            yeni_data[j] = data[i]
            yeni_data[j + 1] = data[i + 1]
            yeni_data[j + 2] = data[i + 2]

    return yeni_data
