import requests # Web sayfalarına HTTP istekleri göndermek için kullanılan kütüphane.
from bs4 import BeautifulSoup # Çekilen HTML içeriğini ayrıştırmak (parse) ve üzerinde gezinmek için kullanılan kütüphane.

# Hedef web sitesinin URL'sini belirliyoruz. Bu örnekte Sağlık Bakanlığı'nın Covid-19 bilgilendirme sayfası.
url = "https://covid19.saglik.gov.tr/" 

# Belirlenen URL'ye GET isteği gönderiyoruz. Bu, sayfayı ziyaret etmek gibidir.
response = requests.get(url) 

# Sunucudan gelen yanıt kodunu kontrol ediyoruz. 
# 200 kodu, isteğin başarılı olduğunu ve sayfanın bulunduğunu ifade eder.
if response.status_code == 200:
    print("Siteden Veri Çekilebilir")
else:
    # Eğer 200 harici bir kod dönerse (örn: 404, 500 vb.), bir sorun olduğunu ve verinin çekilemediğini belirtiriz.
    print(f"Siteden Veri Çekilemez. Hata Kodu: {response.status_code}")

# Sayfanın HTML içeriğini (response.content) alıp BeautifulSoup nesnesine dönüştürüyoruz.
# "html.parser" parametresi, içeriğin HTML formatında ayrıştırılacağını belirtir.
soup = BeautifulSoup(response.content, "html.parser")

# Sağlık bakanlığı siteyi güncellediği veya verileri farklı şekilde yüklediği için (örn. JavaScript ile) tbody doğrudan HTML içinde bulunmayabilir veya isimleri değişmiş olabilir. 
# Not: find("tbody") None dönerse find_all("tr") çalışırken AttributeError verir. Bu yüzden try-except bloğu ile bu durumu güvene alıyoruz.
try:
    # Sayfadaki ilk <tbody> (tablo gövdesi) etiketini bulur ve içindeki tüm <tr> (tablo satırı) etiketlerini liste olarak alır.
    # Her bir <tr> etiketi üzerinde döngü ile geziniriz.
    for i in soup.find("tbody").find_all("tr"):
        print("----------") # Satırları birbirinden ayırmak için kullanılır
        print(i.text) # <tr> etiketinin içindeki tüm metin içeriğini temiz bir şekilde ekrana yazdırır.
except AttributeError:
    # Eğer sitede 'tbody' etiketi bulunamazsa programın çökmesini engelleriz ve bilgi veririz.
    print("Sitede 'tbody' etiketi bulunamadı! Sayfa yapısı değişmiş veya veriler JavaScript ile yükleniyor olabilir.")