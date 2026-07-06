# i2i-Academy-AppliedImageProcessing-9
OpenCV ve EasyOCR ile klasik goruntu isleme yontemleri kullanan Otomatik Plaka Tanima (ALPR) modulu

# Özet
  Bu projede klasik goruntu isleme yontemleri kullanilarak bir Otomatik Plaka Tanima
  modulu gelistirildi. Deep learning kullanmadan, sadece OpenCV ile araba fotografindaki
  plaka bolgesi matematiksel olarak tespit edilip kirpildi ve EasyOCR ile plaka metni
  okunarak konsola yazdirildi.

# Tamamlanan Görevler
  - OpenCV ile goruntu yuklendi ve standart boyuta olceklendirildi
  - Goruntu gri tonlamaya (grayscale) cevrildi
  - bilateralFilter ile gurultu azaltildi (blur)
  - Canny Edge Detection ile kenarlar tespit edildi
  - Contour analizi ile plakaya benzeyen dikdortgen bolge bulundu
  - Tespit edilen plaka bolgesi orijinal goruntuden kirpildi
  - Kirpilan plaka threshold ile temizlenip EasyOCR'a verildi
  - Okunan plaka metni konsola yazdirildi

# Kullanılan Teknolojiler
  - Python 3.11
  - OpenCV
  - EasyOCR
  - NumPy
