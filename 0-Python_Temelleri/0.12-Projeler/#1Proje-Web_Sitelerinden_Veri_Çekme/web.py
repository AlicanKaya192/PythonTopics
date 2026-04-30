import requests # Web sayfalarına HTTP istekleri göndermek için kullanılan kütüphane.
from bs4 import BeautifulSoup # Çekilen HTML içeriğini ayrıştırmak (parse) ve üzerinde gezinmek için kullanılan kütüphane.

# Veri çekme (Web Scraping) pratiği için örnek olarak kullanılan hedef URL.
url = "https://alican-kaya.com/" 

# Hedef URL'ye HTTP GET isteği gönderiliyor ve gelen cevap (response) değişkenine atanıyor.
response = requests.get(url)

# İstek sonucunun durum kodunu kontrol ediyoruz. 
# 200: Başarılı, 403: Erişim Engellendi (Yasak), 404: Bulunamadı, 500: Sunucu Hatası gibi anlamlara gelir.
if response.status_code == 200:
    print("Siteden Veri Çekilebilir")
else:
    print(f"Siteden Veri Çekilemez. Hata Kodu: {response.status_code}")


# Sayfanın kaynak kodunu (HTML içeriğini) BeautifulSoup ile işlenebilir (parse) hale getiriyoruz.
soup = BeautifulSoup(response.content, "html.parser")

# Sitenin <title> etiketini tamamıyla (<title>Başlık</title> şeklinde) yazdırır.
print(soup.title) 

# HTML kodlarını daha okunaklı, girintili (indentation) bir şekilde formatlayıp yazdırır. Kod yapısını anlamak için faydalıdır.
print(soup.prettify())


# --- EXTRA BİLGİLER VE YORUMLAR ---
# Aşağıdaki satırlar BeautifulSoup'un sunduğu farklı veri çekme yöntemlerini gösterir (Yorum satırı olarak bırakılmıştır):
# soup.head.title          -> Sadece head içindeki title etiketini getirir.
# soup.head.title.text     -> Title etiketinin sadece içindeki yazıyı/metni (text) getirir.
# soup.body                -> Sayfanın tüm <body> (içerik) kısmını getirir.
# soup.find("p")           -> Sayfadaki karşılaştığı İLK <p> (paragraf) etiketini getirir.
# soup.find("p").text      -> Karşılaştığı İLK paragrafın sadece metin kısmını getirir.
# soup.find_all("p")       -> Sayfadaki TÜM <p> etiketlerini bir Python listesi olarak getirir.
# soup.find_all("p")[0].text -> Tüm p etiketleri listesinden ilk elemanın metnini getirir (liste döndürdüğü için .text doğrudan kullanılamaz).
# soup.find_all("h2")      -> Sayfadaki tüm <h2> (ikinci seviye başlık) etiketlerini liste olarak döndürür.

# Tüm <html> içeriğini bir değişkene atıyoruz.
yazdir = soup.html
print("-" * 80) # Konsolda çıktılar karışmasın diye 80 adet tire işareti ile ayraç çiziyoruz.

# html içindeki tüm alt elemanları döngüyle tek tek yazdırıyor (genellikle tüm sayfa metnini alt alta yazar)
for i in yazdir:
    print(i.text)

# Sınıfı (class) "h-28" olan İLK <div> etiketini bulur ve içindeki metni çeker.
# Not: Eğer sayfada böyle bir element yoksa "None" dönecek ve sonrasında ".text" çağrıldığı için AttributeError verecektir. Bu yüzden try-except bloğu eklendi.
try:
    div_cek = soup.find("div", {"class": "h-28"})
    print(div_cek.text)
    
    # get("href") kullanımı genellikle link (a) etiketlerinde olur. Eğer div'de bir href özniteliği varsa onu getirir.
    # DİKKAT: .text dedikten sonra dönen değer string olacağı için .get() metodu kullanılamaz. 
    # Bu yüzden yukarıda div_cek değişkenini soup objesi olarak tutup, metni yazdırırken .text dedik. Linki çekerken .get() kullandık.
    print(div_cek.get("href"))
except AttributeError:
    print("Sınıfı 'h-28' olan bir <div> elementi bulunamadı.")


# Sınıfı "flex items-start gap-2 text-sm text-white/90" olan İLK <li> (liste elemanı) etiketini bulur.
try:
    li_cek = soup.find("li", {"class": "flex items-start gap-2 text-sm text-white/90"}).text
    print(li_cek)
except AttributeError:
    print("Belirtilen sınıfa ait bir <li> elementi bulunamadı.")
