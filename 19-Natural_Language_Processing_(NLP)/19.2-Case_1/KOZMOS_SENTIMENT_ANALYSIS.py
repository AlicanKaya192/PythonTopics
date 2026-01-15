##################################################
# Sentiment Analysis and Sentiment Modeling for Amazon Reviews
##################################################

##################################################
# Business Problem
##################################################
# Amazon üzerinden satışlarını gerçekleştiren ev tesktili ve günlük giyim odaklı üretimler yapan Kozmos ürünlerine
# gelen yorumları analiz ederek ve aldığı şikayetlere göre özelliklerini geliştirerek satışlarını artırmayı hedeflemektedir.
# Bu hedef doğrultusunda yorumlara duygu analizi yapılarak etiketlencek ve   etiketlenen veri ile sınıflandırma modeli
# oluşturulacaktır.

##################################################
# Veri Seti Hikayesi
##################################################
# Veri seti belirli bir ürün grubuna ait yapılan yorumları, yorum başlığını, yıldız sayısını ve yapılan yorumu
# kaç kişinin faydalı bulduğunu belirten değişkenlerden oluşmaktadır.

# Review: Ürüne yapılan yorum
# Title: Yorum içeriğine verilen başlık, kısa yorum
# HelpFul: Yorumu faydalı bulan kişi sayısı
# Star: Ürüne verilen yıldız sayısı

##############################################################
# Görevler
##############################################################

# Görev 1: Metin ön işleme işlemleri.
        # 1. amazon.xlsx datasını okutunuz.
        # 2. "Review" değişkeni üzerinde
            # a. Tüm harfleri küçük harfe çeviriniz
            # b. Noktalama işaretlerini çıkarınız
            # c. Yorumlarda bulunan sayısal ifadeleri çıkarınız
            # d. Bilgi içermeyen kelimeleri (stopwords) veriden çıkarınız
            # e. 1000'den az geçen kelimeleri veriden çıkarınız
            # f. Lemmatization işlemini uygulayınız

# Görev 2: Metin Görselleştirme
        # Adım 1: Barplot görselleştirme işlemi
                  # a. "Review" değişkeninin içerdiği kelimeleri frekanslarını hesaplayınız, tf olarak kaydediniz
                  # b. tf dataframe'inin sütunlarını yeniden adlandırınız: "words", "tf" şeklinde
                  # c. "tf" değişkeninin değeri 500'den çok olanlara göre filtreleme işlemi yaparak barplot ile görselleştirme işlemini tamamlayınız.

       # Adım 2: WordCloud görselleştirme işlemi
                 # a. "Review" değişkeninin içerdiği tüm kelimeleri "text" isminde string olarak kaydediniz
                 # b. WordCloud kullanarak şablon şeklinizi belirleyip kaydediniz
                 # c. Kaydettiğiniz wordcloud'u ilk adımda oluşturduğunuz string ile generate ediniz.
                 # d. Görselleştirme adımlarını tamamlayınız. (figure, imshow, axis, show)

# Görev 3: Duygu Analizi
      # Adım 1: Python içerisindeki NLTK paketinde tanımlanmış olan SentimentIntensityAnalyzer nesnesini oluşturunuz

      # Adım 2: SentimentIntensityAnalyzer nesnesi ile polarite puanlarının incelenmesi
                # a. "Review" değişkeninin ilk 10 gözlemi için polarity_scores() hesaplayınız
                # b. İncelenen ilk 10 gözlem için compund skorlarına göre filtrelenerek tekrar gözlemleyiniz
                # c. 10 gözlem için compound skorları 0'dan büyükse "pos" değilse "neg" şeklinde güncelleyiniz
                # d. "Review" değişkenindeki tüm gözlemler için pos-neg atamasını yaparak yeni bir değişken olarak dataframe'e ekleyiniz

# NOT:SentimentIntensityAnalyzer ile yorumları etiketleyerek, yorum sınıflandırma makine öğrenmesi modeli için bağımlı değişken oluşturulmuş oldu.


# Görev 4: Makine öğrenmesine hazırlık!
        # Adım 1: Bağımlı ve bağımsız değişkenlerimizi belirleyerek datayı train test olara ayırınız.
        # Adım 2: Makine öğrenmesi modeline verileri verebilmemiz için temsil şekillerini sayısala çevirmemiz gerekmekte.
                  # a. TfidfVectorizer kullanarak bir nesne oluşturunuz.
                  # b. Daha önce ayırmış olduğumuz train datamızı kullanarak oluşturduğumuz nesneye fit ediniz.
                  # c. Oluşturmuş olduğumuz vektörü train ve test datalarına transform işlemini uygulayıp kaydediniz.

