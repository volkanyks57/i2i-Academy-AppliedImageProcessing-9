# i2i-Academy-AppliedImageProcessing-9
  OpenCV ve EasyOCR ile klasik görüntü işleme yöntemleri kullanan Otomatik Plaka Tanıma (ALPR) modülü

# Özet
  Bu projede klasik görüntü işleme yöntemleri kullanılarak bir Otomatik Plaka Tanıma 
  modülü geliştirildi. Deep learning kullanmadan, sadece OpenCV ile araba fotoğrafındaki
  plaka bölgesi matematiksel olarak tespit edilip kırpıldı ve EasyOCR ile plaka metni 
  okunarak konsola yazdırıldı.

# Tamamlanan Görevler
  - OpenCV ile görüntü yüklendi ve standart boyuta ölçeklendirildi
  - Görüntü gri tonlamaya (grayscale) çevrildi
  - bilateralFilter ile gürültü azaltıldı (blur)
  - Canny Edge Detection ile kenarlar tespit edildi
  - Contour analizi ile plakaya benzeyen dikdörtgen bölge bulundu
  - Tespit edilen plaka bölgesi orijinal görüntüden kırpıldı
  - Kırpılan plaka threshold ile temizlenip EasyOCR'a verildi
  - Okunan plaka metni konsola yazdırıldı

# Kullanılan Teknolojiler
  - Python 3.11
  - OpenCV
  - EasyOCR
  - NumPy
