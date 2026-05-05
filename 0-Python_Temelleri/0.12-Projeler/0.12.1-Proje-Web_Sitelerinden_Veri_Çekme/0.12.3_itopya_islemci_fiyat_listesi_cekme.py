# =============================================================================
# PROJE: İTOPYA İŞLEMCİ FİYAT LİSTESİ ÇEKME (Web Scraping)
# =============================================================================
# Bu script, Türkiye'nin önde gelen bilgisayar donanım e-ticaret sitesi olan
# itopya.com'dan işlemci (CPU) ürünlerinin güncel fiyat listesini otomatik
# olarak çekmektedir.
#
# AMAÇ:
#   - Web scraping (web kazıma) tekniklerini gerçek bir e-ticaret sitesi
#     üzerinde uygulamak.
#   - requests ve BeautifulSoup kütüphanelerinin birlikte kullanımını
#     pekiştirmek.
#   - HTML DOM yapısını analiz ederek hedef verileri (ürün adı, fiyat, link)
#     seçici (selector) ile çekmeyi öğrenmek.
#
# KULLANILAN KÜTÜPHANELERİN KURULUMU:
#   pip install requests beautifulsoup4
#
# ÇALIŞTIRILMASI:
#   python 0.12.3_itopya_islemci_fiyat_listesi_cekme.py
# =============================================================================

# --- KÜTÜPHANE İMPORTLARI ---

import requests # Web sayfalarına HTTP istekleri (GET, POST vb.) göndermek için kullanılan kütüphane.
                 # Tarayıcı gibi bir URL'ye bağlanıp sayfanın HTML içeriğini indirmemizi sağlar.

from bs4 import BeautifulSoup # BeautifulSoup: İndirilen HTML içeriğini ayrıştırıp (parse edip)
                               # içindeki etiketleri, sınıfları ve verileri kolayca bulmamızı
                               # sağlayan güçlü bir HTML/XML parser kütüphanesidir.
                               # bs4 (beautifulsoup4) paketinin içinden import edilir.

# --- HEDEF URL'YE HTTP İSTEĞİ GÖNDERME ---

# itopya.com'un işlemci kategorisi sayfasının URL'sine HTTP GET isteği gönderiyoruz.
# "_k8" parametresi, itopya'nın URL yapısında işlemci kategorisini temsil eder.
# requests.get() fonksiyonu, sunucuya bir GET isteği gönderir ve dönen yanıtı (response) bir nesne olarak döndürür.
# Bu nesne içinde; durum kodu (status_code), içerik (content), başlıklar (headers) gibi bilgiler bulunur.
url = requests.get("https://www.itopya.com/islemci_k8")

# --- BAĞLANTI DURUMU KONTROLÜ ---

# Sunucudan dönen HTTP durum kodunu kontrol ediyoruz.
# Durum Kodları:
#   200 -> OK: İstek başarılı, sayfa sorunsuz yüklendi.
#   403 -> Forbidden: Sunucu isteği reddetti (bot koruması, yetki eksikliği vb.).
#   404 -> Not Found: İstenen sayfa bulunamadı (URL yanlış veya sayfa kaldırılmış olabilir).
#   500 -> Internal Server Error: Sunucu tarafında bir hata oluştu.
#   503 -> Service Unavailable: Sunucu geçici olarak hizmet veremiyor.
if url.status_code == 200:
    print("Siteden Veri Çekilebilir")
else:
    print("Siteden Veri Çekilemez")

# --- HTML İÇERİĞİNİ PARSE ETME (AYRIŞTIRMA) ---

# Sunucudan dönen ham HTML içeriğini (url.content) BeautifulSoup nesnesine dönüştürüyoruz.
# Parametreler:
#   url.content  -> Sayfanın ham HTML bayt içeriği. (.text yerine .content kullanmak,
#                    karakter kodlaması sorunlarını önlemek için tercih edilir.)
#   "html.parser" -> Python'un yerleşik HTML ayrıştırıcısı. Harici bir parser (lxml, html5lib)
#                    kurmadan kullanılabilir. Alternatifler:
#                    - "lxml": Daha hızlı ama ayrıca kurulum gerektirir.
#                    - "html5lib": En toleranslı parser, bozuk HTML'leri bile düzeltir.
# Bu adımdan sonra 'soup' nesnesi üzerinde find(), find_all() gibi arama metotlarını kullanabiliriz.
soup = BeautifulSoup(url.content, "html.parser")

# --- ÜRÜN VERİLERİNİ ÇEKME (ANA DÖNGÜ) ---

