##################################################
# Introduction to Text Mining and Natural Language Processing
# Metin Madenciliği ve Doğal Dil İşleme'ye Giriş
##################################################

"""
===================================================================================
DOĞAL DİL İŞLEME (NLP - Natural Language Processing) NEDİR?
===================================================================================

NLP, bilgisayarların insan dilini anlamasını, yorumlamasını ve üretmesini sağlayan
yapay zeka dalıdır. Metin ve konuşma verilerini işleyerek anlamlı bilgiler çıkarır.

TEMEL KAVRAMLAR:
----------------
1. CORPUS (Derlem): Analiz için kullanılan metin koleksiyonu
2. TOKEN: Metnin en küçük birimi (kelime, karakter, alt-kelime)
3. VOCABULARY: Benzersiz tokenlerin listesi
4. DOCUMENT: Tek bir metin örneği (tweet, yorum, makale vb.)

NLP UYGULAMA ALANLARI:
----------------------
- Duygu Analizi (Sentiment Analysis): Metnin pozitif/negatif olup olmadığını belirleme
- Metin Sınıflandırma: Spam filtreleme, konu belirleme
- Adlandırılmış Varlık Tanıma (NER): İsim, yer, tarih gibi varlıkları çıkarma
- Makine Çevirisi: Google Translate gibi sistemler
- Soru-Cevap Sistemleri: ChatGPT, Siri, Alexa
- Metin Özetleme: Uzun metinleri kısa özet haline getirme
- Otomatik Tamamlama: Klavye önerileri

BU DOSYADA YAPILACAKLAR:
------------------------
1. Metin Ön İşleme (Text Preprocessing)
2. Metin Görselleştirme (Text Visualization)
3. Duygu Analizi (Sentiment Analysis)
4. Özellik Mühendisliği (Feature Engineering)
5. Duygu Modelleme (Sentiment Modeling)

PROJE: Amazon ürün yorumlarını analiz ederek pozitif/negatif sınıflandırma yapacağız.
===================================================================================
"""

##################################################
# Sentiment Analysis and Sentiment Modeling for Amazon Reviews
# Amazon Yorumları için Duygu Analizi ve Duygu Modelleme
##################################################

# 1. Text Preprocessing
# 2. Text Visualization
# 3. Sentiment Analysis
# 4. Feature Engineering
# 5. Sentiment Modeling

# Gerekli kütüphanelerin kurulumu (ilk kez çalıştırırken yorum satırını kaldırın)
# !pip install nltk       # Natural Language Toolkit - NLP için temel kütüphane
# !pip install textblob   # Basit metin işleme ve duygu analizi
# !pip install wordcloud  # Kelime bulutu görselleştirmesi için

# =============================================================================
# KÜTÜPHANE İMPORTLARI
# =============================================================================

from warnings import filterwarnings      # Uyarı mesajlarını filtrelemek için
import matplotlib.pyplot as plt           # Grafik ve görselleştirme kütüphanesi
import numpy as np                         # Sayısal işlemler ve array operasyonları için
import pandas as pd                        # Veri manipülasyonu ve DataFrame işlemleri için
from PIL import Image                      # Görsel dosyalarını okumak için (WordCloud maskeleri)
from nltk.corpus import stopwords          # İngilizce durma kelimeleri (the, is, at, which vb.)
from nltk.sentiment import SentimentIntensityAnalyzer  # VADER duygu analizi aracı
from sklearn.ensemble import RandomForestClassifier    # Rastgele Orman sınıflandırıcı
from sklearn.linear_model import LogisticRegression    # Lojistik Regresyon sınıflandırıcı
from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate  # Model değerlendirme ve hiperparametre optimizasyonu
from sklearn.preprocessing import LabelEncoder         # Kategorik değişkenleri sayısala çevirme
from textblob import Word, TextBlob        # Metin işleme ve sentiment analizi için
from wordcloud import WordCloud            # Kelime bulutu oluşturmak için

# =============================================================================
# GENEL AYARLAR
# =============================================================================
filterwarnings('ignore')  # Uyarı mesajlarını gösterme (temiz çıktı için)
pd.set_option('display.max_columns', None)  # Tüm sütunları göster
pd.set_option('display.width', 200)         # Ekran genişliğini ayarla
pd.set_option('display.float_format', lambda x: '%.2f' % x)  # Ondalık sayıları 2 basamakla göster

