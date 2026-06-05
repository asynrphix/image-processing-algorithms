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

def rgb_to_gray(data, genislik, yukseklik, satir_boyutu):
    """
    RGB'yi gri tonlamaya dönüştürme işlemi.
    """
    gray_data = bytearray(len(data))
    
    for y in range(yukseklik):
        for x in range(genislik):
            index = y * satir_boyutu + x * 3
            r = data[index + 2]
            g = data[index + 1]
            b = data[index]
            # Gri tonlama formülü (luminosity method)
            gri = int(0.299 * r + 0.587 * g + 0.114 * b)
            gray_data[index] = gri
            gray_data[index + 1] = gri
            gray_data[index + 2] = gri
    
    return gray_data

def sobel_kenar_bulma(header, data):
    genislik = struct.unpack('<I', header[18:22])[0]
    yukseklik = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (genislik * 3) % 4) % 4
    satir_boyutu = genislik * 3 + padding
    sonuc = bytearray(data)

    # Sobel maskeleri
    gx = [[-1, 0, 1],
          [-2, 0, 2],
          [-1, 0, 1]]

    gy = [[-1, -2, -1],
          [ 0,  0,  0],
          [ 1,  2,  1]]

    # Gri tonlama işlemi
    gray_data = rgb_to_gray(data, genislik, yukseklik, satir_boyutu)
    
    for y in range(1, yukseklik - 1):
        for x in range(1, genislik - 1):
            sum_x = [0, 0, 0]
            sum_y = [0, 0, 0]

            for j in range(3):
                for i in range(3):
                    nx = x + i - 1
                    ny = y + j - 1
                    index = ny * satir_boyutu + nx * 3
                    for c in range(3):
                        sum_x[c] += gx[j][i] * gray_data[index + c]
                        sum_y[c] += gy[j][i] * gray_data[index + c]

            index = y * satir_boyutu + x * 3
            for c in range(3):
                val = int((sum_x[c]**2 + sum_y[c]**2)**0.5)
                sonuc[index + c] = max(0, min(255, val))

    return sonuc
