# 🖼️ Görüntü İşleme Uygulaması

Python ve PyQt5 ile geliştirilmiş, 20'den fazla görüntü işleme algoritmasını tek arayüzde sunan masaüstü uygulaması. Selçuk Üniversitesi Görüntü İşleme dersi kapsamında geliştirilmiştir.

---

## 📸 Ekran Görüntüsü

![Arayüz](screenshots/1.png)

---

## ✨ Özellikler

- **Renk Dönüşümleri** — Gri dönüşüm, Binary dönüşüm, RGB↔GRAY renk uzayı dönüşümü
- **Geometrik İşlemler** — Görüntü döndürme, kırpma, yakınlaştırma (zoom)
- **Aritmetik İşlemler** — Görüntü toplama ve çarpma
- **Histogram İşlemleri** — Histogram germe ve genişletme
- **Filtreleme** — Gauss konvolüsyon, Blurring, Median filtre, Mean filtre
- **Gürültü** — Salt & Pepper gürültü ekleme
- **Morfolojik İşlemler** — Erozyon (Aşındırma), Genişletme, Açma, Kapama
- **Kenar Tespiti** — Sobel kenar bulma
- **Diğer** — Parlaklık artırma, Adaptif eşikleme
- **Sonucu Kaydet** — İşlenmiş görseli dışa aktarma

---

## 🛠️ Teknolojiler

- **Dil:** Python
- **Arayüz:** PyQt5 (Qt Designer ile tasarlanmış .ui dosyası)
- **Görüntü İşleme:** OpenCV
- **Sayısal İşlem:** NumPy

---

## 🚀 Kurulum

```bash
# Bağımlılıkları yükle
pip install PyQt5 opencv-python numpy

# Uygulamayı çalıştır
cd proje_v1
python arayuz.py
```

---

## 📁 Proje Yapısı

```
proje_v1/
├── arayuz.py                  # Ana uygulama ve arayüz mantığı
├── arayuz_guncel.ui           # Qt Designer arayüz dosyası
├── morfolojik.py              # Morfolojik işlemler
├── sobel.py                   # Kenar tespiti
├── gauss_konvolusyon.py       # Gauss filtresi
├── gurultu_filtre.py          # Gürültü filtreleme
├── histogram_germe.py         # Histogram germe
├── histogram_genisletme.py    # Histogram genişletme
├── adaptif_esikleme.py        # Adaptif eşikleme
├── aritmetik_islem.py         # Görüntü aritmetiği
└── ...                        # Diğer algoritma modülleri
test_görselleri/               # Test için örnek görseller
icons_gui/                     # Arayüz ikonları
```
