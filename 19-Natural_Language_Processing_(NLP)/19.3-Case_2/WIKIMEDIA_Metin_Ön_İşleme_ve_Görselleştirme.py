#################################################
# WIKI 1 - Metin Önişleme ve Görselleştirme (NLP - Text Preprocessing & Text Visualization)
#################################################

###################f##############################
# Problemin Tanımı
#################################################
# Wikipedia örnek datasından metin ön işleme, temizleme işlemleri gerçekleştirip, görselleştirme çalışmaları yapmak.

#################################################
# Veri Seti Hikayesi
#################################################
# Wikipedia datasından alınmış metinleri içermektedir.

#################################################
# Gerekli Kütüphaneler ve ayarlar
#################################################

# =============================================================================
# KÜTÜPHANE İMPORTLARI
# =============================================================================

# Veri manipülasyonu ve DataFrame işlemleri için temel kütüphane
import pandas as pd

# Grafik ve görselleştirme kütüphanesi - çubuk grafik gösterimi için
import matplotlib.pyplot as plt

# Kelime bulutu (word cloud) oluşturmak için kullanılan kütüphane
from wordcloud import WordCloud

# NLTK'nin İngilizce durma kelimeleri (stopwords) listesi
from nltk.corpus import stopwords

# TextBlob kütüphanesi - Word sınıfı lemmatization için, TextBlob tokenization için
from textblob import Word, TextBlob

# Uyarı mesajlarını filtrelemek için
from warnings import filterwarnings

# =============================================================================
# GENEL AYARLAR
# =============================================================================
# Uyarı mesajlarını kapat - temiz çıktı için
filterwarnings('ignore')

# Pandas görüntüleme ayarları
pd.set_option('display.max_columns', None)  # Tüm sütunları göster
pd.set_option('display.float_format', lambda x: '%.2f' % x)  # Ondalıkları 2 basamakla göster
pd.set_option('display.width', 200)  # Ekran genişliğini ayarla

# =============================================================================
# VERİ SETİNİ YÜKLEME
# =============================================================================
# Datayı okumak
# 19.3-Case_2 klasöründen wiki_data.csv dosyasını oku
# index_col=0: İlk sütunu index olarak kullan
df = pd.read_csv("wiki_data.csv", index_col=0)

# İlk 5 satırı görüntüle - veri yapısını anlamak için
df.head()

# İlk 2000 satırı al - işlem hızını artırmak için veri boyutunu sınırla
df = df[:2000]

# Veri setinin boyutunu kontrol et
df.head()
df.shape  # (satır sayısı, sütun sayısı)

#################################################
# Görevler:
#################################################

# Görev 1: Metindeki ön işleme işlemlerini gerçekleştirecek bir fonksiyon yazınız.
# •	Büyük küçük harf dönüşümünü yapınız.
# •	Noktalama işaretlerini çıkarınız.
# •	Numerik ifadeleri çıkarınız.


def clean_text(text):
    """
    Metin temizleme fonksiyonu - temel ön işleme adımlarını uygular.
    
    Parametreler:
    - text: Pandas Series formatında metin verisi
    
    Döndürür:
    - text: Temizlenmiş metin verisi
    """
    # Normalizing Case Folding
    # Tüm karakterleri küçük harfe çevir - "HELLO" -> "hello"
    text = text.str.lower()
    
    # Punctuations
    # Noktalama işaretlerini kaldır - [^\w\s]: kelime ve boşluk karakterleri hariç her şey
    text = text.str.replace(r'[^\w\s]', '', regex=True)
    
    # Satır sonu karakterlerini (\n) kaldır - metni tek satıra indir
    text = text.str.replace("\n" , '', regex=True)
    
    # Numbers
    # Sayıları kaldır - \d: herhangi bir rakam (0-9)
    text = text.str.replace('\d', '', regex=True)
    
    return text


# clean_text fonksiyonunu "text" sütununa uygula
df["text"] = clean_text(df["text"])

# Temizlenmiş veriyi kontrol et
df.head()



# Görev 2: Metin içinde öznitelik çıkarımı yaparken önemli olmayan kelimeleriçıkaracak fonksiyon yazınız.

