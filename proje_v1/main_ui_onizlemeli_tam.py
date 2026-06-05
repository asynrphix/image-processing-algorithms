import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from arayuz import Ui_MainWindow
from onizleme_penceresi import OnizlemePenceresi

from PyQt5.QtGui import QPixmap, QImage, qRgb

from binary_donusum import bmp_oku, bmp_kaydet, binary_donusum
from gri_donusum import gri_donusum
from histogram_germe import histogram_germe
from sobel import sobel_kenar_bulma
from parlaklik_artirma import parlaklik_artir
from gauss_konvolusyon import gauss_konvolusyon
from zoom import goruntu_yakinlastir
from gurultu_filtre import gürültü_ekle, mean_filtre, median_filtre
from morfolojik import genislet, asindir, acma, kapama
from goruntu_dondurme import goruntu_dondurme
from goruntu_kirpma import goruntu_kirp
from renk_uzayi_donusumu import rgb_to_gray_donusum
from aritmetik_islem import goruntu_topla, goruntu_carp
from adaptif_esikleme import adaptif_esikleme
from blurring import blurring
from histogram_genisletme import histogram_genisletme 
from gray_to_rgb import gray_to_rgb

class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.header = None
        self.data = None
        self.data2 = None
        self.orijinal_data = None

        self.ui.btnYukle.clicked.connect(self.gorsel_yukle)
        self.ui.btnBinary.clicked.connect(lambda: self.islem_uygula(binary_donusum, "Binary Dönüşüm"))
        self.ui.btnGri.clicked.connect(lambda: self.islem_uygula(gri_donusum, "Gri Dönüşüm"))
        self.ui.btnHistogram.clicked.connect(lambda: self.islem_uygula(histogram_genisletme, "Histogram Germe")) 
        self.ui.btnHistogramGenisletme.clicked.connect(lambda: self.islem_uygula(histogram_germe, "Histogram Genişletme"))
        self.ui.btnSobel.clicked.connect(lambda: self.islem_uygula(sobel_kenar_bulma, "Sobel Kenar Bulma"))
        self.ui.btnParlaklik.clicked.connect(lambda: self.islem_uygula(lambda h, d: parlaklik_artir(h, d, 40), "Parlaklık Artırma"))
        self.ui.btnGauss.clicked.connect(lambda: self.islem_uygula(gauss_konvolusyon, "Gauss Konvolüsyon"))
        self.ui.btnZoom.clicked.connect(lambda: self.islem_uygula_zoom(2.0))
        self.ui.btnGurultu.clicked.connect(lambda: self.islem_uygula(lambda h, d: gürültü_ekle(h, d, 0.05), "Gürültü Ekleme"))
        self.ui.btnMean.clicked.connect(lambda: self.islem_uygula(mean_filtre, "Mean Filtre"))
        self.ui.btnMedian.clicked.connect(lambda: self.islem_uygula(median_filtre, "Median Filtre"))
        self.ui.btnDilate.clicked.connect(lambda: self.islem_uygula(genislet, "Morfolojik Genişletme"))
        self.ui.btnErode.clicked.connect(lambda: self.islem_uygula(asindir, "Morfolojik Aşındırma"))
        self.ui.btnAcma.clicked.connect(lambda: self.islem_uygula(acma, "Morfolojik Açma"))
        self.ui.btnKapama.clicked.connect(lambda: self.islem_uygula(kapama, "Morfolojik Kapama"))
        self.ui.btnRotate.clicked.connect(lambda: self.islem_uygula(goruntu_dondurme, "Görüntü Döndürme"))
        self.ui.btnCrop.clicked.connect(lambda: self.kirp())
        self.ui.btnRenk.clicked.connect(lambda: self.islem_uygula(rgb_to_gray_donusum, "RGB'den Griye Dönüşüm"))
        self.ui.btnAdaptif.clicked.connect(lambda: self.islem_uygula(adaptif_esikleme, "Adaptif Eşikleme"))
        self.ui.btnBlur.clicked.connect(lambda: self.islem_uygula(blurring, "Blurring"))
        self.ui.btnTopla.clicked.connect(self.topla_uygula)
        self.ui.btnCarp.clicked.connect(self.carp_uygula)
        self.ui.btnKaydet.clicked.connect(self.sonucu_kaydet)
        self.ui.btnRenkGraytoRGB.clicked.connect(lambda: self.islem_uygula(gray_to_rgb, "Gray to RGB Dönüşüm"))

    def gorsel_yukle(self):
        dosya, _ = QFileDialog.getOpenFileName(self, "Görsel Seç", "", "BMP Files (*.bmp)")
        if dosya:
            self.header, self.data = bmp_oku(dosya)
            self.orijinal_data = bytearray(self.data)
            self.orijinal_header = bytearray(self.header)
            self.gorsel_goster()

    def islem_uygula(self, fonksiyon, baslik, **kwargs):
        try:
            sonuc = fonksiyon(self.header, self.data, **kwargs)
            if isinstance(sonuc, tuple) and len(sonuc) == 2:
                self.header, self.data = sonuc
            else:
                self.data = sonuc

            self.gorsel_goster()
            self.onizleme_goster(self.orijinal_header, self.orijinal_data, self.header, self.data, baslik)
        except Exception as e:
            print("İşlem hatası:", e)

    

    def islem_uygula_zoom(self, oran):
        if self.data:
            self.header, self.data = goruntu_yakinlastir(self.header, self.data, oran)
            self.gorsel_goster()
            self.onizleme_goster(self.orijinal_header, self.orijinal_data, self.header, self.data, "Yakınlaştırma")

    def kirp(self):
        if self.data:
            self.header, self.data = goruntu_kirp(self.header, self.data, 50, 50, 200, 200)
            self.gorsel_goster()
            self.onizleme_goster(self.orijinal_header, self.orijinal_data, self.header, self.data, "Görüntü Kırpma")

    def topla_uygula(self):
        yol2, _ = QFileDialog.getOpenFileName(self, "İkinci Görsel", "", "BMP Files (*.bmp)")
        if yol2:
            _, self.data2 = bmp_oku(yol2)
            self.data = goruntu_topla(self.header, self.data, self.data2)
            self.gorsel_goster()
            self.onizleme_goster(self.header, self.orijinal_data, self.data, "Görüntü Toplama")

    def carp_uygula(self):
        yol2, _ = QFileDialog.getOpenFileName(self, "İkinci Görsel", "", "BMP Files (*.bmp)")
        if yol2:
            _, self.data2 = bmp_oku(yol2)
            self.data = goruntu_carp(self.header, self.data, self.data2)
            self.gorsel_goster()
            self.onizleme_goster(self.header, self.orijinal_data, self.data, "Görüntü Çarpma")

    def sonucu_kaydet(self):
        if self.data:
            yol, _ = QFileDialog.getSaveFileName(self, "Kaydet", "", "BMP Files (*.bmp)")
            if yol:
                bmp_kaydet(yol, self.header, self.data)

    def gorsel_goster(self):
        genislik = int.from_bytes(self.header[18:22], byteorder='little')
        yukseklik = int.from_bytes(self.header[22:26], byteorder='little')
        padding = (4 - (genislik * 3) % 4) % 4
        satir_boyutu = genislik * 3 + padding
        image = QImage(genislik, yukseklik, QImage.Format_RGB32)

        for y in range(yukseklik):
            for x in range(genislik):
                i = y * satir_boyutu + x * 3
                if i + 2 < len(self.data):
                    b = self.data[i]
                    g = self.data[i + 1]
                    r = self.data[i + 2]
                    image.setPixel(x, yukseklik - 1 - y, qRgb(r, g, b))

        pixmap = QPixmap.fromImage(image)
        self.ui.label.setPixmap(pixmap.scaled(self.ui.label.size(), Qt.KeepAspectRatio))
        self.ui.label.setScaledContents(False)
        self.ui.label.setAlignment(Qt.AlignCenter)

    def onizleme_goster(self, orijinal_header, orijinal_data, islenmis_header, islenmis_data, baslik):
        OnizlemePenceresi(orijinal_header, orijinal_data, islenmis_header, islenmis_data, baslik).exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec_())