# Aşağıdaki satır, itopya'nın ürün listeleme sayfasındaki HTML yapısını analiz ederek
# her bir ürün kartının verilerini tek tek çekmektedir.
#
# HTML YAPISI (Kısaltılmış):
# <div class="product_product_List">         <- Tüm ürünleri kapsayan ana konteyner
#     <div class="product-block">            <- Her bir ürün kartı
#         <div class="product-block-top">    <- Ürün başlık alanı
#             <h2><a>Ürün Adı</a></h2>       <- Ürün başlığı (h2 > a etiketinde)
#         </div>
#         <div class="product-image">        <- Ürün görseli alanı
#             <a href="/urun-linki">         <- Ürün detay sayfasının linki
#         </div>
#         <span class="product-price">       <- Ürün fiyat bilgisi
#             54.999,00 TL
#         </span>
#     </div>
#     ... (diğer ürün kartları)
# </div>
#
# ADIM ADIM AÇIKLAMA:
# 1) soup.find("div", {"class": "product_product_List"})
#    -> Sayfadaki "product_product_List" sınıfına sahip İLK <div> etiketini bulur.
#       Bu, tüm ürün kartlarını kapsayan ana konteynerdir.
#
# 2) .find_all("div", {"class": "product-block"})
#    -> Bu konteyner içindeki "product-block" sınıfına sahip TÜM <div> etiketlerini
#       bir Python listesi olarak döndürür. Her eleman bir ürün kartıdır.
#
# 3) for i in ... -> Her bir ürün kartı (product-block) üzerinde döngü kurulur.

for i in soup.find("div",{"class": "product_product_List"}).find_all("div",{"class": "product-block"}):

    # --- ÜRÜN BAŞLIĞINI ÇEKME ---
    # i.find("div", {"class": "product-block-top"}) -> Ürün kartı içindeki "product-block-top" sınıflı div'i bulur.
    # .h2   -> Bu div içindeki <h2> etiketine erişir (ürün başlık etiketi).
    # .a    -> <h2> içindeki <a> (link) etiketine erişir.
    # .text -> <a> etiketinin içindeki saf metin içeriğini (HTML etiketleri olmadan) döndürür.
    # .strip() -> Metnin başındaki ve sonundaki boşluk, tab, yeni satır gibi gereksiz karakterleri temizler.
    baslik_al = i.find("div", {"class": "product-block-top"}).h2.a.text.strip()

    # --- ÜRÜN FİYATINI ÇEKME ---
    # i.find("span", {"class": "product-price"}) -> Ürün kartı içindeki "product-price" sınıflı <span> etiketini bulur.
    # .text.strip() -> Fiyat metnini alır ve gereksiz boşlukları temizler.
    # Not: Bazı ürünlerde "Sepette X TL" gibi indirimli fiyat bilgisi de bu alanda görünebilir.
    #       Bu durumda text içinde birden fazla satır (fiyat + sepet fiyatı) gelebilir.
    fiyat_al = i.find("span", {"class": "product-price"}).text.strip()

    # --- ÜRÜN LİNKİNİ ÇEKME ---
    # i.find("div", {"class": "product-image"}) -> Ürün kartındaki "product-image" sınıflı div'i bulur.
    # .a -> Bu div içindeki <a> etiketine erişir.
    # .get("href") -> <a> etiketinin "href" özniteliğindeki (attribute) URL yolunu (path) çeker.
    #                 Not: .get() metodu, öznitelik bulunamazsa hata fırlatmaz, None döndürür.
    #                 Alternatif olarak a["href"] kullanılabilir ama öznitelik yoksa KeyError fırlatır.
    # "https://www.itopya.com/" + ... -> href değeri göreceli (relative) bir yol döndürdüğü için,
    #                                    tam URL oluşturmak adına site ana adresi başına eklenir.
    link = "https://www.itopya.com/" + i.find("div", {"class": "product-image"}).a.get("href")

    # --- SONUÇLARI EKRANA YAZDIRMA ---
    # f-string (formatted string literal) kullanarak ürün bilgilerini düzenli bir şekilde yazdırıyoruz.
    # \n -> Yeni satır (newline) karakteri. Her bilgi ayrı satırda gösterilir.
    # Çıktı formatı:
    #   Ürün Adı: AMD Ryzen 9 9950X3D ...
    #   Ürün Fiyatı: 54.999,00 TL
    #   Ürün Linki: https://www.itopya.com/...
    print(f"\nÜrün Adı: {baslik_al}\nÜrün Fiyatı: {fiyat_al}\nÜrün Linki: {link}\n")

    # Her ürün kartı arasına 50 adet tire (-) işaretinden oluşan bir ayraç çizgisi yazdırıyoruz.
    # Bu, konsol çıktısında ürünlerin birbirinden kolayca ayırt edilmesini sağlar.
    # "-" * 50 -> Python'da string çarpımı: "-" karakterini 50 kere tekrarlar.
    print("-" * 50)

# --- PROGRAMIN AÇIK KALMASI ---
# input("") -> Kullanıcıdan herhangi bir girdi bekler (Enter tuşuna basılmasını bekler).
# Bu satır, programın doğrudan çift tıklayarak (.py dosyasına) çalıştırıldığı durumlarda
# komut satırı penceresinin hemen kapanmasını önlemek için kullanılır.
# IDE (VS Code, PyCharm vb.) içinden çalıştırıldığında bu satıra gerek yoktur,
# çünkü IDE terminali zaten açık kalır.
input("")