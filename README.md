# Görüntü İşleme Projesi

BMP tabanlı görüntü işleme işlevlerini PyQt5 tabanlı bir masaüstü arayüz ile sunan bir projedir. 

---

## Hızlı Başlangıç ✅

1. Proje dizinine gidin:
```bash
cd ~/Downloads/goruntu_isleme_projesi/proje_v1
```
2. Sanal ortam oluşturun ve etkinleştirin (önerilir):
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. Gerekli paketi kurun:
```bash
pip install PyQt5
```
4. Uygulamayı çalıştırın:
```bash
python3 main_ui_onizlemeli_tam.py
```

> Arayüz `.bmp` formatındaki görsellerle çalışır; görsellerinizi bu formatta kullanın.

---

## Özellikler ✨

- Görsel yükleme ve önizleme (.bmp)
- Gri dönüşümü, Binary dönüşümü
- Histogram germe & genişletme
- Gauss konvolüsyon, blurring
- Morfolojik işlemler (genişletme, aşındırma, açma, kapama)
- Gürültü ekleme, mean/median filtre
- Görüntü döndürme, kırpma, yakınlaştırma
- Görüntü kaydetme (.bmp)

---

## Proje yapısı 📁

- `proje_v1/` — tüm kaynak kodu
  - `main_ui_onizlemeli_tam.py` — uygulamanın giriş noktası (UI entegrasyonu ve işlemler)
  - `arayuz.py` — PyQt5 tarafından üretilmiş arayüz sınıfı
  - `*.py` — görüntü işleme fonksiyonları (ör. `binary_donusum.py`, `gri_donusum.py`)
  - `icons_gui/`, `images/` — ikon ve örnek görseller

---

## Gereksinimler 🧩

- Python 3.8+
- PyQt5


---

## Kullanım İpuçları & Hatalar

- Eğer `ModuleNotFoundError: No module named 'PyQt5'` hatası alırsanız:
```bash
pip install PyQt5
```
- Dosya bulunamıyor hataları alıyorsanız, uygulamayı `proje_v1` dizininden çalıştırdığınızdan emin olun ( `python3 main_ui_onizlemeli_tam.py`).

<img width="1091" height="939" alt="image" src="https://github.com/user-attachments/assets/94f7a9c6-b623-4c1b-ad8b-ad6195709950" /> <img width="1083" height="919" alt="Ekran görüntüsü 2025-05-03 183706" src="https://github.com/user-attachments/assets/f7f36b15-a2c9-40aa-8053-98bed660ba24" />   <img width="972" height="548" alt="Ekran görüntüsü 2025-05-04 101951" src="https://github.com/user-attachments/assets/1eef5773-9d87-4380-9832-87a04f4bba5c" />   <img width="1006" height="877" alt="image" src="https://github.com/user-attachments/assets/8375ef30-c051-4df4-8a24-9bcfcf72b3ae" />  ![WhatsApp Image 2025-05-03 at 22 44 25](https://github.com/user-attachments/assets/2cf2de26-9dfd-47a2-9976-cb81997297d3)  <img width="1090" height="929" alt="Ekran görüntüsü 2025-05-03 201105" src="https://github.com/user-attachments/assets/28226729-2167-4481-a790-a32242698928" />   ![WhatsApp Image 2025-05-03 at 19 55 37](https://github.com/user-attachments/assets/766c926f-111d-4342-86bc-93b81f0f0e4d)







