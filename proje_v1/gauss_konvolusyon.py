import struct

# Kendi üs alma fonksiyonumuz
def us_al(x, n):
    sonuc = 1.0
    for _ in range(n):
        sonuc *= x
    return sonuc

# Kendi e^x hesabımız (Taylor Serisi, 10 terim yeterli)
def exp_approx(x):
    toplam = 1.0
    terim = 1.0
    for i in range(1, 10):
        terim *= x / i
        toplam += terim
    return toplam

def gauss_konvolusyon(header, data, kernel_boyutu=3, sigma=1.0, parlaklik_artisi=30):
    PI = 3.14159
    genislik = struct.unpack('<I', header[18:22])[0]
    yukseklik = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (genislik * 3) % 4) % 4
    satir_boyutu = genislik * 3 + padding
    yaricap = kernel_boyutu // 2

    kernel = []
    toplam = 0.0
    for j in range(-yaricap, yaricap + 1):
        for i in range(-yaricap, yaricap + 1):
            uzaklik_kare = i*i + j*j
            deger = exp_approx(-(uzaklik_kare) / (2 * sigma * sigma)) / (2 * PI * sigma * sigma)
            kernel.append(deger)
            toplam += deger
    kernel = [x / toplam for x in kernel]

    sonuc = bytearray(len(data))

    for y in range(yaricap, yukseklik - yaricap):
        for x in range(yaricap, genislik - yaricap):
            toplam_r = toplam_g = toplam_b = 0.0
            for j in range(-yaricap, yaricap + 1):
                for i in range(-yaricap, yaricap + 1):
                    piksel_x = x + i
                    piksel_y = y + j
                    indeks = piksel_y * satir_boyutu + piksel_x * 3
                    cekirdek_indeksi = (j + yaricap) * kernel_boyutu + (i + yaricap)
                    katsayi = kernel[cekirdek_indeksi]
                    toplam_b += data[indeks]     * katsayi
                    toplam_g += data[indeks + 1] * katsayi
                    toplam_r += data[indeks + 2] * katsayi

            merkez = y * satir_boyutu + x * 3
            sonuc[merkez]     = min(255, max(0, int(toplam_b + parlaklik_artisi)))
            sonuc[merkez + 1] = min(255, max(0, int(toplam_g + parlaklik_artisi)))
            sonuc[merkez + 2] = min(255, max(0, int(toplam_r + parlaklik_artisi)))

    return sonuc
