# ==============================================================================
# LangChain Döküman Yükleyiciler (Document Loaders)
# ==============================================================================
# Bu dosya, LangChain'in en önemli bileşenlerinden biri olan döküman yükleyicileri
# (document loaders) göstermektedir.
#
# Neden döküman yükleyiciler önemli?
# ----------------------------------
# Gerçek dünya uygulamalarında, yapay zeka modellerimize besleyeceğimiz veriler
# farklı kaynaklardan ve farklı formatlarda gelir: web sayfaları, PDF dosyaları,
# Excel tabloları, veritabanları, API'ler vb.
#
# LangChain'in loader'ları bu kaynakların hepsini standart bir "Document" formatına
# dönüştürür. Bu sayede aynı pipeline'ı farklı veri kaynakları için kullanabilirsiniz.
#
# Document objesi iki ana bileşenden oluşur:
# 1. page_content: Asıl metin içeriği
# 2. metadata: Kaynak bilgisi, sayfa numarası, tarih vb. ek bilgiler
# ==============================================================================


# ==============================================================================
# BÖLÜM 1: WebBaseLoader - Web Sayfalarından İçerik Yükleme
# ==============================================================================
# WebBaseLoader, herhangi bir URL'den web sayfasının içeriğini çeker.
# HTML etiketlerini temizleyerek sadece metin içeriği alır.
# 
# Kullanım alanları:
# - Güncel haberlerden bilgi çekme
# - Blog yazılarını vektör veritabanına ekleme
# - Rakip analizi için web scraping
# - Döküman arşivlerini işleme
# ==============================================================================

# from langchain_community.document_loaders import WebBaseLoader

# # Örnek URL - KPMG Türkiye'nin üretken yapay zeka makalesi
# target_url = "https://kpmg.com/tr/tr/home/gorusler/2023/12/uretken-yapay-zeka-uygulamalarinin-kurumsallasma-yaklasimi.html"

# # WebBaseLoader'ı hedef URL ile oluştur
# loader = WebBaseLoader(target_url)

# # URL'den içeriği çek ve Document listesi olarak al
# # Not: load() her zaman liste döner, tek sayfa bile olsa
# raw_documents = loader.load()

# # İçeriği bir dosyaya kaydet - debug ve analiz için faydalı
# # Böylece çekilen içeriği inceleyebilirsiniz
# with open("URL_Icerik.txt", "w") as file:
#     file.write(raw_documents[0].page_content)

# print("Dosya işlemi tammamlandı")

# # Metadata bilgilerini yazdır
# # Bu genellikle source URL, title gibi bilgiler içerir
# print(raw_documents[0].metadata)



# ==============================================================================
# BÖLÜM 2: PyPDFLoader - PDF Dosyalarından İçerik Yükleme
# ==============================================================================
# PyPDFLoader, PDF dosyalarını sayfa sayfa okur ve her sayfayı ayrı bir
# Document olarak döndürür.
#
# Özellikler:
# - Sayfa bazlı bölme (her sayfa ayrı Document)
# - Metadata'da sayfa numarası bilgisi
# - extract_images=True ile PDF içindeki görsellerdeki metni de çıkarabilir (OCR)
#
# Kullanım alanları:
# - Şirket raporlarını analiz etme
# - Akademik makaleleri işleme
# - Sözleşme ve hukuki belgeleri tarama
# - Kitap ve e-book içeriklerini indeksleme
# ==============================================================================

# from langchain_community.document_loaders import PyPDFLoader

# # Dosya yolunu datasets_19 klasöründen al
# # timeline.pdf: Zaman çizelgesi içeren örnek PDF
# # Not: Dosya yollarını projenizin yapısına göre ayarlayın
# # filepath = "../datasets_19/19.4-Datasets/timeline.pdf"

# # loader = PyPDFLoader(filepath)

# # PDF'in tüm sayfalarını yükle
# # pages bir liste, her eleman bir sayfa
# # pages = loader.load()

# # 40. sayfanın içeriğini ve metadata'sını göster (0-indexed, yani 39)
# # Bu şekilde belirli bir sayfaya ulaşabilirsiniz
# # print(pages[39].page_content, pages[39].metadata)

# #################################################################
# # İkinci örnek: Görsel içeren PDF
# # digital.pdf: Dijital dönüşüm konulu, görselli bir sunum
# filepath = "../datasets_19/19.4-Datasets/digital.pdf"

# # extract_images=True: PDF'teki görselleri OCR ile okumaya çalışır
# # Bu özellik için ek bağımlılıklar gerekebilir (pytesseract, pdf2image)
# # Görsel ağırlıklı PDF'ler için çok faydalı!
# loader = PyPDFLoader(filepath, extract_images=True)

# pages = loader.load()

# # 7. sayfanın içeriğini göster
# print(pages[6].page_content)



# ==============================================================================
# BÖLÜM 3: UnstructuredExcelLoader - Excel Dosyalarından İçerik Yükleme
# ==============================================================================
# UnstructuredExcelLoader, Excel dosyalarını okur ve yapılandırılmış veya
# yapılandırılmamış formatta çıktı verir.
#
# mode parametresi:
# - "single": Tüm sayfaları tek bir Document olarak döndür
# - "elements": Her hücre/satırı ayrı element olarak işle
#
# Özellikle "elements" modu, tablonun HTML formatını da metadata'ya ekler.
# Bu, veriyi görselleştirmek veya tablonun yapısını korumak için kullanışlıdır.
#
# Kullanım alanları:
# - Finansal raporları işleme
# - Envanter listelerini analiz etme
# - Kurs/eğitim programlarını indeksleme
# - Müşteri verilerini çıkarma
# ==============================================================================

from langchain_community.document_loaders import UnstructuredExcelLoader

# Dosya yolunu datasets_19 klasöründen al
# ai_course.xlsx: Yapay zeka kursu müfredatını içeren Excel dosyası
filepath = "../datasets_19/19.4-Datasets/ai_course.xlsx"

# UnstructuredExcelLoader'ı "elements" modunda oluştur
# Bu mod, tablonun yapısını korur ve HTML olarak da saklar
loader = UnstructuredExcelLoader(filepath, mode="elements")

# Excel içeriğini yükle
# docs listesi, Excel'deki her bir elementi içerir
docs = loader.load()

# İlk elementin HTML formatındaki tablo temsilini al
# Bu, tablonun orijinal görünümünü web'de göstermek için kullanılabilir
excel_content = docs[0].metadata["text_as_html"]

# HTML içeriğini bir dosyaya kaydet
# Bu dosyayı bir tarayıcıda açarak tablonun görsel halini görebilirsiniz
# Böylece Excel verisinin doğru çekilip çekilmediğini kontrol edebilirsiniz
with open("excel.html", "w") as file:
    file.write(excel_content)
