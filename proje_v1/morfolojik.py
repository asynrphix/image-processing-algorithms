
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

def pad_image(image, m, n):
    height = len(image)
    width = len(image[0])
    padded = [[0] * (width + 2 * n) for _ in range(height + 2 * m)]
    for i in range(height):
        for j in range(width):
            padded[i + m][j + n] = image[i][j]
    return padded

def erosion(image, struct_elem, m, n):
    padded = pad_image(image, m, n)
    height = len(image)
    width = len(image[0])
    output = [[0] * width for _ in range(height)]
    for i in range(height):
        for j in range(width):
            uygun = True
            for dy in range(len(struct_elem)):
                for dx in range(len(struct_elem[0])):
                    if struct_elem[dy][dx] == 1:
                        if padded[i + dy][j + dx] == 0:
                            uygun = False
                            break
                if not uygun:
                    break
            output[i][j] = 1 if uygun else 0
    return output

def binarize_image(header, data):
    width = struct.unpack('<I', header[18:22])[0]
    height = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (width * 3) % 4) % 4
    row_size = width * 3 + padding
    image = [[0] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            idx = y * row_size + x * 3
            r, g, b = data[idx + 2], data[idx + 1], data[idx]
            image[y][x] = 1 if (r > 128 and g > 128 and b > 128) else 0
    return image

def binary_to_bmp_data(image, header):
    width = struct.unpack('<I', header[18:22])[0]
    height = struct.unpack('<I', header[22:26])[0]
    padding = (4 - (width * 3) % 4) % 4
    row_size = width * 3 + padding
    data = bytearray(row_size * height)
    for y in range(height):
        for x in range(width):
            val = 255 if image[y][x] else 0
            idx = y * row_size + x * 3
            data[idx] = val
            data[idx + 1] = val
            data[idx + 2] = val
    return data

def disk_yapisal_eleman(yaricap):
    eleman = []
    cap2 = yaricap * yaricap
    for y in range(-yaricap, yaricap + 1):
        satir = []
        for x in range(-yaricap, yaricap + 1):
            if x*x + y*y <= cap2:
                satir.append(1)
            else:
                satir.append(0)
        eleman.append(satir)
    return eleman

def asindir(header, data, yaricap=2):
    se = disk_yapisal_eleman(yaricap)
    binary = binarize_image(header, data)
    eroded = erosion(binary, se, yaricap, yaricap)
    return binary_to_bmp_data(eroded, header)




def dilation(image, struct_elem, m, n):
    padded = pad_image(image, m, n)
    height = len(image)
    width = len(image[0])
    output = [[0] * width for _ in range(height)]
    for i in range(height):
        for j in range(width):
            aktif = False
            for dy in range(len(struct_elem)):
                for dx in range(len(struct_elem[0])):
                    if struct_elem[dy][dx] == 1:
                        if padded[i + dy][j + dx] == 1:
                            aktif = True
                            break
                if aktif:
                    break
            output[i][j] = 1 if aktif else 0
    return output

def genislet(header, data, yaricap=5):
    se = disk_yapisal_eleman(yaricap)
    binary = binarize_image(header, data)
    dilated = dilation(binary, se, yaricap, yaricap)
    return binary_to_bmp_data(dilated, header)

def acma(header, data, yaricap=5):
    eroded = asindir(header, data, yaricap)
    return genislet(header, eroded, yaricap)

def kapama(header, data, yaricap=7):
    dilated = genislet(header, data, yaricap)
    return asindir(header, dilated, yaricap)

