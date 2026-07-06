import cv2
import numpy as np
import easyocr
import sys
import glob

# Kullanıcıdan resim dosyası alıyoruz, eğer yoksa klasördeki ilk resmi kullanıyoruz
if len(sys.argv) > 1:
    image_path = sys.argv[1]
else:
    images = glob.glob("*.jpg") + glob.glob("*.jpeg") + glob.glob("*.png")
    if not images:
        print("Klasorde resim bulunamadi. Bir .jpg/.png dosyasi ekleyin.")
        sys.exit()
    image_path = images[0]
    print("Kullanilan goruntu:", image_path)

img = cv2.imread(image_path)
if img is None:
    print("Goruntu okunamadi:", image_path)
    sys.exit()

# Resmi yeniden boyutlandırıyoruz çünkü çok büyük resimlerde işlem yavaş oluyor
target_width = 600
scale = target_width / img.shape[1]
img = cv2.resize(img, (target_width, int(img.shape[0] * scale)))
img_width = img.shape[1]
cv2.imwrite("1_original.jpg", img)

# Griye çeviriyoruz çünkü renkler OCR için gerekli değil
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("2_gray.jpg", gray)

# Gürültüyü azaltmak için bulanıklaştırıyoruz
blur = cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imwrite("3_blur.jpg", blur)

# Kenarları bulmak için Canny algoritmasını kullanıyoruz
edged = cv2.Canny(blur, 30, 200)
cv2.imwrite("4_canny.jpg", edged)

# Kenarları bulduktan sonra şekilleri tespit ediyoruz
contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]

plate_contour = None

# Plaka genelde dikdörtgen şeklinde olduğu için dört köşeli şekilleri arıyoruz
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    (x, y, w, h) = cv2.boundingRect(approx)
    aspect_ratio = w / float(h)

    dogru_oran = 2.5 < aspect_ratio < 5.5

    # Plaka boyutları genelde resmin %15 ile %60'ı arasında oluyor
    dogru_genislik = (0.15 * img_width) < w < (0.60 * img_width)

    # Eğer dört köşeli ve doğru oranlarda bir şekil bulursak plaka olarak kabul ediyoruz
    if len(approx) == 4 and dogru_oran and dogru_genislik:
        plate_contour = approx
        break

# Eğer plaka bölgesi bulunamadıysa kullanıcıya mesaj verip çıkıyoruz
if plate_contour is None:
    print("Plaka bolgesi tespit edilemedi. Farkli bir goruntu deneyin.")
    sys.exit()

# Bulduğumuz plaka bölgesini yeşil çerçeveyle işaretliyoruz
img_contour = img.copy()
cv2.drawContours(img_contour, [plate_contour], -1, (0, 255, 0), 3)
cv2.imwrite("5_contour.jpg", img_contour)

# Sadece plaka kısmını orijinal fotoğraftan kesip alıyoruz
(x, y, w, h) = cv2.boundingRect(plate_contour)
plate = img[y:y + h, x:x + w]
cv2.imwrite("6_plate.jpg", plate)

# Plaka kısmını OCR için hazırlıyoruz
plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
plate_gray = cv2.resize(plate_gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
_, plate_thresh = cv2.threshold(plate_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# OCR'ı çalıştırıyoruz, sadece harf ve rakamları okumaya izin veriyoruz
reader = easyocr.Reader(['en'])
result = reader.readtext(
    plate_thresh,
    allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
)

result = sorted(result, key=lambda r: r[0][0][0])

parts = []
for (bbox, txt, conf) in result:
    # Sadece güvenilir sonuçları alıyoruz, güven puanı 0.3'ten düşük olanları atıyoruz
    if conf > 0.3:
        parts.append(txt.strip())

text = ' '.join(parts)

print("-" * 30)
print("Okunan Plaka:", text if text else "(metin okunamadi)")
print("-" * 30)

# Görüntüleri ekranda gösteriyoruz
cv2.imshow("Orijinal", img)
cv2.imshow("Grayscale", gray)
cv2.imshow("Blur", blur)
cv2.imshow("Canny", edged)
cv2.imshow("Plaka Tespiti", img_contour)

plate_buyuk = cv2.resize(plate, None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
cv2.imshow("Kirpilan Plaka", plate_buyuk)

cv2.waitKey(0)
cv2.destroyAllWindows()