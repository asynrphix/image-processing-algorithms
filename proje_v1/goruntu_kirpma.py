import struct

def goruntu_kirp(header, data, bas_x, bas_y, bit_x, bit_y):
    genislik = struct.unpack('<I', header[18:22])[0]
    yukseklik = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (genislik * 3) % 4) % 4
    satir_boyutu = genislik * 3 + padding

    yeni_genislik = bit_x - bas_x
    yeni_yukseklik = bit_y - bas_y
    yeni_padding = (4 - (yeni_genislik * 3) % 4) % 4
    yeni_satir_boyutu = yeni_genislik * 3 + yeni_padding

    yeni_data = bytearray(yeni_satir_boyutu * yeni_yukseklik)

    for y in range(yeni_yukseklik):
        eski_y = yukseklik - 1 - (bas_y + y)
        yeni_y = yeni_yukseklik - 1 - y  # BMP ters satır sırası

        for x in range(yeni_genislik):
            eski_x = bas_x + x
            eski_i = eski_y * satir_boyutu + eski_x * 3
            yeni_i = yeni_y * yeni_satir_boyutu + x * 3

            yeni_data[yeni_i:yeni_i+3] = data[eski_i:eski_i+3]

        # yeni padding sıfırla
        for p in range(yeni_padding):
            yeni_data[yeni_y * yeni_satir_boyutu + yeni_genislik * 3 + p] = 0

    # header güncelle
    yeni_header = bytearray(header)
    yeni_header[18:22] = struct.pack('<I', yeni_genislik)
    yeni_header[22:26] = struct.pack('<I', yeni_yukseklik)
    yeni_header[34:38] = struct.pack('<I', len(yeni_data))  # biSizeImage
    yeni_header[2:6] = struct.pack('<I', 54 + len(yeni_data))  # total file size

    return yeni_header, yeni_data

