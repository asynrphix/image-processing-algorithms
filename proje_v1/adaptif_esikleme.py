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

def gri_tonlama(r, g, b):
    return int(0.2989 * r + 0.5870 * g + 0.1140 * b)

def adaptif_esikleme(header, data, pencere_boyutu=15):
    genislik = struct.unpack('<I', header[18:22])[0]
    yukseklik = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (genislik * 3) % 4) % 4
    satir_boyutu = genislik * 3 + padding
    yaricap = pencere_boyutu // 2
    sonuc = bytearray(len(data))

    for y in range(yukseklik):
        for x in range(genislik):
            toplam = 0
            toplam_kare = 0
            piksel_sayisi = 0

            for dy in range(-yaricap, yaricap + 1):
                for dx in range(-yaricap, yaricap + 1):
                    yy = min(max(0, y + dy), yukseklik - 1)
                    xx = min(max(0, x + dx), genislik - 1)
                    i = yy * satir_boyutu + xx * 3
                    gri = gri_tonlama(data[i+2], data[i+1], data[i])
                    toplam += gri
                    toplam_kare += gri * gri
                    piksel_sayisi += 1

            ort = toplam / piksel_sayisi
            varyans = (toplam_kare / piksel_sayisi) - (ort ** 2)
            t = ort * (1 + 0.2 * ((varyans ** 0.5) / 128 - 1))  # Sauvola benzeri eşik

            i_merkez = y * satir_boyutu + x * 3
            gri = gri_tonlama(data[i_merkez+2], data[i_merkez+1], data[i_merkez])
            yeni = 255 if gri > t else 0

            sonuc[i_merkez] = sonuc[i_merkez+1] = sonuc[i_merkez+2] = yeni

    return sonuc