# Görev 5: Modelleme (Lojistik Regresyon)
    # Adım 1: Lojistik regresyon modelini kurarak train dataları ile fit ediniz.
    # Adım 2: Kurmuş olduğunuz model ile tahmin işlemleri gerçekleştiriniz.
        # a. Predict fonksiyonu ile test datasını tahmin ederek kaydediniz.
        # b. classification_report ile tahmin sonuçlarınızı raporlayıp gözlemleyiniz.
        # c. cross validation fonksiyonunu kullanarak ortalama accuracy değerini hesaplayınız
   # Adım 3: Veride bulunan yorumlardan ratgele seçerek modele sorulması.
        # a. sample fonksiyonu ile "Review" değişkeni içerisinden örneklem seçierek yeni bir değere atayınız
        # b. Elde ettiğiniz örneklemi modelin tahmin edebilmesi için CountVectorizer ile vektörleştiriniz.
        # c. Vektörleştirdiğiniz örneklemi fit ve transform işlemlerini yaparak kaydediniz.
        # d. Kurmuş olduğunuz modele örneklemi vererek tahmin sonucunu kaydediniz.
        # e. Örneklemi ve tahmin sonucunu ekrana yazdırınız.

# Görev 6: Modelleme (Random Forest)
        # Adım 1: Random Forest modeliiletahminsonuçlarınıngözlenmesi;
                 # a. RandomForestClassifier modelini kurup fit ediniz.
                 # b. cross validation fonksiyonunu kullanarak ortalama accuracy değerini hesaplayınız
                 # c. Lojistik regresyon modeli ile sonuçları karşılaştırınız.



############################################################################################################################

# =============================================================================
# KÜTÜPHANE İMPORTLARI
# =============================================================================

# Veri manipülasyonu ve DataFrame işlemleri için temel kütüphane
import pandas as pd

# Grafik ve görselleştirme kütüphanesi - çubuk grafik ve wordcloud gösterimi için
import matplotlib.pyplot as plt

# Kelime bulutu (word cloud) oluşturmak için kullanılan kütüphane
from wordcloud import WordCloud

# NLTK'nin İngilizce durma kelimeleri (stopwords) listesi - "the", "is", "at" gibi anlamsız kelimeler
from nltk.corpus import stopwords

# TextBlob kütüphanesi - Word sınıfı lemmatization için, TextBlob genel metin işleme için
from textblob import Word, TextBlob

# Scikit-learn model değerlendirme araçları - çapraz doğrulama ve veri bölme
from sklearn.model_selection import cross_val_score, train_test_split

# Metin vektörleştirme araçları - TF-IDF ve Count Vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# Rastgele Orman sınıflandırıcı - ensemble öğrenme yöntemi
from sklearn.ensemble import RandomForestClassifier

# Lojistik Regresyon sınıflandırıcı - temel ikili sınıflandırma algoritması
from sklearn.linear_model import LogisticRegression

# Sınıflandırma raporu - precision, recall, f1-score metrikleri
from sklearn.metrics import classification_report

# VADER duygu analizi aracı - sosyal medya metinleri için optimize edilmiş
from nltk.sentiment import SentimentIntensityAnalyzer

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

##############################################################
# TEXT PRE-PROCESSING
##############################################################
# Görev 1: Metin ön işleme işlemleri.
        # 1. amazon.xlsx datasını okutunuz.
        # 2. "Review" değişkeni üzerinde
            # a. Tüm harfleri küçük harfe çeviriniz
            # b. Noktalama işaretlerini çıkarınız
            # c. Yorumlarda bulunan sayısal ifadeleri çıkarınız
            # d. Bilgi içermeyen kelimeleri (stopwords) veriden çıkarınız
            # e. 1000'den az geçen kelimeleri veriden çıkarınız
            # f. Lemmatization işlemini uygulayınız

# Veri setini yükle - Kozmos Amazon ürün yorumları
# 19.2-Case_1 klasöründen amazon.xlsx dosyasını oku
df = pd.read_excel("amazon.xlsx")

# İlk 5 satırı görüntüle - veri yapısını anlamak için
df.head()

# Veri seti hakkında genel bilgi - sütun tipleri, eksik değerler, bellek kullanımı
df.info()