##################################################
# 1. Text Preprocessing (Metin Ön İşleme)
##################################################

"""
METİN ÖN İŞLEME NEDİR?
======================
Ham metin verisini makine öğrenmesi algoritmaları için uygun hale getirme sürecidir.
Metinden gürültüyü (noise) temizleyerek anlamlı bilgiyi ortaya çıkarır.

ÖN İŞLEME ADIMLARI:
-------------------
1. Küçük Harfe Çevirme (Lowercasing / Case Folding)
2. Noktalama İşaretlerini Silme (Punctuation Removal)
3. Sayıları Silme (Number Removal)
4. Stopwords Silme (Stop Words Removal)
5. Nadir Kelimeleri Silme (Rare Words Removal)
6. Tokenization (Metni tokenlara ayırma)
7. Lemmatization (Kelimeleri kök formuna indirme)
"""

# Veri setini yükle
# Amazon ürün yorumlarını içeren CSV dosyasını okuyoruz
df = pd.read_csv("../../Datasets_Genel_/amazon_reviews.csv", sep=",")
df.head()  # İlk 5 satırı görüntüle

###############################
# Normalizing Case Folding (Büyük/Küçük Harf Normalleştirme)
###############################

"""
CASE FOLDING (KÜÇÜK HARFE ÇEVİRME):
====================================
Tüm metni küçük harfe çevirerek tutarlılık sağlarız.
"Python" ve "python" aynı kelime olarak değerlendirilir.

Örnek:
- "GREAT Product!" -> "great product!"
- "The Best BOOK" -> "the best book"

NEDEN YAPIYORUZ?
- Aynı kelimenin farklı yazımlarını birleştirmek için
- Vocabulary (kelime dağarcığı) boyutunu küçültmek için
- Model performansını artırmak için
"""
df['reviewText'] = df['reviewText'].str.lower()
# str.lower() -> Pandas string metoduyla tüm karakterleri küçük harfe çevirir

###############################
# Punctuations (Noktalama İşaretleri)
###############################

"""
NOKTALAMA İŞARETLERİNİ SİLME:
=============================
Nokta, virgül, ünlem, soru işareti gibi karakterleri metinden çıkarırız.

Örnek:
- "great!!!" -> "great"
- "what?" -> "what"
- "hello, world." -> "hello world"

REGULAR EXPRESSION (REGEX) KULLANIMI:
- [^\w\s] -> Kelime karakterleri (\w) ve boşluk (\s) HARİÇ her şeyi seç
- ^ işareti köşeli parantez içinde "hariç" anlamına gelir
- \w -> a-z, A-Z, 0-9 ve _ karakterleri
- \s -> boşluk, tab, newline karakterleri
"""
df['reviewText'] = df['reviewText'].str.replace('[^\w\s]', '', regex=True)
# regex=True -> Regular Expression kullanıldığını belirtir (Pandas 2.0+ için gerekli)

# regular expression
# Düzenli ifadeler, metin kalıplarını tanımlamak için kullanılan güçlü bir araçtır

###############################
# Numbers (Sayılar)
###############################

"""
SAYILARI SİLME:
===============
Sayılar genellikle metin analizinde anlam taşımaz ve gürültü oluşturur.

Örnek:
- "I bought 3 items" -> "I bought items"
- "Version 2.0" -> "Version"

REGEX AÇIKLAMASI:
- \d -> Herhangi bir rakamı temsil eder (0-9)
"""
df['reviewText'] = df['reviewText'].str.replace('\d', '', regex=True)
# Tüm rakamları boş string ile değiştirerek sileriz

###############################
# Stopwords (Durma Kelimeleri)
###############################

"""
STOPWORDS (DURMA KELİMELERİ) NEDİR?
====================================
Dilde çok sık kullanılan ancak anlam taşımayan kelimelerdir.
Bu kelimeleri silmek veri boyutunu azaltır ve analizi iyileştirir.

İNGİLİZCE STOPWORDS ÖRNEKLERİ:
- Articles (Tanımlıklar): the, a, an
- Prepositions (Edatlar): in, on, at, to, for, with
- Conjunctions (Bağlaçlar): and, but, or, so
- Pronouns (Zamirler): I, you, he, she, it, we, they
- Auxiliary Verbs (Yardımcı Fiiller): is, am, are, was, were, be, been

NLTK KÜTÜPHANESİ:
- 179 İngilizce stopword içerir
- Türkçe dahil 20+ dil desteği vardır
"""
import nltk
# nltk.download('stopwords')  # İlk kez çalıştırırken yorum satırını kaldırın