def remove_stopwords(text):
    """
    Stopwords (durma kelimeleri) kaldırma fonksiyonu.
    
    İngilizce'de "the", "is", "at" gibi anlamsız kelimeleri metinden çıkarır.
    
    Parametreler:
    - text: Pandas Series formatında metin verisi
    
    Döndürür:
    - text: Stopwords'lerden arındırılmış metin
    """
    # NLTK'nin İngilizce stopwords listesini al
    stop_words = stopwords.words('English')
    
    # Lambda fonksiyonu ile her satırdaki metinden stopwords'leri filtrele
    # split(): Metni kelimelere böl
    # if x not in stop_words: Stopwords listesinde olmayan kelimeleri tut
    # join(): Filtrelenmiş kelimeleri tekrar birleştir
    text = text.apply(lambda x: " ".join(x for x in str(x).split() if x not in stop_words))
    
    return text


# remove_stopwords fonksiyonunu "text" sütununa uygula
df["text"] = remove_stopwords(df["text"])




# Görev 3: Metinde az tekrarlayan kelimeleri bulunuz.
# En az geçen 1000 kelimeyi bul - nadir kelimeler genellikle gürültüdür
# value_counts(): Kelimelerin frekanslarını hesapla
# [-1000:]: Son 1000 kelime (en az geçenler)
pd.Series(' '.join(df['text']).split()).value_counts()[-1000:]



# Görev 4: Metinde az tekrarlayan kelimeleri metin içerisinden çıkartınız. (İpucu: lambda fonksiyonunu kullanınız.)

# Nadir kelimeleri (en az geçen 1000 kelime) bul ve sil değişkenine ata
sil = pd.Series(' '.join(df['text']).split()).value_counts()[-1000:]

# Lambda fonksiyonu ile nadir kelimeleri metinden çıkar
# x.split(): Metni kelimelere böl
# if x not in sil: sil listesinde olmayan kelimeleri tut
df['text'] = df['text'].apply(lambda x: " ".join(x for x in x.split() if x not in sil))




# Görev 5: Metinleri tokenize edip sonuçları gözlemleyiniz.
# Tokenization: Metni kelime veya cümle gibi daha küçük parçalara ayırma
# TextBlob(x).words: Metni kelimelere böler ve WordList döndürür
df["text"].apply(lambda x: TextBlob(x).words)