###############################
# Normalizing Case Folding
###############################
# Tüm metni küçük harfe çevir - "GREAT" ve "great" aynı kelime olarak değerlendirilsin
# str.lower() metodu ile tüm karakterler küçük harfe dönüştürülür
df['Review'] = df['Review'].str.lower()

###############################
# Punctuations
###############################
# Noktalama işaretlerini kaldır - "great!" -> "great"
# [^\w\s] regex kalıbı: kelime karakterleri (\w) ve boşluk (\s) HARİCİ her şeyi seç ve sil
# ^ köşeli parantez içinde "hariç" anlamına gelir
df['Review'] = df['Review'].str.replace('[^\w\s]', '', regex=True)

###############################
# Numbers
###############################
# Sayıları kaldır - "bought 3 items" -> "bought items"
# \d regex kalıbı: herhangi bir rakamı (0-9) temsil eder
df['Review'] = df['Review'].str.replace('\d', '', regex=True)

###############################
# Stopwords
###############################
# nltk.download('stopwords')
# İngilizce stopwords listesini al - "the", "is", "at", "which" gibi anlamsız kelimeler
sw = stopwords.words('english')

# Her yorumdan stopwords'leri filtrele
# Lambda fonksiyonu: metni kelimelere böl, stopwords'de olmayanları tut, tekrar birleştir
df['Review'] = df['Review'].apply(lambda x: " ".join(x for x in str(x).split() if x not in sw))

###############################
# Rarewords / Custom Words
###############################
# Nadir geçen kelimeleri bul - veri setinde en az geçen 1000 kelime
# Bu kelimeler genellikle yazım hataları veya anlamsız ifadelerdir
sil = pd.Series(' '.join(df['Review']).split()).value_counts()[-1000:]

# Nadir kelimeleri metinden çıkar - model karmaşıklığını azaltır
df['Review'] = df['Review'].apply(lambda x: " ".join(x for x in x.split() if x not in sil))


###############################
# Lemmatization
###############################
# Lemmatization: Kelimeleri sözlük formlarına (kök) dönüştürme
# Örnek: "running" -> "run", "better" -> "good", "cats" -> "cat"
# nltk.download('wordnet')