# İngilizce stopwords listesini al
sw = stopwords.words('english')
# sw listesi: ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', ...]

# Her satırdaki metinden stopwords'leri filtrele
df['reviewText'] = df['reviewText'].apply(lambda x: " ".join(x for x in str(x).split() if x not in sw))
"""
LAMBDA FONKSİYONU AÇIKLAMASI:
1. str(x).split() -> Metni boşluklardan bölerek kelime listesi oluştur
2. if x not in sw -> Kelime stopwords listesinde değilse
3. " ".join(...) -> Filtrelenmiş kelimeleri tekrar birleştir

Örnek:
- "the product is very good" -> "product good"
- "I bought this for my friend" -> "bought friend"
"""


###############################
# Rarewords (Nadir Kelimeler)
###############################

"""
NADİR KELİMELERİ SİLME:
========================
Veri setinde çok az geçen kelimeler genellikle:
- Yazım hataları
- Özel isimler
- Anlamsız karakter dizileri

Bu kelimeleri silmek:
- Model karmaşıklığını azaltır
- Overfitting riskini düşürür
- Hesaplama maliyetini azaltır
"""
# Tüm kelimeleri birleştirip frekanslarını hesapla
temp_df = pd.Series(' '.join(df['reviewText']).split()).value_counts()
# ' '.join(df['reviewText']) -> Tüm yorumları tek bir string olarak birleştir
# .split() -> Kelimelere böl
# .value_counts() -> Her kelimenin kaç kez geçtiğini say

# Sadece 1 kez geçen kelimeleri bul (nadir kelimeler)
drops = temp_df[temp_df <= 1]
# Bu kelimeler büyük ihtimalle anlamsız veya yazım hatasıdır

# Nadir kelimeleri metinden çıkar
df['reviewText'] = df['reviewText'].apply(lambda x: " ".join(x for x in x.split() if x not in drops))
# drops index'inde olmayan kelimeleri tut


###############################
# Tokenization (Tokenizasyon)
###############################

"""
TOKENİZASYON NEDİR?
====================
Metni daha küçük parçalara (tokenlara) ayırma işlemidir.

TOKEN TÜRLERİ:
--------------
1. Word Tokenization: Kelime bazlı ayırma
   "Hello World" -> ["Hello", "World"]

2. Sentence Tokenization: Cümle bazlı ayırma
   "Hello. How are you?" -> ["Hello.", "How are you?"]

3. Subword Tokenization: Alt-kelime bazlı (BPE, WordPiece)
   "playing" -> ["play", "##ing"] (BERT tarzı)

TextBlob kütüphanesi basit word tokenization sağlar.
"""
# nltk.download("punkt")  # Tokenizer için gerekli veri (ilk kez çalıştırın)

# TextBlob ile tokenization örneği
df["reviewText"].apply(lambda x: TextBlob(x).words).head()
# .words özelliği metni kelimelere ayırır ve WordList döndürür


###############################
# Lemmatization (Kökleştirme)
###############################

"""
LEMMATİZATİON NEDİR?
=====================
Kelimeleri sözlük formlarına (lemma) dönüştürme işlemidir.
Stemming'den daha akıllıdır çünkü dilin kurallarını kullanır.

LEMMATİZATİON ÖRNEKLERİ:
------------------------
- "running" -> "run"
- "better" -> "good" (düzensiz fiil)
- "cats" -> "cat"
- "studies" -> "study"
- "went" -> "go"

STEMMING vs LEMMATİZATION:
--------------------------
Stemming: Basit kural tabanlı kök bulma (hızlı ama hatalı olabilir)
- "studies" -> "studi" (yanlış)
- "caring" -> "car" (yanlış)

Lemmatization: Sözlük tabanlı doğru kök bulma (daha yavaş ama doğru)
- "studies" -> "study" (doğru)
- "caring" -> "care" (doğru)

WordNet veritabanı kullanılır (İngilizce için en kapsamlı lexical database).
"""
# nltk.download('wordnet')  # WordNet sözlüğü (ilk kez çalıştırın)

