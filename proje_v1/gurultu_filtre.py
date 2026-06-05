import struct

# Basit Linear Congruential Generator
seed = 123456789

def my_rand():
    global seed
    a = 1103515245
    c = 12345
    m = 2**31
    seed = (a * seed + c) % m
    return seed

def randint(min_val, max_val):
    return min_val + (my_rand() % (max_val - min_val + 1))

def choice(choices):
    index = my_rand() % len(choices)
    return choices[index]

def bmp_oku(dosya_yolu):
    with open(dosya_yolu, 'rb') as f:
        header = f.read(54)
        data = bytearray(f.read())
    return header, data

def bmp_kaydet(dosya_yolu, header, data):
    with open(dosya_yolu, 'wb') as f:
        f.write(header)
        f.write(data)

def gürültü_ekle(header, data, oran=0.05):
    genislik = struct.unpack('<I', header[18:22])[0]
    yukseklik = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (genislik * 3) % 4) % 4
    satir_boyutu = genislik * 3 + padding
    toplam_piksel = genislik * yukseklik
    gürültü_sayisi = int(toplam_piksel * oran)

    for _ in range(gürültü_sayisi):
        x = randint(0, genislik - 1)
        y = randint(0, yukseklik - 1)
        i = y * satir_boyutu + x * 3
        deger = choice([0, 255])
        data[i] = data[i+1] = data[i+2] = deger

    return data

def mean_filtre(header, data):
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

def median_filtre(header, data):
    genislik = struct.unpack('<I', header[18:22])[0]
    yukseklik = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (genislik * 3) % 4) % 4
    satir_boyutu = genislik * 3 + padding
    sonuc = bytearray(data)

    for y in range(1, yukseklik - 1):
        for x in range(1, genislik - 1):
            komsular = [[], [], []]
            for j in range(-1, 2):
                for i in range(-1, 2):
                    idx = (y + j) * satir_boyutu + (x + i) * 3
                    for c in range(3):
                        komsular[c].append(data[idx + c])
            idx_merkez = y * satir_boyutu + x * 3
            for c in range(3):
                # Kendi sıralama algoritmamız (bubble sort - küçük resimler için yeterli)
                for m in range(8):
                    for n in range(8 - m):
                        if komsular[c][n] > komsular[c][n+1]:
                            komsular[c][n], komsular[c][n+1] = komsular[c][n+1], komsular[c][n]
                sonuc[idx_merkez + c] = komsular[c][4]
    return sonuc