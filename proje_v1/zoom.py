import struct

def padding_hesapla(genislik, bytes_per_pixel):
    return (4 - (genislik * bytes_per_pixel) % 4) % 4

def goruntu_yakinlastir(header, data, oran=2.0):
    """Merkez bölgeyi yakınlaştırarak büyütülmüş görüntü oluşturur (zoom-in)."""
    width = struct.unpack('<I', header[18:22])[0]
    height_signed = struct.unpack('<i', header[22:26])[0]
    height = abs(height_signed)
    bottom_up = height_signed > 0

    bpp = struct.unpack('<H', header[28:30])[0]
    bytes_per_pixel = bpp // 8

    eski_padding = padding_hesapla(width, bytes_per_pixel)
    eski_row_size = width * bytes_per_pixel + eski_padding

    # Yeni görüntü orijinal boyutta kalacak
    new_width = width
    new_height = height
    yeni_padding = padding_hesapla(new_width, bytes_per_pixel)
    yeni_row_size = new_width * bytes_per_pixel + yeni_padding

    new_data = bytearray(yeni_row_size * new_height)

    # Yakınlaştırılacak merkez bölge
    crop_width = int(width / oran)
    crop_height = int(height / oran)
    start_x = (width - crop_width) // 2
    start_y = (height - crop_height) // 2

    for y in range(new_height):
        for x in range(new_width):
            # Zoom-in işlemi: çıktı pikselini orijinal kırpılmış bölgedeki karşılığına eşleştir
            gx = start_x + int(x / oran)
            gy = start_y + int(y / oran)

            gx = min(width - 1, max(0, gx))
            gy = min(height - 1, max(0, gy))

            row = (height - 1 - gy) if bottom_up else gy
            i = row * eski_row_size + gx * bytes_per_pixel
            new_row = (new_height - 1 - y) if bottom_up else y
            new_i = new_row * yeni_row_size + x * bytes_per_pixel

            for c in range(bytes_per_pixel):
                new_data[new_i + c] = data[i + c]

        # Padding sıfırla
        for p in range(yeni_padding):
            pad_i = new_row * yeni_row_size + new_width * bytes_per_pixel + p
            new_data[pad_i] = 0

    # Header'ı güncelle
    new_header = bytearray(header)
    new_header[2:6] = struct.pack('<I', 54 + len(new_data))  # Dosya boyutu
    new_header[34:38] = struct.pack('<I', len(new_data))     # Piksel veri boyutu

    return new_header, new_data