# Her kelimeyi lemmatize et
df['reviewText'] = df['reviewText'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
"""
AÇIKLAMA:
1. x.split() -> Metni kelimelere böl
2. Word(word).lemmatize() -> Her kelimeyi kökleştir
3. " ".join(...) -> Kelimeleri tekrar birleştir
"""


##################################################
# 2. Text Visualization (Metin Görselleştirme)
##################################################

"""
METİN GÖRSELLEŞTİRME:
=====================
Metin verilerini görsel olarak analiz etme yöntemleridir.

AMAÇLARI:
---------
1. Veri setini anlamak
2. Önemli kelimeleri tespit etmek
3. Kelime dağılımlarını görmek
4. Sunumlarda kullanmak

YÖNTEMLER:
----------
- Bar Plot (Çubuk Grafik)
- Word Cloud (Kelime Bulutu)
- Histogram
"""


###############################
# Terim Frekanslarının Hesaplanması
###############################

"""
TERİM FREKANSI (TERM FREQUENCY - TF):
======================================
Bir kelimenin belgede kaç kez geçtiğini gösterir.

HESAPLAMA ADIMLARI:
1. Her yorumu kelimelere böl
2. Her kelimenin frekansını say
3. Tüm yorumlardaki frekansları topla
"""
# Her yorumun kelime frekanslarını hesapla ve topla
tf = df["reviewText"].apply(lambda x: pd.value_counts(x.split(" "))).sum(axis=0).reset_index()
"""
AÇIKLAMA:
- x.split(" ") -> Yorumu kelimelere böl
- pd.value_counts() -> Her kelimenin frekansını say
- .sum(axis=0) -> Tüm yorumlardaki frekansları topla (sütun bazlı)
- .reset_index() -> Index'i sütuna çevir
"""

# Sütun isimlerini düzenle
tf.columns = ["words", "tf"]
# words: kelime, tf: terim frekansı (kaç kez geçtiği)

# En çok geçen kelimelere göre sırala
tf.sort_values("tf", ascending=False)
# ascending=False -> Büyükten küçüğe sırala

###############################
# Barplot (Çubuk Grafik)
###############################

"""
ÇUBUK GRAFİK:
=============
En sık kullanılan kelimeleri görselleştirir.
500'den fazla geçen kelimeleri gösteriyoruz.
"""
tf[tf["tf"] > 500].plot.bar(x="words", y="tf")
# tf > 500 olan kelimeleri filtrele ve çubuk grafik çiz
plt.show()

###############################
# Wordcloud (Kelime Bulutu)
###############################

"""
KELİME BULUTU (WORD CLOUD):
============================
Kelime frekansını görsel olarak temsil eden bir grafiktir.
Sık geçen kelimeler BÜYÜK, nadir kelimeler küçük gösterilir.

AVANTAJLARI:
- Görsel olarak etkileyici
- Hızlı içgörü sağlar
- Sunum ve raporlarda etkili
"""
# Tüm yorumları tek bir string olarak birleştir
text = " ".join(i for i in df.reviewText)

# Basit Word Cloud oluştur
wordcloud = WordCloud().generate(text)
plt.imshow(wordcloud, interpolation="bilinear")  # Görüntüyü göster
plt.axis("off")  # Eksenleri gizle
plt.show()

# Özelleştirilmiş Word Cloud
wordcloud = WordCloud(max_font_size=50,     # Maksimum font boyutu
                      max_words=100,          # Maksimum kelime sayısı
                      background_color="white").generate(text)  # Arka plan rengi
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# Word Cloud'u dosyaya kaydet
wordcloud.to_file("../images_Genel_/Natural_Language_Processing_(NLP)/wordcloud.png")
# PNG formatında kaydeder


###############################
# Şablonlara Göre Wordcloud (Masked WordCloud)
###############################

"""
MASKELİ KELİME BULUTU:
=======================
Kelimeleri özel bir şekil içinde gösterir.
Örnek: Türkiye haritası, kalp, yıldız vb. şekiller

MASK (MASKE):
- Siyah-beyaz veya şeffaf arka planlı görsel
- Beyaz alanlar boş kalır
- Renkli/siyah alanlar kelimelerle doldurulur
"""
# Türkiye haritası maskesini yükle
tr_mask = np.array(Image.open("../images_Genel_/Natural_Language_Processing_(NLP)/tr.png"))
# Image.open() -> PIL ile görseli aç
# np.array() -> NumPy array'e çevir

# Maskeli Word Cloud oluştur
wc = WordCloud(background_color="white",  # Arka plan rengi
               max_words=1000,             # Maksimum kelime sayısı
               mask=tr_mask,               # Maske görseli
               contour_width=3,            # Kontur kalınlığı
               contour_color="firebrick")  # Kontur rengi (tuğla kırmızısı)

wc.generate(text)  # Word Cloud'u oluştur
plt.figure(figsize=[10, 10])  # Figür boyutunu ayarla
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()


##################################################
# 3. Sentiment Analysis (Duygu Analizi)
##################################################

"""
DUYGU ANALİZİ NEDİR?
=====================
Metindeki duyguyu (pozitif, negatif, nötr) belirleme işlemidir.
Opinion Mining veya Emotion AI olarak da bilinir.

YAKLAŞIMLAR:
------------
1. Lexicon-Based (Sözlük Tabanlı):
   - Önceden tanımlanmış kelime listeleri kullanır
   - Her kelimenin duygu puanı vardır
   - VADER, AFINN, SentiWordNet

2. Machine Learning Based (Makine Öğrenmesi Tabanlı):
   - Etiketli verilerle model eğitilir
   - Naive Bayes, SVM, LSTM, BERT

VADER (Valence Aware Dictionary for Sentiment Reasoning):
----------------------------------------------------------
- Sosyal medya metinleri için optimize edilmiş
- Emoji, büyük harf, noktalama işaretlerini dikkate alır
- -1 (negatif) ile +1 (pozitif) arasında puan verir

VADER ÇIKTILARI:
- neg: Negatif yoğunluk (0-1)
- neu: Nötr yoğunluk (0-1)
- pos: Pozitif yoğunluk (0-1)
- compound: Bileşik skor (-1 ile +1 arası, en önemli metrik)
"""

df["reviewText"].head()  # Ön işlemeden geçmiş yorumları görüntüle

# nltk.download('vader_lexicon')  # VADER sözlüğü (ilk kez çalıştırın)

# VADER Sentiment Analyzer'ı başlat
sia = SentimentIntensityAnalyzer()

# Örnek cümlelerde duygu analizi
sia.polarity_scores("The film was awesome")
# Çıktı: {'neg': 0.0, 'neu': 0.423, 'pos': 0.577, 'compound': 0.6249}
# compound > 0.05 -> Pozitif

sia.polarity_scores("I liked this music but it is not good as the other one")
# Karışık duygular içeren cümle analizi

# İlk 10 yorumun duygu puanlarını hesapla
df["reviewText"][0:10].apply(lambda x: sia.polarity_scores(x))

# Sadece compound değerini al (en önemli metrik)
df["reviewText"][0:10].apply(lambda x: sia.polarity_scores(x)["compound"])

# Tüm yorumlar için polarity_score sütunu oluştur
df["polarity_score"] = df["reviewText"].apply(lambda x: sia.polarity_scores(x)["compound"])

###############################
# 4. Feature Engineering (Özellik Mühendisliği)
###############################

"""
ÖZELLİK MÜHENDİSLİĞİ:
======================
Ham veriden makine öğrenmesi modelleri için anlamlı özellikler
oluşturma sürecidir.

BU BÖLÜMDE YAPILACAKLAR:
------------------------
1. Compound score'u kullanarak sentiment etiketleri oluşturma
2. Label Encoding ile sayısal değerlere dönüştürme
3. Metin özelliklerini vektörlere çevirme (Count Vectors, TF-IDF)
"""

# Compound değerine göre pos/neg etiket oluştur
df["reviewText"][0:10].apply(lambda x: "pos" if sia.polarity_scores(x)["compound"] > 0 else "neg")
# compound > 0 -> "pos" (pozitif)
# compound <= 0 -> "neg" (negatif)

# Tüm veri seti için sentiment_label sütunu oluştur
df["sentiment_label"] = df["reviewText"].apply(lambda x: "pos" if sia.polarity_scores(x)["compound"] > 0 else "neg")

# Etiket dağılımını kontrol et
df["sentiment_label"].value_counts()
# Pozitif ve negatif yorum sayılarını gösterir

# Etiketlere göre ortalama puanı kontrol et
df.groupby("sentiment_label")["overall"].mean()
# Pozitif etiketli yorumların gerçekten yüksek puan verip vermediğini kontrol

# Label Encoding: pos -> 1, neg -> 0
df["sentiment_label"] = LabelEncoder().fit_transform(df["sentiment_label"])
# Kategorik değişkeni sayısal değere çevirir
# Alfabetik sıraya göre: neg=0, pos=1

# Bağımlı ve bağımsız değişkenleri ayır
y = df["sentiment_label"]  # Hedef değişken (0: negatif, 1: pozitif)
X = df["reviewText"]       # Özellikler (metin verisi)

###############################
# Count Vectors (Sayım Vektörleri)
###############################

"""
METİN VEKTÖRLEŞTIRME YÖNTEMLERİ:
=================================
Makine öğrenmesi modelleri sayısal verilerle çalışır.
Metinleri sayısal vektörlere dönüştürmemiz gerekir.

1. COUNT VECTORS (Bag of Words):
   - Her kelimenin belgede kaç kez geçtiğini sayar
   - Frekans tabanlı temsil
   - Basit ama etkili

2. TF-IDF VECTORS:
   - Term Frequency - Inverse Document Frequency
   - Nadir kelimelere daha yüksek ağırlık verir
   - Yaygın kelimelerin etkisini azaltır

3. WORD EMBEDDINGS:
   - Kelimelerin anlamsal temsillerini öğrenir
   - Word2Vec, GloVe, FastText
   - BERT, GPT (bağlamsal embedding'ler)

TOKENİZASYON SEVİYELERİ:
------------------------
- words: Kelime bazlı vektörleştirme
- characters: Karakter bazlı vektörleştirme
- ngram: N-gram bazlı vektörleştirme
"""

# N-GRAM NEDİR?
# N ardışık kelimenin kombinasyonudur

# ngram
a = """Bu örneği anlaşılabilmesi için daha uzun bir metin üzerinden göstereceğim.
N-gram'lar birlikte kullanılan kelimelerin kombinasyolarını gösterir ve feature üretmek için kullanılır"""

TextBlob(a).ngrams(3)
"""
3-gram örneği:
- ["Bu", "örneği", "anlaşılabilmesi"]
- ["örneği", "anlaşılabilmesi", "için"]
- ...

N-GRAM TÜRLERİ:
- Unigram (n=1): tek kelimeler ["Bu", "örneği", "anlaşılabilmesi"]
- Bigram (n=2): ikili kombinasyonlar ["Bu örneği", "örneği anlaşılabilmesi"]
- Trigram (n=3): üçlü kombinasyonlar
"""

###############################
# Count Vectors (CountVectorizer)
###############################

from sklearn.feature_extraction.text import CountVectorizer

# Örnek corpus (belge koleksiyonu)
corpus = ['This is the first document.',
          'This document is the second document.',
          'And this is the third one.',
          'Is this the first document?']

# Word Frekansı (Bag of Words)
vectorizer = CountVectorizer()
X_c = vectorizer.fit_transform(corpus)
# fit_transform: Vocabulary oluştur ve dönüştür

vectorizer.get_feature_names()
# Çıktı: ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']

X_c.toarray()
"""
Çıktı matrisi (her satır bir belge, her sütun bir kelime):
[[0, 1, 1, 1, 0, 0, 1, 0, 1],  # This is the first document
 [0, 2, 0, 1, 0, 1, 1, 0, 1],  # This document is the second document
 [1, 0, 0, 1, 1, 0, 1, 1, 1],  # And this is the third one
 [0, 1, 1, 1, 0, 0, 1, 0, 1]]  # Is this the first document?
"""

# N-gram Frekansı (Bigram örneği)
vectorizer2 = CountVectorizer(analyzer='word', ngram_range=(2, 2))
# ngram_range=(2, 2) -> Sadece bigram'lar
X_n = vectorizer2.fit_transform(corpus)
vectorizer2.get_feature_names()
# Çıktı: ['and this', 'document is', 'first document', 'is the', 'is this', ...]
X_n.toarray()

# Amazon yorumları için Count Vectorizer
vectorizer = CountVectorizer()
X_count = vectorizer.fit_transform(X)

# Örnek kelimeleri ve değerlerini göster
vectorizer.get_feature_names()[10:15]  # 10-15. kelimeler
X_count.toarray()[10:15]               # 10-15. belgelerin vektörleri


###############################
# TF-IDF (Term Frequency - Inverse Document Frequency)
###############################

"""
TF-IDF NEDİR?
==============
Count Vectors'ün gelişmiş versiyonudur.
Yaygın kelimelerin etkisini azaltır, nadir kelimelere ağırlık verir.

FORMÜL:
-------
TF(t,d) = (t kelimesinin d belgesindeki frekansı) / (d belgesindeki toplam kelime sayısı)
IDF(t) = log(Toplam belge sayısı / t kelimesini içeren belge sayısı)
TF-IDF = TF × IDF

ÖRNEK:
------
"the" kelimesi her belgede geçer -> IDF düşük -> TF-IDF düşük
"machine learning" nadir geçer -> IDF yüksek -> TF-IDF yüksek

AVANTAJLARI:
- Yaygın ama anlamsız kelimelerin (the, is, a) etkisini azaltır
- Ayırt edici kelimelere ağırlık verir
"""
from sklearn.feature_extraction.text import TfidfVectorizer

# Word-Level TF-IDF
tf_idf_word_vectorizer = TfidfVectorizer()
X_tf_idf_word = tf_idf_word_vectorizer.fit_transform(X)

# N-gram Level TF-IDF (Bigram ve Trigram)
tf_idf_ngram_vectorizer = TfidfVectorizer(ngram_range=(2, 3))
# ngram_range=(2, 3) -> Bigram ve trigram'ları kullan
X_tf_idf_ngram = tf_idf_ngram_vectorizer.fit_transform(X)


###############################
# 5. Sentiment Modeling (Duygu Modelleme)
###############################

"""
DUYGU MODELLEME:
================
Makine öğrenmesi algoritmalarıyla metin sınıflandırma modellerinin
eğitilmesi ve değerlendirilmesi.

KULLANILACAK ALGORİTMALAR:
- Logistic Regression (Lojistik Regresyon)
- Random Forest (Rastgele Orman)

DEĞERLENDİRME METRİĞİ:
- Accuracy (Doğruluk)
- Cross-Validation (Çapraz Doğrulama)
"""

# 1. Text Preprocessing
# 2. Text Visualization
# 3. Sentiment Analysis
# 4. Feature Engineering
# 5. Sentiment Modeling

###############################
# Logistic Regression (Lojistik Regresyon)
###############################

"""
LOJİSTİK REGRESYON:
===================
İkili sınıflandırma için kullanılan basit ama etkili bir algoritmadır.
Metin sınıflandırmada yaygın olarak tercih edilir.

AVANTAJLARI:
- Hızlı eğitim ve tahmin
- Yüksek boyutlu verilerle iyi çalışır (metin verisi gibi)
- Olasılık tahmini verir
- Yorumlanabilir (hangi kelimelerin etkili olduğu görülebilir)
"""
# TF-IDF Word-Level vektörleriyle Logistic Regression modeli eğit
log_model = LogisticRegression().fit(X_tf_idf_word, y)

# 5-Fold Cross Validation ile model performansını değerlendir
cross_val_score(log_model,
                X_tf_idf_word,
                y,
                scoring="accuracy",
                cv=5).mean()
"""
CROSS VALIDATION (ÇAPRAZ DOĞRULAMA):
- Veriyi 5 parçaya böler
- Her parçayı sırayla test seti olarak kullanır
- 5 farklı accuracy değerinin ortalamasını alır
- Overfitting'i tespit etmeye yardımcı olur
"""

# Yeni yorumlar için tahmin yapma
new_review = pd.Series("this product is great")
new_review = pd.Series("look at that shit very bad")
new_review = pd.Series("it was good but I am sure that it fits me")

# Yeni yorumu TF-IDF vektörüne dönüştür
new_review = TfidfVectorizer().fit(X).transform(new_review)
# fit(X) -> Orijinal vocabulary'yi kullan
# transform(new_review) -> Yeni yorumu dönüştür

# Tahmin yap
log_model.predict(new_review)
# Çıktı: [1] -> Pozitif veya [0] -> Negatif

# Rastgele bir yorum seç ve tahmin et
random_review = pd.Series(df["reviewText"].sample(1).values)
# sample(1) -> Rastgele 1 satır seç

new_review = TfidfVectorizer().fit(X).transform(random_review)

log_model.predict(new_review)


###############################
# Random Forests (Rastgele Ormanlar)
###############################

"""
RASTGELE ORMANLAR:
==================
Birden fazla karar ağacının birleşimidir (Ensemble Learning).
Her ağaç farklı alt örneklerle eğitilir ve sonuçlar birleştirilir.

AVANTAJLARI:
- Overfitting'e karşı dayanıklı
- Non-linear ilişkileri yakalayabilir
- Feature importance (özellik önem düzeyi) verir

DEZAVANTAJLARI:
- Eğitim süresi uzun olabilir
- Yorumlaması zor (black box)
"""

# Count Vectors ile Random Forest
rf_model = RandomForestClassifier().fit(X_count, y)
cross_val_score(rf_model, X_count, y, cv=5, n_jobs=-1).mean()
# n_jobs=-1 -> Tüm CPU çekirdeklerini kullan

# TF-IDF Word-Level ile Random Forest
rf_model = RandomForestClassifier().fit(X_tf_idf_word, y)
cross_val_score(rf_model, X_tf_idf_word, y, cv=5, n_jobs=-1).mean()

# TF-IDF N-GRAM ile Random Forest
rf_model = RandomForestClassifier().fit(X_tf_idf_ngram, y)
cross_val_score(rf_model, X_tf_idf_ngram, y, cv=5, n_jobs=-1).mean()

###############################
# Hiperparametre Optimizasyonu
###############################

"""
HİPERPARAMETRE OPTİMİZASYONU:
=============================
Model performansını artırmak için en iyi hiperparametreleri bulma.

GridSearchCV:
- Tüm parametre kombinasyonlarını dener
- En iyi kombinasyonu bulur
- Cross-validation ile değerlendirir

RANDOM FOREST HİPERPARAMETRELERİ:
- max_depth: Ağaç derinliği (None = sınırsız)
- max_features: Her split'te kullanılacak özellik sayısı
- min_samples_split: Bir düğümü bölmek için gereken minimum örnek sayısı
- n_estimators: Ağaç sayısı
"""
rf_model = RandomForestClassifier(random_state=17)
# random_state -> Tekrarlanabilirlik için seed değeri

# Denenecek hiperparametre aralıkları
rf_params = {"max_depth": [8, None],           # Ağaç derinliği
             "max_features": [7, "auto"],       # Özellik sayısı
             "min_samples_split": [2, 5, 8],    # Minimum split örnek sayısı
             "n_estimators": [100, 200]}        # Ağaç sayısı
# Toplam kombinasyon: 2 × 2 × 3 × 2 = 24 farklı model denenecek

# GridSearchCV ile en iyi parametreleri bul
rf_best_grid = GridSearchCV(rf_model,
                            rf_params,
                            cv=5,              # 5-fold cross-validation
                            n_jobs=-1,         # Paralel işlem
                            verbose=1).fit(X_count, y)  # İlerleme göster

# En iyi parametreleri görüntüle
rf_best_grid.best_params_
# Örnek çıktı: {'max_depth': None, 'max_features': 'auto', 'min_samples_split': 2, 'n_estimators': 200}

# En iyi parametrelerle final modeli oluştur
rf_final = rf_model.set_params(**rf_best_grid.best_params_, random_state=17).fit(X_count, y)
# **rf_best_grid.best_params_ -> Dictionary'yi keyword arguments olarak aç

# Final modelin performansını değerlendir
cross_val_score(rf_final, X_count, y, cv=5, n_jobs=-1).mean()
# Optimize edilmiş hiperparametrelerle accuracy değeri

"""
===================================================================================
SONUÇ VE ÖNERİLER:
===================================================================================

BU DOSYADA ÖĞRENİLENLER:
-------------------------
1. Metin ön işleme teknikleri (lowercase, punctuation, stopwords, lemmatization)
2. Metin görselleştirme (bar plot, word cloud, masked word cloud)
3. VADER ile duygu analizi (lexicon-based sentiment analysis)
4. Metin vektörleştirme (Count Vectors, TF-IDF)
5. Makine öğrenmesi ile sınıflandırma (Logistic Regression, Random Forest)
6. Hiperparametre optimizasyonu (GridSearchCV)

İLERİ SEVİYE KONULAR:
---------------------
- Word Embeddings (Word2Vec, GloVe, FastText)
- Deep Learning modelleri (LSTM, Transformer, BERT)
- Named Entity Recognition (NER)
- Topic Modeling (LDA, LSA)
- Text Summarization
- Machine Translation

ÖNERİLEN KAYNAKLAR:
-------------------
- NLTK Dokümantasyonu: https://www.nltk.org/
- spaCy: https://spacy.io/
- Hugging Face Transformers: https://huggingface.co/
- Stanford NLP: https://nlp.stanford.edu/

===================================================================================
"""