# Görev 6: Lemmatization işlemini yapınız.
# ran, runs, running -> run (normalleştirme)
# Lemmatization: Kelimeleri sözlük formlarına (kök) dönüştürme
# Stemming'den daha akıllı - dilbilgisi kurallarını kullanır
# Word(word).lemmatize(): WordNet sözlüğü kullanarak kelimenin kökünü bulur
df['text'] = df['text'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

# Lemmatization sonrası veriyi kontrol et
df.head()

# Görev 7: Metindeki terimlerin frekanslarını hesaplayınız. (İpucu: Barplot grafiği için gerekli)
# Term Frequency hesaplama
# Her satırdaki kelimelerin frekanslarını say ve tüm satırları topla
tf = df["text"].apply(lambda x: pd.value_counts(x.split(" "))).sum(axis=0).reset_index() # kodu güncellemek gerekecek

# Terim frekansı DataFrame'inin ilk 5 satırını görüntüle
tf.head()

# Görev 8: Barplot grafiğini oluşturunuz.

# Sütunların isimlendirilmesi
# words: kelime, tf: terim frekansı (term frequency)
tf.columns = ["words", "tf"]

# 5000'den fazla geçen kelimelerin görselleştirilmesi
# 2000'den fazla geçen kelimeleri filtrele ve çubuk grafik çiz
# Bu kelimeler en sık kullanılan kelimelerdir
tf[tf["tf"] > 2000].plot.bar(x="words", y="tf")
plt.show()

# Kelimeleri WordCloud ile görselleştiriniz.

# kelimeleri birleştirdik
# Tüm yorumları tek bir string olarak birleştir - WordCloud için gerekli
text = " ".join(i for i in df["text"])

# wordcloud görselleştirmenin özelliklerini belirliyoruz
# max_font_size: En büyük kelimenin font boyutu
# max_words: Gösterilecek maksimum kelime sayısı
# background_color: Arka plan rengi (siyah)
wordcloud = WordCloud(max_font_size=50,
max_words=100,
background_color="black").generate(text)

# Yeni figür oluştur
plt.figure()

# WordCloud görselini göster - bilinear interpolasyon ile yumuşak görüntü
plt.imshow(wordcloud, interpolation="bilinear")

# Eksenleri gizle - sadece kelime bulutu görünsün
plt.axis("off")

# Grafiği ekranda göster
plt.show()

# Görev 9: Tüm aşamaları tek bir fonksiyon olarak yazınız.
# •	Metin ön işleme işlemlerini gerçekleştiriniz.
# •	Görselleştirme işlemlerini fonksiyona argüman olarak ekleyiniz.
# •	Fonksiyonu açıklayan 'docstring' yazınız.

# Veri setini tekrar yükle - fonksiyonu test etmek için temiz veri
df = pd.read_csv("wiki_data.csv", index_col=0)


def wiki_preprocess(text, Barplot=False, Wordcloud=False):
    """
    Textler üzerinde ön işleme işlemleri yapar.
    
    Bu fonksiyon NLP (Doğal Dil İşleme) pipeline'ının temel adımlarını içerir:
    1. Case Folding (Küçük harfe çevirme)
    2. Noktalama işaretlerini kaldırma
    3. Sayıları kaldırma
    4. Stopwords'leri kaldırma
    5. Nadir kelimeleri kaldırma
    
    Opsiyonel olarak görselleştirme yapabilir:
    - Barplot: En sık geçen kelimelerin çubuk grafiği
    - WordCloud: Kelime bulutu görselleştirmesi

    :param text: DataFrame'deki textlerin olduğu değişken (Pandas Series)
    :param Barplot: Barplot görselleştirme - True/False (varsayılan: False)
    :param Wordcloud: Wordcloud görselleştirme - True/False (varsayılan: False)
    :return: text - Ön işlemeden geçmiş metin verisi


    Example:
            wiki_preprocess(dataframe[col_name])
            wiki_preprocess(dataframe[col_name], Barplot=True, Wordcloud=True)

    """
    # Normalizing Case Folding
    # Tüm karakterleri küçük harfe çevir
    text = text.str.lower()
    
    # Punctuations
    # Noktalama işaretlerini kaldır
    text = text.str.replace('[^\w\s]', '', regex=True)
    
    # Satır sonu karakterlerini kaldır
    text = text.str.replace("\n", '', regex=True)
    
    # Numbers
    # Sayıları kaldır
    text = text.str.replace('\d', '', regex=True)
    
    # Stopwords
    # İngilizce stopwords listesini al ve metinden çıkar
    sw = stopwords.words('English')
    text = text.apply(lambda x: " ".join(x for x in str(x).split() if x not in sw))
    
    # Rarewords / Custom Words
    # En az geçen 1000 kelimeyi bul ve metinden çıkar
    sil = pd.Series(' '.join(text).split()).value_counts()[-1000:]
    text = text.apply(lambda x: " ".join(x for x in x.split() if x not in sil))


    # Barplot görselleştirme - opsiyonel
    if Barplot:
        # Terim Frekanslarının Hesaplanması
        # Her kelimenin toplam frekansını hesapla
        tf = text.apply(lambda x: pd.value_counts(x.split(" "))).sum(axis=0).reset_index()
        
        # Sütunların isimlendirilmesi
        tf.columns = ["words", "tf"]
        
        # 5000'den fazla geçen kelimelerin görselleştirilmesi
        # Çubuk grafik ile en sık kelimeleri göster
        tf[tf["tf"] > 2000].plot.bar(x="words", y="tf")
        plt.show()

    # WordCloud görselleştirme - opsiyonel
    if Wordcloud:
        # Kelimeleri birleştirdik
        # Tüm metinleri tek bir string olarak birleştir
        text_combined = " ".join(i for i in text)
        
        # wordcloud görselleştirmenin özelliklerini belirliyoruz
        wordcloud = WordCloud(max_font_size=50,
                              max_words=100,
                              background_color="white").generate(text_combined)
        
        # Figür oluştur ve göster
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    return text


# Fonksiyonu sadece ön işleme ile çağır (görselleştirme yok)
wiki_preprocess(df["text"])

# Fonksiyonu hem ön işleme hem de tüm görselleştirmeler ile çağır
wiki_preprocess(df["text"], True, True)