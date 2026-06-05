
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

def goruntu_topla(header1, data1, data2):
    genislik = struct.unpack('<I', header1[18:22])[0]
    yukseklik = struct.unpack('<I', header1[22:26])[0]
    padding = (4 - (genislik * 3) % 4) % 4
    satir_boyutu = genislik * 3 + padding

    sonuc = bytearray(len(data1))

    for y in range(yukseklik):
        for x in range(genislik):
            i = y * satir_boyutu + x * 3
            for c in range(3):
                toplam = data1[i+c] + data2[i+c]
                sonuc[i+c] = min(255, toplam)
    return sonuc

def goruntu_carp(header1, data1, data2):
    genislik = struct.unpack('<I', header1[18:22])[0]
    yukseklik = struct.unpack('<I', header1[22:26])[0]
    padding = (4 - (genislik * 3) % 4) % 4
    satir_boyutu = genislik * 3 + padding

    if len(data1) != len(data2):
        raise ValueError(f"Veri boyutları uyuşmuyor! data1: {len(data1)}, data2: {len(data2)}")

    sonuc = bytearray(len(data1))

    for y in range(yukseklik):
        for x in range(genislik):
            i = y * satir_boyutu + x * 3
            if i + 2 >= len(data1) or i + 2 >= len(data2):
                continue  # Güvenlik için veri dışına çıkmamak adına kontrol
            for c in range(3):
                carpim = (data1[i+c] * data2[i+c]) // 255
                sonuc[i+c] = min(255, carpim)
    return sonuc
