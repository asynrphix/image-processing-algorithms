from PyQt5.QtWidgets import QDialog, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, qRgb, qRgba
from PyQt5.QtCore import Qt
import struct

class OnizlemePenceresi(QDialog):
    def __init__(self, orijinal_header, orijinal_data, islenmis_header, islenmis_data, baslik):
        super().__init__()
        self.setWindowTitle("Önizleme: " + baslik)
        self.resize(900, 500)

        self.label_baslik = QLabel(baslik)
        self.label_baslik.setAlignment(Qt.AlignCenter)
        self.label_baslik.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.label_orijinal = QLabel()
        self.label_islenmis = QLabel()
        self.label_orijinal.setAlignment(Qt.AlignCenter)
        self.label_islenmis.setAlignment(Qt.AlignCenter)

        placeholder_text = "Görsel yükleniyor..."
        self.label_orijinal.setText(placeholder_text)
        self.label_islenmis.setText(placeholder_text)

        hbox = QHBoxLayout()
        hbox.addWidget(self.label_orijinal)
        hbox.addWidget(self.label_islenmis)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label_baslik)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        try:
            pixmap_orijinal = self.veri_to_pixmap(orijinal_header, orijinal_data)
            if not pixmap_orijinal.isNull():
                self.label_orijinal.setPixmap(pixmap_orijinal.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.label_orijinal.setText("Orijinal Yüklenemedi")
        except Exception as e:
            print(f"Error loading original image: {e}")
            self.label_orijinal.setText(f"Orijinal Hata:\n{e}")
            self.label_orijinal.setWordWrap(True)

        try:
            pixmap_islenmis = self.veri_to_pixmap(islenmis_header, islenmis_data)
            if not pixmap_islenmis.isNull():
                self.label_islenmis.setPixmap(pixmap_islenmis.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.label_islenmis.setText("İşlenmiş Yüklenemedi")
        except Exception as e:
            print(f"Error loading processed image: {e}")
            self.label_islenmis.setText(f"İşlenmiş Hata:\n{e}")
            self.label_islenmis.setWordWrap(True)




    def veri_to_pixmap(self, header: bytes, data: bytes) -> QPixmap:
        # Basic header validation (ensure we have at least the essential parts)
        if not header or len(header) < 54:
             raise ValueError("Invalid or incomplete BMP header provided (need at least 54 bytes).")

        # --- Common Header Info (parsed from the 'header' argument) ---
        if header[0:2] != b'BM':
            raise ValueError("Not a valid BMP file (Missing 'BM' signature).")
        data_offset = int.from_bytes(header[10:14], byteorder='little')
        dib_header_size = int.from_bytes(header[14:18], byteorder='little')
        width = int.from_bytes(header[18:22], byteorder='little')
        height_raw = int.from_bytes(header[22:26], byteorder='little', signed=True)
        abs_height = abs(height_raw)
        top_down = height_raw < 0
        bit_depth = int.from_bytes(header[28:30], byteorder='little')
        compression = int.from_bytes(header[30:34], byteorder='little')

        if compression != 0: # BI_RGB
             raise ValueError(f"Unsupported compression method: {compression}. Only BI_RGB (0) is supported.")

        # --- Calculate where pixel data *actually* starts ---
        # This assumes the 'data' argument starts immediately after the 'header' argument ends.
        # If header is 54 bytes, data starts at file offset 54.
        # The pixel data within the 'data' argument starts at index (data_offset - header_len)
        header_len = len(header) # Usually 54 in this scenario
        pixel_data_start_index_in_data = data_offset - header_len
        if pixel_data_start_index_in_data < 0:
            # This would happen if data_offset < header_len, which is weird but possible
            # Or if the split wasn't done right after the header passed.
            raise ValueError(f"Calculated pixel data start index ({pixel_data_start_index_in_data}) is invalid based on data_offset ({data_offset}) and header_len ({header_len}). Data structure mismatch?")

        image = None # Initialize image variable

        # --- Image Data Loading ---

        if bit_depth == 24:
            padding = (4 - (width * 3) % 4) % 4
            row_size = width * 3 + padding
            # Effective pixel data slice
            actual_pixel_data = data[pixel_data_start_index_in_data:]
            expected_pixel_data_size = row_size * abs_height
            if len(actual_pixel_data) < expected_pixel_data_size:
                 raise ValueError(f"Insufficient pixel data for 24-bit BMP. Expected {expected_pixel_data_size}, got {len(actual_pixel_data)}")

            image = QImage(width, abs_height, QImage.Format_RGB888)
            for y in range(abs_height):
                src_y = y if top_down else abs_height - 1 - y
                row_start = src_y * row_size
                for x in range(width):
                    pixel_index = row_start + x * 3
                    # Read from the actual_pixel_data slice
                    if pixel_index + 2 < len(actual_pixel_data):
                        b, g, r = struct.unpack_from('<BBB', actual_pixel_data, pixel_index)
                        image.setPixel(x, y, qRgb(r, g, b))
                    else:
                        image.setPixel(x, y, qRgb(0,0,0)) # Black for short data

        elif bit_depth == 32:
            row_size = width * 4
            actual_pixel_data = data[pixel_data_start_index_in_data:]
            expected_pixel_data_size = row_size * abs_height
            if len(actual_pixel_data) < expected_pixel_data_size:
                 raise ValueError(f"Insufficient pixel data for 32-bit BMP. Expected {expected_pixel_data_size}, got {len(actual_pixel_data)}")

            image = QImage(width, abs_height, QImage.Format_ARGB32)
            for y in range(abs_height):
                src_y = y if top_down else abs_height - 1 - y
                row_start = src_y * row_size
                for x in range(width):
                    pixel_index = row_start + x * 4
                    if pixel_index + 3 < len(actual_pixel_data):
                        b, g, r, a = struct.unpack_from('<BBBB', actual_pixel_data, pixel_index)
                        image.setPixel(x, y, qRgb(r, g, b)) # Use qRgb for opaque, or qRgba(r,g,b,a)
                    else:
                        image.setPixel(x, y, qRgb(0,0,0)) # Black for short data

        elif bit_depth == 8:
            # --- Palette Loading (from the START of the 'data' argument) ---
            palette_start_offset_in_file = 14 + dib_header_size # Absolute offset in file (e.g., 54)
            # Check consistency: palette should start where the header ends
            if palette_start_offset_in_file != header_len:
                 print(f"Warning: Palette start offset in file ({palette_start_offset_in_file}) "
                       f"does not match header length ({header_len}). Assuming palette starts at the beginning of 'data'.")

            num_palette_colors = int.from_bytes(header[46:50], byteorder='little') # biClrUsed
            if num_palette_colors == 0 or num_palette_colors > 256:
                 num_palette_colors = 256

            palette_size = num_palette_colors * 4 # BGR + Reserved = 4 bytes
            palette_end_index_in_data = palette_size # Palette is bytes 0 to palette_size-1 in 'data'

            # Check if 'data' argument is long enough to contain the palette
            if len(data) < palette_size:
                 raise ValueError(f"Insufficient 'data' length ({len(data)}) for color palette (needs {palette_size} bytes).")

            # Read palette from the 'data' argument
            palette = []
            for i in range(num_palette_colors):
                 entry_offset_in_data = i * 4
                 b, g, r, _ = struct.unpack_from('<BBBB', data, entry_offset_in_data)
                 palette.append(qRgb(r, g, b))

            # --- Pixel Data Loading (from 'data' argument AFTER the palette) ---
            # The actual pixel data starts in 'data' after the palette bytes
            actual_pixel_data = data[palette_end_index_in_data:]

            # Check consistency: pixel data should start at data_offset in the file
            pixel_data_start_offset_in_file = header_len + palette_end_index_in_data
            if pixel_data_start_offset_in_file != data_offset:
                 print(f"Warning: Calculated pixel data start in file ({pixel_data_start_offset_in_file}) "
                       f"does not match header data_offset ({data_offset}). Using calculated offset.")

            padding = (4 - (width % 4)) % 4
            row_size = width + padding
            expected_pixel_data_size = row_size * abs_height
            if len(actual_pixel_data) < expected_pixel_data_size:
                 raise ValueError(f"Insufficient pixel data for 8-bit BMP after palette. Expected {expected_pixel_data_size}, got {len(actual_pixel_data)}")

            image = QImage(width, abs_height, QImage.Format_Indexed8)
            image.setColorCount(num_palette_colors)
            image.setColorTable(palette)

            for y in range(abs_height):
                src_y = y if top_down else abs_height - 1 - y
                row_start = src_y * row_size # Index relative to start of actual_pixel_data
                for x in range(width):
                    pixel_index = row_start + x
                    if pixel_index < len(actual_pixel_data):
                        palette_index = actual_pixel_data[pixel_index]
                        if palette_index < len(palette): # Check index validity
                           image.setPixel(x, y, palette_index)
                        else:
                           image.setPixel(x,y, 0) # Set to color 0 if index out of bounds
                    # else: handle short data within row? (optional)

        else:
            raise ValueError(f"Unsupported BMP bit depth: {bit_depth}")

        if image is None or image.isNull():
             raise ValueError("Failed to create QImage from BMP data.")

        return QPixmap.fromImage(image)