# Her kelimeyi lemmatize et - WordNet sözlüğü kullanılır
# Word(word).lemmatize() fonksiyonu kelimenin kök formunu döndürür
df['Review'] = df['Review'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

# Ön işlemeden geçmiş ilk 10 yorumu görüntüle - sonuçları kontrol et
df['Review'].head(10)



##############################################################
# # Görev 2: Metin Görselleştirme
##############################################################

###############################
# Barplot
###############################
# Adım 1: Barplot görselleştirme işlemi
        # a. "Review" değişkeninin içerdiği kelimeleri frekanslarını hesaplayınız, tf olarak kaydediniz
        # b. tf dataframe'inin sütunlarını yeniden adlandırınız: "words", "tf" şeklinde
        # c. "tf" değişkeninin değeri 500'den çok olanlara göre filtreleme işlemi yaparak barplot ile görselleştirme işlemini tamamlayınız.

# Terim frekanslarını hesapla (Term Frequency)
# Her yorumu kelimelere böl, frekansları say, tüm yorumlardaki frekansları topla
tf = df["Review"].apply(lambda x: pd.value_counts(x.split(" "))).sum(axis=0).reset_index()

# Sütun isimlerini düzenle - words: kelime, tf: terim frekansı (kaç kez geçtiği)
tf.columns = ["words", "tf"]

# 500'den fazla geçen kelimeleri filtrele ve çubuk grafik çiz
# Bu kelimelerin en önemli/sık kullanılan kelimeler olduğu varsayılır
tf[tf["tf"] > 500].plot.bar(x="words", y="tf")
plt.show()


###############################
# Wordcloud
###############################
# Görev 3: WordCloud görselleştirme işlemi
        # a. "Review" değişkeninin içerdiği tüm kelimeleri "text" isminde string olarak kaydediniz
        # b. WordCloud kullanarak şablon şeklinizi belirleyip kaydediniz
        # c. Kaydettiğiniz wordcloud'u ilk adımda oluşturduğunuz string ile generate ediniz.
        # d. Görselleştirme adımlarını tamamlayınız. (figure, imshow, axis, show)

# Tüm yorumları tek bir string olarak birleştir - WordCloud için gerekli
text = " ".join(i for i in df.Review)

# WordCloud nesnesi oluştur ve özelleştir
# max_font_size: en büyük kelimenin font boyutu
# max_words: gösterilecek maksimum kelime sayısı
# background_color: arka plan rengi
wordcloud = WordCloud(max_font_size=50,
                      max_words=100,
                      background_color="white").generate(text)

# Yeni bir figür oluştur
plt.figure()

# WordCloud görselini göster - bilinear interpolasyon ile yumuşak görüntü
plt.imshow(wordcloud, interpolation="bilinear")

# Eksenleri gizle - sadece kelime bulutu görünsün
plt.axis("off")

# Grafiği ekranda göster
plt.show()




##############################################################
# Görev 3: Duygu Analizi
##############################################################

# Adım 1: Python içerisindeki NLTK paketinde tanımlanmış olan SentimentIntensityAnalyzer nesnesini oluşturunuz
# VADER (Valence Aware Dictionary for Sentiment Reasoning) analizi
# Sosyal medya metinleri için optimize edilmiş, emoji ve büyük harfleri dikkate alır
sia = SentimentIntensityAnalyzer()

# Adım 2: SentimentIntensityAnalyzer nesnesi ile polarite puanlarının incelenmesi
                # a. "Review" değişkeninin ilk 10 gözlemi için polarity_scores() hesaplayınız
                # b. İncelenen ilk 10 gözlem için compund skorlarına göre filtrelenerek tekrar gözlemleyiniz
                # c. 10 gözlem için compound skorları 0'dan büyükse "pos" değilse "neg" şeklinde güncelleyiniz
                # d. "Review" değişkenindeki tüm gözlemler için pos-neg atamasını yaparak yeni bir değişken olarak dataframe'e ekleyiniz

# İlk 10 yorumun polarite skorlarını hesapla
# Çıktı: neg (negatif), neu (nötr), pos (pozitif), compound (bileşik skor) değerleri
df["Review"][0:10].apply(lambda x: sia.polarity_scores(x))

# Sadece compound skorlarını al - en önemli metrik (-1 ile +1 arası)
# compound > 0: pozitif, compound < 0: negatif, compound = 0: nötr
df["Review"][0:10].apply(lambda x: sia.polarity_scores(x)["compound"])

# Compound skoruna göre pos/neg etiket oluştur (ilk 10 gözlem için test)
# compound > 0 ise "pos", değilse "neg"
df["Review"][0:10].apply(lambda x: "pos" if sia.polarity_scores(x)["compound"] > 0 else "neg")

# Tüm yorumlar için Sentiment_Label sütunu oluştur
# Bu sütun makine öğrenmesi modelinin hedef (bağımlı) değişkeni olacak
df["Sentiment_Label"] = df["Review"].apply(lambda x: "pos" if sia.polarity_scores(x)["compound"] > 0 else "neg")

# Sentiment etiketlerine göre ortalama yıldız puanını kontrol et
# Pozitif etiketli yorumların yüksek yıldız, negatif etiketlilerin düşük yıldız vermesi beklenir
df.groupby("Sentiment_Label")["Star"].mean()

# NOT:SentimentIntensityAnalyzer ile yorumları etiketleyerek, yorum sınıflandırma makine öğrenmesi modeli için bağımlı değişken oluşturulmuş oldu.




###############################
# GÖREV 4: Makine öğrenmesine hazırlık!
###############################
# Adım 1: Bağımlı ve bağımsız değişkenlerimizi belirleyerek datayı train test olara ayırınız.

# Test-Train
# Veriyi eğitim (%75) ve test (%25) setlerine ayır
# random_state=42: Sonuçların tekrarlanabilir olması için sabit seed değeri
# train_x: Eğitim yorumları, test_x: Test yorumları
# train_y: Eğitim etiketleri, test_y: Test etiketleri
train_x, test_x, train_y, test_y = train_test_split(df["Review"],
                                                    df["Sentiment_Label"],
                                                    random_state=42)

# Adım 2: Makine öğrenmesi modeline verileri verebilmemiz için temsil şekillerini sayısala çevirmemiz gerekmekte.
           # a. TfidfVectorizer kullanarak bir nesne oluşturunuz.
           # b. Daha önce ayırmış olduğumuz train datamızı kullanarak oluşturduğumuz nesneye fit ediniz.
           # c. Oluşturmuş olduğumuz vektörü train ve test datalarına transform işlemini uygulayıp kaydediniz.

# TF-IDF Word Level
# TF-IDF: Term Frequency - Inverse Document Frequency
# Yaygın kelimelerin etkisini azaltır, nadir kelimelere ağırlık verir
# fit(train_x): Sadece eğitim verisiyle vocabulary oluştur (data leakage önleme)
tf_idf_word_vectorizer = TfidfVectorizer().fit(train_x)

# Eğitim ve test verilerini TF-IDF vektörlerine dönüştür
# transform: Metni sayısal sparse matrise çevirir
x_train_tf_idf_word = tf_idf_word_vectorizer.transform(train_x)
x_test_tf_idf_word = tf_idf_word_vectorizer.transform(test_x)



###############################
# Görev 5: Modelleme (Lojistik Regresyon)
###############################

# Adım 1: Lojistik regresyon modelini kurarak train dataları ile fit ediniz.
# Lojistik Regresyon: İkili sınıflandırma için temel algoritma
# fit(): Modeli eğitim verisiyle eğit - ağırlıkları öğren
log_model = LogisticRegression().fit(x_train_tf_idf_word, train_y)

# Adım 2: Kurmuş olduğunuz model ile tahmin işlemleri gerçekleştiriniz.
        # a. Predict fonksiyonu ile test datasını tahmin ederek kaydediniz.
        # b. classification_report ile tahmin sonuçlarınızı raporlayıp gözlemleyiniz.
        # c. cross validation fonksiyonunu kullanarak ortalama accuracy değerini hesaplayınız

# Test verisi üzerinde tahmin yap
# predict(): Her test örneği için "pos" veya "neg" tahmini döndürür
y_pred = log_model.predict(x_test_tf_idf_word)

# Sınıflandırma raporu - precision, recall, f1-score, support değerleri
# Precision: Pozitif tahminlerin doğruluk oranı
# Recall: Gerçek pozitiflerin yakalanma oranı
# F1-Score: Precision ve Recall'un harmonik ortalaması
print(classification_report(y_pred, test_y))

# 5-Fold Cross Validation ile model performansını değerlendir
# Veriyi 5 parçaya böler, her parçayı sırayla test seti olarak kullanır
# Ortalama accuracy değerini döndürür
cross_val_score(log_model, x_test_tf_idf_word, test_y, cv=5).mean()


# Adım 3: Veride bulunan yorumlardan ratgele seçerek modele sorulması.
        # a. sample fonksiyonu ile "Review" değişkeni içerisinden örneklem seçierek yeni bir değere atayınız
        # b. Elde ettiğiniz örneklemi modelin tahmin edebilmesi için CountVectorizer ile vektörleştiriniz.
        # c. Vektörleştirdiğiniz örneklemi fit ve transform işlemlerini yaparak kaydediniz.
        # d. Kurmuş olduğunuz modele örneklemi vererek tahmin sonucunu kaydediniz.
        # e. Örneklemi ve tahmin sonucunu ekrana yazdırınız.


# Rastgele bir yorum seç - modelin gerçek veriler üzerinde nasıl çalıştığını görmek için
random_review = pd.Series(df["Review"].sample(1).values)

# CountVectorizer ile yeni yorumu vektörleştir
# fit(train_x): Eğitim verisinin vocabulary'sini kullan
# transform(random_review): Yeni yorumu aynı formata dönüştür
yeni_yorum = CountVectorizer().fit(train_x).transform(random_review)

# Model ile tahmin yap - "pos" veya "neg"
pred = log_model.predict(yeni_yorum)

# Yorumu ve tahmin sonucunu ekrana yazdır
print(f'Review:  {random_review[0]} \n Prediction: {pred}')

###############################
# Görev 6: Modelleme (Random Forest)
###############################
# Adım 1: Random Forest modeliiletahminsonuçlarınıngözlenmesi;
         # a. RandomForestClassifier modelini kurup fit ediniz.
         # b. cross validation fonksiyonunu kullanarak ortalama accuracy değerini hesaplayınız
         # c. Lojistik regresyon modeli ile sonuçları karşılaştırınız.

# Random Forest modeli oluştur ve eğit
# Random Forest: Birden fazla karar ağacının birleşimi (Ensemble Learning)
# Her ağaç farklı alt örneklerle eğitilir, sonuçlar oylama ile birleştirilir
rf_model = RandomForestClassifier().fit(x_train_tf_idf_word, train_y)

# 5-Fold Cross Validation ile model performansını değerlendir
# n_jobs=-1: Tüm CPU çekirdeklerini kullan (paralel işlem)
# Lojistik Regresyon ile karşılaştırılabilir accuracy değeri
cross_val_score(rf_model, x_test_tf_idf_word, test_y, cv=5, n_jobs=-1).mean()

